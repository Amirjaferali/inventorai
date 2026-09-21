# -*- coding: utf-8 -*-
"""Commercial Evidence Capture — the inventor records what THEY know about the market.

`COMMERCIAL-EVIDENCE-CAPTURE-IMPLEMENT-01` (Owner-authorized). One bounded
user-facing slice on the existing saved-project page: view the Commercial
evidence already recorded for this project, and add one more item.

What these tests prove is mostly what the slice REFUSES to do. It is a live
writer into the authoritative Commercial Evidence Owner, so the interesting
questions are all about what cannot get through it: a forged provenance, a
promoted claim status, a topic outside the closed vocabulary, another account's
project, an accidental duplicate on retry, a state-changing GET. And it is the
first user-facing Commercial surface, so the other half is about what the page
is allowed to SAY: that the inventor recorded something, never that it is true,
sufficient, validated or promising.

Real Flask app, real on-disk SQLite, real accounts, real signed sessions, real
CSRF. Security boundaries are never mocked.
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
from engine.commercial_evidence import (
    CLAIM_STATUS_UNVALIDATED, COMMERCIAL_TOPICS, DEFAULT_PROVENANCE,
    DIMENSION_COMMERCIAL, MAX_STATEMENT_TEXT_CHARS,
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
CEV = "/session/%s/commercial-evidence"

GOOD = {
    "topic": "target_customer",
    "subject_text": "Home-care agencies buying mobility aids",
    "statement_text": "Agencies buy the ramps for clients, not families directly.",
    "source_identity": "Inventor, from their own experience",
    "occurred_on": "",
    "scope_text": "one local region the inventor knows",
    "limitation_text": "not checked against any agency or published source",
}


def _new_client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _mk_account(email, verified=True, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


def _client_for(email, verified=True, status="active"):
    aid = _mk_account(email, verified=verified, status=status)
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c, aid


def _page(client, sid):
    r = client.get(SESSION % sid)
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _token(client, sid):
    m = re.search(r'name="answer_token" value="([^"]+)"', _page(client, sid))
    return m.group(1) if m else None


def _start(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/session/", 1)[-1]
    assert client.post(SESSION % sid, data={
        "response": PROBLEM, "action": "answered",
        "answer_token": _token(client, sid)}).status_code == 302
    return sid


def _record(client, sid, **over):
    data = dict(GOOD)
    data.update(over)
    return client.post(CEV % sid, data=data)


def _rows(sid):
    return webapp._get_store().load_readiness_evidence(sid)


def _raw_rows(sid):
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return conn.execute(
            "SELECT topic, provenance, claim_status, dimension FROM "
            "readiness_evidence WHERE project_id = ? ORDER BY evidence_seq",
            (sid,)).fetchall()
    finally:
        conn.close()


@pytest.fixture
def owner():
    c, aid = _client_for("owner@example.com")
    return c, aid, _start(c)


# ==========================================================================
# 1. the owner can record, and it persists (A, H)
# ==========================================================================
def test_the_owner_can_record_commercial_evidence(owner):
    c, _aid, sid = owner
    assert _record(c, sid).status_code == 302
    rows = _rows(sid)
    assert len(rows) == 1
    row = rows[0]
    assert row.dimension == DIMENSION_COMMERCIAL
    assert row.topic == "target_customer"
    assert row.statement_text == GOOD["statement_text"]
    assert row.scope_text == GOOD["scope_text"]
    assert row.limitation_text == GOOD["limitation_text"]


def test_recorded_evidence_survives_a_reload(owner):
    """H. Persisted through the authoritative owner, not held in the page."""
    c, _aid, sid = owner
    _record(c, sid)
    SESSION_STORE.pop(sid, None)          # drop every runtime trace
    fresh = _new_client()
    fresh.post("/login", data={"email": "owner@example.com", "password": PW})
    body = fresh.get(SESSION % sid).get_data(as_text=True)
    assert GOOD["statement_text"] in body
    assert "data-cev-item" in body


def test_each_distinct_item_is_recorded_once(owner):
    c, _aid, sid = owner
    _record(c, sid)
    _record(c, sid, topic="price", subject_text="What an agency would pay",
            statement_text="An agency would expect to pay under 400 for a ramp.")
    assert [r.topic for r in _rows(sid)] == ["target_customer", "price"]


# ==========================================================================
# 2. who may write (B, C, I)
# ==========================================================================
def test_an_unauthenticated_request_cannot_write(owner):
    """B. Refused per the existing non-enumerating convention: a redirect that
    discloses nothing about whether the project exists."""
    _c, _aid, sid = owner
    anon = _new_client()
    r = anon.post(CEV % sid, data=dict(GOOD))
    assert r.status_code == 302
    assert "/login" not in r.headers["Location"]
    assert _rows(sid) == ()


def test_another_account_cannot_write_to_this_project(owner):
    """C. The ownership predicate is the same one every writing route uses."""
    _c, _aid, sid = owner
    other, _other_aid = _client_for("intruder@example.com")
    r = other.post(CEV % sid, data=dict(GOOD))
    assert r.status_code == 302
    assert _rows(sid) == ()


def test_an_unverified_or_inactive_account_cannot_write(owner):
    _c, _aid, sid = owner
    for email, kw in (("unverified@example.com", {"verified": False}),
                      ("disabled@example.com", {"status": "disabled"})):
        client, _ = _client_for(email, **kw)
        client.post(CEV % sid, data=dict(GOOD))
    assert _rows(sid) == ()


def test_projects_are_isolated(owner):
    """I. One account's two projects never see each other's evidence."""
    c, _aid, sid = owner
    other_sid = _start(c)
    _record(c, sid)
    _record(c, other_sid, topic="demand", subject_text="Who wants it",
            statement_text="Two agencies asked about a ramp last year.")
    assert [r.topic for r in _rows(sid)] == ["target_customer"]
    assert [r.topic for r in _rows(other_sid)] == ["demand"]
    assert GOOD["statement_text"] not in _page(c, other_sid)


# ==========================================================================
# 3. what may be written (D, E, F)
# ==========================================================================
def test_an_invalid_topic_is_rejected(owner):
    """D. The closed Commercial vocabulary, and nothing else."""
    c, _aid, sid = owner
    for bad in ("commercial_risk", "risk", "market_validated", "",
                "TARGET_CUSTOMER", "target customer", "../price"):
        assert _record(c, sid, topic=bad).status_code == 302
    assert _rows(sid) == ()


def test_the_form_offers_exactly_the_closed_topic_vocabulary(owner):
    c, _aid, sid = owner
    select = re.search(r'id="cev-topic".*?</select>', _page(c, sid), re.S).group(0)
    offered = re.findall(r'<option value="([^"]+)">', select)
    assert sorted(offered) == sorted(COMMERCIAL_TOPICS)
    assert not any("risk" in t for t in offered)


def test_provenance_is_forced_and_is_not_a_control(owner):
    """E. Fixed to OWNER_STATED. A submitted provenance is not merely ignored —
    the whole submission is refused, so a forged value never looks accepted."""
    c, _aid, sid = owner
    assert _record(c, sid, provenance="EXTERNAL_EVIDENCE").status_code == 302
    assert _rows(sid) == (), "a forged provenance field was accepted"
    _record(c, sid)
    assert _rows(sid)[0].provenance == DEFAULT_PROVENANCE == "OWNER_STATED"
    assert _raw_rows(sid)[0][1] == "OWNER_STATED"
    body = _page(c, sid)
    assert 'name="provenance"' not in body
    form = re.search(r'id="cev-form".*?</form>', body, re.S).group(0)
    # AMENDED at the Stage-17 D2 slice. The old assertion counted selects,
    # which was a proxy for "the topic is the only control". D2 adds four
    # authorized quantity controls, so the proxy is replaced by the thing it
    # stood for: the controls are ENUMERATED, and provenance and claim status
    # are not among them. An unauthorized fifth control fails here.
    # AMENDED AGAIN at D3: one further authorized control, the optional
    # supporting-item selector. Provenance and claim status are still not
    # controls and still cannot be.
    assert set(re.findall(r'<select name="([a-z_]+)"', form)) == {
        "topic", "value_state", "currency", "value_basis", "estimate_basis",
        "supporting_evidence_id"}
    assert 'name="provenance"' not in form
    assert 'name="claim_status"' not in form


def test_claim_status_is_forced_and_is_not_a_control(owner):
    """F. UNVALIDATED, always. Recording is never validating."""
    c, _aid, sid = owner
    for forged in ("claim_status", "validation_status", "readiness_status"):
        assert _record(c, sid, **{forged: "INDEPENDENTLY_VERIFIED"}).status_code == 302
    assert _rows(sid) == (), "a forged status field was accepted"
    _record(c, sid)
    assert _rows(sid)[0].claim_status == CLAIM_STATUS_UNVALIDATED == "UNVALIDATED"
    assert _raw_rows(sid)[0][2] == "UNVALIDATED"
    body = _page(c, sid)
    for name in ("claim_status", "validation_status", "readiness_status"):
        assert 'name="%s"' % name not in body


def test_over_limit_and_malformed_text_is_rejected(owner):
    c, _aid, sid = owner
    from web.app import MAX_FREE_TEXT_CHARS
    over = _record(c, sid, statement_text="y" * (MAX_FREE_TEXT_CHARS + 50))
    assert over.status_code in (302, 413), over.status_code
    assert _record(c, sid, subject_text="a NUL\x00inside").status_code == 302
    assert _record(c, sid, statement_text="").status_code == 302
    assert _record(c, sid, occurred_on="not-a-date").status_code == 302
    assert _rows(sid) == ()


def test_the_store_boundary_still_governs_beyond_the_form(owner):
    """The route validates what a web form must; the owner re-validates
    everything. An over-cap statement that passes the generic free-text guard is
    still refused at the durable boundary."""
    c, _aid, sid = owner
    long_statement = "a " * (MAX_STATEMENT_TEXT_CHARS // 2 + 200)
    assert len(long_statement) > MAX_STATEMENT_TEXT_CHARS
    assert _record(c, sid, statement_text=long_statement).status_code == 302
    assert _rows(sid) == ()


# ==========================================================================
# 4. idempotency and GET safety (G, O)
# ==========================================================================
def test_an_identical_retry_does_not_create_a_duplicate(owner):
    """G. A refresh or double-submit reproduces the same content, resolves to
    the same event key, and is acknowledged as the replay it is."""
    c, _aid, sid = owner
    _record(c, sid)
    for _ in range(4):
        assert _record(c, sid).status_code == 302
    assert len(_rows(sid)) == 1
    assert ui_text.text("UI_CEV_NOTICE_REPLAY", "en") in _page(c, sid)


def test_a_genuinely_different_item_is_not_deduplicated(owner):
    c, _aid, sid = owner
    _record(c, sid)
    _record(c, sid, statement_text="Actually families buy them directly.")
    assert len(_rows(sid)) == 2


def test_get_performs_no_write(owner):
    """O. There is no state-changing GET anywhere on this surface."""
    c, _aid, sid = owner
    _record(c, sid)
    before = _raw_rows(sid)
    for _ in range(3):
        assert c.get(SESSION % sid).status_code == 200
    assert c.get(CEV % sid).status_code == 405
    assert _raw_rows(sid) == before


def test_csrf_is_enforced(owner):
    """The global protection applies to this route like every other POST."""
    c, _aid, sid = owner
    raw = app.test_client()                       # no CSRF token injection
    raw.post("/login", data={"email": "owner@example.com", "password": PW})
    r = raw.post(CEV % sid, data=dict(GOOD))
    assert r.status_code in (400, 403), r.status_code
    assert _rows(sid) == ()


# ==========================================================================
# 5. what the page says (J, K, L, M, N)
# ==========================================================================
def test_the_empty_state_is_truthful_and_not_a_finding(owner):
    """J. Absence of evidence is not negative evidence."""
    c, _aid, sid = owner
    body = _page(c, sid)
    assert "data-cev-empty" in body
    assert ui_text.text("UI_CEV_EMPTY", "en") in body
    lowered = body.lower()
    for implication in ("insufficient market", "poor commercial",
                        "no demand", "weak market", "failed"):
        assert implication not in lowered, implication


def test_english_labels_render(owner):
    """K."""
    c, _aid, sid = owner
    body = _page(c, sid)
    for key in ("UI_CEV_HEADING", "UI_CEV_EXPLAIN", "UI_CEV_FIELD_TOPIC",
                "UI_CEV_FIELD_STATEMENT", "UI_CEV_FIELD_LIMITATION",
                "UI_CEV_SUBMIT"):
        assert ui_text.text(key, "en") in body, key


def test_arabic_labels_render_and_user_text_is_rtl_safe(owner):
    """L. Chrome switches language; the inventor's own text is never
    translated, and every field carrying it is direction-aware."""
    c, _aid, sid = owner
    arabic_statement = "الوكالات تشتري المنحدرات للعملاء وليس العائلات مباشرة."
    _record(c, sid, statement_text=arabic_statement)
    c.post("/ui-language", data={"lang": "ar"})
    body = _page(c, sid)
    for key in ("UI_CEV_HEADING", "UI_CEV_EXPLAIN", "UI_CEV_FIELD_TOPIC",
                "UI_CEV_SUBMIT", "UI_CEV_META_STANDING_VALUE"):
        assert ui_text.text(key, "ar") in body, key
    assert ui_text.text("UI_CEV_HEADING", "en") not in body
    assert arabic_statement in body                # never translated
    assert 'data-cev-statement dir="auto"' in body
    for marker in ("data-cev-subject", "data-cev-source", "data-cev-scope",
                   "data-cev-limitation"):
        assert re.search(marker + r' dir="auto"', body), marker


def test_every_topic_has_both_languages():
    for topic in COMMERCIAL_TOPICS:
        key = "UI_CEV_TOPIC_" + topic.upper()
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang), (key, lang)
        assert ui_text.text(key, "en") != ui_text.text(key, "ar")


def test_no_readiness_vocabulary_appears_on_the_page(owner):
    """M, AMENDED at `READINESS-SNAPSHOT-RUNTIME-01`.

    This lane still computes no Readiness disposition — that has not changed.
    What changed is the page it shares: the Owner has since authorized the
    Readiness Snapshot, which renders exactly ONE canonical disposition,
    `INSUFFICIENT_EVIDENCE`. So the assertion narrows from "no canonical token
    at all" to what still holds and matters more: no POSITIVE disposition
    anywhere, and nothing from THIS block naming a Readiness state."""
    c, _aid, sid = owner
    _record(c, sid)
    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        body = _page(c, sid)
        for token in ("PASS_WITH_CONDITIONS", "PASS_WITH", "HOLD",
                      "Commercial Readiness", "readiness score",
                      "Readiness score"):
            assert token not in body, (lang, token)
        # The one canonical token on the page belongs to the snapshot block,
        # never to this one.
        cev = re.search(r'id="cev-commercial-evidence".*?</details>',
                        body, re.S).group(0)
        assert "INSUFFICIENT_EVIDENCE" not in cev, lang


def test_no_marketability_or_profitability_claim_appears(owner):
    """N. The block reports what was recorded and offers no opinion on it."""
    c, _aid, sid = owner
    _record(c, sid)
    lowered = _page(c, sid).lower()
    for claim in ("marketable", "market-ready", "market ready", "profitab",
                  "investment ready", "investment-ready", "strong demand",
                  "high commercial potential", "commercially attractive",
                  "validated price", "validated willingness",
                  "viable business", "good opportunity"):
        assert claim not in lowered, claim
    # `proven` as a WORD: the letters also occur inside "provenance", which is
    # the metadata attribute name and not a claim about the evidence.
    assert not re.search(r"\bproven\b", lowered)


def test_provenance_and_claim_status_are_explanatory_not_controls(owner):
    c, _aid, sid = owner
    _record(c, sid)
    body = _page(c, sid)
    assert ui_text.text("UI_CEV_META_ORIGIN_VALUE", "en") in body
    assert ui_text.text("UI_CEV_META_STANDING_VALUE", "en") in body
    assert ui_text.text("UI_CEV_META_NOTE", "en") in body
    # the metadata is rendered as data attributes and prose, never as inputs
    assert 'data-cev-provenance="OWNER_STATED"' in body
    assert 'data-cev-claim-status="UNVALIDATED"' in body
    assert 'name="provenance"' not in body and 'name="claim_status"' not in body


def test_user_text_is_html_escaped(owner):
    c, _aid, sid = owner
    _record(c, sid, statement_text="<script>alert(1)</script> & <b>bold</b>")
    body = _page(c, sid)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in body
    assert "&amp;" in body


# ==========================================================================
# 6. boundaries this slice must not cross
# ==========================================================================
def test_this_blocks_copy_never_borrows_a_settled_status_word():
    """`test_g3_decision_value.py::test_a22` bans a short list of tokens
    anywhere on the session page, so a withdrawn decision alternative can never
    read as an approved, certified or validated one. This block shares that page
    and must not reintroduce one of those words through its own copy — including
    inside an explicit negation, which is how it happened once already."""
    banned = ("eliminated", "Eliminated", "ELIMINATED", "technically_selected",
              "approved", "validated", "certified", "production_ready")
    offenders = []
    for key, entry in ui_text.UI_STRINGS.items():
        if not key.startswith("UI_CEV_"):
            continue
        for lang in ("en", "ar"):
            for token in banned:
                if token in entry.get(lang, ""):
                    offenders.append("%s[%s]: %s" % (key, lang, token))
    assert not offenders, offenders


def test_the_write_route_is_in_the_r05_unsafe_route_inventory():
    """A new state-changing route must be enumerated in the R-05 security
    inventory, which is what subjects it to the CSRF/auth integrity matrix.
    Pinned here too so the coupling is visible from this slice's own suite."""
    from tests.test_r05_request_integrity import MUTATIONS
    assert "/session/<sid>/commercial-evidence" in MUTATIONS
    registered = {rule.rule for rule in app.url_map.iter_rules()
                  if rule.methods - {"GET", "HEAD", "OPTIONS"}}
    assert registered <= set(MUTATIONS)


