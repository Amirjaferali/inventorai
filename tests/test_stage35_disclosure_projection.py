"""Stage 35 — Structured Invention Disclosure Export — first bounded slice —
projection (BASE RED, file P).

Implementation contract ``docs/governance/STAGE35_DISCLOSURE_EXPORT_FIRST_SLICE_IMPLEMENTATION_CONTRACT.md``
§3 (snapshot, failure classes), §5–§8 (sources and mapping), §9 (schema) and
§14 (#1–#28, P rows).

Two seams are exercised: the pure composition over already-materialized sources
(``compose_projection``), with in-memory fixtures built through the canonical
carriers, and the store-backed composer (``compose_disclosure_projection``) over
the real on-disk store and real web journeys.
"""
import copy
import json
import os
import re
import socket
import sqlite3

import pytest

import web.app as webapp
from engine import disclosure_export as dx
from engine import experiment_result as er
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    AcknowledgedUnknown, AssertionRecord, Evidence, Gap, IdeaState, OWNER_STATED,
    REASONED, SuccessCriterion, TestHypothesis, UNVALIDATED,
)
from engine.need_routing import NeedRoutingRevision
from engine.read_export_service import ProjectAccessDenied
from engine.requirement_quantity import RequirementQuantity
from engine.subsystem_model import InterfaceDependency, Subsystem, SubsystemInterface
from tests.test_stage19_durable_success_criteria import (
    _client_for, _journey, _live_ids,
)

# ---------------------------------------------------------------------------
# fixed text (workstream contract §10; implementation contract §12)
# ---------------------------------------------------------------------------
DISCLAIMERS_EN = (
    "This document is not legal advice. InventorAI does not provide legal services.",
    "This document is not a patentability opinion. InventorAI has not assessed whether "
    "this invention is new, inventive or patentable.",
    "This document is not a prior-art search. InventorAI has not searched for or "
    "cleared prior art.",
    "This document is not a freedom-to-operate opinion.",
    "This document is not a filing-ready patent application.",
    "InventorAI has not drafted or generated any patent claim in this document. Any "
    "claim-like wording appears only inside text quoted from the inventor, reproduced "
    "as written and not assessed. Nothing in this document is a legally valid claim.",
    "Evidence recorded here is not a validated conclusion. Items marked unvalidated "
    "have not been checked by InventorAI.",
    "This document does not establish a conception date, an invention date, priority, "
    "inventorship or ownership.",
    "Any digest or date in this document is an integrity aid only. It is not a legal "
    "timestamp, a notarization or proof of priority.",
    "Sharing this document may count as a disclosure of the invention in some "
    "jurisdictions. Consult a qualified patent professional before sharing it.",
    "For legal advice, consult a qualified patent professional.",
)
SCOPE_EN = "Invention disclosure export — this project only — not legal advice"
SCOPE_AR = "تصدير الإفصاح عن الاختراع — هذا المشروع فقط — ليس استشارة قانونية"
CAPTURE_LIMITATION = (
    "InventorAI captures the problem statement at the step where the inventor "
    "describes the problem and may shorten it at a 500-character limit. The text "
    "shown here may therefore have been shortened; an ellipsis (…) at its end may "
    "indicate that shortening.")
FIELDS = (
    "invention_title", "problem_addressed", "background_and_existing_limitations",
    "invention_objective", "technical_concept", "parts",
    "component_descriptions_beyond_parts", "relationships",
    "operating_sequence_or_workflow", "alternative_embodiments",
    "typed_materials_dimensions_parameters_conditions",
    "raw_materials_dimensions_parameters_conditions",
    "interface_verification_preparation_inputs", "novelty_and_differentiation",
    "unresolved_technical_issues", "assumptions", "missing_information",
    "technical_evidence", "commercial_manufacturing_integration_evidence",
    "diagrams_and_files", "experiments", "experiment_result_text",
    "validation_results", "risks", "uncertainty_and_abstentions", "corrections",
    "approvals", "source_and_provenance_references", "requirement_landscape",
)
TRUTH_BEARING = {"resolved_problem", "known_mechanism", "part", "interface",
                 "unresolved_gap", "declared_contradiction",
                 "declared_contradiction_history", "assumption", "acknowledged_unknown",
                 "recorded_unknown", "routed_specialist_need", "experiment",
                 "correction_version", "requirement", "requirement_quantity"}
REFERENCE_ONLY = {"gap_reference": "unresolved_gap",
                  "evidence_reference": ("resolved_problem", "known_mechanism")}
EMPTY_MD = {"success_criteria": {}, "measurement_methods": {}, "test_hypotheses": {},
            "test_variables": {}}

PROBLEM = "Wheelchair users cannot cross a single step at a doorway."
MECH = ("The deck panel rests on a hinge line and a spring latch transfers the load "
        "into the frame rail so the ramp stays flat.")
SUB_A = "sub-" + "a" * 32
SUB_B = "sub-" + "b" * 32
IFC = "ifc-" + "c" * 32
QT = "mechanical:PHYSICAL_FEASIBILITY:Q1"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _src(state, quantities=(), planning=None, deps=(), events=(), outcomes=None):
    return dx.MaterializedSources(
        state=state, requirement_quantities=tuple(quantities),
        planning_metadata=copy.deepcopy(EMPTY_MD) if planning is None else planning,
        interface_dependencies=tuple(deps), result_events=tuple(events),
        section_outcomes=dict(outcomes or {}))


def _compose(state, **kw):
    return dx.compose_projection(_src(state, **kw))


def _field(content, token):
    [f] = [f for f in content["fields"] if f["field"] == token]
    return f


def _items(content, token, kind=None):
    return [i for i in _field(content, token)["items"] if kind is None or i["kind"] == kind]


def _index(content):
    return {i["item_key"]: i for f in content["fields"] for i in f["items"]}


def _dump(content):
    return json.dumps(content, ensure_ascii=False, sort_keys=True)


def _values(content):
    """Every value object in ``content`` with its item kind and slot token."""
    for f in content["fields"]:
        for item in f["items"]:
            for slot, value in item["slots"].items():
                yield item, slot, value


def _rec(state, rid):
    return next(r for r in state.assertions if r.record_id == rid)


def _q(seq, anchor, text, kind="target_value", supersedes=None):
    return RequirementQuantity(
        quantity_id="qty-%032x" % (seq + 1), quantity_seq=seq, anchor_record_id=anchor,
        requirement_id="req:assertion:" + anchor, quantity_kind=kind, value_text=text,
        supersedes_quantity_id=supersedes, event_key="%032x" % (seq + 500),
        recorded_iteration=1, recorded_at="2026-10-01T00:00:00+00:00")


def _route(gap="PHYSICAL_FEASIBILITY", qid="mechanical:PHYSICAL_FEASIBILITY:Q2"):
    return NeedRoutingRevision(
        project_id="p", routing_seq=0, gap_type=gap, question_id=qid,
        after_assertion_seq=-1, operation="ROUTE", required_input="SPECIALIST",
        policy_ref="safe-question-routing/v1", supersedes_seq=None,
        provenance="SYSTEM_INFERRED", event_key="e" * 32)


def _base_state():
    s = IdeaState(idea_id="stage35")
    s.idea_summary = PROBLEM
    s.idea_summary_quality = REASONED
    s.known_mechanism = Evidence(MECH, REASONED, 1, provenance=OWNER_STATED)
    s.gaps = [Gap("MECHANISM_COMPLETENESS", "OPEN", 0),
              Gap("PHYSICAL_FEASIBILITY", "PARTIAL", 0),
              Gap("BOUNDARY_AMBIGUITY", "CLOSED", 0)]
    return s


