"""CAP-08 Slice 1 (Stage 20) — inventor-declared assumption -> answer dependency.

Proves, over the real engine, the real durable store and the real web routes:

* one `assumption_dependency_declared` record per DIRECTED edge on the EXISTING
  ledger (OWNER_STATED, OWNER_INPUT, UNVALIDATED, empty content, neutral
  fields, a typed {assumption_record_id, dependent_answer_record_id} edge) is
  the ONLY durable authority; the dependency view is a pure derived projection;
* endpoint roles: an ACTIVE `provisional_assumption` -> an ACTIVE `answered`
  record, never pair-normalized, never any other disposition;
* chronological validation over durable order through the ONE shared
  relationship walk: declaration-then-correction is valid (only that edge goes
  inactive, nothing transfers), correction-then-declaration is refused — at
  load AND inside the append transaction;
* a multi-answer submission is one all-or-nothing batch (no partial success,
  no silently dropped duplicate), with exact-retry idempotency, fail-closed
  conflicts and committed-state-only confirmation;
* a dedicated CAP-08 binding (not a CAP-10 binding, not a generic answer
  token) with freshness;
* the four activated consumers read the same projection; the landscape,
  validation plan, readiness, next step, progression, serving
  (MULTIPLE_ALTERNATIVES) and NeedRouting are unchanged; EN / AR copy is
  truthful; the primitive is domain-neutral.

Neutral synthetic fixtures only; no study corpus.
"""
import copy
import html as _html
import inspect
import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.progression_loop as pl
import engine.session_reconstruction as SR
from engine.controlled_unknown_progression import report_controlled_unknowns
from engine.decision_composition import declare_decision_context, declare_alternative
from engine.derived_readiness import derive_readiness
from engine.idea_development_outputs import derive_next_development_step
from engine import idea_state as IS
from engine.idea_state import (
    IdeaState, Gap, OPEN, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
    BOUNDARY_AMBIGUITY, DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED,
    DISPOSITION_CONTRADICTION_DECLARED, RELATIONSHIP_METADATA_DISPOSITIONS,
    OWNER_STATED, OWNER_INPUT, UNVALIDATED, LEGACY_UNSPECIFIED,
    SPECIALIST_REVIEWED, project_assumption_dependencies,
)
from engine.record_contract import (
    ContractError, InvalidProvenanceError, InvalidReferenceError,
    InvalidValidationStatusError, ProjectRecordContract, assertion_to_dict,
)
from engine.record_store import AssumptionDependencyDeclarationRejected, StoreError
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from web import ui_text
import web.app as appmod
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, PF_STRONG, BA_1, BA_2, ELEC_SEED, _start, _answer, _live,
    _store, _body, _facts,
)

DEP = DISPOSITION_ASSUMPTION_DEPENDENCY_DECLARED
ASSUMPTION = "Assume the hinge pin carries the full deck load."
FORBIDDEN_EN = ("supports", "proves", "evidence for", " valid ", "invalid",
                "is wrong", "unsafe", "confirmed", "rejected", "resolved",
                "What is at risk")


# ---------------------------------------------------------------------------
# engine helpers
# ---------------------------------------------------------------------------

def _ledger(area_a=PHYSICAL_FEASIBILITY, area_b=BOUNDARY_AMBIGUITY,
            area_c=MECHANISM_COMPLETENESS):
    s = IdeaState(idea_id="cap08")
    s.record_interaction("answered", "A: steel frame", gap_context=area_a)      # rec_1
    s.record_interaction("provisional_assumption", ASSUMPTION,
                         gap_context=area_a)                                   # rec_2
    s.record_interaction("answered", "B: no tools", gap_context=area_b)         # rec_3
    s.record_interaction("answered", "C: spring pin", gap_context=area_c)       # rec_4
    s.record_interaction("unknown", "", gap_context=area_b)                     # rec_5
    return s


def _envelope(records):
    return {"contract_version": "p4-0-record-contract-v1", "idea_id": "cap08",
            "assertions": records}


def _payloads(state):
    return [assertion_to_dict(r) for r in state.assertions]


def _load(records):
    return ProjectRecordContract.from_dict(_envelope(records))


def _dep_payload(assumption, answer, record_id="rec_9", **over):
    d = {"record_id": record_id, "disposition": DEP, "content": "", "gap_context": None,
         "iteration": 0, "provenance": OWNER_STATED, "validation_status": UNVALIDATED,
         "quality": None, "pending": None, "responsibility": OWNER_INPUT,
         "resolves_gap": False, "contradicts": [], "supersedes": [],
         "superseded_by": None, "decision_context_root": None,
         "question_target": None,
         "dependency_edge": {"assumption_record_id": assumption,
                             "dependent_answer_record_id": answer}}
    d.update(over)
    return d


def _correct(state, target, text="corrected"):
    old = next(r for r in state.assertions if r.record_id == target)
    return state.record_interaction(old.disposition, text, gap_context=old.gap_context,
                                    supersedes=[target])


def _active(state):
    return set(project_assumption_dependencies(state.assertions).active_edges)


# ===========================================================================
# record shape, carrier, direction
# ===========================================================================

def test_valid_directed_edge_is_owner_stated_unvalidated_and_neutral():
    s = _ledger()
    [d] = s.record_assumption_dependency_declarations("rec_2", ["rec_3"])
    assert d.dependency_edge == {"assumption_record_id": "rec_2",
                                 "dependent_answer_record_id": "rec_3"}
    assert (d.disposition, d.provenance, d.responsibility, d.validation_status) \
        == (DEP, OWNER_STATED, OWNER_INPUT, UNVALIDATED)
    assert (d.content, d.gap_context, d.question_target, d.decision_context_root,
            d.quality, d.pending, d.resolves_gap, d.contradicts, d.supersedes,
            d.superseded_by, d.contradiction_endpoints) \
        == ("", None, None, None, None, None, False, [], [], None, None)
    # the payload duplicates no endpoint identity or text
    payload = assertion_to_dict(d)
    assert set(payload["dependency_edge"]) == {"assumption_record_id",
                                               "dependent_answer_record_id"}
    assert ASSUMPTION not in json.dumps(payload) and "no tools" not in json.dumps(payload)
    # record_interaction can never mint it; it is relationship metadata
    with pytest.raises(ValueError):
        _ledger().record_interaction(DEP, "x")
    assert DEP in RELATIONSHIP_METADATA_DISPOSITIONS
    assert DEP not in IS.INTERACTION_DISPOSITIONS


def test_role_direction_is_preserved_and_never_pair_normalized():
    s = _ledger()
    s.record_assumption_dependency_declarations("rec_2", ["rec_1"])
    assert _active(s) == {("rec_2", "rec_1")}           # lower id is the DEPENDENT
    before = copy.deepcopy(s.assertions)
    with pytest.raises(ValueError):                      # reversed roles
        s.record_assumption_dependency_declarations("rec_1", ["rec_2"])
    assert s.assertions == before
    # a stored edge with its roles swapped is refused on load
    with pytest.raises(InvalidReferenceError):
        _load(_payloads(_ledger()) + [_dep_payload("rec_3", "rec_2", "rec_6")])


@pytest.mark.parametrize("assumption,answers", [
    ("rec_2", []),                        # no dependent answer
    ("rec_2", ["rec_77"]),                # unknown answer
    ("rec_77", ["rec_3"]),                # unknown assumption
    ("rec_2", ["rec_5"]),                 # an `unknown` record is not an answer
    ("rec_2", ["rec_2"]),                 # assumption as its own dependent
    ("rec_1", ["rec_3"]),                 # an answer as the assumption
    ("rec_5", ["rec_3"]),                 # an `unknown` record as the assumption
    ("rec_2", ["rec_3", "rec_77"]),       # one bad edge rejects the WHOLE batch
    ("rec_2", ["rec_3", "rec_01"]), ("rec_2", ["3"]), ("rec_2", [None]),
    ("rec_0", ["rec_3"]), (None, ["rec_3"]),
])
def test_carrier_refuses_the_whole_batch_and_appends_nothing(assumption, answers):
    s = _ledger()
    before = copy.deepcopy(s.assertions)
    with pytest.raises(ValueError):
        s.record_assumption_dependency_declarations(assumption, answers)
    assert s.assertions == before


def test_other_relationship_or_decision_records_are_never_endpoints():
    s = _ledger()
    s.record_contradiction_declaration("rec_1", "rec_3")                   # rec_6
    [dep] = s.record_assumption_dependency_declarations("rec_2", ["rec_4"])  # rec_7
    before = copy.deepcopy(s.assertions)
    for assumption, answers in (("rec_2", ["rec_6"]), ("rec_6", ["rec_1"]),
                                ("rec_2", [dep.record_id]), (dep.record_id, ["rec_1"])):
        with pytest.raises(ValueError):
            s.record_assumption_dependency_declarations(assumption, answers)
    assert s.assertions == before