def test_no_readiness_conclusion_is_computed_anywhere_in_this_lane():
    source = open(os.path.join(os.path.dirname(__file__), "..", "web", "app.py"),
                  encoding="utf-8").read()
    start = source.index("def record_commercial_evidence")
    end = source.index("def ", source.index("return redirect", start) + 200)
    route = source[start:end]
    for banned in ("PASS_WITH_CONDITIONS", "INSUFFICIENT_EVIDENCE", "score",
                   "marketab", "derive_readiness", "manufacturing"):
        assert banned not in route, banned


def test_manufacturing_is_unreachable_from_the_COMMERCIAL_capture_route(owner):
    """AMENDED at `MANUFACTURING-EVIDENCE-OWNER-IMPLEMENT-01`.

    Manufacturing is now an activated evidence dimension with its own route, so
    "inactive" is no longer the truth to pin. What still holds is the boundary
    THIS route owns: the Commercial route writes Commercial rows and nothing
    else. A submission naming a dimension is refused whole, and no Manufacturing
    row can be created through this path."""
    from engine.commercial_evidence import (
        ACTIVE_DIMENSIONS, DIMENSION_MANUFACTURING, TOPICS_BY_DIMENSION)
    assert DIMENSION_MANUFACTURING in ACTIVE_DIMENSIONS
    assert TOPICS_BY_DIMENSION[DIMENSION_MANUFACTURING] != ()
    c, _aid, sid = owner
    assert _record(c, sid, dimension=DIMENSION_MANUFACTURING).status_code == 302
    assert _rows(sid) == (), "a dimension field was honoured by the route"
    # A Manufacturing topic is not valid on the Commercial route either.
    assert _record(c, sid, topic="material").status_code == 302
    assert _rows(sid) == ()
    # And a genuine Commercial write still lands as COMMERCIAL.
    _record(c, sid)
    assert [r.dimension for r in _rows(sid)] == [DIMENSION_COMMERCIAL]


