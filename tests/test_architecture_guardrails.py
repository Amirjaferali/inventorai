import ast, inspect, os, sys, uuid
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from engine.domain_rules import (
    infer_domain, classify_domain, DomainClassification, DomainResultKind,
    DomainAmbiguityReason, AmbiguousDomainResultError,
)
from engine.idea_state import IdeaState


class TestGuardrails_Sec9_ClassifierReconciliation:
    """GUARDRAILS §9 (P9-E2-R §4.1): classify_domain() is the richer canonical
    entry; infer_domain() remains the LEGACY wrapper — total over SINGLE/NONE and
    fail-loud over richer kinds. One classifier owner; the frozen str|None signature
    is preserved for currently-reachable inputs and must NOT be silently weakened."""

    def test_classify_domain_is_canonical_richer_entry(self):
        r = classify_domain("a voltage sensor circuit")
        assert isinstance(r, DomainClassification)
        assert r.kind in DomainResultKind

    def test_infer_domain_still_str_or_none_for_reachable_inputs(self):
        # The frozen guardrail signature holds for every currently-reachable input.
        for inp in ["ESP32 soil moisture IoT greenhouse", "completely unrelated", "",
                    "gear and catheter"]:
            r = infer_domain(inp)
            assert r is None or isinstance(r, str)

    def test_infer_domain_fails_loud_on_richer_kinds(self, monkeypatch):
        import engine.domain_rules as drm
        multi = DomainClassification(
            kind=DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
            candidates=("mechanical", "medical_device"),
            reason=DomainAmbiguityReason.MULTI_DOMAIN)
        monkeypatch.setattr(drm, "classify_domain", lambda _t: multi)
        with pytest.raises(AmbiguousDomainResultError):
            drm.infer_domain("x")

    def test_single_classifier_owner(self):
        # infer_domain delegates to classify_domain (no duplicate classifier logic).
        assert "classify_domain" in inspect.getsource(infer_domain)

class TestGuardrails_Sec3_InferDomainSignature:
    """GUARDRAILS §3/§8: infer_domain() signature must remain stable."""
    def test_single_parameter_named_idea_text(self):
        """GUARDRAILS §3: infer_domain() must have exactly one parameter named idea_text."""
        sig = inspect.signature(infer_domain)
        params = list(sig.parameters.keys())
        assert len(params) == 1, f"GUARDRAILS §3 VIOLATED: {len(params)} params: {params}. Must be 1."
        assert params[0] == "idea_text",             f"GUARDRAILS §3 VIOLATED: parameter is {params[0]!r}, must be 'idea_text'."
    def test_returns_str_or_none(self):
        """GUARDRAILS §3: infer_domain() must return str or None."""
        for inp in ["ESP32 soil moisture IoT greenhouse","completely unrelated",""]:
            r = infer_domain(inp)
            assert r is None or isinstance(r, str),                 f"GUARDRAILS §3 VIOLATED: infer_domain({inp!r}) returned {type(r).__name__}"
    def test_deterministic(self):
        """GUARDRAILS §3/§8: infer_domain() must be stateless and deterministic."""
        for inp in ["ESP32 temperature sensor","Hall effect motor","unknown cooking"]:
            assert infer_domain(inp) == infer_domain(inp),                 f"GUARDRAILS §3 VIOLATED: infer_domain({inp!r}) non-deterministic"

