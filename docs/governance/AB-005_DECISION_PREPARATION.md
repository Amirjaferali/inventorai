# AB-005 DECISION PREPARATION
# Registry Loader — Strategic Impact and Decision Readiness

**Status:** AWAITING OWNER DECISION
**Depends on:** AB-005_EVIDENCE_REPORT.md (Architectural Blocker confirmed)
**Classification established:** Registry loader INACTIVE — domain pack architecture disconnected from runtime
**Prepared at:** HEAD `1402ed3`, 2026-05-31
**Author:** Incoming agent
**Instruction:** Decision readiness only. No implementation. No remediation. No architecture redesign.

---

## SECTION 1 — STRATEGIC IMPACT ASSESSMENT

AB-005 is not a localized code quality issue. It is a gap between the documented platform architecture and the actual runtime behavior. The domain pack system — the mechanism by which InventorAI is supposed to support multiple domains without engine modification — does not function at runtime.

The strategic impact operates at three levels:

**Level 1 — Current state (today).**
The platform operates correctly for the four hardcoded domains in `domain_rules.py`: electronics_electrical, mechanical, medical_device, software. Users in these domains are not affected. No current functionality is broken. AB-005 is not a current execution blocker for covered domains.

**Level 2 — Stage 3 domain expansion.**
Stage 3 is defined as domain expansion — adding new domain packs. The entire premise of Stage 3 is that domain packs can be created and activated without modifying engine code. AB-005 evidence establishes that this premise is currently false. A `domain.json` file alone activates nothing. Every new domain requires direct modification of `domain_rules.py`. Stage 3 as documented cannot proceed with architectural integrity while AB-005 is unresolved.

**Level 3 — Platform identity.**
The product vision positions InventorAI as a domain-agnostic progression platform. The domain pack architecture is the mechanism that gives this claim operational meaning. If domains can only be added by modifying hardcoded Python source files, the platform is not domain-agnostic — it is a hardcoded multi-domain system that happens to have an unused registry infrastructure. This has implications for commercial positioning, partner onboarding, and technical scalability claims.

---

## SECTION 2 — IMPACT ON STAGE 3 DOMAIN EXPANSION

### 2.1 What Stage 3 requires

Stage 3 requires activating domain packs — new domains added as configuration files, not as engine code changes. Per governance: "AB-005 must be resolved before domain expansion proceeds."

### 2.2 What Stage 3 would actually do under current architecture

Under the current architecture, adding a new domain for Stage 3 requires:

1. Creating `domains/<new_domain>/domain.json` — structural only, no runtime effect
2. Adding signal tokens to `domain_rules.py` hardcoded lists
3. Adding a scoring entry to `infer_domain()` in `domain_rules.py`
4. Adding a branching case to `get_active_rules()` in `domain_rules.py`
5. Adding question entries to `_DOMAIN_QUESTIONS` in `domain_rules.py`

Steps 2–5 all modify `domain_rules.py` source code. This is exactly what the domain pack architecture was designed to avoid.

### 2.3 Can Stage 3 legally and architecturally proceed while AB-005 is unresolved?

**Legally (per governance):** No. The governance documents (ARCHITECTURE-BLOCKER-DISPOSITION.md) classify AB-005 as HIGH severity and state: "No domain pack can be safely activated until [the blocker is resolved]."

**Architecturally:** Stage 3 can proceed in a limited form — adding domains by modifying `domain_rules.py` — but this would:
- Violate the domain-agnosticism invariant (same violation pattern as AB-001)
- Increase the technical debt that AB-005 resolution must eventually address
- Create a growing divergence between `domain.json` files (which would exist but be inert) and `domain_rules.py` (which would be the actual authority)

**Conclusion:** Stage 3 execution is blocked by AB-005. Planning is authorized. Execution requires AB-005 resolution or explicit owner authorization of a scoped exception with documented consequences.

### 2.4 Exact trigger condition for AB-005 mandatory remediation

AB-005 becomes a mandatory remediation item at the moment any of the following occur:

**Trigger T1:** Owner authorizes activation of the first new domain pack outside current coverage (electronics_electrical, mechanical, medical_device, software). This is the same trigger condition as AB-001 — they share a trigger.

