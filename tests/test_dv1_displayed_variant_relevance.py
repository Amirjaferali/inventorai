"""Displayed-variant relevance repair (engine-contract version DV1).

`run_iteration` moves the served gap's counter BEFORE it integrates the
answer, and the W2-C supplemental relevance read that moved counter, so an
answer to the displayed question Qn was checked against Qn+1's committed
markers (W2-C contract §E / §F.6 scope the supplement to the canonical variant
of the question that was served). Under DV1 ONLY the supplement reads the
served gap's counter as it stood when the question was served. Every earlier
version replays exactly as before; the adjusted-display rule is unchanged (the
supplement keeps the CANONICAL index-law variant, not a W2-C-adjusted one).

Every fixture is synthetic or the frozen S2 answer map; no real-user record
is used.
"""
import html as _html
import json
import re

import pytest

import engine.session_reconstruction as sr
from engine.idea_state import (CLOSED, OPEN, PARTIAL, Gap, IdeaState,
                               MECHANISM_COMPLETENESS as MC)
from engine.intent_serving import (_INTENT_MARKERS, _gap_variants,
                                   supplemental_relevance)
from engine.progression_loop import run_iteration
from engine.session_reconstruction import (
    DISPLAYED_VARIANT_RELEVANCE_VERSIONS, ENGINE_CONTRACT_VERSION_DV1,
    ENGINE_CONTRACT_VERSION_NR1, ENGINE_CONTRACT_VERSION_T2G1,
    ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_T2G3,
    ENGINE_CONTRACT_VERSION_XG1, GAP_BOUND_REPLAY_VERSIONS,
    RECONSTRUCTION_VERSION, ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS,
    SUPPORTED_ENGINE_CONTRACT_VERSIONS, reconstruct_readonly_state)
from tests.test_t2g_versioned_journey import (  # noqa: F401 — fixture reuse
    client, _login, _snapshot, _page, _raw, F4_MIXED,
    G4_MIXED, F1_AFFIRM, Q2, Q3, NOT_ADDRESSED_NOTICE)

DV1 = ENGINE_CONTRACT_VERSION_DV1
XG1 = ENGINE_CONTRACT_VERSION_XG1
PRIOR_VERSIONS = (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1,
                  ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_NR1,
                  ENGINE_CONTRACT_VERSION_T2G3, XG1)
MECH = "mechanical"
EE = "electronics_electrical"
Q1 = "PATHN:mechanical:MECHANISM_COMPLETENESS:Q1"
NOT_ADDRESSED = "not addressed"

_S2 = json.load(open("tests/fixtures/s2_run_001_answer_maps.json",
                     encoding="utf-8"))
S2_SEED = {lang: _S2["seeds"]["M-1|" + lang] for lang in ("en", "ar")}
# The W1-N3 measured case: the expert's first answer, then the force-path
# answer to Q2 that the family test does not recognise.
S2_EXPERT = {lang: _S2["answers"]["M-1|expert|" + lang][MC][:2]
             for lang in ("en", "ar")}
UNRELATED = "The weather was nice yesterday and I had tea."


# --------------------------------------------------------------------------
# helpers — the REAL render -> submit path (every hidden form field, the
# server-signed answer target included)
# --------------------------------------------------------------------------
def _form(c, sid):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    form = re.search(r'<form id="answer-form".*?</form>', raw, re.S)
    data = {"answer_token": _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', raw).group(1))}
    for name, value in re.findall(
            r'<input type="hidden" name="([^"]+)" value="([^"]*)"', form.group(0)):
        data.setdefault(name, _html.unescape(value))
    return data


def _target(form):
    import base64
    body = form["answer_target"].rpartition(".")[0]
    return json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))


def _submit(c, sid, text, form=None):
    data = dict(form or _form(c, sid), response=text, action="answered")
    return c.post(f"/session/{sid}", data=data)


def _start_project(c, appmod, version, seed=S2_SEED["en"], domain=MECH):
    """A project genuinely created under ``version`` (the creation constant
    only), with the starting focus chosen explicitly."""
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = version
    try:
        r = c.post("/start", data={"idea": seed, "domain_choice": domain,
                                   "domain_confirm": domain})
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _mc(appmod, sid):
    state = appmod.SESSION_STORE[sid]["state"]
    gap = state.get_gap(MC)
    return None if gap is None else gap.status


def _reason(appmod, sid):
    return (appmod.SESSION_STORE[sid].get("last_result") or {}).get("reason") or ""


def _engine_state(version, domain, served, status=OPEN):
    state = IdeaState(idea_id="dv1")
    state.domain, state.path = domain, "N"
    state.engine_contract_version = version
    state.maturity_level = 1
    state.gaps.append(Gap(gap_type=MC, status=status, opened_at=0,
                          iterations_open=served))
    return state


