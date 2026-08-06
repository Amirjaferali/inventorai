"""Phase 2 fix — session page shows friendly gap labels, not raw internal IDs.

The two session-page surfaces that previously leaked raw gap-type IDs — the Next
Development Step "Reference:" line and acknowledged-unknown gap contexts — now
render short inventor-friendly labels. Internal IDs, state, engine behaviour and
the final deliverable are unchanged; non-gap references pass through untouched.
"""
import os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.gap_labels import friendly_gap_name, GAP_DISPLAY_NAMES
from web.app import app, SESSION_STORE
from engine.idea_state import (
    IdeaState, Evidence, REASONED, Gap, OPEN, MECHANISM_COMPLETENESS,
    AcknowledgedUnknown,
)

_SIX = [
    ("MECHANISM_COMPLETENESS", "Working mechanism"),
    ("PHYSICAL_FEASIBILITY", "Practical feasibility"),
    ("BOUNDARY_AMBIGUITY", "Scope and boundaries"),
    ("PROBLEM_MECHANISM_FIT", "Problem–solution fit"),
    ("ASSUMPTION_INVENTORY", "Untested assumptions"),
    ("EXPERTISE_GAP_AWARENESS", "Expertise needed"),
]


# --- helper unit ------------------------------------------------------------

@pytest.mark.parametrize("raw,friendly", _SIX)
def test_friendly_gap_name_maps_all_six(raw, friendly):
    assert friendly_gap_name(raw) == friendly


def test_map_covers_exactly_the_six_known_gap_types():
    assert set(GAP_DISPLAY_NAMES) == {raw for raw, _ in _SIX}


@pytest.mark.parametrize("value", ["rec_1", "maturity_level_0", "rec_12", "unknown_thing", None, ""])
def test_non_gap_references_pass_through_unchanged(value):
    assert friendly_gap_name(value) == value  # never mangled


# --- rendered session page --------------------------------------------------

def test_session_reference_line_shows_friendly_label_not_raw_id():
    client = app.test_client()
    r = client.post(
        "/start_ilt002_water_leak",
        data={"idea": "An electronic under-sink water leak sensor with wireless alert."},
        follow_redirects=False,
    )
    sid = r.headers["Location"].split("/session/")[1]
    resp = client.get(f"/session/{sid}")
    assert resp.status_code == 200  # route unaffected
    body = resp.get_data(as_text=True)
    assert "Working mechanism" in body                   # friendly label rendered
    assert "MECHANISM_COMPLETENESS" not in body          # raw internal id not exposed
    # the state still holds the raw internal id (backend unchanged)
    state = SESSION_STORE[sid]["state"]
    assert any(g.gap_type == "MECHANISM_COMPLETENESS" for g in state.gaps)
    SESSION_STORE.pop(sid, None)


def test_session_acknowledged_unknown_shows_friendly_label():
    sid = "friendly-unknown-" + uuid.uuid4().hex[:8]
    s = IdeaState(idea_id=sid)
    s.domain_signal = "electronics_electrical"
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=1))
    s.acknowledged_unknowns.append(
        AcknowledgedUnknown(
            iteration=1,
            gap_context="PHYSICAL_FEASIBILITY",
            verbatim="I do not yet know the exact supply voltage.",
            category_basis="owner",
        )
    )
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": []}
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "What You Have Marked as Not Yet Known" in body
        assert "Practical feasibility:" in body           # friendly label rendered
        assert "PHYSICAL_FEASIBILITY" not in body          # raw internal id not exposed
        # backend value remains the raw internal id
        assert s.acknowledged_unknowns[0].gap_context == "PHYSICAL_FEASIBILITY"
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_raw_underscore_gap_ids_for_the_six_in_session_html():
    client = app.test_client()
    r = client.post(
        "/start_ilt002_water_leak",
        data={"idea": "An electronic under-sink water leak sensor with wireless alert."},
        follow_redirects=False,
    )
    sid = r.headers["Location"].split("/session/")[1]
    body = client.get(f"/session/{sid}").get_data(as_text=True)
    for raw, _ in _SIX:
        assert raw not in body, f"raw gap id leaked in session HTML: {raw}"
    SESSION_STORE.pop(sid, None)


def test_final_deliverable_route_unaffected():
    client = app.test_client()
    r = client.post(
        "/start_ilt002_water_leak",
        data={"idea": "An electronic under-sink water leak sensor with wireless alert."},
        follow_redirects=False,
    )
    sid = r.headers["Location"].split("/session/")[1]
    assert client.get(f"/session/{sid}/deliverable").status_code == 200
    SESSION_STORE.pop(sid, None)
