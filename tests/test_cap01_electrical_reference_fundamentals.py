# -*- coding: utf-8 -*-
"""ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1 — BASIC ELECTRICAL REFERENCE
FUNDAMENTALS (Owner-authorized bounded Stage-18 / CAP-01 slice).

What is pinned: when, and only when, the trusted canonical domain is
``electronics_electrical`` AND the EXACT canonical ``PHYSICAL_FEASIBILITY`` gap is in
EXACT state OPEN or PARTIAL, the report / deliverable and the PDF show ONE short
gap-scoped explanatory context plus ONE optional sub-view of exactly three bounded,
source-backed reference fundamentals: V = I × R (Ohm's-law / resistive reference),
P = V × I (basic power reference) and the SI unit discipline V / A / Ω / W.

Why a separate test file: the domain-level Electronics checklist / research profile
(CAP01_ELECTRONICS_INTERFACE_V1) keeps its own owner in
``tests/test_stage18_cap01_bounded_guidance.py``; this gap-scoped context reuses the
Mechanical gap-context seam, whose own guards live in
``tests/test_cap01_mechanical_open_gap_context.py``. Folding this Electronics
gap-scoped layer into either file would couple two separately authorized owners, so
it is proven here, reusing their harness.

Boundaries proven here: exact binding (domain + gap id + lifecycle state only);
no other Electronics gap, no Mechanical gap, no label / text / signal can trigger
it; the Electronics checklist profile and the Mechanical fundamentals are unchanged;
the pack group is inert; provenance electronics_electrical:PR004–PR007 are exact and
PR001–PR003 unchanged; EN / AR meaning-equivalent with LTR-isolated equations; no
calculation, no applicability claim, no source prose / logo / endorsement.
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
from engine.gap_action_pack import derive_gap_action_packs
from engine.idea_state import (
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, IdeaState, MECHANISM_COMPLETENESS, OPEN,
    PARTIAL, PHYSICAL_FEASIBILITY)
from engine.path_n_questions import get_served_question
from web import cap01_guidance, ui_text
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, ELEC_SEED, _start, _live,
)
from tests.test_stage18_cap01_bounded_guidance import (
    ELECTRONICS_IDEA, OPEN_GAP_INPUT, PROFILE_ID, _mask_csrf, _state as _s18_state)
from tests.test_cap01_mechanical_open_gap_context import (
    FUND_CLAIMS as MECH_FUND_CLAIMS, FUND_EQUATIONS as MECH_FUND_EQUATIONS,
    FUND_GROUP as MECH_FUND_GROUP, _executable, _gaps, _pdf_source, _render, _report,
    _visible, _AR_NEGATORS)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")
_GUIDANCE_PATH = os.path.join(_ROOT, "web", "cap01_guidance.py")

DOMAIN = "electronics_electrical"
GROUP_ID = "CAP01_ELECTRONICS_GAP_CONTEXT_V1"
PREFIX = "UI_%s_" % GROUP_ID
FUND_PREFIX = PREFIX + PHYSICAL_FEASIBILITY + "_FUNDAMENTALS_"
FUND_GROUP = "basic_electrical_reference_v1"
FUND_CLAIMS = ("ohms_law_reference", "electrical_power_vi_reference",
               "si_electrical_unit_discipline")
FUND_EQUATIONS = ("V = I × R", "P = V × I", "V, A, Ω, W")
CLAIM_SOURCES = {
    "ohms_law_reference": ("electronics_electrical:PR004", "electronics_electrical:PR006"),
    "electrical_power_vi_reference": ("electronics_electrical:PR004", "electronics_electrical:PR006"),
    "si_electrical_unit_discipline": ("electronics_electrical:PR005", "electronics_electrical:PR007"),
}
NEW_RECORDS = ("electronics_electrical:PR004", "electronics_electrical:PR005",
               "electronics_electrical:PR006", "electronics_electrical:PR007")
# Canonical digests of data that existed BEFORE this slice (computed at base
# e4a36cce7dd9127b457e19b163d7bfd36430659e): PR001–PR003 as a sorted-key list, and
# the whole Electronics pack minus the two additions of this slice.
_PR001_PR003_DIGEST = "6bf7d1c1d43130441236f1dd6cb3204276ee154feafc86eabcf51c1b4cdcb96d"
_PRE_SLICE_PACK_DIGEST = "0d5c3d191aee3f069236e1a1a54d6e789bb396a5644a1e1405d5a45f0ac3f1d6"


# ==========================================================================
# harness
# ==========================================================================
def _pack():
    with io.open(_PACK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _provenance():
    with io.open(_PROVENANCE_PATH, encoding="utf-8") as fh:
        return {r["record_id"]: r for r in json.load(fh)["records"]}


def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _elec_state(*pairs, idea_text=None):
    s = IdeaState(idea_id="cap01-elec-probe")
    s.domain = DOMAIN
    s.domain_signal = DOMAIN
    s.gaps = _gaps(*pairs)
    if idea_text is not None:
        s.idea_text = idea_text
    return s


def _resolve(*pairs, domain=DOMAIN):
    return cap01_guidance.gap_contexts_for_gaps(domain, _gaps(*pairs))


def _fund(*pairs, domain=DOMAIN):
    view = _resolve(*pairs, domain=domain)
    if view is None:
        return None
    return view["contexts"][0]["fundamentals"]


def _render_state(*pairs, lang="en", pdf=False, idea_text=None):
    state = _elec_state(*pairs, idea_text=idea_text)
    return _render(assemble_deliverable(state), state, lang=lang, pdf=pdf)


_FUND_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="basic-electrical-reference-v1">'
    r'.*?\n      </div>', re.S)
_ANY_FUND_RE = re.compile(r'<div class="cap01-fundamentals"', re.S)


def _blocks(html):
    return _FUND_RE.findall(html)


def _equations(block):
    return re.findall(
        r'<bdi class="cap01-fund-equation" dir="ltr" data-cap01-fund-equation>(.*?)</bdi>', block)


def _texts(lang):
    """Every reader-visible string of this slice in ONE language (context + sub-view)."""
    # ELECTRICAL-ENERGY-TIME-REFERENCE-01 owns its own separately namespaced group
    # (tests/test_cap01_electrical_energy_time_reference.py); this slice's strings
    # are everything else under the context prefix, unchanged.
    # 28-T1-SENSING-VALUE-THRESHOLD-01 likewise owns its own namespace under the
    # MECHANISM_COMPLETENESS context (tests/test_cap01_sensing_value_threshold_reference.py).
    return {k[len(PREFIX):]: ui_text.UI_STRINGS[k][lang]
            for k in sorted(ui_text.UI_STRINGS) if k.startswith(PREFIX)
            and not k.startswith(PREFIX + PHYSICAL_FEASIBILITY + "_ENERGY_TIME_FUNDAMENTALS_")
            and not k.startswith(PREFIX + MECHANISM_COMPLETENESS + "_SENSING_FUNDAMENTALS_")}


# 28-T1-SENSING-VALUE-THRESHOLD-01: the ONE separately bound prose-only group of the
# MECHANISM_COMPLETENESS context. The absence checks below concern the
# PHYSICAL_FEASIBILITY reference fundamentals; that group is excluded from them.
_SENSING_FUND_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="sensing-value-threshold-reference-v1">'
    r'.*?\n      </div>', re.S)


def _without_sensing(html):
    return _SENSING_FUND_RE.sub("", html)


def _fund_texts(lang):
    return {k[len(FUND_PREFIX):]: ui_text.UI_STRINGS[k][lang]
            for k in sorted(ui_text.UI_STRINGS) if k.startswith(FUND_PREFIX)}


def _set_gaps(sid, *pairs):
    _live(sid).gaps = _gaps(*pairs)


def _sentences(text):
    return [s for s in re.split(r"(?<=[.؛:])\s+", text) if s.strip()]


# ==========================================================================
# E1. exact binding
# ==========================================================================
@pytest.mark.parametrize("status", (OPEN, PARTIAL))
def test_e01_pf_open_or_partial_renders_the_context_and_fundamentals_exactly_once(status):
    view = _resolve((PHYSICAL_FEASIBILITY, status))
    assert view["group_id"] == GROUP_ID
    assert [(c["gap_type"], c["gap_state"]) for c in view["contexts"]] == [(PHYSICAL_FEASIBILITY, status)]
    fund = view["contexts"][0]["fundamentals"]
    assert fund["group_id"] == FUND_GROUP
    assert tuple(c["claim_id"] for c in fund["claims"]) == FUND_CLAIMS
    html = _render_state((PHYSICAL_FEASIBILITY, status))
    # This slice's group renders exactly once and FIRST; the one later, separately
    # authorized group (ELECTRICAL-ENERGY-TIME-REFERENCE-01) follows it.
    assert len(_blocks(html)) == 1 and len(_ANY_FUND_RE.findall(html)) == 2
    assert html.index('data-cap01-fundamentals="basic-electrical-reference-v1"') < \
        html.index('data-cap01-fundamentals="electrical-energy-time-reference-v1"')
    assert html.count('data-cap01-gap-group="%s"' % GROUP_ID) == 1


@pytest.mark.parametrize("status", (CLOSED, ACCEPTED_RISK, "open", "Open", "PARTIALLY", "", "UNKNOWN", None))
def test_e02_closed_accepted_risk_and_unknown_states_render_nothing(status):
    assert _resolve((PHYSICAL_FEASIBILITY, status)) is None
    assert "cap01-gap-block" not in _render_state((PHYSICAL_FEASIBILITY, status))


@pytest.mark.parametrize("pairs", (
    ((MECHANISM_COMPLETENESS, OPEN),), ((BOUNDARY_AMBIGUITY, PARTIAL),),
    ((MECHANISM_COMPLETENESS, OPEN), (BOUNDARY_AMBIGUITY, OPEN)), ()))
def test_e03_other_electronics_gaps_never_carry_the_fundamentals(pairs):
    """Since the Stage-18 closure MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY carry
    their OWN context; the reference fundamentals stay PHYSICAL_FEASIBILITY-only."""
    view = _resolve(*pairs)
    html = _render_state(*pairs)
    assert "cap01-fundamentals" not in _without_sensing(html)
    if not pairs:
        assert view is None and "cap01-gap-block" not in html
        return
    assert [(c["gap_type"], c["gap_state"]) for c in view["contexts"]] == list(pairs)
    assert all(c["fundamentals"] is None for c in view["contexts"])


def test_e04_the_fundamentals_stay_physical_feasibility_only_beside_other_current_gaps():
    view = _resolve((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, OPEN),
                    (BOUNDARY_AMBIGUITY, OPEN))
    assert [c["gap_type"] for c in view["contexts"]] == [
        MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY]
    assert [c["gap_type"] for c in view["contexts"] if c["fundamentals"]] == [PHYSICAL_FEASIBILITY]
    assert cap01_guidance.CAP01_GAP_CONTEXT_BY_DOMAIN[DOMAIN] == (
        GROUP_ID, (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY))
    for gap in (MECHANISM_COMPLETENESS, BOUNDARY_AMBIGUITY):
        assert cap01_guidance.gap_context_copy(DOMAIN, gap)["fundamentals"] is None
        assert (DOMAIN, gap) not in cap01_guidance.CAP01_GAP_FUNDAMENTALS
        assert not [k for k in ui_text.UI_STRINGS if k.startswith(PREFIX + gap + "_FUNDAMENTALS")]


@pytest.mark.parametrize("domain", ("Electronics_Electrical", "ELECTRONICS_ELECTRICAL", "electronics",
                                    "electrical", "iot_electronics", "software", "medical_device",
                                    "الإلكترونيات", "", None, 3))
def test_e05_near_domain_strings_and_other_domains_never_bind(domain):
    assert _resolve((PHYSICAL_FEASIBILITY, OPEN), domain=domain) is None
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS.get((domain, PHYSICAL_FEASIBILITY)) is None


def test_e06_a_mechanical_pf_gap_renders_the_mechanical_set_never_the_electrical_one():
    mech = cap01_guidance.gap_contexts_for_gaps("mechanical", _gaps((PHYSICAL_FEASIBILITY, OPEN)))
    fund = mech["contexts"][0]["fundamentals"]
    assert fund["group_id"] == MECH_FUND_GROUP != FUND_GROUP
    assert not any(v.startswith(PREFIX) for c in fund["claims"] for v in c.values())


@pytest.mark.parametrize("impostor", (
    "Physical Feasibility", "physical feasibility", "physical_feasibility", "PHYSICAL-FEASIBILITY",
    "Electrical Physical Feasibility", "الجدوى الكهربائية", "الجدوى الفيزيائية",
    "electronics_electrical:PHYSICAL_FEASIBILITY:Q2", "voltage", "current", "resistance", "power",
    "Ohm's law", "V = I × R", "PHYSICAL_FEASIBILITY ", " PHYSICAL_FEASIBILITY"))
def test_e07_display_translated_question_word_and_near_strings_never_bind(impostor):
    assert impostor != PHYSICAL_FEASIBILITY
    assert _resolve((impostor, OPEN)) is None
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS.get((DOMAIN, impostor)) is None


_TRIGGER_TEXT = ("voltage current resistance power ohm ampere volt watt battery power supply "
                 "resistor Ohm's law V = I × R P = V × I circuit")


def test_e08_inventor_text_and_signals_cannot_trigger_the_fundamentals():
    pack = _pack()
    words = " ".join(s["signal"] for s in pack["classification_signals"] + pack["substance_signals"])
    for text in (_TRIGGER_TEXT, words):
        html = _render_state((MECHANISM_COMPLETENESS, OPEN), idea_text=text)
        assert "cap01-fundamentals" not in _without_sensing(html)
        assert 'data-cap01-gap="physical-feasibility"' not in html
    assert cap01_guidance.gap_contexts_for_gaps(DOMAIN, [(w, OPEN) for w in words.split()]) is None
    # a real Electronics session with those words but no current PF gap renders none either
    state = _s18_state(ELECTRONICS_IDEA, _TRIGGER_TEXT)
    assert PHYSICAL_FEASIBILITY not in {g.gap_type for g in state.gaps if g.status in (OPEN, PARTIAL)}
    assert "cap01-fundamentals" not in _without_sensing(_render(assemble_deliverable(state), state))


def test_e09_the_same_bounded_set_renders_regardless_of_project_content():
    a = _blocks(_render_state((PHYSICAL_FEASIBILITY, OPEN), idea_text="a heater cut-off relay"))
    b = _blocks(_render_state((PHYSICAL_FEASIBILITY, PARTIAL), idea_text=_TRIGGER_TEXT))
    assert a == b and len(a) == 1


# ==========================================================================
# E2. technical content
# ==========================================================================
def test_e10_exactly_three_claims_with_the_exact_relationships_and_units():
    fund = _fund((PHYSICAL_FEASIBILITY, OPEN))
    assert len(fund["claims"]) == 3
    for lang in ("en", "ar"):
        assert tuple(ui_text.UI_STRINGS[c["equation_key"]][lang] for c in fund["claims"]) == FUND_EQUATIONS
    assert not [k for k in ui_text.UI_STRINGS if k.startswith(FUND_PREFIX + "ITEM_4")]
    lead = _fund_texts("en")["ITEM_3_LEAD"]
    assert "volts, amperes, ohms and watts" in lead
    assert "الفولت والأمبير والأوم والواط" in _fund_texts("ar")["ITEM_3_LEAD"]
    joined = " ".join(list(_fund_texts("en").values()) + list(_fund_texts("ar").values()))
    for wrong in ("E = I", "E = IR", "P = IE", "P = I × E", "kW", "mA", "kΩ", "VA", "VAR", "Wh",
                  "mAh", "I²R", "V²/R", "cos", "φ"):
        assert wrong not in joined, wrong


_NO_FOURTH_CONCEPT = (
    "power factor", "reactive", "apparent power", "impedance", "capacitance", "inductance",
    "Kirchhoff", "voltage divider", "divider", "level shift", "op-amp", "operational amplifier",
    "filter", "transistor", "MOSFET", "wire gauge", "AWG", "fuse", "PCB", "EMC", "firmware",
    "IoT", "IEC", "IPC", "60050", "2221", "datasheet", "Arduino", "ESP32", "Raspberry",
    "certif", "complian", "readiness", "score", "confidence", "rank", "specialist")


def test_e11_no_fourth_concept_and_no_unauthorized_engineering_topic_in_the_copy():
    for part, text in _texts("en").items():
        for term in _NO_FOURTH_CONCEPT:
            assert not re.search(r"(?<!\w)%s" % re.escape(term), text, re.I), (part, term)
    for part, text in _texts("ar").items():
        for term in ("معامل القدرة", "القدرة الظاهرية", "القدرة غير الفعالة", "مقسم الجهد",
                     "المرشح", "الترانزستور", "المصهر", "الدائرة المطبوعة", "شهادة", "الامتثال",
                     "الجاهزية", "ثقة", "مختص", "أخصائي"):
            assert term not in text, (part, term)


def test_e12_digits_appear_only_in_the_source_citation_and_no_numeric_input_or_result_exists():
    for lang in ("en", "ar"):
        for part, text in _texts(lang).items():
            if part.endswith("FUNDAMENTALS_SOURCE"):
                assert re.findall(r"\d+", text) == ["1011", "1", "92", "811", "9"], text
            else:
                assert not re.search(r"\d", text), (lang, part, text)
    block = _blocks(_render_state((PHYSICAL_FEASIBILITY, OPEN)))[0]
    for control in ("<input", "<form", "<select", "<textarea", "<button"):
        assert control not in block, control
    assert not re.search(r"=\s*\d", _visible(block))


def test_e13_the_required_meanings_are_stated_in_both_languages():
    en, ar = _fund_texts("en"), _fund_texts("ar")
    assert en["TITLE"] == "Reference fundamentals that may help with this electrical feasibility gap"
    assert "InventorAI has not determined that these relationships apply to your design." in en["INTRO"]
    assert "لم يحدد InventorAI أن هذه العلاقات تنطبق على تصميمك." in ar["INTRO"]
    assert "not a calculation for your circuit" in en["ITEM_1_NOTE"]
    assert "وليست حسابًا لدائرتك" in ar["ITEM_1_NOTE"]
    for topic in ("component rating", "power-supply suitability", "battery sizing", "efficiency",
                  "thermal adequacy", "safety"):
        assert topic in en["ITEM_2_NOTE"], topic
    for topic in ("تصنيف المكوّنات", "ملاءمة مصدر التغذية", "سعة البطارية", "الكفاءة",
                  "الكفاية الحرارية", "السلامة"):
        assert topic in ar["ITEM_2_NOTE"], topic
    assert en["ITEM_3_NOTE"] == "Correct units do not validate a circuit or design."
    assert "صحة الوحدات لا تعني صحة الدائرة أو التصميم" in ar["ITEM_3_NOTE"]
    for topic in ("close the electrical feasibility gap", "calculate your design", "establish compatibility",
                  "safe voltage / current limits", "prove that the circuit works", "size any component",
                  "prove electrical safety", "validate the invention"):
        assert topic in en["BOUNDARY"], topic
    for topic in ("لا تغلق فجوة الجدوى الكهربائية", "ولا تحسب تصميمك", "التوافق", "حدود الجهد / التيار الآمنة",
                  "أن الدائرة تعمل", "مقاسات أي مكوّن", "السلامة الكهربائية", "الاختراع تم التحقق منه"):
        assert topic in ar["BOUNDARY"], topic


_NEGATED_ONLY_EN = ("apply to your design", "calculation for your circuit", "behaves this way",
                    "component rating", "power-supply suitability", "battery sizing", "efficiency",
                    "thermal adequacy", "safety", "validate", "compatib", "safe", "circuit works",
                    "electrically feasible", "calculate", "size any component", "close the",
                    "recommend")
_NEGATED_ONLY_AR = ("تنطبق على تصميمك", "حسابًا لدائرتك", "تتصرف بهذه الطريقة", "تصنيف المكوّنات",
                    "ملاءمة مصدر التغذية", "سعة البطارية", "الكفاءة", "الكفاية الحرارية", "السلامة",
                    "تم التحقق", "التوافق", "آمن", "الدائرة تعمل", "ممكن كهربائيًا", "تحسب", "مقاسات",
                    "تغلق", "يوصي")
_EN_NEGATORS = ("not ", "no ", "does not", "do not", "has not", "not a ")


def test_e14_applicability_feasibility_safety_and_validation_are_only_ever_denied():
    for part, text in _texts("en").items():
        for sentence in _sentences(text):
            for term in _NEGATED_ONLY_EN:
                at = sentence.lower().find(term.lower())
                if at >= 0:
                    lead = sentence[:at].lower()
                    assert any(n in lead for n in _EN_NEGATORS), (part, term, sentence)
    for part, text in _texts("ar").items():
        for sentence in _sentences(text):
            for term in _NEGATED_ONLY_AR:
                at = sentence.find(term)
                if at >= 0:
                    assert any(n in sentence[:at] for n in _AR_NEGATORS + ("وهي لا ",)), (part, term, sentence)


def test_e15_the_copy_is_reference_framed_and_never_prescribes_a_value():
    joined = " ".join(_texts("en").values()).lower()
    for forbidden in ("you should use", "you must use", "set the voltage", "choose a resistor",
                      "select a", "we recommend", "your circuit is", "your design is",
                      "the correct value", "will work", "is safe"):
        assert forbidden not in joined, forbidden
    assert "reference" in _fund_texts("en")["INTRO"]


# ==========================================================================
# E3. sources, provenance and the pack
# ==========================================================================
def test_e16_four_new_provenance_records_with_the_exact_authorized_identities():
    recs = _provenance()
    assert all(r in recs for r in NEW_RECORDS)
    ids = [r for r in recs if r.startswith("electronics_electrical:")]
    assert ids[:7] == ["electronics_electrical:PR00%d" % n for n in range(1, 8)]
    # ELECTRICAL-ENERGY-TIME-REFERENCE-01 appends exactly four further records, and
    # 28-T1-SENSING-VALUE-THRESHOLD-01 two more (PR012–PR013).
    assert ids[7:] == ["electronics_electrical:PR%03d" % n for n in range(8, 14)]
    doe, nist, doe_pol, nist_pol = (recs[r] for r in NEW_RECORDS)
    assert doe["standard_number"] == "DOE-HDBK-1011/1-92" and doe["source_type"] == "government_reference_publication"
    assert "Electrical Science" in doe["source_name"] and "Volume 1 of 4" in doe["source_name"]
    assert "Module 1 — Basic Electrical Theory" in doe["source_name"]
    assert "handbook page 14" in doe["version_or_edition"] and "handbook page 16" in doe["version_or_edition"]
    assert nist["standard_number"] == "NIST SP 811" and "Appendix B.9" in nist["source_name"]
    assert nist["url"] == ("https://www.nist.gov/pml/special-publication-811/"
                           "nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9")
    assert doe_pol["source_type"] == nist_pol["source_type"] == "source_use_policy"
    assert "Web Policies" in doe_pol["source_name"] and "Copyright, Restrictions and Permissions" in doe_pol["source_name"]
    assert "Technical Series Publications" in nist_pol["source_name"]
    for rec in (doe, nist, doe_pol, nist_pol):
        assert rec["pack_id"] == DOMAIN and rec["tier"] == 1 and rec["jurisdiction"] == "US"
        assert rec["cross_domain_usage"] == []
    for pol in (doe_pol, nist_pol):
        assert "not a legal opinion" in pol["notes"]


def test_e17_the_doe_record_states_the_archived_boundary_and_the_notation_normalization():
    notes = _provenance()["electronics_electrical:PR004"]["notes"]
    rec = _provenance()["electronics_electrical:PR004"]
    assert "ARCHIVE — Canceled, effective April 2016" in rec["version_or_edition"]
    for phrase in ("status ARCHIVE — Canceled, effective April 2016",
                   "historical / fundamentals reference",
                   "NOT as current regulatory, safety or compliance guidance or authority",
                   "never as proof that a user design is safe, compliant or valid",
                   "E = I × R / E = IR (handbook page 14)",
                   "E = voltage (V), I = current (A) and R = resistance (Ω)",
                   "P = I × E / P = IE (handbook page 16)",
                   "V = I × R (V = IR) and P = V × I (P = VI)", "notation normalization only",
                   "it is not claimed that DOE wrote V = I × R or P = V × I",
                   "no DOE paragraph, explanatory prose, worked numerical example, figure, diagram, "
                   "photograph or logo is copied",
                   "no extra derived equation, conductance, AC relationship or circuit-solving procedure",
                   "no DOE endorsement is stated or implied",
                   "no content attributed to a third party is relied upon",
                   "authorize no copying of those works"):
        assert phrase in notes, phrase


def test_e17b_the_lead_source_inspection_and_the_conservative_dispositions_are_recorded():
    recs = _provenance()
    for rid in NEW_RECORDS:
        rec = recs[rid]
        assert "as inspected 2026-09-28 (Lead-level independent source inspection" in rec["version_or_edition"]
        assert "PENDING" not in json.dumps(rec, ensure_ascii=False)
    doe_pol = recs["electronics_electrical:PR006"]["notes"]
    for phrase in ("SOURCE-USE COMPATIBILITY DISPOSITION (not a legal opinion",
                   "public domain and may be freely distributed / copied",
                   "contributed or licensed by private parties may remain copyright-protected",
                   "EG&G Idaho, Inc.",
                   "No blanket claim is made that every expressive element of the handbook is "
                   "public-domain material"):
        assert phrase in doe_pol, phrase
    nist_pol = recs["electronics_electrical:PR007"]["notes"]
    for phrase in ("SOURCE-USE COMPATIBILITY DISPOSITION (not a legal opinion",
                   "not subject to U.S. copyright protection", "acknowledgement / citation is required",
                   "third-party-authored protected material", "(V; A; Ω; W)"):
        assert phrase in nist_pol, phrase
    assert "ampere — A, volt — V, ohm — Ω and watt — W" in recs["electronics_electrical:PR005"]["notes"]


def test_e18_existing_provenance_pr001_to_pr003_are_unchanged():
    recs = _provenance()
    old = [recs["electronics_electrical:PR00%d" % n] for n in (1, 2, 3)]
    assert _digest(old) == _PR001_PR003_DIGEST
    assert old[0]["standard_number"] == "IEC 60050" and old[1]["standard_number"] == "IPC-2221B"


def test_e19_the_pack_group_declares_the_three_claims_with_exact_source_and_policy_linkage():
    pack, recs = _pack(), _provenance()
    # ELECTRICAL-ENERGY-TIME-REFERENCE-01 appends one further group AFTER this one, and
    # 28-T1-SENSING-VALUE-THRESHOLD-01 one more (MECHANISM_COMPLETENESS).
    groups = pack["reference_fundamentals"]
    assert [g["group_id"] for g in groups] == [FUND_GROUP, "electrical_energy_time_reference_v1",
                                               "sensing_value_threshold_reference_v1"]
    group = groups[0]
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["group_id"] == FUND_GROUP and group["applicable_gap_type"] == PHYSICAL_FEASIBILITY
    assert tuple(c["claim_id"] for c in group["claims"]) == FUND_CLAIMS
    relationships = ("V = I × R", "P = V × I", "voltage: V; current: A; resistance: Ω; power: W")
    for claim, rel in zip(group["claims"], relationships):
        assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation",
                                 "relationship", "source_ref", "source_use_policy_ref"]
        assert claim["relationship"] == rel and claim["applicable_gap_type"] == PHYSICAL_FEASIBILITY
        src, pol = CLAIM_SOURCES[claim["claim_id"]]
        assert (claim["source_ref"], claim["source_use_policy_ref"]) == (src, pol)
        assert recs[src]["source_type"] == "government_reference_publication"
        assert recs[pol]["source_type"] == "source_use_policy"
        assert claim["claim_id"] in recs[src]["notes"]
        assert claim["fact"].strip() and claim["limitation"].strip()
    assert "E = I × R" in group["claims"][0]["fact"] and "notation normalization" in group["claims"][0]["fact"]
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS[(DOMAIN, PHYSICAL_FEASIBILITY)] == (FUND_GROUP, FUND_CLAIMS)


def test_e20_every_pre_existing_pack_field_is_unchanged_and_the_group_is_declared_inert():
    pack = _pack()
    pre = copy.deepcopy(pack)
    pre.pop("reference_fundamentals")
    note = pre["_governance_notes"].pop("electrical_td_slice1_reference_fundamentals")
    # ...and the later, separately authorized energy-time group's own note.
    pre["_governance_notes"].pop("electrical_energy_time_reference_fundamentals")
    pre["_governance_notes"].pop("sensing_value_threshold_reference")
    assert _digest(pre) == _PRE_SLICE_PACK_DIGEST
    for phrase in ("inert", "classifier", "Path-N", "evidence state", "no loader or schema change",
                   "CAP01_ELECTRONICS_INTERFACE_V1", "PR001–PR003 are unchanged",
                   "are not the claim authority"):
        assert phrase in note, phrase
    for rel in ("engine/domain_registry.py", "engine/domain_rules.py", "engine/domain_activation.py",
                "engine/path_n_questions.py", "engine/gap_action_pack.py", "engine/progression_loop.py",
                "engine/idea_state.py", "engine/need_routing.py"):
        with io.open(os.path.join(_ROOT, rel), encoding="utf-8") as fh:
            assert "reference_fundamentals" not in fh.read(), rel


def test_e21_classification_activation_rules_and_question_serving_are_unchanged():
    from engine import domain_activation
    from engine.domain_rules import classify_domain, get_active_rules, infer_domain
    assert domain_activation.is_activated(DOMAIN)
    assert infer_domain(ELECTRONICS_IDEA) == DOMAIN
    rules = json.dumps([getattr(r, "__dict__", r) for r in get_active_rules(DOMAIN)], default=str)
    assert FUND_GROUP not in rules and "ohms_law" not in rules
    cls = classify_domain(_TRIGGER_TEXT)
    assert FUND_GROUP not in json.dumps(getattr(cls, "__dict__", str(cls)), default=str)
    # Path-N (its own committed config) stays the only served-question owner: no
    # served Electronics question carries a relationship, unit set or claim id.
    for mapping in _pack()["gap_type_mappings"]:
        for n in range(len(mapping["questions"])):
            served = get_served_question(mapping["gap_type_id"], n, domain=DOMAIN)
            assert served.question_id and served.text
            for eq in FUND_EQUATIONS + FUND_CLAIMS:
                assert eq not in served.text


def test_e22_source_acknowledgement_is_neutral_and_names_exactly_the_authorized_sources():
    en, ar = _fund_texts("en"), _fund_texts("ar")
    assert en["SOURCE"] == ("Reference source material: U.S. Department of Energy — Electrical Science, "
                            "DOE-HDBK-1011/1-92; NIST Guide to the SI, SP 811 Appendix B.9.")
    assert ar["SOURCE"].startswith("مواد مرجعية:")
    for token in ("U.S. Department of Energy", "Electrical Science", "DOE-HDBK-1011/1-92",
                  "NIST", "SP 811 Appendix B.9"):
        assert token in ar["SOURCE"], token
    for part, text in list(en.items()):
        if "DOE" in text or "NIST" in text or "Department of Energy" in text:
            assert part == "SOURCE", part
    joined = " ".join(list(_texts("en").values()) + list(_texts("ar").values())).lower()
    for forbidden in ("according to doe", "doe confirms", "doe recommends", "endorse", "approved by",
                      "certified by", "reviewed by", "openstax", "wikipedia", "textbook", "logo",
                      "insignia", "image", "figure", "diagram", "شعار", "صورة", "معتمد من"):
        assert forbidden not in joined, forbidden


def test_e23_no_unapproved_source_in_the_pack_group_the_records_or_the_rendered_block():
    group_text = json.dumps(_pack()["reference_fundamentals"], ensure_ascii=False).lower()
    prov_text = json.dumps([_provenance()[r] for r in NEW_RECORDS], ensure_ascii=False).lower()
    for text in (group_text, prov_text):
        for forbidden in ("openstax", "wikipedia", "khan", "electronics-tutorials", "allaboutcircuits",
                          "hyperphysics", "youtube", ".png", ".jpg", ".svg", "<img"):
            assert forbidden not in text, forbidden
    # IEC / IPC are never the claim authority of this group
    assert "pr001" not in group_text and "pr002" not in group_text and "pr003" not in group_text
    block = _blocks(_render_state((PHYSICAL_FEASIBILITY, OPEN)))[0]
    assert "<img" not in block and "http" not in block and "energy.gov" not in block


# ==========================================================================
# E4. ownership / non-regression
# ==========================================================================
def test_e24_the_electronics_checklist_profile_is_unchanged_and_renders_identically(monkeypatch):
    view = cap01_guidance.profile_copy(DOMAIN)
    assert view["profile_id"] == PROFILE_ID and len(view["item_keys"]) == 6
    assert view["research"] is not None and len(view["research"]["item_keys"]) == 6
    state = _elec_state((PHYSICAL_FEASIBILITY, OPEN))
    package = assemble_deliverable(state)
    html = _mask_csrf(_render(package, state))
    profile = re.search(r'<div class="cap01-block" data-cap01-profile="%s">.*?\n  </div>' % PROFILE_ID,
                        html, re.S).group(0)
    assert "cap01-fund" not in profile and "V = I × R" not in profile
    monkeypatch.setattr(cap01_guidance, "CAP01_GAP_CONTEXT_BY_DOMAIN",
                        {k: v for k, v in cap01_guidance.CAP01_GAP_CONTEXT_BY_DOMAIN.items() if k != DOMAIN})
    without = _mask_csrf(_render(package, state))
    assert "cap01-gap-block" not in without
    assert re.search(r'<div class="cap01-block" data-cap01-profile="%s">.*?\n  </div>' % PROFILE_ID,
                     without, re.S).group(0) == profile
    # the gap-scoped layer sits after the checklist block and repeats none of its six topics
    assert html.index('data-cap01-profile="%s"' % PROFILE_ID) < html.index("cap01-gap-block")
    for key in view["item_keys"]:
        assert ui_text.UI_STRINGS[key]["en"] not in " ".join(_texts("en").values())


def test_e25_an_electronics_report_without_a_current_pf_gap_is_byte_identical_to_before(monkeypatch):
    state = _s18_state(ELECTRONICS_IDEA, OPEN_GAP_INPUT)
    package = assemble_deliverable(state)
    with_rows = _mask_csrf(_render(package, state))
    assert PHYSICAL_FEASIBILITY not in {g.gap_type for g in state.gaps if g.status in (OPEN, PARTIAL)}
    # Stage-18 closure: the current MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY
    # contexts may render, but no fundamentals; removing the fundamentals row
    # changes nothing.
    assert "cap01-fundamentals" not in _without_sensing(with_rows)
    assert 'data-cap01-gap="physical-feasibility"' not in with_rows
    monkeypatch.setattr(cap01_guidance, "CAP01_GAP_FUNDAMENTALS",
                        {k: v for k, v in cap01_guidance.CAP01_GAP_FUNDAMENTALS.items() if k[0] != DOMAIN})
    assert _mask_csrf(_render(package, state)) == with_rows


def test_e26_the_mechanical_fundamentals_are_unchanged():
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS[("mechanical", PHYSICAL_FEASIBILITY)] == (
        MECH_FUND_GROUP, MECH_FUND_CLAIMS)
    mech = cap01_guidance.gap_contexts_for_gaps("mechanical", _gaps((PHYSICAL_FEASIBILITY, OPEN)))
    eqs = tuple(ui_text.UI_STRINGS[c["equation_key"]]["en"]
                for c in mech["contexts"][0]["fundamentals"]["claims"])
    assert eqs == MECH_FUND_EQUATIONS


def test_e27_no_state_gap_action_pack_or_readiness_change_and_no_new_framework():
    state = _elec_state((PHYSICAL_FEASIBILITY, OPEN), (MECHANISM_COMPLETENESS, PARTIAL))
    before_state = pickle.dumps(state)
    before_packs = pickle.dumps(derive_gap_action_packs(state))
    _render(assemble_deliverable(state), state)
    assert pickle.dumps(state) == before_state
    assert pickle.dumps(derive_gap_action_packs(state)) == before_packs
    guidance = _executable(_GUIDANCE_PATH)
    for forbidden in ("class ", "eval(", "exec(", "float(", "int(", "calculate", "Registry",
                      "registry", "Framework", "select_formula", "formula_for", "infer_"):
        assert forbidden not in guidance, forbidden


# ==========================================================================
# E5. surfaces: report, PDF, session, EN / AR, RTL
# ==========================================================================
def test_e28_en_report_route_renders_the_full_english_context_and_sub_view(client):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _set_gaps(sid, (MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, OPEN),
              (BOUNDARY_AMBIGUITY, PARTIAL))
    page = _report(client, sid)
    [block] = _blocks(page)
    visible = _visible(page)
    for part, text in _texts("en").items():
        assert text in visible, part
    for part, text in _texts("ar").items():
        if not part.endswith("_EQUATION"):
            assert text not in visible, part
    assert _equations(block) == list(FUND_EQUATIONS)
    assert "UI_CAP01_" not in _visible(block) and PHYSICAL_FEASIBILITY not in _visible(block)


def test_e29_ar_rtl_report_route_renders_arabic_with_ltr_isolated_equations(client):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _set_gaps(sid, (MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, PARTIAL),
              (BOUNDARY_AMBIGUITY, OPEN))
    page = _report(client, sid, lang="ar")
    assert 'dir="rtl"' in page
    [block] = _blocks(page)
    visible = _visible(page)
    for part, text in _texts("ar").items():
        assert text in visible, part
    for part, text in _texts("en").items():
        if not part.endswith("_EQUATION"):
            assert text not in visible, part
    assert _equations(block) == list(FUND_EQUATIONS)
    assert block.count('<bdi class="cap01-fund-equation" dir="ltr"') == 3
    for token in ("InventorAI", "(Physical Feasibility)", "DOE-HDBK-1011/1-92", "SP 811 Appendix B.9"):
        assert token in visible, token


def test_e30_equations_are_language_neutral_and_never_split_by_direction_marks():
    for eq in FUND_EQUATIONS:
        assert not re.search(r"[؀-ۿ‎‏‪-‮]", eq), eq
        assert eq == eq.strip()
    for lang in ("en", "ar"):
        [block] = _blocks(_render_state((PHYSICAL_FEASIBILITY, OPEN), lang=lang))
        for eq in FUND_EQUATIONS:
            assert ('data-cap01-fund-equation>%s</bdi>' % eq) in block, (lang, eq)
        prose = _visible(re.sub(r'<bdi class="cap01-fund-equation"[^>]*>.*?</bdi>', "", block))
        for eq in FUND_EQUATIONS:
            assert eq not in prose, (lang, eq)


def test_e31_pdf_source_matches_the_screen_report_and_changes_no_state(client, monkeypatch):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, OPEN))
    state = _live(sid)
    before = pickle.dumps(state)
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    for lang in ("en", "ar"):
        screen = _report(client, sid, lang=lang)
        source = _pdf_source(client, sid, monkeypatch)
        assert _blocks(source) == _blocks(screen) and len(_blocks(source)) == 1
        assert _equations(_blocks(source)[0]) == list(FUND_EQUATIONS)
    state = _live(sid)
    assert pickle.dumps(state) == before
    readiness = derive_readiness(state)
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready


def test_e32_pdf_source_excludes_the_sub_view_when_pf_is_closed(client, monkeypatch):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, CLOSED), (MECHANISM_COMPLETENESS, OPEN))
    source = _pdf_source(client, sid, monkeypatch)
    assert "cap01-fundamentals" not in _without_sensing(source)
    assert 'data-cap01-gap="physical-feasibility"' not in source
    assert 'data-cap01-gap="mechanism-completeness"' in source    # its own context only


def test_e33_session_page_never_carries_the_context_or_the_fundamentals(client):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, OPEN))
    for lang in ("en", "ar"):
        if lang == "ar":
            client.post("/ui-language", data={"lang": "ar"})
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "cap01-gap-block" not in page and "cap01-fund" not in page
        for eq in FUND_EQUATIONS[:2]:
            assert eq not in page
        assert _fund_texts(lang)["TITLE"] not in page


def test_e34_incomplete_copy_fails_closed_all_or_nothing(monkeypatch):
    monkeypatch.delitem(ui_text.UI_STRINGS, FUND_PREFIX + "ITEM_2_NOTE")
    ctx = _resolve((PHYSICAL_FEASIBILITY, OPEN))["contexts"][0]
    assert ctx["fundamentals"] is None and ctx["meaning_key"] == PREFIX + "PHYSICAL_FEASIBILITY_MEANING"
    monkeypatch.delitem(ui_text.UI_STRINGS, PREFIX + "PHYSICAL_FEASIBILITY_LIMIT")
    assert _resolve((PHYSICAL_FEASIBILITY, OPEN)) is None