def test_the_commercial_owner_remains_the_sole_durable_store(owner):
    """No shadow list, no cache, no parallel model: what the page shows comes
    from the durable table and nowhere else."""
    c, _aid, sid = owner
    _record(c, sid)
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    finally:
        conn.close()
    assert "readiness_evidence" in tables
    # The pre-existing `commercial_*` tables are the P8 billing/quota lane — a
    # different concern this slice neither reads, writes nor duplicates. What
    # must not exist is a SECOND store for commercial EVIDENCE.
    assert not [t for t in tables
                if "evidence" in t.lower() and t != "readiness_evidence"
                and t != "evidence_references"]
    entry = SESSION_STORE.get(sid) or {}
    assert not [k for k in entry if "commercial" in str(k).lower()
                and k not in ("_cev_ack", "_cev_error")]


def test_no_technical_or_decision_surface_changed(owner):
    """Cross-dimension separation: recording Commercial evidence moves no
    Technical readiness, no gap, no maturity and no decision state."""
    from engine.derived_readiness import derive_readiness
    c, _aid, sid = owner
    state = SESSION_STORE[sid]["state"]
    before = (state.maturity_level, [(g.gap_type, g.status) for g in state.gaps],
              len(state.assertions), derive_readiness(state).overall_verified())
    _record(c, sid)
    state = SESSION_STORE[sid]["state"]
    after = (state.maturity_level, [(g.gap_type, g.status) for g in state.gaps],
             len(state.assertions), derive_readiness(state).overall_verified())
    assert after == before
    assert after[3] is False


# ==========================================================================
# The Commercial evidence GAP block
#
# The block names the governed topics nothing has been recorded for. Its entire
# risk is that a reader takes an empty topic for a finding about their market,
# so most of what follows is about what the block must NOT say, in BOTH
# languages, and about the one state where it must not appear at all.
# ==========================================================================
_GAP_ITEM = re.compile(r'data-cev-gap-topic="([a-z_]+)"')


def _gap_topics(body):
    return _GAP_ITEM.findall(body)


def test_a_project_with_no_commercial_evidence_lists_every_topic_as_a_gap(owner):
    c, _aid, sid = owner
    body = _page(c, sid)
    assert _gap_topics(body) == list(COMMERCIAL_TOPICS)
    assert ui_text.text("UI_CEV_GAP_HEADING", "en") in body


def test_recording_one_item_removes_exactly_that_topic_from_the_gaps(owner):
    c, _aid, sid = owner
    _record(c, sid, topic="demand",
            statement_text="Two agencies asked about a ramp last year.")
    gaps = _gap_topics(_page(c, sid))
    assert "demand" not in gaps
    assert len(gaps) == len(COMMERCIAL_TOPICS) - 1
    assert set(gaps) | {"demand"} == set(COMMERCIAL_TOPICS)


def test_full_coverage_renders_no_gap_block_at_all(owner):
    """A covered project is shown no empty list \u2014 and is not congratulated
    either: the block simply is not there, because "complete" would be a
    conclusion and this page draws none."""
    c, _aid, sid = owner
    for i, topic in enumerate(COMMERCIAL_TOPICS):
        r = _record(c, sid, topic=topic,
                    subject_text="subject %d" % i,
                    statement_text="a recorded statement number %d" % i)
        assert r.status_code in (302, 303), (topic, r.status_code)
    body = _page(c, sid)
    assert _gap_topics(body) == []
    assert ui_text.text("UI_CEV_GAP_HEADING", "en") not in body
    assert ui_text.text("UI_CEV_GAP_HEADING", "ar") not in body
    assert "data-cev-gap-list" not in body


def test_manufacturing_evidence_does_not_close_a_commercial_gap(owner):
    """The page's two evidence blocks read their own dimensions only."""
    c, _aid, sid = owner
    r = c.post("/session/%s/manufacturing-evidence" % sid, data={
        "topic": "material",
        "subject_text": "Aluminium extrusion for the ramp frame",
        "statement_text": "The frame is most likely aluminium extrusion.",
        "source_identity": "Inventor, from their own experience",
        "occurred_on": "",
        "scope_text": "the frame only",
        "limitation_text": "not checked against any supplier",
    })
    assert r.status_code in (302, 303), r.status_code
    assert _gap_topics(_page(c, sid)) == list(COMMERCIAL_TOPICS)


def test_the_gap_block_renders_in_arabic_and_says_the_same_thing(owner):
    """EN and AR must both carry the disclaimer. A gap list that warned in one
    language only would be worse than no list."""
    c, _aid, sid = owner
    c.post("/ui-language", data={"lang": "ar"})
    body = _page(c, sid)
    for key in ("UI_CEV_GAP_HEADING", "UI_CEV_GAP_EXPLAIN"):
        assert ui_text.text(key, "ar") in body, key
        assert ui_text.text(key, "en") not in body, key
    assert _gap_topics(body) == list(COMMERCIAL_TOPICS)
    # the topic labels themselves are the Arabic ones
    assert ui_text.text("UI_CEV_TOPIC_DEMAND", "ar") in body


def test_both_languages_carry_the_same_four_statements():
    """Semantic alignment, element by element rather than by length.

    The copy deliberately never quotes the readings it denies \u2014 saying "there
    is no market" in order to deny it would put that phrase on the page, where a
    substring guard and a skimming reader would both find it. So each language
    is checked for the four things it DOES say."""
    en = ui_text.text("UI_CEV_GAP_EXPLAIN", "en")
    ar = ui_text.text("UI_CEV_GAP_EXPLAIN", "ar")
    assert en and ar and en != ar
    for fragment in ("nothing has been written down",   # an empty topic means only that
                     "not a conclusion",                # not a finding
                     "not a measurement",               # not a score
                     "the order below"):                # order carries no priority
        assert fragment in en, fragment
    for fragment in ("\u0644\u0645 \u064a\u064f\u0643\u062a\u0628 \u0639\u0646\u0647 \u0634\u064a\u0621",
                     "\u0644\u064a\u0633 \u0627\u0633\u062a\u0646\u062a\u0627\u062c\u064b\u0627",
                     "\u0648\u0644\u064a\u0633 \u0642\u064a\u0627\u0633\u064b\u0627",
                     "\u0648\u0627\u0644\u062a\u0631\u062a\u064a\u0628 \u0623\u062f\u0646\u0627\u0647"):
        assert fragment in ar, fragment


def test_the_gap_wording_never_states_a_finding_about_the_market(owner):
    """The forbidden readings, scanned on the rendered page in both languages."""
    c, _aid, sid = owner
    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        body = _page(c, sid).lower()
        for claim in ("no market exists", "there is no market",
                      "no demand exists", "there is no demand",
                      "not viable", "no viability exists",
                      "commercially unready", "commercial readiness failed",
                      "not marketable", "market validated",
                      "demand proven", "product-market fit"):
            assert claim not in body, (lang, claim)


