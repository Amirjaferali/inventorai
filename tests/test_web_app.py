import os, sys
from test_p4_1b2a_durable_answer_append import answered_post, seed_direct_session_envelope  # P4-1b-2a
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import (
    app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE,
    CONFIRMATION_REQUIRED_MESSAGE, DOMAIN_CONFIRM_VALUE,
)
from engine.idea_state import (
    IdeaState, Evidence, REASONED, Gap, OPEN, PARTIAL, CLOSED, AcknowledgedUnknown,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY,
)
from engine.domain_rules import (
    infer_domain, classify_domain, DomainClassification, DomainResultKind,
    DomainAmbiguityReason,
)


def _none_result(_t):
    """P9-E2-R test double: the canonical classifier yields NONE."""
    return DomainClassification(kind=DomainResultKind.NONE)


def _single_result(domain):
    """P9-E2-R test double factory: the canonical classifier yields SINGLE(domain)."""
    return lambda _t: DomainClassification(
        kind=DomainResultKind.SINGLE, selected_domain=domain)


def _multi_result(_t):
    """P9-E2-R test double: a genuine multi-domain result (marker only; no D4).
    Registry-recognized candidates, no activation required for MULTI_DOMAIN_NEEDS_D4."""
    return DomainClassification(
        kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
        candidates=("mechanical", "medical_device"),
        reason=DomainAmbiguityReason.MULTI_DOMAIN,
    )


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
        data={"idea": idea_text, "domain_confirm": "electronics_electrical"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/session/" in response.headers["Location"]

    sid = response.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None, "Normal session state not stored"

    state = entry["state"]
    # Admission assigns the explicitly confirmed supported domain.
    assert state.domain == "electronics_electrical"
    assert state.domain_signal == "electronics_electrical"


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
            "Captured Inputs and Assessment Status",  # Phase 4A: renamed from "Requirements"
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
    response = client.post(
        "/start",
        data={"idea": idea_text, "domain_confirm": "electronics_electrical"},
        follow_redirects=False,
    )
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
        # Scope the forbidden-word protection to the acknowledged-unknowns SECTION,
        # not the whole page. Increment 1A added a structured EVIDENCE_REQUESTED
        # action control elsewhere on the page — a request that evidence/a test is
        # needed, NOT a claim that evidence exists — which legitimately contains the
        # word "evidence". The original protection is unchanged in intent and still
        # enforced here: the unknowns section must not claim evidence exists and must
        # not use ILT-002 or evidence-state wording. The section is identified by its
        # stable heading and bounded by its list (no template/production change).
        marker = "What You Have Marked as Not Yet Known"
        assert marker in body  # the unknowns section is present (protection is live)
        start = body.index(marker)
        end = body.index("</ul>", start)
        unknowns_section = body[start:end]
        assert "ILT-002" not in unknowns_section
        assert "evidence" not in unknowns_section.lower()
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


_WEB_REASONED = (
    "The sensor detects voltage drop across the shunt resistor. "
    "When the measured voltage falls below the threshold, the comparator "
    "triggers the relay which disconnects the load. "
    "This mechanism relies on Ohm's law and uses an LM393 comparator IC."
)
_FORM_MARKER = 'name="response"'
_SUBMIT_MARKER = ">Submit</button>"
_COMPLETION_MARKER = "You have worked through the key questions for your idea."
_PMF_Q1 = (
    "Without describing how your mechanism works, describe the problem you are trying to solve. "
    "What is happening for the person or system that has this problem, and why does it matter to them?"
)
_PMF_HEADING = "How does your idea address the problem?"
_PMF_GUIDANCE = (
    "Describe the problem on its own terms first — who experiences it "
    "and why it matters — without describing your idea. Then explain how "
    "your idea is intended to address that problem, and identify situations "
    "where the match may be weaker."
)
_AI_Q1 = (
    "What are you taking for granted about your mechanism that you have not yet tested or verified? "
    "These might be things you expect to be true, materials you assume are available, "
    "or conditions you assume will hold."
)
_AI_HEADING_RENDERED = "What are you assuming that hasn&#39;t been tested yet?"
_AI_GUIDANCE = (
    "List anything you are taking for granted about your idea that you "
    "have not yet verified — materials, conditions, or behaviors you "
    "expect to hold true. Then note which of these would be most "
    "serious if they turned out to be wrong."
)
_CLOSING_FRAGMENT = "NOT do or NOT cover"


def _make_stage2_boundary_state(idea_id):
    state = IdeaState(idea_id=idea_id)
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    state.maturity_level = 1
    state.current_stage = 2
    state.known_problem = Evidence("existing systems miss micro-faults", REASONED, 1)
    state.known_mechanism = Evidence(_WEB_REASONED, REASONED, 2)
    state.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1, closed_at=2))
    state.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=CLOSED, opened_at=3, closed_at=4))
    state.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=PARTIAL, opened_at=5))
    state.iteration = 5
    return state


