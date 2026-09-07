"""Wave-1 RVR-5 — rendered correction UX / T1-B (OD-PDVG-02(a)).

Contract: docs/governance/WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md (RVR-5).
The /session/<sid>/correct route body (PVCG-R4-C semantics) is byte-unchanged;
these tests cover rendered reachability, truthful copy, the ack surface, and
withdrawn-history visibility.
"""
from tests.csrf_client import csrf_client
import html, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
ANSWER = ("The ramp folds up and down by hand. When it is down flat, it must "
          "stay firmly held so a wheelchair can roll over it. I am considering "
          "three ways to hold it: a toggle latch that snaps over its center, a "
          "spring pin that clicks into place, or a small gate piece that drops "
          "into place by its own weight.")
CORRECTED = ("Correction: the holder is (1) an over-centre toggle latch or "
             "(2) a spring-loaded detent pin; the gravity-drop gate latch is "
             "withdrawn because outdoor grit could jam its drop channel.")

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "rvr5.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod

def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    return r.headers["Location"].rsplit("/", 1)[-1]

def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)

def _token(page):
    return html.unescape(re.search(r'name="answer_token" value="([^"]+)"', page).group(1))

def _answer_once(c, sid, answer=ANSWER):
    c.post(f"/session/{sid}", data={"response": answer,
                                    "answer_token": _token(_page(c, sid)),
                                    "action": "answered"})

def test_correction_affordance_hidden_until_an_answer_exists(client):
    c, appmod = client
    sid = _start(c)
    page = _page(c, sid)
    # fresh session serves MECHANISM_COMPLETENESS: accept-risk is correctly
    # HIDDEN there (mechanism can never be risk-accepted), and there is no
    # answer to correct yet.
    assert "/accept-risk" not in page
    assert f"/session/{sid}/correct" not in page
    # after the mechanism closes, the served gap becomes feasibility.
    # W2-D reconciliation (Wave-2 contract §F, W1-S2 — intentional new
    # expectation): the accept-risk affordance no longer appears merely
    # because an eligible gap is served; it requires at least one ACTIVE
    # substantive attempt for that gap first.
    _answer_once(c, sid)
    _answer_once(c, sid)
    page2 = _page(c, sid)
    from engine.progression_loop import select_next_gap
    if select_next_gap(appmod.SESSION_STORE[sid]["state"]) == "PHYSICAL_FEASIBILITY":
        assert "/accept-risk" not in page2  # no substantive attempt yet
        c.post(f"/session/{sid}", data={
            "response": ("I have not tested whether the mechanism stays "
                         "reliable under repeated loading and outdoor use."),
            "answer_token": _token(_page(c, sid)), "action": "answered"})
        assert "/accept-risk" in _page(c, sid)

def test_correction_affordance_reaches_the_governed_route(client):
    c, appmod = client
    sid = _start(c)
    _answer_once(c, sid)
    page = _page(c, sid)
    assert f"/session/{sid}/correct" in page
    m = re.search(r'<option value="(rec_\d+)">([^<]+)</option>', page)
    assert m, "active answered record listed"
    rec_id = m.group(1)
    # truthful copy on the surface: history kept, nothing erased
    assert "withdrawn" in page and "nothing is erased" in page.lower()
    # drive the EXISTING route through the rendered form fields
    r = c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": rec_id, "response": CORRECTED,
        "answer_token": _token(page)})
    assert r.status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]
    withdrawn = [x for x in state.assertions
                 if getattr(x, "superseded_by", None) is not None]
    assert len(withdrawn) == 1 and withdrawn[0].record_id == rec_id
    # the applied ack renders once on the next page (criterion-14 surface)
    page2 = _page(c, sid)
    assert "withdrawn and kept in the project history" in page2

def test_withdrawn_history_visible_on_deliverable(client):
    c, appmod = client
    sid = _start(c)
    _answer_once(c, sid)
    page = _page(c, sid)
    rec_id = re.search(r'<option value="(rec_\d+)">', page).group(1)
    c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": rec_id, "response": CORRECTED,
        "answer_token": _token(page)})
    d = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "withdrawn" in d.lower()
    assert "Corrected (withdrawn) answers kept in history" in d

def test_no_withdrawn_block_when_no_correction(client):
    c, appmod = client
    sid = _start(c)
    _answer_once(c, sid)
    d = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "Corrected (withdrawn) answers kept in history" not in d

def test_route_semantics_untouched_forged_token_still_fails_closed(client):
    c, appmod = client
    sid = _start(c)
    _answer_once(c, sid)
    page = _page(c, sid)
    rec_id = re.search(r'<option value="(rec_\d+)">', page).group(1)
    c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": rec_id, "response": CORRECTED,
        "answer_token": "forged"})
    state = appmod.SESSION_STORE[sid]["state"]
    assert all(getattr(x, "superseded_by", None) is None
               for x in state.assertions)


