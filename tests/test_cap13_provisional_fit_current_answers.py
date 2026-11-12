"""CAP13-PROVISIONAL-FIT-CURRENT-ANSWERS-01 — the CAP-13 provisional dimensional
fit also reads the inventor's CURRENT answers (the PR #956 source rule).

Synthetic data only. What is pinned:
  * the unchanged grammar reads the original idea and each CURRENT answered
    inventor record ON ITS OWN; quantities are never combined across statements;
  * one candidate, or several written identically (dimension pair in either
    order, lift and unit tokens verbatim), give ONE offer: from the original
    idea when it holds one, otherwise from the most recent current answer,
    labelled by source; anything else is a conflict and no candidate is chosen;
  * the real answer and correction paths change the offer on the next read;
    an unreadable history or a missing original idea offers nothing;
  * nothing is stored, prefilled or progressed; replay, domain and the CAP-13
    calculation gate are unchanged.
"""
import random
import re
import time

import pytest

import web.app as webapp
from engine import cap13_functional_configuration as fit
from engine.session_reconstruction import reconstruct_readonly_state
from tests.test_cap12_form_mockup_advisory import SESSION_STORE, _client_for, _page
from tests.test_functional_need_handoff import _start
from tests.test_t2g_versioned_journey import _answer, _correct

SEED = "A wooden stand that lifts my monitor so the screen sits at eye level."
ANSWER = "I want to raise the monitor 15 cm above my desk; dimensions 60 x 20 cm"
ANSWER_SWAPPED = "I want to raise the monitor 15 cm above my desk; dimensions 20 x 60 cm"
ANSWER_OTHER = "I want to raise the monitor 12 cm above my desk; dimensions 60 x 20 cm"
IDEA_WITH_FIT = "I want to raise my monitor 15 cm above my desk; dimensions 60 x 20 cm"
FIT_PAGE = "/session/%s/functional-configuration"
NOTE_EN = ("Your recorded statements do not state the object dimensions or the lift "
           "in the same way, so no provisional dimensional requirement is shown.")
NOTE_AR = "عباراتك المسجلة لا تذكر أبعاد الجسم أو ارتفاع الرفع بالطريقة نفسها"


# ==========================================================================
# 1. the combinator — pure
# ==========================================================================
def test_p01_the_original_idea_alone_behaves_exactly_as_before():
    before = fit.derive_provisional_fit(IDEA_WITH_FIT)
    now = fit.derive_current_fit(IDEA_WITH_FIT, [])
    assert now == before and now.source_type == fit.SOURCE_IDEA == "ORIGINAL_IDEA_STATEMENT"
    assert fit.derive_current_fit(SEED, []) is None
    assert fit.derive_provisional_fit(SEED) is None


def test_p02_a_current_answer_is_a_source_labelled_as_such():
    result = fit.derive_current_fit(SEED, ["The stand is wooden.", ANSWER])
    assert isinstance(result, fit.ProvisionalFit)
    assert result.source_type == fit.SOURCE_ANSWER == "CURRENT_ANSWER"
    assert result.source_excerpt == ANSWER                      # verbatim, never the seed
    assert (result.top_length, result.top_depth, result.size_unit) == ("60", "20", "cm")
    assert (result.surface_lift, result.lift_unit) == ("15", "cm")
    assert result.engineering_status == "NOT_ASSESSED"


def test_p03_identical_candidates_give_one_offer_from_the_preferred_source():
    # the original idea wins when it holds one, whatever the answers say
    assert fit.derive_current_fit(IDEA_WITH_FIT, [ANSWER_SWAPPED]).source_type == fit.SOURCE_IDEA
    # otherwise the MOST RECENT current answer, with its own written order
    result = fit.derive_current_fit(SEED, [ANSWER, ANSWER_SWAPPED])
    assert result.source_excerpt == ANSWER_SWAPPED
    assert (result.top_length, result.top_depth) == ("20", "60")