def test_the_gap_block_introduces_no_score_ranking_or_promotion(owner):
    """No count, percentage, level or disposition may appear with the gaps."""
    c, _aid, sid = owner
    _record(c, sid, topic="price", statement_text="A ramp sells around 400.")
    body = _page(c, sid)
    start = body.index("data-cev-gap-explain")
    end = body.index("</ul>", body.index("data-cev-gap-list"))
    block = body[start:end]
    for forbidden in ("%", "PASS", "PASS_WITH_CONDITIONS", "HOLD",
                      "INSUFFICIENT_EVIDENCE", "score", "level",
                      "14 of 15", "1/15"):
        assert forbidden not in block, forbidden
    # and the list is the vocabulary order, never re-sorted into a priority
    gaps = _gap_topics(body)
    assert gaps == [t for t in COMMERCIAL_TOPICS if t != "price"]


# ==========================================================================
# D1 — lifecycle reachability: correct, withdraw, and the history that results
#
# The owner has always supported supersession and withdrawal; until now no
# product path reached them, so no commercial assumption could be corrected and
# none could be seen changing. These tests are mostly about the two things a
# lifecycle can get wrong: losing history, and letting one act mean another.
# ==========================================================================
CEV_CORRECT = "/session/%s/commercial-evidence/correct"
CEV_WITHDRAW = "/session/%s/commercial-evidence/withdraw"


def _active(sid):
    from engine.commercial_evidence import active_evidence
    return active_evidence(_rows(sid), DIMENSION_COMMERCIAL)


def _only_active(sid):
    rows = _active(sid)
    assert len(rows) == 1, [r.evidence_id for r in rows]
    return rows[0]


def _correct(client, sid, prior_id, **over):
    data = dict(GOOD)
    data.pop("topic")                       # the topic is carried, never posted
    data.update(over)
    data["supersedes_evidence_id"] = prior_id
    return client.post(CEV_CORRECT % sid, data=data)


def _withdraw(client, sid, prior_id):
    return client.post(CEV_WITHDRAW % sid,
                       data={"supersedes_evidence_id": prior_id})


def test_a_correction_appends_and_never_mutates_the_old_row(owner):
    """1 + 2. The old row survives byte-for-byte and is superseded by the new."""
    c, _aid, sid = owner
    _record(c, sid, topic="demand", statement_text="Two agencies asked.")
    first = _only_active(sid)
    before = _raw_rows(sid)

    assert _correct(c, sid, first.evidence_id,
                    statement_text="Two agencies asked, one twice."
                    ).status_code in (302, 303)

    rows = _rows(sid)
    assert len(rows) == 2                       # appended, not replaced
    old = [r for r in rows if r.evidence_id == first.evidence_id][0]
    assert old.statement_text == "Two agencies asked."      # untouched
    assert old.topic == first.topic and old.event_key == first.event_key
    new = [r for r in rows if r.evidence_id != first.evidence_id][0]
    assert new.supersedes_evidence_id == first.evidence_id
    assert new.withdrawn is False
    assert len(_raw_rows(sid)) == len(before) + 1


def test_the_correction_becomes_the_active_item(owner):
    """3. The active view returns the replacement, and only it."""
    c, _aid, sid = owner
    _record(c, sid, topic="price", statement_text="A ramp sells around 400.")
    first = _only_active(sid)
    _correct(c, sid, first.evidence_id,
             statement_text="A ramp sells around 450.")
    active = _only_active(sid)
    assert active.evidence_id != first.evidence_id
    assert active.statement_text == "A ramp sells around 450."
    body = _page(c, sid)
    assert "A ramp sells around 450." in body
    # the earlier version is not gone — it is shown as history
    assert "A ramp sells around 400." in body
    assert 'data-cev-history-state="replaced"' in body


def test_a_correction_does_not_uncover_the_topic(owner):
    """4. Coverage follows the ACTIVE replacement, not the superseded row."""
    c, _aid, sid = owner
    _record(c, sid, topic="licensing", statement_text="No licence needed here.")
    first = _only_active(sid)
    assert "licensing" not in _gap_topics(_page(c, sid))
    _correct(c, sid, first.evidence_id,
             statement_text="A local permit may be needed.")
    assert "licensing" not in _gap_topics(_page(c, sid))
    assert _only_active(sid).topic == "licensing"


def test_a_correction_carries_the_topic_and_cannot_refile_it(owner):
    """The topic is not a field of this route; posting one is refused WHOLE."""
    c, _aid, sid = owner
    _record(c, sid, topic="channel", statement_text="Sold through agencies.")
    first = _only_active(sid)
    r = _correct(c, sid, first.evidence_id, topic="price")
    assert r.status_code in (302, 303)
    assert len(_rows(sid)) == 1                 # refused, nothing appended
    assert _only_active(sid).evidence_id == first.evidence_id


def test_a_withdrawal_preserves_history_and_empties_the_active_view(owner):
    """5 + 6. The chain stops contributing; every row of it is retained."""
    c, _aid, sid = owner
    _record(c, sid, topic="funding_need",
            statement_text="About 20k to reach a first batch.")
    first = _only_active(sid)

    assert _withdraw(c, sid, first.evidence_id).status_code in (302, 303)

    rows = _rows(sid)
    assert len(rows) == 2
    kept = [r for r in rows if r.evidence_id == first.evidence_id][0]
    assert kept.statement_text == "About 20k to reach a first batch."
    assert kept.withdrawn is False              # the ORIGINAL is not rewritten
    withdrawal = [r for r in rows if r.evidence_id != first.evidence_id][0]
    assert withdrawal.withdrawn is True
    assert withdrawal.supersedes_evidence_id == first.evidence_id
    assert _active(sid) == ()


def test_a_withdrawal_uncovers_the_topic_only_when_nothing_else_covers_it(owner):
    """7. Two items on one topic: withdrawing one leaves the topic covered."""
    c, _aid, sid = owner
    _record(c, sid, topic="demand", subject_text="first",
            statement_text="One agency asked in spring.")
    _record(c, sid, topic="demand", subject_text="second",
            statement_text="Another asked in autumn.")
    assert "demand" not in _gap_topics(_page(c, sid))
    one = [r for r in _active(sid) if r.subject_text == "first"][0]

    _withdraw(c, sid, one.evidence_id)
    assert "demand" not in _gap_topics(_page(c, sid))    # still covered

    other = _only_active(sid)
    _withdraw(c, sid, other.evidence_id)
    assert "demand" in _gap_topics(_page(c, sid))        # now uncovered


def test_lifecycle_acts_cannot_cross_the_two_dimensions(owner):
    """8. A Manufacturing row is not a valid target for a Commercial act."""
    c, _aid, sid = owner
    assert c.post("/session/%s/manufacturing-evidence" % sid, data={
        "topic": "material",
        "subject_text": "Aluminium extrusion",
        "statement_text": "The frame is most likely aluminium extrusion.",
        "source_identity": "Inventor, from their own experience",
        "occurred_on": "",
        "scope_text": "the frame only",
        "limitation_text": "not checked against any supplier",
    }).status_code in (302, 303)
    mfg = [r for r in _rows(sid) if r.dimension != DIMENSION_COMMERCIAL]
    assert len(mfg) == 1
    before = len(_rows(sid))

    assert _correct(c, sid, mfg[0].evidence_id).status_code in (302, 303)
    assert _withdraw(c, sid, mfg[0].evidence_id).status_code in (302, 303)

    assert len(_rows(sid)) == before            # both refused, nothing appended
    assert [r for r in _rows(sid) if r.dimension != DIMENSION_COMMERCIAL][0] \
        .withdrawn is False


def test_invalid_stale_and_foreign_targets_all_fail_closed(owner):
    """9. Unknown id, already-superseded id, withdrawn id, another account's
    project and an empty target are each refused with nothing appended."""
    c, _aid, sid = owner
    _record(c, sid, topic="market_entry", statement_text="Start locally.")
    first = _only_active(sid)
    _correct(c, sid, first.evidence_id, statement_text="Start in one city.")
    replacement = _only_active(sid)
    count = len(_rows(sid))

    for bad in ("", "not-an-id", first.evidence_id):   # last is already stale
        assert _correct(c, sid, bad).status_code in (302, 303)
        assert _withdraw(c, sid, bad).status_code in (302, 303)
    assert len(_rows(sid)) == count

    _withdraw(c, sid, replacement.evidence_id)          # now withdrawn
    count = len(_rows(sid))
    assert _correct(c, sid, replacement.evidence_id).status_code in (302, 303)
    assert len(_rows(sid)) == count

    other, _other_id = _client_for("intruder@example.com")
    assert _correct(other, sid, replacement.evidence_id).status_code in (302, 303, 403, 404)
    assert _withdraw(other, sid, replacement.evidence_id).status_code in (302, 303, 403, 404)
    assert len(_rows(sid)) == count


def test_a_retried_lifecycle_act_is_a_replay_not_a_second_row(owner):
    """The create path's durability discipline, held by the lifecycle path."""
    c, _aid, sid = owner
    _record(c, sid, topic="revenue_model", statement_text="One-off sale.")
    first = _only_active(sid)
    _correct(c, sid, first.evidence_id, statement_text="Sold once, not leased.")
    count = len(_rows(sid))
    _correct(c, sid, first.evidence_id, statement_text="Sold once, not leased.")
    assert len(_rows(sid)) == count             # identical retry appended nothing


