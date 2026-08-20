# PSRR-C1 — PSRR Execution Contract

## 0. Record identity (file-creation rules)

```text
File path:        docs/governance/PSRR_C1_PSRR_EXECUTION_CONTRACT.md
Purpose:          instantiate the registered PSRR 37-item minimum scope into an
                  item-by-item, evidence-based, vendor-neutral execution contract;
                  durably record OD-FR1 (first-public-production-deployment intent =
                  YES) and the Owner tax-governance foundation; define the
                  application-layer / provider-dependent / policy-dependent tranches
                  and the infrastructure-gate relationship.
Input contract:   PSRR_PRODUCTION_SECURITY_RELEASE_READINESS_REGISTRATION.md (§4
                  trigger, §5 hard block, §6 outcomes, §7 scope items 1–37, §8
                  preserved Phase-7 §25 items, §9 evidence, §10 independence, §11
                  vendor neutrality); D-PSRR-01; OD-P; D-P8-PL-01 class C; OD-J1/J2;
                  OD-CJ1; P10-LT1 (LQ-01…LQ-27, TQ-01…TQ-13); the authoritative
                  Phase-10 Formal Closure Record; P10-RL1 checklist (live row truth);
                  LEAN §3/§4/§5/§5A/§5B.
Output contract:  a frozen execution contract. PSRR EXECUTION REMAINS NOT AUTHORIZED
                  and NOT STARTED by this contract; execution requires the Owner's
                  separate explicit authorization against this frozen contract.
Prohibited:       starting PSRR execution; selecting any provider/vendor/tool;
                  implementing or activating any tax calculation/charge/display;
                  inventing legal/tax conclusions; authorizing deployment or paid
                  activation; weakening PSRR GO, OD-P, or D-P8-PL-01; expanding
                  OD-J2 §3.2 beyond hosting provider + production region; any
                  runtime/test/schema/guardrail change; future-domain work.
Status:           GOVERNANCE-ONLY CANDIDATE (authoritative only if/when merged and
                  post-merge verified).
Base:             aab8f365f1bd37523dbbbf970533f8e5ecf3ce42 (PR #539 merge —
                  Phase-10 Formal Closure, authoritative).
```

## 1. Authority reconstruction

