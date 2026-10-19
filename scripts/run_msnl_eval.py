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
    MSNL-EVAL-03 (2026-10-19): ONE bounded synthetic evaluation of grounded,
    stated-only proposals on the frozen held-out pack.
  Input contract: ONLY these options —
    `--provider {lexical,openai}` (default `lexical`: no network, ever);
    `--allow-network` and `--managed-credential` (as in
      `scripts/run_technical_orchestration_eval.py`: the egress proxy injects
      the credential, so this process reads and sends no key);
    `--show-cases` (print per-case predictions for human review);
    `--rescore PATH` (MSNL-EVAL-02: re-score a report this harness saved with
      `--show-cases`, offline — no adapter is built and nothing is sent);
    `--holdout` (MSNL-EVAL-03: run the frozen held-out pack
      `tests/fixtures/msnl_holdout_v1.json` instead — lexical, the unmitigated
      LLM and the grounded stated-only LLM arm — and score the grounded arm
      against the pack's own frozen acceptance criteria).
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
    threshold and no production-pass score — evidence collection only. An LLM
    proposal here changes no engineering state, progression, evidence, domain
    activation, persistence or product behaviour.
"""
import argparse
import hashlib
import json
import os
import sys

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
HOLDOUT_PACK_PATH = os.path.join(_ROOT, "tests", "fixtures", "msnl_holdout_v1.json")
HOLDOUT_PACK_SHA256 = "54397e3d053a0b2ffa0da23344b7804bf27f3951929c9e475139a6a223ec8e97"
STATED = "STATED"
IMPLIED = "IMPLIED"
ERR_CIRCUIT_OPEN = "circuit_open"       # stopped after repeated provider failures
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

# MSNL-EVAL-03 grounded arm: the SAME rules as CONCEPT_INSTRUCTIONS, with the
# final "Return PROPOSED with the ids" replaced by evidence per concept. The only
# new semantics is the STATED / IMPLIED distinction itself; no concept is defined.
GROUNDED_CONCEPT_INSTRUCTIONS = CONCEPT_INSTRUCTIONS.replace(
    "Return PROPOSED with the ids otherwise. Output only the JSON object.",
    "Otherwise return PROPOSED with one proposal for every listed concept the answer "
    "might express: its id; quote, the exact words of the answer that express it, "
    "copied character for character; and basis, STATED when those quoted words "
    "themselves express that concept, IMPLIED when the concept is only suggested or "
    "inferred, or is a broader category of something the answer names (naming a "
    "particular part, sensor or battery does not state a general category such as "
    "components or power requirement). Output only the JSON object.")
assert GROUNDED_CONCEPT_INSTRUCTIONS != CONCEPT_INSTRUCTIONS

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


def grounded_payload(request, model=toa.MODEL):
    """The grounded arm's provider body: the same plain-data input as
    `concept_payload`, with one {concept_id, quote, basis} item per proposal."""
    payload = concept_payload(request, model)
    ids = [c.concept_id for c in request.candidates]
    item = {"type": "object",
            "properties": {"concept_id": {"type": "string", "enum": ids},
                           "quote": {"type": "string"},
                           "basis": {"type": "string", "enum": [STATED, IMPLIED]}},
            "required": ["concept_id", "quote", "basis"], "additionalProperties": False}
    payload["instructions"] = GROUNDED_CONCEPT_INSTRUCTIONS
    payload["text"] = {"format": {"type": "json_schema", "name": "msnl_grounded_concepts",
                                  "strict": True, "schema": {
        "type": "object",
        "properties": {
            "outcome": {"type": "string", "enum": [ms.PROPOSED, ms.ABSTAIN, ms.NO_MAPPING]},
            "proposals": {"type": "array", "items": item}},
        "required": ["outcome", "proposals"], "additionalProperties": False}}}
    return payload


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
        self._auth_failures = 0
        self._consecutive_failures = 0

    def _fail(self, kind):
        self.last_error_kind = kind
        self.errors[kind] = self.errors.get(kind, 0) + 1
        return None

    def _transport_failed(self, status=None):
        """Circuit breaker: after 2 authentication failures (401 / 403) or 3
        consecutive provider failures, no further request is sent."""
        self._consecutive_failures += 1
        self._auth_failures += status in (401, 403)

    def _call(self, payload):
        """The parsed JSON reply, ``ms.ABSTAIN`` for a refusal, or None."""
        self.last_error_kind = None
        if not self._allow_network:
            return self._fail(toa.ERR_NETWORK_NOT_ALLOWED)
        if self._auth_failures >= 2 or self._consecutive_failures >= 3:
            return self._fail(ERR_CIRCUIT_OPEN)
        try:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            status, raw = self._transport(toa.ENDPOINT,
                                          {"Content-Type": "application/json"},
                                          body, self._timeout)
        except Exception:
            self._transport_failed()
            return self._fail(toa.ERR_TRANSPORT)
        if status != 200:
            self._transport_failed(status)
            return self._fail(toa.ERR_HTTP_STATUS)
        self._consecutive_failures = 0
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


class GroundedOpenAIMsnlAdapter(OpenAIMsnlAdapter):
    """MSNL-EVAL-03 grounded, stated-only arm (evaluation only).

    Each proposal carries a quote and a STATED / IMPLIED basis. A concept is
    admitted only when it is STATED and its quote occurs verbatim in the
    answer; every other proposal is WITHHELD and recorded in `withheld` (keyed
    by the answer text) — never dropped silently. A matching quote is not proof
    that the concept is right: the unchanged local policy and the frozen labels
    still decide. If every proposal is withheld the reply is ABSTAIN."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "openai-grounded:" + self._model
        self.withheld = {}

    def propose(self, request):
        reply = self._call(grounded_payload(request, self._model))
        if reply is None:
            return ms.ShadowResponse(ms.ERROR)
        if reply == ms.ABSTAIN:
            return ms.ShadowResponse(ms.ABSTAIN)
        try:
            if not isinstance(reply, dict) or set(reply) != {"outcome", "proposals"}:
                raise ValueError("shape")
            outcome, items = reply["outcome"], reply["proposals"]
            if outcome not in (ms.PROPOSED, ms.ABSTAIN, ms.NO_MAPPING) or \
                    not isinstance(items, list):
                raise ValueError("outcome")
            if outcome != ms.PROPOSED:
                return ms.ShadowResponse(outcome)
            admitted, withheld = [], []
            for item in items:
                if (not isinstance(item, dict)
                        or set(item) != {"concept_id", "quote", "basis"}
                        or not isinstance(item["concept_id"], str)
                        or not isinstance(item["quote"], str)
                        or item["basis"] not in (STATED, IMPLIED)):
                    raise ValueError("proposal")
                quote = item["quote"].strip()
                if item["basis"] != STATED:
                    withheld.append({"concept_id": item["concept_id"], "reason": "implied"})
                elif not quote or quote not in request.accepted_text:
                    withheld.append({"concept_id": item["concept_id"], "reason": "ungrounded"})
                elif item["concept_id"] not in admitted:
                    admitted.append(item["concept_id"])
            self.withheld[request.accepted_text] = withheld
            if not admitted:
                return ms.ShadowResponse(ms.ABSTAIN)
            return ms.ShadowResponse(ms.PROPOSED, tuple(admitted))
        except Exception:
            self._fail(toa.ERR_MALFORMED)
            return ms.ShadowResponse(ms.ERROR)


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


# ─── MSNL-EVAL-03: held-out run against the frozen criteria ─────────────────
MULTI_CATEGORIES = ("MULTI_CROSS_QUESTION", "MULTI_SAME_QUESTION")
PASS, FAIL, NOT_VERIFIED = "PASS", "FAIL", "NOT VERIFIED"


def holdout_metrics(results):
    """Concept-level counts per variety and overall for one arm."""
    def agg(sub):
        match = [r for r in sub if r.expectation == "MATCH"]
        return {"cases": len(sub),
                "false_attributions": sum(r.false_attribution for r in sub),
                "match_cases": len(match),
                "hits": sum(r.expected <= r.predicted for r in match),
                "abstained_on_match": sum(r.disposition == ms.DISPOSITION_ABSTAINED
                                          for r in match),
                "no_mapping_on_match": sum(r.disposition == ms.DISPOSITION_NO_MAPPING
                                           for r in match),
                "errors": sum(r.disposition == ms.DISPOSITION_ADAPTER_ERROR for r in sub),
                "discarded_unsupported": sum(
                    r.disposition == ms.DISPOSITION_DISCARDED_UNSUPPORTED for r in sub)}
    out = {"overall": agg(results)}
    out.update({v: agg([r for r in results if r.variety == v]) for v in VARIETIES})
    multi = [r for r in results if r.category in MULTI_CATEGORIES]
    out["multi_concept_exact"] = "%d/%d" % (sum(r.exact for r in multi), len(multi))
    negation = [r for r in results if r.category == "NEGATION"]
    out["negation_clean"] = "%d/%d" % (sum(not r.predicted for r in negation), len(negation))
    as_meaning = [r for r in results if r.category == "NEGATION_AS_MEANING"]
    out["negation_as_meaning_exact"] = "%d/%d" % (sum(r.exact for r in as_meaning),
                                                  len(as_meaning))
    return out


def _num(fraction):
    return int(fraction.split("/")[0])


def holdout_criteria(lexical, plain, grounded, unknown_llm):
    """The frozen msnl-holdout-v1 criteria C1-C7 for the grounded arm (one run).

    Thresholds mirror the fixture's acceptance_criteria text verbatim. Any
    provider error invalidates the run: every criterion then reads NOT VERIFIED."""
    if grounded is None or plain is None or unknown_llm is None:
        return {"verdict": NOT_VERIFIED, "reason": "no LLM arm was run"}
    errors = (plain["overall"]["errors"] + grounded["overall"]["errors"]
              + unknown_llm["overall"]["errors"])
    if errors:
        return {"verdict": NOT_VERIFIED,
                "reason": "RUN INVALID: %d provider error(s) (C7)" % errors}
    c = {}
    scopes = VARIETIES + ("overall",)
    worse = [s for s in scopes
             if grounded[s]["false_attributions"] > lexical[s]["false_attributions"]]
    c["C1"] = {"status": FAIL if worse else PASS,
               "evidence": {s: "%d vs lexical %d" % (grounded[s]["false_attributions"],
                                                     lexical[s]["false_attributions"])
                            for s in scopes}}

    def recall(m, v):
        return m[v]["hits"] / m[v]["match_cases"]
    ok = all(recall(grounded, v) >= 0.75 and recall(grounded, v) > recall(lexical, v)
             for v in ("ar-gulf-kw", "ar-egy"))
    c["C2"] = {"status": PASS if ok else FAIL,
               "evidence": {v: "%d/%d vs lexical %d/%d" % (
                   grounded[v]["hits"], grounded[v]["match_cases"],
                   lexical[v]["hits"], lexical[v]["match_cases"])
                   for v in ("ar-gulf-kw", "ar-egy")}}
    c["C3"] = {"status": PASS if _num(grounded["multi_concept_exact"]) >= 8 else FAIL,
               "evidence": grounded["multi_concept_exact"] + " fully recovered (need 8/12)"}
    ok = (_num(grounded["negation_clean"]) == 4
          and _num(grounded["negation_as_meaning_exact"]) >= 3)
    c["C4"] = {"status": PASS if ok else FAIL,
               "evidence": "negation clean %s; negation-as-meaning exact %s (need 4/4; 3/4)" % (
                   grounded["negation_clean"], grounded["negation_as_meaning_exact"])}
    ov = unknown_llm["overall"]
    ok = ov["explicit_unknown_recognized"] == "8/8" and ov["false_unknown"] == 0
    c["C5"] = {"status": PASS if ok else FAIL,
               "evidence": "%s recognised, %d false" % (ov["explicit_unknown_recognized"],
                                                        ov["false_unknown"])}

    def abst(m):
        return m["overall"]["abstained_on_match"] / m["overall"]["match_cases"]
    c["C6"] = {"status": PASS if abst(grounded) <= abst(plain) + 0.10 + 1e-9 else FAIL,
               "evidence": "abstention on MATCH %.4f vs unmitigated %.4f (limit +0.10)" % (
                   abst(grounded), abst(plain))}
    unsupported = grounded["overall"]["discarded_unsupported"]
    c["C7"] = {"status": FAIL if unsupported else NOT_VERIFIED,
               "evidence": "%d out-of-list proposal(s), 0 provider errors; one run of "
                           "the three required" % unsupported}
    statuses = [v["status"] for v in c.values()]
    c["verdict"] = FAIL if FAIL in statuses else (
        PASS if all(s == PASS for s in statuses) else NOT_VERIFIED)
    return c


def run_holdout(provider, allow_network, managed_credential, show_cases=False):
    """Lexical, unmitigated LLM and grounded LLM on the frozen held-out pack,
    plus the unknown probe, scored against the pack's own frozen criteria."""
    pack = _load(HOLDOUT_PACK_PATH, HOLDOUT_PACK_SHA256)
    unknown_pack = _load(UNKNOWN_PACK_PATH, UNKNOWN_PACK_SHA256)
    from tests.test_msnl_evaluation_pack import run_pack
    arms = [ms.LexicalBaselineAdapter()]
    classifiers = [LexicalUnknownBaseline()]
    if provider == "openai":
        if not (allow_network and managed_credential):
            raise SystemExit(2)
        plain = OpenAIMsnlAdapter(allow_network=True)
        arms += [plain, GroundedOpenAIMsnlAdapter(allow_network=True)]
        classifiers.append(plain)      # the grounded arm leaves the unknown prompt unchanged
    texts = {c["case_id"]: c["text"] for c in pack["cases"]}
    out_arms, metrics = {}, []
    for adapter in arms:
        results = run_pack(adapter, pack)
        m = holdout_metrics(results)
        metrics.append(m)
        withheld = getattr(adapter, "withheld", None)
        arm = {"metrics": m,
               "grains": grain_report([
                   {"variety": r.variety, "expected": sorted(r.expected),
                    "predicted": sorted(r.predicted), "disposition": r.disposition}
                   for r in results])}
        if withheld is not None:
            arm["withheld"] = {"implied": sum(w["reason"] == "implied"
                                              for ws in withheld.values() for w in ws),
                               "ungrounded": sum(w["reason"] == "ungrounded"
                                                 for ws in withheld.values() for w in ws)}
        if show_cases:
            arm["cases"] = [{"case_id": r.case_id, "category": r.category,
                             "expected": sorted(r.expected), "outcome": r.outcome,
                             "disposition": r.disposition, "predicted": sorted(r.predicted),
                             "exact": r.exact,
                             **({"withheld": withheld.get(texts[r.case_id], [])}
                                if withheld is not None else {})}
                            for r in results]
        out_arms[adapter.name] = arm
    unknown = {}
    for classifier in classifiers:
        rep = unknown_report(classifier, unknown_pack)
        if not show_cases:
            rep.pop("cases")
        unknown[rep["classifier"]] = rep
    llm = len(arms) == 3
    criteria = holdout_criteria(metrics[0], metrics[1] if llm else None,
                                metrics[2] if llm else None,
                                unknown[classifiers[1].name] if llm else None)
    out = {"holdout_pack": pack["pack_id"], "unknown_pack": unknown_pack["pack_id"],
           "arms": out_arms, "unknowns": unknown, "criteria": criteria}
    if llm:
        out["llm_error_kinds"] = {a.name: a.errors for a in arms[1:]}
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="MSNL synthetic LLM feasibility harness")
    p.add_argument("--provider", choices=("lexical", "openai"), default="lexical")
    p.add_argument("--allow-network", action="store_true")
    p.add_argument("--managed-credential", action="store_true")
    p.add_argument("--show-cases", action="store_true")
    p.add_argument("--rescore", metavar="PATH")
    p.add_argument("--holdout", action="store_true")
    args = p.parse_args(argv)
    if args.rescore:
        if (args.provider != "lexical" or args.allow_network or args.managed_credential
                or args.holdout):
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
        out = (run_holdout if args.holdout else run)(
            args.provider, args.allow_network, args.managed_credential, args.show_cases)
    except PackError as exc:
        print(json.dumps({"refused": str(exc)}))
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
