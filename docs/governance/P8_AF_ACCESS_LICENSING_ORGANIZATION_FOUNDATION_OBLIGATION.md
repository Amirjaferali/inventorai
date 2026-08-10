# P8-AF — Access, Licensing & Organization Foundation — OBLIGATION REGISTRATION

**Status of THIS record:** governance/documentation-only **obligation registration** — authoritative if/when independently
reviewed, Owner-accepted, and merged. It **registers a mandatory Phase-8 architectural-foundation obligation**; it
**implements nothing**, activates nothing, decides no commercial policy/price/provider, and creates no schema. It is
registered by the P8-I4 formal closure gate (`P8_I4_PAYMENT_PROVIDER_BOUNDARY_FORMAL_CLOSURE_RECORD.md`) and is **subordinate**
to the committed governance anchors, contracts, and `ACTIVE_EXECUTION_ROADMAP.md`. **Recording future work here authorizes
nothing.**

## 1. Purpose & status

- **Obligation:** ensure InventorAI remains technically and governably capable of supporting **multiple future
  commercial/access models WITHOUT redesigning** the core account, entitlement, ownership, subscription-lifecycle, or
  payment architecture.
- **Status:** **REQUIRED — mandatory before `P8-CLOSE`. NOT IMPLEMENTED. NOT ACTIVATED. NOT STARTED.**
- **Distinctness:** `P8-AF` is **NOT** part of the Payment Provider Boundary (`P8-I4`). It is a separate cross-cutting
  foundation.
- **Next gate:** **`P8-AF-C` — Access, Licensing & Organization Foundation Contract** (governance contract first; **no
  implementation before that contract is independently reviewed and accepted**). `P8-AF-C` must determine the **smallest**
  technical seams necessary to make the accepted future-readiness requirements real **without prematurely building all
  product variants**.

## 2. Core architectural principle (binding for the future contract)

Preserve and explicitly register the separation:

**Authentication ≠ Authorization ≠ Account identity ≠ Data ownership ≠ Commercial entitlement ≠ Subscription lifecycle ≠
Payment state ≠ Billing ownership.**

Also binding:

- **Paying for access does NOT automatically confer ownership of user data.** A party paying for an entitlement must not
  automatically receive access to another user's private data unless a **separately accepted** authorization/data-access
  policy permits it.
- No future access mechanism may weaken authentication or security, rewrite user identity, corrupt underlying plan identity,
  create accidental double quota, or become a hidden authentication/authorization/ownership/privacy/payment bypass.

## 3. Registered future-readiness scope (architectural-foundation level only — NOT activated)

The `P8-AF-C` contract must preserve architectural capability for the following. **None is implemented or activated by this
registration.**

### Option 1 — Individual account (unchanged today)
Individual user → individual authenticated account → personal data ownership → individual entitlement/subscription where
applicable. Current individual-account behavior is **unchanged** by this registration.

### Option 2 — 7-DAY per-account trial (directional preference; NOT activated)
Owner-preferred trial duration is **7 DAYS, NOT 14**. If later activated (separate gate): each eligible user has their own
account; the trial begins from a **deterministic canonical start**; trial data remains **durable** and attached to the same
account; if the user subscribes before expiry, **all existing durable trial data MUST remain** — **no destructive reset, no
account replacement, no ownership transfer**; the trial→paid transition must **preserve durable ownership and data**. The
P8-I3 lifecycle already provides a stored `trialing` state and canonical `trial_started` / `trial_converted` / `trial_ended`
events on the append-only event log with an injected deterministic clock; anti-lock-in + OD-O already guarantee
data-preservation across the transition. **Do NOT activate a trial here.**

### Trial expiry / data-lifecycle boundary (OPEN — separate policy)
Intended future pre-use disclosure: trial duration = 7 days; continued access after the trial may require subscription; if
the user does not subscribe, trial data is intended to expire/be deleted **according to a separately accepted retention/
deletion policy**. **However: AUTOMATIC DAY-7 HARD DELETION IS NOT CURRENTLY AUTHORIZED.** Do NOT implement or claim day-7
deletion. A separate accepted retention/privacy/data-lifecycle decision must define expiry-vs-immediate-deletion, any
grace/retention period, soft-vs-hard delete, backups/retention implications, export opportunity, legal/privacy requirements,
notice/consent requirements, and audit evidence. The architecture must preserve the future ability to implement the accepted
policy without redesign.

