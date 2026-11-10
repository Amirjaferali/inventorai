"""BOARD-ENCLOSURE-ARABIC-QUALIFICATION-01 — Arabic qualification of the board-enclosure planar clearance journey.

Synthetic data only. What is pinned (the English journey and its F1 protection stay pinned by
test_board_enclosure_planar_clearance*.py):
  * the catalogue: every UI_PCC_* key holds English and Modern Standard Arabic; the English variant of each
    applicability statement and disclosure line IS the governed method artifact's text, so each Arabic line
    translates one stable governed meaning; placeholders and canonical tokens (mm, X / Y, c, board_x ...)
    survive in the Arabic text; the former English-only notice is gone;
  * language is presentation only: the SAME saved declaration renders the same outcome, margins, revision,
    snapshot digest and value states in English and Arabic, writes nothing and leaves the session page and the
    stored rows untouched; every outcome / state renders in Arabic with the same underlying meaning;
  * the report / PDF section follows the report DOCUMENT's language seam, not the interface on its own;
  * numeric input keeps the exact ASCII-decimal grammar: Arabic-Indic or Persian digits, Arabic decimal or
    group separators, units and words are refused (nothing written, never zero) with an Arabic explanation;
  * dialect fixtures (English, MSA, Kuwaiti / Gulf, Egyptian): component names, region descriptions and basis
    notes - including ordinary uncertainty and negation - are stored and shown verbatim and never turned into a
    dimension, an "unknown" or an applicability answer; the structured choices alone decide the outcome. This
    qualifies the guided workflow and text preservation, NOT understanding of unrestricted dialect text.
"""
import html as _html
import json
import re
import sqlite3

import pytest

import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from engine.record_store import PlanarClearanceCorrupt
from tests.csrf_client import csrf_client
from tests.test_board_enclosure_planar_clearance import (
    APPLIES, _digests, _fields, _margin_cells, _outcome, _page, _revisions, _save)
from tests.test_component_interface_participation import (
    _form as _icp_form, _post as _icp_post, _web_project)
from tests.test_component_inventory_correct_withdraw import _correct
from web import ui_text

ARTIFACT = json.load(open(pcc.ARTIFACT_PATH, encoding="utf-8"))
_ARABIC = re.compile(r"[\u0600-\u06FF]")
_TOKEN = re.compile(r"\b(?:board_[xy]|region_[xy]|mm|X|Y|c|OWNER_STATED|UNVALIDATED|InventorAI|NIST SP 811)\b")


@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _keys():
    return [k for k in ui_text.UI_STRINGS if k.startswith("UI_PCC_")]


def _web(c, names=("Driver board", "Plastic case", "Battery")):
    sid = _web_project(c, names=names)
    form = _icp_form(c, sid)
    ids = [o[0] for o in form["options"]]
    assert _icp_post(c, sid, form, ids).status_code in (200, 302)
    ifc = appmod._get_store().load_planar_clearance(sid)["interfaces"][0].interface_id
    return sid, ifc, ids


def _set_lang(c, lang):
    assert c.post("/ui-language", data={"lang": lang}).status_code in (200, 302)


def _plain(body):
    return " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", body)).split())


def _rows(sid):
    return appmod._get_store()._conn.execute(
        "SELECT * FROM planar_clearance_revisions WHERE project_id = ? ORDER BY event_seq",
        (sid,)).fetchall()


def _stable(body):
    body = re.sub(r'value="[^"]*"', "", body)
    return re.sub(r"\d{4}-\d\d-\d\d[T ]\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)?", "", body)


# ==========================================================================
# 1. catalogue: complete, anchored to the governed artifact, tokens kept
# ==========================================================================
def test_c01_every_key_has_english_and_arabic_and_the_english_only_notice_is_gone():
    keys = _keys()
    # 120 + 15 region-bound keys (BOARD-ENCLOSURE-CONDITIONAL-REGION-BOUND-01)
    # + 14 CAD-download keys (BOARD-ENCLOSURE-CAD-DOWNLOAD-01)
    # + 16 literal-source aid keys (G1-PCC-LITERAL-SOURCE-AID-01)
    # + 54 board-file source keys (BOARD-OUTLINE-SOURCE-BINDING-01)
    # + 4 current-answer aid keys (G1-CURRENT-ANSWER-DIMENSION-HANDOFF-01)
    assert len(keys) == 223 and not ui_text.has_string("UI_PCC_ENGLISH_ONLY")
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert set(entry) == {"en", "ar"}, key
        assert entry["en"].strip() and entry["ar"].strip() and entry["en"] != entry["ar"], key
        assert _ARABIC.search(entry["ar"]), key
        assert entry["en"].count("%s") == entry["ar"].count("%s"), key


