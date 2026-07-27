# Phase 1 — Owner Decisions OD-F, OD-G, OD-H — Multi-Domain, IoT, and Future-Domain Priority

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision IDs:** OD-F (multi-domain / cross-domain activation), OD-G (IoT as
domain and cross-domain capability), OD-H (future-domain priority order) —
recorded together because OD-G and OD-H are scoped by OD-F's deferral-and-design
frame.
**Scope:** documentation-only durable record of three linked accepted owner
decisions. **No implementation. No domain registry, domain pack, capability pack,
IoT/drone/renewable runtime, domain inference change, schema, API, test,
template, UI, or runtime change. No freeze/ADR amendment. No downstream
activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `48a389fdf78beb03d743c52cf0c32c6db4ade0d7`
(official tip after PR #295, which merged the OD-D/OD-E increment).

---

## 1. Decision status

```
OD-F — OWNER DECISION ACCEPTED
OD-G — OWNER DECISION ACCEPTED
OD-H — OWNER DECISION ACCEPTED
```

These three accepted owner decisions **defer and design-for**; they do not
activate. No other open owner decision is resolved, no freeze/ADR is amended,
and no downstream phase is activated.

## 2. Accepted owner decisions (verbatim)

### OD-F — Multi-Domain and Cross-Domain Activation

> **OD-F — OWNER DECISION ACCEPTED**
>
> MULTI-DOMAIN AND CROSS-DOMAIN RUNTIME ACTIVATION REMAINS DEFERRED. THE CURRENT
> MVP REMAINS ELECTRONICS/ELECTRICAL ONLY. THE PLATFORM MUST BE DESIGNED FOR
> FUTURE EXTENSIBILITY WITHOUT ACTIVATING UNSUPPORTED DOMAINS OR CROSS-DOMAIN
> EXECUTION NOW.

Required meaning:
- The current runtime remains Electronics/Electrical only.
- No additional technology domain is activated now.
- No cross-domain runtime execution is activated now.
- Existing domain freezes, safety boundaries, gates, tests, and benchmarks
  remain binding.
- Future extensibility must be supported through governed domain registries,
  domain packs, capability declarations, and explicit activation gates.
- Future implementation must avoid hard-coded core branching on domain names.
- Any runtime activation requires its proper future phase, domain-specific
  readiness evidence, tests, benchmarks, independent review, owner acceptance,
  formal closure, and separate owner authorization.

### OD-G — IoT Domain and Cross-Domain Capability

> **OD-G — OWNER DECISION ACCEPTED**
>
> IOT SHALL BE MODELED IN THE FUTURE AS BOTH: (1) A TECHNOLOGY DOMAIN; AND (2) A
> CROSS-DOMAIN CAPABILITY SPANNING ELECTRONICS, SENSORS, CONNECTIVITY, EMBEDDED
> SOFTWARE, CLOUD, DATA, AND CONTROL. NO IOT RUNTIME ACTIVATION IS AUTHORIZED
> NOW.

Required meaning:
- IoT must not be reduced to a shallow category label.
- IoT may own domain-specific knowledge, requirements, risks, workflows,
  evidence, tests, and guidance.
- IoT may also participate in projects whose primary domain is another
  technology area.
- Cross-domain relationships must be explicit and governed.
- No IoT registry pack, capability pack, schema, workflow, UI, runtime logic, or
  activation is authorized in this increment.

### OD-H — Future-Domain Priority Order

> **OD-H — OWNER DECISION ACCEPTED**
>
> THE CURRENT FUTURE-DOMAIN PRIORITY ORDER IS: 1. IOT; 2. DRONE AND UNMANNED
> SYSTEMS; 3. RENEWABLE-ENERGY TECHNOLOGIES; 4. OTHER OWNER-AUTHORIZED DOMAINS.
> THIS ORDER IS A PLANNING PRIORITY, NOT RUNTIME AUTHORIZATION.

Required meaning:
- The order guides future planning and sequencing only.
- It does not automatically activate any domain.
- Each future domain requires its own Owner Decision, contract, safety
  boundaries, domain pack, tests, benchmarks, independent review, owner
  acceptance, merge, and formal closure.
- The core platform must remain extensible so this sequence can be delivered
  without rebuilding the core.
- The owner may later amend the planning order through a separate governed
  decision without implying activation.

## 3. Distinguished status (must be read exactly)

```
CURRENT MVP RUNTIME:                ELECTRONICS/ELECTRICAL ONLY
MULTI-DOMAIN RUNTIME ACTIVATION:    DEFERRED
CROSS-DOMAIN RUNTIME ACTIVATION:    DEFERRED
DESIGN FOR FUTURE EXTENSIBILITY:    OWNER-APPROVED
IOT FUTURE DOMAIN MODEL:            OWNER-APPROVED
IOT CROSS-DOMAIN CAPABILITY MODEL:  OWNER-APPROVED
IOT RUNTIME ACTIVATION:             NOT AUTHORIZED
FUTURE-DOMAIN PRIORITY ORDER:       OWNER-APPROVED FOR PLANNING ONLY
PHASE 6:                            NOT STARTED — NOT AUTHORIZED
PHASE 9:                            NOT STARTED — NOT AUTHORIZED
CURRENT IMPLEMENTATION AUTHORITY:   NONE
CURRENT DEPLOYMENT AUTHORITY:       NONE
```

## 4. Why OD-F, OD-G, and OD-H are recorded together

The three decisions form one coherent domain-strategy frame: OD-F sets the
deferral-and-design boundary (electronics-only runtime; extensibility approved,
activation deferred); OD-G scopes IoT's future dual role within that frame; OD-H
records the planning-only priority order for future domains. Recording them in
one combined artifact keeps the linked decision coherent and is the smallest
durable increment. Each decision retains its own identifier and status.

## 5. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register all three were recorded only as
`RECOMMENDATION — NOT OWNER DECISION`:
- OD-F recommendation: "keep deferred; design-for extensibility only."
- OD-G recommendation: "dual model; no shallow category."
- OD-H recommendation: "confirm as listed."

This record now converts those recommendations into **accepted decisions**. The
closed Phase 0 registers are unchanged by this record.

## 6. Canonical evidence references (repository truth)

- Plan §3.2 L1–6 — Electronics/Electrical is "only … the initial experimental
  MVP scope," "not the permanent product boundary"; long-term must support
  multiple domains and cross-domain inventions "without rebuilding or hard-coding
  the core"; "Unsupported or inactive domains must not be presented as currently
  available."
- Plan L120 — "Multi-domain registry/pack concepts exist, but future domain
  activation is separately gated."
- Plan §3.4 L157–161 — "IoT is both a selectable future technology domain and a
  cross-domain capability … must not be implemented as a single shallow category
  or as hard-coded core branching."
- Plan §9 Phase 9 L327–330 — priority candidates "1. IoT; 2. drone and unmanned
  systems; 3. renewable energy; 4. other owner-authorized domains"; "No domain
  is activated merely because it appears in the registry or UI design."
- Plan Phase 6 — Domain Registry, Technology Capability Registry, domain-pack /
  capability-pack contracts, cross-domain project model, "no core branching on
  domain names."
- Freezes / ADR: `MVP_SCOPE_FREEZE.md` (electronics/electrical-only; multi-domain
  OUT OF SCOPE — FROZEN); `docs/adr/ADR-001-domain-assignment-and-multi-domain-strategy.md`
  (multi-domain deferred); `docs/governance/DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B.md`
  (preserve infrastructure, restrict runtime to electronics until separately
  authorized). CR-1 (LOW) — latent `infer_domain` vs electronics-only `/start`.
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-F, OD-G, OD-H entries (SPV Principle 3; PLAN §3.2 / §3.4 / §3.3 / §9).

## 7. Accepted interpretation

1. The current runtime stays **Electronics/Electrical only**; multi-domain and
   cross-domain runtime execution remain **deferred**.
2. The platform is **owner-approved to be designed for extensibility** — through
   governed domain registries, domain packs, capability declarations, and
   explicit activation gates, with no hard-coded core branching on domain names.
3. **IoT** is owner-approved to be modeled in the future as **both** a technology
   domain **and** a cross-domain capability; no IoT runtime is authorized now.
4. The **future-domain priority order** (IoT → drone and unmanned systems →
   renewable-energy technologies → other owner-authorized domains) is
   owner-approved **for planning only**; it activates nothing.

## 8. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Activate multi-domain / cross-domain runtime now | Contradicts the MVP scope freeze and ADR-001; requires freeze amendment + replacement ADR + gates + tests + benchmark + separate authorization; scope/safety risk. |
| Present unsupported/inactive domains as available | Violates plan §3.2 (6); misleads users. |
| Model IoT as a shallow single category / hard-coded branch | Violates plan §3.4 L161. |
| Reorder or omit the future-domain priority | Owner selected the listed order; reordering is a separate governed decision. |
| Amend freezes/ADRs in this record | Out of scope; freeze/ADR amendment is a governed, separately-authorized act. |
| Edit closed Phase 0 registers or merged OD records | Append-only / previously merged; a new Phase 1 record is the correct location. |

## 9. Current runtime boundary

```
CURRENT MVP RUNTIME: ELECTRONICS/ELECTRICAL ONLY
```

The active `/start` gate admits only electronics_electrical sessions; this record
changes no runtime, gate, inference, or assignment logic.

## 10. Design-for-extensibility boundary (recorded, non-activating)

Future extensibility must be delivered through governed domain registries, domain
packs, capability declarations, and explicit activation gates, avoiding
hard-coded core branching on domain names. This is a recorded forward constraint;
it authorizes no implementation.

## 11. Distinction between planning, foundation, and activation

```
PLANNING:    priority order and sequencing (OD-H) — authorizes nothing to run.
FOUNDATION:  extensibility scaffolding — owned by Phase 6 (NOT STARTED).
ACTIVATION:  making a domain live — owned by Phase 9 (NOT STARTED), per domain.
```

An item's presence in planning or foundation is never activation.

## 12. IoT domain role

IoT may own domain-specific knowledge, requirements, risks, workflows, evidence,
tests, and guidance — as a future selectable technology domain. Not implemented
here.

## 13. IoT cross-domain capability role

IoT may also participate in projects whose primary domain is another technology
area, spanning electronics, sensors, connectivity, embedded software, cloud,
data, and control. Cross-domain relationships must be explicit and governed. Not
implemented here.

## 14. Future-domain priority order

```
1. IOT
2. DRONE AND UNMANNED SYSTEMS
3. RENEWABLE-ENERGY TECHNOLOGIES
4. OTHER OWNER-AUTHORIZED DOMAINS
```

Planning priority only; no activation. Amendable later by a separate governed
decision.

## 15. Phase 6 foundation dependency (textually supported)

Plan Phase 6 — Multi-Domain and Technology Capability Foundation — owns the
Domain Registry, Technology Capability Registry, domain-pack / capability-pack
contracts, cross-domain project model, and "no core branching on domain names."
The extensibility foundation is therefore assigned to Phase 6 (proven, not
inferred). Phase 6 remains **NOT STARTED / NOT AUTHORIZED**.

## 16. Phase 9 activation dependency (textually supported)

Plan Phase 9 — Domain Activation Workstreams — owns per-domain activation, each
requiring Owner Decision, domain contract, safety boundaries, tests, benchmarks,
representative journeys, independent review, owner acceptance, merge, post-merge
verification, and formal closure. Domain activation is therefore assigned to
Phase 9 (proven, not inferred). Phase 9 remains **NOT STARTED / NOT AUTHORIZED**.

## 17. Preserved freezes and ADR boundaries

`MVP_SCOPE_FREEZE.md`, `MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md`,
`docs/adr/ADR-001-domain-assignment-and-multi-domain-strategy.md`, and
`docs/governance/DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B.md` remain **binding and
unchanged**. CR-1 (LOW) remains a recorded Phase 2 reconciliation item and is not
activated or resolved here.

## 18. What this record authorizes

- Recording OD-F, OD-G, and OD-H as accepted owner decisions (documentation
  only).
- The smallest plan status synchronization and one appended roadmap record.

## 19. What this record prohibits

- Implementing or modifying domain registries, domain packs, or capability packs.
- Activating multi-domain or cross-domain execution.
- Adding IoT, drone, renewable-energy, or other runtime behavior.
- Modifying domain inference or domain assignment logic, or the electronics-only
  runtime gate.
- Modifying APIs, schemas, tests, templates, exports, UI, or runtime code.
- Amending MVP scope freezes, ADRs, or domain-resolution records.
- Modifying Phase 0 evidence, the OD-A…OD-E records, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-I…OD-Q.
- Activating Phase 2, Phase 6, or Phase 9.
- Any implementation or deployment authority.

## 20. Immediate effect

- The domain-strategy frame (deferral + design-for-extensibility + IoT dual model
  + planning-only priority) is owner-accepted and governs future design intent.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No runtime, gate, registry,
  or pack changes.

## 21. Deferred effect

- **Extensibility foundation** (registries, packs, contracts) is deferred to
  Phase 6 under separate authorization.
- **Per-domain activation** (IoT first, then the priority order) is deferred to
  Phase 9 under separate per-domain authorization with full readiness evidence.

## 22. Remaining owner decisions

`OD-I, OD-J, OD-K, OD-L, OD-M, OD-N, OD-O, OD-P, OD-Q` remain **OPEN and
unresolved**. **OD-A, OD-B, OD-C, OD-D, OD-E** remain previously accepted and
merged and are **unchanged** by this record. Only OD-F, OD-G, OD-H are decided
here.

## 23. Implementation and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; Electronics/Electrical remains the
only current MVP runtime scope; the product is NOT PRODUCTION READY.

## 24. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It
is authoritative as a record of the owner's accepted OD-F, OD-G, and OD-H
decisions once independently reviewed, owner-accepted, merged, and post-merge
verified. Its authority is that of a decision record; it grants no implementation
or deployment authority. No domain is activated; no freeze or ADR is amended; the
runtime remains Electronics/Electrical only.
