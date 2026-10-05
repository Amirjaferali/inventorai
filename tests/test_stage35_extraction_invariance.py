"""Stage 35 — first bounded slice — permitted extractions E1–E4 (BASE RED, file X).

Implementation contract §2.3 and §14 #11: each extraction is behaviour-preserving;
existing surfaces stay identical. The canonical deliverable package is compared
against the implementation base module itself (minus ``generated_at``).
"""
import os
import subprocess
import types

import pytest

import web.app as webapp
from engine import deliverable_assembler as da
from engine import experiment_result as er
from engine import session_reconstruction as sr
from engine.idea_state import (
    ASSERTED, Evidence, Gap, IdeaState, MeasurementMethod, PROBLEM_MECHANISM_FIT,
    REASONED, SuccessCriterion, TestHypothesis, TestVariable,
)
from tests.csrf_client import csrf_client

BASE = "c79708519961bc0cd4e254c7c47190af6604b4b4"
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = ("A folding ramp for wheelchairs with a spring latch that locks the deck "
        "flat on a step.")
MECH = ("The load path runs from the deck panel into the hinge line and the spring "
        "latch transfers force into the frame rail, so the ramp stays locked flat.")


def _base_assembler():
    out = subprocess.run(["git", "show", BASE + ":engine/deliverable_assembler.py"],
                         capture_output=True, cwd=_ROOT)
    assert out.returncode == 0
    module = types.ModuleType("_stage35_base_assembler")
    module.__file__ = os.path.join(_ROOT, "engine", "deliverable_assembler.py")
    exec(compile(out.stdout.decode("utf-8"), module.__file__, "exec"), module.__dict__)
    return module


def _states():
    """A spread of in-memory states: problem from idea_summary, from PMF evidence,
    none at all; a REASONED mechanism (priority-3 experiment); an acknowledged
    unknown (priority-1 experiment) with planning metadata attached."""
    a = IdeaState(idea_id="x1")
    a.idea_summary = "Wheelchair users cannot cross a single step."
    a.idea_summary_quality = ASSERTED
    a.known_mechanism = Evidence(MECH, REASONED, 1)
    b = IdeaState(idea_id="x2")
    b.gaps.append(Gap(PROBLEM_MECHANISM_FIT, "PARTIAL", 0,
                      evidence=[Evidence("Steps block wheelchairs.", REASONED, 1)]))
    c = IdeaState(idea_id="x3")
    d = IdeaState(idea_id="x4")
    d.known_mechanism = Evidence(MECH, REASONED, 1)
    d.record_interaction("answered", "The deck is aluminium.",
                         gap_context="PHYSICAL_FEASIBILITY")
    return [a, b, c, d]


def _strip(package):
    package = dict(package)
    package.pop("generated_at", None)
    return package


# ---------------------------------------------------------------------------
# E1 — resolved_problem
# ---------------------------------------------------------------------------
def test_e1_public_resolved_problem_and_alias():
    assert da._resolved_problem is da.resolved_problem
    for state in _states():
        got = da.resolved_problem(state)
        assert got == da._resolved_problem(state)
    assert da.resolved_problem(_states()[2]) is None


def test_e1_e4_canonical_package_identical_to_the_base_module():
    base = _base_assembler()
    for state in _states():
        assert _strip(da.assemble_deliverable(state)) == _strip(base.assemble_deliverable(state))
        assert da.resolved_problem(state) == base._resolved_problem(state)


# ---------------------------------------------------------------------------
# E4 — gap_status_label
# ---------------------------------------------------------------------------
def test_e4_gap_status_label_reads_the_unchanged_dict():
    assert da._STATUS_LABELS == {"OPEN": "Open", "PARTIAL": "Partially addressed",
                                 "CLOSED": "Answered (not yet validated)",
                                 "ACCEPTED_RISK": "Accepted risk"}
    for status, label in da._STATUS_LABELS.items():
        assert da.gap_status_label(status) == label
    assert da.gap_status_label("UNKNOWN_STATUS") is None


# ---------------------------------------------------------------------------
# E3 — execution_states
# ---------------------------------------------------------------------------
def test_e3_constants_and_aliases():
    assert (er.EXECUTION_NONE, er.EXECUTION_RECORDED, er.EXECUTION_UNAVAILABLE) == (
        "none", "recorded", "unavailable")
    assert webapp._EXECUTION_NONE == er.EXECUTION_NONE
    assert webapp._EXECUTION_RECORDED == er.EXECUTION_RECORDED
    assert webapp._EXECUTION_UNAVAILABLE == er.EXECUTION_UNAVAILABLE


def test_e3_execution_states_counts_execution_roots():
    ctx = er.ResultContext("Experiment")
    a1 = er.recorded_root("exp_a_one", "first", ctx)
    a1c = er.recorded_correction("exp_a_one", "first corrected", a1.result_event_id)
    a2 = er.recorded_root("exp_a_one", "retest", ctx)
    events = (a1, a1c, a2)
    got = er.execution_states(events, ["exp_a_one", "exp_b_two"])
    assert got == {"exp_a_one": {"state": "recorded", "count": 2},
                   "exp_b_two": {"state": "none", "count": 0}}
    assert er.execution_states((), []) == {}


