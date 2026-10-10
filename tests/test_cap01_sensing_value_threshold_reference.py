"""28-T1-SENSING-VALUE-THRESHOLD-01 — ONE prose-only sensing reference group.

For the exact Electronics MECHANISM_COMPLETENESS gap (OPEN or PARTIAL) the report /
deliverable and PDF show ONE conceptual explanation — reporting a sensed quantity's
value versus indicating whether it is above a threshold — through the existing
Electronics / CAP-01 owner and its ``CAP01_GAP_FUNDAMENTALS_EXTENSIONS`` seam:

  * pack ``sensing_value_threshold_reference_v1`` (one claim, no relationship);
  * provenance electronics_electrical:PR012 (Kuphaldt, Sensors Overview, ModEL,
    section 2.1, pp. 12–13; Lead-supplied inspection) and PR013 (CC BY 4.0);
  * the Lead-approved EN / AR wording verbatim, with the CC BY 4.0 attribution,
    license link and adaptation / translation notice in the report and PDF;
  * equation omission is allowed for THIS group only — every other group still
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

import web.app as appmod
from engine.deliverable_assembler import assemble_deliverable
from engine.derived_readiness import derive_readiness
from engine.idea_state import (
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, MECHANISM_COMPLETENESS, OPEN, PARTIAL,
    PHYSICAL_FEASIBILITY)
from web import cap01_guidance, ui_text
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, ELEC_SEED, _start, _live,
)
from tests.test_cap01_mechanical_open_gap_context import _gaps, _pdf_source, _report, _visible
from tests.test_cap01_electrical_energy_time_reference import (
    ET_GROUP, _html, _groups, _equations)
from tests.test_cap01_electrical_reference_fundamentals import FUND_GROUP as BASE_GROUP

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")

DOMAIN = "electronics_electrical"
GROUP = "sensing_value_threshold_reference_v1"
CLAIM = "sensed_value_versus_threshold_indication"
PREFIX = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_" + MECHANISM_COMPLETENESS + "_SENSING_FUNDAMENTALS_"
RECORDS = ("electronics_electrical:PR012", "electronics_electrical:PR013")
SOURCE_URL = "https://ibiblio.org/kuphaldt/socratic/model/mod_sensors.pdf"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/legalcode.en"
# Canonical digests at base 46ef7f4c2a6a29156a6a95a2c1da67f29e49007b (before this slice).
_PRE_PACK_DIGEST = "eb4ab6ffafb61dcac3c17ba9647f5bc43efd3440e31c521421bbcb376107b93a"
_PRE_PROVENANCE_DIGEST = "0ec356a2199ebe5cb2564a4c723c23875da0f29e753fe041c65a85b3a6650787"

APPROVED = {
    "en": ("If your design senses a physical quantity, reporting its value and indicating whether it "
           "is above a threshold provide different information. For example, a rotational-speed "
           "reading gives a speed value; an above-threshold indication alone does not."),
    "ar": ("إذا كان تصميمك يستشعر كمية فيزيائية، فإن بيان قيمتها والإشارة إلى كونها أعلى من حدّ معين "
           "يقدّمان معلومات مختلفة. مثلًا، قراءة سرعة الدوران تعطي قيمة للسرعة؛ أما إشارة تجاوز الحد "
           "وحدها فلا تعطي تلك القيمة."),
}
# Executor-authored strings around the approved text, pinned exactly.
PINNED = {
    "en": {
        "TITLE": "Sensing: a value or an above-threshold indication",
        "INTRO": "Reference information only. InventorAI has not determined that your design senses a "
                 "quantity or uses a threshold.",
        "ITEM_1_TITLE": "Value versus above-threshold indication",
        "BOUNDARY": "This explanation does not select a sensor or a threshold, set any value, calibrate "
                    "anything, or establish accuracy, performance or safety.",
        "SOURCE": "Source: Tony R. Kuphaldt, “Sensors Overview”, Modular Electronics Learning (ModEL) "
                  "project, text version of 23 October 2025, section 2.1 “Signals, sensors, and "
                  "switches”, pp. 12–13, © 2017–2025 Tony R. Kuphaldt, " + SOURCE_URL + " — licensed "
                  "under CC BY 4.0 (" + LICENSE_URL + "). Adapted: InventorAI paraphrased this "
                  "explanation; the Arabic version is InventorAI's translation of that adaptation. No "
                  "endorsement by the author is implied. See the license for its terms, including its "
                  "disclaimer of warranties.",
    },
    "ar": {
        "TITLE": "الاستشعار: قيمة أم إشارة تجاوز حدّ",
        "INTRO": "معلومات مرجعية فقط. لم يحدّد InventorAI أن تصميمك يستشعر كمية ما أو يستخدم حدًّا معينًا.",
        "ITEM_1_TITLE": "القيمة مقابل إشارة تجاوز الحدّ",
        "BOUNDARY": "لا يختار هذا الشرح مستشعرًا أو حدًّا، ولا يحدّد أي قيمة، ولا يُجري أي معايرة، ولا "
                    "يثبت الدقة أو الأداء أو السلامة.",
        "SOURCE": ("المصدر: الوثيقة التعليمية Sensors Overview من إعداد Tony R. Kuphaldt ضمن مشروع "
                   "Modular Electronics Learning المعروف اختصارًا بـ ModEL، نسخة النص المؤرخة 23 أكتوبر "
                   "2025، القسم 2.1 بعنوان Signals, sensors, and switches، الصفحتان 12–13. حقوق النشر "
                   "© 2017–2025 للمؤلف Tony R. Kuphaldt. رابط الوثيقة: \u2066" + SOURCE_URL + "\u2069، وهي مرخّصة "
                   "بموجب الترخيص CC BY 4.0 المنشور نصه القانوني على الرابط: \u2066" + LICENSE_URL + "\u2069، مع "
                   "إشعار الاقتباس التالي. مُقتبَس: صاغ InventorAI هذا الشرح بكلماته، والنص العربي ترجمة "
                   "InventorAI لهذه الصياغة. ولا يُقصد أي إيحاء بتأييد المؤلف. راجع الترخيص لمعرفة "
                   "شروطه، بما فيها إخلاء المسؤولية عن الضمانات."),
    },
}

_SENSE_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="sensing-value-threshold-reference-v1">'
    r'.*?\n      </div>', re.S)
_MC_RE = re.compile(
    r'<div class="cap01-gap-context" data-cap01-gap="mechanism-completeness".*?'
    r'(?=<div class="cap01-gap-context"|<div class="cap01-next-steps")', re.S)


def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _pack():
    with io.open(_PACK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _provenance():
    with io.open(_PROVENANCE_PATH, encoding="utf-8") as fh:
        return json.load(fh)["records"]


def _texts(lang):
    return {k[len(PREFIX):]: ui_text.UI_STRINGS[k][lang]
            for k in sorted(ui_text.UI_STRINGS) if k.startswith(PREFIX)}


# ==========================================================================
# 1. Binding: exact domain / gap / state
# ==========================================================================
@pytest.mark.parametrize("state", [OPEN, PARTIAL])
def test_s01_renders_for_the_exact_electronics_mechanism_gap_open_or_partial(state):
    groups = _groups((MECHANISM_COMPLETENESS, state))
    assert [g["group_id"] for g in groups[MECHANISM_COMPLETENESS]] == [GROUP]
    [group] = groups[MECHANISM_COMPLETENESS]
    assert group["prose_only"] is True
    assert [c["claim_id"] for c in group["claims"]] == [CLAIM]


@pytest.mark.parametrize("state", [CLOSED, ACCEPTED_RISK])
def test_s02_absent_when_the_gap_is_not_current(state):
    groups = _groups((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert MECHANISM_COMPLETENESS not in groups
    html = _html((MECHANISM_COMPLETENESS, state), (PHYSICAL_FEASIBILITY, OPEN))
    assert _SENSE_RE.search(html) is None


def test_s03_absent_for_other_gaps_and_other_domains():
    groups = _groups((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, OPEN))
    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
        assert GROUP not in [g["group_id"] for g in groups.get(gap, ())]
    assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP]
    mech = _groups((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")
    assert all(GROUP not in [g["group_id"] for g in gs] for gs in (mech or {}).values())
    assert _SENSE_RE.search(_html((MECHANISM_COMPLETENESS, OPEN), domain="mechanical")) is None
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS.get((DOMAIN, MECHANISM_COMPLETENESS)) is None


def test_s04_the_extension_table_holds_exactly_the_two_fixed_rows():
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS == {
        (DOMAIN, PHYSICAL_FEASIBILITY): (
            (ET_GROUP, ("constant_power_energy_reference", "energy_time_unit_discipline"),
             "ENERGY_TIME_FUNDAMENTALS_"),),
        (DOMAIN, MECHANISM_COMPLETENESS): ((GROUP, (CLAIM,), "SENSING_FUNDAMENTALS_"),),
    }
    assert cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS == frozenset({GROUP})


def test_s05_never_reads_inventor_text_or_signals():
    plain = _html((MECHANISM_COMPLETENESS, OPEN))
    sensing = _html((MECHANISM_COMPLETENESS, OPEN),
                    idea_text="A tachometer sensor with a threshold comparator and speed switch")
    assert _SENSE_RE.search(plain).group(0) == _SENSE_RE.search(sensing).group(0)


# ==========================================================================
# 2. Copy: approved EN / AR, attribution, pinned strings
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_c01_approved_text_and_pinned_strings_are_exact(lang):
    texts = _texts(lang)
    assert texts["ITEM_1_TEXT"] == APPROVED[lang]
    for part, value in PINNED[lang].items():
        assert texts[part] == value, part
    assert sorted(texts) == sorted(["TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "SOURCE",
                                    "BOUNDARY"])


@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("pdf", [False, True])
def test_c02_rendered_block_carries_text_and_full_attribution_without_equation(lang, pdf):
    html = _html((MECHANISM_COMPLETENESS, OPEN), lang=lang, pdf=pdf)
    [block] = _SENSE_RE.findall(html)
    visible = _visible(block)
    assert APPROVED[lang] in visible
    for needle in ("Tony R. Kuphaldt", "© 2017–2025", "CC BY 4.0", SOURCE_URL, LICENSE_URL):
        assert needle in visible, needle
    assert ("Adapted" in visible) if lang == "en" else ("مُقتبَس" in visible)
    assert _equations(block) == [] and "data-cap01-fund-equation" not in block
    assert "data-cap01-fund-item-lead" not in block and "data-cap01-fund-item-note" not in block
    assert block.count("data-cap01-fund-item-text") == 1
    assert 'style="overflow-wrap:anywhere"' in block


def test_c03_text_presents_a_state_not_a_crossing_detector():
    for lang in ("en", "ar"):
        text = APPROVED[lang]
        for banned in ("cross", "crossing", "event", "detect", "اجتياز", "حدث"):
            assert banned not in text, (lang, banned)
    claim = _pack()["reference_fundamentals"][2]["claims"][0]
    assert "not a temporal crossing or event detector" in claim["fact"]


# ==========================================================================
# 3. Fail closed; prose-only is not a global relaxation
# ==========================================================================
def test_f01_missing_required_prose_copy_removes_only_this_group(monkeypatch):
    for part in ("ITEM_1_TEXT", "ITEM_1_TITLE", "SOURCE", "BOUNDARY", "INTRO", "TITLE"):
        strings = dict(ui_text.UI_STRINGS)
        strings.pop(PREFIX + part)
        monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
        groups = _groups((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, OPEN))
        assert MECHANISM_COMPLETENESS in groups and groups[MECHANISM_COMPLETENESS] == (), part
        assert [g["group_id"] for g in groups[PHYSICAL_FEASIBILITY]] == [BASE_GROUP, ET_GROUP]
        monkeypatch.undo()


def test_f02_existing_groups_still_require_their_equation(monkeypatch):
    for key in ("UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_EQUATION",
                "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_ENERGY_TIME_FUNDAMENTALS_ITEM_1_EQUATION"):
        strings = dict(ui_text.UI_STRINGS)
        strings.pop(key)
        monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
        groups = [g["group_id"] for g in _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]]
        assert len(groups) == 1 and groups[0] in (BASE_GROUP, ET_GROUP)
        monkeypatch.undo()
    for group in _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]:
        assert group["prose_only"] is False
        assert all("equation_key" in c and "text_key" not in c for c in group["claims"])


def test_f03_a_text_key_never_substitutes_an_equation_elsewhere(monkeypatch):
    strings = dict(ui_text.UI_STRINGS)
    eq = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_ENERGY_TIME_FUNDAMENTALS_ITEM_1_EQUATION"
    strings.pop(eq)
    strings[eq.replace("EQUATION", "TEXT")] = {"en": "x", "ar": "x"}
    monkeypatch.setattr(ui_text, "UI_STRINGS", strings)
    groups = [g["group_id"] for g in _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]]
    assert groups == [BASE_GROUP]


# ==========================================================================
# 4. Pack / provenance: addition only, claim mapping, source-use basis
# ==========================================================================
def test_p01_pack_minus_exactly_this_addition_equals_the_base_pack():
    pack = _pack()
    assert [g["group_id"] for g in pack["reference_fundamentals"]] == [BASE_GROUP, ET_GROUP, GROUP]
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre["reference_fundamentals"] if g["group_id"] != GROUP]
    note = pre["_governance_notes"].pop("sensing_value_threshold_reference")
    assert _digest(pre) == _PRE_PACK_DIGEST
    assert "28-T1-SENSING-VALUE-THRESHOLD-01" in note and "PR012" in note and "PR013" in note


def test_p02_the_group_is_one_prose_only_claim_with_its_records():
    group = _pack()["reference_fundamentals"][2]
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["applicable_gap_type"] == MECHANISM_COMPLETENESS
    [claim] = group["claims"]
    assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation", "source_ref",
                             "source_use_policy_ref"]
    assert "relationship" not in claim
    assert (claim["claim_id"], claim["applicable_gap_type"]) == (CLAIM, MECHANISM_COMPLETENESS)
    assert (claim["source_ref"], claim["source_use_policy_ref"]) == RECORDS
    for phrase in ("No sensor or threshold selection", "calibration", "safety", "CAP-09"):
        assert phrase in claim["limitation"], phrase


def test_p03_provenance_is_append_only_with_two_claim_specific_records():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids))
    i = ids.index("electronics_electrical:PR011")
    assert tuple(ids[i + 1:i + 3]) == RECORDS
    pre = [r for r in records if r["record_id"] not in RECORDS]
    assert _digest(pre) == _PRE_PROVENANCE_DIGEST
    src, use = (records[ids.index(r)] for r in RECORDS)
    assert src["url"] == SOURCE_URL and use["url"] == LICENSE_URL
    assert "23 October 2025" in src["version_or_edition"] and "pp." not in src["url"]
    assert "printed pages 12–13" in src["version_or_edition"]
    assert "Section 2.1" in src["version_or_edition"]
    for rec in (src, use):
        assert "Lead-supplied inspection" in rec["version_or_edition"]
        assert "not independently re-inspected by the executor" in rec["version_or_edition"]
    assert "page 12" in src["notes"] and "page 13" in src["notes"]
    assert "electronics_electrical:PR013" in src["notes"]
    assert "electronics_electrical:PR012" in use["notes"] and "ONLY" in use["notes"]
    assert "does not extend to any other claim" in use["notes"]


# ==========================================================================
# 5. No effect beyond the report / PDF presentation
# ==========================================================================
def test_x01_no_state_readiness_or_session_page_effect(client, monkeypatch):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((MECHANISM_COMPLETENESS, OPEN))
    state = _live(sid)
    before = pickle.dumps(state)
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    report = _report(client, sid)
    assert _SENSE_RE.search(report) is not None
    source = _pdf_source(client, sid, monkeypatch)
    assert _SENSE_RE.search(source) is not None
    assert pickle.dumps(_live(sid)) == before
    readiness = derive_readiness(_live(sid))
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "sensing-value-threshold-reference-v1" not in page


def test_x02_no_question_signal_or_calculation_owner_changes():
    pack = _pack()
    mc = next(m for m in pack["gap_type_mappings"] if m["gap_type_id"] == MECHANISM_COMPLETENESS)
    assert [q["question_id"] for q in mc["questions"]] == [
        "electronics_electrical:MECHANISM_COMPLETENESS:Q%d" % n for n in (1, 2, 3, 4)]
    for path in ("engine/deterministic_calculation.py", "engine/domain_registry.py",
                 "engine/domain_rules.py", "engine/idea_state.py", "engine/readiness_snapshot.py",
                 "engine/safety_signal.py", "engine/read_export_service.py"):
        text = open(os.path.join(_ROOT, path), encoding="utf-8").read()
        assert GROUP not in text and CLAIM not in text, path
