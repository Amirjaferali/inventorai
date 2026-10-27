"""MEASUREMENT-PLANNING-INTEGRATED-PART-01 — the exact identity of this one scope
amendment of the Electronics pack, shared by the earlier CAP-01 / CAP-09 suites so
that each of them undoes exactly this amendment (and nothing more) before its own
base-digest check.

The amendment adds ONE parenthesis to the CAP-09 eligibility sentence of exactly
two existing governance notes (the C1 guidance and the conditions awareness); no
group, claim, source record or other note changes. It is pinned by
tests/test_measurement_planning_integrated_part.py.
"""
import copy

AMENDED_NOTES = ("measurement_quantity_versus_condition_reference",
                 "measurement_conditions_awareness_reference")
AMENDMENT = (" (amended by MEASUREMENT-PLANNING-INTEGRATED-PART-01: also for the "
             "inventor-declared Electrical / Electronics part of a valid durable "
             "integrated composition, whatever the initial analysis focus, with that "
             "part named; this says nothing about any experiment, sensing need or "
             "technical assessment)")
ANCHOR = "for a project whose trusted durable root domain is exactly electronics_electrical, independent of gap state"


def without_measurement_planning_integrated_part_amendment(pack):
    """A deep copy of the Electronics pack with exactly this amendment undone: the
    one parenthesis removed from each of the two amended notes (a note already
    removed by an earlier suite's own undo is skipped)."""
    pre = copy.deepcopy(pack)
    notes = pre["_governance_notes"]
    for key in AMENDED_NOTES:
        if key in notes:
            assert notes[key].count(ANCHOR + AMENDMENT) == 1, key
            notes[key] = notes[key].replace(ANCHOR + AMENDMENT, ANCHOR)
    return pre
