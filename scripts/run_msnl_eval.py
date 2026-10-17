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
    `--show-cases` (print per-case predictions for human review).
    There is NO option for a file, project, session, account, database or
    free-form input: both pack paths are fixed and their SHA-256 values are
    pinned, so this harness cannot transmit anything but committed synthetic
    material.
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


def main(argv=None):
    p = argparse.ArgumentParser(description="MSNL synthetic LLM feasibility harness")
    p.add_argument("--provider", choices=("lexical", "openai"), default="lexical")
    p.add_argument("--allow-network", action="store_true")
    p.add_argument("--managed-credential", action="store_true")
    p.add_argument("--show-cases", action="store_true")
    args = p.parse_args(argv)
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