def _rich():
    """A fully populated in-memory project: every first-slice owner holds items."""
    s = _base_state()
    s.acknowledged_unknowns = [
        AcknowledgedUnknown(1, "PHYSICAL_FEASIBILITY",
                            "I do not know how much load the hinge pin carries.", "explicit"),
        AcknowledgedUnknown(2, "BOUNDARY_AMBIGUITY",
                            "Unclear which doorways fit. Success criterion: it fits a "
                            "90 cm doorway.", "explicit")]
    s.record_interaction("answered", "The hinge line runs along the deck edge.",
                         gap_context="MECHANISM_COMPLETENESS")                      # rec_1
    s.record_interaction("answered", "The latch is spring-loaded.",
                         gap_context="PHYSICAL_FEASIBILITY")                        # rec_2
    s.record_interaction("answered", "The latch needs no spring.",
                         gap_context="PHYSICAL_FEASIBILITY")                        # rec_3
    s.record_contradiction_declaration("rec_2", "rec_3", content="cannot both hold")  # rec_4
    s.record_interaction("unknown", "", gap_context="BOUNDARY_AMBIGUITY")            # rec_5
    a = s.record_interaction("provisional_assumption", "Assume the pin carries 150 kg.",
                             gap_context="PHYSICAL_FEASIBILITY", question_target=QT)  # rec_6
    b = s.record_interaction("answered", "The pin carries 150 kg.",
                             gap_context="PHYSICAL_FEASIBILITY", question_target=QT,
                             supersedes=[a.record_id])                              # rec_7
    s.record_interaction("answered", "The pin carries 180 kg.",
                         gap_context="PHYSICAL_FEASIBILITY", question_target=QT,
                         supersedes=[b.record_id])                                  # rec_8
    c1 = s.record_interaction("answered", "Old wording of the deck.",
                              gap_context="MECHANISM_COMPLETENESS")                 # rec_9
    s.record_interaction("answered", "New wording of the deck.",
                         gap_context="MECHANISM_COMPLETENESS", supersedes=[c1.record_id])  # rec_10
    s.record_interaction("specialist_requested", "", gap_context="PHYSICAL_FEASIBILITY")  # rec_11
    s.need_routing = [_route()]
    s.subsystems = [
        Subsystem(SUB_A, "mechanical", "Deck", "Carries the user", OWNER_STATED, UNVALIDATED),
        Subsystem(SUB_B, "electronics_electrical", "Step sensor", "Detects the step",
                  OWNER_STATED, UNVALIDATED)]
    s.subsystem_interfaces = [SubsystemInterface(
        IFC, SUB_A, SUB_B, "The sensor is mounted under the deck.", OWNER_STATED,
        UNVALIDATED)]
    return s


def _rich_sources(state=None):
    state = state or _rich()
    ids = [it["experiment_id"] for it in
           assemble_deliverable(copy.deepcopy(state))["section_11_prototype_test_plan"]["items"]]
    planning = copy.deepcopy(EMPTY_MD)
    planning["success_criteria"] = {ids[0]: SuccessCriterion("The pin load is known.")}
    planning["test_hypotheses"] = {ids[0]: TestHypothesis("The pin carries the load.")}
    ctx = er.ResultContext("Experiment")
    events = (er.recorded_root(ids[0], "observed once", ctx),)
    quantities = (_q(0, "rec_1", "12 V"), _q(1, "rec_1", "0.5–0.8 mm",
                                             supersedes="qty-%032x" % 1),
                  _q(2, "rec_9", "≈3 kg", kind="maximum_value"))
    deps = (InterfaceDependency(IFC, "one_way", SUB_B, SUB_A, "The sensor needs the deck."),)
    return _src(state, quantities=quantities, planning=planning, deps=deps, events=events)


def _rich_content():
    return dx.compose_projection(_rich_sources())


# ===========================================================================
# #12 / §9 — versions, top level, determinism, digest
# ===========================================================================
def test_12_versions_top_level_and_determinism():
    a = _rich_content()
    b = _rich_content()
    assert a == b
    assert dx.canonical_bytes(a) == dx.canonical_bytes(b)
    assert set(a) == {"disclaimers", "scope_label", "unavailable_notice", "fields"}
    assert [f["field"] for f in a["fields"]] == list(FIELDS)
    doc1 = dx.export_document(a, "2026-10-05T00:00:00Z", dx.JSON_FORMAT_VERSION)
    doc2 = dx.export_document(a, "2027-01-01T12:34:56Z", dx.JSON_FORMAT_VERSION)
    assert set(doc1) == {"content", "content_digest", "disclosure_schema_version",
                         "export_format_version", "generated_at"}
    assert doc1["content_digest"] == doc2["content_digest"]          # outside the digest
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", doc1["content_digest"])
    assert doc1["disclosure_schema_version"] == "inventorai-disclosure/1"
    assert dx.JSON_FORMAT_VERSION == "inventorai-disclosure-json/1"
    assert dx.HTML_FORMAT_VERSION == "inventorai-disclosure-html/1"
    assert (dx.JSON_FILE_NAME, dx.HTML_FILE_NAME) == (
        "inventorai-disclosure-export-v1.json", "inventorai-disclosure-export-v1.html")
    import hashlib
    canonical = json.dumps(a, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                           allow_nan=False).encode("utf-8")
    assert doc1["content_digest"] == "sha256:" + hashlib.sha256(canonical).hexdigest()
    body = dx.serialize_json(doc1)
    assert body == json.dumps(doc1, sort_keys=True, ensure_ascii=False, indent=2,
                              separators=(",", ": "), allow_nan=False) + "\n"
    assert json.loads(body) == doc1
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", dx.generated_at_now())


# ===========================================================================
# #2 — disclaimers and scope label in the projection
# ===========================================================================
def test_02_disclaimers_and_scope_label():
    c = _rich_content()
    assert [d["id"] for d in c["disclaimers"]] == ["D%02d" % n for n in range(1, 12)]
    assert tuple(d["en"] for d in c["disclaimers"]) == DISCLAIMERS_EN
    assert c["disclaimers"][0]["ar"] == "هذه الوثيقة ليست استشارة قانونية، ولا يقدّم InventorAI خدمات قانونية."
    assert all(d["ar"] and set(d) == {"id", "en", "ar"} for d in c["disclaimers"])
    assert c["scope_label"] == {"en": SCOPE_EN, "ar": SCOPE_AR}
    assert "D12" not in _dump(c)


# ===========================================================================
# #1 — prohibited wording in system assertions (quoted content excluded structurally)
# ===========================================================================
PROHIBITED = (r"\bpatent", r"\bnovel", r"\binventive", r"\bprior[- ]art",
              r"\bfreedom[- ]to[- ]operate", r"\bfiling", r"\blegal", r"\battorney",
              r"\blawyer", r"what is claimed", r"\bwe claim", r"\bclaim \d",
              r"\b(in)?dependent claim")


def test_01_no_prohibited_wording_in_system_assertions():
    c = _rich_content()
    for item, slot, value in _values(c):
        if value["marker"] == "RECORDED" and value["content_class"] == "SYSTEM_ASSERTION" \
                and value["value"]:
            for pattern in PROHIBITED:
                assert not re.search(pattern, value["value"], re.I), (slot, value["value"])
    assert c["scope_label"]["en"] == SCOPE_EN


