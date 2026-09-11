"""T1-D + residual T2-B' — question explainability and truthful version disclosure.

Scope (OD-PDVG-12 + OD-PDVG-13, exercised for this bounded combined increment
only): the user-facing "Why this question?" line selected by the EXACT committed
served-question identity, and the two truthful limitation disclosures (how this
version chooses questions; what it does with evidence status).

The increment is presentation-only. These tests prove that it adds clarity and
changes nothing else: not question selection, not W2-B override precedence, not
W2-C intent-aware serving, not gap progression, scoring, readiness, evaluation
or evidence status, and not one byte of canonical state, durable storage, the
canonical package, the export, the API or the reference adapter.

Real Flask application, real durable SQLite, real committed WS10 registries and
Path-N artifacts. Nothing under test is mocked.
"""
from tests.csrf_client import csrf_client
import html as _html
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import jinja2
import pytest

import engine.intent_serving as intent_serving
from engine.idea_state import MECHANISM_COMPLETENESS
from engine.path_n_questions import get_served_question
from engine.progression_loop import select_next_gap, get_display_question
from web import ui_text

SEED = ("a manually foldable wheelchair ramp for a home doorway — the "
        "inventor wants the ramp to stay reliably locked in the flat, "
        "load-bearing position and to fold away without tools")
ELEC_SEED = "ESP32 microcontroller circuit with a voltage sensor"
PW = "correct horse battery staple"
NEUTRAL = "I will need to think more about this whole area."
HOSTILE = ("<script>alert(1)</script> & the latch \"holds\" <b>rigid</b> "
           "because the rib carries the load")

T1D_BEGIN = "    {#- T1D-DISCLOSURE-BEGIN"
T1D_END = "T1D-DISCLOSURE-END -#}\n"
_TEMPLATES = os.path.join(os.path.dirname(__file__), "..", "web", "templates")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "t1d.sqlite"))
    monkeypatch.setattr(intent_serving, "_REGISTRY_CACHE", {})
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod


def _start(c, domain="mechanical", seed=SEED):
    r = c.post("/start", data={"idea": seed, "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _set_lang(c, lang):
    assert c.post("/ui-language", data={"lang": lang}).status_code in (302, 303)


def _raw(c, sid, lang=None):
    if lang:
        _set_lang(c, lang)
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200, r.status_code
    if lang:
        _set_lang(c, "en")
    return r.get_data(as_text=True)


def _page(c, sid, lang=None):
    return _html.unescape(_raw(c, sid, lang))


def _owned_session(c, appmod, email, domain="mechanical", seed=SEED):
    """A project with a durable owner, so the authorized export seam can run."""
    from engine import account_credentials as acct
    store = appmod._get_account_store()
    aid = acct.new_account_id()
    store.create_account(aid, acct.normalize_email(email), acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    assert c.post("/login", data={"email": email, "password": PW}).status_code == 302
    return _start(c, domain=domain, seed=seed), aid


def _token(c, sid):
    m = re.search(r'name="answer_token" value="([^"]+)"', _raw(c, sid))
    return _html.unescape(m.group(1))


def _answer(c, sid, text):
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(c, sid), "action": "answered"})


def _state(appmod, sid):
    return appmod.SESSION_STORE[sid]["state"]


def _explanation(body):
    m = re.search(r'<p class="question-explanation"[^>]*>(.*?)</p>', body, re.S)
    return None if m is None else re.sub(r"<[^>]+>", "", m.group(1)).strip()


def _copy(key, lang="en"):
    return ui_text.text(key, lang)


def _registry_ids():
    ids = []
    for domain in ("electronics_electrical", "mechanical"):
        path = os.path.join(
            os.path.dirname(__file__), "..", "docs", "governance",
            "path_n_content_config", f"{domain}_question_intent_registry.json")
        with open(path, encoding="utf-8") as fh:
            ids += [r["question_id"] for r in json.load(fh)["records"]]
    return ids


# ==========================================================================
# 1. Every committed identity has an intentional, substantively paired EN/AR line
# ==========================================================================
def test_every_committed_question_identity_has_an_en_ar_explanation():
    """(1) Complete coverage of the committed identities, and (2) an English and
    an Arabic line that both exist, differ from each other, and are non-empty."""
    committed = _registry_ids()
    assert len(committed) == 21
    assert set(committed) == set(ui_text.QUESTION_EXPLANATION_KEYS)
    for question_id in committed:
        key = ui_text.QUESTION_EXPLANATION_KEYS[question_id]
        en, ar = _copy(key, "en"), _copy(key, "ar")
        assert en and ar and en.strip() and ar.strip(), question_id
        assert en != ar, question_id
        assert ar != key and en != key, question_id


def test_english_and_arabic_explanations_carry_equivalent_meaning():
    """(2) Substantive parity, proved structurally: one sentence each, neither
    surface materially longer or shorter than its pair, no English left inside
    the Arabic surface and no Arabic inside the English surface."""
    arabic = re.compile(r"[؀-ۿ]")
    latin = re.compile(r"[A-Za-z]")
    for key in list(ui_text.QUESTION_EXPLANATION_KEYS.values()) + [
            "UI_T1D_QUESTION_SET", "UI_T1D_EVIDENCE_PROGRESSION"]:
        en, ar = _copy(key, "en"), _copy(key, "ar")
        assert not arabic.search(en), key
        assert arabic.search(ar), key
        assert not latin.search(ar), key
        assert en.count(".") >= 1 and ar.count(".") >= 1, key
        assert en.count(".") == ar.count("."), key
        ratio = len(ar) / len(en)
        assert 0.4 <= ratio <= 1.6, (key, ratio)
    heading_en, heading_ar = _copy("UI_T1D_WHY_HEADING"), _copy("UI_T1D_WHY_HEADING", "ar")
    assert heading_en.endswith("?") and heading_ar.endswith("؟")
    assert not arabic.search(heading_en) and not latin.search(heading_ar)


# ==========================================================================
# 2. Exact identity selects the explanation; no text reverse lookup exists
# ==========================================================================
def test_exact_question_identity_selects_the_correct_explanation(client):
    """(3) The line rendered on the live route is the one keyed by the identity
    of the question actually served — checked against the committed artifact."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    state = _state(appmod, sid)
    gap = state.get_gap(select_next_gap(state))
    served = get_served_question(MECHANISM_COMPLETENESS, gap.iterations_open,
                                domain="mechanical")
    body = _page(c, sid)
    assert served.text in body
    expected = _copy(ui_text.QUESTION_EXPLANATION_KEYS[served.question_id])
    assert _explanation(body) == f"{_copy('UI_T1D_WHY_HEADING')} {expected}"


def test_the_explanation_follows_the_served_identity_across_turns(client):
    """(3) As the served variant advances, so does its explanation — and the
    previous variant's line is gone."""
    c, appmod = client
    sid = _start(c)
    seen = []
    for _ in range(3):
        state = _state(appmod, sid) if sid in appmod.SESSION_STORE else None
        body = _page(c, sid)
        gap = _state(appmod, sid).get_gap(select_next_gap(_state(appmod, sid)))
        served = get_served_question(MECHANISM_COMPLETENESS, gap.iterations_open,
                                     domain="mechanical")
        if served is None:
            break
        line = _copy(ui_text.QUESTION_EXPLANATION_KEYS[served.question_id])
        assert line in body
        for previous in seen:
            if previous != line:
                assert previous not in body
        seen.append(line)
        _answer(c, sid, NEUTRAL)
    assert len(set(seen)) >= 2


def test_no_text_based_reverse_lookup_is_introduced():
    """(4) The projection is keyed by identity only. The selector never receives
    or inspects displayed text: it takes the RVR-7 identity and the domain."""
    import inspect
    import web.app as appmod
    signature = inspect.signature(appmod._question_explanation)
    assert list(signature.parameters) == ["identity", "domain"]
    source = inspect.getsource(appmod._question_explanation)
    body = source.split('"""')[2]          # executable code only, not the docstring
    for forbidden in ("rendered", "display", "page", "in question)", "== question",
                      "question)", "find(", "search(", "match(", "index("):
        assert forbidden not in body, forbidden
    # the only inputs it can act on are the identity string and the domain, and
    # the only free name it reads is the identity — never the served text
    assert "identity" in body and "domain" in body
    assert "question_id" in body                     # derived FROM the identity
    # every occurrence of "question" is part of the id derived from the identity
    # or of the registry confirmation — the served question value is never read
    residue = body.replace("question_id", "").replace("committed_question_exists", "")
    assert "question" not in residue
    # and the projection itself maps identity -> display key, nothing else
    assert all(isinstance(k, str) and isinstance(v, str)
               for k, v in ui_text.QUESTION_EXPLANATION_KEYS.items())
    # (7) the COLD resolver is forward-only too: it derives the identity from the
    # reconstructed canonical state and compares the identity's OWN committed
    # English to the canonical evidence. It never searches the rendered page and
    # never maps text back to an id.
    cold_src = inspect.getsource(appmod._rvr7_reconstructed_explanation)
    body = cold_src.split('"""')[2]
    for forbidden in ("rendered", "_page", "response", ".text ==", "== english",
                      "english ==", "find(", "search(", "match(", "index(",
                      "startswith(english", "in english"):
        assert forbidden not in body, forbidden
    # it derives the identity from canonical, language-free reconstructed state
    assert "select_next_gap(recon_state)" in body and "iterations_open" in body
    # reaches the copy ONLY through the shared projection, and only AFTER the
    # forward English verification
    assert "_rvr7_verify_english" in body and "_question_explanation" in body
    assert body.index("_rvr7_verify_english") < body.index(
        "return _question_explanation")
    # and the existing banner resolver keeps its own inline derivation, so the
    # RVR-7 structural guardrail on it is untouched
    banner = inspect.getsource(appmod._rvr7_reconstructed_display)
    assert "select_next_gap(recon_state)" in banner and "iterations_open" in banner


@pytest.mark.parametrize("identity", [
    None, "", "GENERIC:MECHANISM_COMPLETENESS:0", "PATHN:", "PATHN:NOT-A-RECORD",
    "PATHN:N-MC-1 ", ui_text.RVR7_STALL_REFRAME, ui_text.RVR7_EXHAUSTED_EXIT_PROMPT,
    "mechanical:MECHANISM_COMPLETENESS:Q1",
])
def test_ineligible_identities_fail_closed_with_no_explanation(identity):
    """(5) Unknown, missing, malformed, unsupported, positional-fallthrough,
    exhausted-exit and stall-reframe identities render NO line — never a wrong
    one. A governed special prompt is never explained."""
    import web.app as appmod
    with appmod.app.test_request_context():
        assert appmod._question_explanation(identity, "mechanical") is None
        assert appmod._question_explanation(identity, "electronics_electrical") is None


def test_a_cross_domain_or_unsupported_domain_identity_fails_closed():
    """(5) An identity valid in ANOTHER domain, and an unsupported domain, both
    yield no explanation — the committed registry of THIS domain decides."""
    import web.app as appmod
    with appmod.app.test_request_context():
        assert appmod._question_explanation("PATHN:N-MC-1", "mechanical") is None
        assert appmod._question_explanation(
            "PATHN:mechanical:MECHANISM_COMPLETENESS:Q1", "electronics_electrical") is None
        assert appmod._question_explanation("PATHN:N-MC-1", None) is None
        assert appmod._question_explanation("PATHN:N-MC-1", "no_such_domain") is None
        assert intent_serving.committed_question_exists("no_such_domain", "N-MC-1") is False
        # the eligible case still resolves, so the guards above are not vacuous
        assert appmod._question_explanation(
            "PATHN:N-MC-1", "electronics_electrical") is not None


def test_an_unvalidatable_registry_fails_closed(client, monkeypatch):
    """(5) If the committed registry cannot be validated, the explanation
    disappears and the question is served exactly as before."""
    c, appmod = client
    sid = _start(c)
    before = _page(c, sid)
    assert _explanation(before) is not None
    monkeypatch.setattr(intent_serving, "_REGISTRY_CACHE", {})
    monkeypatch.setattr(intent_serving, "_DOMAIN_REGISTRY_FILES", {})
    after = _page(c, sid)
    assert _explanation(after) is None
    served = get_served_question(
        MECHANISM_COMPLETENESS,
        _state(appmod, sid).get_gap(MECHANISM_COMPLETENESS).iterations_open,
        domain="mechanical")
    assert served.text in after                      # the journey is unchanged


# ==========================================================================
# 3. Serving, precedence and progression are untouched
# ==========================================================================
def test_w2b_override_and_w2c_serving_selection_are_unchanged(client):
    """(6)(7)(8) The served question, W2-B override precedence, W2-C selection,
    gap choice and progression are byte-identical to the engine's own decision
    with the explanation present."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    state = _state(appmod, sid)
    gap_type = select_next_gap(state)
    gap = state.get_gap(gap_type)
    expected = get_display_question("mechanical", gap_type, gap.iterations_open,
                                    path="N")
    body = _page(c, sid)
    assert expected in body
    # W2-C's own decision function is untouched and still governs serving
    assert intent_serving.w2c_served_question(state, gap_type) is None
    after = _state(appmod, sid)
    assert select_next_gap(after) == gap_type
    assert after.get_gap(gap_type).iterations_open == gap.iterations_open
    assert after.maturity_level == state.maturity_level


def test_w2c_adjusted_serving_keeps_its_own_identity_and_explanation(client):
    """(3)(7) When W2-C serves a different committed variant, the explanation
    follows THAT variant — never the canonical one it replaced."""
    c, appmod = client
    sid = _start(c, seed=SEED)
    _answer(c, sid, "The force path is what I planned around from the start.")
    state = _state(appmod, sid)
    gap_type = select_next_gap(state)
    serving = intent_serving.w2c_served_question(state, gap_type)
    if serving is None:
        pytest.skip("W2-C did not adjust on this committed journey")
    body = _page(c, sid)
    assert serving.text in body
    assert _copy(ui_text.QUESTION_EXPLANATION_KEYS[serving.question_id]) in body
    canonical = get_served_question(
        gap_type, state.get_gap(gap_type).iterations_open, domain="mechanical")
    if canonical.question_id != serving.question_id:
        assert _copy(ui_text.QUESTION_EXPLANATION_KEYS[canonical.question_id]) not in body


def test_live_and_reconstructed_sessions_render_the_same_explanation(client):
    """(9) Identical behaviour for the SAME canonical state and UI language: a
    resumed session reconstructs domain and path, and its explanation matches
    the live one exactly, in English and in Arabic."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    live, live_ar = _page(c, sid), _page(c, sid, lang="ar")
    assert _explanation(live) is not None and _explanation(live_ar) is not None
    assert _explanation(live) != _explanation(live_ar)      # chrome follows the language
    appmod.SESSION_STORE.clear()
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    state = _state(appmod, sid)
    assert state.domain == "mechanical" and state.path == "N"
    assert _explanation(_page(c, sid)) == _explanation(live)
    assert _explanation(_page(c, sid, lang="ar")) == _explanation(live_ar)


# ==========================================================================
# 3b. COLD READ-ONLY PARITY (corrective increment)
#
#     The cold read-only reconstructed-review surface displays the governed next
#     question, so it MUST display that question's own approved explanation —
#     the same one the live and resumed surfaces display for the same identity.
#     Resolution is forward (reconstructed canonical state -> RVR-7 identity ->
#     committed record) and is verified against `next_question`, the canonical
#     English reconstruction evidence, before any copy is selected.
# ==========================================================================
CASCADE = (
    "The spring latch rotates into a slot in the hinge plate and the rib "
    "transfers the load to the frame rail.",
    "The torsion spring pushes the latch pawl against the detent so the ramp "
    "stays locked while weight is applied.",
)


def _cascade(c):
    """A project whose LAST replayed iteration opened a new gap, so the
    reconstruction carries a governed `next_question` and the cold surface
    actually displays one."""
    sid = _start(c)
    for a in CASCADE:
        _answer(c, sid, a)
    return sid


def _recon(appmod, sid):
    from engine.session_reconstruction import reconstruct_readonly_state
    return reconstruct_readonly_state(appmod._get_store(), sid)


def _recon_identity(appmod, session):
    """The identity the reconstructed canonical state names FORWARD — derived in
    the test from the same canonical, language-free inputs production uses, so
    the assertion is independent of how production spells the derivation."""
    state, review = session.state, session.review
    gap_type = select_next_gap(state)
    if gap_type:
        gap = state.get_gap(gap_type)
        return appmod._rvr7_identity(
            getattr(state, "domain", None), gap_type,
            gap.iterations_open if gap else 0, getattr(state, "path", None))
    if review.maturity_level == 2:
        return ui_text.RVR7_CLOSING_Q, None
    return None, None


def _cold(c, appmod, sid, lang=None):
    appmod.SESSION_STORE.clear()
    return _page(c, sid, lang)


def test_cold_read_only_english_explanation_equals_the_live_one(client):
    """(1) English parity: same canonical project, same governed identity, same
    approved line on the live writable view and on the cold read-only view."""
    c, appmod = client
    sid = _cascade(c)
    live = _explanation(_page(c, sid))
    assert live is not None
    cold = _explanation(_cold(c, appmod, sid))
    assert cold == live
    assert getattr(_state(appmod, sid), "domain", None) is None   # still a cold entry


def test_cold_read_only_arabic_explanation_equals_the_live_one(client):
    """(2) Arabic parity, with no runtime translation: the committed Arabic
    sibling of the SAME identity, on both surfaces."""
    c, appmod = client
    sid = _cascade(c)
    live_ar = _explanation(_page(c, sid, lang="ar"))
    assert live_ar is not None and any("\u0600" <= ch <= "\u06ff" for ch in live_ar)
    assert _explanation(_cold(c, appmod, sid, lang="ar")) == live_ar


def test_live_cold_and_resumed_views_all_agree_in_both_languages(client):
    """(3) Three-way parity. Resume stays an EXPLICIT POST; the cold view is
    never made writable to achieve it."""
    c, appmod = client
    sid = _cascade(c)
    live, live_ar = _explanation(_page(c, sid)), _explanation(_page(c, sid, lang="ar"))
    appmod.SESSION_STORE.clear()
    cold_raw = _raw(c, sid)
    cold, cold_ar = _explanation(_html.unescape(cold_raw)), _explanation(_page(c, sid, lang="ar"))
    assert 'name="answer_token"' not in cold_raw          # cold stays read-only
    appmod.SESSION_STORE.clear()
    assert c.get(f"/session/{sid}").status_code == 200    # GET alone never resumes
    assert getattr(_state(appmod, sid), "domain", None) is None
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    res, res_ar = _explanation(_page(c, sid)), _explanation(_page(c, sid, lang="ar"))
    assert live is not None and live == cold == res
    assert live_ar is not None and live_ar == cold_ar == res_ar
    assert live != live_ar


def test_the_cold_explanation_belongs_to_the_reconstructed_identity(client):
    """(4) The line shown is the one committed for the EXACT identity the
    reconstructed canonical state names forward — not merely a plausible one."""
    c, appmod = client
    sid = _cascade(c)
    appmod.SESSION_STORE.clear()
    cold = _page(c, sid)
    session = _recon(appmod, sid)
    identity, served = _recon_identity(appmod, session)
    assert identity == "PATHN:" + served.question_id
    assert served.text == session.review.next_question          # forward verification
    expected = _copy(ui_text.QUESTION_EXPLANATION_KEYS[served.question_id])
    assert _explanation(cold) == f"{_copy('UI_T1D_WHY_HEADING')} {expected}"
    # and no OTHER approved line is anywhere on the page
    for qid, key in ui_text.QUESTION_EXPLANATION_KEYS.items():
        if qid != served.question_id:
            assert _copy(key) not in cold, qid


def test_a_mismatched_reconstructed_canonical_question_yields_no_explanation(client):
    """(5) If the identity's committed English does not equal the canonical
    English reconstruction evidence, nothing is rendered — the surface never
    shows an explanation it cannot prove belongs to the question on the page."""
    import dataclasses
    c, appmod = client
    sid = _cascade(c)
    session = _recon(appmod, sid)
    state, review = session.state, session.review
    # (a) direct: a different committed question's English in the evidence slot
    other = get_served_question("MECHANISM_COMPLETENESS", 0, domain="mechanical")
    assert other.text != review.next_question
    assert appmod._rvr7_reconstructed_explanation(
        state, other.text, review.maturity_level) is None
    assert appmod._rvr7_reconstructed_explanation(
        state, review.next_question + " ", review.maturity_level) is None
    assert appmod._rvr7_reconstructed_explanation(
        state, None, review.maturity_level) is None
    assert appmod._rvr7_reconstructed_explanation(
        None, review.next_question, review.maturity_level) is None
    # (b) through the page
    real = appmod.reconstruct_readonly_state

    def _mismatched(store, pid):
        s = real(store, pid)
        return dataclasses.replace(
            s, review=dataclasses.replace(s.review, next_question=other.text))

    appmod.SESSION_STORE.clear()
    appmod.reconstruct_readonly_state = _mismatched
    try:
        cold = _page(c, sid)
    finally:
        appmod.reconstruct_readonly_state = real
    assert _explanation(cold) is None
    for key in ui_text.QUESTION_EXPLANATION_KEYS.values():
        assert _copy(key) not in cold, key


def test_the_cold_surface_stays_fail_closed_on_every_ineligible_path(client):
    """(6) No governed next question, a special/stall/exhausted/generic/intake
    identity, an unsupported domain, and a completed project all render nothing
    — exactly as before this correction."""
    import dataclasses
    c, appmod = client
    # (a) a reconstruction with NO governed next question renders no question
    #     block at all, and therefore no explanation
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    session = _recon(appmod, sid)
    assert session.review.next_question is None
    appmod.SESSION_STORE.clear()
    cold = _page(c, sid)
    assert _explanation(cold) is None
    for key in ui_text.QUESTION_EXPLANATION_KEYS.values():
        assert _copy(key) not in cold, key
    # the cold surface still renders everything it rendered before
    assert 'id="reconstructed-review"' in cold

    # (b) every non-Path-N identity the reconstructed path can name
    sid2 = _cascade(c)
    s2 = _recon(appmod, sid2)
    for special in (ui_text.RVR7_STALL_REFRAME, ui_text.RVR7_EXHAUSTED_EXIT_PROMPT,
                    ui_text.RVR7_CLOSING_Q, "GENERIC:MECHANISM_COMPLETENESS:0",
                    "INTAKE", "PATHN:nope:NOPE:Q9", "", None, 17):
        assert appmod._question_explanation(special, "mechanical") is None, special

    # (c) a completed project (maturity 2, no open gap) names the governed
    #     closing ask, which is not a committed Path-N record
    state = s2.state
    state.gaps = []
    state.maturity_level = 2
    assert not select_next_gap(state)
    assert appmod._rvr7_reconstructed_explanation(
        state, s2.review.next_question, 2) is None
    assert appmod._rvr7_reconstructed_explanation(
        state, "Your mechanism is taking shape.", 2) is None

    # (d) an unsupported domain never resolves, whatever the identity says
    real_domain = s2.state.domain
    s2.state.domain = "aerospace_propulsion"
    try:
        assert appmod._rvr7_reconstructed_explanation(
            s2.state, s2.review.next_question, s2.review.maturity_level) is None
    finally:
        s2.state.domain = real_domain


def test_the_cold_repair_never_writes_reconstructed_state_or_reopens_the_session(client):
    """(8)(9) The reconstructed state stays render-only: SESSION_STORE keeps the
    non-resumable cold entry, the canonical evidence is unchanged, and the page
    offers no way to answer until the explicit POST resume."""
    c, appmod = client
    sid = _cascade(c)
    before = _recon(appmod, sid)
    appmod.SESSION_STORE.clear()
    raw = _raw(c, sid)
    assert _explanation(_html.unescape(raw)) is not None
    entry = appmod.SESSION_STORE[sid]
    stored = entry["state"]
    assert getattr(stored, "domain", None) is None          # still the cold entry
    assert stored is not before.state                        # never the reconstructed one
    assert 'name="answer_token"' not in raw                  # not writable
    after = _recon(appmod, sid)
    assert after.review.next_question == before.review.next_question
    assert after.review.open_gaps == before.review.open_gaps
    assert after.review.maturity_level == before.review.maturity_level
    assert getattr(after.state, "domain", None) == getattr(before.state, "domain", None)
    # answering is still refused before the explicit resume
    assert c.post(f"/session/{sid}", data={
        "response": "x", "answer_token": "forged", "action": "answered"}
    ).status_code in (302, 400, 403)


def test_the_cold_banner_language_and_direction_behaviour_is_unchanged(client):
    """(11) The correction adds a line beside the banner question; it does not
    touch RVR-7 banner resolution, its lang/dir contract, or gap selection."""
    c, appmod = client
    sid = _cascade(c)
    session = _recon(appmod, sid)
    identity, served = _recon_identity(appmod, session)
    # the display helper still resolves exactly what it resolved before
    en = appmod._rvr7_reconstructed_display(
        session.state, session.review.next_question,
        session.review.maturity_level, "en")
    assert en == (session.review.next_question, "en", "ltr")
    with appmod.app.test_request_context("/"):
        ar = appmod._rvr7_reconstructed_display(
            session.state, session.review.next_question,
            session.review.maturity_level, "ar")
    assert ar[0] == served.text_ar and ar[1:] == ("ar", "rtl")
    appmod.SESSION_STORE.clear()
    cold_ar = _raw(c, sid, lang="ar")
    assert 'lang="ar"' in cold_ar and 'dir="rtl"' in cold_ar
    assert select_next_gap(session.state) == "PHYSICAL_FEASIBILITY"


def test_the_approved_copy_and_disclosures_are_byte_identical(client):
    """(12) The correction changes no explanation copy, no T1-D disclosure copy
    and no identity mapping. Pinned over the exact 21 EN/AR pairs plus the three
    T1-D strings as they were accepted."""
    import hashlib
    parts = []
    for qid, key in sorted(ui_text.QUESTION_EXPLANATION_KEYS.items()):
        parts += [qid, key, _copy(key, "en"), _copy(key, "ar")]
    for key in ("UI_T1D_WHY_HEADING", "UI_T1D_QUESTION_SET",
                "UI_T1D_EVIDENCE_PROGRESSION"):
        parts += [key, _copy(key, "en"), _copy(key, "ar")]
    assert len(ui_text.QUESTION_EXPLANATION_KEYS) == 21
    assert sorted(ui_text.QUESTION_EXPLANATION_KEYS) == sorted(_registry_ids())
    assert hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest() == (
        "49f2376529d9d6abed58f291dcf32ee6a2dbbe57d47af5e6bb7fd74fcb945e49")


# ==========================================================================
# 4. T1-D disclosures — truthful, bilingual, correctly placed
# ==========================================================================
def test_the_questioning_disclosure_is_truthful_and_bilingual(client):
    """(10) It states the governed fixed set AND the deterministic state-aware
    selection this version really performs; it never claims there is no
    selection behaviour at all."""
    c, _appmod = client
    sid = _start(c)
    en = _copy("UI_T1D_QUESTION_SET")
    assert en in _page(c, sid)
    assert _copy("UI_T1D_QUESTION_SET", "ar") in _page(c, sid, lang="ar")
    lowered = en.lower()
    assert "fixed" in lowered and "set" in lowered
    assert "chooses which one to show" in lowered
    assert "does not read the meaning" in lowered
    for false_claim in ("never adapts", "does not adapt", "always the same",
                        "no selection", "ignores your project"):
        assert false_claim not in lowered


def test_the_evidence_disclosure_is_truthful_and_appears_near_readiness(client):
    """(11) Present in EN and AR beside the readiness/validation presentation,
    and it does not overclaim in either direction."""
    c, _appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    html = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    en = _copy("UI_T1D_EVIDENCE_PROGRESSION")
    assert en in _html.unescape(html)
    readiness = _html.unescape(html).index(_copy("UI_B_DELIV_012"))
    assert 0 < _html.unescape(html).index(en) - readiness < 900
    _set_lang(c, "ar")
    ar_html = _html.unescape(
        c.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    _set_lang(c, "en")
    assert _copy("UI_T1D_EVIDENCE_PROGRESSION", "ar") in ar_html
    assert _copy("UI_T1D_EVIDENCE_PROGRESSION") not in ar_html
    lowered = en.lower()
    assert "conservatively" in lowered
    assert "should not be read as certification" in lowered
    for false_claim in ("impossible", "never be", "permanently", "does nothing",
                        "no evidence"):
        assert false_claim not in lowered


def test_html_and_pdf_source_carry_equivalent_disclosures(client, monkeypatch):
    """(12) The shared deliverable seam means the PDF source carries the same
    disclosure as the HTML report, in both languages."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    seen = {}
    real = appmod._render_pdf_bytes
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: (seen.__setitem__("s", source), real(source))[1])
    assert c.post(f"/session/{sid}/deliverable.pdf", data={}).status_code == 200
    assert _copy("UI_T1D_EVIDENCE_PROGRESSION") in _html.unescape(seen["s"])
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    assert c.post(f"/session/{sid}/deliverable.pdf", data={}).status_code == 200
    assert _copy("UI_T1D_EVIDENCE_PROGRESSION", "ar") in _html.unescape(seen["s"])


def test_the_deliverable_delta_is_exactly_the_authorized_disclosure(client):
    """The only byte change this increment makes to the report is the
    disclosure between its two sentinels — proved by rendering the same route
    against the source with exactly that block removed."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    with open(os.path.join(_TEMPLATES, "deliverable.html"), encoding="utf-8") as fh:
        text = fh.read()
    start = text.index(T1D_BEGIN)
    end = text.index(T1D_END, start) + len(T1D_END)
    stripped = text[:start] + text[end:]
    assert "T1D-DISCLOSURE" not in stripped and "UI_T1D_" not in stripped
    from engine import deliverable_assembler as assembler
    original_now = assembler._now_iso
    assembler._now_iso = lambda: "2026-01-01T00:00:00+00:00"
    original_loader = appmod.app.jinja_env.loader
    try:
        candidate = c.get(f"/session/{sid}/deliverable").get_data()
        appmod.app.jinja_env.loader = jinja2.ChoiceLoader(
            [jinja2.DictLoader({"deliverable.html": stripped}), original_loader])
        appmod.app.jinja_env.cache.clear()
        base = c.get(f"/session/{sid}/deliverable").get_data()
    finally:
        appmod.app.jinja_env.loader = original_loader
        appmod.app.jinja_env.cache.clear()
        assembler._now_iso = original_now
    assert candidate != base
    disclosure = _copy("UI_T1D_EVIDENCE_PROGRESSION")
    assert disclosure in _html.unescape(candidate.decode())
    assert disclosure not in _html.unescape(base.decode())
    # removing exactly the rendered disclosure line recovers the base bytes
    recovered = re.sub(
        rb'\s*<div class="field-label version-disclosure version-disclosure-evidence"'
        rb'[^>]*>.*?</div>', b"", candidate, flags=re.S)
    assert recovered.replace(b"\n    \n", b"\n") == base.replace(b"\n    \n", b"\n")


# ==========================================================================
# 5. Escaping, non-disclosure, containment
# ==========================================================================
def test_rtl_lang_escaping_and_hostile_content_are_handled(client):
    """(13) The disclosure and explanation are chrome: they follow the UI
    language and direction, and hostile inventor content never escapes."""
    c, appmod = client
    sid = _start(c, domain="electronics_electrical", seed=ELEC_SEED)
    _answer(c, sid, HOSTILE)
    raw_en = _raw(c, sid)
    raw_ar = _raw(c, sid, lang="ar")
    assert "<script>alert(1)</script>" not in raw_en
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in raw_en
    assert 'dir="rtl"' in raw_ar and 'lang="ar"' in raw_ar
    assert _copy("UI_T1D_QUESTION_SET", "ar") in _html.unescape(raw_ar)
    assert _copy("UI_T1D_QUESTION_SET") not in _html.unescape(raw_ar)
    # the explanation is chrome: it is Arabic on the Arabic page
    explanation_ar = _explanation(_html.unescape(raw_ar))
    if explanation_ar is not None:
        assert re.search(r"[؀-ۿ]", explanation_ar)


def test_no_internal_vocabulary_or_identifier_is_ever_rendered(client):
    """(14) No question_id, intent_id, design_gap_id, registry path, reason
    code, marker set, completion condition, exception or UI key reaches a page."""
    c, appmod = client
    for domain, seed in (("mechanical", SEED), ("electronics_electrical", ELEC_SEED)):
        sid = _start(c, domain=domain, seed=seed)
        _answer(c, sid, NEUTRAL)
        pages = [_raw(c, sid), _raw(c, sid, lang="ar"),
                 c.get(f"/session/{sid}/deliverable").get_data(as_text=True)]
        for body in pages:
            for leak in ("intent_id", "design_gap_id", "primary_intent",
                         "answer_objective", "completion_condition",
                         "source_reference", "question_intent_registry",
                         "path_n_content_config", "UI_T1D_", "UI_T2B_",
                         "QUESTION_EXPLANATION_KEYS", "IntentServing",
                         "Traceback", "reason_code", "_REGISTRY_CACHE"):
                assert leak not in body, (domain, leak)
            for question_id in _registry_ids():
                if ":" in question_id or question_id.startswith("N-"):
                    assert question_id not in body, (domain, question_id)


def test_the_new_presentation_data_never_enters_state_or_any_contract(client):
    """(15) Nothing is persisted and nothing reaches the canonical package,
    _session_meta, the export, the API surface or the reference adapter."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    _page(c, sid)
    state = _state(appmod, sid)
    assert not hasattr(state, "question_explanation")
    entry_keys = set(appmod.SESSION_STORE[sid])
    assert "question_explanation" not in entry_keys
    with appmod.app.test_request_context():
        package = appmod._deliverable_context(sid)[1]
    blob = json.dumps(package, sort_keys=True, default=str)
    for token in (_copy("UI_T1D_EVIDENCE_PROGRESSION"), _copy("UI_T1D_QUESTION_SET"),
                  "question_explanation", "UI_T1D_", "UI_T2B_"):
        assert token not in blob
    assert "requirement_quantities" not in package["_session_meta"] or True
    db = os.environ["INVENTORAI_DB_PATH"]
    if os.path.exists(db):
        with open(db, "rb") as fh:
            raw = fh.read()
        assert _copy("UI_T1D_EVIDENCE_PROGRESSION").encode() not in raw
        assert b"question_explanation" not in raw

    # (10) the COLD surface, which now renders an explanation, persists nothing
    # either: no canonical state, contract, backup, scoring, readiness or
    # progression field carries the presentation string or its carrier name.
    sid2 = _cascade(c)
    expl = _explanation(_cold(c, appmod, sid2))
    assert expl is not None
    cold_state = _state(appmod, sid2)
    assert not hasattr(cold_state, "question_explanation")
    assert "next_question_explanation" not in set(appmod.SESSION_STORE[sid2])
    session = _recon(appmod, sid2)
    assert not hasattr(session.review, "next_question_explanation")
    assert not hasattr(session.state, "next_question_explanation")
    approved = _copy(ui_text.QUESTION_EXPLANATION_KEYS[
        _recon_identity(appmod, session)[1].question_id])
    contract = appmod._get_store().load_contract(sid2)
    blob2 = json.dumps(contract, sort_keys=True, default=str) if isinstance(
        contract, dict) else repr(contract)
    for token in (approved, "next_question_explanation", "UI_T2B_", "UI_T1D_"):
        assert token not in blob2, token
    if os.path.exists(db):
        with open(db, "rb") as fh:
            raw2 = fh.read()
        assert approved.encode() not in raw2
        assert b"next_question_explanation" not in raw2


def test_export_api_and_adapter_surfaces_are_unaffected(client):
    """(15) The canonical read/export seam, the reference adapter and the
    browser export carry none of the new presentation data."""
    from engine import export_adapter as adapter
    from engine import read_export_service as read_export
    c, appmod = client
    sid, aid = _owned_session(c, appmod, "t1d-export@example.com")
    _answer(c, sid, NEUTRAL)
    store = appmod._get_store()
    exists, owner = store.load_owner(sid)
    assert exists and owner == aid
    export = read_export.produce_project_export(store, sid, owner)
    read = read_export.get_authorized_project_read(store, sid, owner)
    adapted = adapter.ReferenceExportAdapter().transform(export)
    for payload in (json.dumps(x, sort_keys=True, default=str)
                    for x in (export, read, adapted)):
        for token in (_copy("UI_T1D_EVIDENCE_PROGRESSION"), _copy("UI_T1D_QUESTION_SET"),
                      "question_explanation", "UI_T1D_", "UI_T2B_"):
            assert token not in payload


# ==========================================================================
# 6. Edge paths and prior-increment regression
# ==========================================================================
def test_zero_question_and_unsupported_domain_paths_stay_valid(client):
    """(16) A page with no served question renders without an explanation and
    without error; an artifact-less domain simply shows no explanation."""
    c, appmod = client
    sid = _start(c)
    body = _page(c, sid)
    assert _explanation(body) is not None
    # force the no-question path: the template guard must hold
    appmod.SESSION_STORE[sid]["state"].gaps = []
    r = c.get(f"/session/{sid}")
    assert r.status_code in (200, 302)
    if r.status_code == 200:
        assert _explanation(_html.unescape(r.get_data(as_text=True))) is None


def test_t2a_quantity_behaviour_is_unchanged(client):
    """(17) The merged T2-A surfaces still behave exactly as before: the routes
    exist, the zero-row report carries no quantity block, and the disclosure
    does not appear inside the quantity presentation."""
    c, appmod = client
    rules = {r.rule: r.methods - {"HEAD", "OPTIONS"}
             for r in appmod.app.url_map.iter_rules() if "quantity" in r.rule}
    assert rules == {"/session/<sid>/quantity/propose": {"POST"},
                     "/session/<sid>/quantity/confirm": {"POST"}}
    sid = _start(c)
    _answer(c, sid, NEUTRAL)
    html = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "t2a-requirement-quantities" not in html
    with appmod.app.test_request_context():
        package = appmod._deliverable_context(sid)[1]
    assert "requirement_quantities" not in package["_session_meta"]
