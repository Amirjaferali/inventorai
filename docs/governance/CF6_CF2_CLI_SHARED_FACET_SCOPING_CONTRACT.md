# CF-6 / CF-2 — CLI Shared-Facet Scoping Contract (governance-only; joint scoping — implements nothing) — CORRECTED candidate

**Status of THIS record:** governance/documentation-only **SCOPING CONTRACT CANDIDATE**, jointly scoping BOTH
`CF-6` (Web/CLI pre-classifier consistency) and `CF-2` (public-message truthfulness) around their shared CLI
facet, naming both owners explicitly. **It implements nothing in this gate** — no runtime, Web, CLI, test, domain,
activation, schema, or persistence change. It defines WHAT a later, separately-authorized bounded implementation
must achieve and HOW it will be proven. It does NOT close CF-6 or CF-2 as whole trackers, does NOT touch the
ILT-002 legacy-route facet (§2), does NOT touch the Tier-1 label, and does NOT activate Mechanical.
**`OWNER_DECISION_REGISTER.md` UNCHANGED**. **DOCUMENTED NO-VALID-RED.**

**Candidate lineage:** the first scoping candidate `71c16d533f5c5ac014e669d16f8f65ee13192c2a` was independently
REJECTED (two material defects: (1) a fabricated/misattributed quotation — text actually found in
`P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §12 (the D-GMPR/Mechanical-qualification lane) was wrongly
attributed to `CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md` §5, which contains no such sentence; (2) a
technical mischaracterization of the ILT-002 legacy routes as "bypassing classification/activation entirely" —
`_admit_specialist_domain` DOES enforce `domain_activation.is_activated(domain)`, so activation is NOT bypassed;
only classification/domain-selection of the submitted idea text is bypassed) and is preserved as immutable
rejected evidence. THIS corrected candidate is created from the SAME authoritative parent and corrects exactly
those two defects; the structurally sound conclusions the reviewer confirmed are preserved unchanged in substance.

## §1. Authoritative base and fresh verification

Base: `2b985844f093b2730fa6618e6ee2d29e32c87af8` (PR #486 — SHA-preserving merge of the accepted CF-5 NMF-1/FU-1
test-hardening candidate `1ea78443` onto `91f4e5c6`; merge tree `2d43c53e` == candidate tree; POST-MERGE PASS;
freshly fetched; 0 newer; clean tree) — NMF-1 and FU-1 are DISCHARGED; `activated_domains() ==
['electronics_electrical']`; full governed suite **2573 passed / 3 skipped / 1 xfailed / 0 failed** (fresh
re-verification: the two touched files' 112 tests re-run green at this base).

## §2. Reconstructed scope, overlap, and dependency graph

**CF-6 — exact original owner and unresolved obligation.** Originated `CF5_RETROSPECTIVE_ADVERSARIAL_
ARCHITECTURE_AUDIT_CONTRACT.md` §4.G/§13 (audit area "Web strong-unsupported layer" — pre-classifier vs
post-classifier ordering; strong-unsupported vocabulary; admission; fail-closed behavior). Facets (i)–(iv) were
discharged by the F002/CF-6 corrective implementation (the `/start` admission surface only). **Remaining
obligation (verbatim, `CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_FORMAL_CLOSURE_RECORD.md` §6):** "the
general Web/CLI pre-classifier consistency remainder (including the CLI's §5-I2-bypassing electronics literal)
stays in the CF-6 lane" — and the roadmap's own record of the F002 closure additionally names "the legacy
fixed-domain ILT-002 routes (which retain governed hardcoded electronics literals outside this surface)." CF-6
closes only via its own later governed gate "confirming its full stated scope" (audit §13) — an open-ended
consistency-audit obligation, not exhausted by fixing any single named literal.

**CF-2 — exact original owner and unresolved obligation.** Originated the same audit contract §4.H/§14
(public-message truthfulness). The `/start` flow's copy was discharged inside the F002/CF-6 contract §6.
**Remaining obligation (verbatim, roadmap CF5-F002-closure entry):** "public-message truthfulness on every other
surface — CLI copy; legacy ILT-002 route copy; templates/pages outside the `/start` admission flow that assert or
imply electronics-only support; localization of the generalized admission copy (... narrow-Arabic limitation
until CF-2's own gate); and any other public 'electronics only' assertion." CF-2 remains trigger-bound and
separate; Mechanical's own Tier-1 label work explicitly does NOT discharge, close, or absorb it
(`P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §13).

