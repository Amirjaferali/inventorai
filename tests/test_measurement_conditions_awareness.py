# -*- coding: utf-8 -*-
"""MEASUREMENT-CONDITIONS-AWARENESS-01 — ONE further visible, optional measurement-planning
element on the CAP-09 measurement-planning page, after the C1 guidance: the conditions of use
and influence quantities can affect a measurement result and whether an instrument's
calibration results apply under those conditions, so identifying the relevant conditions is
part of planning the measurement.

Proves: the ONE admitted claim is declared in the Electronics pack with claim-specific
provenance (electronics_electrical:PR024 — Phillips, Estler, Doiron, Eberhardt and Levenson
(2001), Journal of Research of NIST 106, Sections 2.1 and 2.2, Lead-supplied inspection — and
PR025, the claim-specific rights disposition that broadens neither PR015 nor PR023); the pack
and provenance changes are additions only; the note is built by the existing group builder
under its own copy namespace and is NOT a report / PDF gap-context group; eligibility is ONLY
the trusted durable root domain, exactly ``electronics_electrical`` — a Mechanical root, a
Mechanical-focus integrated project, an unreadable domain and an unavailable page show nothing,
and the gap state does not matter; the note is visible beside the measurement-method
introduction with its boundary, after the C1 guidance and before the collapsed reference
panel, and its source / adaptation / no-endorsement notice is one click away; every render path
of the page respects the rule; it adds no input, names no condition, value or requirement,
reads no inventor text and writes nothing; the C1 guidance and the PR #816 panel are unchanged;
EN / AR copy is pinned.
Synthetic invention data only.
"""
import hashlib
import json
import os
import pickle
import re
import sqlite3

import pytest

import web.app as webapp
from engine.idea_state import MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY
from web import cap01_guidance, ui_text
from tests.cap01_measurement_conditions_addition import (
    MCOND_CLAIM as CLAIM, MCOND_CLAIMS as CLAIMS, MCOND_GROUP as GROUP, MCOND_NOTE as NOTE,
    MCOND_RECORDS as RECORDS, MCOND_SLUG as SLUG, MCOND_STEM as STEM,
    without_measurement_conditions_addition)
# 28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01 added one further prose-only group on the Electronics
# MECHANISM_COMPLETENESS context; excluded here likewise (tests/cap01_load_switching_addition.py).
from tests.measurement_planning_integrated_part_amendment import (
    without_measurement_planning_integrated_part_amendment)
from tests.cap01_load_switching_addition import (  # noqa: F401
    LSW_GROUP, LSW_RECORDS, LSW_ROW, LSW_SLUG, without_load_switching_addition)
from tests.cap01_measurement_guidance_addition import MGUIDE_GROUP, MGUIDE_SLUG
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
URL = "https://nvlpubs.nist.gov/nistpubs/jres/106/2/j62phi.pdf"
RIGHTS_URL = ("https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-"
              "technical-series-publications")
_BLOCK_RE = re.compile(r'<section class="measurement-conditions"[^>]*>.*?</section>', re.S)
_DETAILS_RE = re.compile(r'<details data-mcond-source>.*?</details>', re.S)
# Canonical digests at base 8a1255153f38ee1d7499e336e88c04c76804ac6e (the merge of
# PR #821): the whole Electronics pack, and the whole provenance record list,
# before this addition.
_PRE_PACK_DIGEST = "51ae5038b3f6e445233e506e48c2b0de9720e54e02540d9662470bdee6cae85f"
_PRE_PROVENANCE_DIGEST = "9598b923934d13d43f600b59b004b34cce45ead8d72e4a9acba15d02cf3afe86"

