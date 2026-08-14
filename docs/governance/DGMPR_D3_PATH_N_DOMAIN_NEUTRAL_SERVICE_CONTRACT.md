# D-GMPR-D3-PN — Path-N Domain-Neutral Question Service Remediation — Bounded Implementation CONTRACT (CORRECTED; supersedes rejected `4d6e4785`)

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE** for the remediation of the LAST open
`D-GMPR-01-D-D3` coupling — the Electronics-pinned Path-N question seam (`engine/path_n_questions.py`). **Correction
lineage:** the prior candidate `4d6e4785d753576d1879656be1ce8979f5f6eabb` was independently reviewed and **REJECTED —
MATERIAL CORRECTION REQUIRED** (it enumerated only three of the FIVE existing-test flips its own end-state forces —
missing the D3-B seam-identity pin and the P9-E1 RED1 generic-fallback equality); it is preserved as immutable
rejected evidence, NOT amended, NOT reused, NOT published. This candidate is a FRESH correction from the same
authoritative parent with the accepted architecture preserved unchanged and the reconciliation set corrected and
re-proven. Canonical owner unchanged: the registered D-GMPR-01-D-D3 shared-core gate (the Mechanical lane depends on,
never performs, it). It becomes AUTHORITATIVE only through the governed lifecycle; **it implements nothing in this
gate**; once authoritative it authorizes ONLY the bounded implementation below (separate Owner authorization
required). It does NOT activate Mechanical, does NOT declare Mechanical qualified, does NOT discharge D-GMPR-01-D-D3
(its closure gate does), and records NO new Owner decision (**`OWNER_DECISION_REGISTER.md` UNCHANGED**).
**DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY CONTRACT GATE.**

## §1. Authoritative base and exact blocker (unchanged from the reviewed reproduction)

Base: `0dca782e5d4f32d403ad79c64ba469f07e46e600` (merge of `8ec39acf` + accepted I5 implementation `baee2542`; tree
`cb95fc97`; freshly verified; clean tree; suite 2531/3/1/0). Blocker: `engine/path_n_questions.py` hard-pins the ONE
Electronics-owned committed artifact and returns `None` for any non-electronics domain (`:92-93`); the live callers
(`progression_loop.py:236/:278`) then fall through to the GENERIC question bank, so non-electronics Path-N sessions
lose all domain content and never reach the (verified domain-neutral) stall reframe.

## §2. Architecture (PRESERVED exactly as reviewed — no redesign)

ONE canonical seam; the SAME two public functions with UNCHANGED signatures; **domain-keyed artifact resolution**
(`docs/governance/path_n_content_config/<domain>_path_n_questions.json`; per-domain load-once cache; identical
fail-loud malformed-artifact semantics per artifact); Electronics + the `None` default byte-identical (exact
backward compatibility); a recognized domain WITH a committed artifact served from ITS OWN artifact; recognized
artifact-less domains (software/medical_device) and unknown/unsupported domains → `None` (unchanged fail-safe →
existing caller fallthrough); NO wrapper, NO duplicate service path, NO `progression_loop.py`/`domain_rules.py`
change, NO Mechanical activation. **Bounded path-resolution hardening (review observation, adopted):** a raw domain
string MUST NOT become an unchecked filesystem path — artifact resolution MUST go through a bounded, explicit
domain→artifact mapping derived from canonical registry identity (e.g. resolve the canonical `pack_id` via the
existing §5-I1 registry/alias identity, then look up the artifact in an explicit in-module mapping or an
existence-checked candidate constrained to the committed directory with the canonical id as the sole variable
component); unmapped/unrecognized identities → `None`. This is a lookup-boundedness rule ONLY — no registry
redesign, no new validation framework.

## §3. Mechanical artifact (verbatim projection; metadata shape SPECIFIED)

