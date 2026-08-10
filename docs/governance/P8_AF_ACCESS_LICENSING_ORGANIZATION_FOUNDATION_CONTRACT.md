# P8-AF-C — Access, Licensing & Organization Foundation — Bounded Contract & Architecture

**Status of THIS record:** governance/documentation-only **contract candidate** (P8-AF-C), authoritative if/when independently
reviewed, Owner-accepted, merged, and post-merge verified. It **defines** the smallest canonical architecture that lets
InventorAI, later and under **separate implementation gates**, support multiple access/licensing/organization/commercial
models **without redesigning** the core account, entitlement, ownership, subscription-lifecycle, or payment architecture. It
**implements nothing**, creates no runtime code or schema, activates no commercial model, and creates no organization / seat /
campaign / role / trial / pricing / enterprise-billing / admin-UI artifact. **DOCUMENTED NO-VALID-RED — CONTRACT-ONLY
GOVERNANCE GATE.** No runtime/test/Domain-Pack/schema/prompt/benchmark/web/CI/provider-config file is changed by this gate.

**Authoritative base:** `61ff4a85989dfc8d9881764597d5d7dc415da213` (PR #428; parents `3a802fd` + `1da9d2d`; tree
`95d9aa4624cb9ab6505976433fd3324678078369`), verified read-only before editing; boot OK; clean.

**Lineage / authority.** Fulfils the registered obligation **`P8-AF`**
(`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_OBLIGATION.md`), mandatory before `P8-CLOSE`. Subordinate to
the accepted Phase-8 contract **P8-C** and to the CLOSED foundations **P8-I1** (Plan & Entitlement — entitlement authority),
**P8-I2** (Commercial Usage Quotas — quota authority), **P8-I3** (Subscription Lifecycle — lifecycle authority), and the
CLOSED **P8-I4** (Payment Provider Boundary — provider-neutral payment boundary). **D-FPC-MAP-06:** consume/extend the existing
authorities and seams; introduce only the smallest new composition seam(s); create no second plan catalog, quota counter, or
lifecycle state machine. This contract selects **no** payment provider, decides **no** commercial policy/price, and starts
**no** implementation.

---

## 1. Purpose

Define the smallest stable canonical architecture — an **access-grant model** plus a single **effective-access resolution
authority** — that composes the existing commercial authorities (P8-I1/I2/I3/I4) so that InventorAI can **later** support, each
under its own separate gate: (1) individual access/subscriptions; (2) a **7-day** per-account trial; (3) a global configurable
promotional free-access period; (4) Owner/Admin non-billed access; (5) organization/institution licensing; (6) named seats;
(7) enterprise/custom commercial agreements; (8) deterministic effective-access precedence; (9) safe composition with the
quota and lifecycle authorities; (10) separation of billing ownership from data ownership; (11) future extensibility without
coupling to a specific payment provider. **None of these capabilities is activated by this contract.**

## 2. Scope (what P8-AF-C governs)

- The **canonical Access-Grant model** (§5): a provider-neutral, source-neutral representation of *why* an account (or scope)
  currently has access, traceable to its source and time-bounded.
- The **single Access-Resolution authority/seam** (§5–§6): one deterministic place that composes evidence from the existing
  authorities + access grants into an **effective access decision**, with a defined **precedence/composition rule** (§6).
- The **future-safe boundaries** for trial (§7), promotional campaign (§8), Owner/Admin non-billed access (§9), organization
  (§10), membership (§11), named seats (§12), billing-vs-data-ownership (§13), enterprise/custom (§14), quota composition
  (§15), lifecycle composition (§16), audit/revocation (§17), and data ownership (§18).
- The **minimum implementation increment** that must follow (§19), its **RED→GREEN acceptance matrix** (§20), the **open
  decisions** left to the Owner (§21), **P8-AF closure criteria** (§22), and the **production/payment/Phase-9/10 blocks**
  (§23).

This contract defines **architecture and invariants only**. Field names and storage shapes below are **candidate
illustrations to be finalized at the implementation-contract stage**, not adopted verbatim here.

## 3. Non-goals (this contract does NOT do)