def test_c02_statements_and_disclosures_are_the_governed_artifact_word_for_word():
    for decl in ARTIFACT["declarations"]:
        assert ui_text.text("UI_PCC_DECL_" + decl["declaration_id"], "en") == decl["statement"]
    assert [ui_text.text("UI_PCC_DISCLOSURE_%d" % n, "en")
            for n in range(1, 8)] == ARTIFACT["disclosure"]
    assert not ui_text.has_string("UI_PCC_DISCLOSURE_8")
    assert len([k for k in _keys() if k.startswith("UI_PCC_DECL_")]) == len(pcc.DECLARATION_IDS)


def test_c03_canonical_tokens_survive_in_the_arabic_text():
    for key in _keys():
        en, ar = ui_text.UI_STRINGS[key]["en"], ui_text.UI_STRINGS[key]["ar"]
        expected = set(_TOKEN.findall(en)) - {"c"}     # "c" also occurs inside English words
        if key.startswith("UI_PCC_DECL_uniform") or key in ("UI_PCC_DIAGRAM_LEGEND",):
            expected |= {"c"}
        assert expected <= set(_TOKEN.findall(ar)), (key, expected - set(_TOKEN.findall(ar)))
        # an Arabic letter fused onto a Latin token (e.g. a conjunction) breaks the token
        assert not re.search(r"[\u0600-\u06FF][A-Za-z_]", ar), key


def test_c04_meaning_bearing_wording_keeps_its_limits_in_arabic():
    ar = lambda key: ui_text.text(key, "ar")
    # MET is only the declared planar condition on the entered data
    assert "بالقيم وطريقة الوضع اللتين صرّحت بهما" in ar("UI_PCC_OUTCOME_MET")
    assert "متحقق" in ar("UI_PCC_OUTCOME_MET") and "غير" not in ar("UI_PCC_OUTCOME_MET")
    # NOT MET is not proof that nothing could work, and nothing is suggested
    for key in ("UI_PCC_NOT_MET_NOTE", "UI_PCC_DISCLOSURE_7"):
        assert "لا تُثبت" in ar(key)
    assert "لا يقترح" in ar("UI_PCC_NOT_MET_NOTE")
    # unknown is never zero; inputs are not verified; no fit / compatibility claim
    assert "صفر" in ar("UI_PCC_VALUE_HELP") and "لن تُعامَل" in ar("UI_PCC_VALUE_HELP")
    assert "لم يتحقق" in ar("UI_PCC_DISCLOSURE_2")
    assert ar("UI_PCC_DISCLOSURE_6").startswith("لا يُبيّن")
    # digits: 0-9 and the decimal point only; Arabic-Indic refused, never read as a number
    assert "0–9" in ar("UI_PCC_DIGITS_HELP") and "٠–٩" in ar("UI_PCC_DIGITS_HELP")
    assert "يُرفض" in ar("UI_PCC_DIGITS_HELP")


# ==========================================================================
# 2. language is presentation only
# ==========================================================================
def test_l01_switching_language_changes_presentation_only(client):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    rows_before = _rows(sid)
    client.get("/session/%s" % sid)
    session_before = _stable(client.get("/session/%s" % sid).get_data(as_text=True))
    en = _page(client, sid, ifc).get_data(as_text=True)
    ar = _page(client, sid, ifc, lang="ar").get_data(as_text=True)
    back = _page(client, sid, ifc, lang="en").get_data(as_text=True)
    for body in (en, ar, back):
        assert _outcome(body) == ["NOT_MET"] and _margin_cells(body) == ["-1 mm", "1 mm"]
        assert _revisions(body) == ["0"]
    assert _digests(en) == _digests(ar) == _digests(back)
    assert re.findall(r'data-pcc-value-state="(\w+)"', en) == re.findall(
        r'data-pcc-value-state="(\w+)"', ar)
    assert 'lang="ar" dir="rtl" data-pcc-page' in ar and 'lang="en" dir="ltr" data-pcc-page' in back
    assert ui_text.text("UI_PCC_OUTCOME_NOT_MET", "ar") in ar
    assert ui_text.text("UI_PCC_OUTCOME_NOT_MET", "en") in en
    assert _rows(sid) == rows_before                                    # nothing written
    assert _stable(client.get("/session/%s" % sid).get_data(as_text=True)) == session_before


