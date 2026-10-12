"""ELECTRICAL-CHARGE-AMPERE-HOUR-REFERENCE-01 — the exact identity of this one
addition, shared by the earlier CAP-01 suites so that each of them excludes exactly
this addition (and nothing more) from its own base-digest and inventory checks.

The addition is pinned by tests/test_cap01_electric_charge_reference.py.
"""
import copy

DOMAIN = "electronics_electrical"
CHARGE_GROUP = "electric_charge_reference_v1"
CHARGE_CLAIMS = ("charge_current_time_reference", "charge_unit_discipline", "ampere_hour_charge_unit")
CHARGE_NOTE = "electric_charge_reference"
CHARGE_NAMESPACE = "CHARGE_FUNDAMENTALS_"
CHARGE_ROW = (CHARGE_GROUP, CHARGE_CLAIMS, CHARGE_NAMESPACE)
CHARGE_SLUG = "electric-charge-reference-v1"
CHARGE_RECORDS = tuple("electronics_electrical:PR%03d" % n for n in (18, 19, 20, 21))
CHARGE_EQUATIONS = ("Q = I × t", "C = A · s", "1 A · h = 3.6 × 10³ C")


def without_charge_addition(pack):
    """A deep copy of the Electronics pack with exactly this addition undone: its
    reference group and its governance note."""
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre.get("reference_fundamentals", [])
                                     if g["group_id"] != CHARGE_GROUP]
    pre["_governance_notes"].pop(CHARGE_NOTE)
    return pre
