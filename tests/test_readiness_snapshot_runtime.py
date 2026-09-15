# -*- coding: utf-8 -*-
"""Readiness Snapshot — the first runtime presentation of Readiness.

`READINESS-SNAPSHOT-RUNTIME-01` (Owner-authorized).

The snapshot answers "what evidence is available for each dimension?" and never
"should I proceed?". So these tests are mostly about restraint: that exactly one
disposition is reachable, that Manufacturing gets none at all, that a count is
never turned into a judgement, and — the thing most likely to go wrong in copy
rather than code — that a reader cannot take an ABSENCE of evidence for NEGATIVE
evidence about their idea.

The strongest guarantee proven here is structural rather than behavioural:
`PASS`, `PASS_WITH_CONDITIONS` and `HOLD` are not merely unreached, they are not
constructible by the composition seam, so no future input can surface one.
"""
import inspect
import os
import re

import pytest

from tests.csrf_client import csrf_client
import web.app as webapp
from web.app import app, SESSION_STORE
from web import ui_text
from engine import account_credentials as _acct
from engine import readiness_snapshot as rs
from engine.commercial_evidence import COMMERCIAL_TOPICS
from engine.idea_state import IdeaState

PW = "correct horse battery staple"
FORM = {"idea": "ESP32 microcontroller circuit with a voltage sensor",
        "domain_confirm": "electronics_electrical"}
PROBLEM = (
    "The problem is that cyclists have no reliable brake light. My circuit senses "
    "deceleration with an accelerometer because sudden voltage change on the sensor "
    "indicates braking, so the microcontroller switches the LED because riders "
    "behind need warning.")
SESSION = "/session/%s"
CEV = "/session/%s/commercial-evidence"
ITEM = {"topic": "target_customer", "subject_text": "Home-care agencies",
        "statement_text": "Agencies buy the ramps, not families.",
        "source_identity": "Inventor, own experience", "occurred_on": "",
        "scope_text": "one local region", "limitation_text": "not checked with any agency"}
POSITIVE = ("PASS_WITH_CONDITIONS", "PASS", "HOLD")


def _new_client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _client_for(email):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c


def _page(client, sid):
    r = client.get(SESSION % sid)
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _start(client):
    sid = client.post("/start", data=FORM).headers["Location"].rsplit("/session/", 1)[-1]
    token = re.search(r'name="answer_token" value="([^"]+)"',
                      _page(client, sid)).group(1)
    client.post(SESSION % sid, data={"response": PROBLEM, "action": "answered",
                                     "answer_token": token})
    return sid


def _record(client, sid, **over):
    data = dict(ITEM)
    data.update(over)
    return client.post(CEV % sid, data=data)


def _code_only(source):
    """Python source with docstrings and comments removed, so a scan asserts
    about CODE — the snapshot module documents, in words, exactly the things it
    must never touch."""
    code = re.sub(r'(?s)"{3}.*?"{3}', "", source)
    return "\n".join(line.split("#")[0] for line in code.splitlines())


def _prose(html):
    """Rendered text with markup removed and entities decoded, so a wording
    scan reads what a PERSON reads — not tag names like <strong>."""
    import html as _html
    return _html.unescape(re.sub(r"<[^>]+>", " ", html)).lower()


def _shown(key, lang="en"):
    """A catalogue string as it appears in the rendered page (autoescaped)."""
    import markupsafe
    return str(markupsafe.escape(ui_text.text(key, lang)))


def _row(body, dimension):
    """The rendered snapshot row for one dimension."""
    m = re.search(r'data-rs-dimension="%s".*?</li>' % dimension, body, re.S)
    return m.group(0) if m else ""


@pytest.fixture
def owner():
    c = _client_for("snapshot-owner@example.com")
    return c, _start(c)


# ==========================================================================
# 1. the structural guarantee: one disposition is reachable, by construction
# ==========================================================================
def test_only_insufficient_evidence_is_emittable():
    """J, K, L — proven structurally, not by sampling. The positive tokens do
    not appear in the module at all, so no branch can return one."""
    assert rs.EMITTABLE_DISPOSITIONS == ("INSUFFICIENT_EVIDENCE",)
    code = _code_only(inspect.getsource(rs))
    for token in POSITIVE:
        assert token not in code, token
    for banned in ("score", "percent", "threshold", "rank", "weight",
                   "composite", "marketab", "profitab"):
        assert banned not in code.lower(), banned


