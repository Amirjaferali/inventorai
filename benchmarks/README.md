# Benchmark Governance

## Directory Structure
- baseline_<date>_score<N>/  — immutable snapshots, never modify
- experiments/               — isolated single-change tests
- working/                   — active development, not preserved
- index.json                 — registry of all baselines

## Workflow
1. Clone baseline into experiments/ before any change
2. Run benchmark
3. If score improves: promote to new baseline
4. If score regresses: discard, restore from baseline SHA256

## Invariants
- Never modify files inside baseline_*/
- Every baseline must have: prompt.md, results.json, metrics.json
- metrics.json must include prompt_sha256 and model provenance
