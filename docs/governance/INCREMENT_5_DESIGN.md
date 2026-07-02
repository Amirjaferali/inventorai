# Increment 5 Design — Concrete Validation-Plan Generation

Status:
`BOUNDED DESIGN DRAFT — NOT AN IMPLEMENTATION CONTRACT, TESTS-FIRST, OR SOURCE AUTHORIZATION`

Authoritative baseline at drafting:
`cdb4f91e9f2ba0ed5da087cbdfd4c342512b35b3` (PR #55 roadmap-sync merge;
product-execution tip `f1734285162915ac577c93a37b30e7babd68586e`, PR #54 Increment 4
SOURCE merge). The live tip is always resolved from Git; this SHA is a
document-publication baseline, not a permanent live-tip assertion.

## 0. Authority, order, and non-authorization

This document is the bounded, owner-gated DESIGN for Increment 5 — Concrete
Validation-Plan Generation, the fifth increment of the committed Product-Value
Correction Plan (dependency order 3 → 4 → **5** → 6). It is subordinate to, and
must be read after, the CLAUDE.md-ordered authority set:
`ILT-002_GOVERNANCE_ANCHOR.md`, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
`STRATEGIC_PRODUCT_VISION.md`, `PATH_N_CURRENT_EXECUTION_ANCHOR.md`,
`DUAL_PATH_PRODUCT_ANCHOR.md`, `ACTIVE_EXECUTION_ROADMAP.md`, the merged Increment 4
authority/design/contract, and `MVP_SCOPE_FREEZE.md`. Where any of those and this
design could differ, they control.

This design authorizes NOTHING to be built. It creates no implementation contract,
no tests-first authority, no tests, no source or template change, no persistence,
no domain work, and no product-behavior change. Every later step is a separate,
explicit, owner-gated authorization.

It ratifies the ten owner rulings of this turn (traced in §18) and translates them
into bounded design decisions D-1 … D-13. It reuses stable concepts from Increments
1–4 but does NOT reopen or redesign them.

**Committed-dependency-order caveat (required):** the committed plan's dependency
order (3 → 4 → 5 → 6) establishes the next governed *product path* only. It is NOT
new market-validation evidence and asserts no market readiness; the competitive
benchmark (`docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md`) is a
non-activating evaluation record and confers no authority here.

## 1. Product problem and user-visible value

After Increment 4, the deliverable shows a static, provenance-anchored Requirement
Landscape in which each requirement carries ONE atomic resolving action, and
Increment 3 surfaces ONE next development step. Neither gives the inventor an
ordered, multi-step **path** for moving an idea toward decision-readiness.

Increment 5 adds exactly that bounded value: a deterministic, ordered **validation
plan** — a sequence of proposed validation steps, each stating what must be
validated, which kind of actor must perform it, what category of evidence would
close it, and the truthful closure condition — WITHOUT asserting that any
validation occurred. This is "Improvement, Not Generation": it reorganizes and
sequences already-recorded, structurally supported signals; it invents no
technical content.

