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

from tests import current_truth_contract as contract

RETENTION = os.path.join("docs", "DATA_RETENTION_POLICY.md")
COST = os.path.join("docs", "COST_GOVERNANCE_PLAN.md")


def _raw(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _norm(path):
    return re.sub(r"\s+", " ", _raw(path))


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
# Stage 19 / CAP-09 IMPLEMENTATION-01 added ONE user-initiated current-value
# removal (the owner clearing their own success criterion). It is a separate
# category, NOT an automatic deletion: the automatic set above is unchanged, and
# the document must name this one explicitly as well.
_USER_INITIATED_DELETION_TABLES = ("prototype_plan_metadata",)


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
    known = _AUTOMATIC_DELETION_TABLES + _USER_INITIATED_DELETION_TABLES
    for path, line in deletes:
        assert any(table in line for table in known), (path, line)
    seen_tables = {table for table in known
                   if any(table in line for _p, line in deletes)}
    assert seen_tables == set(known), seen_tables
    with open(os.path.join("docs", "DATA_RETENTION_POLICY.md"), encoding="utf-8") as fh:
        doc = fh.read()
    assert "cleanup_expired_rate_limits" in doc
    assert "mark_email_delivered" in doc and "email_outbox" in doc
    flat = re.sub(r"\s+", " ", doc)
    assert "One USER-INITIATED removal exists" in flat
    assert "`prototype_plan_metadata`" in flat
    assert "It is NOT an automatic deletion, NOT an erasure capability" in flat
    # the 7-day client TTL claim must keep matching the real script
    with open(os.path.join("web", "static", "js", "local_draft.js"),
              encoding="utf-8") as fh:
        assert "TTL_MS = 7 * 24 * 60 * 60 * 1000" in fh.read()


# ==========================================================================
# COST_GOVERNANCE_PLAN.md
# ==========================================================================
def _cost_current_truth():
    """The explicit CURRENT-TRUTH:COST region — the only current-truth source.

    REPAIRED AGAIN (v1.32 contract hardening). Two earlier attempts tried to
    separate current truth from history by recognising Markdown shapes, and
    both leaked: a preserved claim in a shape the guard had not anticipated
    could satisfy a check about the present. The document now delimits its
    current truth explicitly and this guard reads nothing else. History may sit
    anywhere outside the region, in any format, and may contradict it freely.
    """
    return re.sub(r"\s+", " ", contract.region(_raw(COST), "COST"))


def _cost_history():
    """Everything outside the region — preserved, and never a current claim."""
    return re.sub(r"\s+", " ", contract.outside(_raw(COST), "COST"))


def test_cost_current_truth_region_is_well_formed():
    """Missing, duplicated or malformed region = failure, never a silent pass."""
    assert contract.region(_raw(COST), "COST").strip()


def test_cost_current_truth_states_the_provider_costs_that_exist():
    """The region must name every provider cost that is actually incurred.

    REPAIRED AGAIN (v1.32 contract hardening). Only the delimited region is
    read. A correct-sounding historical claim elsewhere in the file — bullet,
    blockquote, table, italic aside or prose — cannot satisfy any of this.
    """
    current = _cost_current_truth()
    assert "Production hosting exists" in current
    assert "off-provider backup destination exists" in current
    assert "email provider and adapter direction exists" in current
    assert "OD-INFRA-1" in current and "OD-INFRA-5" in current
    assert "OD-INFRA-6" in current


def test_cost_current_truth_states_what_costs_nothing():
    current = _cost_current_truth()
    assert "AI token spend is zero" in current
    assert "AI_ADVISORY_ENABLED = False" in current
    assert "Live production email sending remains DEFERRED" in current
    assert "No payment provider is live" in current
    assert "no live user billing exists" in current
    assert "No paid third-party monitoring service" in current


def test_cost_current_truth_denies_a_runtime_cost_control_system():
    """The plan must not imply that runtime code governs provider spend."""
    current = _cost_current_truth()
    assert ("Runtime code does not provide a complete provider-cost budgeting, "
            "capping or alerting system" in current)
    assert "no kill switch, no spending ceiling, no cost accumulator" in current


def test_cost_current_truth_records_od_infra_4_as_decided():
    """A settled selection is not operational readiness, and vice versa."""
    current = _cost_current_truth()
    assert "OD-INFRA-4 DECISION: SATISFIED AS A SELECTION DECISION" in current
    assert "no dedicated third-party monitoring provider was adopted" in current
    assert "remain OPEN operations work" in current
    assert "Nobody is notified when something breaks" in current
    # the decision must not be recorded as still open anywhere current
    assert "OD-INFRA-4 OPEN" not in current
    assert "OD-INFRA-4 remains OPEN" not in current


def test_cost_current_truth_never_claims_zero_paid_usage():
    """The vague old formulation may not reappear as a current claim."""
    current = _cost_current_truth()
    for vague in ("no live paid usage of any kind",
                  "no provider cost", "no cloud/provider billing",
                  "do not exist today"):
        assert vague.lower() not in current.lower(), vague


def test_old_zero_cost_claim_only_survives_outside_the_region():
    """The superseded claim stays visible — and stays out of current truth."""
    claim = "There is NO live paid usage of any kind"
    assert claim in _cost_history(), (
        "the superseded claim must stay visible as labeled history — deleting "
        "it would hide that the plan once asserted zero provider cost")
    assert claim not in _cost_current_truth()
    text = _norm(COST)
    for match in re.finditer(re.escape(claim), text):
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
