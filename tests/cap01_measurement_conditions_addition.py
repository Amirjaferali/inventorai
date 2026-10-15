"""MEASUREMENT-CONDITIONS-AWARENESS-01 — the exact identity of this one addition, shared
by the earlier CAP-01 / CAP-09 suites so that each of them excludes exactly this addition
(and nothing more) from its own base-digest and inventory checks.

The addition is pinned by tests/test_measurement_conditions_awareness.py. It is a
CAP-09-page-only guidance group: NOT a row of ``CAP01_GAP_FUNDAMENTALS_EXTENSIONS`` and
never a report / PDF gap-context group, so it has no ROW and no report SLUG.
"""
import copy

DOMAIN = "electronics_electrical"
MCOND_GROUP = "measurement_conditions_awareness_reference_v1"
MCOND_CLAIM = "conditions_of_use_affect_measurement"
MCOND_CLAIMS = (MCOND_CLAIM,)
MCOND_NOTE = "measurement_conditions_awareness_reference"
MCOND_STEM = "UI_CAP09_MEASUREMENT_CONDITIONS_V1_"
MCOND_SLUG = "measurement-conditions-awareness-reference-v1"
MCOND_RECORDS = ("electronics_electrical:PR024", "electronics_electrical:PR025")


def without_measurement_conditions_addition(pack):
    """A deep copy of the Electronics pack with exactly this addition undone: its
    reference group and its governance note."""
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre.get("reference_fundamentals", [])
                                     if g["group_id"] != MCOND_GROUP]
    pre["_governance_notes"].pop(MCOND_NOTE)
    return pre