def _preview_records(page):
    from html.parser import HTMLParser

    class Records(HTMLParser):
        def __init__(self):
            super().__init__()
            self.records, self.current, self.field = {}, None, None

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'data-correction-record' in attrs:
                self.current = attrs['data-correction-record']
                self.records[self.current] = {}
            if self.current:
                for field in ('reference', 'context', 'content'):
                    if 'data-record-' + field in attrs:
                        self.field = field
                        self.records[self.current][field] = ''

        def handle_data(self, value):
            if self.current and self.field:
                self.records[self.current][self.field] += value

        def handle_endtag(self, tag):
            if tag in ('bdi', 'span', 'p'):
                self.field = None
            if tag == 'div':
                self.current = None

    parsed = Records()
    parsed.feed(page)
    return parsed.records


@pytest.mark.parametrize('lang', ['en', 'ar'])
def test_full_preview_is_verbatim_and_uses_exact_selector_eligibility(client, lang):
    c, appmod = client
    c.post('/ui-language', data={'lang': lang, 'next': '/'})
    sid = _start(c)
    assert 'correction-preview.js' not in _page(c, sid)
    texts = [ANSWER + '\n  نص عربي EN & <img src=x onerror="alert(1)">\n' + 'x' * 800,
             ANSWER + '\n  Different tail إجابة أخرى']
    for value in texts:
        _answer_once(c, sid, value)
    state = appmod.SESSION_STORE[sid]['state']
    before = [r.record_id for r in state.assertions]
    page = _page(c, sid)
    records = _preview_records(page)
    active = [r for r in state.assertions if r.disposition == 'answered' and r.superseded_by is None]
    assert len(active) == 2 and texts[0][:70] == texts[1][:70]
    assert list(records) == [r.record_id for r in active]
    for record in active:
        assert records[record.record_id]['content'] == record.content
        assert records[record.record_id]['reference'] == record.record_id
        assert records[record.record_id]['context']
        assert f'<option value="{record.record_id}">' in page
    assert '&lt;img' in page and '<img src=x' not in page
    assert [r.record_id for r in state.assertions] == before
    assert 'name="supersedes_record_id" required' in page
    assert 'name="response" rows="3" required' in page
    assert 'name="csrf_token"' in page and 'name="answer_token"' in page


def test_preview_excludes_withdrawn_and_nonanswer_records(client):
    c, appmod = client
    sid = _start(c)
    _answer_once(c, sid)
    first = next(iter(_preview_records(_page(c, sid))))
    c.post(f'/session/{sid}/correct', data={
        'supersedes_record_id': first, 'response': CORRECTED,
        'answer_token': _token(_page(c, sid))})
    c.post(f'/session/{sid}', data={
        'action': 'unknown', 'response': 'Not yet known',
        'answer_token': _token(_page(c, sid))})
    records = _preview_records(_page(c, sid))
    assert first not in records and len(records) == 1
    assert next(iter(records.values()))['content'] == CORRECTED
    assert all(r.disposition == 'answered' and r.superseded_by is None
               for r in appmod.SESSION_STORE[sid]['state'].assertions if r.record_id in records)


@pytest.mark.parametrize('lang', ['en', 'ar'])
def test_preview_owned_isolation_and_cold_resume(client, lang):
    from tests.test_p5_3_project_ownership_authorization import _client_for
    _, appmod = client
    owner = _client_for('preview-owner@example.com')
    other = _client_for('preview-other@example.com')
    owner.post('/ui-language', data={'lang': lang, 'next': '/'})
    sid = _start(owner)
    secret = ANSWER + ' CONFIDENTIAL-OWNER-ANSWER'
    _answer_once(owner, sid, secret)
    other_sid = _start(other)
    _answer_once(other, other_sid, ANSWER + ' OTHER-PROJECT-ANSWER')
    page = _page(owner, sid)
    assert secret in page and 'OTHER-PROJECT-ANSWER' not in page
    denied = other.get(f'/session/{sid}')
    assert denied.status_code == 302 and denied.headers['Location'].endswith('/')
    assert secret not in denied.get_data(as_text=True)
    assert _preview_records(denied.get_data(as_text=True)) == {}
    assert secret not in _page(other, other_sid)
    appmod.SESSION_STORE.pop(sid)
    cold = _page(owner, sid)
    assert 'id="resume-project"' in cold
    assert _preview_records(cold) == {} and 'correction-preview.js' not in cold
    owner.post(f'/session/{sid}/resume', data={})
    resumed = _preview_records(_page(owner, sid))
    assert len(resumed) == 1 and next(iter(resumed.values()))['content'] == secret
