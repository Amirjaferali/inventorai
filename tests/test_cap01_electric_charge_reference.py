# -*- coding: utf-8 -*-
"""ELECTRICAL-CHARGE-AMPERE-HOUR-REFERENCE-01 — the third, separately authorized Electrical
reference-fundamentals group of the Electronics PHYSICAL_FEASIBILITY context (Stage 18 /
CAP-01 bounded extension; NOT Battery / BMS capability).

What is pinned: when, and only when, the trusted canonical domain is
``electronics_electrical`` AND the EXACT canonical ``PHYSICAL_FEASIBILITY`` gap is in EXACT
state OPEN or PARTIAL, the report / deliverable and the PDF show the existing basic and
energy-time groups and then ONE further group, electric_charge_reference_v1, of exactly
three bounded reference claims: current as the rate of electric charge flow with
Q = I × t ONLY for a constant current, C = A · s, and 1 A · h = 3.6 × 10³ C with the
milli prefix — and that a value in A · h or mA · h is charge, not energy.

Boundaries proven here: exact binding (domain + gap id + lifecycle state only), with no
text, keyword or signal access; the group is all-or-nothing on its own copy; the pack and
provenance changes are additions only; PR018–PR021 carry the Lead-supplied passage
locations, observations, edition boundaries and source-use dispositions, and separate
source facts from InventorAI derivations; nothing reaches the shared calculation / units
owner; the EN / AR wording is pinned, keeps the constant-current condition and states that
a charge value alone cannot determine battery runtime — with no runtime, energy,
delivered-charge, charging, sizing or safety estimate.
"""
import hashlib
import io
import json
import os
import pickle
import re

import pytest

from engine import deterministic_calculation as dc
from engine.derived_readiness import derive_readiness
from engine.domain_rules import get_active_rules
from engine.idea_state import (
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, MECHANISM_COMPLETENESS, OPEN, PARTIAL,
    PHYSICAL_FEASIBILITY)
from web import cap01_guidance, ui_text
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, ELEC_SEED, _start, _live,
)
from tests.test_stage18_cap01_bounded_guidance import _mask_csrf
from tests.test_cap01_mechanical_open_gap_context import (
    FUND_GROUP as MECH_FUND_GROUP, _gaps, _pdf_source, _report, _visible)
from tests.test_cap01_electrical_reference_fundamentals import FUND_GROUP as BASE_GROUP, _blocks as _base_blocks
from tests.test_cap01_electrical_energy_time_reference import (
    ET_CLAIMS, ET_GROUP, _ANY_FUND_RE, _ET_RE, _equations, _groups, _html)
from tests.cap01_charge_addition import (
    CHARGE_CLAIMS as CLAIMS, CHARGE_EQUATIONS as EQUATIONS, CHARGE_GROUP as GROUP, CHARGE_NOTE as NOTE,
    CHARGE_RECORDS as RECORDS, CHARGE_ROW as ROW, CHARGE_SLUG as SLUG, without_charge_addition)
# MEASUREMENT-PLAN-GUIDANCE-01 (C1) later appended ONE CAP-09-page-only guidance group to the pack (never a
# report context row); excluded here likewise (tests/cap01_measurement_guidance_addition.py).
from tests.cap01_measurement_guidance_addition import (
    MGUIDE_GROUP, MGUIDE_RECORDS, without_measurement_guidance_addition)
# MEASUREMENT-CONDITIONS-AWARENESS-01 later appended ONE further CAP-09-page-only guidance group (never a
# report context row); excluded here likewise (tests/cap01_measurement_conditions_addition.py).
from tests.cap01_measurement_conditions_addition import (
    MCOND_GROUP, MCOND_RECORDS, without_measurement_conditions_addition)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")

DOMAIN = "electronics_electrical"
PREFIX = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_" + PHYSICAL_FEASIBILITY + "_CHARGE_FUNDAMENTALS_"
ET_ROW = (ET_GROUP, ET_CLAIMS, "ENERGY_TIME_FUNDAMENTALS_")
SOURCES = {
    "charge_current_time_reference": ("electronics_electrical:PR018", "electronics_electrical:PR019"),
    "charge_unit_discipline": ("electronics_electrical:PR020", "electronics_electrical:PR021"),
    "ampere_hour_charge_unit": ("electronics_electrical:PR020", "electronics_electrical:PR021"),
}
# Canonical digests at base 31fef0c7132c7e558a97a1d3545e254dd600f7db: the whole
# Electronics pack, and the whole provenance record list, before this addition.
_PRE_PACK_DIGEST = "2bc7a4a4c4210333d88690bff573893db189a83ced4422941c95aa00e81224e8"
_PRE_PROVENANCE_DIGEST = "c0c42d1cc32e12401c89902207def5afbca4810316260fef8d9ba6d8f053bf5f"

