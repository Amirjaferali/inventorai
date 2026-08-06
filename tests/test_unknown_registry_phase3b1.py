"""Phase 3B-1 — Unknown Registry pilot for acknowledged-unknown deduplication.

Full acknowledged-unknown verbatim appears once (Section 5 / registry); Section 8
references the registry entries (UNK-001/UNK-002) instead of re-copying the long
text. Additive and nested under _session_meta so the top-level canonical-section
contract is unchanged. A SEPARATE namespace/registry from Phase 3A, so EV-001 /
EV-002 and the evidence_registry are untouched. Sections 10 and 11 are
intentionally NOT changed by this phase. No unknown is deleted and no claim is
added.
"""
import json, os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState, Evidence, REASONED, AcknowledgedUnknown
from web.app import app, SESSION_STORE

UNK1 = ("I do not know how long the backup battery must last to survive a multi-hour "
        "power loss without losing the temperature log during a rural delivery route.")
UNK2 = ("I am unsure which wireless protocol keeps working reliably across metal-walled "
        "refrigerated trailers in rural areas with weak or intermittent cellular coverage.")
PROBLEM = ("Delivered meat spoils when the refrigerated compartment drifts out of its safe "
           "temperature band during transit and the driver is not warned in time.")
MECHANISM = ("A microcontroller reads several digital temperature sensors, logs each reading, "
             "and raises a wireless alert to the cabin when the band is exceeded.")

TOP_LEVEL_ENVELOPE = {"package_version", "schema_id", "session_id", "generated_at"}
CANONICAL_SECTIONS = {
    "section_1_disclaimer", "section_2_invention_summary", "section_3_assessment_overview",
    "section_4_requirements", "section_5_assumptions", "section_6_risks",
    "section_7_recommendations", "section_8_unresolved_items", "section_9_stage3_reasoning",
    "section_10_recommended_next_steps", "section_11_prototype_test_plan",
    "section_12_next_development_step", "section_13_requirement_landscape",
    "section_14_validation_plan",
}