def test_stage3_rendered_browser_flow_form_persists_through_partial():
    sid = "test-stage3-rendered-flow-sid"
    _stage3_state = _make_stage2_boundary_state(sid)
    SESSION_STORE[sid] = {"state": _stage3_state,
                          "last_result": None, "transcript": [], "last_question": ""}
    seed_direct_session_envelope(sid, _stage3_state)  # explicit P4-1b-2a durable envelope
    try:
        client = app.test_client()
        answered_post(client, sid, {"response": _WEB_REASONED})
        state = SESSION_STORE[sid]["state"]
        assert state.current_stage == 3
        assert state.get_gap(PROBLEM_MECHANISM_FIT).status == "OPEN"
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert _FORM_MARKER in body and _SUBMIT_MARKER in body
        assert _PMF_Q1 in body and _PMF_HEADING in body and _PMF_GUIDANCE in body
        assert _COMPLETION_MARKER not in body and _CLOSING_FRAGMENT not in body
        answered_post(client, sid, {"response": _WEB_REASONED})
        assert state.get_gap(PROBLEM_MECHANISM_FIT).status == "PARTIAL"
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert _FORM_MARKER in body and _SUBMIT_MARKER in body
        assert _PMF_HEADING in body and _PMF_GUIDANCE in body
        assert _COMPLETION_MARKER not in body
        answered_post(client, sid, {"response": _WEB_REASONED})
        assert state.get_gap(PROBLEM_MECHANISM_FIT).status == "CLOSED"
        assert state.get_gap(ASSUMPTION_INVENTORY).status == "OPEN"
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert _FORM_MARKER in body and _SUBMIT_MARKER in body
        assert _AI_Q1 in body and _AI_HEADING_RENDERED in body and _AI_GUIDANCE in body
        assert _COMPLETION_MARKER not in body
        answered_post(client, sid, {"response": _WEB_REASONED})
        assert state.get_gap(ASSUMPTION_INVENTORY).status == "PARTIAL"
        body = client.get(f"/session/{sid}").get_data(as_text=True)
        assert _FORM_MARKER in body and _SUBMIT_MARKER in body
        assert _COMPLETION_MARKER not in body
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# Option B product-boundary enforcement at POST /start.
# DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B: current generic product activation is
# limited to electronics/electrical. infer_domain(), the registry loader, and
# all domain packs are unchanged — only product admission is restricted.
# Refused requests create no session and are never relabeled as electronics.
# ---------------------------------------------------------------------------

_ERROR_HTML = '<p class="error">' + UNSUPPORTED_DOMAIN_MESSAGE + '</p>'


def _start_post(client, idea, confirm=True):
    # Existing Option B refusal/admission tests exercise the bounded conflict
    # check, so they post WITH explicit electronics confirmation by default.
    data = {"idea": idea}
    if confirm:
        data["domain_confirm"] = "electronics_electrical"
    return client.post("/start", data=data, follow_redirects=False)


def test_start_admits_electronics_idea():
    client = app.test_client()
    before = set(SESSION_STORE)
    resp = _start_post(client, "ESP32 microcontroller circuit with a voltage sensor")
    assert resp.status_code == 302
    assert "/session/" in resp.headers["Location"]
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None
    assert entry["state"].domain == "electronics_electrical"
    assert entry["state"].domain_signal == "electronics_electrical"
    assert set(SESSION_STORE) == before | {sid}


