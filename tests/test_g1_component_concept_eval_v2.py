"""G1-1/2 PROSPECTIVE evidence-traced assessment method (v2) — network-free guards.

The four replies (Q07, Q10, Q12, Q13) come unchanged from the one executed run and are
EXPOSED: they are diagnostic fixtures only — never held-out evidence, a qualification, a
revised verdict for the original run, engineering validation or progression credit. The
diagnostic assessment in the fixture is an AGENT's and is labelled so; it is not human
attestation. The v1 method of that run is pinned unchanged here.
"""
import ast
import copy
import hashlib
import json
import socket
import subprocess
from pathlib import Path

import pytest

from scripts import run_g1_component_concept_eval as cc
from tests.test_g1_component_concept_eval import _oracle, _varieties

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "g1_component_concept_v2_diagnostic.json")
                     .read_text(encoding="utf-8"))
RUN_COMMIT = "2f6925bd2232d3c4bda7fb3119dacd897d3bc3dc"
V2_PREREGISTRATION_SHA256 = "549e5368d9d5efdf3695abf3d4a585b0d11fcd955d1fbb1b8a0a8278da1f05b2"
# sha256 of each v1 definition's source at the PR base 44cfdbc (byte-identical v1 method)
V1_SOURCES = {
    "schema": "3d4e8c0a40c0751ea7a70a1a2e637b5485ef84fac63b55bf8bf93348e931737a",
    "payload": "56197cb0fa70cbbf6637778e7cb3650f469f5f92fd1290b31ce8ef4c8829838a",
    "_structure_ok": "691634e317441676dc1a84eb3c6bcbcb385ab2cfb44e5f52f6c1ff0716808aa8",
    "validate": "dc480fc60fbb92e6fd920488dea52ac7e6a29201941909e0845808f0940ef2c2",
    "preregistration": "376ff61e4ed71e5db312de6c3aed3cae917c848162d2eaad3834a10d51b14c3b",
    "score_case": "cf01b5443e75743885fcf943ee8c3de7afcb85834185a2ddde501ad99883416a",
    "review_items": "ec47a4d09c23203f4d274fffb0e505288eb5b0b653cc35e39d9fdb5e8254d999",
    "check_assessment": "1e03d9c7ca179aae43706631eb634b637c9fe66fa7ddab06a665551d3ed31776",
    "decide": "59a36fff8f7fc1b8cc4a5df9888a30ed2298f2b38d978b8d2eac6d907983f4d1",
}


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("network attempted")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)


@pytest.fixture(scope="module")
def pack():
    return cc.load_pack()


def _canon(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True)
                          .encode("utf-8")).hexdigest()


def _journal_bytes():
    if subprocess.run(["git", "cat-file", "-e", RUN_COMMIT + "^{commit}"], cwd=ROOT,
                      capture_output=True).returncode != 0:
        pytest.fail("the preserved run evidence %s is not available in this checkout" % RUN_COMMIT)
    return subprocess.run(["git", "show", "%s:%s" % (RUN_COMMIT, FIXTURE["source"]["journal"])],
                          cwd=ROOT, capture_output=True, check=True).stdout


def _diag(pack, replies=None, judgments=None, mode=cc.MODE_DIAGNOSTIC, assessor=None,
          annotations=None, attestation=None, attested_on=None):
    """Validate a v2 record over the four diagnostic cases (scored with the v1 scorer)."""
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    replies = replies or FIXTURE["replies"]
    scored = [cc.score_case(replies[cid], by_id[cid], refs[cid]) for cid in sorted(replies)]
    record = {"evaluation_id": cc.EVALUATION_ID_V2,
              "method": [cc.METHOD_V2_ID, cc.METHOD_V2_VERSION], "report_sha256": "r" * 64,
              "mode": mode, "assessor": assessor or FIXTURE["assessment"]["assessor"],
              "attestation": attestation, "attested_on": attested_on,
              "judgments": judgments if judgments is not None
              else copy.deepcopy(FIXTURE["assessment"]["judgments"])}
    labels = cc.check_assessment_v2(record, scored, replies, refs,
                                    annotations or FIXTURE["annotations"], "r" * 64,
                                    [by_id[c]["variety"] for c in replies])
    return scored, labels