ACCEPTED = {
    "en": {
        "TITLE": "Electric charge, current and time",
        "INTRO": "Reference information only. It explains units that appear on many batteries. InventorAI "
                 "has not evaluated your battery, and has not established that the current is constant or "
                 "that these relationships apply to your invention.",
        "ITEM_1_TITLE": "Charge at constant current",
        "ITEM_1_LEAD": "Electric current is the rate of electric charge flow: a current of one ampere means one "
                       "coulomb of charge passes a given point every second. When the current I remains constant "
                       "throughout a time interval t, the charge Q that flows is:",
        "ITEM_1_EQUATION": "Q = I × t",
        "ITEM_1_NOTE": "Q is the charge that flows, I is the constant current, and t is the duration. This holds "
                       "only while the current stays constant.",
        "ITEM_2_TITLE": "The unit of electric charge",
        "ITEM_2_LEAD": "The SI unit of electric charge is the coulomb C. In SI base units:",
        "ITEM_2_EQUATION": "C = A · s",
        "ITEM_2_NOTE": "A is the ampere and s is the second.",
        "ITEM_3_TITLE": "Ampere-hours and milliampere-hours",
        "ITEM_3_LEAD": "The ampere-hour A · h is also a unit of electric charge:",
        "ITEM_3_EQUATION": "1 A · h = 3.6 × 10³ C",
        "ITEM_3_NOTE": "The prefix milli means 10⁻³, one-thousandth, so one milliampere-hour is one-thousandth "
                       "of an ampere-hour. A value in ampere-hours or milliampere-hours, also written Ah or mAh, "
                       "is an amount of charge, not an amount of energy; energy is measured in joules J.",
        "SOURCE": "Reference source material: U.S. Department of Energy — Electrical Science, "
                  "DOE-HDBK-1011/1-92 (archived; fundamentals reference only); NIST Guide to the SI, SP 811 "
                  "Chapter 4 and Appendix B.9.",
        "BOUNDARY": "A charge value alone does not tell you how long a battery will last: because current is the "
                    "rate of electric charge flow, how long a charge lasts also depends on the current drawn, "
                    "which may change during use. This group performs no project-specific calculation and does "
                    "not estimate battery runtime, energy, state of charge or how much charge a particular "
                    "battery can deliver, and it makes no sizing, charging, compatibility or safety assessment.",
    },
    "ar": {
        "TITLE": "الشحنة الكهربائية والتيار والزمن",
        "INTRO": "هذه معلومات مرجعية فقط، تشرح وحداتٍ تظهر على كثير من البطاريات. لم يقيّم InventorAI "
                 "بطاريتك، ولم يثبت أن التيار ثابت أو أن هذه العلاقات تنطبق على اختراعك.",
        "ITEM_1_TITLE": "الشحنة عند تيار ثابت",
        "ITEM_1_LEAD": "التيار الكهربائي هو معدل مرور الشحنة الكهربائية: تيار شدته أمبير واحد يعني مرور كولوم "
                       "واحد من الشحنة عبر نقطة معيّنة في كل ثانية. عندما يبقى التيار I ثابتًا طوال مدة زمنية t، "
                       "تكون الشحنة المارّة Q وفق العلاقة:",
        "ITEM_1_EQUATION": "Q = I × t",
        "ITEM_1_NOTE": "ترمز Q إلى الشحنة المارّة، وI إلى التيار الثابت، وt إلى المدة الزمنية. لا تصحّ هذه "
                       "العلاقة إلا ما دام التيار ثابتًا.",
        "ITEM_2_TITLE": "وحدة الشحنة الكهربائية",
        "ITEM_2_LEAD": "وحدة الشحنة الكهربائية في النظام الدولي للوحدات هي الكولوم C، وتُكتب بالوحدات الأساسية "
                       "هكذا:",
        "ITEM_2_EQUATION": "C = A · s",
        "ITEM_2_NOTE": "ترمز A إلى الأمبير، وs إلى الثانية.",
        "ITEM_3_TITLE": "الأمبير-ساعة والميلي أمبير-ساعة",
        "ITEM_3_LEAD": "الأمبير-ساعة A · h وحدة للشحنة الكهربائية أيضًا:",
        "ITEM_3_EQUATION": "1 A · h = 3.6 × 10³ C",
        "ITEM_3_NOTE": "البادئة «ميلي» تعني جزءًا من ألف، فالميلي أمبير-ساعة جزء من ألف من "
                       "الأمبير-ساعة. والقيمة المكتوبة بالأمبير-ساعة أو بالميلي أمبير-ساعة، وتُكتب أيضًا Ah أو "
                       "mAh، كميةُ شحنة لا كميةُ طاقة؛ فالطاقة تُقاس بالجول J.",
        "SOURCE": "مواد مرجعية: وزارة الطاقة الأمريكية (U.S. Department of Energy) — Electrical Science، "
                  "DOE-HDBK-1011/1-92 (مؤرشف؛ مرجع للأساسيات فقط)؛ ودليل NIST للنظام الدولي للوحدات، "
                  "SP 811 الفصل 4 والملحق B.9.",
        "BOUNDARY": "رقم الشحنة وحده لا يحدّد كم ستدوم البطارية: فلأن التيار هو معدل مرور الشحنة الكهربائية، "
                    "تعتمد المدة أيضًا على التيار المسحوب، وقد يتغيّر أثناء الاستخدام. لا تُجري هذه المجموعة "
                    "حسابًا خاصًا بمشروعك، ولا تقدّر مدة تشغيل البطارية أو طاقتها أو حالة شحنها أو كمية الشحنة "
                    "التي تستطيع بطارية معيّنة توفيرها، ولا تقدّم أي تقييم للحجم أو الشحن أو التوافق أو السلامة.",
    },
}

