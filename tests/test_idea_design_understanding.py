# -*- coding: utf-8 -*-
"""IDEA-DESIGN-UNDERSTANDING-PROJECTION-01 — focused tests.

The composer (``engine/idea_design_understanding.py``) composes the existing
owners' outputs into one read-only picture. These tests prove: owner-native
axes are carried unchanged and never remapped; only identity-bound links the
owner records hold are emitted; one fact has one placement; ABSENT and
UNAVAILABLE stay distinct and section-local (whole-view refusal only without
a usable ledger); nothing is invented, chosen or written; the session page
renders the picture in EN and AR with no internal id as visible text; the
existing panels, Compass and gates are unchanged. Synthetic data only.
"""
import html
import pickle
import re

import pytest

import web.app as webapp
from engine import idea_design_understanding as du
from engine import idea_state as ideastate
from engine import need_routing
from engine import subsystem_model as sm
from engine.functional_need_handoff import Quote
from engine.idea_state import (
    AcknowledgedUnknown, AssertionRecord, Gap, IdeaState, LEGACY_UNSPECIFIED,
    OPEN, OWNER_STATED, PARTIAL, UNVALIDATED)
from tests.test_cap12_form_mockup_advisory import _client_for, _page
from tests.test_cap13_therm01_integrated_part_eligibility import (
    ELEC, MECH, _corrupt, _integrated)
from tests.test_functional_need_handoff import _start
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    BA_1, BA_2, MECH as MECH_ANSWER, PF_STRONG, SEED, _answer, _live,
    _start as _start_mech, client)
from tests.test_stage15_subsystem_interface_declaration import _restart
from web import ui_text

SCREEN_EN = "I want a stand that holds my monitor above my desk."
SCREEN_AR = ("أريد حاملًا خشبيًا يرفع شاشة الحاسوب فوق مكتبي حتى تكون "
             "في مستوى النظر بدون براغي")
WATER_UNKNOWN = ("I want a device that waters my plants automatically, but I "
                 "don't know how it would notice that the soil is dry.")
INVENTED = ("sensor", "pump", "controller", "valve", "battery", "motor",
            "microcontroller")


# ==========================================================================
# helpers
# ==========================================================================
def _du_section(body):
    start = body.find("data-design-understanding")
    if start == -1:
        return None
    return body[start:body.index("</details>", start)]


def _statuses(section):
    return dict(re.findall(
        r'data-du-section="([a-z_]+)" data-du-status="([A-Z]+)"', section))


def _items(section, kind):
    return re.findall(r'data-du-item="%s" data-du-ref="([^"]*)"' % kind, section)


def _visible(section):
    return html.unescape(re.sub(r"<[^>]+>", " ", section))


def _record(rid, disposition, content, gap="MECHANISM_COMPLETENESS",
            provenance=OWNER_STATED, target=None, superseded_by=None):
    return AssertionRecord(record_id=rid, disposition=disposition, content=content,
                           gap_context=gap, iteration=1, provenance=provenance,
                           validation_status=UNVALIDATED, question_target=target,
                           superseded_by=superseded_by)


def _state(records=(), unknowns=(), gaps=(), domain="mechanical"):
    state = IdeaState(idea_id="du-test")
    state.domain = domain
    state.domain_signal = domain
    state.assertions = list(records)
    state.acknowledged_unknowns = list(unknowns)
    state.gaps = list(gaps)
    return state


def _part(sid, domain, name):
    return sm.Subsystem(subsystem_id=sid, domain=domain, display_name=name,
                        function_text="what it does", provenance=OWNER_STATED,
                        validation_state=UNVALIDATED)


