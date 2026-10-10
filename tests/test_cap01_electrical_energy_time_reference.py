# -*- coding: utf-8 -*-
"""ELECTRICAL-ENERGY-TIME-REFERENCE-01 — the second, separately authorized Electrical
reference-fundamentals group (Stage 18 / CAP-01 bounded extension).

What is pinned: when, and only when, the trusted canonical domain is
``electronics_electrical`` AND the EXACT canonical ``PHYSICAL_FEASIBILITY`` gap is in
EXACT state OPEN or PARTIAL, the report / deliverable and the PDF show the existing
basic_electrical_reference_v1 group FIRST and then ONE further group,
electrical_energy_time_reference_v1, of exactly two bounded reference claims:
E = P × t ONLY when P remains constant throughout t, and the unit discipline
J / W / s with J = W · s.

Boundaries proven here: the original three claims, copy, sources and rendering are
unchanged; exact binding (domain + gap id + lifecycle state only), with no text,
keyword or signal access; each group is all-or-nothing on its own copy; the pack
and provenance changes are additions only; PR008–PR011 carry exact claim mappings,
locations, limitations and source-use dispositions; nothing reaches the shared
calculation / units owner; EN / AR wording is the accepted wording with the
constant-power restriction, LTR-isolated equations and an approved negative
disclosure — no calculation, input, battery, charge or Ah / Wh content.
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
from engine import deterministic_calculation as dc
from engine.deliverable_assembler import assemble_deliverable
from engine.derived_readiness import derive_readiness
from engine.idea_state import (
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, IdeaState, MECHANISM_COMPLETENESS, OPEN,
    PARTIAL, PHYSICAL_FEASIBILITY)
from web import cap01_guidance, ui_text
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, ELEC_SEED, _start, _live,
)
from tests.test_stage18_cap01_bounded_guidance import _mask_csrf
from tests.test_cap01_mechanical_open_gap_context import (
    FUND_GROUP as MECH_FUND_GROUP, _gaps, _pdf_source, _render, _report, _visible)
from tests.test_cap01_electrical_reference_fundamentals import (
    FUND_CLAIMS as BASE_CLAIMS, FUND_EQUATIONS as BASE_EQUATIONS, FUND_GROUP as BASE_GROUP,
    _blocks as _base_blocks)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")

DOMAIN = "electronics_electrical"
PREFIX = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_"
ET_PREFIX = PREFIX + PHYSICAL_FEASIBILITY + "_ENERGY_TIME_FUNDAMENTALS_"
BASE_PREFIX = PREFIX + PHYSICAL_FEASIBILITY + "_FUNDAMENTALS_"
ET_GROUP = "electrical_energy_time_reference_v1"
ET_CLAIMS = ("constant_power_energy_reference", "energy_time_unit_discipline")
ET_EQUATIONS = ("E = P × t", "J = W · s")
ET_SOURCES = {
    "constant_power_energy_reference": ("electronics_electrical:PR008", "electronics_electrical:PR010"),
    "energy_time_unit_discipline": ("electronics_electrical:PR009", "electronics_electrical:PR011"),
}
ET_RECORDS = tuple("electronics_electrical:PR%03d" % n for n in (8, 9, 10, 11))
# Canonical digests at base dde13c26226b0034e1ddc605bf89483075ecdd6e: the whole
# Electronics pack, and the whole provenance record list, before this slice.
_PRE_PACK_DIGEST = "e35656974acd579670e5189e028a33f6bb4f4067bad0908b190325ab1a2f882d"
_PRE_PROVENANCE_DIGEST = "b8d51454d9f63e6972e50ddf1678471c3d430afb9d11840466c1420d271773f4"

ACCEPTED = {
    "en": {
        "TITLE": "Energy and power over time",
        "ITEM_1_LEAD": "When power P remains constant throughout a time interval t, the energy "
                       "transferred E is:",
        "ITEM_1_EQUATION": "E = P × t",
        "ITEM_1_NOTE": "E is the energy transferred, P is the constant power, and t is the duration.",
        "ITEM_2_LEAD": "E is measured in joules J, P in watts W, and t in seconds s. The "
                       "corresponding unit relationship is:",
        "ITEM_2_EQUATION": "J = W · s",
        "INTRO": "Reference information only. InventorAI has not established that power is "
                 "constant or that this relationship applies to your invention.",
        "BOUNDARY": "This group performs no project-specific calculation and determines no battery "
                    "capacity, runtime, component suitability or safety.",
        # PR787-REVIEW-CLOSURE-01: the four executor-authored strings, pinned exactly.
        "ITEM_1_TITLE": "Energy at constant power",
        "ITEM_2_TITLE": "Units of energy, power and time",
        "ITEM_2_NOTE": "Correct units do not validate a design or establish that the constant-power "
                       "energy relationship applies to your invention.",
        "SOURCE": "Reference source material: U.S. Department of Energy — Classical Physics, "
                  "DOE-HDBK-1010-92 (archived; fundamentals reference only); NIST Guide to the SI, "
                  "SP 811 Chapter 4 and Appendix B.9.",
    },
    "ar": {
        "TITLE": "الطاقة والقدرة خلال مدة زمنية",
        "ITEM_1_LEAD": "عندما تبقى القدرة P ثابتة طوال مدة زمنية t، تكون الطاقة المنقولة E وفق العلاقة:",
        "ITEM_1_EQUATION": "E = P × t",
        "ITEM_1_NOTE": "ترمز E إلى الطاقة المنقولة، وP إلى القدرة الثابتة، وt إلى المدة الزمنية.",
        "ITEM_2_LEAD": "تُقاس E بالجول J، وP بالواط W، وt بالثانية s. والعلاقة بين الوحدات هي:",
        "ITEM_2_EQUATION": "J = W · s",
        "INTRO": "هذه معلومات مرجعية فقط. لم يثبت InventorAI أن القدرة ثابتة أو أن هذه العلاقة "
                 "تنطبق على اختراعك.",
        "BOUNDARY": "لا تُجري هذه المجموعة حسابًا خاصًا بمشروعك، ولا تحدد سعة البطارية أو مدة "
                    "تشغيلها أو ملاءمة المكونات أو سلامتها.",
        "ITEM_1_TITLE": "الطاقة عند قدرة ثابتة",
        "ITEM_2_TITLE": "وحدات الطاقة والقدرة والزمن",
        "ITEM_2_NOTE": "صحة الوحدات لا تثبت صحة التصميم أو انطباق علاقة الطاقة عند ثبات القدرة على "
                       "اختراعك.",
        "SOURCE": "مواد مرجعية: وزارة الطاقة الأمريكية (U.S. Department of Energy) — Classical Physics، "
                  "DOE-HDBK-1010-92 (مؤرشف؛ مرجع للأساسيات فقط)؛ ودليل NIST للنظام الدولي للوحدات، "
                  "SP 811 الفصل 4 والملحق B.9.",
    },
}

# 28-T1-SENSING-VALUE-THRESHOLD-01 later added ONE Electronics MECHANISM_COMPLETENESS
# group (pack group + note, PR012 / PR013); this file's base-digest and inventory
# checks exclude exactly that later addition, which is pinned by
# tests/test_cap01_sensing_value_threshold_reference.py.
SENSING_GROUP = "sensing_value_threshold_reference_v1"
SENSING_NOTE = "sensing_value_threshold_reference"
SENSING_RECORDS = ("electronics_electrical:PR012", "electronics_electrical:PR013")
SENSING_EXTENSION = (
    (DOMAIN, MECHANISM_COMPLETENESS),
    (("sensing_value_threshold_reference_v1", ("sensed_value_versus_threshold_indication",),
      "SENSING_FUNDAMENTALS_"),))

_ET_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="electrical-energy-time-reference-v1">'
    r'.*?\n      </div>', re.S)
_ANY_FUND_RE = re.compile(r'<div class="cap01-fundamentals" data-cap01-fundamentals="([^"]+)"')


# ==========================================================================
# harness
# ==========================================================================
def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _pack():
    with io.open(_PACK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _provenance():
    with io.open(_PROVENANCE_PATH, encoding="utf-8") as fh:
        return json.load(fh)["records"]


def _state(*pairs, domain=DOMAIN, idea_text=None):
    s = IdeaState(idea_id="cap01-energy-time-probe")
    s.domain = domain
    s.domain_signal = domain
    s.gaps = _gaps(*pairs)
    if idea_text is not None:
        s.idea_text = idea_text
    return s


def _html(*pairs, lang="en", pdf=False, domain=DOMAIN, idea_text=None):
    state = _state(*pairs, domain=domain, idea_text=idea_text)
    return _render(assemble_deliverable(state), state, lang=lang, pdf=pdf)


def _groups(*pairs, domain=DOMAIN):
    view = cap01_guidance.gap_contexts_for_gaps(domain, _gaps(*pairs))
    if view is None:
        return None
    return {c["gap_type"]: c["fundamentals_groups"] for c in view["contexts"]}


def _et_texts(lang):
    return {k[len(ET_PREFIX):]: ui_text.UI_STRINGS[k][lang]
            for k in sorted(ui_text.UI_STRINGS) if k.startswith(ET_PREFIX)}


def _equations(block):
    return re.findall(
        r'<bdi class="cap01-fund-equation" dir="ltr" data-cap01-fund-equation[^>]*>(.*?)</bdi>', block)


# ==========================================================================
# 1. binding, order and isolation
# ==========================================================================
@pytest.mark.parametrize("status", (OPEN, PARTIAL))
def test_t01_pf_open_or_partial_renders_exactly_the_two_groups_in_order(status):
    groups = _groups((PHYSICAL_FEASIBILITY, status))[PHYSICAL_FEASIBILITY]
    assert [g["group_id"] for g in groups] == [BASE_GROUP, ET_GROUP]
    assert tuple(c["claim_id"] for c in groups[0]["claims"]) == BASE_CLAIMS
    assert tuple(c["claim_id"] for c in groups[1]["claims"]) == ET_CLAIMS
    html = _html((PHYSICAL_FEASIBILITY, status))
    assert _ANY_FUND_RE.findall(html) == ["basic-electrical-reference-v1",
                                          "electrical-energy-time-reference-v1"]
    [et] = _ET_RE.findall(html)
    assert _equations(et) == list(ET_EQUATIONS)
    [base] = _base_blocks(html)
    assert _equations(base) == list(BASE_EQUATIONS)


@pytest.mark.parametrize("status", (CLOSED, ACCEPTED_RISK, "open", "PARTIALLY", "", None))
def test_t02_ineligible_states_render_no_group(status):
    assert _groups((PHYSICAL_FEASIBILITY, status)) is None
    assert "cap01-fundamentals" not in _html((PHYSICAL_FEASIBILITY, status))


def test_t03_other_gaps_domains_and_text_grant_no_access():
    groups = _groups((MECHANISM_COMPLETENESS, OPEN), (BOUNDARY_AMBIGUITY, PARTIAL))
    assert groups and all(ET_GROUP not in [g["group_id"] for g in v] for v in groups.values())
    mech = _groups((PHYSICAL_FEASIBILITY, OPEN), domain="mechanical")[PHYSICAL_FEASIBILITY]
    assert [g["group_id"] for g in mech] == [MECH_FUND_GROUP]
    for domain in ("control_loop", "software", "medical_device", "Electronics_Electrical", ""):
        assert cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS.get((domain, PHYSICAL_FEASIBILITY)) is None
    assert tuple(cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS) == (
        (DOMAIN, PHYSICAL_FEASIBILITY), SENSING_EXTENSION[0])
    # battery / energy words in the inventor's text never add or reorder a group
    battery = "A battery pack with a BMS; runtime 4 hours at constant 10 W; capacity in Wh and Ah"
    for pairs in (((PHYSICAL_FEASIBILITY, CLOSED),), ((MECHANISM_COMPLETENESS, OPEN),)):
        assert "electrical-energy-time" not in _html(*pairs, idea_text=battery)
    html = _html((PHYSICAL_FEASIBILITY, OPEN), idea_text=battery)
    assert _mask_csrf(html) == _mask_csrf(_html((PHYSICAL_FEASIBILITY, OPEN)))


def test_t04_the_binding_is_a_fixed_table_without_discovery_or_inference():
    src = io.open(os.path.join(_ROOT, "web", "cap01_guidance.py"), encoding="utf-8").read()
    start = src.index("CAP01_GAP_FUNDAMENTALS_EXTENSIONS = {")
    table = src[start:src.index("\n}\n", start)]
    for token in ("import", "glob", "listdir", "json.load", "reference_fundamentals", "idea_text"):
        assert token not in table, token
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS == {
        (DOMAIN, PHYSICAL_FEASIBILITY): ((ET_GROUP, ET_CLAIMS, "ENERGY_TIME_FUNDAMENTALS_"),),
        SENSING_EXTENSION[0]: SENSING_EXTENSION[1]}


# ==========================================================================
# 2. each group is all-or-nothing on its own copy
# ==========================================================================
def test_t05_missing_new_copy_suppresses_only_the_new_group(monkeypatch):
    monkeypatch.delitem(ui_text.UI_STRINGS, ET_PREFIX + "ITEM_2_NOTE")
    groups = _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]
    assert [g["group_id"] for g in groups] == [BASE_GROUP]
    html = _html((PHYSICAL_FEASIBILITY, OPEN))
    assert _ANY_FUND_RE.findall(html) == ["basic-electrical-reference-v1"]
    assert 'data-cap01-gap="physical-feasibility"' in html


def test_t06_missing_original_copy_suppresses_only_the_original_group(monkeypatch):
    monkeypatch.delitem(ui_text.UI_STRINGS, BASE_PREFIX + "ITEM_3_NOTE")
    ctx = cap01_guidance.gap_contexts_for_gaps(DOMAIN, _gaps((PHYSICAL_FEASIBILITY, OPEN)))["contexts"][0]
    assert ctx["fundamentals"] is None
    assert [g["group_id"] for g in ctx["fundamentals_groups"]] == [ET_GROUP]
    html = _html((PHYSICAL_FEASIBILITY, OPEN))
    assert _ANY_FUND_RE.findall(html) == ["electrical-energy-time-reference-v1"]
    assert 'data-cap01-gap-meaning' in html


def test_t07_a_missing_group_part_suppresses_the_whole_group_never_partial_claims(monkeypatch):
    monkeypatch.delitem(ui_text.UI_STRINGS, ET_PREFIX + "SOURCE")
    html = _html((PHYSICAL_FEASIBILITY, OPEN))
    assert "electrical-energy-time-reference-v1" not in html
    assert "E = P × t" not in html and "J = W · s" not in html


# ==========================================================================
# 3. pack and provenance: additions only, exact mappings
# ==========================================================================
def test_t08_the_pack_change_is_exactly_one_group_and_one_note():
    pack = _pack()
    pre = copy.deepcopy(pack)
    pre["reference_fundamentals"] = [g for g in pre["reference_fundamentals"]
                                     if g["group_id"] not in (ET_GROUP, SENSING_GROUP)]
    note = pre["_governance_notes"].pop("electrical_energy_time_reference_fundamentals")
    pre["_governance_notes"].pop(SENSING_NOTE)
    assert _digest(pre) == _PRE_PACK_DIGEST
    assert [g["group_id"] for g in pack["reference_fundamentals"]] == [BASE_GROUP, ET_GROUP, SENSING_GROUP]
    for phrase in ("inert", "exactly two bounded reference claims", "ONLY when P remains constant",
                   "PR008–PR009", "PR010–PR011", "PR001–PR007 are unchanged",
                   "nothing is added to the shared deterministic calculation / units owner"):
        assert phrase in note, phrase


def test_t09_the_two_claims_have_exact_source_policy_and_limitation_linkage():
    group = _pack()["reference_fundamentals"][1]
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["applicable_gap_type"] == PHYSICAL_FEASIBILITY
    recs = {r["record_id"]: r for r in _provenance()}
    assert tuple(c["claim_id"] for c in group["claims"]) == ET_CLAIMS
    for claim in group["claims"]:
        assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation",
                                 "relationship", "source_ref", "source_use_policy_ref"]
        src, pol = ET_SOURCES[claim["claim_id"]]
        assert (claim["source_ref"], claim["source_use_policy_ref"]) == (src, pol)
        assert recs[src]["source_type"] == "government_reference_publication"
        assert recs[pol]["source_type"] == "source_use_policy"
        assert claim["claim_id"] in recs[src]["notes"]
    energy, units = group["claims"]
    assert energy["relationship"] == "E = P × t (constant P throughout t)"
    assert "remains constant throughout the stated duration t" in energy["fact"]
    assert "InventorAI's own algebraic restatement" in energy["fact"]
    assert "not an equation quoted verbatim from DOE" in energy["fact"]
    for phrase in ("never infers constant power", "No varying-power treatment", "average-power",
                   "integration formula", "battery capacity / runtime"):
        assert phrase in energy["limitation"], phrase
    assert units["relationship"] == "energy: J; power: W; duration: s; J = W · s"
    assert "not added as units, quantities, bindings or methods" in units["limitation"]


def test_t10_four_new_records_appended_after_pr007_with_exact_locations_and_honest_inspection():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    i = ids.index("electronics_electrical:PR007")
    assert tuple(ids[i + 1:i + 5]) == ET_RECORDS
    pre = [r for r in records if r["record_id"] not in ET_RECORDS + SENSING_RECORDS]
    assert _digest(pre) == _PRE_PROVENANCE_DIGEST                  # PR001–PR007 and others unchanged
    recs = {r["record_id"]: r for r in records}
    doe, nist, doe_pol, nist_pol = (recs[r] for r in ET_RECORDS)
    shape = sorted(recs["electronics_electrical:PR004"])
    assert all(sorted(r) == shape for r in (doe, nist, doe_pol, nist_pol))
    assert doe["standard_number"] == "DOE-HDBK-1010-92" and "Classical Physics" in doe["source_name"]
    for phrase in ("June 1992", "Module CP-05", "printed page 8", "PDF page 138", "\"Power\"", "status Archive"):
        assert phrase in doe["version_or_edition"], phrase
    assert doe["url"] == "https://www.energy.gov/sites/default/files/2026-04/DOE-HDBK-1010-92.pdf#page=138"
    assert "April 2016" not in json.dumps(doe) and "Canceled" not in json.dumps(doe)
    assert "NOT as current safety, regulatory or compliance authority" in doe["notes"]
    assert "NOT claimed that DOE wrote E = P × t verbatim" in doe["notes"]
    assert nist["standard_number"] == "NIST SP 811" and "Chapter 4" in nist["source_name"]
    for phrase in ("Table 1", "second, s", "Table 3", "joule, J", "watt, W, expressed as J/s",
                   "Appendix B.9", "watt second"):
        assert phrase in nist["version_or_edition"], phrase
    assert nist["url"] == ("https://www.nist.gov/pml/special-publication-811/"
                           "nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes")
    assert doe_pol["url"] == "https://www.energy.gov/web-policies"
    assert nist_pol["url"] == ("https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-"
                               "srd-data-software-and-technical-series-publications")
    for pol, target in ((doe_pol, "PR008"), (nist_pol, "PR009")):
        assert pol["notes"].startswith("SOURCE-USE COMPATIBILITY DISPOSITION (not a legal opinion")
        assert "electronics_electrical:" + target in pol["notes"]
    assert "no blanket claim is made" in doe_pol["notes"]
    assert "not treated as a blanket license for every NIST-hosted resource" in nist_pol["notes"]
    for r in (doe, nist, doe_pol, nist_pol):
        assert "2026-10-10" in r["version_or_edition"]
        assert "Lead-supplied inspection; not independently re-inspected by the executor" in r["version_or_edition"]


# ==========================================================================
# 4. no calculation, input, owner or state effect
# ==========================================================================
def test_t11_the_shared_calculation_and_unit_inventory_is_unchanged():
    artifact = json.loads(io.open(dc.ARTIFACT_PATH, encoding="utf-8").read())
    text = json.dumps(artifact, ensure_ascii=False)
    assert ET_GROUP not in text and "constant_power_energy" not in text
    tokens = set(re.findall(r'"unit_token":\s*"([^"]+)"', text))
    assert tokens == {"N", "mm", "W", "K/W", "K"}
    methods = set(re.findall(r'"method_id":\s*"([^"]+)"', text))
    assert methods == {"cap13:static_reactions_two_support",
                       "therm01:conduction_temperature_difference_single_path"}


def test_t12_no_input_control_numeric_result_or_state_change(client, monkeypatch):
    [block] = _ET_RE.findall(_html((PHYSICAL_FEASIBILITY, OPEN)))
    for control in ("<input", "<form", "<select", "<textarea", "<button"):
        assert control not in block, control
    assert not re.search(r"=\s*\d", _visible(block))
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((PHYSICAL_FEASIBILITY, OPEN))
    state = _live(sid)
    before = pickle.dumps(state)
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    _report(client, sid)
    _pdf_source(client, sid, monkeypatch)
    assert pickle.dumps(_live(sid)) == before
    readiness = derive_readiness(_live(sid))
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready


# ==========================================================================
# 5. EN / AR wording, restriction, attribution and exclusions
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
def test_t13_accepted_wording_is_verbatim_and_equations_are_identical(lang):
    texts = _et_texts(lang)
    for part, expected in ACCEPTED[lang].items():
        assert texts[part] == expected, (lang, part)
    assert sorted(texts) == sorted(
        ["TITLE", "INTRO", "SOURCE", "BOUNDARY"]
        + ["ITEM_%d_%s" % (n, p) for n in (1, 2) for p in ("TITLE", "LEAD", "EQUATION", "NOTE")])
    for part in ("ITEM_1_EQUATION", "ITEM_2_EQUATION"):
        assert texts[part] == _et_texts("en")[part]
        assert not re.search(r"[؀-ۿ‎‏‪-‮]", texts[part])


def test_t14_the_constant_power_condition_is_explicit_in_both_languages():
    assert "remains constant throughout" in _et_texts("en")["ITEM_1_LEAD"]
    assert "ثابتة طوال" in _et_texts("ar")["ITEM_1_LEAD"]
    assert "constant power" in _et_texts("en")["ITEM_1_NOTE"]
    assert "القدرة الثابتة" in _et_texts("ar")["ITEM_1_NOTE"]
    assert "has not established that power is constant" in _et_texts("en")["INTRO"]
    assert "لم يثبت InventorAI أن القدرة ثابتة" in _et_texts("ar")["INTRO"]


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_t15_exclusions_hold_and_disclaimer_words_are_negative_disclosures_only(lang):
    texts = _et_texts(lang)
    joined = " ".join(texts.values())
    for banned in ("Ah", "Wh", "kWh", "coulomb", "charge", "efficiency", "average", "integral",
                   "chemistry", "rating", "sizing"):
        assert not re.search(r"\b%s\b" % banned, joined, re.I), (lang, banned)
    for banned in ("Q = I", "3600", "∫", "شحن", "كولوم"):
        assert banned not in joined, (lang, banned)
    digits = {part: re.findall(r"\d+", text) for part, text in texts.items()}
    assert digits.pop("SOURCE") == ["1010", "92", "811", "4", "9"]
    assert not any(digits.values()), digits
    # "capacity" / "runtime" occur only inside the boundary's negative disclosure
    for part, text in texts.items():
        for word in (("capacity", "runtime") if lang == "en" else ("سعة البطارية", "مدة تشغيلها")):
            if word in text:
                assert part == "BOUNDARY", (part, word)
    assert ("determines no" in texts["BOUNDARY"]) if lang == "en" else ("لا تحدد" in texts["BOUNDARY"])


def test_t16_attribution_is_neutral_and_names_exactly_the_recorded_sources():
    en, ar = _et_texts("en")["SOURCE"], _et_texts("ar")["SOURCE"]
    for token in ("DOE-HDBK-1010-92", "Classical Physics", "SP 811"):
        assert token in en and token in ar, token
    assert "Chapter 4" in en and "Appendix B.9" in en
    assert "الفصل 4 والملحق B.9" in ar and "Chapter" not in ar and "Appendix" not in ar
    assert en.startswith("Reference source material:") and ar.startswith("مواد مرجعية:")
    for word in ("endorse", "approved", "certified", "recommended"):
        assert word not in en.lower(), word
    assert "archived; fundamentals reference only" in en
    assert "DOE-HDBK-1011" not in en


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_t17_report_and_pdf_carry_the_group_with_attribution_and_limitations(client, monkeypatch, lang):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, PARTIAL))
    page = _report(client, sid, lang=lang)
    if lang == "ar":
        assert 'dir="rtl"' in page
    [block] = _ET_RE.findall(page)
    visible = _visible(block)
    for part, text in _et_texts(lang).items():
        assert text in visible, (lang, part)
    assert block.count('<bdi class="cap01-fund-equation" dir="ltr"') == 2
    source = _pdf_source(client, sid, monkeypatch)
    assert _ET_RE.findall(source) == [block]
    assert [g for g in _ANY_FUND_RE.findall(source) if g != "sensing-value-threshold-reference-v1"] == [
        "basic-electrical-reference-v1", "electrical-energy-time-reference-v1"]


def test_t18_session_page_carries_no_group(client):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((PHYSICAL_FEASIBILITY, OPEN))
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "cap01-fund" not in page and "E = P × t" not in page
    assert _et_texts("en")["TITLE"] not in page


def test_t19_the_note_separation_is_scoped_to_the_new_group_only():
    for pdf in (False, True):
        html = _html((PHYSICAL_FEASIBILITY, OPEN), pdf=pdf)
        [et] = _ET_RE.findall(html)
        assert et.count('data-cap01-fund-equation style="white-space:nowrap">') == 2
        assert et.count('data-cap01-fund-item-note style="display:block;margin-top:2px">') == 2
        # the original group's markup carries no new attribute
        [base] = _base_blocks(html)
        assert "white-space:nowrap" not in base and "display:block" not in base
        assert base.count('data-cap01-fund-equation>') == 3
        assert base.count('data-cap01-fund-item-note>') == 3
    mech = _html((PHYSICAL_FEASIBILITY, OPEN), domain="mechanical")
    assert "white-space:nowrap" not in mech.split('class="cap01-fundamentals"', 1)[1].split("</ul>", 1)[0]