def test_the_history_surface_renders_in_both_languages(owner):
    """10. EN and AR carry the same lifecycle meaning, states included."""
    c, _aid, sid = owner
    _record(c, sid, topic="target_customer", statement_text="Home-care agencies.")
    first = _only_active(sid)
    _correct(c, sid, first.evidence_id, statement_text="Agencies, not families.")
    second = _only_active(sid)
    _record(c, sid, topic="price", subject_text="p", statement_text="Around 400.")
    third = [r for r in _active(sid) if r.topic == "price"][0]
    _withdraw(c, sid, third.evidence_id)

    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        body = _page(c, sid)
        for key in ("UI_CEV_HISTORY_HEADING", "UI_CEV_HISTORY_EXPLAIN",
                    "UI_CEV_STATE_REPLACED", "UI_CEV_STATE_WITHDRAWN",
                    "UI_CEV_CORRECT_HEADING", "UI_CEV_CORRECT_EXPLAIN",
                    "UI_CEV_WITHDRAW_SUBMIT", "UI_CEV_WITHDRAW_EXPLAIN"):
            assert ui_text.text(key, lang) in body, (lang, key)
        assert 'data-cev-history-state="replaced"' in body
        assert 'data-cev-history-state="withdrawn"' in body
    # and the owner's own words are never translated
    assert "Home-care agencies." in _page(c, sid)
    assert second.statement_text == "Agencies, not families."


def test_both_lifecycle_notices_exist_in_both_languages():
    for key in ("UI_CEV_NOTICE_CORRECTED", "UI_CEV_NOTICE_WITHDRAWN",
                "UI_CEV_STATE_REPLACED", "UI_CEV_STATE_WITHDRAWN"):
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang), (key, lang)
        assert ui_text.text(key, "en") != ui_text.text(key, "ar"), key


def test_the_history_presentation_carries_no_ranking_or_promotion(owner):
    """11. History is a record, not an assessment."""
    c, _aid, sid = owner
    _record(c, sid, topic="differentiation", statement_text="Lighter frame.")
    first = _only_active(sid)
    _correct(c, sid, first.evidence_id, statement_text="Lighter and cheaper.")
    body = _page(c, sid)
    start = body.index("data-cev-history-explain")
    end = body.index("</ul>", body.index("data-cev-history-list"))
    block = body[start:end]
    for forbidden in ("%", "PASS", "HOLD", "INSUFFICIENT_EVIDENCE", "score",
                      "SPECIALIST_REVIEWED", "INDEPENDENTLY_VERIFIED",
                      "better", "worse", "improved"):
        assert forbidden not in block, forbidden
    # every row still carries the one frozen claim status
    assert all(r.claim_status == CLAIM_STATUS_UNVALIDATED for r in _rows(sid))


def test_the_gap_behaviour_is_unchanged_by_the_lifecycle_slice(owner):
    """12. D1 does not disturb what the previous slice established."""
    c, _aid, sid = owner
    assert _gap_topics(_page(c, sid)) == list(COMMERCIAL_TOPICS)
    _record(c, sid, topic="willingness_to_pay", statement_text="Maybe 400.")
    gaps = _gap_topics(_page(c, sid))
    assert "willingness_to_pay" not in gaps
    assert len(gaps) == len(COMMERCIAL_TOPICS) - 1
    item = _only_active(sid)
    _correct(c, sid, item.evidence_id, statement_text="Maybe 450.")
    assert _gap_topics(_page(c, sid)) == gaps          # correction changes nothing
    _withdraw(c, sid, _only_active(sid).evidence_id)
    assert _gap_topics(_page(c, sid)) == list(COMMERCIAL_TOPICS)


def test_a_read_only_session_offers_no_lifecycle_affordance(owner):
    """The writable gate governs the new forms exactly as it governs the old."""
    c, _aid, sid = owner
    _record(c, sid, topic="demand", statement_text="One agency asked.")
    body = _page(c, sid)
    assert "data-cev-correct-submit" in body and "data-cev-withdraw-submit" in body
    other, _oid = _client_for("reader@example.com")
    foreign = other.get(SESSION % sid)
    assert foreign.status_code in (302, 303, 403, 404)


# ==========================================================================
# D2 — quantitative commercial structure
#
# APPROXIMATE IS NOT ARBITRARY. Almost everything below is about refusal: a
# number with nothing behind it, a range that is really a guess, a midpoint
# nobody supplied, a currency nobody chose. NONE is a real answer here, and the
# tests treat it as one.
# ==========================================================================
Q_EXACT = {"value_state": "EXACT", "value_exact": "120", "currency": "USD",
           "value_basis": "per_unit", "estimate_basis": "supplier_quote",
           "estimate_rationale": "one quote from a local supplier"}
Q_RANGE = {"value_state": "ESTIMATED_RANGE", "value_min": "100",
           "value_max": "150", "currency": "USD", "value_basis": "per_unit",
           "estimate_basis": "comparable_product_price",
           "estimate_rationale": "two comparable ramps, assuming the same size"}


def _rendered(key, lang):
    """A UI string as it appears in the PAGE, not as it appears in the table.

    Jinja escapes HTML, so a label carrying an apostrophe ("A comparable
    product's price") reaches the body as `&#39;`. Comparing the raw string
    would fail for a correct page, so the escaping is applied here rather than
    removed from the copy."""
    from markupsafe import escape
    return str(escape(ui_text.text(key, lang)))


def _q(client, sid, topic="price", **over):
    data = dict(GOOD)
    data["topic"] = topic
    data.update(over)
    return client.post(CEV % sid, data=data)


def _item_region(body, topic):
    """The rendered region of ONE recorded commercial-evidence item.

    Runs from that item's marker to the next item's, so an assertion about
    what THIS item displays cannot be answered by another item's markup.
    """
    start = body.index('data-cev-item data-cev-topic="%s"' % topic)
    nxt = body.find("data-cev-item ", start + 1)
    return body[start:nxt if nxt != -1 else len(body)]


def _amount_display(body, topic="price"):
    """The element that renders an item's amount — the D2 display contract.

    A quantity assertion belongs here and nowhere wider. The full page also
    carries evidence ids, option values and signed tokens, which are random
    hex and therefore contain arbitrary digit runs; a page-wide substring
    check for a number is a statement about those identifiers, not about the
    displayed amount, and fails on a dice roll rather than on a defect.
    """
    region = _item_region(body, topic)
    m = re.search(r"<p[^>]*data-cev-amount\b.*?</p>", region, re.S)
    assert m, "topic %s renders no amount element" % topic
    return m.group(0)


def _amount_value(body, topic="price"):
    """Just the amount itself, as the page shows it to a reader."""
    m = re.search(r"<span data-cev-amount-value>(.*?)</span>",
                  _amount_display(body, topic), re.S)
    assert m, "the amount element renders no value"
    return m.group(1).strip()


def _quantity_form_values(body, topic="price"):
    """(exact, min, max) as pre-filled into that item's correction form.

    A midpoint could be invented in the form as easily as in the display, so
    both surfaces are checked.
    """
    region = _item_region(body, topic)
    out = []
    for field in ("value_exact", "value_min", "value_max"):
        m = re.search(r'<input[^>]*name="%s"[^>]*value="([^"]*)"' % field,
                      region)
        assert m, "no %s input rendered for topic %s" % (field, topic)
        out.append(m.group(1))
    return tuple(out)


def test_an_exact_amount_is_stored_as_one_truthful_value(owner):
    """1 + 8. The amount and the currency are separate stored fields."""
    c, _aid, sid = owner
    assert _q(c, sid, **Q_EXACT).status_code in (302, 303)
    row = _only_active(sid)
    assert row.value_state == "EXACT"
    assert row.value_exact == "120"
    assert row.currency == "USD"                 # never inside the amount
    assert row.value_min == "" and row.value_max == ""
    assert row.value_basis == "per_unit"
    assert row.estimate_basis == "supplier_quote"


def test_an_estimated_range_stores_min_and_max_distinctly(owner):
    """2 + 6. Both ends are kept, and NO midpoint is synthesised anywhere."""
    c, _aid, sid = owner
    assert _q(c, sid, **Q_RANGE).status_code in (302, 303)
    row = _only_active(sid)
    assert row.value_state == "ESTIMATED_RANGE"
    assert row.value_min == "100" and row.value_max == "150"
    assert row.value_exact == ""                 # no collapsed single value
    body = _page(c, sid)
    assert "125" not in body                     # the midpoint is never derived
    assert "100" in body and "150" in body


def test_none_stores_no_invented_number(owner):
    """3 + 16. NONE is a recorded answer and it renders as absence, not zero."""
    c, _aid, sid = owner
    assert _q(c, sid).status_code in (302, 303)   # no quantity fields sent
    row = _only_active(sid)
    assert row.value_state == "NONE"
    for field in ("value_exact", "value_min", "value_max", "currency",
                  "value_basis", "estimate_basis", "estimate_rationale"):
        assert getattr(row, field) == "", field
    body = _page(c, sid)
    assert "data-cev-amount-state" not in body   # no amount line at all
    assert "data-cev-amount-value" not in body


