# WS1 Future Closure Comparison Requirements

**Document ID:** WS1_CLOSURE_COMPARISON_REQUIREMENTS
**Type:** Evidence-lock closure-comparison definition (Workstream 1, plan §7 item F)
**Status:** RECORDED — binding on all future remediation closures under the plan
**Date:** 2026-07-11

Every remediation workstream closure (plan §12) MUST perform and commit the
following comparison. Passing one example does not establish stability.

## 1. Base defective deliverable

The comparison base is the immutable artifact set in this directory,
regenerated at `f1286c3d9f6dc027de09095eacc41437e405b9a4`:
`deliverable_false_negative.{json,html}` + `journey_log_false_negative.json`
+ `safety_signals_false_negative.json`, produced by `reproduce_baseline.py`
from `inputs_false_negative_journey.json`. These files must never be edited
or regenerated in place.

## 2. Remediated deliverable

After the workstream's merge, re-run `reproduce_baseline.py` (same script,
same verbatim inputs, identifier normalization unchanged) at the post-merge
tip, saving the outputs as NEW files in a NEW evidence directory named for the
workstream (e.g. `workstream2_safety_stabilization/`). The inputs file must be
byte-identical to the Workstream 1 inputs; if a workstream legitimately
changes journey shape (P2 workstreams 8–14), the divergence must be listed
explicitly and owner-approved in that workstream's Increment Contract first.

## 3. Exact target defect

The closure claim must name the defect row(s) from `WS1_DEFECT_MANIFEST.md`
being closed, and the comparison must show, quoting both artifacts, that the
quoted defective output is absent in the remediated artifact. For Workstream 2
specifically: `safety_signals_*.json` for the SAME false-negative inputs must
be non-empty and each signal must trace to one of the dangerous-consequence
statements; the positive baseline (`inputs_positive_baseline.json`) must STILL
produce signals (no regression of the PR #122 wording).

## 4. Allowed changes

Only differences attributable to the authorized workstream scope, enumerated
diff-by-diff in the closure report. Everything else in the deliverable JSON
and HTML must be byte-identical after normalization, OR each difference must
be individually explained and mapped to the authorized scope.

## 5. Prohibited regressions

- The full-suite failure baseline may not grow (baseline: 31 failures, all in
  `tests/test_domain_registry.py` — see `WS1_BASELINE_TESTS.md`).
- Replay/adversarial, WPS-001, benchmark, and gate results may not change
  except under an owner-approved parity proof (CLAUDE.md scoring rules).
- The positive safety baseline may not lose signals.
- No previously-correct deliverable content may disappear or be reworded
  outside the authorized scope.
- No fixture or evidence artifact in this directory may be modified.

## 6. Required independent review evidence

Closure requires a committed independent read-only review record that (a) re-runs
the reproduction script itself, (b) verifies the artifact hashes of both base
and remediated sets, (c) confirms the target-defect absence quote-by-quote,
and (d) confirms the prohibited-regression checks — followed by explicit owner
closure authorization (plan §12). Focused-test greenness alone is
insufficient.
