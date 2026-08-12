# P9-E2 / P9-PREREQ-B — Multi-Activated Domain Tie / Conflict Precedence — FORMAL CLOSURE RECORD

**Status of THIS record:** governance/documentation-only **closure candidate** — authoritative only if independently reviewed
(Mandatory Grill → independent external exact-candidate review), Owner-accepted, merged (create-a-merge-commit), and post-merge
verified. It records the **formal closure of the bounded P9-E2 multi-activated tie/conflict-precedence runtime gate** on its
merged, post-merge-verified implementation (PR #445). It does **not** activate/select any domain, execute D4, decide D8, execute
the Retrospective Adversarial Architecture Audit, start Phase 10, execute PSRR, or authorize deployment/production.
**GOVERNANCE-ONLY FORMAL CLOSURE GATE** — no runtime behavior is created; the P9-E2 RED→GREEN + nine mutation probes occurred at
implementation time (candidate `85fda813`) and are cited + freshly re-reproduced, not re-created. **Expected engine / web / CLI /
domains / Domain Registry / domain activation / schemas / persistence / API / architecture-guardrail / test diff: ZERO.**

## 1. Gate identity & bounded purpose

- **Gate:** P9-E2 / P9-PREREQ-B — Multi-Activated Domain Tie/Conflict Precedence (the governed runtime tie-precedence policy
  required by the authoritative P9-E2 contract, implemented through the P9-E2-R canonical classifier seam per P9-E2-R closure
  CF-1). It replaced the incidental `sorted(activated_tied)[0]` winner with a governed, no-winner ambiguity result when two or more
  ACTIVATED domains are equally top-scored.
- **What it implemented (bounded runtime change, minimum-path):** `engine/domain_rules.py::classify_domain` — the activated-tie
  branch split into: `len(activated_tied) == 0` → unchanged non-activated priority fallback; `len == 1` → `SINGLE`;
  **`len >= 2` → `AMBIGUOUS_TIE(selected_domain=None, candidates=complete canonical activated tied set, reason=EQUAL_SCORE)`**.
- **Explicit truth boundary:** P9-E2 implemented the **tie-precedence mechanism only**. It **did not** activate or select any
  domain, perform per-domain qualification, execute D4 multi-domain composition, or fabricate `MULTI_DOMAIN_NEEDS_D4`. With only
  `electronics_electrical` activated, the `AMBIGUOUS_TIE` branch is **production-unreachable today** (a ≥2-activated tie cannot
  occur); it is exercised only through bounded self-restoring `_ACTIVATED_DOMAINS` doubles.
- **Verdict:** **P9-E2 — FORMALLY CLOSED / SATISFIED** (bounded tie-precedence runtime gate; authoritative if/when this governance
  candidate is merged and post-merge verified). Closing P9-E2 does **not** activate any domain or authorize anything downstream.

## 2. Authoritative lineage — re-verified from Git at candidate creation

- **P9-E2 contract authoritative merge:** `47fce397dfd21175a0012b652f8dde6548e31432` (PR #441; corrected contract candidate
  `1d29a26f`); the bounded **P9-E2-R** representation sub-gate contract/implementation/closure are authoritative (PRs #442/#443/#444).
- **P9-E2 implementation candidate (accepted, corrected):** `85fda813b4e03c5bdec0bde51aa411e80ebfbfb1`.
  - **Implementation candidate parent:** `c11482db7240b5ac628e77cd061f8d5de6df40ee`.
  - **Implementation candidate tree:** `0bffe3f7eeebf765a7a9ce34783cf99935a2ee10`.
- **Implementation authoritative merge / this closure candidate's parent:** `f33663710d6edf506a082b1bfa2f02e9c3fef7ac` (PR #445).
  - **Merge parent 1:** `c11482db7240b5ac628e77cd061f8d5de6df40ee`.
  - **Merge parent 2 (accepted candidate):** `85fda813b4e03c5bdec0bde51aa411e80ebfbfb1`.
  - **Merge tree:** `0bffe3f7eeebf765a7a9ce34783cf99935a2ee10`.
  - **Merge tree == accepted candidate tree:** **VERIFIED** (`85fda813^{tree}` == `0bffe3f7…`, re-computed this gate).
  - **No newer authoritative commit** beyond `f336637` (re-verified this gate).
- **Implementation scope (base `c11482d` → merge `f336637`):** **5 files, 546 insertions(+), 17 deletions(−)**; `git diff --check`
  **CLEAN** (re-verified this gate). Changed paths: `engine/domain_rules.py`, NEW
  `tests/test_p9e2_multi_activated_tie_precedence.py`, `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`,
  `docs/governance/ACTIVE_INCREMENT_CONTRACT.md`, `docs/governance/CURRENT_PROJECT_STATE.md`. `web/app.py`,
  `scripts/run_cli.py`, `engine/domain_activation.py`, `ARCHITECTURE_GUARDRAILS.md`, `OWNER_DECISION_REGISTER.md`, `domains/**`,
  `schemas/**`, `database/**` — **ZERO diff**.

## 3. Review lineage — accepted exact-candidate chain (truthful; non-blocking items NOT overstated as resolved)

- **Rejected implementation candidate:** `3255c4ba1ca6ae50e0c3f20d7f0d4c8ef1fa223c` — REJECTED by Mandatory Grill
  (`GRILL FAIL — MATERIAL CONTRACT CORRECTION REQUIRED`: a false `/start` strong-unsupported "masked for all real ties"
  reachability claim, an omitted achievable distinguishing RED-E2-10, and a misdescribed multi-activation `/start` delta). It was
  **NEVER published, accepted, or merged**, and remains immutable rejected evidence. It is **not** an ancestor of the accepted
  candidate.
- **Corrected accepted candidate:** `85fda813b4e03c5bdec0bde51aa411e80ebfbfb1` — built **directly from authoritative parent
  `c11482d`** (rejected SHA not an ancestor).
  - **Mandatory Grill:** `GRILL PASS WITH NON-BLOCKING HARDENING` — **blocking findings: NONE.**
  - **Independent external exact-candidate review:** `ACCEPT WITH NON-BLOCKING OBSERVATIONS` — **blocking findings: NONE.**
  - **Owner exact-candidate acceptance:** explicitly received for `85fda813` unchanged.
  - **SHA-preserving publication:** verified. **Pre-merge verification:** PASS. **Merge method:** CREATE A MERGE COMMIT (PR #445).
    **Post-merge verification:** PASS.
- The Grill / independent-review **non-blocking** items are recorded in §7 below and are **carried forward, not declared resolved.**

## 4. Closed acceptance behavior — re-verified at `f336637`

1. **One canonical classifier owner:** `classify_domain(...)` in `engine/domain_rules.py` (verified).
2. **`infer_domain(...)` is legacy compatibility only** — a thin fail-loud wrapper delegating to `classify_domain` (annotation
   `-> str | None`); SINGLE → domain string, NONE → `None`, **richer kinds → `AmbiguousDomainResultError`** (a `RuntimeError`
   subclass, not `AssertionError`).
3. **Zero activated tied candidates → existing non-activated priority fallback RETAINED UNCHANGED**
   (`priority = ["medical_device", "electronics_electrical", "mechanical", "software"]`).
4. **Exactly one activated tied candidate → `SINGLE`** (unchanged, D3-D).
5. **Two or more activated tied candidates → `AMBIGUOUS_TIE`** with: `selected_domain = None`; the **complete tied ACTIVATED
   candidate set only**; **canonical (sorted) deterministic ordering**; deterministic **`EQUAL_SCORE`** reason.
6. **No arbitrary / alphabetical winner; no Electronics preference; no registration/file/dict-order precedence; no LLM
   tie-breaker** (verified behaviorally + by the nine mutation probes; canonical order ≠ precedence).
7. **`MULTI_DOMAIN_NEEDS_D4` remains representable but is NOT fabricated** from an ordinary equal-score tie (deterministic
   equal-score evidence cannot distinguish a genuine multi-domain need from ordinary ambiguity); **D4 remains separate and
   unexecuted.**
8. **Only ACTIVATED domains form the candidate set** (recognition ≠ activation; D3-D preserved; recognized-not-activated packs
   excluded from the tie).
9. **Web `/start` and CLI dispatch by `result.kind`** (installed by P9-E2-R): `AMBIGUOUS_TIE` / `MULTI_DOMAIN_NEEDS_D4` fail closed
   (no session, no electronics admission, no winner); `state.domain` remains a resolved string.
10. **No new global framework, no duplicate classifier/router/registry/scoring owner** introduced (a single tie branch inside the
    existing canonical `classify_domain`).
11. **No real specialist domain activated** (activated ties simulated only via self-restoring `_ACTIVATED_DOMAINS` doubles);
    **`activated_domains() == ['electronics_electrical']`** (verified).
12. **D8 remains Owner-reserved; `domains/iot_electronics/**` untouched** (verified: `domains/` zero-diff base→merge).
13. **Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment / production NOT AUTHORIZED.**

## 5. Canonical-owner reconciliation (truthful; no contract rewrite)

The historical P9-E2 contract **predates P9-E2-R** and names `engine/domain_rules.py::infer_domain` as the canonical
classification/precedence owner. The later **authoritative P9-E2-R architecture** (PRs #442/#443/#444) established
**`classify_domain(...)` as the single canonical classifier owner** and **`infer_domain(...)` as the legacy fail-loud compatibility
wrapper**. P9-E2 was therefore implemented through the authoritative `classify_domain` seam (per P9-E2-R closure CF-1). This is
**function-name / architecture evolution governed by the later authoritative architecture**, recorded truthfully here; the old
P9-E2 contract text is **not rewritten and is not described as amended**, and **no separate contract amendment is required.**

## 6. Fresh closure evidence (reproduced at this candidate's parent `f336637`)

- **Full governed suite** `pytest -q`: **2307 passed / 3 skipped / 1 xfailed / 0 failed / 0 errors** (identical to the accepted
  candidate-era count; = 2287 parent baseline + 20 P9-E2 tests; the 3 skips are pre-existing Playwright/forward-only — NOT passes;
  1 xfailed pre-existing). No count regression; no deleted test; no hidden skip/xfail.
- **Focused** `tests/test_p9e2_multi_activated_tie_precedence.py` + `tests/test_p9e2r_result_representation.py` +
  `tests/test_architecture_guardrails.py`: **57 passed.**
- **Cited implementation-time RED→GREEN (candidate `85fda813`):** 20 tests — **12 distinguishing RED** reproduced on parent
  `c11482d` (E2-1..9; **E2-10 a REAL `/start` production-path RED** — `circuit and hinge` under an elec+mech double: parent admits
  an electronics session (302), candidate fails closed 200 UNSUPPORTED, no session; **E2-10b** `hinge and app`; **E2-11** CLI
  bounded stop) + **8 honest GREEN GUARDS**.
- **Nine load-bearing mutation probes — all CAUGHT RED, bytes restored** (bytecode caching disabled; `__pycache__` cleared between
  mutations; each failure causally verified against the governed target test): (1) restore alphabetical/incidental SINGLE winner;
  (2) collapse AMBIGUOUS_TIE to NONE; (3) drop one activated candidate; (4) drop the D3-D activation filter; (5) introduce
  Electronics preference; (6) break canonical candidate ordering; (7) detach Web AMBIGUOUS/MULTI dispatch (→ P9-E2-R RED-R2/R10);
  (8) `infer_domain` returns None on real ambiguity; (9) neutralize the real `/start` AMBIGUOUS fail-closed branch with a
  non-strong-unsupported real tie input (→ RED-E2-10/10b).

## 7. Carry-forward obligations (MUST NOT be erased by closure)

- **CF-1 — P9-E2 runtime tie policy: SATISFIED by the subject of this closure** (implemented authoritatively through the
  `classify_domain` seam via PR #445). Recorded as completed; no residual CF-1 work remains.
- **CF-2 — Shared AMBIGUOUS/MULTI public message: PENDING.** `AMBIGUOUS_TIE` / `MULTI_DOMAIN_NEEDS_D4` currently fail closed
  through the existing `UNSUPPORTED_DOMAIN_MESSAGE`, and richer kinds are production-unreachable today (electronics-only). Before
  those states become genuinely user-reachable under future governed activation, verify public messaging remains truthful and
  honor the already-governed UI-boundary sub-gate rather than silently adding copy. **P9-E2 closure does NOT discharge CF-2.**
- **CF-3 — Non-activated priority fallback / Nth-domain fallthrough hazard: PENDING.** The hardcoded recognized-not-activated
  priority list inside `classify_domain` was **retained intentionally for backward compatibility** (no reachable defect today —
  every recognized pack is represented). It must be reviewed for completeness/extensibility **before the first future Nth-domain
  registration/activation** that could exercise an omitted-pack fallthrough. **P9-E2 closure does NOT claim Nth-domain fallback
  completion.**
- **CF-4 — D4: PENDING/SEPARATE.** `MULTI_DOMAIN_NEEDS_D4` is a truthful marker only; **D4 remains the separate owner** for actual
  multi-domain engineering composition. No D4 work here.
- **CF-5 — Retrospective Adversarial Architecture Audit: PENDING; MANDATORY BEFORE FIRST NEW-DOMAIN ACTIVATION.** Inspect the
  inherited architecture; classify each finding A/B/C/D/E; dispose C/D/E as governed (C = prerequisite before its trigger is
  reachable; D = corrective gate before continuing affected work; E = explicit architecture/Owner decision; any C/D/E requires
  independent validation before reopening closed architecture). **NOT executed here; no findings created; no closed phase reopened;
  no domain activated.**
- **CF-6 — Web pre-classifier / strong-unsupported reachability & admission interaction: PENDING PRE-SECOND-SPECIALIST-DOMAIN
  ACTIVATION (distinct from CF-2).** Before the first second-specialist-domain activation, review and disposition the interaction
  between the Web `/start` strong-unsupported heuristics, canonical-classifier reachability, activated-domain admission, ambiguity
  handling, Web/CLI/core consistency, and public-message truthfulness (which domain signals are intercepted before
  `classify_domain`; which reach it; no hidden Electronics admission; no bypass of `AMBIGUOUS_TIE`; whether the existing
  unsupported-domain copy remains truthful). **P9-E2 closure does NOT execute CF-6 and authorizes NO Web redesign.**

## 8. Independent-review / Grill non-blocking observations (carried forward, NOT discarded)

- **NB-1 — Stale/layered P9-E2-R wording in `CURRENT_PROJECT_STATE.md`.** Historical/layered wording from before PR #444 describes
  P9-E2-R as a closure candidate. Non-blocking historical/layered staleness. Reconciled here only as normal current-truth sync
  (present/current status made unambiguous) **without rewriting legitimate history**; no deceptive history rewrite.
- **NB-2 — Substring signal matching.** Classification uses substring matching; short signals (`led`, `web`) may match inside
  unrelated words. **Pre-existing and unchanged by P9-E2.** Carried forward to future P9-QS/domain qualification, the Retrospective
  Adversarial Architecture Audit, and CF-3/CF-6 where relevant. **Not fixed in this closure candidate.**
- **NB-3 — Mutation-probe invariant coverage.** One mutation probe is partly caught by `DomainClassification` construction
  invariants (which are part of the governed contract) rather than solely by a behavioral assertion. Non-blocking test-hardening
  evidence. **Tests not changed here.**
- **NB-4 — Strong-unsupported vocabulary vs future activated domains.** Governed by **CF-6**. **Web not modified here.**
- **NB-5 — IoT schema warning.** `domains/iot_electronics/domain.json` has a pre-existing registry/schema warning/skip; belongs to
  **D8/IoT (Owner-reserved)** and future registry/domain-qualification work. **`domains/iot_electronics/**` not modified.**

## 9. Phase-9 mandatory completeness checklist (repository-evidenced)

1. **Engineering-knowledge quality and correctness:** `NOT APPLICABLE` — P9-E2 is a tie-precedence policy gate, not domain
   knowledge content.
2. **Technical truthfulness / known-unknown behavior:** `APPLICABLE / PASS` — the incidental tie winner is eliminated; ambiguity is
   surfaced honestly (no-winner AMBIGUOUS_TIE, deterministic reason); `MULTI_DOMAIN_NEEDS_D4` not fabricated; the reachability
   language corrected to source truth.
3. **Real specialization without shared-core coupling:** `APPLICABLE / PASS` — one domain-neutral len-based classifier; dispatch by
   kind; no per-domain branching; no duplicate owner.
4. **Rigorous pre-activation qualification:** `APPLICABLE / PASS` **for the tie-policy mechanism only** (positive/negative/ambiguous/
   ≥3-way/boundary + regression + invariants + nine mutation probes). **Actual per-domain qualification remains DEFERRED TO A
   GOVERNED FUTURE GATE (P9-QS)** — not conflated with tie-policy qualification.
5. **Cross-domain interaction/composition:** `APPLICABLE / PASS` for the ambiguity / no-hidden-precedence behavior; **actual
   composition remains DEFERRED TO D4** — the deferral is explicit, not hidden inside the PASS.
6. **Materials/manufacturing/prototype extensibility:** `DEFERRED TO A GOVERNED FUTURE GATE` (CAP-12 / CAP-13 / WS-PFV).
7. **Deterministic engineering calculations / units / provenance:** `DEFERRED TO A GOVERNED FUTURE GATE`.
8. **Trustworthy technical knowledge sources / licensing / versioning:** `DEFERRED TO A GOVERNED FUTURE GATE` (D13 family).
9. **Long-term Nth-domain extensibility:** `APPLICABLE / PASS` for arbitrary ≥2 activated-tie handling (incl. ≥3-way, no
   pair-specific logic); **CF-3 remains explicitly pending** — full Nth-domain non-activated-fallback completion is NOT claimed.
10. **End-to-end disciplined engineering reasoning:** `APPLICABLE / PASS` for the in-scope Web/CLI ambiguity path (RED-E2-10/10b/11
    exercise the real production classifier and fail closed); the **future first-second-domain Web pre-classifier interaction
    remains DEFERRED TO CF-6** (registration ≠ disposition).

**No acceptance-relevant `APPLICABLE / GAP` remains.**

## 10. Governance scope of this closure candidate

Governance/documentation only: this NEW closure record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **`OWNER_DECISION_REGISTER.md` UNCHANGED** (a
prerequisite/runtime-gate closure records no new accepted Owner product-policy decision — consistent with P9-E2-R / P9-E1 / D3
closure precedent). **ZERO** runtime / engine / test / domain / Domain Registry / domain activation / web / CLI / schema /
persistence / API / architecture-guardrail diff in this closure gate.

## 11. Formal-closure boundaries — this closure authorizes NOTHING downstream

Formal closure of P9-E2 does **NOT** authorize: first second/new-domain activation; Mechanical activation; Medical Device
activation; Software activation; IoT activation; D8 execution; D4 execution/composition; CF-6 execution; Retrospective Audit
execution; CAP-12; CAP-13; WS-PFV; deterministic-calculations capability; knowledge-source capability; Phase 10; PSRR; deployment;
production. **The current activated specialist domain remains Electronics only** (`activated_domains() == ['electronics_electrical']`).

## 12. Candidate state & next gate

**P9-E2 implementation = AUTHORITATIVE** (PR #445, merge `f336637`; accepted candidate `85fda813`). **This P9-E2 formal-closure
record = FORMAL-CLOSURE CANDIDATE ONLY** — it does **not** claim P9-E2 is already formally closed merely because it is authored.
**P9-E2 is NOT YET FORMALLY CLOSED by this candidate until: Mandatory Grill → independent external exact-candidate review → Owner
exact-candidate acceptance → SHA-preserving publication → PR → pre-merge verification → CREATE A MERGE COMMIT → post-merge
verification** have completed (P9-E2-R closure precedent). The **SATISFIED** conclusion proposed here is the conclusion this
candidate proposes, pending that authoritative merge. **Next required gate: MANDATORY GRILL ON THIS EXACT CLOSURE CANDIDATE.**