### Trial time semantics (OPEN — do NOT infer)
Whether "7 days" means **exactly 168 hours from trial start** or **7 calendar-day semantics** is an **OPEN Owner decision**.
Do NOT infer the answer. The runtime foundation should be capable of **deterministic timestamp-based** semantics.

### Option 3 — Global promotional / free-access period (NOT activated)
A future optional ability for the Owner/Admin to make InventorAI available free of charge for a **configurable period**,
distinct from an individual trial (illustrative-only example window 2026-10-01 → 2026-12-31; **no dates are selected now**).
The foundation should later allow configurable concepts such as `campaign_enabled`, `campaign_start_at`, `campaign_end_at`,
a campaign identifier/version, and optional eligibility scope. **Critical:** the Owner/Admin **MUST NOT need a source-code
change** to define, schedule, start, stop, extend, or disable such a future campaign. A future campaign must activate and
expire **deterministically** within its configured window; require **no** payment provider; **not** bypass authentication or
authorization; **not** rewrite user identity; **not** automatically destroy user data when it ends; **coexist safely** with
paid subscriptions and trial access; and be auditable where required. **Do NOT build the configuration UI now.**

### Option 4 — Owner / Admin non-billed access (NOT activated)
A future ability for **explicitly authorized** Owner/Admin/test accounts to use appropriate capabilities without making a real
payment. It must **NOT** be a secret login, an authentication bypass, a hardcoded email bypass, a hidden payment bypass, an
ownership bypass, or a privacy bypass. The future shape must be **explicit and auditable**: authenticated account →
authorization/role → entitlement grant → normal application access path. Owner/Admin non-billed status must remain
conceptually **separate from authentication identity**. **Do NOT implement roles in the closure gate.**

### Option 5 — Organization / institution licensing (MANDATORY future-readiness)
InventorAI must be architecturally capable of supporting institutional customers (universities, schools, training institutes,
companies, engineering firms, research centers, government entities) **without redesigning** the account/subscription system.
Recommended foundation: **Organization → organization subscription/agreement → purchased seat capacity → individual member
accounts → seat assignment** — **NOT** many members sharing one username/password.

- **Named-seat model (preferred initial foundation).** Example: Organization = University A; Purchased Seats = 20; Assigned =
  18; Available = 2. Each assigned member authenticates through **their own account**, retains an individual identity, retains
  **separately attributable** activity/data, and consumes one assigned seat when applicable. **Shared organization login is
  NOT the foundation** (it would undermine attribution, privacy, ownership, auditing, revocation, per-account usage, secure
  member removal, and individual data boundaries). An organization may have a canonical organization identity/account/
  container, but members remain **individually authenticated principals**.
- **Organization Admin foundation.** Future capability for an authorized Organization Admin to invite a member, assign a
  purchased seat, release/revoke a seat, reassign an available seat per accepted policy, and view seat capacity/usage.
  **Organization Admin does NOT automatically equal access to every member's private content.**
- **Billing ownership vs data ownership (binding).** Organization pays ≠ organization automatically owns all member data;
  seat assignment ≠ permission to read member projects; billing administrator ≠ content administrator. Any future
  instructor/supervisor/organization visibility into member work must require a **separately accepted** role / permission /
  sharing / assignment-course-workspace / data-governance policy. Do not infer visibility from who paid.
- **Seat reassignment safety.** Reassigning a released seat (Student A leaves → seat available → Student B receives it) must
  **NOT** transfer the previous user's data to the new seat holder. Account/data identity and seat identity remain separable.
