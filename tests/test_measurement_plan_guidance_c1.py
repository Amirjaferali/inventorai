# -*- coding: utf-8 -*-
"""MEASUREMENT-PLAN-GUIDANCE-01 (C1) — ONE visible, optional measurement-planning
guidance element on the CAP-09 measurement-planning page: before describing HOW an
experiment will be measured or checked, identify WHAT is to be observed — a quantity
that can be measured and expressed with an appropriate unit, or a condition / state
that can be observed without a numerical measurement.

Proves: the ONE admitted claim is declared in the Electronics pack with claim-specific
provenance (electronics_electrical:PR022 — NIST Technical Note 1900, Section 2, Note
2.1, Lead-supplied inspection — and PR023, the claim-specific rights disposition that
does not broaden PR015); the pack and provenance changes are additions only; the
guidance is built by the existing group builder under its own copy namespace and is
NOT a report / PDF gap-context group (the extension table, the report eligibility and
the report group count are unchanged); eligibility is ONLY the trusted durable root
domain, exactly ``electronics_electrical`` — a Mechanical root, a Mechanical-focus
integrated project, an unreadable domain and an unavailable page show nothing, and
the gap state does not matter; the guidance is visible (not collapsed) beside the
measurement-method introduction with its boundary, and its source / adaptation /
no-endorsement notice is one click away in the same block; every render path of the
page respects the rule; it adds no input, reads no inventor text and writes nothing;
the PR #816 reference panel is unchanged; EN / AR copy is pinned.
Synthetic invention data only.
"""
import hashlib
import html as _html
import json
import os
import pickle
import re
import sqlite3

import pytest

import web.app as webapp
from engine.idea_state import MECHANISM_COMPLETENESS, OPEN, PHYSICAL_FEASIBILITY
from web import cap01_guidance, ui_text
from tests.cap01_measurement_guidance_addition import (
    MGUIDE_CLAIM as CLAIM, MGUIDE_CLAIMS as CLAIMS, MGUIDE_GROUP as GROUP, MGUIDE_NOTE as NOTE,
    MGUIDE_RECORDS as RECORDS, MGUIDE_SLUG as SLUG, MGUIDE_STEM as STEM,
    without_measurement_guidance_addition)
from tests.test_28t1_measurement_planning_reference import (
    GROUPS as REFERENCE_GROUPS, _elec, _group_blocks, _page, _panel, _start, _visible)
from tests.test_cap12_form_mockup_advisory import _client_for
from tests.test_cap13_therm01_integrated_part_eligibility import _integrated
from tests.test_stage19_durable_success_criteria import (
    ELEC_IDEA, MECH_ANSWERS, MECH_IDEA, PREFIX, _answer,  # noqa: F401
)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATH = os.path.join(_ROOT, "domains", "electronics_electrical", "domain.json")
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")

DOMAIN = "electronics_electrical"
PAGE = "/session/%s/success-criteria"
PARTS = ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "SOURCE", "BOUNDARY")
SUMMARY_KEY = "UI_SC_MGUIDE_SOURCE_SUMMARY"
_BLOCK_RE = re.compile(r'<section class="measurement-guidance"[^>]*>.*?</section>', re.S)
_DETAILS_RE = re.compile(r'<details data-mguide-source>.*?</details>', re.S)
# Canonical digests at base 8b4125922167cfa5f800b29294d36641314e0ddc (the merge of
# PR #816): the whole Electronics pack, and the whole provenance record list,
# before this addition.
_PRE_PACK_DIGEST = "5a5575ad3348d7f21085990e92339606df405d3e4e4e8e7ab70b223b7850110b"
_PRE_PROVENANCE_DIGEST = "527320d6f867563a2b1a6a49886ff472d8efcfa49954c3b08f3d866b4fc67ed3"

