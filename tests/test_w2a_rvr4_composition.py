"""W2-A / RVR-4 — deterministic decision composition (frozen contract §5/§7/§9).

Covers RVR4-ID-1..8, RVR4-DET-1..3, AA-9 seed suppression / decision-question
injection, empty-by-construction surfaces, and default-constructor
preservation. The composed FDC-001 `DecisionRecord` is a pure derived
projection of the final amended active ledger — no uuid, no timestamp, no
seeded bicycle content, no second canonical model.
"""
import json
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.idea_state import (
    IdeaState,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
)
from engine.decision_workspace import (
    DecisionRecord, CANDIDATE_NAMES, DECISION_QUESTION,
    INSUFFICIENT_INFORMATION,
)
from engine.decision_composition import (
    compose_decision_records, declare_decision_context, declare_alternative,
    refine_alternative, withdraw_alternative,
)
from engine.record_contract import ProjectRecordContract

CTX = DISPOSITION_DECISION_CONTEXT_DECLARED
ALT = DISPOSITION_DECISION_ALTERNATIVE_DECLARED
WDR = DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN


def _dump(rec):
    return json.dumps(rec.to_record_dict(), sort_keys=True)


def _build():
    s = IdeaState(idea_id="pid-1")
    ctx = declare_decision_context(s, "Which latch mechanism should hold it?")
    a1 = declare_alternative(s, "Toggle latch", ctx.record_id)
    a2 = declare_alternative(s, "Spring pin", ctx.record_id)
    return s, ctx, a1, a2


# --- RVR4-ID-1: plural contexts compose independently ------------------------

def test_id1_plural_contexts():
    s, ctx, a1, a2 = _build()
    ctx2 = declare_decision_context(s, "Which battery chemistry?")
    declare_alternative(s, "LiFePO4", ctx2.record_id)
    recs = compose_decision_records(s)
    assert [r.decision_id for r in recs] == [
        f"decision-pn-pid-1-{ctx.record_id}",
        f"decision-pn-pid-1-{ctx2.record_id}"]
    assert len(recs[0].candidates) == 2 and len(recs[1].candidates) == 1


# --- RVR4-ID-2/3: stable roots and ids across reconstruction -----------------

def test_id2_id3_identity_stable_across_contract_reconstruction():
    s, ctx, a1, a2 = _build()
    live = [_dump(r) for r in compose_decision_records(s)]
    restored = ProjectRecordContract.from_dict(
        ProjectRecordContract.from_state(s).to_dict()).to_state()
    cold = [_dump(r) for r in compose_decision_records(restored)]
    assert cold == live


# --- RVR4-ID-4: refinement preserves identity --------------------------------

def test_id4_refinement_preserves_candidate_identity():
    s, ctx, a1, a2 = _build()
    before = compose_decision_records(s)[0]
    refine_alternative(s, "Toggle latch with locking spring", a1.record_id)
    after = compose_decision_records(s)[0]
    ids_before = [c.candidate_id for c in before.candidates]
    ids_after = [c.candidate_id for c in after.candidates]
    assert ids_before == ids_after                       # identity preserved
    refined = [c for c in after.candidates
               if c.candidate_id == f"cand-pn-{a1.record_id}"][0]
    assert refined.name == "Toggle latch with locking spring"


# --- RVR4-ID-5: withdrawal + redeclaration renews identity -------------------

def test_id5_withdrawal_and_redeclaration_renews_root():
    s, ctx, a1, a2 = _build()
    withdraw_alternative(s, a1.record_id, "not robust")
    mid = compose_decision_records(s)[0]
    assert [c.candidate_id for c in mid.candidates] == [f"cand-pn-{a2.record_id}"]
    re = declare_alternative(s, "Toggle latch", ctx.record_id)  # same TEXT
    after = compose_decision_records(s)[0]
    ids = [c.candidate_id for c in after.candidates]
    assert f"cand-pn-{re.record_id}" in ids               # NEW root
    assert f"cand-pn-{a1.record_id}" not in ids           # old root never reused
    # ledger history is retained (nothing deleted)
    assert any(r.record_id == a1.record_id for r in s.assertions)
    assert any(r.disposition == WDR for r in s.assertions)


# --- RVR4-ID-6 / DET-3: insertion-order independence + deterministic order ---