# ===========================================================================
# #3 — markers
# ===========================================================================
_FIXED = {
    "invention_title": ("NOT_CAPTURED", None),
    "background_and_existing_limitations": ("NOT_CAPTURED", None),
    "invention_objective": ("NOT_CAPTURED", None),
    "operating_sequence_or_workflow": ("NOT_CAPTURED", None),
    "alternative_embodiments": ("NOT_CAPTURED", None),
    "typed_materials_dimensions_parameters_conditions": ("NOT_CAPTURED", None),
    "interface_verification_preparation_inputs": ("EXCLUDED_FROM_FIRST_SLICE", "PLANNING_INPUTS"),
    "novelty_and_differentiation": ("NOT_CAPTURED", None),
    "commercial_manufacturing_integration_evidence": (
        "EXCLUDED_FROM_FIRST_SLICE", "CONFIDENTIAL_EVIDENCE_CATEGORIES"),
    "diagrams_and_files": ("NOT_CAPTURED", None),
    "experiment_result_text": ("EXCLUDED_FROM_FIRST_SLICE", "RESULT_TEXT_NOT_CARRIED"),
    "validation_results": ("NOT_CAPTURED", None),
    "uncertainty_and_abstentions": ("NOT_APPLICABLE", "CARRIED_ON_EVERY_ITEM"),
    "approvals": ("NOT_CAPTURED", "NO_APPROVAL_RECORD"),
    "source_and_provenance_references": ("NOT_APPLICABLE", "CARRIED_ON_EVERY_ITEM"),
}


def test_03_fixed_markers_and_integrated_fields():
    c = _rich_content()
    for token, (marker, reason) in _FIXED.items():
        f = _field(c, token)
        assert (f["marker"], f["reason"], f["pointer"], f["items"]) == (marker, reason, None, [])
    assert _field(c, "parts")["marker"] == "RECORDED"
    assert _field(c, "relationships")["marker"] == "RECORDED"
    assert (_field(c, "component_descriptions_beyond_parts")["marker"],
            _field(c, "component_descriptions_beyond_parts")["reason"]) == ("NOT_CAPTURED", None)
    for token in ("problem_addressed", "technical_concept", "unresolved_technical_issues",
                  "assumptions", "missing_information", "technical_evidence",
                  "experiments", "risks", "corrections", "requirement_landscape",
                  "raw_materials_dimensions_parameters_conditions"):
        assert _field(c, token)["marker"] == "RECORDED", token
    assert c["unavailable_notice"] is False
    assert "UNAVAILABLE" not in _dump(c)


def test_03_non_integrated_project_never_nothing_recorded_for_parts():
    c = _compose(_base_state())
    for token in ("parts", "component_descriptions_beyond_parts", "relationships"):
        f = _field(c, token)
        assert (f["marker"], f["reason"]) == ("NOT_CAPTURED", "NON_INTEGRATED_PROJECT")


def test_03_integrated_without_interfaces_is_nothing_recorded():
    s = _rich()
    s.subsystem_interfaces = []
    c = _compose(s)
    assert _field(c, "relationships")["marker"] == "NOTHING_RECORDED"
    assert _field(c, "parts")["marker"] == "RECORDED"


def test_03_empty_project_nothing_recorded():
    c = _compose(IdeaState(idea_id="empty"))
    for token in ("problem_addressed", "technical_concept", "unresolved_technical_issues",
                  "assumptions", "missing_information", "technical_evidence",
                  "experiments", "risks", "corrections", "requirement_landscape",
                  "raw_materials_dimensions_parameters_conditions"):
        f = _field(c, token)
        assert (f["marker"], f["items"]) == ("NOTHING_RECORDED", []), token
    for f in c["fields"]:
        assert f["marker"] in ("RECORDED", "NOTHING_RECORDED", "NOT_CAPTURED",
                               "RAW_TEXT_ONLY", "EXCLUDED_FROM_FIRST_SLICE",
                               "NOT_APPLICABLE")


# ===========================================================================
# #4 — no external transfer
# ===========================================================================
def test_04_no_network_no_provider_import(monkeypatch):
    src = open(dx.__file__, encoding="utf-8").read()
    for banned in ("import socket", "urllib", "requests", "http.client", "smtplib",
                   "email", "openai", "anthropic", "provider", "subprocess"):
        assert not re.search(r"^\s*(import|from)\s+[^\n]*" + re.escape(banned.split()[-1]),
                             src, re.M), banned

    def _no_network(*a, **kw):
        raise AssertionError("network attempted")

    monkeypatch.setattr(socket, "socket", _no_network)
    monkeypatch.setattr(socket, "create_connection", _no_network)
    c = _rich_content()
    dx.serialize_json(dx.export_document(c, "2026-10-05T00:00:00Z", dx.JSON_FORMAT_VERSION))


# ===========================================================================
# #7 / #27 — envelope fidelity and attribution coverage
# ===========================================================================
def test_07_envelope_values_come_from_the_owner():
    s = _rich()
    c = dx.compose_projection(_rich_sources(s))
    [problem] = _items(c, "problem_addressed")
    text = problem["slots"]["text"]
    resolved = Evidence(PROBLEM, REASONED, 0)
    assert text["content_class"] == "QUOTED_INVENTOR_CONTENT"
    assert text["source_owner"] == "SECTION2_RESOLUTION"
    assert text["envelope"] == {
        "provenance": {"marker": "RECORDED", "value": resolved.provenance},
        "validation_state": {"marker": "RECORDED", "value": resolved.validation_status},
        "limitation": {"marker": "NOT_APPLICABLE", "value": None},
        "currency": {"marker": "NOT_APPLICABLE", "value": None}}
    [mech] = _items(c, "technical_concept")
    assert mech["slots"]["text"]["envelope"]["provenance"] == {"marker": "RECORDED",
                                                               "value": OWNER_STATED}
    [assumption] = _items(c, "assumptions")
    env = assumption["slots"]["text"]["envelope"]
    assert env["provenance"]["value"] == _rec(s, "rec_6").provenance
    assert env["validation_state"]["value"] == UNVALIDATED
    assert env["currency"] == {"marker": "RECORDED", "value": "SUPERSEDED"}
    [gap_open, gap_partial] = _items(c, "unresolved_technical_issues", "unresolved_gap")
    assert gap_open["slots"]["gap_state"]["envelope"] == {
        k: {"marker": "NOT_APPLICABLE", "value": None}
        for k in ("provenance", "validation_state", "limitation", "currency")}
    assert gap_open["slots"]["gap_state"]["tokens"] == {"gap_type": "MECHANISM_COMPLETENESS",
                                                         "gap_status": "OPEN"}
    assert gap_partial["slots"]["gap_state"]["tokens"]["gap_status"] == "PARTIAL"
    [route] = _items(c, "missing_information", "routed_specialist_need")
    assert route["slots"]["routed_need"]["envelope"]["provenance"] == {
        "marker": "RECORDED", "value": "SYSTEM_INFERRED"}
    assert route["slots"]["routed_need"]["tokens"] == {"gap_type": "PHYSICAL_FEASIBILITY",
                                                       "required_input": "SPECIALIST"}
    for item, _slot, value in _values(c):
        if value["marker"] == "RECORDED":
            assert value["envelope"]["limitation"] == {"marker": "NOT_APPLICABLE",
                                                       "value": None}
    def _keys(node):
        if isinstance(node, dict):
            for k, v in node.items():
                yield k
                yield from _keys(v)
        elif isinstance(node, list):
            for v in node:
                yield from _keys(v)
    assert not any("approv" in k for k in _keys(c))