ACCEPTED = {
    "en": {
        "TITLE": "Before you describe how: what will you observe or measure?",
        "INTRO": "Guidance to consider while you write your measurement method. It does not say what "
                 "your experiment requires: InventorAI has not identified that, and this guidance does "
                 "not analyze, interpret or assess what you enter.",
        "ITEM_1_TITLE": "A measured quantity or an observed condition",
        "ITEM_1_TEXT": "Before describing how you plan to measure or check this experiment, identify what "
                       "you intend to observe. It may be a quantity that you can measure and express with "
                       "an appropriate unit, or a condition or state that you can observe without a "
                       "numerical measurement, such as an indicator being on or off. Saying which of the "
                       "two you mean makes it easier to describe how you will measure or check it.",
        "SOURCE": "Source: National Institute of Standards and Technology (NIST), Antonio M. Possolo, "
                  "Simple Guide for Evaluating and Expressing the Uncertainty of NIST Measurement "
                  "Results, NIST Technical Note 1900 (2015), Section 2, Note 2.1, "
                  "https://doi.org/10.6028/NIST.TN.1900. Adapted: InventorAI restated, in its own "
                  "words, only the distinction between a quantitative property and a qualitative "
                  "property; the on / off example is InventorAI's own, and the Arabic version is "
                  "InventorAI's translation of that restatement. No sentence, definition, figure or "
                  "table of the publication, and no text it attributes to another source, is "
                  "reproduced. This does not imply that NIST or the author has reviewed, approved or "
                  "endorsed InventorAI or this guidance.",
        "BOUNDARY": "This guidance does not identify what your experiment requires, select an instrument, "
                    "sensor or quantity, set any accuracy, resolution or value, calibrate anything, or "
                    "check what you write. Observing a condition in this way is a practical observation, "
                    "not by itself a formally established measurement result. Measurement planning stays "
                    "yours.",
    },
    "ar": {
        "TITLE": "قبل أن تصف الكيفية: ما الذي ستلاحظه أو تقيسه؟",
        "INTRO": "إرشاد لتأخذه في الاعتبار أثناء كتابة طريقة القياس. وهو لا يحدّد ما تحتاجه تجربتك: فلم "
                 "يحدّد InventorAI ذلك، ولا يحلّل هذا الإرشاد ما تُدخله ولا يفسّره ولا يقيّمه.",
        "ITEM_1_TITLE": "مقدار يُقاس أو حالة تُلاحَظ",
        "ITEM_1_TEXT": "قبل وصف كيفية قياس هذه التجربة أو التحقق منها، حدّد ما الذي تريد ملاحظته. قد يكون "
                       "مقدارًا يمكنك قياسه والتعبير عنه بوحدة مناسبة، أو حالةً يمكنك ملاحظتها دون قياس "
                       "عددي، مثل كون مصباح البيان مضاءً أو مطفأً. وتحديد أيّ الاثنين تقصد يجعل وصف كيفية "
                       "القياس أو التحقق أسهل.",
        "SOURCE": "المصدر: المعهد الوطني للمعايير والتقنية في الولايات المتحدة (NIST)، أنطونيو م. بوسولو "
                  "(Antonio M. Possolo)، Simple Guide for Evaluating and Expressing the Uncertainty of "
                  "NIST Measurement Results، المذكرة التقنية NIST Technical Note 1900 (2015)، القسم 2، "
                  "الملاحظة 2.1، على الرابط: ⁦https://doi.org/10.6028/NIST.TN.1900⁩. مُقتبَس: أعاد "
                  "InventorAI بكلماته صياغة التمييز بين الخاصية الكمّية والخاصية النوعية فقط؛ ومثال "
                  "المضاء / المطفأ من InventorAI نفسه، والنص العربي ترجمة InventorAI لهذه الصياغة. ولا "
                  "تُعاد أي جملة أو تعريف أو شكل أو جدول من المنشور، ولا أي نص ينسبه إلى مصدر آخر. ولا "
                  "يعني ذلك أن NIST أو المؤلف راجع InventorAI أو هذا الإرشاد أو وافق عليه أو أيّده.",
        "BOUNDARY": "لا يحدّد هذا الإرشاد ما تحتاجه تجربتك، ولا يختار أداة قياس أو مستشعرًا أو مقدارًا، ولا "
                    "يحدّد أي دقة أو قدرة تمييز أو قيمة، ولا يُجري أي معايرة، ولا يتحقق مما تكتبه. "
                    "وملاحظة حالةٍ على هذا النحو ملاحظة عملية، وليست بذاتها نتيجة قياس مثبتة رسميًا. "
                    "ويبقى تخطيط القياس بيدك.",
    },
}
ACCEPTED_SUMMARY = {"en": "Source, adaptation and limits", "ar": "المصدر والاقتباس والحدود"}


