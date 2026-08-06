# WS6 Evidence — Protected and Full Regression Record

All commands run at HEAD 4f89d1ae... (clean tree).

1) Focused: python3 -m pytest tests/test_requirement_landscape_synthesis.py
   -> 12 passed.
2) Affected compatibility suites: python3 -m pytest
   tests/test_structured_criticality.py
   tests/test_phase_7b_validation_plan_collapse.py
   tests/test_phase_7c_requirement_landscape_collapse.py
   -> 34 passed (18 + 9 + 7).
3) Contract-listed protected battery: python3 -m pytest
   tests/test_increment_4_requirement_landscape.py (39)
   tests/test_phase_7c_requirement_landscape_collapse.py (7)
   tests/test_phase_4a_requirements_heading.py (8)
   tests/test_increment_5_validation_plan.py (55)
   tests/test_phase_7a_validation_plan_grouping.py (9)
   tests/test_phase_7b_validation_plan_collapse.py (9)
   tests/test_deliverable_hygiene.py (22)
   tests/test_structured_criticality.py (18)
   tests/test_unified_risk_safety_presentation.py (17)
   tests/test_safety_signal.py (18)
   tests/test_safety_signal_stabilization.py (15)
   tests/test_wps001_invariants.py (21)
   tests/test_requirement_landscape_synthesis.py (12)
   -> 249 passed, 1 skipped. The single skip is the pre-existing baseline
   skip tests/test_wps001_invariants.py::TestWPS001_INV004_GapLifecycle::
   test_closed_gap_does_not_reopen (unchanged by Workstream 6).
4) Full suite: python3 -m pytest tests/
   -> 31 failed, 1408 passed, 1 skipped, 1 xfailed, 24 xpassed.
   Mechanical confinement proof:
     pytest tests/ | grep ^FAILED | grep -vc test_domain_registry.py -> 0
     pytest tests/ | grep ^FAILED | grep -c  test_domain_registry.py -> 31
   The 31 failures are the preserved pre-existing tests/test_domain_registry.py
   baseline — NOT introduced, corrected, or reclassified by Workstream 6.
   Passed count = canonical baseline 1396 + the 12 new focused tests = 1408.
   No new failure, no new skip, no new xfail. The full suite does NOT pass
   completely; no such claim is made.