Implement or activate any access model; create runtime code or schema for organization/membership/seat/role/campaign/
trial-config/access-grant/pricing/enterprise-billing; select or integrate a payment provider; decide any commercial policy
(prices, currency, tax, trial duration semantics, retention period, campaign dates/eligibility, seat counts, refunds,
proration, dunning); build an admin UI or configuration UI; design a full RBAC platform; implement SSO / email-domain
onboarding / bulk import; implement concurrent-seat counting; implement automatic trial-data deletion; run implementation
tests; start `P8-AF` implementation, `P8-CLOSE`, Phase 9, Phase 10, or PSRR; authorize production or public paid activation.
A raw trial/campaign/seat/role concept must **not** leak into the deterministic core (OD-N preserved).

## 4. Authority boundaries (binding — composition, not duplication)

| Authority | Owns | P8-AF MUST NOT |
|---|---|---|
| **P8-I1** Plan & Entitlement | Plan catalog + plan→entitlement mapping (the definition of *what a plan grants*) | Create a second plan catalog or redefine entitlements |
| **P8-I2** Commercial Usage Quotas | The sole commercial usage/quota counters + atomic evaluate-and-consume | Create a second counter, double-count, or reset counters from an unrelated grant |
| **P8-I3** Subscription Lifecycle | Canonical per-account lifecycle state machine + append-only event log (incl. `trialing`) | Create a competing lifecycle/seat/campaign state machine or duplicate its states |
| **P8-I4** Payment Provider Boundary | Provider-neutral canonical payment boundary + adapter isolation | Couple access grants to a specific provider or route free access through a provider |
| **P8-AF** (this) | The **access-grant model** + the **single effective-access resolution seam** that *composes* the above | Become the entitlement/quota/lifecycle/payment authority |

**Core separation principle (binding).** **Authentication ≠ Authorization ≠ Account identity ≠ Organization membership ≠ Seat
assignment ≠ Data ownership ≠ Commercial entitlement ≠ Subscription lifecycle ≠ Payment state ≠ Billing ownership.** Also:
**payment for access ≠ automatic ownership of user data; organization pays ≠ organization may read member content; seat
assignment ≠ content visibility; billing administrator ≠ content administrator.** No access mechanism may become a hidden
authentication/authorization/ownership/privacy/payment bypass, weaken authentication/security, rewrite user identity, corrupt
plan identity, or create accidental double quota.

## 5. Canonical access model (the Access-Grant + single resolver)

**5.1 One resolution authority (no scattering).** There MUST be exactly **one** deterministic **effective-access resolution
seam** — a pure, side-effect-free function/service that, given an authenticated account (and optional organization/scope
context) and a resolution instant, returns an **effective access decision** with its source provenance. Access decisions MUST
NOT be scattered across templates, payment adapters, the lifecycle service, organization code, quota code, or ad-hoc role
checks. Those surfaces may **consume** the resolver's decision; they must not each re-derive it.

**5.2 Inputs the resolver composes (references, not copies).**
- base plan entitlement — **from P8-I1** (never recomputed);
- subscription lifecycle state — **from P8-I3** (never recomputed);
- zero or more **Access Grants** (below), each naming its source and time window;
- these compose under the deterministic precedence rule (§6). Quota policy selection is a **reference** to P8-I2 (§15), never
  a counter.

**5.3 Access-Grant concept (candidate representation — finalize at implementation).** A provider-neutral, source-neutral,
auditable record of a granted access, capable of expressing at minimum: **subject** (account or scope), **source/reason**,
**entitlement reference** (a P8-I1 entitlement/plan identity — never a redefinition), **effective_from**, **effective_until**
(nullable/open-ended where policy dictates), **status** (e.g. active / scheduled / expired / revoked), **provenance**
(who/what issued it + version), and an **optional organization/seat reference**. Candidate **sources** include
`individual_subscription`, `organization_seat`, `trial`, `promotional_campaign`, `owner_admin`, `enterprise_contract`. **Do
not adopt these field/source names verbatim** — choose the smallest representation consistent with the existing store and
authorities. **Critical invariant:** effective access MUST be **explainable and traceable to its source** (the resolver
returns *which* grant/authority produced the decision).

**5.4 Provider neutrality.** No Access-Grant field may be a provider-specific customer/subscription identifier; a grant refers
to canonical identities only (P8-I4 owns the opaque external mapping). A trial, a promotional grant, an Owner/Admin grant, and
a seat assignment require **no** payment provider.

## 6. Precedence / composition rule (deterministic; binding)

When multiple valid access sources coexist (examples: paid subscription + global campaign; trial + campaign; organization seat
+ personal subscription; Owner/Admin + expired subscription; enterprise + individual trial), the resolver MUST produce a
**deterministic, explicit, testable, auditable** decision. The rule MUST be defined along these axes rather than a naive
"highest plan wins" (which is **not** assumed safe):

