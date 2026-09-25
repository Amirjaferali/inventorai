"""Provenance Hardening Step 1 — the assertion source / validation boundary.

File-creation contract:
  Path: tests/test_provenance_hardening.py
  Purpose: fix the closed provenance vocabulary and the owner-interaction
    carrier's source, validation and responsibility rules at BOTH boundaries:
    `IdeaState.record_interaction` (mint) and `record_contract.assertion_from_dict`
    (load). Proves the two axes never promote each other, that the engine's own
    Evidence stays OWNER_STATED, that commercial evidence reuses the one
    canonical vocabulary, and that readiness for every currently legal record is
    unchanged.
  Input contract: the committed engine modules; in-memory states only.
  Output contract: pass/fail evidence only.
  Prohibited behaviors: no SYSTEM_INFERRED writer, no validation award, no
    readiness-policy assertion beyond today's unchanged behavior.
"""
import ast
import pathlib

import pytest

from engine import commercial_evidence, idea_state
from engine.decision_composition import declare_alternative, declare_decision_context
from engine.derived_readiness import derive_readiness
from engine.idea_state import (
    ASSERTION_PROVENANCE_VALUES, ASSERTION_RESPONSIBILITY_BY_PROVENANCE,
    DECISION_ACTION_DISPOSITIONS, DISPOSITION_ANSWERED, DISPOSITION_DEFERRED,
    DISPOSITION_EVIDENCE_REQUESTED, DISPOSITION_PROVISIONAL_ASSUMPTION,
    DISPOSITION_RISK_ACCEPTED, DISPOSITION_SPECIALIST_REQUESTED,
    DISPOSITION_UNKNOWN, EMPIRICAL_EVIDENCE, EMPIRICALLY_DEMONSTRATED,
    EXPERT_SUPPLIED, EXTERNAL_EVIDENCE, INDEPENDENTLY_VERIFIED,
    INTERACTION_DISPOSITIONS, IdeaState, LEGACY_UNSPECIFIED,
    MECHANISM_COMPLETENESS, OWNER_INPUT, OWNER_STATED, PROVENANCE_VALUES,
    RESPONSIBILITY_VALUES, SPECIALIST_INPUT, SPECIALIST_REVIEWED, SYSTEM_ANALYSIS,
    SYSTEM_INFERRED, UNDETERMINED, UNVALIDATED, VALIDATED_STATUSES,
    VALIDATION_STATUSES,
)
from engine.record_contract import (
    InvalidProvenanceError, InvalidResponsibilityError,
    InvalidValidationStatusError, assertion_from_dict, assertion_to_dict,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]

LEGACY_DISPOSITIONS = sorted(INTERACTION_DISPOSITIONS - DECISION_ACTION_DISPOSITIONS)
OWNER_ASSERTING = {DISPOSITION_ANSWERED, DISPOSITION_PROVISIONAL_ASSUMPTION,
                   DISPOSITION_RISK_ACCEPTED} | DECISION_ACTION_DISPOSITIONS
NON_OWNER_SOURCES = (SYSTEM_INFERRED, EXPERT_SUPPLIED, EXTERNAL_EVIDENCE)


def _mint(action, **kw):
    s = IdeaState(idea_id="ph1")
    return s, s.record_interaction(action=action, content="c",
                                   gap_context=MECHANISM_COMPLETENESS, iteration=1, **kw)


def _payload(**over):
    s, rec = _mint(DISPOSITION_ANSWERED)
    data = assertion_to_dict(rec)
    data.update(over)
    return data


# ─────────────────────────────────────────────────────────────────────────────
# 1–2 — the closed vocabularies
# ─────────────────────────────────────────────────────────────────────────────

def test_canonical_provenance_vocabulary_is_exactly_the_existing_five():
    assert isinstance(PROVENANCE_VALUES, tuple)          # immutable, fixed order
    assert PROVENANCE_VALUES == (OWNER_STATED, SYSTEM_INFERRED, EXPERT_SUPPLIED,
                                 EXTERNAL_EVIDENCE, LEGACY_UNSPECIFIED)
    assert len(set(PROVENANCE_VALUES)) == 5


