# D3 — Pre-Phase-9 Core Domain-Neutrality — Bounded Contract & Acceptance Criteria

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE** (D3). **It becomes the authoritative
contract-of-record ONLY if this exact accepted candidate is merged (create-a-merge-commit) and post-merge verified.** Until
then it authorizes nothing. It **defines** the smallest implementation contract + acceptance criteria for the three
currently-proven remaining core domain-neutrality couplings (**D3-A / D3-B / D3-D**); it **implements nothing**, changes no
runtime/test/Domain-Pack/web file, activates no domain, and decides no D8 disposition. **DOCUMENTED NO-VALID-RED — CONTRACT-ONLY
GOVERNANCE GATE** (no runtime behavior is created here; the future D3 **implementation** gate MUST use genuine behavioral
RED→GREEN). This gate does not authorize D3 implementation, Phase 9, IoT, any domain activation, Phase 10, PSRR, OD-Q/`main`
reconciliation, deployment, or production.

**Authoritative base:** `00792af36e51808191690a4bf66f9b1a2644d477` (PR #433 — **Phase-8 formal closure merge, already merged at
this base**; parents `e7f7bc7` + `0839c3a`; tree `ed76558ae950287f7fe8936da9261595ce0bcd05`), verified read-only before editing;
boot OK.

**Authorization lineage (truthful).** This is the **first Owner-authorized** D3 contract gate; the Owner's authorization begins
with the instruction that created THIS candidate. A **prior draft candidate `ed5eb14596a3f99e5d6febc90f3ba70a1e91f995` was
REJECTED (process/scope violation + correction required)** and is **NOT** Owner-authorized, **NOT** merged, and must never be
pushed/published/PR'd/merged/amended/rebased or presented as accepted; it is preserved only as historical evidence. This
candidate is **fresh** (new SHA + new tree) and reuses only the **independently-reviewed technical substance**, not the
rejected governance surfaces.

**Lineage / authority.** Fulfils the registered **D3 — Core Domain-Neutrality Prerequisite Gate** (G-MPR-01-D §D3). Subordinate
to CLAUDE.md and the committed anchors. Consumes — never duplicates — the CLOSED canonical owners **`engine/domain_registry.py`**
(§5-I1 / D-P6-14) and **`engine/domain_activation.py`** (§5-I2), and the CLOSED §5-I3 subsystem cross-domain model.
**D-FPC-MAP-06:** extend/consume existing seams; create no new owner.

---

## 1. Purpose & required meaning of neutrality

Make the shared/core domain-dependent seams **consume the already-accepted canonical Domain Registry / Activation authorities
instead of silently assuming Electronics**, so the core can **safely support a future additional governed domain — without
activating one in this gate.** Required meaning of domain neutrality (binding): *the shared/core architecture can safely support
another governed domain* — **NOT** "electronics-specific content is forbidden." Electronics-specific safety cues and electronics
question **content** may remain electronics-owned; the defect is shared/core **behavior/policy** that assumes electronics is the
only possible governed domain.

## 2. Accepted baseline (closed prerequisites — do NOT reopen or duplicate)

- **CLOSED / AUTHORITATIVE (treated as closed unless fresh live evidence proves a regression):** D-P6-14 / **§5-I1** (canonical
  owner `engine/domain_registry.py` — do not duplicate registry hardening); **§5-I2** Activation Status Policy (canonical owner
  `engine/domain_activation.py`; live semantics `ACTIVATED` / `RECOGNIZED_NOT_ACTIVATED` / `UNKNOWN_OR_UNSUPPORTED` — do not
  duplicate activation-status policy); **§5-I3** Subsystem Cross-Domain Model; **§5-CLOSE**.
