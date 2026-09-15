# -*- coding: utf-8 -*-
"""Manufacturing joins the Readiness Snapshot as an evidence-sufficiency row.

`MANUFACTURING-READINESS-SNAPSHOT-01` (Owner-authorized).

Manufacturing previously carried no disposition, because it had no evidence
owner and "insufficient evidence" would have implied an assessment nobody had
made. It has an owner now, so its evidence sufficiency is reportable exactly as
Commercial's is.

What did NOT change is what the row MEANS. It is evidence sufficiency, not
manufacturability. The tests below spend most of their effort on that
distinction and on its two failure modes: a reader taking "insufficient
evidence about manufacturing" for "this would be hard to manufacture", and a
reader taking three identical dispositions for a combined verdict. Neither
reading is available, and both are checked in the rendered page rather than
only in the data.
"""
import inspect
import os
import re
import sqlite3

import pytest

from tests.csrf_client import csrf_client
import web.app as webapp
from web.app import app, SESSION_STORE
from web import ui_text
from engine import account_credentials as _acct
from engine import readiness_snapshot as rs
from engine.commercial_evidence import (
    CLAIM_STATUS_UNVALIDATED, COMMERCIAL_TOPICS, DIMENSION_COMMERCIAL,
    DIMENSION_MANUFACTURING, MANUFACTURING_TOPICS,
)
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
MEV = "/session/%s/manufacturing-evidence"
CEV = "/session/%s/commercial-evidence"
POSITIVE = ("PASS_WITH_CONDITIONS", "PASS", "HOLD")

MITEM = {"topic": "material", "subject_text": "The outer housing",
         "statement_text": "The housing would be aluminium rather than ABS.",
         "source_identity": "Inventor", "occurred_on": "",
         "scope_text": "the handlebar unit", "limitation_text": "not checked"}
CITEM = {"topic": "price", "subject_text": "Unit price",
         "statement_text": "Under 400 per unit.", "source_identity": "Inventor",
         "occurred_on": "", "scope_text": "one region", "limitation_text": "unchecked"}


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
    token = re.search(r'name="answer_token" value="([^"]+)"', _page(client, sid)).group(1)
    client.post(SESSION % sid, data={"response": PROBLEM, "action": "answered",
                                     "answer_token": token})
    return sid


def _record(client, sid, **over):
    data = dict(MITEM)
    data.update(over)
    return client.post(MEV % sid, data=data)


def _record_commercial(client, sid, **over):
    data = dict(CITEM)
    data.update(over)
    return client.post(CEV % sid, data=data)


def _snapshot(body):
    return re.search(r'id="rs-readiness-snapshot".*?</details>', body, re.S).group(0)


def _row(body, dimension):
    m = re.search(r'data-rs-dimension="%s".*?</li>' % dimension,
                  _snapshot(body), re.S)
    return m.group(0) if m else ""


def _shown(key, lang="en"):
    import markupsafe
    return str(markupsafe.escape(ui_text.text(key, lang)))


def _prose(html):
    import html as _html
    return _html.unescape(re.sub(r"<[^>]+>", " ", html)).lower()


def _rows(sid):
    return webapp._get_store().load_readiness_evidence(sid)


def _mfg_row(sid):
    return rs.manufacturing_row(_rows(sid))


@pytest.fixture
def owner():
    c = _client_for("mrs-owner@example.com")
    return c, _start(c)


