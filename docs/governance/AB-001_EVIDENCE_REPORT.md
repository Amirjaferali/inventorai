# AB-001 EVIDENCE REPORT
# Domain-Agnosticism Violation Investigation — progression_loop.py

**Status:** EVIDENCE COLLECTION COMPLETE — AWAITING OWNER REVIEW
**Blocker Severity:** HIGH (per ARCHITECTURE-BLOCKER-DISPOSITION.md)
**File under investigation:** `engine/progression_loop.py`
**Evidence collected at:** HEAD `01d353e`, 2026-05-31
**Author:** Incoming agent
**Instruction:** Classification only. No remediation proposed.

---

## SECTION 1 — EXACT LOCATIONS OF DOMAIN-SPECIFIC BEHAVIOR

### Location 1A — Module docstring (lines 1–17)
```
Line 3: Scope: electronics/electrical, LEVEL 0-2 only.
Line 14: - Domain rule enforcement (domain_rules.py)
```
The module docstring explicitly states its scope is `electronics/electrical`. This is a documentation-level domain reference embedded in the core engine loop file.

### Location 1B — `_SUBSTANCE_SIGNALS` list (lines 146–171)
```python
_SUBSTANCE_SIGNALS = [
    # components/devices (electronics)
    "sensor", "microcontroller", "arduino", "esp", "raspberry",
    "motor", "pump", "relay", "led", "display", "battery",
    "chip", "ic", "resistor", "capacitor", "transistor",
    "bluetooth", "wifi", "ble", "mqtt", "uart", "i2c", "spi",
    # actions/signals (electronics)
    "reads", "sends", "detects", "measures", "activates",
    "triggers", "converts", "transmits", "receives", "processes",
    "samples", "outputs", "controls", "monitors", "calculates",
    # principles (electronics)
    "voltage", "current", "frequency", "analog", "digital",
    "signal", "threshold", "filter", "protocol", "data",
    "piezoelectric", "hall", "infrared", "ultrasonic", "capacitive",
    # mechanical domain
    "piston", "spring", "valve", "gear", "lever", "hydraulic",
    "pneumatic", "pressure", "torque", "compression", "seal",
    "bearing", "actuator", "mechanism", "force", "friction", "bar",
    # software domain
    "algorithm", "parser", "parses", "tokenize", "tokenizes", "token",
    "ast", "function", "database", "api", "cache", "latency",
    "encryption", "runtime", "static analysis",
    # medical domain
    "electrode", "biosensor", "optical", "tissue", "glucose",
    "implant", "catheter", "biomarker", "wearable", "pulse",
]
```
This list is defined directly inside `progression_loop.py` and is organised into domain-labelled sections: electronics, mechanical, software, medical. Four distinct domains are explicitly named in comments.

### Location 1C — `assess_response()` uses `_SUBSTANCE_SIGNALS` (lines 207–233)
```python
Line 207: if r_lower in _WEAK_PATTERNS:
Line 212: substance_tokens = set(_SUBSTANCE_SIGNALS)
Line 215: has_substance = any(sig in r_lower for sig in _SUBSTANCE_SIGNALS)
Line 225: # REASONED path A: substance domain token + causal structure + length
Line 226: # REASONED path B: causal structure + no trap + length (for non-electronics domains)
Line 230: # 4. Length fallback for borderline answers without clear substance signals
Line 233: # No substance signals detected — treat as ASSERTED regardless of length
```
The `assess_response()` function — a core engine classification function — depends directly on `_SUBSTANCE_SIGNALS` to determine whether a response is classified `REASONED` or `ASSERTED`. The comment on line 226 explicitly distinguishes between electronics and non-electronics domains in the classification path.

### Location 1D — `get_question()` function (lines 118–127)
```python
Line 118: def get_question(domain: str, gap_type: str, iterations_open: int) -> str:
Line 121: # Asks domain layer first; falls back to generic questions.
Line 122: # Framework-level delegation — no domain-specific logic here.
Line 124: from engine.domain_rules import get_domain_question
Line 125: domain_q = get_domain_question(domain, gap_type, iterations_open)
Line 126: if domain_q:
Line 127:     return domain_q
```
This function delegates to `domain_rules.py` and explicitly states "no domain-specific logic here." The delegation pattern is correct per the invariant. However, it lives inside `progression_loop.py` alongside Location 1B/1C.

