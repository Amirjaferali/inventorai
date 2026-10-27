"""28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01 — the exact identity of this one addition,
shared by the earlier CAP-01 / CAP-09 suites so that each of them excludes exactly this
addition (and nothing more) from its own base-digest and inventory checks.

The addition is pinned by tests/test_cap01_load_switching_reference.py.
"""
import copy

DOMAIN = "electronics_electrical"
LSW_GROUP = "transistor_load_switching_reference_v1"
LSW_CLAIM = "bjt_current_controlled_load_switching"
LSW_NOTE = "transistor_load_switching_reference"
LSW_NAMESPACE = "LOAD_SWITCHING_FUNDAMENTALS_"
LSW_ROW = (LSW_GROUP, (LSW_CLAIM,), LSW_NAMESPACE)
LSW_SLUG = "transistor-load-switching-reference-v1"
LSW_RECORDS = ("electronics_electrical:PR026", "electronics_electrical:PR027")


def without_load_switching_addition(pack):
    """A deep copy of the Electronics pack with exactly this addition undone: its
    reference group and its governance note (no coverage-declaration change exists)."""
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre.get("reference_fundamentals", [])
                                     if g["group_id"] != LSW_GROUP]
    pre["_governance_notes"].pop(LSW_NOTE)
    return pre
