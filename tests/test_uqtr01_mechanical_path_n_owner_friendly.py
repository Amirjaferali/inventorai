"""UQTR-01 STEP 1 — Mechanical Path-N owner-friendly question rewrite.

Authority: Owner authorization "UQTR-01 STEP 1 — MECHANICAL PATH N OWNER-FRIENDLY
QUESTION REWRITE — CANDIDATE 01"; DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_CONTRACT.md
§8 (additive amendment).

What changes: HOW the owner is asked — the default Mechanical Path-N wording
(EN + AR) of the SAME ten committed question identities. What does not: the
question ids, their gap ownership and order, the specialist Mechanical pack,
the intent registry, the Electronics artifacts, the seam's behavior, and every
engine rule that decides gap status, maturity, accepted risk or readiness.
Owner-friendly questioning is not fake technical completion.

Fixtures are neutral synthetic ideas written for this file. The frozen T1-C′
study corpus is deliberately NOT used.
"""
import hashlib
import html as _html
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.path_n_questions as pnq
import engine.progression_loop as pl
from engine import intent_serving
from engine.idea_state import MECHANISM_COMPLETENESS, CLOSED
from tests.csrf_client import csrf_client
import web.app as appmod

_REPO = os.path.join(os.path.dirname(__file__), "..")
_CONFIG = os.path.join(_REPO, "docs", "governance", "path_n_content_config")
_MECH_ARTIFACT = os.path.join(_CONFIG, "mechanical_path_n_questions.json")
_MECH_REGISTRY = os.path.join(_CONFIG, "mechanical_question_intent_registry.json")
_EE_ARTIFACT = os.path.join(_CONFIG, "electronics_electrical_path_n_questions.json")
_EE_REGISTRY = os.path.join(_CONFIG, "electronics_electrical_question_intent_registry.json")
_MECH_PACK = os.path.join(_REPO, "domains", "mechanical", "domain.json")

# Byte identity of the files this slice must NOT change (values at the
# authorized base 8d8ef633).
_UNCHANGED_SHA256 = {
    _MECH_PACK: "901dd7188ddefda9cbe69a835cc64959c1d55debfe61b262d720abd904069e79",
    _MECH_REGISTRY: "b2db0b898a03c103aa86b1811a78121ec37ad21d8f44b03b3171e480f1d91f24",
    _EE_ARTIFACT: "7b3e06c0492c91486b429ce14479c43a1c8ff3ebe268137c148b07cc7cb8590c",
    _EE_REGISTRY: "5b0d35667635c2470a59fee272b129e27a172c0640e94473efd442ad9b131884",
}