def test_multi_answer_batch_is_one_record_per_edge_in_deterministic_order():
    s = _ledger()
    for _ in range(6):
        s.record_interaction("answered", "x", gap_context=PHYSICAL_FEASIBILITY)
    minted = s.record_assumption_dependency_declarations(
        "rec_2", ["rec_11", "rec_3", "rec_9", "rec_3"])          # dupes + lexical traps
    assert [m.dependency_edge["dependent_answer_record_id"] for m in minted] \
        == ["rec_3", "rec_9", "rec_11"]                          # numeric, unique
    assert [m.record_id for m in minted] == ["rec_12", "rec_13", "rec_14"]
    assert len({m.record_id for m in minted}) == 3
    view = project_assumption_dependencies(s.assertions)
    assert view.by_assumption == (("rec_2", ("rec_3", "rec_9", "rec_11")),)
    assert [d.declaration_record_id for d in view.declarations] \
        == ["rec_12", "rec_13", "rec_14"]


def test_overlapping_active_duplicate_rejects_the_whole_fresh_batch():
    s = _ledger()
    s.record_assumption_dependency_declarations("rec_2", ["rec_3"])
    before = copy.deepcopy(s.assertions)
    with pytest.raises(ValueError):
        s.record_assumption_dependency_declarations("rec_2", ["rec_1", "rec_3", "rec_4"])
    assert s.assertions == before                   # rec_1 / rec_4 were NOT saved alone
    with pytest.raises(InvalidReferenceError):      # and never on load either
        _load(_payloads(s) + [_dep_payload("rec_2", "rec_3", "rec_7")])


# ===========================================================================
# load rules: provenance, validation, malformed payloads, legacy
# ===========================================================================

def test_load_is_owner_stated_and_unvalidated_only():
    base = _payloads(_ledger())
    for bad, err in ((dict(provenance=LEGACY_UNSPECIFIED), InvalidProvenanceError),
                     (dict(provenance="SYSTEM_INFERRED"), InvalidProvenanceError),
                     (dict(provenance="EXPERT_SUPPLIED"), InvalidProvenanceError),
                     (dict(validation_status=SPECIALIST_REVIEWED),
                      InvalidValidationStatusError),
                     (dict(validation_status="INDEPENDENTLY_VERIFIED"),
                      InvalidValidationStatusError)):
        with pytest.raises(err):
            _load(base + [_dep_payload("rec_2", "rec_3", "rec_6", **bad)])
    ok = _load(base + [_dep_payload("rec_2", "rec_3", "rec_6")])
    assert ok.assertions[-1].dependency_edge["assumption_record_id"] == "rec_2"


@pytest.mark.parametrize("over", [
    dict(dependency_edge=None),
    dict(dependency_edge=["rec_2", "rec_3"]),
    dict(dependency_edge={"assumption_record_id": "rec_2"}),
    dict(dependency_edge={"assumption_record_id": "rec_2",
                          "dependent_answer_record_id": "rec_3", "extra": "x"}),
    dict(dependency_edge={"assumption_record_id": "rec_2",
                          "dependent_answer_record_id": "rec_2"}),
    dict(dependency_edge={"assumption_record_id": "rec_02",
                          "dependent_answer_record_id": "rec_3"}),
    dict(dependency_edge={"assumption_record_id": 2,
                          "dependent_answer_record_id": "rec_3"}),
    dict(content="a note"), dict(gap_context=PHYSICAL_FEASIBILITY),
    dict(question_target="mechanical:PHYSICAL_FEASIBILITY:Q1"),
    dict(quality="STRONG"), dict(pending="evidence"), dict(resolves_gap=True),
    dict(contradicts=["rec_1"]), dict(supersedes=["rec_1"]),
    dict(contradiction_endpoints=["rec_1", "rec_3"]),
])
def test_malformed_or_non_neutral_declarations_fail_closed(over):
    with pytest.raises(ContractError):
        _load(_payloads(_ledger()) + [_dep_payload("rec_2", "rec_3", "rec_6", **over)])


def test_edge_field_is_reserved_and_legacy_payloads_round_trip_byte_identically():
    base = _payloads(_ledger())
    assert all("dependency_edge" not in p for p in base)      # omitted, not null
    bad = copy.deepcopy(base)
    bad[0]["dependency_edge"] = {"assumption_record_id": "rec_2",
                                 "dependent_answer_record_id": "rec_3"}
    with pytest.raises(InvalidReferenceError):
        _load(bad)
    # a contradiction declaration may not carry a dependency edge either
    s = _ledger()
    s.record_contradiction_declaration("rec_1", "rec_3")
    bad = _payloads(s)
    bad[-1]["dependency_edge"] = {"assumption_record_id": "rec_2",
                                  "dependent_answer_record_id": "rec_3"}
    with pytest.raises(InvalidReferenceError):
        _load(bad)
    # legacy history (no field anywhere) round-trips byte-identically
    assert _load(base).to_dict()["assertions"] == base
    # a ledger with declarations round-trips byte-identically too
    s = _ledger()
    s.record_assumption_dependency_declarations("rec_2", ["rec_1", "rec_4"])
    full = _payloads(s)
    assert _load(full).to_dict()["assertions"] == full


# ===========================================================================
# chronology through the ONE shared relationship walk
# ===========================================================================

def test_chronology_rules_on_load():
    base = _payloads(_ledger())
    # forward reference: the answer is appended AFTER the declaration
    fwd = base + [_dep_payload("rec_2", "rec_7", "rec_6"),
                  dict(base[0], record_id="rec_7")]
    with pytest.raises(InvalidReferenceError):
        _load(fwd)
    # unknown / foreign-project endpoint (not in THIS ledger)
    with pytest.raises(ContractError):
        _load(base + [_dep_payload("rec_2", "rec_99", "rec_6")])
    # wrong disposition for each role
    for a, d in (("rec_1", "rec_3"), ("rec_2", "rec_5"), ("rec_5", "rec_3")):
        with pytest.raises(InvalidReferenceError):
            _load(base + [_dep_payload(a, d, "rec_6")])


def test_supersession_then_declaration_is_rejected_for_either_endpoint():
    for target in ("rec_2", "rec_3"):
        s = _ledger()
        _correct(s, target)                                            # rec_6
        stale = _payloads(s) + [_dep_payload("rec_2", "rec_3", "rec_7")]
        with pytest.raises(InvalidReferenceError):
            _load(stale)
        before = copy.deepcopy(s.assertions)
        with pytest.raises(ValueError):
            s.record_assumption_dependency_declarations("rec_2", ["rec_3"])
        assert s.assertions == before


def test_declaration_then_later_supersession_is_valid_history():
    s = _ledger()
    s.record_assumption_dependency_declarations("rec_2", ["rec_1", "rec_3", "rec_4"])
    _correct(s, "rec_3")                                              # rec_9 replaces rec_3
    loaded = _load(_payloads(s))                                      # valid history
    view = project_assumption_dependencies(loaded.assertions)
    assert set(view.active_edges) == {("rec_2", "rec_1"), ("rec_2", "rec_4")}
    assert len(view.declarations) == 3                                # history retained
    assert [d.active for d in view.declarations] == [True, False, True]
    # nothing transferred to the replacement answer
    assert all(e[1] != "rec_9" for e in view.active_edges)
    # no record may supersede a declaration
    bad = _payloads(s)
    bad.append(dict(bad[0], record_id="rec_10", supersedes=["rec_6"]))
    with pytest.raises(InvalidReferenceError):
        _load(bad)


def test_independent_edge_inactivity_and_no_transfer():
    # one dependent answer superseded -> only that edge
    s = _ledger()
    s.record_assumption_dependency_declarations("rec_2", ["rec_1", "rec_3"])
    _correct(s, "rec_1")
    assert _active(s) == {("rec_2", "rec_3")}
    # all dependent answers superseded -> no active edge remains
    _correct(s, "rec_3")
    assert _active(s) == set()
    assert len(project_assumption_dependencies(s.assertions).declarations) == 2
    # the assumption superseded -> every edge naming it goes inactive at once
    s = _ledger()
    s.record_assumption_dependency_declarations("rec_2", ["rec_1", "rec_3", "rec_4"])
    new_assumption = _correct(s, "rec_2", "a different assumption")
    view = project_assumption_dependencies(s.assertions)
    assert view.active_edges == () and view.by_assumption == ()
    assert all(d.assumption_record_id == "rec_2" for d in view.declarations)
    assert not any(new_assumption.record_id in (d.assumption_record_id,)
                   for d in view.declarations)
    # the durable load agrees (history valid, projection identical)
    assert project_assumption_dependencies(_load(_payloads(s)).assertions) == view
    # a fresh edge can be declared on the REPLACEMENT assumption explicitly only
    s.record_assumption_dependency_declarations(new_assumption.record_id, ["rec_4"])
    assert _active(s) == {(new_assumption.record_id, "rec_4")}


