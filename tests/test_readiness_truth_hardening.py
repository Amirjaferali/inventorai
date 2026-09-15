"""Readiness truth hardening — the validation axis is an invariant, not a habit.

`READINESS-TRUTH-HARDENING-IMPLEMENT-01` (Owner-authorized), accepting
`READINESS-BLOCKERS-RECONCILE-01` verdict B.

Two related repairs, both about the same thing: what the product is allowed to
CONCLUDE about readiness, and from what.

1. The restore boundary validates `validation_status` against the canonical
   vocabulary. Before this, `record_contract.assertion_from_dict` copied the
   value verbatim, so a stored payload carrying `INDEPENDENTLY_VERIFIED` — or
   the literal string `TOTALLY_MADE_UP` — restored intact and published
   "Derived readiness signal met" into the inventor-facing deliverable. No live
   writer could produce such a row, but nothing enforced that; the honest
   `False` rested on writer discipline alone.

2. Derived readiness aggregates over the canonical GAP contexts only. Before
   this, decision-action records (`gap_context=None`) formed a `None` "context"
   that distorted the aggregate in both directions — inflating it when they were
   the only records, vetoing it when a real gap context had verified.

What this deliberately does NOT do: unlock a tier. `UNVALIDATED` is still the
only value any live path writes, `INDEPENDENTLY_VERIFIED` is still awardable by
nothing, and a normal project still cannot reach a positive verified readiness
state. Validating a vocabulary is not permission to write its values.
"""
import os
import re

import pytest

from engine.derived_readiness import READINESS_GAP_CONTEXTS, derive_readiness
from engine.idea_state import (
    EMPIRICALLY_DEMONSTRATED, INDEPENDENTLY_VERIFIED, IdeaState,
    SPECIALIST_REVIEWED, STAGE_2_GAP_TYPES, STAGE_3_GAP_TYPES, UNVALIDATED,
    VALIDATED_STATUSES, VALIDATION_STATUSES,
)
from engine.decision_composition import (
    declare_alternative, declare_decision_context,
)
from engine.progression_loop import run_iteration
from engine.record_contract import (
    ContractError, InvalidValidationStatusError, ProjectRecordContract,
    assertion_from_dict, assertion_to_dict,
)

_ROOT = os.path.join(os.path.dirname(__file__), "..")
_GAP = "MECHANISM_COMPLETENESS"


def _answered(state, gap_context=_GAP, content="a mechanism statement"):
    return state.record_interaction(
        action="answered", content=content, gap_context=gap_context,
        iteration=state.iteration)


def _payload(validation_status):
    """One canonical answered payload with the validation axis set directly —
    the exact shape a stored row takes, bypassing every writer."""
    s = IdeaState(idea_id="payload")
    row = assertion_to_dict(_answered(s))
    return dict(row, validation_status=validation_status)


# ==========================================================================
# 1. the restore boundary (Owner §1.A)
# ==========================================================================
def test_an_invalid_restored_validation_status_is_rejected():
    """A. A value outside the canonical vocabulary never becomes a live record.
    Rejection is by VALUE, not by shape: these payloads are otherwise perfect."""
    for bad in ("TOTALLY_MADE_UP", "VALIDATED", "unvalidated", "",
                None, 0, True, ["UNVALIDATED"], "UNVALIDATED "):
        with pytest.raises(InvalidValidationStatusError):
            assertion_from_dict(_payload(bad))


def test_the_rejection_is_a_contract_error_and_leaks_no_value():
    """The existing fail-closed discipline: a ContractError/ValueError like every
    other restore failure, so callers that already fail closed need no change —
    and the offending text is never echoed back out of the boundary."""
    assert issubclass(InvalidValidationStatusError, ContractError)
    assert issubclass(InvalidValidationStatusError, ValueError)
    secret = "TOTALLY_MADE_UP_7f3a_secret_marker"
    with pytest.raises(ContractError) as exc:
        assertion_from_dict(_payload(secret))
    assert secret not in str(exc.value)


def test_every_canonical_validation_status_still_deserializes():
    """B. The four canonical values round-trip unchanged. The boundary validates
    the vocabulary; it does not narrow it, reorder it or reinterpret it."""
    assert VALIDATION_STATUSES == frozenset({
        UNVALIDATED, SPECIALIST_REVIEWED, EMPIRICALLY_DEMONSTRATED,
        INDEPENDENTLY_VERIFIED})
    assert VALIDATED_STATUSES == VALIDATION_STATUSES - {UNVALIDATED}
    for value in sorted(VALIDATION_STATUSES):
        assert assertion_from_dict(_payload(value)).validation_status == value


def test_an_invalid_value_is_never_coerced_to_unvalidated():
    """Silently rewriting a stored row as UNVALIDATED would replace one untruth
    with a quieter one — the caller would believe it had loaded real history."""
    with pytest.raises(InvalidValidationStatusError):
        assertion_from_dict(_payload("TOTALLY_MADE_UP"))


