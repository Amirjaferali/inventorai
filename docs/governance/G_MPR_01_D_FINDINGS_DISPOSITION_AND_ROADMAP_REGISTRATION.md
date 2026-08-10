# G-MPR-01-D — Findings Disposition & Roadmap Registration

**Status of THIS record:** governance/documentation-only **disposition candidate**, authoritative if/when
independently reviewed, Owner-accepted, and merged. It converts the accepted findings of **G-MPR-01 — Master
Phase & Roadmap Completeness Review** (read-only master audit, complete) into durable, authoritative governance
records so the findings cannot be forgotten. **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY GATE.**

**This gate registers future obligations only.** It is NOT a runtime/test/Domain-Pack/remediation implementation
gate. It starts no phase, activates no domain, selects no provider, and weakens no production block. It modifies
**governance documents only**; no `engine/**`, `web/**`, `tests/**`, `domains/**`, `schemas/**`, `prompts/**`,
`benchmark/**`, dependency, CI, migration, API, adapter, or deployment file is touched.

**Authoritative base:** `d37caef8cfc0e4c5e53275e6e126ec8247a26219` (PR #421; tree
`d1a8208bb3efe401d9a9797d8cafd1a64703c83c`), verified read-only before editing; boot OK; clean working tree.

**Phase-8 order preserved (binding):** P8-I1 → P8-I2 → **G-MPR-01 / disposition (this gate)** → P8-I3 → P8-I4 →
P8-CLOSE. No Phase-9 domain-neutrality implementation is inserted before P8-I3. P8-I3 is NOT started here.

---

## D-GMPR-01-D — Owner disposition decisions registered (durable)

The following are registered as durable Owner dispositions arising from the accepted G-MPR-01 findings. Each is a
**future obligation or governance-hygiene decision** — none authorizes implementation. They are cross-registered
in `OWNER_DECISION_REGISTER.md`.

### D1 — P8-I1 formal closure gap (finding F1) — RESOLVED (ADD dedicated record)
- **Decision:** ADD a dedicated formal closure record for P8-I1 (precedent-consistent), correcting the missing
  artifact only; do NOT reopen P8-I1 implementation; do NOT change runtime.
