"""T3-A "Project record" — read-only rendering of the existing durable input
history (`T3A-PROJECT-RECORD-IMPLEMENT-01`; OD-PDVG-02 option (b) exercised in
its NARROWED input-history form only).

Route-level journeys against the real integrated code with a real on-disk
SQLite store. Every fixture is synthetic. The block is proven to render only
what the durable owners already carry — the restored assertion ledger in its
order, the supersession edges, the anchored quantity/reference rows and the
adoption ledger — with no write, no schema/store change, no before/after or
validity claim, and with the neighbouring correction and migration blocks
unchanged. Assertions read the FULL rendered block and the canonical state,
never a selected phrase alone.
"""
import hashlib
import html as _html
import inspect
import re
import sqlite3

import pytest

import web.app as appmod
from web import ui_text
from engine import account_credentials as acct
from engine.session_reconstruction import (
    ENGINE_CONTRACT_VERSION_T2G2, RECONSTRUCTION_VERSION,
    reconstruct_readonly_state)
from tests.csrf_client import csrf_client

PW = "correct horse battery staple"
MECH_SEED = ("A folding mechanical wheelchair ramp with a spring latch. The "
             "inventor wants the ramp to stay reliably locked in the flat, "
             "load-bearing position and to fold away without tools")
MECH_ANSWER = ("The spring latch rotates into a slot in the hinge plate and the "
               "rib transfers the load to the frame rail.")
MECH_UNKNOWN = ("I do not know the load path, and I have not worked out how the "
                "hinge line transfers force into the frame rail at all.")
CORRECTED = ("Correction: the deck panel transfers load into the hinge line and "
             "then into the frame rail through the spring latch.")
HTML_TEXT = ("<script>alert(1)</script> the <b>rib</b> & rail carry the load "
             "because the latch pin transfers it.")
LONG_TEXT = ("The latch pin carries the load into the rail because the hinge "
             "plate is bolted to the rail. ") * 8          # > preview length

ELEC_FORM = {"idea": "ESP32 microcontroller circuit with a voltage sensor",
             "domain_confirm": "electronics_electrical"}
ELEC_PROBLEM = (
    "The problem is that cyclists have no reliable brake light. My circuit senses "
    "deceleration with an accelerometer because sudden voltage change on the sensor "
    "indicates braking, so the microcontroller switches the LED because riders "
    "behind need warning.")
ELEC_MECH = (
    "The mechanism works because the accelerometer outputs a voltage proportional "
    "to deceleration; the microcontroller reads it through the ADC and drives the "
    "LED through a transistor because the LED current exceeds the GPIO limit.")

REFERENCE = {
    "source_identity": "Dr A. Khan, structural engineer",
    "occurred_on": "2026-03-14",
    "scope_text": "static load case only",
    "limitation_text": "did not cover fatigue or corrosion",
}

BLOCK_ID = 'id="t3a-project-record"'
BLOCK_END = "T3A-BLOCK-END"
# Words the block's OWN chrome must never use about a historical entry
# (Owner instruction §4 / §5 / §11 and the T2-G forbidden-word rule).
FORBIDDEN_CHROME = ("invalid", "stale", "corrected", "upgraded", "improved",
                    "evaluation changed", "owed again", "asked again",
                    "more valid", "less valid")
# The one accepted use of "wrong": the R4-C M-4 negation ("not a judgement
# that ... was wrong"), which the block's explanation repeats verbatim.
ACCEPTED_NEGATION = "is not a judgement that it was wrong"


# ==========================================================================
# harness
# ==========================================================================
@pytest.fixture()
def client(tmp_path, monkeypatch):
    db = str(tmp_path / "t3a.sqlite")
    monkeypatch.setenv("INVENTORAI_DB_PATH", db)
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod, db