**Trigger T2:** Stage 3 execution is authorized. Stage 3 cannot begin without resolving AB-005 without violating governance.

**Trigger T3:** A partner or commercial requirement necessitates adding a domain without modifying engine source code. At this point AB-005 is no longer a future risk — it is a present blocker.

---

## SECTION 3 — IMPACT ON SPECIFIC DOMAINS

### 3.1 Electronics (electronics_electrical)
**Current status: FULLY FUNCTIONAL**
Hardcoded in `domain_rules.py`. Signal lists, inference scoring, active rules, and question bank all present. `load_registry()` inactivity has no effect on this domain today.

### 3.2 IoT
**Current status: PARTIALLY FUNCTIONAL — HARDCODED**
IoT tokens appear in `ELECTRONICS_SIGNALS` (bluetooth, wifi, ble, mqtt, uart, i2c, spi). An IoT inventor is likely inferred as `electronics_electrical` domain. No dedicated IoT entry exists in `get_active_rules()` or `_DOMAIN_QUESTIONS`. IoT inventors receive electronics rules and questions — functionally approximate but not IoT-specific. Adding a proper IoT domain pack requires `domain_rules.py` modification.

### 3.3 PCB
**Current status: NOT COVERED AS DISTINCT DOMAIN**
PCB tokens may partially match `ELECTRONICS_SIGNALS`. No dedicated PCB domain entry in `domain_rules.py`. A PCB inventor would be inferred as `electronics_electrical` — approximate coverage only. Adding PCB as a distinct domain requires `domain_rules.py` modification.

### 3.4 Solar
**Current status: NOT COVERED — CLASSIFICATION RISK**
No solar tokens in `domain_rules.py` signal lists. `infer_domain()` would return None or default to the weakest match. A solar inventor receives no domain-specific rules or questions. Adding solar requires `domain_rules.py` modification.

### 3.5 Software
**Current status: FULLY FUNCTIONAL — HARDCODED**
Hardcoded in `domain_rules.py` with dedicated signal list, inference scoring, and question bank (though with MVP-scope note: "PHYSICAL_FEASIBILITY excluded"). Functional today. Expanding software sub-domains requires `domain_rules.py` modification.

### 3.6 Medical
**Current status: FUNCTIONAL — HARDCODED**
`MEDICAL_SIGNALS` present in `domain_rules.py`. `infer_domain()` gives medical_device highest tie-breaker priority. Question bank and active rules present. Functional today. Medical sub-specialties (diagnostics, pharma, clinical) require `domain_rules.py` modification.

### 3.7 Future domains (all uncovered domains)
**Current status: BLOCKED — require engine code modification**
Any domain not currently in `domain_rules.py` cannot be activated without modifying Python source. The domain pack architecture (`domain.json` + registry) provides no runtime pathway for activation. Every future domain is subject to the same modification requirement until AB-005 is resolved.

### Domain Impact Summary

| Domain | Today | AB-005 resolved | AB-005 unresolved at Stage 3 |
|--------|-------|-----------------|------------------------------|
| Electronics | Functional | Functional (registry-driven) | Functional (hardcoded) |
| IoT | Approximate | Dedicated pack possible | Requires domain_rules.py edit |
| PCB | Approximate | Dedicated pack possible | Requires domain_rules.py edit |
| Solar | Not covered | Pack-driven activation | Requires domain_rules.py edit |
| Software | Functional | Functional (registry-driven) | Functional (hardcoded) |
| Medical | Functional | Functional (registry-driven) | Requires domain_rules.py edit |
| Future | Blocked | Pack-driven activation | Requires domain_rules.py edit |

---

## SECTION 4 — RUNTIME AUTHORITY ANALYSIS

### 4.1 Current runtime authority

**`domain_rules.py` is the sole runtime authority for all domain behavior.**

It controls:
- Domain inference (`infer_domain()`) — determines which domain an inventor is in
- Active rules per domain (`get_active_rules()`) — determines what rules apply
- Domain questions (`get_domain_question()` via `_DOMAIN_QUESTIONS`) — determines what questions are asked
- Signal lists (`ELECTRONICS_SIGNALS`, etc.) — used by `infer_domain()` scoring

All of this is hardcoded Python. No external configuration file influences runtime behavior.