User-visible value over Increment 4: sequencing (a coherent path, not scattered
per-requirement actions), responsibility classification (who must act), and
explicit closure/evidence conditions — aligned with the benchmark's required
outcome shape ("a bounded, evidence-classified decision-readiness record, or a
truthful blocked outcome").

## 2. Authorized scope and explicit exclusions (rulings 1, 7, 8, 10)

IN SCOPE (MVP-1): a bounded, structural, generic validation plan derived read-only
from committed recorded signals; a single additive deliverable section; a JSON-safe
machine representation; deterministic derivation and ordering.

The plan MAY identify, per step: what must be validated; the responsibility class
of the required actor; the category of evidence that would close the step; and the
truthful closure condition.

EXCLUDED (MUST NOT), in MVP-1 and by this design:
- inventing or prescribing ungrounded standards, equipment, thresholds,
  measurements, test values, acceptance values, jurisdictions, regulatory
  requirements, or domain-specific professional procedures;
- generating external validation documents;
- any scoring of any kind;
- session-UI change; any `web/app.py` change; any change to or dependency on
  persistence, the paused persistence worktree, the domain registry, domain packs,
  a professional workspace, or `engine/scoring.py` / `engine/progression_loop.py`;
- modifying `_s4`, `_s6`, or any Increment 1–4 behavior;
- claiming feasibility, safety, compliance, testing, verification, market-readiness,
  or implementation-readiness (§13).

## 3. Input authority and allowed upstream dependencies (rulings 2, 8)

Increment 5 is an ADDITIONAL, INDEPENDENT read-only selector over the same
`IdeaState`. Allowed committed inputs:
- Increment 4 `derive_requirement_landscape(state)` — the primary feed: its
  requirements, each requirement's `resolving_action`, `source_status`, provenance
  anchor, criticality, and criticality authority;
- Increment 2 truthful axes on records — provenance, validation status,
  disposition, `superseded_by` (active-set rule).

The Increment 5 engine module MAY import, among project modules, ONLY
`engine.idea_state` and the Increment 4 requirement-landscape module (its stable
public derivation and payloads). It MUST NOT import or depend on scoring,
progression, persistence, session, `web/app.py`, the domain registry/packs, or the
AI advisor. It MUST NOT depend on domain-registry behavior; the known
`tests/test_domain_registry.py` failures remain a separate, unauthorized lane.

No new `IdeaState` field is added or required. The derivation invents no recorded
signal.

## 4. Exact conceptual output model (rulings 2, 3, 4, 5)

The derivation returns one immutable **ValidationPlan** value:
- `steps`: an ordered, deduplicated tuple of **ValidationStep**;
- `blocked_items`: an ordered tuple of **BlockedValidationItem** (truthful "cannot
  yet form a step" entries; §9);
- `outcome`: a bounded enum — `PLAN` (≥1 step), `EMPTY` (nothing actionable),
  `BLOCKED` (recorded signals exist but none can support a truthful step).

Each **ValidationStep** carries only:
- `step_id` — deterministic, derived from the supporting requirement/anchor's stable
  identity (§8); never from list position;
- `statement` — a restatement of what must be validated, derived only from the
  supporting recorded signal or a fixed template; invents no technical content;
- `responsibility` — one responsibility class (§5);
- `evidence_category` — the CATEGORY of evidence that would close the step (e.g.
  owner confirmation, specialist input, empirical evidence, reconciliation of
  conflicting records) — a bounded, generic category, never a specific test/value;
- `provenance` — a structurally addressable reference to the authorized recorded
  source (§6), carrying a human-readable label with no raw-enum leak;
- `confidence` — bounded (§6); `UNDETERMINED` where evidence is insufficient;
- `closure_condition` — the truthful statement of what would close the step
  ("evidence required", not "evidence supplied" or "passed").

A ValidationStep has NO result, verdict, "validated", "supplied", "passed", or
"verified" field (§7). All payloads are immutable (frozen), all collections are
tuples, equality is structural — reusing the Increment 4 immutability discipline.

## 5. Responsibility classification (ruling 3)

Bounded responsibility classes, exactly:
`OWNER_EXECUTABLE`, `SYSTEM_DERIVABLE`, `SPECIALIST_REQUIRED`,
`EMPIRICAL_EVIDENCE_REQUIRED`, `UNDETERMINED`. These are conceptually the
Increment 2 responsibility axis re-expressed as validation-actor classes; the
mapping is deterministic and structural (derived from the supporting record's
disposition/provenance and the Increment 4 resolving-action kind), never from
free text.

`PROHIBITED` is NOT a responsibility/actor class. Prohibition is modelled
separately as an **emission-eligibility** decision, justified as follows: "who must
act" (responsibility) and "may a step be emitted at all" (eligibility) are distinct
concerns. A candidate step is emitted ONLY when a structurally addressable recorded
signal supports it; an action that would require inventing ungrounded domain content
is INELIGIBLE and is therefore NOT emitted as a step — instead, where a recorded
signal exists but cannot yet support a truthful step, it is recorded as a
`BlockedValidationItem` (§9) naming the missing evidence/authority. Thus prohibition
never masquerades as an actor and never produces a fabricated step.

## 6. Provenance and confidence rules (ruling 5)

Every emitted step MUST retain structurally addressable provenance to an authorized
recorded source (the requirement's provenance anchor, itself anchored to a `rec_N`
record, a `gap_type`, or an order-normalized contradiction pair per Increment 4).
No step may exist without such provenance.

Confidence is bounded and derived structurally; MVP-1 default is `UNDETERMINED`
wherever evidence is insufficient. Confidence, responsibility, evidence category,
standards, criticality, and any domain fact MUST NOT be derived from free-text
inference, keyword detection, or language-model judgment (mirrors Increment 4
§9.7.3 / §9.8.1). Absent an explicit, structurally addressable signal, the truthful
value is `UNDETERMINED`.

## 7. Proposed-action versus completed-validation truth model (ruling 4)

The design distinguishes four epistemic levels:
1. a **proposed** validation action (what should be done);
2. the **evidence category required** to close it;
3. evidence **actually supplied**;
4. a **verified validation result**.

Increment 5 MVP-1 generates ONLY levels 1 and 2. It never represents levels 3–4 and
never implies them: generating a plan is not evidence, not supply, not a pass, and
not verification. No field, label, ordering, or rendered string may state or imply
that evidence was supplied, a step passed, or the idea was verified.

## 8. Deterministic derivation, ordering, identity, and deduplication (ruling 6)

Derivation is pure, deterministic, read-only, and order-independent: the same
`IdeaState` yields an equal `ValidationPlan`, and reordering input records changes
no identifier and no rendered result. Only active records participate
(`superseded_by is None`), reusing the Increment 2 / Increment 4 active-set rule.

Identity: `step_id` derives solely from the supporting anchor's stable key
(`rec_N`, `gap_type`, or the order-normalized contradiction pair), never from list
position. Steps are deduplicated by their stable key. A step maps one-to-one to a
structurally supported requirement-resolving action or authorized recorded signal;
Increment 5 introduces no new anchor kinds and reuses Increment 4's stable keys.

Ordering is a separate deterministic function of stable keys and is
ORGANIZATIONAL ONLY. It MUST NOT silently imply severity, urgency, business
priority, safety priority, or criticality (all criticality is `UNDETERMINED` in the
current corpus, and grounded risk is empty). The display order carries no ranking
meaning unless a committed structural signal explicitly authorizes another meaning;
no such signal exists in MVP-1.

## 9. Empty, blocked, malformed-record, and degraded outcomes (rulings 9, 4)

- **EMPTY:** when no active recorded signal can support any truthful step, the plan
  is deterministically empty (`outcome = EMPTY`) with an idea-development-framed
  empty statement — not an error and not a fabricated step.
- **BLOCKED:** when authorized recorded signals exist but none can support a
  truthful validation step (e.g. required evidence, authority, or specialist input
  is missing), the derivation returns `outcome = BLOCKED` with `blocked_items` that
  truthfully identify the missing evidence, authority, or specialist input, naming
  the responsibility class and provenance — never inventing a step to fill the gap.
- **Malformed records:** degrade per-record (mirrors Increment 4 §9.10.6) — a
  malformed optional record is skipped independently; valid anchors continue to
  produce steps; the plan is empty only when no valid supporting signal remains;
  malformed data never fabricates fallback content and never crashes derivation or
  deliverable assembly.

## 10. User-visible rendering semantics (rulings 4, 6, 7, 10)

MVP-1 is DELIVERABLE-ONLY: exactly ONE additive deliverable section rendering the
plan. It shows, per step, human-readable labels only (statement, responsibility,
evidence category, provenance label, confidence, closure condition) — with NO raw
enum or internal identifier leak (mirrors Increment 4 §7.3). It renders the empty
and blocked outcomes truthfully. It MUST present the plan as PROPOSED steps, never
as completed/passed/verified, and MUST NOT imply feasibility, safety, compliance,
testing, verification, market-readiness, or implementation-readiness. There is NO
`web/app.py` and NO `web/templates/session.html` change.

## 11. Machine-package semantics

The additive deliverable section is converted to plain JSON-safe
dictionaries/lists/strings (mirroring the Increment 3 `_s12` and Increment 4 `_s13`
conversion discipline), without mutating the immutable engine payload. It contains
only the human-semantic fields above plus the bounded `outcome`; no raw internal
enum leaks into user-facing rendered output. No serialization dependency beyond
plain dict/str/tuple; no circular import.

## 12. Backward-compatibility guarantees

Purely additive. No existing deliverable section, key, or value changes; `_s4`,
`_s6`, the Increment 3 next-development-step section, and the Increment 4
requirement-landscape section are byte/behaviour-identical. No `IdeaState` field is
added or required; legacy states (empty ledger, no gaps) yield a deterministic
empty plan. Only the Increment 4 `derive_requirement_landscape` output is read
(never modified); Increment 5 does not read Increment 3's next-development-step
output. Increment 3 and Increment 4 remain closed.

## 13. Failure and non-claim requirements (rulings 4, 10)

The plan MUST NEVER imply the idea is feasible, safe, compliant, tested, verified,
market-ready, or implementation-ready. Zero grounded risk (from Increment 4) MUST
NEVER be presented as "risk-free" or as validation. Generating the plan asserts no
result. Any wording that presents a proposed step as completed, or that overstates
certainty, is a blocking defect for the future implementation. Malformed or
insufficient input yields empty/blocked outcomes, never a fabricated step.

## 14. Security, epistemic, and scope-drift risks

- **Epistemic over-claim:** a plan being read as verification. Mitigation: §7
  four-level truth model; no result/verdict field; proposed-only rendering (§10);
  non-claim boundary (§13).
- **Domain-fact invention:** steps drifting into standards/equipment/thresholds.
  Mitigation: structural-signal-only derivation (§6); generic evidence categories,
  never specific test/values (§2/§4); emission-eligibility gate (§5).
- **Silent priority implication:** ordering read as severity/urgency. Mitigation:
  organizational-only, severity-neutral ordering (§8).
- **Scope drift into held lanes:** persistence, domain registry, session, external
  documents, scoring. Mitigation: explicit exclusions (§2); import boundary (§3);
  deliverable-only (§10).
- **Injection via free text:** owner/record free text driving classification or
  content. Mitigation: no free-text/keyword/LLM derivation (§6); Jinja autoescape
  preserved in rendering.

## 15. Candidate implementation paths (NON-AUTHORITATIVE until the contract)

These are candidates only; the implementation contract selects and freezes the
exact names. Marked non-authoritative:
- NEW `engine/validation_plan.py` — pure derivation `derive_validation_plan(state)`;
  imports only `engine.idea_state` and the Increment 4 requirement-landscape module.
- MODIFIED `engine/deliverable_assembler.py` — ONE additive section function and ONE
  additive package key (candidate `section_14_validation_plan` / `_s14`, following
  the committed additive numbering where `section_13` is the current highest).
- MODIFIED `web/templates/deliverable.html` — ONE additive section.
- NEW `tests/test_increment_5_validation_plan.py` — the future tests-first package.

Prohibited paths (must remain unchanged): `engine/idea_development_outputs.py`,
`engine/scoring.py`, `engine/progression_loop.py`, `_s4`/`_s6` bodies,
`web/app.py`, `web/templates/session.html`, persistence paths, domain-registry
paths, active anchors, `CLAUDE.md`, and the Increment 4 requirement-landscape
module's behavior.

## 16. Candidate test obligations (NO tests created here)

The future tests-first package should cover at least: pure/read-only/no-mutation;
active-set filtering; deterministic order-independent `step_id`s; deterministic
severity-neutral ordering and repeated-run stability; the five responsibility
classes and their structural mapping; evidence-category correctness (generic, never
specific); provenance presence and no-raw-enum leak; `UNDETERMINED` confidence where
unsupported; the four-level truth model (no result/supplied/passed/verified field or
wording); EMPTY, BLOCKED, and malformed-per-record degradation; additive deliverable
section + JSON-safe conversion; Increment 3/4 and `_s4`/`_s6` non-regression;
import-boundary guardrails; and non-claim wording. Tests must be plain pre-source
failing tests (Increment 3/4 precedent) and must invent no product decision.

## 17. Acceptance criteria for THIS design

This design is acceptable when it: defines the product problem and bounded value;
fixes authorized scope and explicit exclusions; names allowed inputs and the import
boundary; specifies the conceptual output model, responsibility classes,
provenance/confidence rules, and the proposed-vs-completed truth model; specifies
deterministic derivation/ordering/identity/dedup and empty/blocked/malformed
outcomes; specifies deliverable-only rendering and machine-package semantics;
guarantees backward compatibility; states failure and non-claim requirements;
enumerates risks; marks candidate paths/tests non-authoritative; and traces every
one of the ten ratified rulings to design clauses (§18) — all without reopening
Increments 1–4, without authorizing implementation, and without depending on any
held lane.

## 18. Traceability — ten ratified rulings → design clauses

| Ruling | Subject | Design clauses |
|---|---|---|
| 1 | Structural/generic scope; no invented domain content | §2, §4 (`evidence_category` generic), §6, §15 (prohibited paths) |
| 2 | New value beyond Increment 4; compose supported signals only | §1, §3, §4, §8 (one-to-one supported mapping) |
| 3 | Responsibility classes; PROHIBITED not an actor | §5 (five classes; emission-eligibility model) |
| 4 | Epistemic truth boundary (proposed vs required vs supplied vs verified) | §4, §7, §9, §10, §13 |
| 5 | Provenance + confidence; UNDETERMINED where insufficient | §4, §6 |
| 6 | Deterministic, order-independent; organizational-only ordering | §8 |
| 7 | Deliverable-only; no session/app/persistence/domain/scoring | §2, §3, §10, §15 |
| 8 | No domain-pack / domain-registry dependency | §2, §3, §16 (guardrails) |
| 9 | Empty/blocked truthful outcomes; no fabricated step | §4 (`outcome`, `blocked_items`), §9 |
| 10 | Non-claim boundary (not feasible/safe/compliant/verified/market-ready) | §2, §7, §10, §13 |

## 19. Non-authorization boundary

This DESIGN authorizes no implementation contract, tests-first work, tests, source,
template change, product behavior change, persistence, domain work, roadmap change,
or anchor change. The next governed action after this design is independently
reviewed and (separately) merged is a separate INCREMENT 5 IMPLEMENTATION-CONTRACT
readiness/authorization decision — not automatic contract drafting, tests-first
work, or implementation. Every concrete name herein is a candidate, non-authoritative
until an owner-authorized implementation contract fixes it.
