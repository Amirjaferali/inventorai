# INFRA-G1-C — Production Infrastructure & Provider Selection Contract

## 0. Record identity (file-creation rules)

```text
File path:        docs/governance/INFRA_G1_C_PRODUCTION_INFRASTRUCTURE_PROVIDER_SELECTION_CONTRACT.md
Purpose:          the governance contract for the OD-J2 §3.2 delegated infrastructure
                  gate (hosting provider + production region) PLUS selection/
                  configuration COORDINATION for the adjacent production surfaces
                  (TLS/proxy, monitoring/alerting, backup/restore, email,
                  secrets/logging operations); registration of OPS-SM1.
Input contract:   OD-J1/OD-J2 record §3.2 (exact delegated scope); PSRR-C1 §5.2/§8
                  (provider-dependent tranche + named governance gap); the
                  authoritative Infrastructure/Provider Tranche Reconstruction
                  (Owner-accepted); P10-SEC1 / P10-OB1 / P10-BR1 boundary records;
                  RL checklist rows; D-P8-PL-01 class C; OD-P; PSRR registration.
Output contract:  selection CRITERIA and evidence obligations only. Selects NO
                  provider; provisions NOTHING; implements NOTHING; marks NO PSRR
                  item PASS. Every actual selection is a separate future Owner
                  decision under this contract.
Prohibited:       naming/choosing/evaluating a specific provider without separate
                  Owner authorization; expanding or rewriting OD-J2; duplicating or
                  replacing any canonical boundary owner; pulling payment/MoR/
                  pricing/tax/commercial matters in; creating retention/legal/policy
                  substance; authorizing code changes; executing OPS-SM1; implying
                  PSRR GO, deployment, or paid activation.
Status:           GOVERNANCE-ONLY CANDIDATE (authoritative only if/when merged and
                  post-merge verified).
Base:             88c5f4d5d3d3a5afb508b5f26852fd9e13d7ece9 (PR #541 merge — PSRR
                  application-layer recording, authoritative).
```

## 1. Authority boundary

- **OD-J2 §3.2 core (preserved exactly, not expanded):** "The selection of the initial
  provider and production region is DELEGATED TO A LATER, SEPARATELY AUTHORIZED
  INFRASTRUCTURE GATE." THIS contract is that gate's contract for the two delegated
  decisions: **hosting provider + production region — nothing more is added to OD-J2.**
- **Adjacent surfaces — coordination only.** For TLS/proxy, monitoring/alerting,
  backup/restore, email, and secrets/logging operations, this contract defines
  selection/configuration criteria ONLY. The canonical boundary owners remain: P10-SEC1
  (TLS/proxy/security boundaries), P10-OB1 (observability), P10-BR1 (backup/restore),
  the `engine/email_sender.py` dev-sink boundary record (email), RL-C1/PSRR §8 (secrets
  posture), and the observability/ops surfaces (logging). INFRA-G1-C is NOT a boundary
  authority and never overrides those records.
- **Out of scope (binding):** payment provider; Merchant of Record; pricing; invoicing;
  paid activation; tax implementation; commercial charging; production deployment
  authorization (OD-P two-part gate unchanged); legal/policy conclusions; future
  domains. Payment/MoR stays in the commercial lane (OD-CJ1 §8–§9; P8-I4 port).

## 2. Provider-surface matrix

Legend: every surface blocks PSRR GO indirectly (its dependent items cannot close
without it) and blocks deployment via GO; "Owner dec." = each actual selection is a
separate future Owner decision; all surfaces may be selected in parallel EXCEPT that
TLS/proxy, monitoring, backup, and email selections depend on (or are constrained by)
the hosting/region decision and should not finalize before it.

