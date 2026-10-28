"""28-T1-ACCURACY-RESOLUTION-REFERENCE-01 — ONE prose-only measurement reference group.

For the exact Electronics MECHANISM_COMPLETENESS gap (OPEN or PARTIAL) the report /
deliverable and PDF show ONE further conceptual explanation — accuracy, resolution and
the number of displayed digits as distinct notions — after the PR #789 sensing group,
through the existing Electronics / CAP-01 owner and its
``CAP01_GAP_FUNDAMENTALS_EXTENSIONS`` seam:

  * pack ``measurement_accuracy_resolution_reference_v1`` (one claim, no relationship);
  * provenance electronics_electrical:PR014 (NIST/SEMATECH e-Handbook of Statistical
    Methods, sections 2.1.1.3 and 2.4.5.1; NIST explanatory passages only, MSA-labelled
    material excluded; Lead-supplied inspection) and PR015 (NIST source-use / rights
    boundary; passage-level, no blanket public-domain assumption);
  * the Owner-admitted English claim verbatim and its governed Arabic rendering, with the
    NIST attribution, both section links, the adaptation / translation notice and the
    no-endorsement notice in the report and PDF;
  * prose-only for THIS group and the sensing group only — every other group still
    requires its equation and fails closed when any copy is missing.
"""
import copy
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
# 28-T2-CONTROLLER-INPUT-LOGIC-OUTPUT-REFERENCE-01 later appended a further prose-only group AFTER this
# one; this file's checks exclude exactly that addition (tests/cap01_controller_addition.py).
from tests.cap01_controller_addition import (
    CTRL_GROUP, CTRL_NAMESPACE, CTRL_RECORDS, CTRL_ROW, CTRL_SLUG, without_controller_addition)
# ELECTRICAL-CHARGE-AMPERE-HOUR-REFERENCE-01 later appended a third group to the Electronics
# PHYSICAL_FEASIBILITY context; excluded here likewise (tests/cap01_charge_addition.py).
from tests.cap01_charge_addition import (
    CHARGE_GROUP, CHARGE_RECORDS, CHARGE_ROW, without_charge_addition)
# MEASUREMENT-PLAN-GUIDANCE-01 (C1) later appended ONE CAP-09-page-only guidance group to the pack (never a
# report context row); excluded here likewise (tests/cap01_measurement_guidance_addition.py).
from tests.cap01_measurement_guidance_addition import (
    MGUIDE_GROUP, MGUIDE_RECORDS, without_measurement_guidance_addition)
# MEASUREMENT-CONDITIONS-AWARENESS-01 later appended ONE further CAP-09-page-only guidance group (never a
# report context row); excluded here likewise (tests/cap01_measurement_conditions_addition.py).
from tests.cap01_measurement_conditions_addition import (
    MCOND_GROUP, MCOND_RECORDS, without_measurement_conditions_addition)
# 28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01 added one further prose-only group on the Electronics
# MECHANISM_COMPLETENESS context; excluded here likewise (tests/cap01_load_switching_addition.py).
from tests.cap01_load_switching_addition import (  # noqa: F401
    LSW_GROUP, LSW_RECORDS, LSW_ROW, LSW_SLUG, without_load_switching_addition)
from tests.cap01_heat_path_verification_addition import (  # noqa: F401
    HPV_GROUP, HPV_RECORDS, without_heat_path_verification_addition)
from tests.test_cap01_electrical_energy_time_reference import ET_GROUP, _html, _groups, _equations
from tests.test_cap01_electrical_reference_fundamentals import FUND_GROUP as BASE_GROUP
from tests.test_cap01_sensing_value_threshold_reference import (
    GROUP as SENSING_GROUP, CLAIM as SENSING_CLAIM)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")

DOMAIN = "electronics_electrical"
GROUP = "measurement_accuracy_resolution_reference_v1"
CLAIM = "measurement_accuracy_resolution_distinction"
NOTE = "measurement_accuracy_resolution_reference"
PREFIX = ("UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_" + MECHANISM_COMPLETENESS
          + "_ACCURACY_RESOLUTION_FUNDAMENTALS_")
RECORDS = ("electronics_electrical:PR014", "electronics_electrical:PR015")
ACCURACY_URL = "https://www.itl.nist.gov/div898/handbook/mpc/section1/mpc113.htm"
RESOLUTION_URL = "https://itl.nist.gov/div898/handbook/mpc/section4/mpc451.htm"
POLICY_URL = ("https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-"
              "software-and-technical-series-publications")
