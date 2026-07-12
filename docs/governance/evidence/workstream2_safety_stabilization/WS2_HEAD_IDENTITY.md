# WS2 Head Identity Record

**Document ID:** WS2_HEAD_IDENTITY
**Type:** Evidence record (Workstream 2)
**Date:** 2026-07-12

## Identity

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Base (authoritative tip) | `71ace5566ae7060731e46a047384bd822ee69ed1` (PR #171 merge) |
| Implementation branch | `claude/ws2-safety-signal-stabilization` |
| BASE RED commit (tests only) | `4303682f4301b3e9dd09d2b8c90236060ba91171` |
| Implementation commit | `3db477cd2779803f771f59d078046a5e8d459d75` |
| Corrective RED commit (tests only; owner-ordered benign-failover correction) | `291f5d478396012aa3f072bdf39a97d86e7f3c05` |
| Correction commit | `b2888238339f5da311eeb43f246df0c2389f466e` |
| Canonical contract blob | `3db597c77d14aa8f39f7a624c7c32d4984e4f3a3` |
| Generation timestamp (final committed run) | `2026-07-12T09:03:11Z` (normalized to `GENERATED_AT_UTC` in artifacts) |
| Environment | Python 3.11.15; pytest 9.1.1; Flask 3.1.3 (container-installed) |
| Command | `python3 docs/governance/evidence/workstream2_safety_stabilization/regenerate_and_compare.py` (repo root) |
| Normalization | identical to WS1 (SESSION_ID / IDEA_ID / GENERATED_AT_UTC placeholders; nothing else altered) |

## Determinism proof

Two consecutive full runs in different wall-clock seconds produced identical
SHA-256 hashes for every normalized artifact:

| Artifact | SHA-256 (normalized) | vs WS1 baseline |
|---|---|---|
| inputs_false_negative_journey.json | `d177db5a7b36e7da35a680459fa6e4c9fc6163f1b1e3276890285c4ed3f1f27f` | **IDENTICAL to WS1** |
| journey_log_false_negative.json | `328a4f0eed95d9f46eb3c9f7fa38ed7dc92c95edf4c3ac572edd5a9601bb61a0` | **IDENTICAL to WS1** |
| deliverable_false_negative.json | `0f5d044a66b359e4edfcd35af4c92f5e55124b680a567c5892b9013ce4d3b951` | differs (safety block only — see comparison record) |
| deliverable_false_negative.html | `503904906488bca52511b76c023889286dcfeb979cfc80cbad1021402d39ebe5` | differs (safety panel only) |
| safety_signals_false_negative.json | `630cc779075f15ada25ef42ba240fda0b2bf6fb3aa5183c74e039f3babc27995` | base was `[]` (`37517e5f…`); head: 3 signals |
| inputs_positive_baseline.json | `e88fc36a5623abe439635da9aec72107b1c0877428f5d1ace4eeba377fedd602` | **IDENTICAL to WS1** |
| deliverable_positive_regenerated.json | `f660b9d4303214ac933205714f1529cadbdc976bff189174bd895180d0eb774a` | differs (signal count 3→1, dedup) |
| deliverable_positive_regenerated.html | `a5d5dc92c9b8d735c8dba17e608157302d4fd8b5682b90c5da23f0644c3da998` | differs (signal count 3→1, dedup) |
| safety_signals_positive_regenerated.json | `741443fa9245f831bd92c015143da980cabb11d6c919dd5bce9f1d5ec90773b2` | base 3 duplicate-source signals → head 1 (≥1 required; "exactly 3" explicitly not required) |

Headline: **false-negative journey 0 → 3 signals; positive baseline still ≥1
signal (1 after exact-duplicate dedup).** The byte-identical inputs and
journey log prove the journey, scoring, transitions, and reasons are
unchanged by this workstream.

Post-correction note: after the owner-ordered benign-failover correction
(commits `291f5d47` + `b2888238`), the committed harness was re-run and every
artifact above remained BYTE-IDENTICAL (clean git tree) — the correction
changes cue-family membership only and does not alter the journey's derived
signals. The hash table above therefore remains current at the corrected
head.