| Surface | Canonical owner | Why needed | Dependent PSRR items | Evidence before acceptance | Owner dec.? | Parallel? |
|---|---|---|---|---|---|---|
| Hosting provider + production region | OD-J2 §3.2 (this gate) | Every production fact hangs on it | 9, 14-prod, 17–19, 21–22, 26, 28, 31, 32, 34-env | Criteria table §3 satisfied + documented evaluation + exit path | **YES** | First — others follow it |
| TLS / reverse proxy | P10-SEC1 boundaries | Items 10/11; Secure cookies; edge posture | 10, 11 (HSTS reassessment), 23–25 edge | §4 posture evidence | YES | After/with hosting |
| Monitoring / alerting | P10-OB1 | Items 21–22; OPS-SM1 alert delivery | 21, 22, 28 (sink) | §5 evidence | YES | After/with hosting |
| Production backup / restore | P10-BR1 | Items 17–19 | 17, 18, 19 | §6 evidence (retention values remain policy-open) | YES | After/with hosting |
| Production email | email dev-sink boundary | Verified-email flows in production; notifications | production posture of 29; deployment-lane need | §7 evidence | YES | After/with hosting |
| Secrets / logging operations | RL-C1 / PSRR §8; P10-OB1 (logging) | Items 7-prod, 8-prod, 26, 28, 32 | 7-prod, 8-prod, 26, 28, 32 | §8 evidence | YES (procedures acceptance) | With hosting environments |

Shared criteria applying to EVERY surface: security requirements (transport encryption,
access control, least privilege); data/region requirements (consistent with the chosen
region; NO data-location commitment is created here — OD-J1/J2 preserved); exit/
portability requirements (documented export/migration path; no proprietary lock-in
without a recorded exit strategy); lock-in risk explicitly assessed and recorded; cost
transparency; sensitive-data minimization (nothing beyond the data-minimized surfaces
already governed).

## 3. Hosting / region selection criteria (minimum; no provider named)

Region availability; data-residency implications (recorded as FACTS for the future
legal intake — no residency conclusion drawn here); persistent storage capability
(sufficient for the canonical SQLite topology; any topology divergence is a
possible-code diagnostic gate, §9); TLS termination support; secret storage facility;
monitoring integration; backup capability (scheduling + offsite option); logging
capability; network controls; rollback/deployment support; vendor lock-in/portability
(documented export/migration path REQUIRED); cost transparency; operational
reliability; export/migration path evidence. Acceptance evidence: a written evaluation
against every criterion, the exit path, and the Owner's recorded selection decision.

## 4. TLS / proxy requirements

Production HTTPS posture: all public traffic TLS-terminated; termination responsibility
assigned (provider edge or governed proxy); trusted-proxy boundary explicitly
configured before any forwarded-header trust (P10-SEC1 §12 boundary preserved —
currently deliberately no proxy trust); `SESSION_COOKIE_SECURE` becomes effective via
the existing production gate; **HSTS reassessment trigger = trusted HTTPS/proxy context
exists** (RL-C4; adoption would be a separately authorized possible-code change, §9).
Evidence for PSRR items 10/11: termination config, forwarded-header trust config,
redirect posture, cookie-flag verification, HSTS determination record.

## 5. Monitoring / alerting requirements

Health monitoring consuming the existing `/health` surface; error visibility;
structured JSON log ingestion (existing data-minimized seam); alert thresholds and
routing to the P10-IR1 escalation path; retention awareness (values remain policy-open);
sensitive-data minimization in transported logs; documented escalation path. P10-OB1
remains the boundary owner; integration code, if any proves necessary, is a
possible-code diagnostic gate (§9).

## 6. Backup / restore / DR requirements

Scheduled production backups of the durable stores; encrypted storage where applicable;
restoration testing in the production context (production drill evidence, extending the
P10-BR1 local drill); recovery evidence; DR evidence against
`docs/DISASTER_RECOVERY_PLAN.md`; **retention dependency: schedule/retention VALUES
remain policy-open (RL-B4/RL-D6) — this contract consumes the future policy decision
and creates none**; provider portability (backups restorable outside the provider).

## 7. Production email requirements

