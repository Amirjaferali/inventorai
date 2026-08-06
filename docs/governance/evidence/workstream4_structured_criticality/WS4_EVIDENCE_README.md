# Workstream 4 Structured Criticality Capture — Evidence Package

Evidence for the Workstream 4 HEAD GREEN result on Draft PR #183, generated
at head `61f0b14cb6bf2f5c5328eb9958640bf036015720` under the owner
evidence-only authorization. This package is confined to
`docs/governance/evidence/workstream4_structured_criticality/`; the
Workstream 1–3 evidence trees are untouched and remain immutable. Roadmap /
remediation-plan synchronization and the PR #183 merge remain SEPARATELY
owner-gated and are NOT performed or implied by this package.

## Index

| File | Type | Content |
|---|---|---|
| `WS4_HEAD_IDENTITY.md` | narrative index | HEAD/commit-chain/contract identity; authorized-file confinement; BASE equivalence note (F3) |
| `WS4_BASE_RED_RECORD.md` | narrative index | the BASE RED gate: commit identity, 5 pass / 8 genuine RED / 1 owner-recorded skip, review result |
| `WS4_TEST_RECORD.md` | raw output | complete raw pytest outputs and the verified classifications (18/22/18/15/39/316; full suite 31-failed confinement) |
| `WS4_TRACEABILITY.md` | narrative index | R1–R8 → implementation behavior; G1–G5 → user-facing behavior; zero-skip finality |
| `WS4_HYGIENE_RECORD.md` | narrative index | the literal hardening amendment, blanket vs field-aware coverage, allowed-wording proof |
| `WS4_STALE_CONFIRMATION_RECORD.md` | narrative index | stale surfacing example, non-reattachment, placement rationale, reviewer conclusion |
| `WS4_REVIEW_FINDINGS.md` | narrative index | independent review PASS + the four non-blocking findings (future hardening observations) |
| `generate_ws4_artifacts.py` | deterministic harness | regenerates every journey artifact below; loud failure, no partial output |
| `ws4_journey_never_interacted.json` | deterministic artifact | journey A: empty history; summary block + five actions present; §13 never-interacted wordings |
| `ws4_journey_owner_confirmed.json` | deterministic artifact | journey B: confirmed FEASIBILITY-THREATENING end-to-end (statuses, history, §13, token scan) |
| `ws4_journey_owner_confirmed_deliverable.html` | deterministic artifact | journey B rendered inventor-facing deliverable HTML |
| `ws4_journey_deferral_zero_delta.json` | deterministic artifact | journey C: both deferral actions with full before/after zero-side-effect comparison |
| `ws4_journey_correction.json` | deterministic artifact | journey D: correction/missing actions store nothing; free-text path proven |
| `ws4_journey_manipulated_rejection.json` | deterministic artifact | journey E: five manipulated/stale submissions, all HTTP 400, nothing stored |
| `ws4_stale_confirmation.json` | deterministic artifact | stale confirmation: aggregate metadata only, no raw id, no reattachment |
| `WS4_ARTIFACT_MANIFEST.sha256` | manifest | SHA-256 + size + type + generation command per file |

## Regeneration

From the repository root at the evidence commit's parent
(`61f0b14cb6bf2f5c5328eb9958640bf036015720`):

```
python docs/governance/evidence/workstream4_structured_criticality/generate_ws4_artifacts.py
```

The harness is deterministic after the disclosed normalization (SESSION_ID /
IDEA_ID / GENERATED_AT_UTC / FOCUS_TOKEN_n): two consecutive runs print
byte-identical artifact hashes. It exits non-zero with a loud message and
writes nothing if any journey assertion fails.