def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _pack():
    with open(_PACK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _provenance():
    with open(_PROVENANCE_PATH, encoding="utf-8") as fh:
        return json.load(fh)["records"]


def _block(body):
    m = _BLOCK_RE.search(body)
    return m.group(0) if m else None


def _dump():
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return list(connection.iterdump())


# ==========================================================================
# 1. the accessor: the existing builder, its own namespace, CAP-09 only
# ==========================================================================
def test_g01_accessor_builds_the_one_prose_only_group_under_its_own_namespace():
    view = cap01_guidance.measurement_planning_guidance(DOMAIN)
    assert view["group_id"] == GROUP and view["prose_only"] is True
    assert tuple(c["claim_id"] for c in view["claims"]) == CLAIMS
    assert view["title_key"] == STEM + "TITLE" and view["intro_key"] == STEM + "INTRO"
    assert view["source_key"] == STEM + "SOURCE" and view["boundary_key"] == STEM + "BOUNDARY"
    [item] = view["claims"]
    assert item["title_key"] == STEM + "ITEM_1_TITLE" and item["text_key"] == STEM + "ITEM_1_TEXT"
    assert "equation_key" not in item and "lead_key" not in item
    assert (cap01_guidance.CAP09_MEASUREMENT_GUIDANCE_GROUP, cap01_guidance.CAP09_MEASUREMENT_GUIDANCE_CLAIMS,
            cap01_guidance.CAP09_MEASUREMENT_GUIDANCE_STEM) == (GROUP, CLAIMS, STEM)
    # Its own namespace: never under a report gap-context prefix.
    assert not STEM.startswith("UI_CAP01_")


@pytest.mark.parametrize("domain", ["mechanical", "control_loop", "software", None, "",
                                    " electronics_electrical", "Electronics_Electrical", "ELECTRONICS_ELECTRICAL"])
def test_g02_accessor_is_exact_on_the_root_domain(domain):
    assert cap01_guidance.measurement_planning_guidance(domain) is None


@pytest.mark.parametrize("part", PARTS)
def test_g03_accessor_is_all_or_nothing_on_its_own_copy(monkeypatch, part):
    monkeypatch.delitem(ui_text.UI_STRINGS, STEM + part)
    assert cap01_guidance.measurement_planning_guidance(DOMAIN) is None
    # The reference panel (PR #816) is untouched by this copy.
    assert cap01_guidance.measurement_planning_references(DOMAIN) is not None


def test_g04_not_a_report_group_the_extension_table_and_report_contexts_are_unchanged():
    table = cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS
    assert all(GROUP not in [row[0] for row in rows] for rows in table.values())
    assert GROUP not in [row[0] for row in cap01_guidance.CAP01_GAP_FUNDAMENTALS.values()]
    assert [r[0] for r in table[(DOMAIN, MECHANISM_COMPLETENESS)]] == [
        "sensing_value_threshold_reference_v1", "measurement_accuracy_resolution_reference_v1",
        "controller_input_logic_output_reference_v1"]
    assert [r[0] for r in table[(DOMAIN, PHYSICAL_FEASIBILITY)]] == [
        "electrical_energy_time_reference_v1", "electric_charge_reference_v1"]
    for gap in (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, "BOUNDARY_AMBIGUITY"):
        view = cap01_guidance.gap_context_copy(DOMAIN, gap)
        assert GROUP not in [g["group_id"] for g in view["fundamentals_groups"]]
    assert len(cap01_guidance.gap_context_copy(DOMAIN, MECHANISM_COMPLETENESS)["fundamentals_groups"]) == 3
    assert len(cap01_guidance.gap_context_copy(DOMAIN, PHYSICAL_FEASIBILITY)["fundamentals_groups"]) == 3
    # The owner's binding is a fixed constant: no discovery, no inference, no inventor text.
    source = open(cap01_guidance.__file__, encoding="utf-8").read()
    seam = source[source.index("CAP09_MEASUREMENT_GUIDANCE_GROUP ="):]
    for token in ("glob", "listdir", "json.load", "idea_text", "request", "[0]"):
        assert token not in seam, token


# ==========================================================================
# 2. the planning page
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_g05_electronics_page_shows_the_guidance_visibly_with_its_approved_copy(lang):
    client, sid = _elec("guide-%s" % lang)
    if lang == "ar":
        client.post("/ui-language", data={"lang": "ar"})
    status, body = _page(client, sid)
    assert status == 200
    block = _block(body)
    assert block is not None and body.count('data-measurement-guidance="') == 1
    assert 'data-measurement-guidance="%s"' % SLUG in block
    assert 'data-mguide-claim="%s"' % CLAIM.replace("_", "-") in block
    # Visible: the guidance and its boundary are NOT inside any <details>; only the
    # source notice is, inside the same block, closed by default.
    outside = _DETAILS_RE.sub("", block)
    assert "<details" not in outside
    text = _visible(outside)
    for part in ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "BOUNDARY"):
        assert _visible(ACCEPTED[lang][part]) in text, part
        assert ui_text.text(STEM + part, lang) == ACCEPTED[lang][part], part
    details = _DETAILS_RE.search(block).group(0)
    assert " open" not in details.split(">", 1)[0]
    assert _visible(ACCEPTED_SUMMARY[lang]) in _visible(details)
    assert _visible(ACCEPTED[lang]["SOURCE"]) in _visible(details)
    assert ui_text.text(STEM + "SOURCE", lang) == ACCEPTED[lang]["SOURCE"]
    assert ui_text.text(SUMMARY_KEY, lang) == ACCEPTED_SUMMARY[lang]
    # Accessible name and description.
    assert 'aria-labelledby="mguide-title"' in block and 'id="mguide-title"' in block
    assert 'aria-describedby="mguide-intro"' in block and 'id="mguide-intro"' in block
    # Beside the measurement-method introduction: after the intro, before the
    # (collapsed) reference panel and before the experiment form.
    intro = body.index(ui_text.text("UI_SC_METHOD_INTRO", lang).replace("'", "&#39;"))
    assert intro < body.index("data-measurement-guidance") < body.index("data-measurement-reference") \
        < body.index('action="/session/%s/success-criteria"' % sid)


