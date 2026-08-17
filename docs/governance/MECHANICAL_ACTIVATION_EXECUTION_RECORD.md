# Mechanical Activation Execution Gate — IMPLEMENTATION RECORD (Candidate)

**Status of THIS record:** implementation-and-documentation candidate for a HIGH-ASSURANCE runtime-state change.
Activates `mechanical` via the single canonical §5-I2 allowlist mechanism, plus the test-suite reconciliation this
activation makes necessary. Does **NOT** modify classifier logic, admission heuristics, scoring, progression,
persistence, security, Tier-1 label wording, or domain-pack semantics. Does **NOT** authorize a third domain, D4,
Phase 10, or deployment.

## §1. Owner authorization (explicit, quoted verbatim)

> "I explicitly approve activation of the Mechanical domain within InventorAI and authorize proceeding to the
> Mechanical activation execution gate."

## §2. Basis and fresh verification

Base: `18a97da735e68763c7fab6488613cde1dff4675f` (PR #502 — SHA-preserving merge of the accepted Tier-1 EN/AR
Mechanical public label candidate `e635c9f038a58cf117f64f0ac4d7852ce9338062` onto
`7cb5b6e726a726bba223fd997d9d94905173091f`; merge tree `e6f75bdd21d3939537fc96b7c511dfa0bdf7c509` == candidate
tree; candidate→merge diff EMPTY — independently re-verified this gate: `git log -1 --format="%H %P %T"` confirms
parents `7cb5b6e`+`e635c9f`; `origin/feature/atomic-json-session-persistence` confirmed at this exact tip; working
tree clean at checkout).

## §3. Final pre-activation readiness (independently reconfirmed)

D3, P9-MECH-SF safety-cue family, CF-2 (`FORMALLY CLOSED`), CF-6 (`FULLY DISCHARGED`), ILT-002 (`RESOLVED BY OWNER
DECISION`), Path-N/domain-threading, hard-coded electronics tie-break neutrality, CF5-F001/F002/F003 classifier/
admission boundaries, NMF-1+FU-1, L2SC-01 (`FORMALLY CLOSED`), L10N-RH-01 (`FORMALLY CLOSED / DISCHARGED`), Tier-1
EN/AR Mechanical public label (`AUTHORITATIVE`, this exact base) — all PASS. `L2SC-02` confirmed outside
activation-readiness. Explicit Owner Mechanical activation authorization — NOW PRESENT (§1). No prerequisite
found OPEN.

## §4. Canonical activation mechanism (reconstructed from repository truth, not assumed)

The **sole** activation gate is the frozenset literal `_ACTIVATED_DOMAINS` in `engine/domain_activation.py`
(module docstring: "§5-I2 — Activation-status policy... Activation is decided ONLY by the explicit allowlist...
never by pack status, pack existence, pack loading, registry membership, alias resolution, or metadata"). No
config file, env var, database flag, or activation-time migration exists or is needed:
`domains/mechanical/domain.json`'s `status: "active"` is pack **lifecycle** metadata, explicitly documented as
"NEVER" the activation gate. Mechanical's runtime seams (`engine/domain_rules.py`, `engine/path_n_questions.py`,
`engine/safety_signal.py`'s P9-MECH-SF safety-cue family) are already fully wired and domain-parametric — keyed on
domain *identity*, never on `_ACTIVATED_DOMAINS` — so no seam-specific change was needed or made.

## §5. Implementation

Exactly one line changed in `engine/domain_activation.py`:

```python
_ACTIVATED_DOMAINS = frozenset({"electronics_electrical", "mechanical"})
```

Plus a truthfulness update to the module's own boundary docstring (the prior wording, "Only
`electronics_electrical` is currently activated... any further domain is a future, separately-authorized gate,"
would become false the moment this line changed — rewritten to state the current, accurate boundary; no semantic
weakening).

**Pre-activation:** `activated_domains() == ['electronics_electrical']`.
**Post-activation:** `activated_domains() == ['electronics_electrical', 'mechanical']` — exact, sorted, no
duplicate, no alias activation (verified live, and via `TestActivationAllowlist::test_activated_domains_is_a_
bounded_set`, `len(activated_domains()) == 2`).

## §6. No-unintended-domain-leak proof

