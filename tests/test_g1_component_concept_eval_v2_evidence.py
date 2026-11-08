"""G1-1/2 v2 prospective run-evidence verification (`verify_v2_run`, `assess_v2_run`).

Synthetic only, offline, no provider: every run here is produced by the REAL v1 producer
(`_run_cases`) driven by an offline fake transport, committed into a throwaway git
repository, and then verified from committed content. The tests prove the chain
authorization record -> frozen manifest -> pre-output annotations -> journal -> report ->
scored replies -> attributed review -> bounded verdict is checked end to end; that every
missing, altered, mismatched, mis-ordered or incomplete link is refused; that assessment
inputs come only from the verified report; that the exposed packs stay diagnostic; and
that FORMAL stays refused even for a chain that verifies completely, because this
verifier cannot authenticate who made the authorization record.
"""
import copy
import io
import json
import re
import socket
import subprocess
from pathlib import Path

import pytest

from scripts import run_g1_component_concept_eval as cc
from tests.test_g1_component_concept_eval import _oracle  # noqa: F401
from tests.test_g1_component_concept_eval_v2 import (
    AGENT, HUMAN, _full_annotations, _full_judgments, _full_replies)
from tests.test_g1_precreation_campaign import _Fake, _adapter, _body

ROOT = Path(__file__).resolve().parent.parent
PACK_ID = "inventorai-g1-v2-synthetic-verifier-test-pack"
PATHS = {"inputs": "pack/inputs.json", "reference": "pack/reference.json",
         "annotations": "pack/annotations.json"}
AUTH_PATH = "authorizations/g1_v2_run.json"


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("network attempted")
    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c",
                           "user.email=t@example.invalid", *args],
                          capture_output=True, text=True, check=True).stdout.strip()


def _write(repo, path, data):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data if isinstance(data, bytes) else
                       json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8"))