def test_zero_is_a_real_amount_and_is_not_none(owner):
    """17. Zero and "no amount" are different states and stay different."""
    c, _aid, sid = owner
    assert _q(c, sid, topic="cost_revenue_assumption", **dict(
        Q_EXACT, value_exact="0", estimate_basis="owner_assumption",
        estimate_rationale="assumed no unit cost at this stage")
    ).status_code in (302, 303)
    row = _only_active(sid)
    assert row.value_state == "EXACT" and row.value_exact == "0"
    assert row.value_state != "NONE"
    assert 'data-cev-amount-state="EXACT"' in _page(c, sid)


def test_a_range_requires_min_not_above_max(owner):
    """4. An inverted range is refused, not silently swapped."""
    c, _aid, sid = owner
    assert _q(c, sid, **dict(Q_RANGE, value_min="200", value_max="150")
              ).status_code in (302, 303)
    assert _rows(sid) == ()
    assert _q(c, sid, **dict(Q_RANGE, value_min="150", value_max="150")
              ).status_code in (302, 303)
    assert _only_active(sid).value_min == "150"      # equal ends are fine


def test_a_quantity_without_a_documented_basis_is_refused(owner):
    """5. NO BASIS -> NONE. The whole submission is refused, never downgraded
    to a bare number, because a silently basis-less amount is the thing this
    slice exists to prevent."""
    c, _aid, sid = owner
    for missing in ("estimate_basis", "estimate_rationale", "value_basis"):
        payload = dict(Q_RANGE)
        payload[missing] = ""
        assert _q(c, sid, **payload).status_code in (302, 303)
        assert _rows(sid) == (), missing
    assert _q(c, sid, **dict(Q_RANGE, estimate_basis="made_it_up")
              ).status_code in (302, 303)
    assert _rows(sid) == ()


def test_no_range_is_invented_from_an_exact_value(owner):
    """A leftover min/max on an EXACT row is refused rather than reconciled."""
    c, _aid, sid = owner
    assert _q(c, sid, **dict(Q_EXACT, value_min="100", value_max="150")
              ).status_code in (302, 303)
    assert _rows(sid) == ()


def test_usd_is_the_default_and_no_currency_is_inferred(owner):
    """7 + 8. USD applies when the field is absent; an unsupported code is
    refused rather than converted or defaulted over."""
    c, _aid, sid = owner
    payload = dict(Q_EXACT)
    payload.pop("currency")
    assert _q(c, sid, **payload).status_code in (302, 303)
    assert _only_active(sid).currency == "USD"

    assert _q(c, sid, topic="funding_need", **dict(
        Q_EXACT, currency="KWD", estimate_basis="owner_assumption",
        estimate_rationale="r")).status_code in (302, 303)
    assert len(_active(sid)) == 1                # the KWD row was refused
    assert all(r.currency in ("USD", "") for r in _rows(sid))


def test_a_non_monetary_topic_cannot_carry_an_amount(owner):
    """9. price / willingness_to_pay / funding_need structure cannot leak into
    a topic that records no money."""
    c, _aid, sid = owner
    for topic in ("demand", "market_entry", "first_sale_viability",
                  "licensing", "differentiation"):
        assert _q(c, sid, topic=topic, **Q_EXACT).status_code in (302, 303)
        assert _rows(sid) == (), topic
    # and each still records perfectly well WITHOUT an amount
    assert _q(c, sid, topic="demand").status_code in (302, 303)
    assert _only_active(sid).value_state == "NONE"


def test_each_monetary_topic_keeps_its_own_amount(owner):
    """9. Amounts recorded under different topics never migrate."""
    c, _aid, sid = owner
    _q(c, sid, topic="price", subject_text="a", **Q_EXACT)
    _q(c, sid, topic="willingness_to_pay", subject_text="b", **dict(
        Q_EXACT, value_exact="95", estimate_basis="willingness_to_pay_evidence",
        estimate_rationale="one buyer said so"))
    _q(c, sid, topic="funding_need", subject_text="c", **dict(
        Q_RANGE, value_min="20000", value_max="30000",
        estimate_basis="owner_assumption", estimate_rationale="rough plan"))
    by_topic = {r.topic: r for r in _active(sid)}
    assert by_topic["price"].value_exact == "120"
    assert by_topic["willingness_to_pay"].value_exact == "95"
    assert by_topic["funding_need"].value_min == "20000"
    assert by_topic["price"].value_min == ""
    assert by_topic["funding_need"].value_exact == ""


def test_manufacturing_evidence_cannot_carry_a_commercial_amount(owner):
    """10. The quantitative structure does not reach the other dimension."""
    c, _aid, sid = owner
    r = c.post("/session/%s/manufacturing-evidence" % sid, data={
        "topic": "material", "subject_text": "Aluminium",
        "statement_text": "Likely aluminium extrusion.",
        "source_identity": "Inventor", "occurred_on": "",
        "scope_text": "the frame", "limitation_text": "not checked",
        "value_state": "EXACT", "value_exact": "120", "currency": "USD",
    })
    assert r.status_code in (302, 303)
    assert _rows(sid) == (), "a quantity reached the Manufacturing route"
    # the same item without quantity fields records normally, at NONE
    assert c.post("/session/%s/manufacturing-evidence" % sid, data={
        "topic": "material", "subject_text": "Aluminium",
        "statement_text": "Likely aluminium extrusion.",
        "source_identity": "Inventor", "occurred_on": "",
        "scope_text": "the frame", "limitation_text": "not checked",
    }).status_code in (302, 303)
    assert _rows(sid)[0].value_state == "NONE"


def test_a_correction_restates_the_amount_truthfully(owner):
    """11. D1 supersession carries quantitative fields without inventing."""
    c, _aid, sid = owner
    _q(c, sid, **Q_EXACT)
    first = _only_active(sid)
    assert first.value_exact == "120"

    data = dict(GOOD)
    data.pop("topic")
    data.update(Q_RANGE)
    data["supersedes_evidence_id"] = first.evidence_id
    assert c.post(CEV_CORRECT % sid, data=data).status_code in (302, 303)

    active = _only_active(sid)
    assert active.value_state == "ESTIMATED_RANGE"
    assert active.value_min == "100" and active.value_max == "150"
    # the superseded row keeps its own amount, untouched
    old = [r for r in _rows(sid) if r.evidence_id == first.evidence_id][0]
    assert old.value_state == "EXACT" and old.value_exact == "120"


def test_a_correction_that_drops_the_amount_records_none_not_the_old_one(owner):
    """11. Omitting the quantity means NONE. A corrected item must never keep a
    superseded number the owner did not restate."""
    c, _aid, sid = owner
    _q(c, sid, **Q_EXACT)
    first = _only_active(sid)
    data = dict(GOOD)
    data.pop("topic")
    data["supersedes_evidence_id"] = first.evidence_id
    assert c.post(CEV_CORRECT % sid, data=data).status_code in (302, 303)
    active = _only_active(sid)
    assert active.value_state == "NONE" and active.value_exact == ""
    assert [r for r in _rows(sid)
            if r.evidence_id == first.evidence_id][0].value_exact == "120"


def test_a_withdrawal_preserves_the_historical_amount(owner):
    """12. History still shows WHAT was withdrawn, amount included."""
    c, _aid, sid = owner
    _q(c, sid, **Q_RANGE)
    first = _only_active(sid)
    assert _withdraw(c, sid, first.evidence_id).status_code in (302, 303)
    kept = [r for r in _rows(sid) if r.evidence_id == first.evidence_id][0]
    assert kept.value_min == "100" and kept.value_max == "150"
    withdrawal = [r for r in _rows(sid) if r.evidence_id != first.evidence_id][0]
    assert withdrawal.withdrawn is True
    assert withdrawal.value_min == "100"          # carried, not blanked
    assert _active(sid) == ()


def test_malformed_amounts_fail_closed(owner):
    """18 + 19. A malformed or unsupported amount is refused, never parsed,
    rounded, or turned into a guess."""
    c, _aid, sid = owner
    for bad in ("-5", "1,000", "$120", "120.999", "1e3", "about 120",
                "100-150", "١٢٠", " ", "12 0"):
        assert _q(c, sid, **dict(Q_EXACT, value_exact=bad)
                  ).status_code in (302, 303)
        assert _rows(sid) == (), bad
    for bad in ("MAYBE", "exact", "range", "estimated"):
        assert _q(c, sid, **dict(Q_EXACT, value_state=bad)
                  ).status_code in (302, 303)
        assert _rows(sid) == (), bad


