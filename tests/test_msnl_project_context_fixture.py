"""T2-G / R2 — cross-idea facet: the frozen msnl-project-context-v1 pack, integrity tests.

The pack is the PRE-CANDIDATE qualification basis recorded for the R2 cross-idea false-credit
facet (DEFERRED_OBLIGATIONS_REGISTER, T2-G / OD-PDVG-10 row, obligations A1-A5). It holds
synthetic project ideas, answers and blind labels, and the OBSERVED lexical engine baseline.
These tests pin the pre-registered design, the served questions, the reproducibility of the
engine baseline and of the observed measures, and the honesty of the annotation. They read
synthetic material only, send nothing and select, qualify or authorize no method.
"""
import collections
import hashlib
import pathlib

import pytest

from engine.path_n_questions import get_served_question
from engine.idea_state import MECHANISM_COMPLETENESS as MC
from tests.test_msnl_llm_eval_harness import h

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "tests" / "fixtures" / "msnl_project_context_v1.json"
PACK_SHA256 = "aec7ad88c677e8a5fc1bdb7fbb7eb283c5ade738a8769d92a0480bbf86c4449a"

CATEGORIES = ("FAITHFUL_PARAPHRASE", "NEW_DETAIL", "NEGATION_SAME_PROJECT", "EVERYDAY_PARTIAL",
              "OTHER_INVENTION", "OTHER_INVENTION_SHARED_WORDS", "UNDECIDED_SAME_PROJECT",
              "UNKNOWN_SAME_PROJECT", "GENERIC_INSUFFICIENT", "CONTRADICTS_IDEA")


@pytest.fixture(scope="module")
def pack():
    return h._load(str(PACK_PATH), PACK_SHA256)


def test_the_pack_is_pinned_synthetic_and_claims_nothing(pack):
    assert pack["pack_id"] == "msnl-project-context-v1" and pack["status"] == "SYNTHETIC"
    assert hashlib.sha256(PACK_PATH.read_bytes()).hexdigest() == PACK_SHA256
    notice = pack["notice"]
    for phrase in ("PRE-CANDIDATE", "NOT a blind holdout", "selects, qualifies and authorizes nothing",
                   "never the expected answer", "FRESH, independently authored holdout"):
        assert phrase in notice, phrase
    assert "never judged" in pack["target"] and "not engineering validity" in pack["target"]


def test_counts_balance_and_coverage_are_exactly_as_registered(pack):
    d, cases = pack["design"], pack["cases"]
    assert tuple(pack["categories"]) == CATEGORIES
    assert pack["varieties"] == ["en", "ar-msa"]
    assert len(cases) == d["cases"] == 120 and d["groups"] == 60 and d["projects"] == 6
    projects = {p["project_id"]: p for p in pack["projects"]}
    assert [projects[p]["domain"] for p in sorted(projects)] == ["mechanical"] * 3 + ["electronics_electrical"] * 3
    groups = collections.defaultdict(list)
    for c in cases:
        groups[c["group_id"]].append(c["variety"])
    assert all(sorted(v) == ["ar-msa", "en"] for v in groups.values()) and len(groups) == 60
    for p in projects:
        assert [c["category"] for c in cases if c["project_id"] == p and c["variety"] == "en"] == list(CATEGORIES)
    assert len({c["text"] for c in cases}) == 120


def test_every_case_carries_its_slot_label_and_its_project_idea(pack):
    projects = {p["project_id"]: p for p in pack["projects"]}
    for c in pack["cases"]:
        cat = pack["categories"][c["category"]]
        assert (c["relevance"], c["expected_outcome"]) == (cat["relevance"], cat["expected_outcome"])
        assert c["project_idea"] == projects[c["project_id"]]["idea"][c["variety"]]
        assert c["gap_type"] == MC


def test_served_contexts_are_the_committed_questions(pack):
    # the committed Arabic texts, read from the hash-pinned v1 pack
    arabic = {c["question_id"]: c["served_question"]
              for c in h._load(h.MECHANISM_PACK_PATH, h.MECHANISM_PACK_SHA256)["cases"]
              if c["variety"] == "ar-msa"}
    for c in pack["cases"]:
        k = int(c["group_id"].split("-C")[1]) - 1
        assert c["served_index"] == k % 3
        q = get_served_question(MC, c["served_index"], domain=c["domain"])
        assert q.question_id == c["question_id"]
        expected = " ".join(q.text.split()) if c["variety"] == "en" else arabic[c["question_id"]]
        assert c["served_question"] == expected


