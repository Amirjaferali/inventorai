"""CF5-F002 / CF-6 — Web ``/start`` Multi-Domain Admission (RED->GREEN).

Authoritative contract:
``docs/governance/CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md`` (base §4
matrix A-G + §9 RED r1-r6, as re-scoped by Amendment 01 §14: amended production
allowlist §14.1 and rendered-UI acceptance U1-U5 §14.2). Owner policy under test
is D-CF5-F002-01 (``OWNER_DECISION_REGISTER.md``): D1 "confirm classifier-selected
activated domain", D2 "NONE under >1 activated domain requires explicit user
choice", D3 "Electronics-absent derives from the activation set" plus the derived
corner "NONE with exactly one activated domain offers that sole domain under
explicit consent".

Behavioral tests only, against the REAL Flask ``/start`` route (test client) and
the REAL rendered ``/start`` UI. Multi-activation states are exercised ONLY via
bounded, self-restoring test doubles of the 5-I2 activation allowlist
(``engine.domain_activation._ACTIVATED_DOMAINS``) — the committed P9-E2/§5-I2
mechanism. NO real domain is activated; the real runtime state remains
``activated_domains() == ['electronics_electrical']`` (asserted below).

Idea inputs are verified against the live registry / classifier:
  ELEC_IDEA      -> SINGLE(electronics_electrical)
  MECH_IDEA      -> SINGLE(mechanical); no strong-unsupported token; no lay token
  MECH_IDEA_LAY  -> SINGLE(mechanical); no strong-unsupported token; 1 lay token
                    ("switch") — the sharpest parent cross-domain-mislabel input
  MECH_IDEA_STRONG -> SINGLE(mechanical); strong-unsupported mechanical tokens
  MED_IDEA       -> SINGLE(medical_device); strong-unsupported medical tokens
  SW_IDEA        -> SINGLE(software); no strong-unsupported token
  NONE_IDEA      -> NONE
  TIE_IDEA       -> electronics/mechanical 1-1 tie: SINGLE(electronics) under
                    electronics-only; AMBIGUOUS_TIE when both are activated

Session hygiene: every admission test pops its created ``SESSION_STORE`` entry;
refusal tests assert no new ``SESSION_STORE`` entry is created (the conftest
autouse fixtures additionally isolate and clear the durable store per test).
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation
from web.app import (
    app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE,
    CONFIRMATION_REQUIRED_MESSAGE, MECHANISM_GUIDANCE_MESSAGE,
)

ELEC = "electronics_electrical"
MECH = "mechanical"
MED = "medical_device"
SW = "software"

ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
MECH_IDEA = "A hinge mounted bracket with a lever and a spring latch"
MECH_IDEA_LAY = "A hinge mounted bracket with a lever and a small switch"
MECH_IDEA_STRONG = "A gear and pulley hoist with a crankshaft drive"
MED_IDEA = "A catheter guide with an implantable stent"
SW_IDEA = "An app to organize daily schedules"
NONE_IDEA = "something with no recognizable signals at all"
TIE_IDEA = "circuit and hinge"


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring activation double (no real activation).

    Restored automatically by monkeypatch teardown."""
    def _activate(*domains):
        monkeypatch.setattr(
            domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


@pytest.fixture
def client():
    return app.test_client()


def _post(client, idea, confirm=None, choice=None):
    data = {"idea": idea}
    if confirm is not None:
        data["domain_confirm"] = confirm
    if choice is not None:
        data["domain_choice"] = choice
    return client.post("/start", data=data, follow_redirects=False)


def _admitted_domain(resp):
    """Assert ``resp`` admitted a session; return the persisted state.domain and
    remove the runtime entry (session hygiene)."""
    assert resp.status_code == 302, "expected an admitted session (302 redirect)"
    assert "/session/" in resp.headers["Location"]
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.pop(sid)
    return entry["state"].domain


# --------------------------------------------------------- fixture honesty -------
def test_baseline_real_activation_unchanged():
    # No real domain is activated by this file's doubles.
    assert domain_activation.activated_domains() == [ELEC]


# =========================================================================== RED
# §9 r1-r6: reproduce the latent defect under activation doubles. Each fails on
# the authoritative parent and passes after the bounded generalization.

def test_red_r1_activated_second_domain_idea_admittable(activate, client):
    """r1: an ACTIVATED second domain's idea must no longer be refused
    ("electronics only"). Full D1 flow ends in an admitted mechanical session."""
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    first = _post(client, MECH_IDEA)
    assert first.status_code == 200
    body = first.get_data(as_text=True)
    # Not a refusal: the classifier-selected activated domain is presented.
    assert UNSUPPORTED_DOMAIN_MESSAGE not in body
    assert MECHANISM_GUIDANCE_MESSAGE not in body
    assert 'name="domain_confirm"' in body and 'value="mechanical"' in body
    assert set(SESSION_STORE) == before          # presentation creates no session
    second = _post(client, MECH_IDEA, confirm=MECH)
    assert _admitted_domain(second) == MECH


def test_red_r2_no_wrong_electronics_session_for_activated_domain(activate, client):
    """r2: an activated second-domain input must NOT be admitted under a WRONG
    electronics session (cross-domain mislabel — validated defect P-E.3)."""
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    resp = _post(client, MECH_IDEA_LAY, confirm=ELEC)
    # The parent 302-admits this as an electronics session. Corrected behavior:
    # no admission under a mislabeling confirmation; no session is created.
    assert resp.status_code != 302
    assert set(SESSION_STORE) == before
    for entry in SESSION_STORE.values():
        assert entry["state"].domain != ELEC or True  # no new entries at all


def test_red_r3_confirmation_path_exists_for_second_domain(activate, client):
    """r3: a confirmation path must exist for the second activated domain
    (the parent accepts ONLY the hardcoded electronics confirm value)."""
    activate(ELEC, MECH)
    resp = _post(client, MECH_IDEA, confirm=MECH)
    assert _admitted_domain(resp) == MECH


def test_red_r4_stale_strong_vocabulary_must_not_block_activated_domain(activate, client):
    """r4 (CF-6 facet): static strong-unsupported vocabulary must not refuse an
    idea whose domain is ACTIVATED."""
    activate(ELEC, MED)
    first = _post(client, MED_IDEA)
    assert first.status_code == 200
    body = first.get_data(as_text=True)
    assert UNSUPPORTED_DOMAIN_MESSAGE not in body
    assert 'value="medical_device"' in body
    second = _post(client, MED_IDEA, confirm=MED)
    assert _admitted_domain(second) == MED


def test_red_r5_electronics_absent_no_500(activate, client):
    """r5 (D3): with Electronics absent from the activation set, /start must not
    crash with DomainNotActivatedError / HTTP 500."""
    activate(MECH)
    before = set(SESSION_STORE)
    resp = _post(client, NONE_IDEA, confirm=ELEC)
    # Parent: NONE-fallback admission calls
    # _admit_specialist_domain("electronics_electrical") -> 500.
    assert resp.status_code == 200
    assert set(SESSION_STORE) == before


def test_red_r6_public_copy_truthful_after_broadening(activate, client):
    """r6 (§4.E, bounded CF-2 facet): the rendered /start surface must not
    assert "electronics only" when another specialist domain is activated."""
    activate(ELEC, MECH)
    body = client.get("/").get_data(as_text=True)
    assert "Currently supported: electronics and electrical ideas." not in body
    assert "Mechanical" in body


# ================================================ §4.A backward compatibility ===
# Current Electronics-only activation — NO user-visible regression. These pin the
# authoritative-parent behavior; they pass before AND after the change.

def test_a_electronics_idea_admitted_with_confirmation(client):
    resp = _post(client, ELEC_IDEA, confirm=ELEC)
    assert _admitted_domain(resp) == ELEC


def test_a_no_confirmation_refused_exact_message_no_session(client):
    before = set(SESSION_STORE)
    resp = _post(client, ELEC_IDEA)
    assert resp.status_code == 200
    assert CONFIRMATION_REQUIRED_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before


def test_a_none_fallback_admitted_as_electronics_with_confirmation(client):
    resp = _post(client, NONE_IDEA, confirm=ELEC)
    assert _admitted_domain(resp) == ELEC


def test_a_recognized_not_activated_weak_conflict_guided_no_session(client):
    before = set(SESSION_STORE)
    resp = _post(client, MECH_IDEA, confirm=ELEC)
    assert resp.status_code == 200
    assert MECHANISM_GUIDANCE_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before


def test_a_strong_unsupported_refused_unchanged_no_session(client):
    before = set(SESSION_STORE)
    resp = _post(client, MED_IDEA, confirm=ELEC)
    assert resp.status_code == 200
    assert UNSUPPORTED_DOMAIN_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before


def test_a_corroborated_lay_electrical_admission_unchanged(client):
    # The governed Entry-UX weak-conflict resolution is preserved byte-for-byte
    # under the current electronics-only activation state.
    resp = _post(client, MECH_IDEA_LAY, confirm=ELEC)
    assert _admitted_domain(resp) == ELEC


def test_a_u4_rendered_consent_ui_backward_compatible(client):
    """U4: under ['electronics_electrical'] the rendered consent UI is
    behaviorally identical to the authoritative parent."""
    body = client.get("/").get_data(as_text=True)
    assert 'name="domain_confirm"' in body
    assert 'value="electronics_electrical"' in body
    assert "required" in body
    assert ("I confirm that this idea is primarily an electronics or "
            "electrical idea.") in body
    assert "Currently supported: electronics and electrical ideas." in body
    assert "Describe your electronics or electrical invention..." in body
    assert 'name="domain_choice"' not in body     # no chooser under one domain


# ============================================= §4.B Electronics + one activated ==

def test_b_u1_single_electronics_presented_and_admitted(activate, client):
    """U1: classifier-selected electronics is presented for explicit confirm
    (no manual chooser), then admitted with the electronics confirmation."""
    activate(ELEC, MECH)
    first = _post(client, ELEC_IDEA)
    assert first.status_code == 200
    body = first.get_data(as_text=True)
    assert 'value="electronics_electrical"' in body
    assert 'name="domain_choice"' not in body     # no chooser when resolved
    second = _post(client, ELEC_IDEA, confirm=ELEC)
    assert _admitted_domain(second) == ELEC


def test_b_u1_no_auto_admit_without_confirmation(activate, client):
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    resp = _post(client, MECH_IDEA)
    assert resp.status_code == 200                # presented, NOT auto-admitted
    assert set(SESSION_STORE) == before


def test_b_u2_none_requires_explicit_choice_among_activated_only(activate, client):
    """U2: NONE + >=2 activated -> the chooser presents ONLY currently activated
    domains; choose-then-confirm persists the chosen+confirmed domain."""
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    first = _post(client, NONE_IDEA)
    assert first.status_code == 200
    body = first.get_data(as_text=True)
    assert 'name="domain_choice"' in body
    assert 'value="electronics_electrical"' in body
    assert 'value="mechanical"' in body
    assert 'value="medical_device"' not in body   # recognized-not-activated absent
    assert 'value="software"' not in body
    assert set(SESSION_STORE) == before
    chosen = _post(client, NONE_IDEA, choice=MECH)
    assert chosen.status_code == 200              # chosen, still needs confirm
    chosen_body = chosen.get_data(as_text=True)
    assert 'name="domain_confirm"' in chosen_body
    assert 'value="mechanical"' in chosen_body
    assert set(SESSION_STORE) == before
    final = _post(client, NONE_IDEA, choice=MECH, confirm=MECH)
    assert _admitted_domain(final) == MECH


def test_b_none_has_no_silent_default(activate, client):
    """D2: NONE under multi-activation never silently falls back to
    Electronics (or any default)."""
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    resp = _post(client, NONE_IDEA, confirm=ELEC)  # parent's fallback submission
    assert resp.status_code != 302
    assert set(SESSION_STORE) == before


def test_b_recognized_not_activated_inadmissible(activate, client):
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    resp = _post(client, SW_IDEA, confirm=SW)
    assert resp.status_code == 200
    assert set(SESSION_STORE) == before


def test_b_ambiguous_tie_fail_closed(activate, client):
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    for confirm in (None, ELEC, MECH):
        resp = _post(client, TIE_IDEA, confirm=confirm)
        assert resp.status_code == 200
        assert set(SESSION_STORE) == before


def test_b_strong_vocabulary_does_not_suppress_activated_mechanical(activate, client):
    """CF-6 facet: strong mechanical vocabulary must not refuse mechanical once
    mechanical is activated."""
    activate(ELEC, MECH)
    first = _post(client, MECH_IDEA_STRONG)
    assert first.status_code == 200
    assert UNSUPPORTED_DOMAIN_MESSAGE not in first.get_data(as_text=True)
    second = _post(client, MECH_IDEA_STRONG, confirm=MECH)
    assert _admitted_domain(second) == MECH


def test_b_strong_vocabulary_still_blocks_non_activated_families(activate, client):
    """CF-6 boundary: vocabulary families whose domain is NOT activated still
    refuse (medical stays strong-unsupported while only elec+mech are active)."""
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    resp = _post(client, MED_IDEA, confirm=ELEC)
    assert resp.status_code == 200
    assert set(SESSION_STORE) == before


# ==================================== §4.C Electronics-absent activation (D3) ====

def test_c_sole_non_electronics_domain_flow(activate, client):
    """No Electronics special case: GET / presents the sole activated domain;
    classified+confirmed mechanical admits and persists mechanical."""
    activate(MECH)
    body = client.get("/").get_data(as_text=True)
    assert 'name="domain_confirm"' in body
    assert 'value="mechanical"' in body
    assert 'value="electronics_electrical"' not in body
    resp = _post(client, MECH_IDEA, confirm=MECH)
    assert _admitted_domain(resp) == MECH


def test_c_u3_none_sole_activated_domain_explicit_consent(activate, client):
    """U3 / derived corner: NONE with exactly one activated domain offers that
    sole domain under explicit consent; without consent -> no session."""
    activate(MECH)
    before = set(SESSION_STORE)
    unconfirmed = _post(client, NONE_IDEA)
    assert unconfirmed.status_code == 200
    assert set(SESSION_STORE) == before
    confirmed = _post(client, NONE_IDEA, confirm=MECH)
    assert _admitted_domain(confirmed) == MECH


def test_c_electronics_idea_inadmissible_when_electronics_not_activated(activate, client):
    activate(MECH)
    before = set(SESSION_STORE)
    resp = _post(client, ELEC_IDEA, confirm=ELEC)
    assert resp.status_code == 200
    assert set(SESSION_STORE) == before


def test_c_two_non_electronics_domains_choice(activate, client):
    """Electronics-absent multi-activation: D2 choice among {mechanical,
    software} only; chosen+confirmed persists."""
    activate(MECH, SW)
    first = _post(client, NONE_IDEA)
    body = first.get_data(as_text=True)
    assert 'name="domain_choice"' in body
    assert 'value="mechanical"' in body and 'value="software"' in body
    assert 'value="electronics_electrical"' not in body
    final = _post(client, NONE_IDEA, choice=SW, confirm=SW)
    assert _admitted_domain(final) == SW


# ======================================= §4.D three-plus activated (no D4) =======

def test_d_three_activated_single_confirm_flow(activate, client):
    activate(ELEC, MECH, MED)
    resp = _post(client, MECH_IDEA, confirm=MECH)
    assert _admitted_domain(resp) == MECH


def test_d_three_activated_none_choice_is_full_activated_set(activate, client):
    activate(ELEC, MECH, MED)
    body = _post(client, NONE_IDEA).get_data(as_text=True)
    assert 'value="electronics_electrical"' in body
    assert 'value="mechanical"' in body
    assert 'value="medical_device"' in body
    assert 'value="software"' not in body
    final = _post(client, NONE_IDEA, choice=MED, confirm=MED)
    assert _admitted_domain(final) == MED


def test_d_three_activated_tie_fail_closed(activate, client):
    activate(ELEC, MECH, MED)
    before = set(SESSION_STORE)
    resp = _post(client, TIE_IDEA, confirm=ELEC)
    assert resp.status_code == 200
    assert set(SESSION_STORE) == before


# ================================================= §4.E truthful messaging =======

def test_e_refusal_copy_truthful_under_broadened_activation(activate, client):
    activate(ELEC, MECH)
    body = _post(client, MED_IDEA, confirm=ELEC).get_data(as_text=True)
    assert "electronics and electrical ideas only" not in body


# ============================================== §4.F session-domain integrity ====

def test_f_mismatched_confirmation_never_admits(activate, client):
    """Persisted domain must equal the classified+confirmed domain exactly; a
    confirmation for a DIFFERENT activated domain re-presents, never admits."""
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    resp = _post(client, MECH_IDEA, confirm=ELEC)
    assert resp.status_code != 302
    assert set(SESSION_STORE) == before


def test_f_tampered_choice_outside_activated_set_never_admits(activate, client):
    """m6/m12 guard: a forged domain_choice / domain_confirm for a
    recognized-but-not-activated domain must not admit — and must be refused in
    a CONTROLLED way (a 200 re-presentation, never a 500 crash: the choice
    validation must reject it before the §5-I2 admission gate has to)."""
    activate(ELEC, MECH)
    before = set(SESSION_STORE)
    resp = _post(client, NONE_IDEA, choice=MED, confirm=MED)
    assert resp.status_code == 200
    assert set(SESSION_STORE) == before


def test_f_d2_persists_exactly_chosen_confirmed_domain(activate, client):
    activate(ELEC, MECH)
    final = _post(client, NONE_IDEA, choice=ELEC, confirm=ELEC)
    assert _admitted_domain(final) == ELEC


# ============================================ §4.G / U5 ui_lang independence =====

def test_g_u5_ui_language_does_not_alter_admission_or_domains(activate, client):
    activate(ELEC, MECH)
    with client.session_transaction() as sess:
        sess["ui_lang"] = "ar"
    body = _post(client, NONE_IDEA).get_data(as_text=True)
    assert 'value="electronics_electrical"' in body
    assert 'value="mechanical"' in body
    assert 'value="medical_device"' not in body
    resp = _post(client, MECH_IDEA, confirm=MECH)
    assert _admitted_domain(resp) == MECH