def test_cap10_contradiction_semantics_are_not_reused_for_dependencies():
    s = _ledger()
    s.record_assumption_dependency_declarations("rec_2", ["rec_1"])
    assert all(r.contradicts == [] for r in s.assertions)            # no CAP-10 edges
    assert IS.active_declared_contradiction_pairs(s.assertions) == frozenset()
    # a CAP-10 declaration and a CAP-08 declaration coexist in one walk
    s.record_contradiction_declaration("rec_1", "rec_3")
    loaded = _load(_payloads(s))
    assert IS.active_declared_contradiction_pairs(loaded.assertions) == {("rec_1", "rec_3")}
    assert set(project_assumption_dependencies(loaded.assertions).active_edges) \
        == {("rec_2", "rec_1")}


# ===========================================================================
# consumers: containment and invariance
# ===========================================================================

_READINESS_CONTEXTS = (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
                       MECHANISM_COMPLETENESS, "PROBLEM_CLARITY", None)


def _readiness(s):
    """The public readiness outputs (DerivedReadiness defines no equality)."""
    r = derive_readiness(s)
    return (r.overall_verified(), tuple(r.unverified_contexts()),
            tuple(r.is_verified(g) for g in _READINESS_CONTEXTS),
            tuple(r._has_active_unresolved_contradiction(g)
                  for g in _READINESS_CONTEXTS))


def _consumer_state():
    s = _ledger()
    s.domain, s.domain_signal, s.path = "mechanical", "mechanical", "N"
    for g in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS):
        s.gaps.append(Gap(g, OPEN, 0))
    return s


def _snapshot(s):
    landscape = derive_requirement_landscape(s)
    return (
        [(r.requirement_id, r.statement, r.primary_anchor.anchor_kind)
         for r in landscape.requirements],
        derive_validation_plan(s),
        _readiness(s),
        derive_next_development_step(s),
        pl.select_next_gap(s),
        pl.compute_serving_decision(s, register_elevated=False),
        s.maturity_level, s.current_stage,
        [(g.gap_type, g.status, g.iterations_open) for g in s.gaps],
        tuple(s.need_routing),
    )


def test_no_consumer_fall_through_and_zero_progress_effect():
    s = _consumer_state()
    before = _snapshot(s)
    s.record_assumption_dependency_declarations("rec_2", ["rec_1", "rec_3", "rec_4"])
    assert _snapshot(s) == before
    ids = {r.record_id for r in s.assertions if r.disposition == DEP}
    reqs = derive_requirement_landscape(s).requirements
    assert not any(r.primary_anchor.anchor_reference in ids for r in reqs)
    assert not any(v.source_ref in ids for v in report_controlled_unknowns(s))
    # and after an endpoint goes inactive: still nothing
    _correct(s, "rec_3")
    before = _snapshot(s)
    assert _snapshot(s) == before


def test_multiple_alternatives_trigger_ignores_the_declaration():
    s = IdeaState(idea_id="w2b")
    s.domain, s.domain_signal, s.path = "software", "software", "N"
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    s.record_interaction("answered", "a", gap_context=MECHANISM_COMPLETENESS)
    s.record_interaction("provisional_assumption", "p",
                         gap_context=MECHANISM_COMPLETENESS)
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    fired = pl._alternatives_crossing_context(s)
    before = pl.compute_serving_decision(s, register_elevated=False)
    assert fired is not None and pl.TRIGGER_MULTIPLE_ALTERNATIVES in before.triggers
    s.record_assumption_dependency_declarations("rec_2", ["rec_1"])
    assert pl._alternatives_crossing_context(s) == fired
    assert pl.compute_serving_decision(s, register_elevated=False) == before


def test_answer_replay_never_sees_a_declaration(client, monkeypatch):
    sid, assumption, answered = _web_project(client)
    _declare(client, sid, assumption, answered)
    assert len(_deps(sid)) == len(answered)
    replayed = []
    real = pl.run_iteration

    def _spy(state, text, *a, **k):
        replayed.append(text)
        return real(state, text, *a, **k)
    monkeypatch.setattr(pl, "run_iteration", _spy)
    recon = SR.reconstruct_readonly_state(_store(), sid)
    assert recon.review.level == 1
    answers = [p["content"] for p in _rows(sid) if p["disposition"] == "answered"]
    # the seed first (unchanged baseline), then the answers only, in durable order
    assert replayed[1:] == answers and len(replayed) == len(answers) + 1
    assert [r.record_id for r in recon.state.assertions if r.disposition == DEP] \
        == [d["record_id"] for d in _deps(sid)]   # carried as records, never replayed


# ===========================================================================
# domain neutrality
# ===========================================================================

@pytest.mark.parametrize("areas", [
    (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS),   # mechanical-shaped
    ("PROBLEM_CLARITY", "MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY"),  # electronics-shaped
    ("SYNTHETIC_AREA_ONE", None, "SYNTHETIC_AREA_TWO"),    # synthetic, no product domain
])
def test_the_same_primitive_works_across_domains(areas):
    s = _ledger(*areas)
    s.record_assumption_dependency_declarations("rec_2", ["rec_4", "rec_1", "rec_3"])
    _correct(s, "rec_4")
    view = project_assumption_dependencies(_load(_payloads(s)).assertions)
    assert view.by_assumption == (("rec_2", ("rec_1", "rec_3")),)


def test_primitive_source_has_no_domain_or_catalog_logic():
    import engine.record_contract as RC
    sources = [inspect.getsource(f) for f in (
        IS.project_assumption_dependencies, IS.normalize_dependent_answers,
        IS.dependency_edge_of, IS.IdeaState.record_assumption_dependency_declarations,
        RC._check_assumption_dependency_declaration,
        RC.ProjectRecordContract._dependency_at_position,
        appmod.declare_dependency, appmod._assumption_dependency_view,
        appmod._issue_cap08_binding, appmod._cap08_eligible_assumptions)]
    for src in sources:
        code = "\n".join(line for line in src.splitlines()
                         if not line.strip().startswith(("#", '"', "'")))
        for word in ("mechanical", "electronic", "electrical", "ASSUMPTION_INVENTORY",
                     "gap_context ==", "question_target ==", "domain"):
            assert word not in code, word


# ===========================================================================
# web
# ===========================================================================

