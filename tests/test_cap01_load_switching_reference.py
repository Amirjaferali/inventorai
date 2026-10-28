"""28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01 — ONE prose-only transistor load-switching reference.

For the exact Electronics MECHANISM_COMPLETENESS gap (OPEN or PARTIAL) the report /
deliverable and PDF show ONE further general explanation — a bipolar junction transistor
can be used as a current-controlled switch for a load — after the controller group, through
the existing Electronics / CAP-01 owner and its ``CAP01_GAP_FUNDAMENTALS_EXTENSIONS`` seam:

  * pack ``transistor_load_switching_reference_v1`` (one claim, no relationship); no
    coverage-declaration change (the existing covered area holds it);
  * provenance electronics_electrical:PR026 (Kuphaldt, Lessons In Electric Circuits,
    Volume III, online edition, Chapter 4 "The transistor as a switch"; Lead-supplied
    inspection) and PR027 (CC BY 4.0, Appendix 3 of that online edition);
  * conditional EN / AR wording: a general principle that may not apply to the inventor's
    invention, with no component, rating, value, circuit, controller-drive, suitability or
    safety statement, and the attribution, license, adaptation / translation and
    no-endorsement notices.
It is NOT Power Electronics / Motion (28-T3) capability, which stays BLOCKED.
"""
import hashlib
import io
import json
import os
import pickle
import re

import pytest

from engine.derived_readiness import derive_readiness
from engine.idea_state import (
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, MECHANISM_COMPLETENESS, OPEN, PARTIAL,
    PHYSICAL_FEASIBILITY)
from web import cap01_guidance, ui_text
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, ELEC_SEED, _start, _live,
)
from tests.test_cap01_mechanical_open_gap_context import _gaps, _pdf_source, _report, _visible
from tests.test_stage18_cap01_bounded_guidance import _mask_csrf
from tests.test_cap01_electrical_energy_time_reference import ET_GROUP, _html, _groups, _equations
from tests.test_cap01_electrical_reference_fundamentals import FUND_GROUP as BASE_GROUP
from tests.test_cap01_sensing_value_threshold_reference import GROUP as SENSING_GROUP
from tests.test_cap01_accuracy_resolution_reference import GROUP as ACCURACY_GROUP
from tests.cap01_controller_addition import CTRL_GROUP
from tests.cap01_charge_addition import CHARGE_GROUP
from tests.cap01_measurement_guidance_addition import MGUIDE_GROUP
from tests.cap01_measurement_conditions_addition import MCOND_GROUP
from tests.measurement_planning_integrated_part_amendment import (
    without_measurement_planning_integrated_part_amendment)
from tests.cap01_load_switching_addition import (
    LSW_CLAIM as CLAIM, LSW_GROUP as GROUP, LSW_NOTE as NOTE, LSW_RECORDS as RECORDS, LSW_ROW as ROW,
    LSW_SLUG as SLUG, without_load_switching_addition)
from tests.cap01_heat_path_verification_addition import (  # noqa: F401
    HPV_GROUP, HPV_RECORDS, without_heat_path_verification_addition)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")

DOMAIN = "electronics_electrical"
PREFIX = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_" + MECHANISM_COMPLETENESS + "_LOAD_SWITCHING_FUNDAMENTALS_"
SECTION_URL = "https://www.ibiblio.org/kuphaldt/electricCircuits/Semi/SEMI_4.html"
INDEX_URL = "https://www.ibiblio.org/kuphaldt/electricCircuits/Semi/index.html"
APPENDIX_URL = "https://www.ibiblio.org/kuphaldt/electricCircuits/Semi/SEMI_A3.html"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
LICENSE_CODE_URL = "https://creativecommons.org/licenses/by/4.0/legalcode.en"
TITLE = "Lessons In Electric Circuits, Volume III — Semiconductors"
# Canonical digests at base c1654784f590e47f8d33d9ad961759f8de3db7a4 (before this slice).
_PRE_PACK_DIGEST = "aa0d7e4de17d6dcc045e46e7ac697f09443c67700293c0c6949a3d6d029fa121"
_PRE_PROVENANCE_DIGEST = "ae03a14de8e122f7800f08494e96213aa5a47798bdb91fb4d272f0aeaedb57d0"

