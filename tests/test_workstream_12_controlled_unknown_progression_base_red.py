"""
test_workstream_12_controlled_unknown_progression_base_red.py
Workstream 12 — Controlled Unknown Progression BASE RED.

Governance basis (merged, authoritative):
    docs/governance/WORKSTREAM_12_CONTROLLED_UNKNOWN_PROGRESSION_INCREMENT_CONTRACT.md
        (fresh contract + ratified Owner Decisions OD-1 through OD-16, merged and
        post-merge verified via PR #268 / PR #269).

Purpose (deterministic BASE RED):
    Encode the bounded WS12 v1 observation-only public contract through the
    approved seam that does NOT yet exist — the pure module
    `engine.controlled_unknown_progression` exposing:

      * the six proposed controlled-unknown PATH classifications (OD-3)
        NEEDS_EVIDENCE / NEEDS_MEASUREMENT / NEEDS_TEST / NEEDS_SPECIALIST /
        DEFERRED_BY_USER / OUT_OF_SCOPE, collected in
        `WS12_UNKNOWN_PATH_CLASSIFICATIONS`;
      * a frozen observation-only view `ControlledUnknownView`;
      * a pure per-record classifier `classify_controlled_unknown(...)`;
      * a pure state reporter `report_controlled_unknowns(state)`;
      * a fail-loud typed error `ControlledUnknownProgressionError` (with
        `reason_code`).

    These tests prove the ABSENCE of that bounded WS12 behavior. They fail ONLY
    because the authorized WS12 production seam does not yet exist (GREEN is not
    authorized/started).

Controlled-RED discipline (mirrors the merged WS10 / WS11 BASE RED):
    This module imports ONLY the standard library and already-existing, merged
    engine modules at top level; it NEVER imports
    `engine.controlled_unknown_progression` at module scope. Every test resolves
    the missing WS12 seam through a helper (`_require_ws12_module` /
    `_require_ws12_attr`) that converts a missing module/symbol into a clear,
    decision-tagged `pytest.fail(...)`. Therefore all tests COLLECT cleanly and
    each fails for the one intended reason — the authorized WS12 seam is absent —
    never as an uncontrolled import/collection or fixture error. No skips,
    xfails, placeholders, or pass-forcing monkeypatches are used, and no test
    merely asserts the module is absent.

Scope: no production code, existing test, governance file, schema, persistence,
UI, prompt, or registry artifact is modified; `engine.controlled_unknown_progression`
is NOT created. Fixtures are built only from the already-merged
`engine.idea_state` surface (IdeaState, AcknowledgedUnknown, AssertionRecord).
WS12 v1 is observation-only: it must reuse those existing records (OD-2) and
must never mutate progression, maturity, gap status, or closure state (OD-1).
"""

import copy
import importlib

import pytest

# Already-existing, merged engine surface (safe to import at module scope).
from engine.idea_state import (
    IdeaState,
    AcknowledgedUnknown,
    Gap,
    INTERACTION_DISPOSITIONS,
    DISPOSITION_UNKNOWN,
    ACCEPTED_RISK,
    OPEN,
    CLOSED,
    CRITICALITY_FEASIBILITY_THREATENING,
    MECHANISM_COMPLETENESS,
)

_WS12_MODULE = "engine.controlled_unknown_progression"

# OD-3: the six proposed WS12 controlled-unknown PATH classifications. These are
# a SEPARATE vocabulary from the existing INTERACTION_DISPOSITIONS and are NOT
# yet present in production source.
_WS12_PATHS = (
    "NEEDS_EVIDENCE",
    "NEEDS_MEASUREMENT",
    "NEEDS_TEST",
    "NEEDS_SPECIALIST",
    "DEFERRED_BY_USER",
    "OUT_OF_SCOPE",
)

# The six existing interaction dispositions (already merged; the other vocabulary).
_EXISTING_DISPOSITIONS = frozenset({
    "answered", "unknown", "deferred", "provisional_assumption",
    "specialist_requested", "evidence_requested",
})

