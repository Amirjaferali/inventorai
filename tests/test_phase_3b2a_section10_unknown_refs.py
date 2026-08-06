"""Phase 3B-2a — Section 10 (Recommended Next Steps) unknown-reference dedup.

Section 10 previously repeated the full acknowledged-unknown verbatim inside each
"Resolve the inventor-stated unknown: <verbatim>" action. It now references the
unknown registry (UNK-00N, position-based to match Section 5/8) instead. The full
verbatim is no longer repeated in Section 10; every reference resolves to a
registry entry; dedup, NEXT-00N numbering, priority, and the governance basis are
preserved. Sections 5, 8, 11 and Section 13 criticality are unchanged.
"""
import json, os, sys, uuid
import re
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState, Evidence, REASONED, AcknowledgedUnknown

U1 = "sensor reliability on real animals is unknown - will readings stay accurate on a moving, hairy animal?"
U2 = "collar position, comfort and safety on the animal over long periods is unknown"
U3 = "battery life under real field conditions is unknown"


def _state(unknowns=(U1, U2, U3)):
    s = IdeaState(idea_id="p3b2a-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.current_stage = 3
    s.idea_summary = "A livestock health monitoring collar."
    s.known_problem = Evidence("Delivered animals fall ill undetected.", REASONED, 1)
    s.known_mechanism = Evidence("A microcontroller reads sensors and alerts the farmer.", REASONED, 2)
    s.acknowledged_unknowns = [AcknowledgedUnknown(i + 1, "ASSUMPTION_INVENTORY", u, "reasoned")
                               for i, u in enumerate(unknowns)]
    return s


def _s10(pkg):
    return pkg["section_10_recommended_next_steps"]["items"]


def _unknown_steps(pkg):
    return [st for st in _s10(pkg) if "Acknowledged unknown" in st["action"]]


def _reg_ids(pkg):
    return {e["unknown_id"] for e in pkg["_session_meta"]["unknown_registry"]}


# --- references replace verbatim --------------------------------------------

def test_section10_uses_unk_references_not_full_verbatim():
    pkg = assemble_deliverable(_state())
    steps = _unknown_steps(pkg)
    assert steps, "expected acknowledged-unknown next steps"
    for st in steps:
        assert "See UNK-" in st["action"]
        assert "Acknowledged unknown" in st["action"]


def test_full_unknown_text_not_in_section10():
    pkg = assemble_deliverable(_state())
    blob = json.dumps(pkg["section_10_recommended_next_steps"])
    for u in (U1, U2, U3):
        assert u not in blob


def test_every_section10_unk_reference_resolves_to_registry():
    pkg = assemble_deliverable(_state())
    reg = _reg_ids(pkg)
    for st in _unknown_steps(pkg):
        uid = re.search(r"UNK-\d{3}", st["action"]).group()
        assert uid in reg, f"dangling reference: {uid}"


def test_reference_ids_are_position_based_matching_sections_5_8():
    pkg = assemble_deliverable(_state())
    ids = [re.search(r"UNK-\d{3}", st["action"]).group() for st in _unknown_steps(pkg)]
    assert ids == ["UNK-001", "UNK-002", "UNK-003"]


# --- dedup / numbering / metadata preserved ---------------------------------

def test_duplicate_unknown_does_not_create_duplicate_action():
    # positions 0 and 1 share verbatim -> one action, referencing the first id.
    pkg = assemble_deliverable(_state(unknowns=("X repeated", "X repeated", "Y other")))
    steps = _unknown_steps(pkg)
    assert len(steps) == 2
    ids = [re.search(r"UNK-\d{3}", st["action"]).group() for st in steps]
    assert ids == ["UNK-001", "UNK-003"]           # dup UNK-002 collapsed; first id kept
    # all three unknowns are still registered (registry is not de-duplicated)
    assert _reg_ids(pkg) == {"UNK-001", "UNK-002", "UNK-003"}
    for uid in ids:
        assert uid in _reg_ids(pkg)


def test_next_numbering_priority_and_basis_preserved():
    pkg = assemble_deliverable(_state())
    all_steps = _s10(pkg)
    # contiguous NEXT-00N numbering across the whole section
    assert [st["id"] for st in all_steps] == [f"NEXT-{i+1:03d}" for i in range(len(all_steps))]
    for i, st in enumerate(_unknown_steps(pkg)):
        assert st["priority"] == "normal"
        assert st["basis"] == f"acknowledged_unknown:iteration_{i+1}"


# --- other sections unchanged -----------------------------------------------

def test_sections_5_and_8_unchanged():
    pkg = assemble_deliverable(_state())
    # Section 5 still shows full verbatim once, with UNK ids
    s5 = pkg["section_5_assumptions"]["inventor_unknowns"]
    assert [u["unknown_id"] for u in s5] == ["UNK-001", "UNK-002", "UNK-003"]
    assert s5[0]["statement"] == U1
    # Section 8 still references UNK ids (not full text)
    s8 = [i for i in pkg["section_8_unresolved_items"]["items"]
          if i.get("type") == "acknowledged_unknown"]
    assert s8[0]["statement"] == "See UNK-001 — Acknowledged unknown"
    assert U1 not in json.dumps(pkg["section_8_unresolved_items"])


def test_section_11_unchanged_still_has_verbatim_this_phase():
    pkg = assemble_deliverable(_state())
    assert U1 in json.dumps(pkg["section_11_prototype_test_plan"])


def test_section_13_criticality_unchanged():
    pkg = assemble_deliverable(_state())
    for r in pkg["section_13_requirement_landscape"]["requirements"]:
        assert r["criticality"] == "UNDETERMINED"
        assert r["criticality_authority"] == "system-derived"


def test_contract_and_advisory_note_intact():
    pkg = assemble_deliverable(_state())
    assert len([k for k in pkg if k.startswith("section_")]) == 14
    note = pkg["section_10_recommended_next_steps"]["note"]
    assert "Advisory only" in note
