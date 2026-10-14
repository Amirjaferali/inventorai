"""MEASUREMENT-PLAN-GUIDANCE-01 (C1) — the exact identity of this one addition, shared
by the earlier CAP-01 suites so that each of them excludes exactly this addition (and
nothing more) from its own base-digest and inventory checks.

The addition is pinned by tests/test_measurement_plan_guidance_c1.py. It is a
CAP-09-page-only guidance group: NOT a row of ``CAP01_GAP_FUNDAMENTALS_EXTENSIONS`` and
never a report / PDF gap-context group, so it has no ROW and no SLUG in the report.
"""
import copy

DOMAIN = "electronics_electrical"
MGUIDE_GROUP = "measurement_quantity_versus_condition_reference_v1"
MGUIDE_CLAIM = "measured_quantity_versus_observed_condition"
MGUIDE_CLAIMS = (MGUIDE_CLAIM,)
MGUIDE_NOTE = "measurement_quantity_versus_condition_reference"
MGUIDE_STEM = "UI_CAP09_MEASUREMENT_PLANNING_GUIDANCE_V1_"
MGUIDE_SLUG = "measurement-quantity-versus-condition-reference-v1"
MGUIDE_RECORDS = ("electronics_electrical:PR022", "electronics_electrical:PR023")


def without_measurement_guidance_addition(pack):
    """A deep copy of the Electronics pack with exactly this addition undone: its
    reference group and its governance note."""
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre.get("reference_fundamentals", [])
                                     if g["group_id"] != MGUIDE_GROUP]
    pre["_governance_notes"].pop(MGUIDE_NOTE)
    return pre