def _commit(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "--allow-empty", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _synthetic_pack():
    """A NEW synthetic pack in the v1 frame: a new pack id and new idea wording for every
    case (unrelated to every exposed case; it keeps only the reference's exclusion and
    unsupported-claim terms and any figures, so the reference stays consistent). The
    reference structure is the v1 one the v2 decision rule is defined over."""
    inputs = json.loads((ROOT / cc.INPUT_PATH).read_text(encoding="utf-8"))
    reference = json.loads((ROOT / cc.REFERENCE_PATH).read_text(encoding="utf-8"))
    inputs["pack_id"] = reference["pack_id"] = PACK_ID
    refs = {r["case_id"]: r for r in reference["cases"]}
    for c in inputs["cases"]:
        r = refs[c["case_id"]]
        terms = [a for x in r["exclusions"] + r["unsupported_claims"] for a in x["any_of"]]
        figures = re.findall(r"\d+(?:[.,]\d+)?", cc._normalised(c["idea_text"]))
        c["idea_text"] = ("Verifier-only synthetic fixture %s, written for evidence-chain tests; "
                          "it names %s%s." % (c["case_id"], ", ".join(terms) or "no special terms",
                                              (" and the figures " + ", ".join(figures))
                                              if figures else ""))
    return inputs, reference, _full_annotations(refs)


def _files(inputs, reference, annotations):
    return {k: (PATHS[k], json.dumps(v, ensure_ascii=False, indent=1).encode("utf-8"))
            for k, v in (("inputs", inputs), ("reference", reference),
                         ("annotations", annotations))}


def _produce(manifest, cases, refs, replies=None, stop_at=None):
    """A report and journal from the REAL producer with an offline fake transport."""
    pack = (cases, refs)
    replies = replies or _full_replies(pack)
    bodies = [_body(replies[c["case_id"]]) for c in cases]
    if stop_at is not None:
        bodies = bodies[:stop_at]                       # the fake then fails the next call
    fake, journal = _Fake(bodies), io.StringIO()
    report = cc._run_cases(_adapter(fake), cases, manifest, journal)
    return report, journal.getvalue().encode("utf-8")


@pytest.fixture
def chain(tmp_path):
    """candidate commit -> authorization commit (pack + record) -> evidence commit."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"candidate revision\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    model = _adapter(_Fake([]))._model
    manifest = cc.run_manifest_v2(candidate, model, PACK_ID, files)
    record = {"kind": cc.V2_AUTHORIZATION_KIND, "manifest_sha256": cc._digest(manifest),
              "evidence": manifest["evidence"]}
    _write(repo, AUTH_PATH, record)
    authorization = _commit(repo, "authorization")
    cases, refs = inputs["cases"], {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, cases, refs)
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    evidence = _commit(repo, "evidence")
    return {"repo": repo, "candidate": candidate, "authorization": authorization,
            "evidence": evidence, "manifest": manifest, "record": record, "report": report,
            "journal": journal, "cases": cases, "refs": refs, "annotations": annotations,
            "files": files, "model": model}


def _verify(c, authorization=None, evidence=None, path=AUTH_PATH):
    return cc.verify_v2_run(str(c["repo"]), authorization or c["authorization"], path,
                            evidence or c["evidence"])


def _assess(c, record, evidence=None):
    return cc.assess_v2_run(str(c["repo"]), c["authorization"], AUTH_PATH,
                            evidence or c["evidence"], record)


def _record(c, verified, mode=cc.MODE_DIAGNOSTIC, assessor=None):
    pack = (c["cases"], c["refs"])
    judged = _full_judgments(pack, verified.replies, verified.scored)
    formal = mode == cc.MODE_FORMAL
    return {"evaluation_id": cc.EVALUATION_ID_V2,
            "method": [cc.METHOD_V2_ID, cc.METHOD_V2_VERSION],
            "report_sha256": verified.report_sha256, "mode": mode,
            "assessor": assessor or (HUMAN if formal else AGENT),
            "attestation": cc.ATTESTATION if formal else None,
            "attested_on": "2026-11-07" if formal else None, "judgments": judged}


def _new_evidence(c, report=None, journal=None):
    """Replace the committed run evidence on top of the chain and return the new commit."""
    m = c["manifest"]["evidence"]
    if report is not None:
        _write(c["repo"], m["report"], report)
    if journal is not None:
        _write(c["repo"], m["journal"], journal)
    return _commit(c["repo"], "replaced evidence")


# ==========================================================================
# 1. A complete chain verifies, and its evidence status is reported in parts
# ==========================================================================
def test_a_complete_chain_verifies_and_reports_each_fact_separately(chain):
    verified = _verify(chain)
    assert verified.complete is True
    assert verified.manifest_sha256 == chain["record"]["manifest_sha256"]
    assert verified.report_sha256 == cc._digest(chain["report"])
    assert verified.annotations_sha256 == cc.annotations_digest(chain["annotations"])
    assert verified.authorization == {
        "manifest_matches_authorized_hash": True, "authorization_recorded_before_run": True,
        "authorization_commit": chain["authorization"], "evidence_commit": chain["evidence"],
        "owner_identity": cc.OWNER_IDENTITY_NOT_AUTHENTICATED}
    result = _assess(chain, _record(chain, verified))
    assert result["verdict"] == "DIAGNOSTIC_ONLY"
    assert result["qualification"] == "NOT A QUALIFICATION: diagnostic mode"
    assert result["evidence"]["formal_blockers"] == list(cc.V2_FORMAL_BLOCKERS)
    assert result["evidence"]["authorization"]["owner_identity"] == \
        cc.OWNER_IDENTITY_NOT_AUTHENTICATED


def test_the_manifest_binds_method_revision_pack_prompt_and_configuration(chain):
    m = chain["manifest"]
    assert m["method"] == [cc.METHOD_V2_ID, cc.METHOD_V2_VERSION]
    assert m["preregistration_v2_sha256"] == cc.preregistration_v2_digest()
    assert m["code_revision"] == chain["candidate"]
    assert m["annotations_sha256"] == cc.annotations_digest(chain["annotations"])
    assert {k: v["path"] for k, v in m["pack"].items()} == PATHS
    assert m["instructions_sha256"] == cc._sha(cc.INSTRUCTIONS)
    assert m["schema_sha256"] == cc._sha(cc.schema())
    assert (m["max_output_tokens"], m["max_provider_requests"], m["retries"], m["store"]) == (
        2000, 16, 0, False)


# ==========================================================================
# 2. FORMAL stays refused, even for a chain that verifies completely
# ==========================================================================
def test_a_fully_verified_chain_never_yields_a_formal_qualification(chain):
    verified = _verify(chain)
    with pytest.raises(cc.PackError, match="FORMAL qualification is unavailable"):
        _assess(chain, _record(chain, verified, mode=cc.MODE_FORMAL))


@pytest.mark.parametrize("assessor", [AGENT, dict(HUMAN, kind="AI_ASSISTED_HUMAN")])
def test_an_invalid_formal_basis_is_refused(chain, assessor):
    verified = _verify(chain)
    with pytest.raises(cc.PackError, match="FORMAL needs a HUMAN"):
        _assess(chain, _record(chain, verified, cc.MODE_FORMAL, assessor))


def test_a_diagnostic_record_claiming_an_attestation_is_refused(chain):
    verified = _verify(chain)
    record = dict(_record(chain, verified), attestation=cc.ATTESTATION)
    with pytest.raises(cc.PackError, match="claims no attestation"):
        _assess(chain, record)


# ==========================================================================
# 3. Authorization identity and ordering
# ==========================================================================
def test_a_self_supplied_hash_without_a_prior_record_is_refused(chain):
    repo = chain["repo"]
    # the record committed together with the evidence: nothing precedes the run
    with pytest.raises(cc.PackError, match="committed before the run evidence"):
        _verify(chain, authorization=chain["evidence"])


def test_a_record_added_after_the_run_is_refused(tmp_path):
    repo = tmp_path / "late"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    model = _adapter(_Fake([]))._model
    manifest = cc.run_manifest_v2(candidate, model, PACK_ID, files)
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs)
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    evidence = _commit(repo, "evidence first")
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest),
                             "evidence": manifest["evidence"]})
    late = _commit(repo, "authorization afterwards")
    with pytest.raises(cc.PackError):
        cc.verify_v2_run(str(repo), late, AUTH_PATH, evidence)
    with pytest.raises(cc.PackError, match="evidence existed at or before"):
        cc.verify_v2_run(str(repo), late, AUTH_PATH, _commit(repo, "later"))


def test_a_record_naming_another_manifest_is_refused(chain):
    other = dict(chain["record"], manifest_sha256="0" * 64)
    _write(chain["repo"], AUTH_PATH, other)
    with pytest.raises(cc.PackError):
        _verify(chain, evidence=_commit(chain["repo"], "record rewritten"))


@pytest.mark.parametrize("mutate", [
    lambda r: r.update(kind="something else"),
    lambda r: r.update(extra=1),
    lambda r: r.pop("evidence"),
    lambda r: r["evidence"].update(report="elsewhere.json"),
])
def test_a_malformed_or_inconsistent_record_is_refused(tmp_path, mutate):
    repo = tmp_path / "bad"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    manifest = cc.run_manifest_v2(candidate, _adapter(_Fake([]))._model, PACK_ID, files)
    record = {"kind": cc.V2_AUTHORIZATION_KIND, "manifest_sha256": cc._digest(manifest),
              "evidence": copy.deepcopy(manifest["evidence"])}
    mutate(record)
    _write(repo, AUTH_PATH, record)
    auth = _commit(repo, "authorization")
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs)
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    with pytest.raises(cc.PackError):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, _commit(repo, "evidence"))


def test_commits_are_named_exactly(chain):
    for bad in ("HEAD", chain["authorization"][:12], "0" * 40, None, 42):
        with pytest.raises(cc.PackError):
            cc.verify_v2_run(str(chain["repo"]), bad, AUTH_PATH, chain["evidence"])
        with pytest.raises(cc.PackError):
            cc.verify_v2_run(str(chain["repo"]), chain["authorization"], AUTH_PATH, bad)


def test_a_candidate_revision_after_the_authorization_is_refused(tmp_path):
    repo = tmp_path / "rev"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "seed.txt", b"x\n")
    _commit(repo, "seed")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    pending = _commit(repo, "pack")
    # a manifest naming a revision that does not precede the authorization
    _write(repo, "later.txt", b"y\n")
    later = _commit(repo, "a later candidate")
    _git(repo, "reset", "-q", "--hard", pending)
    manifest = cc.run_manifest_v2(later, _adapter(_Fake([]))._model, PACK_ID, files)
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest),
                             "evidence": manifest["evidence"]})
    auth = _commit(repo, "authorization")
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs)
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    with pytest.raises(cc.PackError):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, _commit(repo, "evidence"))


# ==========================================================================
# 4. Frozen, pre-output annotations and pack files
# ==========================================================================
def test_annotations_changed_after_the_authorization_are_refused(chain):
    changed = copy.deepcopy(chain["annotations"])
    changed["cases"]["Q01"]["central"] = []
    _write(chain["repo"], PATHS["annotations"], changed)
    with pytest.raises(cc.PackError, match="changed after it: annotations"):
        _verify(chain, evidence=_commit(chain["repo"], "annotations rewritten after the run"))


def test_a_pack_reference_changed_after_the_authorization_is_refused(chain):
    _write(chain["repo"], PATHS["reference"], b"{}")
    with pytest.raises(cc.PackError, match="changed after it: reference"):
        _verify(chain, evidence=_commit(chain["repo"], "reference rewritten"))


def _chain_with(tmp_path, annotations=None, inputs=None, reference=None, name="variant",
                produce_refs=None):
    repo = tmp_path / name
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    base_inputs, base_reference, base_annotations = _synthetic_pack()
    inputs = inputs or base_inputs
    reference = reference or base_reference
    annotations = annotations or base_annotations
    def encoded(key, value):
        return (PATHS[key], value if isinstance(value, bytes) else
                json.dumps(value, ensure_ascii=False, indent=1).encode("utf-8"))
    files = {"inputs": encoded("inputs", inputs), "reference": encoded("reference", reference),
             "annotations": encoded("annotations", annotations)}
    for path, data in files.values():
        _write(repo, path, data)
    manifest = cc.run_manifest_v2(candidate, _adapter(_Fake([]))._model, PACK_ID, files)
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest),
                             "evidence": manifest["evidence"]})
    auth = _commit(repo, "authorization")
    case_list = json.loads(files["inputs"][1])["cases"]
    refs = produce_refs or {r["case_id"]: r for r in json.loads(files["reference"][1])["cases"]}
    report, journal = _produce(manifest, case_list, refs)
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    return repo, auth, _commit(repo, "evidence")


def test_annotations_written_after_outputs_are_refused(tmp_path):
    _inputs, _reference, annotations = _synthetic_pack()
    annotations["declared_before_outputs"] = False
    repo, auth, evid = _chain_with(tmp_path, annotations=annotations)
    with pytest.raises(cc.PackError, match="not declared before outputs"):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, evid)


def test_the_exposed_packs_stay_diagnostic_only(tmp_path):
    exposed_inputs = (ROOT / cc.INPUT_PATH).read_bytes()
    exposed_reference = (ROOT / cc.REFERENCE_PATH).read_bytes()
    assert {cc.INPUT_SHA256, cc.REFERENCE_SHA256} <= cc.EXPOSED_PACK_SHA256
    repo, auth, evid = _chain_with(tmp_path, inputs=exposed_inputs,
                                   reference=exposed_reference)
    with pytest.raises(cc.PackError, match="exposed pack is diagnostic evidence only"):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, evid)


def test_a_pack_outside_the_v2_decision_frame_is_refused(tmp_path):
    inputs, reference, _annotations = _synthetic_pack()
    reference["cases"][0]["group"] = "AMBIGUOUS"
    repo, auth, evid = _chain_with(tmp_path, inputs=inputs, reference=reference)
    with pytest.raises(cc.PackError):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, evid)


# ==========================================================================
# 5. Journal / report integrity and swapped replies
# ==========================================================================
def test_an_altered_report_reply_is_refused(chain):
    report = copy.deepcopy(chain["report"])
    report["rows"][0]["reply"]["outcome"] = cc.ABSTAIN
    with pytest.raises(cc.PackError, match="do not match the run journal"):
        _verify(chain, evidence=_new_evidence(chain, report=report))


def test_swapped_replies_in_the_report_are_refused(chain):
    report = copy.deepcopy(chain["report"])
    r0, r1 = report["rows"][0], report["rows"][1]
    r0["reply"], r1["reply"] = r1["reply"], r0["reply"]
    with pytest.raises(cc.PackError, match="do not match the run journal"):
        _verify(chain, evidence=_new_evidence(chain, report=report))


def test_an_altered_journal_is_refused(chain):
    lines = chain["journal"].decode("utf-8").splitlines()
    lines.pop()
    with pytest.raises(cc.PackError):
        _verify(chain, evidence=_new_evidence(chain, journal="\n".join(lines).encode()))


def test_a_report_whose_manifest_was_edited_is_refused(chain):
    report = copy.deepcopy(chain["report"])
    report["manifest"]["max_output_tokens"] = 4000
    report["manifest_sha256"] = cc._digest(report["manifest"])
    with pytest.raises(cc.PackError, match="not the authorized run"):
        _verify(chain, evidence=_new_evidence(chain, report=report))


def test_a_manifest_that_does_not_describe_the_pack_is_refused(tmp_path):
    repo = tmp_path / "desc"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    manifest = cc.run_manifest_v2(candidate, _adapter(_Fake([]))._model, PACK_ID, files)
    manifest["max_output_tokens"] = 4000                 # authorized, but not this configuration
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest),
                             "evidence": manifest["evidence"]})
    auth = _commit(repo, "authorization")
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs)
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    with pytest.raises(cc.PackError, match="does not describe this method"):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, _commit(repo, "evidence"))


def test_missing_evidence_is_refused(chain):
    m = chain["manifest"]["evidence"]
    (chain["repo"] / m["journal"]).unlink()
    with pytest.raises(cc.PackError, match="run evidence is missing"):
        _verify(chain, evidence=_commit(chain["repo"], "journal deleted"))


# ==========================================================================
# 6. Assessment inputs come only from the verified report
# ==========================================================================
def test_the_verified_run_is_sealed_and_read_only(chain):
    verified = _verify(chain)
    with pytest.raises(cc.PackError):
        cc.VerifiedRunV2({"scored": []})
    with pytest.raises(cc.PackError):
        verified.scored = []
    tampered = verified.scored
    tampered[0]["status"] = "TAMPERED"                  # a copy: the verified run is unchanged
    verified.replies["Q01"] = None
    assert verified.scored[0]["status"] != "TAMPERED"
    assert verified.replies["Q01"] is not None
    assert "cannot be made tamper-proof" in " ".join(cc.VerifiedRunV2.__doc__.split())


def test_assessment_re_verifies_and_never_trusts_an_object(chain):
    """There is no entry point that accepts replies, scores or a VerifiedRunV2: the
    assessment takes repository coordinates and verifies them itself, so a forged or
    mutated in-memory object (even through its private storage) never reaches it."""
    import inspect
    assert not hasattr(cc, "assess_verified_v2")
    assert list(inspect.signature(cc.assess_v2_run).parameters) == [
        "repo", "authorization_commit", "authorization_path", "evidence_commit", "record"]
    verified = _verify(chain)
    object.__getattribute__(verified, "_fields")["replies"]["Q01"] = None   # tamper in memory
    result = _assess(chain, _record(chain, _verify(chain)))
    assert result["verdict"] == "DIAGNOSTIC_ONLY"


def test_a_record_bound_to_another_report_is_refused(chain):
    verified = _verify(chain)
    record = dict(_record(chain, verified), report_sha256="f" * 64)
    with pytest.raises(cc.PackError, match="not bound to this method and report"):
        _assess(chain, record)


# ==========================================================================
# 7. Incomplete execution
# ==========================================================================
def test_an_incomplete_run_is_reported_incomplete_never_scored_as_success(tmp_path):
    repo = tmp_path / "incomplete"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    manifest = cc.run_manifest_v2(candidate, _adapter(_Fake([]))._model, PACK_ID, files)
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest),
                             "evidence": manifest["evidence"]})
    auth = _commit(repo, "authorization")
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs, stop_at=5)
    assert report["stopped_on"] is not None
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    evid = _commit(repo, "evidence")
    verified = cc.verify_v2_run(str(repo), auth, AUTH_PATH, evid)
    assert verified.complete is False
    result = cc.assess_v2_run(str(repo), auth, AUTH_PATH, evid, None)
    assert result["verdict"] == "INCOMPLETE"
    assert result["evidence"]["formal_blockers"] == list(cc.V2_FORMAL_BLOCKERS)


# ==========================================================================
# 8. Boundaries: v1 unchanged, FORMAL text unchanged, nothing in the product
# ==========================================================================
def test_the_fail_closed_formal_decision_and_v1_run_path_are_unchanged():
    assert cc.FORMAL_UNAVAILABLE.startswith("FORMAL qualification is unavailable")
    assert cc.AUTHORIZED_RUN_MANIFEST_SHA256 is None
    assert "refused in every case" in cc.DECISION_RULE_V2
    for blocker in ("OWNER_IDENTITY", "FRESH_PACK", "AUTHORIZED_RUN", "HUMAN_REVIEW", "METHOD"):
        assert any(b.startswith(blocker + ":") for b in cc.V2_FORMAL_BLOCKERS)


def test_nothing_in_the_product_imports_the_verifier():
    for folder in ("engine", "web"):
        for path in (ROOT / folder).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "verify_v2_run" not in text and "assess_v2_run" not in text
            assert "run_g1_component_concept_eval" not in text


def test_a_record_and_manifest_naming_different_evidence_is_refused(tmp_path):
    """The run evidence really exists where the record says, but the authorized manifest
    names other paths: the two must describe the same run."""
    repo = tmp_path / "paths"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    manifest = cc.run_manifest_v2(candidate, _adapter(_Fake([]))._model, PACK_ID, files)
    elsewhere = {"journal": "other/run_journal.jsonl", "report": "other/run_report.json"}
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest), "evidence": elsewhere})
    auth = _commit(repo, "authorization")
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs)
    _write(repo, elsewhere["report"], report)
    _write(repo, elsewhere["journal"], journal)
    with pytest.raises(cc.PackError, match="name different evidence"):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, _commit(repo, "evidence"))


# ==========================================================================
# 9. Review regressions (B1-B3, N1, N3, N4)
# ==========================================================================
def test_an_attempt_record_cannot_stand_in_for_the_rows_reply(chain):
    """B1: a row whose own reply is forged while its `attempt` carries the journal's reply."""
    report = copy.deepcopy(chain["report"])
    row = report["rows"][0]
    row["attempt"]["reply"] = row["reply"]
    row["reply"] = dict(row["reply"], outcome=cc.ABSTAIN)
    with pytest.raises(cc.PackError, match="report row is malformed"):
        _verify(chain, evidence=_new_evidence(chain, report=report))


def test_an_attempt_record_cannot_stand_in_for_the_rows_status(chain):
    report = copy.deepcopy(chain["report"])
    row = report["rows"][1]
    row["attempt"].update(provider_status=row["provider_status"], reply=row["reply"])
    row["provider_status"], row["reply"] = cc.P_REFUSAL, None
    with pytest.raises(cc.PackError, match="report row is malformed"):
        _verify(chain, evidence=_new_evidence(chain, report=report))


def test_run_evidence_made_on_a_side_branch_before_authorization_is_refused(tmp_path):
    """B2: evidence committed on a branch from the candidate, before the pack and the
    record existed, then merged in after the authorization."""
    repo = tmp_path / "side"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    manifest = cc.run_manifest_v2(candidate, cc.MODEL, PACK_ID, files)
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs)
    _git(repo, "checkout", "-q", "-b", "side")
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    _commit(repo, "outputs first, on a side branch")
    _git(repo, "checkout", "-q", "main")
    for path, data in files.values():
        _write(repo, path, data)
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest),
                             "evidence": manifest["evidence"]})
    auth = _commit(repo, "authorization")
    _git(repo, "merge", "-q", "--no-edit", "side")
    merged = _git(repo, "rev-parse", "HEAD")
    with pytest.raises(cc.PackError, match="existed at or before the authorization"):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, merged)