def _raw(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _token(c, sid):
    return _html.unescape(re.search(r'name="answer_token" value="([^"]*)"',
                                    _raw(c, sid)).group(1))


def _dform(c, sid):
    """(answer_token, dependency_binding, dependency_submission) exactly as ONE
    render issues them ("" when no CAP-08 form is offered)."""
    raw = _raw(c, sid)
    token = _html.unescape(re.search(r'name="answer_token" value="([^"]*)"', raw).group(1))
    m = re.search(r'name="dependency_binding" value="([^"]*)"', raw)
    n = re.search(r'name="dependency_submission" value="([^"]*)"', raw)
    return (token, (_html.unescape(m.group(1)) if m else ""),
            (_html.unescape(n.group(1)) if n else ""))


def _cform(c, sid):
    m = re.search(r'name="conflict_binding" value="([^"]*)"', _raw(c, sid))
    return _html.unescape(m.group(1)) if m else ""


def _declare(c, sid, assumption, dependents, confirm="yes", token=None, form=None,
             binding=None, submission=None):
    if form is None:
        form = _dform(c, sid)
    data = {"answer_token": token if token is not None else form[0],
            "dependency_binding": binding if binding is not None else form[1],
            "dependency_submission": (submission if submission is not None
                                      else form[2]),
            "dependent": list(dependents)}
    if assumption is not None:
        data["assumption"] = assumption
    if confirm:
        data["dependency_confirm"] = confirm
    return c.post(f"/session/{sid}/declare-dependency", data=data)


def _assume(c, sid, text=ASSUMPTION):
    r = c.post(f"/session/{sid}", data={"response": text,
                                         "action": "provisional_assumption",
                                         "answer_token": _token(c, sid)})
    assert r.status_code == 302


def _rows(sid):
    return [json.loads(p) for (p,) in _store()._conn.execute(
        "SELECT payload FROM records WHERE project_id = ? ORDER BY seq", (sid,))]


def _deps(sid):
    return [p for p in _rows(sid) if p["disposition"] == DEP]


def _web_project(c, seed=None, domain="mechanical", answers=(MECH, MECH, PF_STRONG, BA_1),
                 lang="en"):
    kw = {} if seed is None else {"seed": seed}
    sid = _start(c, domain=domain, lang=lang, **kw)
    for text in answers:
        _answer(c, sid, text)
    _assume(c, sid)
    state = _live(sid)
    answered = [r.record_id for r in state.assertions
                if r.disposition == "answered" and r.superseded_by is None]
    [assumption] = [r.record_id for r in state.assertions
                    if r.disposition == "provisional_assumption"]
    return sid, assumption, answered


def _progress(state):
    return (state.maturity_level, state.current_stage, state.iteration,
            [(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            pl.select_next_gap(state), tuple(state.need_routing),
            _readiness(state),
            [(r.requirement_id, r.statement)
             for r in derive_requirement_landscape(state).requirements],
            derive_validation_plan(state), derive_next_development_step(state))


def test_web_multi_answer_declaration_end_to_end(client):
    sid, assumption, answered = _web_project(client)
    raw = _raw(client, sid)
    block = re.search(r'<section class="assumption-dependencies".*?</section>', raw, re.S)
    assert block, "the dependency view + form must render"
    form = block.group(0)
    assert re.findall(r'name="assumption" value="([^"]+)"', form) == [assumption]
    assert re.findall(r'name="dependent" value="([^"]+)"', form) == answered
    assert ui_text.text("UI_CAP08_NONE", "en") in _html.unescape(form)
    before = _progress(_live(sid))
    lo, hi = answered[0], answered[-1]
    assert _declare(client, sid, assumption, [hi, lo, hi]).status_code == 302
    body = _body(client, sid)
    assert appmod.DEPENDENCY_DECLARED_ACK in body
    deps = _deps(sid)
    assert [d["dependency_edge"] for d in deps] == [
        {"assumption_record_id": assumption, "dependent_answer_record_id": lo},
        {"assumption_record_id": assumption, "dependent_answer_record_id": hi}]
    assert all(d["provenance"] == OWNER_STATED and d["content"] == "" for d in deps)
    # endpoint rows untouched
    assert all("dependency_edge" not in p for p in _rows(sid) if p["disposition"] != DEP)
    state = _live(sid)
    assert _progress(state) == before                      # zero progress effect
    # live == cold reconstruction == writable resume
    live = _facts(state)
    assert _facts(SR.reconstruct_readonly_state(_store(), sid).state) == live
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _facts(_live(sid)) == live
    view = project_assumption_dependencies(_live(sid).assertions)
    assert view.by_assumption == ((assumption, (lo, hi)),)
    # compact view (session), project record, report subsection + adjacent view
    body = _body(client, sid)
    assert ui_text.text("UI_CAP08_VIEW_HEADING", "en") in body
    assert ui_text.text("UI_CAP08_VIEW_NOTE", "en") in body
    assert ui_text.text("UI_T3A_EVENT_ASSUMPTION_DEPENDENCY_DECLARED", "en") in body
    assert ui_text.text("UI_T3A_DEPENDS_ON_ASSUMPTION", "en") in body
    assert ui_text.text("UI_T3A_DECLARES_DEPENDENT", "en") in body
    deliv = _html.unescape(client.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    assert ui_text.text("UI_CAP08_REPORT_HEADING", "en") in deliv
    assert ui_text.text("UI_CAP08_REPORT_NOT_REQUIREMENT", "en") in deliv
    assert 'class="cap08-dependency-view"' in deliv
    for claim in ("is confirmed", "was rejected", "is resolved", "What is at risk"):
        assert claim not in deliv


def test_deliverable_without_a_declaration_renders_no_cap08_block(client):
    sid, _assumption, _answered = _web_project(client)
    deliv = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "cap08-" not in deliv
    assert ui_text.text("UI_CAP08_REPORT_HEADING", "en") not in _html.unescape(deliv)


def test_web_correcting_one_answer_deactivates_only_that_edge(client):
    sid, assumption, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    _declare(client, sid, assumption, [a, b])
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": a, "response": MECH + " Steel.",
        "answer_token": _token(client, sid)})
    view = project_assumption_dependencies(_live(sid).assertions)
    assert view.active_edges == ((assumption, b),)
    assert [d.active for d in view.declarations] == [False, True]
    body = _body(client, sid)
    assert ui_text.text("UI_T3A_DEPENDENCY_INACTIVE", "en") in body
    assert len(_deps(sid)) == 2                          # history kept, nothing new


# ===========================================================================
# Astra correction F2 — inactive history is never shown as "none recorded"
# ===========================================================================

def _view_note(body):
    m = re.search(r'<section class="assumption-dependencies".*?</section>', body, re.S)
    return m.group(0) if m else ""


def test_f2_three_truthful_states_on_session_and_report(client):
    none_en = ui_text.text("UI_CAP08_NONE", "en")
    hist_en = ui_text.text("UI_CAP08_INACTIVE_HISTORY", "en")
    sid, assumption, answered = _web_project(client)
    # STATE A — never recorded
    view = _view_note(_body(client, sid))
    assert none_en in view and hist_en not in view
    assert "cap08-" not in client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    # STATE C — active
    a = answered[0]
    _declare(client, sid, assumption, [a])
    view = _view_note(_body(client, sid))
    assert none_en not in view and hist_en not in view
    assert f'data-dependency-answer="{a}"' in view
    # STATE B — Astra's reproduction: declared 1, active 0 after correcting the answer
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": a, "response": MECH + " Steel.",
        "answer_token": _token(client, sid)})
    dv = appmod._assumption_dependency_view(_live(sid))
    assert (dv["declared_count"], dv["active_count"]) == (1, 0)
    view = _view_note(_body(client, sid))
    assert hist_en in view and none_en not in view
    assert "data-dependency-inactive-history" in view
    deliv = _html.unescape(client.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    assert deliv.count(hist_en) == 2                 # Section-13 view + declared subsection
    assert none_en not in deliv
    for claim in ("no dependency exists", "dependency is resolved",
                  "dependency was resolved", "dependency is confirmed",
                  "dependency was rejected", "dependency has been validated"):
        assert claim not in deliv.lower()
    # history is preserved: the declaration stays in the durable ledger and in
    # the project record, marked no longer active
    assert len(_deps(sid)) == 1
    body = _body(client, sid)
    assert ui_text.text("UI_T3A_EVENT_ASSUMPTION_DEPENDENCY_DECLARED", "en") in body
    assert ui_text.text("UI_T3A_DEPENDENCY_INACTIVE", "en") in body


def test_f2_arabic_distinguishes_never_recorded_from_inactive_history(client):
    none_ar = ui_text.text("UI_CAP08_NONE", "ar")
    hist_ar = ui_text.text("UI_CAP08_INACTIVE_HISTORY", "ar")
    assert none_ar == "لم تُسجَّل علاقة اعتماد."
    assert hist_ar == "تم تسجيل علاقات اعتماد سابقًا، ولكن لا توجد علاقة اعتماد نشطة حاليًا."
    assert ui_text.text("UI_CAP08_INACTIVE_HISTORY", "en") == (
        "Dependency declarations were recorded previously, but none is currently active.")
    sid, assumption, answered = _web_project(client, answers=(MECH, MECH, PF_STRONG),
                                             lang="ar")
    assert none_ar in _view_note(_body(client, sid))
    _declare(client, sid, assumption, [answered[0]])
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": answered[0], "response": MECH + " Steel.",
        "answer_token": _token(client, sid)})
    view = _view_note(_body(client, sid))
    assert hist_ar in view and none_ar not in view
    deliv = _html.unescape(client.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    assert hist_ar in deliv and none_ar not in deliv


def test_web_refusals_append_nothing(client):
    sid, assumption, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    rows = len(_rows(sid))
    cases = [
        dict(assumption=assumption, dependents=[a], confirm=None),   # no confirmation
        dict(assumption=assumption, dependents=[]),                  # no answer
        dict(assumption=None, dependents=[a]),                       # no assumption
        dict(assumption=[assumption, assumption], dependents=[a]),   # two assumptions
        dict(assumption=a, dependents=[b]),                          # answer as assumption
        dict(assumption=assumption, dependents=[assumption]),        # assumption as answer
        dict(assumption=assumption, dependents=[a, "rec_999"]),      # outside bound set
        dict(assumption=assumption, dependents=[a, "rec_x"]),        # malformed
        dict(assumption=assumption, dependents=[a], token="forged.token"),
        dict(assumption=assumption, dependents=[a], binding=""),     # no CAP-08 binding
        dict(assumption=assumption, dependents=[a], binding="x.y"),  # forged binding
    ]
    for case in cases:
        _declare(client, sid, **case)
        assert len(_rows(sid)) == rows, case
    # a binding or token issued for ANOTHER project never verifies here
    other, _oa, _ob = _web_project(client)
    _declare(client, sid, assumption, [a], form=_dform(client, other))
    _declare(client, sid, assumption, [a], binding=_dform(client, other)[1])
    assert len(_rows(sid)) == rows and _deps(sid) == []


def test_trust_boundary_binding_is_cap08_specific(client):
    sid, assumption, answered = _web_project(client)
    a = answered[0]
    token, binding, _submission = _dform(client, sid)
    rows = len(_rows(sid))
    # a generic answer token alone is not sufficient
    _declare(client, sid, assumption, [a], token=token, binding="")
    # a CAP-10 binding is not a CAP-08 binding (and vice versa)
    cap10 = _cform(client, sid)
    assert cap10
    _declare(client, sid, assumption, [a], binding=cap10)
    client.post(f"/session/{sid}/declare-conflict", data={
        "answer_token": token, "conflict_binding": binding, "note": "",
        "endpoint": answered[:2], "conflict_confirm": "yes"})
    # an answer target (another signed action) is not a CAP-08 binding either
    raw = _raw(client, sid)
    answer_target = _html.unescape(
        re.search(r'name="answer_target" value="([^"]*)"', raw).group(1))
    _declare(client, sid, assumption, [a], binding=answer_target)
    assert len(_rows(sid)) == rows
    # the wrong action kind under a valid-looking structure fails
    import base64
    body, _, sig = binding.rpartition(".")
    data = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))

    def _forge(d):
        enc = base64.urlsafe_b64encode(json.dumps(
            d, sort_keys=True, separators=(",", ":")).encode()).decode().rstrip("=")
        return enc + "." + sig
    _declare(client, sid, assumption, [a], binding=_forge(dict(data, k="CAP10_DECLARE_CONFLICT")))
    # altered assumption set / altered answer set / swapped roles
    _declare(client, sid, "rec_999", [a], binding=_forge(dict(data, a=data["a"] + ["rec_999"])))
    _declare(client, sid, assumption, ["rec_999"],
             binding=_forge(dict(data, d=data["d"] + ["rec_999"])))
    _declare(client, sid, a, [assumption],
             binding=_forge(dict(data, a=data["d"], d=data["a"])))
    assert len(_rows(sid)) == rows and _deps(sid) == []
    # the correctly bound current form works
    _declare(client, sid, assumption, [a])
    assert len(_deps(sid)) == 1


