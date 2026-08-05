"""G-SC0 Bounded Security Containment — R6 / R16 regression tests.

RED against the authorized base (fa054ab): the /tmp transcript is written, the
source hard-codes debug=True, and a fixed secret is present. GREEN only after the
bounded containment. These tests do NOT launch a real server, open a listening
port, or run web/app.py as a long-lived subprocess; they use Flask's test_client
and monkeypatched environment. No existing test is modified.
"""

import os
from test_p4_1b2a_durable_answer_append import answered_post, seed_direct_session_envelope  # P4-1b-2a
from pathlib import Path

import pytest

from web.app import app, SESSION_STORE
from engine.idea_state import (
    IdeaState, Evidence, REASONED, Gap, PARTIAL, CLOSED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)

APP_SRC = (Path(__file__).resolve().parent.parent / "web" / "app.py").read_text(
    encoding="utf-8"
)

_REASONED = (
    "The sensor detects voltage drop across the shunt resistor. "
    "When the measured voltage falls below the threshold, the comparator "
    "triggers the relay which disconnects the load. "
    "This mechanism relies on Ohm's law and uses an LM393 comparator IC."
)


def _boundary_state(idea_id):
    s = IdeaState(idea_id=idea_id)
    s.domain = "electronics_electrical"
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 1
    s.current_stage = 2
    s.known_problem = Evidence("existing systems miss micro-faults", REASONED, 1)
    s.known_mechanism = Evidence(_REASONED, REASONED, 2)
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1, closed_at=2))
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=CLOSED, opened_at=3, closed_at=4))
    s.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=PARTIAL, opened_at=5))
    s.iteration = 5
    return s


def _answer_once(sid):
    state = _boundary_state(sid)
    SESSION_STORE[sid] = {
        "state": state,
        "last_result": None,
        "transcript": [],
        "last_question": "Q",
    }
    seed_direct_session_envelope(sid, state)  # explicit P4-1b-2a durable envelope
    answered_post(app.test_client(), sid, {"response": _REASONED})


# --------------------------------------------------------------------------- R6

def test_r6_answered_submission_writes_no_tmp_transcript():
    sid = "gsc0-r6-no-tmp-write"
    path = f"/tmp/ilt002_transcript_{sid}.jsonl"
    if os.path.exists(path):
        os.remove(path)
    try:
        _answer_once(sid)
        assert not os.path.exists(path), (
            "R6: an answered submission must not create a /tmp transcript file"
        )
    finally:
        SESSION_STORE.pop(sid, None)
        if os.path.exists(path):
            os.remove(path)


def test_r6_in_memory_transcript_preserved():
    sid = "gsc0-r6-inmem"
    path = f"/tmp/ilt002_transcript_{sid}.jsonl"
    if os.path.exists(path):
        os.remove(path)
    try:
        _answer_once(sid)
        transcript = SESSION_STORE[sid]["transcript"]
        assert transcript, "in-memory transcript must still receive the answered record"
        assert transcript[-1]["response"] == _REASONED, "verbatim in-memory record preserved"
    finally:
        SESSION_STORE.pop(sid, None)
        if os.path.exists(path):
            os.remove(path)


def test_r6_no_tmp_write_path_in_source():
    assert "/tmp/ilt002_transcript_" not in APP_SRC, (
        "R6: the /tmp transcript write path must be removed from web/app.py"
    )


# --------------------------------------------------------------------------- R16

def test_r16_no_hardcoded_secret_literal_in_source():
    assert "inventorai-dev-only" not in APP_SRC, (
        "R16: the hard-coded development secret must be removed from source"
    )


def test_r16_no_hardcoded_debug_true_in_source():
    assert "debug=True" not in APP_SRC, (
        "R16: debug must not be hard-coded True in the runtime entry point"
    )


def test_r16_debug_defaults_off_and_parses_explicit_values(monkeypatch):
    from web.app import _debug_enabled

    monkeypatch.delenv("INVENTORAI_DEBUG", raising=False)
    assert _debug_enabled() is False, "debug must default OFF when unset"
    for truthy in ("1", "true", "TRUE", "Yes", "on"):
        monkeypatch.setenv("INVENTORAI_DEBUG", truthy)
        assert _debug_enabled() is True, f"explicit truthy {truthy!r} must enable debug"
    for falsey in ("", "0", "false", "no", "off", "maybe", "2", "   "):
        monkeypatch.setenv("INVENTORAI_DEBUG", falsey)
        assert _debug_enabled() is False, f"ambiguous/falsey {falsey!r} must not enable debug"


def test_r16_host_defaults_to_loopback(monkeypatch):
    from web.app import _resolve_host

    monkeypatch.delenv("INVENTORAI_HOST", raising=False)
    assert _resolve_host() == "127.0.0.1"


def test_r16_env_secret_used_exactly(monkeypatch):
    from web.app import _resolve_secret_key

    monkeypatch.setenv("INVENTORAI_SECRET_KEY", "supplied-secret-abc123")
    monkeypatch.setenv("INVENTORAI_ENV", "production")
    assert _resolve_secret_key() == "supplied-secret-abc123"


def test_r16_production_fails_without_secret(monkeypatch):
    from web.app import _resolve_secret_key

    monkeypatch.setenv("INVENTORAI_ENV", "production")
    monkeypatch.delenv("INVENTORAI_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError):
        _resolve_secret_key()


def test_r16_dev_fallback_is_random_ephemeral(monkeypatch):
    from web.app import _resolve_secret_key

    monkeypatch.delenv("INVENTORAI_ENV", raising=False)
    monkeypatch.delenv("INVENTORAI_SECRET_KEY", raising=False)
    a = _resolve_secret_key()
    b = _resolve_secret_key()
    assert a and b, "dev fallback secret must be non-empty"
    assert a != b, "dev fallback secret must be random/ephemeral, not a constant"
    assert "inventorai-dev-only" not in (a, b)
