# Observability Architecture
Status: APPROVED

## Log Format
{timestamp_iso} | {level} | {session_id} | {component} | {event} | {payload_json}

## Log Levels
DEBUG 7 days / INFO-WARN-ERROR 30 days / AUDIT 365 days

## 21 Metrics
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

## 20 Audit Events
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
