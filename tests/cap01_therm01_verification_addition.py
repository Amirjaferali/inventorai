"""THERM01-VERIFICATION-MEASUREMENT-STEP-01 — the exact identity of this one addition,
shared by the earlier CAP-01 / CAP-09 suites so that each of them excludes exactly this
addition (and nothing more) from its own base-digest and inventory checks.

The addition is pinned by tests/test_therm01_verification_measurement_step.py. It is a
THERM-01-page-only verification-preparation group: NOT a row of
``CAP01_GAP_FUNDAMENTALS_EXTENSIONS``, never a report / PDF gap-context group and never a
CAP-09 group, so it has no ROW and no report SLUG.
"""
import copy

DOMAIN = "electronics_electrical"
TVM_GROUP = "therm01_verification_measurement_reference_v1"
TVM_CLAIM = "thermal_resistance_measurement_requirements"
TVM_CLAIMS = (TVM_CLAIM,)
TVM_NOTE = "therm01_verification_measurement_reference"
TVM_STEM = "UI_THERM01_VERIFY_V1_"
TVM_SLUG = "therm01-verification-measurement-reference-v1"
TVM_RECORDS = ("electronics_electrical:PR028", "electronics_electrical:PR029")


def without_therm01_verification_addition(pack):
    """A deep copy of the Electronics pack with exactly this addition undone: its
    reference group and its governance note."""
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre.get("reference_fundamentals", [])
                                     if g["group_id"] != TVM_GROUP]
    pre["_governance_notes"].pop(TVM_NOTE)
    return pre