# Symbols whose presence on the WS12 module would breach a ratified boundary.
_FORBIDDEN_PERSISTENCE_EXPORT_NAMES = (   # OD-12 in-memory / non-exporting
    "save", "persist", "to_db", "write", "export", "to_json_file",
    "dump", "migrate", "patent_export",
)
_FORBIDDEN_D13_NAMES = (                  # OD-13 no Structured Technical Guidance
    "research_terms", "search_terms", "measurement_instructions",
    "test_procedure", "specialist_appointment", "technical_guidance",
    "structured_technical_guidance",
)
_FORBIDDEN_WS13_WS14_NAMES = (            # OD-14 WS13/WS14 separation
    "guided_answer", "generate_answer", "adaptive_follow_up",
    "completion_logic", "coach",
)
_FORBIDDEN_CAP_FULL_NAMES = (            # OD-15/OD-16 no CAP full behavior
    "gap_action_pack", "assumption_register", "contradiction_detector",
    "material_recommendation", "manufacturing_recommendation",
    "thickness_advisory", "safety_advisory", "image_interpretation",
    "drawing_interpretation", "multi_view",
)


# ── Controlled-RED seam resolvers (missing seam -> decision-tagged failure) ──
def _require_ws12_module():
    try:
        return importlib.import_module(_WS12_MODULE)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"WS12 BASE RED: the approved pure observation-only module "
            f"'{_WS12_MODULE}' does not exist yet (GREEN not authorized/started): "
            f"{exc}"
        )


def _require_ws12_attr(name, decision):
    module = _require_ws12_module()
    if not hasattr(module, name):
        pytest.fail(
            f"WS12 BASE RED ({decision}): approved public symbol "
            f"'{_WS12_MODULE}.{name}' is not exposed yet."
        )
    return getattr(module, name)


# ── Fixtures built only from the already-merged engine.idea_state surface ──
def _state_with_acknowledged_unknown():
    """An IdeaState carrying one AcknowledgedUnknown and one 'unknown' ledger
    record, both for the same gap_context. idea_id is required (positional)."""
    state = IdeaState(idea_id="ws12-base-red")
    state.iteration = 1
    state.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=1))
    state.acknowledged_unknowns.append(
        AcknowledgedUnknown(
            iteration=1,
            gap_context=MECHANISM_COMPLETENESS,
            verbatim="I do not know the exact clamping force required.",
            category_basis="inventor_stated",
        )
    )
    state.record_interaction(
        DISPOSITION_UNKNOWN,
        content="clamping force unknown",
        gap_context=MECHANISM_COMPLETENESS,
        iteration=1,
    )
    return state


def _snapshot(state):
    """A deep, comparable snapshot of the progression-bearing state, so a test
    can prove an observation-only call mutated nothing."""
    return copy.deepcopy((
        state.maturity_level,
        state.iteration,
        state.direction,
        [(g.gap_type, g.status, g.closed_at) for g in state.gaps],
        len(state.assertions),
        [(r.record_id, r.disposition, r.resolves_gap, r.superseded_by)
         for r in state.assertions],
        len(state.acknowledged_unknowns),
        len(state.criticality_confirmations),
    ))


# ── 1. Module exposes exactly the six OD-3 path classifications ──
def test_ws12_module_exposes_exactly_six_path_classifications():
    classifications = _require_ws12_attr(
        "WS12_UNKNOWN_PATH_CLASSIFICATIONS", "OD-3 classification vocabulary")
    assert frozenset(classifications) == frozenset(_WS12_PATHS), (
        "WS12 must expose exactly the six ratified path classifications (OD-3).")
    for name in _WS12_PATHS:
        value = _require_ws12_attr(name, "OD-3 classification constant")
        assert value == name


# ── 2. WS12 paths are disjoint from the existing INTERACTION_DISPOSITIONS ──
def test_ws12_paths_disjoint_from_interaction_dispositions():
    classifications = _require_ws12_attr(
        "WS12_UNKNOWN_PATH_CLASSIFICATIONS", "OD-3 separation")
    # The two vocabularies are different semantic dimensions (OD-3).
    assert frozenset(classifications).isdisjoint(INTERACTION_DISPOSITIONS)
    assert frozenset(classifications).isdisjoint(_EXISTING_DISPOSITIONS)


# ── 3. No implicit mapping: an INTERACTION_DISPOSITIONS value is not a path ──
def test_no_implicit_mapping_between_vocabularies():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-3 no silent mapping")
    Error = _require_ws12_attr(
        "ControlledUnknownProgressionError", "OD-3 fail-loud typed error")
    state = _state_with_acknowledged_unknown()
    record = state.acknowledged_unknowns[0]
    # Passing an existing disposition ('unknown') where a WS12 path is required
    # must be rejected loudly — never silently mapped/aliased/substituted.
    with pytest.raises(Error):
        classify(record, path=DISPOSITION_UNKNOWN)