def _login(c, email="owner@example.com"):
    store = appmod._get_account_store()
    aid = acct.new_account_id()
    store.create_account(aid, acct.normalize_email(email), acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    assert c.post("/login", data={"email": email, "password": PW}).status_code == 302
    return aid


def _start(c, seed=MECH_SEED, domain="mechanical"):
    r = c.post("/start", data={"idea": seed, "domain_confirm": domain})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _legacy_start(c):
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = RECONSTRUCTION_VERSION
    try:
        return _start(c)
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original


def _raw(c, sid, lang=None):
    if lang:
        assert c.post("/ui-language", data={"lang": lang}).status_code in (302, 303)
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    if lang:
        c.post("/ui-language", data={"lang": "en"})
    return body


def _block(body):
    """The rendered Project Record block (raw HTML, not unescaped)."""
    assert BLOCK_ID in body, "project record block not rendered"
    start = body.index(BLOCK_ID)
    # the block ends at its own closing </details>; find it structurally
    depth, i = 0, start
    while True:
        o = body.find("<details", i)
        cl = body.find("</details>", i)
        if cl == -1:
            raise AssertionError("unterminated project record block")
        if o != -1 and o < cl:
            depth += 1
            i = o + 8
        else:
            depth -= 1
            i = cl + 10
            if depth <= 0:
                return body[start:cl + 10]


def _token(c, sid):
    return _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))


def _post(c, sid, path, **data):
    data.setdefault("answer_token", _token(c, sid))
    return c.post(f"/session/{sid}{path}", data=data)


def _answer(c, sid, text, action="answered"):
    r = c.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(c, sid), "action": action})
    assert r.status_code == 302, r.status_code
    return r


def _correct(c, sid, record_id, text):
    r = _post(c, sid, "/correct", supersedes_record_id=record_id, response=text)
    assert r.status_code == 302, r.status_code


def _active_answer_ids(c, sid):
    return re.findall(r'<option value="(rec_\d+)">', _raw(c, sid))


def _entries(block):
    """[(step, kind, record_id)] in rendered order."""
    return [(int(s), k, r) for s, k, r in re.findall(
        r'data-record-step="(\d+)" data-record-kind="([a-z_]+)" '
        r'data-record-id="(rec_\d+)"', block)]


def _links(block):
    """[(relation, target)] in rendered order, with the owning entry id."""
    out = []
    for m in re.finditer(r'<li class="project-record-entry"(.*?)</li>', block, re.S):
        li = m.group(0)
        rid = re.search(r'data-record-id="(rec_\d+)"', li).group(1)
        for rel, target in re.findall(
                r'data-record-relation="([a-z_]+)" data-record-target="([^"]+)"', li):
            out.append((rid, rel, target))
    return out


def _contents(block):
    return [_html.unescape(x) for x in re.findall(
        r'data-record-content dir="auto"[^>]*>(.*?)</(?:p|bdi)>', block, re.S)]


def _rule_changes(block):
    return re.findall(r'data-record-kind="(rules_[a-z]+)" data-adoption-id="([^"]+)"'
                      r'(?: data-after-step="(\d+)")?', block)


def _chrome(block):
    """The block with every verbatim inventor text removed — its own copy."""
    stripped = re.sub(r'data-record-content dir="auto"[^>]*>.*?</(?:p|bdi)>',
                      "", block, flags=re.S)
    stripped = re.sub(r'data-record-preview dir="auto"[^>]*>.*?</summary>',
                      "", stripped, flags=re.S)
    stripped = re.sub(r'data-record-reason dir="auto">.*?</span>', "", stripped,
                      flags=re.S)
    return stripped.lower()


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _ledger_rows(db, sid):
    con = sqlite3.connect(db)
    try:
        return con.execute(
            "SELECT seq, record_id, payload FROM records WHERE project_id=? "
            "ORDER BY seq", (sid,)).fetchall()
    finally:
        con.close()


def _adoption_rows(db, sid):
    con = sqlite3.connect(db)
    try:
        return con.execute(
            "SELECT adoption_id, from_version, to_version, recorded_iteration "
            "FROM engine_version_adoptions WHERE project_id=? ORDER BY adoption_seq",
            (sid,)).fetchall()
    finally:
        con.close()