# The Owner-approved owner-friendly copy (EN, AR), in committed order.
APPROVED_COPY = {
    "MECHANISM_COMPLETENESS": [
        ("mechanical:MECHANISM_COMPLETENESS:Q1",
         "In your own words, what happens from the moment someone uses your idea until it produces the result you want? Describe the main physical steps you expect, even if you do not know their technical names.",
         "بكلماتك، ماذا يحدث من لحظة استخدام الفكرة إلى أن تحقق النتيجة التي تريدها؟ صف الخطوات المادية الأساسية التي تتوقع حدوثها، حتى لو كنت لا تعرف أسماءها التقنية."),
        ("mechanical:MECHANISM_COMPLETENESS:Q2",
         "Which parts do you expect to move or connect, and what does each one do to the next part? If you are unsure how force is transferred, describe the movement or effect you expect.",
         "ما الأجزاء التي تتوقع أن تتحرك أو تتصل ببعضها، وما الذي يفعله كل جزء بالجزء الذي يليه؟ وإذا لم تكن تعرف كيف تنتقل القوة بينها، فصف الحركة أو التأثير الذي تتوقعه."),
        ("mechanical:MECHANISM_COMPLETENESS:Q3",
         "What main parts do you think your idea needs, and what job should each part do? You do not need to know the technical name of a part.",
         "ما الأجزاء الرئيسية التي تعتقد أن فكرتك تحتاج إليها، وما المهمة التي تتوقع من كل جزء أن يؤديها؟ لا يلزم أن تعرف الاسم التقني للجزء."),
        ("mechanical:MECHANISM_COMPLETENESS:Q4",
         "If someone tried to build a simple prototype tomorrow, what part of how it works would still need more explanation or engineering work? State what you know and do not guess what you do not know.",
         "لو حاول شخص بناء نموذج أولي مبسط غدًا، فما الجزء من طريقة العمل الذي سيظل بحاجة إلى شرح أو عمل هندسي إضافي؟ اذكر ما تعرفه فقط، ولا تخمّن ما لا تعرفه."),
    ],
    "PHYSICAL_FEASIBILITY": [
        ("mechanical:PHYSICAL_FEASIBILITY:Q1",
         "What do you expect makes the movement or physical action happen in your idea? For example: pushing, pulling, turning, sliding, gravity, spring action, or friction. If you do not know the engineering principle, describe what you expect to happen physically.",
         "ما الذي تتوقع أنه يجعل الحركة أو الفعل المادي يحدث في فكرتك؟ مثل الدفع أو السحب أو الدوران أو الانزلاق أو الجاذبية أو عمل النابض أو الاحتكاك. وإذا لم تعرف المبدأ الهندسي، فصف ما تتوقع أن يحدث ماديًا."),
        ("mechanical:PHYSICAL_FEASIBILITY:Q2",
         "What limits or conditions could affect whether the idea works physically? For example: weight, load, force, material, distance, or movement. State what you know; you can record what you do not know instead of guessing.",
         "ما الحدود أو الظروف التي قد تؤثر في عمل الفكرة ماديًا؟ مثل الوزن أو الحمل أو القوة أو المادة أو المسافة أو الحركة. اذكر ما تعرفه، ويمكنك تسجيل ما لا تعرفه بدل التخمين."),
    ],
    "BOUNDARY_AMBIGUITY": [
        ("mechanical:BOUNDARY_AMBIGUITY:Q1",
         "What should your idea do, and what is it deliberately not intended to do or cover?",
         "ما الذي يجب أن تفعله فكرتك، وما الذي لا يُقصد منها أن تفعله أو تغطيه؟"),
        ("mechanical:BOUNDARY_AMBIGUITY:Q2",
         "Where should the limits of your idea be? Give one clear limit — for example, a weight, size, movement, or use situation it is not meant to handle.",
         "أين يجب أن تكون حدود فكرتك؟ اذكر حدًا واضحًا واحدًا، مثل وزن أو حجم أو حركة أو حالة استخدام لا يُفترض أن تتعامل معها."),
        ("mechanical:BOUNDARY_AMBIGUITY:Q3",
         "Do you know of an existing product or mechanism that works in a similar way? If yes, name one example. If not, do not guess.",
         "هل تعرف منتجًا أو آلية موجودة تعمل بطريقة مشابهة؟ إذا نعم، اذكر مثالًا واحدًا. وإذا لم تعرف، فلا تخمّن."),
        ("mechanical:BOUNDARY_AMBIGUITY:Q4",
         "Compared with that example, what physical behaviour, arrangement, or way of use do you expect to be different in your idea? State only what you know.",
         "مقارنةً بذلك المثال، ما الاختلاف المادي أو في ترتيب الأجزاء أو طريقة الاستخدام الذي تتوقعه في فكرتك؟ اذكر فقط ما تعرفه."),
    ],
}

# Specialist-heavy wording that must no longer be the DEFAULT Path-N surface
# (it stays in the specialist pack).
_OLD_DEFAULT_EN = (
    "What physical principle does your mechanism rely on?",
    "gear ratio",
    "State at least one clear mechanical boundary.",
)
_OLD_DEFAULT_AR = ("نسبة التروس", "على أي مبدأ فيزيائي تعتمد آليتك",
                   "اذكر حدا ميكانيكيا واضحا واحدا على الأقل")

# Neutral synthetic mechanical seed (written for this file).
SEED = ("a folding wall-mounted drying rack with a hinge, a spring latch and "
        "a lever that locks the arms open under load")
NOTE = "I do not know how this part works yet."
PLAIN_ANSWER = ("You pull the rack down from the wall, it swings open on its "
                "side hinges, and then you push the sliding pin across so it "
                "stays open while the clothes hang on it.")


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _artifact():
    with open(_MECH_ARTIFACT, encoding="utf-8") as fh:
        return json.load(fh)


def _served_all(domain="mechanical"):
    out = []
    for gap, entries in APPROVED_COPY.items():
        for i in range(len(entries) + 1):          # +1 exercises clamping
            out.append(pnq.get_served_question(gap, i, domain=domain))
    return out


