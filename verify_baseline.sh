#!/usr/bin/env bash
#
# G-IRB Implementation-Readiness Baseline verifier.
#
# Purpose (readiness only): reproducibly install the pinned dependencies into an
# ISOLATED virtual environment and run the governed test suite (the tests/ directory).
# This script is additive infrastructure. It does NOT remediate any security risk
# (R6 world-/group-readable /tmp transcript and R16 debug=True + hard-coded secret
# remain OPEN and are reserved for the separately authorized G-SC0 increment). It
# changes NO application, engine, or product behavior.
#
# Environment safety:
#   * Never installs into the system/global or an already-active Python environment:
#     it creates its own fresh virtualenv (override the location with GIRB_VENV).
#   * Never modifies repository files (read + execute only).
#   * No privileged (sudo) or destructive commands; no Docker/CI/deploy tooling.
#
# Exit status:
#   0  governed suite passed (with only the accepted xfail/skip)
#   >0 any ungoverned failure, an unexpected pass (xfail_strict), a missing tool,
#      or an install failure — surfaced clearly, not swallowed.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "== G-IRB Implementation-Readiness Baseline verification =="
echo "repository root: ${ROOT}"

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found on PATH" >&2
    exit 3
fi

if [ ! -f "${ROOT}/requirements.txt" ]; then
    echo "ERROR: ${ROOT}/requirements.txt not found" >&2
    exit 4
fi

# Isolated environment. Default to a fresh temp venv; allow the caller to pin a
# location via GIRB_VENV (e.g. a pre-activated isolated env in CI later).
VENV_DIR="${GIRB_VENV:-$(mktemp -d)/girb-venv}"
echo "== creating isolated virtualenv: ${VENV_DIR} =="
python3 -m venv "${VENV_DIR}"
# shellcheck disable=SC1091
. "${VENV_DIR}/bin/activate"

echo "== interpreter / installer versions =="
python -V
pip -V

echo "== installing pinned dependencies (isolated) =="
python -m pip install --upgrade pip >/dev/null
python -m pip install -r "${ROOT}/requirements.txt"

echo "== resolved environment (pip freeze) =="
python -m pip freeze

echo "== running governed suite (tests/) from repository root =="
# CWD must be the repository root: engine/domain_rules.py loads the registry from the
# relative path "domains/" at import time.
cd "${ROOT}"
# -rxX reports xfailed/xpassed reasons; xfail_strict=true (pytest.ini) makes any
# unexpected pass a failure. pytest's own nonzero exit propagates via `set -e`.
python -m pytest -rxX

echo "== G-IRB baseline verification completed successfully =="
