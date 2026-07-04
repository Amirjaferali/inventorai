"""Increment 6 — Deliverable Redesign — tests-first.

Authored under an explicit, owner-gated TESTS-FIRST-ONLY authorization, BEFORE any
source, template, or engine change, per the merged and binding governance:

  * docs/governance/INCREMENT_6_DELIVERABLE_REDESIGN_DESIGN.md   (design, active)
  * docs/governance/INCREMENT_6_IMPLEMENTATION_CONTRACT.md       (contract, active)

Authoritative integration tip at authoring time:
  9e87fa6c6635bd4a57f7d4debf70b443066d3b8e
  (parents cbddea9 [PR #71 implementation contract] + 0419784 [PR #72 roadmap sync])

This file is the ONLY file created by this phase. It authors NO source, NO
template change, and NO engine change, and it grants no implementation authority.
It implements the §g tests-first matrix of the implementation contract:

  1. Traceability                — every rendered value maps to an existing
                                    ``package`` key / Increment 1-5 derivation.
  2. Label-preservation          — evidence-state / validation_status / status_label
                                    travel beside each claim (Increment 2 honesty).
  3. No-upgrade                  — no verification-free upgrade to verified/resolved;
                                    ``derived_verified_ready`` stays separate from
                                    stored maturity / ``deliverable_eligible``.
  4. Backward-compatibility      — existing package/session structure and the
                                    ``fdc-001-mvp-v1`` section_11 contract preserved.
  5. Protected-boundary          — no score_case / WPS-001 / progression / domain
                                    registry / _s6 semantic change.
  6. No-persistence              — no persistence write / resumption / ``aec9cf6``.
  7. No-new-truth / no-generation— no new generated content, external document,
                                    new-truth section, or implied cross-link.

Two kinds of tests are present, as the contract §g and the authorizing owner
instruction direct:

  (a) Invariants that MUST already hold on the current committed product and are
      expected to PASS now — they lock preserved behavior so the future redesign
      cannot regress it. These operate on the assembled ``package`` (pure Python).

  (b) Intended post-redesign PRESENTATION expectations that are EXPECTED to FAIL
      now because the design §4 inventor-facing grouping has NOT been implemented
      in ``web/templates/deliverable.html`` yet (source is NOT authorized by this
      phase). Any such failure MUST be read as:
          EXPECTED RED — SOURCE NOT YET AUTHORIZED
      They are named ``test_redesign_*`` and MUST NOT be made to pass by editing
      product code in this phase. The redesign is, per the contract §c, a
      TEMPLATE-ONLY restructuring; these tests therefore assert against the
      committed template source only — no Flask app is started (C6-R6/§g intent),
      keeping every failure attributable to absent redesign rather than absent
      test infrastructure.

Import discipline: only committed, existing modules are imported. No web/Flask
import (avoids an infrastructure-absence failure masquerading as a RED redesign
failure). No fixture is created or mutated; states are built through the committed
public API only.
"""
import os
import sys
import json
import copy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.idea_state import (
    IdeaState, Gap, Evidence,
    OPEN, PARTIAL, CLOSED, ASSERTED, REASONED, DEMONSTRATED,
    PROBLEM_MECHANISM_FIT, STAGE_3_GAP_TYPES,
)
from engine.domain_rules import infer_domain
from engine.progression_loop import run_iteration
from engine.deliverable_assembler import (
    assemble_deliverable, _s9, PACKAGE_VERSION, SCHEMA_ID,
)

# --------------------------------------------------------------------------------
# Frozen structural facts (verified read-only against the assembler at the tip)
# --------------------------------------------------------------------------------
CANONICAL_SECTION_KEYS = (
    "section_1_disclaimer",
    "section_2_invention_summary",
    "section_3_assessment_overview",
    "section_4_requirements",
    "section_5_assumptions",
    "section_6_risks",
    "section_7_recommendations",
    "section_8_unresolved_items",
    "section_9_stage3_reasoning",
    "section_10_recommended_next_steps",
    "section_11_prototype_test_plan",
    "section_12_next_development_step",   # Increment 3 (additive)
    "section_13_requirement_landscape",   # Increment 4 (additive)
    "section_14_validation_plan",         # Increment 5 (additive)
)
ENVELOPE_KEYS = ("package_version", "schema_id", "session_id", "generated_at")

