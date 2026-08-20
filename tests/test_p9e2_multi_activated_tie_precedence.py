"""P9-E2 / P9-PREREQ-B — Multi-Activated Domain Tie/Conflict Precedence (RED->GREEN).

Authoritative contract:
docs/governance/P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_CONTRACT.md, implemented
through the P9-E2-R canonical classifier seam ``classify_domain(...)`` (P9-E2-R
closure CF-1). Behavioral tests only.

Governed target policy inside ``engine/domain_rules.py::classify_domain``:
  len(activated_tied) == 0 -> unchanged non-activated priority fallback;
  len(activated_tied) == 1 -> SINGLE(that one activated domain) (unchanged);
  len(activated_tied) >= 2 -> AMBIGUOUS_TIE(selected_domain=None,
      candidates=complete ACTIVATED tied set in canonical (sorted) order,
      reason=EQUAL_SCORE).
No arbitrary / alphabetical / registration / dict-order winner; no Electronics
preference; no LLM tie-break; ``MULTI_DOMAIN_NEEDS_D4`` is NOT manufactured (D4 is a
separate, unexecuted gate).

Multi-activated ties are simulated with bounded, self-restoring test doubles of the
5-I2 activation allowlist (``domain_activation._ACTIVATED_DOMAINS``); the doubles
keep every combination deterministic and no test here activates a real domain. The
real runtime state is now ``activated_domains() ==
['electronics_electrical', 'mechanical']`` (asserted below), under which the
AMBIGUOUS_TIE branch is production-reachable for an equally top-scored
electronics/mechanical idea. (Historical note: when this file was authored only
``electronics_electrical`` was activated and the branch was reachable solely
through these bounded doubles; the doubled scenarios above remain valid as-is.)

Signal tokens below are verified against the live registry
(``domains/*/domain.json`` classification_signals): each is a single-pack signal.

Web ``/start`` reachability (see the strong-unsupported interaction tests): the route
calls ``classify_domain`` FIRST and dispatches an ``AMBIGUOUS_TIE`` to a fail-closed
UNSUPPORTED response BEFORE the separate ``_has_strong_unsupported_evidence`` gate.
Therefore a multi-activated tie fails closed via the ambiguity branch regardless of
whether its tokens are strong-unsupported words; the strong-unsupported gate is an
independent later layer affecting only SINGLE / NONE (single-domain or
classifier-miss) inputs. RED-E2-10 uses a tie input whose tokens are NOT
strong-unsupported words ("circuit and hinge") so the parent's incidental
single-winner ADMISSION at ``/start`` is directly observable and distinguishing.
"""

import builtins
import importlib.util
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation
from engine.domain_rules import (
    classify_domain, infer_domain, DomainResultKind, DomainAmbiguityReason,
    AmbiguousDomainResultError,
)