def _findings(pack, scored, labels, cid):
    _cases, refs = pack
    s = next(x for x in scored if x["case_id"] == cid)
    return cc.case_findings_v2(s, refs[cid], FIXTURE["annotations"]["cases"].get(cid), labels)


def _judgment(label, evidence, why="x", **kw):
    return dict({"judgment": label, "evidence": evidence, "rationale": why}, **kw)


def _ev(reply, *pointers):
    return [{"pointer": p, "quote": cc.resolve_pointer(reply, p)} for p in pointers]


# ── 1. the original v1 evaluation is immutable ──────────────────────────────
def test_v1_definitions_and_preregistration_are_byte_identical():
    src = (ROOT / "scripts" / "run_g1_component_concept_eval.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    found = {n.name: hashlib.sha256(ast.get_source_segment(src, n).encode()).hexdigest()
             for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in V1_SOURCES}
    assert found == V1_SOURCES
    assert cc.preregistration_digest() == cc.V1_PREREGISTRATION_SHA256
    assert cc.EVALUATION_ID == "g1-component-concept-qualification-01"
    assert cc.preregistration_v2()["v1_preregistration_sha256"] == cc.preregistration_digest()


def test_the_executed_run_still_computes_incomplete_review_under_v1(pack):
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    replies = {}
    for line in _journal_bytes().decode("utf-8").splitlines():
        e = json.loads(line)
        if e.get("event") == "attempt":
            replies[e["case_id"]] = e["reply"]
    assert sorted(replies) == list(cc.CASE_IDS)
    scored = [cc.score_case(replies[c], by_id[c], refs[c]) for c in cc.CASE_IDS]
    d = cc.decide(scored, refs, {})
    assert d["verdict"] == "INCOMPLETE_REVIEW" and not d["critical"]
    assert len(d["not_assessed"]) == 95


def test_the_diagnostic_replies_are_the_preserved_outputs_unchanged():
    raw = _journal_bytes()
    assert hashlib.sha256(raw).hexdigest() == FIXTURE["source"]["journal_sha256"]
    journal = {json.loads(l)["case_id"]: json.loads(l)["reply"] for l in raw.decode().splitlines()
               if json.loads(l).get("event") == "attempt"}
    for cid, reply in FIXTURE["replies"].items():
        assert reply == journal[cid]
        assert _canon(reply) == FIXTURE["source"]["reply_sha256"][cid]
    assert FIXTURE["annotations"]["declared_before_outputs"] is False   # post-exposure: diagnostic


def test_v2_identity_and_preregistration_are_versioned_and_pinned():
    pre = cc.preregistration_v2()
    assert cc.preregistration_v2_digest() == V2_PREREGISTRATION_SHA256
    assert (pre["evaluation_id"], pre["method_version"]) == ("g1-component-concept-qualification-02",
                                                             "2.0")
    assert pre["attestation_formal"] == cc.ATTESTATION            # the formal basis is unchanged
    assert "unchanged" in pre["criteria"]["G1"] and "80%" in pre["criteria"]["G1"]


# ── 2. Q07: matching by meaning, outdoor credit, central outcome ────────────
def test_q07_detection_communication_and_notification_match_by_meaning(pack):
    scored, labels = _diag(pack)
    f = _findings(pack, scored, labels, "Q07")
    assert {k: v["credited"] for k, v in f["functions"].items()} == {
        "Q07-F1": True, "Q07-F2": True, "Q07-F3": True, "Q07-F4": False}
    assert f["functions"]["Q07-F4"]["label"] == "ACKNOWLEDGED_ONLY"
    assert f["central"] == "REPRESENTED" and f["choice"] == cc.G4_COVERED
    # the reply's local ids are permuted against the reference: meaning, not ids, decided
    reply = FIXTURE["replies"]["Q07"]
    assert reply["functions"][0]["id"] == "F1" and "Notify" in reply["functions"][0]["text"]
    ev = FIXTURE["assessment"]["judgments"]["Q07-F3"]["evidence"]
    assert ev[0]["pointer"] == "functions[0]"                       # reference F3 <- reply F1