_CHARGE_RE = re.compile(
    r'<div class="cap01-fundamentals" data-cap01-fundamentals="electric-charge-reference-v1">'
    r'.*?\n      </div>', re.S)


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


def _texts(lang):
    return {k[len(PREFIX):]: ui_text.UI_STRINGS[k][lang]
            for k in sorted(ui_text.UI_STRINGS) if k.startswith(PREFIX)}


# ==========================================================================
# 1. binding, order and isolation
# ==========================================================================
@pytest.mark.parametrize("status", (OPEN, PARTIAL))
def test_c01_pf_open_or_partial_renders_the_group_third_with_its_three_claims(status):
    groups = _groups((PHYSICAL_FEASIBILITY, status))[PHYSICAL_FEASIBILITY]
    assert [g["group_id"] for g in groups] == [BASE_GROUP, ET_GROUP, GROUP]
    group = groups[2]
    assert group["prose_only"] is False
    assert tuple(c["claim_id"] for c in group["claims"]) == CLAIMS
    html = _html((PHYSICAL_FEASIBILITY, status))
    assert _ANY_FUND_RE.findall(html) == ["basic-electrical-reference-v1",
                                          "electrical-energy-time-reference-v1", SLUG]
    [block] = _CHARGE_RE.findall(html)
    assert _equations(block) == list(EQUATIONS)


@pytest.mark.parametrize("status", (CLOSED, ACCEPTED_RISK, "open", "PARTIALLY", "", None))
def test_c02_ineligible_states_render_no_group(status):
    assert _groups((PHYSICAL_FEASIBILITY, status)) is None
    assert SLUG not in _html((PHYSICAL_FEASIBILITY, status))


def test_c03_other_gaps_domains_and_text_grant_no_access():
    groups = _groups((MECHANISM_COMPLETENESS, OPEN), (BOUNDARY_AMBIGUITY, PARTIAL))
    assert groups and all(GROUP not in [g["group_id"] for g in v] for v in groups.values())
    mech = _groups((PHYSICAL_FEASIBILITY, OPEN), domain="mechanical")[PHYSICAL_FEASIBILITY]
    assert [g["group_id"] for g in mech] == [MECH_FUND_GROUP]
    assert SLUG not in _html((PHYSICAL_FEASIBILITY, OPEN), domain="mechanical")
    # battery / charge words in the inventor's text never add, remove or reorder a group
    battery = "A 5000 mAh battery pack with a BMS; runtime 4 hours at 1.2 A; capacity in Ah and Wh; coulomb"
    for pairs in (((PHYSICAL_FEASIBILITY, CLOSED),), ((MECHANISM_COMPLETENESS, OPEN),)):
        assert SLUG not in _html(*pairs, idea_text=battery)
    html = _html((PHYSICAL_FEASIBILITY, OPEN), idea_text=battery)
    assert _mask_csrf(html) == _mask_csrf(_html((PHYSICAL_FEASIBILITY, OPEN)))