def test_27_attribution_coverage():
    c = _rich_content()
    index = _index(c)
    for f in c["fields"]:
        for item in f["items"]:
            recorded = [v for v in item["slots"].values() if v["marker"] == "RECORDED"]
            if item["kind"] in TRUTH_BEARING:
                assert recorded, item["item_key"]
                for v in recorded:
                    assert v["content_class"] in ("SYSTEM_ASSERTION", "QUOTED_INVENTOR_CONTENT")
                    assert v["source_owner"]
                    assert set(v["envelope"]) == {"provenance", "validation_state",
                                                  "limitation", "currency"}
            else:
                assert item["kind"] in REFERENCE_ONLY
                assert not recorded and len(item["refs"]) == 1
                target = index[item["refs"][0]]["kind"]
                want = REFERENCE_ONLY[item["kind"]]
                assert target in (want if isinstance(want, tuple) else (want,))
    [ev1, ev2] = _items(c, "technical_evidence")
    assert ev1["slots"] == {"cap11_form": {
        "marker": "EXCLUDED_FROM_FIRST_SLICE", "reason": "FORM_ROW_QUALITY_DERIVED",
        "content_class": None, "value": None, "tokens": {}, "source_owner": None,
        "envelope": None}}
    assert (ev1["refs"], ev2["refs"]) == (["problem_addressed.1"], ["technical_concept.1"])


def _refused(content):
    with pytest.raises(dx.DisclosureExportRefused):
        dx.check_projection(content)


def test_27_schema_check_refuses_attribution_defects():
    c = _rich_content()
    dx.check_projection(c)
    bad = copy.deepcopy(c)
    _items(bad, "assumptions")[0]["slots"]["text"]["envelope"] = None
    _refused(bad)
    bad = copy.deepcopy(c)
    _items(bad, "risks")[0]["slots"]["text"] = copy.deepcopy(
        _items(c, "assumptions")[0]["slots"]["text"])
    _refused(bad)
    bad = copy.deepcopy(c)
    _items(bad, "risks")[0]["refs"] = ["unresolved_technical_issues.99"]
    _refused(bad)
    bad = copy.deepcopy(c)
    _items(bad, "risks")[0]["refs"] = []
    _refused(bad)
    bad = copy.deepcopy(c)                                 # an injected default
    _items(bad, "unresolved_technical_issues", "unresolved_gap")[0]["slots"][
        "gap_state"]["envelope"]["provenance"] = {"marker": "RECORDED", "value": OWNER_STATED}
    _refused(bad)
    bad = copy.deepcopy(c)
    _items(bad, "assumptions")[0]["tokens"]["confidence"] = 1
    _refused(bad)
    bad = copy.deepcopy(c)
    bad["fields"][0]["unknown"] = 1
    _refused(bad)
    bad = copy.deepcopy(c)
    bad["fields"][1]["marker"] = "VALIDATED"
    _refused(bad)
    bad = copy.deepcopy(c)
    _items(bad, "assumptions")[0]["kind"] = "claim"
    _refused(bad)


# ===========================================================================
# #8 — excluded content absent; no internal identifier
# ===========================================================================
def test_08_excluded_content_and_identifiers_absent():
    s = _rich()
    c = dx.compose_projection(_rich_sources(s))
    dump = _dump(c)
    for banned in ("rec_", "sub-", "ifc-", "qty-", "exp_", "req:", "routing:",
                   "UNDETERMINED", "system-derived", "criticality", "quality",
                   "maturity", "readiness", "Reasoned", "Demonstrated", "REASONED",
                   "verdict", "PROCEED", "REVISE", "mechanical:PHYSICAL_FEASIBILITY:Q",
                   "stage35", "cannot both hold", "observed once", "source_basis",
                   "minimum_prototype", "risk_id", "Grounded"):
        assert banned not in dump, banned
    [claim] = [i for i in _items(c, "experiments")
               if i["slots"]["objective"]["marker"] == "EXCLUDED_FROM_FIRST_SLICE"]
    assert claim["slots"]["objective"]["reason"] == "OBJECTIVE_NAMES_EVIDENCE_LEVEL"


# ===========================================================================
# #9 / #21 — problem seam and capture limitation
# ===========================================================================
def test_09_known_problem_is_never_read():
    s = _base_state()
    s.known_problem = Evidence("SENTINEL-KNOWN-PROBLEM from a mechanism answer", REASONED, 2)
    c = _compose(s)
    assert "SENTINEL-KNOWN-PROBLEM" not in _dump(c)
    assert _items(c, "problem_addressed")[0]["slots"]["text"]["value"] == PROBLEM
    assert "known_problem" not in open(dx.__file__, encoding="utf-8").read()


@pytest.mark.parametrize("text", ["Short.", "x" * 500, ("word " * 99) + "word…",
                                  "The inventor ended with an ellipsis…"])
def test_21_capture_limitation_unconditional(text):
    s = IdeaState(idea_id="p")
    s.idea_summary = text
    c = _compose(s)
    [item] = _items(c, "problem_addressed")
    assert item["slots"]["text"]["value"] == text.strip()
    lim = item["slots"]["capture_limitation"]
    assert (lim["marker"], lim["content_class"], lim["source_owner"], lim["value"]) == (
        "RECORDED", "SYSTEM_ASSERTION", "DISCLOSURE_EXPORT", CAPTURE_LIMITATION)
    assert list(item["slots"]) == ["text", "capture_limitation"] or set(item["slots"]) == {
        "text", "capture_limitation"}
    bad = copy.deepcopy(c)
    _items(bad, "problem_addressed")[0]["slots"]["capture_limitation"]["value"] = "It was shortened."
    _refused(bad)
    bad = copy.deepcopy(c)
    del _items(bad, "problem_addressed")[0]["slots"]["capture_limitation"]
    _refused(bad)


def test_21_no_problem_no_item_no_limitation():
    c = _compose(IdeaState(idea_id="p"))
    assert _field(c, "problem_addressed")["marker"] == "NOTHING_RECORDED"
    assert CAPTURE_LIMITATION not in _dump(c)


# ===========================================================================
# #13 — hostile inventor text
# ===========================================================================
HOSTILE = ("<script>alert(1)</script> <a href=\"javascript:x\">x</a> {{ 7*7 }} {% if %} "
           "\u202eevil\u202c \u2066iso\u2069 \x07 mail@example.com ghp_token123 "
           "/etc/passwd C:\\path " + "W" * 2000)


def test_13_hostile_text_round_trips_exactly():
    s = _base_state()
    s.idea_summary = HOSTILE
    s.record_interaction("answered", HOSTILE, gap_context="MECHANISM_COMPLETENESS")
    c = _compose(s)
    doc = dx.export_document(c, "2026-10-05T00:00:00Z", dx.JSON_FORMAT_VERSION)
    back = json.loads(dx.serialize_json(doc))
    assert _items(back["content"], "problem_addressed")[0]["slots"]["text"]["value"] == HOSTILE.strip()
    [row] = [i for i in _items(back["content"], "requirement_landscape")
             if i["tokens"]["anchor_kind"] == "assertion"]
    assert row["slots"]["statement"]["value"] == HOSTILE


def test_13_unencodable_value_refuses():
    s = IdeaState(idea_id="p")
    s.idea_summary = "bad \ud800 surrogate"
    with pytest.raises(dx.DisclosureExportRefused):
        _compose(s)


