"""
test_gap_labels.py — Stage 3 gap-label mapping contract test.

Scope: web/gap_labels.py GAP_LABELS dictionary and get_gap_label() only.
No Flask app, no session, no SID, no filesystem mutation.
"""

import pytest
from web.gap_labels import GAP_LABELS, get_gap_label

STAGE3_GAPS = [
    "PROBLEM_MECHANISM_FIT",
    "ASSUMPTION_INVENTORY",
    "EXPERTISE_GAP_AWARENESS",
]

REQUIRED_KEYS = {"heading", "guidance", "stage_note"}

EXPECTED_LABELS = {
    "PROBLEM_MECHANISM_FIT": {
        "heading": "How does your idea address the problem?",
        "guidance": (
            "Describe the problem on its own terms first — who experiences it "
            "and why it matters — without describing your idea. Then explain how "
            "your idea is intended to address that problem, and identify situations "
            "where the match may be weaker."
        ),
        "stage_note": "Checking problem fit",
    },
    "ASSUMPTION_INVENTORY": {
        "heading": "What are you assuming that hasn't been tested yet?",
        "guidance": (
            "List anything you are taking for granted about your idea that you "
            "have not yet verified — materials, conditions, or behaviors you "
            "expect to hold true. Then note which of these would be most "
            "serious if they turned out to be wrong."
        ),
        "stage_note": "Surfacing assumptions",
    },
    "EXPERTISE_GAP_AWARENESS": {
        "heading": "What expertise would building this require?",
        "guidance": (
            "List the areas of technical knowledge someone would need to build "
            "your idea — not what you personally know, but what the implementation "
            "itself demands. Then identify which areas require specialist input."
        ),
        "stage_note": "Identifying expertise needs",
    },
}


class TestStage3GapLabelsPresent:

    @pytest.mark.parametrize("gap_type", STAGE3_GAPS)
    def test_gap_has_dedicated_entry_not_default(self, gap_type):
        label = get_gap_label(gap_type)
        assert label != GAP_LABELS["__default__"], (
            f"{gap_type} falls through to __default__ — no dedicated label."
        )

    @pytest.mark.parametrize("gap_type", STAGE3_GAPS)
    def test_gap_has_exact_required_keys(self, gap_type):
        label = get_gap_label(gap_type)
        assert set(label.keys()) == REQUIRED_KEYS, (
            f"{gap_type} label key set mismatch: {set(label.keys())}"
        )

    @pytest.mark.parametrize("gap_type", STAGE3_GAPS)
    def test_gap_label_exact_approved_wording(self, gap_type):
        label = get_gap_label(gap_type)
        expected = EXPECTED_LABELS[gap_type]
        assert label["heading"] == expected["heading"]
        assert label["guidance"] == expected["guidance"]
        assert label["stage_note"] == expected["stage_note"]


class TestUnknownGapStillDefaults:

    def test_unknown_gap_type_returns_default(self):
        label = get_gap_label("SOME_UNKNOWN_GAP_TYPE")
        assert label == GAP_LABELS["__default__"]