def test_the_known_cases_are_excluded(pack):
    text = " ".join([c["text"] for c in pack["cases"]] + [p["idea"]["en"] for p in pack["projects"]]).lower()
    for word in ("wheelchair", "bicycle", "bike", "watering", "enclosure"):
        assert word not in text, word
    arabic = " ".join([c["text"] for c in pack["cases"] if c["variety"] == "ar-msa"]
                      + [p["idea"]["ar-msa"] for p in pack["projects"]])
    for word in ("كرسي متحرك", "دراجة", "سقي النبات", "ري النبات"):
        assert word not in arabic, word


def test_the_frozen_engine_baseline_reproduces(pack):
    """The lexical engine is replayed exactly as recorded (offline, unchanged harness)."""
    for c in pack["cases"]:
        got = {p: h.mc_engine_outcome(pack, c, p) for p in h.PRIORS}
        assert all(o["unadjusted"] for o in got.values()), c["case_id"]
        assert c["engine_baseline"] == {p: {"status_after": o["status_after"], "granted": o["granted"]}
                                        for p, o in got.items()}, c["case_id"]


def _share(units, granted):
    units = list(units)
    return [sum(c["engine_baseline"][p]["granted"] == granted for c, p in units), len(units)]


def _measures(pack):
    units = [(c, p) for c in pack["cases"] if not c["label_disputed"] for p in h.PRIORS]
    out = {}
    for name, scoped in [("overall", units)] + [(v, [u for u in units if u[0]["variety"] == v])
                                                for v in pack["varieties"]]:
        out[name] = {
            "M-FC-UNRELATED": _share((u for u in scoped if u[0]["relevance"] == "UNRELATED"), True),
            "M-FC-INSUFFICIENT": _share((u for u in scoped if u[0]["relevance"] == "INSUFFICIENT"), True),
            "M-FC-SAME-PROJECT-NO-MECHANISM": _share((u for u in scoped if u[0]["relevance"] == "RELEVANT"
                                                      and u[0]["expected_outcome"] == "NO_CREDIT"), True),
            "M-FR": _share((u for u in scoped if u[0]["expected_outcome"] == "GRANT_ELIGIBLE"), False),
            "M-FR-NEW-DETAIL": _share((u for u in scoped if u[0]["category"] == "NEW_DETAIL"), False),
            "M-FR-FAITHFUL-PARAPHRASE": _share((u for u in scoped if u[0]["category"] == "FAITHFUL_PARAPHRASE"), False),
            "M-CLARIFY-SILENT-GRANT": _share((u for u in scoped if u[0]["expected_outcome"] == "CLARIFY"), True),
        }
    out["by_project_M-FC-UNRELATED"] = {
        p["project_id"]: _share((u for u in units if u[0]["project_id"] == p["project_id"]
                                 and u[0]["relevance"] == "UNRELATED"), True)
        for p in sorted(pack["projects"], key=lambda p: p["project_id"])}
    out["by_category_granted"] = {name: _share((u for u in units if u[0]["category"] == name), True)
                                  for name in pack["categories"]}
    return out


def test_the_observed_baseline_measures_recompute_exactly(pack):
    """The recorded measures are what the frozen baseline actually shows: observed failures
    are reported as they are, never turned into expectations."""
    assert pack["baseline_observed"]["measures"] == _measures(pack)
    assert "never expected answers" in pack["baseline_observed"]["note"]


def test_disputed_labels_are_flagged_and_excluded_never_relabelled(pack):
    for c in pack["cases"]:
        b = c["blind_label"]
        assert c["label_disputed"] == ((b["relevance"], b["expected_outcome"])
                                       != (c["relevance"], c["expected_outcome"]))
    disputed = [c["case_id"] for c in pack["cases"] if c["label_disputed"]]
    assert ("Disputed: " + (", ".join(disputed) if disputed else "none")) in \
        pack["annotation"]["disagreement_resolution"]


def test_criteria_are_predeclared_for_a_future_candidate_only(pack):
    a = pack["acceptance_criteria"]
    assert set(a) == {"scope", "QC1", "QC2", "QC3", "QP1", "QP2", "QA1", "QX1", "QG1"}
    assert "FRESH holdout" in a["scope"] and "never used to qualify" in a["scope"]


def test_the_annotation_records_independence_order_and_limits(pack):
    a = pack["annotation"]
    for key in ("preregistration_order", "method", "label_agreement", "disagreement_resolution",
                "independence_limits", "human_native_speaker_review", "reworded_for_eligibility"):
        assert a.get(key), key
    assert "NOT PERFORMED" in a["human_native_speaker_review"]
    assert "NOT a blind holdout" in a["independence_limits"]
    assert "same model family" in a["independence_limits"]
    notes = " ".join(a["post_freeze_review_notes"])
    for marker in ("cases, labels, design, measures, criteria and baseline are unchanged",
                   "Design confound", "not a measured inter-annotator reliability",
                   "cannot be verified from the repository", "SAME fresh holdout"):
        assert marker in notes, marker