# design §4 inventor-facing grouping (reading order). Absent from the template
# today; the future TEMPLATE-ONLY redesign introduces exactly these groups.
REDESIGN_GROUP_HEADINGS = (
    "What your idea is",
    "What we assessed",
    "What it needs",
    "What is assumed vs still unknown",
    "What could go wrong",
    "The reasoning behind it",
    "What we recommend and what to do next",
)

_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "web", "templates", "deliverable.html",
)
_ASSEMBLER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "engine", "deliverable_assembler.py",
)

# The paused-persistence artifact that must never be referenced (C6-R6).
_FROZEN_ARTIFACT = "aec9cf6"


# --------------------------------------------------------------------------------
# State builders — committed public API only (no fixtures created or mutated)
# --------------------------------------------------------------------------------
def _fresh_state(idea="IoT greenhouse temperature sensor with relay control"):
    s = IdeaState(idea_id="inc6-" + str(abs(hash(idea)) % 10_000_000))
    s.domain = infer_domain(idea)
    s.domain_signal = s.domain
    return s


def _session(idea, *inputs):
    s = _fresh_state(idea)
    for text in inputs:
        run_iteration(s, text)
    return s


def _mechanism_session():
    """A Level>=1 session that establishes a known mechanism (so section_2 carries a
    known_mechanism dict with its validation_status)."""
    return _session(
        "IoT greenhouse temperature sensor with automated relay control",
        "Greenhouse monitors require manual calibration every 6 hours causing crop loss",
        "TMP117 digital temperature sensor connected to ESP32 via I2C triggers a relay at threshold",
        "Operating range -10 to 50 Celsius, IP65 enclosure, 3.3V battery, 72-hour life",
        "Sampling 0.1Hz, MQTT to local broker, single greenhouse zone standalone",
    )


def _stage3_state():
    """Build a state carrying one Stage-3 reasoning gap with captured REASONED
    (but unvalidated) evidence, through the committed Gap/Evidence API. Lets the
    label-preservation matrix assert on a real labeled Stage-3 claim."""
    s = _fresh_state("greenhouse temperature sensor")
    g = Gap(gap_type=PROBLEM_MECHANISM_FIT, status=PARTIAL, opened_at=1)
    g.evidence.append(Evidence(
        content="Inventor's structured rationale for the problem-mechanism fit.",
        quality=REASONED, iteration=1,
        provenance="OWNER_INPUT", validation_status="UNVALIDATED",
    ))
    s.gaps.append(g)
    return s


def _package(idea="IoT greenhouse temperature sensor with relay control", *inputs):
    if not inputs:
        inputs = (
            "Greenhouse monitors require manual calibration every 6 hours",
            "TMP117 sensor via ESP32 I2C triggers relay at threshold",
        )
    return assemble_deliverable(_session(idea, *inputs))


def _template_source():
    with open(_TEMPLATE_PATH, encoding="utf-8") as fh:
        return fh.read()


def _assembler_source():
    with open(_ASSEMBLER_PATH, encoding="utf-8") as fh:
        return fh.read()


def _iter_evidence_views(package):
    """Yield every evidence-view dict rendered under section_9 items."""
    for item in package["section_9_stage3_reasoning"]["items"]:
        for ev in item.get("evidence", []):
            yield ev


# ================================================================================
# 1. TRACEABILITY  (guards C6-R2 / C6-R3)  — expected PASS now
# ================================================================================
def test_traceability_only_canonical_sections_are_emitted():
    """No section beyond the fourteen canonical, provenance-anchored sections is
    emitted: nothing rendered can originate outside an existing derivation."""
    pkg = _package()
    emitted = tuple(k for k in pkg if k.startswith("section_"))
    assert emitted == CANONICAL_SECTION_KEYS


def test_traceability_every_section_is_rendered_by_template():
    """Every produced section key is referenced by the committed template, so no
    produced section is silently dropped and none is rendered without a producer."""
    src = _template_source()
    missing = [k for k in CANONICAL_SECTION_KEYS if k not in src]
    assert missing == [], f"sections produced but not rendered: {missing}"


def test_traceability_no_orphan_toplevel_keys():
    """The full top-level key set is exactly envelope + 14 sections + _session_meta;
    a redesign may add none silently."""
    pkg = _package()
    assert set(pkg) == set(ENVELOPE_KEYS) | set(CANONICAL_SECTION_KEYS) | {"_session_meta"}