# Single-pack signal tokens (verified against the live registry).
_ELEC = "circuit"     # electronics_electrical only
_MECH = "hinge"       # mechanical only
_MECH2 = "gear"       # mechanical only
_MED = "catheter"     # medical_device only
_SW = "app"           # software only


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring activation double (no real activation).

    Restored automatically by monkeypatch teardown."""
    def _activate(*domains):
        monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


# --------------------------------------------------------- fixture honesty -------
def test_baseline_real_activation_unchanged():
    # No real domain is activated by this file's doubles beyond the true
    # production activation set.
    assert domain_activation.activated_domains() == ["electronics_electrical", "mechanical"]


# ----------------------------------------------------------------- RED-E2-1 ------
def test_red_e2_1_two_activated_tie_not_alphabetical_single(activate):
    """>= 2 activated tied domains must NOT collapse to an incidental (alphabetical
    / sorted-first) SINGLE winner. Parent returns SINGLE(mechanical)."""
    activate("mechanical", "medical_device")
    r = classify_domain(f"{_MECH2} and {_MED}")          # tied {mechanical, medical_device}
    assert r.kind is not DomainResultKind.SINGLE
    assert r.selected_domain is None
    assert r.selected_domain != "mechanical"             # not the sorted-first winner


# ----------------------------------------------------------------- RED-E2-2 ------
def test_red_e2_2_two_activated_tie_is_ambiguous(activate):
    """Two equally scored activated domains -> AMBIGUOUS_TIE. Parent -> SINGLE."""
    activate("mechanical", "medical_device")
    r = classify_domain(f"{_MECH2} and {_MED}")
    assert r.kind is DomainResultKind.AMBIGUOUS_TIE


# ----------------------------------------------------------------- RED-E2-3 ------
def test_red_e2_3_complete_activated_candidate_set(activate):
    """The tie carries the COMPLETE activated tied set (canonical order)."""
    activate("mechanical", "medical_device")
    r = classify_domain(f"{_MED} and {_MECH2}")
    assert r.candidates == ("mechanical", "medical_device")   # sorted, complete


# ----------------------------------------------------------------- RED-E2-4 ------
def test_red_e2_4_no_electronics_favoritism(activate):
    """Electronics in a tie does NOT win. Parent -> SINGLE(electronics_electrical)."""
    activate("electronics_electrical", "medical_device")
    r = classify_domain(f"{_ELEC} and {_MED}")           # tied {electronics, medical}
    assert r.kind is DomainResultKind.AMBIGUOUS_TIE
    assert r.selected_domain != "electronics_electrical"
    assert "electronics_electrical" in r.candidates      # present but not a winner


# ----------------------------------------------------------------- RED-E2-5 ------
def test_red_e2_5_recognized_not_activated_excluded_from_tie(activate):
    """A recognized-but-NOT-activated domain is excluded from the tie set even when
    it is equally scored. Parent -> SINGLE(electronics_electrical)."""
    activate("electronics_electrical", "mechanical")     # medical NOT activated
    r = classify_domain(f"{_ELEC} and {_MECH2} and {_MED}")  # scored {elec, mech, med}
    assert r.kind is DomainResultKind.AMBIGUOUS_TIE
    assert r.candidates == ("electronics_electrical", "mechanical")
    assert "medical_device" not in r.candidates          # recognized-not-activated excluded


# ----------------------------------------------------------------- RED-E2-6 ------
def test_red_e2_6_permutation_order_independence(activate):
    """Input token order never changes the (canonical-ordered) tie. Parent -> SINGLE
    for both permutations, so asserting AMBIGUOUS_TIE equality is distinguishing."""
    activate("electronics_electrical", "mechanical")
    a = classify_domain(f"{_ELEC} and {_MECH}")
    b = classify_domain(f"{_MECH} and {_ELEC}")
    assert a.kind is DomainResultKind.AMBIGUOUS_TIE
    assert a.kind is b.kind and a.candidates == b.candidates
    assert a.candidates == ("electronics_electrical", "mechanical")


# ----------------------------------------------------------------- RED-E2-7 ------
def test_red_e2_7_three_way_activated_tie_full_set(activate):
    """>= 3-way activated tie preserves ALL activated candidates (no pair logic)."""
    activate("electronics_electrical", "mechanical", "medical_device")
    r = classify_domain(f"{_ELEC} and {_MECH2} and {_MED}")
    assert r.kind is DomainResultKind.AMBIGUOUS_TIE
    assert r.candidates == ("electronics_electrical", "mechanical", "medical_device")


# ----------------------------------------------------------------- RED-E2-8 ------
def test_red_e2_8_no_winner_deterministic_equal_score_reason(activate):
    """selected_domain is None and the reason is the deterministic EQUAL_SCORE enum
    (never free text, never model-generated). Parent -> SINGLE (has a winner)."""
    activate("mechanical", "software")
    r = classify_domain(f"{_MECH} and {_SW}")            # tied {mechanical, software}
    assert r.kind is DomainResultKind.AMBIGUOUS_TIE
    assert r.selected_domain is None
    assert r.reason is DomainAmbiguityReason.EQUAL_SCORE


# ----------------------------------------------------------------- RED-E2-9 ------
def test_red_e2_9_infer_domain_fails_loud_on_real_ambiguity(activate):
    """A REAL classify_domain ambiguity makes the legacy str|None wrapper fail loud
    (never a silent None / arbitrary domain). Parent -> wrapper returns a string."""
    activate("mechanical", "software")
    with pytest.raises(AmbiguousDomainResultError):
        infer_domain(f"{_MECH} and {_SW}")


# ---------------------------------------------------------- web /start RED-E2-10 --
def _start_post(client, idea):
    return client.post(
        "/start",
        data={"idea": idea, "domain_confirm": "electronics_electrical"},
        follow_redirects=False,
    )


def test_red_e2_10_start_real_tie_fails_closed_electronics_pair(activate):
    """REAL /start production-path distinguishing RED->GREEN.

    Input "circuit and hinge" (tokens are NOT strong-unsupported words) with
    electronics_electrical + mechanical activated. On the authoritative parent
    classify_domain -> incidental SINGLE(electronics_electrical), so /start ADMITS an
    electronics session (302 + session created). After the P9-E2 fix classify_domain
    -> AMBIGUOUS_TIE, and /start fails closed: 200 UNSUPPORTED, no admission, no
    session, no None-fallback electronics admission. This exercises the real
    classifier through the route (no injected DomainClassification)."""
    from web import app as web_app
    activate("electronics_electrical", "mechanical")
    client = web_app.app.test_client()
    before = set(web_app.SESSION_STORE)
    resp = _start_post(client, f"{_ELEC} and {_MECH}")
    assert resp.status_code == 200                          # NOT a 302 admission
    assert set(web_app.SESSION_STORE) == before             # no session created
    # Fail closed via the ambiguity branch. Since CF5-F002 §4.E the refusal
    # copy is activation-derived (truthful under a broadened activation set),
    # so the fail-closed message is asserted through the same activation-aware
    # seam rather than the historical electronics-only constant.
    assert web_app._unsupported_domain_message(
        domain_activation.activated_domains()) in resp.get_data(as_text=True)


def test_red_e2_10b_start_real_tie_fails_closed_non_electronics_pair(activate):
    """Non-Electronics real tie at /start. Input "hinge and app" with mechanical +
    software activated. Parent -> SINGLE(mechanical) -> /start MECHANISM_GUIDANCE
    (no UNSUPPORTED-via-ambiguity). Candidate -> AMBIGUOUS_TIE -> UNSUPPORTED fail
    closed. Distinguishing on the fail-closed message + branch."""
    from web import app as web_app
    activate("mechanical", "software")
    client = web_app.app.test_client()
    before = set(web_app.SESSION_STORE)
    resp = _start_post(client, f"{_MECH} and {_SW}")
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert set(web_app.SESSION_STORE) == before             # no session
    # Fail closed via the ambiguity branch (CF5-F002 §4.E: activation-derived
    # truthful refusal copy replaces the electronics-only constant here).
    assert web_app._unsupported_domain_message(
        domain_activation.activated_domains()) in body
    assert web_app.MECHANISM_GUIDANCE_MESSAGE not in body   # NOT the parent guidance path


# ------------------------------------------------------------- CLI RED-E2-11 -----
def _load_run_cli():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "run_cli.py")
    spec = importlib.util.spec_from_file_location("run_cli_p9e2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_red_e2_11_cli_real_tie_bounded_stop(activate, monkeypatch, capsys):
    """A REAL classifier ambiguity makes the CLI stop in bounded fashion (no
    arbitrary winner). Input "gear and catheter" with mechanical + medical_device
    activated. Parent -> SINGLE(mechanical) -> prints 'Domain inferred: mechanical'
    and proceeds. Candidate -> AMBIGUOUS_TIE -> bounded stop. Real classifier path
    (classify_domain is NOT monkeypatched)."""
    mod = _load_run_cli()
    activate("mechanical", "medical_device")
    monkeypatch.setattr(builtins, "input", lambda *_a, **_k: f"{_MECH2} and {_MED}")
    mod.run_cli()
    out = capsys.readouterr().out
    assert "CANNOT DETERMINE A SINGLE SUPPORTED DOMAIN" in out
    assert "Domain inferred:" not in out                    # no arbitrary winner printed
    assert "Domain confirmed" not in out                    # did not proceed


# ---------------------------------------------------- D4 boundary GREEN GUARD E2-12
def test_green_guard_e2_12_d4_not_manufactured(activate):
    """GREEN GUARD (NOT a distinguishing RED): classify_domain NEVER manufactures
    MULTI_DOMAIN_NEEDS_D4. A multi-activated tie is an AMBIGUOUS_TIE (equal-score
    ambiguity), never a claimed multi-domain composition; D4 stays separate and
    unexecuted. Holds on both parent and candidate for reachable inputs."""
    activate("electronics_electrical", "mechanical", "medical_device")
    for idea in (f"{_ELEC} and {_MECH2}", f"{_ELEC} and {_MECH2} and {_MED}", _ELEC):
        r = classify_domain(idea)
        assert r.kind is not DomainResultKind.MULTI_DOMAIN_NEEDS_D4


# --------------------------------------- strong-unsupported interaction (A vs B) --
# Two distinct, honestly labeled classes (do NOT overgeneralize either):
#   A. Some inputs are intercepted by the strong-unsupported heuristic. That gate is
#      a SEPARATE layer, checked AFTER classify_domain in /start, and it governs only
#      SINGLE / NONE (single-domain or classifier-miss) inputs -- e.g. a lone medical
#      token. It is NOT what fails a multi-activated tie closed.
#   B. Valid multi-activated tie inputs whose tokens are NOT strong-unsupported words
#      reach classify_domain and yield AMBIGUOUS_TIE, which /start fails closed via
#      the ambiguity branch that PRECEDES the strong-unsupported gate (see RED-E2-10).
def test_green_guard_strong_unsupported_intercepts_single_token(activate):
    """CLASS A GREEN GUARD: a lone medical token (a SINGLE / priority result, not a
    multi-activated tie) is intercepted by the strong-unsupported gate at /start.
    Behavior is identical on parent and candidate (existing safe surface)."""
    from web import app as web_app
    activate("electronics_electrical")                      # medical NOT activated
    assert web_app._has_strong_unsupported_evidence(_MED)   # 'catheter' is strong-unsupported
    client = web_app.app.test_client()
    before = set(web_app.SESSION_STORE)
    resp = _start_post(client, f"a {_MED} device")
    assert resp.status_code == 200
    assert set(web_app.SESSION_STORE) == before
    assert web_app.UNSUPPORTED_DOMAIN_MESSAGE in resp.get_data(as_text=True)


def test_green_guard_tie_tokens_not_strong_unsupported():
    """CLASS B GREEN GUARD (pure source-truth; GREEN on both parent and candidate):
    the tie tokens of RED-E2-10 / E2-10b are NOT strong-unsupported words, so the
    request is NOT masked by the pre-classifier heuristic and reaches classify_domain.
    That these inputs then classify AMBIGUOUS_TIE (the RED acceptance semantic) is
    asserted by RED-E2-2 / E2-6 / E2-10, not here."""
    from web import app as web_app
    assert web_app._has_strong_unsupported_evidence(f"{_ELEC} and {_MECH}") is False
    assert web_app._has_strong_unsupported_evidence(f"{_MECH} and {_SW}") is False


# ---------------------------------------------------------------- boundary guards -
def test_green_guard_one_activated_in_tie_is_single(activate):
    """Exactly one activated domain among the tied set -> SINGLE (unchanged, D3-D).
    A tie between an activated and a recognized-not-activated domain."""
    activate("electronics_electrical")                      # mechanical NOT activated
    r = classify_domain(f"{_ELEC} and {_MECH2}")            # scored {elec, mech}
    assert r.kind is DomainResultKind.SINGLE
    assert r.selected_domain == "electronics_electrical"


def test_green_guard_zero_activated_tie_priority_fallback_unchanged(activate):
    """No activated tied domain -> unchanged deterministic priority fallback."""
    activate("software")                                    # neither tied domain activated
    r = classify_domain(f"{_MECH2} and {_MED}")             # scored {mechanical, medical}
    assert r.kind is DomainResultKind.SINGLE
    assert r.selected_domain == "medical_device"            # priority-order fallback


def test_green_guard_no_signal_is_none():
    """No recognized signal -> NONE (unchanged)."""
    assert classify_domain("a plain idea with no domain signal").kind is DomainResultKind.NONE


def test_green_guard_electronics_only_unchanged():
    """Real activation state (electronics only): a lone electronics signal ->
    SINGLE(electronics_electrical) (unchanged; production behavior preserved)."""
    r = classify_domain(f"an {_ELEC} board")
    assert r.kind is DomainResultKind.SINGLE
    assert r.selected_domain == "electronics_electrical"