def _journey(c, sid):
    """One mixed journey: answer, non-answer, correction, decision context,
    alternative declared, refined and withdrawn (with a reason)."""
    _answer(c, sid, MECH_UNKNOWN)
    _answer(c, sid, HTML_TEXT, action="unknown")
    withdrawn_id = _active_answer_ids(c, sid)[0]
    _correct(c, sid, withdrawn_id, CORRECTED)
    assert _post(c, sid, "/decision/declare-context",
                 content="Which latch should hold the ramp?").status_code == 302
    root = re.search(r'name="context_root" value="(rec_\d+)"', _raw(c, sid)).group(1)
    assert _post(c, sid, "/decision/declare-alternative", content="toggle latch",
                 context_root=root).status_code == 302
    head = re.search(r'name="supersedes_record_id" value="(rec_\d+)"', _raw(c, sid)).group(1)
    assert _post(c, sid, "/decision/refine-alternative",
                 content="over-centre toggle latch",
                 supersedes_record_id=head).status_code == 302
    head2 = re.search(r'name="supersedes_record_id" value="(rec_\d+)"', _raw(c, sid)).group(1)
    assert _post(c, sid, "/decision/withdraw-alternative",
                 reason="grit could jam the toggle",
                 supersedes_record_id=head2).status_code == 302
    return withdrawn_id


# ==========================================================================
# 1. ordering, event kinds and links come from the ledger only
# ==========================================================================
def test_entries_follow_the_restored_ledger_order_with_truthful_kinds(client):
    c, appmod, db = client
    sid = _start(c)
    withdrawn_id = _journey(c, sid)
    block = _block(_raw(c, sid))
    state = appmod.SESSION_STORE[sid]["state"]
    ledger = list(state.assertions)
    entries = _entries(block)
    assert [e[2] for e in entries] == [r.record_id for r in ledger]
    assert [e[0] for e in entries] == list(range(1, len(ledger) + 1))
    expected_kinds = {
        "answered": "answer_recorded", "unknown": "not_known_yet",
        "decision_context_declared": "decision_context_declared",
        "decision_alternative_declared": "alternative_declared",
        "decision_alternative_withdrawn": "alternative_withdrawn",
    }
    by_id = {r.record_id: r for r in ledger}
    for _step, kind, rid in entries:
        rec = by_id[rid]
        if rec.disposition == "answered" and rec.superseded_by:
            assert kind == "answer_withdrawn_replaced"
        elif rec.disposition == "decision_alternative_declared" and rec.supersedes:
            assert kind == "alternative_refined"
        else:
            assert kind == expected_kinds[rec.disposition], rid
    # exactly one withdrawn answer, and it is the corrected one
    assert [rid for _s, k, rid in entries if k == "answer_withdrawn_replaced"] == [withdrawn_id]
    # every kind rendered is a member of the closed vocabulary with EN+AR copy
    for _s, kind, _r in entries:
        assert kind in appmod.T3A_EVENT_KINDS
        entry = ui_text.UI_STRINGS["UI_T3A_EVENT_" + kind.upper()]
        assert entry["en"] and entry["ar"]


def test_supersession_links_restate_the_ledger_edges_exactly(client):
    c, appmod, db = client
    sid = _start(c)
    _journey(c, sid)
    block = _block(_raw(c, sid))
    state = appmod.SESSION_STORE[sid]["state"]
    by_id = {r.record_id: r for r in state.assertions}
    ordinal = {r.record_id: i + 1 for i, r in enumerate(state.assertions)}
    expected = []
    for r in state.assertions:
        withdrawing = r.disposition == "decision_alternative_withdrawn"
        for target in r.supersedes:
            expected.append((r.record_id, "withdraws" if withdrawing else "replaces", target))
        if r.superseded_by:
            succ = by_id[r.superseded_by]
            expected.append((r.record_id,
                             "withdrawn_in" if succ.disposition == "decision_alternative_withdrawn"
                             else "replaced_by", r.superseded_by))
    assert _links(block) == expected
    assert expected, "the journey must exercise supersession"
    # the visible step numbers name the linked record's own ordinal
    for rid, rel, target in expected:
        li = re.search(r'<li class="project-record-entry"[^>]*data-record-id="%s".*?</li>'
                       % rid, block, re.S).group(0)
        label = {"replaces": "Replaces step", "replaced_by": "Replaced by step",
                 "withdraws": "Withdraws step", "withdrawn_in": "Withdrawn at step"}[rel]
        assert f"{label} {ordinal[target]}" in li


