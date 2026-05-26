# Data Retention Policy
Status: APPROVED

## Data Inventory
Invention descriptions: In-memory session store YES sensitive
Clarification responses: In-memory session store YES sensitive
Session state: In-memory session store YES sensitive
Audit logs: Log files NO
Benchmark fixtures: tests/replay/cases/ NO
Benchmark results: benchmark/ NO

## Retention Schedule
In-memory sessions: Until server restart (automatic)
Audit DEBUG: 7 days
Audit INFO/WARN/ERROR: 30 days
Audit AUDIT events: 365 days minimum
Benchmark fixtures: Indefinite (git controlled)
Benchmark results: 90 days

## High Priority
benchmark/results_20260520_074904.json MUST be committed before Codespace reset (R-004)

## Privacy
1. Invention descriptions are user IP must not be used for retraining
2. Anthropic API receives descriptions governed by API ToS
3. No PII collected in MVP. GDPR/PDPL review required before adding accounts
