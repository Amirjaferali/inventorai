# CF-6 — Web Pre-Classifier / Strong-Unsupported Reachability & Admission Interaction — FULL-SCOPE FORMAL CLOSURE RECORD (Candidate)

**Status of THIS record:** governance/documentation-only **FORMAL CLOSURE RECORD CANDIDATE** for `CF-6`. It
implements nothing, changes no runtime/test/domain/registry/activation/schema/persistence file, and closes NOTHING
else (CF-2 is explicitly NOT closed — see §5). **`CF-6 = FULLY DISCHARGED FOR ITS AUTHORITATIVE SCOPE` becomes
authoritative ONLY if/when this exact candidate is merged (create-a-merge-commit) and post-merge verified**
through the governed lifecycle. **`OWNER_DECISION_REGISTER.md` UNCHANGED** (closure is an evidence-based
determination under already-established Owner/governance text — the CF5-F001/F002/F004/CF-5-Audit closure
convention — not a new product-policy decision).

## §1. Authoritative base and fresh verification

Base: `1fe05e098c5ecf53b63088e12e71549635ead70b` (PR #490 — SHA-preserving merge of the accepted CF-6/CF-2
ILT-002 Owner-decision candidate `a3e4300d` onto `3570863e`; merge tree `bcb012b1` == candidate tree; POST-MERGE
PASS; freshly fetched; 0 newer; clean tree) — Owner decision `D-CF6CF2-ILT002-01` is authoritative; full governed
suite **2577 passed / 3 skipped / 1 xfailed / 0 failed** (fresh re-verification).

## §2. Reconstructed CF-6 obligation — exact, cross-document-consistent

**Origin (`CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_CONTRACT.md` §4, area G, verbatim):** *"Web
strong-unsupported layer (CF-6 concerns) — pre-classifier vs post-classifier ordering; strong-unsupported
vocabulary; future activated-domain collisions; admission; ambiguity; session creation; fail-closed behavior."*
§13 of the same contract: *"CF-6 remains separate: PENDING PRE-SECOND-SPECIALIST-DOMAIN-ACTIVATION... CF-6 closes
only via a later separately governed CF-6 gate."*

