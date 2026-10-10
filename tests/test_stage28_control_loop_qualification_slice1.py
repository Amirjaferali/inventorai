"""Stage 28 — Bounded Control-Loop Concept Owner — Qualification Slice 1 (registered qualification baseline).

Governed by the Owner-accepted contract
``docs/governance/STAGE28_BOUNDED_CONTROL_LOOP_CONCEPT_OWNER_QUALIFICATION_CONTRACT.md`` and the Owner's
Qualification Slice 1 authorization (pack id ``control_loop``; safety-cue Option (b)).

The slice registers ONE standalone v1.0 pack that is recognized by the Domain Registry but NOT activated and NOT
declared qualified. These pins prove:

* registry / lifecycle — recognized, recognized-not-activated, activation and composition unchanged;
* declared scope — only MECHANISM_COMPLETENESS and BOUNDARY_AMBIGUITY, no PHYSICAL_FEASIBILITY, the binding
  not-covered list, real rule nuances and resolvable provenance;
* classification — control-loop examples recognize the pack, Electronics / Mechanical / negative examples are
  unchanged, ties stay governed and the /start refusal for a recognized-not-activated domain stays truthful;
* non-degradation — a before / after differential over the governed classification corpora changes nothing;
* load-bearing evidence — each check rejects a deliberately broken copy of the pack.
"""

import ast
import copy
import functools
import glob
import json
import os
import re
import shutil
import warnings

import pytest

import engine.domain_rules as domain_rules
from engine import domain_activation
from engine.domain_activation import activated_domains, is_activated, support_state
from engine.domain_registry import RegistryLoadError, load_registry
from engine.domain_rules import classify_domain, get_active_rules, get_domain_question
from engine.safety_signal import has_governed_safety_cue_family
from engine.subsystem_model import COMPOSITION_DOMAINS
from tests.csrf_client import csrf_client
from web.app import SESSION_STORE, _unsupported_domain_message, app
from web.domain_label import is_general_fallback, public_domain_label

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOMAINS = os.path.join(_REPO, "domains")
_PACK_PATH = os.path.join(_DOMAINS, "control_loop", "domain.json")
_PROV_PATH = os.path.join(_DOMAINS, "domain_provenance.json")

CL = "control_loop"
ELEC = "electronics_electrical"
MECH = "mechanical"
MC = "MECHANISM_COMPLETENESS"
BA = "BOUNDARY_AMBIGUITY"
PF = "PHYSICAL_FEASIBILITY"

_SIGNALS = ["setpoint", "set point", "closed loop", "open loop", "control loop", "manipulated variable"]

# Vocabulary owned by Electronics / Mechanical, or too generic: never a control_loop classification signal.
_EXCLUDED_SIGNALS = {
    "microcontroller", "arduino", "esp32", "sensor", "controls", "calculates", "samples", "threshold", "filter",
    "signal", "measures", "detects", "triggers", "activates", "processes", "monitors", "outputs", "actuator",
    "control", "loop", "feedback",
}

_NOT_COVERED = [
    "Real-time scheduling", "Deadlines", "Jitter", "Embedded execution architecture", "Firmware implementation",
    "Discrete state-machine design", "Control-law design", "PID design or tuning", "Stability analysis",
    "Controller tuning", "Actuator saturation or rate calculations", "Software / hardware interface design",
    "Sensor physics", "Filtering", "Signal conditioning", "Electrical characteristics", "Mechanical response",
    "Project-specific control calculations", "Fail-safe or safety determination", "SIL / ASIL",
    "Regulatory compliance", "Controller action or update rate",
]

# Expertise the pack must never claim in what it covers, asks or examines.
_UNSUPPORTED_EXPERTISE = re.compile(
    r"\b(pid|tun(e|ing)|stability|firmware|real[- ]time|deadlines?|jitter|calculat\w*|safety|safe|certif\w*|sil|"
    r"asil|state[- ]machine|filter\w*|signal conditioning|voltage|saturation|compliance|scheduling)\b",
    re.IGNORECASE)