- **Executed by this gate:** `docs/governance/P8_I1_PLAN_ENTITLEMENT_FOUNDATION_FORMAL_CLOSURE_RECORD.md` created,
  distinguishing IMPLEMENTATION COMPLETION (historical, PR #418 `2bf389d`) from LATE FORMAL CLOSURE-RECORD
  REGISTRATION (this gate), from authoritative existing evidence, with an honest independent-review provenance
  note (no fabricated verdict letter). **P8-I1 — FORMALLY CLOSED** (increment closure only).

### D2 — P8-I3 lifecycle persistence architectural rule — REGISTERED (contract constraint only)
- **Decision (binding on the future P8-I3 contract):** P8-I3 subscription-lifecycle persistence MUST use a
  **bounded, additive, backward-compatible** strategy — additive lifecycle table(s) or another explicitly
  justified additive schema extension — **not** destructive or risky reshaping of existing P8-I1/P8-I2
  persistence.
- **Requirements:** preserve existing account identity; preserve entitlement data (P8-I1); preserve quota data
  (P8-I2); preserve existing durable records; migration/evolution MUST be idempotent; existing databases MUST
  remain readable; NO destructive migration; NO implicit data rewrite; **rollback/recovery reasoning MUST be part
  of the P8-I3 contract**. Note: no `ALTER TABLE` framework exists — P8-I3 must separately choose an additive
  lifecycle table or a designed idempotent evolution mechanism.
- **Scope:** roadmap/contract constraint only. This gate designs NO schema and starts NO implementation.

### D3 — Core Domain-Neutrality Prerequisite Gate (pre-Phase-9) — REGISTERED (mandatory future gate)
- **Decision:** ADD a mandatory future governance gate **before the first non-electronics Phase-9 domain
  activation**. Purpose: remove or govern the remaining electronics-specific core couplings that would make a
  second activated engineering domain unsafe or misleading.
- **The future gate MUST inspect and, when separately authorized, address (finding evidence from G-MPR-01):**
  1. `engine/safety_signal.py` — electronics-only `_MVP_DOMAIN`; electrical-only cue families;
     domain-label forcing (a non-electronics idea currently gets no safety signals or is mislabeled electronics).
  2. `engine/path_n_questions.py` — electronics-pinned non-specialist question artifact; domain-blind selection.
  3. Scattered web admission / electronics literals (`web/app.py`, `web/domain_label.py`) — consolidate toward the
     canonical activation policy where appropriate.
  4. Hard-coded domain priority / tie-break behavior (`engine/domain_rules.py`) — determine whether it should move
     to governed pack metadata before further domain expansion.
- **Timing:** MANDATORY BEFORE the first additional domain activation; **NOT** mandatory before P8-I3. NOT
  implemented now (this gate touches no runtime file). Aligns with OD-F ("no hard-coded core branching on domain
  names") and Phase-9 per-domain-activation governance.

### D4 — Cross-Domain / Multi-Disciplinary Engineering Integration — REGISTERED (future gate; NOT authorized)
- **Decision:** ADD a future governed capability/gate supporting one invention spanning multiple engineering
  domains while preserving domain-specific truth. Minimum future scope: multiple domain-relevant subsystems;
  domain-specific evaluation preservation; explicit cross-domain dependency representation; cross-domain
  conflicts; engineering trade-offs; propagation of shared constraints where justified; unified invention-level
  assessment; **no silent overwrite of one domain's technical truth by another**; canonical output representation
  of cross-domain findings.
- **Preserved distinction (binding):** **DOMAIN REFERENCE ≠ DOMAIN ACTIVATION ≠ CROSS-DOMAIN EVALUATION.**
- **Placement:** after sufficient Phase-9 domain-activation maturity (requires ≥2 mature/activated domains), or as
  an explicitly governed successor to the earlier skipped cross-domain expansion seam (§5-I4 was an evidence-gated
  SKIP). Do NOT force before P8-I3. Remains **future / NOT AUTHORIZED**.
- **Stale-pointer re-homing:** the runtime note `engine/deliverable_assembler.py` `"cross_capability_conflicts": []`
  / "deferred to Phase 6" points at a now-CLOSED phase. **Governance re-homes this obligation to D4 (this future
  cross-domain gate).** The actual in-code comment lives in a runtime file (`engine/**`) and is therefore **out of
  scope for this governance-only gate**; correcting the code comment is registered as a task for a future
  separately-authorized code-touching gate. The empty `cross_capability_conflicts` output and the null
  `journey_extension.multi_domain_signals` pack slots are the intended future seams.

### D5 — Deferred capability re-homing — REGISTERED (all remain NOT AUTHORIZED)
Durably re-homed so none can be forgotten. **None is authorized or implemented.** The four localization/language
concepts are kept **distinct** (do not collapse): **UI Language** (shipped, D-P6-18) ≠ **Input Language**
(exists) ≠ **Output Language** (deferred) ≠ **Question Translation Assistant** (deferred).

| # | Capability | Current status | Live future home registered here | Preserved prerequisites |
|---|---|---|---|---|
| 1 | **Question Translation Assistant (QTA)** | NOT AUTHORIZED / NOT STARTED | **ADD** a live tracker entry + explicit future gate (previously mention-only; no phase/CAP/OD home) | conceptually follows the D-P6-17 language model + D-P6-18 UI-language foundation (closed); distinct from Output Language |
| 2 | **Output Language implementation** | DEFERRED / NOT AUTHORIZED (D-P6-17 is the accepted decision, not the capability) | **ADD** an explicit future implementation increment/gate distinct from the D-P6-17 decision | defaults to UI Language; distinct from QTA and UI/Input Language |
| 3 | **Approximate Concept Visualization (ACV)** | NOT IMPLEMENTED / LEVEL-1 (OD-U / OD-T) | **MOVE** from its now-closed Phase-3/4/5 anchors to a live post-Phase-5 implementation workstream gate | UX → persistence → accounts/verified ownership → privacy/data lifecycle → later provider-integrated generation; MVP freeze carve-out preserved |
| 4 | **Direct PDF Output Download** | DEFERRED (OD-U; distinct from FDC-001 JSON export) | **MOVE** from its now-closed Phase-4 anchor to a live successor implementation gate | output-version model; secure storage; authorized download; retention; audit |
| 5 | **Email Delivery of Outputs** | DEFERRED (OD-U) | **MOVE** from its now-closed Phase-3/4/5 anchors to a live successor gate | accounts/verified email (P5 shipped only a dev EmailSender abstraction, not output delivery); persistent outputs; rate limiting; OBS-P5-2-01 precondition |

Rules honored: no implementation; no silent assignment to an already-closed phase; existing owner decisions and
prerequisite sequencing preserved; history not rewritten (re-home only).

### D6 — CAP register index range (finding F8) — RESOLVED (truthful alignment)
- **Decision:** the authoritative capability register `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` extends
  through **CAP-18**. Bring master-obligation/index references that say "CAP-01…CAP-14" into truthful alignment
  with the actual register range **CAP-01…CAP-18**. No capability is deleted, renumbered, or changed in substance.
- **Executed by this gate:** the Master Obligation Index reference in `CURRENT_PROJECT_STATE.md` (Layer 4) is
  corrected to "CAP-01…CAP-18". Historical closure records that enumerated "CAP-01…CAP-14" are preserved as
  history (append-only); this record is the current-truth pointer that CAP-15…CAP-18 are equally tracked.

### D7 — Real-vendor integration vs CAP-15 (finding F9) — CLARIFIED (distinct; not merged)
Four related-but-distinct provider concerns are kept separate to avoid duplicate tracking while preserving
different triggers and responsibilities:
- **A. Provider abstraction / replaceability architecture** — **CAP-15 (AI Provider Abstraction)**; recorded
  capability; RECORDED ≠ AUTHORIZED; prevents vendor/SDK coupling; separate future AI-platform gate.
- **B. Actual real-vendor integration activation** — Phase-7 §25 trigger-deferred obligation (trigger: a real
  external integration need; NO vendor selected; "Wokwi" NOT selected).
- **C. Async/webhook integration work** — Phase-7 §25 rows 32/34 (trigger: proven async need).
- **D. External export/integration adapters** — the P7-I3 canonical→adapter→vendor boundary (delivered as a
  local vendor-neutral reference adapter; real adapters are trigger-deferred).
These are **not** merged semantically. Payment-provider boundary (P8-I4) is a separate commercial provider concern.

### D8 — `iot_electronics` legacy disposition — REGISTERED (guarded; Owner decision reserved)
- **Registered evidence-backed current disposition (do NOT decide the semantic question now):**
  `domains/iot_electronics/**` and its benchmark schema/prompt (`schemas/iot_electronics_output.schema.json`,
  `prompts/iot_electronics_system_prompt.md`) are a **historical/legacy benchmark domain artifact**; **not valid
  under the current v1.0 Domain Pack schema** (`schema_version=None`); **intentionally skipped** by the current
  registry (`engine/domain_registry.py`); **not runtime-activated**; the benchmark-linked historical evidence
  remains important (the benchmark is the CLAUDE.md-designated Historical Truth Source).
- **Reserved as an OWNER DECISION before Phase-9 IoT activation (all three preserved as options):** whether
  `iot_electronics` is (a) **superseded** by active `electronics_electrical`, (b) a **future governed IoT domain
  seed** (per OD-G), or (c) **benchmark-only legacy**. Not decided here.
- **Explicit guard (binding):** **NO deletion, migration, schema-normalization, activation, or repurposing of
  `iot_electronics` (or its benchmark schema/prompt) without a separately authorized gate.** Left untouched by
  this gate.

### D9 — OD-Q / `main` reconciliation — REGISTERED (mandatory future gate before production)
- **Decision:** register the OD-Q `main` reconciliation as a **mandatory future gate before any real release /
  production deployment path**. Purpose: reconcile authoritative development history (`feature/atomic-json-session-persistence`)
  with `main`; establish a trustworthy release branch/lineage; preserve exact governance and merge provenance;
  avoid uncontrolled rebasing/squashing/history replacement; ensure release automation does not use stale `main`.
- **Timing:** MUST happen before real production release; does NOT block P8-I3; NOT executed now. No merge into
  `main`, no push to `main`, no release branch created by this gate.

### D10 — Governance hygiene (findings F10–F14/F16, C-1…C-7) — REGISTERED + scoped corrections
Only material governance-readability contradictions are corrected in-place; historical evidence is preserved
(append-only; explicit superseded/current-truth pointers). Not broadened into general cleanup.
- **Corrected in this candidate (scoped, current-truth):** (i) `ACTIVE_INCREMENT_CONTRACT.md` stale "Active
  contract" header still labeled "D-P6-18" → current-truth pointer added (its body already runs through P8-I2);
  (ii) `CURRENT_PROJECT_STATE.md` stale pinned "last independently verified tip" → updated to the authoritative
  tip; (iii) CAP range (D6).
- **Registered as known append-only staleness (preserved as history; current-truth is THIS record + the live
  roadmap/current-truth docs):** the §5 "CLOSED vs NOT-complete" and Phase-6 lane wordings already flagged as
  retained history; the stale P4-1a template tail in `ACTIVE_INCREMENT_CONTRACT.md`; the runtime "deferred to
  Phase 6" code comment (re-homed by D4; code correction deferred to a future authorized code gate). These do not
  materially block current governance readability once this pointer exists.

---

## Consistency checks (governance-only)

All new status statements agree across the changed documents:
- **P8-I1:** FORMALLY CLOSED (dedicated record; increment closure only). **P8-I2:** CLOSED / AUTHORITATIVE
  (unchanged). **G-MPR-01:** READ-ONLY MASTER REVIEW COMPLETE; findings now REGISTERED via this gate.
- **P8-I3 / P8-I4 / P8-CLOSE:** NOT STARTED. **Phase 8:** OPEN. **Phase 9 / Phase 10:** NOT AUTHORIZED.
  **PSRR execution:** NOT STARTED. **Production / public paid activation:** BLOCKED / NOT AUTHORIZED.
- No domain activation occurred; `iot_electronics` untouched and guarded; no runtime/test/Domain-Pack/schema/
  prompt/benchmark file changed; no bundle/evidence deleted.
- P8-I1 closure evidence is authoritative and not fabricated (the independent-review provenance limitation is
  disclosed, not concealed).

## Next-eligible action

With P8-I1 formally closed, the P8-I3 lifecycle-persistence rule (D2) registered, and the accepted G-MPR-01
findings durably registered (D1–D10), the three required P8-I3-entry governance changes are satisfied. **P8-I3 —
Subscription Lifecycle** becomes **ELIGIBLE FOR OWNER CONSIDERATION — NOT AUTHORIZED / NOT STARTED** (a separate
Owner-authorized P8-I3 bounded implementation-contract gate is required; eligibility is not authorization). The
pre-Phase-9 Domain-Neutrality Gate (D3) and the Cross-Domain gate (D4) remain future and are NOT prerequisites to
P8-I3. Production blocks are fully preserved.
