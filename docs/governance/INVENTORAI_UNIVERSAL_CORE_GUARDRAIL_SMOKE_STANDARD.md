# InventorAI Universal Core Guardrail & Smoke Standard

**Document ID:** INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD
**Status:** CANDIDATE (authoritative only if/when the introducing candidate is
merged and post-merge verified)
**Introduced by:** P10-UG1 (Owner-authorized Universal Core Guardrail & Smoke
Framework workstream)
**Subordinate to:** `docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md`
(binding), the committed anchors, `ACTIVE_EXECUTION_ROADMAP.md`, and
`ACTIVE_INCREMENT_CONTRACT.md`. This standard weakens NO existing governance
rule, review requirement, hold, or authorization boundary.

## 1. Purpose

A durable, repository-enforced safety layer applicable to ALL future
candidates (technologies, capabilities, integrations, runtime/UI/security/
persistence/domain/product changes). It reduces repetitive review burden by
giving every candidate one fast, deterministic, composed check of the core
invariants — while preserving the governed review pipeline:

```
EVERY FUTURE CANDIDATE
  -> UNIVERSAL GUARDRAIL SMOKE
  -> GATE-SPECIFIC TESTS
  -> CREATOR GRILL
  -> RISK-BASED INDEPENDENT REVIEW (per the standing protocol §4/§5)
  -> OWNER EXACT-SHA ACCEPTANCE where governed
```

## 2. Scope and architecture

- **Guard inventory (machine-checkable):** `tests/universal_guardrail_manifest.py`
  — the single list of guards. Each guard COMPOSES already-existing canonical
  tests by pytest node id; it never duplicates their assertions.
- **Canonical execution command:**

  ```
  python scripts/run_universal_smoke.py
  ```

- **Self-protection:** `tests/test_p10_ug1_universal_guardrail_framework.py`
  runs inside the governed FULL suite and pins the blocking inventory, the
  collectability of every canonical guard test, the runner's output contract,
  and this document's structure.

## 3. Guard categories and blocking semantics

- **BLOCKING GUARD (`blocking: true`)** — a failing, erroring, skipped, or
  missing canonical test means the candidate MUST STOP:
  `UNIVERSAL GUARDRAIL SMOKE: BLOCK`, exit code 1. The report names the GUARD
  ID, the violated invariant, the canonical owner, the failing test(s), and
  whether the candidate must be corrected, redesigned, or separately
  authorized. Blocking guards are material invariant protections only.
- **NON-BLOCKING OBSERVATION (`blocking: false`)** — a failing canonical test
  is reported as `OBSERVATION` and the candidate may proceed to gate-specific
  review; it is never silently dropped. A MISSING observation test still
  BLOCKs (inventory integrity is always blocking).
- Cosmetic differences must not be classified BLOCK; material invariant
  failures must not be downgraded to observations. Reclassification in either
  direction is a governed framework change (§6).

## 4. The universal invariants (v1 inventory)

Authoritative definitions live in the manifest; summary:

| Guard | Invariant (summary) | Class |
|---|---|---|
| UG-CORE-01 | Deterministic progression / replay parity (deterministic Idea Maturity Engine — never silently a generic chatbot) | BLOCKING |
| UG-CORE-02 | Classifier word-boundary semantics + single canonical entry | BLOCKING |
| UG-CORE-03 | Mechanical real activation, consent-first REAL /start→Tier-1 E2E chain | BLOCKING |
| UG-CORE-04 | Electronics real activation baseline | BLOCKING |
| UG-CORE-05 | Domain-neutral engine seams | BLOCKING |
| UG-CORE-06 | IdeaState/FSM field stability | BLOCKING |
| UG-CORE-07 | Durable persist-before-acknowledge + restart survival + forged-POST fail-closed | BLOCKING |
| UG-CORE-08 | Reconstructed views read-only; no accidental writable resume | BLOCKING |
| UG-CORE-09 | Auth/ownership separation (non-owner / anonymous / sid-possession denied) | BLOCKING |
| UG-CORE-10 | Decision Workspace FDC-001 deterministic envelope | BLOCKING |
| UG-CORE-11 | EN/AR Tier-1 public-label truth; no raw pack-id leak; never-electronics fallback | BLOCKING |
| UG-CORE-12 | Canonical export determinism + preservation floor (Core → Canonical Output Model → Integration/Export → External Tools; no vendor coupling in core) | BLOCKING |
| UG-CORE-13 | Authoritative security headers + transport/input limits preserved | BLOCKING |
| UG-CORE-14 | No implicit paid activation; AI transfer path dormant; entitlement fail-closed | BLOCKING |
| UG-CORE-15 | No unauthorized domain activation (real support-state policy) | BLOCKING |
| UG-META-01 | The framework protects itself (inventory pin + collectability) | BLOCKING |
| UG-OBS-01 | CLI banner names real activated domains (user-facing copy) | OBSERVATION |

