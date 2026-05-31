# AB-005 MISSING EVIDENCE SUPPLEMENT
# Completing the Evidence Record Required by STAGE3_READINESS_DECISION.md Section 8.4

**Status:** EVIDENCE COMPLETE — AWAITING OWNER REVIEW
**Depends on:** AB-005_EVIDENCE_REPORT.md, AB-005_DECISION_PREPARATION.md
**Evidence collected at:** HEAD `49b26e3`, 2026-05-31
**Author:** Incoming agent
**Instruction:** Evidence only. No remediation proposed.

---

## EVIDENCE ITEM 1 — Full domain.json schema for iot_electronics

**File:** `domains/iot_electronics/domain.json` (27 lines)

**Complete content:**
```json
{
  "taxonomy_group": "electronics",
  "capability_id": "iot_electronics",
  "display_name": "IoT Electronics",
  "description": "Internet of Things and embedded electronics domain.",
  "domain_signals": ["electronics_electrical", "iot", "embedded", "microcontroller", "sensor"],
  "gaps": ["MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"],
  "notes": "Hardcoded content in engine/domain_rules.py remains the active runtime source until Phase 5 Step 3 registry loader is implemented.",
  "governance": {"source": "InventorAI internal domain pack", "license": "proprietary", "owner": "inventorai-core-team", "review_date": "2025-01-01", "version": "1.0.0", "deprecation_status": "active"}
}
```

**Critical observation:** The `domain.json` notes field self-documents the AB-005 gap: hardcoded content in `domain_rules.py` is the active runtime source. AB-005 was a known planned gap, not an oversight.

**Schema gap finding:** `domain.json` does not contain question banks, signal token lists, or active rules content. It carries metadata and structural identifiers only.

---

## EVIDENCE ITEM 2 — Full domain_registry.py content

**File:** `engine/domain_registry.py` (96 lines)

**Required fields validated by `_validate_domain()`:**
Top-level: `capability_id`, `domain_signals`, `gaps`, `governance`
Governance sub-fields: `source`, `license`, `owner`, `review_date`, `version`, `deprecation_status`

**The registry validates structure and metadata only.** It does not validate question content, signal token lists, active rules, or lifecycle behavior.

**Schema compatibility finding:** `iot_electronics/domain.json` passes all `_validate_domain()` requirements. Registry infrastructure is schema-compatible with the existing domain pack.

**Three public functions — none called at runtime:**
| Function | Purpose |
|----------|---------|
| `load_registry(domains_dir)` | Loads all domain.json files from a directory |
| `get_domain(registry, capability_id)` | Returns full domain data by capability_id |
| `list_domains(registry)` | Returns sorted list of capability_ids |

---

## EVIDENCE ITEM 3 — get_active_rules() callers and full implementation

**Definition:** `engine/domain_rules.py:39`

**Full implementation (lines 39-65):**
```python
def get_active_rules(domain: str) -> list:
    if domain == "electronics_electrical":
        return ["MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"]
    if domain == "medical_device":
        return ["MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"]
    if domain == "software":
        return ["MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY"]
    return []
```

**Callers found:** `grep -rn "get_active_rules" engine/ web/` — **NO CALLERS FOUND in production code.**

**Finding:** `get_active_rules()` is unused at runtime. `mechanical` domain is absent — a mechanical inventor receives `[]`.

---

## EVIDENCE ITEM 4 — infer_domain() call chain

**Definition:** `engine/domain_rules.py:21`

**Call chain:**
```
web/app.py:8   → from engine.domain_rules import infer_domain
web/app.py:26  → domain = infer_domain(idea_text)
web/app.py:27  → if not domain: return error "Domain not recognized..."
web/app.py:28  → state = IdeaState(...)
web/app.py:29  → state.domain = domain
```

**Critical findings:**
1. `infer_domain()` is the **sole mechanism for domain assignment** at runtime — no user selection.
2. Uses **hardcoded scoring** against `ELECTRONICS_SIGNALS`, `MECHANICAL_SIGNALS`, `MEDICAL_SIGNALS`, `SOFTWARE_SIGNALS`.
3. Error message names only four domains: "electronics, mechanical, medical, or software."
4. Returns `None` for solar — inventor receives "Domain not recognized."
5. Registry plays **no role** in domain assignment even if `load_registry()` were called.

**Implication:** AB-005 resolution must address `infer_domain()` pathway, not only `load_registry()` activation.

---

## EVIDENCE ITEM 5 — Side-by-side schema comparison

| Capability | domain.json field | domain_rules.py equivalent | Match? |
|------------|------------------|---------------------------|--------|
| Domain identity | `capability_id` | Domain string in `if domain ==` branching | Partial |
| Display name | `display_name` | Not present | **Gap** |
| Description | `description` | Not present | **Gap** |
| Domain signals | `domain_signals` (5 category labels) | `ELECTRONICS_SIGNALS` (~20 vocabulary tokens) | **Mismatch** |
| Gap types | `gaps` (3 gap types) | `get_active_rules()` per domain | Partial match |
| Question banks | **Not in domain.json** | `_DOMAIN_QUESTIONS` in domain_rules.py | **Absent** |
| Substance signals | **Not in domain.json** | `_SUBSTANCE_SIGNALS` in progression_loop.py | **Absent** |
| Active rules nuance | **Not in domain.json** | software excludes PHYSICAL_FEASIBILITY | **Absent** |

---

## SUMMARY — MISSING EVIDENCE NOW COMPLETE

| Evidence Item | Status | Key Finding |
|---------------|--------|-------------|
| 1. Full domain.json schema | Complete | Metadata only — no questions, signals, or rules |
| 2. Full domain_registry.py | Complete | No runtime callers. Schema-compatible with iot_electronics. |
| 3. get_active_rules() callers | Complete | **No production callers.** Unused at runtime. |
| 4. infer_domain() call chain | Complete | Sole domain assignment. Hardcoded. Registry not consulted. |
| 5. Schema comparison | Complete | Three structural gaps: question banks, substance signals, rule nuance |

---

## ADDITIONAL FINDING — AB-005 SCOPE IS LARGER THAN PREVIOUSLY DOCUMENTED

**AB-005 full scope (evidence-based):**
1. `load_registry()` is not called at runtime — confirmed previously
2. `infer_domain()` uses hardcoded signal lists — does not consult registry — new finding
3. `get_active_rules()` has no production callers — designed but disconnected — new finding
4. `domain.json` schema missing question banks, substance signals, rule nuance — new finding
5. Remediation is 4-5 integration steps, not a single function call activation

**Implication:** AB-005_DECISION_PREPARATION.md Option C (Remediate) estimated "medium-high effort" — this supplement confirms that estimate is accurate.

---

*Evidence source: terminal output from cat, grep, and sed commands at HEAD 49b26e3.*
*No engine code was modified to produce this document.*
*No remediation proposed. Evidence collection only.*