def test_an_amount_is_never_a_validation_or_readiness_promotion(owner):
    """14 + 15. A number changes no status anywhere."""
    c, _aid, sid = owner
    _q(c, sid, **Q_EXACT)
    assert all(r.claim_status == CLAIM_STATUS_UNVALIDATED for r in _rows(sid))
    body = _page(c, sid)
    for forbidden in ("PASS_WITH_CONDITIONS", "SPECIALIST_REVIEWED",
                      "INDEPENDENTLY_VERIFIED", "EMPIRICALLY_DEMONSTRATED",
                      "commercial_readiness", "readiness_score"):
        assert forbidden not in body, forbidden
    assert "INSUFFICIENT_EVIDENCE" not in re.search(
        r'data-cev-amount.*?</p>', body, re.S).group(0)


def test_the_amount_surface_renders_in_both_languages(owner):
    """13. The same quantitative semantics, including the not-checked note."""
    c, _aid, sid = owner
    _q(c, sid, **Q_RANGE)
    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        body = _page(c, sid)
        for key in ("UI_CEV_Q_HEADING", "UI_CEV_Q_EXPLAIN", "UI_CEV_Q_STATE",
                    "UI_CEV_Q_STATE_NONE", "UI_CEV_Q_STATE_EXACT",
                    "UI_CEV_Q_STATE_ESTIMATED_RANGE", "UI_CEV_Q_CURRENCY",
                    "UI_CEV_Q_ESTIMATE_BASIS", "UI_CEV_Q_NOT_VALIDATED",
                    "UI_CEV_EB_COMPARABLE_PRODUCT_PRICE"):
            assert _rendered(key, lang) in body, (lang, key)
        assert "100" in body and "150" in body    # digits are never localised
        assert "USD" in body


def test_every_quantitative_term_exists_in_both_languages():
    """13. No English-only lifecycle or quantity semantics."""
    from engine.commercial_evidence import (
        ESTIMATE_BASES, VALUE_BASES, VALUE_STATES,
    )
    keys = (["UI_CEV_Q_STATE_" + s for s in VALUE_STATES]
            + ["UI_CEV_BASIS_" + b.upper() for b in VALUE_BASES]
            + ["UI_CEV_EB_" + b.upper() for b in ESTIMATE_BASES]
            + ["UI_CEV_Q_HEADING", "UI_CEV_Q_EXPLAIN", "UI_CEV_Q_STATE",
               "UI_CEV_Q_CURRENCY", "UI_CEV_Q_BASIS", "UI_CEV_Q_RATIONALE",
               "UI_CEV_Q_NOT_VALIDATED"])
    # every governed state, value basis and estimate basis must be sayable in
    # both languages, derived from the owner's vocabularies so a new member
    # cannot be added without its translations
    assert len(keys) == len(VALUE_STATES) + len(VALUE_BASES) + \
        len(ESTIMATE_BASES) + 7
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang), (key, lang)
        assert ui_text.text(key, "en") != ui_text.text(key, "ar"), key


def test_the_arabic_amount_wording_does_not_imply_a_checked_number():
    """13. An estimate must not read as validated or final in either language."""
    en = ui_text.text("UI_CEV_Q_NOT_VALIDATED", "en").lower()
    ar = ui_text.text("UI_CEV_Q_NOT_VALIDATED", "ar")
    assert "does not" in en and "final" in en
    assert "لا يجعله" in ar     # "does not make it"
    assert "نهائي" in ar                  # "final"
    for lang in ("en", "ar"):
        explain = ui_text.text("UI_CEV_Q_EXPLAIN", lang).lower()
        for claim in ("verified", "validated", "confirmed price",
                      "متحقق منه من إنفنتوراي"):
            assert claim not in explain, (lang, claim)


def test_the_gap_and_lifecycle_behaviour_survive_the_quantity_slice(owner):
    """20. D2 disturbs neither of the slices before it."""
    c, _aid, sid = owner
    assert _gap_topics(_page(c, sid)) == list(COMMERCIAL_TOPICS)
    _q(c, sid, **Q_EXACT)
    gaps = _gap_topics(_page(c, sid))
    assert "price" not in gaps
    assert len(gaps) == len(COMMERCIAL_TOPICS) - 1
    _withdraw(c, sid, _only_active(sid).evidence_id)
    assert _gap_topics(_page(c, sid)) == list(COMMERCIAL_TOPICS)
    assert 'data-cev-history-state="withdrawn"' in _page(c, sid)


# ==========================================================================
# 12. D3 — the supporting link on the surface: a traversal, never a rating
# ==========================================================================
def _link_of(sid, event_index=-1):
    return _rows(sid)[event_index].supporting_evidence_id


def _record_pair(c, sid):
    """One item to cite, then the citing item. Returns (target, citing)."""
    _record(c, sid, topic="market_alternative",
            subject_text="The ramp already sold by a national supplier")
    target = _only_active(sid)
    _record(c, sid, topic="differentiation",
            subject_text="Folds flat, unlike the supplier ramp",
            supporting_evidence_id=target.evidence_id)
    citing = [r for r in _rows(sid) if r.topic == "differentiation"][0]
    return target, citing


def test_the_owner_can_link_one_item_to_a_supporting_item(owner):
    """1 + 2. Differentiation linked to the market_alternative it compares."""
    c, _aid, sid = owner
    target, citing = _record_pair(c, sid)
    assert citing.supporting_evidence_id == target.evidence_id
    body = _page(c, sid)
    assert 'data-cev-link-target="%s"' % target.evidence_id in body
    assert _rendered("UI_CEV_LINK_SUPPORTED_BY", "en") in body
    # The page names the item it points at, so the link can be followed.
    assert "The ramp already sold by a national supplier" in body


def test_recording_without_a_link_is_the_ordinary_case(owner):
    """An item with no link renders no link line, and carries NULL."""
    c, _aid, sid = owner
    assert _record(c, sid).status_code == 302
    assert _link_of(sid) is None
    body = _page(c, sid)
    assert "data-cev-link-target" not in body
    # The absence is offered as an ANSWER in the form, not stamped on the item.
    assert _rendered("UI_CEV_LINK_NONE", "en") in body


def test_the_high_value_pairings_are_all_expressible(owner):
    """3 + 4 + 5 of the authorized use cases, recorded end to end.

    funding_need -> cost_revenue_assumption, price -> a comparable-price item,
    and willingness_to_pay -> customer_evidence."""
    c, _aid, sid = owner
    made = {}
    for topic, subject in (("cost_revenue_assumption", "Unit cost as planned"),
                           ("market_alternative", "A comparable ramp's price"),
                           ("customer_evidence", "One agency interview")):
        assert _record(c, sid, topic=topic, subject_text=subject
                       ).status_code == 302
        made[topic] = [r for r in _rows(sid) if r.topic == topic][0].evidence_id
    for topic, support in (("funding_need", "cost_revenue_assumption"),
                           ("price", "market_alternative"),
                           ("willingness_to_pay", "customer_evidence")):
        assert _record(c, sid, topic=topic,
                       subject_text="an item about " + topic,
                       supporting_evidence_id=made[support]).status_code == 302
        row = [r for r in _rows(sid) if r.topic == topic][0]
        assert row.supporting_evidence_id == made[support], topic
        assert row.claim_status == "UNVALIDATED"


def test_an_unresolvable_link_refuses_the_whole_submission(owner):
    """3. Refused, never quietly recorded without the link.

    Dropping it would show the item as deliberately unsupported when the owner
    had chosen support for it."""
    c, _aid, sid = owner
    assert _record(c, sid, supporting_evidence_id="rev-not-a-real-id"
                   ).status_code == 302
    assert _rows(sid) == ()


def test_a_cross_project_link_cannot_be_posted(owner):
    """4. Another project's item is not reachable from this session."""
    c, _aid, sid = owner
    other = _start(c)
    _record(c, other)
    theirs = _only_active(other)
    assert _record(c, sid, supporting_evidence_id=theirs.evidence_id
                   ).status_code == 302
    assert _rows(sid) == ()
    assert len(_rows(other)) == 1


def test_a_withdrawn_or_replaced_item_is_not_offered_as_support(owner):
    """The selector offers this dimension's CURRENT items only."""
    c, _aid, sid = owner
    _record(c, sid, topic="demand", subject_text="An agency asked twice")
    first = _only_active(sid)
    _withdraw(c, sid, first.evidence_id)
    body = _page(c, sid)
    form = re.search(r'id="cev-form".*?</form>', body, re.S).group(0)
    assert 'value="%s"' % first.evidence_id not in form


def test_a_correction_restates_the_link_and_omission_means_no_link(owner):
    """9 + 10. The link is restated exactly as the words and the amount are.

    Omitting it means NO LINK, not "keep the old one": a link surviving its own
    correction unexamined would let the item go on citing support nobody
    re-affirmed."""
    c, _aid, sid = owner
    target, citing = _record_pair(c, sid)

    # Restated explicitly: the replacement carries the link on purpose.
    assert _correct(c, sid, citing.evidence_id,
                    subject_text="Folds flat and stows upright",
                    supporting_evidence_id=target.evidence_id
                    ).status_code == 302
    restated = [r for r in _active(sid) if r.topic == "differentiation"][0]
    assert restated.supporting_evidence_id == target.evidence_id

    # Omitted: the next replacement names no support at all.
    assert _correct(c, sid, restated.evidence_id,
                    subject_text="Folds flat, stows upright, no tools"
                    ).status_code == 302
    dropped = [r for r in _active(sid) if r.topic == "differentiation"][0]
    assert dropped.supporting_evidence_id is None