**C. Every remaining open facet of each (as currently named in repository text; open-ended, not claimed
exhaustive):**
- CF-6: (a) the CLI's hardcoded electronics-only domain check (§2/D below); (b) the ILT-002 legacy routes'
  hardcoded domain selection (§2/D below); (c) any other not-yet-named pre-classifier-consistency issue (the
  audit's "full stated scope" is confirmed only by CF-6's own eventual closing gate, not enumerated exhaustively
  anywhere yet).
- CF-2: (a) CLI copy; (b) ILT-002 route copy; (c) non-`/start` templates/pages; (d) Arabic localization of the
  generalized (non-electronics-pinned) copy — CF-2-ONLY, no CF-6 overlap; (e) any other public electronics-only
  assertion.

**D. Overlap matrix — CORRECTED for technical precision (this candidate's fix).**

| Facet | CF-6 claims it | CF-2 claims it | Code location | Activation enforcement |
|---|---|---|---|---|
| CLI hardcoded domain check + copy | Yes | Yes | `scripts/run_cli.py:60,65-70` — classifies via the REAL canonical `classify_domain` (verified this gate), then compares the result against the hardcoded string `"electronics_electrical"` instead of consulting `engine.domain_activation.activated_domains()`. **The CLI never calls the canonical activation policy at all** — it has its own hardcoded electronics-only truth, independent of and not bound to `engine.domain_activation`. This IS a genuine bypass of the canonical **activated-domain truth**, not merely a classification issue. |
| ILT-002 legacy routes' hardcoded domain selection | Yes | Yes | `web/app.py:1779-1815` — three routes (`/start_ilt002_water_leak`, `/start_ilt002_combination_lock`, `/start_ilt002_combination_lock_path_n`), each calling `_admit_specialist_domain("electronics_electrical")` with a HARDCODED domain argument — the submitted idea text is never classified/routed to a domain at all. **`_admit_specialist_domain` (verified this gate, `web/app.py:966-981`) DOES enforce `domain_activation.is_activated(domain)` and raises `DomainNotActivatedError` if not activated — so canonical activation policy IS already enforced on these routes.** The gap is hardcoded **domain selection** (classifier bypass), NOT activation bypass. Consistent with `OWNER_DECISION_REGISTER.md` D-S5-03 ("all web specialist-admission sites bound to the policy via `_admit_specialist_domain`"). |

**Reconciliation of the prior "one CLI-literal facet" summary (P9-MECH-SF contract §1):** that summary was
INCOMPLETE, not wrong for what it named — the CLI facet it identified is real and accurately described there. The
ILT-002 facet was simply not enumerated in that summary. This is recorded here as a later, additional
evidence-based clarification, NOT a correction of an invalid prior record; the P9-MECH-SF contract remains
authoritative for its own scope and is not reopened.

**E/F/G. May one bounded gate discharge shared facets for both while keeping trackers distinct? Are separate
contracts mandatory? Is one joint contract smaller/safer than two overlapping implementations?** YES to joint
discharge for a genuinely shared facet, by inference from the F002/CF-6 precedent's actual behavior (an INFERENCE,
not a quotation): `CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md` §5 shows ONE implementation discharging
facets (i)-(iv) of CF-6 AND the `/start`-copy facet of CF-2 together, while stating explicitly (§5, verbatim)
"CF-6 is NOT auto-declared complete — CF-6 closes only via its own later governed gate confirming its full stated
scope" — i.e. CF-6 and CF-2 remained separately tracked and neither closed as a whole lane, even though one
implementation touched both. From this behavior, the inference drawn here is: a single bounded gate MAY operate on
a genuinely shared facet on behalf of both trackers, provided it does not declare either tracker's full scope
discharged. Two SEPARATE implementations touching the identical code lines would duplicate ownership/duplicate
review of the same diff — strictly less safe and not smaller. A single joint gate, explicitly naming both owners
and explicitly scoped to NOT close either lane, is the smaller, safer choice. Separate CONTRACTS are not mandatory
when one gate is scoped this way — but explicit joint naming (not a silent merge) is required, and is what THIS
document provides.