def _state(unknowns=((2, "ASSUMPTION_INVENTORY", UNK1), (3, "EXPERTISE_GAP_AWARENESS", UNK2)),
           problem=PROBLEM, mechanism=MECHANISM):
    s = IdeaState(idea_id="unk-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.current_stage = 3
    if problem is not None:
        s.idea_summary = problem
        s.known_problem = Evidence(problem, REASONED, 1)
    if mechanism is not None:
        s.known_mechanism = Evidence(mechanism, REASONED, 2)
    s.acknowledged_unknowns = [AcknowledgedUnknown(i, ctx, txt, "reasoned")
                               for (i, ctx, txt) in unknowns]
    return s


def _registry(pkg):
    return pkg["_session_meta"]["unknown_registry"]


# --- registry creation ------------------------------------------------------

def test_unk_ids_created_in_list_order():
    reg = _registry(assemble_deliverable(_state()))
    assert [e["unknown_id"] for e in reg] == ["UNK-001", "UNK-002"]
    assert reg[0]["content"] == UNK1
    assert reg[1]["content"] == UNK2


def test_registry_entry_shape():
    reg = _registry(assemble_deliverable(_state()))
    e = reg[0]
    assert e["unknown_id"] == "UNK-001"
    assert e["label"] == "Acknowledged Unknown 1"
    assert e["content"] == UNK1                      # full verbatim carried once
    assert e["gap_context"] == "Assumption Inventory"
    assert e["source"] == "inventor_stated"
    assert e["category_basis"] == "reasoned"


def test_ids_are_list_order_not_iteration():
    # iteration values (2, 3) must NOT drive the id; position (1, 2) does.
    reg = _registry(assemble_deliverable(
        _state(unknowns=((7, "ASSUMPTION_INVENTORY", UNK1), (7, "EXPERTISE_GAP_AWARENESS", UNK2)))))
    assert [e["unknown_id"] for e in reg] == ["UNK-001", "UNK-002"]  # stable despite equal iteration


def test_no_entries_when_no_acknowledged_unknowns():
    reg = _registry(assemble_deliverable(_state(unknowns=())))
    assert reg == []


# --- section 5 primary display ----------------------------------------------

def test_section5_shows_full_text_with_unknown_id():
    pkg = assemble_deliverable(_state())
    unknowns = pkg["section_5_assumptions"]["inventor_unknowns"]
    assert [u["unknown_id"] for u in unknowns] == ["UNK-001", "UNK-002"]
    assert unknowns[0]["statement"] == UNK1          # full text still shown here
    assert unknowns[0]["iteration"] == 2             # preserved
    assert unknowns[0]["gap_context"] == "Assumption Inventory"


# --- section 8 references (dedup) -------------------------------------------

def test_section8_references_unknown_ids_not_full_text():
    pkg = assemble_deliverable(_state())
    items = [i for i in pkg["section_8_unresolved_items"]["items"]
             if i.get("type") == "acknowledged_unknown"]
    by_uid = {i["unknown_id"]: i for i in items}
    assert by_uid["UNK-001"]["statement"] == "See UNK-001 — Acknowledged unknown"
    assert by_uid["UNK-002"]["statement"] == "See UNK-002 — Acknowledged unknown"
    blob = json.dumps(pkg["section_8_unresolved_items"])
    assert UNK1 not in blob                          # full verbatim NOT re-copied here
    assert UNK2 not in blob


def test_section8_preserves_existing_item_id_and_provenance():
    pkg = assemble_deliverable(_state())
    items = [i for i in pkg["section_8_unresolved_items"]["items"]
             if i.get("type") == "acknowledged_unknown"]
    assert items[0]["id"] == "UNKNOWN-002"           # existing iteration-based id preserved
    assert items[0]["iteration"] == 2
    assert items[0]["gap_context"] == "Assumption Inventory"
    assert items[0]["source"] == "inventor_stated"
    assert pkg["section_8_unresolved_items"]["acknowledged_unknown_count"] == 2


def test_every_section8_reference_resolves_to_a_registry_entry():
    pkg = assemble_deliverable(_state())
    reg_ids = {e["unknown_id"] for e in _registry(pkg)}
    for i in pkg["section_8_unresolved_items"]["items"]:
        if i.get("type") == "acknowledged_unknown":
            assert i["unknown_id"] in reg_ids, f"dangling reference: {i['unknown_id']}"


def test_full_unknown_text_once_in_section5_not_section8():
    pkg = assemble_deliverable(_state())
    s5 = json.dumps(pkg["section_5_assumptions"])
    s8 = json.dumps(pkg["section_8_unresolved_items"])
    assert UNK1 in s5 and UNK1 not in s8
    assert UNK2 in s5 and UNK2 not in s8


# --- contract + phase 3A non-regression -------------------------------------

def test_top_level_canonical_contract_unchanged():
    pkg = assemble_deliverable(_state())
    assert set(pkg) == TOP_LEVEL_ENVELOPE | CANONICAL_SECTIONS | {"_session_meta"}


def test_evidence_registry_and_ev_ids_untouched():
    # Phase 3A registry stays a separate list containing only EV ids.
    pkg = assemble_deliverable(_state())
    ev = pkg["_session_meta"]["evidence_registry"]
    ev_ids = {e["evidence_id"] for e in ev}
    assert ev_ids == {"EV-001", "EV-002"}
    # no unknown leaked into the evidence registry
    assert all("unknown_id" not in e for e in ev)
    reqs = pkg["section_4_requirements"]["requirements"]
    assert reqs[0]["statement"] == "See EV-001 — Known Problem"


# --- sections 10 / 11 intentionally unchanged by 3B-1 -----------------------

def test_section_11_still_carries_unknown_text_this_phase():
    # 3B-1 scope was Section 5 + Section 8. Section 10 was later de-duplicated in
    # Phase 3B-2a (it now references UNK ids, not the verbatim). Phase 3B-2b then
    # changed only Section 11's user-facing "Based on:" display to a UNK reference;
    # the full verbatim is still retained in the section_11 data (traceability
    # content and the identity source), so it remains present in this JSON dump.
    pkg = assemble_deliverable(_state())
    s10 = json.dumps(pkg["section_10_recommended_next_steps"])
    s11 = json.dumps(pkg["section_11_prototype_test_plan"])
    assert UNK1 not in s10          # Phase 3B-2a: Section 10 now references UNK ids
    assert UNK1 in s11              # Section 11 data still carries the verbatim (traceability)


# --- rendering --------------------------------------------------------------

def test_section5_renders_visible_unknown_ids_and_full_text():
    sid = "unk-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": _state(), "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "(UNK-001)" in body and "(UNK-002)" in body     # visible ids in Section 5
        assert UNK1 in body and UNK2 in body                   # full text still visible
        assert "See UNK-001 — Acknowledged unknown" in body    # Section 8 reference
        assert "See UNK-002 — Acknowledged unknown" in body
        # honest warnings preserved
        assert "Derived readiness" in body
        assert "not technically verified" in body
    finally:
        SESSION_STORE.pop(sid, None)
