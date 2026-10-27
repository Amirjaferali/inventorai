"""MIXED-FUNCTIONAL-ANSWER-FEEDBACK-01 — truthful feedback for an answer that
states the intended behaviour AND explicitly says how it would work is not
known yet.

The T2-G explicit-unknown veto still withholds credit exactly as before (the
gap stays where it was, the raw reason is unchanged, the answer and its
unknown are recorded as before). Only the primary plain-language feedback line
changes: it no longer calls the whole answer an unknown when the answer also
states something about the question, read from the existing canonical
relevance. It never says the mechanism was explained, and it names no part.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine import answer_stance
from engine.idea_state import IdeaState, MECHANISM_COMPLETENESS as MC, OPEN, PARTIAL
from engine.progression_loop import run_iteration
from tests.csrf_client import csrf_client
from web import result_feedback, ui_text
from web.result_feedback import get_result_feedback

ELEC = "electronics_electrical"
MECH = "mechanical"
IDEA = "A device that opens a window automatically when temperature rises."

# The answer observed in the runtime proof: stated behaviour + explicit unknown.
MIXED = ("When the room gets too warm, the device should notice that the air has "
         "become hotter than I want, and then the window should open by itself so "
         "the hot air can go out. I do not know yet what part would feel the heat "
         "or what would push the window open.")
FUNCTION_ONLY = ("When the room gets too warm, the device should notice that the air "
                 "has become hotter than I want, and then the window should open by "
                 "itself so the hot air can go out.")
UNKNOWN_ONLY = ("I do not know yet how the window would be opened or what would "
                "notice that the room is getting warm.")
UNRELATED = "My favourite colour is blue and I enjoy long summer holidays by the sea."
QUESTION_PLUS_UNKNOWN = ("Could it notice the heat and then open the window? I do "
                         "not know yet what part would feel the heat or push the "
                         "window.")
ONE_SENTENCE_MIXED = ("The window should open when the room is hot but I do not "
                      "know yet what part would feel the heat or push it.")
# The T2-G-2 padding / decoy shapes: marker-bearing fragments the existing
# quality floor does not accept must never read as a description.
DECOY_LEAD = "I do not know the load path at all here. "
DECOYS = ("Force path force path force path.", "Hinge line.",
          "Hinge line yesterday.", "Force path runs.", "It needs steps.")
AR_MIXED = ("عندما تصبح الغرفة حارة جدًا، يجب أن يلاحظ الجهاز ذلك ثم تُفتح النافذة "
            "وحدها ليخرج الهواء الحار. لا أعرف بعد ما الجزء الذي سيشعر بالحرارة أو "
            "ما الذي سيدفع النافذة.")

NEW_EN = result_feedback._WARN_EXPLICIT_UNKNOWN_WITH_STATEMENT
OLD_EN = result_feedback._WARN_EXPLICIT_UNKNOWN
UNKNOWN_REASON = (f"{MC} recorded as an explicit unknown — this answer states the "
                  f"information is not known yet and supplies no mechanism explanation")


@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _text(body):
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    return " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", body)).split())


def _token(body):
    return _html.unescape(
        re.search(r'name="answer_token" value="([^"]+)"', body).group(1))


def _start(c, domain, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": IDEA, "domain_choice": domain,
                               "domain_confirm": domain})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _answer(c, sid, text):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    r = c.post(f"/session/{sid}", data={"response": text, "action": "answered",
                                       "answer_token": _token(page)})
    assert r.status_code == 302
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _engine_outcome(domain, text):
    """The same two inputs through the engine alone, with no web layer."""
    st = IdeaState(idea_id="x")
    st.domain, st.path = domain, "N"
    st.engine_contract_version = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    run_iteration(st, IDEA)
    result = run_iteration(st, text)
    return result, st


def _relevant_for(state):
    entry = {"transcript": [{"response": None}]}

    def classify(text, result):
        entry["transcript"][0]["response"] = text
        return appmod._statement_beside_unknown(entry, state, result)
    return classify


# ── The verified defect, replayed ──────────────────────────────────────────

@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_mixed_answer_gets_truthful_feedback_and_unchanged_outcome(client, domain):
    sid = _start(client, domain)
    body = _text(_answer(client, sid, MIXED))
    assert NEW_EN in body
    assert OLD_EN not in body
    # The raw engine reason is still shown as provenance, unchanged.
    assert UNKNOWN_REASON in body
    entry = appmod.SESSION_STORE[sid]
    state = entry["state"]
    assert entry["last_result"]["reason"] == UNKNOWN_REASON
    assert state.get_gap(MC).status == OPEN
    assert state.known_mechanism is None
    # The unknown is still recorded on its own track, verbatim fragment only.
    assert [u.verbatim for u in state.acknowledged_unknowns] == [
        "I do not know yet what part would feel the heat or what would push "
        "the window open."]
    # The whole answer is in the ledger exactly once, verbatim.
    answered = [r for r in state.assertions
                if getattr(r, "content", None) == MIXED]
    assert len(answered) == 1
    assert len(appmod._get_store().ledger_record_ids(sid)) == len(state.assertions)


@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_web_outcome_equals_engine_only_outcome(client, domain):
    sid = _start(client, domain)
    _answer(client, sid, MIXED)
    live = appmod.SESSION_STORE[sid]
    result, st = _engine_outcome(domain, MIXED)
    assert live["last_result"]["transition"] == result["transition"] == "WARN"
    assert live["last_result"]["reason"] == result["reason"]
    assert ([(g.gap_type, g.status, g.iterations_open) for g in live["state"].gaps]
            == [(g.gap_type, g.status, g.iterations_open) for g in st.gaps])
    assert live["state"].maturity_level == st.maturity_level


# ── The other answer shapes keep their existing feedback ─────────────────

@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_unknown_only_keeps_existing_message(client, domain):
    sid = _start(client, domain)
    body = _text(_answer(client, sid, UNKNOWN_ONLY))
    assert OLD_EN in body
    assert NEW_EN not in body
    assert appmod.SESSION_STORE[sid]["state"].get_gap(MC).status == OPEN


@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_function_only_unchanged(client, domain):
    sid = _start(client, domain)
    body = _text(_answer(client, sid, FUNCTION_ONLY))
    assert result_feedback._WARN_PARTIALLY_ADDRESSED in body
    assert NEW_EN not in body and OLD_EN not in body
    assert appmod.SESSION_STORE[sid]["state"].get_gap(MC).status == PARTIAL


@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_unrelated_unchanged(client, domain):
    sid = _start(client, domain)
    body = _text(_answer(client, sid, UNRELATED))
    assert result_feedback._WARN_NOT_ADDRESSED in body
    assert NEW_EN not in body and OLD_EN not in body
    assert appmod.SESSION_STORE[sid]["state"].get_gap(MC).status == OPEN


@pytest.mark.parametrize("domain", [ELEC, MECH])
@pytest.mark.parametrize("text, expected", [
    (MIXED, True),
    (AR_MIXED, True),
    (UNKNOWN_ONLY, False),
    # A stated sentence must state: a question beside the unknown is not one.
    (QUESTION_PLUS_UNKNOWN, False),
    # Sentence grain only: one sentence mixing both reads as the unknown.
    (ONE_SENTENCE_MIXED, False),
])
def test_statement_reading_on_real_engine_results(domain, text, expected):
    result, st = _engine_outcome(domain, text)
    assert result["reason"] == UNKNOWN_REASON
    assert _relevant_for(st)(text, result) is expected


def test_reading_ignores_every_other_result():
    st = IdeaState(idea_id="x")
    st.domain, st.path = ELEC, "N"
    entry = {"transcript": [{"response": MIXED}]}
    for result in (None, {}, {"transition": "PASS", "reason": UNKNOWN_REASON},
                   {"transition": "WARN", "reason": f"{MC} not addressed — x"},
                   {"transition": "WARN", "reason": "BOGUS recorded as an explicit unknown"}):
        assert appmod._statement_beside_unknown(entry, st, result) is False
    assert appmod._statement_beside_unknown(
        {"transcript": []}, st, {"transition": "WARN", "reason": UNKNOWN_REASON}) is False


@pytest.mark.parametrize("domain, decoy",
                         [(MECH, decoy) for decoy in DECOYS]
                         + [(ELEC, "It needs steps.")])
def test_padding_and_decoys_never_read_as_a_description(domain, decoy):
    # Each pinned shape is one the veto really applies to in that domain.
    text = DECOY_LEAD + decoy
    result, st = _engine_outcome(domain, text)
    assert result["reason"] == UNKNOWN_REASON
    assert _relevant_for(st)(text, result) is False


def test_states_beyond_unknown_uses_only_the_callers_predicate():
    yes = lambda s: True  # noqa: E731
    no = lambda s: False  # noqa: E731
    assert answer_stance.states_beyond_unknown("A. B.", yes) is True
    assert answer_stance.states_beyond_unknown("A. B.", no) is False
    assert answer_stance.states_beyond_unknown("A? B?", yes) is False
    assert answer_stance.states_beyond_unknown("Suppose A. B?", yes) is False
    assert answer_stance.states_beyond_unknown(
        "I do not know A. I don't know the B.", yes) is False
    assert answer_stance.states_beyond_unknown("", yes) is False


# ── Feedback owner mapping ────────────────────────────────────────────────

def test_flag_selects_only_between_the_two_unknown_messages():
    unknown = {"transition": "WARN", "reason": UNKNOWN_REASON}
    assert get_result_feedback(unknown) == OLD_EN
    assert get_result_feedback(unknown, statement_beside_unknown=True) == NEW_EN
    assert get_result_feedback(unknown, statement_beside_unknown="yes") == OLD_EN
    for other in ({"transition": "WARN", "reason": f"{MC} partially addressed — needs more depth"},
                  {"transition": "WARN", "reason": f"{MC} not addressed — x"},
                  {"transition": "PASS", "reason": "Problem established — ready for LEVEL 1"},
                  None):
        assert (get_result_feedback(other, statement_beside_unknown=True)
                == get_result_feedback(other))


def test_new_message_claims_no_explanation_validation_or_part():
    lowered = NEW_EN.lower()
    assert "did not recognize" in lowered
    assert "not known yet" in lowered
    for forbidden in ("sensor", "motor", "thermostat", "actuator", "controller",
                      "spring", "validated", "verified", "explained how",
                      "works correctly", "feasible", "safe"):
        assert forbidden not in lowered


# ── EN / AR parity ────────────────────────────────────────────────────────

def test_arabic_translation_exists():
    ar = ui_text.localize_deep(NEW_EN, "ar")
    assert ar != NEW_EN
    assert "غير معروف بعد" in ar
    assert ui_text.localize_deep(NEW_EN, "en") == NEW_EN


@pytest.mark.parametrize("text", [MIXED, AR_MIXED])
def test_arabic_page_shows_arabic_message(client, text):
    sid = _start(client, ELEC, lang="ar")
    body = _text(_answer(client, sid, text))
    assert ui_text.localize_deep(NEW_EN, "ar") in body
    assert ui_text.localize_deep(OLD_EN, "ar") not in body
    assert appmod.SESSION_STORE[sid]["state"].get_gap(MC).status == OPEN