def test_c04_the_binding_is_one_fixed_row_appended_after_the_energy_time_row():
    row = cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS[(DOMAIN, PHYSICAL_FEASIBILITY)]
    assert row == (ET_ROW, ROW)
    assert ROW == (GROUP, CLAIMS, "CHARGE_FUNDAMENTALS_")
    assert sorted(cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS) == [
        (DOMAIN, MECHANISM_COMPLETENESS), (DOMAIN, PHYSICAL_FEASIBILITY)]
    assert GROUP not in cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS
    src = io.open(os.path.join(_ROOT, "web", "cap01_guidance.py"), encoding="utf-8").read()
    start = src.index("CAP01_GAP_FUNDAMENTALS_EXTENSIONS = {")
    table = src[start:src.index("\n}\n", start)]
    for token in ("import", "glob", "listdir", "json.load", "reference_fundamentals", "idea_text"):
        assert token not in table, token


# ==========================================================================
# 2. the group is all-or-nothing on its own copy
# ==========================================================================
@pytest.mark.parametrize("part", ("TITLE", "INTRO", "SOURCE", "BOUNDARY", "ITEM_1_LEAD", "ITEM_2_EQUATION",
                                  "ITEM_3_NOTE", "ITEM_3_TITLE"))
def test_c05_missing_charge_copy_suppresses_only_this_group(monkeypatch, part):
    monkeypatch.delitem(ui_text.UI_STRINGS, PREFIX + part)
    groups = _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]
    assert [g["group_id"] for g in groups] == [BASE_GROUP, ET_GROUP]
    html = _html((PHYSICAL_FEASIBILITY, OPEN))
    assert SLUG not in html
    for equation in EQUATIONS:
        assert equation not in html


def test_c06_missing_earlier_copy_never_removes_this_group(monkeypatch):
    monkeypatch.delitem(ui_text.UI_STRINGS,
                        "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_ENERGY_TIME_FUNDAMENTALS_SOURCE")
    monkeypatch.delitem(ui_text.UI_STRINGS,
                        "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_NOTE")
    groups = _groups((PHYSICAL_FEASIBILITY, OPEN))[PHYSICAL_FEASIBILITY]
    assert [g["group_id"] for g in groups] == [GROUP]
    assert _ANY_FUND_RE.findall(_html((PHYSICAL_FEASIBILITY, OPEN))) == [SLUG]


# ==========================================================================
# 3. pack and provenance: additions only, exact mappings
# ==========================================================================
def test_c07_the_pack_change_is_exactly_one_group_and_one_note():
    pack = _pack()
    assert _digest(without_charge_addition(without_measurement_guidance_addition(
        without_measurement_conditions_addition(pack)))) == _PRE_PACK_DIGEST
    # This group is the last REPORT group; the later CAP-09-only guidance groups follow it in the pack.
    assert [g["group_id"] for g in pack["reference_fundamentals"]][-3:] == [GROUP, MGUIDE_GROUP, MCOND_GROUP]
    note = pack["_governance_notes"][NOTE]
    for phrase in ("ELECTRICAL-CHARGE-AMPERE-HOUR-REFERENCE-01", "NOT Battery / BMS capability", "inert",
                   "exactly three bounded reference claims", "ONLY when the current I remains constant",
                   "PR018", "PR020", "PR019", "PR021", "PR001–PR017 are unchanged",
                   "after electrical_energy_time_reference_v1",
                   "nothing is added to the shared deterministic calculation / units owner",
                   "No Wh, energy-from-charge relation, runtime or duration estimate"):
        assert phrase in note, phrase


