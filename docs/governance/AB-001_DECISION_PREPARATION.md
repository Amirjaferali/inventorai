# AB-001 DECISION PREPARATION
# Domain-Agnosticism Violation — Strategic Impact and Decision Readiness

**Status:** AWAITING OWNER DECISION
**Depends on:** AB-001_EVIDENCE_REPORT.md (Partial Violation confirmed)
**File under investigation:** `engine/progression_loop.py` — `_SUBSTANCE_SIGNALS` (lines 146–171)
**Prepared at:** HEAD `01d353e`, 2026-05-31
**Author:** Incoming agent
**Instruction:** Decision readiness only. No implementation. No refactoring.

---

## SECTION 1 — STRATEGIC IMPACT ASSESSMENT

The violation is the presence of `_SUBSTANCE_SIGNALS` — a multi-domain keyword list — inside `progression_loop.py`. This list directly gates the `REASONED` classification in `assess_response()`, which in turn gates maturity advancement.

The strategic impact operates at three levels:

**Level 1 — Correctness today.**
The current list covers four domains: electronics, mechanical, software, medical. For inventors working in these domains, the classification behavior is functional. No inventor is being incorrectly blocked by a missing domain today — within the current domain scope.

**Level 2 — Scalability as domains expand.**
Every new domain that requires domain-specific substance signals must add tokens to `_SUBSTANCE_SIGNALS` inside `progression_loop.py`. This means every domain expansion requires modifying the core engine loop file — a file that is supposed to be domain-agnostic. This is the architectural cost of leaving the violation in place.

**Level 3 — Governance integrity.**
The architectural invariant states: "progression_loop.py must NEVER contain domain-specific branching." The violation is currently a data structure, not branching logic — but the effect is equivalent. An inventor in a domain not represented in `_SUBSTANCE_SIGNALS` will have their substantive responses mis-classified as `ASSERTED` because their vocabulary does not match the electronics/mechanical/software/medical token set. This is a silent accuracy failure, not a crash.

**Summary:** The violation does not break the engine today for covered domains. It creates a structural dependency that prevents true multi-domain scalability and produces silent classification errors for uncovered domains.

---

## SECTION 2 — IMPACT OF ADDING 5, 10, AND 20 FUTURE DOMAINS

### 2.1 Adding 5 domains (near-term expansion)

If 5 new domains are added (e.g., chemical engineering, aerospace, biotechnology, civil engineering, materials science), each requires domain-specific substance tokens. Under the current architecture:

- 5 new token groups must be appended to `_SUBSTANCE_SIGNALS` in `progression_loop.py`
- Each addition modifies the core engine loop
- Each modification requires benchmark validation
- The list grows to approximately 100–150 tokens
- Risk: token collision between domains (e.g., "pressure" is both mechanical and chemical engineering)
- Each new domain pack developer must understand `progression_loop.py` internals to add their tokens

Under a corrected architecture (signals in `domain_rules.py`):
- Each domain pack defines its own signal list
- `progression_loop.py` is not touched
- Token collision is managed per-domain, not globally

**Impact at 5 domains: Manageable but increasing friction.**

### 2.2 Adding 10 domains (medium-term expansion)

At 10 domains, `_SUBSTANCE_SIGNALS` would contain approximately 200–300 tokens across 10 labelled sections. Problems that become significant:

- **Token overlap:** Multiple domains share vocabulary (e.g., "sensor" appears in electronics, medical, and automotive). The flat list cannot distinguish which domain a token belongs to — it functions as a union across all domains simultaneously.
- **False positives:** An inventor describing a medical device using the word "sensor" gets credit for electronics substance signals — not their own domain's vocabulary.
- **False negatives:** An inventor in an uncovered domain (e.g., aquaculture, textile engineering) produces substantive responses that score `ASSERTED` because no tokens match.
- **Maintenance burden:** 10 domain teams all need to modify the same engine file.

**Impact at 10 domains: Classification accuracy degrades. Silent failures increase. Maintenance becomes a coordination problem.**

### 2.3 Adding 20 domains (platform-scale)

At 20 domains, the flat `_SUBSTANCE_SIGNALS` list approach becomes architecturally untenable:

- 400–600 tokens in a single list with no domain context
- The list cannot serve domain-specific scoring — it serves only a union presence check
- An inventor in domain A gets credit for tokens from domain B, C, or D
- The engine cannot be said to evaluate reasoning quality — it evaluates vocabulary breadth across all registered domains simultaneously
- The REASONED/ASSERTED gate loses meaning as a domain-specific quality signal

**Impact at 20 domains: The classification mechanism breaks down as a meaningful quality gate. The architectural violation becomes a product accuracy problem.**

---

## SECTION 3 — WHETHER THE VIOLATION BLOCKS SPECIFIC DOMAINS

### 3.1 Electronics
**Status: NOT BLOCKED**
Electronics tokens are the most extensively covered in `_SUBSTANCE_SIGNALS` (two subsections: components/devices and actions/signals and principles). An electronics inventor using standard vocabulary will be correctly classified.

### 3.2 IoT
**Status: PARTIALLY COVERED — RISK OF GAP**
IoT vocabulary overlaps significantly with electronics (`mqtt`, `uart`, `i2c`, `spi`, `bluetooth`, `wifi`, `ble` are present). However, IoT-specific concepts (edge computing, cloud connectivity, LPWAN, LoRa, Zigbee, device provisioning) are absent. An IoT inventor using non-electronics vocabulary faces classification risk.

### 3.3 PCB (Printed Circuit Board design)
**Status: PARTIALLY COVERED — GAP EXISTS**
Some PCB vocabulary is present via electronics tokens (`resistor`, `capacitor`, `transistor`, `ic`). PCB-specific concepts (trace routing, impedance matching, ground plane, via, differential pair, EMI, ESD) are absent. A PCB designer describing their innovation in PCB-specific terms faces classification risk.

### 3.4 Solar
**Status: NOT COVERED — HIGH RISK OF MISCLASSIFICATION**
No solar-specific tokens are present in `_SUBSTANCE_SIGNALS`. Vocabulary such as photovoltaic, inverter, MPPT, irradiance, bypass diode, monocrystalline, panel efficiency, charge controller is absent. A solar inventor whose response uses domain-specific vocabulary without overlapping electronics terms is at high risk of `ASSERTED` misclassification. Direct runtime validation has not yet been performed to confirm this behavior.

### 3.5 Software
**Status: COVERED**
Software tokens are present (`algorithm`, `parser`, `database`, `api`, `cache`, `latency`, `encryption`, `runtime`, `static analysis`). Coverage is reasonable for general software concepts. Specialized software subdomains (e.g., compiler design, distributed systems, ML infrastructure) have partial gaps.

### 3.6 Medical
**Status: COVERED WITH GAPS**
Medical tokens are present (`electrode`, `biosensor`, `optical`, `tissue`, `glucose`, `implant`, `catheter`, `biomarker`, `wearable`, `pulse`). Coverage is skewed toward medical devices (implantables, biosensors). Medical software, clinical workflow, diagnostics, and pharmaceutical domains are not represented.

### Domain Coverage Summary

| Domain | Status | Risk |
|--------|--------|------|
| Electronics | Covered | Low |
| IoT | Partial | Medium |
| PCB | Partial | Medium |
| Solar | Not covered | **High — silent failure today** |
| Software | Covered | Low–Medium |
| Medical | Partial | Medium |

---

## SECTION 4 — TECHNICAL DEBT VS ARCHITECTURAL BLOCKER ANALYSIS

### 4.1 Technical Debt Characteristics
Technical debt is an implementation shortcut that increases future cost but does not prevent current function. Characteristics:
- Known, documented
- Deferred deliberately or by oversight
- Does not break current functionality
- Can be paid down incrementally

### 4.2 Architectural Blocker Characteristics
An architectural blocker prevents a category of future work from being done correctly. Characteristics:
- Structural, not just implementation-level
- Cannot be worked around without touching the violated invariant
- Gets worse with scale
- Remediation requires architectural decision, not just code cleanup

### 4.3 Classification of AB-001

AB-001 exhibits characteristics of **both**:

**As technical debt:**
- Current domain coverage is functional for 4 covered domains
- The violation does not crash the engine
- It can be deferred without immediate failure

