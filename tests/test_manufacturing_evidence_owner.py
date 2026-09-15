# -*- coding: utf-8 -*-
"""Manufacturing Evidence Owner — the second live evidence dimension.

`MANUFACTURING-EVIDENCE-OWNER-IMPLEMENT-01` (Owner-authorized).

Manufacturing now accepts evidence on the SAME shared `readiness_evidence`
substrate Commercial already uses. That is ownership of evidence and nothing
more: this slice produces no Manufacturing Readiness conclusion, and the
Readiness Snapshot still gives Manufacturing no disposition of any kind. The
test that matters most here is the one proving activation did NOT quietly turn
into assessment.

The second theme is isolation. Two dimensions now share one table, one row
model and one store, so the tests press hard on the seam between them: a
Commercial topic must not validate a Manufacturing row, neither block may show
the other's evidence, and neither route may write the other's dimension.

The third is the event-key improvement §12 required: Manufacturing derives its
event identity from the values as STORED rather than as typed, so whitespace
variants of the same statement are one event instead of several near-duplicate
rows the inventor never meant to create.
"""
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
    ACTIVE_DIMENSIONS, CLAIM_STATUS_UNVALIDATED, COMMERCIAL_TOPICS,
    DEFAULT_PROVENANCE, DIMENSION_COMMERCIAL, DIMENSION_MANUFACTURING,
    DIMENSIONS, MANUFACTURING_TOPICS, TOPICS_BY_DIMENSION,
    CommercialEvidenceError, make_readiness_evidence,
    manufacturing_evidence_view, commercial_evidence_view,
)

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

MITEM = {"topic": "material", "subject_text": "The outer housing",
         "statement_text": "The housing would be aluminium rather than ABS.",
         "source_identity": "Inventor, from their own experience",
         "occurred_on": "", "scope_text": "the handlebar unit only",
         "limitation_text": "not checked with any supplier or against a standard"}
CITEM = {"topic": "price", "subject_text": "Unit price",
         "statement_text": "Under 400 per unit.",
         "source_identity": "Inventor", "occurred_on": "",
         "scope_text": "one region", "limitation_text": "unchecked"}

# The exact closed vocabulary this slice establishes (§4 reconciliation).
EXPECTED_TOPICS = ("prototype_maturity", "material", "component",
                   "specification", "tolerance", "process", "tooling",
                   "supplier", "cost", "manufacturability")