Defined separately from the current dev-sink (which remains the truthful non-production
state): verified sender/domain; secret handling via the secrets facility; delivery-
failure behavior that never blocks core flows silently; bounce/abuse handling where
applicable; monitoring of delivery; privacy/data minimization (recipient + minimal
content only); vendor portability.

## 8. Secrets / logging operations requirements

Secret storage in the hosting secrets facility; documented rotation procedure +
emergency rotation; access control/least privilege; environment separation
(dev/production isolation — PSRR item 32); production log sink with sensitive-data
handling review (item 28); auditability of secret access where the facility supports
it. RL-C1 and P10-OB1 ownership preserved; procedures are evidence/operational
artifacts, not code.

## 9. Possible-code diagnostic gates (carried forward; NOTHING authorized here)

For EACH of: item 9 production serving posture; item 11 HSTS adoption; item 14
production datastore topology (only if divergence from canonical SQLite is ever
proposed); items 21/22 provider-integration seam; item 26 audit-retention cleanup
mechanism; item 31 deployment tooling; broad abuse controls if edge controls prove
insufficient (items 23–25):

```text
DIAGNOSIS REQUIRED BEFORE CODE:              YES
SEPARATE OWNER IMPLEMENTATION AUTHORIZATION: REQUIRED
```

No runtime change of any kind is authorized by INFRA-G1-C.

## 10. OPS-SM1 registration (registered — NOT executed, NOT implemented)

**OPS-SM1 — SECURITY MAINTENANCE & VULNERABILITY MONITORING OPERATIONS GATE.**
Owner principle (binding for the future gate): automated security/dependency
detection where practical; alerting when action is needed; NO automatic production
dependency/code changes without validation; safe-environment testing first; governed
release after validation (GOV-RBR1 lifecycle); PSRR revalidation only when
governance/risk requires. Existing foundation it builds on (nothing added now):
`scripts/run_dependency_audit.py` (point-in-time by design), RL-C6 freshness
obligation, the full suite + Universal Guardrail Smoke as the validation harness, the
P10-IR1 runbook as the alert-response path. Dependencies: INFRA-G1 facts (scan
execution environment; monitoring/alerting provider; email provider). Sequencing:
successor gate after INFRA-G1 facts exist; **operational no later than the first
public production deployment unless a later authoritative Owner decision changes that
timing**. This candidate builds no scheduling, automation, alerts, or monitoring.

## 11. Policy / legal separation

Retention substance, erasure/privacy regime, legal artifacts, and all adviser-dependent
answers remain OPEN in their lanes (P10-LT1). This contract CONSUMES future policy
decisions where its surfaces depend on them (backup schedule/retention; log/audit
retention) and CREATES none.

## 12. PSRR dependency mapping and state preservation

Surface→item mapping as in §2. Preserved verbatim: APPLICATION-LAYER TRANCHE:
AUTHORITATIVE EVIDENCE; PSRR COMPLETE: NO; PSRR GO ELIGIBLE: NO. **No provider-dependent
PSRR item becomes PASS because this contract exists** — actual provider/environment
evidence must be produced at execution time under the PSRR-C1 evidence model. Free
release / paid separation preserved: FREE PUBLIC RELEASE REQUIRES PAYMENT PROVIDER: NO;
PAID ACTIVATION REQUIRES PAYMENT/MoR: YES (`D-P8-PL-01 class C` + commercial lane).

## 13. Observation carry-forward

Preserved open, none silently resolved: PSRR-C1-N1/N2/N3; REV-REC-O1/O2/O3;
application-layer OBS-1…OBS-4 residuals (OBS-5 resolved in the recording);
GAP-SYNC-01-NB1/NB2; PC3-N2; the nine tranche residual-risk entries.

## 14. Review path

LEVEL 2 governance-only candidate (zero runtime/test/schema/guardrail diff) under LEAN
§3/§4; Independent External Review mandatory per §5B.13 (incl. the mandatory
independent Universal Guardrail Smoke); no mechanical full-suite rerun absent a §5B.6
trigger; no silent tier change (§5B.14).
