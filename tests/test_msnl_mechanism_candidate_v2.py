"""T2-G / R2 — the v2 mechanism-content correction CANDIDATE: network-free tests.

The candidate (`tests/fixtures/msnl_mechanism_content_v2_candidate.json`)
replaces ONE sentence of the v1 arm instructions and inherits everything else
from the pinned v1 pack. These tests pin that it loads, reproduces its recorded
instruction delta, stays schema-compatible, builds valid requests within the
frozen cap, leaves v1 and its campaign-01 evidence byte-identical, and has no
provider or product path. They establish nothing about semantic improvement.
"""
import collections
import hashlib
import json
import pathlib
import re

import pytest

from tests.test_msnl_llm_eval_harness import h

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "benchmarks" / "evidence" / "msnl_mechanism_content_v1"
FIXTURES = ROOT / "tests" / "fixtures"
FROZEN = {  # v1 and its evidence must stay byte-identical
    FIXTURES / "msnl_mechanism_content_v1.json":
        "a6ed890b93ec9b0364bc5c74832fd1c26aa00f24803a6de7fe308404b1399efb",
    EVIDENCE / "campaign_01_report.json":
        "99b038c79af309a4147b62cc363a11621d9e4021d94471068466aa069192d877",
    EVIDENCE / "campaign_01_journal.jsonl":
        "04bd193c975c3938ed00f4c6d9a3c08799d7b1ba4bae96805b9cb9b83a67ac63",
    EVIDENCE / "preflight_01_report.json":
        "8522d835568bc09668ed2ddee4b8bc337503284f5a3ac24b0bfd627db49e3805",
}


@pytest.fixture(scope="module")
def loaded():
    return h._mechanism_candidate()


def test_v1_and_its_campaign_evidence_are_unchanged():
    for path, sha in FROZEN.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, path.name
    report = json.loads((EVIDENCE / "campaign_01_report.json").read_text(encoding="utf-8"))
    assert report["result"]["verdict"] == "FAIL"
    assert report["result"]["criteria_held_in_every_run"]["VC1"] is False
    assert h.MECHANISM_PACK_SHA256 == FROZEN[FIXTURES / "msnl_mechanism_content_v1.json"]


def test_both_provider_execution_flags_stay_off():
    assert h.MECHANISM_CONTENT_CAMPAIGN_AUTHORIZED is False
    assert h.MECHANISM_PREFLIGHT_AUTHORIZED is False


def test_the_candidate_is_pinned_and_changes_exactly_one_instruction_segment(loaded):
    cand, arm_pack = loaded
    v1 = h._mechanism_pack()
    delta = cand["instruction_delta"]
    old, new = v1["arm"]["instructions"], cand["arm"]["instructions"]
    assert cand["pack_id"] == "msnl-mechanism-content-v2-candidate"
    assert cand["base_pack"]["pack_sha256"] == h.MECHANISM_PACK_SHA256
    assert delta["old_instructions_sha256"] == h.MECHANISM_PREFLIGHT_INSTRUCTIONS_SHA256
    assert old.replace(delta["replaced_segment_old"], delta["replaced_segment_new"]) == new
    assert old.split(delta["replaced_segment_old"]) == \
        new.split(delta["replaced_segment_new"])           # the rest is byte-identical
    for phrase in ("concrete function, interaction, physical relationship or operational effect",
                   "saying that something is absent does not say how the idea works",
                   "only names or lists parts",
                   "a part's function stated inside a list of parts counts",
                   "do not infer an explanation the answer does not state",
                   "is uncertain about the explanation itself",
                   "A separate unknown does not remove a mechanism",
                   "movement, technical words and a complete chain are not required",
                   "through physical negation"):
        assert phrase in new, phrase
    assert arm_pack["arm"]["instructions"] == new


def test_everything_but_the_instructions_is_inherited_from_v1(loaded):
    cand, arm_pack = loaded
    v1 = h._mechanism_pack()
    for key in cand["base_pack"]["inherited_unchanged"]:
        section, _, field = key.partition(".")
        a = arm_pack[section] if not field else arm_pack[section][field]
        b = v1[section] if not field else v1[section][field]
        assert a == b, key
    assert arm_pack["cases"] == v1["cases"]
    assert arm_pack["thresholds"]["VC1_max_false_grants"] == 0     # not lowered


