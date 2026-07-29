# OD-R — Cross-Application Communication, Sponsorship, Privacy and Trust Boundaries

**Decision:** OD-R (Phase 2 cross-application boundaries).
**Type:** documentation-only owner decision. **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified base:** `b9f9320ddd933be7bcd4513e9afb919237f81c37`.

---

## 0. Lifecycle status (read first)

```
OD-R / OD-S:  AUTHORIZED FOR DOCUMENTATION CANDIDATE PREPARATION
              NOT MERGED
              NOT FORMALLY CLOSED
```

This is a substantive documentation candidate. It is **not** accepted, merged,
formally closed, or durably closed. Those states are recorded only when their
owner-acceptance and merge evidence exist, per the combined OD-R + OD-S lifecycle.

## 1. Purpose and boundary type

OD-R records **product-governance and architectural boundaries only** for three
conceptually and architecturally **separate** cross-application capabilities. It
defines **no** interface, storage model, database, administration screen, visual
design, frequency behavior, or runtime. All design and implementation are
deferred to Phase 3 or separately authorized downstream workstreams and require
separate explicit owner authorization. No Phase 3 work is begun or authorized.

The three capabilities (A, B, C) remain architecturally separate even though
recorded in one owner decision.

---

## A. Sponsor Recognition and Configurable Branding Boundary

**Intent:** simple recognition of approved sponsors (banks, companies,
institutions, or other supporting organizations). **Explicit non-scope:** this is
**not** a video-advertising system, advertising-auction platform,
behavioral-targeting system, or complex campaign-management platform.

**Recognition may include (boundary intents, not an implementation spec):**
sponsor name; sponsor logo; a short statement such as `Sponsored by` or `برعاية`;
optional sponsor-related colors or visual identity.

**Future authorized administration boundary (capabilities to be designed later):**
add a sponsor; replace the sponsor logo; remove the logo; temporarily disable a
sponsor without deleting its configuration; change the sponsor name; change the
short sponsorship statement; support one or multiple sponsors; control display
order; activate or deactivate each sponsor; define global display / display on all
eligible pages / display on selected pages; support Arabic and English; support
RTL and responsive presentation.

**Architectural constraints:** sponsor data must be **centrally configurable** in
the future and must **not** be hard-coded independently into individual pages
(consistent with OD-B centralized branding indirection). Sponsorship or branding
**must never alter technical evaluation, idea progression, evidence assessment, or
engine behavior** (OD-N plan-neutrality and OD-K core/adapter separation remain
binding; sponsor/branding concerns stay outside the deterministic core).

**Deferred:** actual placement, visual design, size, layout, colors, Themes,
multi-sponsor presentation, administrative interface, storage model, and frontend
implementation belong to **Phase 3 or separately authorized downstream
workstreams**. This section supersedes nothing; it extends the RW-8 boundary
prospectively and does not modify OD-A or OD-B.

---

## B. Centrally Configurable Administrative Notice Boundary

**Intent:** a centrally configurable notice, presentable as a popup, modal,
banner, or another approved UI pattern, belonging to the application
administration or owner, for any legitimate approved communication purpose —
including: a welcome message; an administrative notice; an important platform
update; introduction of a feature; registration or subscription onboarding; a
privacy or confidentiality notice; a material Privacy Policy change; a service,
security, or operational notice; a short sponsor-related message where separately
approved.

**Separation:** this capability is **separate from** sponsor recognition (A) and
**separate from** the permanent Privacy Policy (C).

**Future configuration boundary (to be designed later):** title; short message;
Arabic and English content; optional image or sponsor logo; active or inactive
status; start and end dates; page applicability; display at registration or
subscription onboarding; display once; display once per user or once per notice
version where technically appropriate; another controlled frequency; a clear close
action; an optional acknowledgment or continuation action; priority where multiple
notices exist.

**Behavioral constraint:** the notice must **not** repeatedly interrupt or annoy
users, and must **not** block normal use unless acknowledgment is legitimately
necessary for a material legal, privacy, security, service, or similar change.

