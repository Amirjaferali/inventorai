"""P10-SEC3 — Decision-Workspace Free-Text Hardening Residual Extension (RED/GREEN).

Behaviour-based tests for the bounded technical-continuation gate extending
the canonical P10-SEC2 free-text guard (`web/app.py` `_free_text_error`:
MAX_FREE_TEXT_CHARS cap + NUL rejection; explicit rejection, never
truncation) to the Decision Workspace's seven POST surfaces — exactly the
documented residual recorded by the authoritative release-readiness checklist
row RL-A6 ("criticality/decision-workspace free text are transport-bounded
ONLY"). After this gate the Decision Workspace free-text fields are
field-bounded; the criticality rationale and the legacy fixed-domain ILT-002
start routes REMAIN transport-bounded residuals (truthfully documented).

Guarded fields per route (reconstructed from source):
  /input           text, provenance
  /constraint      text, provenance
  /gap             rationale
  /evidence        text, provenance, method, source_label, evidence_version,
                   limitations
  /gap-assessment  rationale, resolution_rationale
  /preference      rationale
  /candidate       disposition_reason, disposition_basis

Rejections reuse the route family's EXISTING error convention
(`_render_decision_workspace(record, error=..., status=400)`), run BEFORE any
engine call, and mutate nothing. Unicode/Arabic/multiline text and
exactly-at-limit input pass untouched.
"""
import re

import pytest

import web.app as webapp
from web.app import app

LIMIT = 20000
ARABIC = "سبب متعدد الأسطر:\nالسطر الثاني مع علامات ترقيم! ونسبة 50%."
VALID_INPUT = {"claim_class": "observed_fact", "provenance": "operator_entered"}


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _new_workspace(client):
    r = client.get("/decision-workspace")
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/decision-workspace/", 1)[-1]


def _view(client, did):
    return client.get("/decision-workspace/%s" % did).get_data(as_text=True)


def _inputs(did):
    return webapp.FDC001_DECISIONS[did].inputs


def _seeded(did):
    """A fresh DecisionRecord ships with seeded owner-context inputs — capture
    the baseline so mutation checks assert the DELTA, not emptiness."""
    return len(_inputs(did))


OUR_LIMIT_MSG = "longer than the allowed limit"
OUR_NUL_MSG = "invalid character"


# ==========================================================================
# Over-limit / NUL rejection — explicit, convention-preserving, no mutation
# ==========================================================================
def test_input_text_over_limit_rejected_no_mutation():
    client = _new_client()
    did = _new_workspace(client)
    before = _seeded(did)
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT, text="y" * (LIMIT + 1)))
    assert r.status_code == 400
    assert OUR_LIMIT_MSG in r.get_data(as_text=True)   # OUR guard, not engine
    assert _seeded(did) == before                      # nothing stored


def test_input_null_byte_rejected_no_mutation():
    client = _new_client()
    did = _new_workspace(client)
    before = _seeded(did)
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT, text="valid\x00text"))
    assert r.status_code == 400
    assert OUR_NUL_MSG in r.get_data(as_text=True)
    assert _seeded(did) == before


def test_input_provenance_field_also_guarded():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data={"text": "ok", "claim_class": "observed_fact",
                          "provenance": "p" * (LIMIT + 1)})
    assert r.status_code == 400
    # OUR guard fires (not the engine's provenance-enum rule)
    assert OUR_LIMIT_MSG in r.get_data(as_text=True)


def test_constraint_text_over_limit_rejected():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/constraint" % did,
                    data={"text": "y" * (LIMIT + 1),
                          "constraint_strength": "hard",
                          "provenance": "operator_entered"})
    assert r.status_code == 400
    assert OUR_LIMIT_MSG in r.get_data(as_text=True)
    assert webapp.FDC001_DECISIONS[did].constraints == []


def test_gap_rationale_over_limit_rejected():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/gap" % did,
                    data={"action": "waive", "gap_id": "gap-x",
                          "rationale": "y" * (LIMIT + 1)})
    assert r.status_code == 400
    assert OUR_LIMIT_MSG in r.get_data(as_text=True)   # guard precedes engine


