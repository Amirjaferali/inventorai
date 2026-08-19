# Phase 10 — Owner Decision OD-CJ1 — Commercial Jurisdiction / Tax Scope

**Phase:** Phase 10 — Commercial, Legal, Security and Operational Readiness, under the authoritative
`docs/governance/P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md` (merged PR #514) which registered
OD-CJ1 as unresolved.
**Decision ID:** OD-CJ1 (commercial jurisdiction / tax scope).
**Scope:** documentation-only durable record of one Owner decision accepted **at strategy level**. **No
implementation. No billing, tax, pricing, provider, schema, or test change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified authoritative base at authoring:** `b98561b847884557cc90c7c6600644ae23abf4c5` (PR #517 merge —
OD-DR2 acceptance, authoritative; parents `46756528…` + `a9b3aee2…`, merge tree `8654270e…` equal to the
accepted candidate tree — independently re-verified at authoring).

---

## 1. Decision status

```
OD-CJ1 — OWNER DECISION ACCEPTED AT STRATEGY LEVEL
```

**Recorded: `KUWAIT AS THE CURRENT INTENDED COMMERCIAL STARTING JURISDICTION`.**

This is only **`A COMMERCIAL STARTING-POSITION INTENT FACT`**, supplied for later external legal/tax analysis.
The tax-scope component of OD-CJ1 remains **`DEFERRED PENDING EXTERNAL LEGAL/TAX DETERMINATION AND SEPARATE
OWNER AUTHORIZATION`**.

Kuwait is NOT represented as: a final legal entity structure; a final incorporation answer; a final tax nexus;
a final VAT/GST/sales-tax answer; a final Merchant-of-Record decision; a final invoicing jurisdiction; or a
final withholding/reverse-charge answer.

---

## 2. Paid-activation hard gate remains BLOCKED (load-bearing)

**OD-CJ1 acceptance does NOT discharge the requirement that tax/legal/commercial readiness be satisfied BEFORE
PAID ACTIVATION.** Public paid activation remains **`BLOCKED / NOT AUTHORIZED`** under the existing hard gate
**`D-P8-PL-01 class C`**. All independently required conditions are preserved (repository-confirmed):
applicable Phase-10 legal/readiness requirements; external legal/tax input; payment/refund/subscription terms;
`PSRR = GO/PASS` under `D-PSRR-01`; the separate Deployment Gate; and explicit Owner deployment authorization
under `OD-P`. **None of these is satisfied merely by accepting OD-CJ1.** No PSRR is triggered; no deployment
is authorized; no paid activation is authorized.

---

## 3. External legal/tax register remains OPEN

The P10 external legal-input register is preserved. In particular the following remain open: payment terms;
refund terms; subscription terms; tax treatment; tax jurisdiction; invoicing treatment; cross-border
obligations. **OD-CJ1 supplies commercial intent only — it does NOT close external legal/tax review.**

---

## 4. B2C + B2B commercial customer scope

Intended commercial customer eligibility includes BOTH **`INDIVIDUAL USERS / B2C`** and
**`COMPANIES / ORGANIZATIONS / B2B`**.

This cross-references the existing authoritative user-type scope under **OD-J1 §2.3**
(`docs/governance/evidence/phase10_owner_decisions/OD-J1_OD-J2_JURISDICTION_AND_HOSTING.md`), which remains
the authority for intended individual + institutional product/user-type scope — OD-CJ1 does NOT duplicate or
redefine OD-J1. OD-CJ1 records only **`COMMERCIAL CUSTOMER ELIGIBILITY`**.

**Load-bearing rule: `COMMERCIAL CUSTOMER ELIGIBILITY ≠ ENTERPRISE FEATURE ACTIVATION`.** No
enterprise/institutional functionality is activated; no B2B-specific commercial mechanics are authorized now.

---

## 5. No enterprise / B2B feature activation

OD-CJ1 does NOT activate or decide: enterprise tenancy; organization workspaces; institutional
administration; enterprise user management; administrator controls; negotiated contracts; institutional
pricing; enterprise pricing; purchase orders; corporate procurement; company invoicing workflows;
tax-exemption workflows; reverse-charge workflows; withholding-tax workflows; enterprise support obligations.
**Companies may be commercially eligible customers without these features existing.**

---

## 6. Recurring subscription direction (commercial direction only)

The Owner's intended commercial model is **`RECURRING SUBSCRIPTION`** with intended **`AUTOMATIC RECURRING
PAYMENT COLLECTION`**.

This is **`COMMERCIAL DIRECTION ONLY`**. It does NOT decide or authorize: billing frequency; monthly vs annual
model; price; currency; trial policy; grace period; payment retries; failed-payment handling; suspension
rules; renewal notices; cancellation mechanics; refunds; chargebacks; card storage; tokenization; or
provider-specific recurring billing. **No recurring-payment implementation is authorized now.**

---

## 7. P8-I4 Payment Provider Boundary — existing authority referenced, not created

The repository-authoritative boundary already exists: the **P8-I4 Payment Provider Boundary** (verified at the
base: `engine/payment_provider_port.py` defines `class PaymentProviderPort` — the canonical provider-neutral
port — with its fake/reference adapter and ingestion coordinator under the P8-I4 contract and closure record):

```
InventorAI commercial domain → canonical provider-neutral PaymentProviderPort → external payment provider
```

OD-CJ1 **references** this boundary. It does NOT create, rename, duplicate, or expand it. No live provider is
selected; no network/provider activation is authorized. **No new Commercial/Billing Layer is invented.**

---

## 8. Payment-provider neutrality (and the METHOD ≠ PROVIDER distinction)

**`PAYMENT-PROVIDER NEUTRALITY` is preserved.** No provider is selected or implied — not Stripe, PayPal,
Adyen, Paddle, Apple, Google, Visa, Mastercard, KNET, a local Kuwait gateway, a bank gateway, or any other
payment vendor. Provider selection remains separately governed.

**Load-bearing distinction: `PAYMENT METHOD ≠ PAYMENT PROVIDER`.** The Owner's payment-method compatibility
direction (§8A) names payment methods/rails, never platform providers. Adjacent clarifications, so no reading
of this section can conflict with §8A:

* `APPLE PAY COMPATIBILITY INTENT DOES NOT MEAN APPLE IS SELECTED AS INVENTORAI'S PAYMENT PROVIDER.`
* `VISA / MASTERCARD COMPATIBILITY DOES NOT MEAN VISA OR MASTERCARD IS SELECTED AS INVENTORAI'S PAYMENT
  GATEWAY / PROVIDER.`
* `KNET COMPATIBILITY DOES NOT MEAN KNET OR ANY KUWAIT GATEWAY IS SELECTED AS THE PAYMENT PROVIDER.`

---

## 8A. Payment-method compatibility direction (Owner decision; direction only)

**Classification: `PAYMENT-METHOD COMPATIBILITY DIRECTION ONLY`** — no payment method is currently
implemented or activated, and no implementation is authorized.

**Intended commercial payment-method compatibility includes:** Visa / major payment cards; Mastercard / major
payment cards; Apple Pay; and **KNET where commercially and technically applicable to the Kuwait starting
market**. Future compatibility must not be structurally foreclosed for: Google Pay; additional wallets;
additional local/regional payment methods; other internationally relevant payment methods — these are
**`FUTURE NO-FORECLOSURE ONLY`** (not selected as active methods; no additional payment rails selected; no
wallet integration activated; no wallet-specific code or routes created).

**KNET — no lock-in.** KNET compatibility reflects the Kuwait commercial starting position, but it is
**`COMPATIBILITY DIRECTION ONLY`**. It does NOT mean: Kuwait-only customers; Kuwait-only payment capability;
a Kuwait-only provider; permanent dependency on KNET; or that KNET must support every recurring-billing use
case. No KNET implementation is authorized.

**Recurring-subscription / method-capability boundary.** The Owner intends recurring subscription with
automatic recurring collection (§6), but **payment-method support for recurring subscription must be verified
at the future payment-provider implementation/selection gate** — no method is assumed to support recurring
collection identically. That future verification may include, where applicable: initial payment; recurring
renewal; payment authorization/consent; saved-payment reference/token; payment-method update; failed-payment
handling; retries; cancellation; refund handling. **No method is guaranteed now to support all of these. No
implementation is authorized.**

**Card-data / PCI architectural principle (existing P8-I4 authority referenced, not duplicated).** The
authoritative `PHASE_8_I4_PAYMENT_PROVIDER_BOUNDARY_INCREMENT_CONTRACT.md` §15 — "Security / PCI boundary
(architectural avoidance; NO compliance claim)" — already records: *"InventorAI SHOULD NOT receive/store raw
payment-card credentials where a hosted / provider-tokenized checkout flow can keep them off-platform. This
contract makes NO PCI-compliance claim… The system is NOT marked PCI compliant."* The Owner's direction is
recorded as **consistent with that existing architecture**: InventorAI should avoid directly storing raw
payment-card credentials — such as the full card number / PAN and the CVV / security code — where an
appropriately selected external payment provider/payment flow can process those regulated credentials and
expose only the bounded reference/token needed by InventorAI. **This alone establishes no PCI compliance;
tokenization is not designed now; no card data is stored now; no legal/compliance conclusion is made.** Exact
PCI/payment-security obligations remain subject to later provider selection, security review, and applicable
legal/compliance determination. No second PCI/security doctrine is created.

**Deferred `payment methods` register.** The P8-I4 deferred register explicitly lists `payment methods` as
OPEN. The Owner's payment-method compatibility direction **`CONSUMES BUT DOES NOT CLOSE`** that register:
actual implementation, provider-method compatibility, recurring support, and the final enabled methods remain
separately governed.

---

## 9. Tax-provider / Merchant-of-Record neutrality (no-foreclosure only)

No tax provider is selected. No Merchant-of-Record model is selected. Compatibility is preserved with a
future: direct merchant model; Merchant-of-Record model; provider-calculated tax; external tax service; and
accounting/tax reconciliation — **without selecting any**. For these capabilities, which have no existing
authoritative boundary, only **`NO-FORECLOSURE / ARCHITECTURE-PRESERVATION PRINCIPLES`** are recorded —
explicitly NOT a build instruction, NOT a prepare instruction, NOT pre-implementation, NOT a schema
instruction, NOT a route/job/infrastructure instruction.

---

## 10. Initial / base commercial currency — USD (Owner decision)

The Owner has decided: **`USD — UNITED STATES DOLLAR`** is the **`INITIAL / BASE COMMERCIAL PRICING AND
BILLING CURRENCY`** for InventorAI, at strategy level.

This means: initial commercial pricing may be denominated in USD; initial subscription billing may use USD;
USD is the starting commercial currency.

This does **NOT** mean: US commercial jurisdiction; US legal-entity jurisdiction; US hosting; US tax
jurisdiction; US-only customers; a US payment provider; or any VAT/GST/sales-tax conclusion. The separation
is preserved:

```
COMMERCIAL CURRENCY ≠ CUSTOMER LOCATION ≠ COMMERCIAL ENTITY JURISDICTION ≠ HOSTING LOCATION
≠ PAYMENT-PROVIDER LOCATION ≠ TAX JURISDICTION
```

**Legal / tax boundary of the USD decision.** USD is a commercial pricing/billing starting decision only. It
does NOT determine or satisfy any future: local-currency display requirement; invoice-currency requirement;
consumer-protection requirement; accounting requirement; or tax-display requirement. Those remain subject to
external legal/tax/accounting determination.

**Future multi-currency remains `DEFERRED / NOT ACTIVATED`.** Only
**`NO-FORECLOSURE / ARCHITECTURE-PRESERVATION FOR FUTURE MULTI-CURRENCY`** is preserved — compatibility with
future multiple currencies, jurisdiction-specific pricing, B2C/B2B differentiation, market-specific
commercial handling, tax-inclusive/tax-exclusive presentation, and provider substitution. NOT implemented and
NOT authorized: additional currencies; currency conversion; FX-rate logic; a currency selector; regional
currency mapping; multi-currency settlement; multi-currency accounting; currency-specific tax logic. **Future
currencies require a separately governed commercial decision/gate.**

---

## 11. Price / terms remain undecided

Explicitly preserved as unresolved: actual price; billing period; regional pricing; enterprise pricing;
discounts; trial policy; refund policy; cancellation policy; renewal rules; grace policy; tax-inclusive vs
tax-exclusive display; provider selection. **No values are invented.** (The base commercial currency is the
one exception, decided in §10 as USD at strategy level.)

---

## 12. P8C §5 / P8-I4 deferred decisions are CONSUMED, NOT CLOSED (load-bearing)

**The P8C §5 deferred business decisions and the P8-I4 deferred registers are `CONSUMED BY, NOT CLOSED BY,
OD-CJ1`.** They remain open and separately governed. OD-CJ1 must not create the false impression that
commercial readiness is complete — it is not.

---

## 13. Jurisdiction separation rule (anti-drift)

```
USER RESIDENCE ≠ CUSTOMER LOCATION ≠ COMMERCIAL ENTITY JURISDICTION ≠ HOSTING LOCATION
≠ PAYMENT-PROVIDER LOCATION ≠ TAX JURISDICTION ≠ COMMERCIAL CURRENCY
```

In particular, the §10 USD decision must never be read as inferring US jurisdiction, US hosting, US tax
treatment, US-only customers, or a US payment provider.

No one of these may automatically be inferred from another. Explicitly prohibited interpretations: Kuwait
starting jurisdiction = Kuwait-only users; Kuwait starting jurisdiction = Kuwait-only companies; Kuwait
starting jurisdiction = Kuwait hosting; GCC-first marketing = GCC-only tax treatment; provider location =
automatic customer tax treatment; user residence = hosting location. **OD-J1 and OD-J2 are preserved
unchanged.**

---

## 14. Legal / tax escalation (escalation rule only)

**Deferral does NOT suspend any legally applicable obligation.** If a legally binding
commercial/payment/tax/accounting requirement arises before automation exists, it must be escalated as
appropriate to: the Owner; external legal counsel; an external tax/accounting adviser. This is **`AN
ESCALATION RULE ONLY`** — NOT a conclusion that any particular VAT, GST, sales tax, withholding, reverse
charge, registration, or invoicing requirement currently applies.

---

## 15. Preserved decisions and boundaries

OD-J1, OD-J2, OD-DR1, and OD-DR2 remain accepted, authoritative, and unchanged. OD-A continues to govern the
brand/name dependency. The Phase-10 external legal-input register remains open (§3). The paid-activation hard
gate (§2), PSRR trigger, and deployment boundary are untouched.

---

## 16. Non-authorization (binding)

This record authorizes **no** implementation of any kind: no billing or tax logic; no payment or tax provider
selection; no Merchant-of-Record selection; no paid-subscription activation; no recurring-payment
implementation; no payment-method implementation or activation (cards, Apple Pay, KNET, Google Pay, wallets,
or any other rail); no card-data storage or tokenization design; no multi-currency activation; no
enterprise/institutional functionality; no legal/tax artifact drafting; no infrastructure work; no PSRR
execution; no deployment. Every subsequent step remains
separately Owner-authorized under P10-C §10 and the existing P8C/P8-I4/D-P8-PL-01/D-PSRR-01/OD-P gates.