@pytest.mark.parametrize("variant", ["reformatted", "renamed_id", "exposed_id_new_text",
                                     "padded"])
def test_exposed_content_is_refused_however_it_is_repackaged(tmp_path, variant):
    """B3: the exposed pack is refused by content and identity, not only by file bytes."""
    inputs = json.loads((ROOT / cc.INPUT_PATH).read_text(encoding="utf-8"))
    reference = json.loads((ROOT / cc.REFERENCE_PATH).read_text(encoding="utf-8"))
    if variant == "renamed_id":
        inputs["pack_id"] = reference["pack_id"] = "a-new-looking-identity"
    if variant == "padded":
        inputs["pack_id"] = reference["pack_id"] = "a-new-looking-identity"
        for c in inputs["cases"]:
            c["idea_text"] += (" Extra padding sentences written only to lower the similarity "
                               "ratio of this copy below the threshold. " * 4)
    if variant == "exposed_id_new_text":
        inputs, reference, _a = _synthetic_pack()
        inputs["pack_id"] = reference["pack_id"] = cc.PACK_ID
    refs = {r["case_id"]: r for r in reference["cases"]}
    annotations = _full_annotations(refs)
    inputs_bytes = json.dumps(inputs, ensure_ascii=False, indent=3).encode("utf-8")
    reference_bytes = json.dumps(reference, ensure_ascii=False, indent=3).encode("utf-8")
    repo, auth, evid = _chain_with(tmp_path, annotations=annotations, inputs=inputs_bytes,
                                   reference=reference_bytes)
    with pytest.raises(cc.PackError, match="exposed pack is diagnostic evidence only"):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, evid)