### Location 1E — `state.domain` references in run_iteration (lines 416, 422–423, 452, 458–459, 481, 488–489)
```python
Line 416:   "domain": state.domain,
Line 422:   next_q = get_ai_question(state.domain, next_gap_opened, _ai_ctx)
Line 423:       or get_question(state.domain, next_gap_opened, iterations_open)
Line 452:   "domain": state.domain,
Line 458:   question = get_ai_question(state.domain, gap_type, _ai_context)
Line 459:       or get_question(state.domain, gap_type, iterations_open)
Line 481:   "domain": state.domain,
Line 488:   get_ai_question(state.domain, next_gap_opened, ai_ctx)
Line 489:       or get_question(state.domain, next_gap_opened, iterations_open)
```
`state.domain` is passed as a parameter to both `get_question()` and `get_ai_question()`. These are delegation calls — the domain value is passed through, not interpreted inside `progression_loop.py` itself. No branching on the domain value occurs at these call sites.

---

## SECTION 2 — IMPORTED DEPENDENCIES CONTRIBUTING TO DOMAIN-SPECIFIC DECISIONS

### Import 1 — `engine.idea_state` (line 19, repeated at lines 72, 395, 403)
```python
from engine.idea_state import (
    IdeaState, Evidence, Gap, IterationLog,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS,
    OPEN, PARTIAL, CLOSED, ACCEPTED_RISK,
    ASSERTED, REASONED, DEMONSTRATED,
    PROGRESSING, STALLED, REGRESSING
)
```
These are gap-type constants and state enums. They are domain-agnostic labels. No domain-specific values imported here.

### Import 2 — `engine.domain_rules` (line 124, inside `get_question()`)
```python
from engine.domain_rules import get_domain_question
```
This import is inside the function body of `get_question()`. It is a lazy import — only executed when `get_question()` is called. The function delegates to `domain_rules.py` and returns the result without inspecting it. This is the intended separation pattern.

### Import 3 — `engine.ai_advisor` (lines 414, 450, 479)
```python
from engine.ai_advisor import get_ai_question
```
These are also lazy imports inside conditional blocks. `get_ai_question` receives `state.domain` as a parameter but the domain value is not interpreted by `progression_loop.py` — it is passed through to `ai_advisor`.

### Import 4 — `_SUBSTANCE_SIGNALS` itself (no import — defined inline)
`_SUBSTANCE_SIGNALS` is not imported from `domain_rules.py`. It is defined directly in `progression_loop.py` at line 146. This is the primary structural issue identified.

---

## SECTION 3 — DATA FLOW

### 3.1 Input
- `state: IdeaState` — contains `state.domain` (string), `state.idea_summary`, `state.maturity_level`, `state.gaps`, `state.iteration`
- `response: str` — the inventor's text response
- `ai_advisor_enabled: bool` — flag controlling AI layer

### 3.2 Classification (assess_response)
1. `response` is lowercased → `r_lower`
2. `r_lower` checked against `_WEAK_PATTERNS` (domain-agnostic rejection list) — if match → `ASSERTED`
3. `_SUBSTANCE_SIGNALS` tokens extracted — checked against `r_lower` → `has_substance` boolean
4. `_has_causal_structure(r_lower)` — checks `_CAUSAL_STRUCTURE_PATTERNS` (domain-agnostic phrases like "when", "causes", "leads to")
5. `_is_generic_verb_trap(r_lower)` — checks `_GENERIC_CAUSAL_VERBS` (domain-agnostic)
6. Classification decision tree:
   - Weak pattern → `ASSERTED`
   - Substance token + causal structure + length ≥ 40 → `REASONED`
   - Causal structure + no verb trap + length ≥ 40 → `REASONED` (comment: "for non-electronics domains")
   - Length fallback → borderline path
   - No substance signals → `ASSERTED`

**The domain-specific content enters at step 3** via `_SUBSTANCE_SIGNALS`.

### 3.3 Gap Detection
- `integrate_response()` uses the classification result from `assess_response()`
- Gap status updated based on `REASONED` vs `ASSERTED` classification
- No domain branching inside gap detection logic itself

