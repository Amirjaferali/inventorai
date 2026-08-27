"""D-P6-18 final UI-chrome boundary — the reclassified question/criticality/
clarification-flow CHROME follows ui_lang, while the actual asks stay English.

Owner classifier (G-DP6-18 bounded review): "Is the user expected to answer THIS
text as the actual question/prompt?" YES -> canonical ask (English). NO ->
application UI chrome / guidance / control / status (follows UI language).

The core guard here is EXHAUSTIVE: every English string the deterministic guidance
modules and the criticality/ack constants can render is asserted to be mapped to
Arabic, so no ordinary chrome can silently leak English under Arabic UI ("close
the boundary once"). Representative render tests confirm real pages switch.
"""
import re

import pytest

import web.ui_text as ui_text
import web.clarification_labels as cl
import web.scaffolding_guidance as sg
import web.answer_coauthoring_prompts as ac
import web.result_feedback as rf
import web.responsibility_labels as rl
import web.gap_labels as gl
import web.app as app_mod
from web.app import app, SESSION_STORE
from tests.test_structured_criticality import (
    IDEA_WS1,
    _start as _crit_start,
    _drive_ws1_journey_to_completion,
    _focus_token,
)

_ARABIC = re.compile(r"[؀-ۿ]")

IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _set_lang(client, lang):
    assert client.post("/ui-language", data={"lang": lang}).status_code in (302, 303)