def test_g06_the_guidance_adds_no_input_and_no_control():
    client, sid = _elec("noinput")
    block = _block(_page(client, sid)[1])
    for control in ("<input", "<form", "<select", "<textarea", "<button", "<script"):
        assert control not in block, control


def test_g07_the_reference_panel_of_pr816_is_unchanged_beside_it():
    client, sid = _elec("panel")
    body = _page(client, sid)[1]
    panel = _panel(body)
    assert _group_blocks(panel) == [g.replace("_", "-") for g in REFERENCE_GROUPS]
    assert SLUG not in panel and "data-measurement-guidance" not in panel
    assert " open" not in panel.split(">", 1)[0]


def test_g08_the_guidance_does_not_depend_on_the_gap_state_and_never_reaches_the_report():
    client, sid = _elec("gap")
    state = webapp.SESSION_STORE[sid]["state"]
    assert state.get_gap(MECHANISM_COMPLETENESS).status == "CLOSED"
    assert _block(_page(client, sid)[1]) is not None
    # A fresh Electronics project of the same owner has the mechanism gap OPEN and
    # the report carries the three report groups — never this one.
    fresh = _start(client, ELEC_IDEA, DOMAIN, ())
    report = client.get("/session/%s/deliverable" % fresh).get_data(as_text=True)
    assert "sensing-value-threshold-reference-v1" in report
    assert SLUG not in report and "data-measurement-guidance" not in report
    assert STEM not in report
    for part in ("TITLE", "ITEM_1_TEXT"):
        assert _visible(ACCEPTED["en"][part]) not in _visible(report)
    assert _block(_page(client, fresh)[1]) is not None               # gap OPEN: still shown