def test_c08_the_three_claims_have_exact_source_policy_and_limitation_linkage():
    [group] = [g for g in _pack()["reference_fundamentals"] if g["group_id"] == GROUP]
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert (group["group_id"], group["applicable_gap_type"]) == (GROUP, PHYSICAL_FEASIBILITY)
    recs = {r["record_id"]: r for r in _provenance()}
    assert tuple(c["claim_id"] for c in group["claims"]) == CLAIMS
    for claim in group["claims"]:
        assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation",
                                 "relationship", "source_ref", "source_use_policy_ref"]
        assert claim["applicable_gap_type"] == PHYSICAL_FEASIBILITY
        src, pol = SOURCES[claim["claim_id"]]
        assert (claim["source_ref"], claim["source_use_policy_ref"]) == (src, pol)
        assert recs[src]["source_type"] == "government_reference_publication"
        assert recs[pol]["source_type"] == "source_use_policy"
        assert claim["claim_id"] in recs[src]["notes"]
    charge, unit, ampere_hour = group["claims"]
    assert charge["relationship"] == "Q = I × t (constant I throughout t)"
    for phrase in ("rate of electric charge flow", "remains constant throughout the stated duration t",
                   "InventorAI's own algebraic restatement", "not an equation quoted from DOE",
                   "the rate wording is InventorAI's own paraphrase"):
        assert phrase in charge["fact"], phrase
    for phrase in ("never infers constant current", "No varying-current treatment", "average-current",
                   "integration formula", "never rearranged into a duration or runtime estimate",
                   "state of charge", "delivered charge"):
        assert phrase in charge["limitation"], phrase
    assert unit["relationship"] == "electric charge: C; C = A · s"
    assert "expressed in SI base units as s · A" in unit["fact"]
    assert "not added as a unit, quantity, binding or method" in unit["limitation"]
    assert ampere_hour["relationship"] == "1 A · h = 3.6 × 10³ C; milli (m) = 10⁻³; 1 mA · h = 10⁻³ A · h"
    for phrase in ("1 A · h = 3.6 × 10³ C", "InventorAI's arithmetic from the prefix definition, not a NIST "
                   "table row", "not an amount of energy", "electronics_electrical:PR009",
                   "InventorAI's restatement from the coulomb and joule unit facts"):
        assert phrase in ampere_hour["fact"], phrase
    for phrase in ("single conversion-factor reference only", "NOT added as units, conversions",
                   "A charge value alone does not determine how long a battery lasts", "records notation only"):
        assert phrase in ampere_hour["limitation"], phrase


def test_c09_four_records_appended_after_pr017_and_every_other_record_unchanged():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids))
    i = ids.index("electronics_electrical:PR017")
    assert tuple(ids[i + 1:i + 5]) == RECORDS
    assert tuple(ids[i + 5:i + 7]) == MGUIDE_RECORDS and tuple(ids[i + 7:i + 9]) == MCOND_RECORDS
    assert ids[i + 9] == "mechanical:PR001"
    assert _digest([r for r in records if r["record_id"] not in RECORDS + MGUIDE_RECORDS + MCOND_RECORDS]) == _PRE_PROVENANCE_DIGEST
    recs = {r["record_id"]: r for r in records}
    shape = sorted(recs["electronics_electrical:PR004"])
    assert all(sorted(recs[r]) == shape for r in RECORDS)
    assert all(recs[r]["pack_id"] == DOMAIN and recs[r]["tier"] == 1 and recs[r]["cross_domain_usage"] == []
               for r in RECORDS)


