# Workstream 7 — Actionable Validation Plan — Evidence Package

Governing contract: `docs/governance/ACTIONABLE_VALIDATION_PLAN_INCREMENT_CONTRACT.md`
(CONTRACT / CANONICAL; owner decisions D1–D13 with confirmations C1–C3).

## Identities

- **BASE**: `e1e71b3b089cd41fc90ca4f2c0b7ce6a37e37268` — the authoritative
  `feature/atomic-json-session-persistence` tip (PR #196 BASE RED merge;
  ordered parents `4197e692…`, `73a64366…`; tree `31af1ae4…`).
- **HEAD**: `52b1960fc99af6e746c522b9b32509df1a45076d` — the reviewed
  implementation commit on `feature/ws7-actionable-validation-plan-green`
  (parent = BASE; tree `b71ddf77…`; 4 files changed, +78/−6).

See `BASE_IDENTITY.txt` / `HEAD_IDENTITY.txt` for the full identity records
including the blob SHAs of every relevant file at each commit.

## What this package proves

1. **RED → GREEN one-to-one** (`BASE_FOCUSED_PYTEST.txt`,
   `HEAD_FOCUSED_PYTEST.txt`): the six intentional semantic failures R1–R6
   fail on BASE and pass on HEAD; the twelve protected invariants P1–P12 pass
   on both. BASE: 18 collected, 6 failed / 12 passed. HEAD: 18 passed.
2. **Protected battery unchanged** (`PROTECTED_BATTERY_BASE.txt`,
   `PROTECTED_BATTERY_HEAD.txt`, `PROTECTED_BATTERY_FILE_LIST.txt`): the same
   fixed 13-suite list produces 259 passed + 1 known pre-existing WPS001 skip
   on both BASE and HEAD.
3. **Full-suite delta is exactly the six RED tests**
   (`FULL_SUITE_BASE.txt` 37 failed / 1420 passed;
   `FULL_SUITE_HEAD.txt` 31 failed / 1426 passed;
   `FAILURE_DISTRIBUTION_*.txt` machine-derived: the 31 historical failures
   stay confined to `tests/test_domain_registry.py` on both sides and are NOT
   fixed by this workstream).
4. **User-output truthfulness across the ten canonical cases** (the paired
   `BASE_*`/`HEAD_*` JSON/HTML artifacts): answered actions become the exact
   owner wording with the requirement statement embedded byte-verbatim; the
   UNDETERMINED responsibility renders the exact two-line owner wording while
   the internal token stays `UNDETERMINED`; the meaningless confidence line is
   suppressed in HTML while JSON stays byte-compatible; the two pending
   advisories appear exactly and only on pending rows; unknown / deferred /
   provisional pass-through, contradiction, criticality, and risk/safety
   linkage are unchanged (`*_NON_PENDING_CASES.json`,
   `*_PROTECTED_INVARIANTS.txt` with BASE-vs-HEAD cross-checks).
5. **No invention, no D13 claim** (`INVENTION_TOKEN_SCAN.txt`,
   `D13_NON_IMPLEMENTATION_AUDIT.txt`): zero unauthorized specialist types,
   tools, laboratories, standards, simulations, thresholds, methods, products,
   companies, services, referral claims, or confidence scores in
   system-generated output; D13 remains a mandatory future, separately
   owner-gated capability — not designed, implemented, or approximated.

## Reproduction

- `generate_ws7_artifacts.py base|head OUTDIR` — run from the repository root
  of the corresponding checkout (BASE `e1e71b3b…` / HEAD `52b1960f…`); writes
  the case artifacts deterministically. Volatile identifiers (session id,
  generated-at timestamp) are normalized to fixed placeholders in saved HTML;
  JSON artifacts contain only deterministic sections plus verbatim fixture
  inputs. Repeated runs are byte-identical.
- The pytest artifacts record their exact command in a `# command:` header.
- `validate_ws7_evidence.py` — deterministic validator; re-derives every count
  from the raw artifacts in this directory and byte-checks the exact owner
  wordings; exits PASS or STOP (see `EVIDENCE_VALIDATION_REPORT.txt`).
- `MANIFEST.sha256` — SHA-256 of every evidence file except the manifest
  itself; verify with `sha256sum -c MANIFEST.sha256` from this directory.

## Honest record

- The 31 `tests/test_domain_registry.py` failures are the known pre-existing
  baseline and remain unfixed on BASE and HEAD alike.
- During generation, one head-mode run was accidentally launched from the BASE
  worktree working directory and produced BASE behavior; this was detected by
  the wording check, disclosed, and the head artifacts were regenerated from
  the HEAD checkout with deterministic overwrite (byte-reproducibility was
  then re-verified by an independent second run).
- This package records evidence only. It does not merge PR #197, does not
  close Workstream 7, and does not authorize any later gate.