ACCEPTED = {
    "en": {
        "TITLE": "Under what conditions will you measure?",
        "INTRO": "Guidance to consider while you write your measurement method. It does not say which "
                 "conditions matter for your experiment: InventorAI has not identified that, and this "
                 "guidance does not analyze, interpret or assess what you enter.",
        "ITEM_1_TITLE": "Conditions of use can affect a measurement",
        "ITEM_1_TEXT": "The conditions under which you make a measurement, and other quantities besides the "
                       "one you intend to measure, can affect the measurement result. They can also affect "
                       "whether an instrument's calibration results apply under those conditions. "
                       "Identifying the conditions relevant to your measurement is part of planning it "
                       "soundly; if you wish, you can mention them when you describe how you will measure "
                       "or check this experiment.",
        "SOURCE": "Source: National Institute of Standards and Technology (NIST), Phillips, Estler, Doiron, "
                  "Eberhardt and Levenson, A Careful Consideration of the Calibration Concept, Journal of "
                  "Research of the National Institute of Standards and Technology, Vol. 106 (2001), "
                  "pp. 371–379, Sections 2.1 and 2.2, "
                  "https://nvlpubs.nist.gov/nistpubs/jres/106/2/j62phi.pdf. Adapted: InventorAI restated, "
                  "in its own words, only that the conditions of use and other influencing quantities can "
                  "affect a measurement and whether calibration results apply, and that identifying them "
                  "is part of measurement planning; the Arabic version is InventorAI's translation of that "
                  "restatement. No sentence, definition, figure or table of the publication, and no "
                  "definition or text it takes from another source such as the VIM or the GUM, is "
                  "reproduced. This does not imply that NIST or the authors have reviewed, approved or "
                  "endorsed InventorAI or this guidance.",
        "BOUNDARY": "This guidance does not identify which conditions or quantities matter for your "
                    "experiment, give any condition, value, range or limit, select an instrument, set any "
                    "accuracy, resolution or calibration requirement, describe a calibration procedure, "
                    "evaluate uncertainty, or check what you write. Measurement planning stays yours.",
    },
    "ar": {
        "TITLE": "في أيّ ظروف ستقيس؟",
        "INTRO": "إرشاد لتأخذه في الاعتبار أثناء كتابة طريقة القياس. وهو لا يحدّد الظروف المهمة لتجربتك: "
                 "فلم يحدّد InventorAI ذلك، ولا يحلّل هذا الإرشاد ما تُدخله ولا يفسّره ولا يقيّمه.",
        "ITEM_1_TITLE": "ظروف الاستخدام قد تؤثّر في القياس",
        "ITEM_1_TEXT": "قد تؤثّر الظروف التي تُجري فيها القياس، ومقادير أخرى غير المقدار الذي تريد قياسه، في "
                       "نتيجة القياس. وقد تؤثّر أيضًا في مدى انطباق نتائج معايرة أداة القياس في تلك الظروف. "
                       "وتحديد الظروف ذات الصلة بقياسك جزء من التخطيط السليم له؛ ويمكنك، إن شئت، ذكرها عند "
                       "وصف كيفية قياس هذه التجربة أو التحقق منها.",
        "SOURCE": "المصدر: المعهد الوطني للمعايير والتقنية في الولايات المتحدة (NIST)، فيليبس وإستلر ودويرون "
                  "وإيبرهارت وليفنسون (Phillips, Estler, Doiron, Eberhardt, Levenson)، A Careful "
                  "Consideration of the Calibration Concept، مجلة Journal of Research of the National "
                  "Institute of Standards and Technology، المجلد 106 (2001)، الصفحات 371–379، القسمان 2.1 "
                  "و2.2، على الرابط: ⁦https://nvlpubs.nist.gov/nistpubs/jres/106/2/j62phi.pdf⁩. مُقتبَس: "
                  "أعاد InventorAI بكلماته صياغة أن ظروف الاستخدام والمقادير المؤثّرة الأخرى قد تؤثّر في "
                  "القياس وفي مدى انطباق نتائج المعايرة، وأن تحديدها جزء من تخطيط القياس، فقط؛ والنص العربي "
                  "ترجمة InventorAI لهذه الصياغة. ولا تُعاد أي جملة أو تعريف أو شكل أو جدول من المنشور، ولا أي "
                  "تعريف أو نص يأخذه من مصدر آخر مثل VIM أو GUM. ولا يعني ذلك أن NIST أو المؤلفين راجعوا "
                  "InventorAI أو هذا الإرشاد أو وافقوا عليه أو أيّدوه.",
        "BOUNDARY": "لا يحدّد هذا الإرشاد الظروف أو المقادير المهمة لتجربتك، ولا يعطي أي ظرف أو قيمة أو مدى أو "
                    "حدّ، ولا يختار أداة قياس، ولا يحدّد أي متطلب للدقة أو لقدرة التمييز أو للمعايرة، ولا يصف "
                    "إجراء معايرة، ولا يقيّم عدم اليقين، ولا يتحقق مما تكتبه. ويبقى تخطيط القياس بيدك.",
    },
}


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
def test_m01_accessor_builds_the_one_prose_only_group_under_its_own_namespace():
    view = cap01_guidance.measurement_planning_conditions(DOMAIN)
    assert view["group_id"] == GROUP and view["prose_only"] is True
    assert tuple(c["claim_id"] for c in view["claims"]) == CLAIMS
    assert view["title_key"] == STEM + "TITLE" and view["intro_key"] == STEM + "INTRO"
    assert view["source_key"] == STEM + "SOURCE" and view["boundary_key"] == STEM + "BOUNDARY"
    [item] = view["claims"]
    assert item["title_key"] == STEM + "ITEM_1_TITLE" and item["text_key"] == STEM + "ITEM_1_TEXT"
    assert "equation_key" not in item and "lead_key" not in item
    assert (cap01_guidance.CAP09_MEASUREMENT_CONDITIONS_GROUP, cap01_guidance.CAP09_MEASUREMENT_CONDITIONS_CLAIMS,
            cap01_guidance.CAP09_MEASUREMENT_CONDITIONS_STEM) == (GROUP, CLAIMS, STEM)
    assert not STEM.startswith("UI_CAP01_")
    assert GROUP in cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS


@pytest.mark.parametrize("domain", ["mechanical", "control_loop", "software", None, "",
                                    " electronics_electrical", "Electronics_Electrical", "ELECTRONICS_ELECTRICAL"])
def test_m02_accessor_is_exact_on_the_root_domain(domain):
    assert cap01_guidance.measurement_planning_conditions(domain) is None


@pytest.mark.parametrize("part", PARTS)
def test_m03_accessor_is_all_or_nothing_on_its_own_copy(monkeypatch, part):
    monkeypatch.delitem(ui_text.UI_STRINGS, STEM + part)
    assert cap01_guidance.measurement_planning_conditions(DOMAIN) is None
    # The C1 guidance and the PR #816 panel are untouched by this copy.
    assert cap01_guidance.measurement_planning_guidance(DOMAIN) is not None
    assert cap01_guidance.measurement_planning_references(DOMAIN) is not None


def test_m04_not_a_report_group_the_extension_table_and_report_contexts_are_unchanged():
    table = cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS
    assert all(GROUP not in [row[0] for row in rows] for rows in table.values())
    assert GROUP not in [row[0] for row in cap01_guidance.CAP01_GAP_FUNDAMENTALS.values()]
    for gap in (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, "BOUNDARY_AMBIGUITY"):
        view = cap01_guidance.gap_context_copy(DOMAIN, gap)
        assert GROUP not in [g["group_id"] for g in view["fundamentals_groups"]]
    # 28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01 later added a fourth report group to this context.
    assert len(cap01_guidance.gap_context_copy(DOMAIN, MECHANISM_COMPLETENESS)["fundamentals_groups"]) == 4
    assert len(cap01_guidance.gap_context_copy(DOMAIN, PHYSICAL_FEASIBILITY)["fundamentals_groups"]) == 3
    source = open(cap01_guidance.__file__, encoding="utf-8").read()
    seam = source[source.index("CAP09_MEASUREMENT_CONDITIONS_GROUP ="):]
    for token in ("glob", "listdir", "json.load", "idea_text", "request", "[0]"):
        assert token not in seam, token