def test_withdrawn_answer_text_is_shown_verbatim_beside_its_replacement(client):
    c, appmod, db = client
    sid = _start(c)
    withdrawn_id = _journey(c, sid)
    block = _block(_raw(c, sid))
    state = appmod.SESSION_STORE[sid]["state"]
    withdrawn = next(r for r in state.assertions if r.record_id == withdrawn_id)
    successor = next(r for r in state.assertions if r.record_id == withdrawn.superseded_by)
    li = re.search(r'<li class="project-record-entry"[^>]*data-record-id="%s".*?</li>'
                   % withdrawn_id, block, re.S).group(0)
    assert _html.unescape(re.search(
        r'data-record-content dir="auto"[^>]*>(.*?)</p>', li, re.S).group(1)) == withdrawn.content
    assert withdrawn.content == MECH_UNKNOWN
    # R4-C M-4 wording: withdrawn and kept; never a judgement
    assert "kept in the project history" in li
    assert "no longer used as current support" in li
    assert f'data-record-relation="replaced_by" data-record-target="{successor.record_id}"' in li
    succ_li = re.search(r'<li class="project-record-entry"[^>]*data-record-id="%s".*?</li>'
                        % successor.record_id, block, re.S).group(0)
    assert CORRECTED in _html.unescape(succ_li)
    assert f'data-record-relation="replaces" data-record-target="{withdrawn_id}"' in succ_li


def test_every_rendered_text_exists_in_a_durable_owner(client):
    c, appmod, db = client
    _login(c)
    sid = _start(c)
    _journey(c, sid)
    block = _block(_raw(c, sid))
    state = appmod.SESSION_STORE[sid]["state"]
    durable = {r.content for r in state.assertions if r.content}
    for text in _contents(block):
        assert text in durable, text
    # the withdrawal reason is the withdrawal record's own content
    reason = _html.unescape(re.search(
        r'data-record-reason dir="auto">(.*?)</span>', block, re.S).group(1))
    assert reason == "grit could jam the toggle"
    assert reason in durable
    # a withdrawal without a reason says so plainly and invents nothing
    sid2 = _start(c)
    _answer(c, sid2, MECH_ANSWER)
    assert _post(c, sid2, "/decision/declare-context", content="Which pin?").status_code == 302
    root = re.search(r'name="context_root" value="(rec_\d+)"', _raw(c, sid2)).group(1)
    assert _post(c, sid2, "/decision/declare-alternative", content="spring pin",
                 context_root=root).status_code == 302
    head = re.search(r'name="supersedes_record_id" value="(rec_\d+)"', _raw(c, sid2)).group(1)
    assert _post(c, sid2, "/decision/withdraw-alternative", reason="",
                 supersedes_record_id=head).status_code == 302
    block2 = _block(_raw(c, sid2))
    assert "data-record-reason-missing" in block2
    assert "No reason was recorded with this withdrawal." in block2
    assert "data-record-reason " not in block2


def test_no_before_after_or_validity_claim_in_the_chrome(client):
    c, appmod, db = client
    sid = _start(c)
    _journey(c, sid)
    chrome = _chrome(_block(_raw(c, sid)))
    for word in FORBIDDEN_CHROME:
        assert word not in chrome, word
    assert chrome.count("wrong") == chrome.count(ACCEPTED_NEGATION) == 1
    for key, entry in ui_text.UI_STRINGS.items():
        if key.startswith("UI_T3A_"):
            for word in FORBIDDEN_CHROME:
                assert word not in entry["en"].lower(), (key, word)
            if "wrong" in entry["en"].lower():
                assert key == "UI_T3A_EXPLAIN" and ACCEPTED_NEGATION in entry["en"]
    # the block carries no form and no control: it is a record, not a console
    block = _block(_raw(c, sid))
    assert "<form" not in block and "<button" not in block and "<input" not in block


# ==========================================================================
# 2. escaping, direction, bilingual chrome
# ==========================================================================
def test_user_text_is_escaped_and_carries_dir_auto(client):
    c, appmod, db = client
    sid = _start(c)
    _answer(c, sid, HTML_TEXT, action="unknown")
    _answer(c, sid, LONG_TEXT)
    block = _block(_raw(c, sid))
    assert "<script>" not in block and "<b>rib</b>" not in block
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in block
    for m in re.finditer(r'data-record-content', block):
        assert block[m.end():m.end() + 11] == ' dir="auto"'
    # a long text shows a bounded preview and keeps the full text available
    assert 'class="project-record-full"' in block
    assert LONG_TEXT.strip() in _html.unescape(block)
    preview = re.search(r'data-record-preview dir="auto"[^>]*>(.*?)<span', block, re.S).group(1)
    assert len(_html.unescape(preview)) <= appmod._T3A_TEXT_PREVIEW_CHARS + 2
    assert "Show the full text" in block