def test_the_seam_is_pure_and_persists_nothing():
    """P. No store, no I/O, no durable record: composition only."""
    code = _code_only(inspect.getsource(rs))
    for banned in ("_get_store", "sqlite", "INSERT", "UPDATE", "DELETE",
                   "CREATE TABLE", "open(", "request", "session"):
        assert banned not in code, banned
    state = IdeaState(idea_id="pure")
    first = rs.readiness_snapshot(state, ())
    second = rs.readiness_snapshot(state, ())
    assert first == second


def test_every_row_carries_only_a_permitted_disposition():
    state = IdeaState(idea_id="d")
    snapshot = rs.readiness_snapshot(state, ())
    for row in snapshot["rows"]:
        disposition = row["disposition"]
        assert disposition is None or disposition in rs.EMITTABLE_DISPOSITIONS


# ==========================================================================
# 2. the Technical row (A, B, C, D)
# ==========================================================================
def test_the_technical_row_appears_and_is_insufficient_evidence(owner):
    """A, B."""
    c, sid = owner
    body = _page(c, sid)
    assert 'id="rs-readiness-snapshot"' in body
    row = _row(body, "technical")
    assert row
    assert 'data-rs-disposition="INSUFFICIENT_EVIDENCE"' in row
    assert _shown("UI_RS_DISPOSITION_INSUFFICIENT_EVIDENCE") in row


def test_the_technical_row_explains_the_missing_verified_writer(owner):
    """C. It explains WHY, and the why is about this version's limits — not
    about the idea. This is the part that must not read as a duplicate of the
    existing derived-readiness line."""
    c, sid = owner
    row = _row(_page(c, sid), "technical")
    assert _shown("UI_RS_TECHNICAL_WHY") in row
    assert _shown("UI_RS_TECHNICAL_NOT_A_VERDICT") in row
    assert "data-rs-why" in row and "data-rs-not-a-verdict" in row


def test_the_technical_row_counts_recorded_evidence_accurately(owner):
    c, sid = owner
    snapshot = rs.readiness_snapshot(SESSION_STORE[sid]["state"], ())
    technical = snapshot["rows"][0]
    assert technical["dimension"] == "technical"
    assert technical["recorded_items"] >= 1
    assert technical["areas_covered"] >= 1
    assert technical["all_unvalidated"] is True
    assert technical["verified_contexts"] == 0
    assert technical["reason"] == rs.REASON_NO_UPPER_TIER_WRITER


def test_no_positive_technical_state_appears(owner):
    """D. Neither a disposition nor a synonym implying one."""
    c, sid = owner
    row = _row(_page(c, sid), "technical").lower()
    for claim in ("technically feasible", "technically validated",
                  "technically ready", "prototype ready", "feasible",
                  "verified technical result is", "proven"):
        if claim == "verified technical result is":
            continue
        assert claim not in row, claim