def test_a_whole_project_contract_fails_closed_on_a_poisoned_row():
    """The boundary holds at the level callers actually use: one bad row refuses
    the whole restore rather than loading a project with a fabricated axis."""
    s = IdeaState(idea_id="proj")
    _answered(s)
    good = ProjectRecordContract.from_state(s).to_dict()
    good["assertions"][0]["validation_status"] = "TOTALLY_MADE_UP"
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(good)


# ==========================================================================
# 2. derived-readiness aggregation (Owner §1.C)
# ==========================================================================
def test_readiness_contexts_are_exactly_the_six_canonical_gap_types():
    """The scope is taken from the existing gap-type definitions, never re-listed
    and never widened."""
    assert READINESS_GAP_CONTEXTS == frozenset(
        STAGE_2_GAP_TYPES | STAGE_3_GAP_TYPES)
    assert len(READINESS_GAP_CONTEXTS) == 6
    assert None not in READINESS_GAP_CONTEXTS


def test_decision_action_only_records_cannot_produce_overall_verified():
    """C. The inflation path, closed. Decision actions carry gap_context=None;
    a project made only of them has no readiness basis whatsoever, so the flag
    is False even when every such record carries the strongest tier."""
    s = IdeaState(idea_id="dw-only")
    root = declare_decision_context(s, "which sensor", iteration=1)
    declare_alternative(s, "an option", root.record_id, iteration=1)
    for r in s.assertions:
        r.validation_status = INDEPENDENTLY_VERIFIED
    assert s.assertions and all(
        r.validation_status == INDEPENDENTLY_VERIFIED for r in s.assertions)
    d = derive_readiness(s)
    assert d.overall_verified() is False
    assert d.is_verified(None) is False
    assert d.unverified_contexts() == []


def test_a_non_readiness_record_does_not_veto_a_valid_readiness_set():
    """D, second direction. A decision action is not evidence about a technical
    gap, so it must not withhold readiness either. Verified with a hypothetical
    validated gap record, because no live writer can produce one."""
    s = IdeaState(idea_id="mixed")
    g = _answered(s)
    g.validation_status = INDEPENDENTLY_VERIFIED
    assert derive_readiness(s).overall_verified() is True
    s.record_interaction(action="decision_context_declared", content="an option",
                         iteration=1)
    assert derive_readiness(s).overall_verified() is True, "vetoed by a non-gap record"
    assert derive_readiness(s).unverified_contexts() == []


def test_gap_context_evidence_is_still_evaluated_under_the_existing_rules():
    """E. Nothing about what "verified" MEANS inside a gap context changed: an
    unvalidated record still blocks, a provisional assumption still blocks, and
    a second unverified gap context still blocks the aggregate."""
    s = IdeaState(idea_id="rules")
    g = _answered(s)
    assert derive_readiness(s).is_verified(_GAP) is False       # UNVALIDATED
    g.validation_status = SPECIALIST_REVIEWED
    assert derive_readiness(s).is_verified(_GAP) is True
    p = s.record_interaction(action="provisional_assumption", content="assume",
                             gap_context=_GAP, iteration=1)
    p.validation_status = SPECIALIST_REVIEWED
    assert derive_readiness(s).is_verified(_GAP) is False        # provisional
    s.assertions.remove(p)
    other = s.record_interaction(action="answered", content="b",
                                 gap_context="ASSUMPTION_INVENTORY", iteration=1)
    assert derive_readiness(s).overall_verified() is False       # second context
    assert derive_readiness(s).unverified_contexts() == ["ASSUMPTION_INVENTORY"]
    other.validation_status = SPECIALIST_REVIEWED
    assert derive_readiness(s).overall_verified() is True


def test_supersession_and_contradiction_semantics_are_untouched():
    """The F-3 owner ruling and the contradiction rule still decide the active
    set exactly as before; this repair changed WHICH CONTEXTS count, not which
    records within one."""
    s = IdeaState(idea_id="sup")
    old = _answered(s)
    new = s.record_interaction(action="answered", content="corrected",
                               gap_context=_GAP, iteration=2,
                               supersedes=[old.record_id])
    new.validation_status = SPECIALIST_REVIEWED
    assert derive_readiness(s).is_verified(_GAP) is True   # superseded row inactive
    other = _answered(s, content="conflicting")
    other.validation_status = SPECIALIST_REVIEWED
    other.contradicts = [new.record_id]
    assert derive_readiness(s).is_verified(_GAP) is False  # active contradiction