- **Phase 8 — FORMALLY CLOSED / AUTHORITATIVE at this base** (PR #433 merged as `00792af`). This is present current-truth, not a
  pending event.
- **Current activation baseline:** **`electronics_electrical` is the ONLY activated specialist domain**
  (`domain_activation._ACTIVATED_DOMAINS = frozenset({"electronics_electrical"})`). Recognized Domain Packs
  (`mechanical` / `medical_device` / `software`, valid v1.0) are `RECOGNIZED_NOT_ACTIVATED` — **recognition ≠ activation**;
  preserved explicitly.

## 3. In-scope current defects (exactly three; A/B/D) — independent-review findings preserved

### 3A. D3-A — Safety-signal core domain coupling — `engine/safety_signal.py`
- **Reviewed live evidence (real):** electronics-only `_MVP_DOMAIN = "electronics_electrical"`; `_has_electrical_context`
  treats electronics-or-electrical-terms as the sole context; **`domain_context = domain if domain == _MVP_DOMAIN else
  _MVP_DOMAIN`** unconditionally stamps electronics onto the produced signal's domain context. A non-electronics domain case
  either receives no domain-appropriate safety behavior or is misleadingly stamped Electronics.
- **Contract obligation:** the future implementation MUST **remove the inappropriate electronics-only assumption from the
  shared safety decision seam** while **preserving legitimate domain-owned Electronics safety content/semantics**, by consuming
  the canonical activation/registry authority where a domain decision is made. **Do NOT create a second safety-policy registry**
  unless independent evidence proves there is no existing canonical extension seam.

### 3B. D3-B — Path-N shared question-selection domain coupling — `engine/path_n_questions.py`
- **Reviewed live evidence (real):** `_ARTIFACT_PATH` is pinned to the Electronics Path-N artifact
  (`electronics_electrical_path_n_questions.json`); `get_served_question(gap_type, iterations_open)` /
  `get_path_n_question(gap_type, iterations_open)` are **domain-blind** (no canonical domain identity). (The **domain-specific**
  path `engine/domain_rules.get_domain_question(domain, …)` is already neutral / registry-owned and is NOT a defect.)
- **Contract obligation:** the future implementation MUST make shared Path-N selection **consume the existing canonical domain
  identity / Domain-Pack ownership** rather than silently assuming Electronics — electronics question **content** stays
  electronics-owned. **Do NOT create another question framework / registry / orchestration framework** unless independently
  proven necessary.

### 3D. D3-D — Hard-coded domain priority / tie-break behavior — `engine/domain_rules.py`
- **Reviewed live evidence (real):** `infer_domain` contains an ungoverned hard-coded tie-break `priority = ["medical_device",
  "electronics_electrical", "mechanical", "software"]` that can rank a `RECOGNIZED_NOT_ACTIVATED` domain **above** the activated
  `electronics_electrical` (all four packs are registered with `classification_signals`).
- **Contract obligation:** the future implementation MUST **remove or neutralize the inappropriate hard-coded priority** so a
  recognized-but-not-activated domain **cannot become effective activated routing/admission authority**, by respecting canonical
  activation state (and governed Domain-Pack metadata where sufficient). **Do NOT invent a permanent commercial/product ranking
  policy and do NOT build a new routing framework.**

## 4. Explicitly OUT OF SCOPE (independent-review findings preserved)

- **D3-C — Web Admission / Public Domain Labeling:** **EXCLUDED** — independently verified as remediated / not a remaining
  core-neutrality blocker. The canonical admission owner is `engine/domain_activation.py` (admission bound via
  `web/app.py::_admit_specialist_domain` → `is_activated`); public labeling uses the accepted P6-1 resolver
  (`web/domain_label.py::public_domain_label`). Remaining Electronics literals are **not, by themselves, a D3 defect.**
  **`web/app.py` and `web/domain_label.py` MUST NOT be changed under this D3 contract unless fresh live evidence proves a
  regression** (in which case STOP and report before drafting a different scope).
- **D8 / `iot_electronics`:** Owner-reserved; **deferred to the appropriate IoT-activation decision boundary**; **not a blocker
  to core D3 neutrality work** unless fresh repository evidence proves otherwise. `domains/iot_electronics/**` (+
  `schemas/iot_electronics_output.schema.json`, `prompts/iot_electronics_system_prompt.md`) MUST NOT be deleted / migrated /
  normalized / validated-into-v1.0 / repurposed / activated. No disposition (superseded / future IoT seed / benchmark-only) is
  selected here.
- **Also excluded:** runtime implementation; test implementation; IoT activation; any domain activation
  (`mechanical`/`medical_device`/`software`/`iot_electronics`); domain content expansion; Phase 9 activation; Phase 10; PSRR;
  OD-Q/`main` reconciliation; deployment; production; commercial activation; QTA / ACV / PDF / Email / WS17 / STG.

## 5. Canonical owners (reused; no duplicate owner created)

| Responsibility | EXISTING CANONICAL OWNER USED |
|---|---|
| Domain Registry | **`engine/domain_registry.py`** (§5-I1) — consumed |
| Activation / support-status policy | **`engine/domain_activation.py`** (§5-I2) — `support_state` / `is_activated` / `activated_domains` consumed by the safety-signal + tie-break seams |
| Domain-specific question metadata/content | existing governed **Domain-Pack** ownership (registry `gap_type_mappings`; `domain_rules.get_domain_question` already neutral) — consumed |
| Non-specialist Path-N question content | the electronics-owned Path-N artifact remains electronics content; only the **selection seam** consumes canonical domain identity |
| Domain label resolution / web admission | **`web/domain_label.py`** (P6-1) / **`web/app.py`** bound to §5-I2 — unchanged (out of scope) |

Rule: **EXISTING CANONICAL OWNER? YES → consume/extend it. NO → prove a bounded responsibility before creating another owner.**
The contract PROHIBITS a second Domain Registry / activation-policy owner / cross-domain model / global domain orchestrator /
question framework / routing framework.

## 6. Likely implementation file boundary (RED-driven; not blanket-authorized)

- **Likely allowed (only files proven necessary by RED evidence):** `engine/safety_signal.py`, `engine/path_n_questions.py`,
  `engine/domain_rules.py`, plus **focused tests**; governance/current-truth files at publish/closure time.
- **Prohibited (unless a future accepted amendment allows):** `web/app.py`, `web/domain_label.py`, `domains/iot_electronics/**`,
  any new domain pack, any domain activation, new persistence/schema, new commercial/payment module, new global orchestrator /
  routing framework / registry / activation-policy subsystem, broad Domain-Pack redesign, Phase-9 domain-specific content.

## 7. Behavioral invariants (frozen)

1. Electronics remains the **only activated specialist domain** during D3 (unless separately authorized later).
2. Existing Electronics user-visible behavior remains **semantically compatible** — anchored to the existing green
   safety-signal / Path-N / progression / `domain_rules` regression behavior — unless a current bug is fixed and explicitly
   documented.
3. A `RECOGNIZED_NOT_ACTIVATED` domain MUST NOT become admitted/routed **as activated** by winning an inference score.
4. Non-electronics context MUST NOT silently inherit Electronics-specific safety semantics.
5. Shared non-specialist Path-N selection MUST NOT silently assume Electronics when a canonical domain identity is present.
6. No new domain becomes active as a side effect of making the core neutral.
7. `domains/iot_electronics/**` remains untouched.
8. `engine/domain_registry.py` remains the canonical registry owner. 9. `engine/domain_activation.py` remains the canonical
   activation/support owner.
10. D3 remains provider/commercially neutral and independent of Phase-8 access/billing machinery.
11. OD-N / deterministic-core commercial-import protections remain satisfied. 12. Existing fail-closed behavior preserved.

## 8. Genuine RED → GREEN acceptance plan (future implementation gate — NOT run here)

**8A. D3-A RED —** demonstrate the current incorrect electronics `domain_context` behavior at the shared safety seam for a
non-electronics domain case (forced/mapped to electronics semantics). **NOT** a test whose only assertion is the absence of the
word "electronics." GREEN: shared logic no longer assumes electronics is the only possible domain; a non-electronics context
does not receive misleading Electronics safety semantics; Electronics behavior remains correct (anchored to existing safety
regressions).
**8B. D3-B RED —** demonstrate the current shared Path-N seam is incapable of honoring a non-electronics canonical domain
identity and/or serves the Electronics artifact regardless of that identity. GREEN: domain identity is consumed via the
canonical seam; shared selection no longer silently assumes Electronics; Electronics selection remains compatible; **no second
domain is activated to prove neutrality.**
**8D. D3-D RED —** demonstrate the current tie/priority behavior where a `RECOGNIZED_NOT_ACTIVATED` domain can outrank the
activated specialist domain. GREEN: canonical activation/support status respected; recognized-not-activated never becomes
activated routing/admission authority; remaining ranking metadata governed by an accepted existing owner; Electronics behavior
compatible.
**8-Mutation —** load-bearing mutation/adversarial probes MUST fail (turn a targeted test RED) when the corrected behavior is
deliberately broken — targeting bypass of activation-aware safety, bypass of domain-aware Path-N selection, and restoration of
the ungoverned tie-break — then be **restored byte-identically**. A test that still passes after the intended guard is deleted
is insufficient.

## 9. Regression requirements (implementation/review time)

Focused D3 tests; safety-signal tests; Path-N / progression-loop tests; `domain_rules` tests; Domain Registry tests; Activation
Policy tests; Electronics-domain regression tests; relevant **web admission regression tests even though web code is not
changed**; **full repository test suite**. Playwright/environment-dependent behavior reported **truthfully** — an environment
skip is NOT a functional PASS.

## 10. D3 implementation acceptance criteria (D3 may close only if ALL hold)

1. D3-A corrected (electronics-only assumption removed from the safety seam **without** removing legitimate Electronics safety
   content). 2. D3-B corrected (shared Path-N selection consumes canonical domain identity; no silent electronics assumption).
   3. D3-D corrected (recognized-not-activated cannot become effective activated routing/admission authority). 4. **D3-C
   unchanged.** 5. `domains/iot_electronics/**` untouched. 6. No domain activated. 7. `electronics_electrical` remains the only
   activated specialist domain (unless separately authorized later). 8. Domain Registry reused. 9. Activation policy reused.
   10. No duplicate canonical owner. 11. Genuine RED→GREEN for A/B/D. 12. Load-bearing mutation evidence (restored
   byte-identically). 13. Focused regressions green. 14. Full regression suite green. 15. Environment skips reported truthfully
   (skip ≠ PASS). 16. No persistence/schema/commercial/provider coupling introduced. 17. `git diff --check` clean. 18.
   Independent implementation review = ACCEPT. 19. Exact-candidate acceptance + SHA-preserving publication. 20. **CREATE A MERGE
   COMMIT.** 21. Post-merge verification proves exact candidate/tree preservation. 22. Remaining-obligation / exit-criteria
   review confirms no mandatory D3 obligation remains. 23. Separate formal D3 closure recorded and verified.

Only after ALL of the above may D3 become **FORMALLY CLOSED / AUTHORITATIVE.**

## 11. One-increment shape & rollback

**ONE BOUNDED D3 INCREMENT** (A/B/D share the same canonical-owner set, rollback boundary — three engine modules + tests, no
persistence/schema/web migration — test surface, and no risky migration). Do NOT decompose merely to create gates; if
implementation uncovers a genuine independent risk/rollback boundary, **STOP** and report **"D3 CONTRACT DECOMPOSITION
REQUIRED"** with exact evidence. Rollback: three core engine modules + focused tests; revert alters no stored user data or
commercial state.

## 12. Owner decisions & Phase-9 boundary

**Owner product/policy decisions required before D3 implementation: NONE** (scope boundable from accepted architecture).
**Explicit Owner authorization of the D3 implementation gate is still required after this contract is accepted/merged**
(execution-gate authorization ≠ a new product-policy decision). **D8 remains Owner-reserved/deferred.** D3 is a
PRE-PHASE-9 / PRE-SECOND-DOMAIN prerequisite: closing D3 does **NOT** activate Phase 9, select IoT, decide D8, or activate any
domain; any first domain activation requires its own Owner decision (where required) + activation contract + scope + questions +
evidence/risk model + tests + benchmarks + independent review + explicit activation authorization.

## 13. Boundary / status

**D3 is a CONTRACT CANDIDATE ONLY — it becomes the authoritative contract-of-record only if this exact accepted candidate is
merged (create-a-merge-commit) and post-merge verified.** D3 implementation NOT started / NOT authorized by this contract gate;
NO domain activated; NO provider; D8 OPEN / Owner-reserved (blocks IoT activation only, at its own boundary). **DOCUMENTED
NO-VALID-RED** for this contract gate; the future implementation gate MUST use genuine RED→GREEN. **Phase 8 — FORMALLY CLOSED /
AUTHORITATIVE. Phase 9 — NOT AUTHORIZED; IoT — NOT AUTHORIZED; Phase 10 — NOT AUTHORIZED; PSRR — NOT EXECUTED; OD-Q/`main`
reconciliation — separate pre-production gate; deployment / production — NOT AUTHORIZED.** Candidate only until independent
review → Owner exact-candidate acceptance → merge (create-a-merge-commit) → post-merge verification → a **separate**
Owner-authorized D3 implementation gate. Append-only; prior history not rewritten. This entry authorizes no push, PR, merge
beyond this candidate, D3 implementation start, domain activation, D8 decision, Phase-9 start, or deployment.
