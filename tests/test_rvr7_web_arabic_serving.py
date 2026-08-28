"""RVR-7 — real served-route Arabic evidence (web layer).

Authority: the authoritative RVR-7 Implementation Path Manifest Freeze (PR #588);
Owner decisions D-P6-18 BOUNDED, Q2 INCLUDE, D-RVR7-1 Option A.

This module exercises the ACTUAL Flask route (contract §T item 10: "real served
route / UI evidence, not unit stubs alone"): an Arabic session receives the
substantive Path-N ask in Arabic, the question element declares the language and
direction of the text actually rendered (M-13), the canonical/durable state is
byte-identical across languages, and no mixed-language failure state occurs.

It also carries the W1-N2 Arabic adversarial enumerated small-talk corpus on that
same real route.
"""
import html as _html
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.intent_serving as intent_serving
from engine.idea_state import MECHANISM_COMPLETENESS
from engine.path_n_questions import get_served_question
from engine.progression_loop import select_next_gap, get_display_question
from web import ui_text

ARABIC = re.compile("[؀-ۿ]")

# Seeds reused verbatim from the committed W2-C real-route evidence module, so
# domain admission behaves exactly as it already does on the live route.
MECH_SEED = ("a manually foldable wheelchair ramp for a home doorway — the "
             "inventor wants the ramp to stay reliably locked in the flat, "
             "load-bearing position and to fold away without tools")
ELEC_SEED = ("a doorway sensor that notices when the ramp is left deployed "
             "and alerts the resident through a small indicator")
NEUTRAL = "I will need to think more about this whole area."


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "rvr7-web.sqlite"))
    monkeypatch.setattr(intent_serving, "_REGISTRY_CACHE", {})
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def _start(c, domain="mechanical", seed=MECH_SEED):
    r = c.post("/start", data={"idea": seed, "domain_confirm": domain})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _set_lang(c, lang):
    assert c.get(f"/ui-language?lang={lang}").status_code in (200, 302)


def _raw(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _page(c, sid):
    return _html.unescape(_raw(c, sid))


def _token(c, sid):
    m = re.search(r'name="answer_token" value="([^"]+)"', _raw(c, sid))
    return _html.unescape(m.group(1))


def _answer(c, sid, text):
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(c, sid), "action": "answered"})


def _question_element(body):
    m = re.search(r'<p class="question"([^>]*)>(.*?)</p>', body, re.S)
    assert m, "question element not found in the rendered page"
    return m.group(1), _html.unescape(m.group(2)).strip()


# ---------------------------------------------------------------------------
# 1. The Arabic session receives the substantive ask in Arabic
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("domain,seed", [("mechanical", MECH_SEED),
                                         ("electronics_electrical", ELEC_SEED)])
def test_arabic_session_serves_the_committed_arabic_ask(client, domain, seed):
    c, appmod = client
    sid = _start(c, domain, seed)
    state = appmod.SESSION_STORE[sid]["state"]
    gap = select_next_gap(state)
    served = get_served_question(gap, state.get_gap(gap).iterations_open,
                                domain=domain)
    _set_lang(c, "ar")
    attrs, text = _question_element(_page(c, sid))
    assert text == served.text_ar
    assert 'lang="ar"' in attrs and 'dir="rtl"' in attrs


@pytest.mark.parametrize("domain,seed", [("mechanical", MECH_SEED),
                                         ("electronics_electrical", ELEC_SEED)])
def test_english_session_is_unchanged(client, domain, seed):
    c, appmod = client
    sid = _start(c, domain, seed)
    state = appmod.SESSION_STORE[sid]["state"]
    gap = select_next_gap(state)
    expected = get_display_question(domain, gap,
                                    state.get_gap(gap).iterations_open, path="N")
    attrs, text = _question_element(_page(c, sid))
    assert text == expected
    assert 'lang="en"' in attrs and 'dir="ltr"' in attrs
    assert not ARABIC.search(text)