- **Organization ↔ member relationship.** The foundation must be able to represent conceptually: Organization → memberships →
  individual accounts; separately Organization → commercial agreement/subscription → seat capacity; and membership → seat
  assignment — **without collapsing** authentication, data ownership, billing, membership, and entitlement into one coupled
  entity. The **detailed schema is NOT selected here.**
- **Future invitation / domain / SSO.** Preserve architectural openness to email invitations, allowed organization email
  domain, bulk onboarding, and enterprise SSO — but **do NOT implement them now** and **do NOT make SSO mandatory** for
  organization licensing.
- **Concurrent licensing.** NOT a current requirement; **named seats** are the preferred initial foundation. A concurrent-use
  model remains future-reserved and separately governed (materially different concurrency/session/accounting requirements);
  the foundation should not unnecessarily prevent it but need not implement or fully contract it now.

### Option 6 — Enterprise / custom commercial model (NOT activated)
Preserve architectural ability to support negotiated seat quantity, custom billing terms, invoice-based arrangements, and
organization-specific entitlement packages. **No enterprise pricing or commercial policy is chosen now; do NOT implement
enterprise billing.** The purpose is only to prevent an architecture where subscription = mandatory personal card payment by
one individual.

### Commercial-model family compatibility
`P8-AF` must preserve, at minimum, architectural compatibility with **(1) Individual, (2) Organization / Named Seats,
(3) Enterprise / Custom Contract** — **without** requiring three unrelated account systems.

## 4. Cross-cutting requirements the future contract MUST define

- **Access-resolution precedence.** A deterministic effective-access resolution model across simultaneous sources — paid
  individual entitlement, organization-assigned seat, per-account 7-day trial, global promotional free access, Owner/Admin
  non-billed entitlement, future enterprise entitlement. The precedence must be **deterministic, explicit, testable,
  auditable where required**, unable to weaken authentication/security, unable to corrupt underlying plan identity, unable to
  create accidental double quota, and compatible with expiry/revocation. **The final precedence is NOT decided here.**
- **Quota composition.** Future access mechanisms must compose safely with the **P8-I2 quota authority** (individual /
  organization-seat / trial / promotional / enterprise quotas). **Do not decide actual limits and do not duplicate quota
  authority — P8-I2 remains the sole commercial usage/quota authority.**
- **Subscription-lifecycle authority.** **P8-I3 remains the canonical subscription-lifecycle authority.** Do **not** create a
  second lifecycle state machine for organization seats, trial campaigns, Owner/Admin access, or promotional campaigns; the
  contract must determine the cleanest composition without duplicating P8-I3 (**D-FPC-MAP-06**).
- **Payment-provider separation & portability.** Access models must not be coupled to a specific payment provider:
  commercial/access model → canonical commercial state → provider-neutral payment boundary (**P8-I4**) → optional external
  provider. A free trial, a promotional free period, Owner/Admin non-billed access, and organization seat assignment do **not**
  require a provider; real external payment collection remains separately provider-gated. The core account/access model must
  not depend on provider-specific customer/subscription identifiers (enabling provider change, invoice/manual enterprise
  billing, institutional contract billing, and multiple future adapters).

## 5. No premature implementation (hard boundary)

This obligation registration (and the P8-I4 closure gate that created it) must **NOT** create an organizations table,
memberships table, seats table, role table, admin UI, campaign table, trial-duration constant, pricing, subscription SKUs, or
enterprise plans. Those belong only to later bounded contract/implementation gates after independent review and Owner
authorization.

## 6. Boundary / status

`P8-AF` is **REGISTERED as the required next Phase-8 foundation obligation** and is **mandatory before `P8-CLOSE`**. It is
**NOT implemented, NOT activated, NOT started**. The next gate is **`P8-AF-C`** (governance contract first). This registration
authorizes no push, PR, merge beyond the delivering candidate, implementation, role/organization/campaign schema, trial/
promotional/Owner-Admin activation, provider selection, `P8-CLOSE`, `Phase 9`, `Phase 10`, PSRR execution, or deployment.
Public paid activation / production remain **BLOCKED / NOT AUTHORIZED**. Phase 8 remains **OPEN / NOT CLOSED**.