def test_start_refuses_mechanical_idea_and_creates_no_session():
    client = app.test_client()
    before = set(SESSION_STORE)
    idea = "a gearbox with a rotating shaft and bearing torque"
    # Infrastructure inference still identifies the domain ...
    assert infer_domain(idea) == "mechanical"
    # ... but the product boundary refuses it.
    resp = _start_post(client, idea)
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert _ERROR_HTML in body                       # exact stable message rendered
    assert "Location" not in resp.headers             # no redirect to a session
    assert set(SESSION_STORE) == before               # no new session created
    assert "mechanical" not in [v["state"].domain for v in SESSION_STORE.values()]


def test_start_refuses_medical_device_idea_and_creates_no_session():
    client = app.test_client()
    before = set(SESSION_STORE)
    idea = "a surgical implant for patient diagnosis"
    assert infer_domain(idea) == "medical_device"
    resp = _start_post(client, idea)
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert _ERROR_HTML in body
    # the inferred internal pack id must not leak into the response
    assert "medical_device" not in body
    assert set(SESSION_STORE) == before
    assert "medical_device" not in [v["state"].domain for v in SESSION_STORE.values()]


def test_start_refuses_software_idea_and_creates_no_session():
    client = app.test_client()
    before = set(SESSION_STORE)
    idea = "a software application with an api backend and database"
    assert infer_domain(idea) == "software"
    resp = _start_post(client, idea)
    assert resp.status_code == 200
    assert _ERROR_HTML in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before
    assert "software" not in [v["state"].domain for v in SESSION_STORE.values()]


def test_start_without_confirmation_refused_even_when_inference_none(monkeypatch):
    # Under explicit confirmation, a None-classified idea is admitted ONLY with
    # confirmation; without confirmation it is refused and no session is created.
    client = app.test_client()
    before = set(SESSION_STORE)
    monkeypatch.setattr("web.app.classify_domain", _none_result)
    resp = _start_post(client, "something with no recognizable signals", confirm=False)
    assert resp.status_code == 200
    assert CONFIRMATION_REQUIRED_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before


def test_start_refuses_unexpected_inference_value_defensively(monkeypatch):
    # Defensive: an unexpected boundary return must be refused, never admitted
    # or converted to electronics.
    client = app.test_client()
    before = set(SESSION_STORE)
    monkeypatch.setattr("web.app.classify_domain", _multi_result)
    resp = _start_post(client, "an idea the boundary scores oddly")
    assert resp.status_code == 200
    assert _ERROR_HTML in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before
    assert "quantum_widgets" not in [v["state"].domain for v in SESSION_STORE.values()]


def test_start_does_not_fall_back_to_electronics_on_refusal(monkeypatch):
    # A refused non-electronics result must not produce an electronics session.
    client = app.test_client()
    before_electronics = sum(
        1 for v in SESSION_STORE.values() if v["state"].domain == "electronics_electrical"
    )
    monkeypatch.setattr("web.app.classify_domain", _single_result("mechanical"))
    resp = _start_post(client, "a mechanical idea forced through the boundary")
    assert resp.status_code == 200
    after_electronics = sum(
        1 for v in SESSION_STORE.values() if v["state"].domain == "electronics_electrical"
    )
    assert after_electronics == before_electronics    # no electronics fallback session


def test_governed_ilt002_routes_remain_electronics_pinned_after_restriction():
    # The generic /start restriction must not affect the electronics-pinned
    # governed ILT-002 / Path N routes.
    client = app.test_client()
    for route in (
        "/start_ilt002_water_leak",
        "/start_ilt002_combination_lock",
        "/start_ilt002_combination_lock_path_n",
    ):
        resp = client.post(route, data={"idea": "any idea text"}, follow_redirects=False)
        assert resp.status_code == 302
        assert "/session/" in resp.headers["Location"]
        sid = resp.headers["Location"].rsplit("/", 1)[-1]
        assert SESSION_STORE[sid]["state"].domain == "electronics_electrical"