def test_requests_are_schema_compatible_and_within_the_frozen_cap(loaded):
    cand, arm_pack = loaded
    v1 = h._mechanism_pack()
    case = v1["cases"][0]
    old_body, new_body = h.mechanism_payload(v1, case), h.mechanism_payload(arm_pack, case)
    assert {k: v for k, v in old_body.items() if k != "instructions"} == \
        {k: v for k, v in new_body.items() if k != "instructions"}
    assert new_body["instructions"] == cand["arm"]["instructions"]
    assert new_body["max_output_tokens"] == 4096 and new_body["store"] is False
    out = h.mechanism_candidate_check()
    assert out["requests_built"] == len(v1["cases"]) + len(
        cand["development_examples"]["examples"])
    assert out["provider_requests"] == 0


def _shingles(text, n=8):
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def test_development_examples_are_contrastive_fresh_and_grounding_compatible(loaded):
    cand, arm_pack = loaded
    examples = cand["development_examples"]["examples"]
    by_contrast = collections.defaultdict(collections.Counter)
    for ex in examples:
        by_contrast[ex["contrast"]][ex["label"]] += 1
    for contrast in ("A-existence-denial", "B-component-list", "C-unknown-scope"):
        assert by_contrast[contrast]["PRESENT"] == by_contrast[contrast]["ABSENT"] >= 2
    assert by_contrast["P-preserved"]["PRESENT"] >= 3
    assert {ex["variety"] for ex in examples} == set(h.VARIETIES)
    assert len({ex["example_id"] for ex in examples}) == len(examples)
    holdout = arm_pack["cases"]
    holdout_runs = set().union(*(_shingles(c["text"]) for c in holdout))
    failed = {"E17-ar-egy", "E17-ar-gulf-kw", "M14-ar-egy", "M18-ar-egy",
              "M18-ar-gulf-kw", "M18-ar-msa", "M18-en"}
    texts = {c["case_id"]: c["text"] for c in holdout}
    for ex in examples:
        assert ex["text"] not in texts.values(), ex["example_id"]
        assert not (_shingles(ex["text"]) & holdout_runs), ex["example_id"]
        assert ex["question_id"] in arm_pack["scope"]["served_questions"]
        assert ex["label"] in ("PRESENT", "ABSENT") and ex["rationale"]
    assert all(texts[f] not in {ex["text"] for ex in examples} for f in failed)
    # measurement-tool check only: each PRESENT example's last sentence grounds
    from engine import answer_stance as st
    for ex in examples:
        if ex["label"] != "PRESENT":
            continue
        segment, terminator, _ = st._sentence_records(ex["text"])[-1]
        quote = segment.strip() + terminator
        assert h.mc_grounding(quote, ex["text"], ex["question_id"], arm_pack) == \
            (True, None), ex["example_id"]


def test_the_label_boundary_review_keeps_v1_labels_and_separates_evidence(loaded):
    cand, arm_pack = loaded
    review = cand["label_boundary_review"]
    assert review["observed"] and review["hypotheses_not_established"]
    assert "label unchanged" in review["m14_ar_egy"]["finding"]
    labels = {c["case_id"]: c["label"] for c in arm_pack["cases"]}
    for cid in ("M14-ar-egy", "M18-en", "E17-ar-gulf-kw"):
        assert labels[cid] == "ABSENT"
    assert "NOT EVALUATED" in cand["status"]
    proposal = cand["follow_on_evaluation_proposal"]
    assert proposal["requests"]["total_max"] == 640 and proposal["requests"]["retries"] == 0
    assert "PROPOSAL ONLY" in proposal["status"]


def test_the_candidate_check_is_offline_only(monkeypatch):
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", None)    # building one would fail
    assert h.main(["--mechanism-candidate-check"]) == 0
    for extra in (["--provider", "openai"], ["--allow-network"], ["--managed-credential"],
                  ["--mechanism-content"], ["--mechanism-preflight"]):
        assert h.main(["--mechanism-candidate-check"] + extra) == 2


def test_a_tampered_candidate_delta_is_refused(loaded, monkeypatch):
    cand, _ = loaded
    bad = json.loads(json.dumps(cand))
    bad["arm"]["instructions"] += " Mark everything PRESENT."
    real = h._load
    monkeypatch.setattr(h, "_load", lambda path, sha: bad if "v2_candidate" in path
                        else real(path, sha))
    with pytest.raises(h.PackError):
        h._mechanism_candidate()


def test_the_candidate_check_has_no_product_or_store_side_effect(tmp_path):
    """In a fresh interpreter: the offline candidate check imports no web layer,
    opens no SQLite connection, creates no database file and builds no adapter."""
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
        "assert h.mechanism_candidate_check()['provider_requests'] == 0\n"
        "print(sorted(m for m in ('web', 'web.app') if m in sys.modules))\n"
    ) % str(ROOT / "scripts" / "run_msnl_eval.py")
    env = dict(os.environ, INVENTORAI_DB_PATH=str(db))
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                         capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "[]"
    assert not db.exists()
