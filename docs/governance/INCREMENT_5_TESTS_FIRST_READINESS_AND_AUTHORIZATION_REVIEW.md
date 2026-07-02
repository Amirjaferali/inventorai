# Increment 5 — Concrete Validation-Plan Generation

# Owner-Gated Tests-First Readiness and Authorization Review

Status:
`READ-ONLY REVIEW — ASSESSMENT AND RECOMMENDATION ONLY — AUTHORIZES NOTHING`

Review type:
The single next governed action recorded by the active roadmap after the
Increment 5 implementation-contract merge (PR #59):
`OWNER-GATED INCREMENT 5 TESTS-FIRST READINESS AND AUTHORIZATION REVIEW` —
"owner-gated, assessment/authorization only, not automatic tests creation and
not source authority."

Review basis (resolved from Git, not from memory or chat history):
- Integration lane tip reviewed:
  `52a738ec1bf01e64f95a4ab288212d077556dd5f`
  (`origin/feature/atomic-json-session-persistence`, PR #59 roadmap-sync merge).
- Product-execution tip (unchanged by Increment 5 to date):
  `f1734285162915ac577c93a37b30e7babd68586e` (PR #54, Increment 4 SOURCE merge).
- Default branch `main`: `0e89e4636399760965c9ff8086b465c90dbadf8e` (outside the
  increment lane).
- This review artifact is authored on `claude/increment-5-readiness-review-51jsgw`.

---

## 0. Boot compliance and non-authorization

Before this review, the mandatory `CLAUDE.md` reading order was read in full:
`ILT-002_GOVERNANCE_ANCHOR.md`, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
`STRATEGIC_PRODUCT_VISION.md`, `PATH_N_CURRENT_EXECUTION_ANCHOR.md`,
`DUAL_PATH_PRODUCT_ANCHOR.md`, `ACTIVE_EXECUTION_ROADMAP.md`, and the Increment 5
phase authorities (`INCREMENT_5_DESIGN.md`, `INCREMENT_5_IMPLEMENTATION_CONTRACT.md`).
`MVP_SCOPE_FREEZE.md` and the Increment 4 authorities were read to bound scope.

Per the ILT-002 anchor, no global state was reconstructed: every state fact below
is verified against committed Git evidence at the SHAs cited, per session-level
evidence only.

This document:
- is a READ-ONLY assessment;
- does NOT authorize tests-first creation;
- does NOT authorize source or template implementation;
- does NOT authorize staging, commit, push, PR, review, or merge of any tests-first
  or source artifact;
- does NOT resume persistence, touch the domain registry / domain packs, alter
  scoring, `engine/progression_loop.py`, or any prior increment;
- moves no hold, gate, block, or classification;
- creates no product behavior by its existence.

Every downstream step (tests-first authoring, then source) remains a separate,
explicit, owner-gated authorization (contract §24; roadmap §6, §7).

---

## 1. Mandate and method

**Mandate.** Determine, read-only, whether the repository and the Increment 5
lifecycle are in a state where the owner may safely authorize the **tests-first
package** for Increment 5 (a single new file of plain, pre-source, failing tests,
per the Increment 3/4 precedent), and record a recommendation for that owner gate.

**Method.**
1. Confirm the Increment 5 lifecycle state from committed evidence.
2. Verify that every upstream structural dependency the contract's tests-first
   obligations (§19) must bind against is present, stable, and unambiguous at the
   integration tip.
3. Verify the current test baseline the tests-first package will extend.
4. Assess the implementation contract for internal consistency and testable
   determinism (the tests-first package encodes the contract's acceptance criteria).
5. Confirm governance boundaries and preserved holds.
6. Record readiness observations and an owner-gated recommendation.

"Tests-first readiness" here means: a competent author, under a later separate
authorization, could write the §19 tests as plain pre-source failing tests without
inventing a product decision, without touching a held lane, and with every asserted
behavior traceable to a committed structural signal or a fixed contract clause.

---

## 2. Increment 5 lifecycle state (verified)

Increment 5 = **Concrete Validation-Plan Generation**, the fifth increment of the
Product-Value Correction Plan (dependency order 3 → 4 → **5** → 6). Verified state at
`52a738e`:

| Lifecycle step | State | Evidence |
|---|---|---|
| Owner rulings (ten) | Incorporated and traceable in the merged design (§0, §18) | `INCREMENT_5_DESIGN.md` |
| Bounded design | **MERGED** | PR #56 true-merge `0c96c3fc88d9f1faa18860a3046b6d4df4a2b49a`; `INCREMENT_5_DESIGN.md` blob `067c5753deff2fe8af5e2f3ec347f85e6fe28067` (338 lines) |
| Implementation contract | **MERGED** | PR #58 true-merge `4397e0245255b0f3bfcd573101ad78251d37bfa5`; `INCREMENT_5_IMPLEMENTATION_CONTRACT.md` blob `fa1544b904179a534e6b050f1a069c6e28bf31fb` (732 lines) |
| Roadmap synchronization | **MERGED** | PR #59; integration tip `52a738e` |
| Tests-first package | **NOT started, NOT authorized** | `tests/test_increment_5_validation_plan.py` absent at `52a738e` |
| Source implementation | **NOT started, NOT authorized** | `engine/validation_plan.py` absent at `52a738e` |
| Product-execution tip | **Unchanged** at `f1734285` | Increment 5 has advanced no product code |

The design and contract blob SHAs above independently match the SHA-256 / blob
values recorded in the roadmap and in the two PR bodies, confirming the merged
artifacts are the reviewed artifacts.

**Prerequisite chain for authorizing the tests-first step is therefore complete:**
design merged → contract merged → roadmap synced. The only remaining gate before
tests-first authoring is this owner-gated review plus a separate owner authorization.

---

## 3. Tests-first readiness assessment

### 3.1 Upstream structural dependency verification (integration tip `52a738e`)

The tests-first package binds against Increment 4 payloads and `IdeaState` fields
named in the contract §4/§5/§7/§16. Each was verified PRESENT and matching:

| Contract reference | Required shape | Verified at `52a738e` |
|---|---|---|
| §4 entry point | `derive_requirement_landscape(state)` primary feed | `engine/requirement_landscape.py` present |
| §4/§5 landscape | `RequirementLandscape{requirements, risks}` | present (frozen dataclass) |
| §4/§5 requirement | `DerivedRequirement{requirement_id, statement, primary_anchor, source_status, criticality, criticality_authority, criticality_rationale, resolving_action, linked_risk_ids, supporting_references}` | present, field-for-field |
| §4/§5 anchor | `ProvenanceAnchor{anchor_kind, anchor_reference, display_label}` | present |
| §4/§5 action | `ResolvingAction{action_kind, statement, source_reference}` | present |
| §7 anchor kinds | `assertion`, `pending_evidence`, `pending_specialist`, `gap`, `active_contradiction` | all present in `_SOURCE_STATUS` / `_ANCHOR_LABELS` / `_ACTION` |
| §9 requirement-id prefixes | `req:assertion:`, `req:evidence:`, `req:specialist:`, `req:contradiction:`, `req:gap:` | all present in `_record_id_prefix` / builders |
| §4/§7 record axes | `AssertionRecord.{disposition, provenance, validation_status, responsibility, superseded_by}` and `LEGACY_UNSPECIFIED` | all present on `engine/idea_state.py` (`responsibility: Optional[str] = None`, `superseded_by: Optional[str] = None`, provenance default `LEGACY_UNSPECIFIED`) |
| §16 package numbering | highest existing key `section_13_requirement_landscape`; `_s12`, `_s13` present → `section_14_validation_plan` / `_s14` is the correct next additive key | confirmed (`section_10`..`section_13`) |

**Finding:** every named dependency exists and matches the contract. No missing or
renamed field, no numbering collision. The contract fixes only names that are (a)
already present upstream, or (b) new-and-additive (`section_14`, `vstep:`/`vblock:`
prefixes) — none of which conflicts with a committed symbol.

### 3.2 Test-baseline verification

Full suite at `52a738e`:

```
31 failed, 758 passed, 1 skipped, 1 xfailed, 24 xpassed
```

- All **31 failures are confined to `tests/test_domain_registry.py`** (verified by
  reducing the failure set to distinct files → one file). This is the known,
  separate, unauthorized domain-registry lane that the contract (§17, §22.11)
  explicitly excepts and forbids relying on or "fixing" within Increment 5.
- The `24 xpassed` / `1 xfailed` are pre-existing assessment-quality markers
  (RISK-001 / RISK-002 in `test_assess_response_adversarial.py` and
  `test_progression_benchmark.py`), unrelated to Increment 5. They are the same
  arithmetic recorded for the Increment 4 baseline (PR #55) and are outside
  Increment 5 scope.

**Finding:** the baseline is stable, known, and correctly quarantined. A tests-first
package that adds a single new file of failing tests will change only that new
file's arithmetic; the contract's acceptance criterion §22.11 ("no new non-baseline
failures, the 31 `test_domain_registry.py` baseline excepted") is measurable against
this baseline.

### 3.3 Contract implementability and testable determinism

The contract expresses its acceptance criteria (§22) in objective, structural terms —
frozen payloads, stable non-positional identifiers (`vstep:` + Increment 4
`requirement_id`), an order-independent equality property, a bounded five-value
responsibility vocabulary with a total precedence order (§7), a fixed
`closure_condition` template (§13), and a fixed additive package key (§16). Every
assertion the §19 tests must make maps to either a committed structural signal or a
fixed contract clause. §22 explicitly bars unverifiable wording ("robust",
"appropriate", …). The four-level epistemic truth model (§13) and the no-`result`/
`supplied`/`passed`/`verified` prohibition are testable as field-absence and
string-absence assertions.

**Finding:** the contract is implementable as plain pre-source failing tests without
inventing a product decision. No blocking ambiguity was identified.

### 3.4 Import-boundary and non-dependency feasibility

The contract freezes the Increment 5 import boundary to `engine.idea_state` +
`engine.requirement_landscape` only, and forbids importing
`engine.idea_development_outputs` or reading `derive_next_development_step`
(F-INC5-1). Both guardrails are testable at the module level (e.g. import-graph /
source-scan assertions, per the Increment 4 precedent). The record-level fields the
§7 responsibility mapping needs (`disposition`, `provenance`, `responsibility`) are
reachable through `engine.idea_state` alone — no third import is required.

**Finding:** the import boundary is honorable and independently testable.

---

## 4. Readiness observations (non-blocking)

None of the following blocks authorization. Each is a fixture-design note the
tests-first author should address so the §19 obligations are met without drift.

**O-A — `assertion`-anchor responsibility requires a record look-back.**
Increment 4's `_requirement_from_record` collapses the dispositions `answered`,
`unknown`, `deferred`, and `provisional_assumption` into the single anchor kind
`assertion` (only `evidence_requested` → `pending_evidence` and
`specialist_requested` → `pending_specialist` are distinguished at the anchor).
Contract §7 therefore requires the source to recover the actor class by reading the
underlying `AssertionRecord.disposition` / `provenance` via `engine.idea_state`,
keyed by `primary_anchor.anchor_reference` (= `rec_N`). The tests-first package must
build fixtures that drive each branch of the §7 precedence
(`answered` + owner-stated provenance → `OWNER_EXECUTABLE`;
`unknown` / `deferred` / provisional-without-support / `LEGACY_UNSPECIFIED` →
`UNDETERMINED`; explicit valid `AssertionRecord.responsibility` used first). This is
the single most intricate area and warrants dedicated per-branch coverage.

**O-B — `BLOCKED` is corpus-unreachable and must be constructed.**
Contract §6 states that in the current MVP-1 corpus every Increment 4 anchor kind
maps to an eligible step, so a natural `IdeaState` cannot produce `outcome = BLOCKED`.
The §19 / §22.9 "constructed `BLOCKED` case" therefore requires the tests-first
author to synthesize an ineligible input (e.g. a `DerivedRequirement` with
`resolving_action is None`, or an `anchor_kind` outside the §7 mapping) at the test
boundary. This is a legitimate test-construction technique and is anticipated by the
contract; it is flagged so the author does not mistake `BLOCKED`'s natural
absence for a defect.

**O-C — mixed-state fixture likewise requires a crafted ineligible/malformed item.**
§12/§15/§19 require a mixed state (≥1 eligible AND ≥1 ineligible/malformed →
`outcome = PLAN` with non-empty `steps` AND non-empty `blocked_items`, both rendered
and both in the package, no `PARTIAL`). As with O-B, the ineligible/malformed member
must be constructed deliberately at the test boundary.

**O-D — baseline `xpassed`/`xfailed` hygiene is out of Increment 5 scope.**
The 24 `xpassed` + 1 `xfailed` markers are stale relative to current behavior but
are a separate assessment-quality lane. Contract §17 requires existing test
arithmetic outside Increment 5 to remain unchanged; the tests-first package MUST NOT
touch these. Cleaning them up is a distinct, separately-gated hygiene item for the
owner's awareness — not an Increment 5 action.

---

## 5. Governance-boundary confirmation

- **MVP scope freeze.** Increment 5 is deliverable-only and additive: one new
  deliverable section + one machine-package key, **no scoring**, **no external-
  document generation** (a section inside the existing FDC deliverable is not an
  external document), **no domain / multi-domain work**, **no new maturity level**,
  **no new `IdeaState` field**. It reorganizes already-recorded structural signals
  ("Improvement, Not Generation"). This is consistent with `MVP_SCOPE_FREEZE.md`
  (which freezes out "Scoring of any kind", broad external-document generation, and
  multi-domain orchestration) and with the freeze posture under which Increments
  1–4 were merged.
- **Domain-registry red baseline and domain-pack drift are correctly quarantined.**
  The 31 `test_domain_registry.py` failures and the presence of multiple domain
  packs are a separate, unauthorized lane; the contract forbids relying on or fixing
  them within Increment 5, and Increment 5 has no domain dependency. This review
  does not authorize any action on that lane.
- **Preserved holds (unchanged; this review moves none):**
  persistence lane `PRESERVE UNMODIFIED AND PAUSE`; domain-registry cleanup, the
  compact/session-summary item, and Increment 6 remain separately gated; no
  synchronization with `main` is authorized; R2 = HELD; FORM T = BLOCKED;
  S-6 = UNCLASSIFIED; AA-3/AA-4/AA-5 = BLOCKED; Path N Phase 5 / Phase 6 =
  UNAUTHORIZED; ILT-002 evidence collection = NOT AUTHORIZED.

---

## 6. Authorization finding and owner-gated recommendation

**Readiness disposition:**

```
INCREMENT 5 TESTS-FIRST — READY FOR OWNER-GATED AUTHORIZATION,
WITH THREE NON-BLOCKING READINESS OBSERVATIONS (O-A, O-B, O-C).
```

Basis: the lifecycle prerequisites are complete (design merged, contract merged,
roadmap synced); every upstream structural dependency the tests-first obligations
require is present and matching at `52a738e`; the test baseline is stable, known,
and correctly quarantined; the contract is implementable as plain pre-source
failing tests with objective, structural acceptance criteria and an honorable,
testable import boundary. **No blocking finding was identified.**

**Recommended scope of the tests-first authorization, should the owner grant it**
(recorded as a recommendation only — this review grants nothing):
- exactly ONE new file: `tests/test_increment_5_validation_plan.py`;
- plain, pre-source, **failing** tests (Increment 3/4 precedent), inventing no
  product decision;
- coverage of the contract §19 obligations, explicitly including the §7
  responsibility precedence per O-A, and constructed `BLOCKED` (O-B) and mixed-state
  (O-C) cases;
- NO source, template, `web/app.py`, persistence, domain-registry, scoring,
  prior-increment, roadmap, or anchor change; the 31 `test_domain_registry.py`
  baseline failures left untouched (§17, §22.11).

**What remains separately owner-gated after any tests-first authorization:** source
implementation, and every staging / commit / push / PR / review / merge for both the
tests-first and the source artifacts, plus any roadmap synchronization (contract
§24). Authorizing tests-first authoring does not authorize source.

**Transport note.** This review artifact was authored on
`claude/increment-5-readiness-review-51jsgw` (based on `main`), because that is the
branch designated for this task. It is a self-contained, SHA-grounded assessment of
the integration lane at `52a738e`; it modifies no integration-lane or `main` file.
Placing it into the integration lane's `docs/governance/` history (if desired) is a
separate, owner-gated documentation action.

---

## 7. Evidence appendix

Commands were read-only (Git object reads, a detached worktree of the integration
tip, and a full `pytest` run); no lane state was modified.

- Integration tip: `git rev-parse origin/feature/atomic-json-session-persistence`
  → `52a738ec1bf01e64f95a4ab288212d077556dd5f`.
- Merged-artifact identity:
  `INCREMENT_5_DESIGN.md` blob `067c5753deff2fe8af5e2f3ec347f85e6fe28067`;
  `INCREMENT_5_IMPLEMENTATION_CONTRACT.md` blob `fa1544b904179a534e6b050f1a069c6e28bf31fb`
  (both match the roadmap- and PR-recorded values).
- Dependency verification: `git show 52a738e:engine/requirement_landscape.py`,
  `:engine/idea_state.py`, `:engine/deliverable_assembler.py` (dataclass fields,
  anchor-kind maps, id prefixes, section keys as tabulated in §3.1).
- Absence of unauthored artifacts at `52a738e`: `engine/validation_plan.py` and
  `tests/test_increment_5_validation_plan.py` do not exist.
- Baseline: `python -m pytest -q` at `52a738e` →
  `31 failed, 758 passed, 1 skipped, 1 xfailed, 24 xpassed`; failing set reduces to
  the single file `tests/test_domain_registry.py`.

*This review is produced to be accurate, not reassuring. It authorizes nothing.*
*`ACTIVE_EXECUTION_ROADMAP.md` remains the sole authority for execution lanes,*
*holds, and authorized next actions.*