def _new_client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _client_for(email, verified=True, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c, aid


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


def _rows(sid, dimension=None):
    rows = webapp._get_store().load_readiness_evidence(sid)
    return tuple(r for r in rows if dimension is None or r.dimension == dimension)


def _block(body, prefix):
    m = re.search(r'id="%s-.*?</details>' % prefix, body, re.S)
    return m.group(0) if m else ""


def _shown(key, lang="en"):
    import markupsafe
    return str(markupsafe.escape(ui_text.text(key, lang)))


@pytest.fixture
def owner():
    c, aid = _client_for("mfg-owner@example.com")
    return c, aid, _start(c)


# ==========================================================================
# 1. activation and vocabulary (A, B, C)
# ==========================================================================
def test_manufacturing_is_an_activated_evidence_dimension():
    """A."""
    assert DIMENSION_MANUFACTURING in DIMENSIONS
    assert DIMENSION_MANUFACTURING in ACTIVE_DIMENSIONS
    assert TOPICS_BY_DIMENSION[DIMENSION_MANUFACTURING] == MANUFACTURING_TOPICS


def test_commercial_remains_active_and_unchanged():
    """B. Fifteen topics, same order, same tokens."""
    assert DIMENSION_COMMERCIAL in ACTIVE_DIMENSIONS
    assert TOPICS_BY_DIMENSION[DIMENSION_COMMERCIAL] == COMMERCIAL_TOPICS
    assert COMMERCIAL_TOPICS == (
        "target_customer", "problem_severity", "market_alternative",
        "differentiation", "price", "willingness_to_pay", "demand",
        "customer_evidence", "market_entry", "channel", "licensing",
        "revenue_model", "cost_revenue_assumption", "funding_need",
        "first_sale_viability")


def test_the_manufacturing_vocabulary_is_exactly_the_authorized_set():
    """C."""
    assert MANUFACTURING_TOPICS == EXPECTED_TOPICS
    assert len(set(MANUFACTURING_TOPICS)) == 10
    assert not set(MANUFACTURING_TOPICS) & set(COMMERCIAL_TOPICS)


def test_manufacturing_risk_and_safety_are_not_topics():
    """§8, §9: risk stays with the canonical risk owner and safety with the
    existing safety seam. Neither becomes a topic here, which is how this lane
    avoids growing a second risk or safety owner by the back door."""
    for banned in ("manufacturing_risk", "risk", "safety", "hazard",
                   "manufacturing_safety", "compliance", "certification"):
        assert banned not in MANUFACTURING_TOPICS, banned


# ==========================================================================
# 2. the shared store (D, E, Q)
# ==========================================================================
def test_manufacturing_evidence_persists_in_the_shared_table(owner):
    """D."""
    c, _aid, sid = owner
    assert _record(c, sid).status_code == 302
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        stored = conn.execute(
            "SELECT dimension, topic, provenance, claim_status FROM "
            "readiness_evidence WHERE project_id = ?", (sid,)).fetchall()
    finally:
        conn.close()
    assert stored == [("MANUFACTURING", "material", "OWNER_STATED", "UNVALIDATED")]


def test_no_second_readiness_store_exists(owner):
    """Q. One table, two dimensions."""
    c, _aid, sid = owner
    _record(c, sid)
    _record_commercial(c, sid)
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    finally:
        conn.close()
    assert "readiness_evidence" in tables
    assert not [t for t in tables if "manufactur" in t.lower()]
    assert not [t for t in tables
                if "readiness" in t.lower() and t != "readiness_evidence"]


def test_the_two_dimensions_are_isolated_in_store_and_view(owner):
    """E. The isolation is a property of the projection, not a convention."""
    c, _aid, sid = owner
    _record(c, sid)
    _record_commercial(c, sid)
    all_rows = webapp._get_store().load_readiness_evidence(sid)
    assert len(all_rows) == 2
    mfg = manufacturing_evidence_view(all_rows)
    com = commercial_evidence_view(all_rows)
    assert mfg["total"] == 1 and com["total"] == 1
    assert mfg["topics"] == ("material",)
    assert com["topics"] == ("price",)
    assert all(r["dimension"] == DIMENSION_MANUFACTURING for r in mfg["active"])
    assert all(r["dimension"] == DIMENSION_COMMERCIAL for r in com["active"])


def test_each_block_shows_only_its_own_dimension(owner):
    c, _aid, sid = owner
    _record(c, sid)
    _record_commercial(c, sid)
    body = _page(c, sid)
    mev, cev = _block(body, "mev"), _block(body, "cev")
    mfg_text, com_text = MITEM["statement_text"], CITEM["statement_text"]
    assert mfg_text in mev and com_text not in mev
    assert com_text in cev and mfg_text not in cev


# ==========================================================================
# 3. what may be written (F, G, H, I, J)
# ==========================================================================
def test_an_invalid_manufacturing_topic_is_rejected(owner):
    """F."""
    c, _aid, sid = owner
    for bad in ("", "MATERIAL", "materials", "bom", "cad", "../material",
                "manufacturing_risk"):
        assert _record(c, sid, topic=bad).status_code == 302
    assert _rows(sid) == ()


def test_a_commercial_topic_is_not_valid_on_the_manufacturing_route(owner):
    """G + the cross-dimension half: each vocabulary is closed to its own."""
    c, _aid, sid = owner
    for topic in ("price", "demand", "target_customer"):
        assert _record(c, sid, topic=topic).status_code == 302
    assert _rows(sid) == ()
    for topic in ("material", "tooling"):
        assert _record_commercial(c, sid, topic=topic).status_code == 302
    assert _rows(sid) == ()


def test_the_engine_refuses_a_cross_dimension_topic_directly():
    """The store boundary, not only the route."""
    with pytest.raises(CommercialEvidenceError):
        make_readiness_evidence(
            evidence_id="e", evidence_seq=0, dimension=DIMENSION_MANUFACTURING,
            topic="price", subject_text="s", statement_text="t",
            source_identity="i", scope_text="sc", limitation_text="l",
            event_key="k", recorded_iteration=1,
            recorded_at="2026-01-01T00:00:00.000000Z")


def test_provenance_is_forced_to_owner_stated(owner):
    """H."""
    c, _aid, sid = owner
    _record(c, sid)
    assert _rows(sid)[0].provenance == DEFAULT_PROVENANCE == "OWNER_STATED"
    body = _page(c, sid)
    assert 'name="provenance"' not in _block(body, "mev")


def test_claim_status_is_forced_to_unvalidated(owner):
    """I. Recording evidence is not validating evidence."""
    c, _aid, sid = owner
    _record(c, sid)
    assert _rows(sid)[0].claim_status == CLAIM_STATUS_UNVALIDATED == "UNVALIDATED"
    mev = _block(_page(c, sid), "mev")
    for name in ("claim_status", "validation_status", "readiness_status"):
        assert 'name="%s"' % name not in mev


def test_forged_control_fields_are_refused_whole(owner):
    """J. Not silently dropped — refused, so a forged value never looks taken."""
    c, _aid, sid = owner
    for field, value in (("dimension", "COMMERCIAL"),
                         ("dimension", "MANUFACTURING"),
                         ("provenance", "EXTERNAL_EVIDENCE"),
                         ("claim_status", "INDEPENDENTLY_VERIFIED"),
                         ("validation_status", "INDEPENDENTLY_VERIFIED"),
                         ("readiness_status", "PASS")):
        assert _record(c, sid, **{field: value}).status_code == 302
        assert _rows(sid) == (), (field, value)
    _record(c, sid)
    row = _rows(sid)[0]
    assert (row.dimension, row.provenance, row.claim_status) == (
        "MANUFACTURING", "OWNER_STATED", "UNVALIDATED")


def test_over_limit_and_malformed_text_is_rejected(owner):
    c, _aid, sid = owner
    assert _record(c, sid, subject_text="a NUL\x00inside").status_code == 302
    assert _record(c, sid, statement_text="").status_code == 302
    assert _record(c, sid, statement_text="   ").status_code == 302
    assert _record(c, sid, occurred_on="not-a-date").status_code == 302
    assert _record(c, sid, scope_text="z" * 5000).status_code == 302
    assert _rows(sid) == ()


# ==========================================================================
# 4. event identity (K, L) — the §12 improvement
# ==========================================================================
def test_normalized_equivalent_submissions_are_one_event(owner):
    """K. The point of deriving identity from the STORED values: these four
    submissions produce the same durable row, so they are one event."""
    c, _aid, sid = owner
    for variant in ("The housing would be aluminium rather than ABS.",
                    "  The housing would be aluminium rather than ABS.",
                    "The housing would be aluminium rather than ABS.   ",
                    "\tThe housing would be aluminium rather than ABS. \n"):
        assert _record(c, sid, statement_text=variant).status_code == 302
    assert len(_rows(sid)) == 1, "whitespace variants created duplicate rows"
    assert _shown("UI_MEV_NOTICE_REPLAY") in _page(c, sid)


def test_an_exact_retry_remains_idempotent(owner):
    """L."""
    c, _aid, sid = owner
    for _ in range(5):
        assert _record(c, sid).status_code == 302
    assert len(_rows(sid)) == 1


def test_a_genuinely_different_item_is_not_deduplicated(owner):
    c, _aid, sid = owner
    _record(c, sid)
    _record(c, sid, statement_text="Actually ABS, because aluminium is heavy.")
    _record(c, sid, topic="tooling", statement_text="An injection mould would be needed.")
    assert len(_rows(sid)) == 3


def test_the_commercial_event_key_is_deliberately_unchanged(owner):
    """§12 allowed leaving Commercial alone rather than refactoring a merged,
    independently reviewed write path. The asymmetry is real and pinned here so
    it is visible rather than forgotten: Commercial still treats whitespace
    variants as distinct events."""
    c, _aid, sid = owner
    _record_commercial(c, sid)
    _record_commercial(c, sid, statement_text=" Under 400 per unit. ")
    assert len(_rows(sid, DIMENSION_COMMERCIAL)) == 2, (
        "Commercial de-duplication changed; the recorded asymmetry is stale")


# ==========================================================================
# 5. security (M, N, O, P)
# ==========================================================================
def test_project_isolation(owner):
    """M."""
    c, _aid, sid = owner
    other_sid = _start(c)
    _record(c, sid)
    _record(c, other_sid, topic="cost", statement_text="About 40 per unit.")
    assert [r.topic for r in _rows(sid)] == ["material"]
    assert [r.topic for r in _rows(other_sid)] == ["cost"]
    assert "aluminium" not in _page(c, other_sid).lower()


def test_cross_account_write_and_read_are_refused(owner):
    """N."""
    c, _aid, sid = owner
    _record(c, sid)
    other, _ = _client_for("mfg-intruder@example.com")
    assert other.post(MEV % sid, data=dict(MITEM)).status_code == 302
    assert len(_rows(sid)) == 1
    r = other.get(SESSION % sid)
    assert r.status_code in (302, 403, 404)
    assert "aluminium" not in r.get_data(as_text=True).lower()


def test_unauthenticated_and_unverified_cannot_write(owner):
    _c, _aid, sid = owner
    anon = _new_client()
    assert anon.post(MEV % sid, data=dict(MITEM)).status_code == 302
    unverified, _ = _client_for("mfg-unverified@example.com", verified=False)
    unverified.post(MEV % sid, data=dict(MITEM))
    assert _rows(sid) == ()


def test_csrf_is_enforced(owner):
    """O."""
    c, _aid, sid = owner
    raw = app.test_client()
    raw.post("/login", data={"email": "mfg-owner@example.com", "password": PW})
    assert raw.post(MEV % sid, data=dict(MITEM)).status_code in (400, 403)
    assert _rows(sid) == ()


def test_get_causes_zero_mutation(owner):
    """P."""
    c, _aid, sid = owner
    _record(c, sid)

    def snap():
        conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
        try:
            return conn.execute(
                "SELECT evidence_seq, evidence_id, dimension, topic FROM "
                "readiness_evidence ORDER BY project_id, evidence_seq").fetchall()
        finally:
            conn.close()

    before = snap()
    assert c.get(MEV % sid).status_code == 405
    for _ in range(4):
        assert c.get(SESSION % sid).status_code == 200
    assert snap() == before


def test_user_text_is_html_escaped(owner):
    """X."""
    c, _aid, sid = owner
    _record(c, sid, statement_text="<script>alert(1)</script> & <b>x</b>")
    body = _page(c, sid)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in body


# ==========================================================================
# 6. Readiness Snapshot must not change (R, S, T)
# ==========================================================================
def test_manufacturing_readiness_disposition_is_still_unreachable():
    """R, T. Activating evidence did not activate assessment."""
    # AMENDED at `MANUFACTURING-READINESS-SNAPSHOT-01`: Manufacturing now
    # reports evidence sufficiency, so it carries `INSUFFICIENT_EVIDENCE`.
    # What remains unreachable — and is the point of this test — is any
    # POSITIVE Manufacturing readiness state.
    assert rs.manufacturing_row(())["disposition"] == "INSUFFICIENT_EVIDENCE"
    assert rs.EMITTABLE_DISPOSITIONS == ("INSUFFICIENT_EVIDENCE",)
    import inspect
    code = re.sub(r'(?s)"{3}.*?"{3}', "", inspect.getsource(rs))
    code = "\n".join(l.split("#")[0] for l in code.splitlines())
    for token in ("PASS_WITH_CONDITIONS", "PASS", "HOLD"):
        assert token not in code, token


def test_ten_recorded_items_still_reach_no_positive_disposition(owner):
    """S, AMENDED. Recording ten Manufacturing items across every topic must not
    move Manufacturing toward a POSITIVE readiness state. It now reports that
    its evidence is insufficient, which is a statement about the evidence."""
    c, _aid, sid = owner
    for topic in MANUFACTURING_TOPICS:
        _record(c, sid, topic=topic,
                statement_text="A recorded statement about %s." % topic)
    assert len(_rows(sid, DIMENSION_MANUFACTURING)) == 10
    body = _page(c, sid)
    snapshot = _block(body, "rs")
    mfg_row = re.search(r'data-rs-dimension="manufacturing".*?</li>',
                        snapshot, re.S).group(0)
    # AMENDED: ten recorded items now produce an evidence-sufficiency reading
    # rather than silence — and still no positive state, which is what "volume
    # is not sufficiency" means here.
    assert 'data-rs-disposition="INSUFFICIENT_EVIDENCE"' in mfg_row
    assert "Recorded items: 10" in mfg_row
    for token in ("PASS_WITH_CONDITIONS", "PASS", "HOLD"):
        assert token not in mfg_row, token
    assert snapshot.count('data-rs-disposition="INSUFFICIENT_EVIDENCE"') == 3


def test_the_snapshot_reports_evidence_activation_without_implying_readiness():
    """The snapshot's dimension field describes EVIDENCE activation, composed
    from the canonical owner — not a readiness state."""
    from engine.idea_state import IdeaState
    snap = rs.readiness_snapshot(IdeaState(idea_id="x"), ())
    assert snap["evidence_dimensions_active"] == tuple(ACTIVE_DIMENSIONS)
    assert "active_dimensions" not in snap and "inactive_dimensions" not in snap


# ==========================================================================
# 7. product-truth wording (U, V, W)
# ==========================================================================
def test_no_manufacturing_conclusion_is_implied(owner):
    """§14."""
    c, _aid, sid = owner
    for topic in ("material", "process", "tooling", "cost", "supplier"):
        _record(c, sid, topic=topic, statement_text="A statement about %s." % topic)
    import html as _html
    prose = _html.unescape(re.sub(r"<[^>]+>", " ", _block(_page(c, sid), "mev"))).lower()
    for claim in ("manufacturable", "prototype-ready", "prototype ready",
                  "production-ready", "production ready", "inexpensive",
                  "cheap to", "tooling-ready", "supplier-ready", "scalable",
                  "bom-complete", "bom complete", "technically feasible",
                  "feasible", "ready to manufacture", "easy to make"):
        assert claim not in prose, claim
    assert _shown("UI_MEV_NOT_A_CONCLUSION") in _block(_page(c, sid), "mev")


def test_the_empty_state_is_not_negative_evidence(owner):
    c, _aid, sid = owner
    mev = _block(_page(c, sid), "mev")
    assert "data-mev-empty" in mev
    assert _shown("UI_MEV_EMPTY") in mev
    import html as _html
    prose = _html.unescape(re.sub(r"<[^>]+>", " ", mev)).lower()
    for implication in ("difficult to make", "cannot be made", "hard to make",
                        "not manufacturable", "manufacturing problem", "failed"):
        assert implication not in prose, implication


def test_no_cad_pcb_bom_or_supplier_functionality_appears(owner):
    """U. No engineering generation, no sourcing, no external lookup."""
    c, _aid, sid = owner
    _record(c, sid)
    body = _page(c, sid).lower()
    for banned in ("cad", "pcb", "gerber", "step file", "bill of materials",
                   "generate bom", "supplier search", "request a quote",
                   "get quotes", "sourcing"):
        assert banned not in body, banned
    source = open(os.path.join(os.path.dirname(__file__), "..", "web", "app.py"),
                  encoding="utf-8").read()
    start = source.index("def record_manufacturing_evidence")
    route = source[start:start + 6000]
    for banned in ("requests.", "urllib", "httpx", "socket.", "supplier_api",
                   "price_lookup", "scrape"):
        assert banned not in route, banned


def test_english_labels_render(owner):
    """V."""
    c, _aid, sid = owner
    body = _page(c, sid)
    for key in ("UI_MEV_HEADING", "UI_MEV_EXPLAIN", "UI_MEV_FIELD_TOPIC",
                "UI_MEV_FIELD_LIMITATION", "UI_MEV_SUBMIT",
                "UI_MEV_NOT_A_CONCLUSION"):
        assert _shown(key, "en") in body, key


def test_arabic_labels_render_and_text_is_direction_safe(owner):
    """W."""
    c, _aid, sid = owner
    arabic = "الهيكل الخارجي سيكون من الألومنيوم بدل البلاستيك."
    _record(c, sid, statement_text=arabic)
    c.post("/ui-language", data={"lang": "ar"})
    body = _page(c, sid)
    for key in ("UI_MEV_HEADING", "UI_MEV_EXPLAIN", "UI_MEV_SUBMIT",
                "UI_MEV_META_STANDING_VALUE", "UI_MEV_NOT_A_CONCLUSION"):
        assert _shown(key, "ar") in body, key
    assert _shown("UI_MEV_HEADING", "en") not in body
    assert arabic in body
    mev = _block(body, "mev")
    assert 'data-mev-statement dir="auto"' in mev
    for marker in ("data-mev-subject", "data-mev-source", "data-mev-scope",
                   "data-mev-limitation"):
        assert re.search(marker + r' dir="auto"', mev), marker


def test_every_manufacturing_string_has_both_languages():
    for key, entry in ui_text.UI_STRINGS.items():
        if not key.startswith("UI_MEV_"):
            continue
        for lang in ("en", "ar"):
            assert entry.get(lang), (key, lang)
        assert entry["en"] != entry["ar"], key


def test_topic_labels_are_used_not_raw_tokens(owner):
    """§18: no internal token surfaces where a label exists."""
    c, _aid, sid = owner
    _record(c, sid, topic="manufacturability",
            statement_text="A deep pocket would need a custom cutter.")
    mev = _block(_page(c, sid), "mev")
    assert _shown("UI_MEV_TOPIC_MANUFACTURABILITY") in mev
    for topic in MANUFACTURING_TOPICS:
        assert ">%s<" % topic not in mev, topic


def test_no_topic_token_collides_with_another_closed_vocabulary():
    """Adding a topic puts its raw token into the page as a static
    `<option value>`. A security test elsewhere asserts that a REJECTED input is
    not echoed back, and it does that by looking for the rejected string in the
    page — so a topic token that happens to equal some other vocabulary's probe
    value reads as an echo that never happened. `tolerance` did exactly that to
    the T2-A quantity suite. Checked here, at the source, so the next topic
    added is caught by its own suite rather than by an unrelated one."""
    from engine.requirement_quantity import QUANTITY_KINDS
    from engine.idea_state import (
        ASSERTED, DEMONSTRATED, REASONED, VALIDATION_STATUSES)
    from engine import decision_workspace as dw
    other_vocabularies = (
        set(QUANTITY_KINDS)
        | {ASSERTED, REASONED, DEMONSTRATED}
        | set(VALIDATION_STATUSES)
        | {dw.INSUFFICIENT_INFORMATION, dw.BLOCKED_BY_EVIDENCE_GAP,
           dw.COMPARISON_IN_PROGRESS, dw.DECISION_READY_FOR_OWNER_REVIEW}
        | set(COMMERCIAL_TOPICS))
    clashes = set(MANUFACTURING_TOPICS) & other_vocabularies
    assert not clashes, clashes


def test_the_route_is_in_the_r05_inventory():
    from tests.test_r05_request_integrity import MUTATIONS
    assert "/session/<sid>/manufacturing-evidence" in MUTATIONS
    registered = {rule.rule for rule in app.url_map.iter_rules()
                  if rule.methods - {"GET", "HEAD", "OPTIONS"}}
    assert registered <= set(MUTATIONS)