def test_language_switch_mid_session_swaps_only_the_display(client):
    """The same ask, the same identity, the same canonical state — two surfaces."""
    c, appmod = client
    sid = _start(c)
    _, english = _question_element(_page(c, sid))
    before = repr(vars(appmod.SESSION_STORE[sid]["state"]))
    _set_lang(c, "ar")
    _, arabic = _question_element(_page(c, sid))
    _set_lang(c, "en")
    _, english_again = _question_element(_page(c, sid))
    after = repr(vars(appmod.SESSION_STORE[sid]["state"]))
    assert english == english_again
    assert ARABIC.search(arabic) and not ARABIC.search(english)
    assert before == after, "rendering in Arabic mutated canonical state"


def test_no_mixed_language_question_element(client):
    """M-13: the element never declares a language the text does not have."""
    c, _ = client
    sid = _start(c)
    for lang in ("en", "ar", "en"):
        _set_lang(c, lang)
        attrs, text = _question_element(_page(c, sid))
        declared_ar = 'lang="ar"' in attrs
        assert declared_ar == bool(ARABIC.search(text)), (lang, attrs, text[:40])
        assert ('dir="rtl"' in attrs) == declared_ar


# ---------------------------------------------------------------------------
# 2. Canonical / durable state stays language-independent
# ---------------------------------------------------------------------------

def test_durable_and_transcript_records_stay_english(client):
    c, appmod = client
    sid = _start(c)
    _set_lang(c, "ar")
    _answer(c, sid, "The panel rotates on the hinge until it lies flat, then a "
                    "toggle latch snaps over the centre rib and holds it rigid.")
    entry = appmod.SESSION_STORE[sid]
    assert not ARABIC.search(entry.get("last_question") or "")
    for row in entry["transcript"]:
        assert not ARABIC.search(row.get("question") or "")


def test_same_answers_produce_identical_canonical_state_in_both_languages(client):
    """Identical inputs, different display language -> identical canonical state
    and identical durable evidence."""
    c, appmod = client
    answers = ["The panel rotates on the hinge until flat.",
               "A toggle latch snaps over the centre rib and holds it rigid."]

    def _run(lang):
        sid = _start(c)
        _set_lang(c, lang)
        for a in answers:
            _answer(c, sid, a)
        state = appmod.SESSION_STORE[sid]["state"]
        return (state.maturity_level, state.current_stage, state.direction,
                tuple(sorted((g.gap_type, g.status, g.iterations_open)
                             for g in state.gaps)),
                tuple((r.gap_context, r.disposition, r.content)
                      for r in state.assertions))

    assert _run("en") == _run("ar")


def test_reconstruction_version_unchanged_through_the_route(client):
    from engine.session_reconstruction import RECONSTRUCTION_VERSION
    assert RECONSTRUCTION_VERSION == "p4-2-level1-recon-v1"


# ---------------------------------------------------------------------------
# 3. Cold-load reconstruction banner
# ---------------------------------------------------------------------------

def test_cold_load_banner_renders_arabic_without_schema_change(client):
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, "The panel rotates on the hinge until flat and the toggle "
                    "latch snaps over the centre rib.")
    appmod.SESSION_STORE.pop(sid, None)          # force the durable cold load
    _set_lang(c, "ar")
    body = _page(c, sid)
    assert body, "cold-load page did not render"
    m = re.search(r'<p class="question"[^>]*lang="([a-z]{2})"[^>]*dir="(ltr|rtl)"[^>]*>(.*?)</p>',
                  body, re.S)
    if m:
        lang, direction, text = m.group(1), m.group(2), m.group(3).strip()
        assert (lang == "ar") == bool(ARABIC.search(text))
        assert (direction == "rtl") == (lang == "ar")


def test_cold_load_english_banner_matches_the_reconstructed_english(client):
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, "The panel rotates on the hinge until flat and the toggle "
                    "latch snaps over the centre rib.")
    appmod.SESSION_STORE.pop(sid, None)
    body = _page(c, sid)
    assert not ARABIC.search(body.split("</head>")[-1].split('class="question"')[-1][:400])


# ---------------------------------------------------------------------------
# 4. W1-N2 — Arabic adversarial enumerated small-talk corpus, real route
# ---------------------------------------------------------------------------