def test_g09_a_mechanical_root_shows_no_guidance():
    client, _aid = _client_for("c1-mguide-mech@example.com")
    sid = _start(client, MECH_IDEA, "mechanical", MECH_ANSWERS)
    status, body = _page(client, sid)
    assert status == 200 and 'action="/session/%s/success-criteria"' % sid in body
    assert _block(body) is None and "data-measurement-guidance" not in body and SLUG not in body


@pytest.mark.parametrize("focus,shown", [("electronics_electrical", True), ("mechanical", False)])
def test_g10_an_integrated_project_follows_its_trusted_root_domain_only(focus, shown):
    client, _aid = _client_for("c1-mguide-int-%s@example.com" % focus[:4])
    sid = _integrated(client, focus)
    assert (cap01_guidance.measurement_planning_guidance(webapp._cap12_root_domain(sid)) is not None) is shown
    assert (_block(_page(client, sid)[1]) is not None) is shown


@pytest.mark.parametrize("reader", [lambda _sid: None,
                                    lambda _sid: (_ for _ in ()).throw(RuntimeError("unreadable"))])
def test_g11_an_unreadable_root_domain_shows_nothing_and_the_page_still_works(monkeypatch, reader):
    client, sid = _elec("unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", reader)
    status, body = _page(client, sid)
    assert status == 200 and 'action="/session/%s/success-criteria"' % sid in body
    assert _block(body) is None


def test_g12_an_unavailable_page_shows_no_guidance(monkeypatch):
    client, sid = _elec("unavailable")

    def boom(*_a, **_k):
        raise RuntimeError("no reconstruction")
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", boom)
    status, body = _page(client, sid)
    assert status == 503 and _block(body) is None and "data-measurement-guidance" not in body


def test_g13_a_refused_post_rerenders_with_the_same_rule():
    client, sid = _elec("post")
    body = _page(client, sid)[1]
    eid = re.search(r'name="%s([^"]+)"' % re.escape(PREFIX), body).group(1)
    r = client.post(PAGE % sid, data={PREFIX + eid: "x" * (webapp.MAX_CRITERION_LENGTH + 1)})
    assert r.status_code == 400
    refused = r.get_data(as_text=True)
    assert 'id="draft-unsaved"' in refused and _block(refused) is not None


def test_g14_denials_are_unchanged_and_carry_no_guidance():
    _owner, sid = _elec("deny")
    other, _aid = _client_for("c1-mguide-other@example.com")
    r = other.get(PAGE % sid)
    assert r.status_code != 200 and "data-measurement-guidance" not in r.get_data(as_text=True)