# ---------------------------------------------------------------------------
# A. Identity preservation
# ---------------------------------------------------------------------------

def test_ten_ids_same_gaps_same_order_as_the_pack():
    with open(_MECH_PACK, encoding="utf-8") as fh:
        pack = json.load(fh)
    pack_ids = {g["gap_type_id"]: [q["question_id"] for q in g["questions"]]
                for g in pack["gap_type_mappings"]}
    art_ids = {gap: [e["question_id"] for e in entries]
               for gap, entries in _artifact()["gaps"].items()}
    assert art_ids == pack_ids
    assert list(art_ids) == list(APPROVED_COPY)
    assert art_ids == {g: [q for q, _, _ in es] for g, es in APPROVED_COPY.items()}
    assert sum(len(v) for v in art_ids.values()) == 10


def test_en_and_ar_are_one_record_identity():
    for gap, entries in APPROVED_COPY.items():
        for qid, en, ar in entries:
            served = pnq.get_served_question_by_id(gap, qid, domain="mechanical")
            assert served.question_id == qid and served.design_gap_id == gap
            assert (served.text, served.text_ar) == (en, ar)


def test_artifact_shape_and_metadata_state_the_new_truth():
    data = _artifact()
    assert set(data) == {"metadata", "gaps"}
    md = data["metadata"]
    assert set(md) == {"domain", "source", "provenance_ref", "contract",
                       "generated_by_gate"}
    assert md["domain"] == "mechanical"
    assert "owner-friendly" in md["source"] and "NOT a verbatim" in md["source"]
    # Safe Question Reduction Slice 1: the ONE disclosed extension is the
    # bounded routing descriptor on PHYSICAL_FEASIBILITY:Q2 (copy unchanged).
    for entries in data["gaps"].values():
        for e in entries:
            expected = ["question_id", "text", "text_ar"]
            if e["question_id"] == "mechanical:PHYSICAL_FEASIBILITY:Q2":
                expected = expected + ["routing"]
            assert list(e) == expected


# ---------------------------------------------------------------------------
# B. Exact copy
# ---------------------------------------------------------------------------

def test_every_approved_string_is_exact():
    got = {gap: [(e["question_id"], e["text"], e["text_ar"]) for e in entries]
           for gap, entries in _artifact()["gaps"].items()}
    assert got == APPROVED_COPY


def test_the_seam_serves_the_approved_copy_with_clamping():
    for gap, entries in APPROVED_COPY.items():
        for i in range(len(entries) + 2):
            served = pnq.get_served_question(gap, i, domain="mechanical")
            qid, en, ar = entries[min(i, len(entries) - 1)]
            assert (served.question_id, served.text, served.text_ar) == (qid, en, ar)
            assert pnq.get_path_n_question(gap, i, domain="mechanical") == en


# ---------------------------------------------------------------------------
# C. Owner-friendly default (old specialist wording no longer served)
# ---------------------------------------------------------------------------

def test_old_specialist_wording_is_no_longer_the_default():
    for served in _served_all():
        for old in _OLD_DEFAULT_EN:
            assert old.lower() not in served.text.lower(), old
        for old in _OLD_DEFAULT_AR:
            assert old not in served.text_ar, old


# ---------------------------------------------------------------------------
# D. Specialist bank preservation
# ---------------------------------------------------------------------------

def test_specialist_pack_is_byte_identical_and_keeps_its_depth():
    assert _sha(_MECH_PACK) == _UNCHANGED_SHA256[_MECH_PACK]
    with open(_MECH_PACK, encoding="utf-8") as fh:
        text = fh.read()
    for old in _OLD_DEFAULT_EN:
        assert old in text, old          # specialist concepts are NOT deleted


# ---------------------------------------------------------------------------
# E. Intent preservation
# ---------------------------------------------------------------------------

def test_intent_registry_is_byte_unchanged_and_matches_the_ids():
    assert _sha(_MECH_REGISTRY) == _UNCHANGED_SHA256[_MECH_REGISTRY]
    with open(_MECH_REGISTRY, encoding="utf-8") as fh:
        reg = json.load(fh)
    reg_ids = [(r["design_gap_id"], r["question_id"]) for r in reg["records"]]
    art_ids = [(g, q) for g, es in APPROVED_COPY.items() for q, _, _ in es]
    assert reg_ids == art_ids
    intent_serving._REGISTRY_CACHE.pop("mechanical", None)
    assert intent_serving._load_registry("mechanical") is not None