def test_evidence_free_text_fields_guarded():
    client = _new_client()
    did = _new_workspace(client)
    for field in ("text", "provenance", "method", "source_label",
                  "evidence_version", "limitations"):
        data = {"gap_id": "gap-x", "text": "ok",
                "claim_class": "operator_reported_result",
                "provenance": "operator_entered"}
        data[field] = "y" * (LIMIT + 1)
        r = client.post("/decision-workspace/%s/evidence" % did, data=data)
        assert r.status_code == 400, field
        assert OUR_LIMIT_MSG in r.get_data(as_text=True), field


def test_gap_assessment_rationales_guarded():
    client = _new_client()
    did = _new_workspace(client)
    for field in ("rationale", "resolution_rationale"):
        data = {"gap_id": "gap-x", "assessment": "resolved",
                "rationale": "ok", "resolution_decision": ""}
        data[field] = "y" * (LIMIT + 1)
        r = client.post("/decision-workspace/%s/gap-assessment" % did,
                        data=data)
        assert r.status_code == 400, field
        assert OUR_LIMIT_MSG in r.get_data(as_text=True), field


def test_preference_rationale_guarded():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/preference" % did,
                    data={"action": "prefer", "candidate_id": "cand-x",
                          "rationale": "y" * (LIMIT + 1)})
    assert r.status_code == 400
    assert OUR_LIMIT_MSG in r.get_data(as_text=True)


def test_candidate_disposition_fields_guarded():
    client = _new_client()
    did = _new_workspace(client)
    for field in ("disposition_reason", "disposition_basis"):
        data = {"candidate_id": "cand-x", "option_status": "eliminated",
                "disposition_reason": "ok", "disposition_basis": "ok"}
        data[field] = "y" * (LIMIT + 1)
        r = client.post("/decision-workspace/%s/candidate" % did, data=data)
        assert r.status_code == 400, field
        assert OUR_LIMIT_MSG in r.get_data(as_text=True), field


def test_rejection_does_not_echo_raw_input():
    client = _new_client()
    did = _new_workspace(client)
    marker = "ZZDWMARKERZZ"
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT,
                              text=("y" * (LIMIT + 1)).replace(
                                  "yyyy", marker, 1)))
    assert r.status_code == 400
    assert marker not in r.get_data(as_text=True)


# ==========================================================================
# Preservation — at-limit, Arabic/multiline, engine semantics, conventions
# ==========================================================================
def test_exactly_at_limit_input_accepted_and_stored():
    client = _new_client()
    did = _new_workspace(client)
    before = _seeded(did)
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT, text="y" * LIMIT))
    assert r.status_code == 302                     # normal PRG acceptance
    stored = _inputs(did)
    assert len(stored) == before + 1
    assert stored[-1].text == "y" * LIMIT           # verbatim, no truncation


def test_arabic_multiline_input_preserved_verbatim():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT, text=ARABIC))
    assert r.status_code == 302
    assert _inputs(did)[-1].text == ARABIC


def test_engine_validation_semantics_unchanged():
    """Normal-size invalid submissions still fail through the EXISTING engine
    error convention — the guard neither replaces nor masks it."""
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data={"text": "ok", "claim_class": "not_a_class",
                          "provenance": "operator_entered"})
    assert r.status_code == 400
    assert "Input rejected:" in r.get_data(as_text=True)
    # blank text still hits the engine's own blank rule, not our guard
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT, text="   "))
    assert r.status_code == 400
    assert "Input rejected:" in r.get_data(as_text=True)


def test_ownership_denial_precedes_guard():
    """A non-owner/foreign workspace id still gets the generic non-enumerating
    denial redirect — the guard never runs first and never discloses
    existence."""
    client = _new_client()
    r = client.post("/decision-workspace/no-such-decision/input",
                    data=dict(VALID_INPUT, text="y" * (LIMIT + 1)))
    assert r.status_code == 302
    assert r.headers["Location"].endswith("/decision-workspace")


def test_security_headers_on_rejection():
    client = _new_client()
    did = _new_workspace(client)
    r = client.post("/decision-workspace/%s/input" % did,
                    data=dict(VALID_INPUT, text="y" * (LIMIT + 1)))
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("Content-Security-Policy")
    assert "Strict-Transport-Security" not in r.headers