**H. Obligations beyond the shared facets?** YES, both lanes have them (§2 item C): CF-6's open-ended "full stated
scope" beyond the two named facets, and CF-2's Arabic-localization item plus the general non-`/start` sweep. None
of these are touched, waived, or implied-closed by this contract or its future implementation.

**I. Tier-1 timing.** Confirmed unchanged and out of scope here: `P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md`
§13 — the label becomes truthful only at activation-readiness; implementing it now would label an unserved domain.
No dependency on this contract; correctly sequenced after ALL technical blockers, including this one.

**J. Hidden-blocker sweep.** The two-shared-facet finding (§2/D) is this gate's hidden-facet correction — no
FURTHER hidden facet found beyond CLI + ILT-002 in the currently committed governance text; CF-6's and CF-2's own
"beyond-named-facets" residuals (§2/C, §2/H) are pre-existing, already-registered open-endedness, not newly
discovered blockers. No third shared facet identified.

## §3. Scoping decision — smallest correct next gate

Given the ILT-002 legacy routes touch **nine** existing test files (`test_success_criteria.py`,
`test_web_app.py`, `test_increment_1_owner_expert_boundary.py`, `test_security_containment_r6_r16.py`,
`test_path_n_content_config_artifact.py`, `test_p4_1b2a_legacy_ilt002_durability.py`,
`test_phase1_path_designation.py`, `test_path_n_question_content_specification.py`,
`test_session_friendly_gap_labels.py` — a durability/persistence-adjacent surface, P4-1b-2a lane) versus the CLI
facet's **four** touching files (§4 below), and given "smallest" governs: **THIS contract bounds its future
implementation to the CLI facet ONLY.** The ILT-002 routes facet is confirmed (§2/D) as a second shared CF-6/CF-2
facet — a hardcoded-domain-selection / classifier-bypass / public-copy-truthfulness gap, with activation
enforcement already correctly in place and NOT to be duplicated or re-added — but is explicitly DEFERRED to its
own future joint gate (separately authorized; likely requiring coordination with the P4-1b-2a durability lane
given its test footprint) — NOT combined into this gate, and NOT silently dropped.

## §4. The bounded FUTURE implementation — exact definition (governance only; NOT executed by this contract)

```
INCREMENT CONTRACT — CF-6/CF-2 CLI Shared-Facet Discharge   [implementation NOT started]
Responsibility:   Replace scripts/run_cli.py's hardcoded `if domain != "electronics_electrical":` scope check
                  (and its accompanying hardcoded "electronics/electrical ideas only" copy) with derivation from
                  the canonical activation policy (`engine.domain_activation.activated_domains()`), reusing the
                  EXISTING admission authority exactly as CF5-F002 did for the Web `/start` surface — no new
                  admission mechanism, no second consent framework. Under `['electronics_electrical']` (today's
                  only governed activation state) CLI behavior MUST remain byte-identical: the same refusal for
                  any non-electronics-classified idea, the same proceed-and-run flow for electronics. Copy
                  updates MUST be truthful under a broadened (currently hypothetical, test-double-only) activation
                  set — never asserting "electronics only" when more domains are activated — mirroring the CF-2
                  facet of the F002 fix (`web/app.py::_unsupported_domain_message`).
Allowed paths:    scripts/run_cli.py (the scope-check branch and its copy ONLY — no other CLI behavior change:
                  the classifier dispatch for AMBIGUOUS_TIE/MULTI_DOMAIN_NEEDS_D4/UNRESOLVED_NON_ACTIVATED_TIE
                  richer kinds, the iteration loop, and the summary output are UNTOUCHED); the enumerated
                  reconciliation files (§5) ONLY; closure-time governance sync only.
Forbidden paths:  web/app.py (incl. the ILT-002 routes — deferred, §3; already activation-bound via
                  `_admit_specialist_domain`, so NO activation-check addition is needed or permitted there);
                  web/domain_label.py; every engine file; every domain pack; scripts/ other than run_cli.py;
                  every other existing test. FORBIDDEN OUTCOMES: any Electronics-only behavior delta; any
                  activation state change; any Tier-1 label work; any ILT-002 route change; any CF-6 or CF-2
                  full-lane closure claim; any duplicate/new activation-enforcement mechanism.
```

