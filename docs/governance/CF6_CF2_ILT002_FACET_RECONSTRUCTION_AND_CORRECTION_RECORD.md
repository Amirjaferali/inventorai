# CF-6 / CF-2 — ILT-002 Shared-Facet Reconstruction & Correction (governance-only; NO implementation authorized) — CORRECTED candidate

**Status of THIS record:** governance/documentation-only **RECONSTRUCTION & CORRECTION RECORD**. It implements
nothing — no runtime, Web, CLI, test, domain, activation, schema, or persistence change. It does NOT close CF-6 or
CF-2 (globally or for ILT-002), does NOT touch the Tier-1 label, does NOT activate Mechanical. Its purpose is
narrower than a scoping contract: a full evidence-based reconstruction of the ILT-002 shared facet PROVED that the
premise carried forward from the CF-6/CF-2 CLI scoping contract — that ILT-002's hardcoded domain selection is a
technical-debt bug analogous to the CLI's — is **INCOMPLETE in a materially different way than the CLI facet
was**. This record corrects that characterization with fresh evidence and determines that **no bounded
implementation gate can be scoped here without an explicit Owner decision first**. **`OWNER_DECISION_REGISTER.md`
UNCHANGED** (this record makes no new product-policy decision; it identifies that one may be needed and stops
short of proposing one). **DOCUMENTED NO-VALID-RED.**

**Candidate lineage:** a first reconstruction candidate `cad135c5f75233dc3fd175d93f0a5a28fe197eed` was self-Grilled
and self-REJECTED (material completeness defect: the mandatory hidden-surface sweep's route/file inventory omitted
two consumer-tooling files independently found on a fresh post-freeze re-sweep — `scripts/e2_exact_matcher.py`
[transcript-path helper] and `scripts/e2_path_n_smoke_runner.sh` [an Owner-authorized E-2 Path-N evidence smoke
runner that POSTs to `/start_ilt002_combination_lock_path_n`] — even though the same conclusion held once found)
and is preserved as immutable rejected evidence. THIS corrected candidate is created from the SAME authoritative
parent with the sweep table completed.

## §1. Authoritative base and fresh verification

Base: `6524e792786644d3053aeac650bdfa7888ad0653` (PR #488 — SHA-preserving merge of the accepted CF-6/CF-2 CLI
shared-facet implementation candidate `6f1ad899` onto `305961ae`; merge tree `4b8b191f` == candidate tree;
POST-MERGE PASS; freshly fetched; 0 newer; clean tree) — the CLI shared facet is DISCHARGED for both CF-6 and
CF-2 (both trackers remain globally OPEN); full governed suite **2577 passed / 3 skipped / 1 xfailed / 0 failed**
(fresh re-verification).

## §2. Exact ILT-002 route inventory and control-flow reconstruction (A–E)

**A. Three routes, verbatim** (`web/app.py:1779-1817`): `POST /start_ilt002_water_leak`,
`POST /start_ilt002_combination_lock`, `POST /start_ilt002_combination_lock_path_n` (the third additionally sets
`state.path = "N"`). Each handler is otherwise structurally identical. Confirmed exhaustive by a fresh
`@app.route.*ilt002` grep across `web/app.py` this gate — no fourth route definition exists anywhere in the
repository.

**B. Exact seam each route uses:** `idea_text = request.form.get("idea", "").strip()` → new `IdeaState` →
`state.domain = _admit_specialist_domain("electronics_electrical")` → `state.domain_signal = state.domain` →
`run_iteration(state, idea_text)` → `_finalize_started_session(...)` (the SAME shared finalizer `/start` uses,
durably creating the P4-1b-1 project envelope before advertising the live session).

**C. How submitted idea text reaches `run_iteration`:** `idea_text` is passed DIRECTLY as `run_iteration`'s
response/content argument — the SAME parameter used for an answered-iteration response elsewhere in the engine. It
is NEVER passed to `classify_domain`. It functions as the initial mechanism-evidence content for the
already-fixed `electronics_electrical` domain, not as classification input.