# ==========================================================================
# 3. no tier became reachable (Owner §1.B, §1.D)
# ==========================================================================
def test_a_normal_live_project_still_gains_no_positive_readiness_state():
    """F. The point of the whole slice: after hardening, the honest answer is
    unchanged. A real journey through the real loop still produces UNVALIDATED
    records only, and still cannot reach verified readiness."""
    s = IdeaState(idea_id="live")
    s.domain = "mechanical"
    for answer in (
            "Carers cannot transfer a patient alone, which causes back injuries "
            "because the existing hoist requires a second operator.",
            "The mechanism is a lead-screw scissor lift, so the load path runs "
            "through the frame rather than the sling, reducing operator force.",
            "The assumption is that one carer can position it, because the base "
            "clears a standard 210 mm bed frame."):
        ctx = s.gaps[0].gap_type if s.gaps else None
        run_iteration(s, answer)
        s.record_interaction(action="answered", content=answer,
                             gap_context=ctx, iteration=s.iteration)
    assert {r.validation_status for r in s.assertions} == {UNVALIDATED}
    assert derive_readiness(s).overall_verified() is False


def test_no_writer_for_any_upper_tier_was_introduced():
    """B. This slice validates the axis; it awards nothing. No production line
    assigns an upper tier — checked as SOURCE (both the bare constant and the
    quoted literal, which the older sibling guard does not catch) and reinforced
    by the live-journey behaviour above."""
    upper = ("SPECIALIST_REVIEWED", "EMPIRICALLY_DEMONSTRATED",
             "INDEPENDENTLY_VERIFIED")
    offenders = []
    for folder in ("engine", "web"):
        base = os.path.join(_ROOT, folder)
        for dirpath, _dirs, names in os.walk(base):
            if "__pycache__" in dirpath:
                continue
            for name in names:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(dirpath, name)
                for number, line in enumerate(
                        open(path, encoding="utf-8"), 1):
                    code = line.split("#")[0]
                    for value in upper:
                        if re.search(
                                r"validation_status\s*=\s*[\"']?%s\b" % value,
                                code):
                            offenders.append("%s:%d" % (path, number))
    assert not offenders, offenders


def test_independently_verified_is_awarded_by_nothing():
    """No owner or system action may ever award independence. Membership in the
    canonical vocabulary is not permission to write the value."""
    assert INDEPENDENTLY_VERIFIED in VALIDATION_STATUSES
    s = IdeaState(idea_id="never")
    s.domain = "mechanical"
    run_iteration(s, "The mechanism is a lead-screw lift, so the load path runs "
                     "through the frame rather than the sling.")
    rec = _answered(s)
    assert rec.validation_status == UNVALIDATED


# ==========================================================================
# 4. decision-workspace presentation (Owner §2)
# ==========================================================================
def _dw_template():
    return open(os.path.join(_ROOT, "web", "templates",
                             "decision_workspace.html"), encoding="utf-8").read()


def _strip_prose(text):
    """Source with Jinja comments, docstrings and line comments removed, so a
    scan asserts about CODE and MARKUP — never about prose that merely NAMES a
    banned token. Several modules in this repository document, in words, the
    exact vocabularies they must never use."""
    text = re.sub(r"(?s)\{#.*?#\}", "", text)
    text = re.sub(r'(?s)"{3}.*?"{3}', "", text)
    return "\n".join(line.split("#")[0] for line in text.splitlines())


def _dw_markup():
    """The template with its Jinja comments removed, so a scan asserts about
    what the page RENDERS and never about prose that merely NAMES a banned
    token — the template documents, in words, the vocabularies it must not
    borrow."""
    return _strip_prose(_dw_template())


def test_the_workspace_heading_no_longer_uses_the_canonical_word():
    """G. No heading in this non-canonical lane is titled "Readiness"."""
    body = _dw_template()
    assert "<h2>Readiness</h2>" not in body
    assert "<h2>Comparison state</h2>" in body
    assert not re.search(r"<h[1-6][^>]*>\s*Readiness\s*</h[1-6]>", body)


def test_the_raw_internal_status_token_is_not_presented_bare():
    """H. The stored token is mapped through a presentation seam; the bare
    `{{ view.readiness_status }}` rendering is gone."""
    body = _dw_template()
    assert "{{ view.readiness_status }}" not in body
    assert "dw_state_wording" in body


def test_the_workspace_wording_borrows_no_canonical_vocabulary():
    """The lane must not look like either canonical decision system: neither the
    Owner-adopted Readiness vocabulary nor the existing product verdict."""
    body = _dw_markup()
    for token in ("PASS_WITH_CONDITIONS", "INSUFFICIENT_EVIDENCE",
                  "PROCEED WITH CAUTION", "PROCEED", "REVISE", "BLOCK",
                  "PASS", "HOLD"):
        assert token not in body, token


def test_the_workspace_discloses_that_it_is_not_canonical_readiness():
    """D. One concise clarification, and no second readiness label system."""
    body = _dw_template()
    assert "not the product's Readiness assessment" in body