def _composition(with_component=True, with_interface=True, prepared=False,
                 dependency=False, participation=False):
    a, b = _part("sub-a", MECH, "Frame"), _part("sub-b", ELEC, "Driver board")
    components = ((sm.ProjectComponent(
        component_id="cmp-1", display_name="Wheel", function_text="Rolls",
        subsystem_ids=("sub-a",), provenance=OWNER_STATED,
        validation_state=UNVALIDATED),) if with_component else ())
    interfaces = ((sm.SubsystemInterface(
        interface_id="ifc-1", subsystem_a_id="sub-a", subsystem_b_id="sub-b",
        description="The board powers the frame", provenance=OWNER_STATED,
        validation_state=UNVALIDATED),) if with_interface else ())
    preparations = ((sm.InterfacePreparation(
        interface_id="ifc-1", operating_conditions="indoors"),) if prepared else ())
    dependencies = ((sm.InterfaceDependency(
        interface_id="ifc-1", kind=sm.DEPENDENCY_ONE_WAY,
        dependent_subsystem_id="sub-a", depends_on_subsystem_id="sub-b"),)
        if dependency else ())
    participations = ((sm.InterfaceParticipation(
        interface_id="ifc-1", component_id="cmp-1", provenance=OWNER_STATED,
        validation_state=UNVALIDATED),) if participation else ())
    return {"subsystems": (a, b), "focus": ELEC, "interfaces": interfaces,
            "preparations": preparations, "dependencies": dependencies,
            "components": components, "withdrawn_components": (),
            "part_answers": (), "participations": participations}


def _handoff(status="PROPOSED", action="cap13_support_reactions", abstained=0):
    return {"available": True, "idea_available": True, "abstained": abstained,
            "roles": [{"role": "SCREEN_SUPPORT", "object": "SCREEN", "status": status,
                       "groundings": (Quote("IDEA", "idea", 0, 20, SCREEN_EN[:20]),),
                       "negations": (), "uncertain": (),
                       "capabilities": [{"ref": "CAP13_CONDITIONAL_REACTIONS",
                                         "state": "CONDITIONAL", "count": None,
                                         "action": action}]}]}


def _compose(**over):
    base = dict(state=_state(), derived_available=True, original_idea=SCREEN_EN,
                functional_handoff=_handoff(), idea_stated_unknown=None,
                composition=_composition(), prototype_needs={})
    base.update(over)
    return du.compose(du.Sources(**base))


def _all_items(picture):
    return [item for section in picture.sections for item in section.items]


# ==========================================================================
# 1. the composer: axes, links, placement, absence, unavailability
# ==========================================================================
def test_sections_are_fixed_and_in_order():
    picture = _compose()
    assert picture.available
    assert tuple(s.key for s in picture.sections) == du.SECTION_KEYS


def test_owner_native_axes_are_carried_under_their_own_names_only():
    records = [
        _record("rec_1", "answered", "The arm pivots on a pin.", target="Q-1"),
        _record("rec_2", "unknown", "I do not know the load yet."),
        _record("rec_3", "provisional_assumption", "Assume steel.", provenance=LEGACY_UNSPECIFIED),
    ]
    picture = _compose(state=_state(records, gaps=[Gap("MECHANISM_COMPLETENESS", OPEN, 0)]))
    answer = next(i for i in _all_items(picture) if i.reference == "rec_1")
    assert answer.content_kind == du.KIND_ANSWER
    assert dict(answer.attributes) == {
        "provenance": OWNER_STATED, "validation_status": UNVALIDATED,
        "disposition": "answered", "gap_context": "MECHANISM_COMPLETENESS",
        "question_target": "Q-1", "iteration": 1}
    assumption = next(i for i in _all_items(picture) if i.reference == "rec_3")
    assert assumption.content_kind == du.KIND_PROVISIONAL_ASSUMPTION
    assert assumption.attribute("provenance") == LEGACY_UNSPECIFIED
    # a requirement row keeps the landscape's OWN axes and no ledger axis
    rows = [i for i in _all_items(picture) if i.content_kind == du.KIND_REQUIREMENT]
    assert rows
    for row in rows:
        names = {name for name, _ in row.attributes}
        assert names <= {"source_status", "criticality", "criticality_authority"}
        assert row.attribute("criticality_authority") == "system-derived"
    # no item carries another owner's token under a ledger axis
    for item in _all_items(picture):
        assert item.attribute("provenance") not in ("system-derived", "undetermined", "UNDETERMINED")
        assert item.attribute("validation_status") != "UNDETERMINED"
        assert item.attribute("validation_state") != "UNDETERMINED"
        assert "SYSTEM_PROPOSED" not in [v for _, v in item.attributes if isinstance(v, str)]
    # the reading keeps the handoff owner's interpretation label and status
    role = next(i for i in _all_items(picture) if i.content_kind == du.KIND_FUNCTIONAL_ROLE)
    assert role.attribute("interpretation_status") == "PROVISIONAL_READING"
    assert role.attribute("status") == "PROPOSED"
    # a part / component keeps its own validation_state field name
    part = next(i for i in _all_items(picture) if i.content_kind == du.KIND_PART)
    assert ("validation_state", UNVALIDATED) in part.attributes
    assert part.attribute("validation_status") is None


