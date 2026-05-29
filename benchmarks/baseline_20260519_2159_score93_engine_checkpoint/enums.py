"""
engine/enums.py
Canonical enum definitions. Treat changes as contract changes.
DECISION_SIGNALS_VERSION = "v1"
"""

DECISION_SIGNALS_VERSION = "v1"

ENUM_MAP = {
    "confidence_level": ["LOW","MEDIUM","HIGH"],
    "feasibility_signal": ["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS",
                           "FEASIBILITY_UNCLEAR","SIGNIFICANT_CONCERNS_IDENTIFIED","INSUFFICIENT_INPUT"],
    "prototype_path_clarity": ["DESCRIBED_PATH_EXISTS","PARTIAL_PATH_ONLY","INSUFFICIENT_INFO"],
    "component_specificity": ["USER_SPECIFIED","CLEARLY_IMPLIED_TYPE","UNCLEAR"],
}

ALLOWED_FEASIBILITY_SIGNALS = ENUM_MAP["feasibility_signal"]
ALLOWED_CONFIDENCE_LEVELS   = ENUM_MAP["confidence_level"]