@pytest.mark.parametrize("idea,texts", [
    (IDEA_WITH_FIT, [ANSWER_OTHER]),                                       # different lift
    (SEED, [ANSWER, ANSWER.replace("60 x 20", "70 x 20")]),               # different size
    (SEED, [ANSWER, ANSWER.replace("60 x 20", "60.0 x 20")]),             # verbatim, never coerced
    (SEED, [ANSWER, ANSWER.replace("60 x 20 cm", "600 x 200 mm")]),       # never converted
    (SEED, [ANSWER, "أريد رفع الشاشة 15 سم فوق مكتبي وأبعاده 60 × 20 سم"]),  # unit token as written
])
def test_p04_any_difference_is_a_conflict_and_nothing_is_chosen(idea, texts):
    assert fit.derive_current_fit(idea, texts) is fit.CONFLICT


@pytest.mark.parametrize("texts", [
    ["I want to raise the monitor 15 cm above my desk.", "Its dimensions 60 x 20 cm."],
    ["dimensions 60 x 20 cm", "raise it 15 cm on my desk"],
])
def test_p05_quantities_are_never_combined_across_statements(texts):
    assert fit.derive_current_fit(SEED, texts) is None


@pytest.mark.parametrize("text", [
    "I don't want to raise the monitor 15 cm above my desk; dimensions 60 x 20 cm",
    "Raise a person 15 cm above my desk; dimensions 60 x 20 cm",
    "Maybe raise it 15 cm then raise it 12 cm on my desk; dimensions 60 x 20 cm",
    "I want to raise the monitor 15 cm; dimensions 60 x 20 cm",            # no desk / table
    ANSWER + " " + "x" * 2000,                                             # over the bound
])
def test_p06_the_unchanged_grammar_refuses_answers_outside_its_scope(text):
    assert fit.derive_current_fit(SEED, [text]) is None


@pytest.mark.parametrize("texts", [None, ANSWER, [ANSWER, None], [42], (ANSWER, b"x")])
def test_p07_unreadable_answer_texts_raise_and_are_never_read_as_empty(texts):
    with pytest.raises(ValueError):
        fit.derive_current_fit(SEED, texts)



@pytest.mark.parametrize("text", [
    "I want to raise the monitor between 10 and 15 cm above my desk; dimensions 60 x 20 cm",
    "I want to raise the monitor either 10 cm or 15 cm above my desk; dimensions 60 x 20 cm",
    "I want to raise the monitor 10-15 cm above my desk; dimensions 60 x 20 cm",
    "I want to raise the monitor 10 cm; or 15 cm above my desk; dimensions 60 x 20 cm",
    "I want to raise the monitor up to 15 cm above my desk; dimensions 60 x 20 cm",
    "I want to raise the monitor at least 15 cm above my desk; dimensions 60 x 20 cm",
    "أريد رفع الشاشة بين ١٠ و١٥ سم فوق مكتبي؛ أبعاد: ٦٠ × ٢٠ سم",
    "أريد رفع الشاشة إما ١٠ سم أو ١٥ سم فوق مكتبي؛ أبعاد: ٦٠ × ٢٠ سم",
    "أريد رفع الشاشة حتى ١٥ سم فوق مكتبي؛ أبعاد: ٦٠ × ٢٠ سم",
])
def test_p08_ranges_and_alternatives_never_choose_one_lift(text):
    assert fit.derive_provisional_fit(text) is None
    assert fit.derive_current_fit(SEED, [text]) is None
    assert fit.derive_current_fit(SEED, [ANSWER, text]) is None
    assert fit.derive_current_fit(IDEA_WITH_FIT, [text]) is None


def test_p09_one_decimal_lift_remains_a_sourced_exact_offer():
    exact = "I want to raise the monitor 15.5 cm above my desk; dimensions 60 x 20 cm"
    result = fit.derive_current_fit(SEED, [exact])
    assert result.surface_lift == "15.5"
    assert result.source_excerpt == exact
    assert result.source_type == fit.SOURCE_ANSWER
    assert fit.derive_current_fit(SEED, [ANSWER]).surface_lift == "15"