# ── 4. classify is observation-only: it mutates no progression state (OD-1) ──
def test_classify_is_observation_only_no_progression_mutation():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-1 observation-only")
    state = _state_with_acknowledged_unknown()
    before = _snapshot(state)
    classify(state.acknowledged_unknowns[0], path="NEEDS_EVIDENCE")
    assert _snapshot(state) == before, (
        "classify_controlled_unknown must not mutate maturity, gaps, gap status, "
        "the ledger, or closure state (OD-1).")


# ── 5. Reuses AcknowledgedUnknown — no third unknown-record system (OD-2) ──
def test_reuses_acknowledged_unknown_record_no_third_system():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-2 reuse AcknowledgedUnknown")
    state = _state_with_acknowledged_unknown()
    view = classify(state.acknowledged_unknowns[0], path="NEEDS_MEASUREMENT")
    assert getattr(view, "source_kind", None) == "acknowledged_unknown"


# ── 6. Reuses AssertionRecord — no third unknown-record system (OD-2) ──
def test_reuses_assertion_record_no_third_system():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-2 reuse AssertionRecord")
    state = _state_with_acknowledged_unknown()
    unknown_record = state.assertions[0]
    view = classify(unknown_record, path="NEEDS_TEST")
    assert getattr(view, "source_kind", None) == "assertion_record"


# ── 7. Multiple unknowns may share one gap_context — no dedup (OD-9) ──
def test_multiple_unknowns_same_gap_context_no_dedup():
    report = _require_ws12_attr(
        "report_controlled_unknowns", "OD-9 no automatic deduplication")
    state = _state_with_acknowledged_unknown()
    # Second unknown record for the SAME gap_context.
    state.record_interaction(
        DISPOSITION_UNKNOWN, content="second unknown, same gap",
        gap_context=MECHANISM_COMPLETENESS, iteration=2)
    views = report(state)
    same_gap = [v for v in views
                if getattr(v, "gap_context", None) == MECHANISM_COMPLETENESS]
    assert len(same_gap) >= 2, (
        "report_controlled_unknowns must not deduplicate records that share a "
        "gap_context (OD-9).")


# ── 8. Supersession preserves history — no silent overwrite (OD-8) ──
def test_supersession_preserves_history():
    report = _require_ws12_attr(
        "report_controlled_unknowns", "OD-8 supersession preserves history")
    state = _state_with_acknowledged_unknown()
    first = state.assertions[0]
    later = state.record_interaction(
        DISPOSITION_UNKNOWN, content="answered later — supersedes",
        gap_context=MECHANISM_COMPLETENESS, iteration=3)
    state.mark_supersession(first.record_id, later.record_id)
    views = report(state)
    # Both the earlier (superseded) and later record remain represented.
    assert len(state.assertions) == 2 and first.superseded_by == later.record_id
    assert len(views) >= 2, (
        "report must preserve the earlier superseded record, not overwrite it "
        "(OD-8).")


# ── 9. Uniform sufficiency — classification independent of user role (OD-10) ──
def test_uniform_sufficiency_independent_of_user_role():
    """OD-10: classification/sufficiency must not vary by user_role, experience,
    profession, seniority, or confidence. Proven behaviorally — the classifier
    exposes no such parameter and rejects any attempt to supply one loudly; and
    repeated calls yield an identical classification (no hidden per-user path)."""
    import inspect
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-10 uniform sufficiency")
    state = _state_with_acknowledged_unknown()
    record = state.acknowledged_unknowns[0]
    forbidden = ("user_role", "experience", "profession", "seniority", "confidence")
    # (a) The classifier signature must expose none of the user-attribute inputs.
    sig = inspect.signature(classify)
    assert set(forbidden).isdisjoint(sig.parameters), (
        "classify_controlled_unknown must expose no user-attribute parameter "
        "(OD-10 uniform sufficiency).")
    # (b) Supplying any user attribute must fail loudly — never silently vary.
    for attr in forbidden:
        with pytest.raises(TypeError):
            classify(record, path="NEEDS_SPECIALIST", **{attr: "senior-expert"})
    # (c) The classification/sufficiency result is deterministic and identical
    #     across repeated calls (no hidden per-user variation).
    assert (classify(record, path="NEEDS_SPECIALIST").path_classification
            == classify(record, path="NEEDS_SPECIALIST").path_classification)


