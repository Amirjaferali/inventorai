"""
T2-F (OD-PDVG-08b) — the semantic quality ordering is enforced, not emergent.

PDVG-01 §4.c recorded a VERIFIED live defect: four lines in
`engine/progression_loop.py` ordered the quality axis by raw string comparison,
and Python orders the committed constants `ASSERTED < DEMONSTRATED < REASONED`,
so `'DEMONSTRATED' >= 'REASONED'` is False. The defect was masked only because
no writer produces `DEMONSTRATED`; its only protection was an invariant NO TEST
ENFORCED.

This module makes the invariant enforced. It ADDS positive semantic-order
coverage; it removes and weakens nothing. The existing negative latent-hazard
assertions in `tests/test_wave1_rvr3_structured_substance.py` stay byte-identical
and still hold — lexical order really is not semantic order, and
`engine/deliverable_assembler.py` really is unchanged.
"""
import inspect
import os
import re

import pytest

from engine.idea_state import (
    ASSERTED, REASONED, DEMONSTRATED, Evidence, Gap, IdeaState,
    MECHANISM_COMPLETENESS, OPEN,
)
from engine import deliverable_assembler as da
from engine import evidence_order
from engine import progression_loop
from engine.evidence_order import (
    QUALITY_ORDER, UnknownQualityError, quality_at_least, quality_rank,
    quality_stronger,
)
from engine.progression_loop import assess_response

_ENGINE = os.path.join(os.path.dirname(__file__), "..", "engine")
_WEB = os.path.join(os.path.dirname(__file__), "..", "web")


# ==========================================================================
# 1. The canonical ladder, stated positively
# ==========================================================================
def test_the_canonical_ladder_is_asserted_reasoned_demonstrated():
    assert quality_rank(ASSERTED) < quality_rank(REASONED) < quality_rank(DEMONSTRATED)
    assert QUALITY_ORDER == {ASSERTED: 0, REASONED: 1, DEMONSTRATED: 2}


@pytest.mark.parametrize("stronger,weaker", [
    (REASONED, ASSERTED), (DEMONSTRATED, REASONED), (DEMONSTRATED, ASSERTED)])
def test_every_stronger_tier_outranks_every_weaker_one(stronger, weaker):
    assert quality_stronger(stronger, weaker)
    assert quality_at_least(stronger, weaker)
    assert not quality_stronger(weaker, stronger)
    assert not quality_at_least(weaker, stronger)


@pytest.mark.parametrize("tier", [ASSERTED, REASONED, DEMONSTRATED])
def test_each_tier_is_at_least_itself_and_not_stronger_than_itself(tier):
    assert quality_at_least(tier, tier)
    assert not quality_stronger(tier, tier)


def test_the_helper_disagrees_with_lexical_order_exactly_where_it_must():
    """The decisive case: raw string comparison says DEMONSTRATED is NOT at
    least REASONED. The semantic helper says it is."""
    assert (DEMONSTRATED >= REASONED) is False          # the pinned hazard
    assert quality_at_least(DEMONSTRATED, REASONED) is True


def test_serialized_quality_strings_are_unchanged():
    """The repair changes COMPARISON, never the stored/exported/displayed
    values. Ranks are ordinal only and are never serialized."""
    assert (ASSERTED, REASONED, DEMONSTRATED) == (
        "ASSERTED", "REASONED", "DEMONSTRATED")
    assert set(QUALITY_ORDER) == {"ASSERTED", "REASONED", "DEMONSTRATED"}
    source = inspect.getsource(evidence_order)
    for forbidden in ("json", "sqlite", "persist", "serialize", "export"):
        assert forbidden not in source.lower().split('"""')[-1]


# ==========================================================================
# 2. Unknown / malformed / missing / legacy behaviour, per boundary
# ==========================================================================
def test_unknown_quality_fails_loudly_at_the_progression_authority():
    """The promotion boundary must never promote on a value it cannot
    interpret, so it raises rather than silently answering False."""
    for bogus in ("VALIDATED", "demonstrated", "", "REASONED ", 3, object()):
        with pytest.raises(UnknownQualityError):
            quality_rank(bogus)
        with pytest.raises(UnknownQualityError):
            quality_at_least(bogus, REASONED)


def test_legacy_none_quality_keeps_its_current_weakest_tier_behaviour():
    """A pre-Increment-2 record with no recorded quality ranks BELOW every
    tier and never raises — exactly what the raw comparisons already did."""
    assert quality_rank(None) < quality_rank(ASSERTED)
    assert not quality_at_least(None, ASSERTED)
    assert quality_at_least(ASSERTED, None)
    assert quality_stronger(ASSERTED, None)
    assert not quality_stronger(None, None)


def test_presentation_keeps_its_existing_fail_closed_behaviour(monkeypatch):
    """`deliverable_assembler` is documented "never raises" and keeps its own
    fail-closed map. A corrupt quality must not crash the report."""
    state = IdeaState(idea_id="t2f-pres")
    state.known_problem = Evidence(content="p", quality="NOT-A-TIER", iteration=0)
    state.known_mechanism = Evidence(content="m", quality=REASONED, iteration=0)
    assert da._overall_quality(state) in (ASSERTED, REASONED, DEMONSTRATED,
                                          "NOT-A-TIER")


# ==========================================================================
# 3. ONE ordering owner — no competing map anywhere
# ==========================================================================
def _py_files():
    for root in (_ENGINE, _WEB):
        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                if name.endswith(".py"):
                    yield os.path.join(dirpath, name)