def test_english_and_arabic_render_the_same_record(client):
    c, appmod, db = client
    sid = _start(c)
    _journey(c, sid)
    en, ar = _raw(c, sid), _raw(c, sid, lang="ar")
    assert 'dir="rtl"' in ar and 'dir="rtl"' not in en
    blk_en, blk_ar = _block(en), _block(ar)
    assert _entries(blk_en) == _entries(blk_ar)
    assert _links(blk_en) == _links(blk_ar)
    assert _contents(blk_en) == _contents(blk_ar)         # verbatim, untranslated
    assert "سجل المشروع" in blk_ar and "Project record" in blk_en
    assert "Project record" not in blk_ar
    assert "إجابة مسحوبة ومستبدَلة" in blk_ar and "بديل مسحوب" in blk_ar
    for key, entry in ui_text.UI_STRINGS.items():
        if key.startswith("UI_T3A_"):
            assert entry.get("en") and entry.get("ar"), key
            assert re.search(r"[؀-ۿ]", entry["ar"]), key
    for kind in appmod.T3A_EVENT_KINDS:
        assert "UI_T3A_EVENT_" + kind.upper() in ui_text.UI_STRINGS, kind


# ==========================================================================
# 3. anchored rows: quantities and references under the answer they belong to
# ==========================================================================
def test_quantity_rows_render_under_their_anchor_in_seq_order(client):
    c, appmod, db = client
    _login(c)
    r = c.post("/start", data=ELEC_FORM)
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    _answer(c, sid, ELEC_PROBLEM)
    _answer(c, sid, ELEC_MECH)
    anchor = re.findall(r'data-t2a-anchor="([^"]+)"', _raw(c, sid))[0]

    def record(value):
        assert c.post(f"/session/{sid}/quantity/propose", data={
            "anchor_record_id": anchor, "quantity_kind": "target_value",
            "value_text": value}).status_code == 302
        token = re.search(r'name="confirmation_token" value="([^"]+)"', _raw(c, sid)).group(1)
        assert c.post(f"/session/{sid}/quantity/confirm", data={
            "confirmation_token": token, "quantity_action": "confirm"}).status_code == 302
    record("12.5 V")
    record("13 V")
    block = _block(_raw(c, sid))
    li = re.search(r'<li class="project-record-entry"[^>]*data-record-id="%s".*?<ul class="project-record-attached".*?</ul>'
                   % anchor, block, re.S).group(0)
    rows = re.findall(r'<li data-record-kind="(value_[a-z]+)">(.*?)</li>', li, re.S)
    assert [k for k, _ in rows] == ["value_recorded", "value_replaced"]
    assert "Target value" in rows[0][1] and "12.5 V" in rows[0][1]
    assert "13 V" in rows[1][1] and "replaces an earlier entry on this answer" in rows[1][1]
    assert "replaces an earlier entry" not in rows[0][1]
    state = appmod.SESSION_STORE[sid]["state"]
    assert [q.value_text for q in sorted(state.requirement_quantities,
                                         key=lambda q: q.quantity_seq)] == ["12.5 V", "13 V"]
    # quantity rows never appear as numbered steps of their own
    assert all(k not in ("value_recorded", "value_replaced") for _s, k, _r in _entries(block))


def test_reference_rows_render_recorded_replaced_and_withdrawn(client):
    c, appmod, db = client
    _login(c)
    sid = _start(c)
    _answer(c, sid, MECH_ANSWER)
    anchor = re.search(r'name="anchor_record_id" value="([^"]+)"', _raw(c, sid)).group(1)

    def record(intent="record", **over):
        data = dict(REFERENCE, anchor_record_id=anchor, reference_intent=intent)
        data.update(over)
        assert c.post(f"/session/{sid}/evidence-reference/propose", data=data).status_code == 302
        token = _html.unescape(re.search(
            r'name="confirmation_token" value="([^"]+)"', _raw(c, sid)).group(1))
        assert c.post(f"/session/{sid}/evidence-reference/confirm", data={
            "confirmation_token": token, "reference_action": "confirm"}).status_code == 302
    record()
    record(source_identity="Dr A. Khan (revised)")
    record(intent="withdraw")
    block = _block(_raw(c, sid))
    li = re.search(r'<li class="project-record-entry"[^>]*data-record-id="%s".*?<ul class="project-record-attached".*?</ul>'
                   % anchor, block, re.S).group(0)
    rows = re.findall(r'<li data-record-kind="(reference_[a-z]+)">(.*?)</li>', li, re.S)
    assert [k for k, _ in rows] == ["reference_recorded", "reference_replaced",
                                    "reference_withdrawn"]
    assert REFERENCE["source_identity"] in rows[0][1] and "2026-03-14" in rows[0][1]
    assert "Dr A. Khan (revised)" in rows[1][1]
    assert "replaces an earlier entry on this answer" in rows[1][1]
    assert "replaces an earlier entry" not in rows[2][1]
    history = appmod._get_store().load_evidence_references(sid)
    assert [h.withdrawn for h in history] == [False, False, True]