# ==========================================================================
# 2. the planning page
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_m05_electronics_page_shows_the_note_visibly_with_its_approved_copy(lang):
    client, sid = _elec("mcond-%s" % lang)
    if lang == "ar":
        client.post("/ui-language", data={"lang": "ar"})
    status, body = _page(client, sid)
    assert status == 200
    block = _block(body)
    assert block is not None and body.count('data-measurement-conditions="') == 1
    assert 'data-measurement-conditions="%s"' % SLUG in block
    assert 'data-mcond-claim="%s"' % CLAIM.replace("_", "-") in block
    outside = _DETAILS_RE.sub("", block)
    assert "<details" not in outside
    text = _visible(outside)
    for part in ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "BOUNDARY"):
        assert _visible(ACCEPTED[lang][part]) in text, part
        assert ui_text.text(STEM + part, lang) == ACCEPTED[lang][part], part
    details = _DETAILS_RE.search(block).group(0)
    assert " open" not in details.split(">", 1)[0]
    assert _visible(ui_text.text(SUMMARY_KEY, lang)) in _visible(details)
    assert _visible(ACCEPTED[lang]["SOURCE"]) in _visible(details)
    assert ui_text.text(STEM + "SOURCE", lang) == ACCEPTED[lang]["SOURCE"]
    assert 'aria-labelledby="mcond-title"' in block and 'id="mcond-title"' in block
    assert 'aria-describedby="mcond-intro"' in block and 'id="mcond-intro"' in block
    # Order: method intro < C1 guidance < this note < (collapsed) reference panel < form.
    intro = body.index(ui_text.text("UI_SC_METHOD_INTRO", lang).replace("'", "&#39;"))
    assert intro < body.index('data-measurement-guidance="%s"' % MGUIDE_SLUG) \
        < body.index("data-measurement-conditions") < body.index("data-measurement-reference") \
        < body.index('action="/session/%s/success-criteria"' % sid)


def test_m06_the_note_adds_no_input_and_no_control():
    client, sid = _elec("mcond-noinput")
    block = _block(_page(client, sid)[1])
    for control in ("<input", "<form", "<select", "<textarea", "<button", "<script"):
        assert control not in block, control


def test_m07_the_c1_guidance_and_the_pr816_panel_are_unchanged_beside_it():
    client, sid = _elec("mcond-panel")
    body = _page(client, sid)[1]
    panel = _panel(body)
    assert _group_blocks(panel) == [g.replace("_", "-") for g in REFERENCE_GROUPS]
    assert SLUG not in panel and "data-measurement-conditions" not in panel
    assert " open" not in panel.split(">", 1)[0]
    guide = re.search(r'<section class="measurement-guidance"[^>]*>.*?</section>', body, re.S).group(0)
    assert SLUG not in guide and "data-mcond" not in guide
    assert cap01_guidance.measurement_planning_guidance(DOMAIN)["group_id"] == MGUIDE_GROUP


def test_m08_the_note_does_not_depend_on_the_gap_state_and_never_reaches_the_report():
    client, sid = _elec("mcond-gap")
    state = webapp.SESSION_STORE[sid]["state"]
    assert state.get_gap(MECHANISM_COMPLETENESS).status == "CLOSED"
    assert _block(_page(client, sid)[1]) is not None
    fresh = _start(client, ELEC_IDEA, DOMAIN, ())
    report = client.get("/session/%s/deliverable" % fresh).get_data(as_text=True)
    assert "sensing-value-threshold-reference-v1" in report
    assert SLUG not in report and "data-measurement-conditions" not in report and STEM not in report
    for part in ("TITLE", "ITEM_1_TEXT"):
        assert _visible(ACCEPTED["en"][part]) not in _visible(report)
    assert _block(_page(client, fresh)[1]) is not None               # gap OPEN: still shown


def test_m09_a_mechanical_root_shows_no_note():
    client, _aid = _client_for("mcond-mech@example.com")
    sid = _start(client, MECH_IDEA, "mechanical", MECH_ANSWERS)
    status, body = _page(client, sid)
    assert status == 200 and 'action="/session/%s/success-criteria"' % sid in body
    assert _block(body) is None and "data-measurement-conditions" not in body and SLUG not in body


@pytest.mark.parametrize("focus,root_rule", [("electronics_electrical", True), ("mechanical", False)])
def test_m10_an_integrated_project_shows_the_note_for_its_declared_electronics_part(focus, root_rule):
    # The accessor's own root rule is unchanged; MEASUREMENT-PLANNING-INTEGRATED-PART-01
    # (Owner-authorized) shows the note on the page for the declared Electrical /
    # Electronics part of a valid integrated composition, whatever the focus.
    client, _aid = _client_for("mcond-int-%s@example.com" % focus[:4])
    sid = _integrated(client, focus)
    assert (cap01_guidance.measurement_planning_conditions(webapp._cap12_root_domain(sid)) is not None) is root_rule
    assert _block(_page(client, sid)[1]) is not None


