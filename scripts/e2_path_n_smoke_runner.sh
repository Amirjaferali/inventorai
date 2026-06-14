#!/usr/bin/env bash
# e2_path_n_smoke_runner.sh
#
# Standalone E-2 Path N smoke runner (Gate B, B-2).
#
# Modes:
#   scripts/e2_path_n_smoke_runner.sh             — execution mode
#   scripts/e2_path_n_smoke_runner.sh --preflight — preflight mode
#   scripts/e2_path_n_smoke_runner.sh \
#     --validate-sid <candidate>                  — validation mode
#
# Does NOT start or stop Flask.
# Never issues GET/POST in preflight or validate-sid modes.
# Modifies no committed file.

set -euo pipefail

# ── Constants ────────────────────────────────────────────────────────────────

DENIED_SID="830054a4-f9cb-43fb-ab1c-f5d5f3cfb314"
ARTIFACT_PATH="docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json"
MATCHER="scripts/e2_exact_matcher.py"
SERVER_URL="http://127.0.0.1:5000"
START_ROUTE="/start_ilt002_combination_lock_path_n"

# Owner-authorized fixed response array (D-2) — E2_OPERATIONAL_PROCEDURE.md §6
# Verbatim from committed §7.2. No substitution permitted.
RESPONSES=(
    "The keypad detects each key press and sends the entered sequence to a microcontroller for comparison with a stored access code."
    "The main components are a keypad, a microcontroller, a motor driver, a motor, and a mechanical bolt that locks or unlocks the door."
    "When the entered sequence matches the stored code, the controller activates the motor driver, turns the motor, and retracts the bolt."
    "If the code is incorrect, the controller keeps the bolt locked and rejects the attempt without activating the motor."
    "The system needs limits for motor travel, power loss handling, repeated failed attempts, and manual emergency access."
)

# ── UUID validation ───────────────────────────────────────────────────────────