def test_c10_the_doe_records_carry_the_passage_status_and_the_contractor_caveat():
    recs = {r["record_id"]: r for r in _provenance()}
    doe, use = recs["electronics_electrical:PR018"], recs["electronics_electrical:PR019"]
    assert doe["standard_number"] == "DOE-HDBK-1011/1-92" and doe["jurisdiction"] == "US"
    assert "Electrical Science, Volume 1 of 4" in doe["source_name"]
    assert doe["url"] == "https://www.energy.gov/sites/default/files/2026-04/DOE-HDBK-1011-92_VOL1.pdf"
    for phrase in ("Module ES-01", "\"Electrical Terminology\"", "\"Current\"", "printed page ES-01 page 10",
                   "PDF page index 33", "ARCHIVE — Canceled, effective April 2016", "2026-10-12",
                   "Lead-supplied inspection; not independently re-inspected by the executor"):
        assert phrase in doe["version_or_edition"], phrase
    for phrase in ("NOT claimed that DOE wrote Q = I × t", "no passage-specific third-party copyright notice",
                   "EG&G Idaho, Inc.", "general bibliography that includes commercial publications",
                   "NOT a blanket government-authorship determination",
                   "NOT as current safety, regulatory or compliance authority",
                   "historical fundamentals reference", "no DOE endorsement",
                   "electronics_electrical:PR004 (the same handbook, other passages and claims) is unchanged",
                   "Source-use disposition: electronics_electrical:PR019"):
        assert phrase in doe["notes"], phrase
    assert use["url"] == "https://www.energy.gov/web-policies"
    assert use["notes"].startswith("SOURCE-USE COMPATIBILITY DISPOSITION (not a legal opinion")
    for phrase in ("electronics_electrical:PR018", "ONLY", "no blanket claim is made",
                   "no comprehensive authorship verification is claimed", "EG&G Idaho, Inc.",
                   "bibliography of commercial publications is not used",
                   "Reference source material: U.S. Department of Energy — Electrical Science, DOE-HDBK-1011/1-92",
                   "no statement or implication that DOE endorses"):
        assert phrase in use["notes"], phrase
    assert "2026-10-12" in use["version_or_edition"]


def test_c11_the_nist_records_use_the_online_edition_and_never_the_2008_pdf():
    recs = {r["record_id"]: r for r in _provenance()}
    nist, use = recs["electronics_electrical:PR020"], recs["electronics_electrical:PR021"]
    assert nist["standard_number"] == "NIST SP 811" and "online edition" in nist["source_name"]
    assert nist["url"] == ("https://www.nist.gov/pml/special-publication-811/"
                           "nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes")
    for phrase in ("online (web) edition", "Table 3", "electric charge, coulomb, C, expressed in SI base units "
                   "as s · A", "Table 5", "milli, m, 10⁻³", "Appendix B.9",
                   "nist-guide-si-appendix-b9", "ampere hour (A · h) row: 1 A · h = 3.6 × 10³ C",
                   "2026-10-12", "later updates relative to the 2008 PDF edition", "10.6028/NIST.SP.811e2008",
                   "NOT attributed to the 2008 PDF edition"):
        assert phrase in nist["version_or_edition"], phrase
    for phrase in ("charge_unit_discipline", "ampere_hour_charge_unit", "ONE conversion factor",
                   "InventorAI's arithmetic from the prefix definition, not a NIST table row",
                   "joule row already recorded in electronics_electrical:PR009",
                   "no passage-specific third-party attribution or copyright restriction",
                   "NOT a comprehensive authorship verification", "No conversion table",
                   "NOT added as units, conversions, quantities, bindings or methods",
                   "no endorsement implied", "Source-use disposition: electronics_electrical:PR021"):
        assert phrase in nist["notes"], phrase
    assert use["url"] == "https://www.nist.gov/nist-research-library/nist-publications"
    assert "electronics_electrical:PR011" in use["version_or_edition"] and "2026-10-12" in use["version_or_edition"]
    for phrase in ("electronics_electrical:PR020", "ONLY", "not treated as a blanket license",
                   "no blanket public-domain status or comprehensive authorship verification is claimed",
                   "no statement or implication that NIST endorses"):
        assert phrase in use["notes"], phrase


# ==========================================================================
# 4. no calculation, input, owner or state effect
# ==========================================================================
def test_c12_the_shared_calculation_and_unit_inventory_is_unchanged():
    artifact = json.loads(io.open(dc.ARTIFACT_PATH, encoding="utf-8").read())
    text = json.dumps(artifact, ensure_ascii=False)
    assert GROUP not in text and "ampere hour" not in text.lower() and "coulomb" not in text.lower()
    assert set(re.findall(r'"unit_token":\s*"([^"]+)"', text)) == {"N", "mm", "W", "K/W", "K"}
    assert set(re.findall(r'"method_id":\s*"([^"]+)"', text)) == {
        "cap13:static_reactions_two_support", "therm01:conduction_temperature_difference_single_path"}
    assert get_active_rules(DOMAIN) == [
        "PHYSICAL_PRINCIPLE_REQUIRED", "POWER_ACKNOWLEDGMENT_IF_ENERGY", "NO_PLATFORM_SPECIFIC_NAMING"]


