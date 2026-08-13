"""CF5-F004 — Hardcoded Non-Activated Priority Fallback (RED->GREEN).

Authoritative contract:
``docs/governance/CF5_F004_PRIORITY_FALLBACK_CORRECTIVE_CONTRACT.md`` (merged
PR #462) under Owner decisions D-CF5-F004-01 (OD1/OD2/OD3), implementing the
independently validated finding (record merged PR #461): registry-derived
zero-activated candidate membership; the legacy four-domain precedence
preserved EXACTLY as a bounded compatibility layer among the legacy four
(OD2); a sole top-scoring registered domain -> truthful SINGLE; a
zero-activated tie involving a non-legacy registered domain -> the NEW
fail-closed ``UNRESOLVED_NON_ACTIVATED_TIE`` kind carrying the COMPLETE
canonical candidate set (no winner; no activation requirement; distinct from
the untouched activated-only P9-E2 ``AMBIGUOUS_TIE``).

Why ``MULTI_DOMAIN_NEEDS_D4`` is NOT reused (recorded implementation
evidence): equal-score evidence does not establish multi-domain composition;
reusing it would manufacture false D4 semantics; and the CLOSED P9-E2 policy
already deliberately rejects manufacturing that kind from equal-score
evidence.

Future registered domains are simulated ONLY via bounded, self-restoring
in-process doubles of ``engine.domain_rules._REGISTRY`` (monkeypatch; no pack
file, no registry-loader change, no schema change). The simulated pack id
``textile_machinery`` and its signals (``loom``/``spindle``/``textile``) are
verified vocabulary-clean: they match no existing registry signal, no
strong-unsupported family, and no lay-electrical word — so the real ``/start``
chain (R7) exercises the classifier path, not the pre-classifier vocabulary.
"""

import builtins
import importlib.util
import os
import sys
from types import MappingProxyType

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import engine.domain_rules as drm
from engine import domain_activation
from engine.domain_rules import (
    classify_domain, infer_domain, DomainClassification, DomainResultKind,
    DomainAmbiguityReason, AmbiguousDomainResultError,
)

ELEC = "electronics_electrical"
NEWDOM = "textile_machinery"
NEWDOM2 = "glass_blowing"

_NEW_PACK = {"classification_signals": [
    {"signal": "loom"}, {"signal": "spindle"}, {"signal": "textile"}]}
_NEW_PACK2 = {"classification_signals": [
    {"signal": "annealing"}, {"signal": "gaffer"}]}


