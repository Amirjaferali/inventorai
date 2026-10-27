"""MSNL synthetic LLM feasibility — developer-run evaluation harness.

File-creation contract:
  Path: scripts/run_msnl_eval.py
  Purpose: run the COMMITTED synthetic MSNL packs through the existing lexical
    baseline and, optionally, ONE evaluation-only LLM adapter, and print
    deterministic evidence-collection metrics side by side:
      * `tests/fixtures/msnl_evaluation_pack_v1.json` — governed concept
        proposals, scored by the pack's own reusable harness
        (`tests/test_msnl_evaluation_pack.py`: `run_pack` / `report`) through
        the unchanged local policy `engine.msnl_shadow.evaluate`;
      * `tests/fixtures/msnl_unknown_probe_v1.json` — explicit-unknown
        recognition, compared with the existing detector
        (`engine.progression_loop._detect_acknowledged_unknown`).
    It is not a pytest test and never runs in CI.
  Authority: Owner authorization "WAVE 1 / MSNL SYNTHETIC LLM FEASIBILITY"
    (2026-10-17): ONE bounded synthetic-only evaluation, extending the
    existing D3 synthetic-evaluation permission (OpenAI API, the D3 model) to
    MSNL for this assessment only. Not a production-provider decision.
  Input contract: ONLY these options —
    `--provider {lexical,openai}` (default `lexical`: no network, ever);
    `--allow-network` and `--managed-credential` (as in
      `scripts/run_technical_orchestration_eval.py`: the egress proxy injects
      the credential, so this process reads and sends no key);
    `--show-cases` (print per-case predictions for human review);
    `--rescore PATH` (MSNL-EVAL-02: re-score a report this harness saved with
      `--show-cases`, offline — no adapter is built and nothing is sent);
    `--responsiveness` (T2-G / R2: the ONE Owner-authorized campaign over the
      frozen, pinned `tests/fixtures/msnl_responsiveness_v1.json`; with the
      default `lexical` provider it only checks the pack and its lexical
      precondition and sends nothing);
    `--mechanism-content` (T2-G / R2 evaluation PREPARATION: the frozen, pinned
      `tests/fixtures/msnl_mechanism_content_v1.json`; with the default
      `lexical` provider it only checks the pack and its engine baseline, and
      the provider path is refused until a separate campaign authorization);
    `--mechanism-content-rescore PATH` (offline downstream replay of a saved
      mechanism-content report against the pinned pack and unchanged engine).
    There is NO option for a project, session, account, database or free-form
    input: both pack paths are fixed and their SHA-256 values are pinned, and a
    re-scored file is only read and checked against the pinned pack's labels,
    so this harness cannot transmit anything but committed synthetic material.
  Output contract: a JSON report on stdout. Exit 0 on a completed run; 2 on a
    refused invocation (no network permission, pack integrity failure).
  Prohibited behaviors: no real inventor / project / invention / personal
    data; no product import of this module (it lives under scripts/, outside
    every engine / web / API path); no persistence or logging of prompts or
    responses; the credential is never read or printed; no acceptance
    threshold and no production-pass score — evidence collection only. The one
    exception is `--responsiveness`, which applies the acceptance criteria
    FROZEN in that pack (read from the pinned bytes, never from this file) and,
    as the pack's own EV criterion requires, prints each case's parsed verdict
    and quote (synthetic material only; never the prompt or the raw reply). An LLM
    proposal here changes no engineering state, progression, evidence, domain
    activation, persistence or product behaviour.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from fractions import Fraction

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from engine import msnl_shadow as ms  # noqa: E402
from engine import semantic_registry  # noqa: E402
from engine import technical_orchestration_openai as toa  # noqa: E402

CONCEPT_PACK_PATH = os.path.join(_ROOT, "tests", "fixtures", "msnl_evaluation_pack_v1.json")
CONCEPT_PACK_SHA256 = "e9bf685038f6818dac4289479dc6aa03810d83b09b9ae747da9c04f10b5f657b"
UNKNOWN_PACK_PATH = os.path.join(_ROOT, "tests", "fixtures", "msnl_unknown_probe_v1.json")
UNKNOWN_PACK_SHA256 = "88624b67848d4e3189ff6c6334431336d63dc0df6272dd7a0f1dcebbea5ad19d"
VARIETIES = ("en", "ar-msa", "ar-gulf-kw", "ar-egy")
EXPLICIT_UNKNOWN = "EXPLICIT_UNKNOWN"
NOT_UNKNOWN = "NOT_UNKNOWN"
MAX_OUTPUT_TOKENS = 2000

CONCEPT_INSTRUCTIONS = (
    "You support a deterministic engineering-interview product. You receive ONE short "
    "answer an inventor typed, in English or Arabic (Modern Standard Arabic or a "
    "dialect such as Gulf/Kuwaiti or Egyptian), and the closed list of governed "
    "concept ids for the question area it was given in, each with the governed "
    "question it comes from and English example wordings. Return the concept ids "
    "whose meaning the answer itself positively and clearly states as an affirmed "
    "description of the idea. Rules: use only ids from the list and never invent one. "
    "Return ABSTAIN when the answer denies or negates the concept, is vague or "
    "non-committal, is only hypothetical, or could fit several concepts without one "
    "being clearly stated. Return NO_MAPPING when the answer expresses none of the "
    "listed concepts (for example a part number or a topic of another question area). "
    "Return PROPOSED with the ids otherwise. Output only the JSON object.")

UNKNOWN_INSTRUCTIONS = (
    "You support a deterministic engineering-interview product. You receive ONE short "
    "statement an inventor typed, in English or Arabic (Modern Standard Arabic or a "
    "dialect such as Gulf/Kuwaiti or Egyptian). Return EXPLICIT_UNKNOWN when the writer "
    "explicitly says that they themselves do not know, or are not sure about, some part "
    "of their idea. Return NOT_UNKNOWN for confident knowledge, a plain description, or "
    "a technical quantity that is merely called unknown. Return ABSTAIN when you cannot "
    "tell. Output only the JSON object.")


class PackError(ValueError):
    pass


def _load(path, sha256):
    with open(path, "rb") as fh:
        raw = fh.read()
    if hashlib.sha256(raw).hexdigest() != sha256:
        raise PackError("pack integrity failure: " + os.path.basename(path))
    return json.loads(raw.decode("utf-8"))


def _gloss(concept_id):
    concept = next(c for c in semantic_registry.CONCEPTS if c.concept_id == concept_id)
    return [surface for surface, _mode in concept.en_surfaces]


def concept_payload(request, model=toa.MODEL):
    """The exact provider body for one MSNL ShadowRequest. The id enum is the
    request's own registry-derived candidate set; the local policy
    (`msnl_shadow.evaluate`) re-checks every returned id anyway."""
    ids = [c.concept_id for c in request.candidates]
    schema = {
        "type": "object",
        "properties": {
            "outcome": {"type": "string", "enum": [ms.PROPOSED, ms.ABSTAIN, ms.NO_MAPPING]},
            "concept_ids": {"type": "array", "items": {"type": "string", "enum": ids}},
        },
        "required": ["outcome", "concept_ids"],
        "additionalProperties": False,
    }
    body = {"answer": request.accepted_text, "question_area": request.gap_type,
            "candidates": [{"concept_id": c.concept_id, "governed_question": c.provenance,
                            "english_examples": _gloss(c.concept_id)}
                           for c in request.candidates]}
    return {"model": model, "instructions": CONCEPT_INSTRUCTIONS,
            "input": json.dumps(body, ensure_ascii=False, sort_keys=True),
            "store": False, "max_output_tokens": MAX_OUTPUT_TOKENS,
            "text": {"format": {"type": "json_schema", "name": "msnl_concepts",
                                "strict": True, "schema": schema}}}


def unknown_payload(text, model=toa.MODEL):
    schema = {"type": "object",
              "properties": {"outcome": {"type": "string",
                                         "enum": [EXPLICIT_UNKNOWN, NOT_UNKNOWN, ms.ABSTAIN]}},
              "required": ["outcome"], "additionalProperties": False}
    return {"model": model, "instructions": UNKNOWN_INSTRUCTIONS,
            "input": json.dumps({"statement": text}, ensure_ascii=False),
            "store": False, "max_output_tokens": MAX_OUTPUT_TOKENS,
            "text": {"format": {"type": "json_schema", "name": "msnl_unknown",
                                "strict": True, "schema": schema}}}


class OpenAIMsnlAdapter:
    """Evaluation-only MSNL adapter over the D3-approved OpenAI transport.

    Off unless ``allow_network=True``; managed-proxy credential only (no key is
    read or sent). Every failure is ``ERROR`` with a category in
    ``last_error_kind``; a refusal is ``ABSTAIN``. Implements the MSNL adapter
    protocol (``propose``) plus ``classify_unknown`` for the probe."""

    def __init__(self, *, allow_network=False, transport=None, model=toa.MODEL,
                 timeout=toa.TIMEOUT_SECONDS):
        self._allow_network = allow_network is True
        self._transport = transport or toa._urllib_transport
        self._model = model
        self._timeout = timeout
        self.name = "openai:" + model
        self.last_error_kind = None
        self.errors = {}

    def _fail(self, kind):
        self.last_error_kind = kind
        self.errors[kind] = self.errors.get(kind, 0) + 1
        return None

    def _call(self, payload):
        """The parsed JSON reply, ``ms.ABSTAIN`` for a refusal, or None."""
        self.last_error_kind = None
        if not self._allow_network:
            return self._fail(toa.ERR_NETWORK_NOT_ALLOWED)
        try:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            status, raw = self._transport(toa.ENDPOINT,
                                          {"Content-Type": "application/json"},
                                          body, self._timeout)
        except Exception:
            return self._fail(toa.ERR_TRANSPORT)
        if status != 200:
            return self._fail(toa.ERR_HTTP_STATUS)
        try:
            text = toa._output_text(json.loads(raw.decode("utf-8")))
        except LookupError:
            return self._fail(toa.ERR_INCOMPLETE)
        except Exception:
            return self._fail(toa.ERR_MALFORMED)
        if text == toa.ABSTAIN:
            return ms.ABSTAIN
        try:
            return json.loads(text)
        except Exception:
            return self._fail(toa.ERR_MALFORMED)

    def propose(self, request):
        reply = self._call(concept_payload(request, self._model))
        if reply is None:
            return ms.ShadowResponse(ms.ERROR)
        if reply == ms.ABSTAIN:
            return ms.ShadowResponse(ms.ABSTAIN)
        try:
            if set(reply) != {"outcome", "concept_ids"}:
                raise ValueError("shape")
            outcome = reply["outcome"]
            ids = tuple(reply["concept_ids"]) if outcome == ms.PROPOSED else ()
            return ms.ShadowResponse(outcome, ids)
        except Exception:
            self._fail(toa.ERR_MALFORMED)
            return ms.ShadowResponse(ms.ERROR)

    def classify_unknown(self, text):
        reply = self._call(unknown_payload(text, self._model))
        if reply is None:
            return ms.ERROR
        if reply == ms.ABSTAIN:
            return ms.ABSTAIN
        outcome = reply.get("outcome") if isinstance(reply, dict) else None
        if outcome not in (EXPLICIT_UNKNOWN, NOT_UNKNOWN, ms.ABSTAIN):
            self._fail(toa.ERR_MALFORMED)
            return ms.ERROR
        return outcome


class LexicalUnknownBaseline:
    """The existing explicit-unknown detector, unchanged."""

    name = "existing-acknowledged-unknown-detector"

    def classify_unknown(self, text):
        from engine.progression_loop import _detect_acknowledged_unknown
        return (EXPLICIT_UNKNOWN if _detect_acknowledged_unknown(text, None, 0) is not None
                else NOT_UNKNOWN)


def _ratio(num, den):
    return None if den == 0 else round(num / den, 4)


def unknown_report(classifier, pack):
    rows = []
    for case in pack["cases"]:
        got = classifier.classify_unknown(case["text"])
        rows.append({"case_id": case["case_id"], "variety": case["variety"],
                     "expected": case["expectation"], "predicted": got})

    def agg(sub):
        unknown = [r for r in sub if r["expected"] == EXPLICIT_UNKNOWN]
        other = [r for r in sub if r["expected"] == NOT_UNKNOWN]
        return {"cases": len(sub),
                "correct": sum(r["predicted"] == r["expected"] for r in sub),
                "explicit_unknown_recognized": "%d/%d" % (
                    sum(r["predicted"] == EXPLICIT_UNKNOWN for r in unknown), len(unknown)),
                "false_unknown": sum(r["predicted"] == EXPLICIT_UNKNOWN for r in other),
                "abstained": sum(r["predicted"] == ms.ABSTAIN for r in sub),
                "errors": sum(r["predicted"] == ms.ERROR for r in sub)}
    return {"classifier": getattr(classifier, "name", "unnamed"),
            "overall": agg(rows),
            "by_variety": {v: agg([r for r in rows if r["variety"] == v]) for v in VARIETIES},
            "cases": rows}


# ─── MSNL-EVAL-02: one result at three grains ───────────────────────────────
GRAINS = ("concept", "governed_question", "gap")
GRAIN_MEASURE = (
    "AFFIRMED concept attribution against the pack's fixed labels, at three grains "
    "of the same governed concepts: the registry concept, its governed question "
    "(provenance) and its owning gap. A negated, vague or merely relevant answer "
    "is labelled with no concept, so no grain here measures gap relevance as "
    "engine.gap_relevance.addresses_gap decides it, and none qualifies a "
    "relevance, progression or product use. A coarser grain never hides a "
    "concept-level error: concept_errors_beneath counts its cases.")
_CONCEPTS_BY_ID = {c.concept_id: c for c in semantic_registry.CONCEPTS}


def _unit(concept_id, grain):
    concept = _CONCEPTS_BY_ID.get(concept_id)
    if concept is None:
        raise PackError("unregistered concept id: " + str(concept_id))
    if grain == "concept":
        return concept_id
    if grain == "gap":
        return concept.owner
    return concept.provenance.split(" ", 1)[0]       # e.g. MECHANISM_COMPLETENESS/Q2


def grain_report(rows):
    """Score rows ({variety, expected, predicted, disposition}) at every grain.

    Per grain and variety: `hits` = expected units all proposed (MATCH cases);
    `false_attributions` = cases proposing a unit not expected; abstentions,
    no-mapping, discarded-unsupported and adapter errors stay separate counts
    (an error is never an abstention). At the coarser grains,
    `concept_errors_beneath` counts cases that are not false at that grain but
    carry a concept-level false attribution."""
    def agg(sub, grain):
        out = {"cases": len(sub), "match_cases": 0, "hits": 0, "exact": 0,
               "false_attributions": 0, "abstained": 0, "no_mapping": 0,
               "discarded_unsupported": 0, "errors": 0}
        if grain != "concept":
            out["concept_errors_beneath"] = 0
        for row in sub:
            expected = {_unit(i, grain) for i in row["expected"]}
            predicted = {_unit(i, grain) for i in row["predicted"]}
            if expected:
                out["match_cases"] += 1
                out["hits"] += expected <= predicted
            out["exact"] += predicted == expected
            false = bool(predicted - expected)
            out["false_attributions"] += false
            if (grain != "concept" and not false
                    and set(row["predicted"]) - set(row["expected"])):
                out["concept_errors_beneath"] += 1
            disposition = row["disposition"]
            out["abstained"] += disposition == ms.DISPOSITION_ABSTAINED
            out["no_mapping"] += disposition == ms.DISPOSITION_NO_MAPPING
            out["discarded_unsupported"] += (
                disposition == ms.DISPOSITION_DISCARDED_UNSUPPORTED)
            out["errors"] += disposition == ms.DISPOSITION_ADAPTER_ERROR
        return out
    report_ = {"measures": GRAIN_MEASURE}
    for grain in GRAINS:
        by = {"overall": agg(rows, grain)}
        by.update({v: agg([r for r in rows if r["variety"] == v], grain)
                   for v in VARIETIES})
        report_[grain] = by
    return report_


def rescore(path):
    """Re-score a saved `--show-cases` report offline. Every saved case must
    exist in the pinned concept pack with the identical fixed label; no adapter
    is constructed and nothing is sent."""
    pack = _load(CONCEPT_PACK_PATH, CONCEPT_PACK_SHA256)
    by_id = {c["case_id"]: c for c in pack["cases"]}
    with open(path, "rb") as fh:
        raw = fh.read()
    saved = json.loads(raw.decode("utf-8"))
    if saved.get("concept_pack") != pack["pack_id"]:
        raise PackError("saved report is not for " + pack["pack_id"])
    out = {"rescored_sha256": hashlib.sha256(raw).hexdigest(),
           "concept_pack": pack["pack_id"], "concepts": {}}
    for name, by in saved.get("concepts", {}).items():
        cases = by.get("cases")
        if not cases:
            raise PackError("saved report has no per-case rows (use --show-cases)")
        rows = []
        for case in cases:
            fixed = by_id.get(case.get("case_id"))
            if fixed is None or sorted(case["expected"]) != sorted(fixed["expected_concepts"]):
                raise PackError("saved case does not match the pinned pack: "
                                + str(case.get("case_id")))
            rows.append({"variety": fixed["variety"], "expected": case["expected"],
                         "predicted": case["predicted"],
                         "disposition": case["disposition"]})
        if len(rows) != len(by_id) or len({c["case_id"] for c in cases}) != len(by_id):
            raise PackError("saved report does not cover every pack case exactly once")
        out["concepts"][name] = {"grains": grain_report(rows)}
    return out


def run(provider, allow_network, managed_credential, show_cases=False):
    concept_pack = _load(CONCEPT_PACK_PATH, CONCEPT_PACK_SHA256)
    unknown_pack = _load(UNKNOWN_PACK_PATH, UNKNOWN_PACK_SHA256)
    from tests.test_msnl_evaluation_pack import aggregate, run_pack
    adapters = [ms.LexicalBaselineAdapter()]
    classifiers = [LexicalUnknownBaseline()]
    if provider == "openai":
        if not (allow_network and managed_credential):
            raise SystemExit(2)
        llm = OpenAIMsnlAdapter(allow_network=True)
        adapters.append(llm)
        classifiers.append(llm)
    concept = {}
    for adapter in adapters:
        results = run_pack(adapter, concept_pack)
        by = {"overall": aggregate(results)}
        by.update({v: aggregate([r for r in results if r.variety == v]) for v in VARIETIES})
        by["by_category"] = {c: aggregate([r for r in results if r.category == c])
                             for c in concept_pack["categories"]}
        by["adapter_errors"] = sum(r.disposition == ms.DISPOSITION_ADAPTER_ERROR
                                   for r in results)
        by["grains"] = grain_report([
            {"variety": r.variety, "expected": sorted(r.expected),
             "predicted": sorted(r.predicted), "disposition": r.disposition}
            for r in results])
        if show_cases:
            by["cases"] = [{"case_id": r.case_id, "expected": sorted(r.expected),
                            "outcome": r.outcome, "disposition": r.disposition,
                            "predicted": sorted(r.predicted), "exact": r.exact}
                           for r in results]
        concept[adapter.name] = by
    unknown = {}
    for classifier in classifiers:
        rep = unknown_report(classifier, unknown_pack)
        if not show_cases:
            rep.pop("cases")
        unknown[rep["classifier"]] = rep
    out = {"concept_pack": concept_pack["pack_id"], "unknown_pack": unknown_pack["pack_id"],
           "concepts": concept, "unknowns": unknown}
    if provider == "openai":
        out["llm_error_kinds"] = adapters[-1].errors
    return out


# ─── T2-G / R2: served-question responsiveness (msnl-responsiveness-v1) ─────
#
# The ONE Owner-authorized campaign over the frozen PR #853 package. Everything
# that decides the outcome is read from the pinned pack bytes: the arm's
# instructions, its output enum, its input fields, the acceptance thresholds
# and the request budget. Nothing here is tuned, retried or re-run.

RESPONSIVENESS_PACK_PATH = os.path.join(_ROOT, "tests", "fixtures",
                                        "msnl_responsiveness_v1.json")
RESPONSIVENESS_PACK_SHA256 = "5e98cabdeddfd81b0f60d5d828a01fb8c347173be065554f19962e674a73c90a"
RESPONSIVE = "RESPONSIVE"
NOT_RESPONSIVE = "NOT_RESPONSIVE"
TARGET_CATEGORIES = ("PARAPHRASE", "HEDGED", "NEGATIVE_FORM")
CONTROL_CATEGORIES = ("CONTROL_UNKNOWN",)
ERR_REFUSAL = "refusal"
ERR_BUDGET = "budget_exhausted"
_WORD_RUN = re.compile(r"\w+")


def responsiveness_payload(pack, case, model=toa.MODEL):
    """The exact provider body for one case: the frozen instructions verbatim,
    the frozen closed verdict enum, and as input ONLY the case's served
    question and its text (arm.input: nothing else)."""
    schema = {"type": "object",
              "properties": {
                  "verdict": {"type": "string",
                              "enum": list(pack["arm"]["output_schema"]["verdict"])},
                  "quote": {"type": "string"}},
              "required": ["verdict", "quote"], "additionalProperties": False}
    body = {"question": case["served_question"], "answer": case["text"]}
    return {"model": model, "instructions": pack["arm"]["instructions"],
            "input": json.dumps(body, ensure_ascii=False, sort_keys=True),
            "store": False, "max_output_tokens": MAX_OUTPUT_TOKENS,
            "text": {"format": {"type": "json_schema", "name": "msnl_responsiveness",
                                "strict": True, "schema": schema}}}


def _normalised(text):
    return " ".join(semantic_registry.normalize_ar(text).split())


def quote_grounded(quote, text):
    """arm.acceptance_rule, grounding half: after the registry's normalize_ar
    and whitespace collapsing, the quote is a substring of the equally
    normalised text and holds at least two word-character runs."""
    if not isinstance(quote, str) or not isinstance(text, str):
        return False
    q = _normalised(quote)
    return len(_WORD_RUN.findall(q)) >= 2 and q in _normalised(text)


def responsiveness_accepted(verdict, quote, text):
    """arm.acceptance_rule: ACCEPTED only for a RESPONSIVE verdict whose quote
    is grounded; every other outcome is NOT ACCEPTED."""
    return verdict == RESPONSIVE and quote_grounded(quote, text)


def responsiveness_precondition(pack):
    """FR3: every case must be rejected by BOTH existing lexical relevance
    checks, so the arm is consulted for every case. Returns the case ids that
    either check now accepts (empty list = the precondition holds)."""
    from engine.gap_relevance import addresses_gap
    from engine.intent_serving import matches_committed_intent
    return [c["case_id"] for c in pack["cases"]
            if addresses_gap(c["text"], c["gap_type"])
            or matches_committed_intent(c["text"], c["question_id"])]


def classify_responsiveness(adapter, pack, case):
    """ONE provider request for ONE case. Returns (verdict, quote, error_kind):
    a valid reply gives error_kind None; a refusal, a transport / HTTP /
    incomplete / malformed reply or a schema violation gives (None, None, kind)
    — AB2 makes every one of them invalidate the run."""
    reply = adapter._call(responsiveness_payload(pack, case, adapter._model))
    if reply is None:
        return None, None, adapter.last_error_kind
    if reply == ms.ABSTAIN:                     # a provider refusal, not a verdict
        adapter.errors[ERR_REFUSAL] = adapter.errors.get(ERR_REFUSAL, 0) + 1
        return None, None, ERR_REFUSAL
    allowed = set(pack["arm"]["output_schema"]["verdict"])
    if not isinstance(reply, dict) or set(reply) != {"verdict", "quote"} \
            or reply["verdict"] not in allowed or not isinstance(reply["quote"], str):
        adapter._fail(toa.ERR_MALFORMED)
        return None, None, toa.ERR_MALFORMED
    return reply["verdict"], reply["quote"], None


def responsiveness_campaign(adapter, pack):
    """Exactly ``ST1_runs`` independent passes in pack order. The campaign stops
    before the first request that would exceed ``max_provider_requests`` and
    immediately after the first error (AB2: the run, and so the campaign, is
    invalid; nothing is retried). Returns (runs, requests)."""
    t = pack["thresholds"]
    budget = t["max_provider_requests"]
    runs, requests, stopped = [], 0, False
    for _ in range(t["ST1_runs"]):
        if stopped:
            break
        rows = []
        for case in pack["cases"]:
            if requests >= budget:
                rows.append({"case_id": case["case_id"], "verdict": None, "quote": None,
                             "grounded": False, "accepted": False, "error": ERR_BUDGET})
                stopped = True
                break
            requests += 1
            verdict, quote, err = classify_responsiveness(adapter, pack, case)
            rows.append({"case_id": case["case_id"], "verdict": verdict, "quote": quote,
                         "grounded": quote_grounded(quote, case["text"]),
                         "accepted": responsiveness_accepted(verdict, quote, case["text"]),
                         "error": err})
            if err is not None:
                stopped = True
                break
        runs.append(rows)
    return runs, requests


def _meets(num, den, minimum):
    return den > 0 and Fraction(num, den) >= Fraction(str(minimum))


def responsiveness_run_report(pack, rows):
    """Every frozen criterion for ONE run, overall and per variety, at case grain."""
    t = pack["thresholds"]
    cases = {c["case_id"]: c for c in pack["cases"]}
    errors = [r for r in rows if r["error"] is not None]
    complete = len(rows) == len(pack["cases"]) and not errors
    by = {}
    for scope in ("overall",) + VARIETIES:
        sel = [r for r in rows if scope == "overall" or cases[r["case_id"]]["variety"] == scope]
        tgt = [r for r in sel if cases[r["case_id"]]["category"] in TARGET_CATEGORIES]
        neg = [r for r in sel if cases[r["case_id"]]["label"] == NOT_RESPONSIVE]
        ctl = [r for r in sel if cases[r["case_id"]]["category"] in CONTROL_CATEGORIES]
        n_tgt = sum(cases[c]["category"] in TARGET_CATEGORIES for c in cases
                    if scope == "overall" or cases[c]["variety"] == scope)
        by[scope] = {
            "target_cases": n_tgt,
            "target_accepted": sum(r["accepted"] for r in tgt),
            "target_abstained": sum(r["verdict"] == ms.ABSTAIN for r in tgt),
            "target_not_responsive": sum(r["verdict"] == NOT_RESPONSIVE for r in tgt),
            "target_responsive_ungrounded": sum(r["verdict"] == RESPONSIVE and not r["grounded"]
                                                for r in tgt),
            "negatives_answered": len(neg),
            "false_acceptances": sum(r["verdict"] == RESPONSIVE for r in neg),
            "injection_responsive": sum(r["verdict"] == RESPONSIVE for r in neg
                                        if cases[r["case_id"]]["category"]
                                        == "INSTRUCTION_INJECTION"),
            "responsive_ungrounded": sum(r["verdict"] == RESPONSIVE and not r["grounded"]
                                         for r in sel),
            "controls": {"accepted": sum(r["accepted"] for r in ctl),
                         "abstained": sum(r["verdict"] == ms.ABSTAIN for r in ctl),
                         "rejected": sum(r["verdict"] == NOT_RESPONSIVE for r in ctl),
                         "responsive_ungrounded": sum(r["verdict"] == RESPONSIVE
                                                      and not r["grounded"] for r in ctl)},
        }
        by[scope]["recovery"] = _ratio(by[scope]["target_accepted"], n_tgt)
    o = by["overall"]
    en = Fraction(by["en"]["target_accepted"], by["en"]["target_cases"])
    parity = {v: float(en - Fraction(by[v]["target_accepted"], by[v]["target_cases"]))
              for v in VARIETIES if v != "en"}
    criteria = {
        "FA1": complete and all(by[s]["false_acceptances"] <= t["FA1_max_false_acceptances"]
                                for s in by),
        "FA2": complete and o["injection_responsive"] == 0,
        "FR1": complete and _meets(o["target_accepted"], o["target_cases"], t["FR1_overall_min"])
               and all(_meets(by[v]["target_accepted"], by[v]["target_cases"],
                              t["FR1_variety_min"]) for v in VARIETIES),
        "FR2": complete and all(
            en - Fraction(by[v]["target_accepted"], by[v]["target_cases"])
            <= Fraction(str(t["FR2_max_parity_gap"])) for v in VARIETIES if v != "en"),
        "AB1": complete and Fraction(o["target_abstained"], o["target_cases"])
               <= Fraction(str(t["AB1_max_target_abstention"])),
        "AB2": complete,
    }
    return {"valid": complete, "cases_answered": len(rows),
            "errors": [{"case_id": r["case_id"], "kind": r["error"]} for r in errors],
            "by_variety": by, "parity_gap_vs_en": parity, "criteria": criteria}


def responsiveness_agreement(pack, runs):
    """ST1 agreement: the share of non-control cases whose ACCEPTED / NOT
    ACCEPTED outcome is identical in every run (None unless all runs are
    complete)."""
    if len(runs) != pack["thresholds"]["ST1_runs"] or \
            any(len(r) != len(pack["cases"]) for r in runs):
        return None
    ids = [c["case_id"] for c in pack["cases"] if c["category"] not in CONTROL_CATEGORIES]
    per = [{r["case_id"]: r["accepted"] for r in run} for run in runs]
    same = sum(len({p[i] for p in per}) == 1 for i in ids)
    return {"identical": same, "cases": len(ids), "rate": _ratio(same, len(ids))}


def responsiveness_verdict(pack, runs, precondition_violations):
    """The frozen outcome: PASS only when every criterion holds in all three
    runs and ST1 agreement holds; anything else is FAIL. A run invalidated by
    an error is reported as INVALID and, under AB2, counts as a failed run."""
    t = pack["thresholds"]
    reports = [responsiveness_run_report(pack, rows) for rows in runs]
    agreement = responsiveness_agreement(pack, runs)
    st1 = (len(reports) == t["ST1_runs"] and all(r["valid"] for r in reports)
           and agreement is not None
           and _meets(agreement["identical"], agreement["cases"],
                      t["ST1_min_outcome_agreement"]))
    held = {k: len(reports) == t["ST1_runs"] and all(r["criteria"][k] for r in reports)
            for k in ("FA1", "FA2", "FR1", "FR2", "AB1", "AB2")}
    held["FR3"] = not precondition_violations
    held["ST1"] = st1
    invalid = any(not r["valid"] for r in reports) or len(reports) != t["ST1_runs"]
    verdict = "PASS" if all(held.values()) else "FAIL"
    return {"verdict": verdict,
            "campaign_status": "INVALID" if invalid else "COMPLETE",
            "criteria_held_in_every_run": held, "agreement": agreement, "runs": reports}


def responsiveness(provider, allow_network, managed_credential):
    """Load the pinned pack, check FR3, and (with the provider) run the ONE
    campaign. Returns the report dict; raises PackError on integrity failure."""
    pack = _load(RESPONSIVENESS_PACK_PATH, RESPONSIVENESS_PACK_SHA256)
    if pack["thresholds"]["max_provider_requests"] != \
            pack["thresholds"]["ST1_runs"] * len(pack["cases"]):
        raise PackError("responsiveness budget inconsistent with the pack")
    violations = responsiveness_precondition(pack)
    out = {"pack_id": pack["pack_id"], "pack_sha256": RESPONSIVENESS_PACK_SHA256,
           "cases": len(pack["cases"]), "precondition_violations": violations,
           "thresholds": pack["thresholds"]}
    if provider != "openai":
        out["provider_requests"] = 0
        return out
    if not (allow_network and managed_credential):
        raise SystemExit(2)
    if violations:
        out["refused"] = "FR3: the lexical precondition no longer holds; nothing was sent"
        out["provider_requests"] = 0
        return out
    adapter = OpenAIMsnlAdapter(allow_network=True)
    runs, requests = responsiveness_campaign(adapter, pack)
    out.update({"model": adapter._model, "endpoint": toa.ENDPOINT,
                "provider_requests": requests, "error_kinds": adapter.errors,
                "result": responsiveness_verdict(pack, runs, violations),
                "case_level": [[{k: r[k] for k in ("case_id", "verdict", "quote",
                                                   "grounded", "accepted", "error")}
                                for r in rows] for rows in runs]})
    return out


# ─── T2-G / R2: experimental veto-only mechanism content (msnl-mechanism-content-v1)
#
# Evaluation preparation ONLY (Owner authorization "R2 / VETO-ONLY EVALUATION
# PREPARATION"): the arm, the decision table, the RAW-span grounding contract,
# the thresholds and the budget are read from the pinned pack bytes. The
# provider path stays refused by MECHANISM_CONTENT_CAMPAIGN_AUTHORIZED until a
# separate campaign authorization changes it in a reviewed commit. The
# responsiveness arm above, including its normalised `quote_grounded`, is
# unchanged and is not used here. Composition is offline and harness-only: no
# product code is modified, nothing is persisted, and the veto can only
# withhold credit the deterministic engine would grant.

MECHANISM_PACK_PATH = os.path.join(_ROOT, "tests", "fixtures",
                                   "msnl_mechanism_content_v1.json")
MECHANISM_PACK_SHA256 = "1c6c312cb4c53c19e53e003d391d6af79a9dd76678c1973dc8e287ae90f3160c"
MECHANISM_CONTENT_CAMPAIGN_AUTHORIZED = False
MC_FIELDS = ("responsive", "stance", "mechanism_content", "quote")
MC_PRESENT, MC_ABSENT = "PRESENT", "ABSENT"
ALLOWED, WITHHELD_ABSENT, ABSTAINED = "ALLOWED", "WITHHELD_ABSENT", "ABSTAINED"
CONTRADICTORY, UNGROUNDED, MC_ERROR = "CONTRADICTORY", "UNGROUNDED", "ERROR"
_ONLY_STANCES = ("UNKNOWN_ONLY", "SUPPOSES_ONLY", "ASKS_ONLY", "REFERS_ONLY")
PRIORS = ("OPEN", "PARTIAL")


def mechanism_payload(pack, case, model=toa.MODEL):
    """The exact provider body for one case: the frozen instructions, the
    frozen enums, and as input ONLY the served question and the text. Refuses
    (PackError) a body over the frozen per-request input-size cap."""
    enums = pack["arm"]["output_schema"]
    schema = {"type": "object",
              "properties": {f: {"type": "string", "enum": list(enums[f])}
                             for f in MC_FIELDS if f != "quote"},
              "required": list(MC_FIELDS), "additionalProperties": False}
    schema["properties"]["quote"] = {"type": "string"}
    body = json.dumps({"question": case["served_question"], "answer": case["text"]},
                      ensure_ascii=False, sort_keys=True)
    if len(pack["arm"]["instructions"]) + len(body) > \
            pack["thresholds"]["max_input_characters"]:
        raise PackError("request over the frozen input-size cap: " + case["case_id"])
    return {"model": model, "instructions": pack["arm"]["instructions"],
            "input": body, "store": False,
            "max_output_tokens": pack["thresholds"]["max_output_tokens"],
            "text": {"format": {"type": "json_schema", "name": "msnl_mechanism_content",
                                "strict": True, "schema": schema}}}


def mechanism_reply_error(pack, reply):
    """None when ``reply`` satisfies the frozen schema exactly, else the error
    kind (D1). Every field must be present, no other field may appear, every
    enum value must be one of the frozen values and the quote a string."""
    enums = pack["arm"]["output_schema"]
    if not isinstance(reply, dict) or set(reply) != set(MC_FIELDS):
        return toa.ERR_MALFORMED
    if not isinstance(reply["quote"], str):
        return toa.ERR_MALFORMED
    for field in MC_FIELDS[:3]:
        if reply[field] not in enums[field]:
            return toa.ERR_MALFORMED
    return None


def classify_mechanism(adapter, pack, case):
    """ONE provider request for ONE case: (reply, error_kind). A refusal or any
    transport / HTTP / incomplete / malformed / schema failure is an error."""
    reply = adapter._call(mechanism_payload(pack, case, adapter._model))
    if reply is None:
        return None, adapter.last_error_kind
    if reply == ms.ABSTAIN:                     # a provider refusal, not a verdict
        adapter.errors[ERR_REFUSAL] = adapter.errors.get(ERR_REFUSAL, 0) + 1
        return None, ERR_REFUSAL
    kind = mechanism_reply_error(pack, reply)
    if kind is not None:
        adapter._fail(kind)
        return None, kind
    return {f: reply[f] for f in MC_FIELDS}, None


def _mc_word_present(quote, question_id):
    """G2: one non-function word outside every committed-marker occurrence."""
    from engine import answer_stance as st
    spans = st._marker_spans(quote, question_id)
    for word in st._WORD_RE.finditer(quote):
        start, end = word.span()
        if any(a <= start and end <= b for a, b in spans):
            continue
        token = word.group(0)
        if token.lower() in st._T2G2_STOPWORDS_EN or token in st._T2G2_STOPWORDS_AR:
            continue
        return True
    return False


def _mc_governing_cue(prefix, pack):
    """G5: a registered unknown, a T2-G-2 hypothetical cue or a harness negation
    cue in the clause text before the quote."""
    from engine import answer_stance as st
    if not prefix.strip():
        return False
    if st.declares_ignorance(prefix) or st._t2g2_is_hypothetical(prefix + " "):
        return True
    cues = pack["grounding"]["negation_cues"]
    lowered = prefix.lower()
    if "n't" in lowered:
        return True
    english = {w.lower() for w in re.findall(r"[A-Za-z]+", prefix)}
    if english & {c for c in cues["en"] if c != "n't"}:
        return True
    return bool({m.group(0) for m in st._WORD_RE.finditer(prefix)} & set(cues["ar"]))


def _mc_occurrence_reason(quote, text, start, question_id, pack):
    from engine import answer_stance as st
    end = start + len(quote)
    if not _mc_word_present(quote, question_id):
        return "MARKER_ONLY"
    for sentence, terminator, offset in st._sentence_records(text):
        s_end = offset + len(sentence)
        if end <= offset or start >= s_end:
            continue
        if st._t2g3_is_non_assertive(sentence, terminator):
            return "NON_ASSERTIVE"
        position, first = 0, True
        for clause in st._t2g2_clauses(sentence):
            index = sentence.find(clause, position)
            if index < 0:
                continue
            position = index + len(clause)
            c_start, c_end = offset + index, offset + index + len(clause)
            if end <= c_start or start >= c_end:
                continue
            if st.declares_ignorance(clause):
                return "INSIDE_UNKNOWN"
            if first:
                first = False
                if _mc_governing_cue(text[c_start:max(c_start, start)], pack):
                    return "STRIPPED_SCOPE"
    return None


def mc_grounding(quote, text, question_id, pack):
    """The RAW-span grounding contract (pack["grounding"], G1-G7): (grounded,
    reason). Exact verbatim occurrence only — no normalisation of any kind."""
    if not isinstance(quote, str) or not quote or not isinstance(text, str):
        return False, "NOT_FOUND"
    starts, at = [], text.find(quote)
    while at != -1:
        starts.append(at)
        at = text.find(quote, at + 1)
    if not starts:
        return False, "NOT_FOUND"
    first_reason = None
    for start in starts:
        reason = _mc_occurrence_reason(quote, text, start, question_id, pack)
        if reason is None:
            return True, None
        first_reason = first_reason or reason
    return False, first_reason


def mc_decision(pack, case, reply, error_kind=None):
    """The frozen decision table (pack["decision"], D1-D6): (decision, reason)."""
    if error_kind is not None or reply is None:
        return MC_ERROR, error_kind or toa.ERR_MALFORMED
    content, stance = reply["mechanism_content"], reply["stance"]
    responsive, quote = reply["responsive"], reply["quote"]
    if (content == MC_PRESENT and (responsive != RESPONSIVE or stance in _ONLY_STANCES)) \
            or (content != MC_PRESENT and quote != ""):
        return CONTRADICTORY, None
    if content == ms.ABSTAIN or responsive == ms.ABSTAIN:
        return ABSTAINED, None
    if content == MC_ABSENT:
        return WITHHELD_ABSENT, None
    grounded, reason = mc_grounding(quote, case["text"], case["question_id"], pack)
    return (ALLOWED, None) if grounded else (UNGROUNDED, reason)


def mc_engine_outcome(pack, case, prior):
    """The deterministic engine outcome for one case from one prior state, at
    the served index (offline; a fresh state; nothing persisted)."""
    from engine.idea_state import (Evidence, Gap, IdeaState, ASSERTED,
                                   MECHANISM_COMPLETENESS, OWNER_STATED)
    from engine.intent_serving import w2c_served_question
    from engine.path_n_questions import get_served_question
    from engine.progression_loop import integrate_response
    replay = pack["replay"]
    state = IdeaState(idea_id="mc-eval")
    state.domain, state.path = case["domain"], "N"
    state.engine_contract_version = replay["engine_contract_version"]
    state.maturity_level = 1
    state.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=prior, opened_at=0,
                          iterations_open=case["served_index"]))
    if prior == "PARTIAL":
        state.known_mechanism = Evidence(content=replay["prior_partial_text"],
                                         quality=ASSERTED, iteration=0,
                                         provenance=OWNER_STATED)
    served = get_served_question(MECHANISM_COMPLETENESS, case["served_index"],
                                 domain=case["domain"])
    unadjusted = (served is not None and served.question_id == case["question_id"]
                  and w2c_served_question(state, MECHANISM_COMPLETENESS) is None)
    before = state.get_gap(MECHANISM_COMPLETENESS).status
    integrate_response(state, MECHANISM_COMPLETENESS, case["served_question"], case["text"])
    after = state.get_gap(MECHANISM_COMPLETENESS).status
    mechanism = state.known_mechanism
    set_by_answer = mechanism is not None and mechanism.content == case["text"]
    order = {"OPEN": 0, "PARTIAL": 1, "CLOSED": 2}
    return {"unadjusted": unadjusted, "status_before": before, "status_after": after,
            "mechanism_set_by_answer": set_by_answer,
            "granted": order.get(after, -1) > order.get(before, -1) or set_by_answer}


def mc_baseline(pack, case):
    return {prior: mc_engine_outcome(pack, case, prior) for prior in PRIORS}


def mc_precondition(pack):
    """VB1: case ids whose recomputed engine baseline differs from the frozen
    one, is not GRANTED from both priors, or is not an unadjusted context."""
    bad = []
    for case in pack["cases"]:
        got = mc_baseline(pack, case)
        frozen = case.get("engine_baseline")
        ok = all(got[p]["unadjusted"] and got[p]["granted"] for p in PRIORS) and \
            frozen == {p: got[p]["status_after"] for p in PRIORS}
        if not ok:
            bad.append(case["case_id"])
    return bad


def mc_composed(baseline, decision):
    """D7: the engine outcome when ALLOWED, the prior state otherwise."""
    out = {}
    for prior in PRIORS:
        engine = baseline[prior]
        if decision == ALLOWED:
            out[prior] = {"status_after": engine["status_after"],
                          "granted": engine["granted"]}
        else:
            out[prior] = {"status_after": engine["status_before"], "granted": False}
    return out


def mc_row(pack, case, reply, error_kind, baseline):
    decision, reason = mc_decision(pack, case, reply, error_kind)
    return {"case_id": case["case_id"], "reply": reply, "error": error_kind,
            "decision": decision, "grounding_reason": reason,
            "engine": {p: {k: baseline[p][k] for k in ("status_before", "status_after",
                                                       "mechanism_set_by_answer", "granted")}
                       for p in PRIORS},
            "composed": None if decision == MC_ERROR else mc_composed(baseline, decision)}


def mechanism_campaign(adapter, pack):
    """Exactly VS1_runs passes in pack order; stops before a request over the
    frozen budget and immediately after the first error (VE1: nothing is
    retried). Returns (runs, requests)."""
    t = pack["thresholds"]
    baselines = {c["case_id"]: mc_baseline(pack, c) for c in pack["cases"]}
    runs, requests, stopped = [], 0, False
    for _ in range(t["VS1_runs"]):
        if stopped:
            break
        rows = []
        for case in pack["cases"]:
            if requests >= t["max_provider_requests"]:
                rows.append(mc_row(pack, case, None, ERR_BUDGET, baselines[case["case_id"]]))
                stopped = True
                break
            requests += 1
            reply, err = classify_mechanism(adapter, pack, case)
            rows.append(mc_row(pack, case, reply, err, baselines[case["case_id"]]))
            if err is not None:
                stopped = True
                break
        runs.append(rows)
    return runs, requests


def mechanism_run_report(pack, rows):
    """Every frozen criterion for ONE run, overall and per variety, at case grain."""
    t = pack["thresholds"]
    cases = {c["case_id"]: c for c in pack["cases"]}
    errors = [r for r in rows if r["decision"] == MC_ERROR]
    complete = len(rows) == len(pack["cases"]) and not errors
    by = {}
    for scope in ("overall",) + VARIETIES:
        sel = [r for r in rows if scope == "overall" or cases[r["case_id"]]["variety"] == scope]
        pos = [r for r in sel if cases[r["case_id"]]["label"] == MC_PRESENT]
        neg = [r for r in sel if cases[r["case_id"]]["label"] == MC_ABSENT]
        n_pos = sum(c["label"] == MC_PRESENT for c in cases.values()
                    if scope == "overall" or c["variety"] == scope)
        decisions = {d: {"present": sum(r["decision"] == d for r in pos),
                         "absent": sum(r["decision"] == d for r in neg)}
                     for d in (ALLOWED, WITHHELD_ABSENT, ABSTAINED, CONTRADICTORY,
                               UNGROUNDED, MC_ERROR)}
        reasons = {}
        for r in sel:
            if r["decision"] == UNGROUNDED:
                reasons[r["grounding_reason"]] = reasons.get(r["grounding_reason"], 0) + 1
        by[scope] = {
            "present_cases": n_pos, "decisions": decisions, "ungrounded_reasons": reasons,
            "raw_present_on_absent": sum((r["reply"] or {}).get("mechanism_content")
                                         == MC_PRESENT for r in neg),
            "false_grants": sum(r["composed"][p]["granted"] for r in neg
                                if r["composed"] for p in PRIORS),
            "injection_allowed": sum(r["decision"] == ALLOWED for r in neg
                                     if cases[r["case_id"]]["category"]
                                     == "INSTRUCTION_INJECTION"),
            "preserved": decisions[ALLOWED]["present"],
            "preservation": _ratio(decisions[ALLOWED]["present"], n_pos),
        }
    o = by["overall"]
    en = Fraction(by["en"]["preserved"], by["en"]["present_cases"])
    criteria = {
        "VC1": complete and all(by[s]["false_grants"] <= t["VC1_max_false_grants"]
                                for s in by),
        "VC2": complete and o["injection_allowed"] == 0,
        "VP1": complete and _meets(o["preserved"], o["present_cases"], t["VP1_overall_min"])
               and all(_meets(by[v]["preserved"], by[v]["present_cases"],
                              t["VP1_variety_min"]) for v in VARIETIES),
        "VP2": complete and all(
            en - Fraction(by[v]["preserved"], by[v]["present_cases"])
            <= Fraction(str(t["VP2_max_parity_gap"])) for v in VARIETIES if v != "en"),
        "VA1": complete and Fraction(o["decisions"][ABSTAINED]["present"], o["present_cases"])
               <= Fraction(str(t["VA1_max_positive_abstention"])),
        "VE1": complete,
    }
    return {"valid": complete, "cases_answered": len(rows),
            "errors": [{"case_id": r["case_id"], "kind": r["error"]} for r in errors],
            "by_variety": by, "criteria": criteria}


def mechanism_agreement(pack, runs):
    if len(runs) != pack["thresholds"]["VS1_runs"] or \
            any(len(r) != len(pack["cases"]) for r in runs):
        return None
    per = [{r["case_id"]: r["decision"] == ALLOWED for r in run} for run in runs]
    ids = [c["case_id"] for c in pack["cases"]]
    same = sum(len({p[i] for p in per}) == 1 for i in ids)
    return {"identical": same, "cases": len(ids), "rate": _ratio(same, len(ids))}


def mechanism_verdict(pack, runs, precondition_violations):
    """PASS only when every criterion holds in all three runs, VS1 holds and the
    baseline precondition held; anything else is FAIL."""
    t = pack["thresholds"]
    reports = [mechanism_run_report(pack, rows) for rows in runs]
    agreement = mechanism_agreement(pack, runs)
    held = {k: len(reports) == t["VS1_runs"] and all(r["criteria"][k] for r in reports)
            for k in ("VC1", "VC2", "VP1", "VP2", "VA1", "VE1")}
    held["VS1"] = (len(reports) == t["VS1_runs"] and all(r["valid"] for r in reports)
                   and agreement is not None
                   and _meets(agreement["identical"], agreement["cases"],
                              t["VS1_min_outcome_agreement"]))
    held["VB1"] = not precondition_violations
    invalid = any(not r["valid"] for r in reports) or len(reports) != t["VS1_runs"]
    return {"verdict": "PASS" if all(held.values()) else "FAIL",
            "campaign_status": "INVALID" if invalid else "COMPLETE",
            "criteria_held_in_every_run": held, "agreement": agreement, "runs": reports}


def _mechanism_pack():
    pack = _load(MECHANISM_PACK_PATH, MECHANISM_PACK_SHA256)
    t = pack["thresholds"]
    if t["max_provider_requests"] != t["VS1_runs"] * len(pack["cases"]):
        raise PackError("mechanism-content budget inconsistent with the pack")
    return pack


def mechanism_content(provider, allow_network, managed_credential):
    """Load the pinned pack, check VB1 and, only when the campaign is
    authorized and the provider flags are given, run the ONE campaign."""
    pack = _mechanism_pack()
    violations = mc_precondition(pack)
    out = {"pack_id": pack["pack_id"], "pack_sha256": MECHANISM_PACK_SHA256,
           "cases": len(pack["cases"]), "precondition_violations": violations,
           "thresholds": pack["thresholds"]}
    if provider != "openai":
        out["provider_requests"] = 0
        return out
    if not MECHANISM_CONTENT_CAMPAIGN_AUTHORIZED:
        out["refused"] = "the mechanism-content campaign is not authorized; nothing was sent"
        out["provider_requests"] = 0
        return out
    if not (allow_network and managed_credential):
        raise SystemExit(2)
    if violations:
        out["refused"] = "VB1: the engine baseline no longer holds; nothing was sent"
        out["provider_requests"] = 0
        return out
    adapter = OpenAIMsnlAdapter(allow_network=True)
    runs, requests = mechanism_campaign(adapter, pack)
    out.update({"model": adapter._model, "endpoint": toa.ENDPOINT,
                "provider_requests": requests, "error_kinds": adapter.errors,
                "result": mechanism_verdict(pack, runs, violations),
                "case_level": runs})
    return out


def mechanism_rescore(path):
    """Network-free downstream replay of a SAVED campaign report: only each
    row's case id, recorded reply and error are read; every decision, grounding
    reason, engine baseline and composed outcome is recomputed from the pinned
    pack and the unchanged engine. No adapter is built and nothing is sent."""
    pack = _mechanism_pack()
    by_id = {c["case_id"]: c for c in pack["cases"]}
    with open(path, "rb") as fh:
        raw = fh.read()
    saved = json.loads(raw.decode("utf-8"))
    if saved.get("pack_id") != pack["pack_id"] or \
            saved.get("pack_sha256") != MECHANISM_PACK_SHA256:
        raise PackError("saved report is not for the pinned " + pack["pack_id"])
    baselines = {c["case_id"]: mc_baseline(pack, c) for c in pack["cases"]}
    runs = []
    for saved_rows in saved.get("case_level", []):
        rows = []
        for row in saved_rows:
            case = by_id.get(row.get("case_id"))
            if case is None:
                raise PackError("saved case is not in the pinned pack: "
                                + str(row.get("case_id")))
            reply, err = row.get("reply"), row.get("error")
            if err is None and mechanism_reply_error(pack, reply) is not None:
                raise PackError("saved reply violates the frozen schema: " + case["case_id"])
            rows.append(mc_row(pack, case, reply, err, baselines[case["case_id"]]))
        runs.append(rows)
    violations = mc_precondition(pack)
    return {"rescored_sha256": hashlib.sha256(raw).hexdigest(),
            "pack_id": pack["pack_id"], "precondition_violations": violations,
            "result": mechanism_verdict(pack, runs, violations), "case_level": runs}


def main(argv=None):
    p = argparse.ArgumentParser(description="MSNL synthetic LLM feasibility harness")
    p.add_argument("--provider", choices=("lexical", "openai"), default="lexical")
    p.add_argument("--allow-network", action="store_true")
    p.add_argument("--managed-credential", action="store_true")
    p.add_argument("--show-cases", action="store_true")
    p.add_argument("--rescore", metavar="PATH")
    p.add_argument("--responsiveness", action="store_true")
    p.add_argument("--mechanism-content", action="store_true")
    p.add_argument("--mechanism-content-rescore", metavar="PATH")
    args = p.parse_args(argv)
    if args.mechanism_content_rescore:
        if args.provider != "lexical" or args.allow_network or args.managed_credential \
                or args.mechanism_content or args.responsiveness or args.rescore:
            print(json.dumps({"refused": "--mechanism-content-rescore is offline and "
                                         "takes no other mode, provider or network option"}))
            return 2
        try:
            out = mechanism_rescore(args.mechanism_content_rescore)
        except (OSError, ValueError, KeyError, TypeError) as exc:  # PackError, bad JSON
            print(json.dumps({"refused": str(exc)}))
            return 2
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    if args.mechanism_content:
        if args.rescore or args.show_cases or args.responsiveness:
            print(json.dumps({"refused": "--mechanism-content takes no other mode"}))
            return 2
        if args.provider == "openai" and not (args.allow_network and args.managed_credential):
            print(json.dumps({"refused": "--provider openai needs --allow-network "
                                         "--managed-credential"}))
            return 2
        try:
            out = mechanism_content(args.provider, args.allow_network,
                                    args.managed_credential)
        except PackError as exc:
            print(json.dumps({"refused": str(exc)}))
            return 2
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 2 if out.get("refused") else 0
    if args.responsiveness:
        if args.rescore or args.show_cases:
            print(json.dumps({"refused": "--responsiveness takes no --rescore or "
                                         "--show-cases"}))
            return 2
        if args.provider == "openai" and not (args.allow_network and args.managed_credential):
            print(json.dumps({"refused": "--provider openai needs --allow-network "
                                         "--managed-credential"}))
            return 2
        try:
            out = responsiveness(args.provider, args.allow_network, args.managed_credential)
        except PackError as exc:
            print(json.dumps({"refused": str(exc)}))
            return 2
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 2 if out.get("refused") else 0
    if args.rescore:
        if args.provider != "lexical" or args.allow_network or args.managed_credential:
            print(json.dumps({"refused": "--rescore is offline and takes no provider "
                                         "or network option"}))
            return 2
        try:
            out = rescore(args.rescore)
        except (OSError, ValueError, KeyError, TypeError) as exc:  # PackError, bad JSON
            print(json.dumps({"refused": str(exc)}))
            return 2
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    if args.provider == "openai" and not (args.allow_network and args.managed_credential):
        print(json.dumps({"refused": "--provider openai needs --allow-network "
                                     "--managed-credential"}))
        return 2
    try:
        out = run(args.provider, args.allow_network, args.managed_credential,
                  args.show_cases)
    except PackError as exc:
        print(json.dumps({"refused": str(exc)}))
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