_PRIOR_RECORD_IDS = [
    "electronics_electrical:PR001", "electronics_electrical:PR002", "electronics_electrical:PR003",
    "electronics_electrical:PR004", "electronics_electrical:PR005", "electronics_electrical:PR006",
    "electronics_electrical:PR007",
    # ELECTRICAL-ENERGY-TIME-REFERENCE-01: four additive Electronics records after PR007.
    "electronics_electrical:PR008", "electronics_electrical:PR009", "electronics_electrical:PR010",
    "electronics_electrical:PR011",
    # 28-T1-SENSING-VALUE-THRESHOLD-01: two additive Electronics records after PR011.
    "electronics_electrical:PR012", "electronics_electrical:PR013", "mechanical:PR001", "mechanical:PR002", "mechanical:PR003", "mechanical:PR004",
    "mechanical:PR005", "mechanical:PR006", "mechanical:PR007", "mechanical:PR008", "mechanical:PR009",
    "mechanical:PR010", "mechanical:PR011", "medical_device:PR001", "medical_device:PR002", "software:PR001",
]

_CL_RECORDS = [
    ("control_loop:PR001", "government_reference_publication"),
    ("control_loop:PR002", "source_use_policy"),
    ("control_loop:PR003", "government_reference_publication"),
    ("control_loop:PR004", "source_use_policy"),
    ("control_loop:PR005", "government_reference_publication"),
    ("control_loop:PR006", "source_use_policy"),
    ("control_loop:PR007", "governance_record"),
]

# Governed classification corpora: the files whose idea texts already pin classification / admission behaviour.
_CORPUS_FILES = [
    "tests/test_p9_mech_i4_boundary_corpus.py",
    "tests/test_p9_mech_i3_signal_quality.py",
    "tests/test_cf5_f003_classifier_matching_semantics.py",
    "tests/test_cf5_f004_priority_fallback_extensibility.py",
    "tests/test_cf5_f002_web_admission_multidomain.py",
    "tests/test_domain_gate_entry_ux.py",
]

_CL_EXAMPLES = [
    "A closed loop heater that compares the room temperature with a setpoint and adjusts the manipulated variable",
    "An open loop versus closed loop control loop for keeping water level at a set point",
]


