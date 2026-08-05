"""P4-1b-2a BF4 — legacy start_ilt002_* route compatibility (durable envelope).

Owner disposition (REV1): the three existing legacy ``start_ilt002_*`` routes
must remain behaviourally usable and UNLINKED. Under P4-1b-2a an accepted answer
requires a durable project envelope; these tests prove each legacy route now
creates the SAME minimum durable envelope /start creates (via the one canonical
store), so a legacy session can durably accept an answer — with no second
persistence model, no tokenless fallback, no new UX/scope, no replay, and the
routes still unlinked from core navigation.
"""
import os

import pytest

from web.app import app, SESSION_STORE
from engine.record_store import SqliteRecordStore, ProjectNotFound
from test_p4_1b2a_durable_answer_append import get_answer_token

LEGACY_ROUTES = [
    "/start_ilt002_water_leak",
    "/start_ilt002_combination_lock",
    "/start_ilt002_combination_lock_path_n",
]
IDEA = ("A sensor circuit switches a relay to cut power when the measured "
        "current rises above a safe threshold.")


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _start_legacy(client, route):
    r = client.post(route, data={"idea": IDEA}, follow_redirects=False)
    assert r.status_code == 302, f"{route}: legacy route must start (got {r.status_code})"
    loc = r.headers.get("Location", "")
    assert "/session/" in loc, f"{route}: must redirect to a live session"
    return loc.rstrip("/").rsplit("/session/", 1)[1].split("?")[0]


def _answers(db_path, sid):
    store = SqliteRecordStore(db_path)
    try:
        return [r for r in store.load_contract(sid).assertions
                if r.disposition == "answered"]
    finally:
        store.close()


@pytest.mark.parametrize("route", LEGACY_ROUTES)
def test_legacy_route_starts_and_creates_durable_envelope(route, db_path):
    client = app.test_client()
    sid = _start_legacy(client, route)
    # The durable project envelope must exist BEFORE the first accepted answer.
    store = SqliteRecordStore(db_path)
    try:
        contract = store.load_contract(sid)   # raises ProjectNotFound if absent
    finally:
        store.close()
    assert contract.contract_version == "p4-0-record-contract-v1"
    SESSION_STORE.pop(sid, None)


@pytest.mark.parametrize("route", LEGACY_ROUTES)
def test_legacy_route_accepted_answer_persists_recN(route, db_path):
    client = app.test_client()
    sid = _start_legacy(client, route)
    assert _answers(db_path, sid) == []
    tok = get_answer_token(client, sid)
    assert tok, f"{route}: the session page must render a server-issued token"
    answer = "The comparator trips the relay when the shunt voltage exceeds the limit."
    client.post(f"/session/{sid}",
                data={"response": answer, "action": "answered", "answer_token": tok},
                follow_redirects=False)
    persisted = _answers(db_path, sid)
    assert len(persisted) == 1, f"{route}: the accepted answer must durably persist"
    assert persisted[0].content == answer
    # First accepted answer on a fresh legacy session is rec_1 (Option A rec_N).
    assert persisted[0].record_id == "rec_1", f"{route}: record_id must remain rec_1"
    SESSION_STORE.pop(sid, None)


@pytest.mark.parametrize("route", LEGACY_ROUTES)
def test_legacy_route_no_tokenless_fallback(route, db_path):
    client = app.test_client()
    sid = _start_legacy(client, route)
    client.post(f"/session/{sid}",
                data={"response": "A tokenless answer on a legacy route.",
                      "action": "answered"}, follow_redirects=False)
    assert _answers(db_path, sid) == [], (
        f"{route}: a tokenless answered submission must not durably append")
    SESSION_STORE.pop(sid, None)


def test_legacy_routes_remain_unlinked_from_core_navigation():
    client = app.test_client()
    home = client.get("/").get_data(as_text=True)
    data_page = client.get("/data-and-session").get_data(as_text=True)
    for route in LEGACY_ROUTES:
        assert route not in home, f"{route} must stay unlinked from the home page"
        assert route not in data_page, f"{route} must stay unlinked from the data/session page"