def test_w08_a_current_answer_corrected_to_alternatives_withholds_the_offer():
    c, sid = _mech("cap13cur-w08@example.com")
    assert _answer(c, sid, ANSWER).status_code in (200, 302)
    record = [r for r in _ledger(sid) if r.content == ANSWER][-1]
    changed = "I want to raise the monitor either 10 cm or 15 cm above my desk; dimensions 60 x 20 cm"
    assert _correct(c, sid, record.record_id, changed).status_code in (200, 302)
    assert any(r.content == changed for r in _ledger(sid))
    assert "data-engineering-fit-link" not in _page(c, sid)
    assert c.get(FIT_PAGE % sid).status_code != 200
    corrected = [r for r in _ledger(sid) if r.content == changed][-1]
    assert _correct(c, sid, corrected.record_id, ANSWER_OTHER).status_code in (200, 302)
    page = c.get(FIT_PAGE % sid)
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert ANSWER_OTHER in html and 'data-fit-source="answer"' in html
    assert "12 cm" in html




@pytest.mark.parametrize("text", [
    "Either raise the monitor 15 cm above my desk; dimensions 60 x 20 cm",
    "Up to 15 cm, raise the monitor 15 cm above my desk; dimensions 60 x 20 cm",
    "Between 10 cm and 15 cm, raise the monitor 15 cm above my desk; dimensions 60 x 20 cm",
    "إما أرفع الشاشة ١٥ سم فوق مكتبي؛ أبعاد: ٦٠ × ٢٠ سم",
    "حتى ١٥ سم، أرفع الشاشة ١٥ سم فوق مكتبي؛ أبعاد: ٦٠ × ٢٠ سم",
    "أرفع الشاشة ١٥ سم فوق مكتبي، أو ١٠ سم؛ أبعاد: ٦٠ × ٢٠ سم",
])
def test_p10_preverb_limits_and_arabic_comma_alternatives_do_not_select_lift(text):
    assert fit.derive_provisional_fit(text) is None
    assert fit.derive_current_fit(SEED, [text]) is None
    assert fit.derive_current_fit(SEED, [ANSWER, text]) is None


@pytest.mark.parametrize("text", [
    "10 cm or raise the monitor 15 cm above my desk; dimensions 60 x 20 cm",
    "10 to 15 cm, raise the monitor 15 cm above my desk; dimensions 60 x 20 cm",
    "١٠ سم أو أرفع الشاشة ١٥ سم فوق مكتبي؛ أبعاد: ٦٠ × ٢٠ سم",
    "١٠ إلى ١٥ سم، أرفع الشاشة ١٥ سم فوق مكتبي؛ أبعاد: ٦٠ × ٢٠ سم",
])
def test_p12_preverb_numeric_alternatives_never_select_height(text):
    assert fit.derive_provisional_fit(text) is None
    assert fit.derive_current_fit(SEED, [text]) is None
    assert fit.derive_current_fit(SEED, [ANSWER, text]) is None


def test_p11_an_arabic_comma_with_an_extra_number_fails_closed():
    # A comma is not proof of an independent clause: no silent height choice.
    text = "أرفع الشاشة ١٥ سم فوق مكتبي، وربما ١٠ سم؛ أبعاد: ٦٠ × ٢٠ سم"
    assert fit.derive_current_fit(SEED, [text]) is None

# ==========================================================================
# 2. the real product path
# ==========================================================================
def _mech(email, idea=SEED):
    c, _aid = _client_for(email)
    return c, _start(c, idea, "mechanical")


def _ledger(sid):
    return webapp._get_store().load_contract(sid).assertions


def test_w01_before_and_after_an_answer_sourced_fit_becomes_available():
    c, sid = _mech("cap13cur-w01@example.com")
    body = _page(c, sid)
    assert "data-engineering-fit-link" not in body                    # before: nothing to read
    assert "data-engineering-fit-conflict" not in body
    assert c.get(FIT_PAGE % sid).status_code != 200
    assert _answer(c, sid, ANSWER).status_code in (200, 302)
    body = _page(c, sid)
    assert "data-engineering-fit-link" in body                        # after: the answer is read
    assert "Optional: dimensional requirements from your idea or a recorded answer" in body
    page = c.get(FIT_PAGE % sid)
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert 'data-fit-source="answer"' in html and "Your current recorded answer" in html
    assert ANSWER in html and "60 × 20 cm" in html and "15 cm" in html
    assert "Your original statement" not in html
    assert "Not engineering-assessed" in html