# ── 10. Safety-critical unknowns remain explicit — no silent downgrade (OD-11)
def test_safety_critical_unknown_remains_explicit():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-11 safety-critical visibility")
    state = _state_with_acknowledged_unknown()
    view = classify(state.acknowledged_unknowns[0], path="NEEDS_TEST",
                    safety_critical=True)
    assert getattr(view, "safety_critical", None) is True, (
        "A safety-critical unknown must remain explicitly flagged (OD-11).")


# ── 11. Blocker classification is report-only — never blocks/mutates (OD-4) ──
def test_blocker_classification_is_report_only():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-4 blocker classification only")
    state = _state_with_acknowledged_unknown()
    before = _snapshot(state)
    view = classify(state.acknowledged_unknowns[0], path="NEEDS_EVIDENCE",
                    blocking=True)
    assert getattr(view, "blocking", None) is True
    assert _snapshot(state) == before, (
        "Reporting an unknown as blocking must not itself block or mutate "
        "progression (OD-4).")


# ── 12. Criticality is read-only — no silent criticality change (OD-5) ──
def test_criticality_is_read_only():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-5 criticality read-only")
    state = _state_with_acknowledged_unknown()
    before_conf = list(state.criticality_confirmations)
    view = classify(state.acknowledged_unknowns[0], path="NEEDS_SPECIALIST",
                    criticality=CRITICALITY_FEASIBILITY_THREATENING)
    # Criticality is echoed read-only; no confirmation is created or changed.
    assert getattr(view, "criticality", None) == CRITICALITY_FEASIBILITY_THREATENING
    assert state.criticality_confirmations == before_conf, (
        "WS12 must not create, raise, lower, or replace criticality (OD-5).")


# ── 13. Closure path is recommendation only — no resolution/closure (OD-6/7) ──
def test_closure_path_is_recommendation_only():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-6/OD-7 closure recommendation only")
    state = _state_with_acknowledged_unknown()
    gap = state.gaps[0]
    view = classify(state.acknowledged_unknowns[0], path="NEEDS_EVIDENCE",
                    closure_recommendation="obtain a measured clamping-force value")
    assert getattr(view, "closure_recommendation", None)
    # A recommendation resolves nothing and closes nothing.
    assert getattr(view, "resolves_gap", True) is False
    assert gap.status == OPEN and gap.status != CLOSED, (
        "A closure-path recommendation must not close a gap or resolve an "
        "unknown (OD-6/OD-7).")


# ── 14. ACCEPTED_RISK boundary — WS12 never emits/assigns it (OD-6/OD-11) ──
# Supplementary coverage: an unrelated valid path (OUT_OF_SCOPE) never yields or
# assigns ACCEPTED_RISK. The direct rejection contract is test 14b below.
def test_accepted_risk_boundary_not_emitted():
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-6 ACCEPTED_RISK boundary")
    state = _state_with_acknowledged_unknown()
    gap = state.gaps[0]
    # ACCEPTED_RISK is a real Gap.status value (referenced here to protect the
    # boundary); WS12 must never create, assign, infer, recommend, or transition
    # to it.
    assert ACCEPTED_RISK == "ACCEPTED_RISK"
    view = classify(state.acknowledged_unknowns[0], path="OUT_OF_SCOPE")
    assert getattr(view, "path_classification", None) != ACCEPTED_RISK
    assert getattr(view, "closure_recommendation", None) != ACCEPTED_RISK
    assert gap.status != ACCEPTED_RISK, (
        "WS12 must not transition a gap to ACCEPTED_RISK (OD-6).")


# ── 14b. ACCEPTED_RISK rejected as a WS12 path — fails loudly, no state change ─
def test_accepted_risk_rejected_as_path_classification():
    """OD-6 (direct): ACCEPTED_RISK is a Gap.status value, never a WS12 path.
    Supplying it must fail loudly through the governed typed error, produce no
    view, and change no gap/maturity/progression/ledger/closure state."""
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-6 ACCEPTED_RISK rejection")
    Error = _require_ws12_attr(
        "ControlledUnknownProgressionError", "OD-6 fail-loud typed error")
    state = _state_with_acknowledged_unknown()
    gap = state.gaps[0]
    before = _snapshot(state)
    result = None
    with pytest.raises(Error):
        result = classify(state.acknowledged_unknowns[0], path=ACCEPTED_RISK)
    # The call raised: no view was produced, and nothing was mutated.
    assert result is None
    assert _snapshot(state) == before, (
        "A rejected ACCEPTED_RISK path must change no gap/maturity/ledger/closure "
        "state (OD-6).")
    assert gap.status != ACCEPTED_RISK