EXPLANATION = {
    "en": ("In general, a bipolar junction transistor (BJT) can be used as an electrically controlled switch for a "
           "load: a small current into its base controls whether a much larger current flows through the load "
           "along its collector-emitter path. With no base current it does not conduct and the load is off; with "
           "enough base current it conducts fully and the load is on. This describes a general principle only; it "
           "does not show that your design uses it, which transistor or values would be needed, or that any "
           "control signal can drive it."),
    "ar": ("بوجه عام، يمكن استخدام ترانزستور ثنائي القطب (BJT) مفتاحًا يُتحكَّم فيه كهربائيًا لتشغيل حِمل: إذ يتحكم "
           "تيار صغير يدخل قاعدته في مرور تيار أكبر بكثير عبر الحِمل في مسار المجمّع والباعث. فإذا لم يمرّ تيار في "
           "القاعدة لا يوصل الترانزستور ويكون الحِمل مطفأً، وإذا مرّ فيها تيار كافٍ يوصل كليًا ويكون الحِمل "
           "مشغّلًا. هذا وصف لمبدأ عام فقط، ولا يبيّن أن تصميمك يستخدمه، ولا أي ترانزستور أو قيم قد تلزم، ولا أن "
           "أي إشارة تحكم تستطيع تشغيله."),
}


def _iso(text):
    return "⁦" + text + "⁩"


PINNED = {
    "en": {
        "TITLE": "Transistor as a current-controlled switch (general principle)",
        "INTRO": "Reference information only. This general principle may not apply to your invention: InventorAI "
                 "has not determined that your design uses or needs a transistor or switches a load.",
        "ITEM_1_TITLE": "A small base current switches a larger load current",
        "BOUNDARY": "This explanation does not design a circuit, recommend or choose a transistor or any other "
                    "component, give a rating, current, voltage or resistor value, state that a microcontroller "
                    "or other control output can drive a transistor or a load directly or safely, or establish "
                    "that anything is suitable, works or is safe.",
        "SOURCE": "Source: Tony R. Kuphaldt, " + TITLE + ", online edition (index revised November 6, 2021), "
                  "Chapter 4 \"Bipolar Junction Transistors\", section \"The transistor as a switch\", "
                  + SECTION_URL + ". © Tony R. Kuphaldt. Licensed under the Creative Commons Attribution 4.0 "
                  "International License (CC BY 4.0, " + LICENSE_URL + "). Adapted: InventorAI explains this "
                  "point in its own words; the Arabic version is InventorAI's translation of that explanation. No "
                  "figure, circuit diagram, datasheet or other third-party material is used. This does not imply "
                  "that the author has reviewed, approved or endorsed InventorAI or this explanation.",
    },
    "ar": {
        "TITLE": "الترانزستور (transistor) بوصفه مفتاحًا يُتحكَّم فيه بالتيار (مبدأ عام)",
        "INTRO": "معلومات مرجعية فقط. قد لا ينطبق هذا المبدأ العام على اختراعك: لم يحدّد InventorAI أن تصميمك "
                 "يستخدم ترانزستورًا أو يحتاج إليه، ولا أنه يشغّل حِملًا ويطفئه.",
        "ITEM_1_TITLE": "تيار قاعدة صغير يتحكم في تيار حِمل أكبر",
        "BOUNDARY": "لا يصمّم هذا الشرح دائرة، ولا يوصي بترانزستور أو بأي مكوّن آخر ولا يختاره، ولا يعطي قيمة "
                    "اسمية أو تيارًا أو جهدًا أو قيمة مقاومة، ولا يقرّر أن متحكمًا دقيقًا أو أي مخرج تحكم آخر "
                    "يستطيع تشغيل ترانزستور أو حِمل مباشرةً أو بأمان، ولا يثبت أن أي شيء مناسب أو يعمل أو آمن.",
        "SOURCE": ("المصدر: توني آر. كوبالدت (Tony R. Kuphaldt)، " + _iso(TITLE) + "، النسخة الإلكترونية (فهرسها "
                   "منقّح في 6 نوفمبر 2021)، الفصل 4 " + _iso("\"Bipolar Junction Transistors\"") + "، القسم "
                   + _iso("\"The transistor as a switch\"") + "، على الرابط: " + _iso(SECTION_URL) + ". حقوق "
                   "النشر © لتوني آر. كوبالدت، وهو مرخّص بموجب رخصة المشاع الإبداعي "
                   + _iso("Creative Commons Attribution 4.0 International (CC BY 4.0)") + " المنشورة على الرابط: "
                   + _iso(LICENSE_URL) + ". مُقتبَس: شرح InventorAI هذه النقطة بكلماته، والنص العربي ترجمة "
                   "InventorAI لهذا الشرح. ولا يُستخدم أي شكل أو مخطط دائرة أو ورقة بيانات أو مواد أخرى لطرف ثالث. "
                   "ولا يعني ذلك أن المؤلف قد راجع InventorAI أو هذا الشرح أو وافق عليه أو أيّده."),
    },
}

