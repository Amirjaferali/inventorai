# CF5-F002 / CF-6 — Web `/start` Multi-Domain Admission — Corrective Implementation Contract (Candidate)

**Status of THIS record:** governance/documentation-only **CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE** for CF-5 finding
**CF5-F002** (independently VALIDATED **C**, record
`docs/governance/CF5_F002_WEB_START_ADMISSION_INDEPENDENT_VALIDATION_RECORD.md`, merged PR #452) and its shared-surface **CF-6**
facets. It defines **WHAT** a later bounded implementation must achieve and **HOW** it will be proven; **it implements NOTHING** —
no runtime, Web, CLI, test, domain, activation, schema, or persistence change in this gate. **It does NOT close CF5-F002, CF-6,
CF-2, or CF-5, and selects/registers/activates no domain.** It becomes authoritative only if this exact candidate passes the
Mandatory Grill → independent external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving publication → PR →
pre-merge verification → CREATE A MERGE COMMIT → post-merge verification. Expected engine / Web / CLI / domains / Registry /
activation / schema / persistence / API / test diff in THIS gate: **ZERO**. The only production-relevant change in this gate is the
authoritative recording of Owner decisions **D1/D2** in `OWNER_DECISION_REGISTER.md` (§2) — a documentation record, not code.

**Authoritative base:** `8d8dc1541568b7debedb51e094b15004964c333f` (PR #452 — CF5-F002 validation merge; freshly fetched; 0 newer);
boot OK; `activated_domains() == ['electronics_electrical']`.

**Subordinate to** CLAUDE.md, the committed governance anchors, the CF-5 Audit contract (§7 validation / §8 C-policy / §13 CF-6
separation), the CF5-F002 validation record, and Owner decisions **OD-F/G/H**, **D-P6-03/06/15**, **D-S5-03/04**,
**D-GMPR-01-D-D3** (which govern that multi-domain was deferred and that the current electronics-only behavior must not be silently
broadened). This contract does not rewrite those; it records the **bounded** consent/admission policy (§2) they explicitly left for
the pre-trigger gate.

---

## §1. Validated defect boundary (restated, authoritative)

The Web `/start` admission surface (`web/app.py`) hardcodes a single-activated-domain (electronics-only) admission architecture
that does not consume the canonical activation set as a *set*. Four facets (validation record §1; tree `e5f7d42c`/`8d8dc154`):

1. **Consent/admission constant** — `DOMAIN_CONFIRM_VALUE = "electronics_electrical"` (`web/app.py:837`); every admitted session
   is `state.domain = _admit_specialist_domain(DOMAIN_CONFIRM_VALUE)` (`:1420`) — the admitted domain is a hardcoded constant, not
   the classified/consented domain.
2. **Hardcoded admission branch** — `if domain != "electronics_electrical":` (`:1391`) + `CONFLICTING_SUPPORTED_DOMAINS`
   (`:845`) treat every non-electronics classification as conflict/rejection regardless of activation state.
3. **Strong-unsupported vocabulary** — `_STRONG_UNSUPPORTED_WORDS` / `_STRONG_UNSUPPORTED_SUBSTRINGS` (`:897-919`) mark registered
   domains' signals permanently "unsupported", independent of activation (the CF-6 facet).
4. **Public copy** — `UNSUPPORTED_DOMAIN_MESSAGE` / `MECHANISM_GUIDANCE_MESSAGE` (`:826-829, 954-959`) assert "electronics and
   electrical ideas only", truthful only while electronics is the sole activated domain (the CF-2 facet).

`_admit_specialist_domain` (`:853-868`) itself correctly binds admission to the §5-I2 activation policy; the defect is that every
caller passes the electronics constant. **Present reachability: NONE** (validation §5-§6: extensionally equivalent to the canonical
policy under `['electronics_electrical']`). **Exact trigger:** the first moment `activated_domains() != ['electronics_electrical']`
(adding any non-electronics activated domain → four wrong-admission modes; removing electronics → HTTP 500 at `:1420`). **This is a
mandatory pre-trigger corrective prerequisite (audit §8, C-policy): it MUST close before any activation gate makes
`activated_domains() != ['electronics_electrical']`.**

## §2. Recorded Owner decisions (bounded consent/admission policy)

The multi-domain `/start` consent/admission UX was deferred by OD-F/G/H, D-P6-03/06/15, D-S5-04. This gate resolves ONLY the bounded
policy needed for this pre-trigger corrective contract; it authorizes **no** general multi-domain orchestration, domain activation,
D4, D8, or unrelated UX expansion. Recorded authoritatively in `OWNER_DECISION_REGISTER.md` as **D-CF5-F002-01**:

- **D1 — Multi-domain `/start` consent model = "Confirm classifier-selected domain".** When the canonical classifier resolves
  exactly one **activated** specialist domain: `/start` presents that classifier-selected activated domain; the user explicitly
  confirms or declines it; **no auto-admit without confirmation**; the persisted session-domain **equals the classified + confirmed
  domain**; **no manual domain selection is required** when the classifier already resolved one valid activated domain.
  `AMBIGUOUS_TIE` remains fail-closed unless separately governed.
- **D2 — NONE fallback under multi-domain activation = "Require explicit user choice".** When classification is `NONE` **and more
  than one specialist domain is activated**: do **not** silently fall back to Electronics; do **not** silently choose a default;
  present **only currently activated** specialist domains; the user explicitly chooses one; the chosen domain is then explicitly
  confirmed/consented; the persisted session-domain equals the chosen + confirmed domain. **Backward compatibility:** for the current
  single activated-domain state `['electronics_electrical']`, preserve the current governed `NONE`→Electronics explicit-consent
  behavior unchanged.
- **D3 — Consequence (mechanical, not a new decision).** When Electronics is absent from the activation set, `/start` derives
  behavior from the canonical activated-domain set with **no Electronics special case** and **no accidental
  `DomainNotActivatedError` / HTTP 500** merely because Electronics is absent.

**Mechanically-derived corner (no new policy; from D1+D2+D3, recorded to remove ambiguity for §5.C):** when classification is `NONE`
and **exactly one** specialist domain is activated (whichever it is), `/start` offers that sole activated domain under explicit
consent and persists it — the domain-neutral generalization of today's `['electronics_electrical']` `NONE`→Electronics behavior
(D2 backward-compat + D3 no-special-case). Explicit multi-choice (D2) applies only when ≥2 domains are activated.

## §3. Corrective objective & the canonical seam

Generalize the admission surface to consume the **canonical activation set** (`engine.domain_activation.activated_domains()` /
`is_activated`) and the **canonical classifier** (`engine.domain_rules.classify_domain`) as the sole sources of truth, replacing the
hardcoded electronics constant/branch/vocabulary/copy with activation-set-derived behavior implementing D1/D2/D3. **No new admission
authority is created**; `_admit_specialist_domain`'s §5-I2 binding is the single activation gate and is preserved.

## §4. Required GREEN behavioral matrix (the later implementation MUST satisfy exactly)

Activation state is exercised **only** via self-restoring in-process `_ACTIVATED_DOMAINS` doubles in tests (the committed P9-E2/§5-I2
mechanism); **no real activation change**. "Confirm" = the explicit consent step; "persist" = `state.domain` in the created session.

### A. Current Electronics-only activation `['electronics_electrical']` (backward compatibility — NO user-visible regression)
- `SINGLE(electronics_electrical)` + confirm → **302 admitted**, persist `electronics_electrical`; without confirm → 200
  `CONFIRMATION_REQUIRED`, no session (unchanged).
- `NONE` + confirm → admitted as `electronics_electrical` (governed None-fallback + explicit consent), unchanged.
- Recognized-but-not-activated (`SINGLE(mechanical/medical_device/software)`, not activated) → refused (guidance/unsupported), no
  session (unchanged). `AMBIGUOUS_TIE` production-unreachable today → fail-closed if constructed. All public copy unchanged & truthful.

### B. Electronics + one additional activated domain (double)
- `SINGLE(electronics_electrical)` → confirm Electronics; persist Electronics.
- `SINGLE(<other activated domain>)` → show that classified domain; require confirmation; **persist that exact domain** (no
  electronics mislabel).
- `NONE` → require **explicit choice among currently activated domains** (both), then confirmation; persist chosen+confirmed domain.
- **Recognized-but-not-activated MUST NOT be offered** as a choice and MUST NOT be admitted.
- `AMBIGUOUS_TIE` (both activated, tied) → **fail-closed**, no session (unless separately governed).
- **Strong-unsupported vocabulary MUST NOT suppress an activated domain**: an idea whose domain is now activated must not be refused
  merely because its signal was in the static unsupported vocabulary (CF-6 facet).

### C. Non-Electronics-only activation (Electronics absent, e.g. double `{mechanical}` / `{mechanical, software}`)
- **No Electronics special case; no accidental 500.**
- `SINGLE(<activated domain>)` → confirm the classified domain; persist same domain.
- `NONE` with **exactly one** activated domain → offer that sole activated domain under explicit consent; persist it (§2 derived
  corner). `NONE` with **≥2** activated domains → explicit choice required.
- If any residual ambiguity is discovered at implementation time that D1/D2/D3 do **not** resolve, the implementation gate **STOPs**
  and returns the smallest exact Owner question rather than inventing policy.

### D. 3+ activated domains (triple double; domain-neutral; **no hardcoded fixed list**; NO D4 execution)
- `SINGLE(<activated domain>)` → confirm classifier-selected activated domain; persist it.
- `NONE` → explicit choice from the full activated set; persist chosen+confirmed.
- `AMBIGUOUS_TIE` → fail-closed. `MULTI_DOMAIN_NEEDS_D4` remains **never produced** by `classify_domain`; its `/start` branch stays
  dormant/fail-closed; D4 NOT executed.

### E. Public messaging (truthful; minimal CF-2 only)
- Copy MUST derive truthfully from the actual activation/admission state; MUST NOT assert "electronics only" when other specialist
  domains are activated. Include only the CF-2 messaging work necessary to make THIS admission flow truthful; **do not close CF-2
  globally** (§8).

### F. Session integrity
- Persisted `state.domain` MUST equal exactly the domain classified/chosen AND explicitly confirmed. **No cross-domain session
  mislabeling** (the sharpest validated defect, P-E.3).

### G. UI-language independence
- `ui_lang` MUST NOT alter the classifier result, the activated-domain set, the offered domain choices, the admission result, or the
  persisted session-domain. Classification/admission are pure functions of idea text + activation set.

## §5. CF-6 relationship (shared surface / same trigger; NOT a duplicate framework)

**Included here** (the CF-6 facets that share this exact admission surface and trigger): (i) the pre-classifier / strong-unsupported
interaction insofar as it **suppresses an activated domain** (§4.B strong-unsupported); (ii) **no hidden Electronics admission** of a
non-electronics classification (§4.B/F); (iii) **no `AMBIGUOUS_TIE` bypass** (§4.B/D fail-closed); (iv) **no activated-domain
suppression by stale unsupported vocabulary**. **Remaining separate CF-6 obligations** (NOT dispositioned here): general Web/CLI
pre-classifier consistency audit beyond `/start` admission, and any CF-6 scope not on this admission surface. **Disposition criteria:**
this contract's implementation, once merged and post-merge verified, discharges ONLY facets (i)-(iv) above; **CF-6 is NOT
auto-declared complete** — CF-6 closes only via its own later governed gate confirming its full stated scope (audit §13). The
contract MUST state, at implementation closure, exactly which CF-6 facets were discharged and which remain open.

## §6. CF-2 relationship (co-triggered; NOT absorbed)

Only the messaging changes needed for truthful admission under a broadened activation set (§4.E) are in scope. **CF-2 (public-message
truthfulness) is NOT closed** by this work; any CF-2 obligations beyond this admission flow's copy remain separate and trigger-bound.
The contract MUST record the residual independent CF-2 obligations at implementation closure.

## §7. Stale-comment hygiene (bounded; same surface only)
The later implementation MUST correct, in this same admission surface, the validated stale comments (validation §9): (a) the
`SUBSTRINGS` wording and `app`⊂`appliance` example (`web/app.py:870-884`), false since CF5-F003 whole-token matching; (b) the stale
"`classify_domain()` today yields only SINGLE / NONE … dormant" narrative (`web/app.py:1361-1363`), stale since P9-E2 produces
`AMBIGUOUS_TIE`. **Only** these comments, because they directly document the corrected surface. **No** broadening into unrelated
documentation cleanup.

## §8. Scope fence (later implementation)

**Allowed production path (minimal, evidence-backed):** `web/app.py` (the `/start` admission surface: message constants, the consent
constant, the admission branch, the strong-unsupported gate, the admission call, and the two stale comments). **Focused tests:** a
NEW `tests/test_cf5_f002_web_admission_multidomain.py` (and/or mechanically-justified additions to existing Web-admission tests). If
any additional production path becomes mechanically required, the implementation gate **STOPs before expanding scope** and reports
the evidence. **Forbidden unless separately justified by repository evidence:** canonical classifier semantic change
(`engine/domain_rules.py`); activation-policy / activation-set change (`engine/domain_activation.py`); domain
activation/selection/registration; Domain-Pack change; D4 execution; D8 change; broad engine redesign; unrelated CLI redesign;
unrelated UI-framework work; schema/persistence change. `OWNER_DECISION_REGISTER.md` changes ONLY in THIS contract gate (recording
D1/D2); the implementation gate makes ZERO ODR change.

## §9. Required RED→GREEN + regression + mutation evidence (the later implementation MUST provide)

**RED (reproduce the latent defect under activation doubles; fail pre-fix, pass post-fix):** (r1) an activated second domain's idea
still refused ("electronics only"); (r2) an activated second-domain input admitted under a WRONG electronics session
(cross-domain mislabel); (r3) no confirmation path exists for the second domain (`DOMAIN_CONFIRM_VALUE` sole confirm); (r4) stale
strong-unsupported vocabulary blocking an ACTIVATED domain; (r5) Electronics-absent → accidental `DomainNotActivatedError`/500;
(r6) untruthful "electronics only" copy after activation-set broadening.
**GREEN:** the full §4 A-G matrix, via **real Flask `/start`** (test client), self-restoring `_ACTIVATED_DOMAINS` doubles,
asserting **persisted session-domain correctness**, `NONE`, `SINGLE`, recognized-but-not-activated inadmissibility, `AMBIGUOUS_TIE`
fail-closed, 3+ activated, UI-language independence, and **session cleanup** (no `SESSION_STORE` / durable-DB pollution).
**Full regression suite** green (no pre-existing regression; record exact counts).
**Mutation probes (each CAUGHT RED, bytecode-isolated, bytes restored):** (m1) restore hardcoded `DOMAIN_CONFIRM_VALUE` electronics
constant; (m2) restore `domain != "electronics_electrical"` branch; (m3) wrong session-domain persistence; (m4) consent bypass
(auto-admit without confirmation); (m5) hidden default on `NONE` under multi-activation; (m6) an inactive (recognized-not-activated)
domain offered/admitted as a choice; (m7) strong-unsupported vocabulary overriding an activated domain; (m8) `AMBIGUOUS_TIE`
accidental admission; (m9) Electronics-absent crash; (m10) UI-language/domain coupling.
**Broad differential sweep:** authoritative-parent `/start` vs implementation over a broad activation-state × idea corpus; **every
delta categorized** (backward-compatible-unchanged; activated-second-domain correction; strong-unsupported activation-awareness;
messaging truthfulness; Electronics-absent graceful); **ZERO unexplained deltas** (any is blocking).

## §10. Backward-compatibility & rollback
Under `['electronics_electrical']` every `/start` outcome MUST be behaviorally identical to the authoritative parent except the
governed §7 comment cleanup (comment-only, zero runtime effect). No user-visible regression is acceptable. The change is a bounded
generalization of one Web surface; rollback = revert the single `web/app.py` change (no schema/persistence/data migration; existing
sessions unaffected — `state.domain` semantics preserved, only the *source* of the value generalized).

## §11. Exact closure criteria (the later implementation may close CF5-F002 ONLY when ALL hold)
D1/D2/D3 behavior implemented exactly (§4 A-G GREEN); current Electronics-only behavior preserved (§4.A); activation-set broadening
correct (§4.B/D); Electronics-absence correct (§4.C, no 500); no cross-domain session mislabel (§4.F); no hidden fallback under
`NONE` multi-activation (§4.B/C); activated-domain choices derive from the canonical activation set; recognized-but-not-activated
remain inadmissible; public messaging truthful (§4.E); CF-6 overlap dispositioned per §5 (facets (i)-(iv) discharged; CF-6 not
auto-closed); §7 stale comments corrected; full suite green; Mandatory Grill PASS; independent external review ACCEPT of the exact
candidate; Owner exact-candidate acceptance; SHA-preserving merge; post-merge verification. **This contract candidate does NOT close
CF5-F002, CF-6, CF-2, or CF-5, and activates no domain.**

## §12. Governance disposition & non-effects
**CF5-F002 = OPEN C — corrective contract candidate (this record).** CF5-F003 = CLOSED; CF5-F001 = OPEN C; CF5-F004 = OPEN C; CF-5 =
OPEN; CF-6 / CF-2 = PENDING, separate, trigger-bound (this contract governs only the shared-surface facets §5/§6); D4 SEPARATE /
UNEXECUTED; D8 Owner-reserved; `activated_domains() == ['electronics_electrical']`; **NO domain selected/registered/activated; first
new-domain activation remains BLOCKED** (behind this pre-trigger prerequisite among others). This contract relates to the mandatory
Pre-Phase-9 Core Domain-Neutrality gate **D-GMPR-01-D-D3** (it specifies the bounded Web-admission portion) without discharging that
gate's other couplings (`engine/safety_signal.py` = CF5-F001; `engine/path_n_questions.py`; hard-coded tie-break = CF5-F004/CF-3).

## §13. Scope of THIS candidate & next gate
Governance/documentation only: this NEW corrective-contract record + `OWNER_DECISION_REGISTER.md` (record D1/D2 as D-CF5-F002-01) +
`ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **ZERO**
runtime / test / Web / CLI / domain / Registry / activation / schema / persistence / API / guardrail diff. **Next required gate:
Mandatory Grill on this exact candidate**; any material finding rejects it as-is (fresh candidate from the authoritative parent — no
in-place amendment). After this contract is authoritative, the bounded CF5-F002/CF-6 **implementation** is the subsequent separately
governed gate.