# ── 14c. Safety-critical deferral is not silent acceptance/resolution (OD-11) ─
def test_safety_critical_deferral_not_silently_accepted():
    """OD-11: safety_critical=True with path DEFERRED_BY_USER. The unknown
    remains an explicit, unresolved, safety-critical view; deferral is not
    acceptance, resolution, closure, downgrade, or conversion — and the call is
    observation-only (no state mutation)."""
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "OD-11 safety-critical deferral")
    state = _state_with_acknowledged_unknown()
    gap = state.gaps[0]
    before = _snapshot(state)
    view = classify(state.acknowledged_unknowns[0], path="DEFERRED_BY_USER",
                    safety_critical=True)
    # The safety-critical flag survives the deferral and stays prominent.
    assert getattr(view, "safety_critical", None) is True
    assert getattr(view, "path_classification", None) == "DEFERRED_BY_USER"
    # Deferral resolves/closes/accepts nothing.
    assert getattr(view, "resolves_gap", True) is False
    assert gap.status not in (CLOSED, ACCEPTED_RISK)
    assert _snapshot(state) == before, (
        "Deferring a safety-critical unknown must not silently defer, downgrade, "
        "close, accept, or convert it (OD-11).")


# ── 14d. Typed error exposes a stable reason_code (documented public contract) ─
def test_typed_error_exposes_stable_reason_code():
    """The test-file/governance documentation states that
    ControlledUnknownProgressionError exposes a stable reason_code; prove it. An
    invalid path classification must raise the governed typed error carrying a
    non-empty string reason_code."""
    classify = _require_ws12_attr(
        "classify_controlled_unknown", "typed-error reason_code")
    Error = _require_ws12_attr(
        "ControlledUnknownProgressionError", "typed-error reason_code")
    state = _state_with_acknowledged_unknown()
    with pytest.raises(Error) as exc_info:
        classify(state.acknowledged_unknowns[0], path="NOT_A_VALID_WS12_PATH")
    reason_code = getattr(exc_info.value, "reason_code", None)
    assert isinstance(reason_code, str) and reason_code, (
        "ControlledUnknownProgressionError must expose a stable, non-empty "
        "string reason_code.")


# ── 15. In-memory / non-exporting — no persistence/export surface (OD-12) ──
def test_in_memory_non_exporting_no_persistence_surface():
    module = _require_ws12_module()
    present = [n for n in _FORBIDDEN_PERSISTENCE_EXPORT_NAMES if hasattr(module, n)]
    assert present == [], (
        f"WS12 v1 must expose no persistence/export surface (OD-12); found: {present}")


# ── 16. D13 boundary — no Structured Technical Guidance surface (OD-13) ──
def test_d13_boundary_no_technical_guidance_surface():
    module = _require_ws12_module()
    present = [n for n in _FORBIDDEN_D13_NAMES if hasattr(module, n)]
    assert present == [], (
        f"WS12 must not implement Structured Technical Guidance (OD-13); found: {present}")


# ── 17. WS13/WS14 separation — no guided-answer/adaptive-follow-up (OD-14) ──
def test_ws13_ws14_separation():
    module = _require_ws12_module()
    present = [n for n in _FORBIDDEN_WS13_WS14_NAMES if hasattr(module, n)]
    assert present == [], (
        f"WS12 must not implement WS13/WS14 behavior (OD-14); found: {present}")
    # The protected WS13/WS14 modules remain absent regardless.
    for absent in ("engine.guided_answer_support", "engine.adaptive_follow_up"):
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(absent)


# ── 18. CAP-04/08/10 interface-only — no full capability surface (OD-15) ──
def test_cap_04_08_10_interface_boundary_only():
    module = _require_ws12_module()
    present = [n for n in (
        "gap_action_pack", "assumption_register", "contradiction_detector")
        if hasattr(module, n)]
    assert present == [], (
        f"WS12 must expose CAP-04/08/10 only as typed interface boundaries, not "
        f"full implementations (OD-15); found: {present}")


# ── 19. CAP-12/13/14 completely absent from WS12 behavior (OD-16) ──
def test_cap_12_13_14_absent_from_ws12():
    module = _require_ws12_module()
    present = [n for n in _FORBIDDEN_CAP_FULL_NAMES if hasattr(module, n)]
    assert present == [], (
        f"WS12 must contain no CAP-12/13/14 behavior (OD-16); found: {present}")