@pytest.mark.parametrize("pointers", [
    ("component_types[4]",),                                         # "Power source"
    ("functions[3]", "component_types[4]"),                          # "Supply power ..."
    ("missing_information[1]",),                                     # general "conditions"
])
def test_outdoor_operation_is_not_credited_from_power_or_general_conditions(pack, pointers):
    reply = FIXTURE["replies"]["Q07"]
    judged = copy.deepcopy(FIXTURE["assessment"]["judgments"])
    for label in ("ADDRESSED", "OPEN_DECISION_DISCLOSED"):
        judged["Q07-F4"] = _judgment(label, _ev(reply, *pointers))
        with pytest.raises(cc.PackError, match="operating-context"):
            _diag(pack, judgments=judged)


def _with_weather_role(reply):
    r = copy.deepcopy(reply)
    r["functions"].append({"id": "F5", "origin": "AI_PROPOSED", "resolution": "UNRESOLVED",
                           "source_quote": "",
                           "text": "Protect the mailbox-side parts from rain and outdoor temperature."})
    r["component_types"].append({"attribution": "AI_PROPOSED", "id": "C6", "serves": ["F5"],
                                 "status": "UNVERIFIED", "type": "Weather-resistant housing"})
    return r


def test_a_represented_outdoor_exposure_may_be_credited_without_any_rating(pack):
    replies = dict(FIXTURE["replies"], Q07=_with_weather_role(FIXTURE["replies"]["Q07"]))
    judged = copy.deepcopy(FIXTURE["assessment"]["judgments"])
    judged["Q07-F4"] = _judgment("ADDRESSED", _ev(replies["Q07"], "functions[4]",
                                                  "component_types[5]"))
    scored, labels = _diag(pack, replies=replies, judgments=judged)
    assert _findings(pack, scored, labels, "Q07")["functions"]["Q07-F4"]["credited"]


def _without_notification(reply):
    r = copy.deepcopy(reply)
    r["functions"] = [f for f in r["functions"] if f["id"] != "F1"]
    r["component_types"] = [c for c in r["component_types"] if c["id"] != "C4"]
    r["relationships"] = [x for x in r["relationships"] if "C4" not in (x["from"], x["to"])]
    r["alternatives"] = [a for a in r["alternatives"] if a["for_function"] != "F1"]
    r["stated"] = [s for s in r["stated"] if s["kind"] != "FUNCTION"]
    return r


def test_removing_the_central_notification_fails_whatever_the_coverage_ratio(pack):
    r = _with_weather_role(_without_notification(FIXTURE["replies"]["Q07"]))
    replies = dict(FIXTURE["replies"], Q07=r)
    assert not any(c["type"] == "Notification indicator" for c in r["component_types"])
    assert not any(f["text"].startswith("Notify") for f in r["functions"])
    judged = copy.deepcopy(FIXTURE["assessment"]["judgments"])
    judged["Q07-F1"] = _judgment("ADDRESSED", _ev(r, "functions[0]", "component_types[0]"))
    judged["Q07-F2"] = _judgment("ADDRESSED", _ev(r, "functions[1]", "component_types[2]"))
    judged["Q07-F3"] = _judgment("MISSING", [], "Nothing indicates new mail to the inventor.")
    judged["Q07-F4"] = _judgment("ADDRESSED", _ev(r, "functions[3]", "component_types[4]"))
    judged["Q07:G4"] = _judgment(
        cc.G4_COVERED, _ev(r, "alternatives[0].options[0]", "alternatives[0].options[1]"),
        option_map={"A": "alternatives[0].options[1]", "B": "alternatives[0].options[0]"})
    scored, labels = _diag(pack, replies=replies, judgments=judged)
    f = _findings(pack, scored, labels, "Q07")
    assert sum(v["credited"] for v in f["functions"].values()) == 3   # 3/4 >= two-thirds ...
    assert f["central"] == "OMITTED"                                  # ... but the goal is gone