def test_assertion_carrier_holds_only_owner_and_legacy_sources():
    assert ASSERTION_PROVENANCE_VALUES == frozenset({OWNER_STATED, LEGACY_UNSPECIFIED})
    assert set(ASSERTION_PROVENANCE_VALUES) < set(PROVENANCE_VALUES)
    assert ASSERTION_RESPONSIBILITY_BY_PROVENANCE == {OWNER_STATED: OWNER_INPUT,
                                                      LEGACY_UNSPECIFIED: None}


def test_responsibility_vocabulary_is_the_existing_five():
    assert RESPONSIBILITY_VALUES == frozenset({
        OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED})


# ─────────────────────────────────────────────────────────────────────────────
# 3–6, 10, 13 — the mint boundary
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("action", LEGACY_DISPOSITIONS)
def test_every_legacy_disposition_gets_its_dictated_provenance(action):
    _s, rec = _mint(action)
    expected = OWNER_STATED if action in OWNER_ASSERTING else LEGACY_UNSPECIFIED
    assert rec.provenance == expected
    assert rec.validation_status == UNVALIDATED
    assert rec.responsibility == ASSERTION_RESPONSIBILITY_BY_PROVENANCE[expected]


def test_decision_actions_are_owner_stated():
    s = IdeaState(idea_id="ph1-dec")
    ctx = declare_decision_context(s, "which motor?")
    alt = declare_alternative(s, "stepper", ctx.record_id)
    for rec in (ctx, alt):
        assert rec.provenance == OWNER_STATED and rec.responsibility == OWNER_INPUT
        assert rec.validation_status == UNVALIDATED


@pytest.mark.parametrize("action", LEGACY_DISPOSITIONS)
def test_explicit_provenance_may_only_restate_the_disposition(action):
    dictated = OWNER_STATED if action in OWNER_ASSERTING else LEGACY_UNSPECIFIED
    _s, rec = _mint(action, provenance=dictated)           # restating is allowed
    assert rec.provenance == dictated
    for other in PROVENANCE_VALUES:
        if other == dictated:
            continue
        s = IdeaState(idea_id="ph1")
        with pytest.raises(ValueError):
            s.record_interaction(action=action, content="c", iteration=1,
                                 gap_context=MECHANISM_COMPLETENESS, provenance=other)
        assert s.assertions == [], (action, other)


@pytest.mark.parametrize("source", NON_OWNER_SOURCES)
@pytest.mark.parametrize("action", sorted(INTERACTION_DISPOSITIONS))
def test_non_owner_sources_can_never_be_minted(action, source):
    s = IdeaState(idea_id="ph1")
    with pytest.raises(ValueError):
        s.record_interaction(action=action, content="c", iteration=1, provenance=source)
    assert s.assertions == []


@pytest.mark.parametrize("value", ["OWNER", "owner_stated", "", " OWNER_STATED", 7, ["x"]])
def test_arbitrary_provenance_fails_at_mint(value):
    s = IdeaState(idea_id="ph1")
    with pytest.raises(ValueError):
        s.record_interaction(action=DISPOSITION_ANSWERED, content="c", iteration=1,
                             provenance=value)
    assert s.assertions == []


@pytest.mark.parametrize("status", sorted(VALIDATED_STATUSES) + ["MADE_UP", None])
def test_the_owner_seam_mints_unvalidated_only(status):
    s = IdeaState(idea_id="ph1")
    with pytest.raises(ValueError):
        s.record_interaction(action=DISPOSITION_ANSWERED, content="c", iteration=1,
                             validation_status=status)
    assert s.assertions == []
    _s, rec = _mint(DISPOSITION_ANSWERED, validation_status=UNVALIDATED)
    assert rec.validation_status == UNVALIDATED


@pytest.mark.parametrize("action,responsibility", [
    (DISPOSITION_ANSWERED, SYSTEM_ANALYSIS), (DISPOSITION_ANSWERED, SPECIALIST_INPUT),
    (DISPOSITION_ANSWERED, UNDETERMINED), (DISPOSITION_PROVISIONAL_ASSUMPTION, EMPIRICAL_EVIDENCE),
    (DISPOSITION_UNKNOWN, OWNER_INPUT), (DISPOSITION_SPECIALIST_REQUESTED, SPECIALIST_INPUT),
    (DISPOSITION_EVIDENCE_REQUESTED, EMPIRICAL_EVIDENCE), (DISPOSITION_ANSWERED, "NOT_A_TOKEN"),
])
def test_responsibility_cannot_contradict_the_carrier_at_mint(action, responsibility):
    s = IdeaState(idea_id="ph1")
    with pytest.raises(ValueError):
        s.record_interaction(action=action, content="c", iteration=1,
                             responsibility=responsibility)
    assert s.assertions == []


