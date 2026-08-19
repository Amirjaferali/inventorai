# Phase 10 — Internal Technical Incident Response Runbook (P10-IR1)

**Status:** AUTHORITATIVE INTERNAL RUNBOOK (candidate until merged and post-merge verified).
**Scope:** INTERNAL OPERATIONS ONLY — detection, classification, containment, evidence preservation,
diagnosis, recovery, verification, escalation, and closure of TECHNICAL incidents. This is NOT a
customer-facing support policy, NOT a service-level commitment, NOT a legal/breach-notification procedure,
and it creates no customer-facing promise of any kind.
**Base at authoring:** `ee93371808803c488eeba59bf83fcfbb20fccc2a` (PR #522 merge — P10-SEC1, authoritative).
**Structural invariants:** enforced by `tests/test_p10_ir1_incident_runbook_structure.py`.

A future agent must be able to run an incident from this document alone, without chat history.

---

## §1. What is a technical incident

A **technical incident** is a confirmed or reasonably suspected condition in which the application, its
durable data, or its security controls are not behaving as the authoritative repository says they must.
Qualifying examples:

* application unavailable or failing to serve;
* `/health` reporting `"database": "error"` (503) unexpectedly;
* unexpected repeated server errors (5xx) on normal flows;
* suspected unauthorized access to an account, project, or credential;
* suspected exposure of a secret (Flask secret, API credential, password hash, reset/verification token);
* corrupted, missing, or inconsistent durable SQLite database;
* backup or restore failure (`engine/backup_service.py` validation/parity failure);
* security-control bypass (CSRF, session validation, ownership isolation, security headers absent);
* critical data-integrity inconsistency (e.g., cross-table ownership mismatch);
* operational-logging failure that materially impairs diagnosis of one of the above.

NOT technical incidents (never classified here): ordinary product questions, feature requests, usability
complaints, billing disputes, pricing questions, and legal inquiries. Legally significant *requests*
(data access/portability/erasure demands) are NOT incidents either — they follow the accepted OD-DR1/OD-DR2
escalation rules directly.

## §2. Severity model

Four internal levels. Qualitative urgency only — this model deliberately contains **no response-time
clock, no resolution deadline, and no customer commitment** of any kind.

### SEV-1 — critical
* **Triggers:** confirmed loss/corruption of durable data with no verified recovery yet; confirmed
  unauthorized access to another user's data; confirmed secret exposure; total sustained unavailability.
* **Examples:** durable DB fails `PRAGMA quick_check` and the only backup fails validation; a proven
  ownership-isolation bypass; the Flask secret committed or published.
* **Required internal action:** stop all non-incident changes immediately; contain (§6); preserve evidence
  (§4.4) before any recovery attempt; begin diagnosis with the most senior available operator as Incident
  Coordinator.
* **Escalation:** Owner notified immediately, always. Legal/privacy dimension → §10, always evaluated.
* **Closure evidence:** verified recovery (tests + parity/health evidence), root cause documented, Owner
  sign-off recorded, evidence record complete.

### SEV-2 — major
* **Triggers:** material capability broken with a workaround or bounded impact; suspected (unconfirmed)
  security exposure; single-user data-integrity fault; repeated 5xx on a core flow.
* **Examples:** `/health` red on a real dependency failure; export producing wrong-owner denial errors for
  a legitimate owner; a security header missing from responses.
* **Required internal action:** contain; preserve evidence; diagnose before patching (classification before
  correction — repository rule); fix through the normal governed candidate flow unless containment
  requires an immediate bounded operational action.
* **Escalation:** Owner notified before any state-changing recovery beyond containment; §10 evaluated when
  personal data may be involved.
* **Closure evidence:** passing focused + full test suites, verified behavior, evidence record complete.

### SEV-3 — minor
* **Triggers:** degraded non-core behavior; recoverable operational fault; failed backup validation with a
  healthy source still intact.
* **Examples:** operational-logging seam emitting nothing (diagnosis impaired); a stale governance surface
  discovered mid-operation.
* **Required internal action:** record, classify, schedule the fix through the normal governed gate flow.
* **Escalation:** reported to the Owner in the normal course of work; immediate notification not required
  unless it risks growing into SEV-2.
* **Closure evidence:** fix merged or explicitly deferred with rationale; evidence record complete.

### SEV-4 — informational
* **Triggers:** near-miss, anomaly without impact, or lesson-learned observation.
* **Examples:** a test flake traced to harness, not product; an adversarial-probe finding already blocked
  by an existing control.
* **Required internal action:** record briefly; no containment needed.
* **Escalation:** none required beyond the record itself.
* **Closure evidence:** the record itself, with a one-line disposition.

If in doubt between two levels, classify at the higher level until diagnosis says otherwise.

## §3. Roles (truthful — no invented staff)

The actual operating team today is the **Owner** plus **governed execution agents/operators**. Role
semantics, not job titles:

* **Incident Coordinator** — whoever is running the incident (today: the executing governed agent or the
  Owner). Owns classification, the evidence record, and stage discipline. Exactly one at a time.
* **Owner escalation** — the Owner is the sole authority for: authorizing state-changing recovery beyond
  containment, customer communication (§11), anything touching accepted decisions, and closure of SEV-1.
* **Executor/engineer** — performs containment/diagnosis/recovery steps (may be the same person/agent as
  the Coordinator; say so in the record).
* **Reviewer/verification** — for SEV-1/SEV-2 recovery, an independent review of the fix follows the
  repository's existing independent-review model where material claims require independence.

## §4. Response flow

```
DETECT → CLASSIFY → CONTAIN → PRESERVE EVIDENCE → DIAGNOSE → RECOVER → VERIFY → CLOSE / ESCALATE
```

1. **DETECT** — a §5 signal fires or a person observes a §1 condition. Open an evidence record (§12)
   immediately with an incident ID (§13).
2. **CLASSIFY** — assign a severity (§2) and an incident type (availability §8 / database §7 / security §9
   / other). Classification before correction: no patching before the failure class is understood.
3. **CONTAIN** — apply §6 actions only. Containment never includes irreversible destruction of state.
4. **PRESERVE EVIDENCE** — before recovery: record the exact repository SHA in use, copy (never move) the
   affected database/files to an isolated path, capture relevant operational-log lines and audit rows,
   capture failing test/probe output. Never copy secrets or unnecessary personal data into the record.
5. **DIAGNOSE** — trace to root cause using repository truth; classify the drift/defect before fixing
   (existing engineering method). If the root cause cannot be established, say so explicitly.
6. **RECOVER** — through the matching path (§7/§8/§9). State-changing recovery beyond containment requires
   Owner authorization (SEV-1/SEV-2 always).
7. **VERIFY** — prove recovery: focused tests, full suite where code changed, `/health` green, parity
   checks for data recovery. Verification evidence goes in the record.
8. **CLOSE / ESCALATE** — close only per §14; escalate per §2 and §10 whenever criteria are met.

## §5. Detection / signal sources (real signals only)

Signals that EXIST today: the P10-OB1 `GET /health` surface (`ok` / `uninitialized` / `error`); the P10-OB1
operational-logging seam (`web/observability.py`, e.g. `health.db_probe_failed`); the durable audit tables
(`access_audit`, `commercial_audit`, lifecycle tables); test-suite failures; P10-BR1 backup/restore
validation or parity failures (`engine/backup_service.py`); manual operator observation; user-reported
outage/error reaching the Owner.

Signals that DO NOT exist (must never be assumed or claimed): metrics, dashboards, automatic alerting,
paging, external monitoring providers, log aggregation, production telemetry of any kind.

## §6. Containment actions (existing mechanisms only — conceptual authorization, not production execution)

* stop further risky/non-incident changes immediately;
* record and preserve the exact SHA/state in use;
* preserve logs/audit/evidence before anything else changes;
* revoke a compromised account's sessions via the EXISTING `increment_session_epoch` seam, and/or set
  account status via the EXISTING `set_status` seam (both status-gated fail-closed) — only with Owner
  authorization when the account is not the operator's own;
* isolate suspect database copies (copy to an isolated path; never investigate on the live file);
* stop using a suspect backup (quarantine the file; never delete it during an open incident);
* stop the local process where the operator runs it, if serving is itself the risk.

NOT available and NOT created here: a kill switch (none is implemented — a separate authorization would be
required to build one), deployment/rollback controls (no deployment exists), provider-level actions.

## §7. Database / persistence incident path (uses authoritative P10-BR1)

For suspected durable-DB corruption/loss (`INVENTORAI_DB_PATH` SQLite):

1. Preserve the affected original first, where safely possible: copy it to an isolated evidence path; do
   NOT run recovery on, or overwrite, the original during investigation.
2. Validate candidate backups with `validate_sqlite_database` (fail-closed `PRAGMA quick_check` + schema
   inventory).
3. Restore with `restore_database` to an ISOLATED NEW target — never directly onto the live path.
4. Verify with `database_parity_report` (schema + per-table row counts) and by opening the restored file
   through the normal repository stores; run the P10-BR1 suite where practical.
5. Repointing the application (`INVENTORAI_DB_PATH`) at a restored file happens ONLY after verification
   AND separate explicit Owner operational authorization, recorded in the evidence record.
6. Record exact backup/restore evidence (paths, validation output, parity result) in the record.

Truth boundaries: only LOCAL backup capability exists (P10-BR1); no production/offsite/scheduled backup
exists; this runbook creates no retention rule of any kind. Deep recovery procedures live in
`docs/DISASTER_RECOVERY_PLAN.md` Scenario 7 — this runbook coordinates, DR recovers (§16).

## §8. Availability / outage path (uses authoritative P10-OB1)

1. Probe `GET /health` and read it precisely: `"ok"` = local dependencies usable; `"uninitialized"` =
   normal lazy pre-first-use state, NOT a failure; `"error"`/503 = real local dependency failure.
2. Inspect bounded operational-log lines (e.g. `health.db_probe_failed` carries the exception class name
   only). Do NOT begin collecting new sensitive data (IPs, user agents, user content) to diagnose — the
   data-minimization boundary holds during incidents too.
3. Verify local DB state (read-only; §7 if suspect).
4. Classify the failure as app/runtime, durable-data, or environment/infrastructure-dependent, and record
   which.

Truth boundary: no production monitoring exists; availability observations come from the local surface,
tests, and human reports only.

## §9. Security incident path (uses authoritative P10-SEC1 + existing auth controls)

Qualifying suspicions: secret leakage; session/auth anomaly; account-isolation failure; security headers
unexpectedly missing (CSP/nosniff/X-Frame-Options/Referrer-Policy — P10-SEC1 seam); CSP bypass suspicion;
unauthorized API access; credential compromise.

Internal technical actions (in addition to §4/§6): preserve evidence first; verify the running code is the
authoritative SHA (unexplained divergence is itself evidence); revoke affected sessions/credentials through
the existing epoch/status seams (Owner authorization as in §6); verify the security-header set is present
on live responses (`tests/test_p10_sec1_security_headers.py` is the reference probe); run the focused
containment/security suites (`test_security_containment_r6_r16.py`, P5 auth suites); rotate an exposed
Flask secret by changing `INVENTORAI_SECRET_KEY` (this invalidates all signed cookies — record that
consequence). If personal data may be involved in ANY way → §10 immediately.

This runbook never determines whether an event is a legally significant "breach" — that word here is a
technical suspicion label only (§10).

## §10. Legal / privacy escalation boundary — MANDATORY

Whenever an incident may involve personal data, unauthorized access, data disclosure, deletion/loss of
user data, privacy rights, contractual notice, or regulatory reporting:

```
ESCALATE TO OWNER + QUALIFIED EXTERNAL COUNSEL WHEN AVAILABLE
```

Binding rules: the technical team does NOT determine legal applicability; no legal deadline is asserted by
this runbook; no regulator or customer notification is automatically sent — any such notification is an
Owner decision informed by counsel; evidence preservation continues throughout; the external legal input
register (P10-LT1, LQ-01…LQ-27) remains OPEN / DEFERRED PENDING EXTERNAL ADVISER AVAILABILITY, and no LQ
question is answered internally by an incident. The accepted OD-DR1/OD-DR2 escalation rules for legally
binding data-rights requests remain in force and are not modified here.

## §11. Customer communication boundary

```
CUSTOMER COMMUNICATION: OWNER-APPROVED ONLY
```

No final customer-facing outage/incident/breach template exists or is created here. Wording and timing of
any customer communication are potentially legal/commercial-policy sensitive and require Owner approval
(with counsel input where §10 applies). This runbook promises nothing to customers: no availability
percentage, no response or resolution timing, no refund, no compensation, no notification timing.

## §12. Incident evidence record (minimal, mandatory fields)

One record per incident, created at DETECT, stored as a Markdown file under
`docs/governance/evidence/incidents/` (created on first use). Fields:

```
Incident ID:                    (§13)
Detection timestamp (UTC):
Detecting signal:               (§5 source)
Severity:                       (SEV-1..SEV-4, with reclassifications logged)
Incident type:                  (availability / database / security / other)
Affected component(s):
Repository SHA in use:          (and deployed SHA if a deployment ever exists)
Symptoms (bounded, factual):
Containment actions taken:
Evidence references:            (isolated copies, log lines, audit rows, test output)
Backup/restore references:      (if §7 used: backup path, validation, parity result)
Verification evidence:
Current status:                 (OPEN / CONTAINED / RECOVERED / CLOSED / REOPENED)
Owner escalation:               (required? done? when?)
Legal/counsel escalation:       (§10 triggered? status — stays OPEN until external advice)
Closure rationale:              (§14)
```

Never place secrets, credential material, password hashes, tokens, or unnecessary personal data in an
incident record. Reference evidence by path/identifier instead of pasting sensitive content.

## §13. Incident ID

Format: `IR-YYYYMMDD-NN` (date of detection + two-digit sequence within that day). Implementation-neutral;
no database table, service, or schema is created for incident records — the documented evidence file is
the record. (A durable store for incidents would require a separate authorized gate.)

## §14. Closure criteria

An incident may be marked **technically closed** only when ALL hold: immediate containment complete;
technical root cause known OR explicitly documented as unresolved-with-rationale; recovery verified with
evidence; relevant tests/checks pass; no continuing unsafe condition is known; the evidence record is
complete; any required Owner escalation is done; and any §10 legal/privacy question is separately tracked
as OPEN until external advice — **technical closure is never legal closure**.

## §15. Reopen rule

A technically closed incident MUST be reopened when: the same symptom recurs; the recorded root cause is
disproven; recovery verification later fails; new evidence materially changes the impact assessment; or an
independent review identifies a missed material defect. Reopening reuses the same incident ID with a
`REOPENED` status entry and a fresh classification pass.

## §16. IR vs DR boundary

This runbook does NOT replace `docs/DISASTER_RECOVERY_PLAN.md`. **IR** owns detection, classification,
containment, escalation, evidence, and verification discipline; **DR** owns the concrete recovery
procedures (scenario steps, including Scenario 7 durable-database recovery). When recovery is needed, IR
invokes the relevant DR scenario and records the outcome. Neither document duplicates the other.

## §17. Truth classification and non-authorization (binding)

```
INTERNAL TECHNICAL INCIDENT RESPONSE: IMPLEMENTED   (this foundation — internal, provider-neutral)
CUSTOMER-FACING SUPPORT MODEL:        OPEN          (not closed by this gate)
LEGAL/PRIVACY INCIDENT NOTICE RULES:  OPEN — EXTERNAL COUNSEL REQUIRED
```

This runbook authorizes NO implementation, NO new runtime code, NO schema change, NO kill switch, NO
monitoring/alerting build, NO provider selection, NO deployment, NO PSRR execution (PSRR item 27 —
incident-response readiness — is assessed at the future PSRR gate, which this foundation informs but does
not satisfy by itself), and NO customer-facing artifact. Paid activation remains BLOCKED; deployment
remains NOT AUTHORIZED; the external legal/tax registers remain OPEN.
