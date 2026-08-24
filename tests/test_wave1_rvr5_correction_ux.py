"""Wave-1 RVR-5 — rendered correction UX / T1-B (OD-PDVG-02(a)).

Contract: docs/governance/WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md (RVR-5).
The /session/<sid>/correct route body (PVCG-R4-C semantics) is byte-unchanged;
these tests cover rendered reachability, truthful copy, the ack surface, and
withdrawn-history visibility.
"""
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
    with appmod.app.test_client() as c:
        yield c, appmod

def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    return r.headers["Location"].rsplit("/", 1)[-1]

def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)

def _token(page):
    return html.unescape(re.search(r'name="answer_token" value="([^"]+)"', page).group(1))

def _answer_once(c, sid):
    c.post(f"/session/{sid}", data={"response": ANSWER,
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