def test_refusals_persist_no_non_electronics_domain():
    # Aggregate invariant: exercising all refusal cases adds no session, and no
    # stored session carries a non-electronics domain.
    client = app.test_client()
    before = set(SESSION_STORE)
    for idea in (
        "a gearbox with a rotating shaft and bearing torque",
        "a surgical implant for patient diagnosis",
        "a software application with an api backend and database",
    ):
        _start_post(client, idea)
    assert set(SESSION_STORE) == before
    assert all(v["state"].domain == "electronics_electrical" for v in SESSION_STORE.values())


# ---------------------------------------------------------------------------
# Option B start-page copy alignment: the landing page must reflect the current
# authorized product scope (electronics/electrical only) and must not advertise
# mechanical, medical-device, or software as currently supported. GET / has no
# user-entered content, so these assertions target purely static product copy.
# ---------------------------------------------------------------------------

def test_index_page_states_electronics_only_support():
    client = app.test_client()
    body = client.get("/").get_data(as_text=True)
    assert "Currently supported: electronics and electrical ideas." in body


def test_index_page_does_not_advertise_other_domains():
    client = app.test_client()
    body = client.get("/").get_data(as_text=True)
    assert "mechanical" not in body
    assert "medical device" not in body
    assert "medical_device" not in body
    assert "software" not in body


def test_index_page_placeholder_is_electronics_aligned():
    client = app.test_client()
    body = client.get("/").get_data(as_text=True)
    assert "Describe your electronics or electrical invention..." in body


def test_index_error_surface_renders_stable_refusal_message(monkeypatch):
    # The {{ error }} surface still renders the stable refusal message exactly
    # when /start refuses a non-electronics activation.
    client = app.test_client()
    monkeypatch.setattr("web.app.classify_domain", _multi_result)
    body = _start_post(client, "a mechanical idea forced through the boundary").get_data(as_text=True)
    assert _ERROR_HTML in body


# ---------------------------------------------------------------------------
# Explicit electronics/electrical domain confirmation at the generic boundary
# (ADR-001 explicit assignment). POST /start requires non-empty idea text AND
# an affirmative electronics/electrical confirmation. infer_domain() is used
# only as a bounded conflict check: electronics or None is admitted under
# confirmation; a clearly different supported domain is refused and never
# relabeled. infer_domain(), the registry, and the packs are unchanged here.
# ---------------------------------------------------------------------------

WATER_LEAK_IDEA = (
    "A small device installed near a household water pipe detects an early leak, "
    "sounds a local alarm, and sends a notification to the user's phone."
)


def _admitted_sid(resp):
    assert resp.status_code == 302 and "/session/" in resp.headers["Location"]
    return resp.headers["Location"].rsplit("/", 1)[-1]


def test_confirm_admits_valid_electronics_idea():
    client = app.test_client()
    before = set(SESSION_STORE)
    resp = _start_post(client, "ESP32 microcontroller circuit with a voltage sensor")
    sid = _admitted_sid(resp)
    assert SESSION_STORE[sid]["state"].domain == "electronics_electrical"
    assert set(SESSION_STORE) == before | {sid}


def test_water_leak_admitted_even_if_inference_is_none(monkeypatch):
    # Proves admission rests on explicit confirmation + the bounded conflict
    # rule, NOT on the accidental 'led' substring: even when the classifier
    # returns None (as it would after substring matching is corrected later),
    # the confirmed water-leak idea is admitted.
    client = app.test_client()
    monkeypatch.setattr("web.app.classify_domain", _none_result)
    sid = _admitted_sid(_start_post(client, WATER_LEAK_IDEA))
    assert SESSION_STORE[sid]["state"].domain == "electronics_electrical"


