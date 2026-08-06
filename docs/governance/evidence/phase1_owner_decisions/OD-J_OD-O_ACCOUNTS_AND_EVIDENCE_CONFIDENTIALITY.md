# Phase 1 — Owner Decisions OD-J and OD-O — Role Model and Evidence Confidentiality

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision IDs:** OD-J (account/project/contributor/claimed-inventor role model)
and OD-O (evidence confidentiality, sharing, and transcript lifecycle) — recorded
together because OD-O's access/sharing model rests on OD-J's role/permission
distinctions.
**Scope:** documentation-only durable record of two linked accepted owner
decisions. **No authentication, account, role, permission, sharing, persistence,
retention, deletion, audit, export, privacy, transcript, schema, API, UI, or
runtime change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `94b8518d2acdb61fd0aa15c838b2d23e39e2b290`
(official tip after PR #297, which merged the OD-L/OD-M increment).

---

## 1. Decision status

```
OD-J — OWNER DECISION ACCEPTED
OD-O — OWNER DECISION ACCEPTED
```

Both are forward-looking confirmation decisions that bind future Phase 4/Phase 5
implementation. No other open owner decision is resolved, no runtime/schema
changes, and no downstream phase is activated.

## 2. Accepted owner decisions (verbatim)

### OD-J — Account, Project, Contributor and Claimed-Inventor Role Model

> **OD-J — OWNER DECISION ACCEPTED**
>
> THE PRODUCT SHALL DISTINGUISH CLEARLY BETWEEN: (1) ACCOUNT HOLDER; (2) PROJECT
> OWNER OR PROJECT ADMINISTRATOR; (3) CONTRIBUTOR; (4) CLAIMED INVENTOR; (5)
> VIEWER OR OTHER AUTHORIZED COLLABORATOR. NO PRODUCT ROLE, PERMISSION, LABEL, OR
> RECORD SHALL BE REPRESENTED AS PROOF OF LEGAL OWNERSHIP, LEGAL INVENTORSHIP,
> ENTITLEMENT, OR PATENT RIGHTS.

Required meaning:
- An account represents an authenticated product identity, not legal ownership.
- A project owner or administrator controls product-level permissions and
  administration, not legal title to an invention.
- A project creator is not automatically the legal owner or inventor.
- A contributor may supply ideas, evidence, documents, analysis, or work without
  that role determining legal inventorship.
- A claimed inventor is a user-recorded claim or attribution, not a legal
  finding.
- A viewer, reviewer, expert, or collaborator receives only the permissions
  explicitly assigned.
- One person may hold multiple product roles where authorized.
- Multiple people may contribute to one project.
- Product roles must remain distinct from: legal ownership; legal inventorship;
  entitlement; patent rights; enforceability; filing rights.
- OD-E remains binding: the product may document claims and evidence but must not
  determine legal ownership, inventorship, or patentability.
- No authentication, account, role, permission, invitation, onboarding,
  access-control, or production implementation is authorized now.

### OD-O — Evidence Confidentiality, Sharing and Transcript Lifecycle

> **OD-O — OWNER DECISION ACCEPTED**
>
> PROJECTS, EVIDENCE, CONTRIBUTIONS, TRANSCRIPTS, AND OWNERSHIP OR INVENTORSHIP
> CLAIMS SHALL BE PRIVATE BY DEFAULT. ACCESS, SHARING, EXPORT, RETENTION,
> DELETION, AND DISCLOSURE MUST BE EXPLICIT, AUTHORIZED, AUDITABLE WHERE
> REQUIRED, AND GOVERNED BY THE ACCOUNT AND PROJECT PERMISSION MODEL.

Required meaning:
- New projects and their evidence are private by default.
- Transcripts are private by default.
- No project, evidence item, contribution, transcript, or claim becomes public
  merely because it exists.
- Access must be granted explicitly through governed permissions.
- Sharing must identify: authorized recipient; authorized scope; permitted
  action; duration or revocation condition where applicable.
- Product access must distinguish: viewing; contributing; reviewing;
  administering; exporting; sharing.
- Transcript and evidence lifecycle must eventually govern: collection; purpose;
  access; sharing; retention; deletion; export; audit history where required;
  revocation where technically and legally possible.
- Public links, anonymous access, broad workspace visibility, and external
  sharing must not be enabled or assumed by default.
- Exporting a copy must not silently change ownership, confidentiality,
  permission, inventorship, entitlement, or legal status.
- Privacy and confidentiality controls must not be represented as providing:
  legal privilege; patent secrecy guarantees; absolute security; absolute
  confidentiality.
- Current in-memory single-session behavior is not equivalent to a durable
  privacy or authorization system.
- Existing transcript and persistence limitations remain preserved.
- Durable privacy, persistence, role enforcement, retention, deletion, audit,
  and production access controls belong to their future governed phases.
- No account, permission, sharing, transcript, privacy, retention, deletion,
  export, audit, or access-control implementation is authorized now.

## 3. Distinguished status (must be read exactly)

```
ACCOUNT IDENTITY:                 PRODUCT IDENTITY ONLY / NOT LEGAL OWNERSHIP
PROJECT OWNER / ADMINISTRATOR:    PRODUCT ADMINISTRATION ROLE ONLY / NOT LEGAL OWNERSHIP
CONTRIBUTOR:                      PRODUCT CONTRIBUTION ROLE ONLY / NOT LEGAL INVENTORSHIP
CLAIMED INVENTOR:                 USER-RECORDED CLAIM / NOT A LEGAL FINDING
PROJECTS:                         PRIVATE BY DEFAULT
EVIDENCE:                         PRIVATE BY DEFAULT
TRANSCRIPTS:                      PRIVATE BY DEFAULT
EXPLICIT PERMISSION FOR ACCESS AND SHARING: REQUIRED
PUBLIC LINKS / ANONYMOUS ACCESS:  NOT ENABLED BY DEFAULT / NOT AUTHORIZED NOW
CURRENT ACCOUNT / AUTHENTICATION / AUTHORIZATION CAPABILITY: NOT IMPLEMENTED
CURRENT DURABLE PRIVACY ENFORCEMENT: NOT IMPLEMENTED
CURRENT PERSISTENCE:              IN-MEMORY / TEMPORARY / NON-PRODUCTION
RETENTION / DELETION / EXPORT / AUDIT LIFECYCLE: REQUIRED IN FUTURE / NOT IMPLEMENTED NOW
PHASE 4:                          NOT STARTED — NOT AUTHORIZED
PHASE 5:                          NOT STARTED — NOT AUTHORIZED
CURRENT IMPLEMENTATION AUTHORITY: NONE
CURRENT DEPLOYMENT AUTHORITY:     NONE
```

## 4. Why OD-J and OD-O are recorded together

OD-J defines *who* holds which product role and the hard boundary that no role is
legal ownership/inventorship; OD-O defines *what* may be accessed/shared and the
private-by-default rule governed by that role/permission model. OD-O's access and
sharing governance is meaningless without OD-J's roles; the two are inseparable.
Recording them in one combined artifact keeps the linked decision coherent and is
the smallest durable increment. Each decision retains its own identifier and
status.

## 5. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register both were recorded only as
`RECOMMENDATION — NOT OWNER DECISION`:
- OD-J recommendation: "confirm; role ≠ legal ownership."
- OD-O recommendation: "private-by-default + transcript lifecycle."

This record now converts those recommendations into **accepted decisions**. The
closed Phase 0 registers are unchanged by this record.

## 6. Canonical evidence references (repository truth)

- Plan Phase 5 L283–287 — "registration; sign-in; … roles; permissions; project
  ownership; contributors; reviewers; sharing; evidence access controls; …";
  **"Must distinguish: account owner, project owner, project creator,
  contributor, reviewer, expert, claimed inventor, and legal-owner claim"**;
  **"No role label may be treated as legal proof of ownership."**
- Plan §5A.2 L378–384 — sensitive invention information "must be treated as
  potentially confidential"; **"private-by-default project access."** Plan §5A.1
  L351 — "confidentiality of unpublished invention information."
- Plan Phase 4 (L277 ff.) — persistent storage; evidence/provenance/contribution/
  ownership-claims models; privacy-aware data lifecycle; retention; deletion;
  audit; migration from the in-memory model.
- Runtime reality: `web/app.py` `SESSION_STORE = {}` ("in-memory, non-production,
  temporary"; "no durable persistence"); per-session `"transcript": []`;
  `engine/idea_state.py` "no durable retention." No auth/account/role/permission
  routes; export route `/decision-workspace/<did>/export` is a local self-download
  of the user's own record.
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-J and OD-O entries (SPV Principle 1; SPV §11; WS16-IR-104 transcript, SP-2).
- Accepted dependencies: `OD-D_OD-E_EVIDENCE_REGISTER_AND_LEGAL_BOUNDARY.md`
  (OD-D and OD-E accepted, merged PR #295).

## 7. Accepted interpretation

1. The product will distinguish product roles (account holder, project
   owner/administrator, contributor, claimed inventor, viewer/collaborator) and
   **no role is legal ownership or inventorship** (OD-J).
2. Projects, evidence, contributions, transcripts, and claims are **private by
   default**; access/sharing/export/retention/deletion/disclosure are explicit,
   authorized, and governed by the role/permission model (OD-O).
3. These are **forward-looking rules** for future Phase 4/Phase 5 implementation;
   they do not describe or authorize present capabilities.
4. Current single-session in-memory behavior is **not** equivalent to a durable
   privacy or authorization system.

## 8. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Treat any product role as legal ownership/inventorship | Violates OD-E and plan L287; creates false legal assurance. |
| Make projects/evidence/transcripts public or default-open | Privacy/commercial-sensitivity risk (§5A.2); rejected. |
| Enable public links / anonymous access by default | Same privacy risk; must be explicit and governed. |
| Claim current in-memory behavior is a complete privacy system | False — no durable enforcement exists; would misrepresent product state. |
| Implement accounts/roles/privacy now | Out of scope; owned by Phase 5 (accounts/authz) and Phase 4 (durable data), both NOT STARTED. |
| Let export silently change ownership/confidentiality/legal status | Rejected — export is a copy, not a legal transfer. |

## 9. Current absence of real account / authentication / authorization capabilities

There is **no** authentication, registration, account, profile, logout, role,
permission, or access-control capability in the runtime (no such routes or code).
These are future Phase 5 capabilities.

## 10. Current single-session in-memory reality

Storage is `SESSION_STORE = {}` — **in-memory, temporary, non-production**, with
**no durable persistence**. Each session holds its own state and `transcript`
list; nothing is shared between sessions or users.

## 11. Current evidence and transcript behavior

Evidence and the ILT-002 transcript are held in the in-memory session with **no
durable retention**, no governed deletion, no audit lifecycle, and no sharing.
The export route produces a local **self-download** of the user's own decision
record.

## 12. Effective non-public behavior vs durable privacy enforcement (explicit distinction)

```
EFFECTIVE NON-PUBLIC BEHAVIOR:   nothing is published; single-session in-memory only.
DURABLE PRIVACY ENFORCEMENT:     NOT IMPLEMENTED — no accounts, permissions, retention, audit.
```

The absence of public-sharing functionality is **not** a complete privacy
architecture. OD-O's private-by-default rule is a forward requirement, not a
claim that durable privacy enforcement exists today.

## 13. Role boundaries (OD-J)

- **Account identity:** authenticated product identity only — not legal
  ownership.
- **Project owner / administrator:** product administration role only — not legal
  title.
- **Contributor:** product contribution role only — not legal inventorship.
- **Claimed inventor:** user-recorded claim/attribution — not a legal finding.
- **Viewer / reviewer / expert / collaborator:** only the permissions explicitly
  assigned.
- Product roles remain distinct from legal ownership, inventorship, entitlement,
  patent rights, enforceability, and filing rights.

## 14. Confidentiality and sharing rules (OD-O)

- **Private by default:** projects, evidence, contributions, transcripts, claims.
- **Governed sharing:** explicit recipient, scope, permitted action, and
  duration/revocation where applicable; access distinguishes viewing,
  contributing, reviewing, administering, exporting, sharing.
- **Export boundary:** a copy that does not silently change ownership,
  confidentiality, permission, inventorship, entitlement, or legal status.
- **Public links / anonymous access:** not enabled or assumed by default.

## 15. Transcript and evidence lifecycle requirements (future)

Must eventually govern collection, purpose, access, sharing, retention,
deletion, export, audit history (where required), and revocation (where
technically and legally possible). None is implemented now; owned by Phase 4/5.

## 16. Privacy and confidentiality disclaimer boundary

Privacy/confidentiality controls must not be represented as providing legal
privilege, patent secrecy guarantees, absolute security, or absolute
confidentiality.

## 17. OD-D and OD-E dependency status

**OD-D** (evidence/provenance/contribution/ownership-claims register) and
**OD-E** (legal boundary) are **ACCEPTED and merged (PR #295)** — dependencies
**satisfied**. OD-J's "role ≠ legal ownership" and OD-O's "claims are private
records, not findings" both rest on OD-E's binding legal boundary.

## 18. Phase 4 durable-data and lifecycle dependency (textually supported)

Plan **Phase 4 — Durable Data and Evidence Foundation** owns persistent storage,
the evidence/provenance/contribution/ownership-claims models, privacy-aware data
lifecycle, retention, deletion, audit, and migration from the in-memory model.
OD-O's durable privacy/retention/deletion/audit belongs to Phase 4 (proven, not
inferred). Phase 4 remains **NOT STARTED / NOT AUTHORIZED**.

## 19. Phase 5 accounts/authentication/authorization/sharing dependency (textually supported)

Plan **Phase 5 — Accounts, Authentication, Authorization and Sharing** owns
registration, sign-in, roles, permissions, project ownership, contributors,
reviewers, sharing, evidence access controls, and the role-vs-legal-ownership
distinction (L283–287). OD-J's role model and OD-O's governed access belong to
Phase 5 (proven, not inferred). Phase 5 remains **NOT STARTED / NOT AUTHORIZED**.

## 20. Current honest limitations (recorded, not resolved)

No real accounts; no authentication; no authorization; no role or permission
enforcement; no collaboration or sharing controls; no durable persistence; no
governed retention or deletion; no audit history; no revocation capability;
transcript lifecycle limitation (WS16-IR-104, SP-2); in-memory, temporary,
non-production storage; `DEMO_READY_WITH_LIMITATIONS`; NOT PRODUCTION READY. The
absence of public-sharing functionality is **not** equivalent to a complete
privacy architecture.

## 21. What this record authorizes

- Recording OD-J and OD-O as accepted owner decisions (documentation only).
- The smallest plan status synchronization and one appended roadmap record.

## 22. What this record prohibits

- Implementing authentication, registration, accounts, profile, logout,
  invitation, onboarding, or session identity.
- Implementing roles, permissions, access control, collaboration, sharing, public
  links, or anonymous access.
- Implementing durable persistence, retention, deletion, audit, revocation, or
  lifecycle enforcement.
- Modifying transcripts, evidence models, exports, APIs, schemas, UI, tests,
  templates, privacy notices, or legal wording.
- Claiming legal ownership, inventorship, entitlement, patentability, privilege,
  secrecy, or absolute security; or implying current in-memory behavior is a
  complete privacy system.
- Modifying Phase 0 evidence, the OD-A…OD-M records, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-I, OD-K, OD-N, OD-P, or OD-Q.
- Activating Phase 2, Phase 4, or Phase 5.
- Any implementation or deployment authority.

## 23. Immediate effect

- The role model (OD-J) and private-by-default confidentiality rule (OD-O) are
  owner-ratified and bind future Phase 4/Phase 5 implementation.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No runtime/schema/UI change.

## 24. Deferred effect

- **Accounts, authentication, authorization, roles, permissions, sharing** →
  Phase 5 under separate authorization.
- **Durable persistence, privacy enforcement, retention, deletion, audit,
  revocation, transcript/evidence lifecycle** → Phase 4 under separate
  authorization.

## 25. Remaining owner decisions

`OD-I, OD-K, OD-N, OD-P, OD-Q` remain **OPEN and unresolved**. **OD-A, OD-B,
OD-C, OD-D, OD-E, OD-F, OD-G, OD-H, OD-L, OD-M** remain previously accepted and
merged and are **unchanged** by this record. Only OD-J and OD-O are decided here.

## 26. Implementation and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; storage is in-memory / temporary /
non-production; the product is NOT PRODUCTION READY.

## 27. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It
is authoritative as a record of the owner's accepted OD-J and OD-O decisions once
independently reviewed, owner-accepted, merged, and post-merge verified. Its
authority is that of a decision record; it grants no implementation or deployment
authority. No accounts/auth/roles/permissions/sharing/persistence exist or are
implemented; no role is legal ownership/inventorship; private-by-default is a
forward requirement, not a claim of durable privacy enforcement.