**Objective criteria for the CLI fix:** (1) reuse the canonical activation policy exactly — no bespoke CLI-only
admission logic; (2) truthful copy under any activation set, not just electronics-only; (3) byte-identical
Electronics-only behavior (the F002 non-degradation discipline); (4) no change to the classifier-dispatch richer-
kind branches (AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4 / UNRESOLVED_NON_ACTIVATED_TIE), which are unrelated to the
scope-check literal and already correctly derive from the real classifier.

## §5. Preliminary reconciliation sweep (informational; the future implementation's OWN mandatory exhaustive
sweep, per the D-GMPR exhaustive-flip-enumeration doctrine, is not waived or pre-concluded by this preview)

Six existing tests reference the CLI across four files: `test_cf5_f003_classifier_matching_semantics.py`
(`test_red_cli_false_positive_no_electronics_confirmation`, `test_green_cli_electronics_proceeds`);
`test_p9e2r_result_representation.py` (`test_red_r11_cli_bounded_stop_on_richer_kinds`,
`test_cli_single_electronics_proceeds`); `test_p9e2_multi_activated_tie_precedence.py`
(`test_red_e2_11_cli_real_tie_bounded_stop` — exercises the AMBIGUOUS_TIE richer-kind branch under a broadened
`activate()` double, NOT the scope-check literal); `test_cf5_f004_priority_fallback_extensibility.py`
(`test_green_focused_cli_bounded_stop`). Preliminary read: none of the six currently broadens activation past
electronics-only AT the scope-check branch specifically (the one test that does use `activate()` exercises a
different, richer-kind branch untouched by this contract's scope) — so NO flip is currently anticipated, but the
future implementation MUST perform its own fresh, exhaustive grep-based sweep before freezing (this preview is not
a substitute).

## §6. Closure criteria and boundaries

**This contract's own closure:** Mandatory Grill PASS on this exact candidate, independent review, Owner
acceptance, merge, post-merge verification — authorizes ONLY the §4 bounded implementation as a SEPARATE future
gate (itself requiring its own Create→Grill→review→accept→publish lifecycle). **Expected discharge effect of THIS
scoping contract: NONE** — it discharges nothing; it only authorizes/fences the later CLI-facet implementation
gate. **Non-effects:** does NOT close CF-6 or CF-2 (only the future implementation's specific facet, at THAT
gate's own closure); does NOT touch the ILT-002 facet (§3, deferred); does NOT touch the Tier-1 label; does NOT
activate Mechanical; no D4/D8/THERM-01/Phase 10/PSRR/deployment; no P9 closure. `activated_domains() ==
['electronics_electrical']` unchanged. `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED`
unchanged. **STOP conditions for the future implementation:** any Electronics behavior delta; any flip beyond the
exhaustive sweep it must perform; any touch to a forbidden path; any Owner-policy question (e.g. how the CLI
should present a MULTI-domain activated set — out of scope while `['electronics_electrical']` is the only governed
state, but the future gate must flag if Owner input becomes necessary). **Next required gate: Mandatory Grill on
this exact scoping contract candidate**, then the governed lifecycle; thereafter the separately-authorized
CLI-facet implementation gate.