def test_stale_binding_cannot_create_a_new_declaration(client):
    sid, assumption, answered = _web_project(client)
    old = _dform(client, sid)
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": answered[0], "response": MECH,
        "answer_token": _token(client, sid)})
    rows = len(_rows(sid))
    _declare(client, sid, assumption, [answered[1]], form=old)
    assert len(_rows(sid)) == rows
    assert ui_text.text("UI_CAP08_ERR_STALE", "en") in _body(client, sid)
    # a new provisional assumption (eligible assumption set changes) also stales it
    old = _dform(client, sid)
    _assume(client, sid, "Assume the deck stays dry.")
    rows = len(_rows(sid))
    _declare(client, sid, assumption, [answered[1]], form=old)
    assert len(_rows(sid)) == rows
    # a fresh render authorizes again
    _declare(client, sid, assumption, [answered[1]])
    assert len(_deps(sid)) == 1


def test_each_freshness_condition_is_enforced_on_its_own(client):
    """A correctly SIGNED binding for the CURRENT token whose bound assumption
    set, answer set or engine version no longer matches live state is stale."""
    sid, assumption, answered = _web_project(client)
    token = _dform(client, sid)[0]
    state = _live(sid)

    def _signed_for(**over):
        fake = copy.copy(state)
        fake.assertions = [r for r in state.assertions
                           if r.record_id not in over.get("drop", ())]
        if "ecv" in over:
            fake.engine_contract_version = over["ecv"]
        return appmod._issue_cap08_binding(sid, token, fake)
    rows = len(_rows(sid))
    for binding in (_signed_for(drop=[answered[-1]]),          # answer set differs
                    _signed_for(ecv="engine-contract-v0-old")):  # engine version differs
        assert binding
        _declare(client, sid, assumption, [answered[0]], token=token, binding=binding)
        assert len(_rows(sid)) == rows
        assert ui_text.text("UI_CAP08_ERR_STALE", "en") in _body(client, sid)
    # the same construction over the unchanged state is accepted
    _declare(client, sid, assumption, [answered[0]], token=token, binding=_signed_for())
    assert len(_deps(sid)) == 1


def test_duplicate_overlap_rejects_the_whole_fresh_web_batch(client):
    sid, assumption, answered = _web_project(client)
    a, b, c = answered[0], answered[1], answered[-1]
    _declare(client, sid, assumption, [b])
    rows = len(_rows(sid))
    _declare(client, sid, assumption, [a, b, c])            # b already active
    assert len(_rows(sid)) == rows
    assert ui_text.text("UI_CAP08_ERR_STALE", "en") in _body(client, sid)
    assert set(project_assumption_dependencies(_live(sid).assertions).active_edges) \
        == {(assumption, b)}


def test_idempotency_exact_restart_and_after_supersession(client):
    sid, assumption, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    form = _dform(client, sid)
    _declare(client, sid, assumption, [a, b], form=form)
    _declare(client, sid, assumption, [b, a, a], form=form)     # exact retry
    assert len(_deps(sid)) == 2
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)
    # retry after a restart
    appmod.SESSION_STORE.pop(sid)
    client.post(f"/session/{sid}/resume", data={})
    _declare(client, sid, assumption, [a, b], form=form)
    assert len(_deps(sid)) == 2
    # retry after an endpoint was superseded: recognised, reactivates nothing
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": a, "response": MECH, "answer_token": _token(client, sid)})
    rows = len(_rows(sid))
    _declare(client, sid, assumption, [a, b], form=form)
    assert len(_rows(sid)) == rows
    assert project_assumption_dependencies(_live(sid).assertions).active_edges \
        == ((assumption, b),)
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)
    # a DIFFERENT batch on that stale form is new material -> stale, nothing saved
    _declare(client, sid, assumption, [b], form=form)
    assert len(_rows(sid)) == rows


# ===========================================================================
# Astra correction F1 — the submission identity is independent of the material
# ===========================================================================

def _f1_project(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)
    _assume(client, sid)
    for text in (PF_STRONG, BA_1):
        _answer(client, sid, text)
    _assume(client, sid, "Assume the latch spring never fatigues.")
    state = _live(sid)
    answered = [r.record_id for r in state.assertions
                if r.disposition == "answered" and r.superseded_by is None]
    assumptions = [r.record_id for r in state.assertions
                   if r.disposition == "provisional_assumption"]
    assert len(answered) >= 4 and len(assumptions) == 2
    return sid, assumptions, answered


def _edges(sid):
    return [(d["dependency_edge"]["assumption_record_id"],
             d["dependency_edge"]["dependent_answer_record_id"]) for d in _deps(sid)]


@pytest.mark.failure_pattern(
    "FP-02",
    invariant=("a stable action identity never changes with the submitted material; only an exact committed retry is a no-op and the same identity with different material fails closed"),
    constructs=("flask-route", "hmac-signature", "persistence-writer"))
def test_f1_a_to_f_same_identity_changed_material_always_fails_closed(client):
    """Astra's reproduction: the SAME submission identity and SAME valid binding
    first commit one batch; every other material under it is refused."""
    sid, (p1, p2), ans = _f1_project(client)
    form = _dform(client, sid)
    _declare(client, sid, p1, [ans[0], ans[1]], form=form)
    committed = _edges(sid)
    assert committed == [(p1, ans[0]), (p1, ans[1])]
    rows = len(_rows(sid))
    # A — exact retry (any order / duplicates) is a no-op acknowledgement
    _declare(client, sid, p1, [ans[1], ans[0], ans[1]], form=form)
    assert len(_rows(sid)) == rows
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)
    for label, assumption, answers in (
            ("B different assumption", p2, [ans[0], ans[1]]),
            ("C different answer set", p1, [ans[0], ans[2]]),
            ("D subset", p1, [ans[0]]),
            ("E superset", p1, [ans[0], ans[1], ans[2]]),
            ("F disjoint (Astra repro)", p1, [ans[2], ans[3]]),
            ("F disjoint, other assumption", p2, [ans[2], ans[3]])):
        appmod.SESSION_STORE[sid].pop("_interaction_ack", None)
        _declare(client, sid, assumption, answers, form=form)
        assert len(_rows(sid)) == rows, label
        assert _edges(sid) == committed, label
        body = _body(client, sid)
        assert ui_text.text("UI_CAP08_ERR_NOT_SAVED", "en") in body, label
        assert appmod.DEPENDENCY_DECLARED_ACK not in body, label