def test_w02_a_correction_changes_or_removes_the_offer_on_the_next_read():
    c, sid = _mech("cap13cur-w02@example.com")
    _answer(c, sid, ANSWER)
    record = [r for r in _ledger(sid) if r.content == ANSWER][-1]
    assert _correct(c, sid, record.record_id, ANSWER_OTHER).status_code in (200, 302)
    html = c.get(FIT_PAGE % sid).get_data(as_text=True)
    assert "12 cm" in html and ANSWER_OTHER in html and ANSWER not in html
    record = [r for r in _ledger(sid) if r.content == ANSWER_OTHER][-1]
    assert _correct(c, sid, record.record_id,
                    "The stand should be made of oak.").status_code in (200, 302)
    assert "data-engineering-fit-link" not in _page(c, sid)
    assert c.get(FIT_PAGE % sid).status_code != 200


def test_w03_a_conflict_shows_a_neutral_note_and_offers_nothing(monkeypatch):
    c, sid = _mech("cap13cur-w03@example.com", IDEA_WITH_FIT)
    assert "data-engineering-fit-link" in _page(c, sid)
    _answer(c, sid, ANSWER_OTHER)
    body = _page(c, sid)
    assert "data-engineering-fit-link" not in body
    assert "data-engineering-fit-conflict" in body
    assert NOTE_EN in body
    assert "original idea" not in body.split("data-engineering-fit-conflict", 1)[1].split("</p>", 1)[0]
    assert c.get(FIT_PAGE % sid).status_code != 200


def test_w04_the_conflict_note_is_arabic_in_the_arabic_interface():
    c, sid = _mech("cap13cur-w04@example.com", IDEA_WITH_FIT)
    _answer(c, sid, ANSWER_OTHER)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    body = _page(c, sid)
    assert "data-engineering-fit-conflict" in body
    assert NOTE_AR in body
    assert "فكرتك الأصلية" not in body.split("data-engineering-fit-conflict", 1)[1].split("</p>", 1)[0]


def test_w04b_two_conflicting_answers_get_the_same_neutral_note():
    c, sid = _mech("cap13cur-w04b@example.com")                       # no candidate in the idea
    _answer(c, sid, ANSWER)
    _answer(c, sid, ANSWER_OTHER)
    body = _page(c, sid)
    assert "data-engineering-fit-link" not in body
    assert NOTE_EN in body
    assert c.get(FIT_PAGE % sid).status_code != 200


def test_w05_an_unreadable_history_or_original_idea_offers_nothing(monkeypatch):
    c, sid = _mech("cap13cur-w05@example.com")
    _answer(c, sid, ANSWER)
    assert "data-engineering-fit-link" in _page(c, sid)
    store = webapp._get_store()

    def broken(_sid):
        raise RuntimeError("unreadable ledger")
    with monkeypatch.context() as m:
        m.setattr(store, "load_contract", broken)
        assert webapp._current_engineering_fit(sid) is None
    with monkeypatch.context() as m:
        real = store.load_contract
        m.setattr(store, "load_contract", lambda s: type("C", (), {
            "assertions": [object()]})())                     # a record that cannot be read
        assert webapp._current_engineering_fit(sid) is None
        assert real(sid) is not None
    with monkeypatch.context() as m:
        real_inputs = store.load_reconstruction_inputs
        m.setattr(store, "load_reconstruction_inputs",
                  lambda s: dict(real_inputs(s), seed_idea_text=None))
        body = _page(c, sid)
        assert "data-engineering-fit-link" not in body
        assert "data-engineering-fit-conflict" not in body
        assert c.get(FIT_PAGE % sid).status_code != 200


def test_w06_an_ineligible_project_gets_no_offer_from_the_same_answer():
    c, _aid = _client_for("cap13cur-w06@example.com")
    sid = _start(c, SEED, "electronics_electrical")
    _answer(c, sid, ANSWER)
    body = _page(c, sid)
    assert "data-engineering-fit-link" not in body and "data-engineering-fit-conflict" not in body
    assert c.get(FIT_PAGE % sid).status_code != 200


