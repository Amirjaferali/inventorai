"""Phase 1 fix — idea-summary truncation is marked, never a broken mid-phrase.

Verifies engine.progression_loop._trim_idea_summary appends an explicit ellipsis
marker when it truncates, that short answers are untouched, that the full
original statement survives in state.known_problem.content, and that the
rendered deliverable "Known Problem" and REQ-001 no longer end mid-phrase.
"""
import os, sys, uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.progression_loop import _trim_idea_summary, _IDEA_SUMMARY_MAX
from engine.idea_state import IdeaState, Evidence, REASONED
from engine.deliverable_assembler import assemble_deliverable

_ELLIPSIS = "…"  # …


def _long_problem():
    return (
        "This invention is an electronic cold-chain monitoring device for refrigerated "
        "meat delivery trucks. It continuously monitors whether meat inside the "
        "refrigerated compartment stays within a safe temperature band during transit, "
        "using a microcontroller reading multiple digital temperature sensors placed at "
        "different shelf heights, and it logs every reading to onboard memory while also "
        "transmitting periodic wireless status updates to the driver cabin display and to "
        "a back office dashboard so that a spoilage risk can be detected early and the "
        "driver can be alerted before the cargo is compromised in any way whatsoever today."
    )


# --- unit-level behaviour ---------------------------------------------------

def test_short_answer_unchanged():
    s = "A compact electronic leak sensor that alerts the user."
    assert len(s) <= _IDEA_SUMMARY_MAX
    assert _trim_idea_summary(s) == s  # untouched, no marker


def test_answer_at_limit_gets_no_marker():
    s = "x" * _IDEA_SUMMARY_MAX  # exactly at the limit
    assert _trim_idea_summary(s) == s  # no marker at/below the limit


def test_long_answer_gets_explicit_marker_at_word_boundary():
    full = _long_problem()
    assert len(full) > _IDEA_SUMMARY_MAX
    out = _trim_idea_summary(full)
    assert out.endswith(_ELLIPSIS)  # explicit, visible truncation marker
    assert len(out) <= _IDEA_SUMMARY_MAX + len(_ELLIPSIS)
    body = out[: -len(_ELLIPSIS)]
    assert full.startswith(body)  # only the inventor's own words, verbatim
    assert body and body[-1] != " "  # cut cleanly at a word boundary, no trailing space


# --- rendered deliverable ---------------------------------------------------

def _state_with_long_summary():
    full = _long_problem()
    s = IdeaState(idea_id="trunc-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.current_stage = 3
    s.known_problem = Evidence(full, REASONED, 1)  # FULL original preserved here
    s.idea_summary = _trim_idea_summary(full)      # trimmed + marker
    return s, full


def test_rendered_known_problem_ends_with_marker_not_midphrase():
    s, _ = _state_with_long_summary()
    kp = assemble_deliverable(s)["section_2_invention_summary"]["known_problem"]["content"]
    assert kp.endswith(_ELLIPSIS)
    assert not kp.rstrip().endswith("so that")  # the reported broken mid-phrase ending


def test_rendered_req001_statement_carries_marker():
    s, _ = _state_with_long_summary()
    reqs = assemble_deliverable(s)["section_4_requirements"]["requirements"]
    assert reqs, "expected at least REQ-001 from the resolved problem"
    assert reqs[0]["statement"].endswith(_ELLIPSIS)


def test_full_original_remains_intact_in_known_problem_content():
    s, full = _state_with_long_summary()
    assert s.known_problem.content == full  # canonical evidence is never truncated
    assert len(s.known_problem.content) > _IDEA_SUMMARY_MAX