## 5. Prohibited interpretations

`UNIVERSAL GUARDRAIL SMOKE: PASS` means ONLY:

```
CORE INVARIANTS PRESERVED UNDER THIS SUITE
```

It must NOT be interpreted or reported as: secure; production ready; legally
compliant; PSRR complete; deployment approved; or bug-free. Smoke PASS cannot
imply PSRR completion, cannot authorize deployment, cannot activate paid
capability, cannot select a provider, and cannot close any legal/tax item —
all of those remain separately governed and unchanged by this standard.

## 6. Extension process (governed)

When a future capability introduces a genuinely new durable invariant, the
introducing candidate adds — in the SAME candidate — a manifest entry with:

```
GUARD ID / OWNER / INVARIANT / BLOCKING CONDITION / CANONICAL TEST /
RATIONALE / INTRODUCED BY GATE
```

and updates the pinned inventory in
`tests/test_p10_ug1_universal_guardrail_framework.py`. Removing a blocking
guard, weakening its assertion, marking it skipped, excluding it from the
runner, or changing BLOCK → observation is a governed modification of the
guardrail framework itself (HIGH-SENSITIVITY under §7) — never a routine
edit. The framework test fails the full suite on any un-governed removal or
downgrade; the runner independently BLOCKs on missing canonical tests.

## 7. Risk-based review escalation (subordinate to the standing protocol)

This section maps candidates onto the ALREADY-AUTHORITATIVE tiering of
`docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md` §4
(LEVEL/DEPTH model) and §5 (proportionate independent-review policy,
including formal separate-session independence). It creates no new tier and
removes no mandatory review.

- **HIGH-SENSITIVITY — INDEPENDENT REVIEW REQUIRED** (protocol LEVEL 1 /
  DEPTH 1–2): changes touching progression/scoring/FSM semantics;
  persistence/data integrity; auth/session/ownership; domain activation;
  domain classification; Decision Workspace decision semantics; canonical
  output/schema; security/privacy boundaries; reconstructed/resume behavior;
  external integrations with meaningful data transfer; commercial/payment
  activation; deployment/release controls; legal/tax-dependent runtime
  behavior; and ANY change to this guardrail framework itself.
- **LOWER-SENSITIVITY** (protocol DEPTH 3 — low-risk maintenance inside an
  active contract): documentation-only changes; isolated copy corrections;
  non-semantic test improvements; cosmetic UI changes — each with
  `UNIVERSAL GUARDRAIL SMOKE: PASS`. For these, the standing protocol already
  prescribes implementation → targeted verification → inclusion in the
  increment report, without a separate per-file independent review; the smoke
  suite strengthens that existing lighter path. It does not widen it.

**Current governance truth (recorded honestly):** the standing protocol
mandates independent review for LEVEL-1 changes and bounded independent
review for DEPTH-2 authorized increments; DEPTH-3 maintenance inside a
contract has a lighter path. Every gate this framework was born under also
carried a per-candidate Owner directive requiring Independent External
Review of the exact SHA + bundle; nothing in this standard alters those
directives. Any future re-tiering of what requires formal independent review
— for example, allowing `Universal Smoke + Gate-Specific Tests + Creator
Grill` to suffice for a class of candidates currently reviewed externally —
is: **PROPOSED FUTURE REVIEW-TIER AMENDMENT: OWNER DECISION REQUIRED.** This
standard does not enact it.

## 8. Relationship to other assurance layers

- **Gate-specific tests:** unchanged and still required — the smoke suite
  never substitutes for a gate's own RED→GREEN evidence.
- **Full suite:** unchanged and still required where gate policy requires it;
  the smoke selection is a strict subset of the governed full suite.
- **Creator Grill:** unchanged; runs after gate-specific tests.
- **Independent Review:** governed by the standing protocol §4/§5 and any
  per-candidate Owner directive; the smoke suite feeds it, never replaces it.
- **Owner exact-SHA acceptance:** unchanged where governed.
- **PSRR / deployment:** untouched; smoke output has no release semantics.

## 9. What the smoke suite intentionally does NOT cover

Full deliverable content correctness; full localization surface; full
Decision Workspace behavior; auth session lifecycle breadth; backup/restore
drills; dependency audits; performance; accessibility; anything requiring
network, providers, or credentials. Those remain owned by their gate-specific
and full-suite tests and by separately governed processes.