def _state_pages(client, sid, ifc):
    return {lang: _page(client, sid, ifc, lang=lang).get_data(as_text=True) for lang in ("en", "ar")}


@pytest.mark.parametrize("case", ["equality", "unknown", "blank", "inapplicable"])
def test_l02_every_outcome_reads_the_same_meaning_in_both_languages(client, case):
    sid, ifc, ids = _web(client)
    values, unknown, answers = ("84", "50", "88", "54", "2"), (), APPLIES
    if case == "unknown":
        values, unknown = ("84", "50", "86", "56", ""), ("c",)
    elif case == "blank":
        values = ("84", "", "86", "56", "2")
    elif case == "inapplicable":
        answers = tuple(pcc.ANSWER_DOES_NOT_APPLY if d == "not_guide_mounted" else a
                        for d, a in zip(pcc.DECLARATION_IDS, APPLIES))
    _save(client, sid, ifc, ids, values=values, unknown=unknown, answers=answers)
    pages = _state_pages(client, sid, ifc)
    expected = {"equality": "MET", "unknown": "MISSING_INFORMATION",
                "blank": "MISSING_INFORMATION", "inapplicable": "INAPPLICABLE"}[case]
    for lang, body in pages.items():
        assert _outcome(body) == [expected], lang
        assert ui_text.text("UI_PCC_OUTCOME_" + expected, lang) in _html.unescape(body)
    if case == "equality":
        assert _margin_cells(pages["ar"]) == ["0 mm", "0 mm"]
        assert _plain(pages["ar"]).count(ui_text.text("UI_PCC_AXIS_MET", "ar")) >= 2
    if case in ("unknown", "blank"):
        missing = re.findall(r'data-pcc-missing-item="(\w+)"', pages["ar"])
        assert missing == (["c"] if case == "unknown" else ["board_y"])
        assert ui_text.text("UI_PCC_VALUE_" + missing[0], "ar") in _html.unescape(pages["ar"])
        state = "unknown" if case == "unknown" else "not_entered"
        assert 'data-pcc-value-state="%s"' % state in pages["ar"]
        word = ui_text.text("UI_PCC_VALUE_UNKNOWN" if case == "unknown" else "UI_PCC_VALUE_NOT_ENTERED", "ar")
        assert word in _html.unescape(pages["ar"])
        stored = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current.values
        assert stored[4 if case == "unknown" else 1] == ("unknown" if case == "unknown" else None)
    if case == "inapplicable":
        assert ui_text.text("UI_PCC_DECL_not_guide_mounted", "ar") in _html.unescape(pages["ar"])


