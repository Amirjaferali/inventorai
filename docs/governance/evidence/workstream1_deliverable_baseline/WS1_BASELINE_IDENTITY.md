# WS1 Baseline Identity Record

**Document ID:** WS1_BASELINE_IDENTITY
**Type:** Evidence-lock baseline identity (Workstream 1, plan §7 item A)
**Status:** RECORDED — immutable evidence
**Date:** 2026-07-11

## A. Baseline identity

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Branch generated from | `docs/workstream-1-evidence-lock` (created from the authoritative tip; identical tree at generation time) |
| Authoritative tip (code under test) | `f1286c3d9f6dc027de09095eacc41437e405b9a4` (merge of PR #168 into `feature/atomic-json-session-persistence`; parents `c62bd9ab…`, `5f61bc4f…`) |
| Generation timestamp (UTC, both bundles, final committed run) | `2026-07-11T22:36:49Z` (normalized to `GENERATED_AT_UTC` inside artifacts) |
| Python | 3.11.15 |
| pytest | 9.1.1 (container-installed; repository ships no requirements manifest) |
| Flask | 3.1.3 (container-installed) |
| Exact command | `python3 docs/governance/evidence/workstream1_deliverable_baseline/reproduce_baseline.py` (run from repository root) |
| Session IDs / idea IDs | Random per run (Flask `uuid4`); normalized to `SESSION_ID` / `IDEA_ID` in artifacts. Final committed run (last writer): false-negative session `c957eadb-be45-41bc-8a7f-480f89f059dd` / idea `ea985449-acd5-4755-971d-e951bc49b2e2`; positive session `bc6f5f5e-d4e7-45a2-9992-5f361a2cdaef` / idea `0da8fffe-35f6-4e7c-9e54-eec616f7c9ae`. The committed artifacts are identifier-normalized, so these raw values are recorded here for provenance only. |

## Normalization disclosure

Each run creates random UUIDs (session id, `IdeaState.idea_id`) and one
generation timestamp. In every saved artifact these are replaced by the fixed
placeholders `SESSION_ID`, `IDEA_ID`, `GENERATED_AT_UTC`. **No other byte of
any engine output or inventor statement is altered.** With this normalization
the artifacts are byte-identical across repeat runs (verified across runs in
different wall-clock seconds).

## Determinism proof

Two consecutive full runs (separated by >1s) produced identical SHA-256
hashes for every normalized artifact:

| Artifact | SHA-256 (normalized) |
|---|---|
| inputs_false_negative_journey.json | `d177db5a7b36e7da35a680459fa6e4c9fc6163f1b1e3276890285c4ed3f1f27f` |
| journey_log_false_negative.json | `328a4f0eed95d9f46eb3c9f7fa38ed7dc92c95edf4c3ac572edd5a9601bb61a0` |
| deliverable_false_negative.json | `f1057cf7b29d29ebbd596bae3b22cc5f0521f21718c9a46efb787e519bd95cc7` |
| deliverable_false_negative.html | `5552ef4546abd5f2951b96cc78140a0abc8650477928b0135d4f6cc7b7a7568e` |
| safety_signals_false_negative.json | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| inputs_positive_baseline.json | `e88fc36a5623abe439635da9aec72107b1c0877428f5d1ace4eeba377fedd602` |
| deliverable_positive_regenerated.json | `b452a020958c000359b39f05e20045d7e14e4b99ecbad032ab56e3329c25c0e2` |
| deliverable_positive_regenerated.html | `0df632191dea65600dcd3edb049d5699670ff43450ef97b665e23fc1e03cbe38` |
| safety_signals_positive_regenerated.json | `529baa6ed75e2d7c3fb28837bec3e0df127d1ecc1a04ab3c306a623ae05ebc54` |

Headline result (deterministic): **false-negative journey → 0 safety signals;
positive baseline (exact PR #122 wording) → 3 safety signals.**

## Historical-evidence reproducibility statement

The owner's ORIGINAL manual-trial sessions are NOT recoverable: sessions live
only in the in-memory `SESSION_STORE` (persistence is frozen and paused) and
runtime transcripts are written to the local `/tmp` of the machine that ran
them. Therefore the exact historical session state cannot be reproduced, and
this evidence lock does NOT reconstruct it. Instead it preserves the strongest
available bounded evidence: deterministic regeneration at the current
authoritative tip from the owner-specified key statements (verbatim, see
`inputs_false_negative_journey.json`), which reproduces the confirmed
safety-signal false negative and every deliverable-level defect enumerated in
`WS1_DEFECT_MANIFEST.md`. The prior successful safety-signal detection is
anchored by its committed record
(`docs/governance/PR122_INVENTOR_STATED_SAFETY_SIGNALS_MANUAL_DEMO_VERIFICATION.md`)
and reproduced at the current tip with the exact same statement.
