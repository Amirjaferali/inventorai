"""G1 campaign 02 — guarded single-run runner: v2 candidate prompt x independent held-out pack.

File-creation contract:
  Path: scripts/run_g1_precreation_campaign_02.py
  Purpose: ONE manifest-bound, single-run synthetic campaign of the merged v2
    candidate instructions (`scripts/g1_precreation_semantic_v2_candidate.py`)
    over the independently authored 24-case held-out pack and its frozen
    pre-registration (`scripts/g1_precreation_heldout_v2_preregistration.py`,
    reference revision 2). Offline plan and manifest, the exact provider body per
    case, reservation accounting, an fsynced journal, the run report, human
    review items and the pre-registered verdict over a COMPLETED human
    assessment. It is not a pytest test and never runs in CI.
  Authority: Owner instruction "G1 Campaign-02 Guarded Runner Preparation"
    (2026-11-04): preparation only. No provider request is authorized. A run
    needs the Owner to name the SHA-256 of the manifest of the exact clean commit
    that runs; nothing else opens the request path.
  Distinct from campaign 01: campaign 01 (`scripts/run_g1_precreation_campaign.py`,
    evidence in docs/benchmarks/evidence/g1_precreation_semantic_v1/) is consumed
    and is neither modified, reused nor re-run. This runner has its own identity,
    manifest, limits and evidence directory.
  Reuse (all unchanged, imported):
    * prompt: `v2c.candidate_request_view` (v2 instructions over the v1 schema and
      governed concept ids);
    * pack, criteria, decision rule: `ho.load_heldout`, `ho.preregistration_digest`,
      `ho.decide`, `ho.baseline`;
    * scoring and review: `ev.score_case`, `ev.review_items`;
    * price basis, its verification, the reservation rule, provider statuses and
      the canonical-JSON helper: `scripts/run_g1_precreation_campaign.py`;
    * adapter, measured call, model confirmation, price arithmetic:
      `scripts/run_msnl_eval.py`;
    * response recorder, refusal resolution, offline-fake marker, digest,
      clean-revision check, fsynced journal, clock: `scripts/run_proof_b_eval.py`.
    Only the campaign-specific manifest, boundary, request loop and report binding
    are new: campaign 01's are bound to its own pack and limits and stay frozen.
  Input contract: ONLY these options —
    (no option)  the plan: pack, prompt and pre-registration identity, the budget
                 plan of the exact payloads and the authorization state; nothing sent;
    `--manifest` offline: the manifest and its digest for the CURRENT clean
                 checkout; nothing sent;
    `--provider openai --allow-network --managed-credential --authorized-manifest SHA`
                 the campaign path: REFUSED before any adapter or transport exists
                 unless every boundary below holds;
    `--review-items REPORT [--journal J]`, `--aggregate ASSESSMENT --report REPORT
     --authorized-manifest SHA [--journal J]`: offline post-run steps.
  Prohibited behaviors: no real inventor / project / personal data; no product
    import of this module; reference labels and annotations never enter a request;
    no tools, retrieval or stored provider state; no retry; no verdict without
    every K6, K4-context and G5 human assessment; no production or Arabic claim.
"""
import argparse
import hashlib
import json
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from engine import technical_orchestration_openai as toa  # noqa: E402
from engine import msnl_shadow as ms  # noqa: E402
from scripts import g1_precreation_heldout_v2_preregistration as ho  # noqa: E402
from scripts import g1_precreation_semantic_v2_candidate as v2c  # noqa: E402
from scripts import run_g1_precreation_campaign as c01  # noqa: E402  (read only)
from scripts import run_g1_precreation_semantic_eval as ev  # noqa: E402
from scripts.run_msnl_eval import (  # noqa: E402  (reused, unchanged)
    ERR_BUDGET, ERR_COST_CEILING, ERR_COST_UNBOUNDED, ERR_MODEL_UNCONFIRMED,
    OpenAIMsnlAdapter, PackError, _measured_call, _pf_model_confirmed, _pf_usd,
)
from scripts.run_proof_b_eval import (  # noqa: E402  (reused, unchanged)
    RecordingTransport, _digest, _journal, _offline_fake, _sentinel_kind, _utc_now,
    current_revision,
)