def test_responsibility_is_never_inferred_from_provenance():
    for action in LEGACY_DISPOSITIONS:
        _s, rec = _mint(action)
        assert rec.responsibility in (OWNER_INPUT, None)
        assert rec.responsibility not in (SYSTEM_ANALYSIS, SPECIALIST_INPUT,
                                          EMPIRICAL_EVIDENCE, UNDETERMINED)
    _s, rec = _mint(DISPOSITION_ANSWERED, responsibility=OWNER_INPUT)   # restating
    assert rec.responsibility == OWNER_INPUT


# ─────────────────────────────────────────────────────────────────────────────
# 7–9, 11–13 — the load boundary
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("value", ["OWNER", "owner_stated", "", "MARKET_PROOF",
                                   None, 7, ["OWNER_STATED"], {"x": 1}])
def test_invalid_provenance_fails_closed_at_load(value):
    with pytest.raises(InvalidProvenanceError) as err:
        assertion_from_dict(_payload(provenance=value))
    assert "MARKET_PROOF" not in str(err.value)        # the stored value is never echoed


@pytest.mark.parametrize("source", NON_OWNER_SOURCES)
def test_canonical_but_non_owner_provenance_is_refused_by_this_carrier(source):
    with pytest.raises(InvalidProvenanceError):
        assertion_from_dict(_payload(provenance=source, responsibility=None))


@pytest.mark.parametrize("action", LEGACY_DISPOSITIONS)
def test_every_legal_minted_record_round_trips_verbatim(action):
    _s, rec = _mint(action)
    data = assertion_to_dict(rec)
    back = assertion_from_dict(dict(data))
    assert assertion_to_dict(back) == data
    assert back.provenance == rec.provenance and back.responsibility == rec.responsibility


def test_legacy_answered_record_still_loads():
    """History written before provenance defaults (answered + LEGACY) is a
    truthful legacy state: the loader keeps it verbatim, it is never coerced."""
    back = assertion_from_dict(_payload(provenance=LEGACY_UNSPECIFIED, responsibility=None))
    assert back.provenance == LEGACY_UNSPECIFIED and back.responsibility is None


@pytest.mark.parametrize("status", sorted(VALIDATION_STATUSES))
def test_every_canonical_validation_status_stays_loadable(status):
    back = assertion_from_dict(_payload(validation_status=status))
    assert back.validation_status == status
    assert back.provenance == OWNER_STATED            # validation never rewrites source


@pytest.mark.parametrize("status", ["VERIFIED", "", None, 3])
def test_invalid_validation_status_still_fails_closed(status):
    with pytest.raises(InvalidValidationStatusError):
        assertion_from_dict(_payload(validation_status=status))


@pytest.mark.parametrize("provenance,responsibility", [
    (OWNER_STATED, None), (OWNER_STATED, SYSTEM_ANALYSIS), (OWNER_STATED, UNDETERMINED),
    (LEGACY_UNSPECIFIED, OWNER_INPUT), (LEGACY_UNSPECIFIED, SPECIALIST_INPUT),
    (OWNER_STATED, 5), (OWNER_STATED, ["OWNER_INPUT"]),
])
def test_contradictory_responsibility_fails_closed_at_load(provenance, responsibility):
    with pytest.raises(InvalidResponsibilityError):
        assertion_from_dict(_payload(provenance=provenance, responsibility=responsibility))


# ─────────────────────────────────────────────────────────────────────────────
# 14 — commercial evidence reuses the one canonical vocabulary
# ─────────────────────────────────────────────────────────────────────────────

def test_commercial_evidence_reuses_the_canonical_vocabulary():
    assert commercial_evidence.PROVENANCE_VALUES is idea_state.PROVENANCE_VALUES
    assert commercial_evidence.DEFAULT_PROVENANCE == OWNER_STATED
    source = (ROOT / "engine" / "commercial_evidence.py").read_text(encoding="utf-8")
    assert "SYSTEM_INFERRED" not in source and "EXPERT_SUPPLIED" not in source


# ─────────────────────────────────────────────────────────────────────────────
# 15 — the deterministic engine's own Evidence stays OWNER_STATED
# ─────────────────────────────────────────────────────────────────────────────