Verified live: `medical_device` and `software` remain `RECOGNIZED_NOT_ACTIVATED`; an unknown domain remains
`UNKNOWN_OR_UNSUPPORTED`. Adversarial mutation B (§10) independently confirms an accidental third-domain addition
is caught RED by `test_activated_domains_is_a_bounded_set`.

## §7. Real user-flow verification (live, not test-double only)

Fresh `app.test_client()` instances, no monkeypatching:

- `POST /start {idea: "A mechanical latch uses a spring and a lever to release a hinge.", domain_confirm:
  "mechanical"}` → **302**, new session, `state.domain == "mechanical"`.
- Same idea confirmed as `electronics_electrical` (the wrong domain) → **200**, re-prompts for the mechanical
  confirmation (`_present_confirm_message("mechanical")`), no session created — proving activation never
  cross-labels a domain.
- Electronics regression: `POST /start {idea: "ESP32 microcontroller circuit with a voltage sensor",
  domain_confirm: "electronics_electrical"}` → **302**, `state.domain == "electronics_electrical"`, Tier-1 EN
  label `"Electronics-informed review"` renders on the session page — unchanged.

## §8. Tier-1 EN/AR real-surface verification (live, not test-double only)

Same real admitted Mechanical session, fresh clients per language:

- EN surface (`GET /session/<sid>`): renders **"Mechanical-informed review"**; the Arabic string is absent.
- AR surface (`ui_lang=ar` session cookie, fresh client): renders **"مراجعة مستنيرة بمجال الميكانيكا"**; the
  English string is absent — no simultaneous EN+AR (D-P6-16 preserved).

Both verified via live Flask responses, not the `SESSION_STORE` test-double pattern used for pre-activation
coverage in the Tier-1 gate.

## §9. L10N-RH-01 residual disposition — Classification A (non-material/non-blocking)

Independently re-verified this gate: the broadened-activation strings (`UI_B_START_024/025/026/027/028/029`,
already remediated by the L10N-RH-01 bounded remediation gate) are now live/user-reachable for the first time
(`is_elec_only` is False whenever `activated_domains()` has 2+ elements). Their content was inspected fresh —
all are truthful, domain-neutral statements that become **true** precisely because 2 domains are now activated
(e.g. `UI_B_START_026`: "More than one specialist domain is currently supported..." — this was exactly what
L10N-RH-01 hardened these paths for). **No STOP required.** This is Classification **A**, not B.

## §10. Path-N / shared-runtime verification

`engine/progression_loop.py`'s `get_question`/`get_display_question` and `engine/path_n_questions.py`'s
`get_path_n_question`/`get_served_question` are domain-parametric with no hardcoded electronics literal (verified
by fresh code read); `mechanical` already has its own committed Path-N artifact
(`_DOMAIN_ARTIFACTS["mechanical"]`). `engine/domain_rules.py`'s D3-D tie-break (`classify_domain`) is already
fully domain-neutral and was previously production-unreachable for a 2-activated-domain tie by design (module
docstring: "becomes reachable only under a future governed second-domain activation") — activation makes this
pre-existing, already-tested branch reachable, with **no code change**. All relevant focused suites re-run GREEN
(`test_dgmpr_d3_path_n_domain_neutral_service.py`, `test_p9e1_path_n_caller_domain_propagation.py`,
`test_d3_core_domain_neutrality.py`, `test_p9e2_multi_activated_tie_precedence.py`,
`test_p9e2r_result_representation.py`).

## §11. Test-suite reconciliation (the bulk of this gate's diff)

Activating a second domain removes the `sole = activated[0] if len(activated) == 1 else None` shortcut at
`/start` for **every** idea, not just Mechanical ones — a real, pre-designed, previously-doubles-only-tested
behavior change (CF5-F002 D1/D2/D3, CF5-F003, CF5-F004, P9-E2 tie-break). This broke 113 pre-existing tests. Each
was individually triaged (no blind bulk relaxation) into three classes:

1. **Obsolete premise, real behavior now correct** (~20 tests): a NONE classification now requires an explicit
   D2 `domain_choice`; a Mechanical idea confirmed as its own domain now legitimately admits. Assertions rewritten
   to the real, verified, correct outcome.
2. **Still-valid rejection/claim, text/mechanics only changed** (~70 tests): `_unsupported_domain_message`'s
   broadened, truthful copy; corpus classifier pins where D3-D now resolves a tie against mechanical (now
   activated) instead of a legacy zero-activated precedence, or where a tie is now a real
   `AMBIGUOUS_TIE` between two now-activated domains (`electronics_electrical` + `mechanical`) — every such value
   was independently re-derived by calling `classify_domain()` live, never guessed.