**As architectural blocker:**
- Every new domain requires modifying `progression_loop.py` — a file the invariant prohibits from containing domain-specific content
- AB-005 (registry loader inactive) cannot be fully resolved while `_SUBSTANCE_SIGNALS` remains in `progression_loop.py` — a domain pack that defines its own signal vocabulary has no pathway to inject it into `assess_response()` under the current structure
- The violation prevents Stage 3 (domain expansion) from being executed with full architectural integrity

**Conclusion:** AB-001 is **technical debt today** that becomes an **architectural blocker at Stage 3**. The transition point is the moment the first new domain pack is activated.

---

## SECTION 5 — RISK OF LEAVING THE VIOLATION UNCHANGED

### Risk 1 — Silent classification failures for uncovered domains (PRESENT)
**Severity: High**
Solar domain inventors and others in uncovered domains may be misclassified today based on current evidence. Their substantive, reasoned responses risk being rated `ASSERTED` because their vocabulary does not appear in `_SUBSTANCE_SIGNALS`. Direct runtime validation has not yet been performed to confirm this behavior. This risk is not visible in existing tests because no test cases cover solar or other uncovered domains.

### Risk 2 — Stage 3 domain expansion requires engine modification (FUTURE — near-term)
**Severity: High**
Every domain pack added in Stage 3 that requires substance signal coverage must modify `progression_loop.py`. This violates the invariant on every addition. Stage 3 cannot be completed with architectural integrity while the violation exists.

### Risk 3 — AB-005 resolution is incomplete without AB-001 (FUTURE)
**Severity: Medium-High**
AB-005 is the inactive registry loader — domain packs cannot be activated. Even after AB-005 is resolved, a domain pack cannot fully control its own classification behavior because `_SUBSTANCE_SIGNALS` is hardcoded in the engine loop. AB-001 and AB-005 are coupled blockers.

### Risk 4 — Token collision degrades classification quality at scale (FUTURE — medium-term)
**Severity: Medium**
As more domains are added to `_SUBSTANCE_SIGNALS`, vocabulary overlap between domains causes false-positive `REASONED` classifications. An inventor in any domain can trigger substance signals from another domain's vocabulary. Classification becomes less meaningful as a domain-specific quality gate.

### Risk 5 — Governance documentation drift (PRESENT — minor)
**Severity: Low**
The module docstring claims "electronics/electrical only" scope. This is already false. Future agents reading the docstring will have an incorrect model of the file's scope.

---

## SECTION 6 — EVIDENCE STILL MISSING BEFORE REMEDIATION

The following evidence has not been collected and would be required before any remediation decision is authorized:

### Missing Evidence 1 — `domain_rules.py` structure
**What is needed:** Full content of `engine/domain_rules.py` — specifically whether it has a function signature capable of receiving or returning substance signal lists, and whether its current structure supports per-domain signal injection.
**Why needed:** Remediation design depends on what `domain_rules.py` already provides. A new function may need to be defined, or an existing one extended.

### Missing Evidence 2 — `assess_response()` full logic (lines 200–260)
**What is needed:** Complete view of the classification decision tree in `assess_response()` — specifically how `has_substance` interacts with `_has_causal_structure()` and the `MIN_REASONED_RESPONSE_LENGTH` guard.
**Why needed:** Removing `_SUBSTANCE_SIGNALS` from the function requires understanding which paths would be affected and whether path B (`causal structure + no verb trap`) is sufficient as a fallback.

### Missing Evidence 3 — Test coverage of `assess_response()`
**What is needed:** Review of `test_assess_response_adversarial.py` and `test_assess_response_replay.py` to identify which tests depend on `_SUBSTANCE_SIGNALS` tokens directly.
**Why needed:** Any remediation must not break existing tests. Understanding which tests are signal-dependent determines the remediation complexity.

### Missing Evidence 4 — `domain_rules.py` existing domain definitions
**What is needed:** What domains are currently defined in `domain_rules.py` and what structure they use.
**Why needed:** If domain packs in `domain_rules.py` already have a vocabulary/signals section, `_SUBSTANCE_SIGNALS` migration has a natural destination. If not, a new structure must be designed.