# ==========================================================================
# 4. rule changes (engine-version adoption) — truthful, non-duplicating
# ==========================================================================
def test_adoption_and_return_render_as_rule_changes_without_consequence_claims(client):
    c, appmod, db = client
    _login(c)
    sid = _legacy_start(c)
    _answer(c, sid, MECH_UNKNOWN)
    assert _block(_raw(c, sid)).count("data-adoption-id") == 0
    assert "project-record-rules" not in _block(_raw(c, sid))
    assert _post(c, sid, "/engine-version", version_action="adopt",
                 confirm_adoption="yes").status_code == 302
    _answer(c, sid, HTML_TEXT, action="deferred")
    assert _post(c, sid, "/engine-version", version_action="revert",
                 confirm_adoption="yes").status_code == 302
    page = _raw(c, sid)
    block = _block(page)
    rows = _adoption_rows(db, sid)
    assert [(r[1], r[2]) for r in rows] == [
        (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2),
        (ENGINE_CONTRACT_VERSION_T2G2, RECONSTRUCTION_VERSION)]
    changes = _rule_changes(block)
    assert [(k, a) for k, a, _s in changes] == [
        ("rules_adopted", rows[0][0]), ("rules_returned", rows[1][0])]
    assert "Newer rules adopted" in block and "Returned to earlier rules" in block
    assert block.count("Earlier answers were kept exactly as recorded.") == 2
    # "after step" is the last ledger step of an EARLIER iteration — a lower
    # bound proven from the durable iteration values, never a guess
    ledger = _ledger_rows(db, sid)
    import json
    for (_aid, _f, _t, recorded_iteration), (_k, _a, after) in zip(rows, changes):
        preceding = [seq + 1 for seq, _rid, payload in ledger
                     if int(json.loads(payload).get("iteration") or 0) < recorded_iteration]
        assert (int(after) if after else None) == (max(preceding) if preceding else None)
    # never a consequence claim; the migration disclosure is untouched and not
    # duplicated (the after-adoption line stays where it was, once)
    chrome = _chrome(block)
    for word in FORBIDDEN_CHROME:
        assert word not in chrome, word
    assert "recomputed" not in chrome and "asked" not in chrome
    assert 'id="engine-version"' in page and 'id="engine-version"' not in block
    assert "engine-version" not in block
    # the answers recorded under the earlier rules are still listed verbatim
    assert MECH_UNKNOWN in _contents(block)


# ==========================================================================
# 5. live / resumed / cold consistency, read-only guarantee, empty history
# ==========================================================================
def test_cold_page_renders_the_same_record_and_performs_no_mutation(client):
    c, appmod, db = client
    _login(c)
    sid = _legacy_start(c)
    _journey(c, sid)
    assert _post(c, sid, "/engine-version", version_action="adopt",
                 confirm_adoption="yes").status_code == 302
    live = _block(_raw(c, sid))
    appmod.SESSION_STORE.clear()
    before = _sha(db)
    cold_page = _raw(c, sid)
    cold = _block(cold_page)
    assert _sha(db) == before                       # no durable write on GET
    assert getattr(appmod.SESSION_STORE[sid]["state"], "domain", None) is None
    assert _entries(cold) == _entries(live)
    assert _links(cold) == _links(live)
    assert _contents(cold) == _contents(live)
    assert _rule_changes(cold) == _rule_changes(live)
    assert 'id="engine-version"' not in cold_page     # read-only page, as before
    assert f"/session/{sid}/correct" not in cold_page
    # a second cold GET is byte-identical for the block (deterministic)
    assert _block(_raw(c, sid)) == cold
    # the resumed page shows the same record again
    resumed = c.post(f"/session/{sid}/resume", data={})
    if resumed.status_code == 302:
        assert _entries(_block(_raw(c, sid))) == _entries(live)


