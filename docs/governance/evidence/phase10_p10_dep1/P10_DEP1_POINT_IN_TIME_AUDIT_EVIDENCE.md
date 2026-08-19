# P10-DEP1 — Point-in-Time Local Dependency-Audit Evidence

**File path:** `docs/governance/evidence/phase10_p10_dep1/P10_DEP1_POINT_IN_TIME_AUDIT_EVIDENCE.md`
**Purpose:** immutable POINT-IN-TIME evidence of one local dependency audit executed during the
P10-DEP1 gate. **This is NOT a permanent clean bill of health**: vulnerability advisory databases
change over time, so this record proves only what was known at the recorded instant. The formal
production dependency/vulnerability review remains PSRR-time (items 12–13).
**Prohibited:** citing this record as "dependencies are secure", as continuous scanning, as CI
enforcement, or as PSRR satisfaction.

## Audit record — POINT-IN-TIME AUDIT EVIDENCE

```
Repository SHA (base):   8563320b626b8590f10cbf252c9eba0a03b6fbd6  (PR #525 merge, authoritative)
Dependency input:        requirements.txt (the single authoritative declaration)
Dependency input sha256: e0707b647c091e917e82e0456db0be38bef98498264b9583f206c386550e153d
Audit tool:              pip-audit 2.10.1  (local, provider-neutral; OSV/PyPI advisory sources)
Advisory network access: AVAILABLE (PyPI reachable at execution time)
UTC timestamp:           2026-08-19T21:24:47Z (initial run); wrapper re-run 2026-08-19T21:27:11Z
Command:                 python3 -m pip_audit -r requirements.txt   (and via
                         scripts/run_dependency_audit.py, exit preserved verbatim)
Exit status:             0
Direct dependencies:     2  (Flask==3.1.3, pytest==9.1.1)
Total packages scanned:  11 (flask 3.1.3, pytest 9.1.1, pluggy 1.6.0, blinker 1.9.0,
                         click 8.4.2, iniconfig 2.3.0, itsdangerous 2.2.0, jinja2 3.1.6,
                         markupsafe 3.0.3, pygments 2.21.0, werkzeug 3.1.8)
Findings count:          0
Result:                  POINT-IN-TIME AUDIT: ZERO KNOWN FINDINGS AT EXECUTION TIME
pip check:               "No broken requirements found." (exit 0)
```

## Boundaries (binding)

`DEPENDENCY REMEDIATION REQUIRED: NO` at this instant — a later run may differ. No dependency was
upgraded, pinned differently, or replaced by this gate. pip-audit is ENVIRONMENT TOOLING only —
not declared in `requirements.txt`, not imported by any application module. No hosted scanning
vendor, no continuous scanning, no CI enforcement, no automatic remediation exists or is claimed.
Repeat the audit any time with `python3 scripts/run_dependency_audit.py` (network to the advisory
sources required; a network failure is reported and never converted into a clean result).
