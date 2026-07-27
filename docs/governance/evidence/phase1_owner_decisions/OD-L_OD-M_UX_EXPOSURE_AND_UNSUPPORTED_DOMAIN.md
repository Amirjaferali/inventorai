# Phase 1 — Owner Decisions OD-L and OD-M — UX Exposure and Unsupported-Domain Handling

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision IDs:** OD-L (Path N / Path T user exposure) and OD-M (unsupported-domain
user experience) — recorded together because both are Phase 3 truthful-exposure
decisions about what the product honestly presents as available.
**Scope:** documentation-only durable record of two linked accepted owner
decisions. **No runtime, UI, navigation, label, help, flow, gate, anchor, freeze,
ADR, schema, API, test, template, or export change. No Path T exposure. No domain
activation. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `e38ef3ef6183d56871693274bcfc3484848586ac`
(official tip after PR #296, which merged the OD-F/OD-G/OD-H increment).

---

## 1. Decision status

```
OD-L — OWNER DECISION ACCEPTED
OD-M — OWNER DECISION ACCEPTED
```

Both decisions **confirm existing honest runtime/UI behavior**; neither requires
or authorizes a runtime change. No other open owner decision is resolved, no
anchor/freeze/ADR is amended, CR-1 is not reclassified, and no downstream phase
is activated.

## 2. Accepted owner decisions (verbatim)

### OD-L — Path N / Path T User Exposure

> **OD-L — OWNER DECISION ACCEPTED**
>
> THE CURRENT USER-FACING PRODUCT EXPERIENCE SHALL EXPOSE PATH N ONLY. PATH T /
> FORM T SHALL REMAIN BLOCKED AND MUST NOT BE PRESENTED AS AVAILABLE, INTEGRATED,
> OR SUPPORTED UNTIL ITS SEPARATE GOVERNED GATE IS COMPLETED AND SEPARATELY
> AUTHORIZED.

Required meaning:
- The current user-facing experience targets the Path N lane only.
- Path N-only exposure does not mean Path N content is fully runtime-integrated.
- The existing `runtime_integrated=false` limitation remains explicitly
  preserved.
- Path N-designated sessions may continue to receive legacy content until the
  separately governed integration work is completed.
- Path T / FORM T remains blocked and unavailable to users.
- No route, label, navigation item, placeholder, help content, workflow,
  marketing statement, or product wording may imply that Path T is integrated.
- Path T may be referenced only as unavailable, future, blocked, or separately
  gated.
- No Path T implementation, integration, runtime exposure, or activation is
  authorized.
- Any future Path T exposure requires its own contract, implementation evidence,
  tests, independent review, owner acceptance, formal closure, and separate
  authorization.

### OD-M — Unsupported-Domain User Experience

> **OD-M — OWNER DECISION ACCEPTED**
>
> WHEN A USER SELECTS OR REQUESTS AN UNSUPPORTED OR INACTIVE TECHNOLOGY DOMAIN,
> THE PRODUCT MUST REJECT OR BLOCK THE REQUEST HONESTLY AND CLEARLY DISCLOSE THAT
> THE DOMAIN IS NOT CURRENTLY SUPPORTED. THE PRODUCT MUST NOT SIMULATE,
> MISREPRESENT, OR IMPLY SUPPORT FOR AN UNSUPPORTED OR INACTIVE DOMAIN.

Required meaning:
- The current MVP runtime remains Electronics/Electrical only.
- Unsupported or inactive domains must not be presented as available.
- Unsupported-domain requests must be rejected or blocked before session
  creation.
- The product must provide an understandable scope disclosure.
- The UX must distinguish: currently supported; unsupported; inactive/future;
  blocked pending authorization.
- Unsupported requests must not be silently redirected into Electronics/Electrical.
- The product must not fabricate domain-specific guidance, evaluation, evidence,
  readiness, or capability.
- Assignment of `electronics_electrical` after valid electronics confirmation is
  not an unsupported-domain redirect.
- CR-1 LOW remains recorded and unresolved; this increment does not resolve it.
- No production UI change, domain activation, domain pack, schema, workflow, API,
  or runtime implementation is authorized.

## 3. Distinguished status (must be read exactly)

```
CURRENT USER-FACING LANE:                 PATH N ONLY
PATH N CONTENT INTEGRATION:               INCOMPLETE
RUNTIME_INTEGRATED:                       FALSE (UNCHANGED BY THIS DECISION)
PATH T / FORM T:                          BLOCKED
PATH T USER EXPOSURE:                     NOT AUTHORIZED
UNSUPPORTED-DOMAIN UX:                     HONEST REJECT / BLOCK / DISCLOSE
UNSUPPORTED-DOMAIN SESSION CREATION:       PROHIBITED
SILENT REDIRECTION TO ELECTRONICS/ELECTRICAL: PROHIBITED
CURRENT MVP RUNTIME:                      ELECTRONICS/ELECTRICAL ONLY
CR-1:                                     LOW / RECORDED / UNRESOLVED / NOT REMEDIATED BY THIS INCREMENT
PHASE 2:                                  NOT STARTED — NOT AUTHORIZED
PHASE 3:                                  NOT STARTED — NOT AUTHORIZED
CURRENT IMPLEMENTATION AUTHORITY:         NONE
CURRENT DEPLOYMENT AUTHORITY:             NONE
```

## 4. Why OD-L and OD-M are recorded together

Both are Phase 3 truthful-exposure decisions: OD-L governs which lane the
product exposes (Path N only; Path T blocked); OD-M governs how the product
honestly handles requests outside the supported domain. Together they define the
product's honesty boundary — what is presented as available and what is honestly
refused. Recording them in one combined artifact keeps the linked decision
coherent and is the smallest durable increment. Each decision retains its own
identifier and status.

## 5. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register both were recorded only as
`RECOMMENDATION — NOT OWNER DECISION`:
- OD-L recommendation: "Path N only; keep Path T blocked."
- OD-M recommendation: "confirm reject/disclose."

This record now converts those recommendations into **accepted decisions**. The
closed Phase 0 registers are unchanged by this record.

## 6. Canonical evidence references (repository truth)

- `docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md` — Path N designated in
  Phase 1 but **not runtime-integrated** ("Phase 1 does NOT mean Path N is
  runtime-integrated / content is live / asks Path N questions"; Path
  N-designated sessions still receive legacy content); **"Phase 1 does NOT
  unblock FORM T."**
- `web/app.py` `/start` (L392–434) — unsupported/unknown domain →
  `UNSUPPORTED_DOMAIN_MESSAGE`, **no session**; conflicting supported domain
  without corroboration → `MECHANISM_GUIDANCE_MESSAGE`, no session; admitted
  electronics session → `state.domain = DOMAIN_CONFIRM_VALUE` (electronics only).
- `web/templates/index.html` — "Electronics and electrical ideas are currently
  supported … Currently supported: electronics and electrical ideas"; explicit
  `domain_confirm=electronics_electrical` checkbox.
- Plan §3.2 (6) — "Unsupported or inactive domains must not be presented as
  currently available."
- Freezes/ADR: `MVP_SCOPE_FREEZE.md`, `MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md`,
  `docs/adr/ADR-001-domain-assignment-and-multi-domain-strategy.md`,
  `docs/governance/DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B.md`.
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-L and OD-M entries.

## 7. Accepted interpretation

1. The product exposes the **Path N lane only**; **Path T / FORM T stays
   blocked** and must never be presented as available or integrated.
2. Path-N-only exposure is a statement about *which lane is exposed*, **not** a
   claim that Path N content is fully integrated; `runtime_integrated=false`
   remains true and preserved.
3. Requests for **unsupported or inactive domains** are **honestly rejected /
   blocked with clear disclosure, before session creation**, and are **never
   silently redirected** into Electronics/Electrical.
4. The runtime and UI already implement this honest behavior; these decisions
   **ratify** it and bind future work to preserve it.

## 8. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Expose Path T / FORM T now | FORM T is blocked (Path N anchor); exposure needs its own governed gate + evidence + review + authorization. |
| Claim Path N is fully runtime-integrated | False — anchor records `runtime_integrated=false`; would misrepresent product state. |
| Present unsupported domains as available / simulate them | Violates plan §3.2 (6) and product honesty; misleads users. |
| Silently route unsupported requests into Electronics/Electrical | Dishonest; would fabricate scope. Runtime already refuses pre-session. |
| Resolve CR-1 here | Out of scope; CR-1 is a Phase 2 documentation reconciliation item. |
| Edit runtime/UI/anchor/freeze to "align" | Not needed (behavior already matches) and out of scope; this is documentation-only. |

## 9. Current Path N exposure boundary

The user-facing experience targets the **Path N lane only**. Path N content
integration is incomplete; Path N-designated sessions may continue receiving
legacy content until separately governed integration work is completed.

## 10. Path N exposure vs Path N integration completeness (explicit distinction)

```
PATH N EXPOSURE:              the only exposed user lane (owner-ratified).
PATH N CONTENT INTEGRATION:   INCOMPLETE — runtime_integrated=false.
```

Exposing Path N only does **not** assert that Path N content is live or fully
integrated. The two are distinct; this decision addresses exposure, not
integration completeness.

## 11. Preserved `runtime_integrated=false` limitation

The `runtime_integrated=false` limitation recorded in
`PATH_N_CURRENT_EXECUTION_ANCHOR.md` remains **true and unchanged**. This record
does not alter, integrate, or complete Path N content, and does not amend the
anchor.

## 12. Current Path T / FORM T blocked state

Path T / FORM T is **blocked** and **not exposed anywhere** in the runtime or UI
(no route, template, label, or wording references it). It may be referenced only
as unavailable / future / blocked / separately gated. No Path T exposure is
authorized.

## 13. Unsupported-domain runtime behavior (as evidenced)

`/start` refuses unsupported/unknown domains with `UNSUPPORTED_DOMAIN_MESSAGE`
and creates **no session**; conflicting supported-domain input without
corroboration yields `MECHANISM_GUIDANCE_MESSAGE` with no session; only an
explicitly confirmed electronics request is admitted (then `state.domain =
electronics_electrical`). The UI discloses "Currently supported: electronics and
electrical ideas."

## 14. Confirmation — unsupported requests rejected before session creation

Unsupported-domain requests are **rejected/blocked before any session is
created** (no `SESSION_STORE` entry). This matches OD-M.

## 15. Confirmation — silent redirection prohibited

The product must not silently redirect an unsupported-domain request into
Electronics/Electrical. Assigning `electronics_electrical` **after valid
electronics confirmation** is a confirmed-domain admission, **not** an
unsupported-domain redirect.

## 16. Current Electronics/Electrical-only runtime boundary

```
CURRENT MVP RUNTIME: ELECTRONICS/ELECTRICAL ONLY
```

Unchanged by this record.

## 17. Satisfied OD-F prerequisite

OD-M depends on **OD-F** (multi-domain deferral / electronics-only runtime).
OD-F is **ACCEPTED and merged (PR #296)** — the prerequisite is **satisfied**.

## 18. Phase 3 future implementation ownership

Future UX implementation of these exposure rules is owned by **Phase 3 — Product
UX/UI Foundation** (brand-neutral shell; unsupported-domain states; truthful
temporary-session disclosures; Phase 3F bounded implementation increments).
Phase 3 remains **NOT STARTED / NOT AUTHORIZED**.

## 19. CR-1 preservation

```
CR-1: LOW — RECORDED — UNRESOLVED — NOT REMEDIATED BY THIS INCREMENT
```

CR-1 (latent multi-domain `infer_domain` vs electronics-only admission) remains a
recorded Phase 2 reconciliation item. This record neither resolves nor
reclassifies it.

## 20. What this record authorizes

- Recording OD-L and OD-M as accepted owner decisions (documentation only).
- The smallest plan status synchronization and one appended roadmap record.

## 21. What this record prohibits

- Modifying runtime code, UI, navigation, labels, help, placeholders, or flows.
- Exposing or integrating Path T / FORM T; changing Path N content integration;
  claiming Path N is fully integrated.
- Activating unsupported/inactive domains; modifying the unsupported-domain gate.
- Modifying APIs, schemas, tests, templates, exports, or runtime logic.
- Amending Path N / Path T anchors, MVP freezes, ADRs, or domain owner
  resolutions.
- Resolving or reclassifying CR-1.
- Modifying Phase 0 evidence, the OD-A…OD-H records, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-I, OD-J, OD-K, OD-N, OD-O, OD-P, or OD-Q.
- Activating Phase 2 or Phase 3.
- Any implementation or deployment authority.

## 22. Immediate effect

- Path-N-only exposure and honest unsupported-domain handling are owner-ratified
  and bind future work to preserve them.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No runtime, UI, or anchor
  change.

## 23. Deferred effect

- Any future **Path T exposure** requires its own governing contract,
  implementation evidence, tests, independent review, owner acceptance, formal
  closure, and separate authorization.
- **Path N content integration** and the **UX implementation** of these rules are
  deferred to their proper future phases (Path N integration work; Phase 3 for
  UX), under separate authorization.

## 24. Remaining owner decisions

`OD-I, OD-J, OD-K, OD-N, OD-O, OD-P, OD-Q` remain **OPEN and unresolved**.
**OD-A, OD-B, OD-C, OD-D, OD-E, OD-F, OD-G, OD-H** remain previously accepted and
merged and are **unchanged** by this record. Only OD-L and OD-M are decided here.

## 25. Implementation and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; Electronics/Electrical remains the
only current MVP runtime scope; the product is NOT PRODUCTION READY.

## 26. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It
is authoritative as a record of the owner's accepted OD-L and OD-M decisions once
independently reviewed, owner-accepted, merged, and post-merge verified. Its
authority is that of a decision record; it grants no implementation or deployment
authority. Path T stays blocked; Path N integration stays incomplete; the runtime
remains Electronics/Electrical only; CR-1 remains recorded and unresolved.