### 4.2 Intended runtime authority

Per the designed architecture:

**`domain.json` (per domain pack)** should be the authority for:
- Domain identity and metadata (`capability_id`, `display_name`, `version`)
- Domain signals and vocabulary
- Domain-specific rules and gap configurations
- Governance metadata (`governance.source`, `review_date`, `license`)

**`domain_registry.py`** should be the authority for:
- Loading and validating domain packs from disk
- Providing a queryable registry to the engine
- Enforcing schema compliance

**`domain_rules.py`** (in the intended architecture) should either:
- Be replaced by registry-driven lookups, or
- Serve only as a fallback for domains not in the registry

### 4.3 Consequences of the gap

| Consequence | Impact |
|-------------|--------|
| New domains require source code modification | Every domain addition is an engine change — violates domain-agnosticism |
| `domain.json` governance artifacts are inert | Files exist, pass tests, but have no runtime effect — governance evidence is misleading |
| Domain pack standard (Level 1 governance) governs documents that are currently non-functional | The DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md defines a system that does not yet operate at runtime |
| Stage 3 execution requires engine changes | Contradicts the stated architecture for Stage 3 |
| Domain addition is a high-risk operation | Modifying `domain_rules.py` directly touches a file that the invariant says should not contain domain-specific content (per AB-001) |

---

## SECTION 5 — TECHNICAL DEBT VS ARCHITECTURAL BLOCKER ANALYSIS

### 5.1 Technical debt characteristics
A shortcut that increases future cost but does not prevent current function. Deferred deliberately. Does not break existing behavior.

### 5.2 Architectural blocker characteristics
A missing structural connection that prevents a category of future work from being done correctly. Cannot be worked around without violating the stated architecture. Gets worse with scale.

### 5.3 Classification of AB-005

**AB-005 is an architectural blocker — more severe than technical debt.**

Evidence supporting this classification:

- The gap is not between "good" and "better" implementation — it is between a non-functional system and a functional one
- The domain pack architecture is the stated mechanism for Stage 3 — without it, Stage 3 cannot proceed as designed
- Every domain added while AB-005 is unresolved increases the divergence between `domain.json` (governance) and `domain_rules.py` (reality)
- The `domain_rules.py` docstring explicitly marks itself as MVP-scope and "lightweight electronics/electrical only" — confirming it was never intended as the permanent authority

**Comparison with AB-001:**

| Dimension | AB-001 | AB-005 |
|-----------|--------|--------|
| Nature | Data structure in wrong file | Missing runtime connection |
| Scope | Single list (`_SUBSTANCE_SIGNALS`) | Entire domain activation pathway |
| Current impact | Classification quality for uncovered domains | No new domain can be activated without engine changes |
| Stage 3 impact | Blocker at first new domain activation | Blocker at Stage 3 execution |
| Severity | Partial violation | Architectural blocker |
| Dependency | Independent | AB-001 resolution incomplete without AB-005 |

---

## SECTION 6 — RISK OF LEAVING AB-005 UNRESOLVED

### Risk 1 — Stage 3 cannot proceed as documented (FUTURE — imminent)
**Severity: High**
Stage 3 is the next authorized execution phase. Its entire premise depends on domain pack activation. AB-005 means Stage 3 execution requires engine source modification — contradicting the architectural design and governance authorization scope.

### Risk 2 — Governance documentation misleads future agents (PRESENT)
**Severity: Medium**
`DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md` (Level 1 authority) defines a domain pack system. `domain.json` files exist. Tests pass. A future agent reading these documents would reasonably conclude the domain pack system is operational. It is not. This creates a documentation-reality gap that could lead to incorrect architectural decisions.

### Risk 3 — Each domain added under current architecture increases remediation cost (FUTURE — cumulative)
**Severity: Medium-High**
Every domain added to `domain_rules.py` while AB-005 is unresolved adds another hardcoded entry that must eventually be migrated to the registry. The migration cost grows linearly with the number of domains added before AB-005 is resolved.