def test_project_record_is_built_from_load_calls_only_and_never_persisted(client):
    c, appmod, db = client
    _login(c)
    sid = _start(c)
    _journey(c, sid)
    appmod.SESSION_STORE.clear()
    store = appmod._get_store()
    calls = []

    class Spy:
        def __getattr__(self, name):
            attr = getattr(store, name)
            if callable(attr):
                def wrapped(*a, **k):
                    calls.append(name)
                    return attr(*a, **k)
                return wrapped
            return attr
    original = appmod._STORE
    appmod._STORE = Spy()
    try:
        page = _raw(c, sid)
    finally:
        appmod._STORE = original
    assert BLOCK_ID in page
    assert calls and all(n.startswith("load_") for n in calls), calls
    assert "project_record" not in appmod.SESSION_STORE[sid]
    src = inspect.getsource(appmod._project_record_context)
    for forbidden in ("INSERT", "UPDATE", "CREATE TABLE", "append_", ".execute(",
                      "reconstruct_", "run_iteration", "assess_response"):
        assert forbidden not in src, forbidden


def test_zero_and_minimal_history_pages_stay_valid(client):
    c, appmod, db = client
    sid = _start(c)
    page = _raw(c, sid)
    block = _block(page)
    assert "Nothing has been recorded in this project yet." in block
    assert _entries(block) == [] and "project-record-list" not in block
    assert "project-record-rules" not in block
    opening = page[page.rfind("<details", 0, page.index(BLOCK_ID)):page.index(BLOCK_ID)]
    assert opening.strip() == "<details" and " open" not in block[:block.index(">")]
    _answer(c, sid, MECH_ANSWER)
    block = _block(_raw(c, sid))
    assert _entries(block) == [(1, "answer_recorded", "rec_1")]
    assert "Nothing has been recorded" not in block
    assert "project-record-link" not in block
    # Arabic on the empty page
    appmod.SESSION_STORE.clear()
    sid2 = _start(c)
    assert "لم يُسجَّل شيء في هذا المشروع بعد." in _block(_raw(c, sid2, lang="ar"))


def test_block_is_collapsed_by_default_and_placed_after_the_existing_blocks(client):
    c, appmod, db = client
    sid = _start(c)
    _journey(c, sid)
    page = _raw(c, sid)
    start = page.index(BLOCK_ID)
    opening = page[page.rfind("<details", 0, start):start]
    assert " open" not in opening
    # the correction block and its full-answers disclosure are unchanged and
    # precede the record; the record does not contain them
    assert page.index('class="correct-answer"') < start
    assert page.index('class="correction-full-answers"') < start
    block = _block(page)
    assert "correction-full-answers" not in block and "correct-answer" not in block
    assert page.count('class="correct-answer"') == 1
    assert page.count(BLOCK_ID) == 1


# ==========================================================================
# 6. no schema / store / engine change
# ==========================================================================
def test_no_schema_or_store_change_and_no_parallel_history_model(tmp_path, monkeypatch):
    db = str(tmp_path / "fresh.sqlite")
    monkeypatch.setenv("INVENTORAI_DB_PATH", db)
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    store = appmod._get_store()
    con = sqlite3.connect(db)
    try:
        tables = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        record_cols = [r[1] for r in con.execute("PRAGMA table_info(records)")]
    finally:
        con.close()
    assert not any("t3a" in t.lower() or "project_record" in t.lower() or
                   "history" in t.lower() for t in tables), tables
    assert record_cols == ["project_id", "seq", "record_id", "payload", "idempotency_key"]
    import engine.record_store as rs
    import engine.session_reconstruction as sr
    for module in (rs, sr):
        source = inspect.getsource(module)
        assert "t3a" not in source.lower() and "project_record" not in source.lower()
    assert sr.RECONSTRUCTION_VERSION == "p4-2-level1-recon-v1"
    # the web builder names no new persisted field on the state
    src = inspect.getsource(appmod._project_record_context)
    assert "state." not in src.replace("state.assertions", "").replace(
        "state.requirement_quantities", "")
    assert "setattr(" not in src