def test_f1_g_h_exact_retry_after_restart_and_after_supersession(client):
    sid, (p1, _p2), ans = _f1_project(client)
    form = _dform(client, sid)
    _declare(client, sid, p1, [ans[0], ans[1]], form=form)
    rows = len(_rows(sid))
    appmod.SESSION_STORE.pop(sid)                                 # G — restart
    client.post(f"/session/{sid}/resume", data={})
    _declare(client, sid, p1, [ans[0], ans[1]], form=form)
    assert len(_rows(sid)) == rows
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)
    _declare(client, sid, p1, [ans[2], ans[3]], form=form)       # still refused
    assert len(_rows(sid)) == rows
    client.post(f"/session/{sid}/correct", data={                 # H — supersession
        "supersedes_record_id": ans[0], "response": MECH + " Steel.",
        "answer_token": _token(client, sid)})
    rows = len(_rows(sid))
    _declare(client, sid, p1, [ans[0], ans[1]], form=form)
    assert len(_rows(sid)) == rows
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)
    assert project_assumption_dependencies(_live(sid).assertions).active_edges \
        == ((p1, ans[1]),)                                       # nothing reactivated
    _declare(client, sid, p1, [ans[1]], form=form)               # subset: refused
    assert len(_rows(sid)) == rows


def test_f1_i_a_freshly_issued_identity_may_declare_another_batch(client):
    sid, (p1, p2), ans = _f1_project(client)
    first = _dform(client, sid)
    _declare(client, sid, p1, [ans[0], ans[1]], form=first)
    second = _dform(client, sid)                                 # refreshed page
    assert second[2] and second[2] != first[2]                   # a NEW identity
    assert second[1] == first[1]                                 # same WHAT-binding
    _declare(client, sid, p2, [ans[2], ans[3]], form=second)
    assert _edges(sid) == [(p1, ans[0]), (p1, ans[1]), (p2, ans[2]), (p2, ans[3])]
    third = _dform(client, sid)
    assert third[2] not in (first[2], second[2])
    # an identity is retained across renders until consumed (double-submit safe)
    assert _dform(client, sid)[2] == third[2]
    # a spent identity never authorizes new material, even with a fresh binding
    rows = len(_rows(sid))
    _declare(client, sid, p2, [ans[0]], form=third, submission=first[2])
    assert len(_rows(sid)) == rows
    # a correctly SIGNED identity for THIS project that the page never issued
    # (not the live form's current identity) cannot create a new declaration
    unissued = appmod._cap08_submission_for(sid, {})
    _declare(client, sid, p2, [ans[0]], form=third, submission=unissued)
    assert len(_rows(sid)) == rows
    assert ui_text.text("UI_CAP08_ERR_STALE", "en") in _body(client, sid)
    # a forged / other-project identity never verifies
    other = _start(client)
    for bad in ("", "0" * 32 + ".x", first[2][:-1] + "0",
                appmod._cap08_submission_for(other, {})):
        _declare(client, sid, p2, [ans[0]], form=third, submission=bad)
        assert len(_rows(sid)) == rows, bad


@pytest.mark.failure_pattern(
    "FP-08",
    invariant=("a stored batch counts as complete only when exactly its declared number of rows exists; a partial batch is never success"),
    constructs=("parsed-identity-accumulation", "committed-confirmation"))
def test_f1_j_partial_committed_batch_is_never_acknowledged(client):
    sid, (p1, _p2), ans = _f1_project(client)
    form = _dform(client, sid)
    nonce = appmod._verified_cap08_submission(sid, form[2])
    action = appmod._dependency_action_key(sid, nonce)
    keys = appmod._dependency_edge_keys(action, 2)
    # durable state holds ONLY row 0 of a 2-edge batch under this identity
    state = _live(sid)
    minter = IdeaState(idea_id=state.idea_id)
    minter.assertions = copy.deepcopy(state.assertions)
    [first] = minter.record_assumption_dependency_declarations(p1, [ans[0]])
    _store().append_assumption_dependency_declarations(sid, [first], [keys[0]])
    rows = len(_rows(sid))
    for answers in ([ans[0], ans[1]], [ans[0]]):     # the full batch, and the part
        appmod.SESSION_STORE[sid].pop("_interaction_ack", None)
        _declare(client, sid, p1, answers, form=form)
        assert len(_rows(sid)) == rows
        assert appmod.SESSION_STORE[sid].get("_interaction_ack") \
            != appmod.DEPENDENCY_DECLARED_ACK
    assert appmod._committed_dependency_batch(sid, action, p1, [ans[0], ans[1]]) \
        == "conflict"
    assert appmod._committed_dependency_batch(sid, action, p1, [ans[0]]) == "conflict"


def test_f1_k_uncertain_write_needs_the_complete_exact_batch(client, monkeypatch):
    sid, (p1, _p2), ans = _f1_project(client)
    store = _store()
    real = type(store).append_assumption_dependency_declarations

    def commit_part_then_fail(self, project_id, records, keys):
        real(self, project_id, list(records)[:1], list(keys)[:1])  # one row only
        raise StoreError("commit outcome unknown")
    monkeypatch.setattr(type(store), "append_assumption_dependency_declarations",
                        commit_part_then_fail)
    _declare(client, sid, p1, [ans[0], ans[1]])
    assert len(_deps(sid)) == 1                                # the planted part
    entry = appmod.SESSION_STORE[sid]
    assert entry.get("_interaction_ack") != appmod.DEPENDENCY_DECLARED_ACK
    assert project_assumption_dependencies(_live(sid).assertions).declarations == ()
    # the partially spent identity was rotated, so the page offers a new one
    assert appmod.SESSION_STORE[sid].get(appmod._CAP08_SUBMISSION_ENTRY_KEY) is None

    def commit_all_then_fail(self, *args, **kw):
        real(self, *args, **kw)
        raise StoreError("commit outcome unknown")
    monkeypatch.setattr(type(store), "append_assumption_dependency_declarations",
                        commit_all_then_fail)
    # the planted part exists only durably (a real atomic write cannot split
    # like this), so reload the saved project before the next declaration
    appmod.SESSION_STORE.pop(sid)
    client.post(f"/session/{sid}/resume", data={})
    _declare(client, sid, p1, [ans[2], ans[3]])                # a fresh identity
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)
    # the complete exact batch was confirmed (plus the planted part, reloaded)
    assert set(project_assumption_dependencies(_live(sid).assertions).active_edges) \
        == {(p1, ans[0]), (p1, ans[2]), (p1, ans[3])}


# ===========================================================================
# Astra F1 final — canonical, fail-closed committed-batch classification
# ===========================================================================

_ACTION = "ab" * 16
_P = "rec_2"
_A = ["rec_1", "rec_3"]


def _edge(answer):
    return {"disposition": DEP, "content": "",
            "dependency_edge": {"assumption_record_id": _P,
                                "dependent_answer_record_id": answer}}


def _classify(monkeypatch, suffix_rows, answers=_A):
    """Run the REAL classifier over raw committed rows planted verbatim."""
    prefix = appmod._dependency_action_prefix(_ACTION)

    class _Store:
        def committed_records_for_idempotency_key_prefix(self, sid, pfx):
            assert pfx == prefix
            return [(prefix + suffix, _edge(answer)) for suffix, answer in suffix_rows]
    monkeypatch.setattr(appmod, "_get_store", lambda: _Store())
    return appmod._committed_dependency_batch("sid", _ACTION, _P, answers)


@pytest.mark.parametrize("rows,reason", [
    # each fail-closed check is the one that rejects its fixture
    ([("0:2", "rec_1"), ("1:2", "rec_3"), ("00:2", "rec_4")], "non-canonical position"),
    ([("0:2", "rec_1"), ("0:2", "rec_1"), ("1:2", "rec_3")], "duplicate position"),
    ([("0:2", "rec_1"), ("0:2", "rec_3")], "duplicate position"),
    ([("0:2", "rec_1"), ("1:3", "rec_3")], "inconsistent size"),
    ([("0:2", "rec_1"), ("1:2", "rec_3"), ("2:3", "rec_4")], "inconsistent size"),
    ([("0:3", "rec_1"), ("1:3", "rec_3")], "row count"),
    ([("0:1", "rec_1")], "batch size"),
    ([("0:2", "rec_1"), ("1:2", "rec_4")], "material"),
    ([("0:2", "rec_1"), ("1:2", "rec_3")], None),
])
@pytest.mark.failure_pattern(
    "FP-07",
    invariant=("distinct durable rows never collapse onto one logical position; a duplicate position fails closed instead of overwriting"),
    constructs=("parsed-identity-accumulation",))
