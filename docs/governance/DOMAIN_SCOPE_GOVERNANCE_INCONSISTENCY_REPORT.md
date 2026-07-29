# DOMAIN-SCOPE GOVERNANCE INCONSISTENCY REPORT

> **STATUS: HISTORICAL — MISLEADING IF READ AS CURRENT / SUPERSEDED (Phase 2 Increment 3).**
> This report is historical and must not be read as current governance truth. Its
> `Status: DRAFT — OWNER RESOLUTION REQUIRED` header and its core claim that the
> generic `/start` route "calls `infer_domain(idea_text)` and assigns the result to
> `state.domain`" so that "a user may be routed into the `mechanical`,
> `medical_device`, or `software` domain" are **SUPERSEDED**: the current runtime
> admits only electronics/electrical sessions. The current runtime truth is
> `web/app.py` — `DOMAIN_CONFIRM_VALUE = "electronics_electrical"`, the `/start`
> route requires an explicit electronics-electrical confirmation and otherwise
> returns `UNSUPPORTED_DOMAIN_MESSAGE` with no session, and on admission sets
> `state.domain = DOMAIN_CONFIRM_VALUE` (always electronics_electrical). See
> `docs/governance/evidence/phase0_evidence_lock/CONFLICT_REGISTER.md` (CR-1) and
> `docs/governance/evidence/phase0_evidence_lock/STALE_DOCUMENT_REGISTER.md` (SD-2).
> The governing authority for current phasing and status is the canonical
> `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`
> and `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`. This increment defines no new
> architecture and changes no runtime behavior. The full reconciliation is
> `docs/governance/evidence/phase2_governance_corrections/P2I3_STALE_DOMAIN_SCOPE_REPORT_SUPERSESSION.md`.
> The body below is preserved unchanged as history.

## 1. Record identity

```text
Status: DRAFT — OWNER RESOLUTION REQUIRED
Record type: Governance inconsistency report
Product behavior changed by this report: No
Governance state changed by this report: No
Implementation authorization created: No
```

This is a neutral, evidence-based governance report. It records an
unresolved inconsistency for owner decision. It carries no authority beyond
documentation, changes no governance state, and authorizes no repository
write. It is read against true remote `main`
`c6b71fcab08e154303fc8f3d9daed192b5df1905`.

---

## 2. Executive finding

```text
The repository contains an unresolved inconsistency between binding
electronics/electrical-only product-scope authority and active generic
runtime routing into multiple non-electronics domains.
```

This finding is explicitly:

- **not** merely a failing-test issue;
- **not** proof that multi-domain infrastructure is inherently wrong;
- **not** authorization to remove, restrict, or activate anything;
- **not** a STOP declaration.

It identifies a conflict between two layers of committed evidence — binding
product-scope authority and the current live runtime — and refers that
conflict to the owner.

---

## 3. Binding scope authority

The following committed documents constitute the binding scope authority. No
document below is treated as superseded; none is contradicted by a committed
freeze amendment or replacement ADR.

- `MVP_SCOPE_FREEZE.md` (ACTIVE FREEZE; authority rank 1): IN SCOPE is
  "Domain: electronics/electrical inference only"; OUT OF SCOPE — FROZEN
  includes "Multi-domain orchestration" and "Medical / legal / automotive /
  regulatory engines".
- `docs/governance/MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md`: amends
  the freeze only to admit Functional Path N (non-specialist question
  content). It does not amend domain scope. "The freeze remains active for
  everything else." "Anything not explicitly listed as included is outside
  this amendment. Ambiguity resolves toward the freeze, not toward
  expansion."
- `docs/adr/ADR-001-domain-assignment-and-multi-domain-strategy.md`
  (Accepted): "Step 4 wiring is frozen. engine/domain_registry.py will not be
  imported by or wired into any engine runtime component until the conditions
  in Section 6 are met and explicit owner approval is granted."
  "Signal-based automatic domain classification is not approved." "Multi-domain
  support is deferred indefinitely." Section 5 forbids "Importing
  domain_registry in engine/domain_rules.py, engine/progression_loop.py, or
  web/app.py." Supersession requires "a replacement ADR approved by the
  project owner".
- `docs/governance/DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md` (Level 1 Authority):
  "No domain pack may be activated until AB-001 and AB-005 are formally
  resolved, implemented, and validated against the benchmark." Section 7
  activation gates are NOT MET, including "Owner explicit authorization". A
  coverage declaration "does not authorize multi-domain reasoning".
- `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md` (Level 0, EFFECTIVE):
  names the product a "governed idea-development and cross-domain invention
  orchestration platform" and keeps the "multi-domain integration vision"
  binding as long-term vision; but §12 states it does "not Authorize domain
  expansion" and does "not Modify runtime behavior", and preserves Phase 5 as
  UNAUTHORIZED.

Net binding position: current authorized product scope is electronics/
electrical only; multi-domain product-runtime activation is not authorized.

---

## 4. Contradictory implementation lineage

The following committed implementation history runs contrary to the binding
position above and must be weighed by the owner:

- `docs/governance/AB-006_FINAL_CLOSURE_RECORD.md` records CLOSED migration of
  rule authority to the registry for four domains (electronics_electrical,
  mechanical, medical_device, software), and the introduction of registry
  accessors owned by `domain_rules.py`.