# ================================================================================
# 2. LABEL-PRESERVATION  (guards C6-R4)  — expected PASS now
# ================================================================================
def test_label_preservation_meta_carries_maturity_label():
    meta = _package()["_session_meta"]
    assert meta.get("maturity_label")
    assert meta["maturity_label"] == _MATURITY_LABEL_FOR(meta["maturity_level"])


def _MATURITY_LABEL_FOR(level):
    from engine.deliverable_assembler import _MATURITY_LABELS
    return _MATURITY_LABELS.get(level, "Unknown")


def test_label_preservation_stage3_evidence_quality_and_validation_separated():
    """Increment 2 core honesty: each Stage-3 evidence view carries BOTH a quality
    axis (quality/quality_label) AND a separate validation axis
    (validation_status/validation_label); quality never stands in for validation."""
    out = _s9(_stage3_state())
    assert out["items"], "expected a Stage-3 reasoning item"
    ev = out["items"][0]["evidence"][0]
    for field in ("quality", "quality_label", "validation_status", "validation_label"):
        assert field in ev, f"evidence view missing {field}"
    # REASONED quality must NOT be presented as validated.
    assert ev["quality"] == REASONED
    assert ev["validation_status"] == "UNVALIDATED"
    assert "not validated" in ev["validation_label"].lower()


def test_label_preservation_stage3_status_label_present():
    out = _s9(_stage3_state())
    item = out["items"][0]
    assert item.get("status_label")


def test_label_preservation_gaps_detail_carry_status_label():
    """section_3 capability gap rows carry a human-readable status_label.

    Tightened (review caveat C2): the fixture must actually yield at least one
    ``gaps_detail`` row, so the per-row ``status_label`` assertion is exercised on a
    real row rather than passing vacuously on an empty capability/gap set."""
    pkg = _package()
    rows = pkg["section_3_assessment_overview"]["capabilities_assessed"]
    detailed = [d for r in rows for d in r.get("gaps_detail", [])]
    assert detailed, "fixture produced no capability gaps_detail rows to check"
    for d in detailed:
        assert "status_label" in d


def test_label_preservation_known_mechanism_keeps_validation_status():
    """A Level>=1 ``_mechanism_session`` establishes a known mechanism; that mechanism
    must keep its ``validation_status`` label (Increment 2 honesty).

    Tightened (review caveat C2): the test now asserts the known-mechanism path is
    actually exercised (``known_mechanism`` is a dict), failing clearly if the fixture
    stops producing a mechanism instead of passing vacuously on a ``None`` mechanism."""
    pkg = assemble_deliverable(_mechanism_session())
    km = pkg["section_2_invention_summary"]["known_mechanism"]
    assert km is not None, (
        "fixture no longer exercises the known-mechanism path "
        "(_mechanism_session was expected to establish a known_mechanism dict)"
    )
    assert "validation_status" in km


def test_label_preservation_stage9_not_validation_note_preserved():
    note = _package()["section_9_stage3_reasoning"]["note"]
    assert "not validation" in note.lower()


# ================================================================================
# 3. NO-UPGRADE  (guards C6-R4)  — expected PASS now
# ================================================================================
def test_no_upgrade_derived_verified_ready_is_a_separate_meta_key():
    """derived_verified_ready is surfaced separately from stored maturity and from
    legacy deliverable_eligible; the three are distinct keys."""
    meta = _package()["_session_meta"]
    for k in ("derived_verified_ready", "deliverable_eligible", "maturity_level"):
        assert k in meta
    assert isinstance(meta["derived_verified_ready"], bool)


def test_no_upgrade_long_causal_owner_answer_not_rendered_verified():
    """A long, causal, entirely inventor-authored answer with no external validation
    must NOT flip derived_verified_ready to True (length/causality != verification)."""
    long_causal = (
        "Because the greenhouse loses heat rapidly at night, therefore the sensor "
        "must trigger the relay so that the heater engages; consequently crop loss "
        "is avoided because the temperature stays stable, which means the mechanism "
        "works since the relay closes the control loop and thus the design succeeds."
    )
    s = _session(
        "greenhouse temperature sensor",
        "greenhouse monitors need manual calibration causing crop loss",
        long_causal,
        "TMP117 sensor via ESP32 I2C triggers relay at threshold",
    )
    meta = assemble_deliverable(s)["_session_meta"]
    assert meta["derived_verified_ready"] is False