# ── 3. Q12 unknowns, Q10 / Q13 alternatives ─────────────────────────────────
def test_q12_food_capacity_is_not_credited_from_unrelated_evidence(pack):
    scored, labels = _diag(pack)
    f = _findings(pack, scored, labels, "Q12")
    assert {k: v["credited"] for k, v in f["unknowns"].items()} == {
        "Q12-U1": True, "Q12-U2": True, "Q12-U3": False}
    reply = FIXTURE["replies"]["Q12"]
    for pointers in (("missing_information[0]",), ("missing_information[0]",
                                                   "missing_information[1]"),
                     ("clarification_questions[0]",)):
        judged = copy.deepcopy(FIXTURE["assessment"]["judgments"])
        judged["Q12-U3"] = _judgment("RECOGNIZED", _ev(reply, *pointers))
        with pytest.raises(cc.PackError, match="does not name this unknown"):
            _diag(pack, judgments=judged)
    judged = copy.deepcopy(FIXTURE["assessment"]["judgments"])
    judged["Q12-U3"] = _judgment("RECOGNIZED", _ev(reply, "functions[1]"))   # a function, not an unknown
    with pytest.raises(cc.PackError, match="wrong place"):
        _diag(pack, judgments=judged)


def test_q10_and_q13_alternatives_are_classified_under_the_exact_criterion(pack):
    scored, labels = _diag(pack)
    q10, q13 = (_findings(pack, scored, labels, c) for c in ("Q10", "Q13"))
    assert q10["choice"] == cc.G4_PARTIAL and q13["choice"] == cc.G4_OTHER_VALID
    for label in (cc.G4_PARTIAL, cc.G4_OTHER_VALID):
        assert not cc._credited("G4", label)                       # no reference-coverage credit
    # a different valid alternative is reported as legitimate, not as a critical failure
    assert not any(s["critical"] for s in scored)
    reply10 = FIXTURE["replies"]["Q10"]
    judged = copy.deepcopy(FIXTURE["assessment"]["judgments"])
    judged["Q10:G4"] = _judgment(cc.G4_COVERED, _ev(reply10, "alternatives[0].options[0]"),
                                 option_map={"A": "alternatives[0].options[0]"})
    with pytest.raises(cc.PackError, match="COVERED maps both"):
        _diag(pack, judgments=judged)
    judged["Q10:G4"] = _judgment(cc.G4_PARTIAL, [], option_map={"A": "alternatives[0].options[0]"})
    with pytest.raises(cc.PackError, match="needs reply evidence"):
        _diag(pack, judgments=judged)


# ── 4. ids, pointers and semantic validity ──────────────────────────────────
def _renamed(reply):
    ren = {"F1": "F7", "F2": "F5", "F3": "F9", "F4": "F2", "C1": "C8", "C2": "C3", "C3": "C1",
           "C4": "C9", "C5": "C4"}
    r = copy.deepcopy(reply)
    for f in r["functions"]:
        f["id"] = ren[f["id"]]
    for c in r["component_types"]:
        c["id"] = ren[c["id"]]
        c["serves"] = [ren[x] for x in c["serves"]]
    for x in r["relationships"]:
        x["from"], x["to"] = ren[x["from"]], ren[x["to"]]
    for a in r["alternatives"]:
        a["for_function"] = ren[a["for_function"]]
    return r


def _reordered(reply):
    r = copy.deepcopy(reply)
    for key in ("functions", "component_types", "relationships", "missing_information"):
        r[key] = list(reversed(r[key]))
    return r


def _repoint(judgments, old, new):
    """Move every pointer to the same text in the reordered reply (what a reviewer does)."""
    def where(quote, section):
        for i in range(len(new.get(section, []))):
            p = "%s[%d]" % (section, i)
            if section != "alternatives" and cc.resolve_pointer(new, p) == quote:
                return p
        raise AssertionError("quote not found")
    out = copy.deepcopy(judgments)
    for item_id, j in out.items():
        if not item_id.startswith("Q07"):
            continue
        for e in j["evidence"]:
            if not e["pointer"].startswith("alternatives"):
                e["pointer"] = where(e["quote"], e["pointer"].split("[")[0])
    return out