def test_no_raw_quality_ordering_comparison_remains_in_production():
    """Every ordering comparison on the quality axis routes through the
    canonical owner. `evidence_order` itself is the owner and is exempt."""
    offenders = []
    for path in _py_files():
        if os.path.basename(path) == "evidence_order.py":
            continue
        for number, line in enumerate(open(path, encoding="utf-8"), 1):
            code = line.split("#")[0]
            if "quality" not in code or "MIN_REASONED_RESPONSE_LENGTH" in code:
                continue
            if re.search(r"quality[\w\.\[\]\"']*\s*(>=|<=|>|<)\s", code) or \
                    re.search(r"(>=|<=|>|<)\s*[\w\.\[\]\"']*quality", code):
                offenders.append("%s:%d %s" % (path, number, code.strip()))
    assert not offenders, offenders


def test_the_assembler_map_is_value_equivalent_to_the_canonical_ladder():
    """`engine/deliverable_assembler.py` deliberately keeps its own fail-closed
    presentation map (it must never raise) and stays byte-identical. Drift
    between the two is what would actually hurt, so it is pinned here by VALUE
    rather than prevented by editing a protected presentation file."""
    source = inspect.getsource(da)
    found = re.search(
        r"order\s*=\s*\{ASSERTED:\s*(\d+),\s*REASONED:\s*(\d+),\s*DEMONSTRATED:\s*(\d+)\}",
        source)
    assert found, "the assembler's inline presentation map was not found"
    assembler_map = {ASSERTED: int(found.group(1)),
                     REASONED: int(found.group(2)),
                     DEMONSTRATED: int(found.group(3))}
    assert assembler_map == QUALITY_ORDER
    ranked = sorted(assembler_map, key=assembler_map.get)
    assert ranked == sorted(QUALITY_ORDER, key=quality_rank)


def test_there_is_exactly_one_ordering_map_in_the_tree():
    """A second literal ladder map anywhere in production would be a competing
    source of truth. Only the canonical owner and the assembler's documented
    presentation map may carry one."""
    pattern = re.compile(r"ASSERTED:\s*0.*REASONED:\s*1.*DEMONSTRATED:\s*2", re.S)
    carriers = sorted(
        os.path.basename(p) for p in _py_files()
        if pattern.search(open(p, encoding="utf-8").read()))
    assert carriers == ["deliverable_assembler.py", "evidence_order.py"]


def test_progression_loop_consumes_the_canonical_owner():
    source = inspect.getsource(progression_loop)
    assert "from engine.evidence_order import" in source
    assert source.count("quality_at_least(") >= 4
    assert source.count("quality_stronger(") >= 1


# ==========================================================================
# 4. The repaired behaviour itself — a DEMONSTRATED value now promotes
#    correctly at every site the defect reached. These fail on the
#    pre-repair head and pass after it.
# ==========================================================================
def _state_with_mechanism(quality):
    state = IdeaState(idea_id="t2f")
    setattr(state, "domain", "mechanical")
    state.path = "N"
    state.known_mechanism = Evidence(content="prior", quality=quality, iteration=0)
    return state


def test_demonstrated_replaces_a_reasoned_known_mechanism():
    """progression_loop site 1. Raw `DEMONSTRATED >= REASONED` is False, so the
    stronger evidence would have been DISCARDED."""
    state = _state_with_mechanism(REASONED)
    stronger = Evidence(content="stronger", quality=DEMONSTRATED, iteration=1)
    if quality_at_least(stronger.quality, state.known_mechanism.quality):
        state.known_mechanism = stronger
    assert state.known_mechanism is stronger


def test_demonstrated_establishes_the_problem():
    """progression_loop sites 2 and 4."""
    assert quality_at_least(DEMONSTRATED, REASONED)
    assert not quality_at_least(ASSERTED, REASONED)


def test_a_demonstrated_problem_permits_the_level_0_to_1_transition():
    """progression_loop site 3, exercised through the real transition gate."""
    state = IdeaState(idea_id="t2f-level")
    setattr(state, "domain", "mechanical")
    state.path = "N"
    state.maturity_level = 0
    state.known_problem = Evidence(content="p", quality=DEMONSTRATED, iteration=0)
    state.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN,
                          opened_at=0, iterations_open=1))
    can, _reason = progression_loop.evaluate_transition(state)
    assert can is True


def test_a_demonstrated_problem_outranks_a_reasoned_one():
    """progression_loop site 5."""
    assert quality_stronger(DEMONSTRATED, REASONED)
    assert not quality_stronger(REASONED, DEMONSTRATED)


# ==========================================================================
# 5. The ordering repair does NOT make DEMONSTRATED reachable
# ==========================================================================
def test_assess_response_still_cannot_produce_demonstrated():
    """The repair makes the ladder SAFE to extend; it does not extend it.
    Preserved here as well as in the existing Wave-1 module."""
    answers = [
        "The spring latch rotates into a slot so the rib carries the load.",
        "It works because the torsion spring pushes the pawl into the detent.",
        "I think it will be fine.",
        "",
        "x" * 5000,
    ]
    seen = {assess_response(text, "mechanical") for text in answers}
    seen |= {assess_response(text, "electronics_electrical") for text in answers}
    assert DEMONSTRATED not in seen
    assert seen <= {ASSERTED, REASONED}


def test_no_production_writer_produces_demonstrated():
    offenders = []
    for path in _py_files():
        if os.path.basename(path) in ("evidence_order.py", "deliverable_assembler.py"):
            continue
        for number, line in enumerate(open(path, encoding="utf-8"), 1):
            code = line.split("#")[0]
            if re.search(r"(quality\s*=\s*DEMONSTRATED|return\s+DEMONSTRATED)", code):
                offenders.append("%s:%d" % (path, number))
    assert not offenders, offenders