@pytest.mark.parametrize("reader", [lambda _sid: None,
                                    lambda _sid: (_ for _ in ()).throw(RuntimeError("unreadable"))])
def test_m11_an_unreadable_root_domain_shows_nothing_and_the_page_still_works(monkeypatch, reader):
    client, sid = _elec("mcond-unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", reader)
    status, body = _page(client, sid)
    assert status == 200 and 'action="/session/%s/success-criteria"' % sid in body
    assert _block(body) is None


def test_m12_an_unavailable_page_shows_no_note(monkeypatch):
    client, sid = _elec("mcond-unavailable")

    def boom(*_a, **_k):
        raise RuntimeError("no reconstruction")
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", boom)
    status, body = _page(client, sid)
    assert status == 503 and _block(body) is None and "data-measurement-conditions" not in body


def test_m13_a_refused_post_rerenders_with_the_same_rule():
    client, sid = _elec("mcond-post")
    body = _page(client, sid)[1]
    eid = re.search(r'name="%s([^"]+)"' % re.escape(PREFIX), body).group(1)
    r = client.post(PAGE % sid, data={PREFIX + eid: "x" * (webapp.MAX_CRITERION_LENGTH + 1)})
    assert r.status_code == 400
    refused = r.get_data(as_text=True)
    assert 'id="draft-unsaved"' in refused and _block(refused) is not None


def test_m14_denials_are_unchanged_and_carry_no_note():
    _owner, sid = _elec("mcond-deny")
    other, _aid = _client_for("mcond-other@example.com")
    r = other.get(PAGE % sid)
    assert r.status_code != 200 and "data-measurement-conditions" not in r.get_data(as_text=True)


