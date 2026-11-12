"""R2 served-question relevance, preregistration v1.1: the prospective repair
of the authoring protocol (Owner authorization, 2026-11-12).

v1's I2 named an exclusive author input list that omitted the served
question its own author brief requires, and the v1 author message also
carried partner pairs, construction rules and one added steering sentence.
v1.1 changes ONLY prereg_id, status and I2, freezes the complete author
message rendered from the permitted fields, and records v1's authoring as
diagnostic only. Network-free; nothing here authors, labels or runs a case.
"""
import copy
import hashlib
import json
import os

import pytest

from engine.path_n_questions import get_served_question
from tests.test_msnl_llm_eval_harness import h

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORD_DIR = os.path.join(ROOT, "docs", "benchmarks", "evidence",
                          "r2_served_relevance_v1_invalid_authoring")
STEERING = ("The NEW_DETAIL text of each project will also be shown in its partner "
            "project's context, so it must clearly describe its own device.")


@pytest.fixture(scope="module")
def prereg():
    return h.srv_preregistration()


@pytest.fixture(scope="module")
def v1():
    with open(h.SRV_PREREG_V1_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# ==========================================================================
# 1. identities: v1 kept, v1.1 pinned, only I2 changes
# ==========================================================================
def test_v1_is_kept_unchanged_and_v1_1_is_pinned(prereg):
    assert _sha(h.SRV_PREREG_V1_PATH) == h.SRV_PREREG_V1_SHA256 == \
        "020fa7e5d75ad9eeff3da2889f66d3aaa8b7b26239926dd9d7b041ba55f02308"
    assert _sha(h.SRV_PREREG_PATH) == h.SRV_PREREG_SHA256
    assert prereg["prereg_id"] == "r2-served-relevance-v1.1-preregistration"
    assert "supersedes v1 for authoring only" in prereg["status"]
    assert prereg["supersedes"]["preregistration_sha256"] == h.SRV_PREREG_V1_SHA256


def test_every_v1_field_except_id_status_and_i2_is_identical(prereg, v1):
    assert set(prereg) - set(v1) == {"author_protocol", "supersedes"}
    assert set(v1) <= set(prereg)
    changed = {k for k in v1 if prereg[k] != v1[k]}
    assert changed == {"prereg_id", "status", "independence"}
    diff = [i for i, (a, b) in enumerate(zip(prereg["independence"], v1["independence"])) if a != b]
    assert diff == [1] and len(prereg["independence"]) == len(v1["independence"]) == 5
    assert prereg["independence"][1].startswith("I2 ")


def test_candidate_composition_validity_criteria_and_a1_to_a5_are_unchanged(prereg, v1):
    cand = prereg["candidate"]
    assert cand == v1["candidate"]
    assert cand["instructions_sha256"] == \
        "183ae029fd934a739d7e73366ca01e57f055c00e1a060deacafc4a64c4559148"
    assert hashlib.sha256(cand["instructions"].encode("utf-8")).hexdigest() == \
        cand["instructions_sha256"]
    for key in ("composition", "engine", "categories", "label_rules", "validity", "measures",
                "criteria", "invalidity", "run_plan", "author_brief", "projects", "limits"):
        assert prereg[key] == v1[key], key
    assert prereg["criteria"]["a1_to_a5"] == v1["criteria"]["a1_to_a5"]
    assert prereg["criteria"]["thresholds"] == v1["criteria"]["thresholds"]
    assert prereg["engine"]["engine_contract_version"] == h.SRV_ENGINE_CONTRACT_VERSION


def test_the_new_i2_names_exactly_the_permitted_inputs(prereg):
    i2 = prereg["independence"][1]
    for allowed in ("author_brief", "categories (brief and side)", "label_rules",
                    "served questions with their project domains", "neutral output format",
                    "continuation_message", "fresh separate session"):
        assert allowed in i2
    never = " ".join(prereg["author_protocol"]["never_sent"])
    for excluded in ("candidate instructions", "model reply", "composition", "thresholds",
                     "slot labels", "partner-pair", "constructed-case reuse", "coaching"):
        assert excluded in never


# ==========================================================================
# 2. the frozen author message: complete, rendered only from permitted fields
# ==========================================================================
def test_the_author_message_is_frozen_and_is_the_rendering(prereg):
    proto = prereg["author_protocol"]
    assert proto["first_message"] == h.srv_author_message(prereg)
    assert hashlib.sha256(proto["first_message"].encode("utf-8")).hexdigest() == \
        proto["first_message_sha256"]
    assert proto["continuation_message"] == "next"


def test_the_rendering_ignores_every_field_outside_i2(prereg):
    tampered = copy.deepcopy(prereg)
    tampered["candidate"]["instructions"] = "LEAK candidate instructions"
    tampered["composition"] = {"LEAK": "composition"}
    tampered["criteria"]["thresholds"]["C2_overall_min"] = [9, 10]
    tampered["validity"]["P1_min_incumbent_rejected_positives"] = 999
    tampered["measures"] = {"LEAK": "measures"}
    tampered["projects"]["partners"] = {"CH1": "LEAK-PARTNER"}
    tampered["history"] = ["LEAK history"]
    tampered["supersedes"]["reason"] = "LEAK"
    for cat in tampered["categories"].values():
        cat["slot_label"] = {"LEAK": "slot"}
        cat["source"] = "LEAK constructed rule"
    assert h.srv_author_message(tampered) == prereg["author_protocol"]["first_message"]


def test_every_permitted_field_reaches_the_message(prereg):
    message = prereg["author_protocol"]["first_message"]
    for line in prereg["author_brief"] + prereg["label_rules"]:
        assert line in message
    for name, cat in prereg["categories"].items():
        assert "%s [side: %s]: %s" % (name, cat["side"], cat["brief"]) in message
    for pid, q in prereg["author_protocol"]["served_questions"].items():
        assert "%s (%s):" % (pid, q["domain"]) in message
        assert q["en"] in message and q["ar-msa"] in message
    authored = [k for k, c in prereg["categories"].items() if c["source"] == "authored"]
    assert ("one current answer for each of these categories: " + ", ".join(authored) + ".") in message


def test_the_message_carries_no_excluded_content(prereg):
    message = prereg["author_protocol"]["first_message"]
    cand = prereg["candidate"]["instructions"]
    for segment in (cand[:80], cand[-80:], "relevance_quote", "evidence_quote"):
        assert segment not in message
    for token in ("slot_label", "WIDEN", "WITHHOLD", "INCUMBENT", "C1_", "P1_", "2/3", "threshold",
                  "partners", "CH1->", "CH1 -> ", "constructed:", "shown with", "partner project's context",
                  "clearly describe its own device", STEERING):
        assert token not in message, token
    for cat in prereg["categories"].values():
        if cat["source"] != "authored":
            assert cat["source"] not in message
    for opening in prereg["author_protocol"]["opening"] + prereg["author_protocol"]["output_format"]:
        assert "partner" not in opening.lower() and "evaluat" not in opening.lower()


def test_served_questions_match_the_engine_and_the_pinned_arabic_pack(prereg):
    pack = json.load(open(h.MECHANISM_PACK_PATH, encoding="utf-8"))
    arabic = {(c["question_id"], c["served_index"]): c["served_question"]
              for c in pack["cases"] if c["variety"] == "ar-msa"}
    for pid, q in prereg["author_protocol"]["served_questions"].items():
        index = prereg["projects"]["served_index"][pid]
        served = get_served_question("MECHANISM_COMPLETENESS", index,
                                     domain=prereg["projects"]["domains"][pid])
        assert (q["question_id"], q["en"]) == (served.question_id, served.text)
        assert q["ar-msa"] == arabic[(served.question_id, index)]


def _load_tampered(monkeypatch, tmp_path, mutate):
    with open(h.SRV_PREREG_PATH, encoding="utf-8") as fh:
        data = json.load(fh)
    mutate(data)
    raw = (json.dumps(data, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    path = tmp_path / "prereg.json"
    path.write_bytes(raw)
    monkeypatch.setattr(h, "SRV_PREREG_PATH", str(path))
    monkeypatch.setattr(h, "SRV_PREREG_SHA256", hashlib.sha256(raw).hexdigest())
    return h.srv_preregistration


@pytest.mark.parametrize("mutate,message", [
    (lambda d: d["criteria"]["thresholds"].__setitem__("C4_max_fraction", [1, 10]),
     "changes the v1 field criteria"),
    (lambda d: d["validity"].__setitem__("P2_min_categories", 3), "changes the v1 field validity"),
    (lambda d: d["candidate"].__setitem__("instructions", "x"), "changes the v1 field candidate"),
    (lambda d: d["independence"].__setitem__(2, "I3 changed"), "I2 only"),
    (lambda d: d.__setitem__("extra", 1), "adds or drops"),
    (lambda d: d["author_protocol"].__setitem__(
        "first_message", d["author_protocol"]["first_message"] + STEERING + "\n"),
     "not the rendering"),
    (lambda d: d["author_protocol"]["output_format"].append(STEERING), "not the rendering"),
    (lambda d: d["author_protocol"].__setitem__("continuation_message", "next, and be concrete"),
     "fixed neutral"),
    (lambda d: d["author_protocol"]["served_questions"]["CH1"].__setitem__("en", "x"),
     "not the rendering"),
])
def test_the_loader_refuses_any_drift(monkeypatch, tmp_path, mutate, message):
    load = _load_tampered(monkeypatch, tmp_path, mutate)
    with pytest.raises(h.PackError, match=message):
        load()


def test_a_tampered_served_question_rerendered_is_still_refused(monkeypatch, tmp_path):
    def mutate(d):
        d["author_protocol"]["served_questions"]["CH4"]["ar-msa"] = "سؤال آخر"
        d["author_protocol"]["first_message"] = h.srv_author_message(d)
        d["author_protocol"]["first_message_sha256"] = hashlib.sha256(
            d["author_protocol"]["first_message"].encode("utf-8")).hexdigest()
    load = _load_tampered(monkeypatch, tmp_path, mutate)
    with pytest.raises(h.PackError, match="served question differs for CH4"):
        load()


# ==========================================================================
# 3. v1's authoring: preserved as a diagnostic record, excluded from any holdout
# ==========================================================================
def test_the_v1_authoring_record_is_preserved_and_pinned(prereg):
    rec = prereg["supersedes"]["v1_authoring"]
    assert rec["status"].startswith("DIAGNOSTIC ONLY")
    assert sorted(os.listdir(RECORD_DIR)) == sorted(rec["record"])
    for name, digest in rec["record"].items():
        assert _sha(os.path.join(RECORD_DIR, name)) == digest
    assert rec["record"]["author_message_v1.txt"] == \
        "5c0eba74aa40dc006f36c94b5506952e620dd8346066d07a1722ec862098f93a"
    chronology = " ".join(rec["chronology_utc"])
    assert "before the Owner authorized" in chronology and "Owner stop" in chronology


def test_the_v1_author_message_shows_the_recorded_findings(prereg):
    with open(os.path.join(RECORD_DIR, "author_message_v1.txt"), encoding="utf-8") as fh:
        old = fh.read()
    assert STEERING in old and "Partner pairs" in old and "constructed:" in old
    assert STEERING not in prereg["author_protocol"]["first_message"]


def _blocks(name):
    import re
    with open(os.path.join(RECORD_DIR, name), encoding="utf-8") as fh:
        return [json.loads(b) for b in re.findall(r"```json\s*(.*?)```", fh.read(), re.S)]


def test_no_v1_authored_text_can_enter_a_formal_holdout(prereg):
    ch1 = _blocks("author_reply_1_devices_CH1.txt")[1]
    ch3 = _blocks("author_reply_3_CH3.txt")[0]
    reused = {"case_id": "X1", "original_idea": "A new idea.", "preceding_answer": "A new answer.",
              "current_answer": ch1["answers"]["NEW_DETAIL"]["ar-msa"]}
    reused_context = {"case_id": "X2", "original_idea": ch3["original_idea"]["en"],
                      "preceding_answer": "A new answer.", "current_answer": "A new reply."}
    fresh = {"case_id": "X3", "original_idea": "A new idea.", "preceding_answer": "A new answer.",
             "current_answer": "A new reply about a different device."}
    assert h.srv_v1_authoring_overlap(prereg, [reused, reused_context, fresh]) == ["X1", "X2"]


def test_the_record_is_not_a_holdout_fixture_or_evidence_of_a_run():
    fixtures = os.listdir(os.path.join(ROOT, "tests", "fixtures"))
    assert sorted(f for f in fixtures if f.startswith("r2_served_relevance")) == [
        "r2_served_relevance_v1_1_preregistration.json", "r2_served_relevance_v1_preregistration.json"]
    assert not os.path.exists(os.path.join(ROOT, "docs", "benchmarks", "evidence", "r2_served_relevance_v1"))
    assert not os.path.exists(os.path.join(ROOT, "docs", "benchmarks", "evidence", "r2_served_relevance_v1_1"))
