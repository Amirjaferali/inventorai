# P10-LT1 — External Legal & Tax Input Commissioning Gate (governance-only; commissions questions, answers nothing)

**Status:** GOVERNANCE-ONLY CANDIDATE. This gate **defines the exact questions, fact package, required adviser
qualifications, answer format, and intake/acceptance protocol for external legal and tax/accounting input**.
It answers none of the questions, creates no legal or tax conclusion, drafts no customer-facing legal
artifact, and authorizes no implementation.

**Phase:** 10 — Commercial, Legal, Security and Operational Readiness, under
`PHASE_10_COMMERCIAL_LEGAL_SECURITY_OPERATIONAL_READINESS_P10C_CONTRACT.md` §10 (evidence-based; smallest
sufficient scope; Owner-selected; separately authorized). It **operationalizes** the external legal-input
register established by `P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md` §5 — it does not duplicate
or replace that register, and does not close it.

**Authoritative base at drafting:** `5dfc35e34bbfc9a8681d575a7e26613a5038c674` (PR #518 merge — OD-CJ1
acceptance candidate #3 `ec2ff7f0…`; first parent `b98561b8…`, merge tree `76b05623…` equal to the accepted
candidate tree — independently re-verified at authoring).

---

## §1. Preserved authoritative state (verified at base; nothing rewritten)

OD-J1, OD-J2, OD-DR1, OD-DR2, and OD-CJ1 are all ACCEPTED and authoritative (each verified at this exact
base): Kuwait as intended commercial starting jurisdiction; USD as initial/base commercial pricing and
billing currency; B2C + B2B commercial eligibility; recurring-subscription direction with
automatic-recurring-collection direction only; `PAYMENT METHOD ≠ PAYMENT PROVIDER`; Visa/Mastercard, Apple
Pay, and KNET-where-applicable compatibility direction; future wallets/methods no-foreclosure only;
payment-provider / tax-provider / Merchant-of-Record neutrality; the external legal/tax register OPEN; paid
activation BLOCKED (`D-P8-PL-01 class C`); PSRR NOT TRIGGERED; deployment NOT AUTHORIZED. **No prior Owner
decision is rewritten by this gate.**

**PR #518 synchronization (recorded here per repository convention).** OD-CJ1 acceptance candidate
`ec2ff7f0bf8ca6d0614735717384ba887f859228` was Owner-accepted at that exact SHA and merged via **PR #518**,
tip `5dfc35e34bbfc9a8681d575a7e26613a5038c674` (first parent `b98561b8…`, second parent `ec2ff7f0…`, merge
tree `76b05623…`, empty candidate→merge diff — independently re-verified). The accepted OD-CJ1 content is
recorded as authoritative and is NOT altered here.

---

## §2. Gate purpose

`P10-LT1 — EXTERNAL LEGAL & TAX INPUT COMMISSIONING GATE`:
**TO DEFINE THE EXACT QUESTIONS, FACT PACKAGE, REQUIRED ADVISER QUALIFICATIONS, ANSWER FORMAT, AND
INTAKE/ACCEPTANCE PROTOCOL FOR EXTERNAL LEGAL AND TAX/ACCOUNTING INPUT.**

This gate must NOT answer the questions, must NOT create legal conclusions, must NOT create tax conclusions,
and must NOT draft customer-facing legal artifacts.

---

## §3. External LEGAL question register (LQ-*) — questions only, grounded in existing open items

Every question below traces to an already-registered open item (gate §5 register; P10-C §4/§9; OD-DR1/OD-DR2
escalation rules; OD-CJ1 §3). **None is answered here.**

**Commercial / legal entity**
* LQ-01 — What legal/commercial entity structure is appropriate for initial Kuwait commercial operation?
* LQ-02 — What contracting-party identity must appear in customer-facing terms?
* LQ-03 — What legal/contact disclosures are required?

**Privacy / data protection**
* LQ-04 — Which privacy/data-protection regimes apply given globally open availability (OD-J1), the Kuwait
  starting commercial position (OD-CJ1), and the actual data processing (fact pack §6)?
* LQ-05 — Is Kuwait PDPL or any other national privacy law applicable?
* LQ-06 — Is GDPR or any other foreign regime applicable, and under what factual conditions?
* LQ-07 — What privacy notices/disclosures are required?

**Data rights**
* LQ-08 — What access/export rights must be provided?
* LQ-09 — What deletion/erasure rights must be provided?
* LQ-10 — What retention exceptions are legally permissible or required?
* LQ-11 — What response procedures/timelines are required for data-subject requests?
* LQ-12 — How should the accepted OD-DR1 (deactivation-now / erasure-deferred) and OD-DR2 (project-scoped
  export-now / account-wide deferred) positions be implemented legally?

