"""T2-G / R2 — the frozen msnl-mechanism-content-v1 holdout: integrity tests.

Pins the pre-registered design exactly (counts, class balance, domain and
language coverage, pairing), the served-question texts, the frozen engine
baseline (VB1) and the independence of the cases from every older pack. These
tests read synthetic material only and send nothing.
"""
import collections
import json
import pathlib
import re

import pytest

from engine.path_n_questions import get_served_question
from tests.test_msnl_llm_eval_harness import h

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


@pytest.fixture(scope="module")
def pack():
    return h._load(h.MECHANISM_PACK_PATH, h.MECHANISM_PACK_SHA256)


def test_the_pack_is_pinned_and_its_budget_matches_its_cases(pack):
    assert pack["pack_id"] == "msnl-mechanism-content-v1"
    assert h._mechanism_pack()["pack_id"] == pack["pack_id"]
    t = pack["thresholds"]
    assert len(pack["cases"]) == pack["design"]["cases"] == 160
    assert t["max_provider_requests"] == t["VS1_runs"] * len(pack["cases"]) == 480


def test_counts_balance_and_coverage_are_exactly_as_registered(pack):
    d, cases = pack["design"], pack["cases"]
    groups = collections.defaultdict(list)
    for case in cases:
        groups[case["group_id"]].append(case)
    assert len(groups) == d["groups"] == 40
    for members in groups.values():
        assert sorted(c["variety"] for c in members) == sorted(h.VARIETIES)
        assert len({(c["category"], c["label"], c["domain"], c["question_id"],
                     c["pair_id"]) for c in members}) == 1
    first = [m[0] for m in groups.values()]
    count = collections.Counter(c["category"] for c in first)
    assert dict(count) == {**d["positive_groups"], **d["negative_groups"]}
    for case in cases:
        assert case["label"] == pack["categories"][case["category"]][0]
    by_domain = collections.Counter((c["domain"], c["label"]) for c in first)
    assert by_domain == {("mechanical", "PRESENT"): 10, ("mechanical", "ABSENT"): 10,
                         ("electronics_electrical", "PRESENT"): 10,
                         ("electronics_electrical", "ABSENT"): 10}
    assert collections.Counter(c["variety"] for c in cases) == \
        {v: 40 for v in h.VARIETIES}
    assert len({c["case_id"] for c in cases}) == 160
    assert len({c["text"] for c in cases}) == 160


def test_every_pair_joins_one_positive_and_one_negative_on_the_same_question(pack):
    pairs = collections.defaultdict(set)
    for case in pack["cases"]:
        pairs[case["pair_id"]].add((case["group_id"], case["label"], case["domain"],
                                    case["question_id"]))
    assert len(pairs) == 20
    for members in pairs.values():
        assert len(members) == 2
        assert {m[1] for m in members} == {"PRESENT", "ABSENT"}
        assert len({(m[2], m[3]) for m in members}) == 1


def test_served_contexts_are_the_canonical_unadjusted_questions(pack):
    scope = pack["scope"]["served_questions"]
    for case in pack["cases"]:
        assert case["question_id"] in scope
        assert case["served_index"] == scope[case["question_id"]]
        served = get_served_question("MECHANISM_COMPLETENESS", case["served_index"],
                                     domain=case["domain"])
        assert served.question_id == case["question_id"]
        expected = served.text if case["variety"] == "en" else served.text_ar
        assert case["served_question"] == expected
        assert case["gap_type"] == "MECHANISM_COMPLETENESS"


def test_the_frozen_engine_baseline_holds(pack):
    assert h.mc_precondition(pack) == []
    for case in pack["cases"]:
        assert set(case["engine_baseline"]) == set(h.PRIORS)


def _older_answer_texts():
    """Every ANSWER text of the older packs (case "text" fields and the S2
    answer maps). Served-question texts are excluded: answers may echo the
    committed question, which is not copying."""
    texts = []
    for name in ("msnl_evaluation_pack_v1.json", "msnl_unknown_probe_v1.json",
                 "msnl_holdout_v1.json", "msnl_responsiveness_v1.json"):
        data = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
        texts += [c["text"] for c in data["cases"] if isinstance(c.get("text"), str)]
    s2 = json.loads((FIXTURES / "s2_run_001_answer_maps.json").read_text(encoding="utf-8"))

    def walk(node):
        if isinstance(node, str):
            texts.append(node)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
    walk(s2["answers"])
    return texts


def _shingles(text, n):
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def test_no_case_is_copied_from_an_older_pack(pack):
    """Post-authoring independence screen, NOT pre-registered (recorded in
    annotation independence_check): no exact match with an older answer text
    and no shared run of 8 or more words with one, after the committed
    question wording is excluded."""
    older = _older_answer_texts()
    older_set = set(older)
    older_runs = set().union(*(_shingles(t, 8) for t in older))
    question_runs = set().union(*(_shingles(c["served_question"], 8)
                                  for c in pack["cases"]))
    for case in pack["cases"]:
        assert case["text"] not in older_set, case["case_id"]
        assert not ((_shingles(case["text"], 8) - question_runs) & older_runs), \
            case["case_id"]
    assert "POST-AUTHORING SCREEN, not pre-registered" in \
        pack["annotation"]["independence_check"]


def test_the_annotation_records_independence_agreement_and_limits(pack):
    a = pack["annotation"]
    for key in ("preregistration_order", "method", "label_agreement",
                "disagreement_resolution", "reworded_for_eligibility",
                "human_native_speaker_review"):
        assert a.get(key), key
    assert "NOT PERFORMED" in a["human_native_speaker_review"]


def test_the_offline_baseline_has_no_product_or_network_side_effect(tmp_path):
    """In a fresh interpreter: computing every case's engine baseline imports
    no web layer, opens no SQLite connection (no record store), creates no
    database file and builds no provider adapter."""
    import os
    import subprocess
    import sys
    db = tmp_path / "must-not-exist.sqlite"
    code = (
        "import importlib.util, sqlite3, sys\n"
        "def boom(*a, **k): raise SystemExit('side effect')\n"
        "sqlite3.connect = boom\n"
        "spec = importlib.util.spec_from_file_location('h', %r)\n"
        "h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)\n"
        "h.OpenAIMsnlAdapter = boom\n"
        "assert h.mc_precondition(h._mechanism_pack()) == []\n"
        "print(sorted(m for m in ('web', 'web.app') if m in sys.modules))\n"
    ) % str(ROOT / "scripts" / "run_msnl_eval.py")
    env = dict(os.environ, INVENTORAI_DB_PATH=str(db))
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                         capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "[]"
    assert not db.exists()