def test_no_upgrade_zero_maturity_not_eligible_and_not_verified():
    pkg = assemble_deliverable(_fresh_state())  # maturity 0, no iterations
    meta = pkg["_session_meta"]
    assert meta["deliverable_eligible"] is False
    assert meta["derived_verified_ready"] is False


# ================================================================================
# 4. BACKWARD-COMPATIBILITY  (guards C6-R7)  — expected PASS now
# ================================================================================
def test_backward_compat_schema_id_and_version_preserved():
    pkg = _package()
    assert pkg["schema_id"] == SCHEMA_ID == "fdc-001-mvp-v1"
    assert pkg["package_version"] == PACKAGE_VERSION


def test_backward_compat_all_envelope_and_section_keys_present():
    pkg = _package()
    for k in ENVELOPE_KEYS:
        assert k in pkg and pkg[k]
    for k in CANONICAL_SECTION_KEYS:
        assert k in pkg
    assert "_session_meta" in pkg


def test_backward_compat_absent_data_branch_keys_present_in_s2():
    """The template's absent-data branch (known_problem vs known_problem_note) is
    backed by both keys in section_2 regardless of session depth."""
    s2 = _package()["section_2_invention_summary"]
    assert "known_problem" in s2
    assert "known_problem_note" in s2


def test_backward_compat_section_11_shared_and_per_experiment_expertise():
    """section_11 keeps the additive shared_required_expertise field AND, for any
    emitted experiment, the fdc-001-mvp-v1 per-experiment required_expertise_or_tools
    field (schema output contract not altered)."""
    s11 = _package()["section_11_prototype_test_plan"]
    assert "shared_required_expertise" in s11
    for exp in s11.get("items", []):
        assert "required_expertise_or_tools" in exp


# ================================================================================
# 5. PROTECTED-BOUNDARY  (guards C6-R8)  — expected PASS now
# ================================================================================
def test_protected_boundary_assemble_does_not_mutate_state():
    s = _session(
        "smart irrigation sensor",
        "soil moisture sensor triggers relay",
    )
    before = (s.iteration, s.maturity_level, len(s.gaps), s.domain_signal)
    assemble_deliverable(s)
    after = (s.iteration, s.maturity_level, len(s.gaps), s.domain_signal)
    assert before == after


def test_protected_boundary_scoring_not_imported_or_emitted():
    """The deliverable assembler must not touch scoring: score_case remains
    importable (unchanged surface) and the assembler neither imports scoring nor
    emits any scoring key into the package."""
    from engine.scoring import score_case  # importable => surface intact
    assert callable(score_case)
    src = _assembler_source()
    assert "engine.scoring" not in src
    assert "score_case" not in src
    pkg = _package()
    assert "score" not in pkg
    assert "weighted_score" not in json.dumps(pkg)


def test_protected_boundary_s6_zero_maturity_high_risk_parity():
    """_s6 risk semantics unchanged: a maturity-0 state still yields >=1 high-severity
    risk (parity with the existing deliverable-assembler acceptance behavior)."""
    pkg = assemble_deliverable(_fresh_state())
    highs = [r for r in pkg["section_6_risks"]["risks"] if r["severity"] == "high"]
    assert len(highs) >= 1


def test_protected_boundary_no_domain_registry_dependency():
    """The assembler documents and maintains 'No registry dependency'."""
    src = _assembler_source()
    assert "load_registry" not in src
    assert "domain_registry" not in src


# ================================================================================
# 6. NO-PERSISTENCE  (guards C6-R6)  — expected PASS now
# ================================================================================
def test_no_persistence_no_frozen_artifact_reference():
    """Neither the assembled package nor the assembler source references the paused
    frozen persistence artifact aec9cf6."""
    assert _FROZEN_ARTIFACT not in json.dumps(_package(), default=str)
    assert _FROZEN_ARTIFACT not in _assembler_source()


def test_no_persistence_no_write_or_resume_semantics_in_assembler():
    """The assembler performs no file write and encodes no session-resumption."""
    src = _assembler_source()
    assert 'open(' not in src            # no file handle opened
    assert "resume" not in src.lower()
    assert "session_store" not in src.lower()


