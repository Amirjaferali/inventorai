"""Wave-1 RVR-3 — deterministic structured-substance assessment (Layer-3),
MG-5 provenance stamp, and the T2-F quality-tier ordering guard.

Contract: docs/governance/WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md (RVR-3).
The frozen S2 R1–R8 recorded answer corpus is reused as REGRESSION FIXTURES
(docs/benchmarks/evidence/s2_run_001/answer_maps.json). This is NOT an S2 rerun.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    IdeaState, ASSERTED, REASONED, DEMONSTRATED, OWNER_STATED,
    LEGACY_UNSPECIFIED, MECHANISM_COMPLETENESS, OPEN, Gap,
)
from engine.progression_loop import (
    assess_response, integrate_response, run_iteration,
    _structured_technical_form,
)

# Byte-identical copy of the frozen S2 run corpus (extracted from the
# preserved run-evidence candidate ebf243db, docs/benchmarks/evidence/
# s2_run_001/answer_maps.json; sha256 recorded in that evidence pack's
# SHA256SUMS.txt). Fixture use only - NOT an S2 rerun.
_CORPUS = os.path.join(os.path.dirname(__file__), "fixtures",
                       "s2_run_001_answer_maps.json")

def _corpus():
    with open(_CORPUS, encoding="utf-8") as fh:
        return json.load(fh)["answers"]

_DOM = {"E-1": "electronics_electrical", "M-1": "mechanical"}

# --- the S2 perspective inversion is repaired --------------------------------

def test_expert_mechanism_closure_answers_reach_reasoned_en_and_ar():
    """The recorded expert MECHANISM answers (the ones that drive
    PARTIAL->CLOSED) assess REASONED in both languages for both cases."""
    answers = _corpus()
    for case in ("E-1", "M-1"):
        for lang in ("en", "ar"):
            corpus = answers[f"{case}|expert|{lang}"]
            for text in corpus["MECHANISM_COMPLETENESS"][:2]:
                q = assess_response(text, _DOM[case])
                assert q == REASONED, (case, lang, text[:60], q)

def test_expert_feasibility_and_boundary_answers_reach_reasoned_en():
    answers = _corpus()
    for case in ("E-1", "M-1"):
        corpus = answers[f"{case}|expert|en"]
        for gap in ("PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"):
            for text in corpus[gap][:1]:
                assert assess_response(text, _DOM[case]) == REASONED, (case, gap)

def test_novice_answers_do_not_regress():
    """Every recorded novice MECHANISM closure answer keeps its live-run
    REASONED assessment."""
    answers = _corpus()
    for case in ("E-1", "M-1"):
        text = answers[f"{case}|novice|en"]["MECHANISM_COMPLETENESS"][0]
        assert assess_response(text, _DOM[case]) == REASONED, case

def test_expert_wording_not_penalized_solely_for_missing_causal_connectors():
    """Wave-1 hard invariant: an enumerated technical answer with zero
    conversational causal substrings is not ASSERTED for that reason alone."""
    t = ("Retention candidates: (1) over-centre toggle latch, (2) "
         "spring-loaded detent pin, (3) gravity-drop gate latch. Constraint: "
         "no permanent doorway modification permitted.")
    assert assess_response(t, "mechanical") == REASONED

# --- the gate stays honest ----------------------------------------------------

def test_weak_and_vague_answers_stay_asserted():
    for t in (
        "It is amazing: (1) cool (2) nice and everyone will want one for sure soon.",
        "My plan: (1) tell my friends (2) sell many of them and get rich quickly.",
        "My design: a state-of-the-art thing with stuff people like a lot honestly.",
        "no idea",
        "something with technology and stuff",
    ):
        assert assess_response(t, "electronics_electrical") == ASSERTED, t[:40]

def test_structured_form_predicate_is_deterministic_and_bounded():
    t = ("Components: (1) a detection stage, (2) an indicator lamp. "
         "Installation constraint: wire-free mounting at the handlebar.")
    assert _structured_technical_form(t.lower()) is True
    assert _structured_technical_form("short: (1) x") is False
    for _ in range(3):
        assert _structured_technical_form(t.lower()) is True

# --- MG-5: rendered provenance == durable provenance -------------------------

def test_evidence_provenance_stamped_owner_stated():
    s = IdeaState(idea_id="x")
    s.domain = "electronics_electrical"
    s.path = "N"
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0))
    text = ("When I brake, the sensor detects it and the light comes on, "
            "which means drivers behind me see that I am slowing down.")
    integrate_response(s, MECHANISM_COMPLETENESS, "q", text)
    assert s.known_mechanism is not None
    assert s.known_mechanism.provenance == OWNER_STATED
    assert s.known_mechanism.provenance != LEGACY_UNSPECIFIED

def test_deliverable_registry_shows_owner_stated_provenance():
    from engine.deliverable_assembler import assemble_deliverable
    s = IdeaState(idea_id="x")
    s.domain = "electronics_electrical"
    s.path = "N"
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0))
    text = ("When I brake, the sensor detects it and the light comes on, "
            "which means drivers behind me see that I am slowing down.")
    integrate_response(s, MECHANISM_COMPLETENESS, "q", text)
    reg = assemble_deliverable(s)["_session_meta"]["evidence_registry"]
    mech = [e for e in reg if e["evidence_id"] == "EV-002"]
    assert mech and "Not recorded" not in mech[0]["provenance"]

# --- T2-F ordering guard (pins the masking invariant; repair stays OD-PDVG-08b)

def test_assess_response_never_returns_demonstrated():
    answers = _corpus()
    seen = set()
    for key, gaps in answers.items():
        case = key.split("|")[0]
        for texts in gaps.values():
            for t in texts:
                seen.add(assess_response(t, _DOM[case]))
    assert DEMONSTRATED not in seen
    assert seen <= {ASSERTED, REASONED}

def test_string_ordering_of_tiers_is_not_semantic_ordering():
    """Pinned fact: Python string comparison of the tier constants does NOT
    implement the semantic ladder (ASSERTED < REASONED < DEMONSTRATED). Any
    future DEMONSTRATED writer must first repair the ordering comparisons
    (OD-PDVG-08b owns that repair); this guard makes the hazard visible
    instead of recognition-dependent."""
    assert (DEMONSTRATED >= REASONED) is False          # the latent hazard
    assert (ASSERTED < DEMONSTRATED < REASONED) is True  # actual string order
    # the canonical numeric order lives inline in deliverable_assembler
    # (order = {ASSERTED: 0, REASONED: 1, DEMONSTRATED: 2}); pin it by source
    # so a silent rewrite of the canonical ladder trips this guard.
    import inspect, engine.deliverable_assembler as da
    src = inspect.getsource(da)
    assert "{ASSERTED: 0, REASONED: 1, DEMONSTRATED: 2}" in src
