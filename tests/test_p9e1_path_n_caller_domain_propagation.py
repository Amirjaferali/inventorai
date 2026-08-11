"""P9-E1 / P9-PREREQ-A — Path-N production caller domain propagation (RED→GREEN).

Authoritative contract:
docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_CONTRACT.md (merged PR #438).

The Path-N selection seam (engine/path_n_questions.py) is already domain-aware
(D3-B): it returns None for a recognized non-electronics domain. P9-E1 closes the
remaining gap — the production callers inside engine/progression_loop.py
(get_question / get_display_question) must PROPAGATE the canonical session domain
they already hold into that seam, instead of relying on the backward-compatible
domain=None default that serves Electronics-owned content to every domain.

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
    return len(variants) + 3


# --------------------------------------------------------- fixture honesty -------
# Incorporates the independent review's non-blocking recommendation: assert the
# foreign fixture is recognized_not_activated (and not activated), so the RED can
# never be mistaken for an activation.
def test_fixture_is_recognized_not_activated():
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

    # RED (pre-fix): the caller drops domain → Electronics artifact text is served.
    assert result != electronics_text
    assert result == generic_text


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

    # RED (pre-fix): the caller drops domain → Electronics exhaustion fires the
    # Electronics stall reframe (or serves Electronics artifact text) for a foreign
    # domain. After propagation → generic fallthrough.
    assert result != progression_loop._STALL_REFRAME
    assert result != electronics_text
    assert result == generic_text


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


# ------------------------------- GREEN guard: None / backward compatibility ------
# The seam's domain=None default (existing external callers) is unchanged: the
# Electronics-owned artifact is still served when no domain is supplied.
def test_green_guard_none_default_backward_compatible():
    gap = _electronics_path_n_gap()
    assert path_n_questions.get_path_n_question(gap, 0) is not None
    assert path_n_questions.get_served_question(gap, 0) is not None
    # And explicit Electronics identity is unchanged.
    assert path_n_questions.get_path_n_question(gap, 0, domain=_ACTIVATED) is not None