- Phase 10: FORMALLY CLOSED (PR #539; Option 2 structure authoritative). PSRR:
  REGISTERED (D-PSRR-01, PR #413) — trigger §4 verbatim "Mandatory: BEFORE FIRST PUBLIC
  PRODUCTION DEPLOYMENT"; hard block §5 verbatim "PUBLIC PRODUCTION DEPLOYMENT: BLOCKED until
  PSRR = GO", removable only together with OD-P's separate deployment gate + explicit Owner
  deployment authorization; outcomes §6 (GO/PASS or NO-GO/FAIL); evidence §9; independence
  §10 (existing independent-review model); vendor neutrality §11.
- FR-GS1 (accepted read-only decision gate) and the PSRR Entry Reconstruction (accepted)
  established: trigger fact = Owner intent; entry CONDITIONAL pending (a) this execution
  contract + separate execution authorization and (b) provider facts for the
  provider-dependent tranche only.
- The registration's §12 line "Phase 10 remains NOT STARTED" is historical wording from
  registration time; the newest authoritative state (Phase 10 formally closed) controls.

## 2. Durable decision record — OD-FR1 (first durable repository recording)

```text
OD-FR1 — FIRST PUBLIC PRODUCTION DEPLOYMENT INTENT: YES.
"The Owner now intends to proceed toward the FIRST PUBLIC PRODUCTION
DEPLOYMENT of InventorAI."  (Owner decision, made at the FR-GS1 acceptance;
first durable repository recording is THIS document — no earlier repository
provenance is claimed.)
Effect: establishes ONLY the PSRR §4 trigger FACT. It does NOT authorize PSRR
execution, deployment, paid activation, provider selection, legal/tax
conclusions, public brand selection, commercial charging, or future-domain
implementation. PSRR: REGISTERED — TRIGGER CONDITION MET BY OWNER INTENT —
EXECUTION NOT AUTHORIZED / NOT STARTED.
Parallel Owner authorization (same message): begin the P10-LT1 external
legal/tax adviser commissioning process (Owner-side act using the merged
P10-LT1 package; no internal legal/tax conclusions; unrelated technical work
never blocked while responses are pending).
ODR row addition remains future governance housekeeping (NB8 pattern); the
decision is binding from this durable record.
```

## 3. Tax-governance foundation (Owner direction — durable recording; NO implementation)

**3.1 Governing principle (Owner wording, preserved):**

> "InventorAI does not currently assume or activate a Kuwait-specific
> platform/subscription tax. Future tax treatment must remain
> configuration-driven and may be activated only when supported by
> then-current applicable law, platform/store rules, transaction
> jurisdiction, payment/Merchant-of-Record structure, or a separately
> authorized commercial decision."

Bounded rules: do NOT implement or activate a Kuwait-specific platform/subscription tax as
a precaution; do NOT charge or display an invented tax; do NOT hard-code that Kuwait will
never impose such taxes. **SPECULATIVE TAX IMPLEMENTATION REQUIRED NOW: NO.**

**3.2 Architectural intent (FOUNDATION / NO-FORECLOSURE only — nothing implemented now):**
preserve future capability for jurisdiction-aware tax treatment; store/platform-supplied
tax information; tax-inclusive or tax-exclusive pricing where later required;
Merchant-of-Record / payment-provider tax handling; future country-specific tax rules; and
rule/configuration updates without redesigning the subscription architecture. This is
consistent with — and adds nothing to — the existing provider-neutral `PaymentProviderPort`
(P8-I4) and the OD-CJ1 no-foreclosure/architecture-preservation principles. No tax
calculation, schema, route, configuration surface, or runtime is authorized now.

**3.3 User-facing behavior:** no new user-facing tax statement or charge is authorized.
Future checkout/subscription UX must display only taxes/fees actually applicable through
the governing store, platform, payment provider, or applicable law — never speculative
taxes.

**3.4 Transaction-tax vs entity-accounting distinction (binding):** (A) transaction-level
tax charged to the user is DISTINCT from (B) accounting/entity/income obligations on
revenue received by the operating entity. The Owner decision resolves ONLY the
product-development question: no speculative Kuwait platform/subscription tax
implementation is required now. Any later entity/accounting obligation remains a separate
commercial/accounting matter and must not block unrelated PSRR technical execution unless
authoritative governance later proves otherwise.

**3.5 External tax input (amended resolution pathway; P10-LT1 questions preserved):** no
internally invented binding tax conclusion; official-source research first; external
professional tax validation is reserved for material unresolved questions that cannot be
responsibly resolved from authoritative current sources, or where a formal professional
opinion is actually required before commercial activation; unrelated technical/readiness
work is never paused pending such validation. **TQ-01…TQ-13 are NOT erased and remain
OPEN** in the P10-LT1 registers; their resolution pathway is amended per this direction
(they remain hard-blocking where they already hard-block — commercial/paid activation —
and never blocked PSRR technical execution).

## 4. PSRR item-by-item execution matrix (all 37 registered items; scope owner = PSRR registration §7)

Tranche codes: **A** = APPLICATION-LAYER — EXECUTABLE NOW; **P** = PROVIDER /
PRODUCTION-CONTEXT DEPENDENT; **L** = POLICY / LEGAL EVIDENCE DEPENDENT; **F** = FINAL
EVIDENCE / INDEPENDENT REVIEW; **D** = GO / NO-GO DECISION. "Start now?" = executable
against the current repository with no hosting selection, production region, payment
provider, tax conclusion, or public deployment. Every item BLOCKS PSRR GO (the §7 scope is
a minimum) unless marked otherwise; "Risk treatment" = §9 outstanding-risk register
eligibility.

| # | PSRR item | Tranche | Current state (live source) | Evidence required / verification method | Dependency | Owner surface | Start now? | Blocks GO? | Blocks deploy? | Risk treatment |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Application security | A | Foundations merged (P10-SEC1…SEC4; residual gaps disclosed in RL-A6) | Security review of `web/app.py` surfaces + test evidence + residual-gap disposition | none | web/app.py; P10-SEC records | YES | YES | via GO | open risks registrable |
| 2 | Public API security | A | API v1 machine-credential Bearer auth (browser 401 by design) | Review + test evidence of `web/api_v1.py` | none | web/api_v1.py; P7-I2 | YES | YES | via GO | registrable |
| 3 | Authentication | A | P5-2 foundations (scrypt, verify, recovery, epoch revocation) | Review + suite evidence | none | engine/account_store.py; engine/auth_session.py | YES | YES | via GO | registrable |
| 4 | Authorization | A | Owner-only access; non-enumerating denials | Review + suite evidence | none | web/app.py `_project_authorized` | YES | YES | via GO | registrable |
| 5 | Ownership isolation | A | P5-3/P7-I2 isolation | Cross-account denial evidence (existing suites) | none | web/app.py; tests | YES | YES | via GO | registrable |
| 6 | Machine/API credential handling | A | Machine credentials implemented | Review of issuance/verification | none | web/api_v1.py | YES | YES | via GO | registrable |
| 7 | Credential revocation/rotation/expiry | A | Epoch revocation implemented; production secrets OPERATIONS not | App-level review now; ops half → item 8/9 | production ops → P | engine/auth_session.py | YES (app half) | YES | via GO | ops half registrable |
| 8 | Secrets/configuration management | A+P | Env-based fail-closed secret (app); no production ops | App-level review now; production secrets operations need provider context | provider facts | web/app.py; future infra | partial | YES | via GO | ops half registrable |
| 9 | Production configuration | P | None exists (RL-F7) | Config review of the real production environment | INFRA-G1 | future infra gate | NO | YES | via GO | not waivable |
| 10 | TLS / secure transport | P | No TLS termination anywhere (RL-C2) | TLS/termination evidence in production context | INFRA-G1 | P10-SEC1 boundaries | NO | YES | via GO | not waivable |
| 11 | Security headers | A | `_SECURITY_HEADERS` on every response; HSTS deferred to deployment context | Header evidence now; HSTS reassessment at deployment (RL-C4) | HSTS → P | web/app.py | YES | YES | via GO | HSTS deferral already governed |
| 12 | Dependency/vulnerability scanning | A | P10-DEP1 point-in-time (0 findings; expires) | Fresh audit re-run at execution time (RL-C6) | none | scripts/run_dependency_audit.py | YES | YES | via GO | fresh run mandatory |
| 13 | Third-party dependency review | A | requirements.txt (11 pkgs) + tests/requirements-draft-l2.txt (test-only, un-audited note) | Review incl. the test-only declaration | none | P10-DEP1 evidence | YES | YES | via GO | registrable |
| 14 | Database/data security | A | Durable SQLite, BEGIN IMMEDIATE, fail-closed (RL-A9) | Review + suite evidence; production datastore topology → item 9 | topology → P | engine stores | YES | YES | via GO | topology half deferred |
| 15 | Data retention/deletion controls | A+L | Controls implemented (deactivation tombstone; project export); retention SUBSTANCE undecided (RL-D5/D6) | Technical control verification now; policy substance from adviser intake | L (adviser) | engine stores; OD-DR1 | YES (controls) | see §6 | YES (artifacts) | substance → risk register or GO-wait (§6) |
| 16 | Privacy/data-lifecycle verification | L | Regime applicability adviser-open (RL-D2/D3) | Verification against decided policy once adviser input accepted | L (adviser) | P10-LT1 lane | NO (substance) | see §6 | YES | risk register or GO-wait (§6) |
| 17 | Backup verification | P | Local capability drill-verified (P10-BR1); production form absent | Production backup evidence | INFRA-G1 | engine/backup_service.py + provider | NO (prod form) | YES | via GO | local evidence reusable |
| 18 | Restore verification | P | Local restore drill-verified | Production restore evidence | INFRA-G1 | same | NO (prod form) | YES | via GO | local evidence reusable |
| 19 | Disaster-recovery readiness | P | DR plan exists (docs/DISASTER_RECOVERY_PLAN.md); production DR unproven | Production DR assessment | INFRA-G1 | DR plan + provider | NO (prod form) | YES | via GO | registrable |
| 20 | Audit logging | A | access_audit implemented; retention/cleanup unresolved (item 26) | App-level review now | none | engine stores | YES | YES | via GO | see item 26 |
| 21 | Monitoring | P | NOT CLAIMED DELIVERED (PSRR §8; Audit ≠ Monitoring) | Provider-context monitoring evidence | provider selection (named gap §8 below) | P10-OB1 boundaries | NO | YES | via GO | preserved §25 item — assess before GO |
| 22 | Alerting | P | None (operational alerting listed in §8 preserved items) | Provider-context alerting evidence | same | same | NO | YES | via GO | same |
| 23 | Abuse controls | A+P | Auth-surface rate-limit floor only; broad controls NOT CLAIMED DELIVERED | Posture review now; production abuse posture with provider | prod half → P | web/app.py; PSRR §8 | partial | YES | via GO | preserved §25 item |
| 24 | Rate-limit review | A+P | Floor exists | Review now; production posture later | prod half → P | web/app.py | partial | YES | via GO | registrable |
| 25 | Distributed/credential-abuse review | A+P | App-level only | Review now; production posture later | prod half → P | same | partial | YES | via GO | registrable |
| 26 | Audit-retention operational policy | P+L | NOT CLAIMED SOLVED (PSRR §8); retention substance adviser-adjacent | Operational policy + provider context (+ §6 where substance is legal) | INFRA-G1 (+L) | ops lane | NO | YES | via GO | preserved §25 item |
| 27 | Incident-response readiness | A | P10-IR1 internal foundation (informs PSRR item 27, does not satisfy it — RL-B7) | Readiness assessment against the runbook | none | P10-IR1 | YES | YES | via GO | registrable |
| 28 | Production logging / sensitive-data handling | P | Data-minimized JSON logging seam (local) | Production logging evidence | INFRA-G1 | web/observability.py | NO (prod form) | YES | via GO | registrable |
| 29 | External-integration security (where applicable) | A | Current integrations: advisory-only `engine/ai_advisor.py` vendor HTTP (recorded LOW nuance); dev email sink | Review now; production integrations reassessed when they exist | prod form → P | engine/ai_advisor.py; engine/email_sender.py | YES | YES | via GO | registrable |
| 30 | Vendor/third-party integration security (where applicable) | A+P | None selected (vendor-neutral) | Assess as vendors are later selected | provider gates | future | YES (current: n/a evidence) | YES | via GO | registrable |
| 31 | Infrastructure/deployment configuration | P | None exists | Real infrastructure config review | INFRA-G1 + deployment gate | future | NO | YES | via GO | not waivable |
| 32 | Environment/secrets separation | P | None exists | Environment separation evidence | INFRA-G1 | future | NO | YES | via GO | not waivable |
| 33 | Security testing | A | 2951-test suite + universal guardrail smoke + targeted security suites | Execution-time evidence run | none | tests/; scripts/run_universal_smoke.py | YES | YES | via GO | fresh run mandatory |
| 34 | Penetration testing where risk warrants | P | Not performed | Risk determination + production-like environment where warranted | INFRA-G1 (env) | PSRR executor | NO | per risk determination | via GO | risk-based per §7 wording |
| 35 | Release evidence package | F | Does not exist | Assemble §9 evidence classes incl. outstanding-risk register | items 1–34 | PSRR executor | NO (last) | YES | via GO | — |
| 36 | Independent security/release review | F | Not performed | §10 independent verification (existing model) | item 35 | independent reviewer | NO (last) | YES | via GO | — |
| 37 | Formal GO / NO-GO decision | D | No GO exists | Recorded GO/PASS or NO-GO/FAIL | items 1–36 | Owner + gate record | NO (last) | — | **GO required for deployment** | — |

## 5. Tranche summaries

**5.1 Application-layer tranche (EXECUTABLE IMMEDIATELY once execution is authorized —
no hosting, region, payment provider, tax conclusion, or deployment needed):** items 1–7,
8(app half), 11(headers), 12, 13, 14(app half), 15(controls half), 20, 23–25(app halves),
27, 29, 30(current-state), 33. Executable security/readiness work is NOT deferred because
provider items remain open.

**5.2 Provider-dependent tranche (needs real production context; providers NOT selected
here):** items 9, 10, 17–19(production form), 21, 22, 26, 28, 31, 32, 34(environment), plus
the production halves of 7–8, 14, 23–25, and the HSTS reassessment of item 11. Evidence
dependency: the facts produced by the infrastructure lane (§8). Sequencing: fully parallel
with §5.1; must complete before items 35–37.

**5.3 Policy/legal-dependent items:** 15(substance), 16, 26(where substance is legal) —
treatment in §6. **5.4 Final:** 35–36. **5.5 Decision:** 37.

## 6. Legal/policy dependency treatment (no legal conclusions invented)

- **Technically verifiable NOW:** the implemented controls (deactivation tombstone
  semantics, project-scoped export, access-audit capture, fail-closed stores).
- **Policy substance still unresolved (adviser-open):** retention durations (LQ/RL-D6),
  erasure policy substance (RL-D5), regime applicability (RL-D2/D3), account-wide access
  scope (RL-D4).
- **Outstanding-risk-register eligible:** unresolved substance MAY enter the §9
  outstanding-risk register with accepted-risk/waiver records "where governance permits" —
  determining WHETHER governance permits a given waiver is itself part of item 35/36/37 and
  is NOT pre-decided here.
- **Must be resolved before PSRR GO:** any item-15/16 element the §36 independent review
  or §37 decision refuses to carry as an open risk. This contract does not pre-judge that.
- **Blocks DEPLOYMENT regardless of PSRR:** the legal artifacts themselves (Privacy
  Policy/Terms/consent — RL-D1) and OD-A brand clearance — deployment-lane blockers even
  after a PSRR GO.

## 7. GO / NO-GO model (registration §6 preserved verbatim)

Only a recorded **PSRR = GO/PASS** — together with OD-P's separate deployment-gate
completion and explicit Owner deployment authorization — may remove the public-production
block; **NO-GO/FAIL leaves the block in force**. Nothing in this contract weakens the GO
bar, and no tranche completion, evidence volume, or partial result substitutes for the §37
formal decision.

## 8. Infrastructure-gate relationship (exact scopes; NOTHING selected here)

- **OD-J2 §3.2 delegated infrastructure gate — exact scope: hosting provider + production
  region ONLY** (the selection "of the initial provider and production region is DELEGATED
  TO A LATER, SEPARATELY AUTHORIZED INFRASTRUCTURE GATE" — OD-J1/J2 record §3.2). May be
  opened in parallel with §5.1 execution; must deliver its facts before §5.2 completes.
- **Named governance gap (identified, NOT opened, NOT selected):** TLS/proxy termination
  (P10-SEC1 boundary owner), monitoring/alerting provider (P10-OB1 boundary owner),
  production backup provider (P10-BR1 boundary owner), and email provider
  (`engine/email_sender.py` dev-sink boundary) have canonical BOUNDARY owners but **no
  dedicated named selection/configuration gate**. PSRR-C1 registers the need for one —
  proposed name **INFRA-G1 — Production Infrastructure Selection & Configuration Gate** —
  scoped to carry the OD-J2 §3.2 core (hosting + region) plus these adjacent surfaces
  under their existing owners, each selection separately Owner-authorized. Payment/MoR
  selection is explicitly OUTSIDE INFRA-G1 (commercial lane; OD-CJ1 §8–§9; P8-I4 port).

## 9. Separations (all preserved verbatim)

- **PSRR execution:** NOT AUTHORIZED and NOT STARTED by this contract; requires separate
  explicit Owner authorization against this frozen contract.
- **Deployment:** OD-P two-part control (deployment gate + explicit Owner deployment
  authorization) — untouched; DEPLOYMENT AUTHORIZED: NO.
- **Paid activation:** `D-P8-PL-01 class C` hard block — untouched; PAID ACTIVATION
  AUTHORIZED: NO. A FREE first public release remains structurally permitted by current
  authority but skips nothing in §6/§7 (per the authoritative FR-GS1 determination).
- **Future domains:** DOMEX-D1 and all domain contracts remain deferred until after first
  release; OD-H order unchanged.

## 10. Review path

LEVEL 2 governance-only candidate (zero runtime/test/schema/guardrail diff) under LEAN
§3/§4; Independent External Review mandatory per §5B.13 (source-of-truth, exact SHA/bundle,
scope, contradictions, authority/supersession, completeness, Reviewer Grill, PLUS the
mandatory independent Universal Guardrail Smoke); no mechanical full-suite rerun absent a
§5B.6 trigger; no silent tier change (§5B.14).
