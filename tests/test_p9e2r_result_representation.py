"""P9-E2-R — Ambiguity / Multi-Domain Result Representation (RED->GREEN).

Authoritative contract:
docs/governance/P9_E2_R_AMBIGUITY_MULTI_DOMAIN_RESULT_REPRESENTATION_CONTRACT.md
(merged PR #442). Behavioral, self-restoring test doubles only; NO real new domain
is activated (activated ties are simulated by patching
domain_activation._ACTIVATED_DOMAINS and restoring). These tests fail on the
pre-P9-E2-R baseline because classify_domain / DomainClassification did not exist
and /start / the CLI consumed the str|None seam that could not represent ambiguity.
"""

import builtins
import importlib.util
import os
import sys
import uuid

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation
from engine.domain_rules import (
    classify_domain, infer_domain, DomainClassification, DomainResultKind,
    DomainAmbiguityReason, AmbiguousDomainResultError,
)

_ACTIVATED = "electronics_electrical"
_RECOGNIZED_NOT_ACTIVATED = "mechanical"


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring activation of a set of recognized packs (no real activation).
    Restored automatically by monkeypatch teardown."""
    def _activate(*domains):
        monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


# --------------------------------------------------------- fixture honesty -------
def test_baseline_only_electronics_activated():
    assert domain_activation.activated_domains() == [_ACTIVATED]
    assert domain_activation.support_state(_RECOGNIZED_NOT_ACTIVATED) == \
        domain_activation.RECOGNIZED_NOT_ACTIVATED


# ------------------------------------------------------------------ RED-R1 -------
def test_red_r1_ambiguity_is_distinct_from_none_and_single(activate):
    activate("mechanical", "medical_device")
    amb = DomainClassification(
        kind=DomainResultKind.AMBIGUOUS_TIE,
        candidates=("mechanical", "medical_device"),
        reason=DomainAmbiguityReason.EQUAL_SCORE)
    none = DomainClassification(kind=DomainResultKind.NONE)
    single = DomainClassification(kind=DomainResultKind.SINGLE,
                                  selected_domain=_ACTIVATED)
    assert amb.kind is DomainResultKind.AMBIGUOUS_TIE
    assert amb.kind is not none.kind and amb.kind is not single.kind
    assert amb.selected_domain is None          # no winner
    assert len(amb.candidates) >= 2
    assert amb != none and amb != single


# ------------------------------------------------------------------ RED-R3 -------
def test_red_r3_multi_domain_distinct_from_single(activate):
    multi = DomainClassification(
        kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
        candidates=("mechanical", "medical_device"),
        reason=DomainAmbiguityReason.MULTI_DOMAIN)
    single = DomainClassification(kind=DomainResultKind.SINGLE,
                                  selected_domain=_ACTIVATED)
    assert multi.kind is DomainResultKind.MULTI_DOMAIN_NEEDS_D4
    assert multi.selected_domain is None        # never silently one domain
    assert multi.kind is not single.kind


# ------------------------------------------------------------------ RED-R4 -------
def test_red_r4_candidate_order_determinism_not_precedence(activate):
    activate("mechanical", "medical_device")
    a = DomainClassification(kind=DomainResultKind.AMBIGUOUS_TIE,
                             candidates=("mechanical", "medical_device"),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)
    b = DomainClassification(kind=DomainResultKind.AMBIGUOUS_TIE,
                             candidates=("mechanical", "medical_device"),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)
    assert a == b                               # equivalent sets -> equal results
    assert a.selected_domain is None            # canonical order implies NO winner
    # non-canonical order is rejected (canonical ordering is enforced, not assumed)
    with pytest.raises(ValueError):
        DomainClassification(kind=DomainResultKind.AMBIGUOUS_TIE,
                             candidates=("medical_device", "mechanical"),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)


# ------------------------------------------------------------------ RED-R5 -------
def test_red_r5_recognized_not_activated_excluded_from_tie(activate):
    # Only electronics activated: a tie candidate that is not activated is rejected.
    with pytest.raises(ValueError):
        DomainClassification(kind=DomainResultKind.AMBIGUOUS_TIE,
                             candidates=("mechanical", "medical_device"),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)


# ------------------------------------------------------------------ RED-R6 -------
def test_red_r6_genuine_none_preserved():
    result = classify_domain("a nice friendly greeting")
    assert result.kind is DomainResultKind.NONE
    assert result.selected_domain is None and result.candidates == ()
    assert infer_domain("a nice friendly greeting") is None


# ------------------------------------------------------------------ RED-R7 -------
def test_red_r7_line34_priority_fallback_preserved():
    # No activated tied domain -> the unchanged line-34 priority literal governs.
    assert infer_domain("gear and catheter") == "medical_device"
    assert classify_domain("gear and catheter").kind is DomainResultKind.SINGLE
    # electronics single path also unchanged
    assert infer_domain("a voltage sensor circuit") == _ACTIVATED


# ------------------------------------------------------------------ RED-R8 -------
def test_red_r8_three_way_tie_full_candidate_set(activate):
    activate("mechanical", "medical_device", "software")
    tie = DomainClassification(
        kind=DomainResultKind.AMBIGUOUS_TIE,
        candidates=("mechanical", "medical_device", "software"),
        reason=DomainAmbiguityReason.EQUAL_SCORE)
    assert tie.candidates == ("mechanical", "medical_device", "software")  # full set
    assert len(tie.candidates) == 3 and tie.selected_domain is None


# ------------------------------------------------------------------ RED-R9 -------
def test_red_r9_wrapper_fails_loud_on_richer_kinds(activate, monkeypatch):
    import engine.domain_rules as drm
    activate("mechanical", "medical_device")
    amb = DomainClassification(kind=DomainResultKind.AMBIGUOUS_TIE,
                               candidates=("mechanical", "medical_device"),
                               reason=DomainAmbiguityReason.EQUAL_SCORE)
    multi = DomainClassification(kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
                                 candidates=("mechanical", "medical_device"),
                                 reason=DomainAmbiguityReason.MULTI_DOMAIN)
    for richer in (amb, multi):
        monkeypatch.setattr(drm, "classify_domain", lambda _t, _r=richer: _r)
        with pytest.raises(AmbiguousDomainResultError):
            drm.infer_domain("anything")
    # never a silent None / arbitrary domain for richer kinds
    monkeypatch.setattr(drm, "classify_domain", lambda _t: multi)
    with pytest.raises(AmbiguousDomainResultError):
        drm.infer_domain("x")


def test_red_r9_wrapper_total_over_single_none():
    assert infer_domain("a voltage sensor circuit") == _ACTIVATED   # SINGLE
    assert infer_domain("a nice friendly greeting") is None         # NONE


# ------------------------------------------------------ invariant construction ---
def test_invariants_reject_invalid_construction(activate):
    activate("mechanical", "medical_device")
    bad = [
        dict(kind=DomainResultKind.SINGLE, selected_domain="quantum_widgets"),      # non-registry
        dict(kind=DomainResultKind.SINGLE, selected_domain=_ACTIVATED,
             candidates=("mechanical",)),                                           # mutual exclusion
        dict(kind=DomainResultKind.AMBIGUOUS_TIE, candidates=("mechanical",),
             reason=DomainAmbiguityReason.EQUAL_SCORE),                             # singleton
        dict(kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
             candidates=("mechanical", "mechanical"),
             reason=DomainAmbiguityReason.MULTI_DOMAIN),                            # duplicate
        dict(kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
             candidates=("mechanical", "medical_device")),                         # no reason
        dict(kind=DomainResultKind.NONE, selected_domain=_ACTIVATED),              # NONE w/ domain
    ]
    for kwargs in bad:
        with pytest.raises(ValueError):
            DomainClassification(**kwargs)


def test_result_is_immutable():
    r = DomainClassification(kind=DomainResultKind.NONE)
    with pytest.raises(Exception):
        r.selected_domain = "electronics_electrical"   # frozen


def test_reason_is_deterministic_enum_not_free_text(activate):
    activate("mechanical", "medical_device")
    with pytest.raises(ValueError):
        DomainClassification(kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
                             candidates=("mechanical", "medical_device"),
                             reason="equally strong candidates")   # free-form rejected
    ok = DomainClassification(kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
                              candidates=("mechanical", "medical_device"),
                              reason=DomainAmbiguityReason.MULTI_DOMAIN)
    assert isinstance(ok.reason, DomainAmbiguityReason)


# ----------------------------------------------- defensive activation boundary ---
def test_defensive_boundary_rejects_result_object_in_activation():
    result = DomainClassification(kind=DomainResultKind.NONE)
    with pytest.raises(TypeError):
        domain_activation.support_state(result)     # must fail loud, not "unknown"
    with pytest.raises(TypeError):
        domain_activation.is_activated(result)
    # legitimate None / empty-string behavior preserved
    assert domain_activation.support_state(None) == domain_activation.UNKNOWN_OR_UNSUPPORTED
    assert domain_activation.support_state("") == domain_activation.UNKNOWN_OR_UNSUPPORTED


# ---------------------------------------------------------------- web callers ----
def _start_post(client, idea, confirm=True):
    data = {"idea": idea}
    if confirm:
        data["domain_confirm"] = "electronics_electrical"
    return client.post("/start", data=data, follow_redirects=False)


def test_red_r2_start_ambiguous_tie_fails_closed(activate, monkeypatch):
    from web import app as web_app
    activate("mechanical", "medical_device")
    amb = DomainClassification(kind=DomainResultKind.AMBIGUOUS_TIE,
                               candidates=("mechanical", "medical_device"),
                               reason=DomainAmbiguityReason.EQUAL_SCORE)
    monkeypatch.setattr(web_app, "classify_domain", lambda _t: amb)
    client = web_app.app.test_client()
    before = set(web_app.SESSION_STORE)
    resp = _start_post(client, "an ambiguous cross-domain idea")
    assert resp.status_code == 200                       # not a 302 admission
    assert set(web_app.SESSION_STORE) == before          # no session created
    # never admitted as an electronics session
    assert all(v["state"].domain == "electronics_electrical"
               for v in web_app.SESSION_STORE.values()) or not web_app.SESSION_STORE
    assert web_app.UNSUPPORTED_DOMAIN_MESSAGE in resp.get_data(as_text=True)


def test_red_r10_start_multi_domain_fails_closed(monkeypatch):
    from web import app as web_app
    multi = DomainClassification(kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
                                 candidates=("mechanical", "medical_device"),
                                 reason=DomainAmbiguityReason.MULTI_DOMAIN)
    monkeypatch.setattr(web_app, "classify_domain", lambda _t: multi)
    client = web_app.app.test_client()
    before = set(web_app.SESSION_STORE)
    resp = _start_post(client, "a genuine multi-domain invention")
    assert resp.status_code == 200                       # fail closed, no admission
    assert set(web_app.SESSION_STORE) == before          # no session, never one domain
    body = resp.get_data(as_text=True)
    assert web_app.UNSUPPORTED_DOMAIN_MESSAGE in body
    # never implies multi-domain analysis occurred / never leaks the object
    assert "DomainClassification" not in body


def test_start_single_and_none_behavior_unchanged(monkeypatch):
    from web import app as web_app
    client = web_app.app.test_client()
    # SINGLE(electronics) admitted under confirmation (real classifier)
    resp = _start_post(client, "ESP32 microcontroller circuit with a voltage sensor")
    assert resp.status_code == 302 and "/session/" in resp.headers["Location"]
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    assert web_app.SESSION_STORE[sid]["state"].domain == "electronics_electrical"
    # state.domain is a resolved string, never a DomainClassification
    assert isinstance(web_app.SESSION_STORE[sid]["state"].domain, str)
    web_app.SESSION_STORE.pop(sid, None)


# ------------------------------------------------------------------ CLI RED-R11 --
def _load_run_cli():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "run_cli.py")
    spec = importlib.util.spec_from_file_location("run_cli_p9e2r", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_red_r11_cli_bounded_stop_on_richer_kinds(monkeypatch, capsys):
    mod = _load_run_cli()
    multi = DomainClassification(kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
                                 candidates=("mechanical", "medical_device"),
                                 reason=DomainAmbiguityReason.MULTI_DOMAIN)
    monkeypatch.setattr(mod, "classify_domain", lambda _t: multi)
    monkeypatch.setattr(builtins, "input", lambda *_a, **_k: "a multi-domain idea")
    mod.run_cli()
    out = capsys.readouterr().out
    assert "CANNOT DETERMINE A SINGLE SUPPORTED DOMAIN" in out   # bounded stop
    assert "Domain inferred:" not in out                        # no arbitrary winner printed
    assert "DomainClassification" not in out                    # object never stringified
    assert "Domain confirmed" not in out                        # did not proceed


def test_cli_single_electronics_proceeds(monkeypatch, capsys):
    mod = _load_run_cli()
    single = DomainClassification(kind=DomainResultKind.SINGLE,
                                  selected_domain="electronics_electrical")
    monkeypatch.setattr(mod, "classify_domain", lambda _t: single)
    monkeypatch.setattr(builtins, "input", lambda *_a, **_k: "an electronics circuit")
    mod.run_cli()
    out = capsys.readouterr().out
    assert "Domain inferred: electronics_electrical" in out
    assert "Domain confirmed: electronics/electrical" in out
