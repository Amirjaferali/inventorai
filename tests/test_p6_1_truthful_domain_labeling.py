"""P6-1 — Truthful Domain Labeling Foundation (RED/GREEN).

Behaviour-based tests for gate
G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION (Option A; RESUME-01 owner language
decision applied). They prove, through REAL Flask routes rendering REAL templates
(not source grep), that user-facing session and review/deliverable surfaces show a
truthful, central Tier-1 public label for the runtime-operated electronics domain.
The central resolver keeps BOTH canonical variants (English + Arabic), but a
surface renders exactly ONE variant according to that surface's authoritative
language — never English and Arabic simultaneously (owner decision RESUME-01).
These surfaces are the <html lang="en"> (LTR) shell, so the English variant renders
and no extra Arabic dir="rtl" region is introduced (PR #148 invariant preserved).
The label never exposes the raw internal pack id, falls back to a neutral
"General idea review" for missing/unknown/unsupported state (never silently
electronics), and never emits a Tier-2/3/4 (specialist/professional/certified)
claim — while the existing disclaimers and electronics flow remain intact.

Real on-disk SQLite (autouse conftest isolation); the Flask test client; the real
central resolver `web.domain_label.public_domain_label`. No mocks; the label is
resolved server-side from trusted runtime state, never from client input.
"""
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web.domain_label import public_domain_label

EN_ELECTRONICS = "Electronics-informed review"
AR_ELECTRONICS = "مراجعة مستنيرة بمجال الإلكترونيات"
EN_MECHANICAL = "Mechanical-informed review"
AR_MECHANICAL = "مراجعة مستنيرة بمجال الميكانيكا"
EN_GENERAL = "General idea review"
AR_GENERAL = "مراجعة عامة للفكرة"
RAW_PACK_ID = "electronics_electrical"

# Tier-2/3/4 overclaim vocabulary that must never appear IN A PUBLIC LABEL.
_FORBIDDEN_LABEL_WORDS = ("Specialist", "Expert", "Professional", "Certified",
                          "Licensed", "Approved", "Feasible")

IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _start(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


# --- RED-02: the single central bilingual resolver exists & is registered ------
def test_central_resolver_module_and_filter_registered():
    assert callable(public_domain_label)
    assert app.jinja_env.filters.get("public_domain_label") is not None


# --- resolver unit behaviour (RED-04 fallback; RED-05 no overclaim) ------------
def test_resolver_maps_runtime_domain_to_tier1_bilingual():
    lbl = public_domain_label("electronics_electrical")
    assert lbl == {"en": EN_ELECTRONICS, "ar": AR_ELECTRONICS}


# --- Tier-1 EN/AR Mechanical public label (P9-MECH-QC §13; activation-readiness
# edge — labeling readiness only, NOT runtime activation; see §16) ------------
def test_resolver_maps_mechanical_to_tier1_bilingual():
    lbl = public_domain_label("mechanical")
    assert lbl == {"en": EN_MECHANICAL, "ar": AR_MECHANICAL}


def test_mechanical_label_distinct_from_electronics_label():
    elec = public_domain_label("electronics_electrical")
    mech = public_domain_label("mechanical")
    assert elec != mech
    assert elec["en"] != mech["en"]
    assert elec["ar"] != mech["ar"]


@pytest.mark.parametrize("value", [
    None, "", "   ", "medical_device", "software", "iot_electronics",
    "electronics", "ELECTRONICS_ELECTRICAL", "MECHANICAL", "unknown-thing",
    123, {"x": 1},
])
def test_resolver_falls_back_to_general_never_electronics(value):
    lbl = public_domain_label(value)
    assert lbl == {"en": EN_GENERAL, "ar": AR_GENERAL}
    # NEVER silently electronics for an unknown/invalid/unsupported id.
    assert EN_ELECTRONICS not in lbl.values()
    assert EN_MECHANICAL not in lbl.values()


def test_resolver_never_emits_tier2_3_4_wording():
    for value in ("electronics_electrical", "mechanical", None, "unknown"):
        for text in public_domain_label(value).values():
            for word in _FORBIDDEN_LABEL_WORDS:
                assert word.lower() not in text.lower(), (value, word, text)


# --- RED-01 / RED-03 : session surface renders the SINGLE-LANGUAGE public label -
# Owner decision (RESUME-01): the EN and AR variants are BOTH canonical (proven at
# the resolver level below) but MUST NOT render simultaneously on a surface — the
# variant follows the surface's authoritative language. The session shell is
# <html lang="en"> (LTR), so the English variant renders and the Arabic variant is
# NOT co-rendered (which also introduces no extra RTL region — see the PR #148
# invariant, honoured here).
def test_session_page_shows_english_public_label_not_raw_id(client):
    sid = _start(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert EN_ELECTRONICS in body            # RED-03 behavioral: bound to runtime domain
    assert AR_ELECTRONICS not in body        # owner decision: no simultaneous AR on the EN surface
    assert RAW_PACK_ID not in body           # RED-01: raw internal id removed
    assert "Domain: electronics" not in body  # old raw wording gone


def test_session_label_introduces_no_extra_rtl_region(client):
    """The public label must not add an Arabic dir="rtl" region to the English/LTR
    session surface (PR #148 Arabic/RTL invariant preserved)."""
    sid = _start(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    # The label carries no Arabic text and no rtl span of its own.
    assert AR_ELECTRONICS not in body
    assert 'dir="rtl">' + AR_ELECTRONICS not in body


# --- RED-01 / RED-03 : deliverable surface renders the SINGLE-LANGUAGE label ----
def test_deliverable_page_shows_english_public_label_not_raw_id(client):
    sid = _start(client)
    body = client.get("/session/" + sid + "/deliverable").get_data(as_text=True)
    assert EN_ELECTRONICS in body
    assert AR_ELECTRONICS not in body        # owner decision: no simultaneous AR on the EN surface
    assert RAW_PACK_ID not in body
    assert "Capability: electronics_electrical" not in body


# --- RED-04 (behavioral): missing/unknown domain state → General, not electronics
def test_session_fallback_general_when_domain_missing(client):
    """A live in-memory session whose state carries NO domain must render the
    neutral General label (English variant on the EN surface) — never silently
    electronics, and never a co-rendered Arabic variant."""
    from engine.idea_state import IdeaState
    sid = "p61-fallback-sid"
    st = IdeaState(idea_id=sid)
    st.maturity_level = 2
    st.current_stage = 3
    # deliberately do NOT set st.domain
    SESSION_STORE[sid] = {"state": st, "last_result": None, "transcript": []}
    try:
        body = client.get("/session/" + sid).get_data(as_text=True)
        assert EN_GENERAL in body
        assert AR_GENERAL not in body            # owner decision: no simultaneous AR
        assert EN_ELECTRONICS not in body        # never silently electronics
        assert AR_ELECTRONICS not in body
        assert RAW_PACK_ID not in body
    finally:
        SESSION_STORE.pop(sid, None)


# --- RED-05 (route level): no Tier-2/3/4 overclaim label surfaced --------------
def test_no_tier_overclaim_label_on_surfaces(client):
    sid = _start(client)
    for path in ("/session/" + sid, "/session/" + sid + "/deliverable"):
        body = client.get(path).get_data(as_text=True)
        # The public label region must be Tier-1 wording only. Guard against the
        # specific overclaim PHRASES (not the legitimate advisory "specialist
        # input" guidance, which is a different, allowed surface).
        for phrase in ("Electronics Specialist", "Specialist Review",
                       "Expert Review", "Professional Review", "Certified Review",
                       "Licensed Review"):
            assert phrase.lower() not in body.lower(), (path, phrase)


# --- disclaimers preserved (contract §8) --------------------------------------
def test_disclaimers_preserved_on_deliverable(client):
    sid = _start(client)
    body = client.get("/session/" + sid + "/deliverable").get_data(as_text=True)
    # The standard advisory/non-certification boundary remains visible.
    assert "certification" in body.lower()
    assert "advisory" in body.lower() or "not " in body.lower()


# --- no new domain activated; electronics entry flow intact -------------------
def test_no_new_domain_activated_unsupported_still_rejected(client):
    # A clearly non-electronics idea is still rejected at the gate (no session) —
    # P6-1 activates nothing and changes no domain-gate behaviour. (The entry
    # page's confirm-checkbox `value="electronics_electrical"` is the unchanged
    # gate INPUT, not a displayed label surface, so it is intentionally not
    # asserted here — the raw-id-removal scope is the session/deliverable surfaces
    # covered by the tests above.)
    r = client.post("/start", data={
        "idea": "A machine learning model predicts patient body temperature.",
        "domain_confirm": "electronics_electrical"})
    assert r.status_code == 200
    assert "/session/" not in (r.headers.get("Location") or "")   # no session created


def test_electronics_entry_and_session_flow_still_functional(client):
    sid = _start(client)
    assert client.get("/session/" + sid).status_code == 200
    assert client.get("/session/" + sid + "/deliverable").status_code == 200


# ===============================================================================
# Tier-1 EN/AR Mechanical public label (P9_MECHANICAL_DOMAIN_QUALIFICATION_
# CONTRACT.md §13, Requirement 9 — "activation-readiness edge"). A truthful
# Tier-1 label now exists for `mechanical` in the SAME canonical resolver used
# for electronics. Contract §16 (Requirement 12) is explicit: labeling readiness
# is NOT activation. `mechanical` is not runtime-reachable via a real `/start`
# session today (no admission path resolves `state.domain == "mechanical"`), so
# the session-surface test below uses the same bounded SESSION_STORE test-double
# pattern as `test_session_fallback_general_when_domain_missing` above to reach
# the render path directly, exactly as that established convention allows.
# ===============================================================================

def test_session_page_shows_english_mechanical_label_via_test_double(client):
    """A live in-memory session whose state carries `domain="mechanical"` must
    render the Mechanical Tier-1 English label (single-language surface rule
    unchanged) — this does not exercise any real admission/activation path."""
    from engine.idea_state import IdeaState
    sid = "p61-tier1-label-test-sid"
    st = IdeaState(idea_id=sid)
    st.maturity_level = 2
    st.current_stage = 3
    st.domain = "mechanical"
    SESSION_STORE[sid] = {"state": st, "last_result": None, "transcript": []}
    try:
        body = client.get("/session/" + sid).get_data(as_text=True)
        assert EN_MECHANICAL in body
        assert AR_MECHANICAL not in body         # owner decision: no simultaneous AR
        assert "Domain: mechanical" not in body   # raw pack id not leaked as old-style wording
    finally:
        SESSION_STORE.pop(sid, None)


def test_tier1_label_alone_does_not_activate_mechanical(monkeypatch):
    """Historical claim of the Tier-1-label gate, preserved in isolation: adding
    the Tier-1 label (that gate's ONLY change) does not itself move
    `activated_domains()`. Reconstructed here via a local pin to that gate's
    exact pre-activation state — mechanical was subsequently, separately, and
    explicitly Owner-authorized for real activation (Mechanical Activation
    Execution Gate); see test_mechanical_idea_now_activated_via_real_
    activation_not_label below for the current real state."""
    import engine.domain_activation as domain_activation
    monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS",
                         frozenset({"electronics_electrical"}))
    assert domain_activation.activated_domains() == ["electronics_electrical"]
    assert "mechanical" not in domain_activation.activated_domains()


def test_mechanical_now_really_activated_not_by_label_alone():
    """Current real state: mechanical IS activated — but this is the effect of
    the separate, explicit Mechanical Activation Execution Gate, never the
    Tier-1 label by itself (see the pinned test above, which proves the label
    alone never moved activation)."""
    import engine.domain_activation as domain_activation
    assert domain_activation.activated_domains() == ["electronics_electrical", "mechanical"]


def test_start_domain_picker_offers_only_activated_domains(client):
    """The `/start` entry page's real D2 explicit-choice picker (rendered on a
    NONE-classified idea, per `web/app.py`'s `choice_domains=activated`) is
    driven exclusively by `activated_domains()`, never by the Tier-1 label
    catalog or the full domain-registry recognized set. `/start` is POST-only
    (a bare GET never reaches this picker), so this exercises the real
    production POST flow. Corrects a prior vacuous version of this test that
    used `client.get("/start")` (405, generic error page) and so passed
    regardless of real picker content; also corrects that prior version's now-
    stale premise (written before Mechanical's real, explicit Owner-authorized
    activation) that Mechanical must NOT be offered — Mechanical is now
    genuinely activated and is correctly offered."""
    import engine.domain_activation as domain_activation
    idea = "A gadget that watches for a problem and warns the homeowner right away"
    body = client.post("/start", data={"idea": idea}).get_data(as_text=True)
    offered = set(re.findall(r'name="domain_choice" value="([^"]+)"', body))
    assert offered == set(domain_activation.activated_domains())
    assert offered == {"electronics_electrical", "mechanical"}
    assert 'value="medical_device"' not in body
    assert 'value="software"' not in body


def test_tier1_label_alone_did_not_widen_admission_at_entry_gate(client, monkeypatch):
    """Historical claim of the Tier-1-label gate, preserved in isolation: with
    ONLY the Tier-1 label added (not real activation), a clearly-Mechanical
    idea confirmed as mechanical was still rejected at the gate (no session) —
    the label alone never widened admission. Reconstructed here via a local
    pin to that gate's exact pre-activation state."""
    import engine.domain_activation as domain_activation
    monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS",
                         frozenset({"electronics_electrical"}))
    r = client.post("/start", data={
        "idea": "A mechanical latch uses a spring and a lever to release a hinge.",
        "domain_confirm": "mechanical"})
    assert r.status_code == 200
    assert "/session/" not in (r.headers.get("Location") or "")


def test_mechanical_idea_now_admitted_via_real_activation_not_label(client):
    """Current real state: the SAME idea, confirmed as mechanical, is now
    admitted — the effect of the separate, explicit Mechanical Activation
    Execution Gate (real allowlist change), never the Tier-1 label by itself
    (see the pinned test above)."""
    before = set(SESSION_STORE)
    r = client.post("/start", data={
        "idea": "A mechanical latch uses a spring and a lever to release a hinge.",
        "domain_confirm": "mechanical"}, follow_redirects=False)
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None
    assert entry["state"].domain == "mechanical"
    SESSION_STORE.pop(sid, None)
    assert set(SESSION_STORE) == before


def test_mechanical_label_owner_is_unique_not_duplicated_in_picker_helper():
    """The picker's separate, lower-tier `_domain_label()` helper (raw
    `.title()`-cased, `web/app.py`) must never independently reproduce the
    canonical Tier-1 Mechanical wording — there is exactly one owner."""
    assert webapp._domain_label("mechanical") == "Mechanical"
    assert webapp._domain_label("mechanical") != EN_MECHANICAL