- `engine/domain_rules.py` imports and loads the registry at import time.
- This may represent authorized infrastructure / observability work
  (AB-005/AB-006 architecture cleanup), not necessarily a deliberate scope
  expansion.
- AB-006 is a closure record. It is not a freeze amendment and not a
  replacement ADR; it does not claim to amend `MVP_SCOPE_FREEZE.md` or
  supersede ADR-001.
- Code comments and implementation history do not outrank binding governance
  authority.

Note: all governance and engine files in reachable history share a single
squash-import commit, so commit ordering cannot establish authored sequence;
document header dates are the only sequencing signal and are reported as such.

---

## 5. Actual runtime exposure

Observed read-only facts at `c6b71fca`:

- v1.0 domain packs exist for: `electronics_electrical`, `mechanical`,
  `medical_device`, `software`.
- Legacy `iot_electronics` (no `schema_version`) is skipped at load with a
  warning.
- `engine/domain_rules.py` executes `load_registry("domains/")` at import
  time, loading the four v1.0 packs.
- The generic `/start` route in `web/app.py` calls
  `infer_domain(idea_text)` and assigns the result to `state.domain`.
- Through that route, a user may be routed into the `mechanical`,
  `medical_device`, or `software` domain.
- The selected domain affects question selection (`get_question`) and
  response assessment (`assess_response`).
- No feature flag or authorization gate prevents non-electronics routing on
  the generic route.
- The governed ILT-002 and Path N routes
  (`/start_ilt002_water_leak`, `/start_ilt002_combination_lock`,
  `/start_ilt002_combination_lock_path_n`) remain pinned to
  `electronics_electrical`.

This report describes committed code paths only. It makes no claim about
deployment, production use, or any live incident.

---

## 6. Test-suite implication

- The 31 failures in `tests/test_domain_registry.py` encode a legacy
  contract (registry keyed by `capability_id`, expecting `iot_electronics`).
- Technically, those tests are stale relative to the current v1.0 pack_id /
  schema_version implementation.
- Updating the tests now would implicitly ratify the contested multi-domain
  runtime scope.
- Reverting the implementation merely to satisfy the legacy tests could break
  the live runtime path, which depends on the registry accessors and
  `infer_domain`.
- Therefore neither a test correction nor an implementation correction is
  currently authorized.

---

## 7. Exact inconsistency classification

```text
PRIMARY CLASSIFICATION:
Binding scope authority and active runtime behavior are inconsistent.

SECONDARY QUALIFICATION:
Multi-domain registry infrastructure may have been intentionally authorized,
but current product-runtime activation was not formally authorized by a
freeze amendment or replacement ADR.
```

Confidence:

```text
High:
electronics-only authority remains binding.

High:
generic `/start` can route into non-electronics domains.

Medium:
whether AB-005/AB-006 were intended to amend product scope.
```

---

## 8. Owner resolution options

These three strategic options are presented without selection.

### Option A — Formalize multi-domain runtime authorization

Would require, at minimum:

- explicit owner scope decision;
- freeze amendment;
- replacement or superseding ADR;
- activation criteria;
- test-contract migration;
- later roadmap admission if applicable.

This option changes current authorized product scope.

### Option B — Preserve infrastructure but restrict product runtime

Would retain the domain packs and registry infrastructure but prevent generic
runtime routing into non-electronics domains until separately authorized.

This is likely the narrowest compliance-restoration path. No implementation is
authorized by this report.

### Option C — Restore full electronics-only implementation

Would remove or disconnect multi-domain runtime behavior more broadly.

This carries the greatest risk of discarding legitimate future architecture
and is not recommended without stronger owner intent.

---

## 9. Management recommendation

```text
Preserve the multi-domain infrastructure.
Do not ratify multi-domain product runtime through test updates.
Do not remove the architecture.
The next owner decision should determine whether to:

1. formally authorize multi-domain runtime, or
2. temporarily restrict generic runtime activation to electronics/electrical.
```

The recommended immediate technical posture is no implementation until the
owner resolution is committed.

---

## 10. Preserved governance states

```text
R2 = HELD
FORM T = BLOCKED
Path T = BLOCKED
S-6 = UNCLASSIFIED
AA-3 = BLOCKED
AA-4 = BLOCKED
AA-5 = BLOCKED
Phase 5 = UNAUTHORIZED
Phase 6 = UNAUTHORIZED
ILT-002 evidence collection = NOT AUTHORIZED
AA-4 final S-6 classification has NOT been performed.
```

---

## 11. Explicit non-authorization

This report does not authorize:

- domain expansion;
- domain restriction implementation;
- runtime route changes;
- domain-pack changes;
- test migration;
- test removal or xfail;
- CI;
- roadmap synchronization;
- freeze amendment;
- ADR replacement;
- Stage 3 evidence work;
- Phase 5 or Phase 6;
- any downstream repository write.

---

## 12. Decision gate

```text
OWNER DECISION REQUIRED BEFORE ANY CODE OR TEST CHANGE

Required owner choice:

A. Authorize formal multi-domain runtime scope.
B. Preserve infrastructure but restrict current runtime to electronics/electrical.
C. Retain current state temporarily with an explicit unresolved-risk acceptance.
```

No option has been selected. This report records the inconsistency only and
awaits the owner's decision.