# ==========================================================================
# 1. Versioning — one seventh version, new projects only
# ==========================================================================
def test_exactly_one_seventh_version_is_added_for_new_projects():
    assert DV1 == "p4-2-level1-recon-v1-t2g2-nr1-t2g3-xg1-dv1"
    assert SUPPORTED_ENGINE_CONTRACT_VERSIONS == PRIOR_VERSIONS + (DV1,)
    assert sr.CURRENT_ENGINE_CONTRACT_VERSION == DV1
    assert DISPLAYED_VARIANT_RELEVANCE_VERSIONS == (DV1,)


def test_dv1_carries_every_xg1_rule_unchanged():
    import web.app as appmod
    from engine import need_routing as nr
    from engine.answer_stance import t2g_rule_level
    state = IdeaState(idea_id="i")
    state.domain = MECH
    for version in (XG1, DV1):
        state.engine_contract_version = version
        assert t2g_rule_level(state, MC) == 3
        assert nr.is_routing_aware(version)
        assert version in GAP_BOUND_REPLAY_VERSIONS
        assert version in ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS
        assert appmod._questioning_disclosure_key(state) == "UI_T2G3_QUESTION_SET"
    # the legacy-adoption target is unchanged (no automatic migration)
    assert appmod._EVA_ADOPTION_TARGET_VERSION == ENGINE_CONTRACT_VERSION_T2G2


# ==========================================================================
# 2. The defect and its repair through render -> submit -> evaluation
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_the_w1n3_answer_is_read_against_the_question_that_was_displayed(
        client, lang):
    c, appmod, _db = client
    _login(c, appmod)
    outcome = {}
    for version in (XG1, DV1):
        sid = _start_project(c, appmod, version, S2_SEED[lang])
        first, force_path = S2_EXPERT[lang]
        assert _submit(c, sid, first).status_code == 302
        assert _mc(appmod, sid) == PARTIAL
        form = _form(c, sid)
        # the displayed question, its signed target and the version agree
        assert _snapshot(appmod, sid)["identity"] == Q2
        assert _target(form)["q"] == Q2 and _target(form)["v"] == version
        assert _submit(c, sid, force_path, form).status_code == 302
        outcome[version] = (_mc(appmod, sid), _reason(appmod, sid))
    # XG1 read Q3's markers for the answer to Q2: not addressed (preserved)
    assert outcome[XG1][0] == PARTIAL and NOT_ADDRESSED in outcome[XG1][1]
    # DV1 reads Q2's own markers: the REASONED follow-up closes the gap
    assert outcome[DV1][0] == CLOSED
    assert "closed after REASONED follow-up" in outcome[DV1][1]


@pytest.mark.parametrize("answer", [F4_MIXED, G4_MIXED])
def test_q2_vocabulary_is_credited_where_q2_is_displayed_not_at_q1(
        client, answer):
    """The counterpart of the T2-G journeys pinned under XG1 (COUNTER_SCOPED):
    under DV1 these mixed answers are read against the displayed question."""
    c, appmod, _db = client
    _login(c, appmod)
    at_q1 = _start_project(c, appmod, DV1, seed=S2_SEED["en"])
    _submit(c, at_q1, answer)
    assert _mc(appmod, at_q1) == OPEN
    assert NOT_ADDRESSED in _reason(appmod, at_q1)
    assert NOT_ADDRESSED_NOTICE in _page(c, at_q1)
    at_q2 = _start_project(c, appmod, DV1, seed=S2_SEED["en"])
    _submit(c, at_q2, UNRELATED)
    assert _snapshot(appmod, at_q2)["identity"] == Q2
    _submit(c, at_q2, answer)
    got = _snapshot(appmod, at_q2)
    assert got["status"] == PARTIAL and got["known_mechanism"] == "REASONED"


