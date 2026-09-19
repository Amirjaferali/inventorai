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
promise pattern exists; no production-monitoring provider is named; and the §7
backup reality is asserted as CURRENT truth — an off-provider copy exists, the
daily scheduler is merged but neither deployed nor live-activated, and the
superseded "no offsite backup" claim survives only as labeled history.
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


def _current_backup_truth():
    """The §7 CURRENT truth block, excluding preserved historical quotations."""
    text = re.sub(r"\s+", " ", _text())
    start = text.find("**Current truth.**")
    assert start != -1, (
        "the §7 backup section must carry an explicit '**Current truth.**' "
        "block — a runbook an operator reads mid-incident may not leave its "
        "backup reality implicit")
    end = text.find("## §8", start)
    assert end != -1, "the current-truth block must end before §8"
    return text[start:end]


def test_backup_reality_asserted_as_current_truth():
    """The runbook must state the CURRENT backup reality, not merely retain the
    old absence claim.

    REPAIRED (v1.32 truth-guard repair). The previous guard asserted only that
    the phrase "no production/offsite/scheduled backup exists" was present
    somewhere in the file. Once an off-provider backup actually existed, that
    phrase survived as a correctly-labeled historical quotation and the guard
    kept passing while the runbook's live claim had changed underneath it —
    phrase presence, not truth. It now reads the explicit current-truth block
    and checks the facts an operator needs mid-incident, and the stale phrase is
    separately confined to superseded context by the test below.
    """
    current = _current_backup_truth()
    # what EXISTS — so nobody plans a recovery believing there is no copy
    assert "off-provider backup destination exists" in current
    assert "OD-INFRA-5" in current
    assert "live off-provider backup object exists" in current
    assert "full-loss disaster-recovery drill has passed" in current
    # the operator's entry point to that copy must be named
    assert "scripts/inventorai_offsite_backup.py" in current


def test_scheduler_never_presented_as_running():
    """Merged is not deployed; implemented is not activated.

    The dangerous failure here is the mirror of the old one: an operator
    assuming a recent automatic copy exists because scheduler code was merged.
    The runbook must say, in its current-truth region, that no scheduled run has
    occurred and that recency must be checked before anything is relied on.
    """
    current = _current_backup_truth()
    assert "MERGED, NOT DEPLOYED and NOT LIVE-ACTIVATED" in current
    assert "no scheduled run has ever occurred" in current
    assert "never assume a recent automatic copy exists" in current
    # and the restore authorization boundary is not softened by any of this
    assert "separate explicit Owner operational authorization" in current


def test_old_absence_claim_only_survives_as_labeled_history():
    """The superseded phrase stays visible — but never as a live claim."""
    text = re.sub(r"\s+", " ", _text())
    occurrences = list(re.finditer(
        r"no production/offsite/scheduled backup exists", text))
    assert occurrences, (
        "the superseded claim must stay visible as labeled history — deleting "
        "it would hide that the runbook once told operators otherwise")
    for match in occurrences:
        window = text[max(0, match.start() - 400):match.start()]
        assert "SUPERSEDED" in window, (
            "this phrase may appear ONLY inside preserved superseded text: %s"
            % text[max(0, match.start() - 200):match.end() + 80])


def test_incident_id_format_and_no_new_schema():
    text = _text()
    assert "IR-YYYYMMDD-NN" in text
    assert "no database table" in text.lower()