def test_g15_viewing_the_page_writes_nothing():
    client, sid = _elec("nowrite")
    before = (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"]))
    for _ in range(2):
        assert _block(_page(client, sid)[1]) is not None
    assert (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"])) == before


# ==========================================================================
# 3. pack and provenance: additions only, exact claim and rights mappings
# ==========================================================================
def test_p01_the_pack_change_is_exactly_one_group_and_one_note():
    pack = _pack()
    assert _digest(without_measurement_guidance_addition(pack)) == _PRE_PACK_DIGEST
    assert [g["group_id"] for g in pack["reference_fundamentals"]][-1] == GROUP
    note = pack["_governance_notes"][NOTE]
    for phrase in ("MEASUREMENT-PLAN-GUIDANCE-01", "C1 only", "exactly ONE prose-only conceptual claim",
                   "measured_quantity_versus_observed_condition", "electronics_electrical:PR022",
                   "NIST Technical Note 1900", "Note 2.1", "printed page 12",
                   "Lead-supplied primary-source inspection, not executor-performed",
                   "electronics_electrical:PR023", "electronics_electrical:PR015 is NOT broadened",
                   "no relationship / equation by design",
                   "NOT bound to the report / PDF gap context",
                   "ONLY consumer is the CAP-09 measurement-planning page", "independent of gap state",
                   "report / PDF eligibility and group count are unchanged", "inert",
                   "does not read, interpret or grade inventor text",
                   "not imply that a qualitative observation is equivalent to a formally established "
                   "metrological result",
                   "C3 (environmental-condition guidance) stays SOURCE-BLOCKED",
                   "PR001–PR021 are unchanged"):
        assert phrase in note, phrase


def test_p02_the_one_claim_has_exact_source_policy_and_limitation_linkage():
    group = _pack()["reference_fundamentals"][-1]
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert (group["group_id"], group["applicable_gap_type"]) == (GROUP, MECHANISM_COMPLETENESS)
    [claim] = group["claims"]
    assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation", "source_ref",
                             "source_use_policy_ref"]
    assert claim["claim_id"] == CLAIM and "relationship" not in claim      # prose-only by design
    assert (claim["source_ref"], claim["source_use_policy_ref"]) == RECORDS
    recs = {r["record_id"]: r for r in _provenance()}
    assert recs[RECORDS[0]]["source_type"] == "government_reference_publication"
    assert recs[RECORDS[1]]["source_type"] == "source_use_policy"
    assert CLAIM in recs[RECORDS[0]]["notes"] and CLAIM in recs[RECORDS[1]]["notes"]
    for phrase in ("quantitative property", "expressed as a value with an appropriate unit",
                   "qualitative property", "observed or identified without necessarily producing a "
                   "numerical value", "InventorAI restates, in its own words, only this distinction",
                   "NIST Technical Note 1900, Section 2, Note 2.1",
                   "does not state that observing a condition is equivalent to a formally established "
                   "measurement result"):
        assert phrase in claim["fact"], phrase
    for phrase in ("Measurement-planning guidance only", "ONLY consumer is the CAP-09 measurement-planning page",
                   "independent of any gap state", "NOT bound to the report / PDF gap context",
                   "does not identify, read, interpret or grade", "never infers the kind of property",
                   "No instrument, sensor or quantity selection or recommendation",
                   "accuracy or resolution requirement", "calibration, uncertainty evaluation, measurement "
                   "standard, mandatory procedure, required input, value, calculation, readiness, validation "
                   "or safety statement", "CAP-09 keeps the inventor's own measurement planning",
                   "equivalent to a formally established metrological result"):
        assert phrase in claim["limitation"], phrase
    # The guidance stays within the admitted claim: the page copy names only the two
    # kinds the claim distinguishes and no instrument, requirement or procedure.
    for lang in ("en", "ar"):
        text = ui_text.text(STEM + "ITEM_1_TEXT", lang).lower()
        for word in ("multimeter", "oscilloscope", "calibrat", "must ", "required", "accuracy",
                     "resolution", "uncertainty", "tolerance", "±"):
            assert word not in text, (lang, word)


def test_p03_two_records_appended_after_pr021_and_every_other_record_unchanged():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids))
    i = ids.index("electronics_electrical:PR021")
    assert tuple(ids[i + 1:i + 3]) == RECORDS
    assert ids[i + 3] == "mechanical:PR001"
    assert _digest([r for r in records if r["record_id"] not in RECORDS]) == _PRE_PROVENANCE_DIGEST
    recs = {r["record_id"]: r for r in records}
    shape = sorted(recs["electronics_electrical:PR014"])
    assert all(sorted(recs[r]) == shape for r in RECORDS)
    assert all(recs[r]["pack_id"] == DOMAIN and recs[r]["tier"] == 1 and recs[r]["cross_domain_usage"] == []
               for r in RECORDS)
    # PR015 is untouched and still names only its own claim.
    assert "measurement_accuracy_resolution_distinction" in recs["electronics_electrical:PR015"]["notes"]
    assert CLAIM not in recs["electronics_electrical:PR015"]["notes"]