def test_c13_no_input_control_numeric_result_or_state_change(client, monkeypatch):
    [block] = _CHARGE_RE.findall(_html((PHYSICAL_FEASIBILITY, OPEN)))
    for control in ("<input", "<form", "<select", "<textarea", "<button"):
        assert control not in block, control
    # the only "= <number>" is the one source conversion factor
    assert re.findall(r"=\s*\d[\d.]*", _visible(block)) == ["= 3.6"]
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
# 5. EN / AR wording, conditions, attribution and exclusions
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
def test_c14_accepted_wording_is_verbatim_and_equations_are_identical(lang):
    texts = _texts(lang)
    assert sorted(texts) == sorted(
        ["TITLE", "INTRO", "SOURCE", "BOUNDARY"]
        + ["ITEM_%d_%s" % (n, p) for n in (1, 2, 3) for p in ("TITLE", "LEAD", "EQUATION", "NOTE")])
    for part, expected in ACCEPTED[lang].items():
        assert texts[part] == expected, (lang, part)
    for n, equation in enumerate(EQUATIONS, 1):
        assert texts["ITEM_%d_EQUATION" % n] == equation
        assert not re.search(r"[\u0600-\u06ff\u200e\u200f\u202a-\u202e\u2066-\u2069]", equation)


def test_c15_the_rate_wording_and_constant_current_condition_hold_in_both_languages():
    en, ar = _texts("en"), _texts("ar")
    assert "rate of electric charge flow" in en["ITEM_1_LEAD"] and "rate of electric charge flow" in en["BOUNDARY"]
    assert "معدل مرور الشحنة الكهربائية" in ar["ITEM_1_LEAD"] and "معدل مرور الشحنة الكهربائية" in ar["BOUNDARY"]
    assert "remains constant throughout" in en["ITEM_1_LEAD"] and "only while the current stays constant" in \
        en["ITEM_1_NOTE"]
    assert "ثابتًا طوال" in ar["ITEM_1_LEAD"] and "إلا ما دام التيار ثابتًا" in ar["ITEM_1_NOTE"]
    assert "has not established that the current is constant" in en["INTRO"]
    assert "لم يثبت أن التيار ثابت" in ar["INTRO"]
    assert "has not evaluated your battery" in en["INTRO"] and "لم يقيّم InventorAI بطاريتك" in ar["INTRO"]


def test_c16_charge_is_not_energy_and_a_charge_value_cannot_give_runtime():
    en, ar = _texts("en"), _texts("ar")
    assert "is an amount of charge, not an amount of energy" in en["ITEM_3_NOTE"]
    assert "كميةُ شحنة لا كميةُ طاقة" in ar["ITEM_3_NOTE"]
    assert "Ah or mAh" in en["ITEM_3_NOTE"] and "Ah أو mAh" in ar["ITEM_3_NOTE"]
    # milli = 10⁻³: the English note shows the power of ten; the Arabic note states the same value in words,
    # because an inline superscript exponent is visually reordered inside right-to-left text
    assert "10⁻³, one-thousandth" in en["ITEM_3_NOTE"]
    assert "تعني جزءًا من ألف" in ar["ITEM_3_NOTE"] and "10" not in ar["ITEM_3_NOTE"]
    assert en["BOUNDARY"].startswith("A charge value alone does not tell you how long a battery will last")
    assert ar["BOUNDARY"].startswith("رقم الشحنة وحده لا يحدّد كم ستدوم البطارية")
    assert "also depends on the current drawn" in en["BOUNDARY"]
    assert "تعتمد المدة أيضًا على التيار المسحوب" in ar["BOUNDARY"]


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_c17_no_runtime_energy_or_charge_estimate_and_digits_only_where_admitted(lang):
    texts = _texts(lang)
    joined = " ".join(texts.values())
    for banned in ("Wh", "kWh", "watt-hour", "watt hour", "C-rate", "Peukert", "efficiency", "chemistry",
                   "lithium", "voltage"):
        assert not re.search(r"\b%s\b" % re.escape(banned), joined, re.I), (lang, banned)
    for banned in ("t = Q", "Q / I", "Q/I", "E = Q", "= Q ×", "÷", "∫", "%", "3600", "3 600", "18000"):
        assert banned not in joined, (lang, banned)
    digits = {part: re.findall(r"\d+", text) for part, text in texts.items()}
    assert digits.pop("SOURCE") == ["1011", "1", "92", "811", "4", "9"]
    assert digits.pop("ITEM_3_EQUATION") == ["1", "3", "6", "10"]
    assert digits.pop("ITEM_3_NOTE") == (["10"] if lang == "en" else [])
    assert not any(digits.values()), digits
    # runtime / energy / delivered-charge words occur only in the negative disclosures and the
    # charge-versus-energy note
    words = (("runtime", "state of charge", "deliver", "sizing", "charging", "safety")
             if lang == "en" else ("مدة تشغيل", "حالة شحنها", "توفيرها", "للحجم", "الشحن أو", "السلامة"))
    for part, text in texts.items():
        for word in words:
            if word in text:
                assert part == "BOUNDARY", (lang, part, word)
    # (the source line names the U.S. Department of Energy, «وزارة الطاقة», and is set aside)
    energy = "energy" if lang == "en" else "طاق"
    assert {part for part, text in texts.items() if energy in text and part != "SOURCE"} == {
        "ITEM_3_NOTE", "BOUNDARY"}