def test_every_engine_evidence_construction_is_owner_stated():
    tree = ast.parse((ROOT / "engine" / "progression_loop.py").read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "Evidence"]
    assert calls, "precondition: the engine mints Evidence"
    for call in calls:
        kw = {k.arg: k.value for k in call.keywords}
        assert getattr(kw.get("provenance"), "id", None) == "OWNER_STATED", call.lineno
        assert "validation_status" not in kw, call.lineno


def test_engine_evidence_from_a_real_journey_is_owner_stated_and_unvalidated():
    from engine.progression_loop import run_iteration
    s = IdeaState(idea_id="ph1-journey")
    s.domain = "electronics_electrical"
    run_iteration(s, "Cyclists have no reliable brake light, because the sensor "
                     "voltage changes when braking, so riders behind need warning.")
    run_iteration(s, "The mechanism works because the accelerometer outputs a voltage "
                     "proportional to deceleration; the microcontroller reads it through "
                     "the ADC and drives the LED through a transistor.")
    evidence = [e for e in (s.known_problem, s.known_mechanism) if e is not None]
    evidence += [e for g in s.gaps for e in g.evidence]
    assert evidence, "precondition: the journey produced engine Evidence"
    for e in evidence:
        assert e.provenance == OWNER_STATED
        assert e.validation_status == UNVALIDATED


# ─────────────────────────────────────────────────────────────────────────────
# 16 — no cross-promotion between source and validation
# ─────────────────────────────────────────────────────────────────────────────

def test_the_two_axes_share_no_value():
    assert not set(PROVENANCE_VALUES) & set(VALIDATION_STATUSES)
    assert SYSTEM_INFERRED not in VALIDATED_STATUSES        # SYSTEM_INFERRED != validated
    assert EXPERT_SUPPLIED != SPECIALIST_REVIEWED
    assert EXTERNAL_EVIDENCE not in (EMPIRICALLY_DEMONSTRATED, INDEPENDENTLY_VERIFIED)


def test_owner_stated_is_not_true_and_requests_are_not_results():
    _s, answered = _mint(DISPOSITION_ANSWERED)
    assert answered.provenance == OWNER_STATED
    assert answered.validation_status == UNVALIDATED       # OWNER_STATED != true
    _s, spec = _mint(DISPOSITION_SPECIALIST_REQUESTED)
    assert spec.pending == "specialist"                    # requested, not reviewed
    assert spec.validation_status != SPECIALIST_REVIEWED
    _s, evid = _mint(DISPOSITION_EVIDENCE_REQUESTED)
    assert evid.pending == "evidence"                      # requested, not existing
    assert evid.provenance != EXTERNAL_EVIDENCE
    assert evid.validation_status not in VALIDATED_STATUSES


def test_loading_never_moves_one_axis_from_the_other():
    for status in VALIDATION_STATUSES:
        for prov in ASSERTION_PROVENANCE_VALUES:
            back = assertion_from_dict(_payload(
                provenance=prov, validation_status=status,
                responsibility=ASSERTION_RESPONSIBILITY_BY_PROVENANCE[prov]))
            assert (back.provenance, back.validation_status) == (prov, status)


# ─────────────────────────────────────────────────────────────────────────────
# 17 — readiness for currently legal records is unchanged
# ─────────────────────────────────────────────────────────────────────────────

def test_readiness_for_legal_records_is_unchanged():
    s = IdeaState(idea_id="ph1-ready")
    s.record_interaction(action=DISPOSITION_ANSWERED, content="5V",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    ready = derive_readiness(s)
    assert ready.is_verified(MECHANISM_COMPLETENESS) is False   # owner-unvalidated
    assert ready.overall_verified() is False
    s.record_interaction(action=DISPOSITION_DEFERRED, content="later",
                         gap_context=MECHANISM_COMPLETENESS, iteration=2)
    assert derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    # a future writer's validated record (modelled in memory, as the readiness
    # suites already do) is still evaluated exactly as before
    t = IdeaState(idea_id="ph1-ready-2")
    rec = t.record_interaction(action=DISPOSITION_ANSWERED, content="5V",
                               gap_context=MECHANISM_COMPLETENESS, iteration=1)
    rec.validation_status = INDEPENDENTLY_VERIFIED
    assert derive_readiness(t).is_verified(MECHANISM_COMPLETENESS) is True
