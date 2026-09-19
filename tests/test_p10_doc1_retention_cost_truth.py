"""P10-DOC1 — Data-Retention & Cost-Governance truth-repair: structural invariants.

File: tests/test_p10_doc1_retention_cost_truth.py
Purpose: keep the load-bearing truths of `docs/DATA_RETENTION_POLICY.md` and
`docs/COST_GOVERNANCE_PLAN.md` from silently regressing, and tie the documents'
central claims to source truth so a future runtime change (enabling AI
transfer, adding a kill switch, adding a deletion path) cannot leave the
documents stale without failing here. P10-DOC1 changes NO runtime code —
these are repository doc-invariant checks in the established convention.
Input contract: run under pytest from the repository root; reads the two
documents plus the source files their claims cite.
Output contract: superseded claims stay labeled AND stay out of the current
sections; no prescriptive retention duration exists; retention substance stays
OPEN; disabled/absent controls are never claimed active; the cost plan's CURRENT
section states both halves of the real position (zero AI/billing spend, and the
provider costs that now exist uncontrolled by runtime code); cited source truth
still matches in both directions.
Prohibited behaviors: MUST NOT weaken to pass; MUST NOT decide any retention
rule or legal conclusion.
"""
import glob
import os
import re

RETENTION = os.path.join("docs", "DATA_RETENTION_POLICY.md")
COST = os.path.join("docs", "COST_GOVERNANCE_PLAN.md")


def _norm(path):
    with open(path, encoding="utf-8") as fh:
        return re.sub(r"\s+", " ", fh.read())


# ==========================================================================
# DATA_RETENTION_POLICY.md
# ==========================================================================
def test_retention_substance_declared_open():
    text = _norm(RETENTION)
    assert "RETENTION POLICY SUBSTANCE: OPEN — EXTERNAL LEGAL/TAX INPUT REQUIRED" in text
    assert ("No retention duration, deletion deadline, or erasure schedule "
            "is decided by this document." in text)


def test_no_pii_claim_only_as_labeled_superseded_history():
    text = _norm(RETENTION)
    idx = text.find("No PII collected")
    assert idx != -1, "the superseded claim must stay visible as labeled history"
    # every occurrence must sit inside a HISTORICAL — SUPERSEDED context
    for match in re.finditer(r"No PII collected", text):
        window = text[max(0, match.start() - 300):match.start()]
        assert "HISTORICAL — SUPERSEDED" in window
    # and the current truth is stated
    assert "Accounts exist and store personal data" in text


def test_in_memory_only_claim_superseded_and_durable_truth_present():
    text = _norm(RETENTION)
    assert "Durable SQLite" in text
    for match in re.finditer(r"In-memory session store", text):
        window = text[max(0, match.start() - 400):match.start()]
        assert "HISTORICAL — SUPERSEDED" in window
    # live in-memory working state is described truthfully, not as sole storage
    assert "in-memory `SESSION_STORE`" in _norm(RETENTION) or \
           "In-memory `SESSION_STORE`" in _norm(RETENTION)


def test_anthropic_transfer_claim_superseded_and_disabled_truth_present():
    text = _norm(RETENTION)
    for match in re.finditer(r"Anthropic API receives", text):
        window = text[max(0, match.start() - 200):match.start()]
        assert "HISTORICAL — SUPERSEDED" in window
    assert "AI_ADVISORY_ENABLED = False" in text
    assert "NO live external transfer" in text


def test_deactivation_never_equated_with_erasure():
    text = _norm(RETENTION)
    assert "DEACTIVATION ≠ PHYSICAL DELETION" in text
    assert "NO physical-erasure capability exists" in text
    assert "Deactivation only" in text


def test_no_prescriptive_retention_duration():
    text = _norm(RETENTION)
    assert not re.search(
        r"(retained for|kept for|deleted after|erased after|retention period of)"
        r"\s+\d", text, re.I)
    # the historical log-retention schedule stays labeled, never in force
    assert "no such rule is in force" in text


# The two automatic deletions the retention document names. Both are operational
# cleanups of non-user-content rows; the document must keep naming BOTH, and
# engine/ must contain no DELETE FROM for any other table. OD-INFRA-6 added the
# second (delivered outbox message removal); the guard's purpose - doc/source
# parity on automatic deletion - is unchanged, only its enumerated set grew.
_AUTOMATIC_DELETION_TABLES = ("auth_rate_limits", "email_outbox")


def test_retention_doc_matches_source_truth():
    # the "only automatic deletions" claim must keep matching source: DELETE
    # FROM appears in engine/ ONLY for the enumerated tables, and the document
    # names each of them.
    deletes = []
    for path in glob.glob(os.path.join("engine", "*.py")):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if "DELETE FROM" in line:
                    deletes.append((path, line.strip()))
    assert deletes, "expected the bounded rate-limit cleanup to exist"
    for path, line in deletes:
        assert any(table in line for table in _AUTOMATIC_DELETION_TABLES), (path, line)
    seen_tables = {table for table in _AUTOMATIC_DELETION_TABLES
                   if any(table in line for _p, line in deletes)}
    assert seen_tables == set(_AUTOMATIC_DELETION_TABLES), seen_tables
    with open(os.path.join("docs", "DATA_RETENTION_POLICY.md"), encoding="utf-8") as fh:
        doc = fh.read()
    assert "cleanup_expired_rate_limits" in doc
    assert "mark_email_delivered" in doc and "email_outbox" in doc
    # the 7-day client TTL claim must keep matching the real script
    with open(os.path.join("web", "static", "js", "local_draft.js"),
              encoding="utf-8") as fh:
        assert "TTL_MS = 7 * 24 * 60 * 60 * 1000" in fh.read()


