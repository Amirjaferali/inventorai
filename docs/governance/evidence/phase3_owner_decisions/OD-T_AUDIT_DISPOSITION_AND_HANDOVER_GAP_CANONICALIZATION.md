# OD-T — Audit Disposition and Handover-Gap Canonicalization

**Type:** documentation-only owner decision (candidate). **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified prerequisite tip:** `7816bdaddd762c38e6fa8cbbf05b7de26022e306` (PR #326 merge).

---

## 0. Lifecycle status

`OD-T: CANDIDATE / NOT YET REVIEWED / NOT YET MERGED / NOT YET CLOSED.` It becomes an accepted
owner decision only through independent review → owner acceptance → normal merge → post-merge
verification. It grants **no** implementation authority.

## 1. Evidence and top-level verdict

Two independent historical audit reports are recorded here as **owner-reviewed planning
evidence** (not implementation authority). Top-level verdict:

```
B — MATERIAL CONFORMANCE WITH DOCUMENTATION DRIFT
```

- **Historical implementation:** MATERIALLY CONFORMING.
- **No D or E implementation-to-governance contradiction** was found.
- **Principal unresolved issue:** `HANDOVER-TO-REPOSITORY GAP: PRESENT — CANONICALIZATION REQUIRED`.

The audits are **not** evidence that the application must be rebuilt, and **must not** be used
to reopen workstreams that were correctly closed.

## 2. Disposition classes

Every item below is placed in exactly one class:
- **CONFORMING — DO NOT REOPEN;**
- **DOCUMENTATION-ONLY CORRECTION;**
- **OWNER DECISION;**
- **CANONICAL-PLAN AMENDMENT;**
- **FUTURE IMPLEMENTATION OBLIGATION (separately gated);**
- **ACCEPTED LIMITATION.**

## 3. DISC-001 … DISC-018 dispositions

| DISC | Subject | Class | Disposition | Phase | Impl. now |
|---|---|---|---|---|---|
| 001 | Approximate Concept Visualization | OWNER DECISION + CANONICAL-PLAN AMENDMENT | Owner carve-out + canonicalization (OD-U; MVP_SCOPE_FREEZE bounded allowance). No implementation. | 3 UX / 4-5 foundations / later WS | NONE |
| 002 | Email Delivery | OWNER DECISION | Canonical owner decision + phase allocation (OD-U). No implementation. | 3 UX / 4 / 5 | NONE |
| 003 | Direct Output Download | OWNER DECISION | Canonical named capability + phase allocation; distinct from FDC-001 JSON export (OD-U). | 3 UX / 4 | NONE |
| 004 | Legacy ILT-002 evidence routes | DOCUMENTATION-ONLY CORRECTION | Record as historical/non-product pending Phase 3B disposition; no deletion now. | 3B decides | NONE |
| 005 | `/tmp` transcript handling | ACCEPTED LIMITATION | Accepted; Phase 4 remediation; not concealed in Phase 3. | 4 | NONE |
| 006 | Latent domain packs marked active | ACCEPTED LIMITATION | Accepted current limitation. | 6 | NONE |
| 007 | 31 domain-registry test failures | ACCEPTED LIMITATION | Pre-existing recorded debt; Phase 6 or separately authorized bounded remediation. | 6 | NONE |
| 008 | Stale root documents | DOCUMENTATION-ONLY CORRECTION | Banner/register clarification (this candidate). | now | NONE |
| 009 | Dead code | FUTURE IMPLEMENTATION OBLIGATION | Future bounded hygiene candidate; no code change now. | later | NONE |
| 010 | Branch-name ambiguity | DOCUMENTATION-ONLY CORRECTION | Historical note only; no history rewrite. | now | NONE |
| 011 | Old root governance text | DOCUMENTATION-ONLY CORRECTION | Authority clarification/banner where supported. | now | NONE |
| 012 | Runtime certification | ACCEPTED LIMITATION | Accepted; separate optional verification gate. | separate | NONE |
| 013 | "idea" terminology | OWNER DECISION | Phase 3 design/copy input; later Phase 3F implementation; no global replacement of "invention". | 3 / 3F | NONE |
| 014 | Branding / dev secret | FUTURE IMPLEMENTATION OBLIGATION | Branding indirection Phase 3; production secret handling Phase 10. | 3 / 10 | NONE |
| 015 | IoT legacy schema | ACCEPTED LIMITATION | Phase 6 / Phase 9. | 6 / 9 | NONE |
| 016 | `replay_debug` stale | DOCUMENTATION-ONLY CORRECTION | Stale-register entry (raw output — register-only, no in-file banner). | now | NONE |
| 017 | GOVERNANCE_MODEL historical loop | DOCUMENTATION-ONLY CORRECTION | Bounded authority clarification (banner; not "entire file obsolete"). | now | NONE |
| 018 | No-Valid-RED depth (WS8/13/14/15) | OWNER DECISION | Do **not** reopen WS8/13/14/15; add unresolved design depth to Phase 3B/3C; WS17 remains separately authorized. | 3B / 3C | NONE |

No discrepancy is reclassified as resolved implementation.

## 4. Handover-to-repository gap register (record B)

Source status ∈ {committed; committed but partial; handover-only; chat-only owner decision;
not found}. All dispositions grant no implementation authority.

| Item | Source status | Owner disposition | Canonical phase | Dependencies | Impl. authority | Required later gate | Plan amendment? |
|---|---|---|---|---|---|---|---|
| Approximate Concept Visualization | chat-only owner decision | Canonicalize + carve-out (OD-U) | 3 UX / 4-5 / later WS | 4 persistence, 5 accounts, provider WS | NONE (LEVEL 1) | Phase 3 auth; later impl. WS | Yes |
| Direct Output Download | handover-only | Canonical named capability (OD-U) | 3 UX / 4 | 4 secure storage | NONE | Phase 3 gate; Phase 4 | Yes |
| Email Delivery | handover-only | Canonical named capability (OD-U) | 3 UX / 4 / 5 | 4 persistence, 5 accounts/verified email | NONE | Phase 3 gate; 4/5 | Yes |
| Project Technology Profile | committed but partial | Phase 3B specification item | 3B | domain foundation | NONE | 3B | Agenda |
| WS8 expressed-intent depth | committed but partial | Phase 3B/3C design depth (do not reopen WS8) | 3B/3C | — | NONE | 3B/3C | Agenda |
| WS13 non-specialist answer-support depth | committed but partial | Phase 3B/3C design depth (do not reopen WS13) | 3B/3C | — | NONE | 3B/3C | Agenda |
| WS14 follow-up/completion design depth | committed but partial | Phase 3B/3C design depth (do not reopen WS14) | 3B/3C | — | NONE | 3B/3C | Agenda |
| WS15 guidance-consolidation design depth | committed but partial | Phase 3B/3C design depth (do not reopen WS15) | 3B/3C | — | NONE | 3B/3C | Agenda |
| Legacy ILT-002 evidence routes | committed | Historical/non-product; 3B disposition (preserve/test-only/env-guard/retire) | 3B | — | NONE | 3B | No |
| Unbannered stale historical files | committed | Banner + register (this candidate) | now | — | NONE | — | No |
| Sponsor recognition / themes | committed (boundary OD-R-A) | Phase 3 design + separately authorized impl. | 3 / later | branding indirection | NONE | 3 gate | Agenda |
| Administrative notice | committed (boundary OD-R-B) | Phase 3 UX; 4/5 for per-user/version | 3 / 4 / 5 | persistence, accounts | NONE | 3 gate | Agenda |
| Privacy/trust communication | committed (boundary OD-R-C) | Phase 3 layered UX; Phase 10 legal wording | 3 / 10 | legal review | NONE | 3 gate / 10 | Agenda |
| Multi-domain identity UX | committed | Phase 3 honest UX; 6 foundation; 9 activation | 3 / 6 / 9 | domain foundation | NONE | 3/6/9 | Agenda |
| All phase-linked owner reminders | handover/chat | Carried into OWNER_DECISION_REGISTER + Phase 3B agenda | 3+ | — | NONE | per item | Agenda |

## 5. Preserved authority statements

```
HISTORICAL IMPLEMENTATION: MATERIALLY CONFORMING
PRODUCT: multi-domain and cross-domain idea-development platform
CURRENT EXPERIMENTAL MVP RUNTIME: Electronics/Electrical only
PRODUCT STATE: DEMO_READY_WITH_LIMITATIONS   PRODUCTION READY: NO   DEPLOYMENT AUTHORITY: NONE
MAIN: STALE / UNRECONCILED
PHASE 1: FORMALLY CLOSED   PHASE 2: FORMALLY CLOSED AND STATUS-SYNCHRONIZED
PHASE 3 IMPLEMENTATION: NOT AUTHORIZED
STRUCTURED TECHNICAL GUIDANCE: RESERVED / INACTIVE / NOT AUTHORIZED
DOMAIN EXPANSION: NOT AUTHORIZED
ACV IMPLEMENTATION: NOT AUTHORIZED   DIRECT OUTPUT DOWNLOAD IMPLEMENTATION: NOT AUTHORIZED   EMAIL DELIVERY IMPLEMENTATION: NOT AUTHORIZED
```

## 6. Authority granted

None operational. OD-T grants no UI, runtime, schema, database, prompt, AI, test, domain,
deployment, or main-reconciliation authority. It records dispositions and routes future work
to the correct separately-gated phases and to the Phase 3B agenda.
