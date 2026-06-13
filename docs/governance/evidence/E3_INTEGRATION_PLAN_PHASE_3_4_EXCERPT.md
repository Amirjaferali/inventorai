# E-3 — Integration Plan Phase 3 / Phase 4 Recovery

Source commit: `d2b2a9a`

Source file:

`docs/governance/PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN.md`

## Verbatim committed excerpt

| Phase | Content | Touches | Gate to next phase |
|-------|---------|---------|--------------------|
| 3 | Runtime test suite committed and green | `tests/` only | Owner review of full results |
| 4 | Eligibility for `runtime_integrated` metadata update after approved runtime tests pass; actual flag change requires separate owner authorization, JSON metadata update, re-testing, and recorded re-approval | Nothing automatic; flag change only under its own authorization | Recorded re-approval |

No phase may be merged with another. No phase begins without its own
authorization text.

## Authorized interpretation

- Phase 3 is a committed runtime test-suite phase.
- E-2 smoke evidence does not itself constitute or satisfy Phase 3.
- Phase 4 creates eligibility only.
- `runtime_integrated=true` is not automatic.
- Any flag change requires:
  1. separate owner authorization;
  2. JSON metadata update;
  3. re-testing;
  4. recorded re-approval.
- R2 remains non-automatic and requires a separate owner decision.