def test_only_identity_bound_links_are_emitted():
    picture = _compose(composition=_composition(prepared=True, dependency=True,
                                                participation=True),
                       state=_state([_record("rec_1", "answered", "x", target="Q-1")],
                                    gaps=[Gap("MECHANISM_COMPLETENESS", OPEN, 0)]))
    by_kind = {}
    for item in _all_items(picture):
        by_kind.setdefault(item.content_kind, []).append(item)
        for link in item.links:
            assert link.kind in du.LINK_KINDS
    component = by_kind[du.KIND_COMPONENT][0]
    assert component.links == (du.Link("part", "sub-a"),)
    interaction = by_kind[du.KIND_INTERACTION][0]
    assert set(interaction.links) == {
        du.Link("part", "sub-a"), du.Link("part", "sub-b"),
        du.Link("dependent_part", "sub-a"), du.Link("depends_on_part", "sub-b"),
        du.Link("component", "cmp-1")}
    assert interaction.attribute("preparation_presence") == sm.PREPARATION_PARTLY_RECORDED
    assert interaction.attribute("dependency_kind") == sm.DEPENDENCY_ONE_WAY
    role = by_kind[du.KIND_FUNCTIONAL_ROLE][0]
    assert all(l.kind == "grounding_quote" for l in role.links) and role.links
    # a reading never links to a part, a component or a capability; a
    # continuation links to nothing; a part links to nothing
    assert not any(l.kind in ("part", "component") for l in role.links)
    assert by_kind[du.KIND_ENGINEERING_CONTINUATION][0].links == ()
    assert by_kind[du.KIND_PART][0].links == ()
    answer = by_kind[du.KIND_ANSWER][0]
    assert set(answer.links) == {du.Link("gap", "MECHANISM_COMPLETENESS"), du.Link("question", "Q-1")}
    requirement = by_kind[du.KIND_REQUIREMENT][0]
    assert len(requirement.links) == 1 and requirement.links[0].kind == "requirement_anchor"


def test_a_requirement_anchored_on_a_record_is_a_distinct_object_and_the_record_is_not_duplicated():
    records = [_record("rec_1", "unknown", "I do not know the load yet.", target="Q-2")]
    picture = _compose(state=_state(records, gaps=[Gap("MECHANISM_COMPLETENESS", OPEN, 0)]))
    placements = [(s.key, i) for s in picture.sections for i in s.items if i.reference == "rec_1"]
    assert len(placements) == 1 and placements[0][0] == du.SECTION_STATED_UNKNOWNS
    assert placements[0][1].content_kind == du.KIND_NON_ANSWER
    anchored = [i for i in picture.section(du.SECTION_UNRESOLVED_WORK).items
                if i.content_kind == du.KIND_REQUIREMENT
                and i.links[0].reference == "assertion:rec_1"]
    assert len(anchored) == 1 and anchored[0].reference != "rec_1"


def test_superseded_and_non_inventor_records_are_not_shown():
    records = [
        _record("rec_1", "answered", "old", superseded_by="rec_2"),
        _record("rec_2", "answered", "new"),
        _record("rec_3", "answered", "machine", provenance="SYSTEM_INFERRED"),
    ]
    picture = _compose(state=_state(records))
    refs = [i.reference for i in picture.section(du.SECTION_RECORDED_UNDERSTANDING).items]
    assert refs == ["rec_2"]


