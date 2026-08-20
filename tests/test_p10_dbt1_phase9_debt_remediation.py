"""P10-DBT1 — Phase-9 Registered-Debt Remediation (closure record §5 items 1, 2, 4, 5).

File-creation contract:
  Path: tests/test_p10_dbt1_phase9_debt_remediation.py
  Purpose: remediate the post-Phase-9 debts registered in
    docs/governance/PHASE_9_FORMAL_CLOSURE_RECORD.md §5 — (4) the missing single
    REAL admission→Tier-1-render E2E chain test for Mechanical (no activation or
    session doubles anywhere in the chain), (5) the missing REAL-activation CLI
    banner pin, and truth guards for the repairs of (1) the stale
    ``classify_domain`` docstring and (2) the four registered stale pre-activation
    test-file comments.
  Input contract: the live web app (``web.app``), the live activation state
    (``engine.domain_activation``), ``scripts/run_cli.py`` loaded by path, and the
    on-disk text of the five registered stale sites.
  Output contract: pass/fail evidence only; every admitted session is removed in
    ``finally``; no durable artifact is left behind (conftest DB isolation applies).
  Prohibited behaviors: NO monkeypatching of ``_ACTIVATED_DOMAINS`` or
    ``SESSION_STORE`` seeding in the E2E/banner sections (the point of debt (4)/(5)
    is the REAL state; the only patch anywhere is the CLI ``input`` I/O harness);
    no behavior change to the four repaired test files is implied or tested here —
    their own suites remain the behavior authority.

§5 item 3 (UI_B_START_024) is deliberately NOT addressed: it is separately
dispositioned non-blocking by L10N_RH01_FORMAL_CLOSURE_RECORD.md.
"""
import builtins
import importlib.util
import io
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation, domain_rules
from web.app import app, SESSION_STORE
from web.domain_label import public_domain_label

_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

MECH_IDEA = "A hinge mounted bracket with a lever and a spring latch"
EN_MECHANICAL = "Mechanical-informed review"
AR_MECHANICAL = "مراجعة مستنيرة بمجال الميكانيكا"
EN_ELECTRONICS = "Electronics-informed review"


def _client():
    app.config["TESTING"] = True
    return app.test_client()


def _read(relpath):
    with open(os.path.join(_REPO, relpath), encoding="utf-8") as fh:
        return fh.read()


# ==========================================================================
# §5 debt (4) — REAL admission→Tier-1-render E2E chain (no doubles anywhere)
# ==========================================================================
def test_real_activation_state_is_the_chain_precondition():
    """The chain below runs against the REAL activation state — assert it so a
    future activation change fails HERE with an honest message instead of
    silently converting the E2E test into a doubles test."""
    assert domain_activation.activated_domains() == [
        "electronics_electrical", "mechanical"]


def test_real_mechanical_admission_to_tier1_render_e2e_chain():
    """The single real E2E chain registered missing by PHASE_9_FORMAL_CLOSURE_
    RECORD.md §5(4): real classification of a mechanical idea → real /start
    consent offer → real confirmed admission → real session whose persisted
    state carries domain='mechanical' → real session render showing the Tier-1
    English public label. No activation double, no SESSION_STORE seeding."""
    client = _client()

    # 1. Unconfirmed POST: the real classifier + real activation state offer
    #    mechanical under explicit consent (no session yet).
    before = set(SESSION_STORE)
    offer = client.post("/start", data={"idea": MECH_IDEA})
    assert offer.status_code == 200
    offer_body = offer.get_data(as_text=True)
    assert 'name="domain_confirm"' in offer_body
    assert 'value="mechanical"' in offer_body
    assert set(SESSION_STORE) == before          # consent-first: nothing admitted

    # 2. Confirmed POST: real admission.
    admitted = client.post(
        "/start", data={"idea": MECH_IDEA, "domain_confirm": "mechanical"})
    assert admitted.status_code == 302
    assert "/session/" in admitted.headers["Location"]
    sid = admitted.headers["Location"].rsplit("/", 1)[-1]
    try:
        assert SESSION_STORE[sid]["state"].domain == "mechanical"

        # 3. Real Tier-1 render on the live session surface.
        body = client.get("/session/" + sid).get_data(as_text=True)
        assert EN_MECHANICAL in body                    # Tier-1 EN label rendered
        assert AR_MECHANICAL not in body                # single-language surface rule
        assert "Domain: mechanical" not in body         # raw pack id not leaked
        assert EN_ELECTRONICS not in body               # never mislabeled electronics
    finally:
        SESSION_STORE.pop(sid, None)