**B2C / consumer protection**
* LQ-13 — What pre-contract disclosures are required?
* LQ-14 — What cancellation rights apply?
* LQ-15 — What renewal disclosures apply?
* LQ-16 — What recurring-payment consent requirements apply?
* LQ-17 — What refund rights or mandatory cooling-off rights apply, if any?
* LQ-18 — Are local-currency display requirements applicable (given USD base pricing)?

**B2B / companies**
* LQ-19 — Can the same standard terms cover B2B and B2C?
* LQ-20 — What B2B-specific terms/disclosures are required?
* LQ-21 — Are company invoicing/procurement requirements different?
* LQ-22 — Are limitation-of-liability or warranty provisions treated differently for B2B?

**Subscription / payment**
* LQ-23 — What subscription terms are legally required?
* LQ-24 — What automatic-renewal wording and consent are required?
* LQ-25 — What payment-failure/suspension disclosures are required?
* LQ-26 — What payment-method disclosures are required?
* LQ-27 — Are any Apple Pay / KNET / card-scheme-specific legal disclosures required?

---

## §4. External TAX / ACCOUNTING question register (TQ-*) — questions only

* TQ-01 — What tax registrations are required for a Kuwait-based starting commercial operation?
* TQ-02 — What VAT/GST/sales-tax obligations apply, if any?
* TQ-03 — Does customer location/residence create foreign tax obligations?
* TQ-04 — What B2C vs B2B tax-treatment differences apply?
* TQ-05 — Are reverse-charge or withholding rules relevant?
* TQ-06 — What invoice/receipt requirements apply?
* TQ-07 — What accounting records must be retained?
* TQ-08 — Is USD pricing acceptable for the intended markets?
* TQ-09 — Are local-currency display or invoicing requirements applicable?
* TQ-10 — What tax-inclusive vs tax-exclusive presentation is required?
* TQ-11 — What cross-border digital-service tax rules, if any, apply?
* TQ-12 — Does a Merchant-of-Record model materially change tax/compliance obligations?
* TQ-13 — What facts would be needed to evaluate MoR vs direct merchant later?

No tax provider is selected. No MoR is selected. **None of these questions is answered here.**

---

## §5. Canonical adviser fact pack (repository-authoritative facts only; every item cited)