def test_the_workspace_engine_tokens_are_byte_identical():
    """I. Template-only: the engine module keeps its stored vocabulary exactly,
    and the byte pin over it is untouched."""
    import subprocess
    from engine import decision_workspace as dw
    assert dw.INSUFFICIENT_INFORMATION == "insufficient_information"
    assert dw.BLOCKED_BY_EVIDENCE_GAP == "blocked_by_evidence_gap"
    assert dw.COMPARISON_IN_PROGRESS == "comparison_in_progress"
    assert dw.DECISION_READY_FOR_OWNER_REVIEW == "decision_ready_for_owner_review"
    out = subprocess.run(
        ["git", "diff", "--name-only",
         "f96c1900a0f5d0831a7654223ae4e008d4df961e", "--",
         "engine/decision_workspace.py"],
        capture_output=True, text=True, cwd=_ROOT)
    assert out.stdout.strip() == "", "engine/decision_workspace.py changed"


def test_every_stored_token_has_presentation_wording():
    """The map covers the whole stored vocabulary, so no token can fall through
    and be rendered raw."""
    from engine import decision_workspace as dw
    body = _dw_template()
    for token in (dw.INSUFFICIENT_INFORMATION, dw.BLOCKED_BY_EVIDENCE_GAP,
                  dw.COMPARISON_IN_PROGRESS, dw.DECISION_READY_FOR_OWNER_REVIEW):
        assert '"%s":' % token in body, token


# ==========================================================================
# 5. no readiness runtime was introduced (Owner §4)
# ==========================================================================
def test_no_readiness_runtime_vocabulary_exists_anywhere_in_the_product():
    """J. The Owner-adopted Readiness vocabulary belongs to a runtime that is
    NOT authorized and does not exist. It must appear in no engine module, no
    route and no template."""
    # `PASS_WITH_CONDITIONS` is unambiguous — it exists only as a Readiness
    # disposition. `INSUFFICIENT_EVIDENCE` is checked separately below, because
    # one PRE-EXISTING, unrelated use of that identifier already exists.
    tokens = ("PASS_WITH_CONDITIONS",)
    hits = []
    for folder, suffix in (("engine", ".py"), ("web", ".py"),
                           (os.path.join("web", "templates"), ".html")):
        base = os.path.join(_ROOT, folder)
        for dirpath, _dirs, names in os.walk(base):
            if "__pycache__" in dirpath:
                continue
            for name in names:
                if not name.endswith(suffix):
                    continue
                body = _strip_prose(open(
                    os.path.join(dirpath, name), encoding="utf-8").read())
                for token in tokens:
                    if token in body:
                        hits.append("%s:%s" % (name, token))
    assert not hits, hits


def test_the_only_insufficient_evidence_identifier_is_the_domain_reason_code():
    """The one pre-existing use of that identifier is `domain_rules.py`'s
    deterministic reason code for an AMBIGUOUS DOMAIN CLASSIFICATION — its
    stored value is lowercase `insufficient_evidence`, it is never a readiness
    disposition, and it reaches no route and no template. Pinned by name here so
    that a future genuine collision with the Owner-adopted Readiness vocabulary
    is caught rather than blending into an identifier that already existed."""
    from engine.domain_rules import DomainAmbiguityReason
    assert (DomainAmbiguityReason.INSUFFICIENT_EVIDENCE.value
            == "insufficient_evidence")
    users = []
    for folder, suffix in (("engine", ".py"), ("web", ".py"),
                           (os.path.join("web", "templates"), ".html")):
        for dirpath, _dirs, names in os.walk(os.path.join(_ROOT, folder)):
            if "__pycache__" in dirpath:
                continue
            for name in names:
                if not name.endswith(suffix):
                    continue
                body = _strip_prose(
                    open(os.path.join(dirpath, name), encoding="utf-8").read())
                if "INSUFFICIENT_EVIDENCE" in body:
                    users.append(name)
    assert users == ["domain_rules.py"], users


def test_this_slice_added_no_readiness_engine_and_no_second_owner():
    """No new module, no new store, no new axis: the repair lives entirely
    inside three existing owners plus one template."""
    for absent in ("readiness_runtime.py", "readiness_engine.py",
                   "manufacturing_evidence.py", "technical_readiness.py"):
        assert not os.path.exists(os.path.join(_ROOT, "engine", absent)), absent
    source = open(os.path.join(_ROOT, "engine", "derived_readiness.py"),
                  encoding="utf-8").read()
    code = _strip_prose(source)
    for banned in ("PASS_WITH_CONDITIONS", "INSUFFICIENT_EVIDENCE", "score",
                   "GroundedRisk", "commercial", "manufacturing"):
        assert banned not in code, banned
