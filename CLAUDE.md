# InventorAI — Refactor Governance Contract

## Mission

This repository is undergoing behavior-preserving extraction and replay stabilization.

Primary goal:
Preserve historical benchmark behavior while tracing semantic provenance accurately.

This is NOT a redesign project.

---

# Core Rules

1. Do NOT redesign architecture.
2. Do NOT optimize behavior.
3. Do NOT modernize schemas.
4. Do NOT improve heuristics.
5. Do NOT silently upgrade semantics.
6. Do NOT patch replay blindly.

All changes must preserve historical behavior unless explicitly approved.

---

# Historical Truth Source

`benchmark/run_benchmark_v1.py`

This file is the historical behavioral authority unless explicitly overridden.

---

# Required Engineering Method

Every mismatch must first be classified:

- structural contract drift
- semantic drift
- fixture drift
- runtime dependency drift
- actual logic defect

No patching before classification.

---

# Mandatory Provenance Tracing

Every semantic mismatch must be traced chronologically:

raw_response
→ extraction
→ normalization
→ fixture generation
→ replay scoring
→ final report

Never guess the origin of drift.

---

# Scoring Rules

Do NOT modify scoring criteria unless:

1. parity proof exists
2. benchmark lineage is proven
3. behavior matches historical benchmark intent

No replay cosmetics.

---

# Adapter Rules

Compatibility adapters are allowed ONLY for:

- legacy field aliases
- structural compatibility
- schema bridging

Adapters must NEVER alter semantic meaning.

---

# Fixture Rules

Fixtures are evidence artifacts.

Do NOT mutate fixtures unless explicitly approved.

Replay greenness alone is NOT proof of correctness.

---

# Semantic Safety Rules

Avoid:
- forced confidence downgrades
- artificial replay parity
- hidden heuristic upgrades
- semantic masking

Historical parity must be balanced with:
- semantic correctness
- governance intent
- provenance evidence

---

# File Creation Rules

Before creating any file, document:

- file path
- purpose
- input contract
- output contract
- prohibited behaviors

All files must remain:
- small
- deterministic
- single-purpose

---

# Forbidden Behaviors

The following are forbidden unless explicitly approved:

- hidden fallback logic
- silent schema coercion
- benchmark gaming
- replay-only hacks
- implicit semantic upgrades
- uncontrolled aliasing

---

# Stop Conditions

STOP immediately and report diagnosis if:

- semantic origin becomes unclear
- replay passes without provenance proof
- scorer patching becomes tempting
- fixture mutation appears necessary
- historical truth becomes ambiguous

Diagnosis is preferred over speculative coding.

---

# Current Priority

Freeze replay patching.

Current investigation focus:

1. provenance tracing
2. semantic drift source identification
3. confidence assignment lineage
4. recommendation/action contract divergence

No redesign work is authorized.
## Reporting Integrity Rules

The replay report is not allowed to infer, reinterpret, suppress, or recompute scoring truth.

The authoritative scoring result is the raw output of:

engine.scoring.score_case()

Any replay reporter, formatter, verifier, or summary script must render this output faithfully.

Forbidden:
- dropping issues from score_case()
- converting overall=false into pass
- hiding failed criteria
- recomputing pass/fail outside score_case()
- reporting partial truth as full parity
- using replay greenness as proof without raw score evidence

Every replay report must include or reference:
- raw score_case() output
- weighted_score
- overall
- failed criteria
- issues
- scoring_version
- fixture/hash provenance when available

If final replay output disagrees with score_case(), STOP and report:

REPORTING DIVERGENCE DETECTED

---

## Active Governance Documents

The following documents were added after the initial governance contract.
Read them before any code change or architectural decision.

GOVERNANCE_MODEL.md
  Authority hierarchy (Tiers 1-4), confirmed violations,
  and remediation steps for replay/provenance issues.
  Status: ACTIVE

MVP_SCOPE_FREEZE.md
  Hard boundary on MVP scope.
  Read this before writing any code.
  Status: ACTIVE FREEZE

DECISION_PROGRESSION_MODEL.md
  Proposed architecture for the progression engine.
  Electronics/electrical domain, LEVEL 0-2 only.
  Status: PROPOSED — not implemented, not validated

## Document Authority Order

When documents conflict, this order applies:
1. MVP_SCOPE_FREEZE.md       (hard constraint)
2. GOVERNANCE_MODEL.md       (authority hierarchy)
3. CLAUDE.md                 (engineering rules)
4. DECISION_PROGRESSION_MODEL.md (proposal only)