NEW committed `docs/governance/path_n_content_config/mechanical_path_n_questions.json`, a **VERBATIM projection** of
the I5-proven mechanical pack questions: the same three gap-type keys; per gap type the ordered variants copied 1:1
— `question_id` identical, `text` identical, order identical, TEN entries total; **no new content authorship** (the
merged I5 W1–W6 wording verdict carries over unmodified; impossibility of verbatim projection → STOP — OWNER
DECISION REQUIRED). **Exact artifact shape (metadata-ambiguity eliminated):** a top-level JSON object with exactly
two keys — `"metadata"` and `"gaps"`. `"gaps"` mirrors the electronics artifact's schema: gap-type key → ordered
list of `{"question_id": str, "text": str}` objects (exactly the two keys per entry, matching the electronics
entries' shape and the seam's fail-loud reader). `"metadata"` MUST contain at least: `"domain"` (`"mechanical"`),
`"source"` (the pack path `domains/mechanical/domain.json` + the projection rule "verbatim from
gap_type_mappings"), `"provenance_ref"` (`"mechanical:PR001"` lineage), `"contract"` (this record's filename), and
`"generated_by_gate"` (`"D-GMPR-D3-PN implementation"`); no other semantic keys without disclosure. The electronics
artifact file remains byte-frozen.

## §4. Allowed / forbidden paths (CORRECTED)

```
Allowed paths:    engine/path_n_questions.py (the seam ONLY);
                  NEW docs/governance/path_n_content_config/mechanical_path_n_questions.json;
                  NEW tests/test_dgmpr_d3_path_n_domain_neutral_service.py;
                  ENUMERATED RECONCILIATIONS ONLY (§5) in:
                    tests/test_p9_mech_i5_question_sufficiency.py,
                    tests/test_p9e1_path_n_caller_domain_propagation.py,
                    tests/test_d3_core_domain_neutrality.py;
                  governance sync at closure only.
Forbidden paths:  engine/progression_loop.py and every other engine file, web/**, scripts/**, ALL domain packs
                  (byte-frozen — I4 anchor preserved), domains/domain_provenance.json, the electronics artifact
                  file (byte-frozen), every other existing test, schemas/, OWNER_DECISION_REGISTER.md, CI.
                  FORBIDDEN OUTCOMES: second Path-N framework/service/wrapper; Mechanical activation; changes to
                  _STALL_REFRAME / QUESTIONS bank / caller logic; safety/label/weight/THERM-01/D4/D8/Phase-10/
                  PSRR/deployment work; unchecked raw-domain-string file resolution.
```

## §5. CORRECTED RECONCILIATION SET — exactly FIVE expected existing-test flips (re-proven mechanically; anything beyond these = STOP — CONTRACT AMENDMENT)

The corrected end-state simulation, plus a broad pin search (every seam-consuming test file inspected:
`increment_1_owner_expert_boundary`, `workstream_9/10/11`, `phase1/phase2`, `e2_runner_preflight`,
`path_n_content_config_artifact`, `path_n_question_content_specification` — ALL call the seam only via the
None/electronics default and reference no non-electronics domain; the only `path_n_questions.py` hash pin lives in
the I5 file), confirms EXACTLY five flips:

| # | Pin | Current assertion | Why it flips | Authorized reconciliation |
|---|---|---|---|---|
| 1 | I5 `test_dgmpr_seam_blocker_still_present` | mechanical → `None`; None/electronics served | Written to flip at this gate | Replace with the remediated-behavior pin (mechanical served its verbatim artifact; electronics/None unchanged); update the I5 introspected test-inventory list accordingly |
| 2 | I5 `_FROZEN_ENGINE_SHA256["engine/path_n_questions.py"]` | hash `1dcd218a…` | The seam file changes | Re-freeze at the remediated hash (`domain_rules`/`progression_loop` hashes MUST NOT change) |
| 3 | P9-E1 `test_red2_…_no_electronics_stall_reframe` | foreign (mechanical) never reframed at exhaustion | The domain-neutral reframe now truthfully fires at mechanical exhaustion | Reconcile with disclosure; PRESERVE the anti-Electronics truth (never served Electronics text/behavior) |
| 4 | **D3-B `test_d3b_seam_honors_non_electronics_domain_identity`** (`tests/test_d3_core_domain_neutrality.py`) | `get_served_question(gap, 0, domain="mechanical") is None` | Mechanical now receives MECHANICAL Path-N content | Reconcile with disclosure; PRESERVE the original load-bearing truth as: a non-electronics domain must NEVER receive ELECTRONICS content (assert the served content is mechanical-owned, not the electronics entry); the sibling `test_d3b_electronics_and_default_preserved` stays untouched and passing |
| 5 | **P9-E1 `test_red1_get_question_foreign_domain_not_served_electronics_text`** | asserts BOTH `result != electronics_text` AND `result == generic_text` | The generic-fallback equality breaks: mechanical now receives its ARTIFACT text, not the generic variant | Reconcile with disclosure; PRESERVE both anti-Electronics truths (`result != electronics_text`; mechanical service never returns Electronics content) and re-pin `result` to the mechanical artifact text |

The rejected candidate's error is corrected on the record: RED1 was falsely stated to keep passing; D3-B was
omitted entirely. **I4 terminal corpus: NO revalidation** (inventory-scoped; its pinned engine files
`domain_rules.py`/`progression_loop.py` and all packs untouched); every other I5 §12(a) pin (question inventory,
wording, calibration, leakage, provenance, recognition/activation) remains valid and untouched; I1/I2/I3 pins
unaffected. Implementation contradicting any of this → STOP.

## §6. Required evidence (future implementation)

**RED (clean parent, right-reason):** mechanical Path-N service `None` + generic fallthrough despite committed
I5-proven content; mechanical artifact absent. **GREEN:** mechanical served its verbatim artifact through the
canonical seam (all three gap types, all indices, clamping, atomic ServedQuestion identity);
`get_question`/`get_display_question` on `path=="N"` serve mechanical content with the neutral reframe at
exhaustion. **Electronics exact non-regression matrix:** byte-identical served `text`/`question_id` for every
electronics gap type and index under `domain="electronics_electrical"` AND the `None` default (equality against
pre-change captures); stall-reframe behavior identical. **Mechanical latent-service matrix:** service keys on domain
IDENTITY; `support_state("mechanical") == "recognized_not_activated"`; `activated_domains()` unchanged.
**Unsupported-domain/fail-safe matrix:** software/medical_device (recognized, artifact-less) → `None` + generic
fallthrough EXACTLY as today; unknown domain and non-canonical identity strings (incl. path-traversal-shaped
strings, exercising §2's bounded resolution) → `None`; malformed artifact fail-loud. **Verbatim-projection pin:** the
artifact's ten entries equal the pack's `gap_type_mappings` (`question_id`/`text`/order) 1:1. **No cross-domain
leakage; determinism; per-domain cache independence.** **Mutations (each flips a specific pin; none retained):** m1
serve the electronics artifact for mechanical (leakage) → RED; m2 alter one mechanical artifact entry vs its pack
source → verbatim pin RED; m3 tamper the electronics artifact byte → electronics byte pin RED; m4 break the
artifact-less-domain `None` fail-safe → fail-safe pin RED; m5 tamper `progression_loop.py` → its (unchanged) hash
pin RED; m6 expected-text flip in the new tests → RED. **Full governed suite; `git diff --check`; exact scope proof
(only §4 allowed paths; the five §5 flips and nothing else).**

## §7. Closure criteria and boundaries

**Closure:** all §6 evidence green; the FIVE §5 reconciliations executed exactly, each with in-file disclosure
referencing this contract, and a mechanical re-proof that no other existing test changed; the closure record states —
seam domain-neutral; Electronics byte-identical; the LAST D-GMPR-01-D-D3 coupling (`path_n_questions`) DISCHARGED
(web-admission/safety_signal/tie-break were discharged by F002/F001/F004); consequently P9-MECH §12(b) becomes
UNBLOCKED, recordable only at a subsequent Mechanical-lane gate. **Boundaries:** Mechanical remains NOT QUALIFIED /
NOT ACTIVATED; `activated_domains() == ['electronics_electrical']`; §15/§16, safety family, Tier-1 label,
dormant-weight residual, CF-6, CF-2, THERM-01, CAP-12/13, WS-PFV-001, D4, D8, Phase 10, PSRR, deployment — all
untouched with their owners. **STOP conditions:** any forbidden-path need; any flip beyond the enumerated five; any
electronics served-output delta; any content authorship need; any Owner-policy question.
**Next required gate: Mandatory Grill on this exact corrected contract candidate.**