def test_no_persistence_assembly_is_deterministic_and_ephemeral():
    """Two assemblies of the same state are identical except for the volatile
    generated_at timestamp — the deliverable is render-time/ephemeral, not stored."""
    s = _session(
        "greenhouse temperature sensor",
        "greenhouse monitors need calibration",
        "TMP117 sensor triggers relay",
    )
    a = assemble_deliverable(s)
    b = assemble_deliverable(s)
    a2, b2 = copy.deepcopy(a), copy.deepcopy(b)
    a2.pop("generated_at"), b2.pop("generated_at")
    assert a2 == b2
    assert a["session_id"] == b["session_id"] == s.idea_id


# ================================================================================
# 7. NO-NEW-TRUTH / NO-GENERATION  (guards C6-R2 and design §4 improvement B)
#     — expected PASS now
# ================================================================================
def test_no_new_truth_validation_plan_proposes_nothing_verified():
    """section_14 proposes validation; it never marks itself verified/validated."""
    s14 = _package("IoT greenhouse temperature sensor with relay",
                   "greenhouse monitors need calibration causing crop loss",
                   "TMP117 sensor via ESP32 I2C triggers relay at threshold",
                   "range -10 to 50C IP65 3.3V battery 72h")["section_14_validation_plan"]
    assert s14["outcome"] in {"PLAN", "EMPTY", "BLOCKED"}
    # Tightened (review caveat C2): the deep fixture must actually reach the proposal
    # path (a PLAN carrying at least one step), so the "proposes nothing verified"
    # property is exercised against real steps instead of passing vacuously on an
    # empty/blocked plan with no steps to inspect.
    assert s14["outcome"] == "PLAN", (
        "fixture no longer exercises the validation-plan proposal path "
        f"(expected outcome PLAN, got {s14['outcome']!r})"
    )
    assert s14.get("steps"), "expected the PLAN to carry at least one proposed step"
    for step in s14["steps"]:
        # steps are proposals carrying responsibility/confidence, not verdicts
        assert "responsibility" in step
        assert step.get("outcome") not in {"VERIFIED", "VALIDATED"}


def test_no_new_truth_recommendation_section_carries_no_injected_validation_link():
    """Improvement-B (structural): section_7 keeps exactly its four categories; the
    presence of the validation plan (section_14) injects no verified/validated
    cross-link key into the recommendation section."""
    s7 = _package()["section_7_recommendations"]
    assert set(s7) == {
        "category_a_proceed_revise_block",
        "category_b_material_selection",
        "category_c_manufacturing",
        "category_d_open_items",
    }
    # No key injects a cross-link to the validation plan (section_14) or asserts the
    # recommendation is "validated". (The honest Increment 2 field
    # ``derived_verified_ready`` legitimately embeds the substring "verified"; a
    # keyword scan would false-positive, so we assert on structure instead.)
    blob = json.dumps(s7).lower()
    assert "section_14" not in blob
    assert "validation_plan" not in blob
    assert "validated" not in blob


def test_no_new_truth_package_is_json_serialisable():
    """A pure-derivation package must be fully JSON-serialisable (no live objects,
    no generated side-channel)."""
    assert json.dumps(_package(), default=str)


# ================================================================================
# REDESIGN PRESENTATION EXPECTATIONS  — EXPECTED RED (SOURCE NOT YET AUTHORIZED)
#   These assert the design §4 inventor-facing grouping that the future
#   TEMPLATE-ONLY redesign will introduce. They fail today because that grouping
#   is not yet in web/templates/deliverable.html. Do NOT satisfy them by editing
#   product code in this tests-first phase.
# ================================================================================
def test_redesign_all_seven_group_headings_present():
    """EXPECTED RED — SOURCE NOT YET AUTHORIZED.
    The redesigned deliverable presents the fourteen sections under the seven
    design §4 inventor-facing group headings, in reading order."""
    src = _template_source()
    missing = [h for h in REDESIGN_GROUP_HEADINGS if h not in src]
    assert missing == [], (
        "EXPECTED RED — SOURCE NOT YET AUTHORIZED: missing redesign group "
        f"headings {missing}"
    )


