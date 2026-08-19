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
Output contract: superseded claims stay labeled; no prescriptive retention
duration exists; retention substance stays OPEN; disabled/absent controls are
never claimed active; cited source truth still matches.
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


def test_retention_doc_matches_source_truth():
    # the "only automatic deletion is expired rate-limit cleanup" claim must
    # keep matching source: DELETE FROM appears in engine/ ONLY for
    # auth_rate_limits
    deletes = []
    for path in glob.glob(os.path.join("engine", "*.py")):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if "DELETE FROM" in line:
                    deletes.append((path, line.strip()))
    assert deletes, "expected the bounded rate-limit cleanup to exist"
    for path, line in deletes:
        assert "auth_rate_limits" in line, (path, line)
    # the 7-day client TTL claim must keep matching the real script
    with open(os.path.join("web", "static", "js", "local_draft.js"),
              encoding="utf-8") as fh:
        assert "TTL_MS = 7 * 24 * 60 * 60 * 1000" in fh.read()


# ==========================================================================
# COST_GOVERNANCE_PLAN.md
# ==========================================================================
def test_cost_plan_states_no_live_paid_usage():
    text = _norm(COST)
    assert "There is NO live paid usage of any kind" in text
    assert "AI_ADVISORY_ENABLED = False" in text
    assert "no kill switch, no spending ceiling, no cost accumulator" in text


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


def test_paid_activation_block_referenced():
    assert "D-P8-PL-01 class C" in _norm(COST)
