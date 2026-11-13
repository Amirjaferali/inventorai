# -*- coding: utf-8 -*-
"""R2-UNRECOGNISED-ANSWER-DISPLAY-01: display of the R2 "not addressed" result.

When the relevance check cannot recognise how an answer responds to the
question, the page says the point stays open and that the app could not
determine how the inventor's words answer the question, in English and Arabic,
in the primary line and in "Result details". It no longer tells the inventor
to reuse the question's words, it does not repeat the save confirmation the
page already shows, and the raw technical reason stays unchanged in
``last_result``. Display only: evaluation, progression and question texts are
untouched.

Two real answers through the real start and answer path:
* the ``ar_msa-02`` solar-panel brush answer, which states its own trigger and
  response but is not recognised (the known R2 paraphrase under-coverage);
* a genuinely unrelated answer.
The message must be truthful for both.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine.idea_state import MECHANISM_COMPLETENESS as MC, OPEN
from scripts import g1_faithful_rephrasing_eval as ev
from tests.test_g1_pcc_literal_source_aid import client  # noqa: F401  (fixture)
from web import result_feedback, ui_text
from web.result_feedback import get_result_detail, get_result_feedback

ELEC = "electronics_electrical"
BRUSH = ("بحسب فكرتي، تبدأ الفرشاة التنظيف كل أسبوع، ثم تمشي على الألواح وتمسحها. "
         "لم أقرر بعد ما الذي يحرّكها ولا ما إذا كانت تستخدم الماء")
UNRELATED = {"en": "My favourite colour is blue and I enjoy long summer holidays by the sea.",
             "ar": "لوني المفضل هو الأزرق وأحب قضاء العطلات الصيفية الطويلة على البحر."}
RAW = "MECHANISM_COMPLETENESS not addressed — this answer does not respond to the question that was asked"
PRIMARY = {"en": result_feedback._WARN_NOT_ADDRESSED,
           "ar": "بقيت هذه النقطة مفتوحة. لم يتمكن التطبيق من تحديد كيف تجيب كلماتك عن السؤال المطروح."}
DETAIL = {"en": result_feedback._DETAIL_NOT_ADDRESSED,
          "ar": "لم يتمكن التطبيق من تحديد صلة كلمات إجابتك بالسؤال المطروح، لذلك بقيت هذه النقطة مفتوحة."}
OLD = {"en": "in the words the question uses", "ar": "بالكلمات التي يستخدمها السؤال"}
SAVED = {"en": "Your answer was saved to this project.", "ar": "تم حفظ إجابتك في هذا المشروع."}


def _idea():
    cases, _ = ev.load_pack()
    return next(c["idea_text"] for c in cases if c["case_id"] == "ar_msa-02")


def _text(body):
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    return " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", body)).split())


def _answer(c, lang, text):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": _idea(), "domain_choice": ELEC, "domain_confirm": ELEC})
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    page = c.get("/session/" + sid).get_data(as_text=True)
    question = re.search(r'name="answer_target" value="([^"]+)"', page).group(1)
    token = _html.unescape(re.search(r'name="answer_token" value="([^"]+)"', page).group(1))
    r = c.post("/session/" + sid, data={"response": text, "action": "answered",
                                         "answer_token": token, "answer_target": question})
    assert r.status_code == 302
    return sid, question, c.get(r.headers["Location"]).get_data(as_text=True)


def _details(body):
    m = re.search(r'<details class="result-details".*?</details>', body, re.S)
    assert m
    return m.group(0)


# ── Pure display helpers ───────────────────────────────────────────────────
def test_the_message_and_detail_in_both_languages():
    result = {"transition": "WARN", "reason": RAW}
    assert get_result_feedback(result) == PRIMARY["en"]
    assert get_result_detail(result) == DETAIL["en"]
    for lang in ("en", "ar"):
        assert ui_text.localize_deep(get_result_feedback(result), lang) == PRIMARY[lang]
        assert ui_text.localize_deep(get_result_detail(result), lang) == DETAIL[lang]
    for text in PRIMARY.values():
        assert OLD["en"] not in text and OLD["ar"] not in text
    for lang in ("en", "ar"):
        for text in (PRIMARY[lang], DETAIL[lang]):            # no repeated save confirmation
            assert "saved" not in text.lower() and "حُفظت" not in text and "حفظ" not in text


def test_no_claim_about_the_answer_itself():
    for text in (PRIMARY["en"], DETAIL["en"]):
        lowered = text.lower()
        for claim in ("irrelevant", "off-topic", "wrong", "incorrect", "does not respond",
                      "did not answer", "understand", "meaning", "translate", "any language"):
            assert claim not in lowered


@pytest.mark.parametrize("reason", [
    "MECHANISM_COMPLETENESS recorded as an explicit unknown — x",
    "MECHANISM_COMPLETENESS recorded as a question or supposition — x",
    "MECHANISM_COMPLETENESS recorded as an undecided choice — x",
    "MECHANISM_COMPLETENESS recorded as a repeat — x",
    "MECHANISM_COMPLETENESS partially addressed — needs more depth",
    "LEVEL 2 is max for MVP",
])
def test_every_other_reason_keeps_its_raw_detail(reason):
    assert get_result_detail({"transition": "WARN", "reason": reason}) is None
    assert get_result_detail({"transition": "PASS", "reason": RAW}) is None
    assert get_result_detail(None) is None


# ── Rendered pages: the brush answer and an unrelated answer ───────────────
@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("kind", ["brush", "unrelated"])
def test_the_rendered_result(client, lang, kind):
    answer = BRUSH if kind == "brush" else UNRELATED[lang]
    sid, question, body = _answer(client, lang, answer)
    entry = appmod.SESSION_STORE[sid]
    state = entry["state"]
    # unchanged evaluation: not recognised, gap still open, raw reason kept
    assert entry["last_result"]["transition"] == "WARN"
    assert entry["last_result"]["reason"] == RAW
    assert state.get_gap(MC).status == OPEN
    assert state.get_assertions()[-1].content == answer
    text = _text(body)
    assert text.count(SAVED[lang]) == 1                      # saved once, by the page
    assert PRIMARY[lang] in text
    assert OLD[lang] not in text
    details = _details(body)
    assert 'class="reason-detail"' in details and DETAIL[lang] in _text(details)
    assert RAW not in _text(details) and 'class="reason-raw"' not in details
    assert state.get_assertions()[-1].question_target == "PATHN:N-MC-1"   # the same question