def test_the_positive_fixture_is_not_exposed_content():
    inputs, _reference, _a = _synthetic_pack()
    pool = cc._exposed_ideas()
    for c in inputs["cases"]:
        text = cc._normalised(c["idea_text"]).lower()
        assert text not in pool
        assert max(cc.difflib.SequenceMatcher(None, text, e).ratio() for e in pool) \
            < cc.MAX_SIMILARITY


def test_a_manifest_without_a_recorded_price_basis_is_refused(tmp_path):
    """N1: the v1 run boundary's model rule, applied to the v2 manifest."""
    repo = tmp_path / "model"
    repo.mkdir()
    _git(repo, "init", "-q")
    _write(repo, "candidate.txt", b"x\n")
    candidate = _commit(repo, "candidate")
    inputs, reference, annotations = _synthetic_pack()
    files = _files(inputs, reference, annotations)
    for path, data in files.values():
        _write(repo, path, data)
    manifest = cc.run_manifest_v2(candidate, "some-unpriced-model", PACK_ID, files)
    _write(repo, AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                             "manifest_sha256": cc._digest(manifest),
                             "evidence": manifest["evidence"]})
    auth = _commit(repo, "authorization")
    refs = {r["case_id"]: r for r in reference["cases"]}
    report, journal = _produce(manifest, inputs["cases"], refs)
    _write(repo, manifest["evidence"]["report"], report)
    _write(repo, manifest["evidence"]["journal"], journal)
    with pytest.raises(cc.PackError, match="no recorded price basis"):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, _commit(repo, "evidence"))


