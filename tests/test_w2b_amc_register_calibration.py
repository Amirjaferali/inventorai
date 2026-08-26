"""W2-B / RVR-6a (amended contract) — derived register + W/M calibration.

Authority: W2-B contract §C/§D (PR #573) as amended by Contract Amendment 1
§8 (authoritative via PR #575): W=2/M=2 is the CURRENT OWNER-PERMITTED
PROPOSAL — not accepted, not frozen — and this suite's duty is to ATTEMPT TO
FALSIFY it: the calibration mechanism is actually exercised at bounded
alternative values (W in {1,2,3}, M in {1,2,3}) over adversarial and
realistic sequences, and the comparative claims are asserted from computed
traces, never from the proposed constants (Amendment §8.2 anti-hard-coding
rule).

Register invariants (contract §D, in force): derived, deterministic,
reversible, non-persisted, NEUTRAL floor on insufficient/conflicting
evidence, active/superseded ledger semantics, stored `quality` never
consumed as an answer-local signal.
"""
import copy
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    IdeaState,
    DISPOSITION_ANSWERED, DISPOSITION_UNKNOWN, DISPOSITION_RISK_ACCEPTED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)
from engine.adaptive_register import (
    REGISTER_NEUTRAL, REGISTER_ELEVATED,
    SIGNAL_STRONG, SIGNAL_WEAK, SIGNAL_NONE,
    W_PROPOSED, M_PROPOSED,
    classify_answer_signal, compute_register,
)

# frozen fixture vectors (proven against the pure assessors, [EXEC])
S_TEXT = ("(1) load path: the toggle latch carries the vertical load through "
          "a steel pin rated well above the wheelchair weight. (2) energy: "
          "the ramp is unpowered - no power source or current is required. "
          "(3) operating limits: outdoor temperature range and "
          "repeated-folding fatigue stay within the material limits.")
W_TEXT = "i don't know"
N_TEXT = ("I have not tested whether the toggle latch stays reliable "
          "under repeated loading and outdoor use.")
GAP = PHYSICAL_FEASIBILITY
CONTENT = {"S": S_TEXT, "W": W_TEXT, "N": N_TEXT}


def _build(seq):
    s = IdeaState(idea_id="w2b-cal")
    for ch in seq:
        s.record_interaction(action=DISPOSITION_ANSWERED,
                             content=CONTENT[ch], gap_context=GAP)
    return s


def _trace(seq, w, m):
    """Per-answer register levels (as rendered after each answer), flips
    against the NEUTRAL start, and elevation latency."""
    s = IdeaState(idea_id="w2b-cal")
    levels = []
    for ch in seq:
        s.record_interaction(action=DISPOSITION_ANSWERED,
                             content=CONTENT[ch], gap_context=GAP)
        levels.append(compute_register(s, w=w, m=m).level)
    flips = sum(1 for a, b in zip([REGISTER_NEUTRAL] + levels, levels)
                if a != b)
    first_e = next((i + 1 for i, l in enumerate(levels)
                    if l == REGISTER_ELEVATED), None)
    return levels, flips, first_e


# --- signal classification (contract §D, unchanged authority) ----------------

def test_signal_classification():
    s = IdeaState(idea_id="sig")
    strong = s.record_interaction(action=DISPOSITION_ANSWERED,
                                  content=S_TEXT, gap_context=GAP)
    weak = s.record_interaction(action=DISPOSITION_ANSWERED,
                                content=W_TEXT, gap_context=GAP)
    none_ = s.record_interaction(action=DISPOSITION_ANSWERED,
                                 content=N_TEXT, gap_context=GAP)
    nogap = s.record_interaction(action=DISPOSITION_ANSWERED,
                                 content=S_TEXT, gap_context=None)
    assert classify_answer_signal(strong) == SIGNAL_STRONG
    assert classify_answer_signal(weak) == SIGNAL_WEAK
    assert classify_answer_signal(none_) == SIGNAL_NONE
    assert classify_answer_signal(nogap) == SIGNAL_NONE   # insufficient id


def test_quality_field_never_consumed():
    a, b = IdeaState(idea_id="qa"), IdeaState(idea_id="qb")
    for st, q in ((a, None), (b, "DEMONSTRATED")):
        st.record_interaction(action=DISPOSITION_ANSWERED, content=W_TEXT,
                              gap_context=GAP, quality=q)
        st.record_interaction(action=DISPOSITION_ANSWERED, content=W_TEXT,
                              gap_context=BOUNDARY_AMBIGUITY, quality=q)
    assert compute_register(a) == compute_register(b)
    assert compute_register(b).level == REGISTER_NEUTRAL


def test_non_answer_dispositions_never_contribute():
    s = _build("S")
    s.record_interaction(action=DISPOSITION_UNKNOWN, content=S_TEXT,
                         gap_context=GAP)
    s.record_interaction(action=DISPOSITION_RISK_ACCEPTED, content="",
                         gap_context=GAP)
    reg = compute_register(s)
    assert [rid for rid, _ in reg.contributions] == ["rec_1"]


# --- W falsification: 1 vs 2 vs 3 --------------------------------------------

def test_w1_single_point_flap_is_forbidden_by_constraint():
    """W=1 grants a non-neutral posture from ONE data point — the flap
    OD-R5's hysteresis constraint forbids; hence W >= 2."""
    _, _, e1 = _trace("S", 1, M_PROPOSED)
    _, _, e2 = _trace("S", 2, M_PROPOSED)
    assert e1 == 1 and e2 is None


