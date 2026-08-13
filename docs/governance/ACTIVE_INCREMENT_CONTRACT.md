# InventorAI — Active Increment Contract

**Purpose:** the single, fixed location where the currently active phase/increment contract
is declared, plus the reusable contract template. Future agents discover the active contract
here (referenced from `CLAUDE.md` and `CURRENT_PROJECT_STATE.md`). Only one contract is
"active" at a time. When a new increment is authorized, replace the "Active contract"
section (append-only history is kept in the roadmap, not here).

---

## Declaration rule

- The **active contract** is whatever is recorded in the "Active contract" section below.
- An increment is authorized only by committed owner authorization; a contract here without
  such authorization is a template/placeholder, not an authorization.
- A contract governs bounded work at DEPTH 2/LEVEL 2 (and DEPTH 3/LEVEL 3 maintenance inside
  it). LEVEL 1 changes always need separate explicit owner authorization regardless of any
  contract.

## Reusable contract template

```
INCREMENT CONTRACT — <name>
Objective:                <what this increment achieves>
Owner authorization:      <reference to the committed owner authorization>
Risk level:               <LEVEL 1 | LEVEL 2 | LEVEL 3>
Allowed paths:            <exact paths that may change>
Forbidden paths:          <exact paths that must not change; default: engine/, web/, tests/,
                           domains/, database/, schemas/, prompts/, scripts/, CI, runtime/deploy,
                           main, accepted evidence>
Expected behavior:        <observable outcome>
Non-goals:                <explicitly out of scope>
Acceptance criteria:      <testable/verifiable gates>
Required tests:           <tests that must pass; or "none — documentation-only">
Tests not required:       <what is deliberately not tested>
Dependencies:             <prior gates, decisions, foundations>
Unresolved decisions:     <owner decisions still open, if any>
Stop conditions:          <when to stop and escalate>
Independent-review scope: <bounded reviewer questions per protocol §5>
Merge authority:          <who authorizes merge; default: owner, separately>
```

## Active contract
**Status (current — CF5-F001 BOUNDED CORRECTIVE IMPLEMENTATION CANDIDATE; CF5-F001 NOT closed; NO domain activated):** the
CF5-F001 corrective contract is **MERGED and post-merge verified** (PR #458 → authoritative tip
`b06ae40460dce987024fd224610554fdbbcaabc3`; merge tree == contract-candidate tree) and its bounded implementation was
executed fresh from that parent. Changed paths: `engine/safety_signal.py` (governed domain-keyed cue/context-family seam —
PARAMETERIZE; electronics family byte-preserved sole entry; domain-identity keying = NB-R4; additive
`has_governed_safety_cue_family`), `engine/deliverable_assembler.py` (bounded `_s15` truthful capability-scope statement,
electronics output byte-unchanged), `web/app.py` (bounded `_cold_load_entry` NB-R1 restoration from persisted
`confirmed_domain`), NEW `tests/test_cf5_f001_safety_signal_domain_seam.py` (13 tests), one load-bearing-proved D3-A pin
reconciliation. **Disclosed §4 narrowing (mechanically forced; reviewer attention):** identity restored on `domain_signal`
ONLY — `state.domain` is the committed P4-1b-2a non-resume guard anchor and restoring it re-enabled resume-answering
(caught by the governed restart-durability test); the narrowing is a strict subset, pinned in both directions.
`deliverable.html` untouched (existing surface sufficed). Evidence: RED r1–r4 on the clean parent (4 + 3 dependent fail;
5 pins pass); GREEN 13/13; mutations 7/7 CAUGHT (m1–m6 + m5b), bytes restored; differentials d1 = ZERO live-electronics
deltas, d2 = only NB-R1 corrections (resume blocked in both trees), d3 = 45/45 family-seam corrections, 0 unexplained;
full suite **2428 passed / 3 skipped / 1 xfailed / 0 failed** (baseline 2415/3/1 + 13). No dependency / pack / classifier /
activation / schema / Path-N / CAP-13 / D4 / D8 / ODR diff; WS2/Increment-6 frozen surfaces preserved. **IMPLEMENTATION
CANDIDATE ONLY — still requires Mandatory Grill → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → pre/post-merge verification; CF5-F001 NOT closed; first new-domain activation remains
BLOCKED.**