def test_an_annotated_tag_is_not_a_commit(chain):
    """N3: an object that merely peels to a commit is refused."""
    _git(chain["repo"], "tag", "-a", "auth-tag", "-m", "t", chain["authorization"])
    tag = _git(chain["repo"], "rev-parse", "auth-tag")
    assert tag != chain["authorization"]
    with pytest.raises(cc.PackError, match="not a commit object"):
        _verify(chain, authorization=tag)


@pytest.mark.parametrize("journal, path", [
    (b"\xff\xfe not text", AUTH_PATH),
    (None, "a\x00b"),
])
def test_malformed_input_is_a_refusal_never_a_crash(chain, journal, path):
    """N4: undecodable evidence and NUL in a path are PackError, not another exception."""
    evidence = _new_evidence(chain, journal=journal) if journal is not None else None
    with pytest.raises(cc.PackError):
        _verify(chain, evidence=evidence, path=path)


def test_malformed_pack_content_is_a_refusal_never_a_crash(tmp_path):
    inputs, reference, annotations = _synthetic_pack()
    good = {r["case_id"]: copy.deepcopy(r) for r in reference["cases"]}
    reference["cases"][0]["essential_functions"] = ["not a function record"]
    repo, auth, evid = _chain_with(tmp_path, inputs=inputs, reference=reference,
                                   produce_refs=good)
    with pytest.raises(cc.PackError):
        cc.verify_v2_run(str(repo), auth, AUTH_PATH, evid)