@pytest.fixture
def registry_double(monkeypatch):
    """Self-restoring in-process recognized-registry double (no pack files)."""
    def _extend(extra, shuffle=False):
        base = dict(drm._REGISTRY)
        base.update(extra)
        if shuffle:  # reversed insertion order: determinism probe
            base = dict(reversed(list(base.items())))
        monkeypatch.setattr(drm, "_REGISTRY", MappingProxyType(base))
    return _extend


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring activation double (no real activation)."""
    def _activate(*domains):
        monkeypatch.setattr(
            domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


def test_baseline_real_state_unchanged():
    assert domain_activation.activated_domains() == [ELEC]
    assert NEWDOM not in drm._REGISTRY


# =========================================================================== RED
def test_red_r1_sole_top_new_domain_is_truthful_single(registry_double):
    """R1 (arm A): a registered non-legacy domain as SOLE top scorer must be a
    truthful deterministic SINGLE — the parent falls through to silent NONE."""
    registry_double({NEWDOM: _NEW_PACK})
    c = classify_domain("a loom with a spindle")
    assert c.kind is DomainResultKind.SINGLE
    assert c.selected_domain == NEWDOM


def test_red_r2_mixed_tie_not_silently_displaced(registry_double):
    """R2 (arm B): a registered non-legacy domain tied with a legacy
    non-activated domain must yield the fail-closed unresolved kind with the
    COMPLETE candidate set — the parent silently awards the legacy member."""
    registry_double({NEWDOM: _NEW_PACK})
    c = classify_domain("a loom and a gear")
    assert c.kind is DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE
    assert c.selected_domain is None
    assert c.candidates == ("mechanical", NEWDOM)
    assert c.reason is DomainAmbiguityReason.EQUAL_SCORE


def test_red_r8_three_way_tie_exact_complete_candidate_set(registry_double):
    """R8 (reviewer N2): a >=3-way zero-activated mixed tie must carry the
    EXACT complete candidate set — equality, not merely count, so a
    subsetting bug (3 -> 2) is caught."""
    registry_double({NEWDOM: _NEW_PACK})
    c = classify_domain("a loom, a gear and a catheter")
    assert c.kind is DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE
    assert c.candidates == ("mechanical", "medical_device", NEWDOM)


def test_red_r7_start_no_none_based_electronics_admission(registry_double):
    """R7: on the parent, omitted registered-domain evidence becomes NONE and
    is admitted as an electronics-labeled session through the sole-electronics
    consent path; the corrected classifier must prevent that admission.
    (Vocabulary-clean tokens: the strong-unsupported pre-classifier path is
    deliberately NOT triggered — see module docstring.)"""
    registry_double({NEWDOM: _NEW_PACK})
    from web.app import app, SESSION_STORE
    client = app.test_client()
    before = set(SESSION_STORE)
    resp = client.post("/start",
                       data={"idea": "a loom with a spindle",
                             "domain_confirm": ELEC},
                       follow_redirects=False)
    assert resp.status_code != 302          # parent: 302 electronics admission
    assert set(SESSION_STORE) == before     # no session persisted
    for sid in set(SESSION_STORE) - before:
        SESSION_STORE.pop(sid, None)


# ============================================================== pins (R3-R6) ====
def test_r3_legacy_four_domain_priority_pinned():
    """R3 (OD2): legacy zero-activated outputs unchanged on the real registry."""
    assert infer_domain("gear and catheter") == "medical_device"
    assert infer_domain("an app to organize daily schedules") == "software"
    assert infer_domain("a gear lever hinge") == "mechanical"
    assert classify_domain("ESP32 sensor circuit").selected_domain == ELEC
    assert classify_domain("nothing recognizable at all").kind is DomainResultKind.NONE


def test_r4_d3d_activated_over_recognized_unchanged(activate, registry_double):
    """R4: D3-D — an ACTIVATED domain still outranks recognized-not-activated
    domains on a tie, including with a simulated non-legacy domain present."""
    registry_double({NEWDOM: _NEW_PACK})
    activate(ELEC)
    c = classify_domain("a loom and a circuit")     # tie {textile, electronics}
    assert c.kind is DomainResultKind.SINGLE
    assert c.selected_domain == ELEC


def test_r5_p9e2_activated_tie_unchanged(activate):
    """R5: P9-E2 — >=2 ACTIVATED top-tied domains -> AMBIGUOUS_TIE, untouched."""
    activate(ELEC, "mechanical")
    c = classify_domain("circuit and hinge")
    assert c.kind is DomainResultKind.AMBIGUOUS_TIE
    assert c.candidates == (ELEC, "mechanical")


def test_r6_infer_domain_compatibility_pinned(registry_double, monkeypatch):
    """R6: infer_domain stays total over SINGLE/NONE and FAILS LOUD through the
    existing richer-result path for the new kind (no redesign)."""
    assert infer_domain("a voltage sensor circuit") == ELEC
    assert infer_domain("nothing recognizable at all") is None
    registry_double({NEWDOM: _NEW_PACK})
    assert infer_domain("a loom with a spindle") == NEWDOM   # SINGLE passes through
    unresolved = classify_domain("a loom and a gear")
    assert unresolved.kind is DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE
    monkeypatch.setattr(drm, "classify_domain", lambda _t: unresolved)
    with pytest.raises(AmbiguousDomainResultError):
        drm.infer_domain("anything")


# ==================================================================== GREEN =====
def test_green_non_legacy_only_tie_fail_closed(registry_double):
    """Two non-legacy registered domains tied -> the same fail-closed kind with
    the complete set (no invented winner among new domains either)."""
    registry_double({NEWDOM: _NEW_PACK, NEWDOM2: _NEW_PACK2})
    c = classify_domain("a loom and a gaffer")
    assert c.kind is DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE
    assert c.candidates == (NEWDOM2, NEWDOM)


def test_green_determinism_under_shuffled_registry_iteration(registry_double):
    """Shuffled registry iteration order must not change any result (no
    dict/filesystem/iteration-order dependence)."""
    registry_double({NEWDOM: _NEW_PACK})
    a = [classify_domain(t) for t in (
        "a loom and a gear", "a loom with a spindle",
        "gear and catheter", "a loom, a gear and a catheter")]
    registry_double({NEWDOM: _NEW_PACK}, shuffle=True)
    b = [classify_domain(t) for t in (
        "a loom and a gear", "a loom with a spindle",
        "gear and catheter", "a loom, a gear and a catheter")]
    assert a == b


def test_green_new_kind_construction_invariants():
    """The new kind enforces: >=2 recognized candidates, canonical order,
    deterministic reason, no winner, NO activation requirement — and the
    activated-only AMBIGUOUS_TIE invariant is untouched."""
    ok = DomainClassification(
        kind=DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE,
        candidates=("mechanical", "software"),      # recognized, NOT activated
        reason=DomainAmbiguityReason.EQUAL_SCORE)
    assert ok.selected_domain is None
    with pytest.raises(ValueError):                 # < 2 candidates
        DomainClassification(kind=DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE,
                             candidates=("mechanical",),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)
    with pytest.raises(ValueError):                 # non-canonical order
        DomainClassification(kind=DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE,
                             candidates=("software", "mechanical"),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)
    with pytest.raises(ValueError):                 # carried winner forbidden
        DomainClassification(kind=DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE,
                             selected_domain="mechanical",
                             candidates=("mechanical", "software"),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)
    # AMBIGUOUS_TIE stays activated-only (P9-E2-R invariant untouched):
    with pytest.raises(ValueError):
        DomainClassification(kind=DomainResultKind.AMBIGUOUS_TIE,
                             candidates=("mechanical", "software"),
                             reason=DomainAmbiguityReason.EQUAL_SCORE)


def test_green_focused_web_dispatch_fail_closed(registry_double):
    """Focused Web test: the new kind takes the existing fail-closed refusal
    dispatch at /start — no session for the mixed-tie input. The input is
    deliberately VOCABULARY-CLEAN ("hinge", not "gear": "gear" is a
    strong-unsupported word whose pre-classifier refusal would mask a dropped
    dispatch and make this test pass for the wrong reason — the M5 guard)."""
    registry_double({NEWDOM: _NEW_PACK})
    c = classify_domain("a loom and a hinge")
    assert c.kind is DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE  # honest precondition
    from web.app import app, SESSION_STORE
    client = app.test_client()
    before = set(SESSION_STORE)
    resp = client.post("/start",
                       data={"idea": "a loom and a hinge",
                             "domain_confirm": ELEC},
                       follow_redirects=False)
    assert resp.status_code == 200          # fail-closed refusal, never a 302 consent admission
    assert set(SESSION_STORE) == before


def test_green_focused_cli_bounded_stop(registry_double, monkeypatch, capsys):
    """Focused CLI test: the new kind follows the existing bounded-stop
    handling (no arbitrary winner printed, no proceed)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "scripts", "run_cli.py")
    spec = importlib.util.spec_from_file_location("run_cli_f004", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    registry_double({NEWDOM: _NEW_PACK})
    monkeypatch.setattr(builtins, "input", lambda *_a, **_k: "a loom and a gear")
    mod.run_cli()
    out = capsys.readouterr().out
    assert "CANNOT DETERMINE A SINGLE SUPPORTED DOMAIN" in out
    assert "Domain inferred:" not in out
    assert "Domain confirmed" not in out