# ==========================================================================
# 1. zero evidence (A, B)
# ==========================================================================
def test_zero_manufacturing_evidence_is_insufficient_evidence(owner):
    """A."""
    c, sid = owner
    row = _mfg_row(sid)
    assert row["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE
    assert row["reason"] == rs.REASON_NOTHING_RECORDED
    assert row["recorded_items"] == 0 and row["topics_covered"] == 0
    rendered = _row(_page(c, sid), "manufacturing")
    assert 'data-rs-disposition="INSUFFICIENT_EVIDENCE"' in rendered
    assert _shown("UI_RS_DISPOSITION_INSUFFICIENT_EVIDENCE") in rendered


def test_zero_evidence_wording_implies_no_manufacturing_failure(owner):
    """B. The load-bearing wording test: an absence must not read as a finding."""
    c, sid = owner
    rendered = _row(_page(c, sid), "manufacturing")
    assert _shown("UI_RS_MANUFACTURING_NOTHING") in rendered
    assert _shown("UI_RS_MANUFACTURING_NOTHING_NOT_A_VERDICT") in rendered
    prose = _prose(rendered)
    for implication in ("difficult to make", "hard to make", "cannot be made",
                        "not manufacturable", "manufacturing problem",
                        "expensive", "costly", "impossible", "failure",
                        "failed", "risky"):
        assert implication not in prose, implication


# ==========================================================================
# 2. recorded evidence (C, D, E, F, G, H)
# ==========================================================================
def test_one_manufacturing_item_is_still_insufficient_evidence(owner):
    """C."""
    c, sid = owner
    _record(c, sid)
    row = _mfg_row(sid)
    assert row["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE
    assert row["reason"] == rs.REASON_RECORDED_BUT_UNCHECKED
    assert row["recorded_items"] == 1


def test_all_ten_topics_are_still_insufficient_evidence(owner):
    """D. Volume never becomes sufficiency."""
    c, sid = owner
    for topic in MANUFACTURING_TOPICS:
        _record(c, sid, topic=topic, statement_text="A statement about %s." % topic)
    row = _mfg_row(sid)
    assert row["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE
    assert row["recorded_items"] == 10
    assert row["topics_covered"] == 10
    assert 'data-rs-disposition="INSUFFICIENT_EVIDENCE"' in _row(
        _page(c, sid), "manufacturing")


def test_item_and_distinct_topic_counts_are_accurate(owner):
    """E, F. Three items across two distinct topics."""
    c, sid = owner
    _record(c, sid, topic="material", statement_text="Aluminium.")
    _record(c, sid, topic="material", statement_text="Or ABS instead.")
    _record(c, sid, topic="tooling", statement_text="An injection mould.")
    row = _mfg_row(sid)
    assert row["recorded_items"] == 3
    assert row["topics_covered"] == 2
    assert row["topics"] == ("material", "tooling")
    rendered = _row(_page(c, sid), "manufacturing")
    assert "Recorded items: 3" in rendered and "Topics covered: 2" in rendered


def test_topic_labels_are_rendered_not_raw_tokens(owner):
    """G. §14: labels and counts, never internal tokens."""
    c, sid = owner
    _record(c, sid, topic="manufacturability", statement_text="A deep pocket.")
    rendered = _row(_page(c, sid), "manufacturing")
    assert _shown("UI_MEV_TOPIC_MANUFACTURABILITY") in rendered
    for topic in MANUFACTURING_TOPICS:
        assert ">%s<" % topic not in rendered, topic


def test_all_manufacturing_evidence_remains_unvalidated(owner):
    """H."""
    c, sid = owner
    for topic in ("material", "process", "cost"):
        _record(c, sid, topic=topic, statement_text="About %s." % topic)
    assert _mfg_row(sid)["all_unvalidated"] is True
    assert {r.claim_status for r in _rows(sid)} == {CLAIM_STATUS_UNVALIDATED}
    assert _shown("UI_RS_MANUFACTURING_ALL_UNCHECKED") in _row(
        _page(c, sid), "manufacturing")


def test_no_raw_evidence_text_reaches_the_snapshot(owner):
    """§14: counts, labels and standing only."""
    c, sid = owner
    _record(c, sid, statement_text="SECRET_MARKER_7f3a aluminium housing",
            subject_text="SUBJECT_MARKER_7f3a")
    snapshot = _snapshot(_page(c, sid))
    assert "SECRET_MARKER_7f3a" not in snapshot
    assert "SUBJECT_MARKER_7f3a" not in snapshot


# ==========================================================================
# 3. no positive state, no composite (I, J, K, L)
# ==========================================================================
def test_positive_dispositions_are_structurally_unreachable():
    """I, J, K — proven by construction, not by sampling."""
    assert rs.EMITTABLE_DISPOSITIONS == ("INSUFFICIENT_EVIDENCE",)
    code = re.sub(r'(?s)"{3}.*?"{3}', "", inspect.getsource(rs))
    code = "\n".join(l.split("#")[0] for l in code.splitlines())
    for token in POSITIVE:
        assert token not in code, token


def test_no_score_composite_or_overall_result_exists(owner):
    """L. Three independent statements, never combined."""
    snap = rs.readiness_snapshot(IdeaState(idea_id="x"), ())
    assert sorted(snap) == ["dimensions", "evidence_dimensions_active", "rows"]
    for aggregate in ("overall", "overall_disposition", "score", "percentage",
                      "composite", "weakest", "status", "summary"):
        assert aggregate not in snap, aggregate
    code = re.sub(r'(?s)"{3}.*?"{3}', "", inspect.getsource(rs))
    code = "\n".join(l.split("#")[0] for l in code.splitlines())
    for banned in ("score", "percent", "composite", "weakest", "overall",
                   "threshold", "weight", "sum(", "min(", "max("):
        assert banned not in code, banned
    c, sid = owner
    _record(c, sid)
    snapshot = _snapshot(_page(c, sid))
    assert snapshot.count('data-rs-disposition="INSUFFICIENT_EVIDENCE"') == 3
    assert _shown("UI_RS_NO_OVERALL") in snapshot
    assert not re.search(r"\b\d{1,3}\s?%", _prose(snapshot))


def test_three_identical_dispositions_do_not_imply_equivalence(owner):
    """The page must say the three are not added up, because three identical
    words invite exactly that reading."""
    c, sid = owner
    _record(c, sid)
    _record_commercial(c, sid)
    snapshot = _snapshot(_page(c, sid))
    assert _shown("UI_RS_NO_OVERALL") in snapshot
    # Scan the prose with the disclaimer REMOVED: it necessarily contains the
    # very phrases it denies ("there is no overall readiness result"), and a
    # naive scan would read the denial as the claim.
    prose = _prose(snapshot).replace(
        _prose(ui_text.text("UI_RS_NO_OVERALL", "en")), " ")
    for implication in ("overall readiness", "total readiness", "combined",
                        "average", "traffic light", "weakest link",
                        "overall result", "overall status"):
        assert implication not in prose, implication


# ==========================================================================
# 4. non-regression (M, N, O, P, Q, R)
# ==========================================================================
def test_the_technical_row_is_unchanged(owner):
    """M."""
    c, sid = owner
    state = SESSION_STORE[sid]["state"]
    before = rs.technical_row(state)
    _record(c, sid)
    _record_commercial(c, sid)
    after = rs.technical_row(SESSION_STORE[sid]["state"])
    assert after == before
    assert after["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE
    assert after["reason"] == rs.REASON_NO_UPPER_TIER_WRITER
    assert set(after) == {"dimension", "disposition", "reason", "recorded_items",
                          "areas_covered", "qualities", "all_unvalidated",
                          "verified_contexts"}
    rendered = _row(_page(c, sid), "technical")
    assert _shown("UI_RS_TECHNICAL_WHY") in rendered
    assert _shown("UI_RS_TECHNICAL_NOT_A_VERDICT") in rendered


def test_the_commercial_row_is_unchanged(owner):
    """N. Same keys, same semantics, same counts."""
    c, sid = owner
    _record_commercial(c, sid)
    _record_commercial(c, sid, topic="demand", statement_text="Two asked.")
    row = rs.commercial_row(_rows(sid))
    assert set(row) == {"dimension", "disposition", "reason", "recorded_items",
                        "topics_covered", "topics", "all_unvalidated"}
    assert row["disposition"] == rs.DISPOSITION_INSUFFICIENT_EVIDENCE
    assert row["recorded_items"] == 2 and row["topics_covered"] == 2
    assert row["topics"] == ("demand", "price")
    rendered = _row(_page(c, sid), "commercial")
    assert _shown("UI_RS_COMMERCIAL_RECORDED") in rendered
    assert "Recorded items: 2" in rendered


def test_the_two_evidence_rows_never_count_each_other(owner):
    """O. Dimension isolation, in the snapshot rather than only in the store."""
    c, sid = owner
    for topic in ("material", "tooling", "cost"):
        _record(c, sid, topic=topic, statement_text="About %s." % topic)
    _record_commercial(c, sid)
    rows = _rows(sid)
    mfg, com = rs.manufacturing_row(rows), rs.commercial_row(rows)
    assert mfg["recorded_items"] == 3 and com["recorded_items"] == 1
    assert not set(mfg["topics"]) & set(COMMERCIAL_TOPICS)
    assert not set(com["topics"]) & set(MANUFACTURING_TOPICS)
    assert mfg["dimension"] == "manufacturing" and com["dimension"] == "commercial"


def test_project_isolation(owner):
    """P."""
    c, sid = owner
    other = _start(c)
    _record(c, sid)
    assert rs.manufacturing_row(_rows(other))["recorded_items"] == 0
    assert _shown("UI_RS_MANUFACTURING_NOTHING") in _row(
        _page(c, other), "manufacturing")


def test_cross_account_access_is_denied(owner):
    """Q."""
    c, sid = owner
    _record(c, sid)
    intruder = _client_for("mrs-intruder@example.com")
    r = intruder.get(SESSION % sid)
    assert r.status_code in (302, 403, 404)
    assert "aluminium" not in r.get_data(as_text=True).lower()


def test_repeated_get_causes_zero_mutation(owner):
    """R."""
    c, sid = owner
    _record(c, sid)
    _record_commercial(c, sid)

    def snap():
        conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
        try:
            return conn.execute(
                "SELECT evidence_seq, evidence_id, dimension, topic, claim_status "
                "FROM readiness_evidence ORDER BY project_id, evidence_seq"
            ).fetchall()
        finally:
            conn.close()

    before = snap()
    ledger_before = len(SESSION_STORE[sid]["state"].assertions)
    for _ in range(5):
        assert c.get(SESSION % sid).status_code == 200
    assert snap() == before
    assert len(SESSION_STORE[sid]["state"].assertions) == ledger_before


def test_the_seam_stays_pure_and_persists_nothing(owner):
    """§7."""
    source = inspect.getsource(rs)
    for banned in ("_get_store", "sqlite", "INSERT", "UPDATE", "DELETE",
                   "CREATE TABLE", "open(", "request", "session"):
        assert banned not in source, banned
    c, sid = owner
    _record(c, sid)
    rows = _rows(sid)
    state = SESSION_STORE[sid]["state"]
    assert rs.readiness_snapshot(state, rows) == rs.readiness_snapshot(state, rows)
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    finally:
        conn.close()
    assert not [t for t in tables if "snapshot" in t.lower()]
    assert not [t for t in tables
                if "readiness" in t.lower() and t != "readiness_evidence"]


def test_fdc001_and_the_product_verdict_are_untouched(owner):
    """§10."""
    import subprocess
    from engine.deliverable_assembler import assemble_deliverable
    root = os.path.join(os.path.dirname(__file__), "..")
    out = subprocess.run(
        ["git", "diff", "--name-only", "f96c1900a0f5d0831a7654223ae4e008d4df961e",
         "--", "engine/decision_workspace.py"],
        capture_output=True, text=True, cwd=root)
    assert out.stdout.strip() == ""
    c, sid = owner
    before = assemble_deliverable(SESSION_STORE[sid]["state"])["section_7_recommendations"]
    _record(c, sid)
    after = assemble_deliverable(SESSION_STORE[sid]["state"])["section_7_recommendations"]
    assert after == before
    code = re.sub(r'(?s)"{3}.*?"{3}', "", inspect.getsource(rs))
    code = "\n".join(l.split("#")[0] for l in code.splitlines())
    for banned in ("decision_workspace", "DecisionRecord", "FDC", "verdict",
                   "PROCEED", "REVISE", "BLOCK"):
        assert banned not in code, banned


# ==========================================================================
# 5. wording and exclusions (S, T, U, V)
# ==========================================================================
def test_no_manufacturability_conclusion_anywhere_in_the_row(owner):
    """U."""
    c, sid = owner
    for topic in MANUFACTURING_TOPICS:
        _record(c, sid, topic=topic, statement_text="About %s." % topic)
    prose = _prose(_row(_page(c, sid), "manufacturing"))
    for claim in ("manufacturable", "easy to manufacture", "hard to manufacture",
                  "prototype-ready", "prototype ready", "production-ready",
                  "production ready", "supplier-ready", "tooling-ready",
                  "low-cost", "low cost", "scalable", "bom-ready", "bom ready",
                  "feasible"):
        assert claim not in prose, claim
    assert _shown("UI_RS_MANUFACTURING_NOT_A_CONCLUSION") in _row(
        _page(c, sid), "manufacturing")


def test_no_cad_pcb_bom_or_supplier_behaviour_was_introduced():
    """V."""
    source = inspect.getsource(rs)
    for banned in ("cad", "pcb", "gerber", "bom", "bill_of_materials",
                   "supplier_api", "requests.", "urllib", "httpx", "scrape"):
        assert banned not in source.lower().replace("because", ""), banned


def test_english_rendering(owner):
    """S."""
    c, sid = owner
    _record(c, sid)
    body = _page(c, sid)
    for key in ("UI_RS_HEADING", "UI_RS_DIM_MANUFACTURING",
                "UI_RS_DISPOSITION_INSUFFICIENT_EVIDENCE",
                "UI_RS_MANUFACTURING_RECORDED",
                "UI_RS_MANUFACTURING_NOT_A_CONCLUSION", "UI_RS_NO_OVERALL"):
        assert _shown(key, "en") in body, key


def test_arabic_rendering(owner):
    """T."""
    c, sid = owner
    _record(c, sid)
    c.post("/ui-language", data={"lang": "ar"})
    body = _page(c, sid)
    for key in ("UI_RS_HEADING", "UI_RS_DIM_MANUFACTURING",
                "UI_RS_DISPOSITION_INSUFFICIENT_EVIDENCE",
                "UI_RS_MANUFACTURING_RECORDED",
                "UI_RS_MANUFACTURING_NOT_A_CONCLUSION", "UI_RS_NO_OVERALL"):
        assert _shown(key, "ar") in body, key
    assert _shown("UI_RS_MANUFACTURING_RECORDED", "en") not in body


def test_every_snapshot_string_has_both_languages():
    for key, entry in ui_text.UI_STRINGS.items():
        if not key.startswith("UI_RS_"):
            continue
        for lang in ("en", "ar"):
            assert entry.get(lang), (key, lang)
        assert entry["en"] != entry["ar"], key


def test_the_retired_not_assessed_wording_is_gone():
    """The dimension IS assessed for evidence sufficiency now, so a string
    asserting nobody looked would be the stale half of a true statement."""
    assert not hasattr(rs, "STATE_NOT_ASSESSED")
    assert "UI_RS_MANUFACTURING_NOT_ASSESSED" not in ui_text.UI_STRINGS
    template = open(os.path.join(os.path.dirname(__file__), "..", "web",
                                 "templates", "session.html"),
                    encoding="utf-8").read()
    assert "data-rs-state" not in template
    assert "UI_RS_MANUFACTURING_NOT_ASSESSED" not in template
