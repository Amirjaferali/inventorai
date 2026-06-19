import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE
from engine.idea_state import IdeaState, Evidence, REASONED, Gap, OPEN, CLOSED, AcknowledgedUnknown
from engine.domain_rules import infer_domain


def test_start_ilt002_water_leak_forces_electronics_domain():
    client = app.test_client()
    response = client.post(
        "/start_ilt002_water_leak",
        data={"idea": "A water leak detection system using moisture sensors and alarm notification."},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/session/" in response.headers["Location"]

    sid = response.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None, "ILT-002 session state not stored"

    state = entry["state"]
    assert state.domain == "electronics_electrical"
    assert state.domain_signal == "electronics_electrical"
    assert entry["last_result"]["question"] == (
        "Describe how your electronic circuit achieves its intended function — what happens electrically from input to output?"
    )


def test_start_uses_infer_domain_for_normal_flow():
    client = app.test_client()
    idea_text = "ESP32 moisture sensor circuit with WiFi reporting"
    response = client.post(
        "/start",
        data={"idea": idea_text},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/session/" in response.headers["Location"]

    sid = response.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None, "Normal session state not stored"

    state = entry["state"]
    assert state.domain == infer_domain(idea_text)
    assert state.domain_signal == infer_domain(idea_text)


def _make_incomplete_state(idea_id):
    state = IdeaState(idea_id=idea_id)
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    return state


def _make_eligible_state(idea_id):
    state = IdeaState(idea_id=idea_id)
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    state.maturity_level = 2
    state.known_problem = Evidence("Clear problem statement", REASONED, 0)
    state.known_mechanism = Evidence("ESP32 TMP117 mechanism", REASONED, 0)
    return state


def test_deliverable_route_missing_sid_redirects():
    client = app.test_client()
    response = client.get("/session/does-not-exist/deliverable", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_deliverable_route_incomplete_state_returns_200_and_snapshot_language():
    sid = "test-incomplete-sid"
    state = _make_incomplete_state(sid)
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        response = client.get(f"/session/{sid}/deliverable")
        assert response.status_code == 200
        assert response.content_type.startswith("text/html")
        body = response.get_data(as_text=True)
        assert "Assessment Snapshot — In Progress" in body
        assert "This is not a final deliverable" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_deliverable_route_eligible_state_returns_deliverable_language():
    sid = "test-eligible-sid"
    state = _make_eligible_state(sid)
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        response = client.get(f"/session/{sid}/deliverable")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "FDC-001 Deliverable" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_deliverable_route_contains_required_sections():
    sid = "test-sections-sid"
    state = _make_eligible_state(sid)
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        response = client.get(f"/session/{sid}/deliverable")
        body = response.get_data(as_text=True)
        for fragment in [
            "Invention Summary",
            "Assessment Overview",
            "Requirements",
            "Assumptions",
            "Risks",
            "Recommendations",
            "Unresolved Items",
        ]:
            assert fragment in body, f"missing section fragment: {fragment}"
    finally:
        SESSION_STORE.pop(sid, None)


def test_deliverable_route_does_not_mutate_state():
    sid = "test-no-mutation-sid"
    state = _make_incomplete_state(sid)
    state.gaps.append(Gap(gap_type="MECHANISM_COMPLETENESS", status=OPEN, opened_at=0))
    state.acknowledged_unknowns.append(
        AcknowledgedUnknown(iteration=0, gap_context="MECHANISM_COMPLETENESS",
                             verbatim="I do not yet know", category_basis="explicit")
    )
    before = (state.iteration, state.maturity_level, len(state.gaps), len(state.acknowledged_unknowns))
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        client.get(f"/session/{sid}/deliverable")
        after = (state.iteration, state.maturity_level, len(state.gaps), len(state.acknowledged_unknowns))
        assert before == after, f"state mutated: {before} != {after}"
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_incomplete_state_contains_snapshot_link():
    client = app.test_client()
    idea_text = "ESP32 moisture sensor circuit with WiFi reporting"
    response = client.post("/start", data={"idea": idea_text}, follow_redirects=False)
    sid = response.headers["Location"].rsplit("/", 1)[-1]
    try:
        page = client.get(f"/session/{sid}")
        body = page.get_data(as_text=True)
        assert f"/session/{sid}/deliverable" in body
        assert "View In-Progress Assessment Snapshot" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_eligible_state_contains_deliverable_link():
    sid = "test-session-link-eligible-sid"
    state = _make_eligible_state(sid)
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        page = client.get(f"/session/{sid}")
        body = page.get_data(as_text=True)
        assert f"/session/{sid}/deliverable" in body
        assert "View FDC-001 Deliverable" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_deliverable_route_does_not_call_run_iteration(monkeypatch):
    import web.app as web_app_module
    called = {"value": False}

    def _fail_if_called(*args, **kwargs):
        called["value"] = True
        raise AssertionError("run_iteration must not be called by show_deliverable")

    monkeypatch.setattr(web_app_module, "run_iteration", _fail_if_called)

    sid = "test-no-run-iteration-sid"
    state = _make_incomplete_state(sid)
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        response = client.get(f"/session/{sid}/deliverable")
        assert response.status_code == 200
        assert called["value"] is False
    finally:
        SESSION_STORE.pop(sid, None)


def test_deliverable_route_uses_package_eligibility_for_status_selection():
    from engine.deliverable_assembler import assemble_deliverable

    sid_a = "test-eligibility-consistency-incomplete"
    state_a = _make_incomplete_state(sid_a)
    pkg_a = assemble_deliverable(state_a)
    SESSION_STORE[sid_a] = {"state": state_a, "last_result": None, "transcript": []}

    sid_b = "test-eligibility-consistency-eligible"
    state_b = _make_eligible_state(sid_b)
    pkg_b = assemble_deliverable(state_b)
    SESSION_STORE[sid_b] = {"state": state_b, "last_result": None, "transcript": []}

    try:
        client = app.test_client()
        body_a = client.get(f"/session/{sid_a}/deliverable").get_data(as_text=True)
        body_b = client.get(f"/session/{sid_b}/deliverable").get_data(as_text=True)

        assert pkg_a["_session_meta"]["deliverable_eligible"] is False
        assert "Assessment Snapshot — In Progress" in body_a

        assert pkg_b["_session_meta"]["deliverable_eligible"] is True
        assert "FDC-001 Deliverable" in body_b
    finally:
        SESSION_STORE.pop(sid_a, None)
        SESSION_STORE.pop(sid_b, None)


def _make_state_with_unknowns(idea_id, unknowns):
    state = IdeaState(idea_id=idea_id)
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    for it, ctx, verb in unknowns:
        state.acknowledged_unknowns.append(
            AcknowledgedUnknown(iteration=it, gap_context=ctx, verbatim=verb, category_basis="explicit")
        )
    return state


def test_session_page_no_unknowns_section_when_empty():
    sid = "test-no-unknowns-sid"
    state = _make_incomplete_state(sid)
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "What You Have Marked as Not Yet Known" not in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_shows_one_acknowledged_unknown():
    sid = "test-one-unknown-sid"
    state = _make_state_with_unknowns(sid, [(2, "MECHANISM_COMPLETENESS", "I do not yet know the exact voltage")])
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "What You Have Marked as Not Yet Known" in body
        assert "I do not yet know the exact voltage" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_shows_multiple_unknowns_in_order():
    sid = "test-multi-unknown-sid"
    state = _make_state_with_unknowns(sid, [
        (2, "MECHANISM_COMPLETENESS", "First unknown statement"),
        (4, "PHYSICAL_FEASIBILITY", "Second unknown statement"),
    ])
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        idx1 = body.find("First unknown statement")
        idx2 = body.find("Second unknown statement")
        assert idx1 != -1 and idx2 != -1
        assert idx1 < idx2
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_escapes_unknown_text():
    sid = "test-escape-unknown-sid"
    state = _make_state_with_unknowns(sid, [(2, "MECHANISM_COMPLETENESS", "<script>alert(1)</script>")])
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "<script>alert(1)</script>" not in body
        assert "&lt;script&gt;" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_viewing_does_not_mutate_unknowns_or_state():
    sid = "test-unknowns-no-mutation-sid"
    state = _make_state_with_unknowns(sid, [(2, "MECHANISM_COMPLETENESS", "Some unknown")])
    before = (
        state.iteration, state.maturity_level, len(state.gaps),
        len(state.acknowledged_unknowns), state.acknowledged_unknowns[0].verbatim,
    )
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        client.get(f"/session/{sid}")
        after = (
            state.iteration, state.maturity_level, len(state.gaps),
            len(state.acknowledged_unknowns), state.acknowledged_unknowns[0].verbatim,
        )
        assert before == after, f"state mutated: {before} != {after}"
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_unknowns_section_no_resolution_claim():
    sid = "test-unknown-no-resolution-claim-sid"
    state = _make_state_with_unknowns(sid, [(2, "MECHANISM_COMPLETENESS", "Some unknown")])
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        for forbidden in ["resolved unknown", "completed unknown", "feasibility established", "ready to build"]:
            assert forbidden not in body.lower()
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_unknowns_section_no_ilt002_or_evidence_wording():
    sid = "test-unknown-no-ilt002-wording-sid"
    state = _make_state_with_unknowns(sid, [(2, "MECHANISM_COMPLETENESS", "Some unknown")])
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "ILT-002" not in body
        assert "evidence" not in body.lower()
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_with_unknowns_retains_snapshot_link_when_incomplete():
    sid = "test-unknown-retains-snapshot-link-sid"
    state = _make_state_with_unknowns(sid, [(2, "MECHANISM_COMPLETENESS", "Some unknown")])
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "View In-Progress Assessment Snapshot" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_with_unknowns_retains_deliverable_link_when_eligible():
    sid = "test-unknown-retains-deliverable-link-sid"
    state = _make_eligible_state(sid)
    state.acknowledged_unknowns.append(
        AcknowledgedUnknown(iteration=2, gap_context="MECHANISM_COMPLETENESS", verbatim="Some unknown", category_basis="explicit")
    )
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        client = app.test_client()
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "View FDC-001 Deliverable" in body
        assert "What You Have Marked as Not Yet Known" in body
    finally:
        SESSION_STORE.pop(sid, None)
