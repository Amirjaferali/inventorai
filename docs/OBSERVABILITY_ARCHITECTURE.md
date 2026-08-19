# Observability Architecture
Status: APPROVED (truth-labeled per P10-OB1 — each section below is classified;
nothing in a HISTORICAL/TARGET section is implemented unless a section says so)

## IMPLEMENTED NOW (P10-OB1 — provider-neutral local foundation)

- Health/readiness surface: `GET /health` (web/app.py) — one deterministic,
  unauthenticated, session-free, side-effect-free, data-minimized endpoint
  answering whether the required LOCAL runtime dependencies are usable:
  200 `{"database": "ok"|"uninitialized", "status": "ok"}` or
  503 `{"database": "error", "status": "unavailable"}`. The probe never
  creates a file/schema/row (initialized stores probed via public read-only
  reads; an existing DB file opened strictly read-only; a missing file is the
  normal lazy pre-first-use state). Local health is NOT production, security,
  legal, PSRR, or deployment readiness, and is no authorization signal.
- Structured operational-logging seam: `web/observability.py` — stdlib
  `logging` only; JSON lines (stable keys `ts`/`level`/`event` + allowlisted
  fields) on the framework-default stream; strict field ALLOWLIST
  (`component`, `outcome`, `error_class`, `detail_code`, `count`,
  `duration_ms`) with per-field value grammars so emails, free-form user
  text, paths, IPs, session identifiers, and common secret shapes can never
  pass; `emit()` never raises. Event coverage is deliberately minimal
  (health-probe failure category today; new events are governed code changes).
- Data-minimization boundary (binding, verified by tests): no IP, user-agent,
  device/network metadata, geography, email, user/project content, password,
  token, session ID, or API credential is collected or emitted; no analytics,
  no behavioral tracking, no third-party telemetry, no provider SDK.
- Distinct existing layer (NOT part of this logging seam, preserved
  unchanged): durable security/commercial audit tables in
  `engine/account_store.py` (`access_audit`, `commercial_audit`,
  `subscription_lifecycle_events`, …) — domain/security/commercial evidence.
  Operational logs are runtime diagnostics; the two are not duplicated.

## NOT DECIDED / NOT IMPLEMENTED BY P10-OB1 (deferred boundaries)

- Log destination, retention duration, rotation, archival, aggregation/SIEM:
  NOT decided (provider- and legally-relevant; framework-default local stream
  is the only current behavior).
- Metrics system, dashboards, alerting, error-tracking service, paging:
  NOT implemented; provider-dependent, future infrastructure-gated work.
- Live production monitoring: DOES NOT EXIST. The P10-C §4
  monitoring/observability obligation is therefore
  `PARTIAL — PROVIDER-NEUTRAL FOUNDATION IMPLEMENTED`, not complete.
- PSRR items 20–22/28 (audit logging, monitoring, alerting, production
  logging/sensitive-data handling) remain FUTURE VERIFICATION at the PSRR
  gate — nothing here satisfies or executes PSRR.

## HISTORICAL / TARGET DESIGN (pre-Phase-4 draft — NOT implemented; retained
## as future design input only; each item requires revalidation and separate
## authorization before any implementation)

### Log Format (historical draft)
{timestamp_iso} | {level} | {session_id} | {component} | {event} | {payload_json}
(Note: a `session_id` log field would violate the current P10-OB1
data-minimization boundary as applied to operational logs; any future use
requires explicit re-decision.)

### Log Levels / retention (historical draft — retention is NOT decided; see above)
DEBUG 7 days / INFO-WARN-ERROR 30 days / AUDIT 365 days

### 21 Metrics (historical draft — none implemented)
M-01 inv_sessions_total Counter
M-02 inv_sessions_active Gauge
M-03 inv_iterations_total Counter
M-04 inv_verdict_pass_total Counter
M-05 inv_verdict_warn_total Counter
M-06 inv_verdict_block_total Counter
M-07 inv_transition_l0_l1_total Counter
M-08 inv_transition_l1_l2_total Counter
M-09 llm_call_latency_ms Histogram
M-10 llm_call_total Counter
M-11 llm_call_error_total Counter
M-12 llm_tokens_input_total Counter
M-13 llm_tokens_output_total Counter
M-14 llm_schema_validation_fail_total Counter
M-15 inv_gap_open_total Counter
M-16 inv_gap_resolved_total Counter
M-17 inv_session_duration_s Histogram
M-18 inv_domain_detection_total Counter
M-19 web_request_latency_ms Histogram
M-20 web_request_error_total Counter
M-21 inv_cost_usd_total Counter
(LLM-related metrics are additionally moot while AI advisory transfer is
disabled in code.)

### 20 Audit Events (historical draft — none implemented as log events; the
### durable DB audit tables above are a separate, real mechanism)
AE-01 session.created
AE-02 session.ended
AE-03 iteration.started
AE-04 iteration.completed
AE-05 verdict.pass
AE-06 verdict.warn
AE-07 verdict.block
AE-08 transition.attempted
AE-09 transition.approved
AE-10 transition.denied
AE-11 gap.opened
AE-12 gap.partial
AE-13 gap.resolved
AE-14 llm.called
AE-15 llm.responded
AE-16 llm.error
AE-17 schema.valid
AE-18 schema.invalid
AE-19 domain.detected
AE-20 cost.recorded