def test_a_project_with_no_technical_reasoning_says_so_plainly():
    state = IdeaState(idea_id="empty")
    technical = rs.technical_row(state)
    assert technical["recorded_items"] == 0
    assert technical["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE


# ==========================================================================
# 3. the Commercial row (E, F, G)
# ==========================================================================
def test_commercial_with_zero_evidence_is_insufficient_and_not_negative(owner):
    """E. The hardest rule in this slice: an absence must not read as a finding."""
    c, sid = owner
    row = _row(_page(c, sid), "commercial")
    assert 'data-rs-disposition="INSUFFICIENT_EVIDENCE"' in row
    assert _shown("UI_RS_COMMERCIAL_NOTHING") in row
    assert _shown("UI_RS_COMMERCIAL_NOTHING_NOT_A_VERDICT") in row
    lowered = row.lower()
    for implication in ("poor market", "weak demand", "no demand", "not viable",
                        "unviable", "small market", "insufficient market",
                        "no customers", "failed"):
        assert implication not in lowered, implication


def test_commercial_with_recorded_items_stays_insufficient_with_true_counts(owner):
    """F. Counts are accurate; the disposition does not move; the unchecked
    standing is reflected."""
    c, sid = owner
    _record(c, sid)
    _record(c, sid, topic="price", subject_text="Price",
            statement_text="Under 400 per unit.")
    _record(c, sid, topic="price", subject_text="Price again",
            statement_text="Closer to 350 in volume.")
    rows = webapp._get_store().load_readiness_evidence(sid)
    commercial = rs.commercial_row(rows)
    assert commercial["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE
    assert commercial["recorded_items"] == 3
    assert commercial["topics_covered"] == 2          # distinct topics
    assert commercial["all_unvalidated"] is True
    assert commercial["reason"] == rs.REASON_RECORDED_BUT_UNCHECKED
    row = _row(_page(c, sid), "commercial")
    assert _shown("UI_RS_COMMERCIAL_RECORDED") in row
    assert "Recorded items: 3" in row and "Topics covered: 2" in row
    assert _shown("UI_RS_COMMERCIAL_ALL_UNCHECKED") in row


def test_the_commercial_row_never_interprets_what_it_counts(owner):
    c, sid = owner
    for topic in ("demand", "willingness_to_pay", "price", "revenue_model"):
        _record(c, sid, topic=topic, statement_text="A statement about %s." % topic)
    prose = _prose(_row(_page(c, sid), "commercial"))
    for inference in ("market size", "commercially attractive", "attractive",
                      "profitab", "investment", "willing to pay", "strong",
                      "promising", "viable", "opportunity"):
        assert inference not in prose, inference


def test_commercial_evidence_never_crosses_projects(owner):
    """G. Project isolation on the read surface."""
    c, sid = owner
    other_sid = _start(c)
    _record(c, sid, statement_text="Only project A knows this.")
    body_b = _page(c, other_sid)
    assert "Only project A knows this." not in body_b
    row_b = _row(body_b, "commercial")
    assert _shown("UI_RS_COMMERCIAL_NOTHING") in row_b
    assert "Recorded items: 1" not in row_b


def test_another_account_cannot_see_this_projects_snapshot(owner):
    c, sid = owner
    _record(c, sid, statement_text="Private to the owner.")
    intruder = _client_for("snapshot-intruder@example.com")
    r = intruder.get(SESSION % sid)
    assert r.status_code in (302, 403, 404), r.status_code
    assert "Private to the owner." not in r.get_data(as_text=True)


# ==========================================================================
# 4. Manufacturing (H, I)
# ==========================================================================
def test_manufacturing_is_shown_as_not_assessed(owner):
    """H. Option A: a truthful row, not an omission."""
    c, sid = owner
    row = _row(_page(c, sid), "manufacturing")
    assert row
    assert 'data-rs-state="not_assessed"' in row
    assert _shown("UI_RS_MANUFACTURING_NOT_ASSESSED") in row
    assert _shown("UI_RS_MANUFACTURING_NOT_A_VERDICT") in row


def test_manufacturing_receives_no_canonical_disposition(owner):
    """I. Not even INSUFFICIENT_EVIDENCE — that would imply somebody looked."""
    assert rs.manufacturing_row()["disposition"] is None
    c, sid = owner
    row = _row(_page(c, sid), "manufacturing")
    assert "data-rs-disposition" not in row
    assert "INSUFFICIENT_EVIDENCE" not in row
    lowered = row.lower()
    for implication in ("difficult to manufacture", "hard to make",
                        "manufacturing problem", "cannot be made", "failure"):
        assert implication not in lowered, implication


def test_manufacturing_state_is_never_inferred_from_other_evidence(owner):
    """The inactive state is fixed: no materials, cost or requirement text can
    move it."""
    c, sid = owner
    _record(c, sid, topic="cost_revenue_assumption",
            statement_text="Aluminium extrusion and injection-moulded ABS, about 40 per unit in tooling.")
    assert rs.manufacturing_row() == {
        "dimension": "manufacturing", "disposition": None,
        "state": rs.STATE_NOT_ASSESSED}
    assert "data-rs-disposition" not in _row(_page(c, sid), "manufacturing")


# ==========================================================================
# 5. no positive disposition anywhere on the page (J, K, L)
# ==========================================================================
def test_no_positive_readiness_disposition_is_rendered(owner):
    c, sid = owner
    _record(c, sid)
    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        body = _page(c, sid)
        snapshot = re.search(r'id="rs-readiness-snapshot".*?</details>', body, re.S).group(0)
        for token in POSITIVE:
            assert token not in snapshot, (lang, token)
        assert snapshot.count('data-rs-disposition="INSUFFICIENT_EVIDENCE"') == 2


# ==========================================================================
# 6. nothing else moved (M, N, O, P, Q)
# ==========================================================================
def test_the_product_verdict_is_unchanged(owner):
    """M. The snapshot is informational; the recommendation is elsewhere and
    recording Commercial evidence does not move it."""
    from engine.deliverable_assembler import assemble_deliverable
    c, sid = owner
    state = SESSION_STORE[sid]["state"]
    before = assemble_deliverable(state)["section_7_recommendations"]
    _record(c, sid)
    after = assemble_deliverable(
        SESSION_STORE[sid]["state"])["section_7_recommendations"]
    assert after == before, "recording Commercial evidence moved the verdict"
    assert before["category_a_proceed_revise_block"]["verdict"] in (
        "PROCEED", "PROCEED WITH CAUTION", "REVISE", "BLOCK")


def test_fdc001_and_the_decision_workspace_are_untouched():
    """N, O. Byte-identical against the standing pin."""
    import subprocess
    root = os.path.join(os.path.dirname(__file__), "..")
    out = subprocess.run(
        ["git", "diff", "--name-only", "f96c1900a0f5d0831a7654223ae4e008d4df961e",
         "--", "engine/decision_workspace.py"],
        capture_output=True, text=True, cwd=root)
    assert out.stdout.strip() == ""
    code = _code_only(inspect.getsource(rs))
    for banned in ("decision_workspace", "DecisionRecord", "FDC", "verdict",
                   "PROCEED", "REVISE", "BLOCK"):
        assert banned not in code, banned


def test_no_readiness_store_or_persistent_record_was_introduced(owner):
    """P."""
    import sqlite3
    c, sid = owner
    _page(c, sid)
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    finally:
        conn.close()
    assert not [t for t in tables if "snapshot" in t.lower()]
    assert not [t for t in tables
                if "readiness" in t.lower() and t != "readiness_evidence"]


def test_get_causes_zero_mutation(owner):
    """Q. Repeated loads of a read-only surface change nothing."""
    import sqlite3
    c, sid = owner
    _record(c, sid)

    def snapshot_db():
        conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
        try:
            return conn.execute(
                "SELECT evidence_seq, evidence_id, topic, claim_status FROM "
                "readiness_evidence ORDER BY project_id, evidence_seq").fetchall()
        finally:
            conn.close()

    before = snapshot_db()
    ledger_before = len(SESSION_STORE[sid]["state"].assertions)
    for _ in range(5):
        assert c.get(SESSION % sid).status_code == 200
    assert snapshot_db() == before
    assert len(SESSION_STORE[sid]["state"].assertions) == ledger_before


# ==========================================================================
# 7. bilingual and escaping (R, S, T)
# ==========================================================================
def test_english_rendering(owner):
    """R."""
    c, sid = owner
    body = _page(c, sid)
    for key in ("UI_RS_HEADING", "UI_RS_EXPLAIN", "UI_RS_DIM_TECHNICAL",
                "UI_RS_DIM_COMMERCIAL", "UI_RS_DIM_MANUFACTURING",
                "UI_RS_DISPOSITION_INSUFFICIENT_EVIDENCE"):
        assert _shown(key, "en") in body, key


def test_arabic_rendering(owner):
    """S."""
    c, sid = owner
    _record(c, sid)
    c.post("/ui-language", data={"lang": "ar"})
    body = _page(c, sid)
    for key in ("UI_RS_HEADING", "UI_RS_EXPLAIN", "UI_RS_DIM_TECHNICAL",
                "UI_RS_DIM_MANUFACTURING", "UI_RS_TECHNICAL_WHY",
                "UI_RS_COMMERCIAL_RECORDED", "UI_RS_MANUFACTURING_NOT_ASSESSED",
                "UI_RS_DISPOSITION_INSUFFICIENT_EVIDENCE"):
        assert _shown(key, "ar") in body, key
    assert _shown("UI_RS_HEADING", "en") not in body


def test_every_snapshot_string_has_both_languages():
    for key, entry in ui_text.UI_STRINGS.items():
        if not key.startswith("UI_RS_"):
            continue
        for lang in ("en", "ar"):
            assert entry.get(lang), (key, lang)
        assert entry["en"] != entry["ar"], key


def test_inventor_text_reaching_the_snapshot_is_escaped_and_safe(owner):
    """T. The snapshot renders topic LABELS rather than inventor text, so the
    check is that no raw inventor text leaks into it at all — and that what the
    page does render of it elsewhere stays escaped."""
    c, sid = owner
    _record(c, sid, statement_text="<script>alert(1)</script> & co",
            subject_text="<b>bold subject</b>")
    body = _page(c, sid)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in body
    snapshot = re.search(r'id="rs-readiness-snapshot".*?</details>', body, re.S).group(0)
    assert "bold subject" not in snapshot        # counts and labels only
    assert "alert(1)" not in snapshot


def test_topic_labels_are_used_not_raw_tokens(owner):
    """§9: no internal token is exposed where a proper label exists."""
    c, sid = owner
    _record(c, sid, topic="willingness_to_pay")
    row = _row(_page(c, sid), "commercial")
    assert _shown("UI_CEV_TOPIC_WILLINGNESS_TO_PAY") in row
    for topic in COMMERCIAL_TOPICS:
        assert topic not in row, topic
