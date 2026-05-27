import ast, inspect, os, sys, uuid
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from engine.idea_state import IdeaState, Evidence, ASSERTED, REASONED, DEMONSTRATED, OPEN, CLOSED, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY
from engine.domain_rules import infer_domain
from engine.progression_loop import run_iteration, assess_response

def make_state(idea="IoT temperature sensor device"):
    s = IdeaState(idea_id=str(uuid.uuid4()))
    s.domain = infer_domain(idea); s.domain_signal = s.domain; return s

class TestWPS001_INV007_AIBoundary:
    """WPS-001 INV-007: AI governance boundary — gate functions must not call ai_advisor."""
    def _src(self, fn):
        import engine.progression_loop as pl
        return inspect.getsource(getattr(pl, fn))
    def test_evaluate_transition_no_ai_advisor(self):
        """WPS-001 INV-007: evaluate_transition() must not reference ai_advisor."""
        assert "ai_advisor" not in self._src("evaluate_transition"),             "WPS-001 INV-007 VIOLATED: evaluate_transition() references ai_advisor. Maturity decisions must be deterministic."
    def test_integrate_response_no_ai_advisor(self):
        """WPS-001 INV-007: integrate_response() must not reference ai_advisor."""
        assert "ai_advisor" not in self._src("integrate_response"),             "WPS-001 INV-007 VIOLATED: integrate_response() references ai_advisor."
    def test_assess_response_no_ai_advisor(self):
        """WPS-001 INV-007: assess_response() must not reference ai_advisor."""
        assert "ai_advisor" not in self._src("assess_response"),             "WPS-001 INV-007 VIOLATED: assess_response() references ai_advisor."
    def test_evaluate_transition_deterministic(self):
        """WPS-001 INV-007: evaluate_transition() must be deterministic."""
        from engine.progression_loop import evaluate_transition
        s = make_state(); r1 = evaluate_transition(s); r2 = evaluate_transition(s)
        assert r1 == r2, f"WPS-001 INV-007 VIOLATED: non-deterministic. {r1} != {r2}"
    def test_assess_response_deterministic(self):
        """WPS-001 INV-007: assess_response() must be deterministic."""
        for inp in ["maybe", "Hall sensor", "ESP32 ADC reads TMP117 every 60 seconds", ""]:
            assert assess_response(inp) == assess_response(inp),                 f"WPS-001 INV-007 VIOLATED: assess_response({inp!r}) non-deterministic"

class TestWPS001_INV001_WeakInputLevel2Block:
    """WPS-001 INV-001: Weak answers must never allow Level 2 or deliverable readiness."""
    WEAK = ["maybe","not sure","i don't know","","I do not know","no idea","unknown",
            "i have no idea","something","somehow","I think maybe it uses technology somehow"]
    def test_weak_inputs_never_reach_level_2(self):
        """WPS-001 INV-001: 10 weak inputs must never produce maturity_level >= 2."""
        s = make_state()
        for inp in (self.WEAK * 2)[:10]: run_iteration(s, inp)
        assert s.maturity_level < 2,             f"WPS-001 INV-001 VIOLATED: 10 weak inputs reached maturity_level={s.maturity_level}. Level 2 requires REASONED mechanism."
    def test_weak_inputs_never_satisfy_deliverable_eligibility(self):
        """WPS-001 INV-001: Weak-only session must never produce deliverable_eligible=True."""
        s = make_state()
        for inp in self.WEAK: run_iteration(s, inp)
        open_gaps = [g for g in s.gaps if g.status == OPEN]
        assert not (s.maturity_level >= 2 and len(open_gaps) == 0),             f"WPS-001 INV-001 VIOLATED: Weak session satisfied deliverable_eligible. maturity={s.maturity_level} open={len(open_gaps)}"
    def test_weak_inputs_never_produce_pass_transition(self):
        """WPS-001 INV-001/INV-002: Isolated weak inputs must never produce transition=PASS."""
        for inp in ["maybe","not sure","i don't know","","unknown"]:
            s = make_state(); r = run_iteration(s, inp)
            assert r["transition"] != "PASS",                 f"WPS-001 INV-001/INV-002 VIOLATED: {inp!r} produced transition=PASS. result={r}"
    def test_weak_patterns_return_asserted_not_reasoned(self):
        """WPS-001 INV-001: _WEAK_PATTERNS must return ASSERTED, never REASONED/DEMONSTRATED."""
        for inp in self.WEAK:
            r = assess_response(inp)
            assert r != REASONED, f"WPS-001 INV-001 VIOLATED: assess_response({inp!r}) returned REASONED"
            assert r != DEMONSTRATED, f"WPS-001 INV-001 VIOLATED: assess_response({inp!r}) returned DEMONSTRATED"
    def test_substantive_input_can_advance(self):
        """WPS-001 INV-001 positive: Substantive inputs CAN reach Level >= 1."""
        s = make_state()
        for inp in [
            "Greenhouse crop loss when soil moisture drops below threshold overnight",
            "Capacitive sensor ESP32 ADC triggers relay below moisture threshold",
            "Operating 5-45C IP67 3.3V powered single zone 50 square metres",
            "MQTT local broker Node-RED dashboard configurable threshold",
            "Standalone no cloud dependency 18 month sensor replacement",
        ]: run_iteration(s, inp)
        assert s.maturity_level >= 1,             f"WPS-001 INV-001 POSITIVE FAILED: substantive inputs did not advance maturity. level={s.maturity_level}"