def test_absent_is_not_unavailable_and_each_is_section_local():
    picture = _compose(original_idea=None, functional_handoff=None,
                       composition=_composition(with_component=False, with_interface=False),
                       state=_state(gaps=[]))
    statuses = {s.key: s.status for s in picture.sections}
    assert statuses[du.SECTION_ORIGINAL_IDEA] == du.ABSENT
    assert statuses[du.SECTION_FUNCTIONAL_READINGS] == du.ABSENT
    assert statuses[du.SECTION_ENGINEERING_CONTINUATIONS] == du.ABSENT
    assert statuses[du.SECTION_PARTS] == du.PRESENT
    assert statuses[du.SECTION_COMPONENTS] == du.ABSENT
    assert statuses[du.SECTION_INTERACTIONS] == du.ABSENT
    assert statuses[du.SECTION_CONSTRAINTS] == du.ABSENT
    assert statuses[du.SECTION_STATED_UNKNOWNS] == du.ABSENT
    assert statuses[du.SECTION_RECORDED_UNDERSTANDING] == du.ABSENT
    # unreadable inputs: only their own sections read UNAVAILABLE
    picture = _compose(original_idea=du.UNREADABLE, functional_handoff={"available": False},
                       idea_stated_unknown=du.UNREADABLE)
    statuses = {s.key: s.status for s in picture.sections}
    assert statuses[du.SECTION_ORIGINAL_IDEA] == du.UNAVAILABLE
    assert statuses[du.SECTION_FUNCTIONAL_READINGS] == du.UNAVAILABLE
    assert statuses[du.SECTION_ENGINEERING_CONTINUATIONS] == du.UNAVAILABLE
    assert statuses[du.SECTION_PARTS] == du.PRESENT
    assert statuses[du.SECTION_UNRESOLVED_WORK] == du.PRESENT
    unknowns = picture.section(du.SECTION_STATED_UNKNOWNS)
    assert unknowns.status == du.ABSENT and unknowns.unavailable == ("idea_stated_unknown",)


def test_the_stage15_cluster_inherits_its_readers_all_or_nothing_boundary():
    picture = _compose(composition=du.UNREADABLE)
    statuses = {s.key: s.status for s in picture.sections}
    assert [statuses[k] for k in (du.SECTION_PARTS, du.SECTION_COMPONENTS,
                                  du.SECTION_INTERACTIONS)] == [du.UNAVAILABLE] * 3
    assert statuses[du.SECTION_ORIGINAL_IDEA] == du.PRESENT
    assert picture.names == ()
    # unreadable prototype notes leave the component list in place
    picture = _compose(prototype_needs=du.UNREADABLE)
    components = picture.section(du.SECTION_COMPONENTS)
    assert components.status == du.PRESENT and components.unavailable == ("prototype_needs",)
    assert components.items[0].attribute("prototype_need") is None
    picture = _compose(prototype_needs={"cmp-1": "four of these"})
    assert picture.section(du.SECTION_COMPONENTS).items[0].attribute("prototype_need") == "four of these"


def test_whole_view_refusal_only_without_a_usable_ledger():
    assert not du.compose(du.Sources(state=None)).available
    duplicated = _state([_record("rec_1", "answered", "a"), _record("rec_1", "answered", "b")])
    assert not _compose(state=duplicated).available
    assert _compose(state=_state(gaps=[])).available


def test_cold_unreconstructed_state_makes_only_the_derived_section_unavailable():
    picture = _compose(derived_available=False)
    statuses = {s.key: s.status for s in picture.sections}
    assert statuses[du.SECTION_UNRESOLVED_WORK] == du.UNAVAILABLE
    assert statuses[du.SECTION_ORIGINAL_IDEA] == du.PRESENT
    assert statuses[du.SECTION_PARTS] == du.PRESENT


def test_incomplete_and_conflicting_designs_are_shown_not_resolved():
    picture = _compose(functional_handoff=_handoff(status="CONFLICTING", action=None),
                       composition=_composition(with_component=True, with_interface=True),
                       state=_state(gaps=[Gap("MECHANISM_COMPLETENESS", PARTIAL, 0)]))
    role = picture.section(du.SECTION_FUNCTIONAL_READINGS).items[0]
    assert role.attribute("status") == "CONFLICTING"
    assert picture.section(du.SECTION_ENGINEERING_CONTINUATIONS).status == du.ABSENT
    interaction = picture.section(du.SECTION_INTERACTIONS).items[0]
    assert interaction.attribute("preparation_presence") == sm.PREPARATION_NONE_RECORDED
    gap = next(i for i in picture.section(du.SECTION_UNRESOLVED_WORK).items
               if i.content_kind == du.KIND_GAP)
    assert gap.attribute("status") == PARTIAL
    # a component with no part association is shown as such (no links); a
    # part with no component gets no invented component
    picture = _compose(composition=dict(_composition(), components=(sm.ProjectComponent(
        component_id="cmp-9", display_name="Loose part", function_text="?",
        subsystem_ids=(), provenance=OWNER_STATED, validation_state=UNVALIDATED),)))
    assert picture.section(du.SECTION_COMPONENTS).items[0].links == ()
    texts = " ".join((i.text or "") for i in _all_items(picture))
    assert not any(word in texts.lower() for word in INVENTED)


