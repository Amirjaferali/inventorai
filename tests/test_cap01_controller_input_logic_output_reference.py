"""28-T2-CONTROLLER-INPUT-LOGIC-OUTPUT-REFERENCE-01 — ONE prose-only controller reference group.

For the exact Electronics MECHANISM_COMPLETENESS gap (OPEN or PARTIAL) the report /
deliverable and PDF show ONE further conceptual explanation — a microcontroller-based
design can receive inputs, process them using programmed logic and command outputs —
after the PR #789 sensing and PR #794 accuracy / resolution groups, through the existing
Electronics / CAP-01 owner and its ``CAP01_GAP_FUNDAMENTALS_EXTENSIONS`` seam (Option A:
one narrowly governed, presentation-only Electronics extension; not firmware ownership):

  * pack ``controller_input_logic_output_reference_v1`` (one claim, no relationship) and
    ONE bounded exception clause on the existing firmware exclusion of the coverage
    declaration — the exclusion itself stands;
  * provenance electronics_electrical:PR016 (nasa/fprime documentation at commit
    d32863dd63952d1085890cc69c1b25ea6edb2257, executor-inspected) and PR017 (Apache License
    2.0 with the repository NOTICE);
  * original EN wording of the admitted concept and its Arabic translation, separating the
    general capability from what the inventor's design actually does, with the Caltech /
    Apache-2.0 attribution, the NOTICE line, the adaptation / translation notice and the
    no-endorsement notice in the report and PDF.
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
from tests.cap01_controller_addition import (
    COVERAGE_EXCEPTION, CTRL_CLAIM as CLAIM, CTRL_GROUP as GROUP, CTRL_NOTE as NOTE, CTRL_RECORDS as RECORDS,
    CTRL_ROW, FIRMWARE_EXCLUSION, without_controller_addition)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")

DOMAIN = "electronics_electrical"
PREFIX = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_" + MECHANISM_COMPLETENESS + "_CONTROLLER_FUNDAMENTALS_"
COMMIT = "d32863dd63952d1085890cc69c1b25ea6edb2257"
REPO_URL = "https://github.com/nasa/fprime"
LICENSE_URL = "https://www.apache.org/licenses/LICENSE-2.0"
FILES = ("docs/getting-started/features.md", "docs/how-to/develop/develop-device-driver.md",
         "docs/user-manual/design-patterns/app-man-drv.md")
# Canonical digests at base d3bcbe1ef5197382686133a8319410d785740811 (before this slice).
_PRE_PACK_DIGEST = "763c7857fd96f37ce726ca6206f14ab05e26e47ea773cc2480b00c888cdb7c1a"
_PRE_PROVENANCE_DIGEST = "1ca084bfe5a5b5082d307c29ed6edcc82fb62a33fa1554dee1f08508da3421cd"

# The admitted concept, verbatim (the pack fact).
ADMITTED = ("A microcontroller-based design can receive inputs, process them using programmed logic and "
            "command outputs.")
# The reader-facing explanation: the admitted concept with source-supported examples, plus the
# distinction between a general capability and the inventor's design's actual behaviour.
EXPLANATION = {
    "en": ("A microcontroller-based design can receive inputs, such as sensor readings, process them using "
           "programmed logic, and command outputs, such as motors or other actuators. This describes a general "
           "capability; it does not show what your design's program does or that it works as intended."),
    "ar": ("يمكن للتصميم القائم على متحكم دقيق (microcontroller) أن يستقبل مدخلات، مثل قراءات المستشعرات، وأن "
           "يعالجها بمنطق مبرمج، وأن يصدر أوامر إلى مخرجات، مثل المحركات أو غيرها من المشغّلات. هذا وصف لقدرة "
           "عامة، ولا يبيّن ما يفعله برنامج تصميمك ولا أنه يعمل كما هو مقصود."),
}


def _iso(text):
    return "\u2066" + text + "\u2069"


PINNED = {
    "en": {
        "TITLE": "Microcontroller: inputs, programmed logic and outputs",
        "INTRO": "Reference information only. InventorAI has not determined that your design uses a microcontroller "
                 "or what its program does.",
        "ITEM_1_TITLE": "Inputs, programmed logic and outputs",
        "BOUNDARY": "This explanation does not describe your design's program, choose a microcontroller, check "
                    "hardware compatibility, set timing or behaviour, or establish that anything works or is safe.",
        "SOURCE": "Source: F´ (F Prime) flight software framework documentation, nasa/fprime repository, " + REPO_URL
                  + ", commit " + COMMIT + ": " + FILES[0] + ", " + FILES[1] + " and " + FILES[2] + ". © 2026 "
                  "California Institute of Technology (Caltech); U.S. Government sponsorship acknowledged. Licensed "
                  "under the Apache License, Version 2.0 (" + LICENSE_URL + "). Adapted: InventorAI explains this "
                  "point in its own words; the Arabic version is InventorAI's translation of that explanation. No "
                  "code, figure, diagram or third-party material is used. This does not imply that Caltech, the Jet "
                  "Propulsion Laboratory or NASA has reviewed, approved or endorsed InventorAI or this explanation.",
    },
    "ar": {
        "TITLE": "المتحكم الدقيق (microcontroller): المدخلات والمنطق المبرمج والمخرجات",
        "INTRO": "معلومات مرجعية فقط. لم يحدّد InventorAI أن تصميمك يستخدم متحكمًا دقيقًا، ولا ما يفعله برنامجه.",
        "ITEM_1_TITLE": "المدخلات والمنطق المبرمج والمخرجات",
        "BOUNDARY": "لا يصف هذا الشرح برنامج تصميمك، ولا يختار متحكمًا دقيقًا، ولا يتحقق من توافق المكونات، ولا "
                    "يحدد توقيتًا أو سلوكًا، ولا يثبت أن أي شيء يعمل أو أنه آمن.",
        "SOURCE": ("المصدر: وثائق إطار برمجيات الطيران " + _iso("F´ (F Prime)") + "، المستودع nasa/fprime على "
                   "الرابط: "
                   + _iso(REPO_URL) + "، الإيداع " + _iso(COMMIT) + "، الملفات: " + _iso(FILES[0]) + " و"
                   + _iso(FILES[1]) + " و" + _iso(FILES[2]) + ". حقوق النشر © 2026 لمعهد كاليفورنيا للتقنية "
                   "(Caltech)، مع الإقرار برعاية حكومة الولايات المتحدة، وهي مرخّصة بموجب الترخيص Apache "
                   "License, Version 2.0 المنشور على الرابط: " + _iso(LICENSE_URL) + ". مُقتبَس: شرح InventorAI "
                   "هذه النقطة بكلماته، والنص العربي ترجمة InventorAI لهذا الشرح. ولا تُستخدم أي شيفرة برمجية أو "
                   "شكل أو مخطط أو مواد لطرف ثالث. ولا يعني ذلك أن Caltech أو مختبر الدفع النفاث (JPL) أو NASA قد "
                   "راجع InventorAI أو هذا الشرح أو وافق عليه أو أيّده."),
    },
}

_BLOCK_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="controller-input-logic-output-reference-v1">'
    r'.*?\n      </div>', re.S)
_BLOCK_WITH_LEAD_RE = re.compile(r'\n\s*' + _BLOCK_RE.pattern, re.S)
_ANY_FUND_RE = re.compile(r'<div class="cap01-fundamentals" data-cap01-fundamentals="([^"]+)"')


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


# ==========================================================================
# 1. Binding: exact domain / gap / state; fixed order after the accuracy group
# ==========================================================================
@pytest.mark.parametrize("state", [OPEN, PARTIAL])
def test_b01_renders_for_the_exact_electronics_mechanism_gap_after_the_accuracy_group(state):
    groups = _groups((MECHANISM_COMPLETENESS, state))
    assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [SENSING_GROUP, ACCURACY_GROUP, GROUP]
    group = groups[MECHANISM_COMPLETENESS][2]
    assert group["prose_only"] is True
    assert [c["claim_id"] for c in group["claims"]] == [CLAIM]
    html = _html((MECHANISM_COMPLETENESS, state))
    assert _ANY_FUND_RE.findall(html) == ["sensing-value-threshold-reference-v1",
                                          "measurement-accuracy-resolution-reference-v1",
                                          "controller-input-logic-output-reference-v1"]
    assert len(_BLOCK_RE.findall(html)) == 1


@pytest.mark.parametrize("state", [CLOSED, ACCEPTED_RISK])
def test_b02_absent_when_the_gap_is_not_current(state):
    groups = _groups((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert MECHANISM_COMPLETENESS not in groups
    html = _html((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert _BLOCK_RE.search(html) is None and "controller-input-logic-output" not in html


def test_b03_absent_for_other_gaps_and_other_domains():
    groups = _groups((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, OPEN))
    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
        assert GROUP not in [g["group_id"] for g in groups.get(gap, ())]
    assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP]
    mech = _groups((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")
    assert all(GROUP not in [g["group_id"] for g in gs] for gs in (mech or {}).values())
    assert _BLOCK_RE.search(_html((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")) is None
    for domain in ("control_loop", "software", "medical_device", "Electronics_Electrical", ""):
        assert cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS.get((domain, MECHANISM_COMPLETENESS)) is None


def test_b04_the_binding_is_one_fixed_row_appended_last_to_the_mechanism_context():
    row = cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS[(DOMAIN, MECHANISM_COMPLETENESS)]
    assert [r[0] for r in row] == [SENSING_GROUP, ACCURACY_GROUP, GROUP]
    assert row[-1] == CTRL_ROW == (GROUP, (CLAIM,), "CONTROLLER_FUNDAMENTALS_")
    assert sorted(cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS) == [
        (DOMAIN, MECHANISM_COMPLETENESS), (DOMAIN, PHYSICAL_FEASIBILITY)]
    assert GROUP in cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS
    assert len(cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS) == 3


def test_b05_never_reads_inventor_text_or_signals():
    plain = _html((MECHANISM_COMPLETENESS, OPEN))
    mcu = _html((MECHANISM_COMPLETENESS, OPEN),
                idea_text="An Arduino ESP32 microcontroller with firmware, an RTOS, interrupts, a watchdog, "
                          "UART, I2C and SPI driving a servo from a sensor")
    assert _BLOCK_RE.search(plain).group(0) == _BLOCK_RE.search(mcu).group(0)


def test_b06_the_report_differs_from_the_base_rendering_by_exactly_this_block(monkeypatch):
    for pairs in (((MECHANISM_COMPLETENESS, OPEN),),
                  ((MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, OPEN)),
                  ((MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, OPEN))):
        with_row = _mask_csrf(_html(*pairs))
        table = dict(cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS)
        table[(DOMAIN, MECHANISM_COMPLETENESS)] = table[(DOMAIN, MECHANISM_COMPLETENESS)][:2]
        monkeypatch.setattr(cap01_guidance, "CAP01_GAP_FUNDAMENTALS_EXTENSIONS", table)
        without_row = _mask_csrf(_html(*pairs))
        monkeypatch.undo()
        removed, count = _BLOCK_WITH_LEAD_RE.subn("", with_row)
        assert removed == without_row
        assert count == (1 if pairs[0][1] in (OPEN, PARTIAL) else 0)


# ==========================================================================
# 2. Copy: admitted concept, original EN wording, AR rendering, attribution
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c01_explanation_and_pinned_strings_are_exact(lang):
    texts = _texts(lang)
    assert texts["ITEM_1_TEXT"] == EXPLANATION[lang]
    for part, value in PINNED[lang].items():
        assert texts[part] == value, part
    assert sorted(texts) == sorted(["TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "SOURCE", "BOUNDARY"])


def test_c02_the_pack_fact_is_the_admitted_concept_and_the_explanation_carries_it():
    [claim] = _group()["claims"]
    assert claim["fact"] == ADMITTED
    en = EXPLANATION["en"]
    for part in ("A microcontroller-based design can receive inputs", "process them using programmed logic",
                 "command outputs"):
        assert part in en, part


def test_c03_capability_is_separated_from_the_inventors_actual_design():
    en, ar = EXPLANATION["en"], EXPLANATION["ar"]
    assert "This describes a general capability" in en
    assert "it does not show what your design's program does or that it works as intended" in en
    assert "هذا وصف لقدرة عامة" in ar and "ولا يبيّن ما يفعله برنامج تصميمك ولا أنه يعمل كما هو مقصود" in ar
    assert en.startswith("A microcontroller-based design can ")
    assert ar.startswith("يمكن للتصميم القائم على متحكم دقيق (microcontroller)")


def test_c04_english_and_arabic_carry_the_same_statements():
    en, ar = EXPLANATION["en"], EXPLANATION["ar"]
    pairs = (("receive inputs", "يستقبل مدخلات"), ("sensor readings", "قراءات المستشعرات"),
             ("programmed logic", "بمنطق مبرمج"), ("command outputs", "يصدر أوامر إلى مخرجات"),
             ("motors or other actuators", "المحركات أو غيرها من المشغّلات"))
    for en_part, ar_part in pairs:
        assert en_part in en and ar_part in ar, (en_part, ar_part)
    assert len(re.findall(r"\.\s", en + " ")) == len(re.findall(r"\.\s", ar + " ")) == 2
    assert ar.count("(microcontroller)") == 1


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c05_no_out_of_scope_embedded_content(lang):
    """Operating states, startup / shutdown / fault handling, scheduling, interrupts, timing
    guarantees, firmware / code, controller selection and compatibility stay out of scope."""
    texts = _texts(lang)
    body = " ".join(texts[k] for k in ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT")).lower()
    if lang == "en":
        for banned in ("state", "transition", "startup", "start-up", "shutdown", "fault", "error", "watchdog",
                       "interrupt", "schedul", "real-time", "rtos", "bare-metal", "firmware", "code", "loop",
                       "setup", "pwm", "adc", "uart", "i2c", "spi", "arduino", "esp32", "stm32", "recommend",
                       "should", "must", "compatib", "safe"):
            assert banned not in body, banned
    else:
        for banned in ("حالة", "انتقال", "بدء التشغيل", "إيقاف", "عطل", "خطأ", "مقاطعة", "جدولة", "توقيت",
                       "البرنامج الثابت", "شيفرة", "يجب", "ننصح", "توافق", "آمن"):
            assert banned not in body, banned


def test_c06_digits_appear_only_in_the_source_citation():
    for lang in ("en", "ar"):
        for part, text in _texts(lang).items():
            if part == "SOURCE":
                continue
            assert not re.search(r"\d", text), (lang, part, text)


def test_c07_arabic_attribution_isolates_every_url_path_and_commit_left_to_right():
    source = _texts("ar")["SOURCE"]
    for token in ("F´ (F Prime)", REPO_URL, COMMIT, LICENSE_URL) + FILES:
        assert source.count(token) == 1, token
        assert _iso(token) in source, token
    assert source.count("\u2066") == source.count("\u2069") == 7
    assert "\u2066" not in _texts("en")["SOURCE"]


@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("pdf", [False, True])
def test_c08_rendered_block_carries_text_and_full_attribution_without_equation(lang, pdf):
    html = _html((MECHANISM_COMPLETENESS, OPEN), lang=lang, pdf=pdf)
    [block] = _BLOCK_RE.findall(html)
    visible = _visible(block)
    assert EXPLANATION[lang] in visible
    for needle in ("F´ (F Prime)", "nasa/fprime", REPO_URL, COMMIT, LICENSE_URL, "Apache License, Version 2.0",
                   "© 2026", "Caltech", "NASA") + FILES:
        assert needle in visible, needle
    if lang == "en":
        for needle in ("U.S. Government sponsorship acknowledged", "Adapted", "in its own words", "translation",
                       "does not imply that Caltech, the Jet Propulsion Laboratory or NASA"):
            assert needle in visible, needle
    else:
        for needle in ("مع الإقرار برعاية حكومة الولايات المتحدة", "مُقتبَس", "بكلماته", "ترجمة",
                       "ولا يعني ذلك أن Caltech أو مختبر الدفع النفاث (JPL) أو NASA"):
            assert needle in visible, needle
    assert _equations(block) == [] and "data-cap01-fund-equation" not in block
    assert "data-cap01-fund-item-lead" not in block and "data-cap01-fund-item-note" not in block
    assert block.count("data-cap01-fund-item-text") == 1
    assert 'style="overflow-wrap:anywhere"' in block
    for markup in ("<img", "<table", "<svg", "<figure", "<a ", "<code", "<pre", "<input", "<form", "<button"):
        assert markup not in block, markup


# ==========================================================================
# 3. Intellectual-property boundary
# ==========================================================================
def test_i01_no_code_figure_vendor_or_framework_specific_material():
    copy_text = " ".join(list(_texts("en").values()) + list(_texts("ar").values()))
    pack_text = json.dumps(_group(), ensure_ascii=False)
    for text in (copy_text.replace("F´ (F Prime) flight software framework documentation", "").replace(
            "nasa/fprime", ""), pack_text):
        lowered = text.lower()
        for banned in ("mpu6050", "adafruit", "arduino", "stm32", "linux", "littlefs", "fatfs", "googletest",
                       "eric young", "fpp", "c++", "mermaid", ".png", ".svg", "topology", "rate group",
                       "port ", "component base", "application layer", "manager layer", "driver layer",
                       "health check", "state machine", "isr", "fw_assert"):
            assert banned not in lowered, banned


def test_i02_no_source_sentence_is_reproduced():
    text = " ".join(list(_texts("en").values()) + [_group()["claims"][0]["fact"]]).lower()
    # short fragments of the F´ documentation wording, used here only as negative checks
    for fragment in ("represents system logic", "uses peripherals", "obtain sensor data", "wide range of processors",
                     "from microcontrollers to multi-core", "dedicated to a particular hardware interface",
                     "perform the detailed behaviors"):
        assert fragment not in text, fragment


def test_i03_attribution_states_no_endorsement_and_identifies_the_adaptation():
    en, ar = _texts("en"), _texts("ar")
    assert en["SOURCE"].endswith("This does not imply that Caltech, the Jet Propulsion Laboratory or NASA has "
                                 "reviewed, approved or endorsed InventorAI or this explanation.")
    assert ar["SOURCE"].endswith("ولا يعني ذلك أن Caltech أو مختبر الدفع النفاث (JPL) أو NASA قد راجع InventorAI أو "
                                 "هذا الشرح أو وافق عليه أو أيّده.")
    joined = " ".join(en.values()).lower()
    for banned in ("endorsed by", "approved by", "certified by", "recommended by", "according to nasa",
                   "nasa recommends", "jpl recommends", "logo", "public domain"):
        assert banned not in joined, banned
    for lang_texts in (en, ar):
        for part, text in lang_texts.items():
            if "Caltech" in text or "NASA" in text or "Apache" in text:
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
        assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [SENSING_GROUP, ACCURACY_GROUP], part
        assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP]
        monkeypatch.undo()


def test_f02_an_equation_key_never_substitutes_the_prose_text(monkeypatch):
    strings = dict(ui_text.UI_STRINGS)
    strings.pop(PREFIX + "ITEM_1_TEXT")
    strings[PREFIX + "ITEM_1_EQUATION"] = {"en": "x", "ar": "x"}
    monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
    groups = _groups((MECHANISM_COMPLETENESS, OPEN))
    assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [SENSING_GROUP, ACCURACY_GROUP]


def test_f03_existing_groups_keep_requiring_their_equation(monkeypatch):
    key = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_EQUATION"
    strings = dict(ui_text.UI_STRINGS)
    strings.pop(key)
    monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
    assert [g["group_id"] for g in _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]] == [ET_GROUP]
    monkeypatch.undo()
    for group in _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]:
        assert group["prose_only"] is False


# ==========================================================================
# 5. Pack / coverage / provenance: addition only, claim mapping, rights boundary
# ==========================================================================
def test_p01_pack_minus_exactly_this_addition_equals_the_base_pack():
    pack = _pack()
    assert [g["group_id"] for g in pack["reference_fundamentals"]] == [
        BASE_GROUP, ET_GROUP, SENSING_GROUP, ACCURACY_GROUP, GROUP]
    assert _digest(without_controller_addition(pack)) == _PRE_PACK_DIGEST
    note = pack["_governance_notes"][NOTE]
    for phrase in ("28-T2-CONTROLLER-INPUT-LOGIC-OUTPUT-REFERENCE-01", "Option A", "NOT general firmware ownership",
                   "PR016", "PR017", "inert", "the exclusion itself stands", "PR001–PR015 are unchanged",
                   "after measurement_accuracy_resolution_reference_v1"):
        assert phrase in note, phrase


def test_p02_the_coverage_exception_is_one_bounded_clause_on_the_existing_exclusion():
    cov = _pack()["coverage_declaration"]
    with_clause = [a for a in cov["not_covered_areas"] if COVERAGE_EXCEPTION in a]
    assert with_clause == [FIRMWARE_EXCLUSION + COVERAGE_EXCEPTION]
    assert "no other firmware or embedded software guidance is covered" in COVERAGE_EXCEPTION
    joined_covered = " ".join(cov["covered_areas"]).lower()
    assert "firmware" not in joined_covered and "microcontroller" not in joined_covered
    assert len(cov["covered_areas"]) == 4                       # next-step anchors cite these by index


def test_p03_the_group_is_one_prose_only_claim_with_its_records():
    group = _group()
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["applicable_gap_type"] == MECHANISM_COMPLETENESS
    [claim] = group["claims"]
    assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation", "source_ref",
                             "source_use_policy_ref"]
    assert (claim["claim_id"], claim["applicable_gap_type"]) == (CLAIM, MECHANISM_COMPLETENESS)
    assert (claim["source_ref"], claim["source_use_policy_ref"]) == RECORDS
    for phrase in ("No firmware, code or program structure", "no operating states or transitions",
                   "no startup, shutdown or fault handling", "no scheduling, interrupt or timing statement",
                   "no controller or hardware selection", "never infers it from inventor text",
                   "The broader firmware and embedded software exclusion of the coverage declaration stands"):
        assert phrase in claim["limitation"], phrase


def test_p04_provenance_is_append_only_with_two_claim_specific_records():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids))
    i = ids.index("electronics_electrical:PR015")
    assert tuple(ids[i + 1:i + 3]) == RECORDS
    pre = [r for r in records if r["record_id"] not in RECORDS]
    assert _digest(pre) == _PRE_PROVENANCE_DIGEST                     # PR001–PR015 and others unchanged
    src, use = (records[ids.index(r)] for r in RECORDS)
    assert sorted(src) == sorted(use) == sorted(records[i])
    assert (src["source_type"], src["tier"]) == ("openly_licensed_technical_documentation", 1)
    assert (use["source_type"], use["tier"]) == ("source_use_policy", 1)
    assert src["url"] == REPO_URL + "/tree/" + COMMIT + "/docs" and use["url"] == LICENSE_URL
    for f in FILES:
        assert f in src["version_or_edition"], f
    assert COMMIT in src["version_or_edition"] and COMMIT in use["version_or_edition"]
    assert "inspected directly by the executor" in src["version_or_edition"]
    assert "inspected directly by the executor" in use["version_or_edition"]
    assert src["cross_domain_usage"] == use["cross_domain_usage"] == []


def test_p05_claim_mapping_and_exclusions_are_recorded():
    notes = {r["record_id"]: r for r in _provenance()}[RECORDS[0]]["notes"]
    for phrase in ("CLAIM MAPPING", "features.md line 22", "develop-device-driver.md lines 3 and 28–30",
                   "\"Application Component\"", "\"Driver Component\"", "EXCLUDED and not used, quoted or paraphrased",
                   "Mermaid diagram", "third-party MPU6050 / Adafruit datasheet", "googletest",
                   "F´-specific architecture", "device-driver state machine", "health checking",
                   "it presents a possibility, not a prescribed structure", "electronics_electrical:PR017"):
        assert phrase in notes, phrase


def test_p06_rights_boundary_is_recorded_precisely():
    notes = {r["record_id"]: r for r in _provenance()}[RECORDS[1]]["notes"]
    for phrase in ("not a legal opinion or legal determination", "electronics_electrical:PR016", "ONLY",
                   "Apache License 2.0", "California Institute of Technology (Caltech)",
                   "U.S. Government sponsorship acknowledged", "CONTRIBUTING.md lines 110–111",
                   "NOT treated as a U.S. Government work or as public domain",
                   "is not treated as proof of rights for every item",
                   "CONDITIONS APPLIED although the use is an original paraphrase", "(4a)", "(4b)", "(4c/4d)", "(6)",
                   "cryptographic software does not pertain", "no-endorsement condition is honored",
                   "does not extend to any other claim, file or passage"):
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
        assert _BLOCK_RE.search(_report(client, sid, lang=lang)) is not None
    assert _BLOCK_RE.search(_pdf_source(client, sid, monkeypatch)) is not None
    assert pickle.dumps(_live(sid)) == before
    readiness = derive_readiness(_live(sid))
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "controller-input-logic-output-reference-v1" not in page


def test_x02_no_question_signal_calculation_safety_or_persistence_owner_changes():
    pack = _pack()
    mc = next(m for m in pack["gap_type_mappings"] if m["gap_type_id"] == MECHANISM_COMPLETENESS)
    assert [q["question_id"] for q in mc["questions"]] == [
        "electronics_electrical:MECHANISM_COMPLETENESS:Q%d" % n for n in (1, 2, 3, 4)]
    signals = {s["signal"] for s in pack["classification_signals"]} | {s["signal"] for s in pack["substance_signals"]}
    assert not {"firmware", "rtos", "interrupt", "embedded"} & signals
    for path in ("engine/deterministic_calculation.py", "engine/domain_registry.py", "engine/domain_rules.py",
                 "engine/domain_activation.py", "engine/subsystem_model.py", "engine/idea_state.py",
                 "engine/readiness_snapshot.py", "engine/safety_signal.py", "engine/read_export_service.py",
                 "engine/record_store.py", "engine/disclosure_export.py", "engine/derived_readiness.py",
                 "web/app.py", "web/templates/deliverable.html"):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        assert GROUP not in text and CLAIM not in text and "CONTROLLER_FUNDAMENTALS" not in text, path