def test_renamed_or_reordered_local_ids_do_not_change_the_mapping(pack):
    scored, labels = _diag(pack)
    base = _findings(pack, scored, labels, "Q07")
    renamed = dict(FIXTURE["replies"], Q07=_renamed(FIXTURE["replies"]["Q07"]))
    s2, l2 = _diag(pack, replies=renamed)                        # quotes carry no local ids
    assert _findings(pack, s2, l2, "Q07") == base
    reordered = dict(FIXTURE["replies"], Q07=_reordered(FIXTURE["replies"]["Q07"]))
    with pytest.raises(cc.PackError, match="quotation does not match"):
        _diag(pack, replies=reordered)                            # stale pointers never mis-credit
    judged = _repoint(FIXTURE["assessment"]["judgments"], FIXTURE["replies"]["Q07"],
                      reordered["Q07"])
    s3, l3 = _diag(pack, replies=reordered, judgments=judged)
    assert _findings(pack, s3, l3, "Q07") == base


def test_valid_pointers_never_imply_semantic_correctness(pack):
    reply = FIXTURE["replies"]["Q07"]
    judged = copy.deepcopy(FIXTURE["assessment"]["judgments"])
    # structurally valid but semantically wrong evidence (the indicator is not transmission)
    judged["Q07-F2"] = _judgment("ADDRESSED", _ev(reply, "component_types[3]"), "wrong on purpose")
    scored, labels = _diag(pack, judgments=judged)
    assert labels["Q07-F2"] == "ADDRESSED"                       # accepted as the assessor's claim
    assert "never established by the pointer check" in cc.SEMANTIC_BASIS
    assert "not that it satisfies the reference item" in cc.POINTER_RULE
    bad = copy.deepcopy(FIXTURE["assessment"]["judgments"])
    bad["Q07-F1"]["evidence"][0]["quote"] += " (edited)"
    with pytest.raises(cc.PackError, match="quotation does not match"):
        _diag(pack, judgments=bad)
    for pointer in ("functions[99]", "alternatives[0]", "functions[0].options[0]", "x[0]"):
        bad = copy.deepcopy(FIXTURE["assessment"]["judgments"])
        bad["Q07-F1"]["evidence"] = [{"pointer": pointer, "quote": "x"}]
        with pytest.raises(cc.PackError):
            _diag(pack, judgments=bad)


# ── 5. modes, reviewer basis, central rule, unresolved judgments ────────────
def test_diagnostic_and_formal_modes_stay_apart(pack):
    human = {"kind": "HUMAN", "name": "Reviewer", "languages": ["en", "ar-egyptian"]}
    with pytest.raises(cc.PackError, match="FORMAL needs a HUMAN"):
        _diag(pack, mode=cc.MODE_FORMAL, attestation=cc.ATTESTATION, attested_on="2026-11-06")
    with pytest.raises(cc.PackError, match="FORMAL needs a HUMAN"):
        _diag(pack, mode=cc.MODE_FORMAL, attestation=cc.ATTESTATION, attested_on="2026-11-06",
              assessor=dict(human, kind="AI_ASSISTED_HUMAN"))
    with pytest.raises(cc.PackError, match="declared before any output"):
        _diag(pack, mode=cc.MODE_FORMAL, assessor=human, attestation=cc.ATTESTATION,
              attested_on="2026-11-06")
    with pytest.raises(cc.PackError, match="unchanged v1 attestation"):
        _diag(pack, mode=cc.MODE_FORMAL, assessor=human, attestation="I reviewed it.",
              attested_on="2026-11-06")
    with pytest.raises(cc.PackError, match="claims no attestation"):
        _diag(pack, attestation=cc.ATTESTATION, attested_on="2026-11-06")


def _full_run(pack, replace=None):
    cases, refs = pack
    replies = {c["case_id"]: _oracle(c, refs[c["case_id"]]) for c in cases}
    replies.update(replace or {})
    scored = [cc.score_case(replies[c["case_id"]], c, refs[c["case_id"]]) for c in cases]
    labels = {}
    for s in scored:
        for item_id, kind in s["items"].items():
            labels[item_id] = {"K1": cc.CLEAR, "K2": cc.CLEAR, "K3": cc.CLEAR, "G1": "ADDRESSED",
                               "G2": "COHERENT", "G3": "RECOGNIZED", "G4": cc.G4_COVERED,
                               "G5": "CLARIFIED"}[kind]
    ann = {"declared_before_outputs": True, "provenance": "synthetic test",
           "cases": {cid: {"intent": "AMBIGUOUS" if r["group"] == "AMBIGUOUS" else "CLEAR",
                           "central": [r["essential_functions"][0]["function_id"]]
                           if r["group"] == "POSITIVE" else [],
                           "context_needs": {}, "unknown_terms": {}, "choices": []}
                     for cid, r in refs.items()}}
    cc.check_annotations(ann, refs, formal=True)
    return scored, refs, ann, labels


