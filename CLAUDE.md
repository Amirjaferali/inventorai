# Current Repository Execution Authority

This section overrides any older current-priority, active-document, or
document-authority statement in this file when they conflict.

Before any analysis, recommendation, code change, command execution, file
creation, staging, commit, or push, every Claude Code session, team lead,
subagent, and Agent Teams teammate MUST read, in this order:

1. `docs/governance/ILT-002_GOVERNANCE_ANCHOR.md`
2. `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`
3. `docs/governance/STRATEGIC_PRODUCT_VISION.md`
4. `docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md`
5. `docs/governance/DUAL_PATH_PRODUCT_ANCHOR.md`
6. `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`
7. `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`
   — mandatory product-foundation and commercial-readiness remediation plan (the
   owner-approved v2 candidate; it supersedes any earlier draft). Read it in full
   after the governing anchors and the roadmap and before any Product UX/UI,
   persistence, accounts, API, multi-domain, subscription, or other implementation
   work. Every agent MUST: read the full plan; resolve and verify the current
   authoritative branch and tip from the active governance sources (do not treat
   the plan's historical drafting baseline SHA as the expected tip); verify the
   currently active phase from the latest committed roadmap and status surfaces;
   distinguish its statuses (`RECORDED` / `PLANNED` / `ELIGIBLE` /
   `OWNER-AUTHORIZED` / `ACTIVE` / `CLOSED`) and never treat one as another;
   perform no automatic downstream activation (closing one phase never activates
   another); and return `VERIFICATION BLOCKED` when repository state, the
   authoritative tip/branch, the active phase, or authorization cannot be
   verified. The plan is subordinate to the committed anchors, contracts, and
   `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`; recording future work in it
   authorizes nothing.
8. Any phase-specific authorization identified as active by the roadmap
9. `docs/governance/INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md`
   — mandatory strategic product direction; non-activating and non-authorizing;
   subordinate to committed anchors, contracts, and
   `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`.
10. `docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md`
   — mandatory competitive product-value evaluation protocol; non-activating
   and non-authorizing; subordinate to committed anchors, contracts, and
   `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`; no benchmark run or result is
   implied by this record.

Repository truth overrides conversation history, memory, and assumption.

The active roadmap controls:
- the current execution lane;
- authorized next actions;
- blocked states and holds;
- mandatory stop conditions;
- roadmap-staleness handling.

Current statuses, holds, authorization boundaries, and next actions MUST be
read from the latest committed `ACTIVE_EXECUTION_ROADMAP.md`; they must not be
copied, reconstructed, or inferred from this file.

Unless the latest committed roadmap and a separate applicable authority
explicitly authorize an action, agents MUST NOT:

- reopen Gate C;
- run another E-2 attempt;
- create a new SID;
- start Flask or invoke the E-2 runner;
- modify preserved evidence;
- move any status or hold;
- classify S-6;
- create or imply downstream authorization;
- treat analysis, recommendations, or team consensus as authorization.

Agent Teams does not create authority. Every teammate is bound by the same
repository documents, prohibitions, and stop conditions as the team lead.

If Git history contains a qualifying state-change event not reflected in the
roadmap, STOP, report the exact evidence, and request roadmap synchronization.
Do not continue under a stale roadmap.

---

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