# ==========================================================================
# Optional Owner-detached-signature INSPECTION — OFFLINE ONLY.
# These test keys are generated in disposable temp directories; no real key
# or Owner identity is asserted by a synthetic signature.
# ==========================================================================
def _signed_chain(chain, tmp_path, variant=None):
    """Rebuild the fixture with a detached signature committed WITH authorization.

    ``variant`` builds the synthetic key lifecycle: None (one valid primary
    signing key), "subkey" (a valid signing subkey), "revoked" (signed after
    the key's revocation from a pre-revocation copy, the certificate carrying
    the revocation), "expired" (key created and used in the past, now expired)
    or "expired_subkey" (a valid primary whose expired subkey signed)."""
    import os
    import shutil
    from pathlib import Path

    if not shutil.which("gpg"):
        pytest.skip("GPG is required for signature-inspection tests")
    repo = chain["repo"]
    _git(repo, "reset", "--hard", chain["candidate"])
    for path, content in chain["files"].values():
        _write(repo, path, content)
    _write(repo, AUTH_PATH, chain["record"])
    raw = (repo / AUTH_PATH).read_bytes()
    home = tmp_path / "synthetic-gpg-private"
    home.mkdir(mode=0o700)
    env = {**os.environ, "GNUPGHOME": str(home)}
    user = "Synthetic owner for offline test <synthetic@example.invalid>"

    def gpg(*args, input=None):
        return subprocess.run(["gpg", "--batch", "--no-tty", "--homedir", str(home),
                               *args], input=input, capture_output=True, env=env,
                              check=True).stdout

    past = ("--faked-system-time", "20200101T000000!")
    unlocked = ("--pinentry-mode", "loopback", "--passphrase", "")
    created = past if variant in ("expired", "expired_subkey") else ()
    usage, expiry = ("cert", "0") if variant in ("subkey", "expired_subkey") \
        else ("sign", "1y" if variant == "expired" else "0")
    gpg(*created, *unlocked, "--quick-generate-key", user, "ed25519", usage, expiry)
    listing = gpg("--with-colons", "--fingerprint", "--list-keys").decode("utf-8")
    fingerprint = next(line.split(":")[9] for line in listing.splitlines()
                       if line.startswith("fpr:"))
    if variant in ("subkey", "expired_subkey"):
        sub_time = past if variant == "expired_subkey" else ()
        gpg(*sub_time, *unlocked, "--quick-add-key", fingerprint, "ed25519", "sign",
            "1y" if variant == "expired_subkey" else "0")
    sigpath = home / "authorization.sig"
    signing_env = env
    if variant == "revoked":
        # Keep a pre-revocation copy, revoke the key, then sign with the copy:
        # a compromised key used after its Owner revoked it.
        pre_revocation = tmp_path / "gpg-prerev"  # short: agent socket path limit
        shutil.copytree(home, pre_revocation, ignore=shutil.ignore_patterns("S.*"))
        revocation = (home / "openpgp-revocs.d" / (fingerprint + ".rev")).read_bytes()
        gpg("--import", input=revocation.replace(b":-----BEGIN", b"-----BEGIN"))
        signing_env = {**os.environ, "GNUPGHOME": str(pre_revocation)}
        subprocess.run(["gpg", "--batch", "--no-tty", "--homedir", str(pre_revocation),
                        *unlocked, "--detach-sign", "--output", str(sigpath),
                        str(repo / AUTH_PATH)], capture_output=True,
                       env=signing_env, check=True)
    else:
        signing_time = past if variant in ("expired", "expired_subkey") else ()
        gpg(*signing_time, *unlocked, "--detach-sign", "--output", str(sigpath),
            str(repo / AUTH_PATH))
    cert = gpg("--armor", "--export", user)
    signature_path = "authorizations/g1_v2_run.sig"
    _write(repo, signature_path, sigpath.read_bytes())
    auth = _commit(repo, "synthetic signed authorization")
    _write(repo, chain["manifest"]["evidence"]["report"], chain["report"])
    _write(repo, chain["manifest"]["evidence"]["journal"], chain["journal"])
    evidence = _commit(repo, "synthetic evidence")
    return {"repo": repo, "auth": auth, "evidence": evidence,
            "public": cert, "fingerprint": fingerprint,
            "signature_path": signature_path, "record": raw}


