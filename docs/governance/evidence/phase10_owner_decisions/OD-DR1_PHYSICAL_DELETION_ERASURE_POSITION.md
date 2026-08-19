# Phase 10 — Owner Decision OD-DR1 — Physical Deletion / Erasure Product Position

**Phase:** Phase 10 — Commercial, Legal, Security and Operational Readiness, under the authoritative
`docs/governance/P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md` (merged PR #514) which registered
OD-DR1 as unresolved.
**Decision ID:** OD-DR1 (physical deletion / erasure product position).
**Scope:** documentation-only durable record of one Owner decision accepted **at strategy level**. **No
implementation. No deletion capability, retention logic, runtime, schema, or test change. No downstream
activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified authoritative base at authoring:** `f35a399960b131e79f390c8eff2a6e95b29726a0` (PR #515 merge —
OD-J1/OD-J2 acceptance, authoritative; parents `022e5b75…` + `aed0cdf2…`, merge tree `25d839f0…` equal to the
accepted candidate tree — independently re-verified at authoring).

---

## 1. Decision status

```
OD-DR1 — OWNER DECISION ACCEPTED AT STRATEGY LEVEL
```

**Current authorized account-exit capability remains: `Account Deactivation` (P10-D3b, authoritative).**
Account Deactivation is NOT physical deletion or erasure — it changes one status column, stamps `deleted_at`,
and retains every durable row (all re-verified at the base: the only `DELETE FROM` in `engine/` remains
rate-limit cleanup).

**Physical deletion / erasure is: `DEFERRED PENDING EXTERNAL LEGAL DETERMINATION AND SEPARATE OWNER
AUTHORIZATION`.** No physical-deletion implementation is authorized now. No current data-retention behavior is
changed by this decision.

---

## 2. Future deletion capability — principles only (NOT authorization)

If physical deletion / erasure is later authorized through a separate governance gate, the future capability
should, **where legally and operationally appropriate**, support:

* an explicit user deletion request;
* identity / credential re-verification;
* a pending-deletion state;
* a configurable grace/recovery period;
* a configurable notice schedule;
* cancellation before finalization;
* a truthful export opportunity where appropriate;
* truthful final-state communication;
* minimum necessary deletion-processing evidence (§4).

These are **future design principles only**. They authorize no implementation.

---

## 3. Grace period / notice timing — non-binding future UX preference

The Owner's current UX preference may include notices approximately: **around one month before; around one
week before; around one day before** finalization. These are **`NON-BINDING FUTURE UX PREFERENCES`**. They are
NOT legal requirements, NOT fixed retention periods, NOT globally binding timelines, and NOT proof of legal
compliance. Future timing must remain **configurable** and subject to legal and product determination.

**No liability-waiver claim.** Advance notices are intended to protect users from accidental deletion, improve
transparency, allow recovery/cancellation, and provide evidence of process. They must NOT be described as a
liability waiver, a release of responsibility, a waiver of statutory rights, or automatic legal protection.

---

## 4. Deletion-evidence minimization rule (binding on any future gate)

Only **minimum necessary, non-content-bearing evidence** may be retained to prove that a deletion request was
**received, verified, and processed**. Such evidence must: not contain erased user content; not permit
reconstruction of erased content; and not become a hidden backup of deleted data. Its legal basis and
retention duration remain subject to future legal determination — **no retention duration is decided here**.

---

## 5. Erasable data vs. retained records (classification requirement, not a rule)

Future deletion must NOT assume `delete every row everywhere`. Before implementation, data must be
classifiable as: (1) erasable user/account data; (2) records that may need lawful retention; (3) records whose
treatment requires legal determination; (4) append-only/audit evidence; (5) commercial/accounting records;
(6) security/fraud/abuse evidence where applicable. **No specific retention rule or legal basis is decided
here.**

---

## 6. Deferral does NOT suspend legal obligations (governance escalation rule)

**Deferral of the deletion capability does NOT suspend, waive, or defer any legal obligation that already
applies to InventorAI.** If a legally binding erasure/data-subject request is received before a future
self-service deletion capability exists, it must be **escalated to the Owner and external legal counsel as an
exception**. OD-DR1 must NOT be cited as grounds to refuse or improperly delay a legally valid request. This
is a governance escalation rule — NOT a conclusion that any particular legal regime currently applies.

---

## 7. Subscription expiry / inactivity is NOT deletion

Subscription **expiry, non-renewal, or non-payment**, and account **inactivity or absence of sign-in**, do NOT
constitute a deletion request and do NOT automatically trigger physical deletion. Any future
retention/deletion lifecycle for expired or inactive accounts requires a **separate governance decision**;
OD-DR1 does not authorize it.

---

## 8. Institutional deletion boundary (reserved)

InventorAI's intended product scope includes institutional users (OD-J1), but OD-DR1 does NOT decide
institutional deletion authority. Reserved to a later institutional/legal gate: individual vs
organization-owned data; who can request deletion of institutional data; employee/student account data;
institution-owned records; administrator authority; contractual retention obligations; organization workspace
deletion. **No institutional deletion authority is created here; no institutional feature is activated.**

---

## 9. Export / OD-DR2 boundary

Any future export opportunity before deletion is conditional — **"where legally and operationally
appropriate"** — and does NOT resolve OD-DR2, does NOT expand OD-DR2, and does NOT authorize account-wide
export. **Current authoritative export remains project-scoped only (P10-D3a). OD-DR2 stays unresolved.**

---

## 10. Current deactivation terminology preserved (binding)

Existing statuses such as `disabled` and `deleted` (the verified `ACCOUNT_STATUSES` vocabulary) are **account
lifecycle/status markers**. The existing `"deleted"` status is a **tombstone/non-active state — it is NOT
physical erasure**, and no user-facing or governance wording may describe this current status as physical
deletion. A future true erasure capability must use **distinct terminology/state** appropriate to that
separately governed capability. The current runtime status model is NOT altered by this candidate.

---

## 11. Future technical deletion-impact gate (prerequisite requirement)

Before any future physical-deletion implementation is authorized, a **separate technical deletion-impact
contract/gate** is required. That future gate must inventory, at minimum, every relevant data store — such as:
accounts; projects; records; ownership references; email tokens; API credentials; audit records; append-only
ledgers; lifecycle events; commercial/subscription/provider records where present; **backups; replicas;
derived copies/logs where applicable** — and classify each as: erasable; lawfully retained; or requires legal
determination. This is a **future gap/inventory requirement only** — the deletion algorithm is NOT designed
now.

---

## 12. Preserved decisions and boundaries

**OD-DR2** (account-wide data access/export) and **OD-CJ1** (commercial jurisdiction/tax scope) remain
**REGISTERED AND UNRESOLVED**. **OD-J1 and OD-J2 remain authoritative and unchanged** (accepted via PR #515).
OD-A continues to govern the brand/name dependency. **P10-D3b is preserved** — not reopened, modified, or
reinterpreted; Account Deactivation ≠ Physical Deletion remains the operative truth.

---

## 13. Non-authorization (binding)

This record authorizes **no** implementation of any kind: no deletion or erasure capability; no retention or
cleanup logic; no account-wide export; no institutional functionality; no legal-artifact drafting; no
infrastructure work; no PSRR execution; no deployment. Every subsequent step remains separately
Owner-authorized under P10-C §10, and any future deletion implementation additionally requires the §11
technical deletion-impact gate plus external legal determination.