# ==========================================================================
# COST_GOVERNANCE_PLAN.md
# ==========================================================================
def _current_cost_reality():
    """The 'Current cost reality' section, up to the HISTORICAL section."""
    text = _norm(COST)
    start = text.find("## Current cost reality")
    assert start != -1, "the plan must carry a current-cost-reality section"
    end = text.find("## HISTORICAL", start)
    assert end != -1, "the current section must end before the historical one"
    return text[start:end]


def test_cost_plan_current_reality_is_explicit():
    """The plan must state the CURRENT cost reality, not merely retain the old
    zero-cost claim.

    REPAIRED (v1.32 truth-guard repair). The previous guard asserted only that
    the phrase "There is NO live paid usage of any kind" appeared somewhere in
    the document. Once hosting and off-provider storage were actually
    provisioned, that phrase survived as a correctly-labeled historical
    quotation and the guard kept passing while the document's live claim had
    changed underneath it — it was checking phrase presence, not truth. It now
    reads the current section and checks both halves of the real position: what
    still costs nothing, and what now costs something.
    """
    current = _current_cost_reality()
    # --- still true: no metered AI spend, no billing of users, no monitoring
    assert "AI_ADVISORY_ENABLED = False" in current
    assert "AI token spend is zero" in current
    assert "no payment provider" in current
    assert "no live billing of users" in current
    assert "no hosted monitoring" in current
    # --- newly true: provider costs exist and must not be described as absent
    assert "Production hosting exists" in current
    assert "off-provider backup destination exists" in current
    assert "OD-INFRA-5" in current
    assert "OD-INFRA-6" in current
    assert "no longer runs only to a development sink" in current
    # --- unchanged and load-bearing: none of it is controlled by runtime code
    assert ("No usage of them is metered, budgeted, capped or alerted on by "
            "this repository's runtime code" in current)
    assert "no kill switch, no spending ceiling, no cost accumulator" in current


def test_old_zero_cost_claim_only_survives_as_labeled_history():
    """The superseded claim stays visible — but never as a live claim."""
    text = _norm(COST)
    occurrences = list(re.finditer(
        r"There is NO live paid usage of any kind", text))
    assert occurrences, (
        "the superseded claim must stay visible as labeled history — deleting "
        "it would hide that the plan once asserted zero provider cost")
    for match in occurrences:
        window = text[max(0, match.start() - 400):match.start()]
        assert "SUPERSEDED" in window, (
            "this claim may appear ONLY inside preserved superseded text: %s"
            % text[max(0, match.start() - 200):match.end() + 80])


def test_cost_plan_never_claims_active_controls():
    text = _norm(COST)
    # every historical control claim is labeled
    for claim in ("INVENTORAI_KILL_SWITCH", "Max input tokens per call",
                  "Max iterations per session", "Max session cost USD"):
        idx = text.find(claim)
        assert idx != -1, claim
        window = text[idx:idx + 400]
        assert "NOT IMPLEMENTED" in window, claim
    assert "PLANNED / NOT IMPLEMENTED" in text
    assert "none of it is active" in text


def test_cost_plan_matches_source_truth():
    # no kill switch in the runtime (doc truth tied to source truth)
    with open(os.path.join("web", "app.py"), encoding="utf-8") as fh:
        assert "INVENTORAI_KILL_SWITCH" not in fh.read()
    # AI transfer stays hardcoded-disabled with the dormant 150-token path
    with open(os.path.join("engine", "ai_advisor.py"), encoding="utf-8") as fh:
        source = fh.read()
    assert "AI_ADVISORY_ENABLED = False" in source
    assert '"max_tokens": 150' in source


def test_provider_cost_claims_tied_to_source_truth():
    """The document's "these providers now cost money" claims must keep
    matching the source that makes them true, in both directions.

    Added with the v1.32 repair: the current section names an off-provider
    backup path and a production email adapter. If either is ever removed the
    document's cost reality changes, and this test makes that change loud
    instead of leaving a stale claim of cost where none is incurred.
    """
    assert os.path.isfile(os.path.join("engine", "r2_object_upload.py"))
    assert os.path.isfile(os.path.join("engine", "offsite_backup_scheduler.py"))
    assert os.path.isfile(
        os.path.join("scripts", "inventorai_offsite_backup.py"))
    with open(os.path.join("engine", "email_sender.py"), encoding="utf-8") as fh:
        assert "class ResendEmailSender" in fh.read()
    # the scheduler exists in the tree but must not be described as running:
    # nothing in web/ may start it outside the production gate.
    with open(os.path.join("web", "app.py"), encoding="utf-8") as fh:
        app_source = fh.read()
    assert "_start_offsite_backup_scheduler_if_production" in app_source


def test_paid_activation_block_referenced():
    assert "D-P8-PL-01 class C" in _norm(COST)
