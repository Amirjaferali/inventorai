# CF-5 — NMF-1 / FU-1 Bounded Test-Hardening Disposition Record (Candidate)

**Status of THIS record:** governance/documentation-only companion to a bounded, additive, TEST-ONLY implementation
(4 new tests across 2 EXISTING test files; zero engine/web/CLI/domain/pack/provenance/registry/activation/schema/
persistence edit). It is the "bounded standalone test-only hardening gate" that
`docs/governance/CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_FORMAL_CLOSURE_RECORD.md` §6 named as NMF-1/FU-1's
earliest available gate. **The disposition in §3 becomes authoritative ONLY if/when this exact candidate is merged
(create-a-merge-commit) and post-merge verified.** **`OWNER_DECISION_REGISTER.md` UNCHANGED** (test-hardening
execution records no new Owner product-policy decision — it is EXECUTION of an already-accepted disposition option,
not a new policy). **DOCUMENTED NO-VALID-RED** (the runtime behavior under test is asserted, by NMF-1's own origin
text and by fresh empirical verification here, to be ALREADY CORRECT — these are coverage-only additions).

## §1. Basis and fresh verification

Base: `91f4e5c6ad69964d01328e1502ab04d1d76aa0c0` (PR #485 — SHA-preserving merge of the accepted P9-MECH-SF formal
closure candidate `c25c8438` onto `1a23552b`; merge tree `36e2c030` == candidate tree; POST-MERGE PASS; freshly
fetched; 0 newer; clean tree). Fresh verification at this base: full governed suite **2569 passed / 3 skipped / 1
xfailed / 0 failed**; `activated_domains() == ['electronics_electrical']`.

## §2. Dependency-graph reconstruction (why THIS gate, not Tier-1/CF-6/CF-2)

Reconstructed from `docs/governance/P9_MECH_SAFETY_CUE_FAMILY_CONTRACT.md` §1 (the most current statement) and
confirmed unchanged at this tip: the four remaining non-Owner activation blockers are **mutually independent** —
none technically requires another. Sequencing considerations specific to each:

- **Tier-1 EN/AR label** — CANNOT proceed now: `P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §13 states the
  label becomes truthful "not before activation-readiness"; implementing it now would label an unserved domain —
  an untruthful claim while `activated_domains() == ['electronics_electrical']`. Correctly LAST.
- **CF-6 / CF-2** — each is a BROAD, not-yet-scoped lane ("general Web/CLI pre-classifier consistency remainder";
  "general public-message truthfulness beyond `/start`") with its own separate registered owner and NO standalone
  contract document yet defining its bounded next increment. They share one facet (the CLI electronics-pinned
  literal, `scripts/run_cli.py`) dischargeable together per the F002 facet-discharge precedent
  (`CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md` §5) — but that joint gate requires its OWN explicit
  jointly-authorized scoping contract (naming both owners) not yet created, and is a strictly larger surface than
  this gate.
- **NMF-1 / FU-1** — the SMALLEST, most bounded, already-fully-specified item: `CF5_RETROSPECTIVE_ADVERSARIAL_
  ARCHITECTURE_AUDIT_FORMAL_CLOSURE_RECORD.md` §6 registers them ONCE with their exact scope already named (the
  three phrase-contiguity mutation gaps for NMF-1; the one empty-activation refusal-branch gap for FU-1), their
  runtime already declared correct, and their earliest gate already sanctioned in the SAME sentence: "a bounded
  standalone test-only hardening gate." No further scoping contract is needed — the origin registration text IS
  the bounded scope. Zero runtime/web/CLI file is touched; risk is the lowest of the four remaining blockers.

**Determination: THIS gate (NMF-1/FU-1 execution) is the smallest dependency-correct next gate.** It has no
technical dependency on Tier-1/CF-6/CF-2 and does not touch, combine with, or duplicate any of their scope.

## §3. NMF-1 / FU-1 disposition

Per `P9_MECH_SAFETY_CUE_FAMILY_CONTRACT.md` §1: "record their execution or explicit accepted-risk disposition."
Explicit accepted-risk is an OWNER-ONLY disposition (not available to this non-Owner gate). Therefore the
disposition recorded here is **EXECUTION**:

- **NMF-1 (phrase-contiguity mutation-coverage gap, class B):** three new pinned tests added to
  `tests/test_cf5_f003_classifier_matching_semantics.py` — `test_nmf1_reorder_of_registered_phrase_rejected`
  ("delivery drug" → NONE), `test_nmf1_intermediate_token_pluralization_rejected` ("machines learning" → NONE),
  `test_nmf1_final_token_pluralization_still_permitted` ("machine learnings" → software, the permitted contrast
  case). All three empirically verified against the LIVE classifier before pinning (§4); the runtime required
  ZERO change — confirming NMF-1's own "shipped runtime is CORRECT" claim.
- **FU-1 (empty-activation defensive test):** one new pinned test added to
  `tests/test_cf5_f002_web_admission_multidomain.py` — `test_fu1_empty_activation_set_refuses_closed`, exercising
  `web/app.py::start`'s `if not activated:` fail-closed boundary via the file's existing bounded, self-restoring
  `activate()` double (zero domains). Asserts: HTTP 200 (no 500), no session created, the truthful
  no-specialist-domain-available refusal copy present, the electronics-only copy absent. Runtime required ZERO
  change.

**NMF-1 = DISCHARGED (executed). FU-1 = DISCHARGED (executed).** Both, conditional on this candidate's own merge
and post-merge verification.

## §4. Evidence

Empirical pre-pin verification against the live runtime at this base (§1): `classify_domain("delivery drug")` →
NONE; `classify_domain("machines learning")` → NONE; `classify_domain("machine learnings")` → SINGLE(software);
`/start` under `activate()` (zero domains) → HTTP 200, no session, "no specialist domain available" in body,
"electronics and electrical ideas only" absent — all matching the new pins exactly. Focused runs:
`test_cf5_f003_classifier_matching_semantics.py` + `test_cf5_f002_web_admission_multidomain.py` together **112
passed** (108 pre-existing + 4 new). Full governed suite **2573 passed / 3 skipped / 1 xfailed / 0 failed** (base
2569 + 4 new; zero regressions). Mutation probes (byte-verified restoration, `__pycache__` cleared before each):
m1 (reorder tolerance in `_phrase_matches`) CAUGHT by the new reorder pin; m2 (intermediate-token pluralization
tolerance) CAUGHT by the new pluralization pin; m3 (wrong refusal message on the empty-activation branch) CAUGHT
by the new FU-1 pin. Post-restore re-green confirmed. `git diff --check` clean.

## §5. Scope (exact)

**Touched:** `tests/test_cf5_f003_classifier_matching_semantics.py` (additive, 3 new tests); `tests/
test_cf5_f002_web_admission_multidomain.py` (additive, 1 new test); this NEW record; `ACTIVE_EXECUTION_ROADMAP.md`
(append-only); `ACTIVE_INCREMENT_CONTRACT.md`; `CURRENT_PROJECT_STATE.md`. **Untouched (verified):** every engine
file (`domain_rules.py`, `progression_loop.py`, `safety_signal.py`, `path_n_questions.py`, …); `web/app.py`;
`scripts/run_cli.py`; every domain pack; `domains/domain_provenance.json`; every other test file;
`OWNER_DECISION_REGISTER.md`; schemas; persistence. No Tier-1 label work; no CF-6 work; no CF-2 work (the CLI
literal at `scripts/run_cli.py` is UNCHANGED — this gate does not touch it); no D4/D8/THERM-01/Phase 10/PSRR/
deployment; no P9 closure; no activation change.

## §6. Remaining activation blockers (unchanged by this gate)

Tier-1 EN/AR label (activation-readiness edge, correctly last); CF-6 (OPEN, general Web/CLI pre-classifier
consistency remainder incl. the CLI electronics literal — untouched here); CF-2 (OPEN, general public-message
truthfulness beyond `/start` — untouched here); explicit Owner activation authorization. `MECHANICAL = P9-QS
QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED` unchanged in kind (NMF-1/FU-1 discharge does not touch
Mechanical's own blocker set — NMF-1/FU-1 were CF-5-lane carry-forwards referenced by, not owned by, the
Mechanical qualification lane). `activated_domains() == ['electronics_electrical']`; first new-domain activation
remains BLOCKED.

## §7. Next gate

Mandatory Grill on this exact candidate, then the governed lifecycle. After this gate merges, the remaining
non-Owner activation-side items (CF-6, CF-2, each requiring its own bounded scoping contract; the Tier-1 label at
activation-readiness) are the natural next candidates — each separately authorized; nothing here selects,
combines, or pre-authorizes any of them.
