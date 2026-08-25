"""W2-A / RVR-4 — durable-contract compatibility (frozen contract §4).

Covers RVR4-COMPAT-1..5 and the load-side fail-closed rules for malformed
persisted decision-action payloads (RVR4-OW6-7's restore-verbatim half).
The bounded legacy rule: a payload missing ONLY `decision_context_root` with a
LEGACY disposition loads with None; decision-action payloads get no escape.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    IdeaState, PHYSICAL_FEASIBILITY,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
)
from engine.record_contract import (
    ProjectRecordContract, assertion_to_dict, assertion_from_dict,
    ContractError, UnknownFieldError, CONTRACT_VERSION, _ASSERTION_FIELDS,
)

CTX = DISPOSITION_DECISION_CONTEXT_DECLARED
ALT = DISPOSITION_DECISION_ALTERNATIVE_DECLARED
WDR = DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN


def _legacy_payload(rid="rec_1", disposition="answered", **over):
    p = {
        "record_id": rid, "disposition": disposition, "content": "an answer",
        "gap_context": PHYSICAL_FEASIBILITY, "iteration": 1,
        "provenance": "OWNER_STATED", "validation_status": "UNVALIDATED",
        "quality": None, "pending": None, "responsibility": "OWNER_INPUT",
        "resolves_gap": False, "contradicts": [], "supersedes": [],
        "superseded_by": None,
    }
    p.update(over)
    return p


def _decision_payload(rid, disposition, root, supersedes=(), **over):
    p = _legacy_payload(rid, disposition)
    p["gap_context"] = None
    p["decision_context_root"] = root
    p["supersedes"] = list(supersedes)
    p.update(over)
    return p


def _envelope(payloads):
    return {"contract_version": CONTRACT_VERSION, "idea_id": "pid-1",
            "assertions": payloads}


def test_field_set_is_exactly_fifteen_with_new_field():
    assert "decision_context_root" in _ASSERTION_FIELDS
    assert len(_ASSERTION_FIELDS) == 15


def test_compat1_legacy_payload_missing_only_new_field_loads_none():
    for disposition in ("answered", "unknown", "deferred",
                        "provisional_assumption", "specialist_requested",
                        "evidence_requested", "risk_accepted"):
        p = _legacy_payload(disposition=disposition)
        assert "decision_context_root" not in p
        r = assertion_from_dict(p)
        assert r.decision_context_root is None
        assert r.disposition == disposition


def test_serializer_always_emits_new_field_and_roundtrips():
    s = IdeaState(idea_id="pid-1")
    ctx = s.record_interaction(action=CTX, content="which latch?")
    s.record_interaction(action=ALT, content="toggle",
                         decision_context_root=ctx.record_id)
    s.record_interaction(action="answered", content="a",
                         gap_context=PHYSICAL_FEASIBILITY)
    c = ProjectRecordContract.from_state(s)
    data = c.to_dict()
    assert all("decision_context_root" in p for p in data["assertions"])
    restored = ProjectRecordContract.from_dict(data)
    assert restored.to_dict() == data          # lossless round trip
    got = {r.record_id: r for r in restored.assertions}
    assert got[ctx.record_id].decision_context_root is None
    assert got["rec_2"].decision_context_root == ctx.record_id


def test_compat2_decision_action_payload_missing_field_fails_closed():
    p = _legacy_payload(disposition=ALT)   # decision disposition, field absent
    p["gap_context"] = None
    with pytest.raises(ContractError):
        assertion_from_dict(p)


def test_compat2_malformed_decision_payloads_fail_on_validate():
    ctx = _decision_payload("rec_1", CTX, None)
    # alternative with null root
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(_envelope(
            [ctx, _decision_payload("rec_2", ALT, None)]))
    # nonexistent root
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(_envelope(
            [ctx, _decision_payload("rec_2", ALT, "rec_999")]))
    # wrong-class root (root is a legacy answer)
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(_envelope(
            [_legacy_payload("rec_1"),
             _decision_payload("rec_2", ALT, "rec_1")]))
    # context declaration carrying a non-null root
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(_envelope(
            [ctx, _decision_payload("rec_2", CTX, "rec_1")]))
    # forbidden gap_context on a decision action
    bad = _decision_payload("rec_2", ALT, "rec_1",
                            gap_context=PHYSICAL_FEASIBILITY)
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(_envelope([ctx, bad]))
    # cross-context withdrawal (root B over A's alternative)
    ctx_b = _decision_payload("rec_2", CTX, None)
    alt_a = _decision_payload("rec_3", ALT, "rec_1",
                              superseded_by="rec_4")
    wdr_bad = _decision_payload("rec_4", WDR, "rec_2",
                                supersedes=["rec_3"])
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(_envelope([ctx, ctx_b, alt_a, wdr_bad]))
    # multi-target decision supersession
    alt1 = _decision_payload("rec_2", ALT, "rec_1", superseded_by="rec_4")
    alt2 = _decision_payload("rec_3", ALT, "rec_1")
    multi = _decision_payload("rec_4", ALT, "rec_1",
                              supersedes=["rec_2", "rec_3"])
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(_envelope([ctx, alt1, alt2, multi]))


def test_compat3_unknown_fields_still_rejected():
    p = _legacy_payload()
    p["decision_context_root"] = None
    p["sneaky_extra"] = 1
    with pytest.raises(UnknownFieldError):
        assertion_from_dict(p)


def test_compat4_all_other_missing_fields_still_rejected():
    p = _legacy_payload()          # legacy disposition
    del p["content"]               # some OTHER field missing too
    with pytest.raises(UnknownFieldError):
        assertion_from_dict(p)
    p2 = _legacy_payload()
    del p2["provenance"]
    with pytest.raises(UnknownFieldError):
        assertion_from_dict(p2)


def test_compat5_pre_w2a_envelope_loads_without_migration():
    # A full stored pre-W2-A project: every payload has exactly the legacy 14
    # fields. It must load, reconcile, validate, and rebuild a state verbatim.
    a1 = _legacy_payload("rec_1")
    a2 = _legacy_payload("rec_2", superseded_by=None)
    a2["supersedes"] = ["rec_1"]
    c = ProjectRecordContract.from_dict(_envelope([a1, a2]))
    st = c.to_state()
    got = {r.record_id: r for r in st.assertions}
    assert got["rec_1"].superseded_by == "rec_2"      # inverse edge re-derived
    assert got["rec_1"].decision_context_root is None
    assert got["rec_2"].content == "an answer"


def test_valid_decision_envelope_restores_verbatim():
    ctx = _decision_payload("rec_1", CTX, None)
    alt = _decision_payload("rec_2", ALT, "rec_1", superseded_by="rec_3")
    wdr = _decision_payload("rec_3", WDR, "rec_1", supersedes=["rec_2"])
    c = ProjectRecordContract.from_dict(_envelope([ctx, alt, wdr]))
    got = {r.record_id: r for r in c.assertions}
    assert got["rec_2"].decision_context_root == "rec_1"
    assert got["rec_3"].disposition == WDR
    assert got["rec_2"].superseded_by == "rec_3"