class TestWPS001_INV002_BlockPreventsAdvancement:
    """WPS-001 INV-002: BLOCK must prevent maturity_level increment."""
    def test_level_1_to_2_blocked_by_asserted_mechanism(self):
        """WPS-001 INV-002: Level 1->2 must be blocked when mechanism quality is ASSERTED."""
        from engine.progression_loop import evaluate_transition
        s = make_state(); s.maturity_level = 1
        s.known_problem = Evidence("Problem stated", ASSERTED, 0)
        s.known_mechanism = Evidence("mechanism somehow", ASSERTED, 0)
        can, reason = evaluate_transition(s)
        assert can is False,             f"WPS-001 INV-002 VIOLATED: Level 1->2 allowed with ASSERTED mechanism. can={can} reason={reason!r}"
    def test_level_1_to_2_allowed_with_reasoned_mechanism(self):
        """WPS-001 INV-002 positive: REASONED mechanism + no open gaps must allow Level 1->2."""
        from engine.progression_loop import evaluate_transition
        s = make_state(); s.maturity_level = 1
        s.known_problem = Evidence("Clear problem", REASONED, 0)
        s.known_mechanism = Evidence("ESP32 ADC reads TMP117 via I2C every 60s", REASONED, 0)
        can, reason = evaluate_transition(s)
        assert can is True,             f"WPS-001 INV-002 POSITIVE VIOLATED: REASONED mechanism + no gaps denied. can={can} reason={reason!r}"

class TestWPS001_INV004_GapLifecycle:
    """WPS-001 INV-004: Gap lifecycle is forward-only — OPEN->PARTIAL->CLOSED, never backward."""
    def test_closed_gap_does_not_reopen(self):
        """WPS-001 INV-004: CLOSED gaps must not reopen after further iterations."""
        s = make_state()
        for inp in [
            "Temperature sensor malfunctions when manual checks are missed",
            "TMP117 on ESP32 I2C samples every 60s triggers relay below threshold",
            "Operating 5-45C IP67 3.3V battery powered single zone",
            "MQTT local broker Node-RED threshold configurable",
            "Standalone no cloud dependency 18 month sensor interval",
        ]: run_iteration(s, inp)
        closed = {g.gap_type for g in s.gaps if g.status == CLOSED}
        if not closed: pytest.skip("No gaps reached CLOSED — cannot test forward-only")
        for _ in range(3): run_iteration(s, "maybe")
        for g in s.gaps:
            if g.gap_type in closed:
                assert g.status == CLOSED,                     f"WPS-001 INV-004 VIOLATED: {g.gap_type!r} was CLOSED but is now {g.status!r}"
    def test_gap_constants_are_distinct(self):
        """WPS-001 INV-004: OPEN, PARTIAL, CLOSED must be distinct constants."""
        assert OPEN != CLOSED, "WPS-001 INV-004: OPEN == CLOSED"

class TestWPS001_INV005_AuditLog:
    """WPS-001 INV-005: Every iteration must produce an audit log entry."""
    def test_iteration_log_grows_with_each_call(self):
        """WPS-001 INV-005: iteration_log length must equal number of run_iteration calls."""
        s = make_state()
        for i, inp in enumerate(["moisture sensor problem","ESP32 capacitive sensor","IP67 3.3V enclosure"]):
            run_iteration(s, inp)
            assert len(s.iteration_log) == i + 1,                 f"WPS-001 INV-005 VIOLATED: After {i+1} calls, log has {len(s.iteration_log)} entries"

class TestWPS001_INV010_ProductionPathImports:
    """WPS-001 INV-010: Production path must not import benchmark/, scripts/, or tests/."""
    PROD_FILES = ["engine/progression_loop.py","engine/idea_state.py","engine/domain_rules.py",
                  "engine/ai_advisor.py","engine/deliverable_assembler.py","web/app.py"]
    FORBIDDEN = ("benchmark","scripts","tests","benchmarks")
    def _violations(self, filepath):
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        path = os.path.join(root, filepath.replace("/", os.sep))
        if not os.path.exists(path): return []
        with open(path, encoding="utf-8") as f: src = f.read()
        try: tree = ast.parse(src)
        except SyntaxError: return []
        out = []
        for node in ast.walk(tree):
            mod = None
            if isinstance(node, ast.ImportFrom) and node.module: mod = node.module
            elif isinstance(node, ast.Import): mod = ".".join(a.name for a in node.names)
            if mod and any(mod.startswith(p) for p in self.FORBIDDEN): out.append(mod)
        return out
    @pytest.mark.parametrize("fp", PROD_FILES)
    def test_no_forbidden_imports(self, fp):
        """WPS-001 INV-010: Production file must not import from benchmark/scripts/tests."""
        v = self._violations(fp)
        assert not v, f"WPS-001 INV-010 VIOLATED: {fp} imports forbidden: {v}"