- **Access availability** — is access granted at the instant? (any active non-revoked grant or authority within its window).
- **Feature entitlement** — which P8-I1 entitlement applies. Composition MUST NOT corrupt plan identity: the effective
  entitlement is *selected from* an existing P8-I1 entitlement (e.g., the most-capable **currently-valid** source), never a
  synthesized new plan.
- **Quota authority** — exactly one P8-I2 quota policy is selected per effective decision (§15); overlapping grants MUST NOT
  each increment counters (no double quota) and MUST NOT reset counters when switching source unless a separate governance
  decision authorizes it.
- **Expiry / revocation** — an expired or revoked source contributes nothing; revocation affects **effective access only**,
  never user data (§17–§18).
- **Audit provenance** — the winning source (and, where useful, the suppressed sources) are recorded so the decision is
  explainable.

**Prohibited outcomes:** accidental double quota; plan-identity corruption; quota reset from an unrelated grant; accidental
downgrade; hidden access bypass; ambiguous revocation. **A full precedence table is contracted at the implementation stage
once the concrete sources are enabled;** this contract fixes the *axes and invariants*, and defers the concrete ordering of
not-yet-activated sources to the implementation contract that first enables them (no source is activated here).

## 7. Trial foundation (7-day; NOT activated)

Owner-preferred future duration is **7 days, NOT 14.** The architecture MUST preserve future support for: one trial per
eligible account (per later policy); a **deterministic** trial start and **deterministic** expiry (injected clock; P8-I3
already provides this); the **P8-I3 `trialing` state and `trial_started`/`trial_converted`/`trial_ended` events** used where
appropriate (no separate trial state machine — §16); **trial→paid without data loss**, retaining the **same account identity**
and **same durable data** with **no destructive reset** (already guaranteed by anti-lock-in + OD-O). A trial is expressed as an
Access-Grant of source `trial` referencing a P8-I1 entitlement, composed by the resolver like any other source. **OPEN until
activation (do not decide here, do not create a runtime constant):** whether "7 days" = **exactly 168 hours** or **7
calendar-day** semantics; trial eligibility / repeat-trial rules.

## 8. Promotional free-access foundation (global; configurable; NOT activated)