### Risk 4 — AB-001 remediation is incomplete without AB-005 (ARCHITECTURAL)
**Severity: High**
AB-001 resolution moves `_SUBSTANCE_SIGNALS` to the domain configuration layer. But if the domain configuration layer has no runtime connection to the engine (AB-005), then AB-001 remediation cannot be fully executed. The two blockers are coupled: resolving AB-001 alone creates a signal list in a location that has no runtime pathway to `assess_response()`.

### Risk 5 — Commercial and partner readiness claims are unsupported (FUTURE)
**Severity: Medium**
If InventorAI is presented to partners or commercial customers as a domain-extensible platform, the current state cannot support that claim. Domain extensibility requires AB-005 resolution.

---

## SECTION 7 — DEPENDENCIES BETWEEN AB-001 AND AB-005

These two blockers are architecturally coupled. Neither can be fully resolved independently.

### 7.1 AB-001 depends on AB-005

AB-001 resolution requires moving `_SUBSTANCE_SIGNALS` from `progression_loop.py` to the domain configuration layer. The intended destination for these signals is a domain pack structure — either `domain_rules.py` (stopgap) or `domain.json` (correct architecture).

If `_SUBSTANCE_SIGNALS` is moved to `domain_rules.py` without AB-005 being resolved: the signal lists are now in the right file conceptually, but still hardcoded Python with no registry pathway. This is an improvement but not a full resolution.

If `_SUBSTANCE_SIGNALS` is moved to the registry system (full resolution of AB-001): AB-005 must be resolved first, because the registry system must be operational before signal data can be stored and retrieved from it at runtime.

**Conclusion:** Full AB-001 resolution requires AB-005 to be resolved first, or simultaneously.

### 7.2 AB-005 resolution enables AB-001 resolution

Once `domain_registry.py` is connected to the runtime path, domain packs can carry their own signal lists. `_SUBSTANCE_SIGNALS` in `progression_loop.py` can be replaced by a registry lookup — resolving AB-001 cleanly and completely.

### 7.3 Recommended resolution order

Based on the dependency analysis:

```
AB-005 (activate registry) → AB-001 (move signals to registry) → Stage 3 (new domain packs)
```

This order is an interpretation — not an implementation proposal. The owner must authorize each step.

---

## SECTION 8 — MISSING EVIDENCE BEFORE REMEDIATION

The following evidence has not been collected and would be required before any remediation decision is authorized:

### Missing Evidence 1 — Full `domain.json` schema for `iot_electronics`
**What is needed:** Complete content of `domains/iot_electronics/domain.json` — all fields, their values, and their data types.
**Why needed:** To determine whether the schema already includes signal lists, rules, and question data — or only metadata. This determines how much of the domain configuration already exists in the correct format.

### Missing Evidence 2 — Full `domain_registry.py` content (lines 1–67)
**What is needed:** The complete file, particularly the schema validation logic and what fields are required/optional.
**Why needed:** To understand what the registry expects from a domain pack and whether `domain_rules.py` data structures are compatible with the registry schema.

### Missing Evidence 3 — What `domain_rules.py` `get_active_rules()` returns and how it is consumed
**What is needed:** Lines 39–70 of `domain_rules.py` (the full `get_active_rules()` implementation) and all callers of this function.
**Why needed:** If `get_active_rules()` is consumed by the engine, its interface must be preserved or replaced in any remediation. If it has no callers, it may be vestigial.

### Missing Evidence 4 — Whether any `domain.json` field maps to current `domain_rules.py` behavior
**What is needed:** Side-by-side comparison of `domain.json` schema fields vs `domain_rules.py` data structures.
**Why needed:** Remediation design depends on whether the schema is already aligned with the data or requires extension.

### Missing Evidence 5 — How `progression_loop.py` receives `state.domain` initially
**What is needed:** Where `state.domain` is set — specifically whether it comes from `infer_domain()` in `domain_rules.py` or from user input.
**Why needed:** If `infer_domain()` is the source of `state.domain`, then registry-driven domain inference must replace it. If domain is set by user input, the inference pathway is separate from the activation pathway.

---

## SECTION 9 — DECISION OPTIONS

### Option A — ACCEPT
**Description:** Accept the current architecture as-is. `domain_rules.py` remains the permanent runtime authority. `domain_registry.py` and `domain.json` are demoted to governance/metadata artifacts with no runtime role.