def _start(client):
    r = client.post("/start", data={"idea": IDEA,
                                    "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/session/", 1)[-1]


# --------------------------------------------------------------------------
# EXHAUSTIVE coverage: every module/constant chrome string is mapped to Arabic.
# --------------------------------------------------------------------------
def _all_module_chrome_strings():
    """Collect EVERY English UI-chrome string the reclassified flows can render.
    Actual asks (the canonical questions and the criticality clarification) and
    echoed user content are deliberately excluded."""
    s = set()
    # clarification_labels — explanatory guidance about the question (not the ask)
    for entry in list(cl._CLARIFICATION.values()) + [cl._FALLBACK]:
        for k in ("label", "plain_language", "information_needed",
                  "answer_shape", "support_hint"):
            s.add(entry[k])
    # scaffolding_guidance — "what kind of detail to add" guidance/prompts
    for tup in (sg._MECHANISM_PROMPTS, sg._BOUNDARY_PROMPTS, sg._FEASIBILITY_PROMPTS):
        s.update(tup)
    s.update(sg._ASSERTED_BY_FAMILY.values())
    s.update(sg._PARTIAL_BY_FAMILY.values())
    s.update([sg._ASSERTED_GENERIC, sg._PARTIAL_GENERIC, sg._LEAD_INTAKE,
              sg._LEAD_GENERIC, sg._HEADING, sg._NOTE])
    # answer_coauthoring_prompts — optional "what you could include" guidance
    for tup in list(ac._PROMPTS.values()) + [ac._FALLBACK]:
        s.update(tup)
    s.update([ac._HEADING, ac._NOTE])
    # result_feedback — plain-language status/feedback
    s.update([rf._WARN_ASSERTED_ONLY, rf._WARN_PARTIALLY_ADDRESSED,
              rf._PASS_DEMONSTRATED_EVIDENCE, rf._PASS_REASONED_FOLLOW_UP,
              rf._NOT_ESTABLISHED, rf._MVP_CAP, rf._SEQUENCING,
              rf._REASONED_MINIMUM, rf._GENERIC_WARN])
    # responsibility_labels — advisory who-answers guidance
    for v in rl._GUIDANCE.values():
        s.add(v["label"]); s.add(v["guidance"])
    # gap_labels GAP_LABELS heading/guidance/stage_note — framing/guidance chrome
    for v in gl.GAP_LABELS.values():
        s.add(v["heading"]); s.add(v["guidance"]); s.add(v["stage_note"])
    # non-answer acknowledgements — status messages
    s.update(app_mod._NON_ANSWER_ACK.values())
    # criticality chrome — summary lead + choice/action LABELS (not the ask)
    s.add(app_mod.CRITICALITY_SUMMARY_LEAD)
    s.update(lbl for _, lbl in app_mod.CRITICALITY_CHOICES)
    s.update(lbl for _, lbl in app_mod.CRITICALITY_SUMMARY_ACTIONS)
    return s


def test_every_reclassified_chrome_string_is_mapped_to_arabic():
    """CLOSE-THE-BOUNDARY guard: no ordinary chrome may leak English under Arabic."""
    missing = sorted(x for x in _all_module_chrome_strings()
                     if x not in ui_text._DEEP_AR)
    assert missing == [], (
        "UNMAPPED UI chrome would render English under Arabic UI "
        "(reclassify + map these): %r" % missing)


def test_actual_asks_are_never_mapped():
    """The canonical clarification ASK must stay English (never localized)."""
    assert app_mod.CRITICALITY_CLARIFICATION not in ui_text._DEEP_AR


def test_mapped_values_are_arabic_script():
    """Every mapped value is real Arabic, not an accidental English copy."""
    for en, ar in ui_text._DEEP_AR.items():
        assert _ARABIC.search(ar), "non-Arabic value for %r: %r" % (en, ar)


def test_english_selection_is_parity_preserving():
    """Under English UI, localize_deep returns values untouched (no drift)."""
    sample = {"a": app_mod.CRITICALITY_SUMMARY_LEAD, "b": ["x", ("y",)]}
    assert ui_text.localize_deep(sample, "en") == sample


# --------------------------------------------------------------------------
# Representative live-render switching (real routes, real templates).
# --------------------------------------------------------------------------
def test_question_flow_guidance_follows_ui_language(client):
    """On a normal question page the clarification/responsibility/co-authoring/
    gap-guidance CHROME switches to Arabic.

    The CHROME rule this test owns is unchanged by RVR-7 and is asserted exactly
    as before. Only the trailing question-element expectation is realigned: under
    the Owner's `D-P6-18 DISPLAY-RULE SUPERSESSION: BOUNDED` (PR #588) the
    substantive question follows the UI language too, so the element declares
    Arabic/RTL when Arabic is what is rendered (M-13) instead of a hardcoded
    `lang="en"`."""
    sid = _start(client)
    en = client.get("/session/" + sid).get_data(as_text=True)
    assert "What this question is asking" in en           # clarification label EN
    _set_lang(client, "ar")
    ar = client.get("/session/" + sid).get_data(as_text=True)
    assert "ما الذي يسأل عنه هذا السؤال" in ar             # clarification label AR
    assert "What this question is asking" not in ar
    # RVR-7 / M-13: the question element declares the language of the text it
    # actually renders — Arabic/RTL here, never a hardcoded English declaration
    # wrapped around Arabic script.
    match = re.search(r'<p class="question"([^>]*)>(.*?)</p>', ar, re.S)
    assert match, "question element not rendered"
    attrs, text = match.group(1), match.group(2)
    assert 'lang="ar"' in attrs and 'dir="rtl"' in attrs
    assert re.search("[؀-ۿ]", text), "Arabic session served no Arabic question"


def test_criticality_summary_and_choice_chrome_follow_ui_language():
    """Summary-confirm controls, the summary lead, and category-choice labels are
    Arabic under Arabic UI; the criticality clarification ASK stays English."""
    client, sid = _crit_start(IDEA_WS1)
    try:
        _drive_ws1_journey_to_completion(client, sid)
        # summary stage under Arabic
        client.post("/ui-language", data={"lang": "ar"})
        page = client.get("/session/" + sid).get_data(as_text=True)
        assert "نعم، هذا صحيح" in page          # "Yes, that is correct" (AR)
        assert "Yes, that is correct" not in page
        assert "هذا ما فهمته من شرحك:" in page   # summary lead (AR)
        token = _focus_token(page)
        # advance to the clarify stage: the ASK stays English; choices are Arabic
        client.post("/session/" + sid, data={
            "criticality_action": "summary_correct", "focus_token": token})
        clarify = client.get("/session/" + sid).get_data(as_text=True)
        assert app_mod.CRITICALITY_CLARIFICATION in clarify   # ASK stays English
        assert "قد لا تعمل الفكرة بدون هذا" in clarify         # choice label (AR)
    finally:
        SESSION_STORE.pop(sid, None)
