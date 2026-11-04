"""G1 held-out v2 — frozen pack identity and pre-registered acceptance criteria (OFFLINE).

File-creation contract:
  Path: scripts/g1_precreation_heldout_v2_preregistration.py
  Purpose: freeze, BEFORE any provider evaluation, the identity of the
    independently authored 24-case held-out pack and the acceptance criteria a
    future, separately authorized run of a frozen candidate prompt is judged by.
    It loads and checks the pack, scores replies with the UNCHANGED v1 scorer and
    applies the decision rule below. It is not a pytest test and never runs in CI.
  Authority: Owner instruction "ادمج واكمل الخطوه التاليه" (2026-11-04), step 2:
    ONE bounded held-out preparation PR. No provider request, run path,
    adapter, credential or manifest for a run exists here.
  Independence (recorded, verifiable in Git):
    * cases and labels: authored blind in a separate session at base 28f5d4f
      (commit 459abb8, inputs db4b88f0...), which saw no v2 candidate prompt,
      development case or model response;
    * labels: adjudicated in another separate, prompt-blind session
      (commit 6e7880c), which changed only H13 and H16;
    * this file: written by the Execution Lead, who authors no candidate prompt
      after having seen the held-out cases.
  Reuse (unchanged): `scripts/run_g1_precreation_semantic_eval.py` — the
    validator, scorer (`score_case`), review items, assessment checks and the
    deterministic baseline; the governed concept ids come from its canonical
    owners. The original 20-case pack, the 16 development cases and campaign 01
    evidence are not touched and are not part of this pack.
  Output contract: `python scripts/g1_precreation_heldout_v2_preregistration.py`
    prints the pack identity, the pre-registration digest and the deterministic
    baseline; nothing is sent.
"""
import hashlib
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts import run_g1_precreation_semantic_eval as ev  # noqa: E402  (unchanged)
from scripts.run_msnl_eval import PackError, _load  # noqa: E402  (unchanged)

PACK_ID = "inventorai-g1-precreation-semantic-heldout-02"
INPUT_PATH = os.path.join(_ROOT, "tests", "fixtures", "g1_precreation_semantic_heldout_v2_inputs.json")
INPUT_SHA256 = "db4b88f007d26bc02e0da49bfa06e3ae481c41ab749de0d13db4ae594dda059d"
REFERENCE_PATH = os.path.join(_ROOT, "tests", "fixtures",
                              "g1_precreation_semantic_heldout_v2_reference.json")
REFERENCE_SHA256 = "9803322931c2dc4f6e990c4b368b73a521a1b5dae3e628babf07d5500a99fa08"
AUTHOR_COMMIT = "459abb871419dcf534a861237d94995511de7c92"
ADJUDICATION_COMMIT = "6e7880c4a719dea32833540acd6e63b7b4449635"
CASE_IDS = tuple("H%02d" % i for i in range(1, 25))
GROUPS = ("A", "B", "C", "D")
GROUP_MEANING = {
    "A": "a previously existing component intentionally incorporated into the finished assembly",
    "B": "an external device or installation context the invention only holds, mounts on, "
         "connects to or is used with",
    "C": "genuine ambiguity about whether the second kind of part exists: clarify first",
    "D": "a clear composition whose open engineering details do not make it ambiguous",
}

CRITERIA = {
    "K1-K6": "Unchanged from v1 pre-registration revision 4 (ungrounded quote, foreign concept "
             "id, an admitted SUGGEST_INTEGRATED outside the allowed set, a forbidden stated "
             "part, a negated span stated, a human-confirmed authority claim). In every case "
             "whose reference names an EXTERNAL_CONTEXT, every stated part is a human K4 context "
             "item. Any critical failure gives NO_GO.",
    "G1": "Effective composition inside the allowed set in at least 22 of 24 cases.",
    "GA": "Within EACH group A, B, C and D, the effective composition is inside the allowed "
          "set in at least 5 of its 6 cases.",
    "G2": "Admitted SUGGEST_INTEGRATED in at least 9 of the 10 cases whose only allowed "
          "outcome is SUGGEST_INTEGRATED.",
    "G3": "Required stated parts found with the right concept in at least 30 of 33 slots.",
    "G4": "Every required negation recorded under negated_or_excluded (3 of 3).",
    "G5": "At least 15 of the 17 expected unknowns judged RECOGNIZED by a human, and at least "
          "one RECOGNIZED in each of the 12 cases with expected unknowns; an abstaining, "
          "failed or rejected reply earns none.",
    "D1": "Admitted-integrated recall strictly above the deterministic baseline's on this "
          "pack, with no K3 failure.",
}
DECISION_RULE = (
    "One separately authorized run binds the candidate prompt's exact frozen identity, this "
    "pack's two hashes, this pre-registration's digest, the code revision and the model; the "
    "candidate prompt must have been frozen without access to this pack, and no prompt or label "
    "may be tuned on it afterwards. Any case not attempted or stopped by a provider error gives "
    "INCOMPLETE. Any critical failure, or a failed G1, GA, G2, G3, G4 or D1, or a G5 that can "
    "no longer pass, gives NO_GO. Otherwise, while any K6, K4 context or G5 human assessment is "
    "NOT_ASSESSED, the verdict is INCOMPLETE_REVIEW. PRELIMINARY_GO requires every review "
    "complete and clear and every criterion met; it permits only proposing a bounded, "
    "attributed, inventor-decided product design for separate authorization. It is not a "
    "production PASS and says nothing about Arabic or dialects.")