CAMPAIGN_ID = "g1-precreation-campaign-02"
# The request path needs the Owner-named digest of the exact clean commit's
# manifest at run time; it is never committed here.
AUTHORIZED_RUN_MANIFEST_SHA256 = None

MODEL = toa.MODEL                               # "gpt-6-sol", D3 synthetic evaluation only
MAX_PROVIDER_REQUESTS = 24                      # one per held-out case, no repeats
MAX_OUTPUT_TOKENS = c01.MAX_OUTPUT_TOKENS       # 1200: the reservation rule assumes it
RETRIES = 0
CAMPAIGN_CEILING_USD = 5.0
PRICING = c01.PRICING                           # recorded official Standard rates
PRICE_VERIFICATION = c01.PRICE_VERIFICATION     # recorded 2026-11-04 (PR #922)
RESERVATION = c01.RESERVATION                   # Proof B's 6x reservation rule
STOP_RULE = ("Stop at the first provider ERROR (transport, HTTP status, malformed or "
             "incomplete reply, output over the cap, unconfirmed model) or an ambiguous "
             "refusal, and at the request or currency limit; every later case is "
             "NOT_ATTEMPTED. A confirmed provider refusal does not stop the run, but under "
             "the frozen held-out decision rule any case without a reply makes the run "
             "INCOMPLETE; it is never scored as a success.")

EVIDENCE_DIR = os.path.join(_ROOT, "docs", "benchmarks", "evidence",
                            "g1_precreation_semantic_heldout_v2")
JOURNAL_PATH = os.path.join(EVIDENCE_DIR, "campaign_02_journal.jsonl")
REPORT_PATH = os.path.join(EVIDENCE_DIR, "campaign_02_report.json")
CAMPAIGN_01_EVIDENCE = os.path.relpath(c01.EVIDENCE_DIR, _ROOT)

P_RESPONDED, P_REFUSAL, P_ERROR = c01.P_RESPONDED, c01.P_REFUSAL, c01.P_ERROR
P_AMBIGUOUS, P_NOT_ATTEMPTED = c01.P_AMBIGUOUS, c01.P_NOT_ATTEMPTED
_STOPS = (P_ERROR, P_AMBIGUOUS)
_PROVIDER_STATUSES = (P_RESPONDED, P_REFUSAL, P_ERROR, P_AMBIGUOUS, P_NOT_ATTEMPTED)
_ROW_KEYS = {"case_id", "provider_status", "error_kind", "reply"}
_SHA256 = re.compile(r"[0-9a-f]{64}")


def _sha(value):
    raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False,
                                                          sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# What is sent, and the identity of the one run
# ─────────────────────────────────────────────────────────────────────────────
def payload(case, model=MODEL):
    """The exact provider body for ONE held-out case: the frozen v2 candidate
    instructions, the v1 schema and the idea text only."""
    view = v2c.candidate_request_view(case["idea_text"])
    return {"model": model, "instructions": view["instructions"], "input": view["input"],
            "store": False, "max_output_tokens": MAX_OUTPUT_TOKENS,
            "text": {"format": {"type": "json_schema",
                                "name": "g1_precreation_interpretation_v2",
                                "strict": True, "schema": view["schema"]}}}


def _body(case, model):
    return json.dumps(payload(case, model), ensure_ascii=False).encode("utf-8")


def run_manifest(code_revision, model):
    if not (isinstance(code_revision, str) and code_revision.strip()):
        raise PackError("manifest needs a code revision")
    cases, _refs = ho.load_heldout()
    return {"campaign_id": CAMPAIGN_ID, "pack_id": ho.PACK_ID,
            "input_sha256": ho.INPUT_SHA256, "reference_sha256": ho.REFERENCE_SHA256,
            "preregistration_sha256": ho.preregistration_digest(),
            "candidate_instructions_sha256": _sha(v2c.candidate_instructions()),
            "schema_sha256": _sha(ev._schema(ev.governed_concepts())),
            "governed_concepts": list(ev.governed_concepts()),
            "scorer": "scripts/run_g1_precreation_semantic_eval.py score_case",
            "decision_rule": "scripts/g1_precreation_heldout_v2_preregistration.py decide",
            "payloads_sha256": _digest([payload(c, model) for c in cases]),
            "code_revision": code_revision, "model": model, "endpoint": toa.ENDPOINT,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "max_provider_requests": MAX_PROVIDER_REQUESTS, "retries": RETRIES,
            "store": False, "tools": "none", "stop_rule": STOP_RULE,
            "budget": {"ceiling_usd": CAMPAIGN_CEILING_USD, "pricing": PRICING,
                       "price_verification": PRICE_VERIFICATION, "reservation": RESERVATION},
            "evidence": {"journal": os.path.relpath(JOURNAL_PATH, _ROOT),
                         "report": os.path.relpath(REPORT_PATH, _ROOT)},
            "not_campaign_01": {"campaign_01_evidence": CAMPAIGN_01_EVIDENCE,
                                "state": "consumed; never reused or re-run"},
            "one_run_policy": ("Exactly one run: the journal is claimed by exclusive create; "
                               "existing campaign-02 evidence in the tree or in any commit "
                               "refuses a new run; an interrupted run is incomplete and is "
                               "never rerun.")}


