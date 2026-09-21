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
    assert form.count("<select") == 1          # the topic control, and only it
    assert 'name="provenance"' not in form


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