class TestGuardrails_Sec4_IdeaStateFieldStability:
    """GUARDRAILS §4: IdeaState core fields must remain stable."""
    REQUIRED = ["idea_id","iteration","maturity_level","domain_signal","direction",
                "known_problem","known_mechanism","gaps","iteration_log"]
    def test_all_core_fields_present(self):
        """GUARDRAILS §4: All 9 confirmed core fields must be present on new IdeaState."""
        s = IdeaState(idea_id=str(uuid.uuid4()))
        missing = [f for f in self.REQUIRED if not hasattr(s, f)]
        assert not missing, f"GUARDRAILS §4 VIOLATED: IdeaState missing core fields: {missing}"
    def test_maturity_level_initialises_zero(self):
        """GUARDRAILS §4: maturity_level must initialise to 0."""
        s = IdeaState(idea_id=str(uuid.uuid4()))
        assert s.maturity_level == 0, f"GUARDRAILS §4 VIOLATED: maturity_level={s.maturity_level}, expected 0"
    def test_gaps_initialises_empty(self):
        """GUARDRAILS §4: gaps must initialise to empty list."""
        s = IdeaState(idea_id=str(uuid.uuid4()))
        assert isinstance(s.gaps, list) and len(s.gaps) == 0,             f"GUARDRAILS §4 VIOLATED: gaps={s.gaps!r}, expected []"
    def test_iteration_log_initialises_empty(self):
        """GUARDRAILS §4: iteration_log must initialise to empty list."""
        s = IdeaState(idea_id=str(uuid.uuid4()))
        assert isinstance(s.iteration_log, list) and len(s.iteration_log) == 0,             f"GUARDRAILS §4 VIOLATED: iteration_log={s.iteration_log!r}, expected []"
    def test_idea_id_preserved(self):
        """GUARDRAILS §4: idea_id must be preserved from construction."""
        tid = "GUARD-TEST-001"
        assert IdeaState(idea_id=tid).idea_id == tid,             f"GUARDRAILS §4 VIOLATED: idea_id not preserved"

class TestGuardrails_Sec1_DomainAgnosticEngine:
    """GUARDRAILS §1: Gate functions must not contain domain name string literals."""
    DOMAINS = ["electronics","iot_electronics","software","mechanical","biomedical","agriculture"]
    FUNCTIONS = ["evaluate_transition","integrate_response","assess_response"]
    def _src(self, fn):
        import engine.progression_loop as pl
        return inspect.getsource(getattr(pl, fn))
    @pytest.mark.parametrize("fn", FUNCTIONS)
    def test_no_domain_literals_in_function(self, fn):
        """GUARDRAILS §1: Engine gate function must not contain domain string literals."""
        src = self._src(fn)
        found = [f'"{d}"' for d in self.DOMAINS if f'"{d}"' in src] +                 [f"\'{d}\'" for d in self.DOMAINS if f"\'{d}\'" in src]
        assert not found,             f"GUARDRAILS §1 VIOLATED: {fn}() contains domain literals: {found}. Engine must be domain-agnostic."
    def test_gap_constants_domain_agnostic(self):
        """GUARDRAILS §2: Gap type constants must not embed domain names."""
        from engine.idea_state import MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY
        for name, val in [("MECHANISM_COMPLETENESS",MECHANISM_COMPLETENESS),
                           ("PHYSICAL_FEASIBILITY",PHYSICAL_FEASIBILITY),
                           ("BOUNDARY_AMBIGUITY",BOUNDARY_AMBIGUITY)]:
            for d in self.DOMAINS:
                assert d.lower() not in str(val).lower(),                     f"GUARDRAILS §2 VIOLATED: {name}={val!r} contains domain {d!r}"

class TestGuardrails_Sec6_AIBoundaryStructural:
    """GUARDRAILS §6/§7: ai_advisor must not be called inside protected gate functions."""
    ENGINE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "engine", "progression_loop.py")
    PROTECTED = {"evaluate_transition","integrate_response","assess_response"}
    def test_protected_functions_no_ai_advisor_by_ast(self):
        """GUARDRAILS §6/§7: AST confirms no ai_advisor import inside protected functions."""
        with open(self.ENGINE_FILE, encoding="utf-8") as f: src = f.read()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or node.name not in self.PROTECTED: continue
            for child in ast.walk(node):
                if isinstance(child, ast.ImportFrom) and child.module and "ai_advisor" in child.module:
                    pytest.fail(f"GUARDRAILS §6 VIOLATED: {node.name}() has ai_advisor import at L{child.lineno}")
                if isinstance(child, ast.Import):
                    for a in child.names:
                        assert "ai_advisor" not in a.name,                             f"GUARDRAILS §6 VIOLATED: {node.name}() imports {a.name!r} at L{child.lineno}"
    def test_no_top_level_ai_advisor_import(self):
        """GUARDRAILS §6/§7: engine.ai_advisor must not be imported at module level in progression_loop.py."""
        with open(self.ENGINE_FILE, encoding="utf-8") as f: src = f.read()
        tree = ast.parse(src)
        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                assert node.module != "engine.ai_advisor",                     f"GUARDRAILS §6 VIOLATED: engine.ai_advisor imported at module level (L{node.lineno})"
