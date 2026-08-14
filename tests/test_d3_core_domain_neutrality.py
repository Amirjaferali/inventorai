"""D3 — Pre-Phase-9 Core Domain-Neutrality (RED→GREEN).

Authoritative contract: docs/governance/D3_CORE_DOMAIN_NEUTRALITY_FORMAL_CONTRACT.md
(merged PR #434). Behavioral RED-first evidence for the three proven shared-core
couplings, consuming the CLOSED canonical owners engine/domain_registry.py (§5-I1)
and engine/domain_activation.py (§5-I2) — never duplicating them, never activating
a second domain.

Required meaning of neutrality (contract §1): the shared/core architecture can
safely support another governed domain — NOT "electronics content is forbidden".
None of these tests merely checks for the presence/absence of the literal word
"electronics"; each asserts a concrete semantic behavior.
"""

import uuid

import pytest

from engine.idea_state import IdeaState
from engine import safety_signal
from engine import path_n_questions
from engine import domain_rules
from engine import domain_activation

# A recognized-but-NOT-activated valid v1.0 pack (§5-I2): used to prove neutrality
# WITHOUT activating a second specialist domain.
_RECOGNIZED_NOT_ACTIVATED = "mechanical"
_ACTIVATED = "electronics_electrical"


def _state(text, domain):
    s = IdeaState(idea_id=str(uuid.uuid4()))
    s.domain = domain
    s.domain_signal = domain
    s.idea_summary = text
    return s


# Guard: keep the baseline the D3 contract assumes (electronics is the only
# activated specialist domain; the recognized pack is NOT activated).
def test_activation_baseline_preserved():
    assert domain_activation.is_activated(_ACTIVATED) is True
    assert domain_activation.is_activated(_RECOGNIZED_NOT_ACTIVATED) is False


# ---------------------------------------------------------------- D3-A ----------
# A non-electronics canonical domain context that reaches the safety-cue behavior
# must NOT have its SafetySignal.domain_context forced to electronics_electrical.
_TRIGGER = "The battery insulation may malfunction and cause harm."


def test_d3a_non_electronics_domain_context_not_forced_electronics():
    # CF5-F001 reconciliation (corrective contract merged PR #458; disclosed
    # per the F002 precedent): this test's original PRECONDITION — a
    # non-electronics-domain session deriving an electronics-cue signal — was
    # itself the unconditional-exposure defect the F001 correction removes
    # (r2): a domain with no governed safety-cue family now derives NO signals.
    # The LOAD-BEARING D3-A invariant is unchanged and still asserted here: a
    # non-electronics session domain is NEVER force-mapped to an
    # electronics-labeled signal. Post-F001 that holds in the strongest form —
    # no signal exists at all to mislabel — and the electronics/legacy labeling
    # paths keep their own pins (the test below and the CF5-F001 seam suite).
    signals = safety_signal.derive_inventor_stated_safety_signals(
        _state(_TRIGGER, _RECOGNIZED_NOT_ACTIVATED))
    assert signals == ()                       # no family -> nothing derived
    assert not any(s.domain_context == _ACTIVATED for s in signals)


def test_d3a_electronics_domain_context_preserved():
    signals = safety_signal.derive_inventor_stated_safety_signals(
        _state(_TRIGGER, _ACTIVATED))
    assert len(signals) == 1
    assert signals[0].domain_context == _ACTIVATED          # electronics unchanged


# ---------------------------------------------------------------- D3-B ----------
# The shared Path-N selection seam must be CAPABLE of honoring canonical domain
# identity and must not silently serve the Electronics artifact to a non-electronics
# domain. Electronics (and the None default) keep serving Electronics-owned content.
def test_d3b_seam_honors_non_electronics_domain_identity():
    gap = _some_electronics_gap_type()
    # D-GMPR-D3-PN reconciliation #4 (disclosed; DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_
    # SERVICE_CONTRACT.md §5): pre-remediation this pin asserted `served is None`
    # (mechanical received nothing). The domain-neutral canonical seam now serves
    # mechanical its OWN committed artifact. The ORIGINAL LOAD-BEARING TRUTH is
    # preserved in its intended form: a non-electronics recognized domain must
    # NEVER receive ELECTRONICS Path-N content.
    served = path_n_questions.get_served_question(gap, 0, domain=_RECOGNIZED_NOT_ACTIVATED)
    electronics = path_n_questions.get_served_question(gap, 0, domain=_ACTIVATED)
    assert served is not None
    # Mechanical-owned content, never the Electronics entry:
    assert served.question_id.startswith("mechanical:")
    assert served.question_id != electronics.question_id
    assert served.text != electronics.text


def test_d3b_electronics_and_default_preserved():
    gap = _some_electronics_gap_type()
    # Explicit electronics identity → Electronics-owned content (unchanged).
    assert path_n_questions.get_served_question(gap, 0, domain=_ACTIVATED) is not None
    # Backward-compatible default (no domain supplied) → Electronics content unchanged.
    assert path_n_questions.get_served_question(gap, 0) is not None
    assert path_n_questions.get_path_n_question(gap, 0) is not None


def _some_electronics_gap_type():
    """A gap_type that the committed Electronics Path-N artifact maps (so 'served'
    is non-None for electronics). Read via the public seam, not a private helper."""
    import json
    from pathlib import Path
    art = (Path(path_n_questions.__file__).resolve().parent.parent
           / "docs" / "governance" / "path_n_content_config"
           / "electronics_electrical_path_n_questions.json")
    gaps = json.load(open(art, encoding="utf-8"))["gaps"]
    return next(iter(gaps))


# ---------------------------------------------------------------- D3-D ----------
# On a classification tie, a RECOGNIZED_NOT_ACTIVATED domain must NOT outrank the
# ACTIVATED specialist domain through the shared inference seam.
def test_d3d_activated_domain_wins_tie_over_recognized_not_activated():
    # 'circuit' is electronics-only; 'catheter' is medical_device-only → a clean
    # best-score tie between electronics_electrical (ACTIVATED) and medical_device
    # (RECOGNIZED_NOT_ACTIVATED).
    inferred = domain_rules.infer_domain("the circuit and the catheter")
    # RED (pre-fix): the ungoverned priority literal returns medical_device.
    assert inferred == _ACTIVATED
    assert domain_activation.is_activated(inferred) is True


def test_d3d_single_domain_match_unchanged():
    # Only electronics signals present → electronics inferred (unchanged behavior).
    assert domain_rules.infer_domain("a voltage sensor circuit") == _ACTIVATED
    # No signals → None (unchanged behavior).
    assert domain_rules.infer_domain("a nice friendly greeting") is None