def _inspect_signed(s, **kw):
    return cc.inspect_v2_detached_authorization(
        str(s["repo"]), kw.get("authorization", s["auth"]), AUTH_PATH,
        kw.get("evidence", s["evidence"]),
        kw.get("signature_path", s["signature_path"]),
        kw.get("public", s["public"]), kw.get("fingerprint", s["fingerprint"]))


def test_signed_authorization_proves_only_signature_not_owner_or_formal(chain, tmp_path):
    s = _signed_chain(chain, tmp_path)
    result = _inspect_signed(s)
    assert result["signature_valid"] is True
    assert result["trusted_primary_fingerprint"] == s["fingerprint"].upper()
    assert result["owner_identity"] == cc.OWNER_IDENTITY_NOT_AUTHENTICATED
    assert result["publication_time"] == "NOT_AUTHENTICATED_BY_GIT_ANCESTRY"
    assert result["qualification"] == "NOT_A_MODEL_QUALIFICATION"
    assert len(result["formal_blockers"]) == len(cc.V2_FORMAL_BLOCKERS)
    assert result["manifest_sha256"] == chain["record"]["manifest_sha256"]
    assert result["signed_authorization_sha256"] == __import__("hashlib").sha256(
        s["record"]).hexdigest()
    verified = cc.verify_v2_run(str(s["repo"]), s["auth"], AUTH_PATH, s["evidence"])
    with pytest.raises(cc.PackError, match="FORMAL qualification is unavailable"):
        cc.assess_v2_run(str(s["repo"]), s["auth"], AUTH_PATH, s["evidence"],
                         _record(chain, verified, mode=cc.MODE_FORMAL))