# ===========================================================================
# #18 — experiment slots
# ===========================================================================
def test_18_experiment_allow_list_and_classes():
    s = _rich()
    package = assemble_deliverable(copy.deepcopy(s))["section_11_prototype_test_plan"]
    c = dx.compose_projection(_rich_sources(s))
    items = _items(c, "experiments")
    assert len(items) == len(package["items"]) == 3
    by_type = {}
    for it, src in zip(items, package["items"]):
        by_type[src["traceability"]["source_type"]] = (it, src)
        assert set(it["slots"]) == {"title", "objective", "what_to_observe",
                                    "success_criterion", "measurement_method",
                                    "test_hypothesis", "test_variable", "execution_state"}
        assert it["slots"]["title"]["value"] == src["experiment_title"]
        assert it["slots"]["title"]["content_class"] == "SYSTEM_ASSERTION"
        assert it["slots"]["what_to_observe"]["value"] == src["what_to_observe"]
        assert it["tokens"] == {} and it["refs"] == []
    first, src1 = items[0], package["items"][0]
    assert src1["traceability"]["source_type"] == "acknowledged_unknown"
    assert first["slots"]["objective"]["value"] == src1["objective"]
    crit = first["slots"]["success_criterion"]
    assert (crit["content_class"], crit["value"], crit["source_owner"]) == (
        "QUOTED_INVENTOR_CONTENT", "The pin load is known.", "PLANNING_METADATA")
    assert crit["envelope"]["provenance"] == {"marker": "RECORDED", "value": "user_defined"}
    assert first["slots"]["test_hypothesis"]["value"] == "The pin carries the load."
    for slot in ("measurement_method", "test_variable"):
        assert first["slots"][slot]["marker"] == "NOTHING_RECORDED"
    assert first["slots"]["execution_state"]["tokens"] == {"state": "recorded", "count": 1}
    assert first["slots"]["execution_state"]["source_owner"] == "EXPERIMENT_RESULTS"
    second = items[1]
    assert package["items"][1]["success_criterion_provenance"] == "source_stated"
    assert second["slots"]["success_criterion"]["envelope"]["provenance"]["value"] == "source_stated"
    assert second["slots"]["success_criterion"]["content_class"] == "QUOTED_INVENTOR_CONTENT"
    assert second["slots"]["execution_state"]["tokens"] == {"state": "none", "count": 0}
    claim, src3 = by_type["reasoned_leading_claim"]
    assert claim["slots"]["objective"]["marker"] == "EXCLUDED_FROM_FIRST_SLICE"
    assert src3["success_criterion_status"] == "required"
    assert claim["slots"]["success_criterion"]["marker"] == "NOTHING_RECORDED"
    assert claim["slots"]["what_to_observe"]["marker"] == "RECORDED"


def test_18_none_planning_collection_refuses():
    planning = copy.deepcopy(EMPTY_MD)
    planning["test_variables"] = None
    with pytest.raises(dx.DisclosureExportRefused):
        _compose(_rich(), planning=planning)


# ===========================================================================
# #19 — Requirement Landscape classes
# ===========================================================================
def test_19_landscape_rows_are_never_one_combined_string():
    s = _rich()
    c = dx.compose_projection(_rich_sources(s))
    rows = _items(c, "requirement_landscape")
    kinds = [r["tokens"]["anchor_kind"] for r in rows]
    assert kinds[0] == "active_contradiction"
    declared = rows[0]
    assert set(declared["slots"]) == {"label", "status", "resolving_action", "answer_a",
                                      "answer_b"}
    assert declared["slots"]["answer_a"]["value"] == "The latch is spring-loaded."
    assert declared["slots"]["answer_b"]["value"] == "The latch needs no spring."
    assert declared["slots"]["label"]["value"] == "Contradiction you declared"
    [iface] = [r for r in rows if r["tokens"]["anchor_kind"] == "subsystem_interface"]
    assert set(iface["slots"]) == {"label", "status", "resolving_action", "part_a",
                                   "part_b", "description"}
    assert (iface["slots"]["part_a"]["value"], iface["slots"]["part_b"]["value"]) == (
        "Deck", "Step sensor")
    assert iface["refs"] == ["relationships.1"]
    for row in rows:
        statement = row["slots"].get("statement")
        if statement and statement["content_class"] == "SYSTEM_ASSERTION":
            assert "“" not in (statement["value"] or "")
    dump = _dump(c)
    assert "You declared an interaction between" not in dump
    assert "You marked these two recorded answers" not in dump
    [pending] = [r for r in rows if r["tokens"]["anchor_kind"] == "pending_specialist"
                 and r["slots"]["statement"]["marker"] == "NOTHING_RECORDED"]
    assert "Specialist input requested" not in dump
    [routing] = [r for r in rows if r["tokens"]["anchor_kind"] == "pending_specialist"
                 and r["slots"]["statement"]["marker"] == "RECORDED"]
    assert routing["slots"]["statement"]["content_class"] == "SYSTEM_ASSERTION"


def test_19_unresolvable_interface_part_refuses():
    s = _rich()
    s.subsystem_interfaces = [SubsystemInterface(IFC, SUB_A, "sub-" + "f" * 32, "x",
                                                 OWNER_STATED, UNVALIDATED)]
    with pytest.raises(dx.DisclosureExportRefused):
        _compose(s)


# ===========================================================================
# #20 — OD-A requirement quantities
# ===========================================================================
ODD_VALUES = ("12 V", "0.5–0.8 mm", "≈3 kg", "1,5 bar", "10^3 N", "about 20")


def test_20_quantities_verbatim_owner_tokens_and_refs():
    s = _rich()
    qs = tuple(_q(n, "rec_1", v) for n, v in enumerate(ODD_VALUES))
    qs = qs + (_q(len(qs), "rec_9", "withdrawn 5 V"),)
    c = _compose(s, quantities=qs)
    f12 = _field(c, "raw_materials_dimensions_parameters_conditions")
    assert (f12["marker"], f12["pointer"]) == ("RECORDED", None)
    items = f12["items"]
    assert [i["slots"]["value_text"]["value"] for i in items] == list(ODD_VALUES) + ["withdrawn 5 V"]
    index = _index(c)
    for item in items[:-1]:
        assert set(item["slots"]) == {"value_text"}
        assert set(item["tokens"]) == {"quantity_kind", "active", "anchor_active"}
        v = item["slots"]["value_text"]
        assert (v["content_class"], v["source_owner"]) == ("QUOTED_INVENTOR_CONTENT",
                                                           "REQUIREMENT_QUANTITY")
        assert v["envelope"]["provenance"]["value"] == "OWNER_STATED"
        assert v["envelope"]["validation_state"]["value"] == "UNVALIDATED"
        assert v["envelope"]["currency"]["marker"] == "NOT_APPLICABLE"
        assert item["tokens"]["anchor_active"] is True
        [ref] = item["refs"]
        target = index[ref]
        assert target["kind"] == "requirement"
        assert target["tokens"]["anchor_kind"] == "assertion"
        assert target["slots"]["statement"]["value"] == _rec(s, "rec_1").content
    withdrawn = items[-1]
    assert withdrawn["tokens"]["anchor_active"] is False and withdrawn["refs"] == []
    dump = _dump(c)
    for value in ODD_VALUES:
        assert dump.count(json.dumps(value, ensure_ascii=False)) == 1
    for row in _items(c, "requirement_landscape"):
        assert "value_text" not in row["slots"]
    for key in ("unit", "numeric", "normalized", "magnitude", "parsed"):
        assert '"%s"' % key not in dump


def test_20_schema_check_refuses_a_parsed_quantity_field():
    c = _compose(_rich(), quantities=(_q(0, "rec_1", "12 V"),))
    bad = copy.deepcopy(c)
    _items(bad, "raw_materials_dimensions_parameters_conditions")[0]["tokens"]["unit"] = "V"
    _refused(bad)
    bad = copy.deepcopy(c)
    _items(bad, "raw_materials_dimensions_parameters_conditions")[0]["slots"]["numeric"] = \
        copy.deepcopy(_items(c, "raw_materials_dimensions_parameters_conditions")[0][
            "slots"]["value_text"])
    _refused(bad)