**Fuller, pre-CF-5 authoritative definition (`P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_FORMAL_CLOSURE_RECORD.md`
§7, verbatim, predates and is consistent with the audit contract):** *"CF-6 — Web pre-classifier / strong-unsupported
reachability & admission interaction: PENDING PRE-SECOND-SPECIALIST-DOMAIN ACTIVATION (distinct from CF-2). Before
the first second-specialist-domain activation, review and disposition the interaction between the Web `/start`
strong-unsupported heuristics, canonical-classifier reachability, activated-domain admission, ambiguity handling,
Web/CLI/core consistency, and public-message truthfulness (which domain signals are intercepted before
`classify_domain`; which reach it; no hidden Electronics admission; no bypass of `AMBIGUOUS_TIE`; whether the
existing unsupported-domain copy remains truthful)."* **This is adopted here as CF-6's exact reconstructed scope**
— it is the most complete, earliest, and most specific authoritative statement, and every later document (the CF-5
closure record's "general Web/CLI pre-classifier consistency remainder," the CF6/CF2 CLI/ILT-002 contracts) is
consistent with it, not narrower or broader.

**Every named CF-6 facet (synthesized, nothing invented):** (1) pre-classifier vs post-classifier ordering / which
signals reach `classify_domain` before admission; (2) strong-unsupported vocabulary interaction with the
activation set; (3) activated-domain admission (no hidden Electronics admission — the SAME canonical activation
truth everywhere); (4) ambiguity handling (no `AMBIGUOUS_TIE` bypass); (5) session creation / fail-closed
behavior; (6) Web/CLI/core consistency (every consumer uses the same canonical classifier, interprets richer
result kinds consistently, fails closed consistently); (7) — shared with CF-2 only, not CF-6-exclusive — whether
public unsupported-domain copy remains truthful.

**What counts as discharge:** every consumer that makes a domain-selection or activation-admission decision uses
the SAME canonical sources (`engine.domain_rules.classify_domain`, `engine.domain_activation.activated_domains`/
`is_activated`) with no hardcoded electronics-only assumption, no duplicate activation registry, and no silent
classifier bypass — OR is an explicitly Owner-governed, documented exception (ILT-002) — OR belongs to a
DIFFERENT already-closed tracker (CF5-F001/F002/F003/F004, D-GMPR-01-D-D3) and is not new CF-6 debt.

**What does NOT count as discharge:** narrowing the scope by assumption because the two most recently worked
facets (the CLI literal, the ILT-002 ambiguity) are resolved — CF-6's own text requires "full stated scope"
confirmation, which THIS record's §3 sweep performs exhaustively, not selectively.

**CF-6 is: a broader shared-facet obligation** — not classifier-consistency alone, not activated-domain-truth
consumption alone, not domain-selection consistency alone. It is the SIX-dimension interaction defined above,
spanning every Web/CLI/shared consumer that decides or reports on domain admission.

## §3. Mandatory full-scope adversarial sweep — methodology and complete classification

**Methodology.** An independent read-only sweep (Explore agent, zero write access) exhaustively grepped:
`"electronics_electrical"` literals across `web/*.py engine/*.py scripts/*.py`; every `classify_domain(` /
`activated_domains(` / `is_activated(` / `_admit_specialist_domain(` call site; any second activated-domains-style
registry; every `web/templates/*.html` "electronics" occurrence; cold-load/persistence-restore seams
(`path_n_questions.py`, `deliverable_assembler.py`, `progression_loop.py`, `session_reconstruction.py`);
question/gap-selection domain branching; every executable script that could drive session creation; every
`infer_domain` definition/call site. This session then personally read full surrounding context for every
ambiguous match (`web/app.py:1639`, `engine/progression_loop.py:415`, `scripts/run_summary_demo.py`,
`DOMAIN_CONFIRM_VALUE`'s full consumer list, every session-creation write site) before classifying. No item is
left unclassified.

**Complete classification table (every suspicious match; six-category scheme):**

| Item | Location | Classification |
|---|---|---|
| `_PUBLIC_DOMAIN_LABELS` dict key | `web/domain_label.py:24` | **3 — SHARED-CONSUMER — CANONICAL** (presentation-only; documented truthful neutral fallback for unmapped domains) |
| `DOMAIN_CONFIRM_VALUE = "electronics_electrical"` | `web/app.py:873` | **5 — HISTORICAL / NON-EXECUTABLE** (exhaustively confirmed: zero production-logic readers; used ONLY as a test-convenience form-data constant across ~20 test files; comment confirms POST `/start` no longer reads it) |
| `_unsupported_domain_message` electronics branch | `web/app.py:925` | **3 — SHARED-CONSUMER — CANONICAL** (wording selected from the caller's activation-derived `activated` value; already-discharged F002 pattern) |
| `_confirmation_required_message` electronics branch | `web/app.py:939` | **3 — SHARED-CONSUMER — CANONICAL** (same pattern) |
| `is_elec_only = (activated == [...])` | `web/app.py:1162` | **3 — SHARED-CONSUMER — CANONICAL** (`activated` derived from `_activated_specialist_domains()`) |
| Weak-conflict resolution branch (`sole == "electronics_electrical" and _is_recognized_not_activated(...)`) | `web/app.py:1639` | **2 — GOVERNED EXCEPTION** (in-code comment explicitly tags this "activation-aware since CF5-F002 (CF-6 facet)"; independently reviewed and merged under `D-CF5-F002-01`; condition-gated behind the registry/activation-driven `_is_recognized_not_activated` helper, not a hardcode) |
| Three `start_ilt002_*` routes | `web/app.py:1786,1799,1812` | **2 — GOVERNED EXCEPTION** (`D-CF6CF2-ILT002-01`) |
| `_ELECTRONICS_DOMAIN` legacy default | `engine/path_n_questions.py:36,48` | **6 — OUTSIDE CF-6 — TRACK UNDER `D-GMPR-01-D-D3`** (already FULLY DISCHARGED; the domain-neutral seam remediation is a separate, already-closed lane) |
| `_MVP_DOMAIN = "electronics_electrical"` | `engine/safety_signal.py:55` | **6 — OUTSIDE CF-6 — TRACK UNDER `CF5-F001`** (already FORMALLY CLOSED) |
| `_LEGACY_ZERO_ACTIVATED_PRECEDENCE` | `engine/domain_rules.py:211` | **6 — OUTSIDE CF-6 — TRACK UNDER `CF-3` / `CF5-F004`** (already FORMALLY CLOSED/DISCHARGED) |
| `_ACTIVATED_DOMAINS = frozenset({"electronics_electrical"})` | `engine/domain_activation.py:39` | **3 — SHARED-CONSUMER — CANONICAL** (this IS the one legitimate activation source of truth, not a duplicate) |
| CLI scope-check + confirmation copy | `scripts/run_cli.py:90,106` | **3 — SHARED-CONSUMER — CANONICAL** (the freshly discharged, mutation-tested CLI facet) |
| `classify_domain` definition + call sites | `engine/domain_rules.py:215` (def); `web/app.py:1602`, `scripts/run_cli.py:54` (calls); `engine/domain_rules.py:308` (internal, via `infer_domain`) | **3 — SHARED-CONSUMER — CANONICAL** (exactly one classifier, no duplicated ownership) |
| `activated_domains`/`is_activated`/`_admit_specialist_domain` call sites | `web/app.py:892,977,1700`; `engine/subsystem_model.py:76`; `engine/domain_rules.py:198,242`; `scripts/run_cli.py:84` | **3 — SHARED-CONSUMER — CANONICAL** (single source, consistently consumed) |
| Second activated-domains-style registry | repo-wide sweep | **no hits** — confirms no duplicate source of truth exists |
| `web/templates/index.html` electronics copy (5 occurrences) | `index.html:20-22,26,54,59` | **3 — SHARED-CONSUMER — CANONICAL** (every rendered occurrence gated behind `start_is_electronics_only`/`start_sole_domain`, both server-computed from `_activated_specialist_domains()`) |
| `ui_text.py` copy strings (`UI_B_INDEX_006/007/009`) | `web/ui_text.py:153,157,162` | **3 — SHARED-CONSUMER — CANONICAL** (inert data, reachable only through the gated template branches above) |
| `deliverable_assembler.py`, `progression_loop.py` domain handling | throughout | **3 — SHARED-CONSUMER — CANONICAL** (fully generic `state.domain`/`domain` propagation; no electronics-specific branch found) |
| `session_reconstruction.py` domain restore | `session_reconstruction.py:137,140,166-167` | **3 — SHARED-CONSUMER — CANONICAL** (reads persisted `confirmed_domain` verbatim; NO default; fails closed — returns early — on missing domain) |
| Scoring-correction rule requiring an electronics-domain substance signal | `engine/progression_loop.py:415` (context read in full) | **1 — LEGITIMATE DOMAIN-SPECIFIC** (a specific, Owner-authorized scoring-correction rule's evidentiary requirement — substantive scoring content, not an admission/activation-truth consistency matter; analogous to Mechanical's own domain-scoped rule nuances) |
| `scripts/e2_path_n_smoke_runner.sh`, `scripts/e2_exact_matcher.py` | throughout | **2 — GOVERNED EXCEPTION** (already-known ILT-002/E-2 evidence tooling, protected by `D-CF6CF2-ILT002-01`) |
| `scripts/run_summary_demo.py:18` (`state.domain_signal = "electronics"`) | read in full this gate | **6 — OUTSIDE CF-6** (a standalone, offline "C phase acceptance test" that hand-builds an `IdeaState` and calls `build_summary` directly; NEVER calls `classify_domain`, `activated_domains`, `is_activated`, or `_admit_specialist_domain`; makes no admission decision and drives no session/route at all — not a shared admission consumer within CF-6's reconstructed scope; non-blocking observation, no existing tracker applies) |
| `scripts/verify_parity.py`, `build_replay_fixtures.py`, `check_extract_json_contract.py`, `check_normalize_output_contract.py`, `run_replay_benchmark(_v2).py`, `write_governance_docs.py` | repo-wide sweep | **no hits** — clean |
| `infer_domain` definition + call sites | `engine/domain_rules.py:297` (def, delegates internally to `classify_domain`); zero production call sites; all real call sites in `tests/*.py` | **3 — SHARED-CONSUMER — CANONICAL** (legacy wrapper, no duplicate classification logic, unused in production) |
| Stale comment claiming `/start` uses `infer_domain` | `tests/test_increment_1a_actions.py:39` | **5 — HISTORICAL / NON-EXECUTABLE** (a comment in a test file; does not match current `web/app.py` behavior which calls `classify_domain` directly at line 1602; non-blocking documentation staleness, not a code defect — flagged for future comment-hygiene, not a CF-6 residual) |
| Every session-creation write site (`SESSION_STORE[sid] = ...`) | `web/app.py:1732` (`/start`), `web/app.py:1770` (`_finalize_started_session`, shared by ILT-002), `web/app.py:1845` (`show_session` NB-R1 cold-load restore) | **3 — SHARED-CONSUMER — CANONICAL** (all three trace to `_admit_specialist_domain` for domain assignment, or restore an already-persisted, already-admitted domain verbatim; no fourth, undiscovered session-creation path exists) |

**Result: zero items classified `4 — SHARED-CONSUMER — DEFECT`.** Every match resolves to canonical/governed
behavior, legitimate domain-specific content, an already-closed separate tracker, historical/non-executable
material, or a genuinely out-of-scope standalone script.

## §4. CLI facet and ILT-002 facet disposition (restated, authoritative)

**CLI facet: DISCHARGED** (merge `6524e792786644d3053aeac650bdfa7888ad0653`, candidate `6f1ad899` — `scripts/
run_cli.py` now derives admissibility from `domain_activation.activated_domains()`, mutation-tested, zero
Electronics regression). **ILT-002 facet: RESOLVED BY OWNER DECISION, NOT A DEFECT** (merge
`1fe05e098c5ecf53b63088e12e71549635ead70b`, `D-CF6CF2-ILT002-01` — the fixed-domain design is a governed protocol
invariant; activation enforcement already correctly in place via `_admit_specialist_domain`; no remediation
required or authorized).

## §5. Non-effects (no over-closure)

This closure closes ONLY `CF-6`, for the reconstructed scope in §2, on the evidence in §3. It does NOT: close
`CF-2` (public-message truthfulness remains its own separate, OPEN tracker — the residual truthfulness question
preserved by `D-CF6CF2-ILT002-01` §"CF-2 residual preserved" stays open pending CF-2's own full-scope sweep; CF-2's
Arabic-localization and non-`/start` template items are entirely untouched); activate Mechanical
(`activated_domains() == ['electronics_electrical']`, `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS;
NOT ACTIVATED`, unchanged); authorize Tier-1 (still deferred to activation-readiness, P9-MECH-QC §13); close
Phase 9 (remains OPEN — CF-2, the Tier-1 label, NMF-1/FU-1 are already-discharged/OPEN as their own items, and
explicit Owner activation authorization is still outstanding); touch D4 (SEPARATE / UNEXECUTED), D8
(Owner-reserved), THERM-01 (future-only); authorize Phase 10, PSRR, or deployment. No runtime, test, script, or
domain file is touched by this candidate.

## §6. Closure statement and scope of THIS candidate

**`CF-6 = FULLY DISCHARGED for its authoritative reconstructed scope`** — authoritative ONLY after this
candidate's own merge and post-merge verification. Governance/documentation only: this NEW closure record +
`ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md`
current-truth sync. `OWNER_DECISION_REGISTER.md` UNCHANGED (closure-gate convention, matching CF5-F001/F002/F004
and the CF-5 Audit umbrella's own closure precedent). ZERO runtime/test/pack/registry/activation/schema/
persistence diff. **Next required gate: Mandatory Grill on this exact candidate**, then the governed lifecycle.
After this closure merges, the remaining pre-activation items are: CF-2's own full-scope closure gate; the
Tier-1 EN/AR label (at activation-readiness); NMF-1/FU-1 disposition (already discharged); and explicit Owner
activation authorization — each separately authorized; nothing here activates or pre-authorizes any of them.