def test_p04_the_source_record_carries_the_exact_passage_the_lead_supplied_status_and_the_exclusions():
    recs = {r["record_id"]: r for r in _provenance()}
    src = recs[RECORDS[0]]
    assert src["standard_number"] == "NIST TN 1900" and src["jurisdiction"] == "US"
    assert "Antonio M. Possolo (2015)" in src["source_name"]
    assert "Simple Guide for Evaluating and Expressing the Uncertainty of NIST Measurement Results" in \
        src["source_name"]
    assert "Section 2, Note 2.1" in src["source_name"]
    assert src["url"] == "https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1900.pdf"
    for phrase in ("DOI 10.6028/NIST.TN.1900", "https://doi.org/10.6028/NIST.TN.1900",
                   "Section 2, Note 2.1, printed page 12",
                   "Lead-supplied primary-source inspection, NOT executor-performed",
                   "not independently re-inspected by the executor", "blocked by environment policy",
                   "2026-10-14"):
        assert phrase in src["version_or_edition"], phrase
    for phrase in ("CLAIM MAPPING (passage level)", "quantitative property", "qualitative property",
                   "found no third-party attribution attached to the relied-upon Note 2.1 statement",
                   "NOT a comprehensive authorship or rights verification",
                   "ONLY that narrow factual distinction", "InventorAI Arabic translation",
                   "indicator on / off example is InventorAI's own illustration",
                   "EXCLUDED and not used, quoted or paraphrased",
                   "definitions of measurement, measurand, measurement uncertainty and measurement result",
                   "every VIM, ISO, JCGM / GUM or other third-party definition",
                   "whole publication is NOT treated as unrestricted reusable material",
                   "not state or imply that a qualitative observation is equivalent to a formally "
                   "established metrological result",
                   "no uncertainty evaluation, accuracy or resolution requirement, instrument selection, "
                   "calibration, measurement standard or procedure",
                   "no-endorsement notice",
                   "Source-use / rights disposition: electronics_electrical:PR023",
                   "electronics_electrical:PR015 is not broadened"):
        assert phrase in src["notes"], phrase


def test_p05_the_rights_record_is_claim_specific_and_does_not_broaden_pr015():
    recs = {r["record_id"]: r for r in _provenance()}
    use = recs[RECORDS[1]]
    assert use["standard_number"] is None and use["jurisdiction"] == "US"
    assert use["url"] == ("https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-"
                          "software-and-technical-series-publications")
    assert use["url"] == recs["electronics_electrical:PR015"]["url"]       # the existing precedent page
    for phrase in ("electronics_electrical:PR007, PR011 and PR015", "ONE new claim", "Lead-supplied",
                   "not independently re-inspected by the executor", "2026-10-14"):
        assert phrase in use["version_or_edition"], phrase
    assert use["notes"].startswith("SOURCE-USE COMPATIBILITY DISPOSITION AND RIGHTS BOUNDARY (not a legal opinion")
    for phrase in ("electronics_electrical:PR022", "ONLY", "RIGHTS BASIS", "17 U.S.C. § 105",
                   "passage-level", "NOT treated as unrestricted reusable material",
                   "electronics_electrical:PR015 is NOT broadened",
                   "every VIM, ISO, JCGM / GUM or other third-party definition",
                   "no source sentence, definition, figure or table is reproduced",
                   "InventorAI Arabic translation", "DOI 10.6028/NIST.TN.1900",
                   "no statement or implication that NIST or the author reviewed, approved, certified or "
                   "endorses", "no NIST logo or mark",
                   "does not imply that a qualitative observation is equivalent to a formally established "
                   "metrological result", "InventorAI remains responsible for its own presented output"):
        assert phrase in use["notes"], phrase


def test_p06_the_page_copy_carries_the_attribution_adaptation_and_no_endorsement_in_both_languages():
    for lang in ("en", "ar"):
        source = ui_text.text(STEM + "SOURCE", lang)
        for phrase in ("NIST", "Possolo", "Simple Guide for Evaluating and Expressing the Uncertainty of NIST "
                       "Measurement Results", "1900", "2.1", "https://doi.org/10.6028/NIST.TN.1900", "InventorAI"):
            assert phrase in source, (lang, phrase)
    en = ui_text.text(STEM + "SOURCE", "en")
    for phrase in ("Adapted:", "in its own words", "Arabic version is InventorAI's translation",
                   "No sentence, definition, figure or table", "does not imply", "endorsed"):
        assert phrase in en, phrase
    ar = ui_text.text(STEM + "SOURCE", "ar")
    assert "⁦https://doi.org/10.6028/NIST.TN.1900⁩" in ar        # LTR isolate around the DOI link
    for phrase in ("مُقتبَس", "ترجمة InventorAI", "أيّده"):
        assert phrase in ar, phrase
    assert ui_text.has_string(SUMMARY_KEY)