def test_l03_reconfirmation_withdrawal_and_unavailable_in_arabic(client, monkeypatch):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    _correct(appmod._get_store(), sid, ids[0], 0, "Driver board v2", "Controls the motor")
    pages = _state_pages(client, sid, ifc)
    for lang, body in pages.items():
        assert 'data-pcc-state="NEEDS_RECONFIRMATION"' in body and _outcome(body) == []
    issue = ui_text.text("UI_PCC_ISSUE_COMPONENT_CHANGED", "ar") % ui_text.text("UI_PCC_ROLE_board", "ar")
    assert issue in _html.unescape(pages["ar"])
    data = _fields(_page(client, sid, ifc, lang="ar").get_data(as_text=True),
                   form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    r = client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    body = _html.unescape(r.get_data(as_text=True))
    assert ui_text.text("UI_PCC_MSG_WITHDRAWN", "ar") in body
    assert ui_text.text("UI_PCC_STATE_WITHDRAWN", "ar") in body

    def broken(self, project_id):
        raise PlanarClearanceCorrupt("broken")
    monkeypatch.setattr(type(appmod._get_store()), "load_planar_clearance", broken)
    r = _page(client, sid, ifc, lang="ar")
    assert r.status_code == 503
    assert ui_text.text("UI_PCC_UNAVAILABLE", "ar") in _html.unescape(r.get_data(as_text=True))


def test_l04_acknowledgement_currency_messages_in_arabic(client, monkeypatch):
    sid, ifc, ids = _web(client)
    _set_lang(client, "ar")
    page = _page(client, sid, ifc)
    assert ui_text.text("UI_PCC_MSG_SAVED", "ar") in _html.unescape(
        _save(client, sid, ifc, ids, page=page).get_data(as_text=True))
    _save(client, sid, ifc, ids, values=("84", "50", "90", "56", "2"))
    retried = _html.unescape(_save(client, sid, ifc, ids, page=page).get_data(as_text=True))
    assert ui_text.text("UI_PCC_MSG_RECORDED_EARLIER", "ar") in retried
    store_type = type(appmod._get_store())
    monkeypatch.setattr(store_type, "load_planar_clearance",
                        lambda self, pid: (_ for _ in ()).throw(sqlite3.OperationalError("locked")))
    unknown = _html.unescape(_save(client, sid, ifc, ids, page=page).get_data(as_text=True))
    assert ui_text.text("UI_PCC_MSG_RECORDED_CURRENCY_UNKNOWN", "ar") in unknown
    assert ui_text.text("UI_PCC_MSG_SAVED", "ar") not in unknown


# ==========================================================================
# 3. the report / PDF follows the document language
# ==========================================================================
def _section(body):
    return re.search(r"<section class=\"group\" data-pcc-report.*?</section>", body, re.S).group(0)


@pytest.mark.parametrize("ui,document", [("ar", "en"), ("en", "ar"), ("ar", "ar"), ("en", "en")])
def test_r01_the_report_section_follows_the_document_language(client, monkeypatch, ui, document):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    _set_lang(client, ui)
    monkeypatch.setattr(appmod, "_deliverable_document_lang", lambda: document)
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    section = _section(report)
    assert 'lang="%s"' % document in section.split(">", 1)[0]
    assert ui_text.text("UI_PCC_REPORT_HEADING", document) in _html.unescape(section)
    assert ui_text.text("UI_PCC_OUTCOME_NOT_MET", document) in _html.unescape(section)
    assert _outcome(section) == ["NOT_MET"] and _margin_cells(section) == ["-1 mm", "1 mm"]
    other = "en" if document == "ar" else "ar"
    assert ui_text.text("UI_PCC_REPORT_HEADING", other) not in _html.unescape(section)


def test_r02_the_arabic_pdf_carries_the_same_snapshot_and_outcome(client, monkeypatch):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    _set_lang(client, "ar")
    page = _page(client, sid, ifc).get_data(as_text=True)
    seen = {}
    real = appmod._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)
    monkeypatch.setattr(appmod, "_render_pdf_bytes", spy)
    r = client.post("/session/%s/deliverable.pdf" % sid, data={})
    assert r.status_code == 200 and r.data[:5] == b"%PDF-"
    section = _section(seen["source"])
    assert 'lang="ar"' in section.split(">", 1)[0]
    assert _outcome(section) == ["NOT_MET"] and _digests(section) == _digests(page)
    assert ui_text.text("UI_PCC_HISTORICAL_NOTE", "ar") in _html.unescape(section)


# ==========================================================================
# 4. numeric input: the exact ASCII grammar, refused otherwise, never zero
# ==========================================================================
@pytest.mark.parametrize("bad", ["٨٤", "۸۴", "84٫5", "84,5", "84،5", "84 mm", "84مم", "ثمانون",
                                 "٨٤.٥", "8٤", "1٬000", "−84", "84.5 ", ""])
def test_n01_non_ascii_digits_separators_units_and_words_are_refused(client, bad):
    sid, ifc, ids = _web(client)
    _set_lang(client, "ar")
    r = _save(client, sid, ifc, ids, values=(bad, "50", "86", "56", "2"))
    if bad.strip() == "84.5":
        # surrounding whitespace is trimmed at capture; the number itself is admitted
        assert r.status_code == 200
        assert appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(
            ifc).current.values[0] == "84.5"
        return
    if bad == "":
        # blank is "not entered": saved as missing information, never zero
        assert r.status_code == 200 and _outcome(r.get_data(as_text=True)) == ["MISSING_INFORMATION"]
        assert appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(
            ifc).current.values[0] is None
        return
    assert r.status_code == 400
    assert ui_text.text("UI_PCC_MSG_REJECTED", "ar") in _html.unescape(r.get_data(as_text=True))
    assert appmod._get_store().load_planar_clearance(sid)["ledger"].records == ()