def test_functional_electronics_paraphrase_admitted_when_confirmed():
    # A functional electronics idea with no component keywords infers None, yet
    # is admitted because the user explicitly confirmed the domain.
    idea = "A gadget that watches for a problem and warns the homeowner right away"
    assert infer_domain(idea) is None              # no signal keyword present
    client = app.test_client()
    sid = _admitted_sid(_start_post(client, idea))
    assert SESSION_STORE[sid]["state"].domain == "electronics_electrical"


def test_no_confirmation_creates_no_session():
    client = app.test_client()
    before = set(SESSION_STORE)
    resp = _start_post(client, "ESP32 microcontroller circuit", confirm=False)
    assert resp.status_code == 200
    assert CONFIRMATION_REQUIRED_MESSAGE in resp.get_data(as_text=True)
    assert "Location" not in resp.headers
    assert set(SESSION_STORE) == before


def test_empty_idea_creates_no_session_even_with_confirmation():
    client = app.test_client()
    before = set(SESSION_STORE)
    resp = client.post("/start", data={"idea": "   ", "domain_confirm": DOMAIN_CONFIRM_VALUE},
                       follow_redirects=False)
    assert resp.status_code == 302
    assert "/session/" not in resp.headers.get("Location", "")
    assert set(SESSION_STORE) == before


def test_confirmed_software_idea_refused_and_no_session():
    client = app.test_client()
    before = set(SESSION_STORE)
    idea = "a software application with an api backend and database"
    assert infer_domain(idea) == "software"
    resp = _start_post(client, idea)              # confirmation present
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert _ERROR_HTML in body and "software" not in body
    assert set(SESSION_STORE) == before


def test_confirmed_medical_idea_refused_and_no_session():
    client = app.test_client()
    before = set(SESSION_STORE)
    idea = "a surgical implant for patient diagnosis"
    assert infer_domain(idea) == "medical_device"
    resp = _start_post(client, idea)
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert _ERROR_HTML in body and "medical_device" not in body
    assert set(SESSION_STORE) == before


def test_confirmed_mechanical_idea_refused_and_no_session():
    client = app.test_client()
    before = set(SESSION_STORE)
    idea = "a gearbox with a rotating shaft and bearing torque"
    assert infer_domain(idea) == "mechanical"
    resp = _start_post(client, idea)
    assert resp.status_code == 200
    assert _ERROR_HTML in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before


def test_confirmation_never_relabels_conflicting_domain():
    # A confirmed-but-conflicting idea must neither persist its real domain nor
    # be silently converted into an electronics session.
    client = app.test_client()
    before_electronics = sum(
        1 for v in SESSION_STORE.values() if v["state"].domain == "electronics_electrical")
    for idea in ("a gearbox with a rotating shaft and bearing torque",
                 "a surgical implant for patient diagnosis",
                 "a software application with an api backend and database"):
        _start_post(client, idea)                 # confirmed, yet conflicting
    after_electronics = sum(
        1 for v in SESSION_STORE.values() if v["state"].domain == "electronics_electrical")
    assert after_electronics == before_electronics
    assert all(v["state"].domain == "electronics_electrical" for v in SESSION_STORE.values())


def test_unexpected_classifier_value_refused_even_with_confirmation(monkeypatch):
    client = app.test_client()
    before = set(SESSION_STORE)
    # P9-E2-R: an unadmittable (richer-kind) classification fails closed even under
    # explicit confirmation — no session, never relabeled electronics. (An
    # out-of-scope SINGLE value like "quantum_widgets" is now impossible to
    # construct — see the invariant tests in tests/test_p9e2r_result_representation.)
    monkeypatch.setattr("web.app.classify_domain", _multi_result)
    resp = _start_post(client, "an idea the boundary scores oddly")
    assert resp.status_code == 200
    assert _ERROR_HTML in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before


def test_index_page_states_scope_and_has_confirmation_control():
    client = app.test_client()
    body = client.get("/").get_data(as_text=True)
    # current scope stated
    assert "Electronics and electrical ideas are currently supported." in body
    # required confirmation control present
    assert 'name="domain_confirm"' in body
    assert 'value="electronics_electrical"' in body
    assert "required" in body
    assert "I confirm that this idea is primarily an electronics or electrical idea." in body