is_valid_uuid() {
    local candidate="$1"
    if [[ "$candidate" =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; then
        return 0
    fi
    return 1
}

# ── --validate-sid mode ───────────────────────────────────────────────────────

cmd_validate_sid() {
    if [[ $# -ne 1 ]]; then
        echo "STOP: invalid SID format"
        exit 1
    fi
    local candidate="$1"
    if ! is_valid_uuid "$candidate"; then
        echo "STOP: invalid SID format"
        exit 1
    fi
    if [[ "$candidate" == "$DENIED_SID" ]]; then
        echo "STOP: denied prior SID"
        exit 1
    fi
    exit 0
}

# ── --preflight mode ──────────────────────────────────────────────────────────

cmd_preflight() {
    if [[ $# -ne 0 ]]; then
        echo "STOP: invalid argument"
        exit 1
    fi

    # CHECK 1: working directory is repository root
    if [[ ! -d "docs/governance" ]] || [[ ! -d "engine" ]]; then
        echo "PREFLIGHT FAIL: CHECK 1"
        exit 1
    fi

    # CHECK 2: git status --short is empty
    local git_status
    git_status="$(git status --short 2>/dev/null || true)"
    if [[ -n "$git_status" ]]; then
        echo "PREFLIGHT FAIL: CHECK 2"
        exit 1
    fi

    # CHECK 3: HEAD equals origin/main
    local head origin
    head="$(git rev-parse HEAD 2>/dev/null || true)"
    origin="$(git rev-parse origin/main 2>/dev/null || true)"
    if [[ -z "$head" ]] || [[ "$head" != "$origin" ]]; then
        echo "PREFLIGHT FAIL: CHECK 3"
        exit 1
    fi

    # CHECK 4: matcher exists
    if [[ ! -f "$MATCHER" ]]; then
        echo "PREFLIGHT FAIL: CHECK 4"
        exit 1
    fi

    # CHECK 5: matcher passes py_compile
    if ! python3 -m py_compile "$MATCHER" 2>/dev/null; then
        echo "PREFLIGHT FAIL: CHECK 5"
        exit 1
    fi

    # CHECK 6: approved artifact exists
    if [[ ! -f "$ARTIFACT_PATH" ]]; then
        echo "PREFLIGHT FAIL: CHECK 6"
        exit 1
    fi

    # CHECK 7: five fixed responses defined and non-empty
    if [[ "${#RESPONSES[@]}" -lt 5 ]]; then
        echo "PREFLIGHT FAIL: CHECK 7"
        exit 1
    fi
    local i
    for i in "${!RESPONSES[@]}"; do
        if [[ -z "${RESPONSES[$i]}" ]]; then
            echo "PREFLIGHT FAIL: CHECK 7"
            exit 1
        fi
    done

    # CHECK 8: --validate-sid on denied SID returns correct output and non-zero
    local vsid_out vsid_rc
    vsid_out="$(bash "$0" --validate-sid "$DENIED_SID" 2>/dev/null || true)"
    bash "$0" --validate-sid "$DENIED_SID" >/dev/null 2>&1 && vsid_rc=0 || vsid_rc=$?
    if [[ "$vsid_out" != "STOP: denied prior SID" ]] || [[ "$vsid_rc" -eq 0 ]]; then
        echo "PREFLIGHT FAIL: CHECK 8"
        exit 1
    fi

    # CHECK 9: /tmp is writable
    if ! touch /tmp/.e2_preflight_write_test 2>/dev/null; then
        echo "PREFLIGHT FAIL: CHECK 9"
        exit 1
    fi
    rm -f /tmp/.e2_preflight_write_test

    echo "PREFLIGHT OK"
    exit 0
}

# ── Execution mode ────────────────────────────────────────────────────────────

cmd_execute() {
    # Verify server readiness via non-mutating GET / (§7.1)
    local http_status
    http_status="$(curl -s -o /dev/null -w "%{http_code}" \
        "${SERVER_URL}/" 2>/dev/null)" || {
        echo "STOP: server not ready"
        exit 1
    }
    if [[ "$http_status" != "200" ]]; then
        echo "STOP: server not ready"
        exit 1
    fi

    # Submit idea and extract SID from Location header (§7.2)
    local headers_file
    headers_file="$(mktemp)"

    curl -s -o /dev/null -D "$headers_file" \
        -X POST \
        "${SERVER_URL}${START_ROUTE}" \
        --data-urlencode \
        "idea=An electronic combination lock that uses a keypad and a motor to control a bolt for a household door." \
        2>/dev/null || {
        rm -f "$headers_file"
        echo "STOP: session creation POST failed"
        exit 1
    }

    local sid
    sid="$(tr -d '\r' < "$headers_file" |
        sed -nE 's#^[Ll]ocation:[[:space:]]*/session/([^[:space:]]+).*#\1#p')"
    rm -f "$headers_file"

    if [[ -z "$sid" ]]; then
        echo "STOP: SID missing"
        exit 1
    fi

    if ! is_valid_uuid "$sid"; then
        echo "STOP: SID is not a UUID"
        exit 1
    fi

    if [[ "$sid" == "$DENIED_SID" ]]; then
        echo "STOP: denied prior SID"
        exit 1
    fi

    export SID="$sid"
    printf 'SID=%s\n' "$SID"

    # GET-before-POST loop — for n in 1 2 3 4 5 (§7.4)
    local match_cycle=""
    local match_qid=""

    for n in 1 2 3 4 5; do

        # Step 1 — mandatory GET before POST
        curl -s \
            "${SERVER_URL}/session/${SID}" \
            > "/tmp/e2_session_get_iter_${n}.html" \
            2>/dev/null || {
            echo "STOP: GET failed on cycle $n"
            exit 1
        }

        # Step 2 — POST fixed response for this cycle
        local response="${RESPONSES[$((n-1))]}"
        local status
        status="$(curl -s -o /dev/null -w "%{http_code}" \
            -X POST "${SERVER_URL}/session/${SID}" \
            --data-urlencode "response=${response}" \
            2>/dev/null)" || {
            echo "STOP: POST failed on cycle $n"
            exit 1
        }

        printf 'cycle=%d http_status=%s\n' "$n" "$status"

        if [[ "$status" != "302" ]]; then
            echo "STOP: unexpected HTTP status $status on cycle $n"
            exit 1
        fi

        # Step 3 — run exact match command as subprocess (§7.3, Gate B §7)
        local match_result match_rc
        match_result="$(python3 "$MATCHER" --sid "$SID" 2>/dev/null)" \
            && match_rc=0 || match_rc=$?

        printf '%s\n' "$match_result"

        if [[ "$match_rc" -ne 0 ]]; then
            echo "STOP: match command exited non-zero on cycle $n"
            exit 1
        fi

        case "$match_result" in
            MATCH\ *)
                match_cycle="$n"
                match_qid="${match_result#MATCH }"
                break
                ;;
            NO_MATCH)
                ;;
            *)
                echo "STOP: unexpected match result on cycle $n: $match_result"
                exit 1
                ;;
        esac

    done

    # §7.5 — always capture final session state
    curl -s \
        "${SERVER_URL}/session/${SID}" \
        > /tmp/e2_session_final_state.html \
        2>/dev/null || true

    if [[ -z "$match_cycle" ]]; then
        echo "STOP: no MATCH within five responses — E-2 NOT ACCEPTED"
        echo "Preserve all output files for owner review."
        echo "Do not create a successful E-2 evidence commit."
        exit 1
    else
        printf 'E-2 ACCEPTED: first MATCH at cycle=%s qid=%s\n' \
            "$match_cycle" "$match_qid"
    fi
}

# ── Entry point ───────────────────────────────────────────────────────────────

case "${1:-}" in
    --preflight)
        shift
        cmd_preflight "$@"
        ;;
    --validate-sid)
        shift
        cmd_validate_sid "$@"
        ;;
    "")
        cmd_execute
        ;;
    *)
        echo "STOP: unknown argument"
        exit 1
        ;;
esac