### Missing Evidence 5 — git history of `_SUBSTANCE_SIGNALS` evolution
**What is needed:** `git log -p engine/progression_loop.py | grep -A5 -B5 "_SUBSTANCE_SIGNALS"` to identify when each domain section was added.
**Why needed:** Understanding whether the expansion was deliberate or incremental informs the decision classification (was this a known trade-off or an oversight?).

---

## SECTION 7 — DECISION OPTIONS

### Option A — ACCEPT
**Description:** Acknowledge the violation, document it as a known exception to the domain-agnosticism invariant, and continue domain expansion by adding tokens to `_SUBSTANCE_SIGNALS`.

**Conditions where this is reasonable:**
- Domain expansion is limited to ≤5 domains total
- Token collision is acceptable at that scale
- Stage 3 scope is narrow and well-defined

**Consequences:**
- Invariant is permanently weakened — "domain-specific content in progression_loop.py is prohibited, except for _SUBSTANCE_SIGNALS"
- Each new domain modifies the engine loop
- Solar and other uncovered domains remain silently broken
- AB-005 resolution remains incomplete

**Verdict on this option:** Creates a precedent that exceptions to the invariant are acceptable. Not recommended unless Stage 3 scope is permanently limited.

---

### Option B — DEFER
**Description:** Leave `_SUBSTANCE_SIGNALS` in place for now. Document the violation formally. Set a condition: must be resolved before the Nth domain pack is activated (e.g., before the 3rd domain pack).

**Conditions where this is reasonable:**
- Stage 3 is not imminent
- Missing evidence (Section 6) needs to be collected first
- Owner wants a remediation design proposal before authorizing

**Consequences:**
- Solar domain remains silently broken in the interim
- AB-005 resolution is possible but incomplete
- Deferred work is formally tracked — not forgotten

**Verdict on this option:** Reasonable as a short-term position while missing evidence is collected and remediation is designed. Requires a clear trigger condition for activation.

---

### Option C — REMEDIATE
**Description:** Move `_SUBSTANCE_SIGNALS` out of `progression_loop.py` and into the domain configuration layer. `assess_response()` would receive signal lists from `domain_rules.py` via a new or extended function interface.

**Conditions where this is reasonable:**
- Missing evidence (Section 6) has been collected
- `domain_rules.py` structure is understood
- Test impact is mapped
- Owner has approved the remediation design
- Benchmark (WPS001) passes before and after

**Consequences:**
- Invariant fully restored
- Stage 3 can proceed with architectural integrity
- AB-005 resolution becomes fully effective
- Solar and uncovered domains can be correctly classified
- Existing tests must be verified against new structure

**Verdict on this option:** Correct long-term path. Requires missing evidence and owner approval before execution.

---

### Option D — REPLACE ARCHITECTURE
**Description:** Replace the token-matching approach in `assess_response()` entirely with a domain-configurable scoring mechanism — e.g., each domain pack defines a scoring function, and `assess_response()` delegates to it.

**Conditions where this is reasonable:**
- Token matching is deemed insufficient as a quality gate at scale
- A more sophisticated classification mechanism is desired
- Owner authorizes a significant engine refactor

**Consequences:**
- Highest remediation cost
- Highest long-term flexibility
- Requires full benchmark validation
- Would resolve AB-001 and enable future quality gate improvements
- Not justified by current evidence alone — requires separate architectural proposal

**Verdict on this option:** Not justified by current evidence. Premature at this stage. Would require a separate architectural design process.

---

## DECISION SUMMARY TABLE

| Option | Invariant restored? | Stage 3 unblocked? | Solar fixed? | Effort | Risk |
|--------|--------------------|--------------------|--------------|--------|------|
| A — Accept | No | No | No | None | High (long-term) |
| B — Defer | No (temporary) | Partially | No | Low | Medium |
| C — Remediate | Yes | Yes | Yes | Medium | Low (if evidence complete) |
| D — Replace | Yes | Yes | Yes | High | Medium |

---

*This document contains no implementation proposals.*
*No code changes are recommended or implied.*
*Decision authority rests with the owner.*
*Evidence sources: AB-001_EVIDENCE_REPORT.md, progression_loop.py at HEAD 01d353e.*
