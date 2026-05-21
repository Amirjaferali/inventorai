"""
run_summary_demo.py — C phase acceptance test. No API calls.
"""
import json, sys
sys.path.insert(0, '.')

from engine.idea_state import (
    IdeaState, Evidence, Gap, IterationLog,
    OPEN, PARTIAL, CLOSED,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS,
    PROGRESSING, ASSERTED, REASONED,
)
from engine.summary import build_summary


def build_tc01_state() -> IdeaState:
    state = IdeaState(idea_id="TC-01")
    state.domain_signal  = "electronics"
    state.maturity_level = 2
    state.direction      = PROGRESSING

    state.known_problem   = Evidence(
        content="Wearable temp monitors drain battery within 6h and need manual calibration.",
        quality=REASONED,
        iteration=1
    )
    state.known_mechanism = Evidence(
        content="ESP32 + TMP117 at 0.1Hz with delta-compression firmware → 72h battery life.",
        quality=ASSERTED,
        iteration=2
    )

    state.gaps = [
        Gap(gap_type=PHYSICAL_FEASIBILITY,   status=CLOSED,  opened_at=1, iterations_open=0, closed_at=1),
        Gap(gap_type=MECHANISM_COMPLETENESS, status=PARTIAL, opened_at=1, iterations_open=1),
        Gap(gap_type=BOUNDARY_AMBIGUITY,     status=OPEN,    opened_at=1, iterations_open=2),
    ]

    state.iteration_log = [
        IterationLog(
            iteration=1,
            gap_targeted=PHYSICAL_FEASIBILITY,
            question_asked="What is the power source and target battery life?",
            response_summary="USB-C LiPo 3.7V 500mAh; target 72h continuous.",
            gaps_changed=[PHYSICAL_FEASIBILITY],
            maturity_before=1, maturity_after=1
        ),
        IterationLog(
            iteration=2,
            gap_targeted=MECHANISM_COMPLETENESS,
            question_asked="Describe HOW the device maintains accuracy over 72h.",
            response_summary="Delta-compression + TMP117 auto-calibration every 30min.",
            gaps_changed=[MECHANISM_COMPLETENESS],
            maturity_before=1, maturity_after=2
        ),
    ]
    return state


def verify(summary: dict) -> bool:
    checks = {
        "maturity_level present":       "maturity_level" in summary,
        "known_problem present":        bool(summary.get("known_problem")),
        "known_mechanism present":      bool(summary.get("known_mechanism")),
        "known_boundaries present":     "known_boundaries" in summary,
        "open_gaps non-empty":          len(summary.get("open_gaps", [])) > 0,
        "next_recommended_step set":    bool(summary.get("next_recommended_step")),
        "no API (generated_at exists)": "generated_at" in summary,
    }
    print("\n── Acceptance Criteria ──────────────────────")
    ok = True
    for label, passed in checks.items():
        print(f"  [{'✓' if passed else '✗ FAIL'}] {label}")
        if not passed: ok = False
    return ok


def main():
    print("=== InventorAI — run_summary_demo (C phase) ===\n")
    state   = build_tc01_state()
    summary = build_summary(state)
    print("── Full JSON Summary ────────────────────────")
    print(json.dumps(summary, indent=2, default=str))
    ok = verify(summary)
    print("\n─────────────────────────────────────────────")
    print("✓ All criteria passed. Ready to commit." if ok else "✗ Fix failures before commit.")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
