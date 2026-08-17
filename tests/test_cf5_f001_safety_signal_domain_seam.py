"""CF5-F001 — Shared-Core Electronics-Specific Safety Signal (RED->GREEN).

Authoritative contract:
``docs/governance/CF5_F001_SAFETY_SIGNAL_CORRECTIVE_CONTRACT.md`` (merged PR
#458), implementing the independently validated finding (validation record
merged PR #457): a governed domain-keyed safety cue/context-family seam
(PARAMETERIZE; electronics family byte-preserved; the seam keys on domain
IDENTITY, never activation — NB-R4), the bounded NB-R1 cold-load domain
restoration from the already-persisted ``confirmed_domain``, and the truthful
capability-scope statement for a session domain with no governed family.

P9-MECH-SF RECONCILIATION (contract §4 items 5-6 + 13-15, disclosed): the
governed MECHANICAL family now exists through its own separately authorized
gate (exactly as this seam anticipated), so mechanical is no longer this
file's family-less example: the capability-query pin moved mechanical to the
True set, and the family-less example tests below switched to ``software`` (a
still-family-less domain) — each pin's load-bearing truth is preserved
unchanged. The vocabulary-conditional derive-() pins (r2; the MECH-envelope
cold-load) were verified UN-flipped: the mechanical vocabulary matches none of
their texts (its evidence file asserts those texts affirmatively).

Behavioral tests only. Multi-domain states are exercised via directly
constructed ``IdeaState`` domains and bounded self-restoring activation
doubles; NO real domain is activated (asserted below). The NB-R1 tests use the
REAL Flask surfaces: production ``/start``, the real answer flow (durable
accepted-answer append), a simulated memory loss (``SESSION_STORE`` entry
removed; the durable envelope remains), and the real ``show_session``
cold-load rebuild.

Signal-bearing statements are chosen deliberately:
  ANSWER_NO_TERMS -- carries failure/subject/consequence cues but NO literal
      electrical term, so live detection depends on the session DOMAIN branch
      (this is exactly the validated NB-R1 divergence);
  HAZARD_WITH_TERMS -- carries cues AND literal electrical terms, so the
      parent derives an electronics-cue signal even for a non-electronics
      session domain (the validated unconditional-exposure defect).
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation
from engine.idea_state import IdeaState
from engine.safety_signal import derive_inventor_stated_safety_signals
from engine.deliverable_assembler import assemble_deliverable
from web.app import app, SESSION_STORE, _get_store
from engine.record_contract import ProjectRecordContract
from test_p4_1b2a_durable_answer_append import answered_post

ELEC = "electronics_electrical"
MECH = "mechanical"

SEED_IDEA = "A device that watches for problems in the home"
ANSWER_NO_TERMS = ("If the alarm fails to warn people, the fire hazard could "
                   "cause harm to anyone nearby.")
HAZARD_WITH_TERMS = ("If the sensor fails to detect overcurrent, it could "
                     "cause a fire.")

_DETECTION_EMPTY_MARKER = ("no inventor-stated safety-critical failure "
                           "condition was detected")


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring activation double (no real activation)."""
    def _activate(*domains):
        monkeypatch.setattr(
            domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


def _state(domain, text):
    st = IdeaState(idea_id="cf5-f001-test")
    if domain is not None:
        st.domain = domain
        st.domain_signal = domain
    st.idea_summary = text
    return st


def _signals_block(state):
    return assemble_deliverable(state)["_session_meta"][
        "inventor_stated_safety_signals"]


def _started_answered_session(client):
    """Real /start + real answer flow; returns sid with one durable accepted
    answer carrying ANSWER_NO_TERMS. SEED_IDEA classifies as NONE; with 2
    activated domains (Mechanical Activation Execution Gate) the D2 branch
    additionally requires an explicit domain_choice."""
    r = client.post("/start", data={"idea": SEED_IDEA, "domain_confirm": ELEC,
                                     "domain_choice": ELEC},
                    follow_redirects=False)
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    resp = answered_post(client, sid,
                         {"response": ANSWER_NO_TERMS, "action": "answered"})
    assert resp.status_code == 302
    return sid


# --------------------------------------------------------- fixture honesty -------
def test_baseline_real_activation_unchanged():
    assert domain_activation.activated_domains() == [ELEC, "mechanical"]


# =========================================================================== RED
def test_red_r1_family_less_domain_gets_truthful_scope_statement():
    """r1: a session domain with NO governed safety-cue family must carry the
    truthful capability-scope statement, not the electronics detection-scoped
    empty statement (which would imply detection ran meaningfully).
    P9-MECH-SF reconciliation (contract §4 item 6, disclosed): mechanical now
    HAS a governed family, so the family-less example switched to ``software``
    — the pin's load-bearing truth is unchanged."""
    block = _signals_block(_state("software", "A daily planner app idea"))
    assert block["signals"] == []
    assert block.get("capability_scope") == "no_governed_safety_cue_family"
    assert _DETECTION_EMPTY_MARKER not in block["empty_statement"].lower()
    assert "not yet available" in block["empty_statement"].lower()
    # the truthful statement still never makes a safety determination
    assert "NOT a determination" in block["empty_statement"]


def test_red_r2_no_unconditional_electronics_cue_exposure():
    """r2: a non-electronics-domain session must NOT receive electronics-cue
    signal semantics merely because electronics vocabulary appears in its
    text (the validated unconditional-exposure defect)."""
    signals = derive_inventor_stated_safety_signals(
        _state(MECH, HAZARD_WITH_TERMS))
    assert signals == ()


def test_red_r3_cold_load_detection_matches_live():
    """r3 (NB-R1): the durably cold-loaded session derives the SAME signals as
    the live session for an accepted-answer statement without literal
    electrical terms."""
    client = app.test_client()
    sid = _started_answered_session(client)
    live = derive_inventor_stated_safety_signals(SESSION_STORE[sid]["state"])
    assert len(live) == 1                      # honest precondition, not the fix
    SESSION_STORE.pop(sid)                     # simulate memory loss
    assert client.get(f"/session/{sid}").status_code == 200   # real cold-load
    cold_state = SESSION_STORE[sid]["state"]
    cold = derive_inventor_stated_safety_signals(cold_state)
    assert [ (s.safety_subject, s.failure_condition, s.possible_consequence,
              s.domain_context, s.statement) for s in cold ] == \
           [ (s.safety_subject, s.failure_condition, s.possible_consequence,
              s.domain_context, s.statement) for s in live ]
    SESSION_STORE.pop(sid, None)


def test_red_r4_cold_load_restores_session_domain_identity():
    """r4 (NB-R1): the cold-loaded state carries the restored SAFETY-RELEVANT
    session-domain identity from the already-persisted confirmed_domain — via
    `domain_signal` ONLY (the derivation's `_domain_of` fallback). The
    mechanically-forced narrowing of contract §4 is pinned here explicitly:
    `state.domain` stays absent because it is the committed P4-1b-2a
    non-resume guard anchor (a cold-loaded session must remain unanswerable —
    complete resume is P4-2 and out of scope)."""
    client = app.test_client()
    sid = _started_answered_session(client)
    SESSION_STORE.pop(sid)
    assert client.get(f"/session/{sid}").status_code == 200
    cold_state = SESSION_STORE[sid]["state"]
    assert getattr(cold_state, "domain_signal", None) == ELEC   # restored
    assert getattr(cold_state, "domain", None) is None          # guard anchor kept
    SESSION_STORE.pop(sid, None)


def test_green_cold_load_remains_unanswerable_after_restoration():
    """Governed-boundary pin (P4-1b-2a): the NB-R1 restoration must NOT
    re-enable resume-answering — a new answered submission on a cold-loaded
    session still fails closed with no second durable append."""
    client = app.test_client()
    sid = _started_answered_session(client)
    SESSION_STORE.pop(sid)
    assert client.get(f"/session/{sid}").status_code == 200
    before = len(SESSION_STORE[sid]["state"].assertions)
    r = answered_post(client, sid, {"response": "post-restart answer attempt",
                                    "action": "answered"})
    assert r.status_code in (200, 302)          # generic, no 500
    assert len(SESSION_STORE[sid]["state"].assertions) == before
    SESSION_STORE.pop(sid, None)


# ================================================================== GREEN =======
def test_green_electronics_block_unchanged_shape_and_empty_statement():
    """§6.A/E: the electronics-rendered block carries the committed
    detection-scoped empty statement and NO capability_scope key (live
    electronics differential parity)."""
    block = _signals_block(_state(ELEC, "a plain electronics idea"))
    assert "capability_scope" not in block
    assert _DETECTION_EMPTY_MARKER in block["empty_statement"].lower()
    with_sig = _signals_block(_state(ELEC, ANSWER_NO_TERMS))
    assert "capability_scope" not in with_sig
    assert with_sig["total"] == 1
    sig = with_sig["signals"][0]
    assert set(sig.keys()) == {
        "signal_id", "source", "provenance", "safety_subject",
        "failure_condition", "possible_consequence", "domain_context",
        "validation_status", "display_label", "caution_text", "statement"}


def test_green_family_less_domain_never_crashes_or_stamps_electronics():
    """§6.C: family-less domains yield no signals for ANY text — no crash, no
    electronics domain_context stamping. P9-MECH-SF reconciliation (contract
    §4 item 14, disclosed): the first loop's example switched from mechanical
    (now family-governed) to ``software``; the second loop is unchanged."""
    for text in ("", "plain words", HAZARD_WITH_TERMS, ANSWER_NO_TERMS):
        st = _state("software", text)
        assert derive_inventor_stated_safety_signals(st) == ()
    for domain in ("medical_device", "software", "unknown_future_domain"):
        st = _state(domain, HAZARD_WITH_TERMS)
        assert derive_inventor_stated_safety_signals(st) == ()
        block = _signals_block(st)
        assert block.get("capability_scope") == "no_governed_safety_cue_family"


def test_green_domain_identity_keying_not_activation(activate):
    """§6.D (NB-R4): derivation keys on the session's domain IDENTITY, not the
    activation set — a historical electronics session still derives its
    electronics-owned signals when electronics is absent from the activation
    set."""
    activate(MECH)
    signals = derive_inventor_stated_safety_signals(
        _state(ELEC, ANSWER_NO_TERMS))
    assert len(signals) == 1
    assert signals[0].domain_context == ELEC


def test_green_legacy_missing_domain_fallback_unchanged():
    """§5 `:272` disposition: a state with NO domain keeps today's governed
    behavior — electrical context must come from the text; a derived signal is
    labeled with the electronics MVP default."""
    st = _state(None, ANSWER_NO_TERMS)          # no electrical terms -> no signal
    assert derive_inventor_stated_safety_signals(st) == ()
    st2 = _state(None, HAZARD_WITH_TERMS)       # terms present -> signal, MVP label
    signals = derive_inventor_stated_safety_signals(st2)
    assert len(signals) == 1
    assert signals[0].domain_context == ELEC


def test_green_legacy_null_envelope_cold_load_fail_safe():
    """§4 fail-safe: a legacy envelope with NULL reconstruction inputs restores
    nothing — cold-load still works and the state keeps no domain."""
    client = app.test_client()
    sid = "cf5f001-legacy-envelope-sid"
    st = IdeaState(idea_id="cf5f001-legacy")
    _get_store().create_project(ProjectRecordContract.from_state(st),
                                project_id=sid)     # NO reconstruction inputs
    SESSION_STORE.pop(sid, None)
    assert client.get(f"/session/{sid}").status_code == 200
    cold_state = SESSION_STORE[sid]["state"]
    assert getattr(cold_state, "domain", None) is None
    SESSION_STORE.pop(sid, None)


def test_green_cold_load_restores_stored_domain_verbatim():
    """§4/m4 guard: the restoration source is the persisted confirmed_domain,
    verbatim — a stored non-electronics domain is restored as itself (identity
    restoration, not admission; no activation implied). P9-MECH-SF disclosure
    (contract §4 item 15): mechanical now has a governed family, so the
    derive-() pin below holds because the seed text carries no mechanical
    cues (verified un-flipped), no longer because the domain is family-less."""
    client = app.test_client()
    sid = "cf5f001-mech-envelope-sid"
    st = IdeaState(idea_id="cf5f001-mech")
    _get_store().create_project(
        ProjectRecordContract.from_state(st), project_id=sid,
        reconstruction_inputs={
            "seed_idea_text": "a hinge idea",
            "confirmed_domain": MECH,
            "path": "N",
            "engine_contract_version":
                __import__("engine.session_reconstruction",
                           fromlist=["RECONSTRUCTION_VERSION"]).RECONSTRUCTION_VERSION,
        })
    SESSION_STORE.pop(sid, None)
    assert client.get(f"/session/{sid}").status_code == 200
    cold_state = SESSION_STORE[sid]["state"]
    assert getattr(cold_state, "domain_signal", None) == MECH   # verbatim
    assert getattr(cold_state, "domain", None) is None          # guard anchor kept
    assert derive_inventor_stated_safety_signals(cold_state) == ()
    SESSION_STORE.pop(sid, None)


def test_green_capability_query():
    """P9-MECH-SF reconciliation (contract §4 item 5, disclosed): mechanical
    moved from the False loop to the True set — its governed family now exists
    (evidence: tests/test_p9_mech_safety_cue_family.py). The electronics/None
    True pins and the remaining-domain False pins are unchanged."""
    from engine.safety_signal import has_governed_safety_cue_family
    assert has_governed_safety_cue_family(ELEC) is True
    assert has_governed_safety_cue_family(None) is True     # governed legacy default
    assert has_governed_safety_cue_family(MECH) is True     # P9-MECH-SF
    for d in ("medical_device", "software", "anything_else"):
        assert has_governed_safety_cue_family(d) is False
