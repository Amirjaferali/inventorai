# Phase 10 — Owner Decisions OD-J1 and OD-J2 — Launch Markets / User Scope and Hosting Strategy

**Phase:** Phase 10 — Commercial, Legal, Security and Operational Readiness
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`), under the authoritative
`docs/governance/P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md` (merged PR #514, tip
`022e5b75cb0e7bc9ee248f20aed5df7da1368989`) which registered both decisions as unresolved.
**Decision IDs:** OD-J1 (launch markets / user-residence and user scope) and OD-J2 (hosting / data-location
strategy) — recorded together because they jointly establish the business/product/technical intent that later
external legal analysis will evaluate.
**Scope:** documentation-only durable record of two accepted Owner decisions. **No implementation. No code,
test, template, schema, infrastructure, provider, or region change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified authoritative base at authoring:** `022e5b75cb0e7bc9ee248f20aed5df7da1368989` (PR #514 merge —
Jurisdiction & Data-Rights Owner-Decision Gate, authoritative; parents `07389b24…` + `ca4956c2…`, merge tree
`39e2ee43…` equal to the accepted candidate tree).

**Identifier disambiguation (binding).** Phase 1 contains an earlier, distinct accepted decision **OD-J**
("Product role model", recorded with OD-O in
`docs/governance/evidence/phase1_owner_decisions/OD-J_OD-O_ACCOUNTS_AND_EVIDENCE_CONFIDENTIALITY.md`). The
Phase-10 decisions **OD-J1 / OD-J2** recorded here are **Jurisdiction & Data-Rights decisions established by
the P10 gate and are distinct from Phase-1 OD-J**. The historical Phase-1 decision is not modified, renamed,
or reinterpreted by this record, and OD-J1/OD-J2 keep their gate-established identifiers unchanged.

---

## 1. Decision status

```
OD-J1 — OWNER DECISION ACCEPTED
OD-J2 — OWNER DECISION ACCEPTED AT STRATEGY LEVEL
```

---

## 2. OD-J1 — Launch Markets / User-Residence and User Scope (ACCEPTED)

**Canonical statement:** *GCC-first commercial marketing; globally open user availability from launch;
global-ready product from the outset.*

**2.1 Commercial / marketing focus.** InventorAI's initial practical and commercial **marketing** focus is
**GCC / Gulf markets first**. This is a marketing/commercial **sequencing** decision only. It must NOT be
interpreted as: GCC-only availability; Kuwait-only availability; a permanent GCC restriction; a geographic
access restriction; or a technical architecture limitation.

**2.2 User-residence scope.** The Owner explicitly decides: **InventorAI is NOT intended to be geo-restricted
at launch.** Users residing **outside the GCC may access the application, register, create an account, and use
the product from launch**, subject only to later lawfully-required restrictions if any are established through
separate legal/governance processes. InventorAI is intended to be usable by people across the GCC, the Middle
East, Europe, Asia, Africa, North America, South America, and Oceania — and generally **worldwide**.

**This is the Owner's product/market intent. It is NOT a legal conclusion that the product is already cleared
for every jurisdiction.**

**2.3 User type scope.** InventorAI is intended for both **INDIVIDUAL USE** and **INSTITUTIONAL USE**,
including: the general public; inventors; researchers; students; companies; universities; authorities;
institutions; and organizations. This records **intended product/user scope only**. It does NOT activate:
institutional tenancy; enterprise administration; organizational contracts; Layer 5; Stage 6; B2B-specific
implementation; separate institutional pricing; or institutional compliance features. Whether consumer and
institutional terms are later unified or separated remains a future legal/commercial determination.

---

## 3. OD-J2 — Hosting / Data-Location Strategy (ACCEPTED AT STRATEGY LEVEL)

**Owner principle:** *minimum practical infrastructure now, clean expansion seams later.*

**3.1 Strategy.** InventorAI may begin with a practical **single production hosting region** for the initial
rollout. The architecture must preserve future flexibility for: provider migration; additional regions;
regional data residency; jurisdiction-driven hosting requirements; institutional/customer-specific hosting
requirements; geographic hosting changes; and future global expansion. The core product must avoid unnecessary
permanent coupling to: one cloud provider; one permanent region; one permanent country; or one
jurisdiction-specific storage assumption.

**3.2 What is NOT decided here (binding boundaries).** The following are NOT decided by OD-J2: AWS; Azure;
Google Cloud; any other provider; Bahrain; UAE; Saudi Arabia; Europe; United States; or any exact production
region. The selection of the initial provider and production region is **DELEGATED TO A LATER, SEPARATELY
AUTHORIZED INFRASTRUCTURE GATE**. This is an **accepted delegation decision**, not an unresolved
product-strategy ambiguity. Explicitly: **GCC-focused rollout does NOT mean the hosting region must be inside
the GCC. No data-location commitment inside or outside the GCC is made by OD-J1 or OD-J2.**

**3.3 No premature multi-region requirement.** "Global-ready" must NOT be interpreted as: multi-region must be
built now; active-active infrastructure is required now; regional sharding is required now; or multiple cloud
providers must be configured now. The intended principle is: **avoid architectural foreclosure without
over-engineering the first release** — build the smallest infrastructure justified by current evidence while
preserving future expansion seams.

---

## 4. Legal boundary (binding)

OD-J1 and OD-J2 provide business/product/technical intent **for later legal analysis**. They do NOT decide:
GDPR applicability; Kuwait or any GCC PDPL applicability; EU legal applicability; any other national privacy
regime; lawful basis; consent requirements; cookie requirements; retention periods; erasure requirements;
portability requirements; or tax treatment. Those remain subject to **external legal input** (the gate's §5
register) once the relevant facts — now including these accepted intents — are evaluated.

---

## 5. Remaining Owner decisions (explicitly NOT resolved here)

**OD-DR1** (physical deletion / erasure product position), **OD-DR2** (account-wide data access / export
product position), and **OD-CJ1** (commercial jurisdiction / tax scope) remain **REGISTERED AND UNRESOLVED**
exactly as the gate left them. The brand/name dependency remains governed by the existing **OD-A** authority
(final public product name deferred to its brand-validation gate); no duplicate decision is created and the
product is not renamed.

---

## 6. P10-D3b historical stat correction (numeric correction only)

The merged gate record and two synchronization surfaces recorded the P10-D3b implementation diff stat as
`+487/-1`. The repository-verified figure for candidate `a751cb3b1ffb882ea8596cefafe7ef1a9222cd81`
(authoritative merge `07389b24ce9c4a606526315f2c19118f292f04db`) is:

```
5 files changed, 487 insertions(+), 3 deletions(-)
```

The prior `+487/-1` figure is **superseded by the repository-verified `+487/-3`**. This is a **numeric/stat
correction only**: P10-D3b is NOT reopened, modified, or reinterpreted, and the already-merged
`P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md` is deliberately NOT byte-edited (historical
preservation); this correction note and the live status surfaces carry the corrected figure.

---

## 7. Non-authorization (binding)

This record authorizes **no** implementation of any kind: no infrastructure, provider, or region work; no
institutional/enterprise feature; no geo-restriction mechanism; no legal-artifact drafting; no
deletion/erasure or account-wide export capability; no payment activation; no PSRR execution; no deployment.
Every subsequent step remains separately Owner-authorized under P10-C §10.