# ---------------------------------------------------------------------------
# F. Electronics non-regression
# ---------------------------------------------------------------------------

def test_electronics_artifacts_are_byte_identical():
    assert _sha(_EE_ARTIFACT) == _UNCHANGED_SHA256[_EE_ARTIFACT]
    assert _sha(_EE_REGISTRY) == _UNCHANGED_SHA256[_EE_REGISTRY]
    for served in _served_all(domain="electronics_electrical"):
        assert not served.question_id.startswith("mechanical:")


# ---------------------------------------------------------------------------
# web helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _start(c, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _token(c, sid):
    m = re.search(r'name="answer_token" value="([^"]+)"', _page(c, sid))
    return _html.unescape(m.group(1))


def _question(body):
    m = re.search(r'<p class="question"[^>]*>(.*?)</p>', body, re.S)
    return _html.unescape(m.group(1)).strip() if m else None


def _state(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _snapshot(state):
    return (tuple((g.gap_type, g.status, g.iterations_open) for g in state.gaps),
            state.maturity_level, getattr(state, "current_stage", None))


def _revisit_block(body):
    start = body.find('<details class="uqtr-revisit"')
    if start < 0:
        return None
    depth = 0
    for m in re.finditer(r"<details\b|</details>", body[start:]):
        depth += 1 if m.group(0) == "<details" else -1
        if depth == 0:
            return body[start:start + m.end()]
    raise AssertionError("unterminated revisit disclosure")


MC_Q1 = APPROVED_COPY["MECHANISM_COMPLETENESS"][0]


# ---------------------------------------------------------------------------
# G. RVR-7 — EN/AR render surfaces of ONE identity
# ---------------------------------------------------------------------------

def test_english_and_arabic_pages_render_the_same_identity(client):
    en_sid = _start(client)
    en_body = _page(client, en_sid)
    assert _question(en_body) == MC_Q1[1]
    ar_client_sid = None
    with csrf_client(appmod.app) as ar:
        ar_client_sid = _start(ar, lang="ar")
        ar_body = _page(ar, ar_client_sid)
        assert re.search(r'<html[^>]*lang="ar"[^>]*dir="rtl"', ar_body)
        assert _question(ar_body) == MC_Q1[2]
    # language never reaches canonical state: the same gap is served in both
    assert pl.select_next_gap(_state(en_sid)) == pl.select_next_gap(
        _state(ar_client_sid)) == MECHANISM_COMPLETENESS
    assert _snapshot(_state(en_sid)) == _snapshot(_state(ar_client_sid))


# ---------------------------------------------------------------------------
# H. UQTR CORE integration on the rewritten Mechanical Path N
# ---------------------------------------------------------------------------

def test_mechanical_unknown_is_durable_suppressed_unresolved_and_revisitable(client):
    sid = _start(client)
    before = _snapshot(_state(sid))
    assert _question(_page(client, sid)) == MC_Q1[1]
    r = client.post(f"/session/{sid}", data={"response": NOTE, "action": "unknown"})
    assert r.status_code == 302
    state = _state(sid)
    assert state.assertions[-1].disposition == "unknown"
    assert state.assertions[-1].gap_context == MECHANISM_COMPLETENESS
    sup = pl.compute_non_answer_suppression(state)
    assert sup is not None and sup.gap_type == MECHANISM_COMPLETENESS
    assert _snapshot(state) == before                 # no structural movement
    assert state.get_gap(MECHANISM_COMPLETENESS).status != CLOSED
    body = _page(client, sid)
    assert 'id="uqtr-suppressed"' in body
    revisit = _revisit_block(body)
    assert revisit is not None and MC_Q1[1] in _html.unescape(revisit)
    # a later answered interaction resumes ordinary serving
    r = client.post(f"/session/{sid}", data={
        "response": PLAIN_ANSWER, "action": "answered",
        "answer_token": _token(client, sid)})
    assert r.status_code == 302
    assert pl.compute_non_answer_suppression(_state(sid)) is None
    assert 'id="uqtr-suppressed"' not in _page(client, sid)


def test_deferred_is_equally_truthful_on_mechanical(client):
    sid = _start(client)
    before = _snapshot(_state(sid))
    client.post(f"/session/{sid}", data={"response": NOTE, "action": "deferred"})
    assert pl.compute_non_answer_suppression(_state(sid)).disposition == "deferred"
    assert _snapshot(_state(sid)) == before


# ---------------------------------------------------------------------------
# I. No AI / network / translation on this path
# ---------------------------------------------------------------------------

def test_no_model_network_or_translation_call(client, monkeypatch):
    import socket
    from engine import ai_advisor

    def _boom(*a, **k):
        raise AssertionError("network/model call attempted")

    monkeypatch.setattr(socket, "create_connection", _boom)
    monkeypatch.setattr(socket.socket, "connect", _boom)
    for name in dir(ai_advisor):
        if name.startswith("get_") and callable(getattr(ai_advisor, name)):
            monkeypatch.setattr(ai_advisor, name, _boom)
    sid = _start(client, lang="ar")
    assert _question(_page(client, sid)) == MC_Q1[2]
    client.post(f"/session/{sid}", data={"response": NOTE, "action": "unknown"})
    assert 'id="uqtr-suppressed"' in _page(client, sid)


# ---------------------------------------------------------------------------
# J. Wording is presentation only — no engine semantic change
# ---------------------------------------------------------------------------

def _run_journey(client):
    sid = _start(client)
    for answer in (PLAIN_ANSWER, "I am not sure which parts carry the weight."):
        client.post(f"/session/{sid}", data={
            "response": answer, "action": "answered",
            "answer_token": _token(client, sid)})
    client.post(f"/session/{sid}", data={"response": NOTE, "action": "unknown"})
    state = _state(sid)
    return (_snapshot(state), [(r.disposition, r.gap_context)
                               for r in state.assertions],
            pl.select_next_gap(state))


def test_identical_answers_give_identical_state_whatever_the_wording(client, monkeypatch):
    real = _run_journey(client)
    pnq._load_content("mechanical")
    altered = {gap: [dict(e, text="Neutral placeholder wording " + str(i),
                          text_ar="صياغة بديلة " + str(i))
                     for i, e in enumerate(entries)]
               for gap, entries in pnq._PATH_N_GAPS["mechanical"].items()}
    monkeypatch.setitem(pnq._PATH_N_GAPS, "mechanical", altered)
    assert real == _run_journey(client)


def test_owner_friendly_answer_is_not_fake_completion(client):
    sid = _start(client)
    maturity_before = _state(sid).maturity_level
    client.post(f"/session/{sid}", data={
        "response": "It folds.", "action": "answered",
        "answer_token": _token(client, sid)})
    state = _state(sid)
    assert state.get_gap(MECHANISM_COMPLETENESS).status != CLOSED
    assert state.maturity_level == maturity_before


# ---------------------------------------------------------------------------
# Browser (real Chromium): one EN and one AR mechanical journey
# ---------------------------------------------------------------------------

from tests.test_draft_l2_local_continuity import server, _browser  # noqa: E402,F401


def _browser_start_mechanical(page, base, arabic=False):
    page.goto(base + "/")
    if arabic:
        page.locator("form button[lang=ar]").first.click()
        page.wait_for_load_state()
    page.fill("#idea", SEED)
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    choice = page.locator('input[type=radio][name=domain_choice][value="mechanical"]')
    if choice.count():
        choice.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    confirm = page.locator("input[name=domain_confirm]")
    assert confirm.input_value() == "mechanical"
    confirm.check()
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    assert "/session/" in page.url


@pytest.mark.parametrize("arabic", [False, True], ids=["en", "ar"])
def test_browser_mechanical_owner_friendly_journey(server, _browser, arabic):
    ctx = _browser.new_context()
    page = ctx.new_page()
    try:
        _browser_start_mechanical(page, server, arabic=arabic)
        expected = MC_Q1[2] if arabic else MC_Q1[1]
        question = page.locator("p.question")
        assert question.inner_text().strip() == expected
        direction = question.evaluate("e => getComputedStyle(e).direction")
        assert direction == ("rtl" if arabic else "ltr")
        body = page.content()
        for old in (_OLD_DEFAULT_AR if arabic else _OLD_DEFAULT_EN):
            assert old not in body
        page.locator('input[name="action"][value="unknown"]').check()
        page.locator('#answer-form button[type="submit"]').click()
        page.wait_for_load_state()
        assert page.locator("#uqtr-suppressed").is_visible()
        page.locator("#uqtr-revisit > summary").click()
        assert page.locator("p.question").inner_text().strip() == expected
    finally:
        ctx.close()