def test_chain_label_source_is_the_canonical_resolver():
    """The label asserted above is the canonical Tier-1 resolver output — the
    E2E test and the resolver can never drift apart silently."""
    assert public_domain_label("mechanical")["en"] == EN_MECHANICAL
    assert public_domain_label("mechanical")["ar"] == AR_MECHANICAL


# ==========================================================================
# §5 debt (5) — REAL-activation CLI banner pin (no activation double)
# ==========================================================================
def test_real_cli_banner_names_both_activated_domains(monkeypatch, capsys):
    """The multi-activated banner wording was previously pinned only under the
    self-restoring activation double; this pins it against the REAL state.
    (The only patch here is the ``input`` I/O harness — not an activation
    double.)"""
    path = os.path.join(_REPO, "scripts", "run_cli.py")
    spec = importlib.util.spec_from_file_location("run_cli_p10dbt1", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(builtins, "input", lambda *_a, **_k: "")
    mod.run_cli()
    out = capsys.readouterr().out
    assert "  Scope: Electronics Electrical or Mechanical, Level 0-2" in out
    assert "Scope: Electronics/Electrical, Level 0-2" not in out   # stale claim absent


# ==========================================================================
# §5 debts (1) + (2) — truth guards over the five repaired stale sites
# ==========================================================================
def test_classify_domain_docstring_no_longer_claims_unreachable():
    """§5(1): the docstring claimed the AMBIGUOUS_TIE branch is
    'production-unreachable today' under an electronics-only activation state —
    false since the governed Mechanical activation."""
    doc = domain_rules.classify_domain.__doc__
    assert "production-unreachable today" not in doc
    assert "(``electronics_electrical`` only)" not in doc
    assert "production-reachable" in doc               # truthful current state


def test_tie_precedence_file_comment_truthful():
    """§5(2): the file claimed the real runtime state 'remains'
    electronics-only and the tie branch 'production-unreachable today' —
    contradicting its own real-state assertion."""
    text = _read("tests/test_p9e2_multi_activated_tie_precedence.py")
    assert "production-unreachable today" not in text
    assert "== ['electronics_electrical']`` (asserted below)" not in text
    assert "'electronics_electrical', 'mechanical'" in text


def test_i5_file_comment_historically_framed():
    """§5(2): the recorded evidence verdict stays untouched; only the
    present-tense activation claim becomes explicitly historical."""
    text = _read("tests/test_p9_mech_i5_question_sufficiency.py")
    assert "Mechanical remains NOT QUALIFIED and NOT ACTIVATED" not in text
    assert "VERDICT (recorded)" in text                # evidence verdict preserved


def test_safety_cue_file_comment_historically_framed():
    text = _read("tests/test_p9_mech_safety_cue_family.py")
    assert "Mechanical remains NOT ACTIVATED" not in text
    assert "NEVER a safety determination" in text      # semantics record preserved


def test_p6_1_file_comment_truthful_about_reachability():
    """§5(2): 'mechanical is not runtime-reachable via a real /start session
    today' — false since activation; the double-based render-path unit test
    remains valid, and the real chain now lives in THIS file."""
    text = _read("tests/test_p6_1_truthful_domain_labeling.py")
    assert "is not runtime-reachable via a real" not in text
    assert "test_p10_dbt1_phase9_debt_remediation" in text   # forward pointer


def test_closure_record_register_untouched():
    """The §5 debt REGISTER is a frozen closure record: remediation is recorded
    in the live governance surfaces, never by rewriting the register itself
    ('This closure does NOT claim any of them fixed' must survive verbatim)."""
    text = _read("docs/governance/PHASE_9_FORMAL_CLOSURE_RECORD.md")
    assert "This closure does NOT claim any of them fixed" in text
    assert "Missing a single real admission→Tier-1-render E2E chain test" in text