def test_c18_attribution_is_neutral_and_names_exactly_the_recorded_sources():
    en, ar = _texts("en")["SOURCE"], _texts("ar")["SOURCE"]
    for token in ("U.S. Department of Energy", "Electrical Science", "DOE-HDBK-1011/1-92", "NIST", "SP 811"):
        assert token in en and token in ar, token
    assert "(archived; fundamentals reference only)" in en and "(مؤرشف؛ مرجع للأساسيات فقط)" in ar
    assert "Chapter 4 and Appendix B.9" in en and "الفصل 4 والملحق B.9" in ar
    assert en.startswith("Reference source material:") and ar.startswith("مواد مرجعية:")
    joined = " ".join(list(_texts("en").values()) + list(_texts("ar").values())).lower()
    for word in ("endorse", "approved", "certified", "recommended", "according to doe", "doe confirms",
                 "2008", "dhbk-1010", "doe-hdbk-1010", "logo", "شعار", "معتمد من"):
        assert word not in joined, word
    for part, text in _texts("en").items():
        if "DOE" in text or "NIST" in text or "Department of Energy" in text:
            assert part == "SOURCE", part


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_c19_report_and_pdf_carry_the_group_with_ltr_equations(client, monkeypatch, lang):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, PARTIAL))
    page = _report(client, sid, lang=lang)
    if lang == "ar":
        assert 'dir="rtl"' in page
    [block] = _CHARGE_RE.findall(page)
    visible = _visible(block)
    for part, text in _texts(lang).items():
        assert text in visible, (lang, part)
    assert block.count('<bdi class="cap01-fund-equation" dir="ltr"') == 3
    assert page.index('data-cap01-fundamentals="electrical-energy-time-reference-v1"') < \
        page.index('data-cap01-fundamentals="%s"' % SLUG)
    source = _pdf_source(client, sid, monkeypatch)
    assert _CHARGE_RE.findall(source) == [block]


def test_c20_session_page_carries_no_group(client):
    sid = _start(client, seed=ELEC_SEED, domain=DOMAIN)
    _live(sid).gaps = _gaps((PHYSICAL_FEASIBILITY, OPEN))
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert SLUG not in page and "Q = I × t" not in page
    assert _texts("en")["TITLE"] not in page


def test_c21_equation_and_note_separation_extends_to_this_group_only():
    for pdf in (False, True):
        html = _html((PHYSICAL_FEASIBILITY, OPEN), pdf=pdf)
        [block] = _CHARGE_RE.findall(html)
        assert block.count('data-cap01-fund-equation style="white-space:nowrap">') == 3
        assert block.count('data-cap01-fund-item-note style="display:block;margin-top:2px">') == 3
        [et] = _ET_RE.findall(html)
        assert et.count('data-cap01-fund-equation style="white-space:nowrap">') == 2
        [base] = _base_blocks(html)
        assert "white-space:nowrap" not in base and "display:block" not in base
    mech = _html((PHYSICAL_FEASIBILITY, OPEN), domain="mechanical")
    assert "white-space:nowrap" not in mech.split('class="cap01-fundamentals"', 1)[1].split("</ul>", 1)[0]