3. **Legacy-scoped regression guards** (~20 tests, files explicitly documented as "§4.A backward compatibility" /
   electronics-only-scoped, e.g. `test_cf5_f001/f002/f003_*.py`, `test_d3_core_domain_neutrality.py`,
   `test_p9e1_path_n_caller_domain_propagation.py`, `test_s01_entry_alignment.py`): reconstructed via a LOCAL
   `activate`/`monkeypatch` pin to the exact pre-activation state each file's own documented scope requires,
   preserving their original claim in isolation rather than deleting or silently relaxing them.

**Discovered, disclosed, not silently fixed:**
- The `sole == "electronics_electrical"` weak-conflict-resolution branch in `web/app.py` (and its sole consumer,
  `MECHANISM_GUIDANCE_MESSAGE`) is now **provably dead code** for any input — it required `sole is not None`,
  which never holds again with 2+ domains activated. This is pre-existing code, explicitly self-documented as
  "§4.A backward compatibility" scoped to the "governed electronics-only one-step flow" — its dormancy is an
  intended consequence of activation, not a defect. `tests/test_domain_gate_entry_ux.py` retains a standalone
  constant-level test of the guidance wording (now unreachable via `/start`) plus explicit tests proving the flat
  refusal message now renders in its place, with no wrongful admission in any case.
- The `medical_device` lay-electrical-token corroboration mechanism (`_lay_electrical_evidence_count`/
  `_MEDICAL_CONFLICT_LAY_MINIMUM`), which lived entirely inside that now-dead branch, is likewise provably
  unreachable for any input under 2+ domain activation. `tests/test_domain_gate_entry_ux.py::
  test_medical_conflict_corroboration_mechanism_now_dormant_still_refused` documents this explicitly. **No
  regression** (nothing wrongly admits either way) — a UX-nuance retirement, flagged here for the record rather
  than silently absorbed.
- `test_p9_mech_i4_boundary_corpus.py`'s own stated terminality premise ("Mechanical remains NOT QUALIFIED and NOT
  ACTIVATED... any future authorized... change invalidates this terminal corpus and requires its re-validation at
  that future gate") is explicitly invoked and satisfied here — this gate IS that re-validation, performed
  in-place with per-entry disclosure of exactly which outcomes changed and why.