### 3.4 Progression Evaluation
- `evaluate_transition()` checks `maturity_level`, gap closure status, mechanism classification
- No domain-specific branching observed in transition logic
- `state.domain` passed to `get_question()` which delegates to `domain_rules.py`

### 3.5 Maturity Transitions
- Transition from Level 0→1 and Level 1→2 governed by gap closure and mechanism classification
- Mechanism classification (`REASONED` / `ASSERTED`) is the gate
- The `REASONED` classification is produced by `assess_response()` which uses `_SUBSTANCE_SIGNALS`
- Therefore: domain-specific token lists in `_SUBSTANCE_SIGNALS` indirectly influence maturity transitions

---

## SECTION 4 — LOCATION-BY-LOCATION CLASSIFICATION

### Location 1A — Module docstring scope claim (line 3)
| Field | Value |
|-------|-------|
| Code reference | `Line 3: Scope: electronics/electrical, LEVEL 0-2 only.` |
| Purpose | Documents the original design scope of the module |
| What breaks if removed | Nothing at runtime — it is a comment |
| Classification | **domain-specific** — names a specific domain in the engine core docstring |
| Notes | The comment is outdated: `_SUBSTANCE_SIGNALS` already contains mechanical, software, and medical tokens, contradicting the "electronics/electrical only" scope claim |

### Location 1B — `_SUBSTANCE_SIGNALS` list (lines 146–171)
| Field | Value |
|-------|-------|
| Code reference | `_SUBSTANCE_SIGNALS = [...]` with domain comments: electronics, mechanical, software, medical |
| Purpose | Provides a keyword list used to determine whether a response demonstrates domain knowledge |
| What breaks if removed | `assess_response()` cannot determine `has_substance`. All responses without causal structure alone would fall to `ASSERTED`. `REASONED` classification rate would drop significantly. |
| Classification | **domain-specific** — contains tokens explicitly labelled by domain name; extends across 4 named domains |
| Notes | The existence of this list in `progression_loop.py` is the core of AB-001. The invariant states domain-specific behavior belongs in `domain_rules.py` only. |

### Location 1C — `assess_response()` usage of `_SUBSTANCE_SIGNALS` (lines 207–233)
| Field | Value |
|-------|-------|
| Code reference | `has_substance = any(sig in r_lower for sig in _SUBSTANCE_SIGNALS)` |
| Purpose | Gates REASONED classification on presence of domain substance tokens |
| What breaks if removed | `REASONED` path A becomes unreachable without substance signal. Classification falls to path B (causal structure only) or `ASSERTED`. |
| Classification | **domain-specific** — depends directly on `_SUBSTANCE_SIGNALS` which contains domain-labelled tokens |
| Notes | The comment on line 226 `(for non-electronics domains)` confirms the author was aware of domain-specific implications |

### Location 1D — `get_question()` delegation (lines 118–127)
| Field | Value |
|-------|-------|
| Code reference | `from engine.domain_rules import get_domain_question` |
| Purpose | Delegates question generation to `domain_rules.py` |
| What breaks if removed | Question generation falls to generic fallback. Domain-specific questions are lost. |
| Classification | **engine-generic** — the delegation pattern is correct. The function passes domain as a parameter without interpreting it. |
| Notes | This is the intended pattern per the architectural invariant. Its presence in `progression_loop.py` is appropriate. |

### Location 1E — `state.domain` passthrough calls (lines 416–489)
| Field | Value |
|-------|-------|
| Code reference | `get_question(state.domain, ...)` and `get_ai_question(state.domain, ...)` |
| Purpose | Passes domain context to question generation layers |
| What breaks if removed | Domain-specific questions cannot be generated |
| Classification | **engine-generic** — `state.domain` is passed through, not branched on. No `if domain == "electronics"` logic present at these sites. |
| Notes | Passing domain as a parameter is not a violation. The violation would be interpreting the domain value inside `progression_loop.py`. |

---

## SECTION 5 — EVIDENCE / INTERPRETATION / ASSUMPTIONS

### 5.1 Evidence (directly observed in code)