**Immediately prior (CF5-F001 corrective contract — MERGED via PR #458; retained as history):**
**Status (prior — CF5-F001 CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE; governance-only; implementation NOT started; NO
domain activated):** the CF5-F001 independent validation record is **MERGED and post-merge verified** (PR #457 → authoritative
tip `17ff20cd18267b71ed2ce615ae144d4e94729ab3`, SHA-preserving merge of accepted candidate `23eb12b5`; merge tree ==
candidate tree). This gate records the bounded **corrective implementation contract candidate**
(`docs/governance/CF5_F001_SAFETY_SIGNAL_CORRECTIVE_CONTRACT.md`): direction **PARAMETERIZE** (evidence-settled via the
merged D3-B pattern; electronics cue vocabulary byte-preserved as the sole family; seam keys on domain identity — NB-R4
disposition; no new Owner decision — the §8 policy question is settled by committed truthfulness authority, wording =
implementation detail; the family-before-activation question is an explicitly-preserved open P9-QS input); **NB-R1
dispositioned mechanically** (cold-load seam `web/app.py::_cold_load_entry` restores `domain`/`domain_signal` from the
already-persisted creation-validated `confirmed_domain`; legacy/NULL envelopes fail-safe unchanged; no schema/migration);
allowlist = `engine/safety_signal.py` + bounded `_cold_load_entry` + bounded `_s15` scope statement + focused tests
(+ template only if mechanically required); forbidden = second framework, pack schema/data, classifier/activation,
store schema, Path-N, CAP-13, D4/D8, ODR, de-electronicsifying cues. Evidence: GREEN A–F incl. electronics live
differential parity (d1 = ZERO deltas) and NB-R1 elimination; RED r1–r4 (STOP if irreproducible); mutations m1–m6 CAUGHT;
differentials d1–d3 with 0 unexplained; full suite green. Governance-only: ZERO runtime/test/Web/CLI/domain/activation/
schema/persistence/ODR diff this gate. **CONTRACT CANDIDATE ONLY — CF5-F001 NOT closed; implementation NOT authorized;
first new-domain activation remains BLOCKED.** Next required gate: **Mandatory Grill on this exact contract candidate**;
then independent external exact-candidate review → Owner acceptance → SHA-preserving publication → PR → pre/post-merge
verification; after authoritative, the bounded CF5-F001 implementation gate.

**Immediately prior (CF5-F001 independent validation — MERGED via PR #457; retained as history):**
**Status (prior — CF5-F001 INDEPENDENT VALIDATION RECORD CANDIDATE; governance-only; validation only, no remediation; NO
domain activated):** the completed CF5-F001 independent validation (genuinely separate session; verdict **ACCEPT WITH
NON-BLOCKING OBSERVATIONS**, NB-R1…NB-R4, blocking NONE) is recorded by a governance-only candidate on authoritative base
`2daf5c70d8fd86a3b63001fce675eeac252495ed` (PR #456 merge; 0 newer). Canonical record:
`docs/governance/CF5_F001_SAFETY_SIGNAL_INDEPENDENT_VALIDATION_RECORD.md`. **CF5-F001 = OPEN C — INDEPENDENTLY VALIDATED**:
residual shared-core electronics coupling in `engine/safety_signal.py` (`_MVP_DOMAIN`; electronics-gated
`_has_electrical_context`; shared-core electronics context/cue families; no per-domain seam; the `:272` missing-domain
fallback as a contract-time examination item); the corrected D3-A history is NOT reopened. No presently reachable
non-electronics manifestation (multi-domain defect latent Class C); **NB-R1** (presently reachable electronics-only
live-vs-cold-load detection divergence via the `:272` fallback) preserved as a MANDATORY corrective-contract disposition
item, not overturning Class C. Binding trigger (precision-corrected): before the first point a non-electronics-domain
session can be produced by a production surface and reach the safety-signal derivation — current enabler = activation-set
broadening; equivalent future enablers per NB-R2; registration alone and empty activation are NOT triggers (the trigger is
deliberately NOT `activated_domains() != ['electronics_electrical']`). Architecture selection OPEN (PARAMETERIZE = leading
candidate only; frozen in the later corrective-contract gate); backward compatibility = behavioral/differential electronics
parity + the WS2/Increment-6 frozen surfaces; NB-R3/NB-R4 preserved; CF-2 / CF-3(F004) / CF-6 / CAP-13 / Path-N / Domain
Packs / WS2 / anti-duplication fenced; FU-1 outside F001 (registered once, CF-5 lane); Owner re-disposition only via an
explicit governed, recorded Owner decision that cannot silently waive the pre-trigger blocker or CF-5 completion.
Governance-only: ZERO runtime / test / Web / CLI / domain / activation / schema / persistence / ODR diff. **Remediation NOT
required now; the bounded pre-trigger corrective prerequisite remains; first new-domain activation remains BLOCKED.** No
push / PR / merge / corrective contract / remediation / activation / D4 / D8 is authorized by this candidate. Next required
gate: **Mandatory Grill on this exact validation-record candidate**; after authoritative, the bounded CF5-F001 corrective
contract is the subsequent separately governed gate.

**Immediately prior (CF5-F002 formal closure — MERGED via PR #456; retained as history):**
**Status (prior — CF5-F002 FORMAL CLOSURE CANDIDATE; governance-only; CF-6 facets (i)–(iv) discharged; CF-6 / CF-2 / CF-5 NOT
closed; NO domain activated):** the CF5-F002/CF-6 bounded corrective implementation is **MERGED and post-merge verified** —
PR #455 → authoritative tip `9683f64b8467705f3bb1715c4b86b7a14a96f397`, a SHA-preserving two-parent merge of `2861f548` + the
Grill-passed, independently-reviewed (ACCEPT WITH NON-BLOCKING OBSERVATIONS), Owner-accepted exact candidate
`34103a2600200d0cc671510bd494739a107f929d`; merge tree `88aaba3a` == candidate tree; post-merge full suite 2415 passed / 3
skipped / 1 xfailed / 0 failed; boot OK; `activated_domains() == ['electronics_electrical']`. All contract §11 closure criteria
verified mechanically (see the roadmap CLOSURE entry) → **this candidate records CF5-F002 = FORMALLY CLOSED over the
authoritative runtime** (authoritative if/when this closure candidate is merged and post-merge verified). CF-6 facets (i)–(iv)
discharged; remaining CF-6 (general Web/CLI pre-classifier consistency beyond `/start`; legacy fixed-domain ILT-002 routes) and
CF-2 (all non-`/start`-flow public copy; localization of the generalized copy) remain OPEN and separately gated. Follow-ups
registered once: FU-1 empty-activation-branch defensive test (CF-5 lane); FU-2 human-quality/localized non-electronics labels
(CF-2/Arabic lane). Governance-only: ZERO runtime / test / Web / CLI / domain / activation / schema / persistence / ODR diff.
No push / PR / merge / activation / D4 / D8 / CF-6 / CF-2 / CF-5 closure is authorized by this candidate. Next required gate:
**Mandatory Grill on this exact closure candidate** → independent external exact-candidate review → Owner acceptance →
SHA-preserving publication → PR → pre/post-merge verification.

**Immediately prior (CF5-F002/CF-6 bounded corrective implementation — MERGED via PR #455; retained as history):**
**Status (prior — CF5-F002 / CF-6 BOUNDED CORRECTIVE IMPLEMENTATION CANDIDATE (amended contract §14); NO domain activated;
F002 / CF-6 / CF-2 / CF-5 NOT closed):** the bounded CF5-F002/CF-6 **implementation** was executed fresh from the authoritative
parent `2861f5488aac438648af5f2a06d113d0b1720858` (PR #454 made Amendment 01 authoritative; 0 newer) against the amended §14.1
allowlist and the §4 A–G + §14.2 U1–U5 acceptance matrix. Changed paths: `web/app.py` (activation-set-derived `/start` admission:
D1 confirm-classifier-selected-activated-domain with a bounded two-step presentation seam; D2 explicit choice among ONLY activated
domains on NONE + ≥2 activated; D3 no Electronics special case / no 500; activation-aware strong-unsupported vocabulary; truthful
activation-derived copy; §7 stale-comment hygiene), `web/templates/index.html` (generalized consent control + bounded D2 chooser;
NO separate `domain_choice.html` — minimum-path), NEW `tests/test_cf5_f002_web_admission_multidomain.py` (34 tests), and
mechanically-justified fail-closed-assertion adjustments to three existing Web-admission tie tests (message-identity → the
activation-derived truthful refusal seam; load-bearing fail-closed/no-session assertions unchanged). Evidence: RED r1–r6 fail on
the parent for the validated defect reasons (incl. the Electronics-absent 500) while all 17 electronics-only backward-compat pins
pass on the parent; GREEN 34/34; mutation probes m1–m12 (+ supplementary m11b) 13/13 CAUGHT, bytes sha256-restored; differential
sweep parent-vs-implementation 396 cases, all deltas categorized (100 unchanged incl. ALL 66 electronics-only cases; 31
activated-second-domain correction; 42 strong-unsupported activation-awareness; 215 messaging truthfulness; 8 Electronics-absent
graceful), 0 unexplained; full governed suite 2415 passed / 3 skipped / 1 xfailed / 0 failed; no dependency / engine / CLI /
domain / Registry / activation / schema / persistence / API / guardrail / ODR diff. CF-6 facets (i)–(iv) implemented at candidate
level; CF-6 / CF-2 NOT closed; residuals recorded in the roadmap entry. **IMPLEMENTATION CANDIDATE ONLY — still requires Mandatory
Grill on this exact candidate → independent external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving
publication → PR → pre/post-merge verification.** `activated_domains() == ['electronics_electrical']`; NO domain activated; first
new-domain activation remains BLOCKED; no push / PR / merge / activation / D4 / D8 / ODR change / closure is authorized by this
candidate.

**Immediately prior (CF5-F002/CF-6 Amendment 01 — AUTHORITATIVE via PR #454; retained as history):**
**Status (prior — CF5-F002 / CF-6 CORRECTIVE CONTRACT AMENDMENT 01 (scope re-scope) CANDIDATE; governance-only; implementation NOT
started; NO domain activated):** **`CF5-F002` / `CF-6` corrective contract is AMENDED (Amendment 01, §14)** on authoritative base
`0124ac336c654caaa6f89b44e3d55a947e6bb2c6` (PR #453 made the corrective contract authoritative; 0 newer). The prior implementation
gate correctly **STOPPED (§2)**: the `web/app.py`-only allowlist cannot implement a user-complete D1/D2 flow — `web/templates/
index.html:26` hardcodes `domain_confirm value="electronics_electrical"` (the sole consent control) and no D2 chooser exists.
Amendment 01 widens the production allowlist to the **minimum mechanically required** — `web/app.py` (incl. a bounded two-step
`/start` presentation seam if needed) + `web/templates/index.html` (dynamic consent control) + one bounded D2 domain-choice template
ONLY IF evidence requires + focused tests — and extends the acceptance matrix with **real rendered-UI GREEN** (U1 present
classifier-selected activated domain for confirmation; U2 NONE + ≥2 activated → present only activated domains for explicit
choice+confirm; U3 ratified NONE + exactly-one activated → explicit confirmation; U4 rendered backward-compat; U5 UI-language
independence) + mutation probes m11/m12. **D1/D2 and the ratified single-domain NONE case are PRESERVED EXACTLY** (policy unchanged;
only implementation scope + acceptance evidence widened). `OWNER_DECISION_REGISTER.md` UNCHANGED (D-CF5-F002-01 already authoritative;
no new Owner decision). Still forbidden: classifier/activation-policy/set change, domain activation, Domain-Pack change, D4, D8, broad
engine/CLI/unrelated-UI-framework work, schema/persistence change, implementation-gate ODR change. **AMENDMENT CANDIDATE ONLY —
CF5-F002 / CF-6 / CF-2 / CF-5 NOT closed; no domain activated; `activated_domains() == ['electronics_electrical']`; first new-domain
activation remains BLOCKED.** ZERO runtime/test/Web/CLI/domain/activation/ODR diff this gate. Next required gate: **Mandatory Grill of
this amendment candidate**; then, once authoritative, the CF5-F002/CF-6 implementation re-runs against the amended §14.1 allowlist +
§4/§14.2 matrix.

**Immediately prior (CF5-F002/CF-6 corrective implementation contract + D1/D2 — AUTHORITATIVE via PR #453; retained as history;
implementation gate STOPPED at §2, prompting Amendment 01 above):**
**Status (prior — CF5-F002 / CF-6 CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE + Owner decisions D1/D2 recorded; governance-only;
implementation NOT started; NO domain activated):** **`CF5-F002` / `CF-6` — Web `/start` multi-domain admission is DEFINED by a
bounded governance-only CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE** (record:
`docs/governance/CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md`) on authoritative base
`8d8dc1541568b7debedb51e094b15004964c333f` (PR #452 — CF5-F002 validation merge; 0 newer). CF5-F002 is VALIDATED **C** (present
defect NONE; exact trigger `activated_domains() != ['electronics_electrical']`). This gate **records Owner decisions D1/D2** in
`OWNER_DECISION_REGISTER.md` as **D-CF5-F002-01** — **D1** consent = "confirm classifier-selected activated domain" (no auto-admit;
persist classified+confirmed); **D2** `NONE` under >1 activated domain = "require explicit user choice" among activated domains (no
silent fallback), with `['electronics_electrical']` backward-compat preserved; **D3** Electronics-absent derives from the activation
set (no special case, no 500) — bounded consent/admission policy only (no multi-domain orchestration / activation / D4 / D8). The
contract fences the later implementation to `web/app.py` (`/start` admission) + a focused test, defines the full RED→GREEN matrix
(A electronics-only backward-compat; B elec+one-additional; C non-electronics-only; D 3+; E truthful messaging; F session-domain
integrity; G UI-language independence), the CF-6 shared-surface facets (strong-unsupported activation-awareness, no hidden
electronics admission, no AMBIGUOUS_TIE bypass — CF-6 NOT auto-closed), the co-triggered CF-2 messaging facet (CF-2 NOT closed),
bounded stale-comment hygiene (`SUBSTRINGS` + SINGLE/NONE-only), 10 mutation probes, and a 0-unexplained-delta differential sweep.
**Forbidden:** classifier semantic change, activation-set change, domain activation, Domain-Pack change, D4, D8, broad engine/CLI/UI
work. **CORRECTIVE CONTRACT CANDIDATE ONLY — CF5-F002 / CF-6 / CF-2 / CF-5 NOT closed; no domain activated;
`activated_domains() == ['electronics_electrical']`.** ZERO runtime/test/Web/CLI/domain/activation diff this gate (the only
production-relevant record is the D1/D2 ODR entry). Next required gate: **Mandatory Grill of this exact contract candidate**; then,
once authoritative, the bounded CF5-F002/CF-6 implementation.

**Immediately prior (CF5-F002 independent validation — AUTHORITATIVE via PR #452; retained as history):**
**Status (prior — CF5-F002 INDEPENDENT VALIDATION CANDIDATE; governance-only; VALIDATION ONLY — NO remediation authorized;
NO domain activated):** **`CF5-F002` — Web `/start` Electronics-Only Admission is INDEPENDENTLY VALIDATED by a governance-only
VALIDATION CANDIDATE** (record: `docs/governance/CF5_F002_WEB_START_ADMISSION_INDEPENDENT_VALIDATION_RECORD.md`) on
authoritative parent `e5f7d42c5a2c7ff6590816a87cd9f5ca3f650da0` (PR #451 made CF5-F003 formal closure AUTHORITATIVE; 0 newer),
per audit-contract §7 (validation separated from remediation). **Validated defect:** the `/start` admission surface hardcodes a
single-activated-domain (electronics-only) admission architecture — consent + admitted domain are the constant
`DOMAIN_CONFIRM_VALUE` (`web/app.py:837`, `:1420`); hardcoded `domain != "electronics_electrical"` branch + static
`CONFLICTING_SUPPORTED_DOMAINS` (`:1391`, `:845`); static strong-unsupported vocabulary encoding registered domains' signals as
permanently unsupported (`:897-919`; CF-6/NB-4); "electronics and electrical ideas only" public copy (CF-2). **Classification
C RETAINED ON EVIDENCE** (real production `/start` probes, isolated DB + self-restoring activation doubles, session cleanup
PASS): today every probed outcome is correct and truthful (activated-electronics admission; NONE fallback under explicit
confirmation; recognized-but-not-activated refused; real AMBIGUOUS_TIE production-unreachable; UI-language independent);
under an elec+mech double the surface fails four ways — activation state has zero effect on outcomes; activated-domain signals
refused as "unsupported"; **`a hinge that you plug in` → SINGLE(mechanical) [ACTIVATED] yet ADMITTED as an
`electronics_electrical` session (cross-domain mislabeling)**; no consent path for any second domain. **Trigger (narrowed):**
first moment `activated_domains() != ['electronics_electrical']` (extensionally = second-specialist-domain activation today);
NOT registration, NOT recognition. **CF-6:** partly owned; single "CF5-F002 / CF-6 Web-admission lane" validated; no duplicate
framework. **CF-2:** separate, co-triggered; no message defect reachable today. **Stale `SUBSTRINGS` comment
(`web/app.py:870-884`):** partly stale, comment-only, zero runtime consequence, owner F002/CF-6 lane CONFIRMED, NOT edited.
**Remediation required NOW: NO; pre-trigger corrective gate: YES (binding C obligation before any activation gate changes the
activation set); Owner multi-domain consent/admission UX policy required at that future gate, NONE now.**
**CF5-F003 remains CLOSED; CF5-F001 / CF5-F004 remain OPEN C; CF-5 remains OPEN; first new-domain activation remains
BLOCKED.** `OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/schema/web/CLI/guardrail diff;
`activated_domains() == ['electronics_electrical']`. **VALIDATION CANDIDATE ONLY — remediation NOT authorized; corrective
contract NOT created.** Next required gate: **Mandatory Grill on this exact validation candidate.**

**Immediately prior (CF5-F003 formal closure — retained as history):**
**Status (prior — CF5-F003 FORMALLY CLOSED; governance-only closure sync; NO domain activated):** **`CF5-F003` — Classifier
Matching Semantics is FORMALLY CLOSED.** The VALIDATED **D** defect (raw-substring classifier false positives) is corrected in the
AUTHORITATIVE runtime: `engine/domain_rules.py::classify_domain` performs deterministic whole-token matching (`[a-z0-9]+`; exact /
bounded `+s` / `+es`), contiguous multi-word phrase matching (bounded plural on the final token only), and at-most-once /
set-membership same-domain registered containment preservation fired on any authorized container base form (plural-container aware),
with no cross-domain leakage and no non-registered-word credit. **Authoritative implementation merge PR #450 → tip
`0563843445c55ab1d3b5dcf2bd1e995d131b419f`** (two-parent create-a-merge-commit of `107d2eb` + exact Grill-passed implementation
candidate `6cd1fbbf532a57c4b7fa40ea7732d85ea3469273`; **merge/authoritative tree `5d3f0a40bf422f570848e050e1664a4d8616b14e` ==
implementation-candidate tree** — post-merge content byte-identical to the accepted candidate; 0 newer). Evidence of record: 8 RED
(false positives + real Web `/start` + real CLI) RED-before/GREEN-after; GREEN preservation (singular+plural, multi-word/punctuation,
containment singular + plural-container, cross-domain non-leakage, at-most-once parity, genuinely executed 0/1/2/3+ activation + Web
session cleanup, Web/CLI parity); **full regression `2381 passed / 3 skipped / 1 xfailed / 0 failed`**; 8 mutation probes all caught
(bytecode-isolated, bytes restored); adversarial differential sweep 281 inputs / 20 categorized deltas / **0 unexplained**; Mandatory
Grill PASS; Independent External Review ACCEPT WITH NON-BLOCKING OBSERVATIONS; exact Owner acceptance; SHA-preserving publication; PR
#450; post-merge verification PASS. `activated_domains() == ['electronics_electrical']` (no activation change); P9-E2 tie/fallback
semantics and `DomainClassification` unchanged. **Non-blocking carry-forward (registered once in the roadmap; NOT F003 obligations):**
(NMF-1) phrase-contiguity mutation-coverage gap — runtime is CORRECT (`delivery drug`→NONE, `machines learning`→NONE), only the
committed mutation suite lacks reorder/intermediate-pluralization negatives → bounded TEST-HARDENING follow-up; (stale `SUBSTRINGS`
comment in `web/app.py::_admit_specialist_domain`) — Web runtime intentionally zero-diff → bounded DOCUMENTATION/COMMENT-HYGIENE
follow-up in the CF5-F002 / CF-6 Web-admission lane. The pre-existing `iot_electronics` schema/load warning is UNRELATED to F003 and
keeps its existing owner. **CF5-F001 / CF5-F002 / CF5-F004 remain OPEN C; CF-5 remains OPEN (F003 closure does NOT close CF-5); first
new-domain activation remains BLOCKED.** Rejected evidence preserved immutable: `a29789a9` (impl — containment-loss tie flips),
`0f48df20` (amendment — double-count), `5ebc927d` (amendment — plural-container gap + over-broad invariant). This closure gate is
**governance-only**: ZERO runtime / test / domain / Web / CLI / `OWNER_DECISION_REGISTER.md` diff.

**Immediately prior (CF5-F003 implementation candidate — now AUTHORITATIVE via PR #450 `0563843`; retained as history):**
**Status (prior — CF5-F003 IMPLEMENTATION CANDIDATE (base contract v2 + Amendment 01); RED→GREEN; NOT merged; CF5-F003 NOT
closed; NO domain activated):** **`CF5-F003` — Classifier Matching Semantics is IMPLEMENTED by a bounded IMPLEMENTATION CANDIDATE**
on authoritative base `107d2eb08e9cdf14dade12a46693cf5dd2dd1533` (live tip; two-parent merge of `cfdc58cc` + Amendment 01 candidate
`c26f676c`; merge tree `fcc00cd5` == Amendment 01 tree; 0 newer). The bounded runtime change replaces the raw-substring scoring in
`engine/domain_rules.py::classify_domain` with deterministic **whole-token** matching over `[a-z0-9]+` tokens (exact / bounded
`+s` / `+es`), **contiguous multi-word** phrase matching (bounded plural on the final token only), and **same-domain registered
containment preservation** credited **AT-MOST-ONCE / set-membership** and fired when the container is present via **any authorized
base form (incl. its bounded plural — plural-container aware, Amendment 01 §A3/§A3a)**; **no cross-domain containment leakage**; no
credit inside a non-registered word. New module-level `_TOKEN_RE` + `_single_word_matches` / `_phrase_matches` /
`_present_signal_count`; `import re` added. **Tie policy (0→fallback / 1→SINGLE / ≥2→AMBIGUOUS_TIE), the non-activated priority
fallback list, `DomainClassification` semantics, the P9-E2-R fail-loud `infer_domain` wrapper, and D3-D precedence are UNCHANGED.**
**RED→GREEN evidence:** NEW `tests/test_cf5_f003_classifier_matching_semantics.py` (74 tests) — 8 RED (false positives
`controlled`/`compiled`/`knowledge`→`led`, `patriotic`→`iot`, `concurrent`→`current`, `hearth`→`heart`; a real Web `/start`
guidance-bypass; a real CLI incorrect-confirmation) fail on the pre-fix parent `107d2eb` and pass after the fix; GREEN preservation
(singular+plural, multi-word/punctuation, containment singular + **plural-container**, cross-domain non-leakage `biosensor`/
`biosensors`→medical, **at-most-once parity** singular+plural, genuinely-executed **0/1/2/3+** activation with Web session cleanup,
Web/CLI parity). **Full regression:** `pytest -q` = **2381 passed / 3 skipped / 1 xfailed / 0 failed** (= 2307 parent baseline + 74
new; no existing-test regression; no deleted test; no new skip/xfail). **Mutation suite (8, all CAUGHT RED, bytecode-isolated, bytes
restored):** substring-restore; `+s` removal; `+es` removal; punctuation regression; containment removal; cross-domain/non-registered
containment leak; non-idempotent double-count; exact-token-only container (plural-container M1). **Adversarial differential sweep:**
281-input corpus, 20 parent-vs-candidate deltas ALL categorized (F003 false-positive/accepted-compound-loss; cross-domain-leakage
correction; authorized phrase/tokenization expansion), **0 UNEXPLAINED**. **Scope:** `engine/domain_rules.py` (matching/scoring only)
+ the new focused test + this governance current-truth sync. **ZERO diff:** `web/app.py`, `scripts/run_cli.py`,
`engine/safety_signal.py`, `engine/domain_activation.py`, Domain Registry, Domain-Pack signal data, tie policy, fallback priority,
`ARCHITECTURE_GUARDRAILS.md`, `OWNER_DECISION_REGISTER.md`, schemas, persistence, API. `activated_domains() ==
['electronics_electrical']`; NO activation change. **IMPLEMENTATION CANDIDATE ONLY — CF5-F003 NOT closed** (closure is a later gate
after independent review → Owner acceptance → merge → post-merge verification). CF5-F001 / CF5-F002 / CF5-F004 remain UNCHANGED open
C; CF-5 remains OPEN; first new-domain activation remains BLOCKED. Next required gate: **Mandatory Grill of this exact implementation
candidate.**

**Immediately prior (CF5-F003 Amendment 01 CONTRACT candidate — now AUTHORITATIVE via PR #449, merge `107d2eb`; retained as
history):**
**Status (prior — CF5-F003 CONTRACT AMENDMENT 01 CANDIDATE; governance-only; implementation NOT started; NO domain activated):**
**`CF5-F003` Amendment 01 — Same-Domain Containment Preservation is DEFINED by a governance-only CONTRACT AMENDMENT CANDIDATE**
(record: `docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT_AMENDMENT_01.md`) on authoritative base
`cfdc58cc798d02b8d9f50030b627a8302e0de889` (PR #448 made the corrected CF5-F003 corrective contract v2 AUTHORITATIVE; 0 newer). The
CF5-F003 implementation candidate `a29789a948829133812d1a80b297e9b5b907cdc1` (whole-token + bounded plural; Creator Grill PASS WITH
NON-BLOCKING HARDENING) was **REJECTED by Independent External Review — MATERIAL CORRECTION REQUIRED**, blocking finding
**CONTAINMENT-LOSS TIE FLIPS** (`an implantable sensor`: medical → electronics because whole-token drops the `implant`⊂`implantable`
same-domain reinforcement, ties electronics, and activated precedence flips it; likewise `application`+sensor → electronics via
`app`⊂`application`). `a29789a9` is immutable rejected evidence (NOT published/merged/reused; not an ancestor of this amendment).
The blocking finding is a **contract-level** gap; this amendment corrects the CONTRACT. **Complete containment inventory (5 pairs):**
SAME-domain `implant`⊂`implantable`(med) + `app`⊂`application`(soft) [regressions → preserve], `monitoring`⊂`patient_monitoring`
[neutral]; CROSS-domain `sensor`⊂`biosensor` [improvement — biosensor now correctly medical; do NOT restore], `neural`⊂
`neural network` [neutral]; the full graph was re-enumerated mechanically (exactly 5 pairs; no new relation after plural/phrase
normalization; no chained containment; no signal in >1 container). **Amended semantics — Design A (bounded same-domain
registered-signal containment preservation, AT-MOST-ONCE, plural-container aware):** retain the base whole-token + `+s`/`+es` rule
PLUS — when a registered container signal `Y` of domain `D` is present via ANY authorized base form (`Y` matched by the base rule:
exact `Y` / `Y+"s"` / `Y+"es"` for single-word, or a multi-word `Y`'s authorized token sequence), also credit same-domain registered
single-word signals `X` with `X` substring of `Y`; nothing else, counted as a set UNION (at most once). Verified this gate: restores
`an implantable sensor` → medical and `application`+sensor → software AND their plural-container forms (`applications with a sensor` →
software; `implantables in a sensor` → medical); does NOT restore arbitrary substrings (container must be a REGISTERED signal, so
controlled/knowledge/ecosystem stay false) or cross-domain containment (`biosensor`/`biosensors` stay medical). **P9-E2 tie policy,
priority fallback, `DomainClassification` semantics, D3-D UNCHANGED; no Domain-Pack edit.** Designs A–E evaluated; A recommended
(minimal, technical, domain-neutral, N-domain). The containment credit is **AT-MOST-ONCE / set-membership** (a signal already matched
as a standalone base token is NOT credited again). **Containment-credit invariant (M2 — narrow, replaces the withdrawn global
claim):** a signal's containment contribution is set-based/at-most-once, cannot duplicate a base contribution, cannot be cross-domain,
cannot arise from a non-registered container, and cannot exceed the single boolean contribution the same signal could have supplied
via parent substring matching. **The over-broad global claim "a domain's Design-A score never exceeds parent on any input" is FALSE
and WITHDRAWN** — authorized phrase/tokenization recognition (e.g. `clinical_trial` in `clinical trial`, `drug delivery` in
`drug-delivery`) legitimately produces new matches, so the COMPLETE classifier score may exceed parent; only the containment
contribution is bounded. **Two earlier drafts REJECTED:** `0f48df20` (unqualified score increment → A3-OVER-CREDIT / CONTAINMENT
DOUBLE-COUNT) and `5ebc927d` (EXACT-token-only container trigger → **M1 plural-container containment loss** `applications with a
sensor` → electronics; and **M2 over-broad global invariant**), both immutable rejected evidence, neither an ancestor. This candidate
triggers containment on any authorized container base form (incl. bounded plural) and states only the narrow invariant. The
underscore-signal reviewer observation (`clinical_trial`/`patient_monitoring` "unmatchable") was mechanically **DISPROVED** (same
tokenizer applies to signal and input → matched); contract NOT modified to accommodate it. **Owner-policy: NONE required** (technical
preservation; no new routing policy) → `OWNER_DECISION_REGISTER.md` UNCHANGED. Strengthened evidence required of the future
implementation: singular- AND plural-container GREEN cases + at-most-once parity cases (singular and plural: `an implant that is
implantable in a sensor circuit` / `implants implantables sensors circuits` → electronics, medical 2 not 3); original REDs preserved;
genuinely executed 0/1/2/3+ activation coverage + Web session cleanup; mutation probes for same-domain-containment removal /
cross-domain over-broadening / non-registered-word containment / non-idempotent double-count / **exact-token-only container match
(plural-container loss)**. **CF5-F003 = VALIDATED D / OPEN; impl `a29789a9` REJECTED (containment tie flips); amendment drafts
`0f48df20` REJECTED (double-count) and `5ebc927d` REJECTED (plural-container gap + over-broad invariant); CF5-F001 / CF5-F002 /
CF5-F004 remain UNCHANGED open C; CF-5 remains OPEN.** ZERO runtime/test/domain/schema/web/CLI/guardrail diff; `activated_domains() ==
['electronics_electrical']`; NO domain selected; first new-domain activation remains BLOCKED. **This amendment = AMENDMENT CANDIDATE
ONLY; implementation NOT started.** This exact candidate has passed the Creator Mandatory Grill; the next required gate is
**independent external exact-candidate review**; any material finding rejects it as-is (NEW SHA/tree/bundle — no in-place amendment).

**Immediately prior (CF5-F003 corrected corrective contract — retained as history; v2 merged AUTHORITATIVE via PR #448 `cfdc58cc`;
its whole-token-only rule superseded by Amendment 01 above after the implementation `a29789a9` was independently REJECTED):**
**Status (prior — CF5-F003 CORRECTED CORRECTIVE CONTRACT CANDIDATE; governance-only; implementation NOT started; NO active
runtime increment; NO domain activated):** **`CF5-F003` — Classifier Matching Semantics corrective gate is DEFINED by a corrected
governance-only CORRECTIVE CONTRACT CANDIDATE** (record: `docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT.md`)
on authoritative base `8c38812086cfd3c17bc61ad47bba94e8b7a9de8d` (PR #447 made the CF-5 Audit contract AUTHORITATIVE; 0 newer). The
CF-5 Audit (Execution Gate 1) ran read-only and produced four material findings (CF5-F001 shared-core electronics-specific
`safety_signal`; CF5-F002 Web `/start` electronics-only admission / CF-6; CF5-F003 classifier substring false positives; CF5-F004
hardcoded non-activated priority fallback / CF-3). **CF5-F003 was independently validated D — Material current issue, reachable
now** (`signal in text` substring scoring matches short signals inside unrelated words: `controlled`→`led`, `compiled`→`led`,
`patriotic`→`iot`, `concurrent`→`current`, `hearth`→`heart`; effects: incorrect classification, untruthful CLI confirmation, Web
`/start` bypass/admission). **The first CF5-F003 corrective contract candidate `9857ba3e21a8bbd8d73bcde83cb85b7744d0f85b` was
REJECTED by Mandatory Grill (BF-1: its strict exact-whole-token / no-plural-inference rule would regress ~76 signals' plural forms
and flip `a system of gears and levers` Mechanical→Software).** This corrected candidate replaces the rejected rule with a
**bounded plural-preserving whole-token matcher**: tokenize on `[a-z0-9]+`; a single-word signal matches a token equal to the
signal or its bounded plural `+"s"`/`+"es"` (nothing else — no stemming/fuzzy/substring/`+ies`); multi-word signals match a
contiguous whole-token sequence (bounded plural on the final token only). Collision guard validated (false positives stay false —
whole-token, not substring); plural inventory reproduced (76 single-word + 5 multi-word signals; only `diagnosis` sibilant, its
irregular plural not caught today → no obligation; no cross-pack `+s`/`+es` collision). Required GREEN preservation is MANDATORY and
explicitly repairs BF-1 (`LEDs`/`sensors`/`circuits`/`resistors`/`PCBs`; `gears`/`levers`; `catheters`; `apps`/`databases`/`APIs`;
`a system of gears and levers` stays Mechanical), plus RED (real Web/CLI reproductions) and mutation probes (incl. over-broad plural
rule → RED). **It implements NOTHING** and is scoped to `engine/domain_rules.py` matching only. **Forbidden:** Web admission redesign
(F002/CF-6), safety-signal redesign (F001), fallback-priority redesign (F004), activation, D4, D8, Domain-Pack signal-data edits.
Preservation: canonical `classify_domain` sole owner (Web/CLI consumers, no duplicate matcher); `DomainClassification` semantics;
P9-E2-R fail-loud wrapper; P9-E2 tie policy; D3-D precedence; recognized-not-activated; no new MULTI producer; no activation change.
**CF5-F003 = VALIDATED D / corrective gate OPEN; prior `9857ba3e` = REJECTED (BF-1); CF5-F001 / CF5-F002 / CF5-F004 remain UNCHANGED
open C; CF-5 remains OPEN.** **`OWNER_DECISION_REGISTER.md` UNCHANGED** (bounded technical matching rule; no new Owner
product-policy decision — D3/P9-QS/P9-E1/CF-5 precedent). ZERO runtime/test/domain/schema/web/CLI/guardrail diff;
`activated_domains() == ['electronics_electrical']`; NO domain selected; first new-domain activation remains BLOCKED. **CF5-F003
corrected corrective contract = CANDIDATE ONLY; IMPLEMENTATION NOT STARTED.** The next required gate is the **Mandatory Grill on this
exact immutable corrected CF5-F003 contract candidate**; any material Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/
independent review — no amendment).

**Immediately prior (CF-5 Audit contract/entry candidate — retained as history; merged AUTHORITATIVE via PR #447 `8c38812`; CF-5
Audit subsequently executed (Gate 1) producing CF5-F001..F004; superseded as CURRENT status by the corrected CF5-F003 corrective
contract candidate above):**
**Status (prior — CF-5 AUDIT CONTRACT/ENTRY CANDIDATE; governance-only; Audit NOT executed; NO active runtime increment; NO
domain activated):** **`CF-5` — Retrospective Adversarial Architecture Audit is DEFINED by a governance-only CONTRACT / ENTRY
CANDIDATE** (record: `docs/governance/CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_CONTRACT.md`) on authoritative base
`54a5565bdcdfa37ff247ceb9e806bd5b2b42cb9d` (PR #446 made P9-E2 formal closure AUTHORITATIVE; 0 newer). CF-5 was registered
(P9-E2-R closure §5, re-affirmed P9-E2 closure §7) and is MANDATORY before first new-domain activation; it is **generic to
inherited architecture and requires no selected domain to enter.** The candidate defines Audit entry, minimum scope (shared-core;
Registry; activation; classifier ownership; scoring/signals; hardcoded fallback (CF-3); Web strong-unsupported (CF-6);
public-message truthfulness (CF-2); Web/CLI/core consistency; persistence; domain isolation; schema/version; extensibility; hidden
Electronics assumptions; test architecture; reachable-on-activation debt), the **preserved A/B/C/D/E finding taxonomy** (no new
taxonomy), the **independent-validation requirement for C/D/E before reopening closed architecture**, the correction-gate policy
(C → pre-trigger prerequisite; D → bounded corrective gate; E → STOP for architecture/Owner decision), and Audit completion
criteria. **It does NOT execute the Audit, produce findings, or select/qualify/activate any domain.** Separation preserved (none
discharged): P9-QS AUTHORITATIVE (per-domain qualification separate, selection-first); CF-6 PENDING PRE-SECOND-SPECIALIST-DOMAIN
ACTIVATION; CF-2 / CF-3 separate trigger-bound; D8 Owner-reserved; D4 separate. Recommended partial-order: CF-5 → domain selection
→ per-domain P9-QS → CF-6/CF-2/CF-3 → explicit Owner activation authorization. **`OWNER_DECISION_REGISTER.md` UNCHANGED** (contract
candidate records no new accepted Owner product-policy decision — D3/P9-QS/P9-E1 precedent). ZERO runtime/test/domain/Registry/
activation/web/CLI/schema/guardrail diff; `activated_domains() == ['electronics_electrical']`; NO domain selected. **CF-5 =
CONTRACT/ENTRY CANDIDATE ONLY — Audit NOT executed; execution NOT yet authorized; the candidate does not claim the Audit is ACTIVE/
COMPLETE/PASSED.** The next required gate is the **Mandatory Grill on this exact immutable CF-5 contract candidate**; any material
Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (P9-E2 formal-closure candidate — retained as history; merged AUTHORITATIVE via PR #446 `54a5565`; P9-E2 now
FORMALLY CLOSED / AUTHORITATIVE; superseded as CURRENT status by the CF-5 contract candidate above):**
**`P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence (bounded tie-precedence runtime
gate) is FORMALLY CLOSED / SATISFIED as a governance-only CLOSURE CANDIDATE** (record:
`docs/governance/P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_FORMAL_CLOSURE_RECORD.md`). Authoritative implementation parent
`f33663710d6edf506a082b1bfa2f02e9c3fef7ac` (PR #445; parent 1 `c11482db…` + parent 2 accepted candidate `85fda813…`; merge tree
`0bffe3f7…` == candidate tree; 0 newer). **This is a governance-only closure candidate — NOT yet authoritative and P9-E2 is NOT yet
formally closed; closure becomes authoritative only after: Mandatory Grill → independent external exact-candidate review → Owner
exact-candidate acceptance → SHA-preserving publication → PR → pre-merge verification → CREATE A MERGE COMMIT → post-merge
verification.** Implementation lineage: contract PR #441 (`47fce397`; candidate `1d29a26f`); rejected candidate `3255c4ba` (Grill
FAIL — never published/accepted/merged; not an ancestor) → accepted corrected candidate `85fda813` (built from `c11482d`) → Grill
**PASS WITH NON-BLOCKING HARDENING** (blocking NONE) → independent review **ACCEPT WITH NON-BLOCKING OBSERVATIONS** (blocking NONE)
→ Owner-accepted → published → PR #445 (5 files / +546 / −17; `git diff --check` CLEAN) → post-merge verified. **Bounded
tie-precedence policy via the canonical `classify_domain` seam (CF-1 SATISFIED):** `len(activated_tied) == 0` → non-activated
priority fallback retained unchanged; `== 1` → `SINGLE`; **`>= 2` → `AMBIGUOUS_TIE(selected=None, complete canonical activated tied
set, reason=EQUAL_SCORE)`** — no arbitrary/alphabetical/registration/dict winner, no Electronics preference, no LLM; `MULTI_DOMAIN_
NEEDS_D4` NOT fabricated (D4 separate); only ACTIVATED domains (D3-D). Fresh closure evidence reproduced at `f336637`: full suite
**2307 passed / 3 skipped / 1 xfailed / 0 failed**; focused **57 passed**; **nine load-bearing mutation probes all CAUGHT RED**,
bytes restored. Canonical-owner reconciliation: `classify_domain` = canonical owner, `infer_domain` = legacy fail-loud wrapper
(later authoritative P9-E2-R architecture governs the name evolution; the old P9-E2 contract is NOT rewritten/amended). **Carry-forward
(not erased):** CF-1 SATISFIED by this gate's subject; CF-2 shared AMBIGUOUS/MULTI public message PENDING; CF-3 non-activated
priority fallback PENDING (retained for backward compatibility; before first Nth-domain registration/activation); CF-4 D4 separate;
CF-5 Retrospective Adversarial Architecture Audit PENDING (MANDATORY before first new-domain activation); CF-6 Web
pre-classifier/strong-unsupported reachability & admission interaction PENDING (PRE-SECOND-SPECIALIST-DOMAIN ACTIVATION; distinct
from CF-2). Non-blocking observations NB-1…NB-5 carried forward (not discarded). **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is
NO active runtime increment.** **NO new domain activated; NO domain selected; P9-E2-R remains FORMALLY CLOSED / SATISFIED; P9-E1
remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT
EXECUTED; deployment / production = NOT AUTHORIZED.** The next required gate is the **Mandatory Grill on this exact immutable closure
candidate**; any material Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (P9-E2 implementation candidate — retained as history; merged AUTHORITATIVE via PR #445 `f336637`; superseded as
CURRENT status by the P9-E2 formal-closure candidate above):**
**`P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence — was IMPLEMENTED as a CORRECTED IMPLEMENTATION CANDIDATE**
built fresh from authoritative parent `c11482db7240b5ac628e77cd061f8d5de6df40ee` (live tip re-verified; 0 newer). It **supersedes the
REJECTED prior candidate `3255c4ba1ca6ae50e0c3f20d7f0d4c8ef1fa223c`** (Mandatory Grill `GRILL FAIL — MATERIAL CONTRACT CORRECTION
REQUIRED`: sound runtime, but a FALSE `/start` strong-unsupported "masked for all real ties" reachability claim, an omitted
achievable distinguishing RED-E2-10, and a misdescribed multi-activation `/start` delta); `3255c4ba` remains immutable rejected
evidence and is NOT reused/amended/rebased/built upon. **Bounded runtime change (via the canonical `classify_domain` seam, CF-1):**
`len(activated_tied) == 0` → unchanged priority fallback; `== 1` → `SINGLE`; **`>= 2` → `AMBIGUOUS_TIE(selected_domain=None,
candidates=canonical activated tied set, reason=EQUAL_SCORE)`** — no arbitrary/alphabetical/registration/dict winner, no Electronics
preference, no LLM, `MULTI_DOMAIN_NEEDS_D4` NOT manufactured (D4 separate). Only ACTIVATED domains form the set (D3-D).
**CORRECTED reachability truth:** `/start` calls `classify_domain` FIRST and fails an `AMBIGUOUS_TIE` closed to `UNSUPPORTED`
(200, no session) BEFORE the separate `_has_strong_unsupported_evidence` gate; that gate is an independent later layer over
SINGLE/NONE inputs only, so a multi-activated tie fails closed via the ambiguity branch regardless of strong-unsupported token
membership (verified: `strong("circuit and hinge") == strong("hinge and app") == False`). **RED→GREEN:** NEW
`tests/test_p9e2_multi_activated_tie_precedence.py` (20 tests) — 12 distinguishing RED on parent (E2-1..9, **E2-10 a REAL `/start`
production-path RED**: `circuit and hinge` under an elec+mech double → parent ADMITS an electronics session (302), candidate fails
closed 200 UNSUPPORTED; **E2-10b** `hinge and app` mech+sw → parent GUIDANCE, candidate UNSUPPORTED; **E2-11** `gear and catheter`
mech+med → CLI bounded stop) + 8 honest GREEN GUARDS. **9 load-bearing mutation probes all CAUGHT RED** (incl. NEW probe 9:
neutralize the real `/start` AMBIGUOUS branch → E2-10/10b RED; probe 7: detach Web AMBIGUOUS/MULTI dispatch → P9-E2-R R2/R10 RED),
bytecode-isolated, bytes restored. **Full suite 2307 passed / 3 skipped / 1 xfailed / 0 failed** (= 2287 parent + 20). **Scope:**
`engine/domain_rules.py` (tie branch + corrected docstring) + the NEW test + governance current-truth (roadmap + this file +
`CURRENT_PROJECT_STATE.md`); **`web/app.py` ZERO diff** (runtime found safe; correction is evidence/governance + stronger tests);
ZERO diff `scripts/run_cli.py`, `engine/domain_activation.py`, `ARCHITECTURE_GUARDRAILS.md`, `OWNER_DECISION_REGISTER.md`,
`domains/**`, `schemas/**`, `database/**`. **Backward-compat (truthful):** current activation is electronics-only so ≥2 activated
tie is production-unreachable → ZERO current production delta; under a FUTURE governed second-domain activation, non-intercepted
ties change OLD incidental-SINGLE/possible-single-domain-admission → NEW AMBIGUOUS_TIE/fail-closed — an INTENDED future correction,
not a regression; `/start` is NOT universally "unchanged" under future multi-activation. **Carry-forwards:** CF-2 (public-message
truthfulness) retained; CF-3 (Nth-domain priority/fallback) retained; CF-5 (Retrospective Adversarial Architecture Audit) remains a
future pre-activation obligation; **NEW CF-6 — Web pre-classifier / strong-unsupported reachability & admission interaction
(distinct from CF-2), a FUTURE PRE-SECOND-DOMAIN-ACTIVATION obligation, NOT executed here.** **`OWNER_DECISION_REGISTER.md`
UNCHANGED.** **P9-E2 = CORRECTED IMPLEMENTATION CANDIDATE ONLY — NOT closed / NOT authoritative; NO domain activated; NO domain
selected; MULTI_DOMAIN_NEEDS_D4 NOT manufactured; D4 SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 NOT AUTHORIZED; PSRR NOT
EXECUTED; deployment/production NOT AUTHORIZED.** The next required gate is a **NEW Mandatory Grill on this exact new candidate**;
any material Grill finding rejects it as-is (NEW SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (P9-E2-R closure candidate — retained as history; superseded as CURRENT status by the P9-E2 implementation
candidate above; P9-E2-R closure evidence itself unchanged):** **`P9-E2-R` — Ambiguity / Multi-Domain Result Representation (bounded representation sub-gate)
is FORMALLY CLOSED / SATISFIED as a governance-only CLOSURE CANDIDATE** (record:
`docs/governance/P9_E2_R_AMBIGUITY_MULTI_DOMAIN_RESULT_REPRESENTATION_FORMAL_CLOSURE_RECORD.md`; authoritative pre-closure parent
`b42a3e6c246b98d425460f80d91d8de12d554039`, PR #443). **This is a governance-only closure candidate — it is NOT yet authoritative
and P9-E2-R is NOT yet formally closed; closure becomes authoritative only after: Mandatory Grill → independent external
exact-candidate review → Owner exact-candidate acceptance → SHA-preserving publication → PR → pre-merge verification → CREATE A
MERGE COMMIT → post-merge verification.** Implementation lineage: contract PR #442 (`3434c235`; candidate `3cbb16b6`) +
implementation PR #443 (`b42a3e6`; candidate `813bc5aa`; merge tree `35a58482` == candidate tree; diffstat 11 files / +725 / −48;
`git diff --check` CLEAN). **P9-E2-R established the representation seam only — it DID NOT implement the P9-E2 tie policy**
(`classify_domain` constructs SINGLE/NONE only; AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4 representable/consumable but classifier-
produced only via the separate later P9-E2 runtime; `sorted(activated_tied)[0]` + priority fallback unchanged; no multi-domain
analysis). Fresh closure evidence reproduced at `b42a3e6`: full suite **2287 passed / 3 skipped / 1 xfailed / 0 failed**; focused
`test_p9e2r_result_representation.py` + `test_architecture_guardrails.py` **37 passed**; **six load-bearing mutation probes all
CAUGHT RED** (wrapper fail-loud; `/start` AMBIGUOUS; `/start` MULTI; defensive activation boundary; canonical order;
migrated-monkeypatch detachment), bytes restored. Closed acceptance behavior re-verified: one classifier owner; legacy wrapper
total over SINGLE/NONE + fail-loud over richer kinds; Web/CLI dispatch by kind; `state.domain` a resolved string; defensive
activation type boundary; canonical order ≠ precedence; no new framework / duplicate owner; `activated_domains() ==
['electronics_electrical']`. Phase-9 completeness checklist: no acceptance-relevant APPLICABLE/GAP. **Carry-forward (not erased):**
CF-1 P9-E2 runtime tie policy still pending; CF-2 shared AMBIGUOUS/MULTI public message NON-BLOCKING, carried to P9-E2; CF-3
non-activated priority fallback (`engine/domain_rules.py` line 142) — no reachable defect today, MANDATORY before first Nth-domain
registration/activation; CF-4 D4 separate owner for actual composition; **CF-5 Retrospective Adversarial Architecture Audit now
REGISTERED as a future PRE-ACTIVATION obligation (A/B/C/D/E classification; material C/D/E dispositioned/independently validated
BEFORE first new-domain activation) — NOT executed here.** **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is NO active runtime
increment.** **NO new domain activated; NO domain selected; P9-E2 tie precedence remains a separate later runtime gate; P9-E1
remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 =
NOT AUTHORIZED; PSRR = REGISTERED / NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next required gate is the
**Mandatory Grill on this exact immutable closure candidate**; any material Grill finding rejects this candidate as-is (NEW
SHA/tree/bundle/Grill/independent review — no amendment).

**Immediately prior (retained as history — P9-E2-R IMPLEMENTATION CANDIDATE; merged AUTHORITATIVE via PR #443 `b42a3e6`):**
**`P9-E2-R` — Ambiguity / Multi-Domain Result Representation is now IMPLEMENTED as an IMPLEMENTATION CANDIDATE** on authoritative
base `3434c2350b4c08cabcc362d175947a311070b493` (PR #442 made the corrected P9-E2-R contract AUTHORITATIVE). Minimum-sufficient
representation seam (NO tie-policy change): `engine/domain_rules.py` gains `DomainResultKind {SINGLE, NONE, AMBIGUOUS_TIE,
MULTI_DOMAIN_NEEDS_D4}`, deterministic `DomainAmbiguityReason`, `AmbiguousDomainResultError`, and an immutable frozen
`DomainClassification` with all invariants enforced at construction (registry-valid SINGLE + empty candidates; NONE empty; tie/multi
no-winner + ≥2 unique registry-recognized canonical-sorted candidates + deterministic reason; AMBIGUOUS_TIE all-activated (D3-D);
mutual exclusion; canonical order ≠ precedence). Canonical `classify_domain(...)` is the single classifier owner (today SINGLE/NONE
only — behavior-equivalent, no tie detection); legacy `infer_domain(...) -> str | None` is a thin wrapper, **total over SINGLE/NONE
and FAIL-LOUD (`AmbiguousDomainResultError`) over richer kinds**. `web/app.py` `/start` and `scripts/run_cli.py` migrated to
**dispatch by `result.kind`** (never truthiness/string comparison of the object): SINGLE byte-identical, NONE unchanged,
AMBIGUOUS_TIE + MULTI_DOMAIN_NEEDS_D4 **fail closed** via an existing safe surface (no session/no electronics admission/no winner/no
D4/no new UX/no implied multi-domain analysis); `state.domain` remains a resolved string. `engine/domain_activation._resolve_pack_id`
gains a **defensive fail-loud `TypeError`** for non-string domain ids (a `DomainClassification` can never be silently swallowed;
None/empty preserved). `ARCHITECTURE_GUARDRAILS.md` §9 reconciled (classify_domain = richer canonical entry; infer_domain
legacy/fail-loud; new admission callers must use classify_domain; one owner) with deliberate guardrail tests; the frozen `str |
None` signature test is NOT weakened. **RED→GREEN** via new `tests/test_p9e2r_result_representation.py` (19) + 4 guardrail tests
(RED-R1…R11 + invariant/immutability/mutual-exclusion/duplicate/deterministic-reason/defensive-boundary), all GREEN; activated ties
simulated with self-restoring `_ACTIVATED_DOMAINS` doubles (NO real activation). **Six load-bearing mutation probes** all caught RED
(wrapper fail-loud; `/start` AMBIGUOUS; `/start` MULTI; defensive boundary; canonical-order; **migrated-monkeypatch detachment** —
the six `web.app.infer_domain` monkeypatches were migrated to `web.app.classify_domain` and proven still load-bearing), byte-restored.
**Fresh full suite: 2287 passed / 3 skipped / 1 xfailed / 0 failed** (2264 baseline + 23 new). **Scope:** the 8 runtime/test/guardrail
paths + governance current-truth registration (roadmap + this file + `CURRENT_PROJECT_STATE.md`, per D3 implementation precedent);
**`OWNER_DECISION_REGISTER.md` UNCHANGED**; no persistence/schema/public-API/export/Domain-Pack change; no P9-E2 tie-policy change;
`activated_domains() == ['electronics_electrical']`. Phase-9 completeness checklist: no acceptance-relevant APPLICABLE/GAP. **P9-E2-R
= IMPLEMENTATION CANDIDATE ONLY — NOT closed** (formal closure, if precedent requires, is a separate gate after independent review →
Owner acceptance → merge → post-merge verification); **NO new domain activated; NO domain selected; P9-E2 tie precedence remains a
separate later runtime gate; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase
8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is:
independent review of this exact implementation candidate → Owner acceptance → merge → post-merge verification → (if precedent
requires) a separate P9-E2-R formal-closure gate.

**Immediately prior (retained as history — P9-E2-R CONTRACT CANDIDATE, corrected; merged AUTHORITATIVE via PR #442 `3434c23`):**
**`P9-E2-R` — Ambiguity / Multi-Domain Result Representation (bounded sub-gate) is DEFINED by a CORRECTED
governance-only CONTRACT CANDIDATE** (record: `docs/governance/P9_E2_R_AMBIGUITY_MULTI_DOMAIN_RESULT_REPRESENTATION_CONTRACT.md`;
authoritative base `47fce397dfd21175a0012b652f8dde6548e31432`). It is the corrected reissue that **supersedes the Grill-REJECTED
prior candidate `1b817f06e7d86b3af6e44b298bcf7a31102e5e32`** (which remains **immutable historical evidence only — NOT amended /
NOT merged / NOT reused**); a NEW independent candidate from the current authoritative parent, incorporating all MATERIAL Mandatory
Grill findings. **Contract-first only — no runtime/test change, no domain activation, no domain selection.** Corrections applied
(contract §22 ledger): legacy `infer_domain` wrapper **FAILS LOUD** (raises a dedicated bounded exception, never silent
`None`/arbitrary domain) on AMBIGUOUS_TIE/MULTI_DOMAIN_NEEDS_D4, total over SINGLE/NONE (§4) + **RED-R9**; **all six
`web.app.infer_domain` monkeypatch surfaces migrated + proven load-bearing** (§7.3); **architecture-guardrail reconciliation** of
the frozen `str | None` vs fail-loud richer kinds (§4.1); `classify_domain` richer canonical entry, one classifier owner (§3);
**web + CLI dispatch by `result.kind`** (never truthiness/string comparison of the object) (§7) + **RED-R10** (`/start × MULTI`) +
**RED-R11** (CLI bounded stop); **`state.domain` remains a resolved string** (§10); strengthened invariants (unique ids, ≥2
candidates, all-activated, mutual exclusion, duplicate rejection, immutable) (§11); **deterministic non-LLM `reason`** (§12);
**defensive fail-loud type boundary** vs silent `DomainClassification` swallowing (§19); **line-34 future Nth-domain fallthrough
hazard registered** as a mandatory pre-Nth-domain obligation (§21); future implementation **classified architecture-affecting /
higher-governance** (§22); D4 marker-only, no-analysis-implied wording (§16/§18). **Confirmed gap (verified at `47fce39`):**
`infer_domain -> str | None` conflates the truths and `web/app.py /start` admits `domain is None` as an electronics session
(lines 1393–1394); guardrail freezes the `str | None` signature; activated tie unreachable today (only electronics activated).
**Architecture (retained, minimum-sufficient):** `DomainResultKind {SINGLE, NONE, AMBIGUOUS_TIE, MULTI_DOMAIN_NEEDS_D4}` +
immutable `DomainClassification` + canonical `classify_domain(...)` + legacy fail-loud `infer_domain` wrapper; no new
framework/router/registry/activation-engine/schema. RED-R1…R11 + additional invariant/mutation/monkeypatch-load-bearing/
type-boundary tests designed (not implemented). Phase-9 completeness checklist fully dispositioned (no acceptance-relevant
APPLICABLE/GAP). **Governance-only scope:** the new contract doc + append-only roadmap entry + this current-truth sync +
`CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/domain/web/CLI/schema/prompt/benchmark
diff.** **P9-E2-R = CONTRACT CANDIDATE ONLY — authoritative only if this exact accepted candidate is merged and post-merge
verified; the P9-E2-R runtime + tests are a separate later architecture-affecting gate, NOT authorized here; the Grill-rejected
`1b817f06` remains immutable historical evidence only; NO new domain activated (`activated_domains() == ['electronics_electrical']`);
NO domain selected; P9-E2 tie precedence remains a separate later runtime gate; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 =
SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED;
deployment / production = NOT AUTHORIZED.** The next state is: independent review of this exact corrected contract candidate →
Owner acceptance → merge → post-merge verification → a separate P9-E2-R implementation gate.

**Immediately prior (retained as history — P9-E2 CONTRACT CANDIDATE, definition only; merged AUTHORITATIVE via PR #441
`47fce39`):** **`P9-E2` / `P9-PREREQ-B` — Multi-Activated Domain Tie/Conflict Precedence is DEFINED by a governance-only CONTRACT
CANDIDATE**
(record: `docs/governance/P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_CONTRACT.md`; authoritative base
`05184f9166fa3a9e45a3384be5bafccc86e05ebe` — PR #440 made the P9-E1 formal closure AUTHORITATIVE). This is the mandatory
D3-registered prerequisite **P9-PREREQ-B** carried by the authoritative P9-QS §16; **contract-first only — no runtime/test change,
no domain activation, no domain selection.** **Live evidence (verified at `05184f91`): still required** —
`engine/domain_rules.py::infer_domain` lines 31–33 pick `sorted(activated_tied)[0]` (incidental alphabetical precedence among
ACTIVATED tied domains; plus the line-34 `priority` literal for the no-activated-tie fallback); reachable only when ≥2 specialist
domains are activated and tie. Behaviorally proven read-only (monkeypatched `_ACTIVATED_DOMAINS`, restored; no real activation): a
clean `mechanical`+`medical_device` activated tie returns `mechanical` purely alphabetically. **Critical representation finding:**
`infer_domain` returns `str | None`, which cannot honestly express an ambiguous tie / tied candidate set / no-governed-winner /
genuine multi-domain (Case 4) — so the contract explicitly calls out a bounded, **separately-reviewed representation sub-gate
`P9-E2-R`** rather than hiding it. Precedence policy: Case 1 (single winner) unchanged; Case 3 (tie, no governed precedence) →
explicit ambiguous/unresolved outcome (safe default, no silent pick); Case 4 → surface D4 need truthfully; forbidden answers =
alphabetical/file/registration/iteration/dict order, hardcoded Electronics preference, model guess, silent default. RED-1…RED-6
designed (not implemented); Phase-9 completeness checklist fully dispositioned (no APPLICABLE/GAP). **First-new-domain implication
(verified): Electronics is already activated, so the first new-domain activation creates a >1-activated state — P9-E2 is a
MANDATORY prerequisite before the first actual new-domain activation.** **Governance-only scope:** the new contract doc +
append-only roadmap entry + this current-truth sync + `CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO
runtime/test/domain/schema/prompt/benchmark/web diff.** **P9-E2 = CONTRACT CANDIDATE ONLY — authoritative only if this exact
accepted candidate is merged and post-merge verified; the P9-E2 runtime, the P9-E2-R representation sub-gate, and their tests are
separate later gates, NOT authorized here; NO new domain activated (`activated_domains() == ['electronics_electrical']`); NO domain
selected; P9-E1 remains FORMALLY CLOSED / SATISFIED; D4 = SEPARATE / UNEXECUTED; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY
CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is: independent
review of this exact contract candidate → Owner acceptance → merge → post-merge verification → a separate P9-E2 (+ P9-E2-R)
implementation gate.

**Immediately prior (retained as history — P9-E1 FORMALLY CLOSED / SATISFIED / AUTHORITATIVE via PR #440 `05184f91`):** **`P9-E1` /
`P9-PREREQ-A` — Path-N Production Caller Domain Propagation is FORMALLY CLOSED / SATISFIED** as a governance-only CLOSURE CANDIDATE
(prerequisite closure only; authoritative if/when merged; dedicated record
`docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_FORMAL_CLOSURE_RECORD.md`; authoritative base
`f22085066d8a0b2b1e90c04c6808f44f606316e6`, PR #439). Implementation lineage: contract PR #438 (`8fbc239`; candidate `3b485131`) +
implementation PR #439 (`f220850`; candidate `8ebc1c1a`; merge tree `14c286ba` == candidate tree; diffstat 5 files / +251 / −5;
`git diff --check` CLEAN; independent review ACCEPT WITH NON-BLOCKING OBSERVATIONS). Live-verified at `f220850`:
`support_state("mechanical") == "recognized_not_activated"`; `activated_domains() == ['electronics_electrical']`; a foreign
recognized-not-activated domain on the Path-N flow no longer receives the Electronics artifact text (`get_question`) nor the
Electronics `_STALL_REFRAME` at exhaustion (`get_display_question`); Electronics + `domain=None` behavior intact; exactly the
three production `get_path_n_question(...)` sites threaded, no hidden caller. RED→GREEN (RED parent `8fbc239`: RED-1 foreign
artifact text + RED-2 foreign stall reframe → all 6 GREEN); independently reproduced mutation matrix (site 1 alone → RED; site 2
alone → GREEN; site 3 alone → GREEN; sites 2+3 jointly → RED; all 3 → RED — **sites 2+3 jointly, not individually, load-bearing;
recorded honestly**); fresh full suite **2264 passed / 3 skipped / 1 xfailed / 0 failed** (2258 baseline + 6 new). Phase-9
completeness checklist for P9-E1: no APPLICABLE/GAP remains (truthfulness / no-shared-core-coupling / Nth-domain extensibility /
end-to-end reasoning = PASS; knowledge-quality = NOT APPLICABLE; qualification / composition / materials / calculations /
knowledge-sources = DEFERRED to their governed gates). **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is NO active increment.**
**P9-E1 / P9-PREREQ-A = FORMALLY CLOSED / SATISFIED / AUTHORITATIVE (prerequisite closure only); NO new domain activated; NO
domain selected; Electronics remains the only activated specialist domain; recognition ≠ activation; P9-E2 / P9-PREREQ-B =
SEPARATE / UNSATISFIED / NOT STARTED (`sorted(activated_tied)[0]` untouched); D4 = SEPARATE / UNEXECUTED; D8 = OPEN /
Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT
AUTHORIZED.** The recommended next major gate is **P9-E2 / P9-PREREQ-B — Multi-Activated Domain Tie/Conflict Precedence**
(separately governed; NOT started; closing P9-E1 does NOT auto-advance to it or authorize any activation).

**Immediately prior (retained as history — P9-E1 IMPLEMENTATION CANDIDATE; merged AUTHORITATIVE via PR #439 `f220850`):**
**The `P9-E1` / `P9-PREREQ-A` — Path-N Production Caller Domain Propagation is now IMPLEMENTED as an IMPLEMENTATION
CANDIDATE** on authoritative base `8fbc239c98ab89e596554a8c52c7e7b1c5b22ad5` (PR #438 made the P9-E1 contract AUTHORITATIVE). The
bounded runtime fix threads the canonical `domain` (already the first parameter of both callers) into the existing three
`get_path_n_question(...)` calls in `engine/progression_loop.py` as `domain=domain` — (1) `get_question` (path=="N") selection,
(2) `get_display_question` exhaustion `current` read, (3) `get_display_question` exhaustion `previous` read; no signature change,
**`engine/path_n_questions.py` unchanged**, no domain branching, no second router, no activation-policy/Registry/Domain-Pack/D8/
P9-E2 change. **RED→GREEN** via the new behavioral `tests/test_p9e1_path_n_caller_domain_propagation.py` (6 tests): baseline RED-1
(`get_question` foreign recognized domain served Electronics artifact text) + RED-2 (`get_display_question` foreign domain served
the Electronics `_STALL_REFRAME`) both FAILED pre-edit and are GREEN post-edit; guards preserve Electronics artifact text, the
Electronics stall reframe, the `domain=None` seam default, and assert the fixture `mechanical` is `recognized_not_activated` /
not-activated. **Per-site proof (honest):** site-1 mutation is individually caught; sites 2+3 are *jointly* load-bearing (either
domain-aware reframe read alone suppresses the erroneous foreign reframe — defense-in-depth), and the joint site-2+3 mutation (the
original defect) is caught by RED-2; both threaded for a domain-consistent comparison per contract §3; no probe left in the
candidate. **Full suite fresh: 2264 passed / 3 skipped / 1 xfailed / 0 failed** (2258 baseline + 6 new). **Scope:**
`engine/progression_loop.py` + the new test + governance current-truth registration (this file + roadmap append +
`CURRENT_PROJECT_STATE.md`, per D3 implementation precedent); **`OWNER_DECISION_REGISTER.md` UNCHANGED;
`activated_domains() == ['electronics_electrical']`.** **P9-E1 = IMPLEMENTATION CANDIDATE ONLY — NOT closed** (formal closure is a
separate gate after independent review → Owner acceptance → merge (create-a-merge-commit) → post-merge verification); **NO new
domain activated; NO domain selected; P9-E2 NOT implemented; D4 NOT executed; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY
CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is: independent
review of this exact candidate → Owner acceptance → merge → post-merge verification → a separate bounded P9-E1 formal-closure gate.

**Immediately prior (retained as history — P9-E1 CONTRACT CANDIDATE, definition only; merged AUTHORITATIVE via PR #438 `8fbc239`):**
**The `P9-E1` / `P9-PREREQ-A` — Path-N Production Caller Domain Propagation implementation is DEFINED by a
governance-only CONTRACT CANDIDATE** (record: `docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_CONTRACT.md`; authoritative
base `f08dd2e0319b2777c47dad9cdb49c05d106bc7a0` — PR #437 made P9-QS AUTHORITATIVE). This is the mandatory D3-registered
prerequisite **P9-PREREQ-A** now carried by the authoritative P9-QS §16; the Owner authorization **begins Phase 9 only at this
bounded contract gate.** **Live evidence (verified at `f08dd2e`): the prerequisite is STILL REQUIRED** — the Path-N seam is
already domain-aware (`engine/path_n_questions.py`), but the production callers in `engine/progression_loop.py` drop the in-scope
`domain` at three `get_path_n_question(...)` sites (line 232 in `get_question`; lines 269 and 273–274 in `get_display_question`),
so `get_question("mechanical", "MECHANISM_COMPLETENESS", 0, path="N")` returns the Electronics artifact text (domain-blind) while
the seam already yields `None` for `"mechanical"`. Canonical domain identity is available at every caller (`web/app.py:1566`,
`engine/progression_loop.py:904/944/981`, `scripts/run_cli.py:79` all pass `state.domain`); those three seam calls are the
complete production-caller set. **Bounded implementation (LATER, separate gate — NOT executed here):** thread `domain=domain` into
those three sites only; no signature/seam/registry/activation/web/CLI change; Electronics/`None` behavior and stall reframe
preserved exactly, correctly suppressed for a recognized-not-activated foreign domain. **RED design:** behavioral tests with the
neutral fixture `"mechanical"` on gap `MECHANISM_COMPLETENESS` (RED on baseline → GREEN after propagation) plus Electronics
GREEN-guards; not implemented in this gate. **Governance-only scope:** the new contract doc + append-only roadmap entry + this
current-truth sync + `CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/schema/prompt/
benchmark/web/CI diff.** **P9-E1 = IMPLEMENTATION CONTRACT CANDIDATE ONLY — authoritative only if this exact accepted candidate is
merged (create-a-merge-commit) and post-merge verified; the P9-E1 runtime + tests are a separate later gate, NOT authorized here;
NO new domain activated (`activated_domains() == ['electronics_electrical']`); NO domain selected; P9-E2 NOT implemented; D4 NOT
executed; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment /
production = NOT AUTHORIZED.** Owner product/policy decisions required before P9-E1 acceptance: NONE — only independent review →
Owner acceptance → merge → post-merge verification, then a separate P9-E1 implementation gate. The next state is: P9-E1 contract
reviewed; if accepted+merged, a separate P9-E1 implementation gate performs the bounded propagation with RED→GREEN tests.

**Immediately prior (retained as history — P9-QS AUTHORITATIVE / merged PR #437 `f08dd2e`):**
**The `P9-QS` — Phase-9 Technical Quality Standard is DEFINED by a CORRECTED governance-only CONTRACT CANDIDATE** (record:
`docs/governance/P9_QS_PHASE_9_TECHNICAL_QUALITY_STANDARD_CONTRACT.md`; authoritative base
`99c08555351e031bd3cc11f536cf558c91dc0c32`). It is the corrected reissue that **supersedes the REJECTED prior candidate
`6a3e25df79bfe2399474a1ecf9154ca3ccfbe307`** (which remains **historical rejected evidence only — NOT modified / NOT merged /
NOT reused**); this is a NEW independent candidate from the current authoritative parent, not an amendment of the rejected SHA.
Corrections applied: **B1** — the future deterministic-calculation capability is assigned **no CAP number** (an unnumbered
*future deterministic-calculation adapter gate*); `CAP-06` is repository-canonical for the *Multi-Axis Invention Readiness
Dashboard* and MUST NOT be reused for it. **B2** — the **Output-Language override capability is DEFERRED / NOT IMPLEMENTED / NOT
AUTHORIZED / separately governed (D-P6-17 is the accepted decision, not the capability) and is NOT a pre-new-domain activation
prerequisite**; the actual repository-authoritative pre-new-domain prerequisite is the separate **Domain Registry validation
hardening (D-P6-14 / §5-I1, already CLOSED)**. Non-blocking O1 (audit/addendum/sweep = session-level review/development inputs,
not committed repository authority), O2 (`P9-PREREQ-A/B` are convenient labels for the already-D3-registered obligations, not
pre-existing canonical identifiers), and O3 (§4b references the existing **D13 knowledge-governance / evidence-governance /
licensing** family, reference/reuse only) also addressed. The standard expresses the Domain Capability Contract **through** the
canonical Domain Registry (§5-I1; no second registry), preserves the activation-quality principle, and keeps every deferred item
(deterministic-calculation adapter, Units, CAP-12/CAP-13/WS-PFV, D4, D8, Output-Language) as REFERENCE-ONLY / DEFERRED.
**Governance-only scope:** the new contract doc + append-only roadmap entry + this current-truth sync +
`CURRENT_PROJECT_STATE.md`; **`OWNER_DECISION_REGISTER.md` UNCHANGED; ZERO runtime/test/schema/prompt/benchmark/web/CI diff.**
**P9-QS = CONTRACT CANDIDATE ONLY — it becomes the authoritative contract-of-record only if this exact accepted candidate is
merged (create-a-merge-commit) and post-merge verified; there is NO active implementation increment; NO domain activated; the
future deterministic-calculation capability remains UNNUMBERED / DEFERRED; Output-Language remains separately governed / DEFERRED
and NOT an activation prerequisite; D8 = OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 9 = INACTIVE / NOT AUTHORIZED
(accepting this standard does NOT open a Phase-9 implementation contract); Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED;
deployment / production = NOT AUTHORIZED.** Owner product/policy decisions required before P9-QS acceptance: NONE — only
independent review → Owner acceptance → merge → post-merge verification. The next state is: P9-QS reviewed; Phase 9 remains
inactive pending separate Owner authorization plus the Phase-9 entry gates (and, for a second/non-electronics domain, the
P9-PREREQ-A/B prerequisites and the already-CLOSED Domain Registry hardening D-P6-14 / §5-I1).

**Immediately prior (retained as history — D3 FORMALLY CLOSED):** **`D3` — Pre-Phase-9 Core Domain-Neutrality is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE
(prerequisite closure only; authoritative if/when merged; dedicated record
`docs/governance/D3_CORE_DOMAIN_NEUTRALITY_FORMAL_CLOSURE_RECORD.md`; base `e51eaf7eee001ef6012579852c8da7cbeda8e144`, PR #435).
Contract PR #434 (`2dbde37`) + implementation PR #435 (`e51eaf7`; merge tree = accepted candidate tree `f027c93`, post-merge
verified; independent review ACCEPT WITH NON-BLOCKING OBSERVATIONS). D3-A/B/D live-verified; D3 focused 7 / full suite 2258
passed / 3 skipped / 1 xfailed / 0 failed. Canonical owners consumed not duplicated (domain_registry §5-I1 + domain_activation
§5-I2); D3-C not reopened; D8 untouched / Owner-reserved; `activated_domains() == ['electronics_electrical']` (only). **Three
mandatory future prerequisites REGISTERED (not authorized here):** Path-N caller propagation (before any second / non-electronics
domain activation); multi-activated tie precedence (before more than one specialist domain is activated); Phase-9 Capability
Overlap & Preservation Audit (before the first Phase-9 activation contract). **`OWNER_DECISION_REGISTER.md` UNCHANGED. There is
NO active implementation increment.** **D3 = FORMALLY CLOSED / AUTHORITATIVE (prerequisite closure only); Phase 8 = FORMALLY
CLOSED; Phase 9 = INACTIVE / NOT AUTHORIZED (D3 closure does NOT auto-open a Phase-9 contract or activate any domain); D8 = OPEN
/ Owner-reserved; Phase 10 = NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** The next state is:
D3 prerequisite formally closed; Phase 9 remains inactive pending separate Owner authorization and the Phase-9 entry/audit
gates.

**Immediately prior (retained as history — D3 IMPLEMENTATION CANDIDATE):** The accepted **D3
contract is MERGED (PR #434, merge `2dbde37a3c409356691a17fd868f90b087df417c`; merge tree = accepted candidate tree, post-merge
verified)**, and **`D3` — Core Domain-Neutrality is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED →
GREEN)**: minimum-path corrections to exactly three existing engine seams + one new focused test — **D3-A**
`engine/safety_signal.py` (`domain_context` reflects the actual §5-I2 session domain, no longer force-mapped to the electronics
MVP for a non-electronics context; electronics safety cues unchanged); **D3-B** `engine/path_n_questions.py` (`get_served_question`
/ `get_path_n_question` honor an optional canonical `domain` identity; Electronics-owned artifact served only for Electronics /
`None`; a non-electronics identity is not silently served Electronics content); **D3-D** `engine/domain_rules.py` (`infer_domain`
consumes §5-I2 activation so an ACTIVATED domain wins a tie and a RECOGNIZED_NOT_ACTIVATED domain never becomes routing/admission
authority). Canonical owners consumed, never duplicated (`domain_registry.py` §5-I1 + `domain_activation.py` §5-I2). Behavioral
RED (4 seam defects) → GREEN: **D3 focused 7 / focused regressions 167 / web consumers 87 (2 skipped) / full suite 2258 passed /
3 skipped / 1 xfailed / 0 failed** (2251 baseline + 7); three load-bearing mutation probes each turned the targeted test RED and
were restored byte-identical. Scope invariants proven: only the three engine seams + the new test changed; D3-C (`web/app.py` +
`web/domain_label.py`) UNCHANGED; D8 (`domains/iot_electronics/**`) UNCHANGED; `activated_domains() == ['electronics_electrical']`
(only); no persistence/schema/commercial/quota/AccessGrant/auth diff. **D3 = IMPLEMENTATION CANDIDATE ONLY — NOT closed** (formal
closure is a separate gate after independent review → Owner acceptance → merge (create-a-merge-commit) → post-merge verification
→ remaining-obligation review); **NO domain activated; D8 OPEN / Owner-reserved; Phase 8 = FORMALLY CLOSED; Phase 9 / Phase 10 =
NOT AUTHORIZED; PSRR = NOT EXECUTED; deployment / production = NOT AUTHORIZED.** There is no other active implementation
increment.

**Immediately prior (retained as history — D3 contract-of-record, definition only):** **`Phase 8` — Subscription, Billing and Entitlements is FORMALLY
CLOSED / AUTHORITATIVE** (technical-foundation phase; no active increment remains) — **P8-CLOSE merged PR #433
(`00792af36e51808191690a4bf66f9b1a2644d477`)**; dedicated record `docs/governance/PHASE_8_FORMAL_CLOSURE_RECORD.md`. **`D3` —
Core Domain-Neutrality is now DEFINED by a governance-only CONTRACT CANDIDATE** (Owner-authorized fresh gate; the Owner's
authorization begins with the current instruction — a prior draft `ed5eb14` was REJECTED / process-scope violation / NOT
authorized / NOT merged, preserved only as historical evidence; this candidate is fresh with a new SHA + new tree). Dedicated
record `docs/governance/D3_CORE_DOMAIN_NEUTRALITY_FORMAL_CONTRACT.md`; base `00792af…`. It covers exactly **D3-A**
(`engine/safety_signal.py`), **D3-B** (`engine/path_n_questions.py`), **D3-D** (`engine/domain_rules.py`); **excludes D3-C**
(independently verified remediated by §5-I2 + P6-1). It **consumes — never duplicates** — `engine/domain_registry.py` (§5-I1)
+ `engine/domain_activation.py` (§5-I2; `electronics_electrical` = the ONLY activated specialist domain; recognition ≠
activation). Frozen invariants (12); ONE BOUNDED D3 INCREMENT; likely RED-driven boundary = the three engine modules + focused
tests; prohibited: `web/app.py`, `web/domain_label.py`, `domains/iot_electronics/**`, new packs/activation/persistence/schema/
commercial/router. Genuine RED→GREEN + load-bearing mutation + create-a-merge-commit + post-merge verification required at
implementation; 23-item acceptance criteria frozen. **DOCUMENTED NO-VALID-RED** for this contract gate. **There is NO active
implementation increment.** Owner product/policy decisions required before D3 implementation: **NONE** (only explicit D3
implementation-gate authorization after contract acceptance). **D3 = CONTRACT CANDIDATE ONLY — becomes authoritative
contract-of-record only if this exact accepted candidate is merged (create-a-merge-commit) and post-merge verified; D3
implementation = NOT STARTED / NOT AUTHORIZED by this gate; NO domain activated; D8 / `iot_electronics` = OPEN / Owner-reserved
(blocks IoT activation only); Phase 8 = FORMALLY CLOSED / AUTHORITATIVE; Phase 9 / Phase 10 = NOT AUTHORIZED; PSRR = NOT
EXECUTED; deployment / production = NOT AUTHORIZED.**

**Immediately prior (retained as history — Phase 8 formal closure candidate status when written):** **`Phase 8` — Subscription,
Billing and Entitlements is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE (P8-CLOSE; a technical-foundation phase
closure; authoritative if/when merged; dedicated record `docs/governance/PHASE_8_FORMAL_CLOSURE_RECORD.md`; base
`e7f7bc7e1f17550dc83d658976a07462de434e17`, PR #432). The Phase-8 Remaining-Obligation / Exit-Criteria Review returned **A —
ELIGIBLE FOR P8-CLOSE**. **Obligation closure matrix (all CLOSED / AUTHORITATIVE):** P8-C; P8-I1; P8-I2; P8-I3; P8-I4 (no
provider selected); P8-AF. **All mandatory Phase-8 exit criteria PASS**; N/A (contract-designed): real provider =
OWNER-SELECTION-TRIGGERED, P8-I4-I2 verified webhook + P8-I4-I3 reconciliation = EVIDENCE-TRIGGERED / DEFERRED, public paid
activation = OUTSIDE Phase 8. Delivered FOUNDATION ONLY (no commercial launch): plan-identity/entitlement + quota (sole
authority) + subscription-lifecycle mechanics + provider-neutral payment boundary + access-grant/resolution + subject-scoped
composition + fail-closed ambiguity; full suite 2251 passed / 3 skipped / 1 xfailed / 0 failed. **There is NO active
implementation increment.** Preserved OPEN/DEFERRED (none blocked closure): all Owner business decisions (plan names / pricing
/ currency / cadence / trial policy / packaging / enterprise / grandfathering / refunds / tax / grace / over-limit-downgrade /
provider selection / proration / cancellation timing); P8-AF future activation guards; trial / global-promo / Owner-Admin /
organization-named-seat / enterprise runtime; deferred capability lanes (QTA/ACV/PDF/Email/WS17/STG). PSRR = REGISTERED /
MANDATORY BEFORE PUBLIC PRODUCTION / NOT EXECUTED; `main`/OD-Q reconciliation = separate pre-production gate (not a blocker,
not performed). **Phase-8 closure authorizes nothing downstream.** **P8-C / P8-I1 / P8-I2 / P8-I3 / P8-I4 / P8-AF = CLOSED /
AUTHORITATIVE; Phase 8 = FORMAL CLOSURE CANDIDATE → FORMALLY CLOSED / AUTHORITATIVE if/when merged;** NO provider selected; NO
commercial model activated. **Next gate: separately authorized — Phase 9 is NOT AUTHORIZED and requires explicit Owner
authorization; no gate is auto-activated by Phase-8 closure.** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED;
production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-AF FORMALLY CLOSED):** **`P8-AF` — Access, Licensing &
Organization Foundation is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE (foundation-obligation closure only;
authoritative if/when merged). **P8-AF-I2** (uniform-subject correction) is **MERGED (PR #431, merge
`1132cfe8fde16a8c3a5784a2b1351a43620eda94`) / POST-MERGE VERIFIED** (independent review A); the P8-AF-C §22 closure criteria
are ALL satisfied: (a) P8-AF-C reviewed/accepted/merged (PR #429)/post-merge verified; (b) minimum increment(s) via P8-AF-I1 +
P8-AF-I2 with genuine RED→GREEN, proving the architecture can represent and resolve the models safely without activating any;
(c) authority boundaries (§4) + binding invariants (§6/§13/§16/§17/§18) demonstrated and unweakened; (d) dedicated closure
record produced (`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_FORMAL_CLOSURE_RECORD.md`). Delivered
foundation (backend composition only; NO runtime activation): canonical source-neutral `AccessGrant`; one deterministic
read-only `resolve_access(grants, *, subject, now)` seam; provenance; P8-I1 entitlement reuse; P8-I2 quota non-interference;
P8-I3 lifecycle non-interference; P8-I4 provider independence; authenticated-subject-scoped resolution + cross-account grant
isolation; fail-closed competing-entitlement ambiguity; deterministic injected-time; **`[effective_from, effective_until)`
FROZEN**. **There is NO active implementation increment.** Deferred (remain deferred): organization / membership / named seats
/ seat persistence / campaign config / global promotional-free-access runtime / Owner-Admin authorization seam / 7-day trial
activation (automatic day-7 hard deletion NOT AUTHORIZED) / enterprise-custom billing / SSO-domain onboarding / concurrent
licensing — ALL NOT STARTED / DEFERRED; future hardening/triggers preserved (constructor hardening before first runtime
caller; durable duplicate-grant-id rule before first persistence; separately governed precedence before a second real source;
global/scope semantics separately governed; data ownership independent). **P8-AF-C = CLOSED / AUTHORITATIVE; P8-AF-I1 = CLOSED
/ AUTHORITATIVE; P8-AF-I2 = CLOSED / AUTHORITATIVE; P8-AF = FORMALLY CLOSED / AUTHORITATIVE; `P8-CLOSE` = NOT STARTED; Phase 8
= NOT CLOSED;** NO provider selected; NO access model activated. **Next Phase-8 gate: the separate Phase-8 Remaining-Obligation
/ Exit-Criteria Review and `P8-CLOSE` — NOT STARTED.** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED;
production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-AF-I2 CORRECTIVE IMPLEMENTATION CANDIDATE):** **P8-AF-I1** is **MERGED (PR #430, merge
`1ac9c603b14a172a737f3577791e9f23a46533bd`) / POST-MERGE VERIFIED**; the Remaining-Obligation / Closure-Eligibility Review
returned **verdict B** (one mandatory pre-closure correction — the contract-required uniform-subject invariant, P8-AF-C §5.1
"given an authenticated account"). **P8-AF-I2 — Subject-Scoped Access Resolution is now IMPLEMENTED as a governance-only
CORRECTIVE IMPLEMENTATION CANDIDATE (RED → GREEN)**: the canonical resolver is now `resolve_access(grants, *, subject, now)`
(required authenticated `subject`); **subject scoping runs BEFORE entitlement composition**; a foreign-subject grant is
excluded **INERTLY** (never contributes/denies/raises) with explicit `foreign_subject` provenance (smallest-ambiguity — raising
would let another account deny/DoS this subject); an empty/missing subject is **NEVER** a wildcard; the post-filter precedence
is UNCHANGED (zero → DENY; one distinct entitlement → GRANT; competing distinct → FAIL CLOSED). `AccessGrant` UNCHANGED; single
runtime file changed (`engine/access_resolver.py`); no persistence/schema; no new dependency. Behavioral RED (mixed-subject
composition demo against merged I1 + 22 RED subject-scoped tests + six mutation probes) → GREEN: **focused 23 / P8-AF-I1+I2 53 /
Phase-8 177 / full suite 2251 passed / 3 skipped / 1 xfailed / 0 failed** (2228 baseline + 23); six probes each turned a test
RED and were restored byte-identical. Verified: cross-account grants never compose; foreign grant cannot rescue a denied
subject; **no authentication behavior** (subject already-authenticated; no email/password/session; no hardcoded Owner); **no
data-ownership implication** (access ≠ ownership); order-independent; `[effective_from, effective_until)` FROZEN; P8-I1/I2/I3/I4
authorities unchanged; OD-N unweakened. **Deferred (Review classifications): duplicate durable grant-identity rule = DEFERRED
UNTIL FIRST PERSISTENCE INCREMENT; direct-constructor hardening = DEFERRED BEFORE FIRST REAL RUNTIME CALLER; global/scope
(campaign) semantics = NOT STARTED / DEFERRED.** **P8-AF-I2 is a CORRECTIVE IMPLEMENTATION CANDIDATE ONLY — uniform-subject
isolation IMPLEMENTED IN CANDIDATE; P8-AF NOT closed.** Organization / membership / named seats — NOT STARTED / DEFERRED;
campaign — NOT STARTED / DEFERRED; Owner/Admin seam — NOT STARTED / DEFERRED; trial activation — NOT STARTED. **P8-AF-I1 =
MERGED/POST-MERGE VERIFIED; P8-AF-I2 = CORRECTIVE IMPLEMENTATION CANDIDATE; P8-AF = NOT CLOSED; `P8-CLOSE` = NOT STARTED;
Phase 8 = NOT CLOSED;** NO provider selected; NO access model activated. Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT
STARTED; production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-AF-I1 IMPLEMENTATION CANDIDATE):** The accepted **P8-AF-C** contract is **MERGED (PR #429, merge
`06683179f843b71f8d151f0c3c5647778b4b0acf`) / POST-MERGE VERIFIED**, and **P8-AF-I1 — Canonical Access-Grant +
Access-Resolution Foundation is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN)** — the FIRST and
SMALLEST P8-AF increment, proving ONLY the canonical access-composition seam. `engine/access_grant.py` (NEW — a LEAF immutable,
source-neutral, provider-neutral `AccessGrant` value object whose fixed slots forbid quota/provider/credential/pricing/
data-ownership fields; fail-closed `make_access_grant(...)`; pure `is_effective_at`/`exclusion_reason`; imports no engine
module) + `engine/access_resolver.py` (NEW — the SINGLE deterministic, pure, read-only `resolve_access(grants, *, now)` →
immutable `AccessResolution`; **REFERENCES** the P8-I1 authority via `plan_catalog.entitlement_descriptor` for entitlement
IDENTITY validation only — never reads capabilities, never redefines entitlement; imports only `access_grant` + `plan_catalog`)
+ the OD-N guard extension recognizing both as commercial seams. **Minimal safe precedence (P8-AF-C §6; no invented business
priority):** zero effective grants → DENY; all-one-distinct-entitlement → GRANT that single entitlement (one quota path, never
additive); **competing distinct entitlements → FAIL CLOSED** (precedence deferred). Behavioral RED (import-absent + six
mutation probes) → GREEN: **focused 30 / Phase-8 154 / full suite 2228 passed / 3 skipped / 1 xfailed / 0 failed** (2198
baseline + 30); six probes each turned a test RED and were restored byte-identical. Verified: no double quota; explainable
provenance; resolver mutates nothing and consumes NO quota/lifecycle/account/payment; entitlement REFERENCED not redefined; NO
provider coupling; **NO authentication bypass** (no hardcoded Owner; privileged-looking subject/source confers nothing); **NO
data-ownership inference** (access ≠ ownership); injected epoch time only; order-independent determinism; fail-closed on
malformed/ambiguous input; **no new persistence/schema**; P8-I1/I2/I3/I4 authorities unchanged. **P8-AF-I1 is an IMPLEMENTATION
CANDIDATE ONLY — NOT closed; P8-AF NOT closed.** **Organization / membership / named seats — DEFERRED / NOT STARTED; campaign
configuration — DEFERRED / NOT STARTED; Owner/Admin authorization seam — DEFERRED / NOT STARTED; trial activation — NOT
STARTED.** **P8-AF-C = CLOSED / AUTHORITATIVE; P8-AF-I1 = IMPLEMENTATION CANDIDATE; P8-AF = NOT CLOSED; `P8-CLOSE` = NOT
STARTED; Phase 8 = NOT CLOSED;** NO provider selected; NO access model activated. Phase 9 / Phase 10 NOT AUTHORIZED; PSRR
EXECUTION NOT STARTED; production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — contract-of-record = P8-AF-C, definition only):** **`P8-AF` — Access,
Licensing & Organization Foundation is now DEFINED by a governance-only CONTRACT CANDIDATE (P8-AF-C)** (dedicated record
`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_CONTRACT.md`; base `61ff4a85989dfc8d9881764597d5d7dc415da213`,
PR #428). It defines the smallest canonical architecture — a provider-neutral, source-neutral **Access-Grant model** + a single
deterministic **effective-access resolution seam** — that **composes** P8-I1 (entitlement) / P8-I2 (sole quota authority) /
P8-I3 (canonical lifecycle, incl. `trialing`) / P8-I4 (payment boundary) **without duplicating** any of them (D-FPC-MAP-06),
preserving **Authentication ≠ Authorization ≠ Account identity ≠ Organization membership ≠ Seat assignment ≠ Data ownership ≠
Commercial entitlement ≠ Subscription lifecycle ≠ Payment state ≠ Billing ownership** and **paying ≠ owning user data**.
Contracted (definition only): a single resolver (no scattered access decisions); an access-grant traceable to its source; a
**deterministic precedence rule** (no double quota / plan-identity corruption / accidental downgrade / hidden bypass /
ambiguous revocation); a **7-day** trial reusing P8-I3 `trialing` (168h-vs-calendar OPEN; no runtime constant; trial→paid
preserves data); a **global configurable promotional campaign** operable **without a source-code change**; **Owner/Admin
non-billed access** as authorization→entitlement (no bypass; minimal role seam, no RBAC platform); canonical **organization /
membership / named-seat** capacity-assignment-reassignment (**reassignment never transfers prior-member data**; **billing
ownership ≠ data ownership**); enterprise/custom compatibility; safe **quota** + **lifecycle composition**; **audit/provenance +
deterministic revocation** (removes access, never data); preserved **data ownership** (**automatic day-7 hard deletion NOT
authorized**; retention a separate policy); the **smallest implementation increment**; a **12-item RED→GREEN acceptance
matrix**; the **OPEN owner/business decisions**; **P8-AF closure criteria**; and **explicit production/payment/Phase-9-10
blocks**. **There is NO active implementation contract** (P8-AF-C is definition only; a separate Owner-authorized `P8-AF`
implementation gate is required, and it must select only the smallest necessary seams). **P8-I4 = CLOSED / AUTHORITATIVE;
P8-AF-C = FORMAL CONTRACT CANDIDATE; P8-AF implementation = NOT STARTED; `P8-CLOSE` = NOT STARTED; Phase 8 = NOT CLOSED;** NO
provider selected; NO access model activated; NO organization/membership/seat/role/campaign/access-grant/pricing/
enterprise-billing runtime code or schema. Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public
paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history — P8-I4 FORMAL CLOSURE / P8-AF REQUIRED NEXT):** **P8-I4 — Payment
Provider Boundary is FORMALLY CLOSED** as a governance-only CLOSURE CANDIDATE (increment closure only — authoritative if/when
merged). The accepted P8-I4-I1 implementation (independent review **verdict A — ACCEPT**) is **MERGED (PR #427, merge
`3a802fd84055f475feafcd55893da301af45c67d`; parents `fccd895` + `6f83e496…`; merged tree `191709299…`; exact diffstat 10
files / +1175 / −5) / POST-MERGE VERIFIED**; full suite **2198 passed / 3 skipped / 1 xfailed / 0 failed** (cited, not
re-run). Evidence-triggered lanes are **deferred / NOT triggered** (P8-I4-I2 verified webhook ingestion; P8-I4-I3
reconciliation; real-provider integration NOT STARTED; **provider selection OPEN OWNER DECISION**; real payment collection NOT
ACTIVATED). Canonical record: `docs/governance/P8_I4_PAYMENT_PROVIDER_BOUNDARY_FORMAL_CLOSURE_RECORD.md`. **Mandatory
handoff:** formal P8-I4 closure does **NOT** close Phase 8 — a separate cross-cutting obligation **`P8-AF` — Access, Licensing
& Organization Foundation** is **REGISTERED as the required next Phase-8 foundation gate, mandatory before `P8-CLOSE` / NOT
IMPLEMENTED / NOT ACTIVATED / NOT STARTED** (record:
`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_OBLIGATION.md`; preserves **Authentication ≠ Authorization ≠
Account identity ≠ Data ownership ≠ Commercial entitlement ≠ Subscription lifecycle ≠ Payment state ≠ Billing ownership** and
**paying ≠ owning user data**; NON-ACTIVATED future-readiness scope = individual access, a **7-DAY** (NOT 14) per-account
trial preserving durable data on trial→paid [**automatic day-7 hard deletion NOT authorized**; 168h-vs-calendar semantics
OPEN], a **global configurable promotional free period** administrable **without a source-code change**, **Owner/Admin
non-billed access** as an explicit auditable authorization→entitlement grant [no bypass], **organization/named-seat
licensing** [billing ownership ≠ data ownership; seat reassignment never transfers prior-member data], enterprise/custom
compatibility, a deterministic **access-resolution precedence**, safe **quota composition** [P8-I2 remains the sole quota
authority], and **no second lifecycle state machine** [P8-I3 remains canonical; D-FPC-MAP-06]). **There is NO active
implementation contract.** **Expected next gate: `P8-AF-C` — Access, Licensing & Organization Foundation Contract (governance
contract first; NO implementation before it is independently reviewed and accepted).** **Phase 8 remains OPEN / NOT CLOSED;
`P8-AF` / `P8-AF-C` / `P8-CLOSE` NOT STARTED; NO real provider selected; NO provider SDK; NO webhook; NO trial/promotional/
Owner-Admin/organization access activated; NO roles/organizations/seats/campaign implemented; NO automatic trial-data
deletion.** Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED / NOT
AUTHORIZED.

**Immediately prior (retained as history — P8-I4-I1 IMPLEMENTATION CANDIDATE):** The accepted **P8-I4-C** contract is **MERGED (PR #426, merge
`fccd8955afdfdd5167c4b7a4f0dbe6c14d00127b`) / POST-MERGE VERIFIED**, and **P8-I4-I1 — Provider-Neutral Payment Boundary
Foundation is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN)**: `engine/payment_provider_port.py`
(NEW port + canonical types + stdlib fingerprint) + `engine/payment_fake_adapter.py` (NEW two fakes A/B — replaceability) +
`engine/payment_ingestion.py` (NEW coordinator) + additive `engine/account_store.py` (`_apply_lifecycle_in_txn` refactor
[P8-I3 unchanged] + `provider_mapping` + `provider_event_dedupe` tables + mapping/ingest methods; atomic dedupe + P8-I3
lifecycle in ONE `BEGIN IMMEDIATE`) + `tests/test_p8_i4_i1_payment_provider_boundary.py` (30 tests) + the OD-N guard
extension. Behavioral RED (seven boundary defects) → GREEN: focused 30 / Phase-8 124 / **full suite 2198 passed / 3 skipped /
1 xfailed / 0 failed**; seven mutation probes each turned a test RED and were fully restored (byte-identical); two-thread races
deterministic. **NO real provider selected; NO provider SDK; NO webhook.** Preserved: canonical-mapping-only (raw provider name
never enters the P8-I3 log); strict provider-event idempotency (conflicting fingerprint fails closed); P8-I1/I2/I3 authorities
unchanged; anti-lockout; opaque refs; no raw payload/secret/card persisted; OD-N import isolation. **P8-I4-I1 is an
IMPLEMENTATION CANDIDATE ONLY — NOT closed; Phase 8 NOT complete / NOT paid-active**; candidate-only until independent
implementation review → Owner acceptance → PR → pre-merge check → merge → post-merge verification → a dedicated P8-I4 closure
gate. **P8-I4-I2 (verified webhook ingestion) / P8-I4-I3 (reconciliation) / real-provider selection sub-gate: NOT STARTED**
(real-provider work requires a separate Owner provider-selection decision). P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT
AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.

**Immediately prior (retained as history — P8-I4-C CONTRACT CANDIDATE):** **Current contract-of-record (DEFINITION ONLY, no implementation
authority): P8-I4-C — Payment Provider Boundary — Bounded Contract & Architecture** (governance/documentation-only CONTRACT
CANDIDATE; base `f66ea96` (PR #425); dedicated contract
`docs/governance/PHASE_8_I4_PAYMENT_PROVIDER_BOUNDARY_INCREMENT_CONTRACT.md`; authoritative if/when independently reviewed,
Owner-accepted, merged, post-merge verified). It freezes the smallest provider-neutral payment boundary (adapter port;
canonical↔provider separation; opaque canonical identities; additive mapping/dedupe persistence; event-authenticity + hard
secrets boundary; **strict provider-event idempotency incl. conflicting-payload fail-closed** — resolving the P8-I3
non-blocking observation; atomicity; P8-I1/I2/I3 authority preserved with adapters mapping to the P8-I3 lifecycle seam;
fail-closed catalogue; outage/reconciliation rules; replaceability acceptance property; PCI architectural avoidance with no
compliance claim; a 30-item future RED matrix; fake-adapter-first decomposition). **NO provider selected** — provider
selection is an OPEN Owner decision and a registered prerequisite for real adapter work. **P8-I4-C confers NO implementation
authorization; P8-I4 remains NOT STARTED / NOT IMPLEMENTED / NOT AUTHORIZED** — a separate Owner-authorized P8-I4
implementation gate (starting with the fake/reference-adapter P8-I4-I1) is required. Immediately prior: **P8-I3 — Subscription
Lifecycle FORMALLY CLOSED** (PR #424 `cef9a52`). Phase 8 OPEN; P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR
EXECUTION NOT STARTED; production / public paid activation BLOCKED / NOT AUTHORIZED.

**Immediately prior (retained as history):** **P8-I3 — Subscription
Lifecycle is FORMALLY ACCEPTED AND CLOSED** (increment closure only): corrected implementation candidate
`8e600c0674bfeb7be96fd6875b68de1da02eae2f` (initial verdict B → corrected re-reviewed **A**) **MERGED (PR #424, merge
`cef9a522dfae53493ceb1b47bd9faf409617e13e`; parents `09743b9` + `8e600c0`; merged tree `3d1586e…` == accepted candidate tree)
/ POST-MERGE VERIFIED (Pre-Merge Safety Check PASS; Post-Merge Verification PASS)**; dedicated record
`docs/governance/P8_I3_SUBSCRIPTION_LIFECYCLE_FORMAL_CLOSURE_RECORD.md` (**DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY FORMAL
CLOSURE GATE**). RED→GREEN focused 45 / Phase-8 94 / full suite 2168 passed / 3 skipped / 1 xfailed / 0 failed; diffstat 8
files / 1416 / −10. The invalidated prior implementation candidate `4385a33` (verdict B) remains EVIDENCE-ONLY / NOT MERGED.
Non-blocking observations preserved (idempotency-payload replay carried to P8-I4; optional future store-level stale test — do
not reopen P8-I3). **P8-I3 closure is an increment closure only — it does NOT close Phase 8, does NOT start P8-I4, selects NO
payment provider, and enables NO public paid activation.** **NEXT PHASE-8 GATE: `P8-I4` — Payment Provider Boundary — NOT
STARTED / NOT AUTHORIZED to begin by this closure (no provider selected).** Phase 8 OPEN; P8-CLOSE NOT STARTED; Phase 9 /
Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.

**Immediately prior (retained as history):** the P8-I3 IMPLEMENTATION CANDIDATE (CORRECTED). The accepted **corrected
P8-I3-C** contract is **MERGED
(PR #423, merge `09743b91b764e5ac2956401d7a88c91df48d3d8b`) / POST-MERGE VERIFIED**, and **P8-I3 — Subscription Lifecycle is
now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN; verdict-B CORRECTED — supersedes the invalidated
prior implementation candidate `4385a33`, EVIDENCE-ONLY / NOT MERGED)**: `engine/subscription_lifecycle_service.py` (NEW seam)
+ additive `engine/account_store.py` lifecycle tables/methods (append-only event log source-of-truth carrying the scheduled
target plan + derived cache; one-`BEGIN IMMEDIATE` atomicity with **in-transaction** stale-effective_at + pending-schedule
exclusivity + from-state guards) + `tests/test_p8_i3_subscription_lifecycle.py` (45 tests) + the OD-N guard extension.
Verdict-B corrections RC-I1..RC-I6 implemented and mutation-proven (pending-schedule exclusivity; in-txn stale check;
different-transition conflict guard causally tested; scheduled target plan in the event log + reconstructable; event-id-scoped
materialization idempotency; lifecycle reads fail closed for missing/disabled/deleted). Behavioral RED → GREEN: focused 45 /
Phase-8 94 / **full suite 2168 passed / 3 skipped / 1 xfailed / 0 failed**; six correction mutation probes each turned a test
RED and were fully restored (byte-identical); two-thread races deterministic. Preserved: `none` entitlement-neutral,
canonical `past_due` exits, unique cancellation mapping, P8-I2 sole quota authority + no reset, anti-lockout, provider
neutrality, OD-N. **P8-I3 is an IMPLEMENTATION CANDIDATE ONLY — NOT closed; Phase 8 NOT complete / NOT billing-live / NOT
paid-active**; no provider selected; candidate-only until independent re-review → Owner acceptance → PR → pre-merge check →
merge → post-merge verification → a dedicated formal P8-I3 closure gate. P8-I4 / P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT
AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.

**Immediately prior (retained as history):** the corrected P8-I3-C contract-of-record (definition only) —
**P8-I3-C — Subscription Lifecycle — Bounded Implementation Contract (CORRECTED — verdict-B remediation)**
(governance/documentation-only CONTRACT CANDIDATE; base `0a19daf` (PR #422); dedicated contract
`docs/governance/PHASE_8_I3_SUBSCRIPTION_LIFECYCLE_INCREMENT_CONTRACT.md`; authoritative if/when independently re-reviewed,
Owner-accepted, merged, post-merge verified). It **supersedes the prior candidate `ead186d`** (independent review verdict
**B — ACCEPT WITH REQUIRED PRE-MERGE CORRECTIONS**; INVALIDATED / NOT MERGEABLE / EVIDENCE-ONLY / NOT MERGED; preserved as
evidence). Corrections applied: **RC-1** `none` entitlement-neutral (no silent legacy downgrade); **RC-2** canonical
`past_due` exits (`subscription_expired`/`subscription_cancelled`); **RC-3** unique cancellation-request mapping
(`subscription_change_scheduled` reserved for PLAN changes only); + due-scheduled-transition materialization and
equal-`effective_at` tie-break clarifications. It defines the smallest safe provider-neutral, additive, backward-compatible,
deterministic, auditable, account-scoped lifecycle state model + persistence/service boundaries (subordinate to P8-C §6 and
the closed P8-I1/P8-I2 foundations; honoring G-MPR-01-D D2). **There is NO active *implementation* contract-of-record;
P8-I3-C confers NO implementation authorization** — a separate Owner-authorized P8-I3 implementation gate is required.
**P8-I3 remains NOT STARTED / NOT IMPLEMENTED / NOT AUTHORIZED.** Immediately prior: G-MPR-01-D (findings disposition;
formally closed P8-I1; registered the P8-I3 persistence rule + future gates) — MERGED (PR #422). Phase 8 OPEN; P8-I4 /
P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation
BLOCKED. (Header note: this "Active contract"
section previously still labeled **D-P6-18 — Global UI Language** as the status line; that increment is
**FORMALLY ACCEPTED AND CLOSED** — see below — and is preserved as history, not the current active gate; the running current
truth is in the paragraph that follows and in `CURRENT_PROJECT_STATE.md` + `ACTIVE_EXECUTION_ROADMAP.md`.)

**Immediately prior (retained as history):** **D-P6-18 — Global UI Language (English | العربية) (Phase 6)** —
**IMPLEMENTED / INDEPENDENTLY REVIEWED (B — ACCEPT, zero blockers) / MERGED (PR #388, merge `b47bf4bb57446956c47488283248cfbacd603e85`; parents `a0426cbb6a188a366006d22472c875ec4e5e446b` + `62818a8c71a83be487928d8b2ccaa2feb4dd678d`; merged tree `f6ed63d94db15a5e84326f9e551a7c1eddd3dd34`) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED (G-DP6-18-GLOBAL-UI-LANGUAGE-FORMAL-CLOSURE-01; dedicated record `docs/governance/D_P6_18_GLOBAL_UI_LANGUAGE_FORMAL_CLOSURE_RECORD.md`).**
Accepted lineage `98c47d5` → `8920f46` → `62818a8` (SHA-preserving); cumulative scope 27 files / +2012 / −337, entirely under `web/` + `tests/` (no engine/domains/schema/migration/dependency/CI). There is **no active contract-of-record**. Closing D-P6-18 authorizes **no** successor: the **Question Translation Assistant remains NOT AUTHORIZED / NOT STARTED**. **Current truth (synchronized):** the Master Obligation Index governance-only gate was subsequently OWNER-AUTHORIZED and MERGED (PR #390, tip `9665413`; **D-MOI-01** / **G-MOI-01**), and the **executed Phase 6 lane — Domain Specialization / Truthful Specialist Labeling, Option A — is now FORMALLY ACCEPTED AND CLOSED** (owner gate **G-PHASE-6-DOMAIN-SPECIALIZATION-FORMAL-CLOSURE-01**; **D-P6-CLOSE**; dedicated record `docs/governance/PHASE_6_DOMAIN_SPECIALIZATION_FORMAL_CLOSURE_RECORD.md`). The Product-Foundation §5 "Multi-Domain and Technology Capability Foundation" is a **DISTINCT FUTURE PROGRAM — NOT closed / NOT authorized** by that closure. **Current contract-of-record (definition only): §5-C1 — Product-Foundation §5 Multi-Domain & Technology Capability Foundation** — a governance/documentation-only contract-definition + owner-decision gate (**G-S5-C1-MULTI-DOMAIN-FOUNDATION-CONTRACT-01**; dedicated contract `docs/governance/PRODUCT_FOUNDATION_S5_MULTI_DOMAIN_FOUNDATION_CONTRACT.md`; owner decisions **D-S5-C1** / **D-S5-01…D-S5-09**). It records owner decisions, a formalized backward-compatible domain-pack contract, and a bounded 5-increment plan (§5-I1…§5-CLOSE), and **authorizes no implementation**. There is **no active *implementation* contract-of-record**. **§5-I1 — Domain Registry Validation Hardening (D-P6-14) is IMPLEMENTED / INDEPENDENTLY REVIEWED (B, zero blockers) / MERGED (PR #393, merge `9d5e3bf1870d9f59def8bcd0d686a5b682886c8a`; parents `3da1e03`+`5d518f4`; merged tree `a62f46f`) / FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-I1-DOMAIN-REGISTRY-HARDENING-FORMAL-CLOSURE-01**; **D-S5-I1-CLOSE**; dedicated record `docs/governance/S5_I1_DOMAIN_REGISTRY_HARDENING_FORMAL_CLOSURE_RECORD.md`). It hardened the existing canonical Domain Registry only (no new registry; D-FPC-MAP-06); no domain activated; electronics-only activation unchanged. **§5-I2 — Activation-status policy + explicit unsupported-domain model is now IMPLEMENTED / INDEPENDENTLY REVIEWED (foundation B + completion-delta B, zero blockers) / MERGED (PR #396, merge `e224215228b52a53bb2a0cba8eacbdfc19e1ed78`; parents `4770244`+`56afc7a`; merged tree `1576c9c`) / FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-I2-ACTIVATION-STATUS-POLICY-FORMAL-CLOSURE-01**; **D-S5-I2-CLOSE**; dedicated record `docs/governance/S5_I2_ACTIVATION_STATUS_POLICY_FORMAL_CLOSURE_RECORD.md`). It added an explicit engine activation policy (three support states; electronics-only activation, pack-status ≠ activation; web admission bound to the policy) with no domain activated and no persistence/domain-pack/user-copy change. **§5-I3 — Subsystem + cross-domain project model foundation is now IMPLEMENTED / INDEPENDENTLY REVIEWED (B, zero blockers) / MERGED (PR #398, merge `dac5696ebcf9c9814b2adb66887a535e089a6c85`; parents `04a9c4d`+`0a7f135`; merged tree `63a63e3`) / FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-I3-SUBSYSTEM-CROSS-DOMAIN-MODEL-FORMAL-CLOSURE-01**; **D-S5-I3-CLOSE**; dedicated record `docs/governance/S5_I3_SUBSYSTEM_CROSS_DOMAIN_MODEL_FORMAL_CLOSURE_RECORD.md` — closure authoritative if/when its governance candidate is merged). It added an additive in-memory subsystem foundation (one project → zero-or-more subsystems → each may reference a canonical domain as metadata; support-state via the §5-I2 policy) with the scalar root domain and all persistence preserved; durable subsystem persistence / identity / display-name / subsystem-grain evidence-risk-validation remain **future / NOT delivered**. **§5-I4 — EVIDENCE GATE NOT MET → SKIP at current evidence** (no Technology Capability Registry). **Product-Foundation §5 — Multi-Domain and Technology Capability Foundation is now FORMALLY ACCEPTED AND CLOSED** (gate **G-S5-CLOSE-PRODUCT-FOUNDATION-FORMAL-CLOSURE-01**; **D-S5-CLOSE**; dedicated record `docs/governance/PRODUCT_FOUNDATION_S5_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when its governance candidate is merged) after §5-C1 + §5-I1 + §5-I2 + §5-I3 + the §5-I4 evidence-gate decision and the four governance-gap reconciliations (GAP-1…GAP-4); ORIGINAL §5 unfinished material obligation = NONE; POST-§5 material implementation gap = NONE. **Phase 7 — API and Integration Foundation** (canonical authority in `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` §5) is now the **active phase** under a **Standing Owner Authorization**. **Current contract-of-record: P7-C — Formal Phase-7 Contract & Acceptance Criteria** — an owner-accepted governance/documentation-only Phase-7 contract-of-record (owner gate **G-P7C-FORMAL-PHASE-7-CONTRACT-PUBLICATION-01**; **D-P7C-01**; dedicated contract `docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`) that formalizes the frozen P7-A discovery + P7-B architecture decisions (and both accepted P7-B/P7-C correction addenda) — read/export-first v1 (product surface = Project read + Versioned Structured Output/Export only); a Lean internal read/export service seam before public exposure; a distinct least-privilege machine/API identity separate from browser auth; a first-public-exposure security baseline (authn/authz/version-identity/stable-errors/correlation/audit/rate-limit/provenance); the outbound canonical→adapter→vendor boundary (InventorAI central context authority; no orchestrator); the untrusted-by-default inbound-result invariant; DEFERRED subsystem-durable-identity / async / write-import / inbound-persistence / vendor-integration; Audit≠Monitoring and rate-limit≠all-Abuse-Controls and Reference-Harness≠Partner-Sandbox as distinct preserved obligations; and a §18 obligation register whose closure classification is **RESERVED EXCLUSIVELY for a mandatory §25 Phase-7 Remaining-Obligation / Exit-Criteria Review (a successful first proof never auto-authorizes P7-CLOSE)**. **The P7-C contract itself confers no implementation authorization.** **A distinct, later owner decision — the Standing Phase-7 Authorization (`D-P7-STANDING-01`) — GRANTS continuation through the remaining Phase-7 gates and formal Phase-7 closure, subject to the contract boundaries, per-gate bounded scope, accepted evidence triggers, tests where applicable, Lean minimum-path, independent review where required, and the §25 exit review; no repeated top-level owner authorization is required at each intermediate gate, but no gate self-activates.** **Standing authorization ≠ active implementation increment:** **there is currently no active implementation increment.** The **P7-I1 — Internal Read/Export Service Boundary** increment (P7-C §8 first slice; bounded contract merged PR #402, merge `0041097`) is now **IMPLEMENTED / INDEPENDENTLY REVIEWED (A — ACCEPT; one required pre-merge correction applied and independently re-reviewed A) / MERGED (PR #403, merge `94ccccd4399847d5fc0fc477f24bed5145d9a7d3`; parents `0041097`+`8f30f4f`; merged tree `fba951ed86a269e2487352e206b3de65979e6e65` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure under the Standing Phase-7 Authorization `D-P7-STANDING-01`; dedicated record `docs/governance/P7_I1_INTERNAL_READ_EXPORT_SERVICE_BOUNDARY_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when this governance candidate is merged). It delivered one thin Flask-free internal seam `engine/read_export_service.py` — authorized durable Project Read via `store.load_contract`, and a distinct deterministic Structured Export composed from durable record data + canonical domain support-state (`store.load_reconstruction_inputs` → `engine.domain_activation.support_state`) — consuming the existing `store.load_owner` ownership foundation + explicit caller identity, fail-closed (NULL-owner not auto-authorized; IR-5), with no `web/app.py` change (IR-3/IR-4), no datastore construction in the seam (IR-1), no `ProjectRecordContract`/`from_state(live_state)` use (IR-2), no frozen public/export version or field names (IR-6), no public API, no governed-state mutation; changed paths = exactly `engine/read_export_service.py` + `tests/test_p7_i1_read_export_service.py` (+448). Independently reproduced evidence: focused 22 passed; regression anchors 69 passed; full suite 2047 passed / 1 skipped / 1 xfailed / 0 failed. Superseded implementation candidate `acf0c46` is evidence only (NOT accepted). **P7-I1 closure is an increment closure only — it does NOT close Phase 7, creates NO public API, and satisfies NO later Phase-7 obligation** (API security/versioning/machine identity/scopes/rate-limits/audit/adapters/import-export remain governed by P7-C and later increments; the mandatory §25 Remaining-Obligation / Exit-Criteria Review remains reserved before P7-CLOSE). The **P7-I2 — Versioned Read/Export Public API + first-public-exposure security baseline** increment is now **CONTRACT ESTABLISHED (independently reviewed A + Owner-accepted; MERGED PR #405) / IMPLEMENTED / INDEPENDENTLY REVIEWED (A — ACCEPT) / OWNER ACCEPTED / MERGED (PR #406, merge `5971b7a1c35186aa6bdb425b6846bd633d5f8b11`; parents `7abdd06`+`cd46c7f`; merged tree `a299bce1cc6e58b873fb3e20a1e6f98a7b1ab1ae` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure under the Standing Phase-7 Authorization `D-P7-STANDING-01`; dedicated record `docs/governance/P7_I2_VERSIONED_READ_EXPORT_PUBLIC_API_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when this governance candidate is merged). It delivered a versioned read-only public API (`GET /api/v1/projects/<id>` + `.../export`; `web/api_v1.py` blueprint mounted in `web/app.py` by registration only) that **consumes the P7-I1 seam** (no business-logic duplication) with the full first-public-exposure security baseline: a distinct machine/API principal (`Authorization`-header credential, never the browser session; bound to one `owner_account_id`; token-style hash-only secret; issuance/revocation/expiry/rotation + bound-account-status enforcement) with a single `project:read` scope; API + export version identity; a stable non-enumerating error envelope (cross-owner ≡ missing); request/correlation identity (malformed caller value replaced); a durable minimal access/security audit (`access_audit`, fail-closed on audit-write failure); and two-tier rate limiting reusing the hardened atomic `record_rate_attempt` (a pre-auth bounded-subject limiter before secret verification + a post-auth `api_read` limiter; both fail-closed). `api_credentials`/`access_audit` are additive tables in the existing `SqliteAccountStore` schema lifecycle with no handler-owned DDL/migration; no project-state mutation; no writes/import; no P7-I3/adapters. Changed paths = exactly `engine/account_store.py` + `web/api_v1.py` + `web/app.py` (mount) + `tests/test_p7_i2_public_api.py` (+1076). Independently reproduced evidence at the merged tip: P7-I2 focused 36 passed; P7-I1 + ownership + record-store regressions 52 passed; full suite 2083 passed / 1 skipped / 1 xfailed / 0 failed. Superseded pre-review contract candidate `4933c26` is evidence only (NOT accepted). Retained NON-BLOCKING observations: post-auth `api_read` limiter runs after the scope check; residual micro-timing on unknown credential id; `API_CREDENTIAL_STATUSES` currently inert/documentary; `access_audit` is append-only with no retention/cleanup path (later obligation — retention NOT solved). **P7-I2 closure is an increment closure only — it does NOT close Phase 7 and satisfies NO remaining Phase-7 obligation** (quotas, import/write, webhooks, adapters/P7-I3, partner sandbox, monitoring, broad abuse controls, audit retention remain governed by P7-C and later increments; the mandatory §25 Remaining-Obligation / Exit-Criteria Review remains reserved before P7-CLOSE). The **P7-I3 — Canonical Export + Local/Reference Adapter Proof (outbound-only, non-mutating)** increment is now **CONTRACT ESTABLISHED (independently reviewed A + Owner-accepted; MERGED PR #408) / IMPLEMENTED / INDEPENDENTLY REVIEWED (A — ACCEPT; one required pre-merge guard-hardening correction applied and independently re-reviewed A) / OWNER ACCEPTED / MERGED (PR #409, merge `2ee60ec018d3816c47ad20ac2136e61aa1f9d3b9`; parents `c66a219`+`27e3104`; merged tree `76ce6007aa4faffa9bb6bd8081d3616ade042dc6` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure under the Standing Phase-7 Authorization `D-P7-STANDING-01`; dedicated record `docs/governance/P7_I3_CANONICAL_EXPORT_LOCAL_REFERENCE_ADAPTER_PROOF_FORMAL_CLOSURE_RECORD.md`; closure authoritative if/when this governance candidate is merged). It delivered one local, deterministic, network-free, vendor-neutral **reference** adapter `engine/export_adapter.py` that consumes the canonical P7-I1 Structured Export (no second output model; no invented export-version identity) → a structurally distinct flattened reference DTO → an independent semantic `validate_equivalence` enforcing a contract-owned non-empty preservation floor + integrity/tamper detection (changed-floor-field / missing / duplicate / `record_id`-collision / `assertion_count`·`validation_summary`·`provenance_summary` row-inconsistency / malformed all fail); outbound-only, non-mutating, UNTRUSTED BY DEFAULT; no store/network/Flask/vendor; no public-API/domain-activation change. Changed paths = exactly `engine/export_adapter.py` + `tests/test_p7_i3_export_adapter.py` + `tests/test_p7_i2_public_api.py` (+517/−11). The P7-I2 amendment strengthened (not weakened) the adapter-import boundary, preserving the P7-I2 import allowlist and all security tests (independently reviewed A). Independently reproduced evidence at the merged tip: P7-I3 focused 21 passed; P7-I2 suite 37 passed; combined regressions 102 passed; full suite 2105 passed / 1 skipped / 1 xfailed / 0 failed. Superseded pre-review candidates `51b8fc6` (contract) and `8ee0551` (implementation) are evidence only (NOT accepted; local evidence tags; remote tag not verified/present). **P7-I3 closure is an increment closure only — it does NOT close Phase 7 and satisfies NO remaining Phase-7 obligation.** There is **no active implementation increment**. P7-I3 formal closure was MERGED (PR #410, merge `7fda709209f9c97d67bdaf752de7bda3a951ce15`; parents `2ee60ec`+`24dbe0f`; merged tree `e77d475508f53c6360a5a1b990f3e974842e7455`) / POST-MERGE VERIFIED. The mandatory **§25 Phase-7 Remaining-Obligation / Exit-Criteria Review** is now **PERFORMED as a governance-only REVIEW CANDIDATE** (dedicated record `docs/governance/PHASE_7_REMAINING_OBLIGATION_EXIT_CRITERIA_REVIEW.md`; authoritative if/when independently reviewed, Owner-accepted, and merged). It classifies all **35 P7-C §18 obligations** — **18 DELIVERED AND VERIFIED**, **17 INTENTIONALLY DEFERRED WITH OWNER-REASON-TRIGGER** (each trigger unfired), **0 NOT APPLICABLE**, **0 STILL REQUIRED BEFORE PHASE-7 CLOSURE** — yielding **PHASE-7 EXIT VERDICT: PASS — ELIGIBLE FOR A SEPARATE FORMAL PHASE-7 CLOSURE GATE** (eligibility only; not production readiness; monitoring / broad abuse controls / audit retention / partner sandbox / write-import / inbound / subsystem durable identity / async-webhook / real-vendor remain preserved trigger-deferred obligations). **Phase 7 remains OPEN / IN PROGRESS; the §25 review does NOT close Phase 7 and creates NO formal closure record.** The §25 review is now **AUTHORITATIVE / MERGED (PR #411, merge `1a8d4c70acf05f7d787d5ae24c26b6323b51b7a7`; parents `7fda709`+`dbe54e1`; merged tree `909d7bf`) / POST-MERGE VERIFIED**. **P7-CLOSE — Formal Phase-7 Closure** is now **PERFORMED as a governance-only CLOSURE CANDIDATE** (dedicated record `docs/governance/PHASE_7_FORMAL_CLOSURE_RECORD.md`) under `D-P7-STANDING-01`: it closes the **accepted Phase-7 scope under P7-C**, preserving the authoritative §25 result verbatim (35 obligations: 18 DELIVERED AND VERIFIED / 17 INTENTIONALLY DEFERRED WITH OWNER-REASON-TRIGGER / 0 NOT APPLICABLE / 0 STILL REQUIRED; EXIT PASS). **Phase-7 formal closure is CANDIDATE ONLY until this governance candidate is independently reviewed, Owner-accepted, merged, and post-merge verified** — only then is **Phase 7: FORMALLY CLOSED**. Closure makes **NO** production/security/operations-readiness claim; the 17 deferred obligations remain **future governed obligations with their accepted triggers** (NOT delivered — Audit≠Monitoring, rate-limit floor≠broad abuse controls, reference harness≠partner sandbox all preserved; access_audit retention remains an unresolved operational observation, not a closure obligation). **Phase 7 is now FORMALLY CLOSED** (P7-CLOSE MERGED PR #412, merge `c15b7e72272951a8e32d3065d96e7a24ebd1a993`; parents `1a8d4c7`+`db09fe4`; merged tree `5b25ccb`; POST-MERGE VERIFIED). The current gate is **PSRR — Production Security & Release Readiness — GOVERNANCE REGISTRATION** (NOT PSRR execution): a governance-only registration of the Owner-mandated cross-phase release gate (dedicated record `docs/governance/PSRR_PRODUCTION_SECURITY_RELEASE_READINESS_REGISTRATION.md`; durable Owner decision **D-PSRR-01**), registered as the **named release gate operationalizing OD-P / Phase-10 ownership** (D-FPC-MAP-06: existing owner extended — no competing framework; Phase 10 owns production/release/security/operational readiness; OD-P defers evaluation to Phase 10 after Phases 4–9). **PSRR governance registration is now MERGED (PR #413, merge `6c0626e3ca659f90133a7df865e2a439f7b74f73`; parents `c15b7e7`+`a569f4b`; merged tree `4f1780ce` == accepted candidate tree) / POST-MERGE VERIFIED / AUTHORITATIVE; D-PSRR-01 is AUTHORITATIVE.** **PSRR EXECUTION: NOT STARTED** (no security scan / pen-test / config review / vendor selection performed; no production-readiness claim). **Trigger: before first public production deployment. Public Production: BLOCKED until PSRR = GO** (NO-GO/FAIL leaves the block; no inference from phase-complete / tests-green / security-baseline). Phase-7 §25 deferred security/ops items (Monitoring; broad Abuse Controls; `access_audit` retention; production secrets operations) remain **NOT delivered / NOT solved** — PSRR may reassess, not auto-implement. **Phases 8/9/10 remain NOT AUTHORIZED.** The **Phase-8 privacy/legal entry boundary is now clarified** (Owner decision **D-P8-PL-01**, governance-only): the §340 "privacy and legal prerequisites accepted" prerequisite means the bounded **entry-level design/architecture/legal-scope** rules (plans/subscriptions/entitlements/quotas/commercial-data model, provider-neutral commercial architecture, cancellation/refund **state-model interfaces**) are accepted before a Phase-8 contract proceeds — it does **NOT** require the final Phase-10 public legal artifacts (Privacy Policy, Terms, payment terms, refund policy, consent) merely to *define* the commercial model; **Phase 10 retains ownership** of those final public legal/commercial/security/operational-readiness artifacts. Building Phase-8 mechanics authorizes **no public paid activation** — public paid activation stays blocked until applicable Phase-10 legal/readiness + **PSRR = GO/PASS** + the governing separate Deployment Gate + explicit Owner deployment authorization. **OD-I/OD-N substance is unchanged** (persistence+accounts-before-activation; plan-neutrality). This clarification activates no Phase-10 work, no PSRR work, and no billing implementation; it is a candidate until independently reviewed, Owner-accepted, merged, and post-merge verified. The **Phase-8 Formal Contract & Acceptance Criteria (P8-C)** is now **DEFINED by a governance-only CONTRACT CANDIDATE** (dedicated contract `docs/governance/PHASE_8_SUBSCRIPTION_BILLING_ENTITLEMENTS_P8C_CONTRACT.md`; authoritative if/when independently reviewed, Owner-accepted, merged, and post-merge verified). It defines the canonical plan/subscription/entitlement architecture (hybrid entitlement: durable subscription-state + plan catalog, derived at evaluation via one Flask-free fail-closed `evaluate_entitlement` seam consuming the existing account foundation — D-FPC-MAP-06, no new registry/manager/adapter), the critical distinctions (security rate-limit ≠ commercial quota; API scope ≠ paid entitlement; plan access ≠ domain activation; subscription active ≠ production authorization; payment success ≠ technical progression; enterprise ≠ relaxed safety; billing audit ≠ security monitoring), the binding invariants (OD-I/OD-N/OD-O/D-P8-PL-01/OD-P/D-PSRR-01/OD-K; plan-neutral core; data preserved on entitlement decrease; fail-closed), provider neutrality (**no provider selected; no prices set**), the bounded increment decomposition (**P8-I1 Plan & Entitlement Foundation [recommended first, no payment provider]** → P8-I2 Usage Quotas → P8-I3 Subscription Lifecycle → P8-I4 Payment Provider Boundary → P8-CLOSE), acceptance criteria, and the Owner/business decisions REQUIRED (plan names, prices, trial/refund/grandfathering/enterprise/tax/provider-selection policies). **Phase 8 is CONTRACT CANDIDATE ONLY — NOT implementation-started, NOT billing-live, NOT paid-active; NOT AUTHORIZED.** No implementation begins until P8-C is independently reviewed, Owner-accepted, merged, post-merge verified, and a **separate P8 implementation authorization/gate** is granted. Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. **P8-C is now ACCEPTED / MERGED (PR #416, merge `5db47a2959507fa0cb8a4c717d32e617f23a08f0`; parent 2 = accepted candidate `1aed84a`; merged tree `d3ae4a5` == accepted candidate tree) / POST-MERGE VERIFIED.** The first Phase-8 increment **P8-I1 — Plan & Entitlement Foundation** is now **DEFINED by a governance-only BOUNDED IMPLEMENTATION-CONTRACT CANDIDATE (CORRECTED — verdict-B remediation)** (dedicated contract `docs/governance/PHASE_8_I1_PLAN_ENTITLEMENT_FOUNDATION_INCREMENT_CONTRACT.md`; supersedes prior candidate `2a4b65b`, evidence only; authoritative if/when independently reviewed, Owner-accepted, merged, post-merge verified). It bounds the smallest provider-neutral proof of **Account → Commercial Plan Identity → Entitlement Evaluation → Governed Capability Access** with NO payment provider/checkout/charges/invoices/tax/quota/lifecycle/proration/UI: a code-resident versioned plan catalog + additive durable `commercial_assignments` (plan-identity only) + minimal atomic-with-audit `commercial_audit` in the existing account-store schema lifecycle + one Flask-free fail-closed derived-entitlement seam (`evaluate_entitlement`; no stored snapshot; no `if plan==` branching) + one neutral internal governed-capability proof. It records an **explicit, bounded, Owner-acceptance-conditional REFINEMENT of P8-C** (catalog is code-resident versioned declarative data vs P8-C §18 DB-durable; P8-I1 assignment carries plan identity only — lifecycle states/period boundaries deferred to P8-I3; honest future schema-evolution path — no `ALTER TABLE` framework exists, so P8-I3 must separately choose an additive lifecycle table or a designed idempotent evolution mechanism) — **NOT a silent supersession**; the accepted P8-C history is preserved. **Backward-compatible:** valid active account with no commercial row = legitimate technical-default identity (NOT an error; default/free behavior preserved; derived not back-filled); unknown/malformed plan, catalog error, missing account, and disabled/deleted account all **fail closed** (missing account must NOT get the default identity); additive idempotent migration on existing+fresh DBs; rollback-safe; no `ALTER TABLE`. **OD-N** enforced by an **engine-wide inverted-allowlist static import guard** (no `engine/*.py` imports a commercial symbol except a minimal allowlist) + a behavioral guard (identical technical inputs under differing commercial identities → identical technical evaluation). Assignment mutation + its audit commit in ONE `BEGIN IMMEDIATE` transaction (no unaudited mutation). Credential revocation stays plan-independent; internal technical identifiers not exposed via public API/UI; security rate-limit ≠ commercial quota; API scope ≠ paid entitlement; plan entitlement ≠ domain activation; anti-lock-in (owner data preserved on future downgrade) carried forward. A genuinely-RED 15-test matrix is specified; full-suite verification mandatory for the implementation candidate. **No Owner/business decision blocks P8-I1** (plan names/prices/packaging/proration deferred, not invented). The corrected P8-I1-C contract is now **ACCEPTED / MERGED (PR #417, merge `29f3aebb93452015f2354e05f63a308c22726633`; parent 2 = accepted candidate `b14396b`; merged tree `7f36a13` == accepted contract tree) / POST-MERGE VERIFIED**, and P8-I1 is now **IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN)** on the accepted contract: `engine/plan_catalog.py` (code-resident versioned declarative catalog; internal technical default `__default_technical__`; neutral internal proof capability — none exposed via public API/UI) + `engine/entitlement_service.py` (single Flask-free fail-closed `evaluate_entitlement` seam; derived-not-snapshot; fail-closed for unknown/malformed/catalog-error/missing/non-active account; valid active account with no assignment → technical default) + additive `engine/account_store.py` `commercial_assignments`/`commercial_audit` tables + `get_/set_commercial_assignment` (assignment+audit atomic in one `BEGIN IMMEDIATE`) + `tests/test_p8_i1_plan_entitlement_foundation.py`. Genuine RED first (ImportError: `plan_catalog` absent), then GREEN: **P8-I1 focused 17 passed; directly-impacted regressions 164 passed; full suite 2122 passed / 1 skipped / 1 xfailed / 0 failed** (2105 baseline + 17). OD-N proven behaviorally + by an engine-wide inverted-allowlist static import guard; credential revocation stays plan-independent; no payment/provider/checkout/quota/lifecycle/proration/UI; no domain activation; no public paid activation; no real user-facing paywall; changed paths exactly the REQUIRED allowlist (`engine/plan_catalog.py` + `engine/entitlement_service.py` + `engine/account_store.py` + the test). **P8-I1 — Plan & Entitlement Foundation is now IMPLEMENTED / INDEPENDENTLY REVIEWED / MERGED (PR #418, merge `2bf389ddaa16b6f92a9dd505e65987686f0531fa`; parent 2 = accepted impl `f55ce02`; merged tree `814d15d` == accepted impl tree) / POST-MERGE VERIFIED** (`engine/plan_catalog.py` + `engine/entitlement_service.py` + additive `engine/account_store.py` commercial tables + `tests/test_p8_i1_plan_entitlement_foundation.py`; full suite 2122 passed). The next increment **P8-I2 — Commercial Usage Quotas / Limits** is now **DEFINED by a governance-only BOUNDED IMPLEMENTATION-CONTRACT CANDIDATE** (dedicated contract `docs/governance/PHASE_8_I2_COMMERCIAL_USAGE_QUOTAS_INCREMENT_CONTRACT.md`; authoritative if/when independently reviewed, Owner-accepted, merged, post-merge verified). It bounds a provider-neutral usage-limit foundation: quota subject **(account_id, meter)** (the account principal — never browser session, never API credential); declarative **versioned quota policy in the P8-I1 catalog** (derived-at-evaluation, no per-account snapshot); a **smallest technical window** (lifetime or fixed-seconds; explicitly NOT final billing cadence — P8-I3 owns that); a new Flask-free fail-closed `engine/quota_service.py` seam (`consume_quota`/`evaluate_quota`) with **atomic evaluate-and-consume** in one `BEGIN IMMEDIATE` (no oversubscription of a hard cap); optional **idempotency key** (retry double-charge prevention); additive `commercial_usage` (canonical counter) + `commercial_usage_idempotency` tables; machine-level outcomes (`allowed`/`denied_not_entitled`/`denied_quota_exhausted`/`denied_invalid…`/`internal_fail_closed`). Binding separations: **security rate-limit ≠ commercial quota** (`record_rate_attempt` stays security-only; paid customers still rate-limited); **quota ≠ entitlement** (entitlement first, then quota); **API scope ≠ quota; credential ≠ quota subject; credential revocation plan/quota-independent**; **domain entitlement ≠ domain activation**. **HIGH-PRIORITY anti-lock-in:** commercial creation/consumption limits ≠ Owner data access/control — quotas never block reading/exporting/deleting existing Owner data; quota reduction below consumed usage is fail-safe/non-destructive. **OD-N:** engine-wide static import guard extended to `quota_service` + a commercial dynamic-import prohibition + behavioral guard; **no lower quality for free users**. No overage; no provider/lifecycle/proration; no pricing/usage UI; no public web/API surface; no public paid activation. A true prior-schema migration test convention is required; a genuinely-RED 21-test matrix is specified; **no Owner/business decision blocks P8-I2** (real quota values/cadence/packaging deferred, not invented). **The P8-I2-C contract is now **ACCEPTED / MERGED (PR #419, merge `d3e950cb5b34ee7fc0dd8522264fc412252236d3`; parent 2 = accepted candidate `1f42714`; merged tree `7c09f10` == accepted contract tree) / POST-MERGE VERIFIED**, and **P8-I2 — Commercial Usage Quotas / Limits is now IMPLEMENTED as a governance-only IMPLEMENTATION CANDIDATE (RED → GREEN; verdict-B CORRECTED replacement candidate — supersedes the invalidated prior candidate `1490548`, evidence only, NOT merged)**: a new Flask-free fail-closed `engine/quota_service.py` seam (`consume_quota`/`evaluate_quota` → `QuotaDecision`) reusing the P8-I1 entitlement seam (entitlement FIRST) + declarative versioned `quota_policy` in `engine/plan_catalog.py` (derived, no per-account snapshot) + additive `engine/account_store.py` `commercial_usage` (canonical counter) + `commercial_usage_idempotency` tables with atomic evaluate-and-consume in ONE `BEGIN IMMEDIATE` + `tests/test_p8_i2_commercial_quota.py` (P8-I1 engine-wide OD-N guard extended to the quota seam). **Verdict-B corrections applied: R1 — the read-only `evaluate_quota` no longer fails open at exhaustion (finite quota with `used >= limit`, including explicit zero-limit, now returns `denied_quota_exhausted`/`allowed=False`/`remaining=0`, no mutation; UNLIMITED unchanged); R2 — the `consume_quota` docstring now accurately describes fail-closed behavior + that `QuotaError` also arises from missing/invalid time for a fixed-window policy; plus two adjacent cleanups (lifetime `now=None` no longer persists the literal `"None"` timestamp; idempotency-key across-windows semantics documented — one logical consumption, keyed by (account,meter,key), no re-consume on later-window replay).** RED-first proof: the R1 discriminating tests FAIL against the invalid implementation (evaluate_quota allowed exhausted/zero-limit) and PASS after the fix. GREEN: **P8-I2 focused 32 passed; directly-impacted regressions 141 passed; full suite 2123 passed / 3 skipped / 1 xfailed / 0 failed (same-environment base 2091 + 32, no regression)**. Re-verified unchanged: security rate-limit ≠ commercial quota (`record_rate_attempt` untouched); entitlement ≠ quota; atomic hard-cap (no concurrent oversubscription); idempotency incl. same-key/different-amount conflict; anti-lock-in (existing Owner data read/export/account-delete when quota exhausted); OD-N behavioral + engine-wide static + dynamic-import guards; credential revocation plan/quota-independent; API scope unchanged; no domain activation; no public quota surface / no real paywall / no provider/payment/lifecycle/UI. Changed paths = the REQUIRED allowlist + the authorized guard extension. **P8-I2 — Commercial Usage Quotas / Limits is now IMPLEMENTED / INDEPENDENTLY REVIEWED (initial verdict B → corrected candidate re-reviewed A) / OWNER-ACCEPTED / MERGED (PR #420, merge `e3c65afcee1127d3dd75e4860ccb9480f7223f16`; parent 1 `d3e950cb5b34ee7fc0dd8522264fc412252236d3`; parent 2 = accepted corrected candidate `6f269acb2ebda129d220d0387693a659db48bd1a`; merged tree `65d1a660b61f975d5d9614452aeefc97f300212e` == accepted candidate tree) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure only; dedicated record `docs/governance/P8_I2_COMMERCIAL_USAGE_QUOTAS_FORMAL_CLOSURE_RECORD.md`; DOCUMENTED NO-VALID-RED — governance/documentation-only closure after an already-tested merged implementation; closure authoritative if/when this governance candidate is merged). The invalidated prior candidate `1490548` (verdict B, fail-open `evaluate_quota`) remains EVIDENCE-ONLY / NOT MERGED. Post-merge evidence reproduced at `e3c65af`: P8-I2 focused 32 passed; full suite 2123 passed / 3 skipped / 1 xfailed / 0 failed. **Process-deviation recorded truthfully:** PR #420 was merged BEFORE the planned pre-merge safety check ran (the check did NOT occur; this record does NOT claim it did), mitigated by an expanded post-merge identity verification (exact parents, merged-tree == accepted-candidate-tree, exactly the changed paths, diffstat 897/−8, clean diff-check, post-merge tests green). **P8-I2 closure is an increment closure only — it does NOT close Phase 8, does NOT start P8-I3/P8-I4, does NOT enable public paid activation, and registers/executes no PSRR.** **The MANDATORY next governance gate is `G-MPR-01` — Master Phase & Roadmap Completeness Review (read-only) — REGISTERED / NOT YET EXECUTED; execution STOPS before P8-I3. P8-I3 — Subscription Lifecycle: NOT STARTED. P8-I4 — Payment Provider Boundary: NOT STARTED. P8-CLOSE: NOT STARTED. Phase 8 remains OPEN.** Preserved for G-MPR-01: the recurring `iot_electronics` domain-pack skipped-warning (`schema_version=None`; NOT fixed here) and the prior P8-I1 closure-record ambiguity (P8-I1 closed via current-truth/roadmap sync without a dedicated formal closure record). **G-MPR-01 (read-only master review) is now COMPLETE, and `G-MPR-01-D — Findings Disposition & Roadmap Registration` (governance-only; base `d37caef`) durably registers its accepted findings.** **P8-I1 — Plan & Entitlement Foundation is now FORMALLY CLOSED** via a dedicated late-registered closure record (`docs/governance/P8_I1_PLAN_ENTITLEMENT_FOUNDATION_FORMAL_CLOSURE_RECORD.md`; closure-record documentation gap only — NO implementation reopened; historical evidence cited: implemented RED→GREEN full suite 2122, merged PR #418 `2bf389d`, merged tree `814d15d` == accepted impl tree, post-merge verified; independent-review letter-verdict provenance disclosed per the PR #341 honesty precedent). **G-MPR-01-D dispositions D1–D10** registered (dedicated record `docs/governance/G_MPR_01_D_FINDINGS_DISPOSITION_AND_ROADMAP_REGISTRATION.md`; cross-registered in `OWNER_DECISION_REGISTER.md`): D2 P8-I3 additive/backward-compatible lifecycle-persistence rule (contract constraint only); D3 mandatory pre-Phase-9 **Core Domain-Neutrality Prerequisite Gate** (future; NOT before P8-I3); D4 future **Cross-Domain / Multi-Disciplinary Engineering Integration** gate (DOMAIN REFERENCE ≠ DOMAIN ACTIVATION ≠ CROSS-DOMAIN EVALUATION; ≥2 activated domains; re-homes the stale "deferred to Phase 6" pointer); D5 deferred-capability re-homing (QTA + Output-Language implementation = ADD live homes; ACV/PDF/Email = MOVE off closed Phase-3/4/5 anchors; all NOT AUTHORIZED); D6 CAP index range CAP-01…CAP-18; D7 real-vendor vs CAP-15 vs async/webhook vs export-adapters distinction; D8 `iot_electronics` legacy status registered + guarded (no deletion/migration/normalization/activation/repurposing without a separate gate; semantic disposition reserved to Owner); D9 OD-Q `main` reconciliation = mandatory future gate before production (NOT before P8-I3); D10 governance-hygiene scoped corrections. **`P8-I3 — Subscription Lifecycle` is ELIGIBLE FOR OWNER CONSIDERATION — NOT AUTHORIZED / NOT STARTED; Phase 8 OPEN; P8-I4/P8-CLOSE NOT STARTED; Phase 9/10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; production / public paid activation BLOCKED.** Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. Public paid activation remains blocked until applicable Phase-10 legal/readiness + PSRR = GO/PASS + governing Deployment Gate + explicit Owner deployment authorization. The mandatory §25 Phase-7 Remaining-Obligation / Exit-Criteria Review is now COMPLETE / AUTHORITATIVE (MERGED PR #411, post-merge verified) and **P7-CLOSE is COMPLETE — Phase 7 is FORMALLY CLOSED** (MERGED PR #412, merge `c15b7e7`, post-merge verified); **PSRR governance registration is now COMPLETE / AUTHORITATIVE** (MERGED PR #413, merge `6c0626e3ca659f90133a7df865e2a439f7b74f73`, post-merge verified). **Current active implementation: NONE; next development work is NOT automatically activated by this synchronization.** Public Production remains **BLOCKED until PSRR = GO/PASS + the governing separate deployment gate + explicit Owner deployment authorization**. **NOT authorized:** Phases 8/9/10, deployment/release, separately governed CAP-15…18 / AISR / QTA / ACV / WS17 / STG / PDF-Email / Output-Language, domain activation outside authorized Phase-7 scope, and any evidence-triggered Phase-7 capability before its accepted trigger is actually met. The next-eligible action is read from the live `ACTIVE_EXECUTION_ROADMAP.md` + Master Obligation Index + `OWNER_DECISION_REGISTER.md`.

**Immediately prior:** **P6-1 — Truthful Domain Labeling Foundation (Phase 6, Option A)** —
**IMPLEMENTED / INDEPENDENTLY REVIEWED (B — ACCEPT, zero blockers) / MERGED (PR #385, merge `a8b874be5c994687e02d64b6e84404b641ab501e`) / POST-MERGE VERIFIED / GOVERNANCE-SYNC MERGED (PR #386, merge `1a61ae5bca4b01b6c51be2c27c396016b676f2ee`) / FORMALLY ACCEPTED AND CLOSED (G-P6-1-TRUTHFUL-DOMAIN-LABELING-FORMAL-CLOSURE-01; dedicated record `docs/governance/P6_1_TRUTHFUL_DOMAIN_LABELING_FORMAL_CLOSURE_RECORD.md`).**
Implementation candidate `ddaf4357e91f3c1d9443135b903871fdb3bd554a` (parent `df9e6abc5e0fae1ff78c91bccfa88a2ccb34a27b`,
tree `c50d79110da61bd6d2ea5f2283660c0876b3853a`; 5 files / +259 / −2; central resolver `web/domain_label.py`). Per owner
decision **D-P6-16** (RESUME-01) a surface renders exactly ONE language variant — English and Arabic are never displayed
simultaneously; both EN and AR remain canonical in the resolver, and the current `<html lang="en">`/LTR session and
deliverable surfaces rendered the English variant only at P6-1 time (the Arabic variants were canonical but presently
unrendered because no global UI-language selector existed yet — that selector, **D-P6-18**, was then a FUTURE,
independently-authorized gate; it has SINCE been implemented and FORMALLY CLOSED (PR #388 `b47bf4b`), and the P6-1 labels
now follow the selected UI language). Originally defined (contract-of-record) by the documentation-only
contract-definition gate **G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-CONTRACT-01** (authoritative base
`3703b4ff3a74ff735964e9f16be135f17834dc17`, Merge PR #380), on the owner-accepted Phase 6 discovery
**G-P6-DOMAIN-SPECIALIZATION-DISCOVERY-01** and owner decisions **D-P6-00 … D-P6-18**. The implementation gate
**G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-IMPLEMENTATION-01** is COMPLETED and MERGED, and P6-1 is now **FORMALLY
ACCEPTED AND CLOSED**. There is **no active contract-of-record**; the next eligible owner gate is read from the live
`ACTIVE_EXECUTION_ROADMAP.md` and is **ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED** (Phase 6 as a whole is NOT
complete; no later Phase-6 increment is authorized or started by this closure). (The P6-1 CONTRACT-OF-RECORD body below is
retained as the definitional record.)

---

### P6-1 — Truthful Domain Labeling Foundation — CONTRACT-OF-RECORD (Phase 6, Option A; DEFINITION ONLY)

**Phase-6 naming (D-P6-00).** The authoritative Phase 6 lane for this execution is the `ACTIVE_EXECUTION_ROADMAP` lane —
**Domain Specialization / Truthful Specialist Labeling**. A separate registry-parity lane also historically called
"Phase 6" (`docs/GOVERNANCE_DOCUMENTS.md`, 23/23 parity) is a **distinct historical/registry-reconciliation track**;
`PRODUCT_ARCHITECTURE_AND_CREDIBILITY_ROADMAP.md` records that **neither lane authorizes the other**. This contract is
scoped to the execution lane only.

**Objective (D-P6-01, D-P6-09).** Give users truthful, human-readable information about the *limited* domain support
that actually exists, WITHOUT building a new domain engine, activating a new domain, changing deterministic behavior, or
overstating capability. Option A only: truthful labeling + truthful scope messaging + disclaimer preservation +
behavioral truthfulness tests. **No new deterministic domain rules.**

**Truthful user outcome (contract §4/§7).** Replace the raw internal identifier `electronics_electrical` on user-facing
domain/capability surfaces with a bounded **public Tier-1 label**:
- Internal id `electronics_electrical` → EN **"Electronics-informed review"**, AR **"مراجعة مستنيرة بمجال الإلكترونيات"**.
- Unknown / unsupported / missing / invalid domain → EN **"General idea review"**, AR **"مراجعة عامة للفكرة"**. The
  fallback MUST NOT silently label an unknown domain as electronics.
- State clearly the system provides **structured reasoning assistance, not professional specialist or licensed
  engineering review**; preserve truthful electronics-only scope; never imply `mechanical` / `medical_device` /
  `software` / `iot_electronics` are runtime-supported user domains. No new selection flow, dashboard, wizard,
  marketplace, multi-domain selector, or account-preference panel.

**Allowed label tiers (D-P6-02).** Tier 0 (General idea review) and Tier 1 (Domain-informed review) only. **Tier 2**
(domain-specific structured review) NOT authorized until a future increment proves real domain-specific
questions/rules/output/tests. **Tier 3 (Specialist) and Tier 4 (Licensed/professional) are PROHIBITED** under the
current product identity (`STRATEGIC_PRODUCT_VISION.md`: domain-agnostic reasoning-quality assessor, not an
implementation-readiness certifier).

**Exact technical capability (contract §5; DEFINITION — authorizes the future implementation to do ONLY):** (1) a
bounded central **public-domain-label map/policy** for the active runtime domain; (2) render that public label on the
current user-facing domain/capability surfaces; (3) truthful scope + disclaimer wording; (4) a **runtime-backed
truthfulness invariant** proving public-label ↔ actual runtime-operated domain capability; (5) **replace/supplement the
source-grep-only** runtime-integration evidence with BEHAVIORAL evidence; (6) tests preventing unsupported
Tier-2/3/4 labels; (7) bilingual EN/AR; (8) preserve accessibility + RTL/LTR. The label map MUST NOT itself activate a
domain and MUST be resolved **server-side from durable/validated runtime state** (`confirmed_domain` / validated
`state.domain`), **never from arbitrary client input**.

**Domain selection & scope (D-P6-03/04/05/06/07/11).** Preserve the current electronics confirmation gate unchanged; add
no recommendation, AI inference, confidence scoring, or multi-domain UX. The only runtime-operated domain remains
`electronics_electrical`. Low-confidence/unsupported → General/Uncertain, never a specialist label. Multi-domain NOT
supported. High-risk domains (medical, regulated, structural) remain unsupported/restricted and MUST NOT be activated or
labeled as specialized.

**Deterministic vs AI responsibility (D-P6-09; contract §14).** Presentation/labeling only. **No** change to deterministic
evaluation, gap selection, scoring, question generation, reconstruction, or the substance-signal logic. **No** AI,
model, provider, agent, or prompt change.

**Data model / migration (D-P6-10; contract §15).** Schema change NONE; migration NONE. `confirmed_domain` and
`domain_signal` unchanged. Do NOT add confidence, secondary-domain, label-history, provenance, or override fields
(future multi-domain increment).

**Claims policy (D-P6-12; contract §8).** Preserve the existing non-professional-advice / non-certification boundaries
and the deliverable forbidden-words guard. Prohibited public wording (unless a future separately-authorized capability
truly supports it): "Electronics Specialist", "Engineering Specialist Review", "Expert Review", "Professional Review",
"Certified Review", "Approved", "Feasible", "Safe to build", "Ready for implementation".

**Permitted implementation paths (contract §13 — the future gate may touch ONLY, and only those proven necessary by an
exact inventory):** one small public-domain-label helper/module; `web/app.py` (server-side label resolution/context
only); the current session/review/deliverable templates that today expose a raw domain/pack-id
(`web/templates/session.html`, the deliverable/review-snapshot template, entry-page domain wording, and a user-facing
export field ONLY if it exposes a raw pack id and truthfulness requires it); focused Phase-6 truthful-label tests; the
existing domain-gate / registry test files ONLY where required for behavioral proof; `tests/conftest.py` only if
necessary. The implementation contract MUST list exact file paths, not directories.

**Prohibited implementation paths (contract §14 — the future gate must NOT change):** `domains/*.json`;
`engine/domain_registry.py`; `engine/domain_rules.py`; `engine/progression_loop.py`; `engine/scoring.py`;
`engine/idea_state.py`; `engine/record_contract.py`; `engine/session_reconstruction.py`; `engine/path_n_questions.py`;
`engine/safety_signal.py`; `engine/requirement_landscape.py`; `engine/idea_development_outputs.py`; schemas; migrations;
dependencies; CI/deployment; prompts; provider adapters; agents/models. If an exact inventory proves a prohibited path
is genuinely necessary, the implementation gate MUST STOP and return to the owner rather than silently broaden scope.

**RED-first plan (contract §10).** Genuine RED on the exact live parent before GREEN:
- **RED-01** a user-facing surface exposes the raw internal pack id / inconsistent raw domain wording (evidence today:
  `web/templates/session.html` "Domain: {{ state.domain or 'electronics' }}"; the deliverable snapshot renders
  `Capability: {{ cap.capability_id }}` = the raw `electronics_electrical` pack id).
- **RED-02** no central enforced public-label tier policy exists.
- **RED-03** no behavioral test binds the public label to runtime-operated capability.
- **RED-04** the existing source-grep runtime-integration test (`tests/test_domain_registry.py::TestRuntimeIntegration`)
  can stay green even if runtime behavior is disconnected.
- **RED-05** no test prevents unsupported specialist/expert/professional labels being introduced.
- **RED-06** unknown/invalid domain label fallback is not behaviorally proved.
- **RED-07** bilingual public labels are not behaviorally proved.
For each RED test record: exact failure; why it is a real missing behavior; why it cannot false-green; expected GREEN;
exact path.

**GREEN plan (contract §11).** internal pack id not shown on user-facing surfaces; Tier-1 label renders (EN+AR);
fallback = General idea review / مراجعة عامة للفكرة; Tier-2/3/4 rejected/absent; disclaimer visible+truthful; no new
domain activated; existing electronics flow functional; unknown/invalid domain does not overclaim; current domain-gate
tests green; registry tests green; full suite green.

**Runtime truthfulness test (contract §9).** A genuine BEHAVIORAL test (NOT source grep / file existence / import /
string-presence): a real user session enters via the electronics gate → receives the validated electronics runtime
domain → reaches a current user-facing review/session surface → sees the Tier-1 public label → does NOT see the raw
pack id → does NOT see Tier-2/3/4 language → receives the safe fallback when domain state is missing/invalid. The exact
mechanism is defined from live repository evidence in the implementation gate.

**Independent review (contract §12).** A/B requires: no overclaim; no raw internal identifier leakage on current
user-facing surfaces; behavioral runtime-label proof; truthful fallback; disclaimer preservation; no new domain
activation; no deterministic-engine change; no schema change; no AI/model/agent change; no material false-green. **C is
mandatory** if: Tier-2/3/4 shown without supporting capability; unsupported domains appear active; label derives from
client input; unknown domain silently becomes electronics; runtime truthfulness proved only by source grep; disclaimers
weakened; deterministic evaluation changed; a new domain activated; or scope expands into registry hardening or
multi-domain work.

**Rollback (contract §16).** Revert the bounded label/helper/template/test commit; no DB rollback; no domain-pack
rollback; no project-data rewrite; no account/ownership effect; no output-contract change beyond user-facing
presentation.

**Observability (contract §17).** No analytics/external telemetry. Permitted evidence: deterministic tests,
rendered-template assertions, existing app logs without raw project/domain content. Do NOT log project text, raw tokens,
unnecessary account ids, or client-provided domain values as trusted labels.

**Registry hardening (D-P6-14).** The deferred Domain Registry validation gaps (version-format, date-field, allowed
status values, classification/substance signal completeness, gap_type_mappings completeness+element types, rule_nuances
completeness+element types, provenance/governance metadata, pack-id collision detection, alias resolution) remain a
**SEPARATE bounded increment and a prerequisite before any new domain activation** — NOT fixed in this contract gate or
in the first labeling implementation.

**Explicit deferrals (D-P6-15).** new domain activation; multi-domain orchestration; AI-assisted domain recommendation;
model/provider routing; new agents; new prompts; new output types; deterministic domain-rule activation; registry
hardening; post-output refinement; WS17 AI Coach; STG; ACV; PDF/download; output email delivery; production email
provider.

**Lean justification (contract §18).** Option A is the minimum safe next increment: current specialization is thin (only
`electronics_electrical` is runtime-operated; `rule_nuances` dead, `gap_type_mappings` inert in the shipped flow);
product identity forbids professional-specialist claims; raw/internal labels need truthful public mapping; behavioral
truthfulness evidence is missing; no new engine or schema is necessary; the increment is independently reviewable and
reversible. Do not broaden it to make Phase 6 look more substantial.

**Completion criteria (contract §19).** Complete only when: paths stay within contract; RED genuine; GREEN focused
tests pass; domain-gate tests pass; registry tests pass; UX/accessibility tests pass; full suite passes; no raw
active-domain pack id on current user-facing surfaces; Tier-1 label + fallback truthful; no Tier-2/3/4 overclaim;
disclaimers intact; no new domain active; no schema/engine/AI change; independent review A/B with no blockers;
bundle/commit/tree/parent/round-trip evidence passes.

**Stop conditions (contract §20).** Stop and return to the owner if truthful labeling requires modifying deterministic
engine behavior or domain packs; the user-facing output contract cannot be changed safely; a new domain must be
activated; multi-domain selection becomes necessary; a schema change becomes necessary; a material conflict appears
between the two Phase 6 numbering tracks; product-identity documents contradict the proposed labels; or scope cannot
remain bounded and Lean.

**Merge authority.** Owner, separately. **Independent-review scope:** the reviewer questions in "Independent review"
above. **This is a contract of record only — it authorizes no code, test, schema, dependency, CI, push, PR, merge, or
implementation.**

---

**Immediately prior status.** **THERE IS NO ACTIVE OPEN IMPLEMENTATION CONTRACT. PHASE 5 — Accounts / Authentication /
Ownership / Verified Email is FORMALLY CLOSED** across all three increments (**P5-1 → P5-2 → P5-3**), each IMPLEMENTED /
INDEPENDENTLY REVIEWED (verdict **B**, PUBLISH) / MERGED / POST-MERGE VERIFIED / OWNER ACCEPTED / FORMALLY CLOSED. Final
closure is recorded by **G-P5-FINAL-CLOSURE-SYNC-01** (authoritative base `d9f888bd0def7b3275cd04860dfa2e8cc1504111`,
Merge PR #379, tree `e6a03ab46d6d01ca4b95ee87d240ce6658eeb47c`). The most recently completed increment is **P5-3 —
Project Ownership and Route Authorization** (gate **G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-IMPLEMENTATION-01**;
candidate `a0997c3`, tree `e6a03ab`, parent `b14c931`; merged via **PR #379** `d9f888b`, ancestry PASS; scope **6 files /
+562 / −15**; disallowed paths **NONE**; source branch `feat/p5-3-project-ownership-authorization` PRESERVED; focused
**19 passed**, full suite **1893 passed, 1 skipped, 1 xfailed**). **Delivered by P5-3:** additive nullable
`projects.owner_account_id` (indexed, idempotent legacy-safe migration); atomic verified-account owned-project creation
(ownership immutable, no transfer); one central fail-closed server-side route-authorization helper (ownership from
durable state + the validated session, never the `sid`/cookie/client) enforced on every protected `/session/<sid>`
GET/POST route; cross-account + anonymous denial for owned projects; generic missing/not-authorized equivalence;
disabled/deleted denial; owner-scoped project list; Draft L2 account+project isolation. **Does NOT implement** anonymous
project claim, ownership transfer, multiple owners, collaboration/sharing/teams/organizations, Draft Level 3, writable
continuation, output email delivery, ACV, AI Coach, or STG. **Preserved observations:** **OBS-P5-3-01** (replace the
`sid in SESSION_STORE` in-memory authorization fallback with caller/session-scoped authorization before any
project-deletion / broader in-memory access / session-restoration expansion); **OBS-P5-2-01** / **OBS-P5-2-02** (P5-2
email-link-tokens-in-URL and reset-atomicity, preserved). **NEXT ELIGIBLE GATE (owner consideration only — NOT started,
NOT authorized):** **Phase 6 — domain specialization / truthful specialist labeling** per the authoritative roadmap phase
map (the roadmap does NOT designate Phase 6 as "Post-Output Refinement Orchestration"). **Draft Level 3, writable
continuation, output email delivery, and every FPC remain NOT AUTHORIZED / NOT STARTED.** Decision **D17** and the AISR
seven-owner model are preserved.

The **immediately prior** contract-of-record was **P5-2 — Authenticated Sessions, Verified Email & Account Recovery
(Phase 5, Option A)**, now **IMPLEMENTED, INDEPENDENTLY REVIEWED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND
FORMALLY
CLOSED** (independent review **G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-INDEPENDENT-REVIEW-01**, verdict **B — ACCEPT
WITH NON-BLOCKING OBSERVATIONS**, PUBLISH). Gate **G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01**;
candidate `87c85c7` (tree `375db689`, parent `f84c87d`); merged via **PR #377** (merge commit
`402727a557edd7dbea3e92f477bf9cbefe74ea3e`, two-parent merge of `f84c87dc190b431ecb258b03aea699045d68a945` (base) +
`87c85c7bb2b2c41e4510377eac9ce0133061f61e` (reviewed candidate), tree `375db6895748d101905b44ca8e622128acb3f51b`, equal
to the candidate tree; ancestry PASS). Merged scope **13 files / +1712 / −78**; disallowed paths **NONE** (no
deterministic engine file, no `engine/record_store.py`, no `projects.owner_account_id`, no production
`requirements.txt`); source branch `feat/p5-2-auth-sessions-verification-recovery` PRESERVED. Focused **40 passed**; full
suite **1874 passed, 1 skipped, 1 xfailed**. The two mandatory P5-1-closure preconditions were satisfied first —
**P5-2-PRE-01** (rate-limit concurrency: `BEGIN IMMEDIATE` read-modify-write proven race-free under real concurrent
threads + bounded expired-row cleanup) and **P5-2-PRE-02** (SQLite thread strategy: one connection
`check_same_thread=False` + re-entrant lock + immediate transactions, proven under real multi-thread tests; not a bare
`check_same_thread` override). **Delivered:** login/logout; logout-all via `session_epoch`; a signed-cookie authenticated
session distinct from the project `sid`; idle 2h / absolute 14d expiry; session rotation on login; CSRF on authenticated
mutations; email-verification completion + resend; recovery request + password-reset completion (reset revokes all
sessions, no auto sign-in); disabled/deleted denial; generic non-enumerating responses; Draft L2 account-switch
isolation; bilingual accessible UX. **Does NOT implement** `projects.owner_account_id`, project ownership, project route
authorization, anonymous project claim, collaboration/sharing, P5-3, Draft Level 3, writable continuation, output email
delivery, or a production email provider. **Preserved non-blocking observations:** **OBS-P5-2-01** email-link raw tokens
in URL paths (hash-only, single-use, short expiry, not app-logged; revisit before production email/reverse-proxy) and
**OBS-P5-2-02** password-reset sequential-transaction atomicity (accepted resilience debt; evaluate one atomic operation
when `account_store` is next touched for a related security increment). **NEXT ELIGIBLE INCREMENT: P5-3 — Project
Ownership and Route Authorization**, authorized under the continuing Phase 5 owner authorization **only after this
closure sync is merged and post-merge verified**. **Draft Level 3, writable continuation, output email delivery, and
every FPC remain NOT AUTHORIZED / NOT STARTED.**

The **immediately prior** contract-of-record was **P5-1 — Account & Credential Foundation (Phase 5, Option A)**,
**IMPLEMENTED, INDEPENDENTLY REVIEWED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (verdict
**B**, PUBLISH). Gate **G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01**; candidate `6be86f5` (tree
`128b2d4`, parent `e84526d`); merged via **PR #375** (merge commit
`65a2c0e258bf9635921046ad27f8a886cce78218`, two-parent merge of `e84526d36e8518bea75da109c77f0851c0acf5c2` (base) +
`6be86f5853d84216d2bd0792c4ca98babadbfe31` (reviewed candidate), tree `128b2d415ace8a5fee2c0cff4c84aeeb28bcf5e6`, equal
to the candidate tree; ancestry PASS). Merged scope **7 files / +1024** (`engine/account_credentials.py`,
`engine/account_store.py`, `engine/email_sender.py`, `web/app.py`, `web/templates/register.html`,
`tests/test_p5_1_account_credential_foundation.py`, `tests/conftest.py`); disallowed paths **NONE**; source branch
`feat/p5-1-account-credential-foundation` PRESERVED. Focused **35 passed**; full suite **1834 passed, 1 skipped, 1
xfailed**. **Delivered (foundation only):** additive `accounts` persistence; immutable UUID `account_id` (never email);
normalized + unique email; Werkzeug **scrypt** hashing; active/disabled/deleted status; `session_epoch` foundation;
registration route + bilingual accessible form; generic non-enumerating response; verification-token **hash-only**
persistence with **24h** expiry and supersession; development `EmailSender` abstraction + memory sink; bounded
store-backed rate-limit foundation; additive idempotent legacy-safe migration; **no plaintext password** and **no raw
verification-token** storage or logging. **Does NOT implement** login/logout, authenticated Flask sessions,
authentication cookies, CSRF for authenticated mutations, verification completion, resend, password recovery/reset,
project ownership, `projects.owner_account_id`, route authorization, anonymous project claim, Draft Level 3, P5-3, output
email delivery, or a production email provider; registration does **not** sign in, create a project, or establish
ownership. **Mandatory P5-2 preconditions (binding, engineering):** **P5-2-PRE-01 rate-limit concurrency hardening** and
**P5-2-PRE-02 SQLite thread/connection strategy** — both must be addressed within the first P5-2 implementation
candidate before login/session security is accepted (full text in the §"Phase 5 increments" / roadmap P5-1 closure
entry and `OWNER_DECISION_REGISTER.md`). **NEXT ELIGIBLE INCREMENT: P5-2 — Authenticated Sessions, Verified Email, and
Recovery**, authorized under the continuing Phase 5 owner authorization **only after this closure sync is merged and
post-merge verified**. **P5-3: NOT STARTED. Draft Level 3, writable continuation, output email delivery, and every FPC
remain NOT AUTHORIZED / NOT STARTED.**

The **immediately prior** contract-of-record was **P4-2 Level-1 — Deterministic Read-Only Reconstruction of Review State
(OPTION A)**,
now **IMPLEMENTED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (owner verdict
**B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**). Merged via **PR #369** (merge commit
`276e89681e6008ec859383771b845833321b5552`, two-parent merge of `2cde5868249f5e2b135b13fb33adff5dd5e4a816` (base) +
`e66ae3a7d95994b32dd590000b1bd1e95c499c64` (reviewed candidate), tree `1f6babf08ca6aae04677739d6c945581ed90db56`,
equal to the candidate tree; candidate ancestry PASS). **Delivered (Option A / Level 1):**
`engine.session_reconstruction.reconstruct_review_state(store, sid)` — a deterministic, **read-only** reconstruction for
a durably recorded **Path-N** session. It additively persists the reconstruction inputs (`seed_idea_text`,
`confirmed_domain`, `recon_path`, `engine_contract_version`) at project creation, loads accepted-answer evidence in
authoritative `seq` order, builds a **fresh** canonical `IdeaState`, replays the seed then answer contents through the
**unchanged** `progression_loop.run_iteration`, and returns an **immutable** `ReconstructedReviewState`. Version
`p4-2-level1-recon-v1`; replay limit **500**. Legacy / missing-metadata / unsupported-path / version-mismatch fail
closed to Level-0 evidence (no AI, no network); malformed history raises the canonical `ContractError`; **no DB /
`SESSION_STORE` mutation, no UI, no session resume, no writable continuation, no prior-output validity claim.** Merged
scope **4 files / +795 / −13** (`engine/record_store.py`, `engine/session_reconstruction.py`, `web/app.py`,
`tests/test_p4_2_session_reconstruction.py`); disallowed paths **NONE**. **P4-2 Level-1 is no longer a candidate,
pending review, pending publication, not-authorized, or not-started. PHASE 4 (Durable Data and Evidence Foundation) is
FORMALLY CLOSED within its implemented boundary** (P4-0 → P4-1a → P4-1b-1 → P4-1b-2a → P4-1b-2b → P4-2 Level-1);
**Draft Level 2 — Same-Device Unsubmitted-Text Recovery is FORMALLY CLOSED (PR #372).** **Phase 5 — Accounts /
Authentication / Ownership / Verified Email Foundations is now FORMALLY PLANNED (Option A; P5-1 → P5-2 → P5-3) under the
formal contract-of-record recorded below (gate G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01); NO Phase 5
implementation is active. P5-1 becomes the next eligible implementation gate only after this formal contract is merged
and post-merge verified.** Draft Level 3, writable continuation, output email delivery, and every FPC remain NOT
AUTHORIZED / NOT STARTED.**

The **immediately prior** contract-of-record **P4-1b-2b — Read-Only Accepted-Answer Evidence Reconstruction (OPTION A)**
remains **IMPLEMENTED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** (owner verdict
**B — ACCEPT WITH BINDING CONTRACT REFINEMENTS**, refinements satisfied). Merged via **PR #367** (merge commit
`1c9dff7962a428cfd32ab577dbbbb84ce21909b3`, two-parent merge of `7d8895122235a4da25a7f4d9d0d4d5e4bab20c6b` (base) +
`945f4a36a6a6eef5bcab1ea55e30ce1dfa468820` (reviewed candidate), tree `bff45ada35e8d3bb606bcf4e6bd80e3df33d449d`,
equal to the candidate tree; candidate ancestry PASS). **Delivered (Option A):** a bounded, **read-only**
`SqliteRecordStore.load_accepted_answer_evidence(sid)` returning an **immutable `tuple`** of the `answered`-disposition
`AssertionRecord`s in persisted (`seq`) order via the project-scoped `load_contract`; `record_id` preserved as `rec_N`;
unknown `sid` → `()`; corruption → canonical `ContractError` (fail closed); no mutation, no runtime/UI/route, no session
resume, and **not** full deterministic replay (P4-2). Merged scope **2 files / +367 / −0** (`engine/record_store.py`,
`tests/test_p4_1b2b_accepted_answer_evidence.py`); disallowed paths **NONE**. **P4-1b-2b is no longer a candidate,
pending review, pending publication, not-authorized, or not-started.** The **immediately prior** contract-of-record
**P4-1b-2a — Durable Answered-Event Append and Web-Layer Idempotency** remains **IMPLEMENTED / MERGED / VERIFIED /
ACCEPTED / CLOSED** (owner verdict **B**; PR #365, merge `77bd10cc55a731b18d4e35ea262b55342a9f847f`, tree `c8808be`;
`record_id` = `rec_N`; separate durable idempotency identity; no deterministic-output engine changed). **There is NO
active open implementation contract. Phase 4 is FORMALLY CLOSED; writable continuation, Phase 5, and every FPC remain
NOT AUTHORIZED / NOT STARTED.** The most recently completed increment is **Draft Level 2 — Same-Device Unsubmitted-Text
Recovery (Local Draft Recovery)**, now **IMPLEMENTED / REMEDIATED / INDEPENDENTLY REVIEWED / MERGED / POST-MERGE VERIFIED
/ OWNER ACCEPTED / FORMALLY CLOSED** (re-review verdict **B**; contract PR #371 → implementation **PR #372**, merge
`43223dd6ab6ad169eefd64e37dee211f8bc306b9`, tree `83dbf367d0754d1b59f53ba85db0867672c3f543`; local-only, same-device;
blockers **B1/B2/B3 fixed**; no engine/schema/account/server-draft change). The Draft Level 2 increment-contract section
retained below is a **fulfilled contract-of-record** (its "CONTRACT CANDIDATE / IMPLEMENTATION NOT AUTHORIZED / NOT
STARTED" wording is **superseded** by this status). **Phase 5 — Accounts / Authentication / Ownership / Verified Email
— DISCOVERY IS COMPLETE / ACCEPTED (verdict B) and the FORMAL Phase 5 CONTRACT is now recorded below (Option A; P5-1 →
P5-2 → P5-3; gate G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01). NEXT ELIGIBLE GATE: P5-1 — Account & Credential
Foundation, which becomes eligible only after this formal contract is merged and post-merge verified. Phase 5
implementation is NOT active in this gate.** (Documentation note: the historical "P4-1b-2a … REV1" and "Contract Amendment" sections
retained below, and any statement anywhere below that "P4-2 … / P4-1b-2b … remain NOT AUTHORIZED / NOT STARTED", were
accurate as of their PR #365/#367 boundary and are **superseded** by this status for current truth. **Further superseded
(P5-1 boundary):** this rolling narrative and the Phase 5 formal-contract section below predate the P5-1 merge; every
forward-looking phrase such as "NEXT ELIGIBLE GATE: P5-1", "P5-1 becomes the next eligible implementation gate", or
"Phase 5 … remain NOT AUTHORIZED / NOT STARTED" was accurate as of the PR #374 formal-contract boundary and is
**superseded by the leading "Status (current)" block**. **Further superseded (P5-2 boundary):** this rolling narrative
and every forward-looking phrase below such as "NEXT ELIGIBLE INCREMENT: P5-2", "P5-2 is the next eligible increment", or
"P5-3: NOT STARTED" was accurate as of the PR #375/#376 boundary and is superseded by the leading "Status (current)"
block. **Further superseded (Phase 5 final closure):** every forward-looking phrase anywhere below such as "P5-3 is the
next eligible increment", "P5-3 — Project Ownership and Route Authorization — is the next eligible increment", or "Draft
Level 3 … NOT AUTHORIZED / NOT STARTED" that treats P5-3 as pending is superseded by the leading "Status (current)"
block: **P5-1, P5-2, and P5-3 are ALL IMPLEMENTED / MERGED (PR #375, PR #377, PR #379) / FORMALLY CLOSED, PHASE 5 is
FORMALLY CLOSED, and the next eligible gate — for owner consideration only, NOT started / NOT authorized — is Phase 6
(domain specialization / truthful specialist labeling) per the authoritative roadmap phase map.**)

**Review lineage (HISTORICAL — for the record).** DOC-01 candidate `0e2a5cec24d71462eadbffa193e3467d40d506a0` carried
verdict `C — REVISE AND RE-REVIEW` (preserved, unmerged); a separately-claimed
`518cfdfe0eca3fb0f52c88c5baea46c643d3c288` candidate/bundle is **NOT** an established repository artifact and must not be
relied upon. The B3 finding that a token-derived `evt-*` id would change deterministic output — historically stated as
"CONTRACT AMENDMENT / OWNER DECISION REQUIRED" — was **resolved by selecting Option A** (that requirement is no longer
outstanding). The implementation candidate `b1eb91e6fb1b3cd60637e0808c9976c408cc090a` (verdict `C`, four blocking
findings) was superseded by REV1 `0b5f7577371e196e2f7e453afc720ca168544188` (verdict `B`, all four verified closed), which
is the merged implementation. The "P4-1b-2a Increment Contract Candidate — REV1" and "P4-1b-2a Contract Amendment"
sections below are retained as **HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE**, not the current status.

**P4-1b-1 is FULLY CLOSED** (implementation MERGED and POST-MERGE VERIFIED via PR #360; governance closure COMPLETE via
PR #361 `25dacb00295bcd3d34fd2cb5f789e9eae390ae11`). *(Preserved observation: the closure section below still reads
"pending its own merge", now satisfied by PR #361.)* The bounded P4-1b-1 (Runtime Store
Construction and Durable Project Create/Load) contract (gate **G-P4-1B-1-DOC-01**, corrected by **G-P4-1B-1-AMEND-01**)
is retained below as the fulfilled contract-of-record. *(The next paragraph's "GOVERNANCE CLOSURE is PENDING" wording is
historical and superseded by this status line.)* **P4-1b-1 implementation is MERGED and POST-MERGE VERIFIED
(technically COMPLETE); its GOVERNANCE CLOSURE is PENDING** until the G-P4-1B-1-CLOSURE-SYNC-01 candidate below is
itself separately reviewed, published, PR-created, merged, and post-merge verified. The bounded P4-1b-1 (Runtime Store
Construction and Durable Project Create/Load) contract (gate **G-P4-1B-1-DOC-01**, corrected by **G-P4-1B-1-AMEND-01**)
was fulfilled by the merged correction candidate `3179cd556673e5c5b6b596a052b0744bddab011a` (independent verdict
**B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**; **PR #360**, merge `cbd0ce3046b24631c23e482dadd413aaa42dea05`; changed
exactly `web/app.py`, `tests/test_p4_1b1_runtime_project_persistence.py`, `tests/conftest.py`; 3 files / 497 insertions
/ 2 deletions). The superseded first candidate `1eced7d280449b9c0842355a1882a9d3b731a633` (verdict C) remains preserved
intact and unmerged as superseded review evidence. **P4-1b-2, P4-2, and Phase 5 remain NOT AUTHORIZED / NOT STARTED**;
**P4-1b READ-ONLY DISCOVERY is COMPLETE** (owner decision package delivered) and authorizes nothing further.
**Product-truth boundary (unchanged):** P4-1b-1 proves durable **new-project** create/restart-survival/cold-load only;
the live application does **not** durably persist accepted answers, outputs, or complete ideas — that remains P4-1b-2.
See the **"P4-1b-1 Governance Closure Sync (G-P4-1B-1-CLOSURE-SYNC-01)"** section below for the merge, post-merge
verification, preserved observations, and the recorded procedural deviation. The P4-1b-1 contract and its
G-P4-1B-1-AMEND-01 amendment below are retained as the fulfilled contract-of-record and MUST NOT be interpreted as an
active authorization for further work.

**P4-1a closure boundary (post-PR #356):** the **P4-1a — Durable-Store Proof** increment was: recorded as a contract
candidate (merged PR #355); **separately and explicitly authorized for implementation by the owner** (a distinct
authorization — the PR #355 contract merge did **not** by itself grant implementation authority); implemented;
independently reviewed (verdict **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, 0 blocking); published; merged through
**PR #356** (merge commit `dfa082af0e6f9c09222608ca47d088dc7e2df6a8`; candidate `faf57300121a74d3493e88fc1e9a9631f6ab5815`,
tree `415aee66eb92c6c3fd6683c36deb70756af6cb36`; changed exactly `engine/record_store.py` and
`tests/test_p4_1a_record_store.py`; 2 files, 426 insertions, 0 deletions); post-merge verified (candidate-ancestor
PASS; focused post-merge tests 11 passed; no prohibited path changed; no new runtime dependency); and **FORMALLY
CLOSED**. The "P4-1a Increment Contract Candidate" block retained later in this file is now a **historical
contract-of-record** and MUST NOT be interpreted as the currently active contract. **Product-truth boundary:** P4-1a
proves only a durable-store adapter capability; because P4-1b runtime integration has not started, the application
still uses the existing temporary in-memory session behaviour, no user-facing "saved"/"recoverable"/durable-project
claim is permitted, and existing in-memory sessions remain unrecoverable and unmigrated. Current live tip
`dfa082af0e6f9c09222608ca47d088dc7e2df6a8` (Merge PR #356 — P4-1a implementation closure; always re-resolve from Git).
The "Verified authoritative tip (synchronized closure pointer)" value below records an earlier closure merge and is
not re-synchronized by this entry.

**Current synchronized boundary (post-PR #353):** P4-0 — Readiness and Storage-Contract Proof was separately
authorized, implemented, independently reviewed, corrected, merged through PR #353, post-merge verified, and
formally closed by the owner. The authoritative merge commit recorded for that closure is
`286b83ffbd6916086c834658f9e16411ef4de4fe`. This synchronization records completed history only; it does not
activate or authorize P4-1, P4-2, any other Phase 4 increment, repository implementation, testing, runtime work,
publication, merge, release, or deployment. The P4-0 candidate block retained later in this file is a historical
contract-of-record and MUST NOT be interpreted as the currently active contract. Any next gate requires separate
explicit owner authorization.

**Verified authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified authoritative tip (synchronized closure pointer):** `286b83ffbd6916086c834658f9e16411ef4de4fe`
(Merge PR #353 — P4-0 implementation closure; always re-resolve the live tip from Git). Since the PR #327 gate, the bounded **remediation program** was
authorized and is now **FORMALLY CLOSED** (executable track COMPLETE): G-R01 CLOSED via PR #329/#330; DISC-007
CLOSED via PR #331 (Domain Registry v1.0 test reconciliation) and PR #332 (v1.0 validation hardening); tip at that
closure `239557e1` (PR #332 merge); repository-wide XPASS `0`; deferred Domain Registry v1.0 rules FORMALLY DEFERRED
— NOT IMPLEMENTED — NOT SOLVED. See `docs/governance/evidence/phase3_owner_decisions/REMEDIATION_PROGRAM_FORMAL_CLOSURE.md`.
**Since then, the following bounded gates have been separately owner-authorized, executed, merged, post-merge
verified, and FORMALLY CLOSED** (separate-session independent review is recorded in the respective owner
authorizations for these gates, except **PR #341 — G-PDSR**, for which merge, post-merge verification, and owner
closure are verified but a separate-session independent-review record and a letter verdict were not independently
located from inspectable PR evidence) (full merge SHAs; enumerated in
`docs/governance/evidence/phase3_owner_decisions/POST_PHASE_3_UX_IMPLEMENTATION_GATES_FORMAL_CLOSURE.md`):
PR #338 Phase 3E–3F governance sync (`a7a141ce7f25eab261e29a3e44930b76a9e7c1f4`); PR #339 G-IRB
(`fa054abe8979d9f1fe63fe9ca3122d9ce9df7078`); PR #340 G-SC0 (`94b6b9df61d655a9005599e1e18fe19de26e7338`);
PR #341 G-PDSR (`745aaaf77aaad838d418f597710194f61db3c98e`); PR #342 G-UX-SHELL
(`43453ceb87936d3a041e6edcccc0e7a8f16237a7`); PR #343 G-UX-TRUST (`cc71ab7acb39d9f772dbb1a347c78bc53f86beae`);
PR #344 G-UX-ENTRY (`41e51ba070c71e9a1ca1c351a680abb73d72204e`); PR #345 G-UX-GUIDED-LABEL
(`82cf45f94cf6a9701e10ad02c2f2d557add1ed55`); PR #346 G-GOV-SYNC-01 governance currency synchronization —
documentation-only (`6b375121648e08b882fcc2b475a5986f6a9508ef`); PR #347 G-UX-ANSWER-VALIDATION
(`722cf1c5d9b1756503ba92b34d0938fca3d1b695`); PR #348 G-UX-SNAPSHOT-DECISION — classification A, entry-point-only
refinement (`115239ffc4b4f2f1a108aae498cb1bbf016bbf08`). The **last formally closed implementation gate is
G-UX-SNAPSHOT-DECISION (PR #348)**. Current active work: **NONE** — no implementation work is presently
authorized; the next gate requires **separate explicit owner authorization**. Phase 3F bounded implementation
broadly, **Phase 4, Phase 5, WS17, and STG remain NOT AUTHORIZED / NOT STARTED**. The block below is retained as the prior
completed contract of record (Audit-Disposition & Lean-Governance gate, PR #327).

```
INCREMENT CONTRACT — Audit Disposition & Handover-Gap Canonicalization + Lean-Governance Adoption   [CLOSED — PR #327]
Objective:                Documentation-only canonicalization of the historical audit
                          disposition, the handover-to-repository gaps (DISC-001…018), the
                          deferred output/visualization capabilities (ACV/Download/Email), the
                          Phase 3B owner-decision agenda, stale-document clarification, and the
                          Lean Governance & Agent Continuity Protocol with its registers.
Owner authorization:      Owner messages "AUDIT DISPOSITION AND HANDOVER-GAP CANONICALIZATION"
                          and "LEAN GOVERNANCE AND AGENT CONTINUITY ADOPTION" (this gate).
Risk level:               Documentation-only (no code risk level; governance change).
Allowed paths:            docs/governance/** (new phase3_owner_decisions/ records; protocol,
                          state, register, contract, handover; append-only STALE_DOCUMENT_REGISTER,
                          plan, roadmap); CLAUDE.md (bounded boot-section); MVP_SCOPE_FREEZE.md
                          (append-only bounded allowance); root banners on NEXT_SESSION.md,
                          FUTURE_ARCHITECTURE_NOTES.md, VALIDATION_LOG.md, GOVERNANCE_MODEL.md.
Forbidden paths:          engine/, web/, tests/, domains/, database/, schemas/, prompts/,
                          scripts/, CI/workflow, runtime/deploy config, main, raw outputs
                          (incl. replay_debug.txt), accepted owner-decision/closure evidence
                          except the append-only edits listed above.
Expected behavior:        No runtime/product change. Governance clarity and lean continuity only.
Non-goals:                No Phase 3 activation; no Phase 3B decisions; no ACV/Download/Email/
                          sponsor/notice/privacy/Arabic-RTL/accessibility/STG design or impl.
Acceptance criteria:      Exact scope; forbidden paths unchanged; roadmap append-only; banners
                          do not overstate; phase allocations consistent; no capability described
                          as implemented; owner notes carried forward; no later gate activated.
Required tests:           None — documentation-only; DOCUMENTED NO-VALID-RED.
Tests not required:       Application/pytest execution (forbidden here).
Dependencies:             Phase 1 & 2 formally closed; OD-R/OD-S; live tip verification.
Unresolved decisions:     Phase 3B UX choices remain open (agenda-staged, not decided here).
Stop conditions:          Any forbidden-path change; base drift; a Level-1 need; a material
                          contradiction — stop and escalate.
Independent-review scope: Per protocol §5, plus: banners accurate; carve-out bounded; no
                          implementation authority granted; roadmap prefix preserved.
Merge authority:          Owner, separately (not by the execution agent).
```

---

## Draft Level 2 — Same-Device Unsubmitted-Text Recovery — Increment Contract (G-DRAFT-L2-LOCAL-CONTINUITY-CONTRACT-01) — FULFILLED CONTRACT-OF-RECORD (IMPLEMENTED / REMEDIATED / MERGED / FORMALLY CLOSED via PR #372)

> **[CLOSURE STATUS — G-DRAFT-L2-CLOSURE-SYNC-01.]** This contract is **FULFILLED**: Draft Level 2 is **IMPLEMENTED,
> REMEDIATED, INDEPENDENTLY REVIEWED, MERGED, POST-MERGE VERIFIED, OWNER ACCEPTED, AND FORMALLY CLOSED** — original impl
> candidate `9138f96` (independent review **C — REJECT**, blockers **B1/B2/B3**) → remediation candidate `4696567`
> (re-review **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**, PUBLISH) → **PR #372**, merge
> `43223dd6ab6ad169eefd64e37dee211f8bc306b9`, tree `83dbf367d0754d1b59f53ba85db0867672c3f543`. Merged scope **8 files /
> +981 / −6**; disallowed paths **NONE**; **B1/B2/B3 fixed**; focused **30 passed**, full suite **1799 passed, 1 skipped,
> 1 xfailed**. The candidate/contract text below is preserved as the fulfilled contract-of-record; its
> "CONTRACT CANDIDATE / IMPLEMENTATION NOT AUTHORIZED / NOT STARTED" wording is **superseded**. See
> `ACTIVE_EXECUTION_ROADMAP.md` and `OWNER_DECISION_REGISTER.md` (`D-DRAFT-L2-IMPL-01…07`). **NEXT ELIGIBLE GATE: Phase 5
> — Accounts / Authentication / Ownership / Verified Email — DISCOVERY AND CONTRACT DEFINITION (implementation NOT
> authorized).**

**Status (HISTORICAL — as written at the contract gate; SUPERSEDED by the closure status above):**
`CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED — DRAFT LEVEL 2 NOT STARTED`. Recording this
candidate grants **no** implementation, client-JavaScript, `localStorage`/IndexedDB, template, `web/app.py`, schema,
migration, dependency, account, or Phase 5 authority. Implementation requires a **separate explicit owner
authorization** after this candidate is independently reviewed and accepted. Follows the accepted discovery
**G-P5-DISCOVERY-AND-DRAFT-CONTINUITY-ASSESSMENT-01** (overlap **D — NOT FOUND**; current **Draft Level 0**; selected
**Option B**). Sequence of record: **Draft Level 2 (this) → Phase 5 identity foundation → Draft Level 3 (server,
account-linked)**.

**Canonical capability name:** **Same-Device Unsubmitted-Text Recovery** (short label: **Local Draft Recovery**). The
term "autosave" is avoided standalone to prevent confusion with the existing, still-binding prohibition against
automatically **authoring / rewriting / accepting / submitting** user answers (GUIDED_ANSWER_COAUTHORING; Guided
Uncertainty Support scope decision, PR #132). This capability stores a **literal copy of text the user typed** and does
**NOT** write on the user's behalf, rewrite text, accept or submit an answer, create an `AssertionRecord`, run
deterministic evaluation, close a gap, change maturity, or generate/alter outputs.

### 1. Objective & truthful user outcome
Protect unfinished user-entered text on the **same supported browser/device** against power/battery loss, tab/browser
closure, refresh, browser crash, temporary internet loss, and intentional pause — so the user can **explicitly** recover
the latest locally saved version on return. It is **local-only**: it does **NOT** provide cross-device recovery, server
persistence, accounts, writable continuation, or any change to accepted-answer semantics. It must **never** claim
recovery when browser storage is unavailable, data was cleared, private mode removed it, the user moved to another
device/browser, the draft expired, the context no longer matches, or the user explicitly discarded it.

### 2. First-increment surface scope (§6)
- **REQUIRED:** (1) **seed idea** input (`web/templates/index.html`, `textarea#idea`); (2) **main answer** input
  (`web/templates/session.html` `textarea#response`, the answered form). Highest data-loss + user-value.
- **CONDITIONAL (adopt only if the same primitive covers it at trivial cost):** the **criticality-correction free-text**
  textarea (`session.html`, the no-`action` answered-producing correction form).
- **DEFERRED:** the criticality **clarify rationale** (server-prefilled), **success-criteria** textareas.
- **PROHIBITED (this increment):** the **FDC-001 Decision Workspace** inputs (`decision_workspace.html`) and any
  legacy/unlinked surface — separate lane, in-memory, out of the minimum coherent experience.

### 3. Local storage decision (§7)
- **Selected mechanism: `localStorage`.** Minimum-Lean: synchronous simple key/value API, no schema, ubiquitous support;
  drafts are small text well under the ~5 MB origin quota. IndexedDB (async, heavier) is unnecessary for a few small
  text drafts; **no** service worker, offline app shell, or third-party library.
- **Per-draft size cap:** bounded (recommend **64 KB** per draft; oversized input is not stored — truthful "could not
  save" status, submission still allowed). **Failure/private-mode/quota:** wrap every access in try/catch; any failure
  **fails closed to Level 0** with a truthful *"Could not save a draft on this device"* and never blocks typing or
  submission. **Compatibility:** all supported evergreen browsers; unsupported/JS-disabled → Level 0.
- **No client-side encryption is claimed** (a client-held key adds no real protection); protection is by **disclosure +
  TTL + cleanup + explicit-restore**, not cryptography.

### 4. Draft identity contract (§8)
Local key (raw invention text is **never** part of the key):
`inventorai:draft:v1:<scope>:<field>:<context-id>:<context-version>` where
`v1` = draft-schema version; `<scope>` = the temporary-session/project `sid` for session surfaces, or the reserved
`__seed__` for the pre-submission seed-idea form (no `sid` yet); `<field>` = surface type (`idea` | `answer` |
`correction`); `<context-id>` = the current question/step identity where applicable; `<context-version>` = a
content/engine/question-context version stamp so a **stale** question/idea never restores. Before a stable `sid` exists
(seed-idea form), a single per-browser `__seed__` draft is used and is cleared once `/start` is confirmed accepted. **No
account ownership** is introduced.

### 5. Save behavior (§9)
Debounced save (**recommend ~800 ms** idle) on input, **plus** a flush on `pagehide` and on `visibilitychange`→hidden.
`beforeunload` is **avoided** as a primary trigger (unreliable/discouraged); `pagehide` is the interruption-flush path.
Stored record = `{ text, ts (local ISO), schema_version, key fields }`. **No network request** is made to save a Level-2
draft. Not every keystroke (debounced). Storage-write failure → truthful failure status; never blocks.

### 6. Recovery behavior (§10)
Recovery is **explicit and safe**. On load, a **matching** non-stale draft for the current key is detected; it is offered
only when the current field is empty (or holds only a server-prefilled value) via a **low-emphasis, non-modal** prompt
with **Restore / Discard** (ignoring = continue without restoring). It **never silently overwrites** newer current text.
Stale/mismatched drafts (wrong `sid`/project, wrong field, wrong `context-id`/`context-version`, expired, malformed) are
**rejected, not restored**. The last-saved time is shown; an optional truncated preview may be shown. Bilingual EN/AR +
correct RTL. Recommended wording — EN: *"Unsent text was found on this device."* AR:
*"تم العثور على نص غير مرسل محفوظ على هذا الجهاز."*  Actions — EN: *Restore / Discard*; AR: *استعادة / حذف*.

### 7. Product-truth messages (§11)
Exact truthful states: *Saving locally…* · *Draft saved on this device* · *Could not save a draft on this device* ·
*Unsent text found on this device* · *Draft restored* · *Draft discarded* · *Answer submitted*. The UI **must NOT** say
"saved to your account", "saved securely on the server", "available on another device", or "permanently saved" (Level 2
is local-only). *"Draft saved on this device"* appears **only after a save event** (low-emphasis, transient/inline —
never a persistent banner). The experience stays low-emphasis and non-disruptive.

### 8. Successful-submission cleanup (§12)
The matching local draft is deleted **only after the client receives truthful evidence that the corresponding submission
was accepted** — i.e., the Post/Redirect/Get lands on the session view showing acceptance (the just-submitted answer was
accepted and the journey advanced), **not** merely that a POST was sent. Because the answered path redirects to
`show_session` on both success and error, the client distinguishes acceptance via a **minimal server-provided truthful
accepted signal** on the redirected render (a per-submit render-context flag — the only conditional `web/app.py`
change). The draft is **NOT** cleared on client/server/CSRF/token validation failure, store-unavailable, timeout,
disconnect-before-confirmation, ambiguous result, or an error redirect. The existing **accepted-answer idempotency model
is preserved unchanged**; **no** second submission/retry model is introduced. **Ambiguous case** (server may have
committed but the browser missed confirmation): **retain the local draft**; the existing token idempotency guarantees a
same-token/same-content resubmission is an idempotent no-op (no duplicate accepted answer); truthful retry is offered;
the draft clears only once a confirmed-accepted signal is observed.

### 9. Privacy (§13)
Invention/idea text is **sensitive**. The contract requires: a **disclosure at/before the first local draft save**,
delivered by **extending the existing Data & Session Notice** (`/data-and-session`, `data_session.html`) with **one
narrowly-scoped local-draft sentence** (no new large privacy system) plus a brief inline note at the surface; disclosure
of shared-device, browser-profile, and browser-sync risks and private-mode limitations; **explicit discard**; **local
expiry**; **cleanup after successful submit** and when the user chooses to start over. **No raw draft text** may appear
in logs, analytics, exception messages, URLs, query strings, browser history, or third-party telemetry. (The draft never
leaves the browser as a draft; the server receives text only through the normal, already-governed submission path.)

### 10. Retention / TTL (§14)
Local TTL options: **(a) 24 h**, **(b) 7 days**, **(c) 30 days**. **RECOMMENDED: (b) 7 days** — balances "return later"
usefulness against shared-device exposure; enforced by **lazy cleanup on load** + cleanup on submit + explicit discard;
stale (past-TTL) drafts are ignored and purged, never restored. **TTL classification: RECOMMENDED contract-fixed at
7 days, but REQUIRES OWNER CONFIRMATION at the implementation-authorization gate** (it is a privacy tradeoff). Not
configurable at runtime in the first increment.

### 11. Failure & fallback (§15)
Fail-closed for: storage unavailable; quota exceeded; invalid/corrupted JSON; incompatible schema version; missing
project/question identity; stale question; mismatched project; malformed timestamp; expired draft; JavaScript disabled;
unsupported browser; private-browsing restriction; multiple tabs; successful submission with cleanup failure. **A draft
failure must never block normal answer submission**; the application remains fully usable at truthful **Level 0** whenever
local draft storage cannot operate.

### 12. Multi-tab boundary (§16)
Minimum Level-2 rule: **last-write-wins by local timestamp per key**, with a `storage`-event **awareness note** when a
newer same-browser draft appears in another tab (so an older tab does not silently clobber it on its next flush). **No**
cross-tab locking, **no** conflict merge, **no** multi-device conflict resolution (that is Level 4 — out of scope).

### 13. Accessibility & bilingual UX (§17)
Preserve Arabic + English with correct RTL/LTR; full keyboard operation; screen-reader announcements via `aria-live`
polite for save/restore status; **non-color-only** save/failure indication; accessible Restore/Discard controls; **no**
disruptive repeated modal (inline non-modal recovery prompt); clear focus handling after restoration. Follow the existing
Phase 3 bilingual and accessibility principles and the G-UX-SHELL baseline.

### 14. Security (§18)
DOM insertion via `.value`/`textContent` only — **never** `innerHTML`; **no** third-party scripts; a single first-party
static script compatible with a current/future **CSP** (external file, no inline handlers; nonce if required); enforce the
size cap; ignore malformed content; **never** trust draft metadata; **no** ownership or server-authorization decision is
derived from local data; local draft content is **never** treated as an accepted answer without an explicit submit; no
draft execution or HTML interpretation. On submission the restored text is **untrusted client input** — existing
server-side validation and idempotency remain authoritative.

### 15. Permitted / prohibited future paths (§19)
- **REQUIRED (future implementation):** `web/templates/index.html`, `web/templates/session.html` (script include via the
  `{% block head %}` hook + minimal markup hooks/data-attributes + the recovery-prompt region); **one new first-party
  static JS file** under a new `web/static/js/` (served by Flask's default static route, currently unused); new focused
  tests.
- **CONDITIONAL:** `web/app.py` (minimal render context **only**: the per-submit truthful accepted signal + the
  `context-id`/`context-version` + field/key identifiers passed to templates); `web/templates/base.html` /
  `web/templates/data_session.html` (the one-sentence local-draft disclosure); registration of the static assets folder
  if none is wired.
- **PROHIBITED (unchanged):** `engine/progression_loop.py`, `engine/scoring.py`, `engine/idea_state.py`,
  `engine/record_contract.py`, `engine/session_reconstruction.py`, `engine/path_n_questions.py`,
  `engine/requirement_landscape.py`, `engine/idea_development_outputs.py`; any schema/migration; any server-side draft
  store; any account/auth path; CI/deploy. **No schema or migration is required for Draft Level 2.**

### 16. RED test contract (§20) — 22 behaviour-first proofs (to be written in the implementation gate, not here)
Each fails on the live tip because **no draft mechanism exists** (typed text is lost on reload / never offered for
recovery) and **cannot false-green** because each asserts an observable browser-storage/DOM/submission outcome, not mere
existence: (1) seed idea survives reload; (2) main answer survives reload before submit; (3) main answer survives
temporary offline; (4) interruption preserves the latest saved local version; (5) a matching draft is offered for
**explicit** restoration; (6) a draft is **not** silently restored over newer current text; (7) wrong project/session
draft not restored; (8) wrong field/question draft not restored; (9) stale question/version draft not restored;
(10) expired draft not restored; (11) corrupted draft ignored safely; (12) storage failure → truthful status, submission
not blocked; (13) failed submission keeps the draft; (14) successful accepted submission clears **only** the matching
draft; (15) ambiguous network result keeps the draft and idempotency prevents a duplicate accepted answer; (16) draft
storage never creates an `AssertionRecord`; (17) never calls deterministic evaluation; (18) never changes maturity/gaps/
outputs; (19) explicit discard removes the matching draft; (20) no raw draft content in logs/URLs/analytics/errors;
(21) JavaScript-disabled behaviour remains valid Level 0; (22) existing P4-1b-2a / P4-1b-2b / P4-2 / submission /
idempotency tests remain green. Likely test file: `tests/test_draft_l2_local_continuity.py` (+ a Level-0/no-JS server
regression assertion in the existing Flask tests).

### 17. Testing approach (§21)
The app is server-rendered with **no** existing client-JS test framework, no `web/static`, and no `package.json`.
Proving client-side `localStorage` persistence across reload/close/offline requires a **real browser** — server-only
Flask tests cannot. The environment **pre-provisions Chromium + Playwright browser binaries** (`/opt/pw-browsers`,
`PLAYWRIGHT_BROWSERS_PATH`) and Node 22. **RECOMMENDED (single approach): `pytest` + Playwright (Python) driving headless
Chromium** — it integrates with the existing pytest suite and truthfully exercises localStorage/reload/offline/restore/
submit-cleanup end-to-end. This requires adding the **`playwright` Python package as a TEST-only dependency**, justified
because no existing method can prove client-side storage behaviour and the browser binaries are already present (no
download; `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`). A pure-function Node/jsdom unit test of the extracted key/staleness/
cleanup logic is an acceptable **complement** but is not sufficient alone (it cannot prove real reload/offline
lifecycle). No large frontend framework or heavyweight suite is introduced.

### 18. Implementation structure (§22) — ONE increment
**RECOMMENDED: a single implementation increment** (RED behavioural Playwright tests → the localStorage save/recovery
primitive → UX integration, successful-submit cleanup, privacy disclosure, accessibility → GREEN + regressions).
Rationale: splitting storage from cleanup/privacy would ship an **unsafe intermediate** (drafts stored with no cleanup or
disclosure = a privacy hazard). The surface is bounded (2–3 fields, one primitive), so one coherent increment is the Lean
and safe choice. Internal RED→GREEN order applies. **Rollback:** clear the `localStorage` keys and remove the script
include + template hooks + optional render flag; **no** server or schema state exists to roll back; fully reversible with
no data loss (drafts are ephemeral local copies).

### 19. Product-truth boundary (binding)
Draft Level 2 is **local-only, same-device, explicit-recovery**. It does **NOT** provide cross-device recovery, server/
account persistence, accounts, authentication, authorization, ownership, verified email, writable continuation, or any
change to accepted-answer / idempotency / deterministic-evaluation semantics. It authorizes **no** implementation. Phase 5
remains the next step **immediately after** this bounded increment and is **NOT STARTED / NOT AUTHORIZED**; server-side
Draft Level 3, writable continuation, and every FPC remain **NOT AUTHORIZED / NOT STARTED**.


## Phase 5 — Accounts / Authentication / Project Ownership / Authorization / Verified Email — FORMAL CONTRACT-OF-RECORD (G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01)

**Status:** `FORMAL PHASE 5 CONTRACT-OF-RECORD — DOCUMENTATION-ONLY — NO PHASE 5 IMPLEMENTATION ACTIVE IN THIS GATE`.
The owner accepted the discovery **G-P5-IDENTITY-OWNERSHIP-DISCOVERY-CONTRACT-01** (verdict **B — ACCEPT WITH
NON-BLOCKING RISKS**), selected **Identity Option A (application-managed email + password)** and the implementation
structure **P5-1 → P5-2 → P5-3**, and granted a **continuing authorization** to complete all three bounded increments
through formal Phase 5 closure under the controls in §"RED/GREEN and review controls" below. **P5-1 becomes the next
eligible implementation gate only after THIS formal contract is merged and post-merge verified.** Recorded on live tip
`3b231936c5d01d2af9a1c0eca2dfd39d39161cff` (Merge PR #373).

### Accepted current state (evidence)
Existing **account / authentication / ownership / verified-email** foundation: **NONE**. Reusable primitives (no new
runtime dependency needed for Option A): a configured Flask `app.secret_key` (from `INVENTORAI_SECRET_KEY`, production
fail-fast; ephemeral in dev); Werkzeug **scrypt** password hashing; `itsdangerous`; stdlib `secrets`/`hmac`/`hashlib`;
the `SqliteRecordStore` adapter + additive-migration pattern; the existing generic-unavailable behaviour. Recorded
explicitly: **`flask.session` is currently unused; CSRF protection is absent; `projects` has no owner column; `sid` is a
project capability, NOT user identity; `sid` possession alone is never ownership proof.**

### Owner decisions (binding)
- **Identity approach:** application-managed **email + password**. Immutable **UUID `account_id`** as the durable primary
  key (**never email**); **normalized email with uniqueness**; **Werkzeug scrypt** password hashes; **no** plaintext
  passwords; **no** raw verification/reset/session tokens stored.
- **Unverified-account policy:** an unverified user MAY register, sign in, request/complete verification, request
  recovery, and access basic account-management surfaces. An unverified user MAY NOT create an account-owned durable
  project, claim an anonymous project, or use future sensitive delivery capabilities.
- **Verified-account policy:** **email verification is required before creating and owning a durable account-linked
  project.** Verified email is **not** itself authorization to any other project.
- **Anonymous-project policy:** existing and future anonymous projects keep the current `sid`-capability behaviour where
  explicitly allowed; they remain **`owner_account_id = NULL`**; they are **not automatically claimable**; possession of
  `sid` alone must never permit ownership assignment; anonymous-to-account **claim is deferred** to a separate future
  increment.
- **Session policy:** **idle expiry 2 hours; absolute expiry 14 days**; cookie `HttpOnly` + `SameSite=Lax` + `Secure`
  (production) and **not** the project `sid`; **`session_epoch`** used for revocation; **password reset revokes all
  existing authenticated sessions**; current-session logout plus a bounded **logout-all** via epoch rotation.
- **Account-deletion policy:** support **disable** (reversible immediate access block) and **delete** (tombstoned
  account state). On disable/delete: authenticated sessions invalidated; verification/reset tokens invalidated; new
  login blocked as applicable; **project-ownership links must not be silently transferred**; **accepted-answer data must
  not be automatically destroyed.** Final legal/commercial retention periods remain **outside this contract** and must
  not be invented.
- **Legacy-project policy:** legacy projects remain **`owner_account_id = NULL`**, capability-accessible only under the
  existing truthful boundary; they cannot be automatically claimed or converted to account ownership.
- **Email policy:** development = a **local file/console sink**; production = a provider adapter behind an `EmailSender`
  abstraction. **Verification token expiry 24h; password-reset token expiry 1h.** Tokens are random, **hashed at rest**,
  single-use, expiring, rate-limited, **never logged raw**. Phase 5 email is limited to **verification, password
  recovery, and future email change** — it does **not** include output/marketing/notification delivery.
- **Draft Level 2 policy:** Phase 5 **consumes but does not replace** Draft Level 2. On logout / account switching, a
  local draft must not be shown under another account/project identity; preserve truthful local-device wording; do
  **not** upload the draft to the server; do **not** implement Draft Level 3.

### Canonical account model (minimum fields)
`account_id` (UUID PK) · `email_normalized` (UNIQUE) · `email_verified` (bool) · `status` (`active`|`disabled`|`deleted`)
· `password_hash` (scrypt) · `session_epoch` (int) · `created_at` · `updated_at` · `deleted_at` (nullable). **No raw
credentials or tokens stored.**

### Token model (bounded, typed)
`token_id` · `account_id` · `token_type` (`verification`|`reset`) · `token_hash` · `expires_at` · `used_at` (nullable) ·
`created_at`. Raw tokens exist only in outbound email content and the user's request. Token responses must not permit
account enumeration.

### Project-ownership model
Additive **nullable `projects.owner_account_id`** (no separate ownership table for the MVP unless implementation
evidence proves the nullable column cannot support the accepted **single-owner** model). The ownership check runs
**server-side** for every protected read, answer submission, reconstruction, output view, delete, export, future
download, future output email, and future server-draft operation. **Templates and JavaScript must not be the
authorization boundary.**

### Security requirements (fail-closed)
scrypt hashing; non-enumerating authentication/recovery responses; login/session rotation; `session_epoch` revocation;
`HttpOnly`/`Secure`/`SameSite` cookies; **CSRF on authenticated state-changing requests**; hashed single-use expiring
tokens; server-side ownership checks; generic denial; brute-force + resend rate limits; **no** raw password/token/secret
logging; disabled/deleted-account fail-closed behaviour; **legacy-route authorization coverage**; **no `sid`-based
ownership claim**.

### Phase 5 increments
**P5-1 — Account & Credential Foundation.** Scope: additive `accounts` schema; normalized-email uniqueness; immutable
`account_id`; registration; scrypt hashing; account status; email-token data model; development email sink; generic
registration response; foundational rate-limit storage; RED/GREEN tests. **Not** included: authenticated project
ownership; route authorization; Draft Level 3; output email; social login; live production email provider.

**P5-2 — Authenticated Sessions, Verified Email & Recovery.** Scope: login/logout; Flask signed authenticated cookie;
`session_epoch` revocation; idle + absolute expiry; CSRF; verification flow; resend behaviour; account recovery;
password reset; reset revokes sessions; generic non-enumerating responses; RED/GREEN tests. **Not** included: project
ownership enforcement; anonymous claiming; Draft Level 3.

**P5-3 — Project Ownership & Route Authorization.** Scope: additive nullable `projects.owner_account_id`; owner linkage
at **authenticated + verified** project creation; legacy NULL-owner compatibility; a central server-side ownership
check; the authorization matrix across protected project routes; generic 404/not-available; cross-account isolation;
disabled/deleted-account handling; Draft Level 2 logout/account-switch isolation; RED/GREEN tests. **Not** included:
collaboration; sharing; organization ownership; multiple owners; anonymous claiming; Draft Level 3; writable
continuation.

### RED/GREEN and review controls (each increment)
(1) define the bounded implementation contract; (2) produce genuine RED on the live parent; (3) implement the minimum
GREEN; (4) run focused + related + security + full-suite tests; (5) adversarial self-review; (6) one SHA-preserving
bundle; (7) stop before publication; (8) independent adversarial review; (9) publish only after **A or B without
blockers**; (10) merge via "Create a merge commit"; (11) post-merge verification; (12) governance synchronization
before the next increment where materially required. **The continuing owner authorization permits moving P5-1 → P5-2 →
P5-3 without a new owner authorization, provided all controls pass.** Stop and return to the owner only on: a material
blocker; live repository contradicting the accepted discovery; scope outside the accepted Phase 5 boundary; a new
product-policy decision not resolved above; an independent review returning **C**; or security that cannot be proved
fail-closed.

### Non-blocking risks (recorded)
(1) production `Secure`-cookie behaviour depends on confirmed HTTPS/reverse-proxy configuration; (2) no current
rate-limit primitive exists — use a small bounded store-backed counter, **not** a broad new platform/dependency; (3)
production email deliverability is an operational dependency — begin with the development sink and preserve the provider
abstraction. These do not block P5-1 contract definition.

### Permitted / prohibited future implementation paths
**REQUIRED (future):** `web/app.py`; new auth/account/session/token/ownership/email modules; new register/login/verify/
recover templates; additive schema/migration in the store adapter; new tests. **CONDITIONAL:** `engine/record_store.py`
— additive nullable `owner_account_id` column + migration + owner get/set + ownership-scoped read (additive-only,
mirroring the P4-1b-2a `idempotency_key` and P4-2 reconstruction-column precedent); a privacy-notice template update.
**PROHIBITED:** the deterministic engine — `engine/progression_loop.py`, `engine/scoring.py`, `engine/idea_state.py`,
`engine/record_contract.py`, `engine/session_reconstruction.py`, `engine/path_n_questions.py`,
`engine/requirement_landscape.py`, `engine/idea_development_outputs.py`; production `requirements.txt` (Option A needs
**no** new runtime dependency); CI/deploy; Draft Level 3; writable continuation; output/marketing email delivery;
PDF/ACV/AI-Coach/WS17/STG; collaboration/sharing/teams/orgs/subscriptions/social-login-SSO/admin dashboard; any later
phase. **Authorization logic must never live only in templates/JS.**

### Continuing authorization boundary
This is a **documentation-only** formal contract. It authorizes **no** production/test code, no schema/migration, no
dependency, no CI, no push/PR/merge in this gate. **P5-1 implementation is the next eligible gate, eligible only after
this formal contract is merged and post-merge verified.** **P5-2 and P5-3 are NOT STARTED. Draft Level 3, writable
continuation, output email delivery, and every FPC remain NOT AUTHORIZED / NOT STARTED.** Decision **D17** and the AISR
seven-owner model are preserved; Phase 4 remains FORMALLY CLOSED; P4-2 Level-1 and Draft Level 2 remain CLOSED.


## P4-1b-2a Increment Contract Candidate — REV1 — G-P4-1B-2-DOC-01-REV1 (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE — the increment is now IMPLEMENTED / MERGED / CLOSED via PR #365; see the closure banner and the "Active contract" status above)

> **[CLOSURE STATUS — G-P4-1B-2A-IMPLEMENTATION-01-REV1, owner verdict B.]** The increment defined by this contract (as
> amended for OPTION A by G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01) is now **IMPLEMENTED, MERGED, VERIFIED, ACCEPTED, AND
> CLOSED** — merged via **PR #365** (merge commit `77bd10cc55a731b18d4e35ea262b55342a9f847f`, parents `4a31ece` +
> `0b5f757`, tree `c8808be`; candidate ancestry PASS). `record_id` remains `rec_N`; a separate durable idempotency
> identity was implemented; no deterministic-output engine changed. The candidate/contract-definition text below is
> **preserved as historical record** and is no longer the pending state. **P4-1b-2b, P4-2, Phase 5+, and every FPC
> remain NOT AUTHORIZED / NOT STARTED.** See `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` and
> `OWNER_DECISION_REGISTER.md` (`D-P4-1B-2A-IMPL-01…04`).

**0. Provenance & preservation.** REV1 supersedes the original P4-1b-2a contract candidate
`0e2a5cec24d71462eadbffa193e3467d40d506a0` (gate G-P4-1B-2-DOC-01), which received independent-review verdict
**C — REVISE AND RE-REVIEW** and is **PRESERVED intact, unmerged, NOT PUBLISHABLE, and NOT amended**. A previously
claimed `518cfdfe0eca3fb0f52c88c5baea46c643d3c288` candidate/bundle is **not an established repository artifact** and is
not relied upon. REV1 is a **new** candidate created from live tip `25dacb00295bcd3d34fd2cb5f789e9eae390ae11`.

**1. Gate identity & status.** P4-1b-2a — Durable Answered-Event Append and Web-Layer Idempotency. Gate
**G-P4-1B-2-DOC-01-REV1**. **Status (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE):** at the time this contract was
defined it read `CORRECTED CONTRACT CANDIDATE — NOT YET MERGED · IMPLEMENTATION NOT AUTHORIZED · P4-1b-2a NOT STARTED`;
**that state is superseded — P4-1b-2a is now IMPLEMENTED / MERGED / VERIFIED / ACCEPTED / CLOSED (PR #365; see the
"Active contract" status above).** **P4-1b-2b, P4-2, Phase 5 remain NOT AUTHORIZED / NOT STARTED.** Owner decisions govern
`D-P4-1B-2-01 … -14` (unchanged) plus the REV1 corrections `D-P4-1B-2-REV1-B1/B2/B3` and clarifications
`D-P4-1B-2-REV1-C1 … C8` in `OWNER_DECISION_REGISTER.md`.

**2. Objective (unchanged).** Prove durable accepted-answer evidence: durably append each answered-submission
accepted-input event exactly once, persist-before-acknowledge, with mandatory web-layer idempotency — no full session/
progression/deliverable/output/Keep-Refine/account durability, no replay (P4-2).

**B1 — Mandatory token & affected existing tests (correction).** A server-issued token is **mandatory for every
answered submission**; **no tokenless fallback** is permitted (a POST resolving to `answered` without a valid token
fails closed, generic behaviour, no acceptance). The future implementation MUST enumerate and update **only** the
existing test files that genuinely POST answered submissions, **solely to obtain and submit a real valid token**, with
**no weakened assertion, no skipped behaviour, and no conftest auto-injection of tokens** (auto-injection would create a
false-green path and is prohibited). **Enumerated affected test paths (evidence, live tip):** `test_web_app.py`,
`test_p4_1b1_runtime_project_persistence.py`, `test_security_containment_r6_r16.py`, `test_increment_1a_actions.py`,
`test_structured_criticality.py`, `test_success_criteria.py`, `test_gux_snapshot_decision.py`,
`test_s04_guided_answer_validation.py`, `test_actionable_validation_plan.py`, `test_advisory_panel_precedence.py`,
`test_deliverable_hygiene.py`, `test_domain_gate_entry_ux.py`, `test_guided_answer_coauthoring_increment_1.py`,
`test_guided_uncertainty_support.py`, `test_layer1_feedback_wording.py`, `test_more_detail_needed_scaffolding.py`,
`test_plain_language_result_feedback.py`, `test_requirement_landscape_synthesis.py`,
`test_unified_risk_safety_presentation.py`, `test_acknowledged_unknown_fragment_capture.py`,
`test_causal_connective_substance_gate.py` (final set re-verified at the implementation gate). **Any answered-producing
test path not identified by evidence → STOP — CONTRACT AMENDMENT REQUIRED.**

**B2 — Token transport on every answered-producing form (correction).** Token transport MUST cover **every** form whose
POST resolves to `answered`. Verified answered-producing forms (`web/templates/session.html`): (i) the **main answer
form** (`name="response"` + `action=answered`); (ii) the **criticality-correction free-text form**, whose POST carries
**no `action` field** and is therefore treated as `answered` by the legacy-compatibility rule in
`web/app.py::submit_answer`. Both MUST carry a hidden server-issued token. The contract REQUIRES an **inventory/route-form
regression** proving **no answered-producing form bypasses the token requirement** (fail closed if any does).

**B3 — Downstream `evt-*` semantic consequences (correction; CONTRACT AMENDMENT / OWNER DECISION REQUIRED).** A
token-derived event id (`evt-*`) replacing the positional `rec_N` on an accepted answered record is **NOT semantically
neutral**. Static evidence at the live tip:
  * `engine/idea_development_outputs.py::_record_sort_key` (`_REC_ID_RE = ^rec_(\d+)$`): `rec_N` ids receive tuple lead
    **0** (numeric order) and **always precede** non-`rec_N` ids (lead 1/2). An `evt-*` answered record therefore sorts
    differently, **changing which record `_select_record` picks** for the deterministic next-development-step output.
  * `engine/requirement_landscape.py`: mirrors the same `rec_N` sort key (`_rec_sort_key`) **and embeds `record_id` into
    derived identifiers and metadata** — `requirement_id = _record_id_prefix(kind) + record.record_id` (e.g.
    `req:assertion:rec_3` → `req:assertion:evt-…`), `anchor_reference`, `ResolvingAction`, and contradiction-pair
    ordering (`_order_pair`). `evt-*` ids therefore **change derived requirement identifiers, rationale metadata, and
    pair ordering** — deterministic outputs.
The contract REQUIRES **protected regression tests for mixed `rec_N` / `evt-*` ledgers and deterministic output
behaviour**. **Because static inspection already demonstrates a material change, this contract does NOT authorize the
`evt-*` id scheme for implementation.** **DETERMINATION: CONTRACT AMENDMENT / OWNER DECISION REQUIRED** before P4-1b-2a
implementation — the owner must choose one of: **(a)** explicitly accept the changed deterministic output (owner
decision + regenerated golden expectations); **(b)** authorize a **bounded engine amendment** so durable event ids are
order-equivalent to `rec_N` and embed acceptably in `idea_development_outputs.py`/`requirement_landscape.py`; or
**(c)** adopt an idempotency design that keeps `rec_N` as the identifier consumed by the derived-output engines. **The
semantic change must NOT be silently normalized or accepted.** *(This corrects the original candidate's erroneous
"STABLE RECORD-ID FEASIBILITY: PASS — no amendment".)*
>
> **[SUPERSEDED / RESOLVED — see “P4-1b-2a Contract Amendment — G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01” below.]** The
> owner has formally **SELECTED OPTION A**: the deterministic engine `record_id` **stays `rec_N` (unchanged)**, and a
> **SEPARATE durable idempotency identity** (distinct from `record_id`) is introduced. The `evt-*` scheme is therefore
> **NOT adopted as `record_id`**, and the derived-output engines (`engine/idea_development_outputs.py`,
> `engine/requirement_landscape.py`) are **NOT changed**. Options **(b)** and **(c)** above are recorded **REJECTED**
> (reasons in the amendment). This resolution introduces a **bounded `engine/record_store.py` storage amendment**, so
> stable idempotency is **NOT a web-layer-only change**.

**Clarification C1 — Web-layer staging (D-P4-1B-2-REV1-C1).** On an answered submission the implementation MUST: clone
the live `IdeaState`; run evaluation and create the `AssertionRecord` on the **staged copy**; set the canonical event
id; **append durably**; and **only after durable success** publish staged state, transcript, and `last_result` into
`SESSION_STORE`. On append failure it MUST discard the staged copy and leave live memory unchanged (persist-before-ack;
no partial publication).

**Clarification C2 — Duplicate retry (D-P4-1B-2-REV1-C2).** A duplicate valid-token retry MUST cause: no second durable
event; no second progression; no reconstructed `last_result`; no claim of reproducing the prior response; a no-op with a
`show_session` redirect where truthful, otherwise a generic redirect.

**Clarification C3 — IntegrityError handling (D-P4-1B-2-REV1-C3).** No `sqlite3.IntegrityError` may be **automatically**
classified as a duplicate. On IntegrityError the runtime MUST reload the durable contract and confirm the **exact event
id, same project, and same logical accepted content** before treating it as an idempotent duplicate. **Same token with
different content fails closed.** Unrelated integrity failures remain **generic store failures** (fail closed).

**Clarification C4 — Concurrency boundary (D-P4-1B-2-REV1-C4).** The bounded MVP relies on the existing
`threaded=False` single-process/single-thread serving topology (G-P4-1B-1-AMEND-01); the store **primary key is the
durable duplicate backstop**; multi-thread/multi-worker behaviour is **out of scope**.

**Clarification C5 — Canonical token/event-id model (D-P4-1B-2-REV1-C5).** A **cryptographically strong** server-issued
token; **URL/form-safe bounded** encoding; **exact-match** validation; **hidden-form transport only**; **never** placed
in URLs, logs, or user-facing errors. **One precise digest model is chosen: the canonical durable event id is
`evt-` + hex SHA-256 of (`sid` ‖ separator ‖ raw token), truncated to a bounded length** — i.e. the raw token is
**hashed, not stored raw**, and **`sid` is included in the canonical derivation** so the event id is project-bound.
*(This id scheme is subject to the B3 amendment/owner decision above before implementation.)*
> **[AMENDED — see G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01 below.]** Under the selected **Option A**, this hashed,
> project-bound, token-derived value is the **SEPARATE durable idempotency identity** — it is **NOT** the engine
> `record_id` and is **NOT** rendered as an `evt-*` `record_id`. The `record_id` remains the positional `rec_N`
> produced by `engine/idea_state.py`. The precise raw-vs-hash-vs-HMAC form, encoding, and truncation bound are refined
> by the amendment and remain an **implementation-gate decision**, not locked here.

**Clarification C6 — Durable-success / memory-failure (D-P4-1B-2-REV1-C6).** If the durable append succeeds but the
in-memory publish fails: the durable ledger remains authoritative; the temporary `SESSION_STORE` entry is invalidated;
the runtime redirects safely; it does **not** continue from partially published progression, does **not** append again,
and does **not** claim replay or exact resume.

**Clarification C7 — Pre-append scanning (D-P4-1B-2-REV1-C7).** A full-ledger `load_contract(sid)` load/scan is
acceptable for this bounded MVP and is recorded as **O(n)**; **no `project_ids()` exposure**; a direct-record lookup
optimization is **deferred**.

**Clarification C8 — Mixed-id state (D-P4-1B-2-REV1-C8).** Durable `evt-*` answered records may coexist with legacy or
volatile `rec_N` non-answer records; **protected regressions MUST cover this mixed-id state** (feeds directly into B3).

**Ordering / failure / reconciliation / restart / product-truth (unchanged from DOC-01, retained):** store `seq`
ordering, one accepted event per token, no cross-project append; the ten-case failure model with generic non-disclosing
errors and no raw SQLite/user-content logs; durable-authoritative reconciliation; restart guarantees ledger + fresh
readiness only (no progression/deliverable restore — P4-2); product may claim only **durable accepted-answer evidence**
and must not claim saved project / fully saved idea / durable outputs / "resume exactly where you left off" / complete
session resume / Keep-Refine durability / account-owned records.

**Permitted paths (future implementation).** `web/app.py`; `web/templates/session.html` (hidden token field on **both**
answered-producing forms — B2); ONE focused test module `tests/test_p4_1b2a_durable_answer_append.py` (new);
`tests/conftest.py` (reuse only — **no token auto-injection**); and the **enumerated B1 existing test files** updated
**only** to obtain/submit a real token without weakening assertions. **Prohibited (unless a separately reviewed
amendment authorizes):** `engine/idea_state.py`, `engine/record_store.py`, `engine/record_contract.py`,
`engine/derived_readiness.py`, `engine/idea_development_outputs.py`, `engine/requirement_landscape.py`,
`engine/deliverable_assembler.py`, `requirements.txt`, `pytest.ini`, `database/`, `schemas/`, migrations; accounts/
auth/ownership; outputs; replay; durable Keep/Refine; retention/deletion; local-dev permission hardening; P4-1b-2b;
P4-2; Phase 5. **NOTE:** the B3 resolution may require an authorized amendment touching
`engine/idea_development_outputs.py` and/or `engine/requirement_landscape.py`; that is a **separate** authorization, not
granted here.
> **[AMENDED — see G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01 below.]** Under the selected **Option A** the B3 resolution does
> **NOT** touch `engine/idea_development_outputs.py` or `engine/requirement_landscape.py` (the derived-output engines are
> left unchanged because `record_id` stays `rec_N`). Instead it introduces a **bounded, additive
> `engine/record_store.py` storage amendment** for the separate durable idempotency identity (evaluated — not locked — as
> an additive nullable column + uniqueness constraint, or a sibling table). That storage amendment is a **separate future
> implementation authorization**, not granted by this documentation-only gate.

**RED / GREEN (corrected).** RED-1…11 (DOC-01) **plus**: RED-B1 an answered POST without a valid token **fails closed**
(no acceptance); RED-B2 an inventory/route-form test proves **no answered-producing form** (main + criticality-correction)
bypasses the token; RED-B3 mixed `rec_N`/`evt-*` ledger **deterministic-output** regressions (next-development-step
selection + derived requirement identifiers) — these are **gating**: if they demonstrate a material change (as static
analysis indicates), implementation STOPS pending the B3 amendment/owner decision; RED-C3 IntegrityError is **not**
auto-classified as duplicate (same-token-different-content fails closed). GREEN additionally requires: real token
lifecycle end-to-end; staging (C1) with persist-before-publish; idempotent retry (C2) with no second event/progression;
IntegrityError confirmation-by-reload (C3); no false-green via conftest/`SESSION_STORE`; protected regressions incl.
mixed-id (C8) pass **only** under an owner-approved B3 resolution; full governed suite green.

**Preserved (unchanged by REV1):** decision **D17**; the **AISR seven-owner model**; the original `0e2a5ce` candidate and
its verdict-C history; all P4-1b-1 implementation-review and post-closure documentation observations (closure
"pending its own merge" now satisfied by PR #361; non-material tree-attribution note; stale "current" wording;
authorization-record lag) — recorded, not fixed here. **P4-1b-2b, P4-2, Phase 5–7, WS17, STG** remain **NOT
AUTHORIZED**.

---

## P4-1b-2a Contract Amendment — G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01 (B3 OWNER DECISION = OPTION A) — MERGED (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE; the Option-A decision below remains authoritative, but its "not authorized / not merged" status is superseded — P4-1b-2a is IMPLEMENTED / MERGED / CLOSED via PR #365)

**A0. Provenance & preservation.** This amendment amends the merged **P4-1b-2a REV1** contract candidate
(`G-P4-1B-2-DOC-01-REV1`, above) **only** to correctly incorporate the owner's B3 decision. The REV1 candidate and all
prior candidates, verdict-C history, clarifications `C1…C8`, and preserved observations remain **intact and preserved**;
this amendment supersedes **only** the specific B3 `DETERMINATION` (the "(a)/(b)/(c) owner-decision-required" outcome),
the C5 event-id parenthetical, and the Permitted/Prohibited paths NOTE — each flagged inline above. Authored on the
authoritative live tip resolved from Git (`origin/feature/atomic-json-session-persistence`); this gate mints its own
newly generated commit/tree/bundle SHAs and reports them honestly. A previously claimed
`518cfdfe0eca3fb0f52c88c5baea46c643d3c288` artifact remains **not an established repository artifact** and is not relied
upon.

**A1. Gate identity & status.** Gate **G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01**. **Type:** documentation-only contract
amendment preparation. **Status (HISTORICAL PRE-IMPLEMENTATION CONTRACT STATE):** at amendment-preparation time this read
`CONTRACT AMENDMENT CANDIDATE — NOT YET MERGED · IMPLEMENTATION NOT AUTHORIZED · P4-1b-2a NOT STARTED`; **that state is
superseded — the amendment is merged and P4-1b-2a is IMPLEMENTED / MERGED / CLOSED (PR #365).** The Option-A decision
recorded here remains authoritative. As authored, this gate recorded an owner decision and corrected the contract text; it authorized **no** push,
PR, merge, code/engine/schema/test/template change, or phase activation. **P4-1b-2b, P4-2, Phase 5+ remain NOT
AUTHORIZED / NOT STARTED.** Governing decision: `D-P4-1B-2A-B3-01` (Option A selection) plus the retained
`D-P4-1B-2-REV1-*` decisions in `OWNER_DECISION_REGISTER.md`.

**A2. B3 OWNER DECISION — OPTION A SELECTED (binding).** The owner formally **SELECTED OPTION A: SEPARATE THE DURABLE
IDEMPOTENCY IDENTITY FROM THE DETERMINISTIC ENGINE `record_id`.** Concretely:
  * The engine **`record_id` remains the positional `rec_N`** produced by `engine/idea_state.py`
    (`record_id = f"rec_{len(self.assertions)+1}"`). It is **unchanged** in value, format, creation site, ordering role,
    and every derived-identifier consumer.
  * A **SEPARATE durable idempotency identity** (the server-issued-token-derived value) is introduced and stored
    **separately** from `record_id`. It is the durable duplicate/idempotency backstop **only**; it is **never** consumed
    by the deterministic derived-output engines and is **never** rendered as an `evt-*` `record_id`.
  * **Option B REJECTED:** engineering a durable event id that is "order-equivalent to `rec_N`" and embeds acceptably in
    `idea_development_outputs.py`/`requirement_landscape.py` enlarges the deterministic-engine blast radius, couples the
    idempotency key to sort/derivation semantics, and risks silent semantic drift — contrary to the governance contract.
  * **Option C REJECTED:** "keep `rec_N` in the derived path" while still deriving the idempotency key **from** `rec_N`
    conflates two concerns (positional identity vs. request-idempotency) and provides no unpredictable, request-bound,
    replay-safe idempotency guarantee. Option A keeps `rec_N` in the derived path **and** gives idempotency its own
    identity — a strict superset of C's benefit with none of the conflation.

**A3. Correction of the "web-layer-only / no-amendment" implication (mandatory).** Any statement — in REV1 or earlier —
implying that stable/durable idempotency is a **web-layer-only** change, or that **no engine/storage amendment** is
required, is **INCORRECT and is hereby superseded.** Evidence at the live tip: `engine/record_store.py` `records` table
is `PRIMARY KEY (project_id, record_id)` with **no** idempotency/token column and no separate uniqueness constraint for a
request-idempotency identity. Storing a **separate** durable idempotency identity therefore **requires a bounded,
additive `engine/record_store.py` storage amendment.** Option A is **not** implementable in the web layer alone.

**A4. Two separate identity concepts (normative definitions).**
  * **Deterministic engine `record_id` (`rec_N`)** — positional, append-only, assigned by `engine/idea_state.py`;
    consumed by ordering (`_record_sort_key` / `_rec_sort_key` lead-0 precedence), derived requirement identifiers
    (`req:assertion:rec_N`), anchors, rationale metadata, contradiction-pair ordering, and other `record_id` consumers.
    **Unchanged by Option A.**
  * **Durable idempotency identity** — a separate, server-issued-token-derived value bound to a single accepted
    answered-submission request; its sole role is to make durable append **idempotent** (exactly-once) and to detect
    duplicate retries. It is **not** an engine identifier, **not** an ordering key, and **not** embedded in any derived
    output. It lives in the storage amendment (A9), not in `record_id`.

**A5. Token & security requirements (implementation-gate contract).** The idempotency token MUST be:
  * **server-issued** (never client-supplied as authority), **cryptographically strong / unpredictable**, of a
    **bounded, sufficient length**, and **URL/form-safe**;
  * **bound** to project/session (`sid`) and to the specific answered **operation** (one accepted answered submission);
  * **single-use for acceptance** — a valid token accepts at most one durable answered event;
  * transported **only** via a hidden server-issued form field on the answered-producing forms (A7); **never** placed in
    URLs, logs, analytics, or user-facing errors;
  * subject to a defined **lifecycle/expiration** (issued with the form render; consumed on acceptance; re-issued for a
    fresh legitimate submission);
  * **raw-vs-hash-vs-HMAC storage form is an explicit implementation-gate decision that remains REQUIRED** — the
    amendment records the requirement (do not store a reversible secret unnecessarily; prefer a one-way/keyed digest for
    the stored idempotency identity) but does **not** finalize the exact digest/keying here.
  * **Rejection contract (fail closed):** a **missing**, **malformed**, **expired**, **cross-session**, or
    **cross-project** token MUST cause a fail-closed, generic, non-disclosing rejection with **no** durable append and
    **no** acceptance. There is **no tokenless fallback** (retained from B1).

**A6. Uniqueness & payload binding.** The durable idempotency identity's uniqueness is scoped to
**(project + idempotency identity + operation)**. The durable record MUST bind the idempotency identity to a
**normalized fingerprint of the accepted-request content**, so that:
  * **same token + same normalized request** → return the **prior** durable result (no second event, no second
    progression, no reconstructed `last_result`, no replay claim) — an idempotent no-op (retains C2);
  * **same token + different request content** → **fail closed** (retains C3: never auto-classify an IntegrityError as a
    duplicate; confirm exact identity + same project + same logical content by reload before treating as duplicate);
  * uniqueness is enforced **durably** (storage-level constraint, A9), not only in the web layer.

**A7. Both answered-producing forms (retained B2).** The hidden idempotency token MUST be carried by **every**
answered-producing form in `web/templates/session.html`: (i) the **main answer form**; (ii) the **criticality-correction
free-text form** (which posts no `action` and is treated as `answered` by the legacy rule in `web/app.py`). An
inventory/route-form regression MUST prove **no** answered-producing form bypasses the token.

**A8. Persist-before-acknowledge ordering (retained C1/C6).** On an accepted answered submission the implementation MUST
stage evaluation on a cloned `IdeaState`, create the `AssertionRecord` (with its **`rec_N`** `record_id`) and the
**separate** durable idempotency identity, **append durably**, and **only after durable success** publish staged state /
transcript / `last_result` into `SESSION_STORE`. On append failure it discards the staged copy and leaves live memory
unchanged. Durable-success / memory-failure invalidation follows C6.

**A9. Storage amendment — likely-owner `engine/record_store.py` (evaluated, not locked).** The separate durable
idempotency identity requires a **bounded, additive** amendment to `engine/record_store.py`. Two shapes are recorded as
**candidates to evaluate at the implementation gate** — the schema is **NOT locked here**:
  * **(i)** an **additive nullable column** on `records` (e.g. an `idempotency_key` / `idempotency_fingerprint`) plus a
    **partial/nullable UNIQUE constraint** scoped to `(project_id, idempotency_key)` for non-null keys; **or**
  * **(ii)** a **sibling table** keyed by `(project_id, idempotency_key)` referencing the owning record, with its own
    UNIQUE constraint.
  In **both** shapes: the existing `PRIMARY KEY (project_id, record_id)` and `rec_N` semantics are **unchanged**;
  legacy/volatile `rec_N` non-answer records and pre-amendment rows carry a **NULL** idempotency identity and remain
  valid (mixed-state, retains C8); the change is **additive only** (no column drop, no type change, no `rec_N`
  rewrite). Selection between (i) and (ii) and the exact constraint form is a **separate implementation-gate decision**.

**A10. Migration & rollback (against the live DB mechanism).** Because a durable SQLite store already exists, the storage
amendment MUST specify a **real forward migration** against the live schema (additive column/constraint or new table,
applied idempotently to existing databases) and a **defined rollback** that is safe on populated databases — **not**
"just drop the column." Rollback MUST preserve existing `records`/`rec_N` data and MUST NOT corrupt or orphan durable
answered evidence; where a physical drop is unsafe, rollback is specified as **disable-and-ignore** (stop enforcing/
reading the idempotency identity) rather than destructive removal. Exact migration/rollback mechanics are an
implementation-gate deliverable.

**A11. RED test contract & false-green prohibitions (retained + extended).** The future implementation remains **RED-first
and behavior-based**. Required RED coverage: **RED-B1** answered POST without a valid token **fails closed**; **RED-B2**
inventory/route-form regression proves no answered-producing form bypasses the token; **RED-A6** same-token+same-request
→ idempotent no-op (one durable event), same-token+different-request → fail closed, duplicate retry produces no second
event/progression; **RED-A9** durable uniqueness is enforced at the storage layer (constraint proven, not only web-layer
guarded); **RED-C8/mixed-id** `rec_N` answered/non-answer records with NULL idempotency identity coexist with
idempotency-bearing records and deterministic derived output (**`rec_N` ordering, `req:assertion:rec_N` identifiers,
pair ordering**) is **unchanged** (this is now a *stability* assertion, since Option A leaves the derived engines
untouched). **Prohibited false-green paths:** no conftest token auto-injection; no weakened/skipped assertions in the
enumerated B1 existing tests; no reliance on `SESSION_STORE`/replay to simulate durability; no recomputation of
pass/fail outside real behavior. Replay greenness is not proof.

**A12. Logging & observability.** The idempotency token and any raw user answer content MUST NOT appear in logs, error
messages, analytics, or URLs. Observability is limited to non-sensitive, non-disclosing signals (e.g. accepted / duplicate
no-op / fail-closed **counts or generic markers**) sufficient to prove the idempotency behavior without leaking secrets or
user content.

**A13. Explicit exclusions (unchanged scope walls).** This amendment does **NOT** authorize: any change to the engine
`record_id` / `rec_N` scheme; adoption of the `evt-*` id as `record_id`; P4-1b-2b; P4-2 (replay / durable output /
stale-output / full session resume); Phase 5 (accounts, ownership, sharing, permissions); any FPC (FPC-01…FPC-04);
PDF / Email / STG / WS17 / ACV; any event-bus or general-idempotency abstraction; retention/deletion/permission
hardening; multi-thread/multi-worker concurrency (C4 `threaded=False` topology retained). No downstream activation is
implied; closing this gate activates nothing.

**A14. Product-truth boundary (unchanged).** Even after implementation, P4-1b-2a may claim only **durable accepted-answer
evidence** with re-derivable readiness; it does **not** restore progression, deliverable, outputs, or Keep/Refine, and
does not claim a saved project / fully saved idea / durable outputs / "resume exactly where you left off" / complete
session resume / account-owned records.

**Boundary.** This is a documentation-only contract amendment. **No implementation authority is granted.** P4-1b-2a
implementation still requires: this amendment independently reviewed and merged; a separate explicit implementation
authorization; and RED-first behavior-based proof. Append-only governance; prior candidate history preserved.

---

## P4-1b-1 Increment Contract Candidate (CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED)

**1. Gate identity & status.** P4-1b-1 — Runtime Store Construction and Durable Project Create/Load (the first
runtime-integration sub-increment of P4-1b, itself the first runtime half of P4-1). Produced under gate
**G-P4-1B-1-DOC-01** on live tip `e4f9cd97e1b4329b98f1678412a6a36b9d7238bf` (Merge PR #357; always re-resolve from Git).
**Status:** `CONTRACT CANDIDATE ONLY` · `IMPLEMENTATION NOT AUTHORIZED` · `P4-1b-1 NOT STARTED`. This block authorizes
no `web/app.py` change, no test, no database creation/opening, no dependency, and no runtime work. It governs the
future P4-1b-1 increment only after independent review (Lean §5, genuinely separate session), owner acceptance,
publication, merge, post-merge verification, and a **separate explicit P4-1b-1 implementation authorization**.

**2. Authorized objective (future implementation).** Prove, through the application boundary, that a **new project is
durably created at `/start`, survives a real process/store restart, and is cold-loaded back into runtime** from the
merged P4-1a durable store (`engine.record_store.SqliteRecordStore`) via the P4-0 record contract — while preserving
the existing generic unavailable behaviour and R6/R16 containment. The future implementation may ONLY: construct the
store at application startup; resolve the SQLite path safely; create a durable empty/new project during `/start`;
use the **`sid` as the durable `project_id`** (one unified capability); load a durable project after memory loss via
**`load_contract(sid)`**; rebuild minimum runtime state; preserve generic unavailable behaviour; translate storage
errors at the web boundary; and prove real restart/cold-load behaviour. Nothing else.

**3. Owner decisions (recorded; governs D-P4-1B-01 … D-P4-1B-11 in `OWNER_DECISION_REGISTER.md`).**
- **D-P4-1B-01 Split:** P4-1b = **P4-1b-1** (Runtime Store Construction + Durable Project Create/Load) + **P4-1b-2**
  (Accepted-Input Append + Keep/Refine Runtime Integration). Each requires a separate contract, separate implementation
  authorization, RED/GREEN evidence, independent review, owner publication decision, owner merge decision, post-merge
  verification, and formal closure. **P4-1b-2 is NOT authorized by this gate.**
- **D-P4-1B-02 Runtime state model:** for the current MVP, `SESSION_STORE` remains the active in-memory state during a
  live process; **SQLite is the durable mirror and cold-reload source**; when memory is absent and a durable project
  exists, state may be rebuilt from `load_contract(sid).to_state()` (the `sid` IS the durable `project_id`);
  **readiness must always be derived again**;
  **no cache framework or invalidation platform is authorized**. If durable persistence fails, the application must not
  present the in-memory state as successfully durable.
- **D-P4-1B-03 Store lifecycle:** **one application-scoped `SqliteRecordStore` instance** for the current
  single-process MVP. Explicitly defer multi-worker topology, connection pools, per-request connection architecture,
  WAL tuning, production database selection, and provider-managed databases. SQLite remains a reference/MVP adapter.
- **D-P4-1B-04 Configuration:** use **`INVENTORAI_DB_PATH`**. Local/test execution may use a safe explicit file path;
  **pytest must use test-managed temporary directories**; **no repository-tracked `.db`/`.sqlite`/user-data file is
  permitted**; **production must fail fast** when the path is missing, unusable, or unsafe; **no new runtime
  dependency**. The exact local default must be specified truthfully and must not write user content to an uncontrolled
  `/tmp` transcript path (R6).
- **D-P4-1B-05 Durability start policy:** P4-1b-1 durability applies to **newly created projects only**. Existing lost
  in-memory sessions are **not recoverable, not migratable, and must not be claimed restorable**. Promotion of
  already-live pre-integration sessions is **excluded** from the first increment.
- **D-P4-1B-06 Unified pre-account capability identifier (correction, BF-1):** for P4-1b-1, **`sid` and the durable
  `project_id` are the SAME `uuid4` value** — one unguessable pre-account capability used for route/session lookup,
  durable project lookup, and cold-load after process restart. The route capability IS the durable project key:
  **cold-load calls `load_contract(sid)`**; **no separate `sid`→`project_id` mapping table, no scan through
  `project_ids()`, and no derived/reversible mapping layer is introduced**. It is **lookup only** — not authentication,
  ownership, account authorization, or verified identity. **`project_ids()` must never be exposed** through route, API,
  template, UI, or user-facing runtime behaviour. This capability model is temporary before Phase 5 (which may later
  introduce account ownership and a separately governed external/public identifier model). P4-1b-1 does **not** use
  `new_record_id()` (accepted-input record creation is P4-1b-2). **No modification to `engine/record_store.py` or
  `engine/record_contract.py` is required by this model** (`create_project(contract, project_id=sid)` and
  `load_contract(sid)` are already supported by the merged P4-1a store).
- **D-P4-1B-07 Project creation order:** (1) validate the `/start` request; (2) generate **one** `uuid4` capability
  value used as **both** `sid` and `project_id`, plus an `idea_id`; (3) construct the initial `IdeaState`; (4) create
  the durable project through the store **with `project_id = sid`**; (5) **only after durable creation succeeds**,
  create the `SESSION_STORE[sid]` entry; (6) redirect to the session. On durable-creation failure: do not advertise or
  retain a successful live session; fail closed; show one generic unavailable response; log no user content.
- **D-P4-1B-08 Cold-load behaviour:** when a valid capability (`sid`) is presented and `SESSION_STORE` has no live
  entry: attempt **`load_contract(sid)`** (the `sid` IS the durable `project_id`); validate through the existing P4-0
  record contract; reconstruct `IdeaState` from the contract; derive readiness freshly; create only the minimum
  temporary runtime entry needed; **do not restore transcript or cached `last_result` as authoritative**. No
  `sid`→`project_id` mapping lookup and no `project_ids()` scan is used.
- **D-P4-1B-09 Error translation:** translate storage errors **at the web integration boundary**; **do not modify
  `engine/record_store.py` by default**. Minimum categories: `ProjectNotFound` → generic unavailable; malformed/
  unsupported contract → generic unavailable, fail closed; database unavailable/locked/path error → generic temporarily
  unavailable; unknown SQLite error → generic unavailable, fail closed. Permitted internal logging: error class,
  operation, non-content technical identifier when safe. Prohibited logging: idea text, answers, assertion payloads,
  serialized records, transcript content.
- **D-P4-1B-10 Generic non-disclosure:** the user-facing result must not reveal whether a project never existed, a
  capability was wrong, a project was deleted/unavailable, the database failed, the contract was malformed, or the
  contract version was unsupported. Use **one generic unavailable behaviour** consistent with existing session handling.
- **D-P4-1B-11 Product-truth boundary:** P4-1b-1 may prove durable creation of a **new** project, process-restart
  survival of that created project, and cold loading into runtime. It must **not** claim: accepted answers are durably
  persisted; Keep creates a durable snapshot; Refine is durably recorded; durable output exists; version history
  exists; recovery of existing temporary sessions; or that user ideas are fully saved. **Full accepted-input durability
  requires P4-1b-2.**

**4. Authorized paths for future implementation.** `web/app.py` (store construction at startup; `INVENTORAI_DB_PATH`
resolution; durable project creation in `/start`; `sid`↔`project_id` association; cold-load of a durable project;
minimum runtime-state rebuild; web-boundary storage-error translation; preserved generic unavailable behaviour;
**explicit single-threaded MVP serving mode `threaded=False` — G-P4-1B-1-AMEND-01 / D-P4-1B-1-AMEND-01**);
ONE focused test module — **`tests/test_p4_1b1_runtime_project_persistence.py`** (new); and, per
**G-P4-1B-1-AMEND-01 / D-P4-1B-1-AMEND-02**, **`tests/conftest.py`** (new) — authorized ONLY for a minimal pytest
isolated-DB fixture (see the "P4-1b-1 Contract Amendment" section below).

**5. Conditional paths.** A small new **configuration helper** (e.g. a `web/`-side path resolver) **only if** inline
configuration would make `web/app.py` unsafe or untestable — env-sourced with production fail-fast, mirroring the
existing `INVENTORAI_*` pattern; default is inline resolution and **no** new file. Existing tests
(`tests/test_web_app.py`, `tests/test_security_containment_r6_r16.py`) may be updated **only** to inject a temporary DB
safely; existing assertions must not be weakened.

**6. Prohibited paths (by default).** `engine/record_store.py`, `engine/record_contract.py`, `engine/idea_state.py`,
`engine/derived_readiness.py`, `requirements.txt`, `database/` (incl. dormant `supabase_schema.sql`), `schemas/`,
`pytest.ini`, templates/static files, `prompts/`, `domains/`, `scripts/`, `benchmark/`, CI/`.github/`/deployment files,
and any Phase 5 / P4-2 / P4-1b-2 / FDC-001 / provider path. **No new `sid`→`project_id` mapping module and no new
database table/schema are introduced** (the unified capability makes both unnecessary — D-P4-1B-06; the merged P4-1a
schema is reused unchanged). If implementation genuinely requires a prohibited or unlisted path → **STOP — CONTRACT
AMENDMENT REQUIRED**.

**7. Store lifecycle.** One app-scoped `SqliteRecordStore` constructed at startup over a real on-disk SQLite file
resolved from `INVENTORAI_DB_PATH`; single-process MVP; `close()` on teardown where applicable. Multi-worker/pooling/
WAL/production-datastore topology is explicitly deferred (D-P4-1B-03).

**8. Configuration rules.** `INVENTORAI_DB_PATH` env-sourced; safe explicit local/test path; pytest uses `tmp_path`;
**no repository-tracked database file**; production fail-fast on missing/unusable/unsafe path; **no new dependency**
(stdlib `sqlite3`); no uncontrolled `/tmp` user-content write (R6).

**9. Project creation ordering.** Exactly D-P4-1B-07 (validate → **one `uuid4` used as both `sid` and `project_id`**
(+ `idea_id`) → IdeaState → **durable create with `project_id = sid`** → `SESSION_STORE[sid]` entry → redirect),
durable-create as the commit point; fail closed with one generic response and no live session on failure.

**10. Cold-load behaviour.** Exactly D-P4-1B-08: **`load_contract(sid)`** (the `sid` IS the durable `project_id`) →
P4-0 validation → `to_state()` → fresh `derive_readiness` → minimum runtime entry; transcript and cached `last_result`
are never restored as authority; no mapping lookup or `project_ids()` scan.

**11. Source-of-truth model.** SESSION_STORE = active working cache within a live process; SQLite = durable mirror and
cold-reload source (keyed by the `sid`=`project_id` capability); readiness always re-derived; no cache-invalidation
framework and **no `sid`→`project_id` mapping module or table** (D-P4-1B-02, D-P4-1B-06). This is not P4-2 replay.

**12. Capability-isolation boundary.** A **single** unguessable `uuid4` used as both `sid` and `project_id` (no separate
identifier, no mapping); project-scoped store access; lookup/isolation only — **not** authentication/ownership/
authorization (Phase 5). `project_ids()` never exposed; cross-project isolation proved with two distinct capabilities.

**13. Error translation.** Exactly D-P4-1B-09 — at the web boundary; `record_store.py` unmodified by default; storage
errors mapped to generic user-facing responses; non-content technical logging only.

**14. Generic unavailable behaviour.** Exactly D-P4-1B-10 — one generic unavailable response consistent with the
existing missing-session redirect; never discloses project existence, capability validity, deletion, DB failure, or
contract/version state.

**15. Product-truth boundary.** Exactly D-P4-1B-11 — P4-1b-1 proves durable **new-project** create/restart-survival/
cold-load only; **no accepted-answer persistence, Keep/Refine durability, durable output, version history, session
recovery, or full-save claim** (all P4-1b-2 or later).

**16. RED criteria (behaviour-based; not written in this gate).** Each RED states its expected current failure, the
genuine missing capability, a false-RED control, and the prohibited shortcut.
- **RED-1** `/start` does **not** currently create a durable project. *Current failure:* no store call exists (grep-proven
  unwired). *Missing capability:* durable project creation at the boundary. *False-RED control:* assert a real row via a
  reopened store, not an in-memory dict. *Prohibited shortcut:* asserting only `SESSION_STORE` contents.
- **RED-2** a project does **not** survive clearing `SESSION_STORE` and reconstructing the app. *Failure:* in-memory
  state is lost on restart. *Missing:* durable persistence. *False-RED control:* **preserve only the route `sid` value**
  across restart; real store close + a new store on the same file; discard the original app/store/SESSION_STORE/
  IdeaState objects. *Shortcut:* reusing a module-global or stale memory.
- **RED-3** a cold request **cannot** currently load durable state. *Failure:* missing-sid redirects with nothing to
  load. *Missing:* cold-load path. *Control:* clear SESSION_STORE; create a fresh runtime/store; call the route with the
  **same `sid`**; prove **`load_contract(sid)`** restores the correct project. *Shortcut:* same-object reuse, a mapping
  table, or a `project_ids()` scan.
- **RED-4** failed project creation must **not** leave a live `SESSION_STORE` entry. *Failure:* no durable step, so no
  fail-closed ordering. *Missing:* create-before-advertise ordering + compensation. *Control:* inject a durable-write
  failure; assert no live entry and one generic response. *Shortcut:* swallowing the error.
- **RED-5** unknown project capability must remain **generic**. *Failure/known-good:* generic redirect exists; guard
  against regression. *Missing:* durable-missing path kept generic. *Control:* assert identical generic response.
  *Shortcut:* leaking existence.
- **RED-6** malformed or unsupported stored contract must **fail closed**. *Failure:* no load-validation path yet.
  *Missing:* fail-closed cold-load. *Control:* store a bad `contract_version`; assert generic unavailable, no traceback.
  *Shortcut:* 500/traceback or silent repair.
- **RED-7** database-unavailable behaviour must remain **generic**. *Failure:* no DB path/handling yet. *Missing:*
  boundary translation. *Control:* point at an unusable path; assert generic temporarily-unavailable. *Shortcut:* raw
  `sqlite3` error to the user.
- **RED-8** cross-project capability isolation must hold. *Failure:* project scoping not exercised at runtime. *Missing:*
  project-scoped cold-load. *Control:* create two projects; assert neither loads the other. *Shortcut:* shared id.
- **RED-9** readiness must be **freshly derived** after cold load. *Failure:* no reload path. *Missing:* re-derivation.
  *Control:* compare `derive_readiness` of the cold-loaded `to_state()` against a fresh derivation; never a stored value.
  *Shortcut:* persisting/restoring a readiness value.
- **RED-10** transcript and cached `last_result` must **not** be restored as authoritative. *Failure:* nothing durable
  yet. *Missing:* authoritative-input boundary. *Control:* assert the cold entry carries no restored transcript/
  last_result authority. *Shortcut:* persisting transcript (violates R6).
- **RED-11** **no repository-tracked database file** may be created. *Failure/guard.* *Missing:* safe path discipline.
  *Control:* assert the SQLite file lives only under `tmp_path`; `git status` clean of DB artifacts. *Shortcut:* writing
  a DB into the repo tree or uncontrolled `/tmp`.

**17. GREEN criteria (future implementation).** Real SQLite file in a pytest-managed temporary directory; `/start`
durably creates a new project keyed by the `sid`=`project_id` capability; the store connection and original runtime
objects are discarded; a **new** runtime/store instance opens the **same** database; `SESSION_STORE` begins empty; a
cold request **presenting the same `sid`** reconstructs the correct `IdeaState` via **`load_contract(sid)`** (no mapping
table, no `project_ids()` scan, no stale memory); readiness is newly derived; no transcript or cached result becomes
authoritative; failed durable creation creates no live session; unknown/malformed/unavailable conditions produce
**one** generic response; two capabilities cannot cross-load each other; **no `project_ids()` exposure**; **no new
dependency**; **no P4-1b-2 behaviour**; **full governed suite remains green**.

**18. False-RED & false-GREEN controls.** RED must fail for missing **behaviour**, not import/file absence, and must
not be satisfiable by an empty stub. **False-green is prohibited through:** reused `SESSION_STORE`; a reused `app`
instance when restart behaviour is claimed; a reused store connection; a reused `IdeaState` object; a mocked/fake
datastore; `:memory:` SQLite for restart proof; database-file-existence-only assertions; direct insertion of expected
state into `SESSION_STORE`; bypassing route behaviour by calling store methods only; **a `sid`→`project_id` mapping
table, a `project_ids()` scan, or any stale-memory substitute for `load_contract(sid)`**; or weakening existing
missing-session or security assertions. GREEN must exercise the **route** through Flask `test_client`, preserve **only
the `sid` value** across restart, actually close and reopen a **real** SQLite file, discard originals, and assert
reconstructed field equality.

**19. Security & privacy preservation.** Preserve **R6** (no transcript/user-content disk or log write) and **R16**
(env-sourced debug/secret, no hard-coded values, production fail-fast); no repository-tracked DB; generic
non-disclosure; project-scoped store access; malformed-record fail-closed on load; no provider/network call; no
auth/ownership overclaim. Deletion/retention, backup exposure, permissions hardening, and oversized-content DoS caps
are **deferred** (Phase 5 / production hardening) and out of P4-1b-1 scope.

**20. P4-1b-1 / P4-1b-2 / P4-2 / Phase 5 separation.** **P4-1b-1:** store construction + durable **new-project**
create/load + cold-load + web-boundary error translation — no accepted-input append. **P4-1b-2:** `append_record`
integration in `submit_answer`, durable accepted-input mutation, duplicate/retry handling, Keep/Refine runtime
integration. **P4-2:** deterministic replay, durable output records, stale-output invalidation, full re-evaluation.
**Phase 5:** accounts, authentication, ownership, verified email, account-linked authorization. All beyond P4-1b-1
remain separately gated and NOT AUTHORIZED.

**20a. Decision-trace clarification.** The P4-1b READ-ONLY DISCOVERY package identified **14** owner decisions. This
P4-1b-1 contract records only the decisions required for P4-1b-1 (D-P4-1B-01 … D-P4-1B-11 as corrected here). The
remaining discovery decisions — accepted-input append/write-path, duplicate/retry & idempotency,
supersession/contradiction mutation strategy, failure/compensation on the write path, and the Keep/Refine *durable*
behaviour — are **deferred to P4-1b-2 or later, not dropped**; they remain open and will be recorded when their gate is
authorized. Nothing here resolves or discards them.

**21. Test sequence (future implementation gate).** (1) focused P4-1b-1 RED tests; (2) focused GREEN tests;
(3) existing web-route tests (`tests/test_web_app.py`); (4) P4-1a store tests (`tests/test_p4_1a_record_store.py`);
(5) P4-0 record-contract tests (`tests/test_p4_0_record_contract.py`); (6) R6/R16 tests
(`tests/test_security_containment_r6_r16.py`); (7) protected regression tests; (8) full governed suite. No exact future
count is predicted; existing tests may be updated only to inject a temporary DB safely, without weakening assertions.

**22. Evidence-package requirements (future implementation gate).** Candidate SHA/parent/tree; changed paths; diffstat;
RED evidence (failing for the right reason, incl. a stub-still-fails demonstration); GREEN evidence (real restart/
cold-load round-trip through the route); full governed-suite result; no-new-dependency proof (`requirements.txt`
unchanged); `record_store.py`/`record_contract.py`/`idea_state.py`/`derived_readiness.py`-untouched proof; no
repository-tracked DB proof; bundle + sha256; §5A self-review.

**23. Independent-review requirement.** This candidate and the future P4-1b-1 implementation each require **formal Lean
§5 independent review in a genuinely separate session**; same-session self-review/subagents do not qualify.

**24. Owner publication & merge boundary.** Publication/PR/merge are owner-side (this environment's writes are
org-policy blocked). No push/PR/merge in this gate; the candidate stops at delivery.

**25. Mandatory stop.** On completion of this documentation candidate, stop; do not write RED tests or implementation
code; do not modify `web/app.py`; do not create/open a database; do not add a dependency; do not start P4-1b-1,
P4-1b-2, P4-2, or Phase 5.

### Reusable contract-template rendering
```
INCREMENT CONTRACT — P4-1b-1 Runtime Store Construction & Durable Project Create/Load   [CANDIDATE — NOT AUTHORIZED]
Objective:                Construct the merged P4-1a store at startup; durably create a NEW project at /start; survive
                          a real process/store restart; cold-load it back into runtime via the P4-0 contract — no
                          accepted-input append, no Keep/Refine durability.
Owner authorization:      G-P4-1B-1-DOC-01 (documentation-only candidate); implementation NOT authorized.
Risk level:               LEVEL 2 (bounded web/app.py runtime wiring + focused test; no engine/schema/dependency change).
Allowed paths:            web/app.py; tests/test_p4_1b1_runtime_project_persistence.py (new);
                          conditional web-side config helper only if inline config is unsafe/untestable;
                          existing web/security tests updated only to inject a temporary DB (no assertion weakening).
Forbidden paths:          engine/record_store.py, engine/record_contract.py, engine/idea_state.py,
                          engine/derived_readiness.py, requirements.txt, pytest.ini, database/, schemas/, templates/,
                          static/, prompts/, domains/, scripts/, benchmark/, CI/.github, P4-1b-2/P4-2/Phase 5 paths.
Expected behavior:        Durable new-project creation surviving restart; cold-load reconstruction; fresh readiness;
                          generic unavailable non-disclosure; R6/R16 preserved; no project_ids() exposure.
Non-goals:                Accepted-input append; Keep/Refine durability; duplicate/retry; relationship mutation;
                          transcript/last_result/output/readiness persistence; migration; accounts/auth; replay.
Acceptance criteria:      GREEN criteria (§17); false-RED/false-GREEN controls (§18); full-suite non-regression.
Required tests:           RED-1..RED-11 → GREEN; real restart/cold-load via Flask test_client; real tmp_path SQLite.
Tests not required:       Any provider/network/server-process test; exact future baseline count.
Dependencies:             P4-1a store (merged PR #356) + P4-0 contract (merged PR #353); stdlib sqlite3; NO new dep.
Unresolved decisions:     Whether a separate config helper is proved necessary (default: no).
Stop conditions:          Any need to modify a forbidden path or add P4-1b-2 behaviour → STOP — CONTRACT AMENDMENT REQUIRED.
Independent-review scope: Per §5; plus real restart/cold-load; no fake durability; create-before-advertise ordering;
                          generic non-disclosure; capability ≠ authorization; readiness never authoritative;
                          no accepted-input append; no P4-1b-2/P4-2/Phase 5 work.
Merge authority:          Owner, separately (not by the execution agent).
```

**Preserved (unchanged by this candidate):** decision **D17**; the **AISR seven-owner model**; **P4-1b-2, P4-2,
Phase 5–7, WS17, STG**, provider selection, and exact UX all remain **NOT AUTHORIZED**. The merged P4-1a and P4-0
artifacts are unchanged; this candidate wires nothing and creates no database.

---

## P4-1b-1 Contract Amendment — G-P4-1B-1-AMEND-01 (Threading & Pytest DB Isolation) — AMENDMENT CANDIDATE ONLY

**Status:** `AMENDMENT CANDIDATE ONLY` · `CORRECTION IMPLEMENTATION NOT AUTHORIZED` · `P4-1b-1 CORRECTION NOT STARTED`.
This is a **documentation-only** amendment to the P4-1b-1 Increment Contract above. It responds to the independent
review of implementation candidate `1eced7d280449b9c0842355a1882a9d3b731a633` (verdict **C — REVISE AND RE-REVIEW**)
and records the owner-approved contract corrections. It authorizes **no** edit to candidate `1eced7d`, `web/app.py`,
tests, runtime, dependency, database, publication, or a replacement implementation. The corrected implementation is a
**separate** future authorization (see "Correction-implementation boundary" below). Recorded on live tip
`b22f82ef1f7d08ce802ecbc52d68706d358fadb5` (Merge PR #358; always re-resolve from Git).

**Blocking findings addressed (contract-level only).**
- **B1 — Threading.** The merged P4-1a `SqliteRecordStore` owns one application-scoped `sqlite3` connection. Flask's
  built-in dev server is threaded by default, so serving requests through that shared connection across request threads
  is unsafe (`sqlite3` objects are thread-bound). The prior contract did not pin the serving mode.
- **B2 — Pytest DB isolation.** Governed tests outside the focused P4-1b-1 file that reach `/start` write project
  envelopes to the shared local-development default database instead of a pytest-managed temporary path.

**Owner decisions (recorded; govern D-P4-1B-1-AMEND-01 … D-P4-1B-1-AMEND-04 in `OWNER_DECISION_REGISTER.md`).**
- **D-P4-1B-1-AMEND-01 — Explicit single-threaded MVP serving mode.** For the bounded P4-1b-1 SQLite reference
  implementation, the Flask development/runtime entry point MUST explicitly use **`threaded=False`**, because the merged
  P4-1a `SqliteRecordStore` owns one application-scoped `sqlite3` connection that must not be used across request
  threads. The implementation MUST NOT rely on Flask's default threaded mode. **No change to `engine/record_store.py`;
  no `check_same_thread=False`; no connection pool, per-thread store, or per-request connection model.** Multi-threaded,
  multi-worker, and production-topology redesign remain deferred. **`threaded=False` is a bounded MVP decision, not a
  claim that Flask's built-in server is a production deployment architecture.**
- **D-P4-1B-1-AMEND-02 — Governed pytest database isolation.** All governed pytest execution that can reach P4-1b-1
  runtime-store creation MUST use test-managed isolated database files. This authorizes **`tests/conftest.py`** ONLY for
  a minimal fixture that: assigns `INVENTORAI_DB_PATH` to a unique pytest-managed `tmp_path`; prevents tests from writing
  to the shared local-development database; resets `SESSION_STORE`; **safely closes** an existing app-scoped store before
  replacing/resetting it; restores environment and runtime state after each test; introduces no production behaviour;
  weakens no existing assertion. The fixture MUST NOT: use a repository-tracked DB; use `:memory:` SQLite for
  durability/restart tests; expose `project_ids()`; persist transcripts or accepted-answer content; hide failures by
  mocking the store globally; or make tests order-dependent. **Focused restart tests continue using a real on-disk
  SQLite file under pytest-managed temporary storage.**
- **D-P4-1B-1-AMEND-03 — Threading regression proof.** The corrected implementation MUST include a focused regression
  proving the single-threaded serving boundary is explicitly configured and cannot silently regress to Flask's threaded
  default. The proof may use a narrowly bounded helper or run-entry test, but MUST NOT claim that `test_client` alone
  proves cross-thread safety. The evidence must also reproduce the reviewer's scenario (or an equivalent check)
  demonstrating that the corrected selected execution mode no longer serves requests through a shared SQLite connection
  across threads.
- **D-P4-1B-1-AMEND-04 — Local-development DB boundary.** The local-development default MAY remain under the system
  temporary directory ONLY for non-test, non-production development. Recorded truthfully: it **persists across local
  application runs until OS/user cleanup**; it **may contain durable project capability identifiers**; it is **not an
  account or ownership store**; **pytest must never use it**; and **P4-1b-2 must re-evaluate retention, permissions,
  deletion, and user-content implications** before adding accepted-input persistence. **Production still requires an
  explicit `INVENTORAI_DB_PATH` with fail-fast behaviour.**

**Amended implementation paths (supersede §4/§5 for the corrected P4-1b-1 implementation).**
- **Required / permitted:** `web/app.py`; `tests/test_p4_1b1_runtime_project_persistence.py`; **`tests/conftest.py`**
  (new — pytest isolated-DB fixture per D-P4-1B-1-AMEND-02 only).
- **Conditionally permitted:** narrowly necessary existing test files, ONLY when their setup must be adapted to the
  global isolated-DB fixture, **without weakening assertions**.
- **Remain prohibited:** `engine/record_store.py`, `engine/record_contract.py`, `engine/idea_state.py`,
  `engine/derived_readiness.py`, `requirements.txt`, `database/`, `schemas/`, `templates/`, `static/`, CI/deployment
  files. **Any engine-store threading redesign still requires a separate contract amendment.**

**Correction-implementation boundary (NOT authorized by this amendment).** After this documentation amendment is
independently reviewed, accepted, published, merged, and post-merge verified, a **separate** correction authorization
may permit a replacement implementation candidate that: (1) keeps candidate `1eced7d` intact as superseded evidence;
(2) starts from the then-live authoritative tip; (3) explicitly configures the Flask run entry as single-threaded;
(4) introduces the minimal `tests/conftest.py` isolated-DB fixture; (5) closes/resets stores safely in tests; (6) adds a
threading/run-mode regression; (7) re-runs RED/GREEN, protected regressions, and the full suite; (8) creates a new
commit and bundle; (9) undergoes a new independent review. **This amendment itself authorizes none of those changes.**

**Preserved observations (recorded, not expanded by this gate).** Cold-load route coverage is currently limited to the
normal session route (non-blocking for this increment); the restart proof was accepted as sufficient module-level
reconstruction under the current contract; explicit production-grade connection topology remains deferred; P4-1b-2
remains responsible for accepted-input append and related retention implications.

**Preserved (unchanged by this amendment):** decision **D17**; the **AISR seven-owner model**; the unified
`sid`==`project_id` model (D-P4-1B-06); candidate `1eced7d` is **preserved intact as superseded review evidence and is
NOT amended**; **P4-1b-2, P4-2, Phase 5–7, WS17, STG** remain **NOT AUTHORIZED**.

---

## P4-1b-1 Governance Closure Sync — G-P4-1B-1-CLOSURE-SYNC-01 (documentation-only) — GOVERNANCE CLOSURE CANDIDATE — NOT YET MERGED

**Status:** `GOVERNANCE CLOSURE CANDIDATE — NOT YET MERGED`. This documentation-only sync records the completed P4-1b-1
correction implementation, its independent review, merge, and post-merge verification, preserves the non-blocking
observations, and records a procedural deviation truthfully. It authorizes **no** code, test, runtime, dependency,
schema, database, UI, CI, release, deployment, or later-phase work. Recorded on live tip
`cbd0ce3046b24631c23e482dadd413aaa42dea05` (Merge PR #360; always re-resolve from Git).

**What was completed (evidence-first).**
- The P4-1b-1 **correction** implementation (threading + pytest DB isolation) was **separately owner-authorized** and
  built as candidate `3179cd556673e5c5b6b596a052b0744bddab011a` from authoritative base
  `ccb1f23fdd9f5cb1a318ec3cec1ca05248c04bae` (tree `f3ec086d845577a0b5befae019b4ebebdb2f7fcf`).
- The superseded first candidate `1eced7d280449b9c0842355a1882a9d3b731a633` (independent verdict C) **remains preserved
  intact and unmerged** as superseded evidence.
- Independent review of `3179cd5` returned **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**.
- **PR #360** merged the **exact reviewed candidate**; merge commit `cbd0ce3046b24631c23e482dadd413aaa42dea05`
  (parents `ccb1f23` + `3179cd5`).
- **Post-merge verification (independently reproduced):** candidate-ancestor check exit 0; changed exactly
  `web/app.py`, `tests/test_p4_1b1_runtime_project_persistence.py`, `tests/conftest.py`; diffstat **3 files / 497
  insertions / 2 deletions**; explicit **`threaded=False`** present in `web/app.py`; **pytest DB isolation via
  `INVENTORAI_DB_PATH`** present in `tests/conftest.py`; no engine path changed; no accepted-input persistence; no
  P4-1b-2 behaviour.
- **P4-1b-1 implementation:** MERGED AND POST-MERGE VERIFIED. **P4-1b-1 technical status:** COMPLETE.

**Procedural deviation (recorded truthfully, neutral language).** PR #360 was **merged before a separate explicit merge
authorization was issued in the conversation**. This was a **governance-process deviation**. It does **not** invalidate
the independently reviewed candidate or the successful technical post-merge verification, and repository evidence does
not indicate a security incident or technical defect. It **must not be normalized as precedent**: future gates must
preserve the separation among **publication authorization**, **PR-creation authorization**, **merge authorization**,
and **post-merge closure**. No wording in this record states or implies that a separate merge authorization existed
before the PR #360 merge; the owner **later** authorized this governance closure sync (G-P4-1B-1-CLOSURE-SYNC-01).

**Preserved non-blocking observations (recorded, not fixed).** (1) Committed authorization-record lag: the separate
correction-implementation authorization was owner-issued in conversation and is being recorded here at closure. (2) The
superseded candidate `1eced7d` was unavailable to the independent reviewer for byte-level verification. (3) The
author's protected-regression count (82) differed from the reviewer's equivalent set (83) due to set composition, not a
substantive discrepancy. (4) RED against `1eced7d` was not independently reproducible; base RED was used. (5) The test
helper returning zero on a SQLite error was a minor false-green risk, neutralized by external SQLite inspection. (6) The
RED-B2 path-string proof is weak alone but is backed by behavioural proof. (7) Local-development DB file permissions and
retained capability identifiers remain deferred to P4-1b-2. (8) A harmless `runpy` `RuntimeWarning` remains. (9) Legacy
ILT demo `/start` routes remain memory-only. (10) Cold-load route coverage remains limited to `show_session`. None is
silently deleted or marked resolved.

**Closure boundary.** **P4-1b-1 governance closure is PENDING** and becomes complete only after this
G-P4-1B-1-CLOSURE-SYNC-01 candidate is itself separately reviewed, published, PR-created, merged, and post-merge
verified. **P4-1b-2, P4-2, and Phase 5 remain NOT AUTHORIZED / NOT STARTED.** No durable claim about accepted answers,
outputs, or complete ideas is made. Decision **D17** and the AISR seven-owner model are preserved.

---

## P4-0 Historical Increment Contract Record — SUPERSEDED AS ACTIVE AUTHORITY

**Current interpretation:** the text below is preserved as the pre-implementation P4-0 contract candidate and
historical execution record. P4-0 has since been completed and formally closed through PR #353. Nothing in the
historical wording below reopens P4-0 or authorizes P4-1/P4-2.

## P4-0 Increment Contract Candidate (CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED)

**Gate identity:** P4-0 — Readiness and Storage-Contract Proof (first, provider-free proof increment of Phase 4).
**Status:** `CONTRACT CANDIDATE ONLY` · `IMPLEMENTATION NOT AUTHORIZED` · `P4-0 NOT STARTED`. This block is a
documentation-only candidate produced under gate **G-P4-0-DOC-01**; it authorizes no code, tests, contract module,
datastore, schema, migration, dependency, or runtime work. It governs the *future* P4-0 increment only after
independent review (Lean §5), owner acceptance, merge, post-merge verification, and a **separate explicit P4-0
implementation authorization**.

**Governing evidence (cross-reference, not duplicated):**
`docs/governance/PHASE_4_DURABLE_DATA_AND_EVIDENCE_ENTRY_DECISION.md` (Phase 4 entry decision; obligations
`P4-OBL-DATA-01`, `P4-OBL-PROV-01`, `P4-OBL-REEVAL-01`, `P4-OBL-OUTPUT-01`, `P4-OBL-LIFE-01`);
`POST_OUTPUT_AI_ASSISTED_SPECIALIST_REFINEMENT_CANONICAL_DECISION.md` (AISR seven-owner model; `AISR-OBL-P4-*`);
decision **D17** (full re-evaluation is the safe default; targeted partial re-evaluation prohibited); the accepted
planning gate **G-P4-0-CONTRACT-DEFINITION** and owner decisions **D-P4-0-01 … D-P4-0-10** recorded below.

### 1. Purpose
Establish and validate the minimum **provider-free, datastore-neutral record contract** able to represent the
accepted Phase 4 durable records and prove **lossless round-trip fidelity + invariants** before any datastore is
chosen. A proof increment — not persistence.

### 2. Non-goals (D-P4-0-01)
No real datastore; no durable persistence; no database integration; no migrations; no runtime wiring; no Phase 4
generally; no P4-1; no P4-2; no SQL/ORM/Supabase/Postgres/SQLite/Redis/object/cloud storage/credentials; no
`web/app.py`/route/session-migration; no accounts/auth/ownership; no file storage/backup/restore/DR;
no retention/deletion execution; no AI/provider/WS17/STG/domain/exact-UX/PDF/email/ACV/API/billing/deploy. The
dormant `database/supabase_schema.sql` is reference-only and must not be adopted or modified.

### 3. Governing owner decisions (as recorded)
- **D-P4-0-01** provider-free, datastore-neutral contract proof (non-goals above).
- **D-P4-0-02** representation: Python dataclasses + explicit `to_dict`/`from_dict` + JSON-compatible dicts + stdlib
  `json`; no external serialization library; no ORM/datastore model; minimal, reversible naming/organization.
- **D-P4-0-03** a `contract_version` identifier is required; unsupported versions **fail explicitly**; no silent
  acceptance/coercion/downgrade.
- **D-P4-0-04** distinguish (A) authoritative accepted source data that must survive round-trip exactly from (B)
  derived/cached data that must not be treated as source truth; derived readiness/deterministic conclusions must not
  be restored as authoritative facts.
- **D-P4-0-05** preserve current runtime provenance verbatim (`OWNER_STATED`, `LEGACY_UNSPECIFIED`); mapping to the
  future Phase 4 vocabulary is adapter-only and deferred to P4-1; P4-0 must not rewrite provenance, populate
  `AI_PROPOSED`/`USER_MODIFIED_AI_PROPOSAL`, or create a final migration mapping.
- **D-P4-0-06** prove contract-level invariants (round-trip fidelity, stable-id preservation, append-only
  preservation, provenance/validation preservation, valid supersession/contradiction references, rejection of
  unknown references / self-supersession / cyclic supersession, explicit unknown-version failure); no durable
  enforcement/storage.
- **D-P4-0-07** RED proves missing capabilities (RED-1…RED-6 below), not missing files.
- **D-P4-0-08** GREEN (14 criteria below) with the scope limit that **P4-0 does not prove full deterministic replay
  from accepted source inputs** (that is P4-2); P4-0 only proves readiness-relevant contract data survives round-trip
  and can seed a fresh `derive_readiness` call.
- **D-P4-0-09** authorized/prohibited paths (below); if implementation proves `idea_state.py` must change, STOP and
  request a contract amendment.
- **D-P4-0-10** next action = this documentation-only contract candidate; P4-0 implementation remains unauthorized
  until candidate complete → adversarial self-review → separate-session independent review → owner acceptance →
  publish/merge → post-merge verification → separate implementation authorization.

### 4. Exact proposed implementation paths (selected by convention; confirmed at the implementation gate)
- **AUTHORIZED PATH 1 (new):** one datastore-neutral engine contract module — proposed `engine/record_contract.py`
  (snake_case, consistent with `engine/*.py`).
- **AUTHORIZED PATH 2 (new):** one focused test module — proposed `tests/test_p4_0_record_contract.py`.
- **CONDITIONAL PATH:** one minimal package export (e.g. an `engine/__init__.py` line) **only if** direct-import
  conventions prove it necessary — evidence to date shows engine modules are imported directly
  (`from engine.<mod> import ...`), so **no export is expected or authorized** unless proved.

### 5. Prohibited paths (must remain untouched in P4-0)
`engine/idea_state.py`; `engine/derived_readiness.py`; `engine/decision_workspace.py`; `web/app.py`; `database/`;
`schemas/`; `migrations/`; `requirements.txt`; `pytest.ini`; `prompts/`; `templates/`; `static/`;
CI/configuration; `ACTIVE_EXECUTION_ROADMAP.md` (except later closure recording); any Phase 5–7, WS17, or STG path.
Any need outside AUTHORIZED PATH 1/2 (or a proved CONDITIONAL export) triggers: **STOP — CONTRACT AMENDMENT
REQUIRED.**

### 6. RED design (D-P4-0-07 — behavior-based; not written in this gate)
For each: name · intended API under test · expected pre-implementation failure · why it is a genuine missing
capability · false-RED control · DB-free · AI-free · prohibited workaround.
- **RED-1 `test_accepted_input_roundtrip_is_lossless`** — API: `record_contract.from_dict(to_dict(record))`.
  Expected failure: no lossless accepted-input round-trip capability exists (no `from_dict` today). Genuine: core
  accepted-source truth cannot be serialized/restored. False-RED control: assert the *behavior* (deep equality) via
  the intended API, not module import. DB-free ✓ / AI-free ✓. Prohibited workaround: satisfying it via
  `decision_workspace` export-only `to_dict`.
- **RED-2 `test_provenance_and_validation_preserved_through_roundtrip`** — provenance/validation not preserved by any
  canonical round-trip. Genuine: no serializer preserves them. Control: assert exact values, not presence.
- **RED-3 `test_supersession_and_contradiction_validated_after_restore`** — links not validated post-restore.
  Genuine: no reload path. Control: include valid+invalid link fixtures.
- **RED-4 `test_readiness_relevant_state_supports_fresh_derivation_after_restore`** — readiness-relevant state cannot
  be serialized/restored and fed to a fresh `derive_readiness`. Genuine: no serializer. Control: re-run
  `derive_readiness` on restored state; never restore a cached readiness value.
- **RED-5 `test_unknown_fields_governed_by_versioned_contract`** — unknown/unsupported fields not governed. Genuine:
  no versioned contract. Control: assert explicit handling (reject/segregate), not silent drop.
- **RED-6 `test_unknown_contract_version_is_rejected`** — unknown version not rejected. Genuine: no version handling.
  Control: assert explicit error on an unknown version string.

### 7. GREEN criteria (D-P4-0-08 — scope-limited)
(1) datastore-neutral versioned contract exists; (2) authoritative fields serialize to JSON-compatible data;
(3) authoritative fields restore losslessly (**deep equality + explicit field-coverage assertion**);
(4) stable identifiers preserved (not regenerated); (5) append-only history preserved; (6) provenance/validation
preserved verbatim; (7) supersession/contradiction references validated; (8) invalid references and cycles fail
safely; (9) unsupported versions fail explicitly; (10) unknown fields handled explicitly (not silently dropped);
(11) derived/cached conclusions not restored as authoritative; (12) **readiness freshly derived from restored
readiness-relevant state (no cached-readiness restoration)**; (13) no database/ORM/driver/provider/external
dependency introduced; (14) existing governed suite does not regress. GREEN must not require or permit a real
durable store, adapter, transaction, migration, or runtime wiring. Fixtures must be **non-trivial** (multiple
records, multiple provenance/validation values, at least one supersession and one contradiction).

### 8. P4-0 / P4-1 / P4-2 boundary
**P4-0 PROVES:** contract representation; version behavior; JSON-compatible round-trip; authoritative-field
fidelity; identifier preservation; relationship validation; datastore neutrality; fresh readiness derivation from
restored readiness-relevant state.
**P4-0 DOES NOT IMPLEMENT:** a durable repository; transactions; datastore adapters; runtime persistence;
session-to-project creation; durable migration; persistence isolation; persistence failure handling; full
deterministic replay from accepted source inputs.
**P4-1 OWNS:** real durable project + accepted-input storage; repository/store behavior; datastore adapter;
transactions; runtime integration; durable supersession behavior; actual migration; persistent isolation;
durability-safe identifier strategy (the current sequence-based `record_id = f"rec_{n}"` is not collision-safe
across reload/concurrency — P4-1 resolves this); provenance migration/mapping.
**P4-2 OWNS:** deterministic rebuild/replay from accepted source inputs; deterministic output records;
stale-output invalidation; complete full re-evaluation; proof that readiness/output can decrease or change after an
accepted revision.

### 9. Authoritative-vs-derived, provenance, versioning, identifier, and relationship rules
- **Authoritative (round-trip exact):** `idea_id`; the append-only `assertions` ledger (all `AssertionRecord`
  fields incl. `contradicts`/`supersedes`/`superseded_by`); `criticality_confirmations`; `success_criteria`;
  owner-stated Evidence. **Derived (recompute / non-authoritative):** `maturity_level`, `gaps[].status`,
  `derive_readiness` output, `last_result`.
- **Provenance:** preserved verbatim; mapping adapter-only and deferred (D-P4-0-05).
- **Versioning:** `contract_version` present; unknown versions rejected explicitly (D-P4-0-03).
- **Identifiers:** preserved exactly, never regenerated on restore; sequence-id durability risk documented for P4-1.
- **Relationships:** supersession/contradiction references validated; unknown refs, self-supersession, and cycles
  rejected (mirrors the engine's existing acyclic O-2 / F-5 guards, at contract level only).

### 10. Non-trivial fixture requirement & false-green controls
The contract must explicitly guard against: shape-only dictionary tests; silently dropped fields; empty-only
fixtures; regenerated identities; cached-readiness comparison; unvalidated relationship strings; silently accepted
unknown versions; silently ignored unknown fields; hidden database imports; datastore-specific models;
implementation inside `idea_state.py` without amendment; accidental P4-1 work; and any claim of full deterministic
replay.

### 11. Dependency rule
Python standard library and existing project dependencies only (`json`, `dataclasses`, `typing`). **No** new
external dependency, DB driver, ORM, schema-generation library, or provider SDK. Any proposed new dependency is
**prohibited** for P4-0.

### 12. Rollback / reversibility
P4-0 writes no durable data. Rollback = revert the single bounded implementation commit; remove the new contract
module + focused test (+ any proved-necessary minimal export); **no data migration, no runtime-state recovery, no
persisted-record cleanup.**

### 13. Security statement
P4-0 introduces no credentials, no datastore, no network, no provider, and no persisted user data. Pure in-memory
value objects + deterministic tests.

### 14. Validation commands (for the future implementation gate)
Changed-path check; forbidden-path check (esp. `idea_state.py` untouched); no-new-dependency check
(`requirements.txt` unchanged); deterministic RED (fails for behavior) then GREEN; full governed suite must not
regress (`pytest`), DB-free and AI-free.

### 15. Required evidence package (future implementation gate)
Candidate SHA/parent/tree; changed paths; diffstat; RED evidence (failing for the right reason) and GREEN evidence;
suite result; no-dependency proof; `idea_state.py`-untouched proof; bundle + sha256; adversarial self-review.

### 16. Independent review · publication · merge · post-merge verification · stop gate
This candidate and the future P4-0 implementation each require **formal Lean §5 independent review in a genuinely
separate session** (same-session subagents do not qualify). Publication/PR/merge are owner-side (this environment's
writes are org-policy blocked). After merge, read-only post-merge verification is required. **Mandatory stop:** on
completion of this documentation candidate, stop; do not write RED tests or implementation code; do not create the
contract module; do not modify engine code; do not select a datastore or add a dependency; do not start P4-0/P4-1/
P4-2, Phase 5–7, WS17, or STG.

### Reusable contract-template rendering
```
INCREMENT CONTRACT — P4-0 Readiness and Storage-Contract Proof   [CANDIDATE — NOT AUTHORIZED]
Objective:                Provider-free, datastore-neutral record-contract proof with lossless round-trip + invariants.
Owner authorization:      G-P4-0-DOC-01 (documentation-only candidate); implementation NOT authorized.
Risk level:               LEVEL 2 (new isolated engine module + focused test; no runtime/persistence).
Allowed paths:            engine/record_contract.py (new); tests/test_p4_0_record_contract.py (new);
                          conditional minimal engine/__init__.py export only if proved necessary.
Forbidden paths:          engine/idea_state.py, engine/derived_readiness.py, engine/decision_workspace.py, web/,
                          database/, schemas/, migrations/, requirements.txt, pytest.ini, prompts/, templates/,
                          static/, CI/config, ACTIVE_EXECUTION_ROADMAP.md (except closure), Phase 5–7/WS17/STG.
Expected behavior:        Contract serialize/restore round-trip + invariant enforcement; no durable persistence.
Non-goals:                Durable store, adapter, transactions, migration, runtime wiring, full replay (P4-1/P4-2).
Acceptance criteria:      GREEN criteria 1–14 (§7); scope limit (no full deterministic replay).
Required tests:           RED-1…RED-6 → GREEN; deterministic, DB-free, AI-free; no suite regression.
Tests not required:       Any durable-store/datastore/provider test.
Dependencies:             stdlib + existing deps only; no new dependency.
Unresolved decisions:     Exact module name; whether a minimal export is needed (default: no).
Stop conditions:          Any need to modify idea_state.py or any forbidden path → STOP — CONTRACT AMENDMENT REQUIRED.
Independent-review scope: Per §5; plus: RED behavior-based; GREEN not P4-1/P4-2; readiness re-derived not cached;
                          provenance verbatim; no datastore/dependency; identifier + relationship invariants.
Merge authority:          Owner, separately (not by the execution agent).
```

**Preserved (unchanged by this candidate):** decision **D17**; the **AISR seven-owner model** (post-output
refinement is not a substitute for Phase 4/5/6/7/WS17/STG); Phase 4 implementation, P4-1, P4-2, Phase 5–7, WS17,
STG, provider selection, and exact UX all remain **NOT AUTHORIZED**.

---

## P4-1a Historical Increment Contract Record — SUPERSEDED AS ACTIVE AUTHORITY

**Current interpretation:** the text below is preserved as the pre-implementation P4-1a contract candidate and
historical execution record. P4-1a has since been separately owner-authorized for implementation, implemented,
independently reviewed, merged through PR #356, post-merge verified, and **FORMALLY CLOSED**. Nothing in the
historical wording below reopens P4-1a or authorizes P4-1b, P4-2, or Phase 5.

## P4-1a Increment Contract Candidate (CONTRACT CANDIDATE ONLY — IMPLEMENTATION NOT AUTHORIZED)

**1. Gate identity & status.** P4-1a — Durable-Store Proof (first sub-increment of P4-1: a datastore-neutral durable
record store proved without runtime/web integration). Produced under gate **G-P4-1A-DOC-01**.
**Status:** `CONTRACT CANDIDATE ONLY` · `IMPLEMENTATION NOT AUTHORIZED` · `P4-1a NOT STARTED`. This block authorizes
no code, tests, database creation/opening/migration, dependency, or runtime work. It governs the future P4-1a
increment only after independent review (Lean §5), owner acceptance, merge, post-merge verification, and a **separate
explicit P4-1a implementation authorization**.

**2. Exact purpose.** Prove a **datastore-neutral repository/store abstraction with a Python standard-library SQLite
reference adapter** that durably persists and restores the accepted-source record set (the P4-0 record contract),
surviving an explicit store **close-and-reopen**, with atomic writes, rollback, project-scoped isolation,
durability-safe identifiers, provenance preservation, and validation — **without** any runtime/`web/` integration.

**3. Owner decisions (recorded; governs D-P4-1-01 … D-P4-1-10 in `OWNER_DECISION_REGISTER.md`).**
- **D-P4-1-01 Split:** P4-1 = P4-1a (durable-store proof) + P4-1b (runtime integration), each separately gated.
- **D-P4-1-02 Datastore:** datastore-neutral repository/store abstraction + a **stdlib SQLite reference adapter**;
  SQLite is a reference/MVP adapter, **not a permanent production commitment**; future PostgreSQL/other adapters
  remain possible through the abstraction.
- **D-P4-1-03 Dependencies:** **no new runtime dependency**; stdlib `sqlite3` only; no SQLAlchemy/psycopg/Supabase/
  provider SDK/server dependency.
- **D-P4-1-04 Existing sessions:** current in-memory sessions are **not recoverable and will not be migrated**;
  durability is future-facing (post-P4-1b). Do not imply existing temporary sessions can be restored.
- **D-P4-1-05 Identifiers:** new durable records use **durability-safe UUID-based identifiers**; **existing serialized
  identifiers are preserved exactly on load**; no adapter regenerates or silently rewrites existing record ids.
- **D-P4-1-06 Pre-account isolation:** unguessable capability identifiers; all reads/writes **scoped by project**;
  generic unavailable-project/session behavior preserved. **This is not authentication, ownership, or authorization**;
  no accounts or user ownership.
- **D-P4-1-07 Exclusions:** exclude FDC-001 persistence; P4-2 replay / durable output records / stale-output
  invalidation / full re-evaluation; Phase 5 accounts/authentication/ownership; providers; ACV; PDF; Email;
  production deployment.
- **D-P4-1-08 No web integration:** P4-1a must not modify `web/app.py`; runtime creation/retrieval/answer-submission/
  Keep-Refine/unavailable-session wiring is **P4-1b**.
- **D-P4-1-09 Required proof:** durable project creation; durable accepted-input round-trip; close-and-reopen
  persistence; atomic append; rollback with no partial write; append-only history preservation; cross-project
  isolation; stable identifier preservation; provenance preservation + allowed mapping; unknown-contract-version
  rejection; malformed-reference validation; readiness never persisted/accepted as authoritative; no P4-2 replay
  claim.
- **D-P4-1-10 Governance currency:** no additional governance-synchronization gate is required before defining P4-1a;
  this gate records the decisions and the P4-1a contract candidate.

**4. Authorized paths for future implementation.** ONE new datastore-neutral store module — proposed
`engine/record_store.py` (repository/store protocol + SQLite reference adapter + mapping to/from the P4-0 record
contract; exact name confirmed at the implementation gate); ONE focused test module — proposed
`tests/test_p4_1a_record_store.py`. CONDITIONAL: a minimal config/env helper for the SQLite file path **only if
proved necessary** and env-sourced with production fail-fast (mirroring the existing `INVENTORAI_*` pattern) — default
is to accept an explicit path/`:memory:`-then-reopen argument and add **no** config path.

**5. Prohibited & conditional paths.** PROHIBITED: `web/app.py` (D-P4-1-08); `engine/idea_state.py`,
`engine/record_contract.py`, `engine/derived_readiness.py`, `engine/decision_workspace.py`; `database/` (including the
dormant `supabase_schema.sql`); `schemas/`; `migrations/`; `requirements.txt`; `pytest.ini`; `prompts/`, `templates/`,
`static/`, `domains/`, `scripts/`, `benchmark/`; CI/`.github/`; governance docs except a later closure recording;
any Phase 5 / P4-2 / FDC-001 / provider path. CONDITIONAL: the config helper above. Any need beyond the authorized/
conditional set → **STOP — CONTRACT AMENDMENT REQUIRED**.

**6. Product & technical non-goals.** No runtime/web integration; no migration of current temporary sessions; no
general migration framework; no accounts/authentication/ownership; no replay/output persistence/stale-invalidation/
full re-evaluation; no retention-policy implementation, backup service, encryption-key management, deletion UI, or
production operations; no new dependency; no datastore server.

**7. Storage abstraction boundary.** A repository/store **protocol/interface** (responsibilities: create a project;
append an accepted-input record; record supersession/contradiction links; load a project's records; scoped lookup)
that is **datastore-agnostic**, so a future PostgreSQL/other adapter can be added without redesign. The store persists
and restores exactly the **P4-0 record-contract shape** (reuse `record_contract.to_dict`/`from_dict`); it introduces
no parallel schema authority and performs no evaluation.

**8. SQLite adapter boundary.** A stdlib `sqlite3` reference adapter behind the protocol: real on-disk (or explicit
file) SQLite; explicit **connection close and reopen**; project-scoped tables/rows keyed by project id; no ORM; no
server; single-file backup semantics are noted but backup/restore tooling is out of scope.

**9. Transaction & rollback rules.** Each mutation (project creation; accepted-input append with its link updates;
supersession edge; contradiction edges) is **atomic** (single transaction). A failed write **rolls back with no
partial record**. Loads validate the restored set via the record contract (reject invalid references / cycles /
unknown version) and **fail closed** — never silently repair.

**10. Identifier rules.** New durable records receive **durability-safe UUID-based** identifiers; **existing serialized
identifiers (`sid`, `idea_id`, `record_id`) are preserved exactly on load and never regenerated or rewritten**. The
P4-0 sequence-based `record_id` collision risk is resolved for **new** records only; previously serialized ids are
honored verbatim.

**11. Provenance rules.** Provenance/validation values are preserved **verbatim** (`OWNER_STATED`,
`LEGACY_UNSPECIFIED`, and the existing validation vocabulary). Any allowed mapping to the future target vocabulary is
**adapter-only**; **`AI_PROPOSED` / `USER_MODIFIED_AI_PROPOSAL` must not be populated** in P4-1a.

**12. Project-isolation rules.** All reads/writes are **scoped by project id**; one project's records must never be
returned for another. Identifiers are unguessable capability tokens (uuid). **This is lookup/isolation, not
authentication or authorization** (Phase 5).

**13. Unknown-version & malformed-record handling.** On load, an unknown/unsupported `contract_version` is rejected
explicitly (via the P4-0 record contract); malformed or invalid-reference records are rejected and never silently
coerced, dropped, or repaired.

**14. RED criteria (behavior-based; not written in this gate).** RED-1 accepted-input data does **not** survive store
**close/reopen** (impossible today — in-memory). RED-2 atomic **rollback is absent** (a failing multi-write leaves
partial state). RED-3 **project isolation is absent** (cross-project read). RED-4 an unknown persisted
`contract_version` is **not rejected through the future store**. RED-5 **append-only** records are not preserved after
reload. RED-6 **stable ids and provenance** do not survive durable round-trip.

**15. GREEN criteria.** Actual SQLite persistence; connection **close and reopen**; deterministic durable round-trip;
transaction rollback with **no partial records**; cross-project isolation; **stable ids preserved**; append-only
preserved; provenance preserved (+ allowed mapping, no AI values); unknown-version rejection; malformed-reference
rejection; **no persisted or cached readiness accepted as authority** (readiness re-derived from restored records via
the existing engine, never stored as a value); **provider-free and network-free** execution; **no runtime/web
integration claim**; **full governed-suite non-regression** after implementation.

**16. False-RED & false-GREEN controls.** RED must fail for missing **behavior**, not file/import absence, and must
not be satisfiable by an empty/`NotImplementedError` stub. **Fake durability is prohibited:** module-level
dictionaries; process-lifetime caches; reusing the same in-memory object; mocks that never close/reopen a real SQLite
connection; assertions based only on file existence. GREEN must **actually close and reopen** a real SQLite connection
and read the data back, use **non-trivial fixtures** (multiple records, multiple provenance/validation values, a
supersession, a contradiction, ≥2 projects), assert deep field equality, and re-derive readiness rather than compare a
cached value.

**17. Security & privacy preservation.** Persist only accepted-source records (the contract already excludes derived/
cached). Datastore file path/credential env-sourced with production fail-fast if adopted. No content logging. Validate
all loaded (potentially untrusted) serialized data via the record contract. Prevent cross-project leakage by scoping.
No backup exposure surface introduced (backup tooling out of scope). Preserve the **generic unavailable behavior**
(never disclose whether a project exists) — enforced at P4-1b, and P4-1a must not introduce a leak.

**18. R6/R16 preservation.** No `/tmp`/transcript disk write is introduced (R6); any datastore secret/path is
env-sourced with production fail-fast and no hard-coded secret (R16). The security-containment tests remain green
(non-regression).

**19. No cached readiness as authority.** Readiness is **never** serialized, persisted, or restored as an authoritative
value; it is always re-derived from restored accepted-source records by the existing engine. (Preserves D17 and the
P4-0 boundary.)

**20. P4-1a / P4-1b / P4-2 / Phase 5 separation.** **P4-1a:** durable store + SQLite adapter + mapping + transactions
+ durable ids + isolation + close/reopen + rollback/validation — **no web change**. **P4-1b:** runtime integration in
`web/app.py` (create/retrieve/answer-submission/Keep-Refine/unavailable-session), future-facing migration. **P4-2:**
deterministic replay, durable output records, stale-output invalidation, full re-evaluation. **Phase 5:** accounts,
authentication, ownership, verified email, account-linked authorization. All remain separately gated and NOT
AUTHORIZED.

**21. Evidence-package requirements (future implementation gate).** Candidate SHA/parent/tree; changed paths; diffstat;
RED evidence (failing for the right reason, incl. a stub-still-fails demonstration); GREEN evidence (real close/reopen
round-trip); full governed-suite result; no-new-dependency proof (`requirements.txt` unchanged); `web/app.py`- and
`idea_state.py`-untouched proof; bundle + sha256; §5A self-review.

**22. Independent-review requirement.** This candidate and the future P4-1a implementation each require **formal Lean
§5 independent review in a genuinely separate session**; same-session self-review/subagents do not qualify.

**23. Owner publication & merge boundary.** Publication/PR/merge are owner-side (this environment's writes are
org-policy blocked). No push/PR/merge in this gate; the candidate stops at delivery.

**24. Mandatory stop.** On completion of this documentation candidate, stop; do not write RED tests or implementation
code; do not create the store module; do not create/open/migrate a database; do not add a dependency; do not modify
`web/app.py`; do not start P4-1a/P4-1b/P4-2 or Phase 5.

### Reusable contract-template rendering
```
INCREMENT CONTRACT — P4-1a Durable-Store Proof   [CANDIDATE — NOT AUTHORIZED]
Objective:                Datastore-neutral durable record store + stdlib SQLite reference adapter, proved by
                          close/reopen round-trip + transactions + isolation, with no runtime/web integration.
Owner authorization:      G-P4-1A-DOC-01 (documentation-only candidate); implementation NOT authorized.
Risk level:               LEVEL 2 (new isolated engine module + focused test; no runtime/web/schema change).
Allowed paths:            engine/record_store.py (new); tests/test_p4_1a_record_store.py (new);
                          conditional minimal config/env helper only if proved necessary.
Forbidden paths:          web/app.py, engine/idea_state.py, engine/record_contract.py, engine/derived_readiness.py,
                          engine/decision_workspace.py, database/, schemas/, migrations/, requirements.txt,
                          pytest.ini, prompts/, templates/, static/, domains/, scripts/, benchmark/, CI/.github,
                          governance docs (except later closure), Phase 5 / P4-2 / FDC-001 / provider paths.
Expected behavior:        Durable SQLite persistence surviving close/reopen; atomic writes + rollback; project
                          isolation; durable-safe ids; provenance verbatim; validate-on-load; no readiness persisted.
Non-goals:                Runtime/web integration; session migration; accounts/auth/ownership; replay/output
                          persistence; retention policy; backup service; encryption key mgmt; deletion UI; provider.
Acceptance criteria:      GREEN criteria (§15); false-RED/false-GREEN controls (§16); full-suite non-regression.
Required tests:           RED-1..RED-6 → GREEN; deterministic, provider-free, network-free; real close/reopen.
Tests not required:       Any server/provider/web-route test.
Dependencies:             stdlib sqlite3 + existing deps only; NO new dependency.
Unresolved decisions:     Exact module name; whether a config helper is proved necessary (default: no).
Stop conditions:          Any need to modify web/app.py or any forbidden path → STOP — CONTRACT AMENDMENT REQUIRED.
Independent-review scope: Per §5; plus real close/reopen durability; no fake durability; ids/provenance preserved;
                          isolation not authorization; readiness never authoritative; no P4-1b/P4-2/Phase 5 work.
Merge authority:          Owner, separately (not by the execution agent).
```

**Preserved (unchanged by this candidate):** decision **D17**; the **AISR seven-owner model**; P4-1b, P4-2, Phase 5–7,
WS17, STG, provider selection, and exact UX all remain **NOT AUTHORIZED**.