The architecture MUST preserve a future **globally configurable** free-access campaign that the Owner/Admin can define,
schedule, start, stop, extend, or disable **WITHOUT a source-code change**. It MUST support concepts equivalent to: **campaign
identity**, **enabled/disabled**, **start timestamp**, **end timestamp**, **optional eligibility scope**, **version**, and
**audit/provenance** (candidate fields; finalized at implementation). Campaign properties (binding): **deterministic
activation** and **deterministic expiry** within the configured window; **no payment provider required**; **no automatic data
deletion at campaign end**; **coexists safely with paid users** (never downgrades or corrupts a paid user's plan identity);
**does not reset quota** unless separately governed; **remains auditable**. A campaign is surfaced to the resolver as an Access
source (`promotional_campaign`) evaluated against the resolution instant. **Canonical time representation:** repository-
consistent **UTC epoch** semantics (matching the P8-I3 injected integer-epoch clock) unless the implementation contract proves
another representation necessary. **No storage/UI is built here.** **OPEN:** actual dates, eligibility, and paid-user
treatment during a campaign (Owner decisions).

## 9. Owner/Admin non-billed access foundation (explicit; auditable; NOT activated)

Owner/Admin non-billed access MUST be shaped as: **authenticated account → explicit authorization → explicit
entitlement/access grant** (source `owner_admin`), and MUST NOT be a secret login, hardcoded email bypass, authentication
bypass, payment bypass embedded in provider code, privacy bypass, or ownership bypass. The contract **reserves a minimal
explicit authorization/role seam** — the smallest representation sufficient to mark an account as holding a non-billed
authorization that maps to a normal entitlement through the resolver — **without designing a full RBAC platform.** Owner/Admin
non-billed status is conceptually **separate from authentication identity** and is independently auditable and revocable
(§17). **OPEN:** the exact Owner/Admin entitlement scope. **No role table/UI is built here.**

## 10. Organization model (canonical; NOT activated)

Define a canonical **Organization/Institution** concept capable of representing universities, schools, companies, engineering
firms, research institutions, government entities, and training organizations. An Organization is conceptually **separate**
from individual account, billing agreement, membership, seat assignment, and content ownership. Organization *type* MUST NOT
be coupled to runtime behavior unless a later gate proves it necessary. An organization may hold a **canonical organization
identity/container**, but members remain **individually authenticated principals** (no shared credentials — §12). **No
organization schema/table is built here.**

## 11. Membership model (NOT activated)

Preserve the relationship **Organization → Membership → individual authenticated Account.** Membership expresses a bounded
organizational relationship **without replacing account identity** (the account remains the authentication + data-ownership
principal). A membership may carry a **narrow** status (candidate future states: `invited` / `active` / `suspended` /
`removed`) — **not** a duplicate of the subscription lifecycle (§16). **Do not overdesign** the membership lifecycle beyond
what a later gate needs. **No membership schema is built here.**

## 12. Named-seat licensing (preferred initial org foundation; NOT activated)

**Named seats** are the preferred initial organization licensing foundation (example: an organization purchases 20 seats;
Assigned 18; Available 2). Each assigned member remains **individually authenticated**. A **seat is a commercial entitlement
assignment** — it is **NOT** a user account, a data container, or a content owner. **Shared credentials are NOT the licensing
model.** A seat assignment surfaces to the resolver as an Access-Grant of source `organization_seat` referencing a P8-I1
entitlement. **Concurrent-use licensing is NOT a current requirement** and the foundation MUST NOT be designed around
concurrent-use counting — while not making future concurrent licensing impossible.

## 13. Seat capacity/assignment + billing-vs-data-ownership separation (binding)

Define future-safe concepts for **seat capacity, assignment, release, reassignment, assignment provenance, assignment
effective time, and optional expiry.** **Seat reassignment safety (binding invariant):** if Seat X is reassigned from User A
to User B, **User B MUST NOT inherit User A's content** — account/data identity and seat identity remain strictly separable;
the seat carries entitlement, not data. **Billing ownership vs data ownership (binding):** an organization may **pay for**
member access (`Organization → Commercial Agreement → Seat Capacity`) while members remain `Individual Account → Membership →
Seat Assignment`; **organization pays ≠ organization owns/reads member data; seat assignment ≠ content visibility; billing
administrator ≠ content administrator.** Any future organization/instructor/supervisor visibility into member work MUST require
a **separately governed** permission / sharing / instructor-supervisor relationship / workspace-course assignment / explicit
data-governance rule — **never inferred from who paid.**

**Organization Admin (reserved; NOT activated).** A future authorized Organization Admin may perform **bounded** administration
(invite member; assign/release/reassign seat per policy; view capacity/usage; manage allowed organization settings).
**Organization Admin ≠ automatic content visibility.** Broad content-admin rights MUST NOT be conferred merely by being an
organization administrator.

## 14. Enterprise / custom commercial compatibility (NOT activated)

Preserve architectural compatibility with negotiated seat quantities, invoice/manual billing, enterprise contracts, custom
entitlement packages, and custom payment terms — **without** implementing pricing, invoices, tax, enterprise billing, or
contracts, and **without** assuming all subscriptions are purchased by a personal credit card. The architecture MUST be able
to represent, at minimum, the **commercial-model family (1) Individual, (2) Organization / Named Seats, (3) Enterprise /
Custom Contract** **without building three separate account systems.** Future combinations (organization trial, promotional
seat allocation, enterprise pilot, temporary institutional access) MUST NOT be architecturally precluded, but are **not**
contracted in detail here. **Future onboarding openness** (email invitations, allowed email-domain onboarding, bulk import,
enterprise **SSO**) is preserved but **not** implemented and **SSO is NOT required** for named-seat licensing.

## 15. Quota composition (P8-I2 remains sole authority)

Access grants **select or reference** a P8-I2 quota policy; they do **not** hold or increment counters. The implementation
contract MUST define how the effective decision maps to **exactly one** applicable quota policy per account per instant, such
that: multiple overlapping grants do **not** each increment counters; there is **no double allowance**; and switching access
source does **not** reset counters unless a separate governance decision explicitly authorizes it. Candidate quota-policy
sources to reference: individual plan / trial / organization-seat / campaign / enterprise. **No counter is created,
duplicated, or reset by this contract; P8-I2 remains the sole quota authority.**

## 16. Lifecycle composition (P8-I3 remains sole lifecycle authority)

P8-I3 remains the canonical subscription-lifecycle authority. The contract MUST NOT create: a **seat** lifecycle state machine
that competes with subscription lifecycle; a **campaign** lifecycle state machine duplicating commercial subscription states;
or a **trial** lifecycle outside P8-I3 where P8-I3 already handles `trialing`. Organization **membership** and **seat
assignment** may carry their **own narrow status semantics** (e.g., assigned/released; invited/active/removed) that are
**distinct from** and **do not duplicate** the subscription lifecycle. Where a trial maps to a subscription lifecycle, it uses
the P8-I3 `trialing` state and its canonical events.

## 17. Audit / provenance + revocation expectations

**Audit/provenance (preserve fields; full audit-log implementation only where existing governance already mandates it).** The
architecture MUST preserve evidence/provenance fields sufficient to later record actions such as: access grant issued/revoked;
campaign enabled/changed/disabled; seat assigned/released/reassigned; Owner/Admin non-billed entitlement granted/revoked;
organization commercial capacity changed. **Revocation (deterministic; binding).** Trial expiry, campaign end, seat
revocation, member removal, Owner/Admin entitlement removal, and enterprise-agreement end MUST each deterministically remove
**effective access** via the resolver — and MUST NOT silently destroy user data. Ambiguous revocation is prohibited (a revoked
source contributes nothing to the decision, explainably).

## 18. Data ownership / portability (preserve current guarantees; no expansion)

Existing **anti-lock-in / data-ownership** guarantees are preserved unchanged: loss of commercial entitlement (trial expiry,
campaign end, cancellation, downgrade, seat revocation, membership removal) MUST NOT silently destroy user identity, durable
user data, or ownership records. **Read/export/delete** rights remain governed by the **existing** privacy/data-lifecycle
policy (Phase-4 governance + OD-O + OD-R). **Trial-data expiry/deletion is separate from commercial entitlement expiry:**
trial expiry MUST NOT automatically equal hard delete. **AUTOMATIC DAY-7 HARD DELETION IS NOT AUTHORIZED.** The architecture
MUST allow a later separately-accepted retention/deletion policy (e.g., expired/inaccessible → retention window → deletion, or
another accepted policy) without redesign; it MUST NOT decide the retention period, deletion mode, grace, backups, or notice
here. This contract expands **no** legal/ownership claim beyond existing governance.

**Pre-use notice/consent boundary (capability, not implementation).** The architecture MUST be **capable of later recording**
(without implementing now) evidence equivalent to: trial terms/notice **version**, **shown_at**, **accepted_at** (only if
acceptance is later required), **trial_started_at**, **trial_expires_at**. The implementation contract MUST determine whether
this belongs in an **existing** consent/audit mechanism or a small new record — **avoiding duplication of any consent
system.** Exact notice wording is an **OPEN** Owner decision.

## 19. Minimum implementation increment (the SMALLEST foundation to follow — NOT started)

After this contract is accepted, the **first** `P8-AF` implementation increment MUST prove **only** that the architecture can
**represent and resolve** these models safely — not build every feature. It MUST select the **smallest** seams necessary to
prevent later redesign, and MUST justify each seam as necessary. Candidate seams to **evaluate** (adopt only the necessary
subset; each is additive `CREATE TABLE IF NOT EXISTS` / new isolated module per the P8-I1…I4 precedent — **no `ALTER TABLE`,
no back-fill, no destructive migration**, and OD-N import isolation preserved):

- a canonical **Access-Grant** model (additive persistence);
- the single **Access-Resolution** seam (pure composition over P8-I1/I3 + grants; references P8-I2);
- a minimal **organization identity** seam;
- a **membership** seam;
- a **named-seat capacity/assignment** seam;
- a **campaign config** seam (runtime-configurable, no source-code change to operate);
- a minimal explicit **authorization/role** seam (Owner/Admin non-billed);
- **audit/provenance** support on the above.

**Do NOT assume all are required.** The likely minimal first increment is the **Access-Grant model + the Access-Resolution
seam + provenance**, proving composition/precedence/quota-reference/revocation against **fake/in-memory** sources, with the
organization/seat/campaign/role seams contracted-but-deferred unless the increment proves one is needed to avoid redesign.
Each increment is a **separate Owner-authorized gate** with its own RED→GREEN evidence and independent review.

## 20. RED→GREEN acceptance matrix (for the FUTURE implementation increment — NOT run here)

The eventual implementation increment MUST include genuine behavioral RED→GREEN tests (RED fails for missing **behavior**, not
import absence; no fake durability) covering at least:

1. **trial→paid preserves data** (same account identity + durable data retained; no destructive reset);
2. **campaign start/end access resolution** (deterministic activation and expiry at the window boundaries);
3. **paid + campaign coexistence** (a paid user is not downgraded/plan-corrupted by an active campaign);
4. **seat assignment grants access** (an assigned member resolves to the seat entitlement);
5. **seat reassignment does not transfer data** (User B does not inherit User A's content);
6. **organization payer cannot read member content by default** (billing ≠ data-access);
7. **Owner/Admin entitlement does not bypass authentication** (auth still required; grant is authorization→entitlement);
8. **deterministic precedence** (fixed decision + provenance when multiple sources coexist);
9. **quota not double-counted** (overlapping grants reference exactly one P8-I2 policy; no double allowance/reset);
10. **revocation removes access but not data** (trial/campaign/seat/member/Owner-Admin/enterprise revocation);
11. **provider independence** (trial/campaign/Owner-Admin/seat require no payment provider; real payment still routes through
    P8-I4);
12. **restart/durability** where persistence is introduced (close/reopen round-trip; deterministic).

**No implementation tests are run in this contract-only gate.**

## 21. Deferred / OPEN Owner & business decisions (do NOT invent; keep OPEN)

7-day = 168h vs calendar semantics; trial eligibility / repeat-trial rules; post-trial retention duration; exact trial notice
wording; campaign dates; campaign eligibility; paid-user treatment during a campaign; Owner/Admin entitlement scope;
organization pricing; seat pricing; minimum/maximum seat counts; seat-reassignment frequency; organization data-visibility
policy; instructor/supervisor permissions; enterprise billing model; invoice requirements; SSO requirements; **payment-provider
selection**; payment methods; pricing/currency/tax; refunds/proration/dunning. All remain **OPEN — REQUIRED OWNER/BUSINESS
DECISIONS**, subordinate to P8-C §8 / P8-I3-C §9 / P8-I4-C §18 and not duplicated. Recording them here authorizes nothing.

## 22. P8-AF closure criteria

`P8-AF` (the obligation) is eligible for formal closure only when **all** hold: (a) this P8-AF-C contract is independently
reviewed, Owner-accepted, merged, and post-merge verified; (b) the necessary minimum implementation increment(s) (§19) are
implemented with genuine RED→GREEN evidence from the §20 matrix, independently reviewed, Owner-accepted, merged, and
post-merge verified — proving the architecture can **represent and resolve** the models safely **without** activating any of
them; (c) the authority boundaries (§4) and binding invariants (§6, §13, §16, §17, §18) are demonstrated and unweakened;
(d) a dedicated `P8-AF` formal closure record is produced. Closure of `P8-AF` does **not** activate any access model, close
Phase 8, or authorize production. After `P8-AF` closure, the remaining Phase-8 gate is **`P8-CLOSE`** (Phase-8 exit review).

## 23. Explicit production / payment / Phase-9-10 blocks (unweakened)

This contract selects/integrates **no** payment provider; activates **no** trial/promotional/Owner-Admin/organization/
enterprise access; creates **no** organization/membership/seat/role/campaign/access-grant/pricing/enterprise-billing runtime
code or schema; starts **no** implementation. **OD-I / OD-N / OD-O / OD-K / D-P8-PL-01 / D-PSRR-01 / OD-P / anti-lock-in**
remain in force. **`P8-AF` implementation — NOT STARTED; `P8-CLOSE` — NOT STARTED; Phase 8 — NOT CLOSED; Phase 9 / Phase 10 —
NOT AUTHORIZED; PSRR EXECUTION — NOT STARTED; public paid activation / production — BLOCKED / NOT AUTHORIZED** until applicable
Phase-10 legal/readiness + PSRR = GO/PASS + a governing separate Deployment Gate + explicit Owner deployment authorization.

**Boundary / status after this entry.** **P8-AF-C is a CONTRACT CANDIDATE ONLY — definition only; NOT started, NOT
implemented, NOT authorized; NO provider selected; NO access model activated.** Candidate only until independent review →
Owner acceptance → merge → post-merge verification → a **separate** Owner-authorized `P8-AF` implementation gate. Append-only;
prior history not rewritten. This entry authorizes no push, PR, merge beyond this candidate, `P8-AF` implementation start,
provider selection, access-model activation, `P8-CLOSE`, or deployment.