def test_n02_the_numeric_fields_are_ltr_and_explain_the_digits_in_arabic(client):
    sid, ifc, ids = _web(client)
    body = _page(client, sid, ifc, lang="ar").get_data(as_text=True)
    for role in pcc.VALUE_ROLES:
        field = re.search(r'<input type="text" id="pcc-v-%s"[^>]*>' % role, body).group(0)
        assert 'dir="ltr"' in field and 'inputmode="decimal"' in field
    assert ui_text.text("UI_PCC_DIGITS_HELP", "ar") in _html.unescape(body)
    radios = re.findall(r'<input type="radio"[^>]*>', body)
    assert len(radios) == 16 and not any("checked" in radio for radio in radios)


# ==========================================================================
# 5. dialect fixtures: preservation, not interpretation
# ==========================================================================
FIXTURES = {
    "en": {"names": ("Controller board", "Plastic box", "Battery"),
           "region": "Inside floor between the four posts; nothing blocks it, I think",
           "basis_clearance": "I don't know the clearance yet, not measured"},
    "msa": {"names": ("لوحة التحكم", "الصندوق البلاستيكي", "البطارية"),
            "region": "الأرضية الداخلية بين الأعمدة الأربعة؛ لا شيء يعترضها على ما أظن",
            "basis_clearance": "لا أعرف الخلوص المطلوب بعد، لم أقِسه"},
    "kuwaiti": {"names": ("البورد حق التحكم", "البوكس البلاستيك", "البطارية"),
                "region": "الأرضية اللي بين العواميد الأربعة، مافي شي يسدها جذي",
                "basis_clearance": "ما أدري كم المسافة اللي أحتاجها، ما قستها للحين"},
    "egyptian": {"names": ("بوردة التحكم", "العلبة البلاستيك بتاعت الجهاز", "البطارية"),
                 "region": "الأرضية اللي جوه بين العواميد الأربعة، مفيش حاجة سادّاها تقريبًا",
                 "basis_clearance": "مش عارف المسافة المطلوبة لسه، مقستهاش"},
}


@pytest.mark.parametrize("variant", sorted(FIXTURES))
def test_d01_dialect_text_is_preserved_and_never_interpreted(client, variant):
    fx = FIXTURES[variant]
    sid, ifc, ids = _web(client, names=fx["names"])
    _set_lang(client, "ar" if variant != "en" else "en")
    # the structured choices: clearance explicitly unknown; the obstruction answer left unanswered
    answers = tuple(None if d == "region_unobstructed" else a
                    for d, a in zip(pcc.DECLARATION_IDS, APPLIES))
    r = _save(client, sid, ifc, ids, values=("84", "50", "86", "56", ""), unknown=("c",),
              answers=answers, extra={"region_description": fx["region"],
                                      "basis_clearance": fx["basis_clearance"],
                                      "basis_board": ""})
    body = r.get_data(as_text=True)
    material = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert material.region_description == fx["region"]                     # verbatim
    assert material.basis == (None, None, fx["basis_clearance"])
    assert material.values == ("84", "50", "86", "56", "unknown")          # the box, not the note
    assert material.applicability[pcc.DECLARATION_IDS.index("region_unobstructed")] is None
    assert _outcome(body) == ["MISSING_INFORMATION"]
    missing = re.findall(r'data-pcc-missing-item="(\w+)"', body)
    assert missing == ["c", "region_unobstructed"]                         # nothing inferred
    shown = _html.unescape(body)
    for text in (fx["region"], fx["basis_clearance"], fx["names"][0], fx["names"][1]):
        assert text in shown
    assert '<bdi dir="auto">%s</bdi>' % _html.escape(fx["region"], quote=False) in body or \
        '<bdi dir="auto">%s</bdi>' % _html.escape(fx["region"]) in body


def test_d02_the_same_structured_inputs_give_the_same_outcome_whatever_the_notes_language(client):
    outcomes = {}
    for variant, fx in FIXTURES.items():
        sid, ifc, ids = _web(client, names=fx["names"])
        r = _save(client, sid, ifc, ids, extra={"region_description": fx["region"],
                                                "basis_clearance": fx["basis_clearance"]})
        body = r.get_data(as_text=True)
        outcomes[variant] = (_outcome(body), _margin_cells(body))
    assert set(map(repr, outcomes.values())) == {repr((["NOT_MET"], ["-1 mm", "1 mm"]))}