# Canonical digests at base 633d89bdf4411e47bece765f34fd7739d2a5e6ce (before this slice).
_PRE_PACK_DIGEST = "481692d0a4d4369ae1fe7d20de645017910846c7233876eb1bf0aa6704b64a9b"
_PRE_PROVENANCE_DIGEST = "5e7c913ec8131747e1747017c6cbc8805de29825baa62d0d973c4f22351e470f"

# The Owner-admitted English claim, verbatim, and its governed Arabic rendering.
ADMITTED = {
    "en": ("Measurement accuracy concerns agreement with a true or reference value. Measurement "
           "resolution concerns distinguishing small differences. The number of displayed digits "
           "does not by itself establish instrument resolution."),
    "ar": ("تتعلق دقة القياس (accuracy) بتوافق القياس مع قيمة حقيقية أو مرجعية. وتتعلق قدرة التمييز "
           "في القياس (resolution) بالتمييز بين الفروق الصغيرة. ولا يكفي عدد الأرقام المعروضة وحده "
           "لإثبات قدرة التمييز لدى أداة القياس."),
}
# Executor-authored strings around the admitted text, pinned exactly.
PINNED = {
    "en": {
        "TITLE": "Measurement: accuracy and resolution",
        "INTRO": "Reference information only. InventorAI has not determined that your design measures a "
                 "quantity or what accuracy or resolution it needs.",
        "ITEM_1_TITLE": "Accuracy, resolution and displayed digits",
        "BOUNDARY": "This explanation does not select or recommend an instrument or sensor, set or assess "
                    "any accuracy or resolution value, calibrate anything, or establish measurement "
                    "quality, performance or safety.",
        "SOURCE": "Source: National Institute of Standards and Technology (NIST), NIST/SEMATECH "
                  "e-Handbook of Statistical Methods, section 2.1.1.3 (accuracy), " + ACCURACY_URL
                  + ", and section 2.4.5.1 (resolution), " + RESOLUTION_URL + ". Adapted: InventorAI "
                  "restated these points in its own words from NIST's explanatory text; the Arabic "
                  "version is InventorAI's translation of that restatement. No figure, table or text "
                  "that the handbook attributes to another source is used. This does not imply that "
                  "NIST has reviewed, approved or endorsed InventorAI or this explanation.",
    },
    "ar": {
        "TITLE": "القياس: الدقة وقدرة التمييز",
        "INTRO": "معلومات مرجعية فقط. لم يحدّد InventorAI أن تصميمك يقيس كمية ما، ولا مقدار الدقة أو "
                 "قدرة التمييز التي يحتاجها.",
        "ITEM_1_TITLE": "الدقة وقدرة التمييز وعدد الأرقام المعروضة",
        "BOUNDARY": "لا يختار هذا الشرح أداة قياس أو مستشعرًا ولا يوصي بأيٍّ منهما، ولا يحدّد أو يقيّم "
                    "أي قيمة للدقة أو لقدرة التمييز، ولا يُجري أي معايرة، ولا يثبت جودة القياس أو "
                    "الأداء أو السلامة.",
        "SOURCE": ("المصدر: المعهد الوطني للمعايير والتقنية في الولايات المتحدة (NIST)، الدليل "
                   "الإلكتروني NIST/SEMATECH e-Handbook of Statistical Methods، القسم 2.1.1.3 (الدقة) "
                   "على الرابط: ⁦" + ACCURACY_URL + "⁩، والقسم 2.4.5.1 (قدرة التمييز) على "
                   "الرابط: ⁦" + RESOLUTION_URL + "⁩. مُقتبَس: أعاد InventorAI صياغة هذه "
                   "النقاط بكلماته استنادًا إلى النص التوضيحي الصادر عن NIST، والنص العربي ترجمة "
                   "InventorAI لهذه الصياغة. ولا يُستخدم أي شكل أو جدول أو نص ينسبه الدليل إلى مصدر "
                   "آخر. ولا يعني ذلك أن NIST راجع InventorAI أو هذا الشرح أو وافق عليه أو أيّده."),
    },
}

_BLOCK_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="measurement-accuracy-resolution-reference-v1">'
    r'.*?\n      </div>', re.S)