**D. Where classification is bypassed:** entirely — `engine.domain_rules.classify_domain` is never called or
imported in any ILT-002 route. `web.app.classify_domain` (used by `/start` and `web.app.infer_domain`/
`_admit_specialist_domain`'s callers elsewhere) plays no role here.

**E. Where activation is already enforced:** `_admit_specialist_domain` (`web/app.py:966-981`, verified again this
gate) calls `domain_activation.is_activated("electronics_electrical")` and raises `DomainNotActivatedError` if not
activated. This is IDENTICAL enforcement to every other web specialist-admission site (`OWNER_DECISION_REGISTER.md`
D-S5-03: "all web specialist-admission sites bound to the policy via `_admit_specialist_domain`"). **Confirmed:
activation enforcement fully exists on all three routes; nothing here is missing or duplicated.**

## §3. CRITICAL FINDING — the fixed-domain design is GOVERNED, INTENTIONAL, and TESTED, not an oversight

This is the material correction this record exists to make. Fresh evidence, found during the mandatory
hidden-surface sweep (§5), proves the ILT-002 routes' hardcoded domain selection is **deliberate governed
behavior with its own dedicated regression test — and is the load-bearing basis of a SECOND, separately Owner-
authorized evidence-gathering procedure beyond the route definitions themselves (§5)** — not an accidental
defect analogous to the CLI's:

- `tests/test_web_app.py::test_governed_ilt002_routes_remain_electronics_pinned_after_restriction` (verbatim
  comment): *"The generic `/start` restriction must not affect the electronics-pinned governed ILT-002 / Path N
  routes."* This test submits `{"idea": "any idea text"}` — deliberately domain-NEUTRAL, non-electronics text —
  to all three routes and asserts they still succeed (302) with `state.domain == "electronics_electrical"`
  **regardless of the submitted text's actual content**. This is the opposite of a classifier-bypass bug pin: it
  is an explicit invariant that these routes must NEVER derive domain from submitted text.
- `tests/test_web_app.py::test_start_ilt002_water_leak_forces_electronics_domain` pins the EXACT electronics-
  specific question text `run_iteration` returns for this scenario ("Describe how your electronic circuit
  achieves its intended function…") — proving the fixed domain is load-bearing for the route's actual downstream
  content, not merely its admission gate.
- `scripts/e2_path_n_smoke_runner.sh` (found in §5's sweep) is a standalone, Owner-authorized "E-2 Path N smoke
  runner (Gate B, B-2)" that POSTs a FIXED, VERBATIM, "Owner-authorized fixed response array (D-2) —
  `E2_OPERATIONAL_PROCEDURE.md` §6. Verbatim from committed §7.2. No substitution permitted" idea/response
  sequence to `/start_ilt002_combination_lock_path_n` and produces an "E-2 ACCEPTED"/"E-2 NOT ACCEPTED" evidence
  verdict via exact-text matching (`scripts/e2_exact_matcher.py`) against a committed Path-N artifact. This is a
  SECOND, independent, Owner-authorized evidence-gathering procedure (beyond the ILT-002 evidence-ledger itself)
  that depends on this exact route always producing the fixed electronics domain for its fixed script.
- Commit-history evidence (`docs/governance/AB-006_FINAL_CLOSURE_RECORD.md`): `"ILT-002 water leak fixed-domain
  route"`, `"/start_ilt002_combination_lock route"`, `"ILT-002 authoring gap closure"` — these routes were
  authored as **fixed-domain scenario routes for a separate, dedicated ILT-002 evidence-ledger protocol**
  (referenced governance apparatus: `ILT002_EXECUTION_GUIDE.md`, `ILT002_FORM_T.md`,
  `ILT002_EMERGENCE_TIMING_TABLE.md`, the AA-2/AA-4A/AB-006 lineage), used to produce comparable, fixed-domain
  evidence transcripts (`AUTHORIZATION_REVIEW.md`: *"Source: ILT-002 transcripts… The fixed-domain route
  `/start_ilt002_combination_lock` is in place"*). Changing the domain-selection mechanism would alter the
  semantic basis of that separate evidence-ledger protocol's already-produced and future transcripts, AND would
  break the E-2 Path N smoke runner's fixed-response/exact-match evidence procedure.
- The P4-1b-2a REV1 Owner disposition (`OWNER_DECISION_REGISTER.md` D-P4-1B-2A-IMPL-01/`-02`, BF4) that made
  these routes durably backed is SCOPED ONLY to persistence/token/idempotency mechanics ("legacy `start_ilt002_*`
  routes durably backed (usable, unlinked)") — it says nothing about, and does not authorize changing, domain
  selection. It neither froze nor unfroze that design; domain-selection was simply untouched by that decision.

**Conclusion: there is no "hardcoded domain-selection bug" to fix here analogous to the CLI facet.** The CLI's
hardcoded check was an unintentional oversight with no governing test asserting it must stay hardcoded; ILT-002's
is the opposite — an intentional, tested, dual-protocol-serving invariant (the ILT-002 evidence ledger AND the
separate E-2 Path N smoke-evidence procedure both depend on it).

## §4. CF-6 / CF-2 exact obligations reassessed against this finding (F, G)

**F. CF-6's exact obligation, reassessed.** CF-6 was originally described (audit contract, CF6/CF2 CLI scoping
contract §2) as covering "the CLI's hardcoded electronics literal" and, by extension, "the legacy fixed-domain
ILT-002 routes (which retain governed hardcoded electronics literals outside this surface)" — note the ROADMAP'S
OWN prior wording already said **"governed hardcoded electronics literals"**, which in hindsight was accurate and
should have been read literally rather than assumed equivalent to the CLI's ungoverned oversight. CF-6's
pre-classifier-consistency concern for ILT-002 is, on this evidence, **not actionable as a bounded technical
fix**: the routes ARE consistent with the canonical activation policy (§2/E); their INCONSISTENCY with
`/start`'s classifier-driven admission is the intended, tested, dual-protocol-serving design (§3), not a defect.
Whether CF-6 should still consider this consistent (i.e., whether "pre-classifier consistency" as an audit goal
ever intended to include deliberately-scenario-fixed routes) is a **scope-of-obligation question CF-6's own
eventual full-scope closure gate must answer** — this record does not answer it, only reports the evidence.

**G. CF-2's exact obligation, reassessed.** No user-facing copy tied to these routes was found anywhere (§5) — no
template references `water_leak`, `combination_lock`, or `ilt002` in rendered copy; the resulting session page is
the SAME generic session template every session uses, truthfully reflecting the actually-stored
`state.domain == "electronics_electrical"` (which is TRUE for these routes by design). **CF-2's "ILT-002 route
copy" item, as listed in the roadmap's CF-2 residual inventory, appears to have no live surface to fix** — there
is no untruthful public claim on these routes today. This record flags this as a finding, not a closure: CF-2's
own eventual full-scope gate should confirm or correct this reading before removing the item from its residual
list.

## §5. Mandatory hidden-surface sweep — classification table (CORRECTED, complete)

| Surface | Finding | Classification |
|---|---|---|
| Three ILT-002 route definitions | `web/app.py:1779-1817`, exhaustively enumerated (§2/A); fresh `@app.route.*ilt002` grep confirms exactly three, no fourth | Confirmed OUT OF SCOPE for any bounded technical fix (§3) |
| Hardcoded `"electronics_electrical"` arguments | `_admit_specialist_domain("electronics_electrical")` × 3 (one per route) | MUST REMAIN UNCHANGED (governed, tested, §3) |
| `run_iteration` calls | One per route, `run_iteration(state, idea_text)`, unconditional | MUST REMAIN UNCHANGED |
| Session persistence writes | `_finalize_started_session` → `_get_store().create_project(... reconstruction_inputs=_reconstruction_inputs(seed_idea, state))` — `confirmed_domain` persisted as `state.domain` (= `"electronics_electrical"`) | MUST REMAIN UNCHANGED — changing domain-selection would change persisted `confirmed_domain` and downstream NB-R1 cold-load restoration semantics for these sessions |
| Action/review routes consuming results | `/session/<sid>` (generic, shared with all sessions) — no ILT-002-specific action/review route exists | OUT OF SCOPE (no ILT-002-specific consumer beyond the generic session surface) |
| Templates/copy | Zero matches for these route names or `ilt002` in `web/templates/*.html` (verified this gate) | OUT OF SCOPE — no live CF-2 copy surface found (§4/G) |
| Repo-wide `ilt002` reference sweep (fresh, `grep -rl` over `web/ engine/ scripts/`) | Exactly three files reference `ilt002` outside the route definitions themselves: `web/app.py` (the routes); `scripts/e2_exact_matcher.py:74` — `_resolve_transcript_path` returns a default `/tmp/ilt002_transcript_{sid}.jsonl` path (a transcript-file-naming convention, consumed by the E-2 matcher tool; does not touch domain-selection); `scripts/e2_path_n_smoke_runner.sh:24` — `START_ROUTE="/start_ilt002_combination_lock_path_n"`, the Owner-authorized E-2 Path N smoke-evidence runner (§3) | `e2_exact_matcher.py`: OUT OF SCOPE, transcript-path naming only, no domain-selection role. `e2_path_n_smoke_runner.sh`: OUT OF SCOPE, but material CORROBORATING EVIDENCE for §3 — a second Owner-authorized fixed-response procedure depends on this route's fixed domain; MUST REMAIN UNCHANGED if that procedure is to remain valid |
| Tests referencing route names | 9 files (the CF6/CF2 CLI contract's own count, re-confirmed this gate): `test_success_criteria.py` (uses a `/tmp/ilt002_transcript_*` path matching the matcher's default, unrelated to domain-selection — transcript-file-naming only), `test_web_app.py` (the two governed-pinning tests, §3), `test_increment_1_owner_expert_boundary.py`, `test_security_containment_r6_r16.py` (path/security-containment checks, unrelated to domain-selection), `test_path_n_content_config_artifact.py` (a needle-string check, unrelated to domain-selection), `test_p4_1b2a_legacy_ilt002_durability.py` (durability/token contract, REV1-scoped, unrelated to domain-selection), `test_phase1_path_designation.py`, `test_path_n_question_content_specification.py` (a needle-absence check, unrelated), `test_session_friendly_gap_labels.py` | MUST RECONCILE ONLY IF an Owner-authorized domain-selection change is later scoped; NONE require any change today |
| Response-text pins | `test_start_ilt002_water_leak_forces_electronics_domain`'s exact electronics-specific question-text equality pin (§3) | MUST REMAIN UNCHANGED (load-bearing evidence of the governed design) |
| Hash/snapshot pins over `web/app.py` or these routes specifically | None found (verified this gate: no `sha256`/`hashlib` pin covers `web/app.py`'s ILT-002 lines) | N/A — no hash surface exists to flip |
| P4-1b-2a durability/persistence coupling | `test_p4_1b2a_legacy_ilt002_durability.py` — REV1/BF4 scope is durability/token mechanics ONLY (§3), not domain-selection | OUT OF SCOPE for any domain-selection question; already CLOSED (`D-P4-1B-2A-IMPL-01`) and not reopened by this record |

**No hidden fourth ROUTE exists** (§2/A). Two hidden CONSUMER/TOOLING surfaces beyond the routes and their nine
test files were found on this corrected sweep (`e2_exact_matcher.py`, `e2_path_n_smoke_runner.sh`) — both are
classified OUT OF SCOPE for any technical change, and the smoke runner is additional corroborating evidence for
§3 rather than a new obligation.

## §6. Persistence/session/action-semantics answer (N)

**Yes, materially** — changing hardcoded domain selection would change the persisted `confirmed_domain`
reconstruction input, the downstream engine question content (proven domain-specific, §3), and would contradict
the dedicated governed-pinning test's own explicit invariant, AND would break the separate Owner-authorized E-2
Path N smoke-evidence procedure's exact-match verdict (§3/§5). This is a strictly higher-consequence change than
the CLI facet's (which touched no persisted state and no other Owner-authorized procedure, only ephemeral CLI
console output).

## §7. Classifier-reuse answer (O)

Moot given §3: no classifier reuse is being scoped, because no defect requiring classification exists on these
routes under the current governed design. Were an Owner to ever authorize a redesign, `engine.domain_rules.
classify_domain` remains the sole canonical classifier and would be the only correct reuse target (no second
framework) — but that is a hypothetical future gate, not this one.

## §8. CF-2-only localization/template boundary (P)

Not implicated — §5 found zero ILT-002-specific template/copy surface at all, so there is no localization work
of any kind (CF-2-only or shared) to bound here.

## §9. Determination — exact next gate

**No implementation gate is created or authorized by this record.** Per the task's own anti-duplication
preference and CLAUDE.md's stop conditions ("historical truth becomes ambiguous," "semantic origin becomes
unclear" → diagnosis preferred over speculative coding): the correct outcome of this reconstruction is **STOP
before implementation** — not because an existing contract already fully scopes it (the CF6/CF2 CLI contract
explicitly did NOT scope ILT-002's implementation, only deferred it), but because **fresh evidence disproves the
deferred premise that ILT-002 domain-selection is a bounded technical-debt bug**. Any further ILT-002 gate
requires an **explicit Owner decision** on a genuine product/protocol question this record is not authorized to
answer: whether the ILT-002 evidence-ledger routes' fixed-domain design should ever change, and if so, under what
protocol-preserving terms (e.g., a NEW route/mechanism rather than altering the existing evidence-producing
routes, to avoid retroactively changing the semantic basis of already-produced transcripts and to avoid breaking
the separate E-2 Path N smoke-evidence procedure). This record surfaces that question; it does not decide it.

## §10. CF-6 / CF-2 tracker status (unchanged; no closure of any kind)

**CF-6 remains globally OPEN**: the ILT-002 facet is NOT discharged, NOT implied discharged, and is now recorded
as requiring Owner input before any further technical work; CF-6's open-ended "full stated scope" beyond the CLI
facet (already discharged) and this reassessed ILT-002 item remains outstanding. **CF-2 remains globally OPEN**:
the ILT-002 "route copy" item is reassessed as likely moot (§4/G) but NOT closed by this record — Arabic
localization and the non-`/start` template sweep remain fully outstanding and untouched. **Tier-1 EN/AR label**
remains deferred until activation-readiness (P9-MECH-QC §13; reconfirmed, unchanged, not addressed here).
**Mechanical remains NOT ACTIVATED**; `activated_domains() == ['electronics_electrical']`; no D4/D8/THERM-01/
Phase 10/PSRR/deployment; no P9 closure.

## §11. Scope of THIS record

Governance-only: this NEW record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` +
`CURRENT_PROJECT_STATE.md` current-truth sync. ZERO runtime/test/pack/registry/activation/schema/persistence/ODR
diff. **Next required gate: Mandatory Grill on this exact candidate**, then the governed lifecycle. No further
ILT-002 gate should be attempted until the Owner has reviewed §3/§9 and either (a) confirms no change to ILT-002's
fixed-domain design is wanted (in which case CF-6's ILT-002 item is effectively N/A and CF-2's is effectively
moot, pending each tracker's own full-scope closure gate to say so formally), or (b) authorizes a specific,
protocol-preserving design for a future gate to scope and implement.