def test_m15_viewing_the_page_writes_nothing():
    client, sid = _elec("mcond-nowrite")
    before = (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"]))
    for _ in range(2):
        assert _block(_page(client, sid)[1]) is not None
    assert (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"])) == before


# ==========================================================================
# 3. pack and provenance: additions only, exact claim and rights mappings
# ==========================================================================
def test_p01_the_pack_change_is_exactly_one_group_and_one_note():
    pack = _pack()
    assert _digest(without_measurement_planning_integrated_part_amendment(without_measurement_conditions_addition(without_load_switching_addition(pack)))) == _PRE_PACK_DIGEST
    assert [g["group_id"] for g in pack["reference_fundamentals"]][-1] == GROUP
    note = pack["_governance_notes"][NOTE]
    for phrase in ("MEASUREMENT-CONDITIONS-AWARENESS-01", "exactly ONE prose-only conceptual claim",
                   CLAIM, "electronics_electrical:PR024", "Journal of Research of NIST, Vol. 106",
                   "Section 2.1, printed page 372", "Section 2.2, printed page 373",
                   "Lead-supplied primary-source inspection, not executor-performed",
                   "electronics_electrical:PR025", "electronics_electrical:PR015 and PR023 are NOT broadened",
                   "no relationship / equation by design", "NOT bound to the report / PDF gap context",
                   "ONLY consumer is the CAP-09 measurement-planning page", "independent of gap state",
                   "report / PDF eligibility and group count are unchanged", "inert",
                   "this guidance does not analyze, interpret or assess the inventor's entry",
                   "It is NOT the C3 environmental-condition guidance, which stays SOURCE-BLOCKED",
                   "PR001–PR023 are unchanged"):
        assert phrase in note, phrase


def test_p02_the_one_claim_has_exact_source_policy_and_limitation_linkage():
    [group] = [g for g in _pack()["reference_fundamentals"] if g["group_id"] == GROUP]
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["applicable_gap_type"] == MECHANISM_COMPLETENESS
    [claim] = group["claims"]
    assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation", "source_ref",
                             "source_use_policy_ref"]
    assert claim["claim_id"] == CLAIM and "relationship" not in claim
    assert (claim["source_ref"], claim["source_use_policy_ref"]) == RECORDS
    recs = {r["record_id"]: r for r in _provenance()}
    assert recs[RECORDS[0]]["source_type"] == "government_reference_publication"
    assert recs[RECORDS[1]]["source_type"] == "source_use_policy"
    assert CLAIM in recs[RECORDS[0]]["notes"] and CLAIM in recs[RECORDS[1]]["notes"]
    for phrase in ("conditions under which a measurement is made", "influence quantities",
                   "can affect the measurement result and whether an instrument's calibration results apply "
                   "under those conditions", "identifying the relevant conditions is part of sound measurement "
                   "planning", "InventorAI restates, in its own words, only this awareness",
                   "Sections 2.1 and 2.2", "names no condition, quantity, value or limit",
                   "states no calibration or measurement requirement"):
        assert phrase in claim["fact"], phrase
    for phrase in ("Measurement-planning awareness only", "ONLY consumer is the CAP-09 measurement-planning page",
                   "independent of any gap state", "NOT bound to the report / PDF gap context",
                   "This guidance does not analyze, interpret or assess the inventor's entry",
                   "does not identify which conditions or influence quantities are relevant",
                   "never infers them", "No environmental or operating condition, value, range or limit",
                   "no instrument, sensor or quantity selection or recommendation",
                   "no accuracy, resolution or calibration requirement",
                   "no calibration procedure, calibration-validity determination, uncertainty evaluation",
                   "CAP-09 keeps the inventor's own measurement planning",
                   "NOT the C3 environmental-condition guidance, which stays SOURCE-BLOCKED"):
        assert phrase in claim["limitation"], phrase
    # The page copy stays within the admitted awareness: no named condition, instrument,
    # value or requirement.
    for lang in ("en", "ar"):
        text = ui_text.text(STEM + "ITEM_1_TEXT", lang).lower()
        for word in ("temperature", "humidity", "vibration", "multimeter", "oscilloscope", "must ",
                     "required", "tolerance", "±", "°", "%", "حرارة", "رطوبة", "يجب"):
            assert word not in text, (lang, word)


def test_p03_two_records_appended_after_pr023_and_every_other_record_unchanged():
    records = _provenance()
    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids))
    i = ids.index("electronics_electrical:PR023")
    assert tuple(ids[i + 1:i + 3]) == RECORDS and tuple(ids[i + 3:i + 5]) == LSW_RECORDS
    assert ids[i + 5] == "mechanical:PR001"
    assert _digest([r for r in records if r["record_id"] not in RECORDS + LSW_RECORDS]) == _PRE_PROVENANCE_DIGEST
    recs = {r["record_id"]: r for r in records}
    shape = sorted(recs["electronics_electrical:PR022"])
    assert all(sorted(recs[r]) == shape for r in RECORDS)
    assert all(recs[r]["pack_id"] == DOMAIN and recs[r]["tier"] == 1 and recs[r]["cross_domain_usage"] == []
               for r in RECORDS)
    for earlier in ("electronics_electrical:PR015", "electronics_electrical:PR023"):
        assert CLAIM not in recs[earlier]["notes"]


PMC_URL = "https://pmc.ncbi.nlm.nih.gov/articles/PMC4862813/"


def test_p04_the_source_record_carries_the_exact_passages_the_lead_supplied_status_and_the_exclusions():
    src = {r["record_id"]: r for r in _provenance()}[RECORDS[0]]
    assert src["jurisdiction"] == "US" and src["url"] == URL
    for phrase in ("Phillips, Estler, Doiron, Eberhardt and Levenson (2001)",
                   "A Careful Consideration of the Calibration Concept", "Vol. 106, pp. 371–379",
                   "Sections 2.1 and 2.2"):
        assert phrase in src["source_name"], phrase
    for phrase in ("Volume 106, Number 2 (2001), pages 371–379", URL, "Section 2.1, printed page 372",
                   "Section 2.2, printed page 373", "Lead-supplied primary-source inspection, NOT executor-performed",
                   "not independently re-inspected by the executor", "blocked by environment policy",
                   "2026-10-15"):
        assert phrase in src["version_or_edition"], phrase
    for phrase in ("CLAIM MAPPING (passage level)", "the definition of the measurand together with the relevant "
                   "influence quantities", "the conditions under which calibration results are valid and the "
                   "conditions of use", "InventorAI Arabic translation",
                   "NOT a comprehensive authorship or rights verification",
                   "EXCLUDED and not used, quoted or paraphrased", "the VIM, the GUM, ISO, JCGM",
                   "whole publication is NOT treated as unrestricted reusable material",
                   "names no condition, influence quantity, value, range or limit", "no-endorsement notice",
                   "Source-use / rights disposition: electronics_electrical:PR025",
                   "electronics_electrical:PR015 and electronics_electrical:PR023 are not broadened"):
        assert phrase in src["notes"], phrase
    # PR #822 IP-evidence correction: the Lead's confirmed direct inspection and the documented affiliation, with the
    # residual uncertainty stated, never upgraded to verified government employment
    assert "the Lead confirmed its direct inspection of the primary NIST publication" in src["version_or_edition"]
    assert "no expansion of the claim was made" in src["version_or_edition"]
    for phrase in ("AUTHORSHIP / AFFILIATION EVIDENCE (Lead-supplied", PMC_URL,
                   "lists all five authors with NIST affiliation",
                   "U.S. Government employment status at the time of authorship has NOT been independently established"):
        assert phrase in src["notes"], phrase
    assert "employment is verified" not in src["notes"] and "employment was verified" not in src["notes"]