_ANY_FUND_RE = re.compile(r'<div class="cap01-fundamentals" data-cap01-fundamentals="([^"]+)"')
# The same block with the line break and indentation the template emits before it.
_BLOCK_WITH_LEAD_RE = re.compile(r'\n\s*' + _BLOCK_RE.pattern, re.S)


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


def _sentences(text, lang):
    return [s for s in re.split(r"(?<=\.)\s+", text.strip()) if s]


# ==========================================================================
# 1. Binding: exact domain / gap / state; fixed order after the sensing group
# ==========================================================================
@pytest.mark.parametrize("state", [OPEN, PARTIAL])
def test_b01_renders_for_the_exact_electronics_mechanism_gap_after_the_sensing_group(state):
    groups = _groups((MECHANISM_COMPLETENESS, state))
    assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [SENSING_GROUP, GROUP, CTRL_GROUP, LSW_GROUP]
    sensing, group = groups[MECHANISM_COMPLETENESS][:2]
    assert [c["claim_id"] for c in sensing["claims"]] == [SENSING_CLAIM]
    assert group["prose_only"] is True
    assert [c["claim_id"] for c in group["claims"]] == [CLAIM]
    html = _html((MECHANISM_COMPLETENESS, state))
    assert _ANY_FUND_RE.findall(html) == ["sensing-value-threshold-reference-v1",
                                          "measurement-accuracy-resolution-reference-v1", CTRL_SLUG, LSW_SLUG]
    assert len(_BLOCK_RE.findall(html)) == 1