| Fact | Authority |
|---|---|
| Product: deterministic invention-development evaluation product; inventor remains sole author; no legal ownership/patentability determinations | `STRATEGIC_PRODUCT_VISION.md`; OD-D/OD-E (`OWNER_DECISION_REGISTER.md`) |
| Intended users: individuals AND institutions (B2C + B2B) | OD-J1 §2.3; OD-CJ1 §4 |
| Kuwait intended commercial starting jurisdiction (intent fact, not entity/tax decision) | OD-CJ1 §1 |
| Globally open user availability from launch; no geo-restriction intended | OD-J1 §2.2 |
| USD initial/base commercial pricing and billing currency; multi-currency deferred | OD-CJ1 §10 |
| Recurring-subscription commercial direction with automatic recurring collection (direction only) | OD-CJ1 §6 |
| Payment-method compatibility direction: Visa/Mastercard/major cards, Apple Pay, KNET where applicable; `METHOD ≠ PROVIDER` | OD-CJ1 §8/§8A |
| No payment provider, no tax provider, no Merchant of Record selected | OD-CJ1 §8–§9 |
| No production hosting provider/region selected (delegated to a future infrastructure gate) | OD-J2 §3.2 |
| Data actually processed server-side: account identity (opaque id, normalized email, scrypt password hash, status, timestamps), hashed verification/reset tokens, signed-cookie sessions validated server-side, hashed API credentials, projects/records (user invention content), append-only audit/commercial scaffolding tables (no live billing data) | Jurisdiction gate §3 data-truth baseline; `engine/account_store.py`; `engine/record_store.py` |
| NOT processed: IP/device/network metadata; analytics/telemetry; any live third-party transfer (AI transfer disabled hardcoded; email dev-sink only; no payment webhook) — no external transfer path exists without a source-code change | Jurisdiction gate §3 baseline (revalidated at PR #514 base; `engine/`+`web/` unchanged since except governed D3a/D3b/none) |
| Browser draft text: client-side localStorage only (7-day lazy TTL); not server-held | `web/static/js/local_draft.js`; OD-DR2 §9 |
| Account exit today: Deactivation only — status tombstone retains all data; NO physical deletion/erasure capability; no enforced retention | P10-D3b; OD-DR1 §1/§10 |
| Export today: project-scoped self-service export only; no account-wide export | P10-D3a; OD-DR2 §2 |
| No live billing, no live payment integration, no production deployment; paid activation BLOCKED | OD-CJ1 §2; `D-P8-PL-01 class C` |
| Card-data architecture principle: hosted/provider-tokenized checkout keeps raw PAN/CVV off-platform; NO PCI-compliance claim | P8-I4 contract §15; OD-CJ1 §8A |
| Legal artifacts currently absent: no Privacy Policy, Terms, subscription/refund/cookie/payment/consent/B2B/data-processing artifacts; the live trust page itself discloses this | Privacy/Legal Readiness Assessment; `web/ui_text.py` `UI_SENS_DATA_07` |
| Product name `InventorAI` is a temporary internal working name; final name deferred to the OD-A brand gate | OD-A (`OWNER_DECISION_REGISTER.md`) |

No speculation is included; an adviser needing a fact not listed here must request it (§7 answer format:
"unresolved fact needed").

---

## §6. Required adviser qualifications (types only; no firm or person selected)

**`LEGAL COUNSEL`** — competent in: Kuwait commercial/consumer law; privacy/data protection; online
subscription/digital-service terms; cross-border customer exposure.

**`TAX / ACCOUNTING ADVISER`** — competent in: Kuwait taxation/accounting; digital services; cross-border
B2C/B2B taxation; invoicing/recordkeeping.

**Optional specialist lane:** if privacy/data-protection requires separate specialist input beyond general
counsel, that is recorded as an optional specialist lane — no provider is selected.

---

## §7. Required answer format (structured, not conversational)

Each external answer MUST carry: question ID (LQ-*/TQ-*); answer/conclusion; jurisdiction; factual
assumptions; legal/tax basis; mandatory-vs-recommended classification; required product/policy change;
required operational change; required documentation; timing/deadline if applicable; unresolved fact needed;
confidence/qualification; date of advice; adviser identity/credentials.

**The repository never converts external advice into authoritative product truth automatically.**

---

## §8. External-input intake protocol (future sequence; binding)

```
EXTERNAL RESPONSE → SOURCE VERIFICATION → INTERNAL MAPPING → OWNER REVIEW → GOVERNANCE CANDIDATE
→ CREATOR GRILL → INDEPENDENT REVIEW → OWNER ACCEPTANCE
```

External advice itself is **`EVIDENCE / INPUT`**, not automatically an accepted InventorAI governance
decision. **No implementation may be authorized solely because counsel/an adviser sent an answer.**

**Conflict / supersession rule.** If two advisers disagree: conclusions are NOT merged; the conflict is
recorded; it escalates to the Owner; specialist clarification is obtained if necessary. Later, more
authoritative/current external advice may supersede older advice **only through explicit governance
acceptance**; historical advice is preserved as evidence.

---

## §9. Legal-artifact boundary (binding)

P10-LT1 does NOT authorize drafting or publishing: a Privacy Policy; Terms of Service; Subscription Terms; a
Refund/Cancellation Policy; a Cookie Notice; payment disclosures; recurring-billing consent text;
institutional/B2B terms; data-processing terms; or legal/contact disclosures. These may be drafted **only
after the relevant external input is accepted through governance** (§8).

---

## §10. Commercial-policy boundary (binding)

This gate does NOT decide: actual price; monthly vs annual plans; trial duration/policy; grace period;
dunning/retry policy; refund policy; cancellation mechanics; renewal mechanics; discounts; B2B pricing;
packaging; enabled payment methods; payment provider; or MoR. **If external counsel needs proposed policy
assumptions to advise, those are registered as `OWNER INPUT REQUIRED` — not as decided facts.**

## §11. Provider / infrastructure boundary (binding)

No selection of: payment provider; tax provider; MoR; hosting provider; production region. The OD-J2
delegated infrastructure gate remains separate and untouched.

## §12. Paid activation / PSRR / deployment (preserved)

```
PAID ACTIVATION AUTHORIZED: NO   (D-P8-PL-01 class C — P10-LT1 does not satisfy it by itself)
PSRR TRIGGERED: NO               PSRR EXECUTION AUTHORIZED: NO
DEPLOYMENT AUTHORIZED: NO        (OD-P two-part gate unsatisfied)
```

---

## §13. Governance truth sweep (performed at base before freezing)

All 22 registered challenges were run against this record: no legal or tax question is answered; no regime
(GDPR/PDPL/VAT/GST) is claimed applicable; no adviser, firm, provider, MoR, or hosting is selected; no legal
terms are drafted; adviser input is never automatic authority (§7/§8); paid activation, PSRR, and deployment
are untouched (§12); OD-J1/J2/DR1/DR2/CJ1 are unaltered (§1); the external-input register is operationalized,
not closed; P8C §5 / P8-I4 deferred commercial decisions remain open (§10); every LQ-*/TQ-* item and fact-pack
row traces to a registered repository authority (no invented obligation); PR #518 synchronization is included
(§1); no existing register or contract is duplicated (this gate references the §5 register and the OD
evidence records rather than restating them as new authority). **Result: zero material failures.**