_BLOCK_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="transistor-load-switching-reference-v1">'
    r'.*?\n      </div>', re.S)
_BLOCK_WITH_LEAD_RE = re.compile(r'\n\s*' + _BLOCK_RE.pattern, re.S)
_ANY_FUND_RE = re.compile(r'<div class="cap01-fundamentals" data-cap01-fundamentals="([^"]+)"')
REPORT_ORDER = ["sensing-value-threshold-reference-v1", "measurement-accuracy-resolution-reference-v1",
                "controller-input-logic-output-reference-v1", SLUG]


def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _pack():
    with io.open(_PACK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _provenance():
    with io.open(_PROVENANCE_PATH, encoding="utf-8") as fh:
        return json.load(fh)["records"]


def _group():
    [group] = [g for g in _pack()["reference_fundamentals"] if g["group_id"] == GROUP]
    return group


def _texts(lang):
    return {k[len(PREFIX):]: ui_text.UI_STRINGS[k][lang]
            for k in sorted(ui_text.UI_STRINGS) if k.startswith(PREFIX)}


def _body(lang):
    """Every reader-facing part of the group except the source attribution."""
    texts = _texts(lang)
    return " ".join(texts[k] for k in ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "BOUNDARY"))


# ==========================================================================
# 1. Binding: exact domain / gap / state; fixed order after the controller group
# ==========================================================================
@pytest.mark.parametrize("state", [OPEN, PARTIAL])
def test_b01_renders_for_the_exact_electronics_mechanism_gap_after_the_controller_group(state):
    groups = _groups((MECHANISM_COMPLETENESS, state))
    assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [
        SENSING_GROUP, ACCURACY_GROUP, CTRL_GROUP, GROUP]
    group = groups[MECHANISM_COMPLETENESS][3]
    assert group["prose_only"] is True
    assert [c["claim_id"] for c in group["claims"]] == [CLAIM]
    for lang in ("en", "ar"):
        html = _html((MECHANISM_COMPLETENESS, state), lang=lang)
        assert _ANY_FUND_RE.findall(html) == REPORT_ORDER
        assert len(_BLOCK_RE.findall(html)) == 1