@pytest.mark.parametrize("state", [CLOSED, ACCEPTED_RISK])
def test_b02_absent_when_the_gap_is_not_current(state):
    groups = _groups((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert MECHANISM_COMPLETENESS not in groups
    html = _html((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert _BLOCK_RE.search(html) is None and "measurement-accuracy-resolution" not in html


def test_b03_absent_for_other_gaps_and_other_domains():
    groups = _groups((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, OPEN))
    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
        assert GROUP not in [g["group_id"] for g in groups.get(gap, ())]
    assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP, CHARGE_GROUP]
    mech = _groups((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")
    assert all(GROUP not in [g["group_id"] for g in gs] for gs in (mech or {}).values())
    assert _BLOCK_RE.search(_html((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")) is None
    for domain in ("control_loop", "software", "medical_device", "Electronics_Electrical", ""):
        assert cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS.get((domain, MECHANISM_COMPLETENESS)) is None
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS.get((DOMAIN, MECHANISM_COMPLETENESS)) is None


def test_b04_the_binding_is_one_fixed_row_appended_to_the_sensing_context():
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS == {
        (DOMAIN, PHYSICAL_FEASIBILITY): (
            (ET_GROUP, ("constant_power_energy_reference", "energy_time_unit_discipline"),
             "ENERGY_TIME_FUNDAMENTALS_"), CHARGE_ROW),
        (DOMAIN, MECHANISM_COMPLETENESS): (
            (SENSING_GROUP, (SENSING_CLAIM,), "SENSING_FUNDAMENTALS_"),
            (GROUP, (CLAIM,), "ACCURACY_RESOLUTION_FUNDAMENTALS_"), CTRL_ROW, LSW_ROW),
    }
    assert cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS == frozenset({SENSING_GROUP, GROUP, CTRL_GROUP, MGUIDE_GROUP, MCOND_GROUP, LSW_GROUP, HPV_GROUP})


def test_b05_never_reads_inventor_text_or_signals():
    plain = _html((MECHANISM_COMPLETENESS, OPEN))
    measuring = _html((MECHANISM_COMPLETENESS, OPEN),
                      idea_text="A 6.5-digit multimeter with 0.001 V resolution, 0.5 % accuracy and a "
                                "calibrated precision sensor")
    assert _BLOCK_RE.search(plain).group(0) == _BLOCK_RE.search(measuring).group(0)


def test_b06_the_report_differs_from_the_base_rendering_by_exactly_this_block(monkeypatch):
    for pairs in (((MECHANISM_COMPLETENESS, OPEN),),
                  ((MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, OPEN)),
                  ((MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, OPEN))):
        with_row = _mask_csrf(_html(*pairs))
        table = dict(cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS)
        row = table[(DOMAIN, MECHANISM_COMPLETENESS)]
        table[(DOMAIN, MECHANISM_COMPLETENESS)] = row[:1] + row[2:]
        monkeypatch.setattr(cap01_guidance, "CAP01_GAP_FUNDAMENTALS_EXTENSIONS", table)
        without_row = _mask_csrf(_html(*pairs))
        monkeypatch.undo()
        removed, count = _BLOCK_WITH_LEAD_RE.subn("", with_row)
        assert removed == without_row
        assert count == (1 if pairs[0][1] in (OPEN, PARTIAL) else 0)


# ==========================================================================
# 2. Copy: admitted EN claim, governed AR rendering, attribution, pinned strings
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c01_admitted_text_and_pinned_strings_are_exact(lang):
    texts = _texts(lang)
    assert texts["ITEM_1_TEXT"] == ADMITTED[lang]
    for part, value in PINNED[lang].items():
        assert texts[part] == value, part
    assert sorted(texts) == sorted(["TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "SOURCE",
                                    "BOUNDARY"])


def test_c02_the_pack_fact_is_the_admitted_english_claim_verbatim():
    [claim] = _group()["claims"]
    assert claim["fact"] == ADMITTED["en"] == _texts("en")["ITEM_1_TEXT"]


@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("pdf", [False, True])
def test_c03_rendered_block_carries_text_and_full_attribution_without_equation(lang, pdf):
    html = _html((MECHANISM_COMPLETENESS, OPEN), lang=lang, pdf=pdf)
    [block] = _BLOCK_RE.findall(html)
    visible = _visible(block)
    assert ADMITTED[lang] in visible
    for needle in ("NIST", "NIST/SEMATECH e-Handbook of Statistical Methods", "2.1.1.3", "2.4.5.1",
                   ACCURACY_URL, RESOLUTION_URL):
        assert needle in visible, needle
    if lang == "en":
        for needle in ("Adapted", "in its own words", "translation", "does not imply that NIST"):
            assert needle in visible, needle
    else:
        for needle in ("مُقتبَس", "بكلماته", "ترجمة", "لا يعني ذلك أن NIST"):
            assert needle in visible, needle
    assert _equations(block) == [] and "data-cap01-fund-equation" not in block
    assert "data-cap01-fund-item-lead" not in block and "data-cap01-fund-item-note" not in block
    assert block.count("data-cap01-fund-item-text") == 1
    assert 'style="overflow-wrap:anywhere"' in block
    for markup in ("<img", "<table", "<svg", "<figure", "<a ", "<input", "<form", "<button"):
        assert markup not in block, markup


def test_c04_english_and_arabic_carry_the_same_three_statements():
    en, ar = _sentences(ADMITTED["en"], "en"), _sentences(ADMITTED["ar"], "ar")
    assert len(en) == len(ar) == 3
    # 1. accuracy <-> agreement with a true or reference value
    assert en[0].startswith("Measurement accuracy concerns agreement with a true or reference value")
    assert "دقة القياس (accuracy)" in ar[0] and "بتوافق القياس" in ar[0]
    assert "قيمة حقيقية أو مرجعية" in ar[0]
    # 2. resolution <-> distinguishing small differences
    assert en[1] == "Measurement resolution concerns distinguishing small differences."
    assert "قدرة التمييز في القياس (resolution)" in ar[1] and "بالتمييز بين الفروق الصغيرة" in ar[1]
    # 3. displayed digits do not BY THEMSELVES establish instrument resolution
    assert en[2] == "The number of displayed digits does not by itself establish instrument resolution."
    for phrase in ("لا يكفي", "عدد الأرقام المعروضة", "وحده", "لإثبات قدرة التمييز", "أداة القياس"):
        assert phrase in ar[2], phrase
    # the first-use bilingual labels appear exactly once each
    assert ADMITTED["ar"].count("(accuracy)") == 1 and ADMITTED["ar"].count("(resolution)") == 1


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c05_no_statement_that_resolution_or_digits_establish_accuracy(lang):
    """The previously rejected formulation (finer resolution establishing accuracy) is not
    reintroduced anywhere in this group's copy or its pack text: accuracy is stated only
    as agreement with a true or reference value, and no comparative resolution or digit
    count is linked to it."""
    joined = " ".join(_texts(lang).values())
    lowered = joined.lower()
    if lang == "en":
        for banned in ("finer", "higher resolution", "better resolution", "more digits",
                       "more accurate", "improves accuracy", "ensures accuracy", "guarantees accuracy",
                       "establish accuracy", "establishes accuracy", "precision", "precise"):
            assert banned not in lowered, banned
        assert not re.search(r"resolution[^.]*(?:establish|ensure|guarantee|impl|determin)[^.]*accura",
                             lowered)
        assert not re.search(r"digits[^.]*accura", lowered)
    else:
        for banned in ("أدق", "أعلى دقة", "أكثر دقة", "يضمن الدقة", "تضمن الدقة", "يثبت الدقة",
                       "تثبت الدقة", "لإثبات الدقة", "الإحكام"):
            assert banned not in joined, banned
    claim_text = json.dumps(_group(), ensure_ascii=False).lower()
    for banned in ("finer resolution", "higher resolution", "more digits", "ensures accuracy",
                   "guarantees accuracy"):
        assert banned not in claim_text, banned
    assert "no statement that resolution or displayed digits establish, imply or bound accuracy" in claim_text


def test_c06_digits_appear_only_in_the_source_citation():
    for lang in ("en", "ar"):
        for part, text in _texts(lang).items():
            if part == "SOURCE":
                continue
            assert not re.search(r"\d", text), (lang, part, text)


def test_c07_arabic_attribution_isolates_each_url_left_to_right():
    source = _texts("ar")["SOURCE"]
    for url in (ACCURACY_URL, RESOLUTION_URL):
        assert source.count(url) == 1
        assert ("⁦" + url + "⁩") in source
    assert source.count("⁦") == source.count("⁩") == 2
    assert "⁦" not in _texts("en")["SOURCE"]


# ==========================================================================
# 3. Intellectual-property boundary
# ==========================================================================
def test_i01_no_msa_or_other_third_party_definition_material_in_copy_or_pack():
    copy_text = " ".join(list(_texts("en").values()) + list(_texts("ar").values()))
    pack_text = json.dumps(_group(), ensure_ascii=False)
    for text in (copy_text, pack_text):
        lowered = text.lower()
        for banned in ("msa", "measurement systems analysis", "aiag", "δ", "delta", "equal probability",
                       "artifact", "least-significant", "least significant", "manufacturer",
                       "reference standard", "gauge", "iso ", "vim", "astm", "ansi"):
            assert banned not in lowered, banned


def test_i02_no_source_sentence_is_reproduced():
    copy_text = " ".join(list(_texts("en").values()) + list(_texts("ar").values()) + [_group()["claims"][0]["fact"]])
    lowered = copy_text.lower()
    # short fragments of the NIST handbook wording, used here only as negative checks
    for fragment in ("qualitative term", "digits displayed", "discriminate between", "close together in value",
                     "made on an object", "target or reference"):
        assert fragment not in lowered, fragment


def test_i03_attribution_states_no_endorsement_and_identifies_the_adaptation():
    en, ar = _texts("en"), _texts("ar")
    assert en["SOURCE"].endswith("This does not imply that NIST has reviewed, approved or endorsed "
                                 "InventorAI or this explanation.")
    assert ar["SOURCE"].endswith("ولا يعني ذلك أن NIST راجع InventorAI أو هذا الشرح أو وافق عليه أو أيّده.")
    joined = " ".join(list(en.values())).lower()
    for banned in ("endorsed by", "approved by", "certified by", "recommended by", "according to nist",
                   "nist recommends", "nist-approved", "nist certified", "nist confirms", "logo"):
        assert banned not in joined, banned
    for part, text in en.items():
        if "NIST" in text:
            assert part == "SOURCE", part
    for part, text in ar.items():
        if "NIST" in text:
            assert part == "SOURCE", part


# ==========================================================================
# 4. Fail closed; prose-only is not a global relaxation
# ==========================================================================
def test_f01_missing_required_prose_copy_removes_only_this_group(monkeypatch):
    for part in ("ITEM_1_TEXT", "ITEM_1_TITLE", "SOURCE", "BOUNDARY", "INTRO", "TITLE"):
        strings = dict(ui_text.UI_STRINGS)
        strings.pop(PREFIX + part)
        monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
        groups = _groups((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, OPEN))
        assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [SENSING_GROUP, CTRL_GROUP, LSW_GROUP], part
        assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP, CHARGE_GROUP]
        monkeypatch.undo()


def test_f02_an_equation_key_never_substitutes_the_prose_text(monkeypatch):
    strings = dict(ui_text.UI_STRINGS)
    strings.pop(PREFIX + "ITEM_1_TEXT")
    strings[PREFIX + "ITEM_1_EQUATION"] = {"en": "x", "ar": "x"}
    monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
    groups = _groups((MECHANISM_COMPLETENESS, OPEN))
    assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [SENSING_GROUP, CTRL_GROUP, LSW_GROUP]


def test_f03_existing_groups_keep_requiring_their_equation(monkeypatch):
    key = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_EQUATION"
    strings = dict(ui_text.UI_STRINGS)
    strings.pop(key)
    monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
    assert [g["group_id"] for g in _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]] == [
        ET_GROUP, CHARGE_GROUP]
    monkeypatch.undo()
    for group in _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]:
        assert group["prose_only"] is False
        assert all("equation_key" in c and "text_key" not in c for c in group["claims"])


# ==========================================================================
# 5. Pack / provenance: addition only, claim mapping, rights boundary
# ==========================================================================
def test_p01_pack_minus_exactly_this_addition_equals_the_base_pack():
    pack = _pack()
    assert [g["group_id"] for g in pack["reference_fundamentals"]] == [BASE_GROUP, ET_GROUP, SENSING_GROUP,
                                                                       GROUP, CTRL_GROUP, LSW_GROUP, CHARGE_GROUP,
                                                                       MGUIDE_GROUP, MCOND_GROUP, HPV_GROUP]
    pre = without_measurement_conditions_addition(without_measurement_guidance_addition(without_charge_addition(without_controller_addition(without_load_switching_addition(without_heat_path_verification_addition(pack))))))
    pre["reference_fundamentals"] = [g for g in pre["reference_fundamentals"] if g["group_id"] != GROUP]
    note = pre["_governance_notes"].pop(NOTE)
    assert _digest(pre) == _PRE_PACK_DIGEST
    for phrase in ("28-T1-ACCURACY-RESOLUTION-REFERENCE-01", "PR014", "PR015", "inert",
                   "MSA-labelled material excluded", "no blanket public-domain assumption",
                   "PR001–PR013 are unchanged", "after sensing_value_threshold_reference_v1"):
        assert phrase in note, phrase


def test_p02_the_group_is_one_prose_only_claim_with_its_records():
    group = _group()
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["applicable_gap_type"] == MECHANISM_COMPLETENESS
    [claim] = group["claims"]
    assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation", "source_ref",
                             "source_use_policy_ref"]
    assert "relationship" not in claim
    assert (claim["claim_id"], claim["applicable_gap_type"]) == (CLAIM, MECHANISM_COMPLETENESS)
    assert (claim["source_ref"], claim["source_use_policy_ref"]) == RECORDS
    for phrase in ("No instrument or sensor selection or recommendation", "calibration conclusion",
                   "safety", "CAP-09", "never infers it from inventor text"):
        assert phrase in claim["limitation"], phrase


def test_p03_provenance_is_append_only_with_two_claim_specific_records():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids))
    i = ids.index("electronics_electrical:PR013")
    assert tuple(ids[i + 1:i + 3]) == RECORDS
    pre = [r for r in records if r["record_id"] not in RECORDS + CTRL_RECORDS + CHARGE_RECORDS + MGUIDE_RECORDS + MCOND_RECORDS + LSW_RECORDS + HPV_RECORDS]
    assert _digest(pre) == _PRE_PROVENANCE_DIGEST                     # PR001–PR013 and others unchanged
    src, use = (records[ids.index(r)] for r in RECORDS)
    assert sorted(src) == sorted(use) == sorted(records[i])
    assert (src["source_type"], src["jurisdiction"], src["tier"]) == ("government_reference_publication", "US", 1)
    assert (use["source_type"], use["jurisdiction"], use["tier"]) == ("source_use_policy", "US", 1)
    assert src["url"] == ACCURACY_URL and RESOLUTION_URL in src["notes"]
    assert ACCURACY_URL in src["version_or_edition"] and RESOLUTION_URL in src["version_or_edition"]
    assert use["url"] == POLICY_URL
    assert "NIST/SEMATECH e-Handbook of Statistical Methods" in src["source_name"]
    assert "2.1.1.3" in src["source_name"] and "2.4.5.1" in src["source_name"]
    assert src["cross_domain_usage"] == use["cross_domain_usage"] == []


def test_p04_inspection_status_is_recorded_honestly():
    records = {r["record_id"]: r for r in _provenance()}
    src, use = (records[r] for r in RECORDS)
    for rec in (src, use):
        assert "Lead-supplied inspection" in rec["version_or_edition"]
        assert "not independently re-inspected by the executor" in rec["version_or_edition"]
        assert "blocked by environment policy" in rec["version_or_edition"]
    assert "search-index results" in src["version_or_edition"]
    assert "not a source inspection" in src["version_or_edition"]


def test_p05_claim_mapping_is_passage_level_and_excludes_msa_and_third_party_material():
    src = {r["record_id"]: r for r in _provenance()}[RECORDS[0]]
    notes = src["notes"]
    for phrase in ("CLAIM MAPPING (passage level", "sentence 1", "sentence 2", "sentence 3",
                   "Section 2.1.1.3", "Section 2.4.5.1", "EXCLUDED and not used, quoted or paraphrased",
                   "MSA (Measurement Systems Analysis) manual", "any other MSA-labelled text",
                   "every figure, target diagram, table, worked example and data set",
                   "no source sentence, figure or table is reproduced",
                   "does not state that resolution or displayed digits establish, imply or bound accuracy",
                   "no-endorsement notice", "electronics_electrical:PR015"):
        assert phrase in notes, phrase


def test_p06_rights_boundary_is_recorded_precisely():
    use = {r["record_id"]: r for r in _provenance()}[RECORDS[1]]
    notes = use["notes"]
    for phrase in ("not a legal opinion or legal determination", "electronics_electrical:PR014",
                   "ONLY", "RIGHTS BASIS", "not subject to U.S. copyright protection",
                   "17 U.S.C. § 105", "acknowledgement / citation is required",
                   "third-party-authored protected material", "RESTRICTIONS APPLIED",
                   "NIST/SEMATECH publication hosted by NIST",
                   "NOT treated as evidence that the whole handbook is public domain",
                   "no blanket license is assumed", "passage-level",
                   "NIST-authored federal-government explanatory passages",
                   "MSA (Measurement Systems Analysis) manual content and any MSA-labelled text",
                   "SEMATECH-attributed or jointly authored material",
                   "proprietary standards and unattributed definitions",
                   "no source sentence, figure or table is reproduced",
                   "reviewed, approved, certified or endorses",
                   "does not extend to any other claim, passage or NIST resource"):
        assert phrase in notes, phrase


# ==========================================================================
# 6. No effect beyond the report / PDF presentation
# ==========================================================================
def test_x01_no_state_readiness_or_session_page_effect(client, monkeypatch):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((MECHANISM_COMPLETENESS, OPEN))
    state = _live(sid)
    before = pickle.dumps(state)
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    for lang in ("en", "ar"):
        report = _report(client, sid, lang=lang)
        assert _BLOCK_RE.search(report) is not None
    source = _pdf_source(client, sid, monkeypatch)
    assert _BLOCK_RE.search(source) is not None
    assert pickle.dumps(_live(sid)) == before
    readiness = derive_readiness(_live(sid))
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "measurement-accuracy-resolution-reference-v1" not in page


def test_x02_no_question_signal_calculation_or_safety_owner_changes():
    pack = _pack()
    mc = next(m for m in pack["gap_type_mappings"] if m["gap_type_id"] == MECHANISM_COMPLETENESS)
    assert [q["question_id"] for q in mc["questions"]] == [
        "electronics_electrical:MECHANISM_COMPLETENESS:Q%d" % n for n in (1, 2, 3, 4)]
    for path in ("engine/deterministic_calculation.py", "engine/domain_registry.py",
                 "engine/domain_rules.py", "engine/idea_state.py", "engine/readiness_snapshot.py",
                 "engine/safety_signal.py", "engine/read_export_service.py", "engine/record_store.py",
                 "engine/disclosure_export.py", "engine/derived_readiness.py", "engine/commercial_evidence.py",
                 "web/app.py", "web/templates/deliverable.html"):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        assert GROUP not in text and CLAIM not in text and "ACCURACY_RESOLUTION" not in text, path