**Deferred:** the UI pattern, visual design, frequency logic, acknowledgment
persistence, administration interface, storage, responsive behavior, RTL,
accessibility, and implementation belong to **Phase 3 or separately authorized
downstream workstreams**.

---

## C. Privacy, Confidentiality and User Trust Communication Boundary

InventorAI may process sensitive information, including: idea descriptions;
technical concepts; user answers; supporting evidence; uploaded materials;
personal data; account-related data; future subscription-related information.

**Terminology rule (narrow, user-facing only):** use the word **`idea`** instead
of **`invention`** in user-facing privacy, confidentiality, trust, onboarding, and
sensitive-data-collection communication (sensitive information may be processed
before an idea has legally or technically become an invention). This is a **narrow
user-facing terminology rule**; it does **not** authorize a repository-wide
replacement of `invention` in existing technical, patent, legal, engine,
product-identity, or governance terminology where `invention` remains correct.

**Layered privacy-communication model (boundary, not final wording):**
1. a short notice during registration or subscription onboarding;
2. an inline context-specific notice near forms collecting sensitive idea-related
   or personal information;
3. a permanently accessible comprehensive Privacy Policy;
4. a popup or modal notice **only when appropriate**, such as: first registration;
   first subscription activation; first sensitive-data submission; a material
   Privacy Policy change; a material change to data-processing practices.

A popup must **not** be the only privacy mechanism.

**Truthful-claims rule:** the platform must **not** make absolute or unverified
statements such as `No one can access your data.` or `Your data will never be
viewed.` Any published privacy or confidentiality statement must **accurately
reflect the technical, operational, contractual, and legal controls that actually
exist at that time**, including where applicable: authorized access; authentication
and authorization; storage; encryption; access logging; auditability; retention;
deletion; backups and recovery; hosting and third-party processors; support access;
artificial-intelligence processing; whether user data is used for model training;
and user access, correction, export, and deletion rights.

**No final legal wording:** final legal Privacy Policy wording is **not** drafted
by OD-R and must not be published until checked against actually-implemented
controls and applicable legal requirements (Phase 10 / separate legal review).

**Launch constraint:** user-facing notices are **not a substitute for technical
protection**. Real registration, authentication, subscription, payment, or
collection of sensitive idea-related information must **not** be launched until the
required foundations are implemented and independently verified — as applicable:
secure authentication; authorization and role-based access; secure durable
persistence; encryption; secrets management; audit logging; retention and deletion;
backups and recovery; third-party processor governance; security testing;
privacy-policy accuracy; and applicable legal and regulatory review. Exact
sequencing is governed by the future authorized workstreams (Phase 3/4/5/8/10).

---

## 2. Deferral and non-authorization

All design and implementation for A, B, and C are deferred and separately gated
(Phase 3 UX/UI, presentation, responsive, Arabic/English, RTL; Phase 4 durable
data/privacy lifecycle; Phase 5 accounts/auth; Phase 8 subscription/payment;
Phase 10 production readiness, legal Privacy Policy/Terms/consent, security/release).

**No code, UI, runtime, schema, database, legal-policy, account, authentication,
subscription, payment, sponsor-management, popup/notice behavior, or privacy-control
implementation is authorized by OD-R.** No Phase 3 work is begun. Existing accepted
records (OD-A, OD-B, OD-I, OD-K, OD-N, and all prior evidence) are unchanged and are
extended prospectively only.

## 3. RED path

`DOCUMENTED NO-VALID-RED`. Documentation-only; changes no runtime code, JSON,
behavior, or executable contract. Validation uses documentation consistency, exact
scope, protected tree/blob verification, roadmap byte-prefix preservation, and
ancestry — not a test transition.

## 4. Evidence classification

Phase 2 owner-decision evidence artifact (documentation candidate). It becomes an
accepted, merged, and durably closed decision only through the combined OD-R + OD-S
lifecycle (independent candidate review → owner acceptance → normal merge →
post-merge verification → one combined formal-closure record → one post-closure
synchronization). It grants no implementation, release, or deployment authority.
