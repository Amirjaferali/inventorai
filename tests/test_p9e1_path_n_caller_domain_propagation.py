"""P9-E1 / P9-PREREQ-A — Path-N production caller domain propagation (RED→GREEN).

Authoritative contract:
docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_CONTRACT.md (merged PR #438).

The Path-N selection seam (engine/path_n_questions.py) is domain-aware (D3-B).
At P9-E1 time it returned None for every recognized non-electronics domain; the
D-GMPR-D3-PN remediation (DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_CONTRACT.md)
later made it a domain-neutral canonical seam serving each mapped domain its OWN
committed artifact (mechanical included), with reconciliations #3/#5 disclosed
in RED1/RED2 below. P9-E1's own subject is unchanged — the production callers
inside engine/progression_loop.py (get_question / get_display_question)
PROPAGATE the canonical session domain they already hold into that seam, instead
of relying on the backward-compatible domain=None default that would serve
Electronics-owned content to every domain.

These tests are BEHAVIORAL: each asserts a concrete selection behavior through the
real production functions (no source inspection, no monkeypatching of the seam).
They consume the CLOSED canonical owner engine/domain_activation.py (§5-I2) to keep
the fixture honest; they never activate a second specialist domain.

Meaning of neutrality (P9-QS / D3): the shared caller path can safely support a
future governed domain WITHOUT serving it Electronics content — NOT "electronics
content is forbidden". Electronics (and the None default) keep their behavior.
"""

import json
from pathlib import Path

from engine import domain_activation
from engine import path_n_questions
from engine import progression_loop

# A recognized-but-NOT-activated valid v1.0 pack (§5-I2): proves propagation
# WITHOUT activating a second specialist domain.
_RECOGNIZED_NOT_ACTIVATED = "mechanical"
_ACTIVATED = "electronics_electrical"


def _electronics_path_n_gap():
    """A gap_type the committed Electronics Path-N artifact maps AND that the
    generic QUESTIONS bank also covers, so a foreign-domain fallthrough resolves to
    a generic variant whose text differs from the Electronics artifact text. Read
    via the committed artifact + the public QUESTIONS map, not a private helper."""
    art = (Path(path_n_questions.__file__).resolve().parent.parent
           / "docs" / "governance" / "path_n_content_config"
           / "electronics_electrical_path_n_questions.json")
    gaps = json.load(open(art, encoding="utf-8"))["gaps"]
    for gap in gaps:
        if gap in progression_loop.QUESTIONS:
            return gap
    raise AssertionError("no artifact gap overlaps the generic QUESTIONS bank")


def _exhaustion_iteration(gap):
    """An iterations_open large enough to clamp past the last Electronics variant,
    so get_display_question's exhaustion comparison (current == previous) is true
    for Electronics → the Electronics stall reframe fires on the baseline."""
    art = (Path(path_n_questions.__file__).resolve().parent.parent
           / "docs" / "governance" / "path_n_content_config"
           / "electronics_electrical_path_n_questions.json")
    variants = json.load(open(art, encoding="utf-8"))["gaps"][gap]
    # Wave-1 RVR-2 reconciliation (WAVE_1_REMEDIATION_IMPLEMENTATION_
    # CONTRACTS.md): the stall reframe is now served exactly ONCE, at the
    # FIRST exhausted render (iterations_open == len(variants), where the
    # current==previous clamp comparison first holds); deeper renders serve
    # the domain-neutral exhausted-exit prompt instead of repeating the
    # reframe. This test's domain-propagation truths are unchanged and are
    # additionally asserted against the deeper renders below.
    return len(variants)


# --------------------------------------------------------- fixture honesty -------
# Incorporates the independent review's non-blocking recommendation: assert the
# foreign fixture is recognized_not_activated (and not activated), so the RED can
# never be mistaken for an activation.
def test_fixture_is_recognized_not_activated(monkeypatch):
    # `_RECOGNIZED_NOT_ACTIVATED = "mechanical"` is kept as-is (other tests in
    # this file rely on mechanical's own committed Path-N artifact); pinned
    # locally to the electronics-only precondition this specific claim needs,
    # since mechanical is now really activated in production (Mechanical
    # Activation Execution Gate).
    monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS",
                         frozenset({_ACTIVATED}))
    assert domain_activation.support_state(_RECOGNIZED_NOT_ACTIVATED) == \
        domain_activation.RECOGNIZED_NOT_ACTIVATED
    assert domain_activation.is_activated(_RECOGNIZED_NOT_ACTIVATED) is False
    assert domain_activation.is_activated(_ACTIVATED) is True
    assert domain_activation.activated_domains() == [_ACTIVATED]