def _pack():
    with open(_PACK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _records():
    with open(_PROV_PATH, encoding="utf-8") as fh:
        return json.load(fh)["records"]


def _registry(domains_dir=_DOMAINS):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return load_registry(domains_dir)


def _outcome(text):
    r = classify_domain(text)
    return r.kind.value, r.selected_domain, tuple(r.candidates or ())


def _scores(text):
    tokens = domain_rules._TOKEN_RE.findall(text.lower())
    return {p: domain_rules._present_signal_count(d, tokens, set(tokens)) for p, d in domain_rules._REGISTRY.items()}


def _scope_problems(pack):
    """Every way ``pack`` departs from the accepted Slice-1 scope; [] when it holds."""
    problems = []
    gaps = [m["gap_type_id"] for m in pack["gap_type_mappings"]]
    if gaps != [MC, BA]:
        problems.append("gap set %r" % gaps)
    if [rn["modifier_value"] for rn in pack["rule_nuances"]] != [MC, BA]:
        problems.append("rule-nuance markers")
    if pack["capability_declaration"]["supported_gap_types"] != [MC, BA]:
        problems.append("supported gap types")
    if PF in json.dumps(pack["gap_type_mappings"]) or PF in json.dumps(pack["rule_nuances"]):
        problems.append("PHYSICAL_FEASIBILITY present")
    for item in pack["classification_signals"]:
        if item["signal"] in _EXCLUDED_SIGNALS:
            problems.append("excluded signal %r" % item["signal"])
    texts = list(pack["coverage_declaration"]["covered_areas"])
    texts += [q["text"] for m in pack["gap_type_mappings"] for q in m["questions"]]
    texts += [rn["description"] for rn in pack["rule_nuances"]]
    texts += pack["capability_declaration"]["supported_analysis_categories"]
    for text in texts:
        m = _UNSUPPORTED_EXPERTISE.search(text)
        if m:
            problems.append("unsupported expertise %r in %r" % (m.group(0), text))
    if pack["coverage_declaration"]["not_covered_areas"] != _NOT_COVERED:
        problems.append("not-covered list")
    return problems


def _pack_refs(pack):
    refs = [s["provenance_ref"] for s in pack["classification_signals"] + pack["substance_signals"]]
    refs += [q["provenance_ref"] for m in pack["gap_type_mappings"] for q in m["questions"]]
    refs += [rn["provenance_ref"] for rn in pack["rule_nuances"]]
    refs.append(pack["capability_declaration"]["provenance_ref"])
    return refs


def _broad_files():
    """Every test module except control-loop ones (whose texts are meant to classify as control_loop)."""
    return sorted(os.path.relpath(p, _REPO) for p in glob.glob(os.path.join(_REPO, "tests", "*.py"))
                  if "control_loop" not in os.path.basename(p))


@functools.lru_cache(maxsize=None)
def _corpus(files=tuple(_CORPUS_FILES)):
    texts = set()
    for rel in files:
        with open(os.path.join(_REPO, rel), encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                s = node.value.strip()
                if len(s.split()) >= 2 and any(c.isalpha() for c in s):
                    texts.add(s)
    for path in sorted(glob.glob(os.path.join(_REPO, "tests", "replay", "cases", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            stack = [json.load(fh).get("input")]
        while stack:
            x = stack.pop()
            if isinstance(x, str) and len(x.split()) >= 2:
                texts.add(x)
            elif isinstance(x, dict):
                stack.extend(x.values())
            elif isinstance(x, list):
                stack.extend(x)
    return sorted(texts)


def _domains_copy(tmp_path, pack=None):
    """A copy of ``domains/`` with the control_loop pack replaced by ``pack`` — or removed, with its provenance
    records, when ``pack`` is None (the pre-Slice-1 registry)."""
    target = os.path.join(str(tmp_path), "domains")
    shutil.copytree(_DOMAINS, target)
    if pack is None:
        shutil.rmtree(os.path.join(target, CL))
        prov_path = os.path.join(target, "domain_provenance.json")
        with open(prov_path, encoding="utf-8") as fh:
            prov = json.load(fh)
        prov["records"] = [r for r in prov["records"] if r["pack_id"] != CL]
        with open(prov_path, "w", encoding="utf-8") as fh:
            json.dump(prov, fh)
    else:
        with open(os.path.join(target, CL, "domain.json"), "w", encoding="utf-8") as fh:
            json.dump(pack, fh)
    return target + os.sep


def _changed_outcomes(monkeypatch, before_registry, after_registry, texts):
    monkeypatch.setattr(domain_rules, "_REGISTRY", before_registry)
    before = {t: _outcome(t) for t in texts}
    monkeypatch.setattr(domain_rules, "_REGISTRY", after_registry)
    after = {t: _outcome(t) for t in texts}
    return [(t, before[t], after[t]) for t in texts if before[t] != after[t]]


# ============================================================ registry / lifecycle

def test_registry_recognizes_control_loop_as_a_standalone_registered_v1_pack():
    registry = _registry()
    assert CL in registry
    pack = registry[CL]
    assert pack["schema_version"] == "1.0"
    assert pack["status"] == "registered"
    assert pack["domain_family_role"] == "standalone"
    assert pack["parent_pack_id"] is None
    assert "authorized_child_domains" not in pack
    assert pack["aliases"] == [CL]
    assert pack["activated_date"] is None


def test_control_loop_is_recognized_but_not_activated():
    assert support_state(CL) == domain_activation.RECOGNIZED_NOT_ACTIVATED
    assert is_activated(CL) is False
    assert activated_domains() == [ELEC, MECH]
    assert domain_activation._ACTIVATED_DOMAINS == frozenset({ELEC, MECH})
    assert COMPOSITION_DOMAINS == (MECH, ELEC)


def test_no_safety_cue_family_no_runtime_label_and_no_path_n_artifact():
    # Owner Option (b): no control-loop safety-cue family in Slice 1.
    assert has_governed_safety_cue_family(CL) is False
    # No Tier-1 public label: a recognized-not-activated domain keeps the neutral fallback.
    assert is_general_fallback(public_domain_label(CL))
    config = os.path.join(_REPO, "docs", "governance", "path_n_content_config")
    assert not glob.glob(os.path.join(config, "control_loop*"))


# ================================================================== declared scope

def test_declared_scope_holds_exactly():
    assert _scope_problems(_pack()) == []


def test_only_the_two_authorized_gap_types_are_active():
    assert get_active_rules(CL) == [MC, BA]
    assert get_domain_question(CL, PF, 0) is None
    assert get_domain_question(CL, MC, 0) == _pack()["gap_type_mappings"][0]["questions"][0]["text"]


def test_questions_are_ordered_and_identified_per_gap():
    for mapping in _pack()["gap_type_mappings"]:
        questions = mapping["questions"]
        assert [q["order"] for q in questions] == list(range(1, len(questions) + 1))
        for q in questions:
            assert q["question_id"] == "%s:%s:Q%d" % (CL, mapping["gap_type_id"], q["order"])


def test_rule_nuances_have_the_qualification_grade_shape():
    for rn in _pack()["rule_nuances"]:
        assert sorted(rn) == ["description", "layer", "modifier_type", "modifier_value", "provenance_ref", "rule_id"]
        assert rn["modifier_type"] == "active_gap_rule_marker"
        assert rn["rule_id"].startswith(CL + ":RN")
        assert rn["description"].startswith("Active gap rule marking the Control-Loop ")
        assert "at concept level only" in rn["description"]


def test_capability_declaration_carries_the_option_b_safety_statement():
    cap = _pack()["capability_declaration"]
    assert cap["supported_gap_types"] == [MC, BA]
    assert cap["unsupported_categories"][0].startswith("Safety determination of any kind is NOT COVERED")
    assert "no governed control-loop safety-cue family exists" in cap["unsupported_categories"][0]
    limitations = " ".join(_pack()["coverage_declaration"]["known_limitations"])
    for needle in ("Concept level only", "No project-specific calculation", "No stability analysis",
                   "No embedded execution", "No safety determination", "controller's action or update rate",
                   "No prediction of physical", "P9-QS qualified with activation blockers; not activated"):
        assert needle in limitations, needle


def test_every_pack_reference_resolves_to_its_own_provenance_record():
    ids = {r["record_id"] for r in _records() if r["pack_id"] == CL}
    refs = _pack_refs(_pack())
    assert refs and set(refs) <= ids


def test_provenance_records_are_pack_scoped_and_bounded():
    records = _records()
    assert [r["record_id"] for r in records if r["pack_id"] != CL] == _PRIOR_RECORD_IDS
    ours = [r for r in records if r["pack_id"] == CL]
    assert [(r["record_id"], r["source_type"]) for r in ours] == _CL_RECORDS
    shape = sorted(next(r for r in records if r["record_id"] == "mechanical:PR010"))
    by_id = {r["record_id"]: r for r in ours}
    for r in ours:
        assert sorted(r) == shape and r["tier"] == 1 and r["cross_domain_usage"] == []
    doe, nasa, nist = by_id["control_loop:PR001"], by_id["control_loop:PR003"], by_id["control_loop:PR005"]
    assert "pages 4-6" in doe["version_or_edition"] and "pages 7-10" in doe["version_or_edition"]
    assert "archived" in doe["version_or_edition"] and "control_loop:PR002" in doe["notes"]
    assert "section 1.2.2" in nasa["version_or_edition"] and "printed page 1-3" in nasa["version_or_edition"]
    assert "PDF page 16" in nasa["version_or_edition"]
    assert "Work of the US Gov. Public Use Permitted" in nasa["version_or_edition"]
    assert "control_loop:PR004" in nasa["notes"]
    assert "section 8.1 (page 23)" in nist["version_or_edition"] and "control_loop:PR006" in nist["notes"]
    for policy, source in (("PR002", "PR001"), ("PR004", "PR003"), ("PR006", "PR005")):
        assert ("control_loop:" + source) in by_id["control_loop:" + policy]["notes"]


# ================================================================== classification

def test_classification_signals_are_the_minimal_control_loop_set():
    pack = _pack()
    assert [s["signal"] for s in pack["classification_signals"]] == _SIGNALS
    others = _registry()
    for pack_id in (ELEC, MECH):
        theirs = {s["signal"] for s in others[pack_id]["classification_signals"]}
        theirs |= {s["signal"] for s in others[pack_id]["substance_signals"]}
        assert not theirs & set(_SIGNALS)


@pytest.mark.parametrize("text", _CL_EXAMPLES)
def test_control_loop_examples_recognize_the_pack(text):
    assert _outcome(text) == ("single", CL, ())


@pytest.mark.parametrize("text, expected", [
    ("ESP32 microcontroller circuit with a voltage sensor", ELEC),
    ("A thermistor in a voltage divider feeds a comparator with hysteresis; the comparator output drives a "
     "transistor that energises the relay coil, and the relay contacts open the heater supply line when the "
     "measured temperature passes the set point, closing again once it falls below the lower threshold.", ELEC),
    ("A gear and pulley hoist with a crankshaft drive", MECH),
    ("A spring loaded bracket reaches its setpoint", MECH),
])
def test_electronics_and_mechanical_examples_are_unchanged(text, expected):
    assert _outcome(text) == ("single", expected, ())


@pytest.mark.parametrize("text", [
    "A customer feedback loop for my bakery",
    "A remote control toy car",
    "A loop of rope that holds a bundle",
    "the controls monitor and adjust the output",
    "something with no recognizable signals at all",
])
def test_negative_examples_are_not_captured(text):
    assert _outcome(text)[1] != CL
    assert _scores(text)[CL] == 0


def test_ties_stay_governed():
    # Equal score with an ACTIVATED domain: the activated domain wins (D3-D), never control_loop.
    text = "A sensor reports when the setpoint is reached"
    scores = _scores(text)
    assert scores[CL] == scores[ELEC] == 1
    assert _outcome(text) == ("single", ELEC, ())
    # Equal score with only a non-activated, non-legacy domain: fail closed with the complete candidate set.
    text = "A setpoint algorithm"
    assert _scores(text)[CL] == _scores(text)["software"] == 1
    assert _outcome(text) == ("unresolved_non_activated_tie", None, (CL, "software"))


def test_recognized_not_activated_refusal_stays_truthful():
    client = csrf_client(app)
    before = set(SESSION_STORE)
    for confirm in (None, ELEC, MECH, CL):
        data = {"idea": _CL_EXAMPLES[0]}
        if confirm is not None:
            data["domain_confirm"] = confirm
        resp = client.post("/start", data=data, follow_redirects=False)
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert _unsupported_domain_message(activated_domains()) in body
        assert "Control Loop" not in body          # the recognized domain is never offered or named
    assert set(SESSION_STORE) == before


# ===================================================================== non-degradation

def test_governed_classification_corpora_are_unchanged_by_registration(monkeypatch, tmp_path):
    texts = _corpus()
    assert len(texts) >= 250
    before = _registry(_domains_copy(tmp_path))
    assert CL not in before
    changed = _changed_outcomes(monkeypatch, before, _registry(), texts)
    assert changed == []


def test_the_whole_test_suite_vocabulary_is_unchanged_by_registration(monkeypatch, tmp_path):
    """Broad sweep: every string literal in the test suite (control-loop modules excluded) plus the replay-case
    inputs keeps its classification outcome."""
    texts = _corpus(tuple(_broad_files()))
    assert len(texts) >= 5000
    before = _registry(_domains_copy(tmp_path))
    changed = _changed_outcomes(monkeypatch, before, _registry(), texts)
    assert changed == []


def test_the_differential_detects_a_real_change(monkeypatch, tmp_path):
    before = _registry(_domains_copy(tmp_path))
    changed = _changed_outcomes(monkeypatch, before, _registry(), _CL_EXAMPLES)
    assert [t for t, _, _ in changed] == _CL_EXAMPLES
    assert all(after == ("single", CL, ()) for _, _, after in changed)


# ===================================================================== load-bearing probes

def test_generic_signals_would_change_the_test_suite_vocabulary(monkeypatch, tmp_path):
    bad = _pack()
    bad["classification_signals"] = [{"signal": s, "provenance_ref": "control_loop:PR001"}
                                     for s in ("control", "loop", "feedback")]
    before = _registry(_domains_copy(tmp_path / "before"))
    after = _registry(_domains_copy(tmp_path / "after", bad))
    assert _changed_outcomes(monkeypatch, before, after, _corpus(tuple(_broad_files())))
    assert _scope_problems(bad)


@pytest.mark.parametrize("mutate", [
    lambda p: p["gap_type_mappings"].append({"gap_type_id": PF, "questions": [{"text": "Will it work?"}]}),
    lambda p: p["rule_nuances"].append(dict(p["rule_nuances"][0], modifier_value=PF)),
    lambda p: p["capability_declaration"]["supported_gap_types"].append(PF),
    lambda p: p["classification_signals"].append({"signal": "sensor"}),
    lambda p: p["coverage_declaration"]["not_covered_areas"].remove("Stability analysis"),
    lambda p: p["coverage_declaration"]["covered_areas"].append("Concept-level PID tuning guidance"),
    lambda p: p["gap_type_mappings"][0]["questions"].append({"text": "What firmware runs the loop?"}),
], ids=["pf-gap", "pf-nuance", "pf-supported", "excluded-signal", "dropped-exclusion", "covered-pid",
        "firmware-question"])
def test_scope_check_rejects_each_widening(mutate):
    pack = copy.deepcopy(_pack())
    mutate(pack)
    assert _scope_problems(pack)


def test_registry_refuses_the_pack_without_its_provenance(tmp_path):
    target = _domains_copy(tmp_path)
    shutil.copytree(os.path.join(_DOMAINS, CL), os.path.join(target, CL))
    with pytest.raises(RegistryLoadError):
        _registry(target)