def test_20_field12_raw_text_only_and_nothing_recorded():
    s = _base_state()
    s.record_interaction("answered", "The deck is 80 cm wide.", gap_context="BOUNDARY_AMBIGUITY")
    c = _compose(s)
    f12 = _field(c, "raw_materials_dimensions_parameters_conditions")
    assert (f12["marker"], f12["pointer"], f12["items"]) == (
        "RAW_TEXT_ONLY", "requirement_landscape", [])
    c = _compose(_base_state())
    f12 = _field(c, "raw_materials_dimensions_parameters_conditions")
    assert (f12["marker"], f12["pointer"]) == ("NOTHING_RECORDED", None)


def test_20_quantity_on_a_contradiction_endpoint_refuses_through_the_owner():
    s = _rich()
    with pytest.raises(dx.DisclosureExportRefused):
        _compose(s, quantities=(_q(0, "rec_2", "5 V"),))


# ===========================================================================
# #22 / #25 / #28 — references
# ===========================================================================
_REF_KINDS = {
    "assumption": {"assumption", "requirement", "correction_version"},
    "recorded_unknown": {"requirement"},
    "routed_specialist_need": {"requirement"},
    "gap_reference": {"unresolved_gap"},
    "declared_contradiction": {"requirement"},
    "evidence_reference": {"resolved_problem", "known_mechanism"},
    "requirement_quantity": {"requirement"},
    "correction_version": {"assumption"},
    "interface": {"part"},
    "requirement": {"declared_contradiction", "interface"},
}


def _check_refs(c):
    index = _index(c)
    for f in c["fields"]:
        for item in f["items"]:
            for ref in item["refs"]:
                assert ref in index, (item["item_key"], ref)
                assert index[ref]["kind"] in _REF_KINDS[item["kind"]], (item["item_key"], ref)


def test_22_reference_integrity_in_the_populated_fixture():
    c = _rich_content()
    _check_refs(c)
    index = _index(c)
    for g in _items(c, "missing_information", "gap_reference") + _items(c, "risks"):
        assert index[g["refs"][0]]["kind"] == "unresolved_gap"
    assert len(_items(c, "risks")) == len(_items(c, "unresolved_technical_issues",
                                                 "unresolved_gap")) == 2
    [unknown] = _items(c, "missing_information", "recorded_unknown")
    assert unknown["slots"]["unknown_disposition"]["tokens"] == {
        "disposition": "unknown", "gap_type": "BOUNDARY_AMBIGUITY"}
    [row] = [index[r] for r in unknown["refs"]]
    assert row["tokens"]["anchor_kind"] == "assertion"
    assert row["slots"]["label"]["value"] == "Recorded unknown"
    [route] = _items(c, "missing_information", "routed_specialist_need")
    assert index[route["refs"][0]]["slots"]["statement"]["content_class"] == "SYSTEM_ASSERTION"
    assert [i["slots"]["text"]["value"] for i in
            _items(c, "missing_information", "acknowledged_unknown")] == [
        "I do not know how much load the hinge pin carries.",
        "Unclear which doorways fit. Success criterion: it fits a 90 cm doorway."]
    [declared] = _items(c, "unresolved_technical_issues", "declared_contradiction")
    assert declared["slots"]["declaration"]["tokens"] == {"active": True}
    assert index[declared["refs"][0]]["tokens"]["anchor_kind"] == "active_contradiction"
    [iface] = _items(c, "relationships")
    assert iface["refs"] == ["parts.2", "parts.1"] or iface["refs"] == ["parts.1", "parts.2"]
    dep = iface["slots"]["dependency"]
    assert dep["tokens"] == {"dependency_kind": "one_way", "dependent_part": "parts.2",
                             "depends_on_part": "parts.1"}
    assert iface["slots"]["dependency_note"]["value"] == "The sensor needs the deck."


def test_22_dangling_reference_refuses():
    c = _rich_content()
    bad = copy.deepcopy(c)
    _items(bad, "assumptions")[0]["refs"] = ["requirement_landscape.999"]
    _refused(bad)


def test_25_assumption_origin_history():
    s = _rich()
    c = dx.compose_projection(_rich_sources(s))
    index = _index(c)
    [assumption] = _items(c, "assumptions")
    assert assumption["slots"]["text"]["value"] == "Assume the pin carries 150 kg."
    assert assumption["tokens"] == {"gap_type": "PHYSICAL_FEASIBILITY"}
    chains = {}
    for item in _items(c, "corrections"):
        chains.setdefault(item["tokens"]["chain"], []).append(item)
    texts = {k: [i["slots"]["text"]["value"] for i in v] for k, v in chains.items()}
    assert sorted(texts.values()) == sorted([
        ["The pin carries 150 kg.", "The pin carries 180 kg."],
        ["Old wording of the deck.", "New wording of the deck."]])
    [origin] = [v for v in chains.values() if v[0]["slots"]["text"]["value"] == "The pin carries 150 kg."]
    a, b = origin
    assert (a["tokens"]["position"], b["tokens"]["position"]) == (1, 2)
    assert a["tokens"]["disposition"] == b["tokens"]["disposition"] == "answered"
    assert a["slots"]["text"]["envelope"]["currency"]["value"] == "SUPERSEDED"
    assert b["slots"]["text"]["envelope"]["currency"]["value"] == "CURRENT"
    assert assumption["refs"] == [a["item_key"]]
    assert a["refs"] == [assumption["item_key"]] and b["refs"] == []
    assert any(r["slots"].get("statement", {}).get("value") == "The pin carries 180 kg."
               for r in _items(c, "requirement_landscape"))
    for item in _items(c, "corrections"):
        assert item["kind"] == "correction_version"
    assert "Assume the pin carries 150 kg." not in [
        i["slots"]["text"]["value"] for i in _items(c, "corrections")]
    _check_refs(c)
    assert index[assumption["refs"][0]]["kind"] == "correction_version"


def _assumption_then(answers, two_assumptions=False):
    s = _base_state()
    prior = s.record_interaction("provisional_assumption", "Assume A.",
                                 gap_context="PHYSICAL_FEASIBILITY", question_target=QT)
    if two_assumptions:
        prior = s.record_interaction("provisional_assumption", "Assume A again.",
                                     gap_context="PHYSICAL_FEASIBILITY", question_target=QT,
                                     supersedes=[prior.record_id])
    for text in answers:
        prior = s.record_interaction("answered", text, gap_context="PHYSICAL_FEASIBILITY",
                                     question_target=QT, supersedes=[prior.record_id])
    return s


def test_25_variants_one_answer_and_two_assumptions():
    c = _compose(_assumption_then(["Answer only."]))
    [assumption] = _items(c, "assumptions")
    [row] = [_index(c)[r] for r in assumption["refs"]]
    assert row["kind"] == "requirement" and row["slots"]["statement"]["value"] == "Answer only."
    assert _field(c, "corrections")["marker"] == "NOTHING_RECORDED"
    c = _compose(_assumption_then(["Answer."], two_assumptions=True))
    first, second = _items(c, "assumptions")
    assert first["refs"] == [second["item_key"]]
    assert _index(c)[second["refs"][0]]["slots"]["statement"]["value"] == "Answer."
    _check_refs(c)


def test_25_malformed_ancestry_refuses():
    s = _base_state()
    a = AssertionRecord("rec_1", "provisional_assumption", "Assume.", "PHYSICAL_FEASIBILITY",
                        0, provenance=OWNER_STATED, question_target=QT)
    b = AssertionRecord("rec_2", "answered", "Answer.", "BOUNDARY_AMBIGUITY", 0,
                        provenance=OWNER_STATED, question_target=QT, supersedes=["rec_1"])
    a.superseded_by = "rec_2"
    s.assertions = [a, b]
    with pytest.raises(dx.DisclosureExportRefused):
        _compose(s)