def test_the_adjusted_display_keeps_the_canonical_evaluation_scope(client):
    """W2-C §F.6: under a W2-C-adjusted display the supplement stays with the
    canonical index-law variant. After F1 covers Q2, Q3 is displayed but the
    canonical served variant is Q2, so a Q2-vocabulary answer is relevant."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start_project(c, appmod, DV1, seed=S2_SEED["en"])
    _submit(c, sid, F1_AFFIRM)
    entry = appmod.SESSION_STORE[sid]
    qctx = appmod._resolve_question_context(entry["state"], entry["last_result"])
    assert qctx.identity == Q3 and qctx.iterations_open == 1   # adjusted display
    _submit(c, sid, F4_MIXED)
    assert _mc(appmod, sid) == CLOSED


# ==========================================================================
# 3. Engine level — which variant the supplement consults
# ==========================================================================
@pytest.mark.parametrize("domain", [MECH, EE])
def test_the_supplement_reads_the_served_variant_under_dv1_only(domain):
    variants = _gap_variants(domain, MC)
    for served in range(len(variants)):
        seen = {}
        for version in (XG1, DV1):
            state = _engine_state(version, domain, served)
            calls = []
            import engine.intent_serving as isv
            original = isv._matches_intent
            isv._matches_intent = lambda text, qid: (calls.append(qid), False)[1]
            try:
                run_iteration(state, "zzz qqq")
            finally:
                isv._matches_intent = original
            seen[version] = calls[0] if calls else None
        assert seen[DV1] == variants[served].question_id
        assert seen[XG1] == variants[min(served + 1, len(variants) - 1)].question_id


def test_no_served_index_keeps_the_existing_counter_read():
    state = _engine_state(DV1, MECH, 1)
    force_path = S2_EXPERT["en"][1]
    assert supplemental_relevance(state, MC, force_path) is True
    assert supplemental_relevance(state, MC, force_path, served_index=0) is False
    assert supplemental_relevance(state, MC, force_path, served_index=1) is True


def test_the_render_time_feedback_does_not_depend_on_the_counter():
    """MIXED-FUNCTIONAL-ANSWER-FEEDBACK-01 reads relevance at render time,
    after the counter moved. Its sentence test also accepts EVERY committed
    variant's markers, which covers whichever variant the supplement reads,
    so the feedback line is the same for any counter (consistent with the
    corrected evaluation by construction; no feedback change is needed)."""
    import web.app as appmod
    text = ("I do not know the exact bolt size yet. The load path runs from "
            "the deck into the hinge line and then into the frame rail.")
    entry = {"transcript": [{"response": text}]}
    reason = (f"{MC} recorded as an explicit unknown — this answer states the "
              f"information is not known yet and supplies no mechanism explanation")
    result = {"transition": "WARN", "reason": reason}
    for served in range(4):
        state = _engine_state(DV1, MECH, served)
        assert appmod._statement_beside_unknown(entry, state, result) is True


# ==========================================================================
# 4. Parity, historical versions and refusals
# ==========================================================================
def _sequence(c, appmod, version, lang="en"):
    sid = _start_project(c, appmod, version, S2_SEED[lang])
    for text in S2_EXPERT[lang] + [UNRELATED]:
        _submit(c, sid, text)
    return sid


def _facts(state):
    return ([(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            state.maturity_level,
            None if state.known_mechanism is None else state.known_mechanism.quality)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_live_cold_and_resumed_agree_under_dv1(client, lang):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _sequence(c, appmod, DV1, lang)
    live_state = appmod.SESSION_STORE[sid]["state"]
    live = (_facts(live_state), _snapshot(appmod, sid))
    assert live[0][0][0][:2] == (MC, CLOSED)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    assert session.state.engine_contract_version == DV1
    assert _facts(session.state) == live[0]
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live[1]
    assert _facts(appmod.SESSION_STORE[sid]["state"]) == live[0]


@pytest.mark.parametrize("version", PRIOR_VERSIONS)
def test_every_earlier_version_replays_its_own_reading(client, version):
    c, appmod, db = client
    _login(c, appmod)
    sid = _sequence(c, appmod, version)
    live = _facts(appmod.SESSION_STORE[sid]["state"])
    assert live[0][0][:2] == (MC, PARTIAL)       # the moved-counter reading
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.state.engine_contract_version == version
    assert _facts(session.state) == live


def test_stale_and_cross_project_forms_are_still_refused(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start_project(c, appmod, DV1)
    other = _start_project(c, appmod, DV1)
    stale = _form(c, sid)
    _submit(c, sid, S2_EXPERT["en"][0], stale)
    records = len(appmod._get_store().load_contract(sid).assertions)
    assert _target(stale)["q"] == Q1
    # the consumed Q1 form, now with different text: refused, nothing written
    _submit(c, sid, S2_EXPERT["en"][1], stale)
    assert len(appmod._get_store().load_contract(sid).assertions) == records
    # another project's live form: refused, nothing written to either
    foreign = _form(c, other)
    _submit(c, sid, S2_EXPERT["en"][1], foreign)
    assert len(appmod._get_store().load_contract(sid).assertions) == records
    assert appmod._get_store().load_contract(other).assertions == []


# ==========================================================================
# 5. Negative controls — multi-answer sequences from OPEN and from PARTIAL
# ==========================================================================
def _controls(domain):
    out = []
    for variant in _gap_variants(domain, MC):
        en, ar = _INTENT_MARKERS[variant.question_id]
        out += [variant.text, " ".join(en), " ".join(ar),
                "I don't know the " + en[0] + ".", "What is the " + en[0] + "?",
                "Maybe the " + en[0] + " could be something, I suppose.",
                "There is no " + en[0] + " in my idea.",
                "My cat likes the sofa; " + en[0] + ".",
                "I already explained the " + en[0] + " in my earlier answer, it "
                "is the same as before because nothing changed."]
    return out + [UNRELATED, "I don't know.", "لا أعرف"]


def _outcomes(version):
    got = {}
    for domain in (MECH, EE):
        served_range = range(len(_gap_variants(domain, MC)))
        for text in _controls(domain):
            for start in (OPEN, PARTIAL):
                for served in served_range:
                    for repeats in (1, 2):
                        state = _engine_state(version, domain, served, start)
                        for _ in range(repeats):
                            run_iteration(state, text)
                        got[(domain, text, start, served, repeats)] = \
                            state.get_gap(MC).status
    return got


def test_controls_keyed_changes_are_pinned_exactly():
    xg1, dv1 = _outcomes(XG1), _outcomes(DV1)
    for start in (OPEN, PARTIAL):
        for status in (PARTIAL, CLOSED):
            count = lambda o: sum(1 for k, v in o.items()          # noqa: E731
                                  if k[2] == start and v == status and v != start)
            assert count(dv1) <= count(xg1), (start, status)
    # unrelated text and a bare unknown never move a gap in either version
    for outcome in (xg1, dv1):
        for key, status in outcome.items():
            if key[1] in (UNRELATED, "I don't know.", "لا أعرف"):
                assert status == key[2], key
    # KEYED comparison — same domain, served index, prior state and answer
    # sequence. Every outcome DV1 advances beyond XG1 is pinned exactly here.
    # Each is the existing marker-supplement weakness (a weak answer carrying
    # a committed marker), now read against the question it belongs to: the
    # same text earned the same credit from XG1 one question EARLIER (except
    # N-MC-1, whose markers XG1 never consulted). At these keys it is still
    # new false credit, one of them a CLOSED — recorded as evidence for the
    # Owner decision, not approved as harmless.
    rank = {OPEN: 0, PARTIAL: 1, CLOSED: 2}
    gains = {k: (xg1[k], dv1[k]) for k in dv1 if rank[dv1[k]] > rank[xg1[k]]}
    en2, ar2 = _INTENT_MARKERS["mechanical:MECHANISM_COMPLETENESS:Q2"]
    m = en2[0]
    restate = ("I already explained the " + m + " in my earlier answer, it is the "
               "same as before because nothing changed.")
    weak_q2 = (" ".join(ar2), "I don't know the " + m + ".",
               "Maybe the " + m + " could be something, I suppose.",
               "There is no " + m + " in my idea.",
               "My cat likes the sofa; " + m + ".", restate)
    ar_first = " ".join(_INTENT_MARKERS["N-MC-1"][1])
    expected = {(MECH, t, OPEN, 1, r): (OPEN, PARTIAL) for t in weak_q2 for r in (1, 2)}
    expected.update({(MECH, restate, PARTIAL, 1, r): (PARTIAL, CLOSED) for r in (1, 2)})
    expected.update({(EE, ar_first, OPEN, 0, r): (OPEN, PARTIAL) for r in (1, 2)})
    assert gains == expected
    # the mechanical gains are XG1's own credit for the same text one
    # question earlier (same prior state, one answer)
    for (domain, text, start, served, repeats), (_x, d) in gains.items():
        if domain == MECH and repeats == 1:
            assert rank[xg1[(domain, text, start, served - 1, 1)]] >= rank[d]


def test_a_q2_answer_at_q1_is_not_a_dead_end(client):
    """Coverage versus credit: under DV1 a Q2-vocabulary answer at Q1 earns no
    credit, W2-C still marks Q2 covered and serves Q3, and the journey goes on:
    an ordinary explanation progresses and a second one closes the gap."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start_project(c, appmod, DV1)
    _submit(c, sid, F4_MIXED)
    got = _snapshot(appmod, sid)
    assert got["status"] == OPEN and got["identity"] == Q3
    assert got["coverage"] == ["mechanical:MECHANISM_COMPLETENESS:Q2"]
    _submit(c, sid, F1_AFFIRM)
    assert _mc(appmod, sid) == PARTIAL
    _submit(c, sid, "Each component contributes to the overall motion: the deck "
                    "panel pivots on the hinge and the spring latch locks it flat "
                    "because it hooks the frame rail.")
    assert _mc(appmod, sid) == CLOSED