1. `_SUBSTANCE_SIGNALS` is defined at line 146 inside `progression_loop.py`.
2. The list contains tokens explicitly grouped under four domain labels: electronics, mechanical, software, medical.
3. `assess_response()` at line 215 uses `_SUBSTANCE_SIGNALS` directly to produce `has_substance`.
4. `has_substance` influences the `REASONED` vs `ASSERTED` classification path.
5. `REASONED` classification is a gate for maturity advancement.
6. The module docstring at line 3 claims scope is "electronics/electrical only" — contradicted by the list itself which includes mechanical, software, and medical tokens.
7. `get_question()` at line 124 imports from `engine.domain_rules` — this delegation is present and correct.
8. No `if domain == X` branching was observed in `run_iteration`, `evaluate_transition`, or `integrate_response`.

### 5.2 Interpretation (agent's reading of the evidence)

The violation identified in AB-001 is **confirmed by evidence**. `_SUBSTANCE_SIGNALS` is a domain-specific data structure — it contains tokens organised by domain and used to make classification decisions — and it resides in `progression_loop.py` rather than `domain_rules.py`.

The comment on line 226 (`for non-electronics domains`) suggests the original author was aware that the classification logic needed to handle multiple domains but implemented the expansion by adding tokens to `_SUBSTANCE_SIGNALS` rather than moving the list to `domain_rules.py`.

The `get_question()` delegation pattern at lines 118–127 demonstrates that the correct architectural pattern was known and applied for question generation. The same pattern was not applied to substance signal detection.

The `state.domain` passthrough calls (Location 1E) are not violations — they are correct usage of the delegation architecture.

### 5.3 Assumptions (not directly confirmed by evidence)

1. **Assumption:** `domain_rules.py` has a structure that could accept a `_SUBSTANCE_SIGNALS`-equivalent per domain. This has not been verified in this report.
2. **Assumption:** Moving `_SUBSTANCE_SIGNALS` to `domain_rules.py` would require a new function signature (e.g., `get_substance_signals(domain)`) — this is an interpretation of how a fix might work, not a confirmed fact.
3. **Assumption:** The 4-domain expansion of `_SUBSTANCE_SIGNALS` happened incrementally as new domains were added, rather than as a deliberate architectural decision. This is plausible but not confirmed by git history inspection.
4. **Assumption:** Removing `_SUBSTANCE_SIGNALS` from `progression_loop.py` would break existing tests. Confirmed likely by the presence of `test_assess_response_adversarial.py` and `test_assess_response_replay.py` which test classification behavior — but test internals not examined in this report.

---

## SECTION 6 — AB-001 PRELIMINARY VERDICT

**PARTIAL VIOLATION**

### Rationale

The evidence shows one clear violation and one correct pattern coexisting in the same file:

**Violation confirmed:** `_SUBSTANCE_SIGNALS` (lines 146–171) is a domain-specific data structure — labelled by domain name, containing domain-specific vocabulary — that resides in `progression_loop.py`. Its use in `assess_response()` means that domain-specific token lists directly influence the REASONED/ASSERTED classification, which gates maturity advancement. This behavior belongs in `domain_rules.py` per the architectural invariant.

**No violation found:** `get_question()` (lines 118–127) correctly delegates to `domain_rules.py`. `state.domain` passthrough calls (lines 416–489) pass domain as a parameter without interpreting it. `_WEAK_PATTERNS` and `_CAUSAL_STRUCTURE_PATTERNS` appear domain-agnostic.

**Mixed case confirmed:** The violation is isolated to `_SUBSTANCE_SIGNALS` and its usage in `assess_response()`. The rest of the domain interaction pattern in `progression_loop.py` follows the correct delegation model.

**Scope of violation:** One data structure + one function's dependency on it. Not a systemic misarchitecture of the entire file.

**Additional finding:** The module docstring scope claim ("electronics/electrical only") is factually wrong — the file already handles mechanical, software, and medical domains via `_SUBSTANCE_SIGNALS`. This documentation inconsistency is a secondary finding, not an architectural violation.

---

*Evidence source: grep output and sed sections from engine/progression_loop.py at HEAD 01d353e.*
*No engine code was modified to produce this report.*
*No remediation proposed. Classification only.*