# Superseded before any model run (never evaluated): the PR #926 independent
# review found that decide() did not give INCOMPLETE for a provider error and
# that H12's only expected unknown was not stated by the inventor.
SUPERSEDED = ({"preregistration_sha256":
               "d4df1e33c9eefbecec4b7a381fbe2ff1f0de9a3f65f9ae25452ac0a82b7243d5",
               "reference_sha256":
               "6748366706acde0c36d1a9e89a0b01fb33da7257f19c6ee3e44afa5ddad7d31b",
               "evaluated": False},)


def preregistration():
    return {"pack_id": PACK_ID, "input_sha256": INPUT_SHA256, "supersedes": list(SUPERSEDED),
            "reference_sha256": REFERENCE_SHA256, "author_commit": AUTHOR_COMMIT,
            "adjudication_commit": ADJUDICATION_COMMIT, "groups": GROUP_MEANING,
            "criteria": CRITERIA, "decision_rule": DECISION_RULE,
            "scorer": "scripts/run_g1_precreation_semantic_eval.py score_case (revision 4)"}


def preregistration_digest():
    raw = json.dumps(preregistration(), ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_heldout():
    """The pinned pack, checked with the v1 rules plus the held-out shape."""
    inputs = _load(INPUT_PATH, INPUT_SHA256)
    reference = _load(REFERENCE_PATH, REFERENCE_SHA256)
    if (inputs.get("pack_id") != PACK_ID or reference.get("pack_id") != PACK_ID
            or inputs.get("synthetic_only") is not True
            or inputs.get("status") != ev.FROZEN_STATUS
            or reference.get("status") != ev.FROZEN_STATUS):
        raise PackError("held-out pack identity")
    cases, refs = inputs["cases"], reference["cases"]
    if [c["case_id"] for c in cases] != list(CASE_IDS) \
            or [r["case_id"] for r in refs] != list(CASE_IDS):
        raise PackError("held-out case identities")
    concepts = set(ev.subsystem_model.COMPOSITION_DOMAINS)
    text = {}
    for c in cases:
        if set(c) != {"case_id", "language", "synthetic", "idea_text"} or c["synthetic"] is not True \
                or c["language"] not in ev.PACK_LANGUAGES or not c["idea_text"].strip():
            raise PackError("held-out input shape: " + c.get("case_id", "?"))
        text[c["case_id"]] = c["idea_text"].lower()
    for r in refs:
        cid = r["case_id"]
        if r.get("group") not in GROUPS or not isinstance(r.get("category"), str):
            raise PackError("held-out group: " + cid)
        if not r["allowed_composition"] or not set(r["allowed_composition"]) <= set(
                ev.COMPOSITION_OUTCOMES):
            raise PackError("allowed composition: " + cid)
        for p in r["required_parts"]:
            if p["concept"] not in concepts or not all(a in text[cid] for a in p["any_of"]):
                raise PackError("required part: " + cid)
        for n in r["required_negations"]:
            if not all(a in text[cid] for a in n["any_of"]):
                raise PackError("required negation: " + cid)
        for f in r["forbidden_stated_parts"]:
            if f["concept"] not in concepts | {None} or (f["term"] is None and f["concept"] is None) \
                    or set(f) - {"term", "concept", "role"} \
                    or ("role" in f and (f["role"] != ev.EXTERNAL_CONTEXT or not f["term"]
                                         or f["term"] not in text[cid])):
                raise PackError("forbidden part: " + cid)
        for i, u in enumerate(r["expected_unknowns"]):
            if (set(u) != {"unknown_id", "meaning", "screen_stems"}
                    or u["unknown_id"] != "%s-U%d" % (cid, i + 1) or not u["meaning"].strip()
                    or not all(st in text[cid] for st in u["screen_stems"])):
                raise PackError("expected unknown: " + cid)
    if sorted(sum(1 for r in refs if r["group"] == g) for g in GROUPS) != [6, 6, 6, 6]:
        raise PackError("held-out group balance")
    return cases, {r["case_id"]: r for r in refs}


def baseline():
    """Today's deterministic /start behaviour on this pack (exact composed-pair tie only)."""
    cases, refs = load_heldout()
    only_s = [c for c, r in refs.items() if r["allowed_composition"] == [ev.SUGGEST_INTEGRATED]]
    ok, recall = 0, 0
    for case in cases:
        outcome, _c = ev.deterministic_composition(case["idea_text"])
        ok += outcome in refs[case["case_id"]]["allowed_composition"]
        recall += case["case_id"] in only_s and outcome == ev.SUGGEST_INTEGRATED
    return {"composition_ok": ok, "cases": len(cases), "integrated": len(only_s),
            "integrated_recall": recall / len(only_s)}


def decide(scored, refs, baseline_recall, assessment=None):
    """The pre-registered verdict over one complete run's per-case scores."""
    if [s["case_id"] for s in scored] != list(CASE_IDS):
        return {"verdict": "INCOMPLETE"}
    if any(s["status"] == ev.V_ERROR for s in scored):
        # A case stopped by a provider error (no reply) makes the run incomplete;
        # a model's malformed or rejected reply is scored, not excused.
        return {"verdict": "INCOMPLETE",
                "provider_errors": [s["case_id"] for s in scored if s["status"] == ev.V_ERROR]}
    k6, g5_judged, k4_judged = ev._check_assessment(assessment, scored)
    unknowns = {k: g5_judged.get(k, st) for s in scored for k, st in s["unknowns"].items()}
    context = {k: k4_judged.get(k, st) for s in scored for k, st in s["context_review"].items()}
    critical = sorted({k for s in scored for k in s["critical"]}
                      | ({"K6"} if k6["status"] == ev.K6_FAILURE else set())
                      | ({"K4"} if ev.K6_FAILURE in context.values() else set()))
    only_s = [c for c, r in refs.items() if r["allowed_composition"] == [ev.SUGGEST_INTEGRATED]]
    recall = sum(1 for s in scored if s["case_id"] in only_s
                 and s["effective"] == ev.SUGGEST_INTEGRATED)
    by_group = {g: sum(s["composition_ok"] for s in scored if refs[s["case_id"]]["group"] == g)
                for g in GROUPS}
    g = {"G1": sum(s["composition_ok"] for s in scored) >= 22,
         "GA": all(v >= 5 for v in by_group.values()),
         "G2": recall >= 9,
         "G3": sum(s["parts_found"] for s in scored) >= 30,
         "G4": all(s["negations_found"] == s["negations_required"] for s in scored),
         "D1": recall / len(only_s) > baseline_recall and "K3" not in critical}
    recognized = [k for k, st in unknowns.items() if st == ev.G5_RECOGNIZED]
    unassessed = sorted(k for k, st in unknowns.items() if st == ev.G5_NOT_ASSESSED)
    per_case = {r: [k for k in unknowns if k.startswith(r + "-U")] for r in refs}
    g5_possible = (len(recognized) + len(unassessed) >= 15 and all(
        any(unknowns[k] != ev.G5_NOT_RECOGNIZED for k in ks) for ks in per_case.values() if ks))
    g["G5"] = (not unassessed and len(recognized) >= 15 and all(
        any(unknowns[k] == ev.G5_RECOGNIZED for k in ks) for ks in per_case.values() if ks))
    if critical or not all(g[k] for k in ("G1", "GA", "G2", "G3", "G4", "D1")) or not g5_possible:
        verdict = "NO_GO"
    elif k6["status"] == ev.K6_NOT_ASSESSED or unassessed or ev.K6_NOT_ASSESSED in context.values():
        verdict = "INCOMPLETE_REVIEW"
    else:
        verdict = "PRELIMINARY_GO" if g["G5"] else "NO_GO"
    return {"verdict": verdict, "critical": critical, "graded": g, "by_group": by_group,
            "integrated_recall": "%d/%d" % (recall, len(only_s)), "k6": k6["status"],
            "g5": {"recognized": len(recognized), "of": len(unknowns), "not_assessed": unassessed},
            "k4_context_not_assessed": sorted(k for k, v in context.items()
                                              if v == ev.K6_NOT_ASSESSED)}


if __name__ == "__main__":
    try:
        cases, _refs = load_heldout()
        print(json.dumps({"pack_id": PACK_ID, "cases": len(cases),
                          "input_sha256": INPUT_SHA256, "reference_sha256": REFERENCE_SHA256,
                          "preregistration_sha256": preregistration_digest(),
                          "baseline": baseline(), "provider_path": "NONE"}, indent=2))
    except PackError as exc:
        print(json.dumps({"refused": str(exc)}))
        sys.exit(2)