def test_w07_reading_the_offer_changes_no_state_replay_or_domain():
    c, sid = _mech("cap13cur-w07@example.com")
    _answer(c, sid, ANSWER)
    store = webapp._get_store()
    ids = [r.record_id for r in _ledger(sid)]
    inputs = store.load_reconstruction_inputs(sid)
    state = SESSION_STORE[sid]["state"]
    gaps = [(g.gap_type, g.status) for g in state.gaps]
    known = state.known_mechanism
    replayed = reconstruct_readonly_state(store, sid).state
    assert replayed is not None
    for _ in range(2):
        assert "data-engineering-fit-link" in _page(c, sid)
        assert c.get(FIT_PAGE % sid).status_code == 200
    assert [r.record_id for r in _ledger(sid)] == ids
    assert store.load_reconstruction_inputs(sid) == inputs
    assert inputs["confirmed_domain"] == "mechanical"
    assert [(g.gap_type, g.status) for g in SESSION_STORE[sid]["state"].gaps] == gaps
    assert SESSION_STORE[sid]["state"].known_mechanism == known
    again = reconstruct_readonly_state(store, sid).state
    assert [(g.gap_type, g.status) for g in again.gaps] == \
        [(g.gap_type, g.status) for g in replayed.gaps]
    assert again.known_mechanism == replayed.known_mechanism
    # the CAP-13 calculation page is unchanged: nothing is prefilled from the answer
    calc = c.get("/session/%s/support-reactions" % sid).get_data(as_text=True)
    assert 'value="60"' not in calc and 'value="15"' not in calc and 'value="20"' not in calc


# ==========================================================================
# 3. bounded scan work (Codex security review on c248795)
# ==========================================================================
_OLD_NUMBER = r"[0-9]+(?:\.[0-9]+)?"
_OLD_DIMENSION = re.compile(
    rf"(?P<a>{_OLD_NUMBER})\s*[×xX*]\s*(?P<b>{_OLD_NUMBER})\s*(?P<unit>{fit._UNITS})(?![\w/])")
_OLD_RISE = re.compile(
    rf"(?P<verb>\braise\b|\blift\b|\belevate\b|رفع|أرفع|ارفع|يرفع)"
    rf"[^\n.؛!?؟]{{0,80}}?(?P<n>{_OLD_NUMBER})\s*(?P<unit>{fit._UNITS})(?![\w/])",
    re.IGNORECASE)


def _matches(pattern, text):
    return [(m.span(), m.groupdict()) for m in pattern.finditer(text)]


def test_b01_the_digit_run_guard_changes_no_match():
    """Differential proof: on a seeded random corpus over the grammar's own
    alphabet (digits, decimal points, operators, units, verbs, breaks), the
    guarded patterns find exactly the matches, spans and groups the earlier
    patterns found."""
    rng = random.Random(968)
    pieces = ["1", "2", "15", "60", "20", "0", ".", "..", " ", "x", "X", "×", "*", "cm",
              "mm", "سم", "ملم", "raise ", "lift ", "رفع ", "desk ", ";", "\n", "a", "/", "1.5"]
    texts = ["".join(rng.choice(pieces) for _ in range(rng.randint(1, 40)))
             for _ in range(6000)]
    texts += ["raise 1.2.3x4 cm", "12.x3 cm", "dimensions 60 x 20.5.cm",
              "raise it " + "9" * 90 + " cm", "x" * 3 + "123x45 cm"]
    for text in texts:
        assert _matches(fit._DIMENSION, text) == _matches(_OLD_DIMENSION, text), text
        assert _matches(fit._RISE, text) == _matches(_OLD_RISE, text), text


def test_b02_many_long_digit_answers_are_read_in_linear_time():
    hostile = ["desk " + "1" * 1990, "raise " * 5 + "desk " + "1" * 1960]
    answers = [hostile[i % 2] for i in range(400)]
    start = time.perf_counter()
    assert fit.derive_current_fit(SEED, answers) is None
    # about 0.15 s here after the guard (about 30 s before it); a generous bound
    assert time.perf_counter() - start < 5.0
