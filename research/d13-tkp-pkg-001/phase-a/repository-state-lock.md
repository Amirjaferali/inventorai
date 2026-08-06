# Phase A Repository-State Lock (as fixed at start)

| Lock field | Value |
|---|---|
| Authoritative branch | `feature/atomic-json-session-persistence` |
| Authoritative commit (at Phase A start) | `70f032d13f503195b716e4e627e87f373f80ed29` |
| Authoritative tree | `fd885e4705978722497eb54ac5e45f705b1aab95` |
| Authoritative ordered parents | `8ccb977cc29fc9ec56fa9113c45a24913270e6ae`, `dc7da27c388dd3760bda7bd67bfd350e70043b9f` |
| Authoritative subject | Merge pull request #217 from Amirjaferali/docs/d13-tkp-pkg-001-phase-a-no-date-execution-recording |
| Phase A branch | `research/d13-tkp-pkg-001-phase-a-read-only-analysis` |
| Phase A issuance-locked commit (analysis base) | `57e2fac837f333224b2f985be285fe9e0a9f6243` |
| Phase A base tree | `9487ad0aa7ccb3d31884c94086624cda946f7ea6` |
| Workspace path | `research/d13-tkp-pkg-001/phase-a/` |
| Evidence-storage path | `research/d13-tkp-pkg-001/phase-a/evidence/` |
| Start-authorization ID | `D13-TKP-PKG-001-PHASE-A-START-AUTH-001` |
| Execution model | no-date, owner-and-gate-based (AMEND-001 no-date) |
| Gate 3 validity | valid; expiry 2026-10-16 23:59 Asia/Kuwait (outer authorization bound only) |

**Branch-alignment note.** The Phase A branch is fixed at `57e2fac8` and must not absorb the governance-recording
commits of PR #215 / PR #216 / PR #217 or any later governance-only recording commit during Phase A execution. The
authoritative branch is 6 commits in total beyond `57e2fac8` — of which 3 are first-parent merge commits corresponding
to PR #215, PR #216, and PR #217 (the other 3 are the merged governance-recording commits) — solely through those
governance-only recordings, and the Phase A base remains an ancestor of the authoritative tip.
Product/application/schema/prompt files are byte-identical between
`57e2fac8` and the current tip (only `docs/governance/` differs), so read-only analysis of product source is
unaffected. Controlling governance documents are read from the authoritative tip as external governance records.

**Contemporaneous pre-start verification result:** PASS (all items). See `session-log.md`.