def test_the_composer_mutates_nothing():
    state = _state([_record("rec_1", "answered", "x")], gaps=[Gap("MECHANISM_COMPLETENESS", OPEN, 0)])
    before = pickle.dumps(state)
    composition = _composition()
    _compose(state=state, composition=composition)
    assert pickle.dumps(state) == before
    assert composition == _composition()


def test_constraints_keep_their_owner_fields_and_withdrawn_ones_are_not_current():
    def decl(rid, text, strength, supersedes=()):
        return AssertionRecord(
            record_id=rid, disposition=ideastate.DISPOSITION_CONSTRAINT_DECLARED,
            content=text, gap_context=None, iteration=0, provenance=OWNER_STATED,
            validation_status=UNVALIDATED, supersedes=list(supersedes),
            constraint_strength=strength)
    records = [decl("rec_1", "Must fit a car boot", "mandatory_constraint"),
               decl("rec_2", "Prefer wood", "preference")]
    records[0].superseded_by = None
    state = _state(records)
    picture = _compose(state=state)
    items = picture.section(du.SECTION_CONSTRAINTS).items
    assert [i.text for i in items] == ["Must fit a car boot", "Prefer wood"]
    assert items[0].attribute("strength") == "mandatory_constraint"
    assert ("provenance", OWNER_STATED) in items[0].attributes
    assert items[0].links == (du.Link("record", "rec_1"),)
    # an unreadable history is UNAVAILABLE, never "none"
    broken = _state([AssertionRecord(record_id="rec_7", disposition="answered",
                                     content="x", gap_context="MECHANISM_COMPLETENESS",
                                     iteration=0, constraint_strength="preference")])
    assert _compose(state=broken).section(du.SECTION_CONSTRAINTS).status == du.UNAVAILABLE


def test_routed_needs_and_declared_contradictions_come_from_their_owners(monkeypatch):
    monkeypatch.setattr(need_routing, "outstanding_needs",
                        lambda state: (("PHYSICAL_FEASIBILITY", "PF-Q2", "SPECIALIST", None),))
    records = [_record("rec_1", "answered", "a"), _record("rec_2", "answered", "b")]
    state = _state(records)
    monkeypatch.setattr(ideastate, "active_declared_contradiction_pairs",
                        lambda assertions: (("rec_1", "rec_2"),))
    picture = _compose(state=state)
    items = picture.section(du.SECTION_UNRESOLVED_WORK).items
    routed = next(i for i in items if i.content_kind == du.KIND_ROUTED_NEED)
    assert routed.reference == "PHYSICAL_FEASIBILITY:PF-Q2"
    assert routed.attribute("required_input") == "SPECIALIST"
    assert set(routed.links) == {du.Link("gap", "PHYSICAL_FEASIBILITY"), du.Link("question", "PF-Q2")}
    pair = next(i for i in items if i.content_kind == du.KIND_DECLARED_CONTRADICTION)
    assert pair.links == (du.Link("record", "rec_1"), du.Link("record", "rec_2"))


def test_module_imports_only_engine_owners():
    with open("engine/idea_design_understanding.py", encoding="utf-8") as handle:
        source = handle.read()
    for forbidden in ("from web", "import web", "record_store", "flask", "sqlite3",
                      "msnl_shadow", "ai_advisor", "openai", "requests"):
        assert forbidden not in source, forbidden
    assert "SYSTEM_PROPOSED" not in source


