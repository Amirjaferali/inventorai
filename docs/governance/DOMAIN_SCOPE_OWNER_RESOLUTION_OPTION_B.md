# DOMAIN-SCOPE OWNER RESOLUTION — OPTION B

## 1. Record identity

```text
Status: OWNER DECISION — IMPLEMENTATION NOT YET AUTHORIZED
Record type: Domain-scope owner resolution
Selected option: B
Product behavior changed by this record: No
Repository implementation authorized by this record: No
Governance decision recorded: Yes
```

This record documents an owner strategic decision. It records a direction; it
does not implement it. It is read against true remote `main`
`0878ab6807a3d91dc5582260f9c401887a9f04dd`.

---

## 2. Decision

```text
The owner selects Option B:

Preserve the multi-domain registry infrastructure and domain packs, while
restricting currently authorized generic product-runtime activation to
electronics/electrical until non-electronics runtime use is separately and
explicitly authorized.
```

---

## 3. Decision rationale

Option B is selected because it:

- restores alignment with the active electronics/electrical scope freeze;
- preserves legitimate future cross-domain architecture;
- avoids silently ratifying unauthorized multi-domain behavior;
- avoids destructively removing domain packs or registry infrastructure;
- creates a reversible and narrowly bounded compliance path;
- separates infrastructure capability from product-runtime activation.

---

## 4. Meaning of "preserve infrastructure"

The following are NOT ordered for deletion or architectural rollback:

```text
engine/domain_registry.py
the v1.0 domain-pack schema
electronics_electrical
mechanical
medical_device
software
registry accessors and infrastructure
```

Preservation does not authorize current product use of every pack. The
infrastructure may remain installed; product-runtime activation of
non-electronics packs remains unauthorized.

---

## 5. Meaning of "restrict runtime activation"

Current product-runtime behavior must eventually ensure that:

- generic user entry cannot activate a non-electronics domain without separate
  authority;
- electronics/electrical remains the only currently authorized product domain;
- governed ILT-002 and Path N routes remain electronics/electrical;
- no non-electronics domain is presented as currently authorized product
  behavior;
- infrastructure may remain installed but unavailable for unauthorized
  activation.

The technical mechanism is not prescribed here. This record specifically does
NOT preselect any of:

- hardcoded routing;
- a feature flag;
- an allowlist;
- removal of inference;
- domain-pack unloading;
- UI removal.

Those choices belong to the later implementation-planning assessment.

---

## 6. Relationship to the inconsistency report

This resolution answers the owner decision gate of:

```text
docs/governance/DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md
```

It answers that decision gate by selecting Option B. The inconsistency is
strategically resolved by the owner, but remains technically unresolved until a
separately authorized implementation is merged and verified.

---

## 7. Relationship to binding scope and product vision

- `MVP_SCOPE_FREEZE.md` remains binding for current product runtime.
- electronics/electrical remains the authorized current scope.
- the long-term cross-domain idea-development vision remains preserved.
- this decision does not permanently prohibit future domains.
- future non-electronics activation requires explicit authority, governance
  criteria, testing, and roadmap admission where applicable.

---

## 8. Test-suite disposition

- No immediate change to `tests/test_domain_registry.py` is authorized.
- The 31 failures remain a known legacy-contract issue.
- Tests must not be migrated in a way that ratifies current multi-domain
  runtime activation.
- Test disposition must follow the approved implementation design.
- Loader/infrastructure tests may later be separated from product-scope
  assertions.
- CI remains deferred until the domain-scope implementation and test contract
  are resolved.

---

## 9. Required next gate

The next permitted action after this record becomes active is:

```text
A read-only implementation-planning assessment for the narrowest reversible
method of restricting generic runtime activation to electronics/electrical
while preserving the multi-domain infrastructure.
```

That assessment must compare at least:

- domain allowlist at the product boundary;
- feature-gated non-electronics activation;
- route-level restriction;
- inference-result filtering or fallback;
- separation of infrastructure tests from product-scope tests.

It must not implement anything.

---

## 10. Explicit non-authorization

This record does not authorize:

- editing `/start`;
- editing `infer_domain`;
- changing domain loading;
- deleting or modifying domain packs;
- changing questions or assessment rules;
- changing tests;
- adding xfail or deleting tests;
- adding CI;
- amending the scope freeze;
- replacing ADR-001;
- updating the roadmap;
- Phase 5 or Phase 6;
- Stage 3 evidence work;
- any implementation, commit, push, PR, or deployment beyond this record's own
  governed admission process.

---

## 11. Preserved governance states

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

## 12. Decision boundary

```text
OWNER OPTION B SELECTED

STRATEGIC DIRECTION:
Preserve multi-domain infrastructure.
Restrict current generic product-runtime activation to electronics/electrical.

IMPLEMENTATION STATUS:
NOT AUTHORIZED

NEXT GATE:
Read-only implementation-planning assessment, followed by separate
exact-scope owner authorization.
```
