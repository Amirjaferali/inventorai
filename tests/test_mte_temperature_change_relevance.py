"""MTE-TEMPERATURE-CHANGE-RELEVANCE-01 (Increment B) — authority guards.

The free linear thermal-expansion method contract (§1A) and its governed
artifact's ``governance_note`` admit ONE bounded relevance relationship: a
CURRENT valid part temperature-change statement for the same declared
Mechanical Stage-15 part makes this method potentially relevant to examining
possible free dimensional change of that part. It is governance authority
only, with ONE runtime presentation (Increment C, guarded by
``tests/test_mte_temperature_change_discoverability.py``). These guards prove
the admission is exactly that and that the method itself never consumes the
statement; the method's own invariants (identity, declarations,
numeric domain, eligibility, no prefill) stay pinned by
``tests/test_mechanical_thermal_expansion.py`` and the statement's
no-consumer guards by ``tests/test_part_temperature_change_declaration.py``.
"""
import inspect
import json
import re
from pathlib import Path

import web.app as webapp
from engine import mechanical_thermal_expansion as te

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "docs" / "governance" / \
    "MECHANICAL_FREE_LINEAR_THERMAL_EXPANSION_METHOD_CONTRACT.md"

RELATION = ("allows InventorAI to treat this method as potentially relevant to "
            "examining possible free dimensional change of that part")
BOUNDARY = ("This relevance does not establish that the free-expansion model "
            "applies and does not change eligibility")

# Any runtime reading of the part temperature-change statement.
_FACT_TOKENS = ("PartTemperatureChange", "part_temperature_change",
                "load_part_temperature_changes",
                "subsystem_temperature_change_declarations", "_part_tc")


def _flat(text):
    return re.sub(r"\s+", " ", text)


def _section_1a():
    text = CONTRACT.read_text(encoding="utf-8")
    assert text.count("## 1A. Relevance authority") == 1
    start = text.index("## 1A. Relevance authority")
    return _flat(text[start:text.index("\n## 2. ", start)])


def test_contract_admits_exactly_the_one_bounded_relationship():
    section = _section_1a()
    assert "MTE-TEMPERATURE-CHANGE-RELEVANCE-01" in section
    assert "`PART-BOUND-TEMPERATURE-CHANGE-DECLARATION-01`" in section
    assert "OWNER_STATED / UNVALIDATED" in section
    assert "`(project_id, subsystem_id)`" in section
    assert RELATION in section
    assert "if the method's own applicability conditions (§5) are satisfied" in section
    assert BOUNDARY in section
    for kept in ("supply any input", "D-1 to D-8", "pre-select any screen answer",
                 "validate the inventor's statement",
                 "authorize presentation or routing",
                 "give no positive relevance basis", "Runtime: ONE presentation only.",
                 "needs its own Owner authorization"):
        assert kept in section, kept
    # The only scientific basis is the admitted SRC-031 claim.
    assert "SRC-031" in section and "SRC-029" not in section
    # No runtime use beyond the Increment C presentation is admitted.
    assert "any runtime use of the §1A relevance beyond the Increment C session-page presentation" in _flat(
        CONTRACT.read_text(encoding="utf-8"))


def test_governance_note_mirrors_the_relationship_and_artifact_still_validates():
    data = json.loads(te.ARTIFACT_PATH.read_text(encoding="utf-8"))
    note = data["governance_note"]
    assert "contract §1A, MTE-TEMPERATURE-CHANGE-RELEVANCE-01" in note
    assert RELATION in note
    assert BOUNDARY in note
    assert "its one runtime use is the Increment C session-page presentation" in note
    # No generic relationship field was added: the existing loader's exact
    # key set, semantic digests and version still accept the artifact.
    assert te.load_artifact() is not None
    assert data["artifact_version"] == "1"
    assert data["method"]["method_id"] == te.METHOD_ID == \
        "mechanical:free_linear_thermal_expansion"
    assert data["method"]["method_version"] == te.METHOD_VERSION == "1.0"
    assert [d["declaration_id"] for d in data["declarations"]] == [
        "free_unrestrained", "one_material_uniform_temperature",
        "own_coefficient", "coefficient_direction", "average_over_interval",
        "reference_length", "signed_change", "reversible_thermal_change_only"]


def test_no_runtime_surface_of_the_method_reads_the_statement():
    sources = [
        (ROOT / "engine" / "mechanical_thermal_expansion.py").read_text(encoding="utf-8"),
        (ROOT / "engine" / "mechanical_thermal_expansion_method.py").read_text(encoding="utf-8"),
        (ROOT / "engine" / "deterministic_calculation.py").read_text(encoding="utf-8"),
        (ROOT / "engine" / "functional_need_handoff.py").read_text(encoding="utf-8"),
        (ROOT / "web" / "templates" / "mechanical_thermal_expansion.html").read_text(encoding="utf-8"),
    ]
    sources += [inspect.getsource(fn) for fn in (
        webapp._calc_gate, webapp._calc_declared_part, webapp._mte_eligible,
        webapp._mte_link_offered, webapp._mte_result_view,
        webapp.mechanical_thermal_expansion,
        webapp.mechanical_thermal_expansion_post,
        webapp._functional_handoff_view)]
    for src in sources:
        for token in _FACT_TOKENS:
            assert token not in src, token


def test_the_contract_wording_is_not_copied_into_the_ui():
    # The inventor-facing wording is UI_MTE_TC_RELEVANCE (Increment C); the
    # contract's own sentences stay governance text.
    texts = [(ROOT / "web" / "ui_text.py").read_text(encoding="utf-8")]
    texts += [p.read_text(encoding="utf-8")
              for p in (ROOT / "web" / "templates").glob("*.html")]
    for text in texts:
        flat = _flat(text).lower()
        assert "potentially relevant to examining" not in flat
        assert "free dimensional change of that part" not in flat