def test_redesign_reading_order_needs_group_before_risks_group():
    """EXPECTED RED — SOURCE NOT YET AUTHORIZED.
    Design §4 reading order: 'What it needs' (requirements + requirement landscape)
    precedes 'What could go wrong' (risks)."""
    src = _template_source()
    assert "What it needs" in src and "What could go wrong" in src, (
        "EXPECTED RED — SOURCE NOT YET AUTHORIZED: redesign groups absent"
    )
    assert src.index("What it needs") < src.index("What could go wrong")


def test_redesign_needs_group_colocates_requirements_and_landscape():
    """EXPECTED RED — SOURCE NOT YET AUTHORIZED.
    Under 'What it needs', section_4 (requirements) and section_13 (requirement
    landscape) are grouped together (design §5 mapping, Group 3)."""
    src = _template_source()
    assert "What it needs" in src, (
        "EXPECTED RED — SOURCE NOT YET AUTHORIZED: 'What it needs' group absent"
    )
    start = src.index("What it needs")
    nxt = min(
        (src.index(h) for h in REDESIGN_GROUP_HEADINGS if h in src and src.index(h) > start),
        default=len(src),
    )
    group = src[start:nxt]
    assert "section_4_requirements" in group
    assert "section_13_requirement_landscape" in group


def test_redesign_honest_status_strip_separate_from_maturity():
    """EXPECTED RED — SOURCE NOT YET AUTHORIZED.
    Design §4/§7: the honest ``_session_meta`` signals — the stored maturity label AND
    the Increment 2 ``derived_verified_ready`` readiness signal — are surfaced together
    in a small honest status strip, presented SEPARATELY from each other and never
    merged into one 'resolved/verified' impression.

    Asserted SEMANTICALLY (review caveat C1). The design describes the honest status
    strip conceptually; it does NOT mandate any specific CSS class or the literal words
    'status strip', so this test no longer requires that phrase. It requires only the
    design's actual semantic outcome: both honest signals surfaced as two DISTINCT,
    design-named ``_session_meta`` fields (``maturity_label`` and
    ``derived_verified_ready``) CO-LOCATED in one small strip. Today the template
    renders ``maturity_label`` deep inside the Invention Summary body and uses
    ``derived_verified_ready`` only as a hidden branch guard ~3.6k characters away — the
    two honest signals are not co-surfaced as one strip — so this is EXPECTED RED until
    the TEMPLATE-ONLY redesign introduces that strip.
    """
    src = _template_source()
    # Both honest _session_meta signals must be surfaced by the template at all.
    assert "maturity_label" in src, (
        "EXPECTED RED — SOURCE NOT YET AUTHORIZED: stored maturity label not surfaced"
    )
    assert "derived_verified_ready" in src, (
        "EXPECTED RED — SOURCE NOT YET AUTHORIZED: derived_verified_ready readiness "
        "signal not surfaced"
    )
    # ...and the two distinct signals must be CO-LOCATED in a single small honest status
    # strip (shown separately, not merged into one verified/resolved label). A generous
    # character window keeps the check class-name/phrase-agnostic while still failing
    # today's ~3.6k-character separation across two different section bodies.
    STRIP_WINDOW = 800
    maturity_at = src.index("maturity_label")
    verified_at = src.index("derived_verified_ready")
    assert abs(maturity_at - verified_at) <= STRIP_WINDOW, (
        "EXPECTED RED — SOURCE NOT YET AUTHORIZED: the honest maturity and "
        "derived_verified_ready signals are not yet co-located in one honest status "
        "strip (still presented far apart in separate section bodies)"
    )


if __name__ == "__main__":
    # Fallback self-runner so results can be classified even without the pytest
    # CLI. Prefer `pytest tests/test_increment_6_deliverable_redesign.py`.
    import traceback
    fns = sorted(
        (n, f) for n, f in globals().items()
        if n.startswith("test_") and callable(f)
    )
    passed, failed = [], []
    for name, fn in fns:
        try:
            fn()
            passed.append(name)
            print(f"PASS  {name}")
        except Exception:
            failed.append(name)
            print(f"FAIL  {name}")
            traceback.print_exc()
    print(f"\n{len(passed)} passed, {len(failed)} failed")
    print("RED (expected, source not yet authorized):",
          [n for n in failed if n.startswith("test_redesign_")])
    print("UNEXPECTED failures:",
          [n for n in failed if not n.startswith("test_redesign_")])
    sys.exit(1 if any(not n.startswith("test_redesign_") for n in failed) else 0)
