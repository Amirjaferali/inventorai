"""P10-IR1 — Internal Technical Incident Response Runbook: structural invariants.

File: tests/test_p10_ir1_incident_runbook_structure.py
Purpose: deterministic structural validation of the authoritative internal
runbook `docs/governance/PHASE_10_INTERNAL_TECHNICAL_INCIDENT_RESPONSE_
RUNBOOK.md`. P10-IR1 changes NO runtime code (`RUNTIME CODE REQUIRED: NO`),
so these are repository-truth checks in the established doc-invariant test
convention — not artificial unit tests. They fail on any base where the
runbook is absent, and keep the load-bearing invariants from silently
regressing later.
Input contract: run under pytest from the repository root; reads the runbook
file only.
Output contract: every severity level carries its full structure; the three
authoritative foundations (P10-BR1 / P10-OB1 / P10-SEC1) are referenced; the
mandatory legal-escalation and customer-communication boundary language is
verbatim-present; no SLA/response-time/compensation/notification-deadline
promise pattern exists; no production-monitoring/offsite-backup claim exists.
Prohibited behaviors: MUST NOT weaken to pass; MUST NOT read chat history or
anything outside the repository.
"""
import os
import re

RUNBOOK = os.path.join(
    "docs", "governance",
    "PHASE_10_INTERNAL_TECHNICAL_INCIDENT_RESPONSE_RUNBOOK.md")


def _text():
    with open(RUNBOOK, encoding="utf-8") as fh:
        return fh.read()


def _severity_section(text, sev):
    match = re.search(r"### %s —(.*?)(?=\n### |\n## )" % sev, text, re.S)
    assert match, "missing severity section %s" % sev
    return match.group(1)


def test_runbook_exists():
    assert os.path.isfile(RUNBOOK)


def test_every_severity_has_full_structure():
    text = _text()
    for sev in ("SEV-1", "SEV-2", "SEV-3", "SEV-4"):
        section = _severity_section(text, sev)
        for required in ("**Triggers:**", "**Examples:**",
                         "**Required internal action:**", "**Escalation:**",
                         "**Closure evidence:**"):
            assert required in section, (sev, required)


def test_response_flow_stages_present():
    assert ("DETECT → CLASSIFY → CONTAIN → PRESERVE EVIDENCE → DIAGNOSE → "
            "RECOVER → VERIFY → CLOSE / ESCALATE") in _text()


def test_authoritative_foundation_references():
    text = _text()
    # database path → P10-BR1 seam and its real functions
    assert "engine/backup_service.py" in text
    assert "validate_sqlite_database" in text
    assert "restore_database" in text
    assert "database_parity_report" in text
    # availability path → P10-OB1 surface and seam, with truthful states
    assert "/health" in text
    assert "web/observability.py" in text
    assert '"uninitialized"' in text
    assert "health.db_probe_failed" in text
    # security path → P10-SEC1 and existing controls
    assert "P10-SEC1" in text
    assert "increment_session_epoch" in text
    assert "test_p10_sec1_security_headers.py" in text
    # IR/DR boundary
    assert "DISASTER_RECOVERY_PLAN.md" in text


def test_mandatory_boundary_language_verbatim():
    text = _text()
    assert "ESCALATE TO OWNER + QUALIFIED EXTERNAL COUNSEL WHEN AVAILABLE" in text
    assert "CUSTOMER COMMUNICATION: OWNER-APPROVED ONLY" in text
    assert "does NOT determine legal applicability" in text
    assert "no legal deadline is asserted" in text
    assert "technical closure is never legal closure" in text


def test_truth_classifications_present_and_separate():
    text = _text()
    assert "INTERNAL TECHNICAL INCIDENT RESPONSE: IMPLEMENTED" in text
    assert "CUSTOMER-FACING SUPPORT MODEL:        OPEN" in text
    assert "LEGAL/PRIVACY INCIDENT NOTICE RULES:  OPEN — EXTERNAL COUNSEL REQUIRED" in text


def test_no_sla_or_deadline_promise_patterns():
    text = _text()
    assert not re.search(r"\bSLA\b", text)
    # no availability-percentage promise
    assert not re.search(r"\b\d{2}(\.\d+)?\s*%", text)
    # no bounded response/resolution/notification clocks
    assert not re.search(
        r"within\s+\d+\s*(minute|hour|day|business)", text, re.I)
    assert not re.search(r"(respond|resolve|notify)\s+within", text, re.I)
    # "refund"/"compensation"/"uptime" may appear ONLY inside the mandated
    # boundary NEGATIONS ("no refund", "no compensation", …) — never as a
    # promise. Strip the negated phrases, then require the bare words gone.
    negation_stripped = re.sub(
        r"no\s+(refund|compensation|notification timing|availability)",
        "", text.lower())
    for forbidden in ("refund", "compensation", "uptime"):
        assert forbidden not in negation_stripped, forbidden
    assert not re.search(r"(will|shall|guarantee[ds]?)\s+"
                         r"(refund|compensat|respond|notify)", text, re.I)


def test_no_fictional_capability_claims():
    text = _text()
    # the runbook must state these do NOT exist, in its §5 negative list —
    # and must never name a monitoring/paging provider
    assert "Signals that DO NOT exist" in text
    for provider in ("pagerduty", "datadog", "sentry", "opsgenie",
                     "grafana", "cloudwatch"):
        assert provider not in text.lower(), provider
    # no offsite/production backup claim; P10-BR1 stays local-only
    # (whitespace-normalized: the source line wraps)
    assert ("no production/offsite/scheduled backup exists"
            in re.sub(r"\s+", " ", text))


def test_incident_id_format_and_no_new_schema():
    text = _text()
    assert "IR-YYYYMMDD-NN" in text
    assert "no database table" in text.lower()