@pytest.mark.parametrize("state", [CLOSED, ACCEPTED_RISK])
def test_b02_absent_when_the_gap_is_not_current(state):
    groups = _groups((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert MECHANISM_COMPLETENESS not in groups
    html = _html((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert _BLOCK_RE.search(html) is None and SLUG not in html


def test_b03_absent_for_other_gaps_and_other_domains():
    groups = _groups((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, OPEN))
    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
        assert GROUP not in [g["group_id"] for g in groups.get(gap, ())]
    assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP, CHARGE_GROUP]
    assert SLUG not in _html((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, PARTIAL))
    mech = _groups((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")
    assert all(GROUP not in [g["group_id"] for g in gs] for gs in (mech or {}).values())
    assert _BLOCK_RE.search(_html((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")) is None
    for domain in ("mechanical", "control_loop", "software", "medical_device", "Electronics_Electrical", ""):
        rows = cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS.get((domain, MECHANISM_COMPLETENESS)) or ()
        assert GROUP not in [r[0] for r in rows], domain


def test_b04_the_binding_is_one_fixed_row_appended_last_to_the_mechanism_context():
    row = cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS[(DOMAIN, MECHANISM_COMPLETENESS)]
    assert [r[0] for r in row] == [SENSING_GROUP, ACCURACY_GROUP, CTRL_GROUP, GROUP]
    assert row[-1] == ROW == (GROUP, (CLAIM,), "LOAD_SWITCHING_FUNDAMENTALS_")
    assert sorted(cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS) == [
        (DOMAIN, MECHANISM_COMPLETENESS), (DOMAIN, PHYSICAL_FEASIBILITY)]
    assert all(GROUP not in [r[0] for r in rows]
               for key, rows in cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS.items()
               if key != (DOMAIN, MECHANISM_COMPLETENESS))
    assert cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS == frozenset(
        {SENSING_GROUP, ACCURACY_GROUP, CTRL_GROUP, GROUP, MGUIDE_GROUP, MCOND_GROUP, HPV_GROUP})


def test_b05_never_reads_inventor_text_or_signals():
    plain = _html((MECHANISM_COMPLETENESS, OPEN))
    worded = _html((MECHANISM_COMPLETENESS, OPEN),
                   idea_text="A 2N2222 NPN transistor switch with a 1 kOhm base resistor driving a 12 V relay "
                             "and a DC motor from an Arduino pin through a MOSFET")
    assert _BLOCK_RE.search(plain).group(0) == _BLOCK_RE.search(worded).group(0)
    # the same words never make it appear where the binding does not hold
    assert _BLOCK_RE.search(_html((MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, OPEN),
                                  idea_text="a transistor switch driving a motor")) is None


def test_b06_the_report_differs_from_the_base_rendering_by_exactly_this_block(monkeypatch):
    for pairs in (((MECHANISM_COMPLETENESS, OPEN),),
                  ((MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, OPEN)),
                  ((MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, OPEN))):
        with_row = _mask_csrf(_html(*pairs))
        table = dict(cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS)
        table[(DOMAIN, MECHANISM_COMPLETENESS)] = tuple(
            r for r in table[(DOMAIN, MECHANISM_COMPLETENESS)] if r[0] != GROUP)
        monkeypatch.setattr(cap01_guidance, "CAP01_GAP_FUNDAMENTALS_EXTENSIONS", table)
        without_row = _mask_csrf(_html(*pairs))
        monkeypatch.undo()
        removed, count = _BLOCK_WITH_LEAD_RE.subn("", with_row)
        assert removed == without_row
        assert count == (1 if pairs[0][1] in (OPEN, PARTIAL) else 0)


# ==========================================================================
# 2. Copy: conditional, general educational wording in EN and AR
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c01_explanation_and_pinned_strings_are_exact(lang):
    texts = _texts(lang)
    assert texts["ITEM_1_TEXT"] == EXPLANATION[lang]
    for part, value in PINNED[lang].items():
        assert texts[part] == value, part
    assert sorted(texts) == sorted(["TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "SOURCE", "BOUNDARY"])


def test_c02_the_principle_is_stated_as_general_and_possibly_inapplicable():
    en, ar = _texts("en"), _texts("ar")
    assert "This general principle may not apply to your invention" in en["INTRO"]
    assert "has not determined that your design uses or needs a transistor or switches a load" in en["INTRO"]
    assert "قد لا ينطبق هذا المبدأ العام على اختراعك" in ar["INTRO"]
    assert "لم يحدّد InventorAI أن تصميمك يستخدم ترانزستورًا أو يحتاج إليه" in ar["INTRO"]
    assert en["ITEM_1_TEXT"].startswith("In general, a bipolar junction transistor (BJT) can be used ")
    assert ar["ITEM_1_TEXT"].startswith("بوجه عام، يمكن استخدام ترانزستور ثنائي القطب (BJT)")
    assert "This describes a general principle only" in en["ITEM_1_TEXT"]
    assert "it does not show that your design uses it" in en["ITEM_1_TEXT"]
    assert "هذا وصف لمبدأ عام فقط" in ar["ITEM_1_TEXT"] and "ولا يبيّن أن تصميمك يستخدمه" in ar["ITEM_1_TEXT"]
    assert "(general principle)" in en["TITLE"] and "(مبدأ عام)" in ar["TITLE"]


def test_c03_english_and_arabic_carry_the_same_statements():
    en, ar = EXPLANATION["en"], EXPLANATION["ar"]
    pairs = (("bipolar junction transistor (BJT)", "ترانزستور ثنائي القطب (BJT)"),
             ("electrically controlled switch", "مفتاحًا يُتحكَّم فيه كهربائيًا"),
             ("small current into its base", "تيار صغير يدخل قاعدته"),
             ("much larger current", "تيار أكبر بكثير"),
             ("collector-emitter path", "مسار المجمّع والباعث"),
             ("With no base current it does not conduct", "فإذا لم يمرّ تيار في القاعدة لا يوصل"),
             ("enough base current it conducts fully", "تيار كافٍ يوصل كليًا"),
             ("which transistor or values would be needed", "ولا أي ترانزستور أو قيم قد تلزم"),
             ("or that any control signal can drive it", "ولا أن أي إشارة تحكم تستطيع تشغيله"))
    for en_part, ar_part in pairs:
        assert en_part in en and ar_part in ar, (en_part, ar_part)
    assert len(re.findall(r"\.\s", en + " ")) == len(re.findall(r"\.\s", ar + " ")) == 3


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c04_no_project_requirement_selection_rating_or_circuit_instruction(lang):
    """Outside the boundary sentence (which negates them), no transistor requirement or
    recommendation, value, rating, part number, circuit or motor-control instruction appears."""
    texts = _texts(lang)
    body = " ".join(texts[k] for k in ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT")).lower()
    if lang == "en":
        for banned in ("your design needs", "your invention needs", "you need", "you should", "should use",
                       "must", "recommend", "choose", "select", "use a ", "connect", "wire", "resistor", "ohm",
                       "volt", "ampere", "milliamp", "gain", "beta", "hfe", "rating", "datasheet", "2n2222",
                       "pn2222", "npn", "pnp", "mosfet", "relay", "motor", "pwm", "h-bridge", "diode", "heat",
                       "suitable", "compatib", "safe", "directly", "microcontroller", "arduino", "gpio", "pin"):
            assert banned not in body, banned
    else:
        for banned in ("يحتاج تصميمك", "يجب", "ننصح", "اختر ", "استخدم ", "وصّل", "مقاومة", "أوم", "فولت",
                       "أمبير", "كسب", "قيمة اسمية", "ورقة بيانات", "محرك", "مرحّل", "صمام", "مناسب", "توافق",
                       "آمن", "مباشرة", "متحكم"):
            assert banned not in body, banned


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c05_no_direct_or_safe_controller_drive_implication(lang):
    """A controller output driving the transistor or the load is mentioned ONLY in the
    boundary sentence, as something this explanation does NOT state."""
    texts = _texts(lang)
    for part, text in texts.items():
        lowered = text.lower()
        drive_words = (("microcontroller", "control output", "directly", "safely") if lang == "en"
                       else ("متحكم", "مخرج تحكم", "مباشرةً", "بأمان"))
        if part == "BOUNDARY":
            for word in drive_words:
                assert word in lowered, word
        else:
            for word in drive_words:
                assert word not in lowered, (part, word)
    if lang == "en":
        assert ("state that a microcontroller or other control output can drive a transistor or a load directly "
                "or safely") in texts["BOUNDARY"]
        assert texts["BOUNDARY"].startswith("This explanation does not ")
        assert texts["ITEM_1_TEXT"].endswith("or that any control signal can drive it.")
    else:
        assert ("ولا يقرّر أن متحكمًا دقيقًا أو أي مخرج تحكم آخر يستطيع تشغيل ترانزستور أو حِمل مباشرةً أو بأمان"
                in texts["BOUNDARY"])
        assert texts["BOUNDARY"].startswith("لا يصمّم هذا الشرح")


def test_c06_digits_appear_only_in_the_source_citation():
    for lang in ("en", "ar"):
        for part, text in _texts(lang).items():
            if part == "SOURCE":
                continue
            assert not re.search(r"\d", text), (lang, part, text)


def test_c07_arabic_attribution_isolates_every_url_and_english_title_left_to_right():
    source = _texts("ar")["SOURCE"]
    for token in (TITLE, "\"Bipolar Junction Transistors\"", "\"The transistor as a switch\"", SECTION_URL,
                  "Creative Commons Attribution 4.0 International (CC BY 4.0)", LICENSE_URL):
        assert source.count(_iso(token)) == 1, token
    assert source.count("⁦") == source.count("⁩") == 6
    assert "⁦" not in _texts("en")["SOURCE"]


@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("pdf", [False, True])
def test_c08_rendered_block_carries_text_and_full_attribution_without_equation(lang, pdf):
    html = _html((MECHANISM_COMPLETENESS, OPEN), lang=lang, pdf=pdf)
    [block] = _BLOCK_RE.findall(html)
    visible = _visible(block)
    assert EXPLANATION[lang] in visible
    for part in ("TITLE", "INTRO", "ITEM_1_TITLE", "BOUNDARY", "SOURCE"):
        assert PINNED[lang][part].replace("⁦", "").replace("⁩", "") in visible.replace(
            "⁦", "").replace("⁩", ""), part
    for needle in ("Tony R. Kuphaldt", TITLE, SECTION_URL, LICENSE_URL, "CC BY 4.0", "November 6, 2021"
                   if lang == "en" else "6 نوفمبر 2021"):
        assert needle in visible, needle
    assert _equations(block) == [] and "data-cap01-fund-equation" not in block
    assert "data-cap01-fund-item-lead" not in block and "data-cap01-fund-item-note" not in block
    assert block.count("data-cap01-fund-item-text") == 1
    for markup in ("<img", "<table", "<svg", "<figure", "<a ", "<code", "<pre", "<input", "<form", "<button"):
        assert markup not in block, markup


# ==========================================================================
# 3. Intellectual-property boundary
# ==========================================================================
def test_i01_attribution_license_adaptation_and_no_endorsement():
    en, ar = _texts("en")["SOURCE"], _texts("ar")["SOURCE"]
    for needle in ("Tony R. Kuphaldt", TITLE, "online edition (index revised November 6, 2021)",
                   "Chapter 4 \"Bipolar Junction Transistors\"", "section \"The transistor as a switch\"",
                   SECTION_URL, "© Tony R. Kuphaldt", "Creative Commons Attribution 4.0 International License",
                   LICENSE_URL, "Adapted: InventorAI explains this point in its own words",
                   "the Arabic version is InventorAI's translation of that explanation",
                   "No figure, circuit diagram, datasheet or other third-party material is used"):
        assert needle in en, needle
    assert en.endswith("This does not imply that the author has reviewed, approved or endorsed InventorAI or "
                       "this explanation.")
    for needle in ("مُقتبَس", "بكلماته", "ترجمة InventorAI", "رخصة المشاع الإبداعي", "حقوق النشر © لتوني آر. كوبالدت"):
        assert needle in ar, needle
    assert ar.endswith("ولا يعني ذلك أن المؤلف قد راجع InventorAI أو هذا الشرح أو وافق عليه أو أيّده.")
    for lang in ("en", "ar"):
        for part, text in _texts(lang).items():
            if "Kuphaldt" in text or "CC BY" in text or "ibiblio" in text:
                assert part == "SOURCE", part


def test_i02_the_2007_pdf_edition_and_copyright_years_are_not_claimed():
    joined = " ".join(list(_texts("en").values()) + list(_texts("ar").values()))
    for banned in ("2007", "Design Science", "2000–2023", "2000-2023", ".pdf", "public domain",
                   "endorsed by", "recommended by"):
        assert banned not in joined, banned


def test_i03_no_source_figure_datasheet_or_example_circuit_material():
    text = (" ".join(list(_texts("en").values())) + " " + json.dumps(_group(), ensure_ascii=False)).lower()
    for banned in ("pn2222", "2n2222", "fairchild", "lamp", "solar cell", "thermocouple", "microphone",
                   "schematic", ".png", ".jpg", ".svg"):
        assert banned not in text, banned


# ==========================================================================
# 4. Fail closed; prose-only is not a global relaxation
# ==========================================================================
def test_f01_missing_required_prose_copy_removes_only_this_group(monkeypatch):
    for part in ("ITEM_1_TEXT", "ITEM_1_TITLE", "SOURCE", "BOUNDARY", "INTRO", "TITLE"):
        strings = dict(ui_text.UI_STRINGS)
        strings.pop(PREFIX + part)
        monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
        groups = _groups((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, OPEN))
        assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [
            SENSING_GROUP, ACCURACY_GROUP, CTRL_GROUP], part
        assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP, CHARGE_GROUP]
        monkeypatch.undo()


def test_f02_an_equation_key_never_substitutes_the_prose_text(monkeypatch):
    strings = dict(ui_text.UI_STRINGS)
    strings.pop(PREFIX + "ITEM_1_TEXT")
    strings[PREFIX + "ITEM_1_EQUATION"] = {"en": "x", "ar": "x"}
    monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
    groups = _groups((MECHANISM_COMPLETENESS, OPEN))
    assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [SENSING_GROUP, ACCURACY_GROUP, CTRL_GROUP]


# ==========================================================================
# 5. Pack / provenance: addition only, claim mapping, rights boundary
# ==========================================================================
def test_p01_pack_minus_exactly_this_addition_equals_the_base_pack():
    pack = _pack()
    assert _digest(without_measurement_planning_integrated_part_amendment(without_load_switching_addition(without_heat_path_verification_addition(pack)))) == _PRE_PACK_DIGEST
    ids = [g["group_id"] for g in pack["reference_fundamentals"]]
    assert ids.index(GROUP) == ids.index(CTRL_GROUP) + 1
    note = pack["_governance_notes"][NOTE]
    for phrase in ("28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01", "NOT Power Electronics / Motion (28-T3)",
                   "stays BLOCKED", "PR026", "PR027", "Lead-supplied primary-source inspection",
                   "the 2007 PDF edition is NOT the admitted source", "No coverage-declaration change",
                   "after controller_input_logic_output_reference_v1", "may not apply to the inventor's invention",
                   "inert", "PR001–PR025 are unchanged"):
        assert phrase in note, phrase


def test_p02_the_coverage_declaration_is_unchanged_and_already_covers_the_explanation():
    cov = _pack()["coverage_declaration"]
    assert "Concept-level explanation of basic circuit function and electronic mechanism" in cov["covered_areas"]
    assert len(cov["covered_areas"]) == 4
    joined = " ".join(cov["not_covered_areas"]).lower()
    assert "transistor" not in joined and "switch" not in joined and "power electronics" not in joined


def test_p03_the_group_is_one_prose_only_claim_with_its_records():
    group = _group()
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["applicable_gap_type"] == MECHANISM_COMPLETENESS
    [claim] = group["claims"]
    assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation", "source_ref",
                             "source_use_policy_ref"]
    assert "relationship" not in claim
    assert (claim["claim_id"], claim["applicable_gap_type"]) == (CLAIM, MECHANISM_COMPLETENESS)
    assert (claim["source_ref"], claim["source_use_policy_ref"]) == RECORDS
    assert "never a statement that the inventor's design uses or needs a transistor" in claim["fact"]
    for phrase in ("The principle may not apply to the inventor's invention", "never infers it from inventor text",
                   "No transistor or other component recommendation or selection",
                   "no rating, current, voltage, gain, base-drive or resistor value",
                   "no switching-circuit design or wiring instruction",
                   "no statement that a microcontroller or other control output can drive a transistor or a load "
                   "directly or safely", "no motor-control implementation",
                   "no compatibility, suitability, performance, validation or safety statement",
                   "NOT Power Electronics / Motion (28-T3) capability, which stays BLOCKED"):
        assert phrase in claim["limitation"], phrase


def test_p04_provenance_is_append_only_with_two_claim_specific_records():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids))
    i = ids.index("electronics_electrical:PR025")
    assert tuple(ids[i + 1:i + 3]) == RECORDS and tuple(ids[i + 3:i + 5]) == HPV_RECORDS
    assert ids[i + 5] == "mechanical:PR001"
    assert _digest([r for r in records if r["record_id"] not in RECORDS + HPV_RECORDS]) == _PRE_PROVENANCE_DIGEST
    src, use = (records[ids.index(r)] for r in RECORDS)
    assert sorted(src) == sorted(use) == sorted(records[i])
    assert (src["source_type"], src["tier"], src["pack_id"]) == ("openly_licensed_educational_text", 1, DOMAIN)
    assert (use["source_type"], use["tier"], use["pack_id"]) == ("source_use_policy", 1, DOMAIN)
    assert src["url"] == SECTION_URL and use["url"] == LICENSE_CODE_URL
    for needle in ("revised November 6, 2021", INDEX_URL, SECTION_URL, "Chapter 4 \"Bipolar Junction Transistors\"",
                   "section \"The transistor as a switch\"", "opening paragraph and section review",
                   "The 2007 PDF edition, which carries a different license, is NOT the admitted source"):
        assert needle in src["version_or_edition"], needle
    assert APPENDIX_URL in use["version_or_edition"]
    for rec in (src, use):
        edition = rec["version_or_edition"]
        assert "Lead-supplied primary-source inspection" in edition
        assert "not independently re-inspected by the executor" in edition
        assert "The Lead's inspection date was not supplied and is not stated" in edition or \
            "the Lead's inspection date was not supplied and is not stated" in edition
        assert rec["cross_domain_usage"] == []


def test_p05_claim_mapping_and_exclusions_are_recorded():
    notes = {r["record_id"]: r for r in _provenance()}[RECORDS[0]]["notes"]
    for phrase in ("CLAIM MAPPING", "\"The transistor as a switch\"", "cutoff (off)", "saturation (fully on)",
                   "EXCLUDED and not used, quoted or paraphrased", "every figure, schematic and circuit diagram",
                   "every worked example circuit", "every third-party datasheet and bibliography entry",
                   "no source sentence, figure or table is reproduced",
                   "The exact copyright-year range was not part of the Lead-supplied inspection record",
                   "No endorsement by the author is stated or implied", "electronics_electrical:PR027",
                   "NOT Power Electronics / Motion (28-T3) capability"):
        assert phrase in notes, phrase


def test_p06_rights_boundary_is_recorded_precisely():
    notes = {r["record_id"]: r for r in _provenance()}[RECORDS[1]]["notes"]
    for phrase in ("not a legal opinion or legal determination", "electronics_electrical:PR026", "ONLY",
                   "Appendix 3", "CC BY 4.0", "permits commercial reuse and adaptation with attribution",
                   "The differently licensed 2007 PDF edition and every older edition are NOT relied upon",
                   "the license name and link", "adapted (paraphrased)", "InventorAI's translation",
                   "no endorsement is stated or implied", "does not extend to any other claim"):
        assert phrase in notes, phrase


# ==========================================================================
# 6. No effect beyond the report / PDF presentation
# ==========================================================================
def test_x01_no_state_gap_progression_readiness_or_session_page_effect(client, monkeypatch):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((MECHANISM_COMPLETENESS, OPEN))
    state = _live(sid)
    before = pickle.dumps(state)
    gaps_before = [(g.gap_type, g.status) for g in state.gaps]
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    for lang in ("en", "ar"):
        assert _BLOCK_RE.search(_report(client, sid, lang=lang)) is not None
    assert _BLOCK_RE.search(_pdf_source(client, sid, monkeypatch)) is not None
    assert pickle.dumps(_live(sid)) == before
    assert [(g.gap_type, g.status) for g in _live(sid).gaps] == gaps_before == [(MECHANISM_COMPLETENESS, OPEN)]
    readiness = derive_readiness(_live(sid))
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert SLUG not in page


def test_x02_no_question_signal_calculation_safety_or_persistence_owner_changes():
    pack = _pack()
    mc = next(m for m in pack["gap_type_mappings"] if m["gap_type_id"] == MECHANISM_COMPLETENESS)
    assert [q["question_id"] for q in mc["questions"]] == [
        "electronics_electrical:MECHANISM_COMPLETENESS:Q%d" % n for n in (1, 2, 3, 4)]
    for path in ("engine/deterministic_calculation.py", "engine/domain_registry.py", "engine/domain_rules.py",
                 "engine/domain_activation.py", "engine/subsystem_model.py", "engine/idea_state.py",
                 "engine/readiness_snapshot.py", "engine/safety_signal.py", "engine/read_export_service.py",
                 "engine/record_store.py", "engine/disclosure_export.py", "engine/derived_readiness.py",
                 "engine/need_routing.py", "web/app.py", "web/templates/deliverable.html"):
        full = os.path.join(_ROOT, path)
        if not os.path.exists(full):
            continue
        text = open(full, encoding="utf-8").read()
        assert GROUP not in text and CLAIM not in text and "LOAD_SWITCHING_FUNDAMENTALS" not in text, path