def test_e3_web_helper_keeps_its_catch_all(monkeypatch):
    package = {"section_11_prototype_test_plan": {"items": [{"experiment_id": "exp_a_one"}]}}

    class _Boom:
        def load_result_events(self, sid):
            raise RuntimeError("boom")

    monkeypatch.setattr(webapp, "_get_store", lambda: _Boom())
    assert webapp._experiment_execution_states("p", package) == {
        "exp_a_one": {"state": "unavailable", "count": None}}
    assert webapp._experiment_execution_states("p", {}) == {}


def test_e3_engine_function_never_reads_the_store_or_swallows():
    import inspect
    import re
    code = re.sub(r'(?s)"{3}.*?"{3}', "", inspect.getsource(er.execution_states))
    assert "store" not in code and "except" not in code and "try" not in code


# ---------------------------------------------------------------------------
# E2 — planning metadata
# ---------------------------------------------------------------------------
@pytest.fixture()
def project():
    webapp.app.config["TESTING"] = True
    with csrf_client(webapp.app) as c:
        r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
        assert r.status_code == 302
        pid = r.headers["Location"].rsplit("/", 1)[-1]
    return webapp._get_store(), pid


def test_e2_load_planning_metadata_builds_the_same_maps(project):
    store, pid = project
    eid = "exp_stage35_e2_probe"
    store.apply_planning_metadata_delta(pid, {eid: "crit"}, {eid: "meth"},
                                        {eid: "hyp"}, {eid: "var"})
    md = sr.load_planning_metadata(store, pid)
    assert set(md) == {"success_criteria", "measurement_methods", "test_hypotheses",
                       "test_variables"}
    assert md["success_criteria"] == {eid: SuccessCriterion(criterion="crit")}
    assert md["measurement_methods"] == {eid: MeasurementMethod(method="meth")}
    assert md["test_hypotheses"] == {eid: TestHypothesis(hypothesis="hyp")}
    assert md["test_variables"] == {eid: TestVariable(variable="var")}
    assert webapp._durable_success_criteria(pid) == md["success_criteria"]
    assert webapp._durable_measurement_methods(pid) == md["measurement_methods"]
    assert webapp._durable_test_hypotheses(pid) == md["test_hypotheses"]
    assert webapp._durable_test_variables(pid) == md["test_variables"]


def test_e2_project_not_found_is_none_per_collection(project):
    store, _pid = project
    md = sr.load_planning_metadata(store, "no-such-project")
    assert md == {"success_criteria": None, "measurement_methods": None,
                  "test_hypotheses": None, "test_variables": None}
    assert webapp._durable_success_criteria("no-such-project") is None
    state = IdeaState(idea_id="x")
    state.success_criteria = {"keep": SuccessCriterion("kept")}
    assert sr.attach_planning_metadata(store, "no-such-project", state) is True
    assert state.success_criteria == {"keep": SuccessCriterion("kept")}


def test_e2_every_other_failure_raises_from_the_loader_and_attach_is_all_or_nothing(
        project, monkeypatch):
    store, pid = project

    def boom(self, project_id):
        raise RuntimeError("storage")

    monkeypatch.setattr(type(store), "load_test_variables", boom)
    with pytest.raises(RuntimeError):
        sr.load_planning_metadata(store, pid)
    state = IdeaState(idea_id="x")
    state.success_criteria = {"keep": SuccessCriterion("kept")}
    assert sr.attach_planning_metadata(store, pid, state) is False
    assert state.success_criteria == {"keep": SuccessCriterion("kept")}
    assert webapp._attach_planning_metadata(pid, state) is False
    assert state.success_criteria == {"keep": SuccessCriterion("kept")}


def test_e2_apply_is_pure_and_leaves_none_collections_untouched():
    state = IdeaState(idea_id="x")
    state.measurement_methods = {"keep": MeasurementMethod("kept")}
    md = {"success_criteria": {"e": SuccessCriterion("c")}, "measurement_methods": None,
          "test_hypotheses": {}, "test_variables": {}}
    sr.apply_planning_metadata(state, md)
    assert state.success_criteria == {"e": SuccessCriterion("c")}
    assert state.measurement_methods == {"keep": MeasurementMethod("kept")}
    assert state.test_hypotheses == {} and state.test_variables == {}


def test_e2_web_wrappers_delegate_to_the_engine():
    import inspect
    for name in ("_durable_success_criteria", "_durable_measurement_methods",
                 "_durable_test_hypotheses", "_durable_test_variables"):
        src = inspect.getsource(getattr(webapp, name))
        assert "_load_planning_collection(" in src
    assert "attach_planning_metadata(" in inspect.getsource(webapp._attach_planning_metadata)