# ------------------------------------------------------------------- RED-1 -------
# get_question: a foreign recognized domain on the Path-N flow must NOT receive
# Electronics Path-N artifact text; it must fall through to the generic variant.
def test_red1_get_question_foreign_domain_not_served_electronics_text():
    gap = _electronics_path_n_gap()
    electronics_text = path_n_questions.get_path_n_question(gap, 0, domain=_ACTIVATED)
    generic_text = progression_loop.QUESTIONS[gap][0]
    assert electronics_text != generic_text, "gap must be distinguishable for a valid RED"

    result = progression_loop.get_question(
        _RECOGNIZED_NOT_ACTIVATED, gap, 0, path="N")

    # D-GMPR-D3-PN reconciliation #5 (disclosed; DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_
    # SERVICE_CONTRACT.md §5): pre-remediation the foreign domain fell through to
    # the generic bank (`result == generic_text`). The domain-neutral canonical
    # seam now serves mechanical its OWN artifact text. BOTH anti-Electronics
    # truths are preserved: never Electronics text, never Electronics content.
    assert result != electronics_text
    mechanical_text = path_n_questions.get_path_n_question(
        gap, 0, domain=_RECOGNIZED_NOT_ACTIVATED)
    assert mechanical_text is not None
    assert result == mechanical_text
    assert result != generic_text


# ------------------------------------------------------------------- RED-2 -------
# get_display_question: at Path-N variant exhaustion, a foreign recognized domain
# must NOT receive the Electronics-specific _STALL_REFRAME; it must fall through to
# the generic variant.
def test_red2_get_display_question_foreign_domain_no_electronics_stall_reframe():
    gap = _electronics_path_n_gap()
    it = _exhaustion_iteration(gap)
    generic_text = progression_loop.QUESTIONS[gap][
        min(it, len(progression_loop.QUESTIONS[gap]) - 1)]
    electronics_text = path_n_questions.get_path_n_question(gap, it, domain=_ACTIVATED)

    result = progression_loop.get_display_question(
        _RECOGNIZED_NOT_ACTIVATED, gap, it, path="N")

    # D-GMPR-D3-PN reconciliation #3 (disclosed; DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_
    # SERVICE_CONTRACT.md §5): pre-remediation the foreign domain was never
    # served, so exhaustion could not fire the reframe and control fell to the
    # generic bank. With mechanical served its OWN artifact, the DOMAIN-NEUTRAL
    # stall reframe now truthfully fires at mechanical variant exhaustion. The
    # anti-Electronics truth is preserved: the result is never Electronics
    # artifact text, and the reframe text itself is domain-neutral (it contains
    # no electronics vocabulary — asserted below), so nothing Electronics-
    # specific is served to a foreign domain.
    assert result == progression_loop._STALL_REFRAME
    assert result != electronics_text
    # RVR-2: deeper exhausted renders serve the domain-neutral exit prompt -
    # still never Electronics artifact text at a foreign domain.
    deeper = progression_loop.get_display_question(
        _RECOGNIZED_NOT_ACTIVATED, gap, it + 3, path="N")
    assert deeper == progression_loop._EXHAUSTED_EXIT_PROMPT
    assert deeper != electronics_text
    assert result != generic_text
    for electronics_only in ("circuit", "electrical", "electronic", "voltage"):
        assert electronics_only not in result.lower()


# ------------------------------------------------- GREEN guard: Electronics ------
# Electronics behavior must be unchanged by the propagation.
def test_green_guard_electronics_artifact_text_preserved():
    gap = _electronics_path_n_gap()
    electronics_text = path_n_questions.get_path_n_question(gap, 0, domain=_ACTIVATED)
    assert progression_loop.get_question(_ACTIVATED, gap, 0, path="N") == electronics_text


def test_green_guard_electronics_stall_reframe_preserved():
    gap = _electronics_path_n_gap()
    it = _exhaustion_iteration(gap)
    # Electronics at exhaustion still gets the deterministic stall reframe.
    assert progression_loop.get_display_question(_ACTIVATED, gap, it, path="N") == \
        progression_loop._STALL_REFRAME
    # RVR-2: past the single reframe render, the exit prompt takes over.
    assert progression_loop.get_display_question(_ACTIVATED, gap, it + 3, path="N") == \
        progression_loop._EXHAUSTED_EXIT_PROMPT


# ------------------------------- GREEN guard: None / backward compatibility ------
# The seam's domain=None default (existing external callers) is unchanged: the
# Electronics-owned artifact is still served when no domain is supplied.
def test_green_guard_none_default_backward_compatible():
    gap = _electronics_path_n_gap()
    assert path_n_questions.get_path_n_question(gap, 0) is not None
    assert path_n_questions.get_served_question(gap, 0) is not None
    # And explicit Electronics identity is unchanged.
    assert path_n_questions.get_path_n_question(gap, 0, domain=_ACTIVATED) is not None