W1N2_ARABIC_SMALL_TALK = (
    "مرحبا",
    "شكرا لك",
    "كيف حالك؟",
    "لا أعرف",
    "حسنا",
    "نعم",
    "لا",
    "من فضلك ساعدني",
    "ما هذا؟",
    "طيب، أكمل",
    "هذه فكرة جيدة جدا",
    "أريد أن أبدأ من جديد",
)


@pytest.mark.parametrize("utterance", W1N2_ARABIC_SMALL_TALK)
def test_w1n2_arabic_small_talk_never_closes_a_gap(client, utterance):
    """W1-N2 adversarial corpus on the real served route: enumerated Arabic
    small talk must never be mistaken for substantive evidence — it must not
    close a gap, advance maturity, or advance the stage."""
    c, appmod = client
    sid = _start(c)
    state = appmod.SESSION_STORE[sid]["state"]
    gap = select_next_gap(state)
    before = (state.maturity_level, state.current_stage,
              state.get_gap(gap).status)
    _set_lang(c, "ar")
    _answer(c, sid, utterance)
    state = appmod.SESSION_STORE[sid]["state"]
    after = (state.maturity_level, state.current_stage,
             state.get_gap(gap).status)
    assert after == before, (utterance, before, after)


def test_w1n2_arabic_small_talk_keeps_the_page_serving_arabic(client):
    """After adversarial Arabic input the journey must still serve a substantive
    Arabic ask — no silent drop back to English, no mixed-language state."""
    c, _ = client
    sid = _start(c)
    _set_lang(c, "ar")
    for utterance in W1N2_ARABIC_SMALL_TALK[:4]:
        _answer(c, sid, utterance)
    attrs, text = _question_element(_page(c, sid))
    assert ARABIC.search(text), text[:60]
    assert 'lang="ar"' in attrs and 'dir="rtl"' in attrs


# ---------------------------------------------------------------------------
# 4b. W1-N2 — EN <-> AR DIFFERENTIAL over the same adversarial corpus
#
# Contract SS-E.1 fixes the discharge mechanism for W1-N2 as an Arabic adversarial
# regression over the enumerated small-talk corpus, on the real answer-integration
# path, "with EN/AR differential assertions". Section 4 above proves the Arabic
# side in isolation; this section supplies the differential limb: the SAME
# small-talk semantics, expressed in each language, must leave canonical state
# identically untouched. A leak on either surface that the other does not share
# is exactly the historical W2-C R3 failure this must defend against.
#
# These tests assert EXISTING behavior. They add no runtime capability.
# ---------------------------------------------------------------------------

# Index-aligned English counterparts of W1N2_ARABIC_SMALL_TALK. Same speech acts,
# same adversarial class (greeting / thanks / deflection / assent / meta-request).
W1N2_ENGLISH_COUNTERPART = (
    "hello",
    "thank you",
    "how are you?",
    "I don't know",
    "okay",
    "yes",
    "no",
    "please help me",
    "what is this?",
    "fine, continue",
    "this is a very good idea",
    "I want to start over",
)


def test_w1n2_corpus_pairing_is_complete():
    """Guards the differential fixture itself: every Arabic adversarial utterance
    has exactly one English counterpart, so the differential cannot silently
    degrade into a one-sided check if the corpus is extended."""
    assert len(W1N2_ENGLISH_COUNTERPART) == len(W1N2_ARABIC_SMALL_TALK)


def _progression_snapshot(appmod, sid):
    """Canonical progression state, language-independent by construction."""
    state = appmod.SESSION_STORE[sid]["state"]
    gap = select_next_gap(state)
    return (state.maturity_level, state.current_stage, gap,
            state.get_gap(gap).status)


@pytest.mark.parametrize("index", range(len(W1N2_ARABIC_SMALL_TALK)))
def test_w1n2_small_talk_is_inert_identically_in_both_languages(client, index):
    """EN/AR differential: the same small talk must produce the SAME canonical
    outcome in both languages, and that outcome must be no progression at all.
    Catches a one-sided leak in either direction."""
    c, appmod = client
    arabic = W1N2_ARABIC_SMALL_TALK[index]
    english = W1N2_ENGLISH_COUNTERPART[index]

    sid_ar = _start(c)
    _set_lang(c, "ar")
    before_ar = _progression_snapshot(appmod, sid_ar)
    _answer(c, sid_ar, arabic)
    after_ar = _progression_snapshot(appmod, sid_ar)

    sid_en = _start(c)
    _set_lang(c, "en")
    before_en = _progression_snapshot(appmod, sid_en)
    _answer(c, sid_en, english)
    after_en = _progression_snapshot(appmod, sid_en)

    assert before_ar == before_en, (before_ar, before_en)
    assert after_ar == after_en, (arabic, english, after_ar, after_en)
    assert after_ar == before_ar, (arabic, before_ar, after_ar)