- `tests/test_p6_1_truthful_domain_labeling.py`'s narrower historical claim ("the Tier-1 label alone never widens
  admission") is preserved as its own pinned test in isolation (`test_tier1_label_alone_does_not_activate_
  mechanical`, `test_tier1_label_alone_did_not_widen_admission_at_entry_gate`), alongside new tests proving the
  current real truth (mechanical now activates — via the separate, explicit activation gate, never the label).

No test file's *substantive subject matter* was weakened, deleted, or silently reinterpreted — every change is
traceable to the single root cause (`sole` becoming `None`) and independently verified against live
`classify_domain()`/`activated_domains()`/Flask-response output, not guessed.

## §12. Tests (final totals)

Focused activation: `test_s5_i2_domain_activation.py` (31), `test_p9_mech_safety_cue_family.py` (39, incl. the
renamed `test_activation_state_now_includes_mechanical`). Mechanical admission/user-flow:
`test_domain_gate_entry_ux.py` (28), `test_web_app.py` (47). Tier-1 real-surface: `test_p6_1_truthful_domain_
labeling.py` (32). Path-N/shared-runtime: `test_dgmpr_d3_path_n_domain_neutral_service.py` (15), `test_p9e1_path_n_
caller_domain_propagation.py` (6), `test_d3_core_domain_neutrality.py` (7). P9-MECH qualification/safety corpus:
`test_p9_mech_i1..i5_*.py`, `test_p9_mech_i4_boundary_corpus.py` (20) — all GREEN with per-entry disclosure (§11).
**Full governed suite: 2696 passed / 3 skipped / 1 xfailed / 0 failed** (baseline 2691; +5 net new tests).

## §13. Mutation/adversarial differential sweep (all 4 required mutations, byte-restored after each)

- **A — remove `mechanical` from the allowlist:** RED (`test_activated_allowlist_matches_policy`,
  `test_activation_state_now_includes_mechanical` both failed). Restored; SHA-256 confirmed byte-identical.
- **B — add an unintended extra domain** (`medical_device` injected into `_ACTIVATED_DOMAINS`): RED
  (`test_activated_domains_is_a_bounded_set`, `test_recognition_is_not_activation` both failed). Restored;
  byte-identical.
- **C — break Mechanical picker/admission exposure while leaving the activation constant unchanged**
  (`_activated_specialist_domains()` temporarily filtered to exclude `"mechanical"`): RED
  (`test_mechanical_idea_confirmed_as_mechanical_is_admitted`, `test_mechanical_idea_now_admitted_via_real_
  activation_not_label` both failed — real admission broke while `_ACTIVATED_DOMAINS` itself stayed untouched).
  Restored; byte-identical.
- **D — break real Mechanical Tier-1 rendering** (mutated the Mechanical catalog entry to the General fallback
  values): RED (`test_resolver_maps_mechanical_to_tier1_bilingual`,
  `test_session_page_shows_english_mechanical_label_via_test_double` both failed). Restored; byte-identical.

Full suite re-run GREEN after all four mutations restored: 2696/3/1/0.

## §14. Non-modification proofs

- `engine/domain_rules.py`, `engine/progression_loop.py`, `engine/path_n_questions.py`, `engine/safety_signal.py`,
  `engine/domain_registry.py`: byte-unchanged (absent from `git diff --name-only`).
- `web/domain_label.py` (Tier-1 label wording), persistence (`persistence/`), and security-relevant code: byte-
  unchanged.
- `web/app.py`: byte-unchanged — no permanent change; the only touches were the temporary, byte-restored mutation
  C probe.
- Classifier/admission/scoring/progression logic: unchanged; only its real-world reachability under 2 activated
  domains changed, which is the intended effect of this gate, not a code modification.

## §15. Governance boundary statements

1. **Explicit Owner Mechanical activation authorization: RECORDED** for this gate (§1; see also ODR entry
   `D-P9-MECH-03`, §16 below).
2. **Mechanical is now ACTIVE / runtime-operated**: `activated_domains() == ['electronics_electrical',
   'mechanical']`.
3. **Tier-1 EN/AR Mechanical public label remains authoritative** — unchanged by this gate.
4. **L10N-RH-01 remains `FORMALLY CLOSED / DISCHARGED`** — its residual disposition re-verified as non-blocking
   (§9), not reopened.
5. **Phase 9 remains OPEN** until activation post-merge verification / a future formal-closure gate satisfies its
   own criteria — NOT claimed closed by this implementation gate.
6. **Phase 10 remains NOT AUTHORIZED. Deployment remains NOT AUTHORIZED.**
7. **No third domain is activated or implied.** Activating any further domain remains a future, separately-
   authorized gate.

## §16. Owner Decision Register recording

No document (`P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §16, `S5_I2_ACTIVATION_STATUS_POLICY_FORMAL_
CLOSURE_RECORD.md`, `ACTIVE_INCREMENT_CONTRACT.md`) prescribes a mandatory ID/format for the activation-execution
act itself. The consistent, observed repository convention — every other governed implementation increment in
this lineage (`D-P9-MECH-01` selection/qualification-planning, `D-P9-MECH-02` OD-M2 safety-cue-family timing) gets
its own recorded, Owner-accepted decision row under the `## P9-MECH-QC` section — is followed here: this gate adds
exactly one new row, `D-P9-MECH-03`, the next sequential ID under the existing `P9-MECH` topic prefix (per the
observed `D-<TOPIC>-<NN>` sequencing pattern), recording the explicit Owner activation authorization (§1) and its
execution. No ID was invented outside this observed convention.

## §17. Scope of THIS candidate

`engine/domain_activation.py` (the one-line allowlist change + docstring truthfulness) + 31 test files (reconciled
per §11, per-file disclosed) + this record + `ACTIVE_EXECUTION_ROADMAP.md` + `ACTIVE_INCREMENT_CONTRACT.md` +
`CURRENT_PROJECT_STATE.md` + `OWNER_DECISION_REGISTER.md` (`D-P9-MECH-03`, new row only). **ZERO
classifier/admission/scoring/progression/persistence/security/Tier-1-label diff.** Next required gate: Mandatory
Grill on this exact candidate, then the governed lifecycle. Mechanical activation post-merge verification / a
future formal-closure gate remains the next eligible step for Phase 9 disposition — not performed here.