def test_28_canonical_field29_representation():
    # (1) assumption -> answer A, A an endpoint of an active declared contradiction.
    s = _assumption_then(["Answer A."])
    other = s.record_interaction("answered", "Answer C.", gap_context="BOUNDARY_AMBIGUITY")
    a_id = [r.record_id for r in s.assertions if r.content == "Answer A."][0]
    s.record_contradiction_declaration(a_id, other.record_id)
    c = _compose(s)
    [assumption] = _items(c, "assumptions")
    [row] = [_index(c)[r] for r in assumption["refs"]]
    assert row["tokens"]["anchor_kind"] == "active_contradiction"
    rows = _items(c, "requirement_landscape")
    assert not any(r["slots"].get("statement", {}).get("value") == "Answer A." for r in rows)
    _check_refs(c)
    # (3) A an endpoint of two active pairs: both rows, in owner order.
    third = s.record_interaction("answered", "Answer D.", gap_context="BOUNDARY_AMBIGUITY")
    s.record_contradiction_declaration(a_id, third.record_id)
    c = _compose(s)
    [assumption] = _items(c, "assumptions")
    contradiction_rows = [r["item_key"] for r in _items(c, "requirement_landscape")
                          if r["tokens"]["anchor_kind"] == "active_contradiction"]
    assert assumption["refs"] == contradiction_rows and len(contradiction_rows) == 2
    # (2) assumption -> A -> B with B in an active declared contradiction.
    s = _assumption_then(["Answer A.", "Answer B."])
    other = s.record_interaction("answered", "Answer C.", gap_context="BOUNDARY_AMBIGUITY")
    b_id = [r.record_id for r in s.assertions if r.content == "Answer B."][0]
    s.record_contradiction_declaration(b_id, other.record_id)
    c = _compose(s)
    a_item, b_item = _items(c, "corrections")
    [assumption] = _items(c, "assumptions")
    assert assumption["refs"] == [a_item["item_key"]]
    assert a_item["refs"] == [assumption["item_key"]]
    [row] = [r for r in _items(c, "requirement_landscape")
             if r["tokens"]["anchor_kind"] == "active_contradiction"]
    assert "Answer B." in (row["slots"]["answer_a"]["value"], row["slots"]["answer_b"]["value"])
    _check_refs(c)
    # (4) an active unknown joined by a legacy contradicts edge.
    s = _base_state()
    ans = s.record_interaction("answered", "Answer X.", gap_context="BOUNDARY_AMBIGUITY")
    unk = s.record_interaction("unknown", "", gap_context="BOUNDARY_AMBIGUITY")
    s.mark_contradiction(ans.record_id, unk.record_id)
    c = _compose(s)
    [unknown] = _items(c, "missing_information", "recorded_unknown")
    [row] = [_index(c)[r] for r in unknown["refs"]]
    assert row["tokens"]["anchor_kind"] == "active_contradiction"
    assert row["slots"]["statement"]["content_class"] == "SYSTEM_ASSERTION"
    assert row["refs"] == []
    # (5) ordinary fixtures resolve to own rows (covered by #22); (6) quantities (#20).
    _check_refs(c)


# ===========================================================================
# #24 — UNAVAILABLE admission at the section-outcome seam
# ===========================================================================
def test_24b_section_local_outcome_renders_only_its_own_section():
    sources = _rich_sources()
    base = dx.compose_projection(sources)
    failed = dx.compose_projection(dx.MaterializedSources(
        state=sources.state, requirement_quantities=sources.requirement_quantities,
        planning_metadata=sources.planning_metadata,
        interface_dependencies=sources.interface_dependencies,
        result_events=sources.result_events,
        section_outcomes={"experiments": "UNAVAILABLE"}))
    assert failed["unavailable_notice"] is True and base["unavailable_notice"] is False
    f = _field(failed, "experiments")
    assert (f["marker"], f["items"]) == ("UNAVAILABLE", [])
    for a, b in zip(base["fields"], failed["fields"]):
        if a["field"] != "experiments":
            assert a == b
    dx.check_projection(failed)


# ===========================================================================
# store-backed composer: #5 / #6 / #10 / #17 / #23 / #24a / #26
# ===========================================================================
@pytest.fixture()
def owned():
    webapp.app.config["TESTING"] = True
    c, aid = _client_for("s35-owner@example.com")
    sid = _journey(c)
    return c, aid, sid, webapp._get_store()


def _db():
    return os.environ["INVENTORAI_DB_PATH"]


def _store_dump():
    con = sqlite3.connect(_db())
    try:
        return list(con.iterdump())
    finally:
        con.close()


class _SqlLog:
    def __init__(self, real, log):
        self._real, self._log = real, log

    def execute(self, sql, *a):
        self._log.append(" ".join(sql.split()))
        return self._real.execute(sql, *a)

    def __getattr__(self, name):
        return getattr(self._real, name)


def test_composer_returns_a_checked_projection_for_the_owner(owned):
    c, aid, sid, store = owned
    content = dx.compose_disclosure_projection(store, sid, aid)
    dx.check_projection(content)
    assert _field(content, "experiments")["marker"] == "RECORDED"
    assert store.committed_state_readable()


def test_06a_every_read_inside_one_snapshot_r1_reads_last(owned, monkeypatch):
    c, aid, sid, store = owned
    sql, calls = [], []
    monkeypatch.setattr(store, "_conn", _SqlLog(store._conn, sql))
    names = ("load_owner", "load_contract", "load_reconstruction_inputs",
             "load_need_routing", "load_requirement_quantities", "load_success_criteria",
             "load_measurement_methods", "load_test_hypotheses", "load_test_variables",
             "load_interface_dependencies", "load_result_events")
    for name in names:
        real = getattr(store, name)

        def spy(*a, _real=real, _name=name, **kw):
            calls.append((_name, store._conn.in_transaction))
            return _real(*a, **kw)
        monkeypatch.setattr(store, name, spy)
    dx.compose_disclosure_projection(store, sid, aid)
    assert sql[0] == "SAVEPOINT need_routing_read_snapshot"
    assert sql[-1] == "RELEASE SAVEPOINT need_routing_read_snapshot"
    assert sum(1 for s in sql if s.startswith("SAVEPOINT")) == 1
    assert not any(s.split()[0].upper() in ("INSERT", "UPDATE", "DELETE", "BEGIN", "COMMIT")
                   for s in sql)
    assert all(inside for _n, inside in calls)
    order = [n for n, _i in calls]
    assert order[0] == "load_owner"
    tail = [n for n in order if n in names[4:]]
    assert tail == list(names[4:])