def test_final_f1_each_check_rejects_its_own_fixture(rows, reason):
    prefix = appmod._dependency_action_prefix(_ACTION)
    raw = [(prefix + suffix, _edge(answer)) for suffix, answer in rows]
    outcome, why = appmod._classify_dependency_rows(prefix, raw, _P, _A)
    assert why == reason and outcome == ("committed" if reason is None else "conflict")


@pytest.mark.parametrize("label,rows,expected", [
    ("A astra: 0,1,00", [("0:2", "rec_1"), ("1:2", "rec_3"), ("00:2", "rec_4")], "conflict"),
    ("A' 00 same answer", [("0:2", "rec_1"), ("1:2", "rec_3"), ("00:2", "rec_1")], "conflict"),
    ("B canonical exact", [("0:2", "rec_1"), ("1:2", "rec_3")], "committed"),
    ("C 00 instead of 0", [("00:2", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("D sign", [("+0:2", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("E size 02", [("0:02", "rec_1"), ("1:02", "rec_3")], "conflict"),
    ("F duplicate raw position", [("0:2", "rec_1"), ("0:2", "rec_1"),
                                  ("1:2", "rec_3")], "conflict"),
    ("F' duplicate, no index 1", [("0:2", "rec_1"), ("0:2", "rec_3")], "conflict"),
    ("G extra row 2:2", [("0:2", "rec_1"), ("1:2", "rec_3"), ("2:2", "rec_4")], "conflict"),
    ("H incomplete 0:3,1:3", [("0:3", "rec_1"), ("1:3", "rec_3")], "conflict"),
    ("I inconsistent size", [("0:2", "rec_1"), ("1:3", "rec_3")], "conflict"),
    ("J extra component", [("0:2:x", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J empty index", [(":2", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J empty size", [("0:", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J no separator", [("02", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J whitespace", [(" 0:2", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J trailing space", [("0:2 ", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J minus", [("-0:2", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J unicode digit", [("\u0660:2", "rec_1"), ("1:2", "rec_3")], "conflict"),
    ("J underscore", [("0:2", "rec_1"), ("1_0:2", "rec_3")], "conflict"),
    ("J index >= size", [("0:2", "rec_1"), ("2:2", "rec_3")], "conflict"),
    ("J size zero", [("0:0", "rec_1")], "conflict"),
    ("material differs", [("0:2", "rec_1"), ("1:2", "rec_4")], "conflict"),
])
def test_final_f1_classifier_accepts_only_the_exact_canonical_batch(
        monkeypatch, label, rows, expected):
    assert _classify(monkeypatch, rows) == expected, label


@pytest.mark.failure_pattern(
    "FP-06",
    invariant=("a durable identifier is accepted only in the exact canonical spelling the writer emits"),
    constructs=("canonical-identifier-parsing", "parsed-identity-accumulation"))
def test_final_f1_canonical_position_parser():
    ok = appmod._canonical_edge_position
    assert ok("0:1") == (0, 1) and ok("9:10") == (9, 10) and ok("10:11") == (10, 11)
    for bad in ("00:1", "01:2", "0:01", "+1:2", "-1:2", " 1:2", "1:2 ", "1 :2",
                "1:2:3", ":", "", "1", "a:2", "1:b", "1.0:2", "2:2", "3:2", "0:0",
                "\u0661:2", None):
        assert ok(bad) is None, bad
    # the writer emits only spellings the reader accepts
    for n in (1, 2, 11):
        keys = appmod._dependency_edge_keys(_ACTION, n)
        prefix = appmod._dependency_action_prefix(_ACTION)
        assert [ok(k[len(prefix):]) for k in keys] == [(i, n) for i in range(n)]


def _plant(sid, nonce, rows, p, extra_prefix=None):
    """Durably commit raw rows under the action prefix of ``nonce``: ``rows`` is
    [(suffix, answer_id)], all under assumption ``p`` (one atomic append)."""
    action = appmod._dependency_action_key(sid, nonce)
    prefix = appmod._dependency_action_prefix(action)
    state = _live(sid)
    minter = IdeaState(idea_id=state.idea_id)
    minter.assertions = copy.deepcopy(state.assertions)
    records = minter.record_assumption_dependency_declarations(
        p, [answer for _suffix, answer in rows])
    by_answer = {r.dependency_edge["dependent_answer_record_id"]: r for r in records}
    ordered = [by_answer[answer] for _suffix, answer in rows]
    _store().append_assumption_dependency_declarations(
        sid, ordered, [prefix + suffix for suffix, _answer in rows])


def test_final_f1_k_astra_reproduction_through_exact_retry_is_not_acknowledged(client):
    sid, (p1, _p2), ans = _f1_project(client)
    form = _dform(client, sid)
    nonce = appmod._verified_cap08_submission(sid, form[2])
    _plant(sid, nonce, [("0:2", ans[0]), ("1:2", ans[1]), ("00:2", ans[2])], p1)
    rows = len(_rows(sid))
    live_before = copy.deepcopy(_live(sid).assertions)
    appmod.SESSION_STORE[sid].pop("_interaction_ack", None)
    _declare(client, sid, p1, [ans[0], ans[1]], form=form)       # "exact retry"
    assert len(_rows(sid)) == rows
    entry = appmod.SESSION_STORE[sid]
    assert entry.get("_interaction_ack") != appmod.DEPENDENCY_DECLARED_ACK
    assert entry.get("_answer_error") == appmod.DEPENDENCY_NOT_SAVED_MESSAGE
    assert _live(sid).assertions == live_before                  # nothing published


def test_final_f1_l_astra_reproduction_through_uncertain_write_is_not_acknowledged(
        client, monkeypatch):
    sid, (p1, _p2), ans = _f1_project(client)
    form = _dform(client, sid)
    nonce = appmod._verified_cap08_submission(sid, form[2])
    store = _store()

    def plant_malformed_then_fail(self, project_id, records, keys):
        # the durable outcome of this attempt is Astra's inconsistent state
        monkeypatch.undo()
        _plant(sid, nonce, [("0:2", ans[0]), ("1:2", ans[1]), ("00:2", ans[2])], p1)
        raise StoreError("commit outcome unknown")
    monkeypatch.setattr(type(store), "append_assumption_dependency_declarations",
                        plant_malformed_then_fail)
    live_before = copy.deepcopy(_live(sid).assertions)
    _declare(client, sid, p1, [ans[0], ans[1]], form=form)
    entry = appmod.SESSION_STORE[sid]
    assert entry.get("_interaction_ack") != appmod.DEPENDENCY_DECLARED_ACK
    assert entry.get("_answer_error") == appmod.DEPENDENCY_NOT_SAVED_MESSAGE
    assert _live(sid).assertions == live_before                  # no partial publication
    assert project_assumption_dependencies(_live(sid).assertions).declarations == ()
    assert len(_deps(sid)) == 3                                  # nothing deleted/repaired


def test_final_f1_m_n_normal_retry_and_new_action_still_work(client):
    sid, (p1, p2), ans = _f1_project(client)
    form = _dform(client, sid)
    _declare(client, sid, p1, [ans[0], ans[1]], form=form)
    rows = len(_rows(sid))
    appmod.SESSION_STORE[sid].pop("_interaction_ack", None)
    _declare(client, sid, p1, [ans[1], ans[0]], form=form)       # M: exact retry
    assert len(_rows(sid)) == rows
    assert appmod.SESSION_STORE[sid].get("_interaction_ack") \
        == appmod.DEPENDENCY_DECLARED_ACK
    _declare(client, sid, p2, [ans[2]])                          # N: new action
    assert _edges(sid) == [(p1, ans[0]), (p1, ans[1]), (p2, ans[2])]


def test_f1_identity_does_not_depend_on_the_selection():
    a = appmod._dependency_action_key("sid-x", "0" * 32)
    assert a == appmod._dependency_action_key("sid-x", "0" * 32)
    assert a != appmod._dependency_action_key("sid-y", "0" * 32)
    assert inspect.signature(appmod._dependency_action_key).parameters.keys() \
        == {"sid", "nonce"}
    keys = appmod._dependency_edge_keys(a, 3)
    assert keys == [f"cap08:{a}:0:3", f"cap08:{a}:1:3", f"cap08:{a}:2:3"]


def test_uncertain_or_failed_commits_never_claim_a_save(client, monkeypatch):
    sid, assumption, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    store = _store()
    real = type(store).append_assumption_dependency_declarations

    def fail_before(self, *args, **kw):
        raise StoreError("unavailable")
    monkeypatch.setattr(type(store), "append_assumption_dependency_declarations",
                        fail_before)
    live_before = copy.deepcopy(_live(sid).assertions)
    _declare(client, sid, assumption, [a, b])
    assert _deps(sid) == [] and _live(sid).assertions == live_before
    assert ui_text.text("UI_CAP08_ERR_NOT_SAVED", "en") in _body(client, sid)

    def commit_then_fail(self, *args, **kw):          # committed, outcome lost
        real(self, *args, **kw)
        raise StoreError("commit outcome unknown")
    monkeypatch.setattr(type(store), "append_assumption_dependency_declarations",
                        commit_then_fail)
    _declare(client, sid, assumption, [a, b])
    assert len(_deps(sid)) == 2
    assert set(project_assumption_dependencies(_live(sid).assertions).active_edges) \
        == {(assumption, a), (assumption, b)}
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)

    monkeypatch.setattr(type(store), "append_assumption_dependency_declarations",
                        fail_before)
    monkeypatch.setattr(type(store), "committed_records_for_idempotency_key_prefix",
                        lambda self, *a, **k: (_ for _ in ()).throw(StoreError("x")))
    rows = len(_rows(sid))
    _declare(client, sid, assumption, [answered[1]])
    assert len(_rows(sid)) == rows


class _CommitAndRollbackFail:
    def __init__(self, conn):
        self._conn = conn
        self.armed = True

    def execute(self, sql, *args):
        if self.armed and sql in ("COMMIT", "ROLLBACK"):
            if sql == "ROLLBACK":
                self.armed = False
            raise sqlite3.OperationalError("injected: %s failed" % sql)
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def _independent_deps(sid):
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return [json.loads(p) for (p,) in conn.execute(
            "SELECT payload FROM records WHERE project_id = ?", (sid,))
            if json.loads(p)["disposition"] == DEP]
    finally:
        conn.close()


def test_failed_commit_and_rollback_never_publishes_uncommitted_data(client):
    sid, assumption, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    store = _store()
    real = store._conn
    live_before = copy.deepcopy(_live(sid).assertions)
    try:
        store._conn = _CommitAndRollbackFail(real)
        _declare(client, sid, assumption, [a, b])
        assert real.in_transaction                        # own uncommitted rows exist
        assert _independent_deps(sid) == []               # nothing committed
        assert store.committed_state_readable() is False
        assert _live(sid).assertions == live_before       # nothing published
        entry = appmod.SESSION_STORE[sid]
        assert entry.get("_interaction_ack") != appmod.DEPENDENCY_DECLARED_ACK
        assert entry.get("_answer_error") == appmod.DEPENDENCY_UNKNOWN_MESSAGE
        entry.pop("_answer_error", None)
        _declare(client, sid, assumption, [answered[1]])  # unresolved: writes nothing
        assert _independent_deps(sid) == []
    finally:
        store._conn = real
        if real.in_transaction:
            real.execute("ROLLBACK")
    store.close()
    appmod._STORE = None
    assert _independent_deps(sid) == []
    _declare(client, sid, assumption, [a, b])
    assert len(_independent_deps(sid)) == 2


def test_uncertain_commit_confirmed_from_committed_state_is_acknowledged(client):
    sid, assumption, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    store = _store()
    real = store._conn

    class _CommitThenRaise:
        def __init__(self, conn):
            self._conn, self.armed = conn, True

        def execute(self, sql, *args):
            if sql == "COMMIT" and self.armed:
                self.armed = False
                self._conn.execute("COMMIT")
                raise sqlite3.OperationalError("injected: error after commit")
            return self._conn.execute(sql, *args)

        def __getattr__(self, name):
            return getattr(self._conn, name)
    try:
        store._conn = _CommitThenRaise(real)
        _declare(client, sid, assumption, [a, b])
    finally:
        store._conn = real
    assert store.committed_state_readable() is True
    assert len(_independent_deps(sid)) == 2
    assert appmod.DEPENDENCY_DECLARED_ACK in _body(client, sid)


def test_store_batch_is_atomic_and_revalidated_inside_the_transaction(client):
    sid, assumption, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    state = _live(sid)
    minter = IdeaState(idea_id=state.idea_id)
    minter.assertions = copy.deepcopy(state.assertions)
    staged = minter.record_assumption_dependency_declarations(assumption, [a, b])
    # a correction of ONE endpoint commits between the check and the append
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": b, "response": BA_1, "answer_token": _token(client, sid)})
    n = len(_rows(sid))
    for i, r in enumerate(staged):
        r.record_id = "rec_%d" % (n + 1 + i)
    with pytest.raises(AssumptionDependencyDeclarationRejected):
        _store().append_assumption_dependency_declarations(sid, staged, ["k1" * 16, "k2" * 16])
    assert len(_rows(sid)) == n                         # NOT even the valid first edge
    # a duplicate key on the SECOND edge rolls back the FIRST edge too
    state = _live(sid)
    minter = IdeaState(idea_id=state.idea_id)
    minter.assertions = copy.deepcopy(state.assertions)
    [first] = minter.record_assumption_dependency_declarations(assumption, [a])
    _store().append_assumption_dependency_declarations(sid, [first], ["j" * 32])
    n = len(_rows(sid))
    minter.assertions = copy.deepcopy(_live(sid).assertions) + [first]
    batch = minter.record_assumption_dependency_declarations(assumption, [answered[1], answered[2]])
    with pytest.raises(sqlite3.IntegrityError):
        _store().append_assumption_dependency_declarations(sid, batch, ["m" * 32, "j" * 32])
    assert len(_rows(sid)) == n
    # malformed batches are refused before any write
    for records, keys in (([], []), (batch, ["x" * 32]), (batch, ["y" * 32, "y" * 32]),
                          (batch, ["z" * 32, ""])):
        with pytest.raises(AssumptionDependencyDeclarationRejected):
            _store().append_assumption_dependency_declarations(sid, records, keys)
    assert len(_rows(sid)) == n


def test_copy_is_truthful_in_english_and_arabic(client):
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP08_")] + [
        "UI_T3A_EVENT_ASSUMPTION_DEPENDENCY_DECLARED", "UI_T3A_DEPENDS_ON_ASSUMPTION",
        "UI_T3A_DECLARES_DEPENDENT", "UI_T3A_DEPENDENCY_INACTIVE"]
    assert len(keys) >= 20
    for key in keys:
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en and ar and en != ar and re.search("[؀-ۿ]", ar)
        for bad in FORBIDDEN_EN + ("AI ", "detected", "verified"):
            assert bad not in " " + en + " ", (key, bad)
        for bad in ("تم التحقق", "معتمد", "الذكاء الاصطناعي", "مؤكَّد", "مرفوض"):
            assert bad not in ar, (key, bad)
    for msg in (appmod.DEPENDENCY_NOT_SAVED_MESSAGE, appmod.DEPENDENCY_INVALID_MESSAGE,
                appmod.DEPENDENCY_STALE_MESSAGE, appmod.DEPENDENCY_UNKNOWN_MESSAGE):
        assert ui_text.localize_message(msg, "ar") != msg
    ack_ar = ui_text.localize_deep(appmod.DEPENDENCY_DECLARED_ACK, "ar")
    assert ack_ar != appmod.DEPENDENCY_DECLARED_ACK and "غير مُتحقَّق" in ack_ar
    # "No dependency recorded", never "no dependency exists"
    assert ui_text.text("UI_CAP08_NONE", "en") == "No dependency recorded."
    # Arabic journey
    sid, assumption, answered = _web_project(client, answers=(MECH, MECH, PF_STRONG),
                                             lang="ar")
    body = _body(client, sid)
    assert ui_text.text("UI_CAP08_HEADING", "ar") in body
    _declare(client, sid, assumption, answered[:2])
    body = _body(client, sid)
    assert ack_ar in body and ui_text.text("UI_CAP08_VIEW_NOTE", "ar") in body
    assert len(_deps(sid)) == 2


def test_electronics_journey_uses_the_same_primitive(client):
    sid = _start(client, seed=ELEC_SEED, domain="electronics_electrical")
    assert 'class="assumption-dependencies"' not in _raw(client, sid)   # nothing eligible
    for text in ("The heater relay opens when a thermistor reading passes a set "
                 "threshold, cutting mains power to the heater element.",
                 "A microcontroller reads the thermistor and drives the relay coil "
                 "through a transistor."):
        _answer(client, sid, text)
    _assume(client, sid, "Assume the relay contacts are rated for the heater current.")
    state = _live(sid)
    answered = [r.record_id for r in state.assertions if r.disposition == "answered"]
    [assumption] = [r.record_id for r in state.assertions
                    if r.disposition == "provisional_assumption"]
    before = _progress(state)
    _declare(client, sid, assumption, answered)
    assert len(_deps(sid)) == len(answered)
    assert _progress(_live(sid)) == before
    assert project_assumption_dependencies(_live(sid).assertions).by_assumption \
        == ((assumption, tuple(answered)),)