def test_a_superseded_row_keeps_its_own_link(owner):
    """11. History is not rewritten by a correction that drops the link."""
    c, _aid, sid = owner
    target, citing = _record_pair(c, sid)
    _correct(c, sid, citing.evidence_id,
             subject_text="Folds flat, stows upright, no tools")
    old = [r for r in _rows(sid) if r.evidence_id == citing.evidence_id][0]
    assert old.supporting_evidence_id == target.evidence_id
    body = _page(c, sid)
    assert _rendered("UI_CEV_LINK_WAS_SUPPORTED_BY", "en") in body


def test_a_withdrawal_carries_the_link_forward(owner):
    """12. History shows what provenance was withdrawn, not merely that some
    was. Erasing the link here would quietly unpick the trail afterwards."""
    c, _aid, sid = owner
    target, citing = _record_pair(c, sid)
    assert _withdraw(c, sid, citing.evidence_id).status_code == 302
    withdrawal = _rows(sid)[-1]
    assert withdrawal.withdrawn is True
    assert withdrawal.supersedes_evidence_id == citing.evidence_id
    assert withdrawal.supporting_evidence_id == target.evidence_id
    assert withdrawal.supersedes_evidence_id != withdrawal.supporting_evidence_id


def test_a_link_cannot_be_the_item_it_replaces(owner):
    """8. The correction form never offers the item being corrected, and a
    posted attempt is refused rather than reconciled."""
    c, _aid, sid = owner
    _record(c, sid, topic="demand", subject_text="Two agencies asked")
    first = _only_active(sid)
    body = _page(c, sid)
    correct_form = re.search(
        r'action="/session/%s/commercial-evidence/correct".*?</form>' % sid,
        body, re.S).group(0)
    assert 'value="%s"' % first.evidence_id in correct_form   # the hidden target
    select = re.search(r'<select name="supporting_evidence_id".*?</select>',
                       correct_form, re.S).group(0)
    assert first.evidence_id not in select
    assert _correct(c, sid, first.evidence_id,
                    supporting_evidence_id=first.evidence_id).status_code == 302
    assert len(_rows(sid)) == 1                               # nothing appended


def test_a_linked_quantity_keeps_every_d2_rule(owner):
    """13 + 14 + 15. 100-150 USD, linked, and still an estimated range."""
    c, _aid, sid = owner
    _record(c, sid, topic="market_alternative",
            subject_text="A comparable ramp's listed price")
    quote = _only_active(sid)
    assert _q(c, sid, topic="price", supporting_evidence_id=quote.evidence_id,
              **Q_RANGE).status_code == 302
    row = [r for r in _rows(sid) if r.topic == "price"][0]
    assert row.supporting_evidence_id == quote.evidence_id
    assert row.value_state == "ESTIMATED_RANGE"
    assert (row.value_min, row.value_max) == ("100", "150")
    assert row.value_exact == ""
    assert row.currency == "USD"
    assert row.claim_status == "UNVALIDATED"
    body = _page(c, sid)
    # No invented midpoint, asserted where the amount is actually rendered.
    # This used to read `"125" not in body`: right rule, wrong surface. The
    # page also carries random evidence ids and signed tokens, and one in
    # roughly thirteen renders contains "125" inside one of them, so the
    # assertion failed on hex rather than on an invented midpoint. Scoped to
    # the amount element, the same rule holds without the dice roll.
    amount = _amount_display(body, "price")
    assert "125" not in amount, amount
    # ...and the range is still shown as a range, not collapsed into anything
    assert _amount_value(body, "price") == "100\u2013150"
    assert 'data-cev-amount-state="ESTIMATED_RANGE"' in amount
    # nor may a midpoint be pre-filled into the correction form
    assert _quantity_form_values(body, "price") == ("", "100", "150")
    assert _rendered("UI_CEV_Q_NOT_VALIDATED", "en") in body
    # A link is not a basis: the same submission without one is still refused.
    ranged = dict(Q_RANGE)
    ranged["estimate_basis"] = ""
    ranged["estimate_rationale"] = ""
    before = len(_rows(sid))
    assert _q(c, sid, topic="willingness_to_pay",
              supporting_evidence_id=quote.evidence_id, **ranged
              ).status_code == 302
    assert len(_rows(sid)) == before


def test_the_link_surface_shows_no_count_badge_or_score(owner):
    """18. A link is a traversal; the page must never turn it into a rating."""
    c, _aid, sid = owner
    target, _citing = _record_pair(c, sid)
    _record(c, sid, topic="demand", subject_text="Two agencies asked",
            supporting_evidence_id=target.evidence_id)
    body = _page(c, sid)
    # Scoped to the Commercial evidence block itself: the assertion is about
    # what THIS surface says, and the rest of the page has its own vocabulary
    # that this slice neither owns nor changed.
    start = body.index('id="cev-commercial-evidence"')
    block = body[start:body.index('id="t3a-project-record"', start)] \
        if 'id="t3a-project-record"' in body[start:] else body[start:]
    for forbidden in ("supporting-count", "link-count", "data-cev-link-count",
                      "data-cev-link-score", "data-cev-link-strength",
                      "data-cev-link-badge", "supported-score"):
        assert forbidden not in block
    # The claim is about what the LINK copy says, so it is asked of the link
    # copy. A page-wide word sweep would fire on the block's existing truthful
    # negations ("InventorAI has verified none of it"), which are exactly the
    # sentences this slice must keep.
    # The LABELS are the strings that stand beside an item as an assertion, so
    # they are what a badge would have to hide in. The explanatory paragraph is
    # excluded on purpose: it is where this slice's own denials live ("nothing
    # is counted, rated or ranked"), and a word sweep cannot tell a denial from
    # a claim.
    labels = " ".join(ui_text.text(key, lang).lower()
                      for lang in ("en", "ar")
                      for key in ("UI_CEV_LINK_LABEL", "UI_CEV_LINK_NONE",
                                  "UI_CEV_LINK_SUPPORTED_BY",
                                  "UI_CEV_LINK_WAS_SUPPORTED_BY"))
    for word in ("verified", "validated", "proven", "certified", "confirmed",
                 "score", "rating", "ranked", "strength", "sufficient",
                 "strong", "weak"):
        assert word not in labels, word
    # And the explanation does carry the denial, rather than merely omitting a
    # claim: an owner reading it is told a link is not a rating.
    explain = ui_text.text("UI_CEV_LINK_EXPLAIN", "en").lower()
    assert "not" in explain and "ranked" in explain
    # Two items cite the same target and the page says so twice, identically:
    # nothing tallies them and the target gains nothing from being cited twice.
    assert block.count('data-cev-link-target="%s"' % target.evidence_id) == 2
    assert "%" not in re.sub(r'%[0-9A-Fa-f]{2}', "", block)


def test_the_link_reads_the_same_in_both_languages(owner):
    """19. Equivalent semantics, and neither language implies verification."""
    c, _aid, sid = owner
    target, _citing = _record_pair(c, sid)
    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        body = _page(c, sid)
        assert _rendered("UI_CEV_LINK_SUPPORTED_BY", lang) in body
        assert _rendered("UI_CEV_LINK_LABEL", lang) in body
        assert _rendered("UI_CEV_LINK_NONE", lang) in body
        assert _rendered("UI_CEV_LINK_EXPLAIN", lang) in body
        assert 'data-cev-link-target="%s"' % target.evidence_id in body
    for lang in ("en", "ar"):
        for key in ("UI_CEV_LINK_LABEL", "UI_CEV_LINK_NONE",
                    "UI_CEV_LINK_SUPPORTED_BY", "UI_CEV_LINK_WAS_SUPPORTED_BY",
                    "UI_CEV_LINK_EXPLAIN"):
            assert ui_text.text(key, lang).strip()
    ar = " ".join(ui_text.text(k, "ar") for k in (
        "UI_CEV_LINK_LABEL", "UI_CEV_LINK_NONE", "UI_CEV_LINK_SUPPORTED_BY",
        "UI_CEV_LINK_WAS_SUPPORTED_BY", "UI_CEV_LINK_EXPLAIN"))
    for implies_verification in ("متحقق",      # verified
                                "موثّق",      # documented/certified
                                "مؤكد",            # confirmed
                                "مثبت",            # proven
                                "معتمد"):     # certified
        assert implies_verification not in ar, implies_verification


def test_the_link_field_cannot_carry_a_forged_status(owner):
    """The new control widens nothing: the refused field set is unchanged."""
    c, _aid, sid = owner
    _record(c, sid, topic="market_alternative", subject_text="A rival ramp")
    target = _only_active(sid)
    for forged in ("provenance", "claim_status", "validation_status",
                   "dimension", "supporting_evidence_ids"):
        assert _record(c, sid, supporting_evidence_id=target.evidence_id,
                       **{forged: "x"}).status_code == 302
    assert len(_rows(sid)) == 1