def test_06b_06c_concurrent_commit_never_mixes_state_and_a_later_export_sees_it(owned, monkeypatch):
    c, aid, sid, store = owned
    eid = _live_ids(sid)[0]
    store.apply_planning_metadata_delta(sid, {eid: "before"}, {})
    expected = dx.compose_disclosure_projection(store, sid, aid)
    outcome = {}
    real = store.load_success_criteria

    def racing(project_id):
        other = sqlite3.connect(_db(), timeout=0.05, isolation_level=None)
        try:
            other.execute("BEGIN IMMEDIATE")
            other.execute("UPDATE prototype_plan_metadata SET success_criterion = ? "
                          "WHERE project_id = ? AND experiment_id = ?", ("after", sid, eid))
            try:
                other.execute("COMMIT")
                outcome["committed"] = True
            except sqlite3.OperationalError:
                other.execute("ROLLBACK")
                outcome["committed"] = False
        finally:
            other.close()
        return real(project_id)

    monkeypatch.setattr(store, "load_success_criteria", racing)
    during = dx.compose_disclosure_projection(store, sid, aid)
    assert during == expected
    monkeypatch.setattr(store, "load_success_criteria", real)
    if not outcome["committed"]:
        other = sqlite3.connect(_db())
        other.execute("UPDATE prototype_plan_metadata SET success_criterion = ? "
                      "WHERE project_id = ? AND experiment_id = ?", ("after", sid, eid))
        other.commit()
        other.close()
    later = dx.compose_disclosure_projection(store, sid, aid)
    values = [i["slots"]["success_criterion"]["value"] for i in _items(later, "experiments")]
    assert "after" in values and later != expected


def test_06d_acquisition_and_integrity_failures_refuse(owned, monkeypatch):
    c, aid, sid, store = owned
    store._connection_unsafe = True
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_disclosure_projection(store, sid, aid)
    store._connection_unsafe = False
    store._conn.execute("BEGIN")                       # caller-owned / no-op branch
    try:
        with pytest.raises(dx.DisclosureExportRefused):
            dx.compose_disclosure_projection(store, sid, aid)
    finally:
        store._conn.execute("ROLLBACK")
    real = store.load_requirement_quantities

    def lose(project_id):
        out = real(project_id)
        store._conn.execute("ROLLBACK")                # snapshot lost before the R1 reads
        return out
    monkeypatch.setattr(store, "load_requirement_quantities", lose)
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_disclosure_projection(store, sid, aid)
    monkeypatch.setattr(store, "load_requirement_quantities", real)
    real_events = store.load_result_events

    def lose_last(project_id):
        out = real_events(project_id)
        store._conn.execute("ROLLBACK")                # lost after the last read
        return out
    monkeypatch.setattr(store, "load_result_events", lose_last)
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_disclosure_projection(store, sid, aid)
    assert store.committed_state_readable()


def test_06d_release_failure_refuses_at_step_6(owned, monkeypatch):
    c, aid, sid, store = owned
    real_events = store.load_result_events

    def unresolve(project_id):
        out = real_events(project_id)
        store._conn.execute("ROLLBACK")
        store._conn.execute("BEGIN")                   # RELEASE fails and leaves it open
        return out
    monkeypatch.setattr(store, "load_result_events", unresolve)
    try:
        with pytest.raises(dx.DisclosureExportRefused):
            dx.compose_disclosure_projection(store, sid, aid)
        assert store._connection_unsafe is True
    finally:
        store._conn.execute("ROLLBACK")
        store._connection_unsafe = False


def test_10_no_mutation(owned):
    c, aid, sid, store = owned
    before = _store_dump()
    dx.compose_disclosure_projection(store, sid, aid)
    assert _store_dump() == before


def test_17_no_store_read_after_the_snapshot_exits(owned, monkeypatch):
    c, aid, sid, store = owned
    sql = []
    monkeypatch.setattr(store, "_conn", _SqlLog(store._conn, sql))
    after_exit = []
    for name in [n for n in dir(store) if not n.startswith("_")
                 and callable(getattr(store, n))]:
        real = getattr(store, name)

        def spy(*a, _real=real, _name=name, **kw):
            if sql and sql[-1].startswith("RELEASE"):
                after_exit.append(_name)
            return _real(*a, **kw)
        monkeypatch.setattr(store, name, spy)
    content = dx.compose_disclosure_projection(store, sid, aid)
    assert set(after_exit) <= {"committed_state_readable"}
    assert sql[-1].startswith("RELEASE")
    n = len(sql)
    dx.serialize_json(dx.export_document(content, dx.generated_at_now(),
                                         dx.JSON_FORMAT_VERSION))
    assert len(sql) == n


_INJECT = ("load_contract", "load_need_routing", "load_requirement_quantities",
           "load_success_criteria", "load_measurement_methods", "load_test_hypotheses",
           "load_test_variables", "load_interface_dependencies", "load_result_events")
_ERRORS = (sqlite3.OperationalError("no such table: x"),
           sqlite3.OperationalError("no such column: y"),
           sqlite3.DatabaseError("database disk image is malformed"),
           sqlite3.IntegrityError("constraint failed"),
           sqlite3.Error("unclassified"),
           RuntimeError("unclassified exception"))


@pytest.mark.parametrize("method", _INJECT)
def test_23_24a_every_source_failure_refuses_never_unavailable(owned, monkeypatch, method):
    c, aid, sid, store = owned
    for error in _ERRORS:
        def boom(*a, _e=error, **kw):
            raise _e
        monkeypatch.setattr(store, method, boom)
        with pytest.raises(dx.DisclosureExportRefused):
            dx.compose_disclosure_projection(store, sid, aid)
        monkeypatch.undo()
        assert store.committed_state_readable()


def test_23_project_not_found_and_none_collection_refuse(owned, monkeypatch):
    from engine.record_store import ProjectNotFound
    c, aid, sid, store = owned
    for method in ("load_test_hypotheses", "load_result_events",
                   "load_interface_dependencies", "load_requirement_quantities"):
        def gone(*a, **kw):
            raise ProjectNotFound(sid)
        monkeypatch.setattr(store, method, gone)
        with pytest.raises(dx.DisclosureExportRefused):
            dx.compose_disclosure_projection(store, sid, aid)
        monkeypatch.undo()


def test_23_level_zero_refuses(owned, monkeypatch):
    c, aid, sid, store = owned
    real = store.load_reconstruction_inputs
    monkeypatch.setattr(store, "load_reconstruction_inputs",
                        lambda pid: dict(real(pid), path="not-a-path"))
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_disclosure_projection(store, sid, aid)


def test_26_s1_denial_versus_refusal(owned, monkeypatch):
    c, aid, sid, store = owned
    with pytest.raises(ProjectAccessDenied):
        dx.compose_disclosure_projection(store, "no-such-project", aid)
    other, other_aid = _client_for("s35-other@example.com")
    with pytest.raises(ProjectAccessDenied):
        dx.compose_disclosure_projection(store, sid, other_aid)
    from tests.csrf_client import csrf_client
    with csrf_client(webapp.app) as anon:
        r = anon.post("/start", data={"idea": "A sensor circuit that cuts power when hot.",
                                      "domain_confirm": "electronics_electrical"})
        null_owner = r.headers["Location"].rsplit("/", 1)[-1]
    assert store.load_owner(null_owner) == (True, None)
    with pytest.raises(ProjectAccessDenied):
        dx.compose_disclosure_projection(store, null_owner, aid)

    def lookup_fails(pid):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(store, "load_owner", lookup_fails)
    with pytest.raises(ProjectAccessDenied):
        dx.compose_disclosure_projection(store, sid, aid)
    monkeypatch.undo()

    def contract_fails(pid):
        raise sqlite3.DatabaseError("database disk image is malformed")
    monkeypatch.setattr(store, "load_contract", contract_fails)
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_disclosure_projection(store, sid, aid)


def test_05_projection_never_contains_another_project(owned):
    c, aid, sid, store = owned
    marker = "UNIQUE-OTHER-PROJECT-IDEA-TEXT circuit with a relay"
    r = c.post("/start", data={"idea": marker, "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302
    content = dx.compose_disclosure_projection(store, sid, aid)
    assert "UNIQUE-OTHER-PROJECT" not in _dump(content)
    assert sid not in _dump(content) and aid not in _dump(content)