def test_id6_insertion_order_independent_projection():
    s, ctx, a1, a2 = _build()
    live = [_dump(r) for r in compose_decision_records(s)]
    shuffled = IdeaState(idea_id="pid-1")
    shuffled.assertions = list(reversed(s.assertions))
    assert [_dump(r) for r in compose_decision_records(shuffled)] == live


def test_det3_candidates_ordered_by_numeric_root():
    s, ctx, a1, a2 = _build()
    withdraw_alternative(s, a1.record_id)
    re = declare_alternative(s, "Re-declared toggle", ctx.record_id)
    rec = compose_decision_records(s)[0]
    roots = [int(c.candidate_id.rsplit("_", 1)[-1]) for c in rec.candidates]
    assert roots == sorted(roots)
    assert rec.candidates[0].candidate_id == f"cand-pn-{a2.record_id}"
    assert rec.candidates[-1].candidate_id == f"cand-pn-{re.record_id}"


# --- RVR4-ID-7: cross-project non-collision ----------------------------------

def test_id7_project_qualified_ids():
    s1, ctx1, _, _ = _build()
    s2 = IdeaState(idea_id="pid-2")
    ctx2 = declare_decision_context(s2, "Which latch mechanism should hold it?")
    d1 = compose_decision_records(s1)[0].decision_id
    d2 = compose_decision_records(s2)[0].decision_id
    assert d1 != d2 and d1.startswith("decision-pn-pid-1-")
    assert d2.startswith("decision-pn-pid-2-")


# --- RVR4-ID-8 / DET-2: no uuid / placeholder identity anywhere --------------

def test_id8_det2_no_uuid_or_random_identity_reachable():
    import re as _re
    s, ctx, a1, a2 = _build()
    refine_alternative(s, "better", a1.record_id)
    blob = " ".join(_dump(r) for r in compose_decision_records(s))
    uuid_re = _re.compile(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
    assert not uuid_re.search(blob)
    for rec in compose_decision_records(s):
        assert rec.decision_id == f"decision-pn-pid-1-{ctx.record_id}"
        for c in rec.candidates:
            assert c.candidate_id.startswith("cand-pn-rec_")


# --- RVR4-DET-1: byte-for-byte double composition ----------------------------

def test_det1_double_composition_byte_identical():
    s, *_ = _build()
    one = [_dump(r) for r in compose_decision_records(s)]
    two = [_dump(r) for r in compose_decision_records(s)]
    assert one == two


# --- question injection ------------------------------------------------------

def test_question_from_active_context_head_and_stable_id():
    s, ctx, a1, a2 = _build()
    rec = compose_decision_records(s)[0]
    assert rec.decision_question == "Which latch mechanism should hold it?"
    # refine the context: question follows the head; identity keeps the ROOT
    s.record_interaction(action=CTX, content="Which latch, given cost limits?",
                         supersedes=[ctx.record_id])
    rec2 = compose_decision_records(s)[0]
    assert rec2.decision_question == "Which latch, given cost limits?"
    assert rec2.decision_id == rec.decision_id


# --- AA-9: seed suppression + default preservation ---------------------------

def test_no_seeded_bicycle_content_in_composed_state():
    s, *_ = _build()
    blob = " ".join(_dump(r) for r in compose_decision_records(s))
    for name in CANDIDATE_NAMES:
        assert name not in blob
    assert DECISION_QUESTION not in blob
    assert "brake" not in blob.lower()


def test_default_constructor_behavior_preserved():
    rec = DecisionRecord()
    assert rec.decision_question == DECISION_QUESTION
    assert [c.name for c in rec.candidates] == list(CANDIDATE_NAMES)
    assert len(rec.inputs) == 3 and len(rec.gaps) == 2   # seeded owner context


# --- empty-by-construction surfaces + truthful readiness ---------------------

def test_empty_surfaces_and_truthful_readiness():
    s, *_ = _build()
    d = compose_decision_records(s)[0].to_record_dict()
    for key in ("inputs", "constraints", "gaps", "risks", "evidence",
                "gap_assessments", "history"):
        assert d[key] == []
    assert d["owner_preference"] is None
    assert d["change_impact_summary"] is None
    assert d["revision"] == 0
    assert d["readiness_status"] == INSUFFICIENT_INFORMATION  # truthful, not fabricated


def test_no_contexts_composes_to_empty_list():
    s = IdeaState(idea_id="pid-1")
    s.record_interaction(action="answered", content="a",
                         gap_context="PHYSICAL_FEASIBILITY")
    assert compose_decision_records(s) == []              # no fabricated context
