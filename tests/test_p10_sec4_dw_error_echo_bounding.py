"""P10-SEC4 — Decision-Workspace Engine-Error Echo Bounding (RED/GREEN).

Behaviour-based tests for the bounded technical-continuation gate that bounds
the USER-REFLECTED copy of deterministic engine diagnostics in the Decision
Workspace 400 error convention.

Confirmed base behavior (live probe, source: engine/decision_workspace.py
raises ``DecisionError("invalid claim_class: %r" % claim_class)`` and ~14
similar sites; web/app.py renders ``error="Input rejected: %s" % exc``): a
user-controlled enum/id field of arbitrary size (up to the 128 KiB transport
bound — these fields are NOT free-text-guarded, deliberately) is echoed
VERBATIM into the 400 page (autoescaped, so no markup executes — proven —
but kilobytes of reflected junk).

The fix bounds ONLY the rendered message via the route family's existing
error seam (`_dw_bounded_error`): messages over `_DW_ERROR_ECHO_BOUND` chars
are truncated with an EXPLICIT marker; short legitimate diagnostics render
verbatim; the engine's own exception messages remain byte-complete (no
engine change); the P10-SEC3 free-text guard and its precedence are
untouched.
"""
import pytest

import web.app as webapp
from web.app import app
from engine import decision_workspace as fdc001_dw

JUNK = "J" * 50000
VALID_INPUT = {"claim_class": "observed_fact", "provenance": "operator_entered"}


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _new_workspace(client):
    r = client.get("/decision-workspace")
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/decision-workspace/", 1)[-1]


# ==========================================================================
# Echo bounding on representative surfaces
# ==========================================================================
def test_input_claim_class_junk_not_echoed_unbounded():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data={"text": "ok", "claim_class": JUNK,
                          "provenance": "operator_entered"})
    body = r.get_data(as_text=True)
    assert r.status_code == 400
    assert JUNK[:1000] not in body                 # bulk junk never reflected
    assert "Input rejected" in body                # diagnostic prefix kept
    assert "[diagnostic truncated]" in body        # explicit, never silent


def test_constraint_strength_junk_bounded():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/constraint" % did,
                    data={"text": "ok", "constraint_strength": JUNK,
                          "provenance": "operator_entered"})
    body = r.get_data(as_text=True)
    assert r.status_code == 400
    assert JUNK[:1000] not in body
    assert "Constraint rejected" in body
    assert "[diagnostic truncated]" in body


def test_gap_assessment_enum_junk_bounded():
    client = _new_client()
    did = _new_workspace(client)
    # the engine validates gap_id FIRST (source order), so the junk goes in
    # the first-checked field: "unknown gap_id: %r" is the echoing diagnostic
    r = client.post("/decision-workspace/%s/gap-assessment" % did,
                    data={"gap_id": JUNK, "assessment": "resolved",
                          "rationale": "ok", "resolution_decision": ""})
    body = r.get_data(as_text=True)
    assert r.status_code == 400
    assert JUNK[:1000] not in body
    assert "[diagnostic truncated]" in body


def test_candidate_id_junk_bounded():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/preference" % did,
                    data={"action": "set", "candidate_id": JUNK,
                          "rationale": "ok"})
    body = r.get_data(as_text=True)
    assert r.status_code == 400
    assert JUNK[:1000] not in body
    assert "[diagnostic truncated]" in body


def test_bounded_error_page_stays_small():
    client = _new_client()
    did = _new_workspace(client)
    normal = len(client.get("/decision-workspace/%s" % did).get_data())
    r = client.post("/decision-workspace/%s/input" % did,
                    data={"text": "ok", "claim_class": JUNK,
                          "provenance": "operator_entered"})
    # the error page must not balloon with reflected junk: allow only the
    # bounded message + small rendering overhead over the normal page
    assert len(r.get_data()) < normal + 2000


# ==========================================================================
# Diagnostics preserved — short messages verbatim; engine unchanged
# ==========================================================================
def test_short_legitimate_diagnostic_rendered_verbatim():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data={"text": "ok", "claim_class": "not_a_class",
                          "provenance": "operator_entered"})
    body = r.get_data(as_text=True)
    assert r.status_code == 400
    # full deterministic engine diagnostic, untruncated (Jinja-escaped quotes)
    assert "invalid claim_class:" in body
    assert "not_a_class" in body
    assert "[diagnostic truncated]" not in body


def test_engine_exception_message_remains_complete():
    """The bound is RENDER-ONLY: the engine's own DecisionError still carries
    the full deterministic diagnostic (no engine change, nothing hidden at
    the engine seam)."""
    record = fdc001_dw.DecisionRecord()
    with pytest.raises(fdc001_dw.DecisionError) as excinfo:
        record.add_input("ok", JUNK, "operator_entered")
    assert JUNK in str(excinfo.value)              # byte-complete at the seam


def test_helper_bound_semantics():
    bounded = webapp._dw_bounded_error("Input rejected", ValueError("x" * 10))
    assert bounded == "Input rejected: " + "x" * 10          # short: verbatim
    long_msg = webapp._dw_bounded_error("Input rejected", ValueError("x" * 5000))
    assert long_msg.endswith(" … [diagnostic truncated]")
    assert len(long_msg) <= webapp._DW_ERROR_ECHO_BOUND + len(
        " … [diagnostic truncated]")


# ==========================================================================
# Preservation — autoescape, SEC3 precedence, headers
# ==========================================================================
def test_markup_still_escaped_never_executed():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data={"text": "ok", "claim_class": "<script>alert(1)</script>",
                          "provenance": "operator_entered"})
    body = r.get_data(as_text=True)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;" in body                # escaped rendering intact


def test_sec3_free_text_guard_precedence_untouched():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT, text="y" * 20001))
    body = r.get_data(as_text=True)
    assert r.status_code == 400
    assert "longer than the allowed limit" in body  # SEC3 guard, not engine
    assert "[diagnostic truncated]" not in body


def test_security_headers_on_bounded_rejection():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data={"text": "ok", "claim_class": JUNK,
                          "provenance": "operator_entered"})
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("Content-Security-Policy")
    assert "Strict-Transport-Security" not in r.headers