def test_the_central_rule_blocks_credit_but_never_penalises_valid_clarification(pack):
    scored, refs, ann, labels = _full_run(pack)
    assert cc.decide_v2(scored, refs, ann, labels, cc.MODE_FORMAL)["verdict"] == "PRELIMINARY_GO"
    diag = cc.decide_v2(scored, refs, ann, labels, cc.MODE_DIAGNOSTIC)
    assert diag["verdict"] == "DIAGNOSTIC_ONLY" and diag["diagnostic_outcome"] == "PRELIMINARY_GO"
    assert "NOT A QUALIFICATION" in diag["qualification"]
    central = ann["cases"]["Q07"]["central"][0]
    labels_missing = dict(labels, **{central: "MISSING"})
    d = cc.decide_v2(scored, refs, ann, labels_missing, cc.MODE_FORMAL)
    assert d["verdict"] == "NO_GO" and d["central_omitted"] == ["Q07"] and not d["graded"]["G1"]
    # an AMBIGUOUS case that validly asks is judged under G5 and is never a central omission
    for s in scored:
        if s["group"] == "AMBIGUOUS":
            f = cc.case_findings_v2(s, refs[s["case_id"]], ann["cases"][s["case_id"]], labels)
            assert f["central"] == "NOT_APPLICABLE"
    bad = copy.deepcopy(ann)
    bad["cases"]["Q03"]["intent"] = "CLEAR"
    with pytest.raises(cc.PackError, match="intent contradicts"):
        cc.check_annotations(bad, refs)
    bad = copy.deepcopy(ann)
    bad["cases"]["Q07"]["central"] = []
    with pytest.raises(cc.PackError, match="central outcome declared"):
        cc.check_annotations(bad, refs)


def test_insufficient_evidence_and_disputes_earn_nothing(pack):
    scored, refs, ann, labels = _full_run(pack)
    item = "Q07-F1"
    a, b = dict(labels), dict(labels, **{item: "MISSING"})
    merged, positions = cc.reconcile_v2([a, b])
    assert merged[item] == cc.DISPUTED and positions[item] == ["ADDRESSED", "MISSING"]
    d = cc.decide_v2(scored, refs, ann, merged, cc.MODE_FORMAL)
    assert d["verdict"] == "INCOMPLETE_REVIEW" and item in d["unresolved"]
    d = cc.decide_v2(scored, refs, ann, dict(labels, **{item: cc.INSUFFICIENT_EVIDENCE}),
                     cc.MODE_FORMAL)
    assert d["verdict"] == "INCOMPLETE_REVIEW" and not d["graded"]["G1"]
    # a disputed G4 never becomes reference-coverage credit
    assert not cc._credited("G4", cc.DISPUTED) and not cc._credited("G1", cc.DISPUTED)


def test_open_decision_credit_needs_the_reference_permission(pack):
    _cases, refs = pack
    may = {f["function_id"]: f for r in refs.values() for f in r["essential_functions"]}
    assert cc._credited("G1", "OPEN_DECISION_DISCLOSED", may["Q07-F1"])        # may be unresolved
    assert not cc._credited("G1", "OPEN_DECISION_DISCLOSED", may["Q07-F4"])    # may not
    for label in ("ACKNOWLEDGED_ONLY", "MISSING", "INVENTED_DETAIL"):
        assert not cc._credited("G1", label, may["Q07-F1"])


def test_nothing_in_the_product_imports_the_method():
    for top in ("engine", "web"):
        for path in (ROOT / top).rglob("*.py"):
            assert "run_g1_component_concept_eval" not in path.read_text(encoding="utf-8"), path
