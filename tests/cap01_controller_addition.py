"""28-T2-CONTROLLER-INPUT-LOGIC-OUTPUT-REFERENCE-01 — the exact identity of this one
addition, shared by the earlier CAP-01 suites so that each of them excludes exactly
this addition (and nothing more) from its own base-digest and inventory checks.

The addition is pinned by tests/test_cap01_controller_input_logic_output_reference.py.
"""
import copy

DOMAIN = "electronics_electrical"
CTRL_GROUP = "controller_input_logic_output_reference_v1"
CTRL_CLAIM = "controller_input_logic_output"
CTRL_NOTE = "controller_input_logic_output_reference"
CTRL_NAMESPACE = "CONTROLLER_FUNDAMENTALS_"
CTRL_ROW = (CTRL_GROUP, (CTRL_CLAIM,), CTRL_NAMESPACE)
CTRL_SLUG = "controller-input-logic-output-reference-v1"
CTRL_RECORDS = ("electronics_electrical:PR016", "electronics_electrical:PR017")
FIRMWARE_EXCLUSION = ("Firmware and embedded software logic — outside the authority of the current parent "
                      "electronics pack and requires separate governance authorization.")
COVERAGE_EXCEPTION = (" Bounded exception (28-T2-CONTROLLER-INPUT-LOGIC-OUTPUT-REFERENCE-01): ONE concept-level "
                      "reference explanation that a microcontroller-based design can receive inputs, process them "
                      "using programmed logic and command outputs (reference_fundamentals group "
                      "controller_input_logic_output_reference_v1); no other firmware or embedded software guidance "
                      "is covered.")


def without_controller_addition(pack):
    """A deep copy of the Electronics pack with exactly this addition undone: its
    reference group, its governance note and its bounded coverage exception clause."""
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre.get("reference_fundamentals", [])
                                     if g["group_id"] != CTRL_GROUP]
    pre["_governance_notes"].pop(CTRL_NOTE)
    areas = pre["coverage_declaration"]["not_covered_areas"]
    [i] = [n for n, area in enumerate(areas) if area == FIRMWARE_EXCLUSION + COVERAGE_EXCEPTION]
    areas[i] = FIRMWARE_EXCLUSION
    return pre