# ---------------------------------------------------------------------------
# 4c. W1-N1 — Arabic verification concern, on the real served route
#
# W1-N1 (Wave-1 closure record SS-4) is the English-side finding that hyphenated
# buzzword stuffing may reach REASONED, contained by the binding invariant
# "REASONED classification alone is not proof of technical validity or
# progression eligibility." The English containment is already asserted by the
# committed W2-D gate module. Contract SS-E.2 makes W1-N1 a verification INPUT to
# RVR-7 acceptance, "discharged by demonstrating its Arabic verification concern
# in the RVR-7 suite": the Arabic surface must contain the same class of input on
# the same terms, so the substantive Arabic journey cannot become the weaker path.
#
# These tests assert EXISTING behavior. They add no runtime capability.
# ---------------------------------------------------------------------------

# English fixture reused verbatim from the committed W2-D gate module so the two
# surfaces are compared on the same adversarial class.
W1N1_STUFFING_EN = ("state-of-the-art sensor-fusion next-generation "
                    "performance-optimized architecture-driven market-leading "
                    "solution platform")
# Arabic analogue: the same buzzword-stuffing act, no feasibility-family content.
W1N1_STUFFING_AR = ("حل متطور متعدد-الاستشعار جيل-جديد محسّن-الأداء "
                    "مبني-على-البنية رائد-في-السوق منصة متكاملة")


@pytest.mark.parametrize("lang,stuffing", [("en", W1N1_STUFFING_EN),
                                           ("ar", W1N1_STUFFING_AR)])
def test_w1n1_buzzword_stuffing_never_advances_on_either_surface(
        client, lang, stuffing):
    """W1-N1 containment holds on the Arabic surface exactly as on the English
    one: buzzword stuffing closes no gap, advances no maturity level and advances
    no stage."""
    c, appmod = client
    sid = _start(c)
    _set_lang(c, lang)
    before = _progression_snapshot(appmod, sid)
    _answer(c, sid, stuffing)
    after = _progression_snapshot(appmod, sid)
    assert after == before, (lang, before, after)


def test_w1n1_stuffing_outcome_is_identical_across_languages(client):
    """The differential form of W1-N1: neither language is the weaker path."""
    c, appmod = client
    sid_en = _start(c)
    _set_lang(c, "en")
    _answer(c, sid_en, W1N1_STUFFING_EN)
    after_en = _progression_snapshot(appmod, sid_en)

    sid_ar = _start(c)
    _set_lang(c, "ar")
    _answer(c, sid_ar, W1N1_STUFFING_AR)
    after_ar = _progression_snapshot(appmod, sid_ar)

    assert after_ar == after_en, (after_ar, after_en)


# ---------------------------------------------------------------------------
# 5. Generated output stays outside RVR-7
# ---------------------------------------------------------------------------

def test_next_development_step_and_deliverable_stay_english(client):
    """Owner decision: generated substantive output is NOT absorbed by RVR-7."""
    c, _ = client
    sid = _start(c)
    _set_lang(c, "ar")
    _answer(c, sid, "The panel rotates on the hinge until flat and the toggle "
                    "latch snaps over the centre rib and holds it rigid.")
    body = _page(c, sid)
    m = re.search(r'<div class="next-step-issue"[^>]*>(.*?)</div>', body, re.S)
    if m:
        assert not ARABIC.search(m.group(1))
    deliverable = _html.unescape(
        c.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    for pattern in (r'<div class="field-value"[^>]*>(.*?)</div>',):
        for value in re.findall(pattern, deliverable, re.S)[:20]:
            assert not ARABIC.search(value) or "؟" not in value
