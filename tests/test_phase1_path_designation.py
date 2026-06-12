"""
Phase 1 — Path designation tests.
Authorized by docs/governance/PHASE_1_PATH_DESIGNATION_AUTHORIZATION.md (16e020e).
Phase 1 carries the path designation only. It must NOT change content:
Path N sessions receive legacy question content until Phase 2.
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE
from engine.idea_state import IdeaState
from engine.progression_loop import run_iteration


IDEA_TEXT = (
    "An electronic combination lock that uses a keypad and a motor "
    "to control a bolt for a household door."
)


def _client():
    return app.test_client()


def _post_route(client, route):
    return client.post(route, data={"idea": IDEA_TEXT}, follow_redirects=False)


def _sid_from_redirect(resp):
    return resp.headers["Location"].rstrip("/").split("/")[-1]


def test_ideastate_path_default():
    state = IdeaState(idea_id=str(uuid.uuid4()))
    assert state.path == "legacy_undesignated_current_behavior"


def test_legacy_session_behavior_unchanged_with_field_present():
    state = IdeaState(idea_id="phase1-zerochange")
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"

    result = run_iteration(state, IDEA_TEXT)

    assert isinstance(result, dict)
    assert state.iteration >= 1
    assert state.path == "legacy_undesignated_current_behavior"


def test_path_n_session_receives_same_question_as_legacy():
    client = _client()

    r_legacy = _post_route(client, "/start_ilt002_combination_lock")
    r_pathn = _post_route(client, "/start_ilt002_combination_lock_path_n")

    sid_l = _sid_from_redirect(r_legacy)
    sid_n = _sid_from_redirect(r_pathn)

    res_l = SESSION_STORE[sid_l]["last_result"]
    res_n = SESSION_STORE[sid_n]["last_result"]

    assert res_l.get("question") == res_n.get("question")
    assert res_l.get("transition") == res_n.get("transition")

    st_l = SESSION_STORE[sid_l]["state"]
    st_n = SESSION_STORE[sid_n]["state"]

    assert st_l.maturity_level == st_n.maturity_level
    assert [g for g in st_l.gaps] == [g for g in st_n.gaps]


def test_path_n_route_sets_designation():
    client = _client()

    resp = _post_route(client, "/start_ilt002_combination_lock_path_n")

    assert resp.status_code in (301, 302, 303)

    sid = _sid_from_redirect(resp)
    state = SESSION_STORE[sid]["state"]

    assert state.path == "N"
    assert state.domain == "electronics_electrical"
    assert state.domain_signal == "electronics_electrical"


def test_existing_fixed_routes_carry_default_path():
    client = _client()

    for route in ("/start_ilt002_combination_lock", "/start_ilt002_water_leak"):
        resp = _post_route(client, route)
        sid = _sid_from_redirect(resp)

        assert (
            SESSION_STORE[sid]["state"].path
            == "legacy_undesignated_current_behavior"
        )


def test_inferred_route_carries_default_path():
    client = _client()

    resp = _post_route(client, "/start")

    if (
        resp.status_code in (301, 302, 303)
        and "/session/" in resp.headers.get("Location", "")
    ):
        sid = _sid_from_redirect(resp)
        assert (
            SESSION_STORE[sid]["state"].path
            == "legacy_undesignated_current_behavior"
        )


def test_same_idea_twice_identical_state():
    s1 = IdeaState(idea_id="determinism-check")
    s2 = IdeaState(idea_id="determinism-check")

    s1.domain = "electronics_electrical"
    s2.domain = "electronics_electrical"

    s1.domain_signal = "electronics_electrical"
    s2.domain_signal = "electronics_electrical"

    run_iteration(s1, IDEA_TEXT)
    run_iteration(s2, IDEA_TEXT)

    assert s1.maturity_level == s2.maturity_level
    assert s1.iteration == s2.iteration
    assert s1.path == s2.path == "legacy_undesignated_current_behavior"