# ==========================================================================
# 2. the session page
# ==========================================================================
def test_screen_journey_renders_the_picture_with_owner_attributes_and_no_internal_ids():
    c, _aid = _client_for("du-screen@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    body = _page(c, sid)
    section = _du_section(body)
    assert section
    statuses = _statuses(section)
    assert statuses["original_idea"] == "PRESENT"
    assert statuses["functional_readings"] == "PRESENT"
    assert statuses["engineering_continuations"] == "PRESENT"
    assert statuses["unresolved_work"] == "PRESENT"
    assert statuses["parts"] == "ABSENT" and statuses["components"] == "ABSENT"
    assert statuses["interactions"] == "ABSENT" and statuses["constraints"] == "ABSENT"
    assert statuses["recorded_understanding"] == "ABSENT"
    visible = _visible(section)
    assert SCREEN_EN in visible
    assert ui_text.text("UI_DU_VAL_PROPOSED", "en") in visible
    assert ui_text.text("UI_DU_VAL_PROVISIONAL_READING", "en") in visible
    assert ui_text.text("UI_DU_BOUNDARY", "en") in visible
    assert ui_text.text("UI_DU_ADJACENCY", "en") in visible
    assert ('href="/session/%s/support-reactions"' % sid) in section
    assert "?" not in re.search(r'data-du-action="[^"]*" href="([^"]*)"', section).group(1)
    # the picture is a composition of what exists: the existing panels stay
    assert "data-functional-handoff" in body and "data-fh-action=" in body
    # internal ids never appear as visible text
    for ref in re.findall(r'data-du-ref="([^"]*)"', section):
        if ref.startswith(("sub-", "cmp-", "ifc-", "rec_")):
            assert ref not in visible
    assert not any(word in visible.lower() for word in INVENTED)


def test_the_page_passes_the_handoff_view_once_and_the_compass_is_unchanged(monkeypatch):
    c, _aid = _client_for("du-once@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    calls = []
    real = webapp._functional_handoff_view

    def counting(*args):
        calls.append(args)
        return real(*args)
    monkeypatch.setattr(webapp, "_functional_handoff_view", counting)
    state = webapp.SESSION_STORE[sid]["state"]
    compass_before = webapp._project_compass_context(state)
    before = pickle.dumps(state)
    body = _page(c, sid)
    assert len(calls) == 1
    assert pickle.dumps(state) == before
    assert webapp._project_compass_context(state) == compass_before
    assert 'data-project-compass' in body or 'project-compass' in body


def test_watering_idea_shows_the_stated_unknown_without_inventing_a_design(client):
    c, _aid = _client_for("du-water@example.com")
    sid = _start(c, WATER_UNKNOWN, ELEC)
    section = _du_section(_page(c, sid))
    statuses = _statuses(section)
    assert statuses["stated_unknowns"] == "PRESENT"
    assert _items(section, "idea_stated_unknown") == ["seed_idea_text"]
    assert statuses["functional_readings"] == "PRESENT"
    assert 'data-du-item="functional_role" data-du-ref="WATERING:' in section
    assert statuses["components"] == "ABSENT" and statuses["interactions"] == "ABSENT"
    assert statuses["engineering_continuations"] == "ABSENT"
    visible = _visible(section).lower()
    # the inventor's own words appear; nothing is added to them
    assert "soil is dry" in visible
    for word in ("sensor", "pump", "controller", "valve", "battery", "timer"):
        assert word not in visible


def test_answers_and_non_answers_each_appear_once_with_their_own_axes(client):
    sid = _start_mech(client, seed=SEED)
    _answer(client, sid, MECH_ANSWER)
    raw = client.get("/session/%s" % sid).get_data(as_text=True)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    r = client.post("/session/%s" % sid, data={"action": "unknown", "answer_token": token,
                                               "response": "I do not know the latch load yet."})
    assert r.status_code == 302
    section = _du_section(client.get("/session/%s" % sid).get_data(as_text=True))
    statuses = _statuses(section)
    assert statuses["recorded_understanding"] == "PRESENT"
    assert statuses["stated_unknowns"] == "PRESENT"
    visible = _visible(section)
    assert MECH_ANSWER in visible
    assert "I do not know the latch load yet." in visible
    # the record is placed ONCE (stated unknowns); the only other wording is
    # the Requirement Landscape's own derived row, a distinct object with its
    # own identity that links back to the record
    unknowns = section[section.index('data-du-section="stated_unknowns"'):
                       section.index('data-du-section="constraints"')]
    assert _visible(unknowns).count("I do not know the latch load yet.") == 1
    others = [m.group(1) for m in re.finditer(
        r'<li data-du-item="([a-z_]+)" data-du-ref="[^"]*"[^>]*>(.*?)</li>', section, re.S)
        if "latch load" in m.group(2)]
    assert sorted(others) == ["non_answer", "requirement"]
    assert 'data-du-link="requirement_anchor" data-du-link-ref="assertion:rec_' in section
    assert ui_text.text("UI_DU_VAL_OWNER_STATED", "en") in visible
    assert ui_text.text("UI_DU_VAL_UNVALIDATED", "en") in visible
    assert ui_text.text("UI_DU_VAL_UNKNOWN", "en") in visible
    answers = _items(section, "answer")
    assert len(answers) == 1 and len(_items(section, "non_answer")) == 1
    # each ledger record is referenced by exactly one item
    refs = re.findall(r'data-du-item="[a-z_]+" data-du-ref="(rec_\d+)"', section)
    assert len(refs) == len(set(refs))


def test_integrated_project_shows_the_declared_parts_by_name_and_the_cluster_fails_closed_whole():
    c, _aid = _client_for("du-integrated@example.com")
    sid = _integrated(c, ELEC, idea=SCREEN_EN)
    section = _du_section(_page(c, sid))
    statuses = _statuses(section)
    assert statuses["parts"] == "PRESENT"
    parts = _items(section, "part")
    assert len(parts) == 2 and all(p.startswith("sub-") for p in parts)
    visible = _visible(section)
    subs = webapp._get_store().load_project_subsystems(sid)
    for sub in subs:
        assert sub.display_name in visible and sub.subsystem_id not in visible
    assert ui_text.text("UI_DU_ATTR_INITIAL_ANALYSIS_FOCUS", "en") in visible
    assert statuses["components"] == "ABSENT" and statuses["interactions"] == "ABSENT"
    _corrupt("UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0")
    body = c.get("/session/%s" % sid).get_data(as_text=True)
    section = _du_section(body)
    if section is not None:
        statuses = _statuses(section)
        assert [statuses[k] for k in ("parts", "components", "interactions")] == ["UNAVAILABLE"] * 3
        assert statuses["original_idea"] == "PRESENT"


def test_an_unreadable_composite_reader_makes_only_the_cluster_unavailable(monkeypatch):
    c, _aid = _client_for("du-unreadable@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    store = webapp._get_store()

    def broken(project_id):
        raise OSError("disk I/O error")
    monkeypatch.setattr(store, "load_parts_components_interactions", broken)
    section = _du_section(_page(c, sid))
    statuses = _statuses(section)
    assert [statuses[k] for k in ("parts", "components", "interactions")] == ["UNAVAILABLE"] * 3
    assert statuses["original_idea"] == "PRESENT"
    assert statuses["functional_readings"] == "PRESENT"
    assert ui_text.text("UI_DU_SECTION_UNAVAILABLE", "en") in _visible(section)


def test_a_broken_composition_is_the_whole_view_refusal_never_a_partial_picture(monkeypatch):
    c, _aid = _client_for("du-refusal@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    monkeypatch.setattr(webapp._du, "compose", lambda sources: (_ for _ in ()).throw(RuntimeError("x")))
    section = _du_section(_page(c, sid))
    assert "data-du-unavailable" in section
    assert 'data-du-section=' not in section


def test_cold_reload_keeps_the_recorded_sections_and_marks_derived_truth_unavailable(client):
    sid = _start_mech(client, seed=SEED + " " + SCREEN_EN)
    _answer(client, sid, MECH_ANSWER)
    _restart()
    body = client.get("/session/%s" % sid).get_data(as_text=True)
    section = _du_section(body)
    assert section
    statuses = _statuses(section)
    assert statuses["original_idea"] == "PRESENT"
    assert statuses["recorded_understanding"] == "PRESENT"
    assert statuses["unresolved_work"] == "UNAVAILABLE"
    assert MECH_ANSWER in _visible(section)


def test_a_get_writes_nothing():
    c, _aid = _client_for("du-readonly@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    store = webapp._get_store()
    before = store.load_contract(sid)
    _page(c, sid)
    _page(c, sid)
    assert store.load_contract(sid) == before


def test_every_du_copy_key_has_distinct_en_and_ar():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_DU_")]
    assert len(keys) >= 70
    for key in keys:
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en and ar and en != key and ar != en, key


def test_arabic_page_renders_the_picture_rtl():
    c, _aid = _client_for("du-ar@example.com")
    sid = _start(c, SCREEN_AR, MECH)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = _page(c, sid)
    assert 'dir="rtl"' in body
    section = _du_section(body)
    visible = _visible(section)
    assert ui_text.text("UI_DU_TITLE", "ar") in visible
    assert ui_text.text("UI_DU_SEC_ORIGINAL_IDEA", "ar") in visible
    assert ui_text.text("UI_DU_BOUNDARY", "ar") in visible
    assert "بدون براغي" in visible
    assert ui_text.text("UI_DU_VAL_PROVISIONAL_READING", "ar") in visible