def reservation_usd(body_bytes):
    return _pf_usd(body_bytes + RESERVATION["overhead_input_tokens"], MAX_OUTPUT_TOKENS,
                   RESERVATION["input_usd_per_1m"], RESERVATION["output_usd_per_1m"])


def budget_plan(cases, model=MODEL):
    reserved = [reservation_usd(len(_body(c, model))) for c in cases]
    return {"ceiling_usd": CAMPAIGN_CEILING_USD, "requests": len(reserved),
            "max_reservation_usd": round(max(reserved), 6),
            "all_reservations_usd": round(sum(reserved), 6),
            "within_ceiling": sum(reserved) <= CAMPAIGN_CEILING_USD,
            "published_rate_maximum_usd": round(sum(reserved) / RESERVATION["multiplier"], 6)}


def campaign_authorized(manifest, authorized_manifest_sha256):
    return (isinstance(authorized_manifest_sha256, str)
            and _SHA256.fullmatch(authorized_manifest_sha256) is not None
            and authorized_manifest_sha256 == _digest(manifest))


def _evidence_in_history():
    import subprocess
    try:
        out = subprocess.run(["git", "-C", _ROOT, "rev-list", "--all", "--",
                              os.path.relpath(EVIDENCE_DIR, _ROOT)],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        raise PackError("repository history unavailable")
    return bool(out.strip())


def check_campaign_boundary(cases, manifest, authorized_manifest_sha256, journal=None):
    """Every check a real campaign must pass, BEFORE any adapter, transport or
    evidence file exists. Fails closed on the first violation."""
    if not campaign_authorized(manifest, authorized_manifest_sha256):
        raise PackError("campaign 02 not authorized for this manifest")
    if not c01.price_verified():
        raise PackError("price basis not verified for this run")
    pinned, _refs = ho.load_heldout()
    if list(cases) != pinned or len(pinned) > MAX_PROVIDER_REQUESTS:
        raise PackError("cases are not the pinned held-out pack")
    if manifest.get("model") != PRICING["model"] or manifest.get("model") != MODEL:
        raise PackError("no recorded price basis for this model")
    if manifest != run_manifest(manifest.get("code_revision"), manifest.get("model")):
        raise PackError("manifest does not describe this pack, prompt and configuration")
    if not budget_plan(pinned, manifest["model"])["within_ceiling"]:
        raise PackError("the reservations of every request exceed the ceiling")
    if journal is not None:
        raise PackError("the campaign journal is created by the campaign itself")
    if os.path.exists(JOURNAL_PATH) or os.path.exists(REPORT_PATH) or _evidence_in_history():
        raise PackError("campaign 02 evidence already exists: one run only, and an "
                        "interrupted run is incomplete, never rerun")
    if manifest.get("code_revision") != current_revision():
        raise PackError("manifest does not describe this checkout")


# ─────────────────────────────────────────────────────────────────────────────
# One request per case, never retried
# ─────────────────────────────────────────────────────────────────────────────
def classify(adapter, case):
    reply, meta = _measured_call(adapter, payload(case, adapter._model))

    def result(status, kind, value):
        return {"provider_status": status, "error_kind": kind, "reply": value, "meta": meta}
    out = meta["usage"]["output_tokens"]
    if meta["sent"] and isinstance(out, int) and out > MAX_OUTPUT_TOKENS:
        return result(P_ERROR, ERR_COST_UNBOUNDED, None)
    if reply is None:
        return result(P_ERROR, adapter.last_error_kind, None)
    if not _pf_model_confirmed(meta["model"], adapter._model):
        return result(P_ERROR, ERR_MODEL_UNCONFIRMED, None)
    if reply == ms.ABSTAIN:
        kind = _sentinel_kind(adapter)
        return result(P_REFUSAL if kind == "refusal" else P_AMBIGUOUS, None, None)
    return result(P_RESPONDED, None, reply)


def campaign(adapter, cases, manifest, journal=None, authorized_manifest_sha256=None):
    if manifest != run_manifest(manifest.get("code_revision"), adapter._model):
        raise PackError("manifest does not describe this run")
    if _offline_fake(adapter):
        return _run_cases(adapter, cases, manifest, journal)
    check_campaign_boundary(cases, manifest, authorized_manifest_sha256, journal)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    try:
        claimed = open(JOURNAL_PATH, "x", encoding="utf-8")
    except FileExistsError:
        raise PackError("campaign 02 evidence already exists: one run only, and an "
                        "interrupted run is incomplete, never rerun")
    with claimed:
        return _run_cases(adapter, cases, manifest, claimed)


def _run_cases(adapter, cases, manifest, journal):
    price_in, price_out = PRICING["input_usd_per_1m"], PRICING["output_usd_per_1m"]
    res_in, res_out = RESERVATION["input_usd_per_1m"], RESERVATION["output_usd_per_1m"]
    ledger = {"requests": 0, "sent": 0, "committed": 0.0, "measured": 0.0,
              "measured_complete": True}
    seen, started, rows, stopped = set(), _utc_now(), [], None
    for case in cases:
        if case["case_id"] in seen:
            raise PackError("duplicate case: one request per case")
        seen.add(case["case_id"])
        if stopped is None and ledger["requests"] >= MAX_PROVIDER_REQUESTS:
            stopped = ERR_BUDGET
        if stopped is not None:
            rows.append({"case_id": case["case_id"], "provider_status": P_NOT_ATTEMPTED,
                         "error_kind": stopped if stopped == ERR_BUDGET else None,
                         "reply": None})
            continue
        reserved = reservation_usd(len(_body(case, adapter._model)))
        if ledger["committed"] + reserved > CAMPAIGN_CEILING_USD:
            _journal(journal, {"event": "refused_before_send", "case_id": case["case_id"],
                               "reason": ERR_COST_CEILING,
                               "committed_usd": round(ledger["committed"], 6),
                               "reserved_usd": round(reserved, 6)})
            stopped = ERR_COST_CEILING
            rows.append({"case_id": case["case_id"], "provider_status": P_NOT_ATTEMPTED,
                         "error_kind": ERR_COST_CEILING, "reply": None})
            continue
        ledger["requests"] += 1
        _journal(journal, {"event": "reserved", "attempt": ledger["requests"],
                           "case_id": case["case_id"], "reserved_usd": round(reserved, 6),
                           "committed_usd": round(ledger["committed"], 6)})
        result = classify(adapter, case)
        meta = result.pop("meta")
        usage = meta["usage"]
        known = isinstance(usage["input_tokens"], int) and isinstance(usage["output_tokens"], int)
        if not meta["sent"]:
            bound = 0.0
        elif known and meta["http_status"] == 200 and result["error_kind"] is None:
            bound = _pf_usd(usage["input_tokens"], usage["output_tokens"], res_in, res_out)
        else:
            bound = reserved                     # missing usage or failure: the whole reservation
        cost = (_pf_usd(usage["input_tokens"], usage["output_tokens"], price_in, price_out)
                if known else None)
        if meta["sent"]:
            ledger["sent"] += 1
            if cost is None:
                ledger["measured_complete"] = False
        ledger["measured"] += cost or 0.0
        ledger["committed"] += bound
        attempt = {"attempt": ledger["requests"], "sent": meta["sent"],
                   "http_status": meta["http_status"], "response_id": meta["response_id"],
                   "requested_model": adapter._model, "returned_model": meta["model"],
                   "response_status": meta["response_status"],
                   "incomplete_reason": meta["incomplete_reason"], "usage": usage,
                   "latency_ms": meta["latency_ms"], "reserved_usd": round(reserved, 6),
                   "measured_cost_usd": None if cost is None else round(cost, 6),
                   "bound_usd": round(bound, 6)}
        row = {"case_id": case["case_id"], **result, "attempt": attempt}
        rows.append(row)
        _journal(journal, {"event": "attempt", "case_id": case["case_id"],
                           "provider_status": row["provider_status"],
                           "error_kind": row["error_kind"], "reply": row["reply"], **attempt})
        if row["provider_status"] in _STOPS:
            stopped = row["provider_status"]
    return {"manifest": manifest, "manifest_sha256": _digest(manifest),
            "started_at": started, "finished_at": _utc_now(),
            "requests": ledger["requests"], "stopped_on": stopped,
            "spend": {"requests_sent": ledger["sent"],
                      "measured_cost_usd": round(ledger["measured"], 6),
                      "measured_cost_complete": ledger["measured_complete"],
                      "conservative_bound_usd": round(ledger["committed"], 6),
                      "ceiling_usd": CAMPAIGN_CEILING_USD},
            "rows": rows}


# ─────────────────────────────────────────────────────────────────────────────
# After the run: report binding, review items and the pre-registered verdict
# ─────────────────────────────────────────────────────────────────────────────
def _check_report(report, authorized_manifest_sha256, journal_lines):
    """The report must be the authorized campaign-02 run, well formed, with every
    attempted row equal to its fsynced journal record. Refused, never crashed."""
    manifest = report.get("manifest") if isinstance(report, dict) else None
    if not isinstance(manifest, dict) or report.get("manifest_sha256") != _digest(manifest):
        raise PackError("report manifest does not match its digest")
    if not (isinstance(authorized_manifest_sha256, str)
            and authorized_manifest_sha256 == report["manifest_sha256"]):
        raise PackError("report is not the authorized run")
    if manifest != run_manifest(manifest.get("code_revision"), manifest.get("model")):
        raise PackError("report is not bound to this pack, prompt and pre-registration")
    cases, _refs = ho.load_heldout()
    rows = report.get("rows")
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        raise PackError("report rows are malformed")
    if [r.get("case_id") for r in rows] != [c["case_id"] for c in cases]:
        raise PackError("report rows are not the pinned cases in order")
    attempted = []
    for r in rows:
        status = r.get("provider_status")
        if status not in _PROVIDER_STATUSES:
            raise PackError("report row status is malformed")
        if status == P_NOT_ATTEMPTED:
            if set(r) != _ROW_KEYS or r["reply"] is not None:
                raise PackError("report row is malformed")
            continue
        if set(r) != _ROW_KEYS | {"attempt"} or not isinstance(r["attempt"], dict):
            raise PackError("report row is malformed")
        if (r["reply"] is None) == (status == P_RESPONDED):
            raise PackError("report row reply does not match its status")
        attempted.append(c01._canonical({"event": "attempt", "case_id": r["case_id"],
                                         "provider_status": status,
                                         "error_kind": r["error_kind"], "reply": r["reply"],
                                         **r["attempt"]}))
    if report.get("requests") != len(attempted):
        raise PackError("report request count does not match its rows")
    try:
        if not all(isinstance(line, str) for line in journal_lines):
            raise PackError("journal is unreadable")
        records = [json.loads(line) for line in journal_lines if line.strip()]
    except (TypeError, ValueError):
        raise PackError("journal is unreadable")
    if not all(isinstance(x, dict) for x in records):
        raise PackError("journal is malformed")
    journalled = [x for x in records if x.get("event") == "attempt"]
    reserved = [x for x in records if x.get("event") == "reserved"]
    if journalled != attempted or len(reserved) != len(attempted):
        raise PackError("report rows do not match the run journal")


def score_report(report):
    cases, refs = ho.load_heldout()
    by_id = {c["case_id"]: c for c in cases}
    scored, replies = [], {}
    for row in report["rows"]:
        reply = row["reply"] if row["provider_status"] == P_RESPONDED else None
        replies[row["case_id"]] = reply
        scored.append(ev.score_case(reply, by_id[row["case_id"]]["idea_text"],
                                    refs[row["case_id"]]))
    return scored, replies


def review_items(report, authorized_manifest_sha256, journal_lines):
    _check_report(report, authorized_manifest_sha256, journal_lines)
    scored, replies = score_report(report)
    return dict(ev.review_items(scored, ho.load_heldout(), replies),
                report_sha256=_digest(report))


def aggregate(report, assessment, authorized_manifest_sha256, journal_lines):
    """INCOMPLETE for any provider stop or case not attempted (the frozen rule
    also gives INCOMPLETE for any case without a reply); otherwise the frozen
    held-out decision rule over an assessment bound to this exact report."""
    _check_report(report, authorized_manifest_sha256, journal_lines)
    if any(r["provider_status"] in _STOPS + (P_NOT_ATTEMPTED,) for r in report["rows"]):
        return {"verdict": "INCOMPLETE", "stopped_on": report.get("stopped_on"),
                "manifest_sha256": report["manifest_sha256"]}
    judged = None
    if assessment is not None:
        if not isinstance(assessment, dict) or assessment.get("report_sha256") != _digest(report):
            raise PackError("assessment is not bound to this report")
        judged = {k: v for k, v in assessment.items() if k != "report_sha256"}
    scored, _replies = score_report(report)
    _cases, refs = ho.load_heldout()
    decision = ho.decide(scored, refs, ho.baseline()["integrated_recall"], judged)
    return dict(decision, manifest_sha256=report["manifest_sha256"],
                report_sha256=_digest(report), spend=report.get("spend"))


def plan():
    cases, _refs = ho.load_heldout()
    return {"campaign_id": CAMPAIGN_ID, "cases": len(cases), "model": MODEL,
            "endpoint": toa.ENDPOINT, "price_verified": c01.price_verified(),
            "budget": budget_plan(cases), "preregistration_sha256": ho.preregistration_digest(),
            "candidate_instructions_sha256": _sha(v2c.candidate_instructions()),
            "authorized_manifest": "named by the Owner at run time; none committed",
            "payload_preview": payload(cases[0])}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--provider", choices=("none", "openai"), default="none")
    p.add_argument("--allow-network", action="store_true")
    p.add_argument("--managed-credential", action="store_true")
    p.add_argument("--manifest", action="store_true")
    p.add_argument("--review-items", metavar="REPORT")
    p.add_argument("--aggregate", metavar="ASSESSMENT")
    p.add_argument("--report", metavar="REPORT")
    p.add_argument("--journal", metavar="JOURNAL", default=JOURNAL_PATH)
    p.add_argument("--authorized-manifest", metavar="SHA256",
                   default=AUTHORIZED_RUN_MANIFEST_SHA256)
    a = p.parse_args(argv)
    try:
        if a.manifest:
            manifest = run_manifest(current_revision(), MODEL)
            out = {"manifest": manifest, "manifest_sha256": _digest(manifest),
                   "price_verified": c01.price_verified()}
        elif a.review_items:
            with open(a.review_items, encoding="utf-8") as fh:
                report = json.load(fh)
            with open(a.journal, encoding="utf-8") as fh:
                out = review_items(report, a.authorized_manifest, fh.readlines())
        elif a.aggregate:
            if not a.report:
                raise PackError("--aggregate needs --report")
            with open(a.report, encoding="utf-8") as fh:
                report = json.load(fh)
            with open(a.aggregate, encoding="utf-8") as fh:
                assessment = json.load(fh)
            with open(a.journal, encoding="utf-8") as fh:
                out = aggregate(report, assessment, a.authorized_manifest, fh.readlines())
        elif a.provider == "openai":
            if not (a.allow_network and a.managed_credential):
                raise PackError("network and managed credential required")
            cases, _refs = ho.load_heldout()
            manifest = run_manifest(current_revision(), MODEL)
            # Every boundary BEFORE an adapter or transport exists.
            check_campaign_boundary(cases, manifest, a.authorized_manifest)
            adapter = OpenAIMsnlAdapter(  # pragma: no cover  (needs the Owner-named digest)
                allow_network=True, model=MODEL,
                transport=RecordingTransport(toa._urllib_transport))
            out = campaign(adapter, cases, manifest, None,  # pragma: no cover
                           a.authorized_manifest)
            with open(REPORT_PATH, "x", encoding="utf-8") as fh:  # pragma: no cover
                fh.write(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
        else:
            out = plan()
    except PackError as exc:
        print(json.dumps({"refused": str(exc)}))
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