def test_p05_the_rights_record_is_claim_specific_and_broadens_no_earlier_record():
    recs = {r["record_id"]: r for r in _provenance()}
    use = recs[RECORDS[1]]
    assert use["standard_number"] is None and use["jurisdiction"] == "US"
    assert use["url"] == RIGHTS_URL == recs["electronics_electrical:PR023"]["url"]
    for phrase in ("electronics_electrical:PR007, PR011, PR015 and PR023", "ONE new claim", "Lead-supplied",
                   "not independently re-inspected by the executor", "2026-10-15"):
        assert phrase in use["version_or_edition"], phrase
    assert use["notes"].startswith("SOURCE-USE COMPATIBILITY DISPOSITION AND RIGHTS BOUNDARY (not a legal opinion")
    for phrase in ("electronics_electrical:PR024", "ONLY", "RIGHTS BASIS", "17 U.S.C. § 105",
                   "authors' NIST employment is not independently verified by the executor", "passage-level",
                   "NOT treated as unrestricted reusable material",
                   "electronics_electrical:PR015 and electronics_electrical:PR023 are NOT broadened",
                   "every VIM, GUM, ISO, JCGM or other third-party definition",
                   "no source sentence, definition, figure or table is reproduced", "InventorAI Arabic translation",
                   "no statement or implication that NIST or the authors reviewed, approved, certified or endorse",
                   "no NIST logo or mark", "InventorAI remains responsible for its own presented output"):
        assert phrase in use["notes"], phrase
    # PR #822 IP-evidence correction: the article-level notice is recorded as Lead-supplied, bounded to the United
    # States, with third-party material excluded and the residual uncertainty stated
    assert PMC_URL in use["version_or_edition"]
    for phrase in ("ARTICLE-LEVEL EVIDENCE (Lead-supplied)", PMC_URL, "lists all five authors with NIST affiliation",
                   "public domain within the United States",
                   "exceptions for independently copyrighted third-party illustrations or material",
                   "RESIDUAL UNCERTAINTY", "has NOT been independently established, by the Lead or the executor",
                   "not read as making the whole publication, its third-party material or all NIST material unrestricted",
                   "every independently copyrighted third-party illustration or material"):
        assert phrase in use["notes"], phrase


def test_p06_the_page_copy_carries_the_attribution_adaptation_and_no_endorsement_in_both_languages():
    for lang in ("en", "ar"):
        source = ui_text.text(STEM + "SOURCE", lang)
        for phrase in ("NIST", "Phillips", "Estler", "Doiron", "Eberhardt", "Levenson",
                       "A Careful Consideration of the Calibration Concept", "106", "371–379", "2.1", "2.2",
                       URL, "InventorAI", "VIM", "GUM"):
            assert phrase in source, (lang, phrase)
    en = ui_text.text(STEM + "SOURCE", "en")
    for phrase in ("Adapted:", "in its own words", "Arabic version is InventorAI's translation",
                   "No sentence, definition, figure or table", "does not imply", "endorsed"):
        assert phrase in en, phrase
    ar = ui_text.text(STEM + "SOURCE", "ar")
    assert "⁦" + URL + "⁩" in ar                         # LTR isolate around the link
    for phrase in ("مُقتبَس", "ترجمة InventorAI", "أيّدوه"):
        assert phrase in ar, phrase