**Conditions where this is reasonable:**
- Domain expansion beyond the current four is permanently deprioritized
- The platform's multi-domain claim is scoped to the four hardcoded domains only
- Stage 3 is redefined to mean "modifying domain_rules.py" rather than "activating domain packs"

**Consequences:**
- Every new domain requires engine source modification
- Domain-agnosticism invariant is permanently weakened
- `domain_registry.py` and `domain.json` are governance theater — they exist but serve no runtime purpose
- Commercial domain-extensibility claims cannot be supported

**Verdict:** Viable only if the product vision is explicitly narrowed. Contradicts the current stated vision.

---

### Option B — DEFER
**Description:** Leave AB-005 unresolved. Document the trigger condition explicitly. Set a hard gate: AB-005 must be resolved before Stage 3 execution begins.

**Conditions where this is reasonable:**
- Stage 3 is not imminent
- Missing evidence (Section 8) needs collection
- Owner wants a remediation design before authorizing
- Current four-domain coverage is sufficient for immediate product needs

**Consequences:**
- No new domains can be activated without engine changes in the interim
- Documentation-reality gap persists
- AB-001 full resolution remains blocked
- Risk 3 (cumulative migration cost) is managed by not adding new domains

**Verdict:** Reasonable as a holding position. Requires explicit trigger conditions and must not allow Stage 3 execution to begin without resolution.

---

### Option C — REMEDIATE
**Description:** Connect `domain_registry.py` to the runtime path. `domain_rules.py` either delegates to the registry or is replaced by registry-driven lookups.

**Conditions where this is reasonable:**
- Missing evidence (Section 8) has been collected
- Owner has approved a remediation design
- Benchmark (WPS001) passes before and after
- AB-001 remediation is sequenced to follow

**Consequences:**
- Domain pack architecture becomes operational
- New domains can be activated via `domain.json` without engine changes
- AB-001 can be fully resolved (signals move to registry)
- Stage 3 can proceed as designed
- Existing four domains must be migrated to registry format — migration risk

**Verdict:** Correct long-term path. Requires missing evidence, design approval, and sequenced execution with AB-001.

---

### Option D — REPLACE ARCHITECTURE
**Description:** Discard `domain_registry.py` and `domain.json`. Redesign the domain activation mechanism from scratch — possibly using a different configuration format or runtime injection model.

**Conditions where this is reasonable:**
- The current `domain_registry.py` design is found to be inadequate after evidence review
- A significantly better architecture is identified
- Owner authorizes a full architectural redesign

**Consequences:**
- Highest cost and risk
- Existing domain pack governance standard (Level 1) would need revision
- Only justified if Option C evidence review reveals fundamental flaws in the current design

**Verdict:** Not justified by current evidence. Premature. Would require a separate architectural design process.

---

## DECISION SUMMARY TABLE

| Option | Domain pack functional? | Stage 3 unblocked? | AB-001 resolvable? | Effort | Risk |
|--------|------------------------|--------------------|--------------------|--------|------|
| A — Accept | No (permanently) | No (redefined) | Partial | None | High (long-term) |
| B — Defer | No (temporarily) | No (gated) | Partial | Low | Medium |
| C — Remediate | Yes | Yes | Yes (full) | Medium-High | Low (if evidence complete) |
| D — Replace | Depends | Depends | Depends | Very High | High |

---

## BLOCKER CLASSIFICATION SUMMARY

| Question | Answer |
|----------|--------|
| Is AB-005 a current execution blocker? | **No** — current four-domain operation is unaffected |
| Is AB-005 a Stage 3 blocker? | **Yes** — Stage 3 cannot proceed as designed without resolution |
| Is AB-005 a future scalability blocker? | **Yes** — every domain beyond the current four requires engine modification |
| Can Stage 3 legally proceed while AB-005 is unresolved? | **No** — governance prohibits it without explicit owner exception |
| What is the exact trigger condition? | First authorization of a new domain pack outside current coverage, OR Stage 3 execution authorization — whichever comes first |

---

*This document contains no implementation proposals.*
*No code changes are recommended or implied.*
*Decision authority rests with the owner.*
*Evidence sources: AB-005_EVIDENCE_REPORT.md, domain_registry.py, domain_rules.py, domain.json at HEAD 1402ed3.*
