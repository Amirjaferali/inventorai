"""G1-1/2 v2 prospective run-evidence verification (`verify_v2_run`, `assess_verified_v2`).

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
    """The v1 held-out pack's content under a NEW identity, so it is not an exposed file."""
    inputs = json.loads((ROOT / cc.INPUT_PATH).read_text(encoding="utf-8"))
    reference = json.loads((ROOT / cc.REFERENCE_PATH).read_text(encoding="utf-8"))
    inputs["pack_id"] = reference["pack_id"] = PACK_ID
    refs = {r["case_id"]: r for r in reference["cases"]}
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
    result = cc.assess_verified_v2(verified, _record(chain, verified))
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
        cc.assess_verified_v2(verified, _record(chain, verified, mode=cc.MODE_FORMAL))


@pytest.mark.parametrize("assessor", [AGENT, dict(HUMAN, kind="AI_ASSISTED_HUMAN")])
def test_an_invalid_formal_basis_is_refused(chain, assessor):
    verified = _verify(chain)
    with pytest.raises(cc.PackError, match="FORMAL needs a HUMAN"):
        cc.assess_verified_v2(verified, _record(chain, verified, cc.MODE_FORMAL, assessor))


def test_a_diagnostic_record_claiming_an_attestation_is_refused(chain):
    verified = _verify(chain)
    record = dict(_record(chain, verified), attestation=cc.ATTESTATION)
    with pytest.raises(cc.PackError, match="claims no attestation"):
        cc.assess_verified_v2(verified, record)


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


def _chain_with(tmp_path, annotations=None, inputs=None, reference=None, name="variant"):
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
    refs = {r["case_id"]: r for r in json.loads(files["reference"][1])["cases"]}
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


def test_only_a_verified_run_can_be_assessed(chain):
    verified = _verify(chain)
    record = _record(chain, verified)
    for fake in (None, {"scored": verified.scored}, chain["report"]):
        with pytest.raises(cc.PackError, match="verified by verify_v2_run"):
            cc.assess_verified_v2(fake, record)


def test_a_record_bound_to_another_report_is_refused(chain):
    verified = _verify(chain)
    record = dict(_record(chain, verified), report_sha256="f" * 64)
    with pytest.raises(cc.PackError, match="not bound to this method and report"):
        cc.assess_verified_v2(verified, record)


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
    verified = cc.verify_v2_run(str(repo), auth, AUTH_PATH, _commit(repo, "evidence"))
    assert verified.complete is False
    result = cc.assess_verified_v2(verified, None)
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
            assert "verify_v2_run" not in text and "run_g1_component_concept_eval" not in text


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