@pytest.mark.parametrize("invalid", ["fingerprint", "certificate", "wrong_valid_certificate",
                                      "missing_key", "invalid_fingerprint",
                                      "wrong_signature_path"])
def test_signature_inspection_refuses_untrusted_material(chain, tmp_path, invalid):
    s = _signed_chain(chain, tmp_path)
    options = {}
    if invalid == "fingerprint":
        options["fingerprint"] = "0" * 40
    elif invalid == "certificate":
        # A genuine private-key export must not be accepted as public-only
        # trust material, even if GPG can read its signing certificate.
        home = tmp_path / "synthetic-gpg-private"
        result = subprocess.run(
            ["gpg", "--batch", "--no-tty", "--homedir", str(home),
             "--pinentry-mode", "loopback", "--passphrase", "",
             "--armor", "--export-secret-keys", s["fingerprint"]],
            capture_output=True, check=True)
        assert b"BEGIN PGP PRIVATE KEY BLOCK" in result.stdout
        options["public"] = result.stdout
    elif invalid == "wrong_valid_certificate":
        home = tmp_path / "synthetic-gpg-private"
        other = "Untrusted second key <other@example.invalid>"
        subprocess.run(
            ["gpg", "--batch", "--no-tty", "--homedir", str(home),
             "--pinentry-mode", "loopback", "--passphrase", "",
             "--quick-generate-key", other, "ed25519", "sign", "0"],
            capture_output=True, check=True)
        certificate = subprocess.run(
            ["gpg", "--batch", "--no-tty", "--homedir", str(home),
             "--armor", "--export", other],
            capture_output=True, check=True).stdout
        assert certificate != s["public"] and b"BEGIN PGP PUBLIC KEY BLOCK" in certificate
        options["public"] = certificate
    elif invalid == "missing_key":
        options["public"] = b""
    elif invalid == "invalid_fingerprint":
        options["fingerprint"] = "trust-me"
    else:
        options["signature_path"] = "../secrets/owner.key"
    with pytest.raises(cc.PackError):
        _inspect_signed(s, **options)


def test_signature_inspection_refuses_mutated_or_late_signature(chain, tmp_path):
    s = _signed_chain(chain, tmp_path)
    # Replacing bytes later cannot retroactively change the committed signature.
    signature = (s["repo"] / s["signature_path"]).read_bytes()
    _write(s["repo"], s["signature_path"], signature + b"tampered")
    changed = _commit(s["repo"], "tampered signature after run")
    with pytest.raises(cc.PackError, match="signature must precede"):
        _inspect_signed(s, evidence=changed)
    # The signed authorization is immutable: a changed record is refused by v2.
    _write(s["repo"], AUTH_PATH, {"kind": cc.V2_AUTHORIZATION_KIND,
                                  "manifest_sha256": "0" * 64,
                                  "evidence": chain["manifest"]["evidence"]})
    bad = _commit(s["repo"], "changed authorization after signature")
    with pytest.raises(cc.PackError):
        _inspect_signed(s, evidence=bad)


def test_signed_inspection_has_no_provider_or_private_key_requirement(chain, tmp_path):
    s = _signed_chain(chain, tmp_path)
    # The private signing directory is removed: public verification must still work.
    import shutil
    shutil.rmtree(tmp_path / "synthetic-gpg-private")
    assert _inspect_signed(s)["signature_valid"] is True


def test_signature_from_a_valid_signing_subkey_is_accepted(chain, tmp_path):
    s = _signed_chain(chain, tmp_path, variant="subkey")
    result = _inspect_signed(s)
    assert result["signature_valid"] is True
    assert result["trusted_primary_fingerprint"] == s["fingerprint"].upper()
    assert result["signer_fingerprint"] != s["fingerprint"].upper()
    assert result["owner_identity"] == cc.OWNER_IDENTITY_NOT_AUTHENTICATED


@pytest.mark.parametrize("variant", ["revoked", "expired", "expired_subkey"])
def test_signature_from_a_revoked_or_expired_key_is_refused(chain, tmp_path, variant):
    # F1 (PR #943 security review): GnuPG exits 0 and emits VALIDSIG for these
    # signatures, with the right fingerprint; they must still be refused.
    s = _signed_chain(chain, tmp_path, variant=variant)
    with pytest.raises(cc.PackError, match="invalid detached authorization signature"
                                           "|revoked, expired or invalid"):
        _inspect_signed(s)


def test_refused_gpg_status_and_validity_sets_are_fail_closed():
    assert {"REVKEYSIG", "EXPKEYSIG", "EXPSIG", "BADSIG", "ERRSIG", "KEYREVOKED",
            "KEYEXPIRED", "NO_PUBKEY"} <= cc._GPG_REFUSED_STATUS
    assert {"r", "e"} <= cc._GPG_REFUSED_VALIDITY