def test_w3_starves_realistic_mixed_sequences():
    """W=3 never calibrates on ANY of the realistic mixed shapes — the
    starvation consequence is broad, not fixture-bound; W=2 calibrates."""
    for seq in ("SSW", "SSWS", "SSNS", "SSWSSWSSWSSW"):
        _, _, e3 = _trace(seq, 3, 2)
        assert e3 is None, seq
    _, _, e2 = _trace("SSWS", 2, 2)
    assert e2 == 2
    # W=3 is honest on uninterrupted strong runs (fixture-honesty guard)
    _, _, e3s = _trace("SSS", 3, 2)
    assert e3s == 3


def test_elevation_latency_w2():
    _, _, e = _trace("SS", 2, 2)
    assert e == 2
    levels, _, _ = _trace("S", 2, 2)
    assert levels == [REGISTER_NEUTRAL]     # no single-point elevation


# --- M falsification: 1 vs 2 vs 3 --------------------------------------------

def test_m1_churn_overturns_m1():
    """(SSW)x4: M=1 flips the register 8 times in 12 answers (suppression
    toggling with it); M=2 flips once and stays calibrated. This is the
    oscillation evidence that rejected the earlier M=1 proposal."""
    _, flips_m1, _ = _trace("SSWSSWSSWSSW", 2, 1)
    _, flips_m2, _ = _trace("SSWSSWSSWSSW", 2, 2)
    assert flips_m1 == 8
    assert flips_m2 == 1


def test_m2_still_lowers_on_genuine_contrary_run():
    levels, _, _ = _trace("SSWW", 2, 2)
    assert levels[-1] == REGISTER_NEUTRAL      # effective finite lowering
    assert levels[-2] == REGISTER_ELEVATED     # hysteresis held one weak


def test_m3_delays_truthful_lowering():
    """M=3 holds ELEVATED through TWO contrary weak signals — degraded
    truthful lowering; rejected."""
    levels3, _, _ = _trace("SSWW", 2, 3)
    assert levels3[-1] == REGISTER_ELEVATED
    levels_deg, _, _ = _trace("SSWWWW", 2, 3)
    assert levels_deg[3] == REGISTER_ELEVATED  # still elevated after 2 weaks
    assert levels_deg[4] == REGISTER_NEUTRAL   # lowers only at the 3rd


def test_single_noise_stability_on_technical_journey():
    _, flips_m1, _ = _trace("SSSSWSSS", 2, 1)
    _, flips_m2, _ = _trace("SSSSWSSS", 2, 2)
    assert flips_m1 == 3 and flips_m2 == 1


# --- floor / conflict / noise -------------------------------------------------

def test_conflicting_alternation_stays_neutral_all_pairs():
    for w in (2, 3):
        for m in (1, 2, 3):
            levels, flips, _ = _trace("SWSWSW", w, m)
            assert set(levels) == {REGISTER_NEUTRAL} and flips == 0


def test_noise_and_novice_journeys_stay_neutral():
    for seq in ("SNSNS", "NWNNWN"):
        levels, _, _ = _trace(seq, W_PROPOSED, M_PROPOSED)
        assert set(levels) == {REGISTER_NEUTRAL}


def test_none_breaks_run_without_lowering():
    levels, _, _ = _trace("SSN", 2, 2)
    assert levels[-1] == REGISTER_ELEVATED    # NONE is not contrary evidence
    levels2, _, _ = _trace("SNS", 2, 2)
    assert levels2[-1] == REGISTER_NEUTRAL    # but it breaks consecutiveness


# --- reversibility: supersession / correction ---------------------------------

def test_supersession_reverses_both_directions():
    for m in (1, 2):
        s = _build("SS")
        strong2 = s.assertions[-1]
        s.record_interaction(action=DISPOSITION_ANSWERED, content=N_TEXT,
                             gap_context=GAP, supersedes=[strong2.record_id])
        assert compute_register(s, w=2, m=m).level == REGISTER_NEUTRAL
        s2 = _build("SSW")
        weak = s2.assertions[-1]
        s2.record_interaction(action=DISPOSITION_ANSWERED, content=S_TEXT,
                              gap_context=GAP, supersedes=[weak.record_id])
        assert compute_register(s2, w=2, m=m).level == REGISTER_ELEVATED


# --- determinism / replay / no persistence ------------------------------------

def test_shuffle_and_recompute_equivalence():
    s = _build("SSWSSW")
    base = compute_register(s)
    sh = copy.deepcopy(s)
    rng = random.Random(5)
    for _ in range(5):
        rng.shuffle(sh.assertions)
        assert compute_register(sh) == base
    assert compute_register(copy.deepcopy(s)) == base


def test_register_never_persisted_and_pure():
    s = _build("SS")
    before = repr(s.__dict__)
    compute_register(s)
    assert repr(s.__dict__) == before
    assert not hasattr(s, "register") and not hasattr(s, "register_level")


# --- the proposal itself (NOT calibration evidence) ---------------------------

def test_current_proposal_constants():
    """The proposed values (Amendment §8.1: Owner-permitted proposal, NOT
    accepted, NOT frozen). This test only pins the proposal constants; the
    calibration evidence is the comparative-trace suite above."""
    assert (W_PROPOSED, M_PROPOSED) == (2, 2)
