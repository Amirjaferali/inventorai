"""G1-1/2 component-concept qualification — evaluation-only module (OFFLINE preparation).

File-creation contract:
  Path: scripts/run_g1_component_concept_eval.py
  Purpose: ONE bounded, synthetic-only qualification of the question Campaign 02
    did not answer: from an ordinary idea whose inventor does not know the
    components, can a model produce a PROVISIONAL functional concept — functions,
    candidate component types and their roles, conceptual relationships, missing
    information and alternatives — that keeps the inventor's statements apart from
    its own proposals, respects exclusions, claims no engineering authority and
    asks or abstains when the idea is ambiguous or not a device? It holds the
    frozen candidate instructions and output structure, the deterministic
    structural / grounding checks, the semantic-review questions, the reviewer
    assessment-record checks, the fixed decision rule, the conservative budget
    and a guarded single-run runner. It is not a pytest test and never runs in CI.
  Authority: Owner instruction "G1-1/2 COMPONENT-CONCEPT QUALIFICATION PREPARATION"
    (2026-11-05): preparation only. NO provider request is authorized. A run needs
    a separate Owner authorization naming the SHA-256 of the manifest of the exact
    clean commit that runs; nothing else opens the request path.
  What it is NOT: a product feature, a component-selection engine, a canonical
    record, a schema, persistence or a question-serving path. Nothing in engine/ or
    web/ imports it. Every proposal it scores is provisional, unverified and
    unpersisted; a PRELIMINARY_GO is qualification evidence only.
  Distinct from Campaigns 01 / 02: their scripts, packs, pre-registrations and
    evidence are imported read-only or not at all, and are never modified, replayed
    or tuned on. This evaluation has its own identity, pack, criteria, limits and
    evidence directory.
  Reuse (imported, unchanged):
    * quote grounding and normalisation: `scripts/run_msnl_eval.py`
      (`quote_grounded`, `_normalised`, `_load`, `PackError`);
    * price basis, its verification, the reservation rates, provider statuses and
      the canonical-JSON helper: `scripts/run_g1_precreation_campaign.py`;
    * adapter, measured call, model confirmation, price arithmetic:
      `scripts/run_msnl_eval.py`;
    * response recorder, refusal resolution, offline-fake marker, digest,
      clean-revision check, fsynced journal, clock: `scripts/run_proof_b_eval.py`.
    The single-run mechanics mirror `scripts/run_g1_precreation_campaign_02.py`
    (manifest, boundary, one request per case, report binding), which is bound to
    its own pack and cannot be reused without being modified.
  Independence: the candidate instructions, output structure, criteria and decision
    rule below were written and committed by the Execution Lead BEFORE the pack
    existed; the pack and its reference are authored blind in a separate session
    and adjudicated in another, prompt-blind session (recorded in the pack files).
    No instruction or criterion may be tuned on the pack afterwards.
"""
import argparse
import difflib
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
from scripts import run_g1_precreation_campaign as c01  # noqa: E402  (read only)
from scripts.run_msnl_eval import (  # noqa: E402  (reused, unchanged)
    ERR_BUDGET, ERR_COST_CEILING, ERR_COST_UNBOUNDED, ERR_MODEL_UNCONFIRMED,
    OpenAIMsnlAdapter, PackError, _load, _measured_call, _normalised, _pf_model_confirmed,
    _pf_usd, quote_grounded,
)
from scripts.run_proof_b_eval import (  # noqa: E402  (reused, unchanged)
    RecordingTransport, _digest, _journal, _offline_fake, _sentinel_kind, _utc_now,
    current_revision,
)

EVALUATION_ID = "g1-component-concept-qualification-01"
PACK_ID = "inventorai-g1-component-concept-01"
FROZEN_STATUS = "FROZEN"

# ─────────────────────────────────────────────────────────────────────────────
# The output structure and the candidate instructions (frozen before the pack)
# ─────────────────────────────────────────────────────────────────────────────
RESPONDED, ABSTAIN = "RESPONDED", "ABSTAIN"
STATED, AI_PROPOSED = "STATED", "AI_PROPOSED"
UNVERIFIED = "UNVERIFIED"
STATED_KINDS = ("FUNCTION", "COMPONENT", "CONSTRAINT", "VALUE", "CONTEXT")
RELATIONSHIP_KINDS = ("SIGNAL", "POWER", "FLOW", "MECHANICAL")
LIMITS = {"stated": 8, "functions": 8, "component_types": 10, "relationships": 12,
          "alternatives": 6, "options": 3, "missing_information": 6,
          "clarification_questions": 2, "excluded_by_inventor": 4, "item_chars": 240}
_ID = {"stated": re.compile(r"S[1-9][0-9]?"), "functions": re.compile(r"F[1-9][0-9]?"),
       "component_types": re.compile(r"C[1-9][0-9]?")}

INSTRUCTIONS = (
    "You help a person who has an idea for an invention but may not know which technologies or "
    "components it needs. Read only the idea text you are given and return one JSON object in the "
    "required schema. Write every text in the language of the idea.\n"
    "Keep two things strictly apart. stated: only what the person actually wrote, each with "
    "source_quote copied exactly from the idea (kind FUNCTION, COMPONENT, CONSTRAINT, VALUE or "
    "CONTEXT). Everything else is your proposal.\n"
    "functions: what the invention would need to do. origin STATED only when the person wrote it, "
    "with an exact source_quote; otherwise origin AI_PROPOSED with an empty source_quote. Use "
    "resolution UNRESOLVED when a function depends on information the person has not given.\n"
    "component_types: generic kinds of component that could perform the functions (for example "
    "'soil moisture sensor', not a product, model or part number), each serving one or more "
    "function ids, always attribution AI_PROPOSED and status UNVERIFIED.\n"
    "relationships: how components or functions conceptually connect, kind SIGNAL, POWER, FLOW or "
    "MECHANICAL, between existing ids. A relationship is a conceptual connection, never a claim that "
    "parts are compatible.\n"
    "alternatives: for a function where a genuinely different approach exists, up to three options. "
    "missing_information: decisions or facts the person has not given that the design depends on. "
    "clarification_questions: at most two questions a nontechnical person can answer.\n"
    "excluded_by_inventor: anything the person says the invention must not have or use, quoted "
    "exactly; never propose a component that contradicts it.\n"
    "Never invent ratings, sizes, quantities, part numbers or other specifications; quote a number "
    "only if the person wrote it. Never say or imply that anything is safe, certified, compatible, "
    "guaranteed, tested, verified or will work. If the person asks for something that cannot be "
    "promised, record it as missing information, not as achieved.\n"
    "If it is unclear what the invention is or does, ask first: give clarification_questions and do "
    "not commit to a design. If the text describes no invention to build, or only an object the "
    "person does not design, use outcome ABSTAIN with every list empty except missing_information "
    "and clarification_questions.")


def schema():
    def obj(props, required=None):
        return {"type": "object", "properties": props,
                "required": required or list(props), "additionalProperties": False}
    s = {"type": "string"}
    strings = {"type": "array", "items": s}
    return obj({
        "outcome": {"type": "string", "enum": [RESPONDED, ABSTAIN]},
        "stated": {"type": "array", "items": obj({
            "id": s, "kind": {"type": "string", "enum": list(STATED_KINDS)}, "text": s,
            "source_quote": s})},
        "functions": {"type": "array", "items": obj({
            "id": s, "text": s, "origin": {"type": "string", "enum": [STATED, AI_PROPOSED]},
            "source_quote": s,
            "resolution": {"type": "string", "enum": ["PROPOSED", "UNRESOLVED"]}})},
        "component_types": {"type": "array", "items": obj({
            "id": s, "type": s, "serves": strings,
            "attribution": {"type": "string", "enum": [AI_PROPOSED]},
            "status": {"type": "string", "enum": [UNVERIFIED]}})},
        "relationships": {"type": "array", "items": obj({
            "from": s, "to": s, "kind": {"type": "string", "enum": list(RELATIONSHIP_KINDS)}})},
        "alternatives": {"type": "array", "items": obj({"for_function": s, "options": strings})},
        "missing_information": strings,
        "clarification_questions": strings,
        "excluded_by_inventor": {"type": "array", "items": obj({"text": s, "source_quote": s})},
    })


def payload(case, model=None):
    model = model or MODEL
    return {"model": model, "instructions": INSTRUCTIONS, "input": case["idea_text"],
            "store": False, "max_output_tokens": MAX_OUTPUT_TOKENS,
            "text": {"format": {"type": "json_schema", "name": "g1_component_concept_v1",
                                "strict": True, "schema": schema()}}}


# ─────────────────────────────────────────────────────────────────────────────
# Deterministic checks (InventorAI's decision; the model's labels are not trusted)
# ─────────────────────────────────────────────────────────────────────────────
V_VALID, V_ABSTAIN, V_ERROR = "VALID", "MODEL_ABSTAIN", "ERROR"
V_STRUCTURE, V_REJECTED = "STRUCTURE_VIOLATION", "REJECTED"
# A number with a unit or percentage the inventor did not write is an invented
# specification (K3, automatic). Anything subtler is a human K3 judgment.
_UNIT_NUMBER = re.compile(
    r"(?<![\w.])(\d+(?:[.,]\d+)?)\s*(?:mm|cm|m|km|ml|l|v|mv|kv|a|ma|w|kw|mw|wh|kwh|mah|ah|"
    r"hz|khz|mhz|ghz|rpm|nm|n|kg|g|mg|bar|psi|pa|kpa|db|lm|lux|°c|°f|c\b|%|"
    r"ملم|مم|سم|متر|لتر|مل|فولت|واط|أمبير|امبير|كجم|كغ|غرام|جرام)(?![\w])",
    re.IGNORECASE)
_NUMBER_TOKEN = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?(?![\d])")
_CLAIM_HINTS = re.compile(
    r"(?i)\b(safe|safely|certified|certification|guarantee[ds]?|compatible|compatibility|"
    r"verified|tested|proven|will work|works reliably|approved)\b|"
    r"آمن|معتمد|مضمون|متوافق|مجرب|مختبر")
_ALL_KEYS = set(schema()["properties"])


def _is_text(v):
    return isinstance(v, str) and len(v) <= LIMITS["item_chars"]


def _structure_ok(reply):
    """K5: exact keys, types, limits, unique ids and resolvable references."""
    if not isinstance(reply, dict) or set(reply) != _ALL_KEYS:
        return False
    if reply["outcome"] not in (RESPONDED, ABSTAIN):
        return False
    for key in _ALL_KEYS - {"outcome"}:
        if not isinstance(reply[key], list) or len(reply[key]) > LIMITS[key]:
            return False
    item_keys = {k: set(v["items"]["properties"]) for k, v in schema()["properties"].items()
                 if k != "outcome" and v["items"].get("type") == "object"}
    for key, keys in item_keys.items():
        for item in reply[key]:
            if not isinstance(item, dict) or set(item) != keys:
                return False
    for key in ("missing_information", "clarification_questions"):
        if not all(_is_text(x) for x in reply[key]):
            return False
    ids = {}
    for key, rx in _ID.items():
        seen = [i["id"] for i in reply[key]]
        if not all(isinstance(x, str) and rx.fullmatch(x) for x in seen) or len(set(seen)) != len(seen):
            return False
        ids[key] = set(seen)
    for i in reply["stated"]:
        if i["kind"] not in STATED_KINDS or not (_is_text(i["text"]) and _is_text(i["source_quote"])):
            return False
    for f in reply["functions"]:
        if f["origin"] not in (STATED, AI_PROPOSED) or f["resolution"] not in ("PROPOSED", "UNRESOLVED") \
                or not (_is_text(f["text"]) and _is_text(f["source_quote"])):
            return False
    nodes = ids["stated"] | ids["functions"] | ids["component_types"]
    for c in reply["component_types"]:
        if not _is_text(c["type"]) or not isinstance(c["serves"], list) or not c["serves"] \
                or not all(x in ids["functions"] for x in c["serves"]) \
                or (c["attribution"], c["status"]) != (AI_PROPOSED, UNVERIFIED):
            return False
    for r in reply["relationships"]:
        if r["kind"] not in RELATIONSHIP_KINDS or r["from"] not in nodes or r["to"] not in nodes \
                or r["from"] == r["to"]:
            return False
    for a in reply["alternatives"]:
        if a["for_function"] not in ids["functions"] or not isinstance(a["options"], list) \
                or not 1 <= len(a["options"]) <= LIMITS["options"] \
                or not all(_is_text(o) for o in a["options"]):
            return False
    for e in reply["excluded_by_inventor"]:
        if not (_is_text(e["text"]) and _is_text(e["source_quote"])):
            return False
    if reply["outcome"] == ABSTAIN and any(reply[k] for k in (
            "stated", "functions", "component_types", "relationships", "alternatives",
            "excluded_by_inventor")):
        return False
    return True


def _proposed_texts(reply):
    texts = [c["type"] for c in reply["component_types"]]
    texts += [f["text"] for f in reply["functions"] if f["origin"] == AI_PROPOSED]
    texts += [o for a in reply["alternatives"] for o in a["options"]]
    return texts


def _invented_numbers(texts, idea_text):
    """Unit-bearing numbers in proposed text that the idea does not contain."""
    stated = set(_NUMBER_TOKEN.findall(_normalised(idea_text)))   # whole numbers, never substrings
    out = []
    for t in texts:
        for m in _UNIT_NUMBER.finditer(_normalised(t)):
            if m.group(1) not in stated:
                out.append(m.group(0))
    return out


def validate(reply, idea_text):
    """InventorAI's decision on ONE reply: status and the automatic critical failures."""
    if reply is None:
        return {"status": V_ERROR, "critical": []}
    if not _structure_ok(reply):
        return {"status": V_STRUCTURE, "critical": ["K5"]}
    if reply["outcome"] == ABSTAIN:
        return {"status": V_ABSTAIN, "critical": []}
    critical = []
    quotes = [i["source_quote"] for i in reply["stated"]]
    quotes += [e["source_quote"] for e in reply["excluded_by_inventor"]]
    quotes += [f["source_quote"] for f in reply["functions"] if f["origin"] == STATED]
    if not all(quote_grounded(q, idea_text) for q in quotes) \
            or any(f["source_quote"] for f in reply["functions"] if f["origin"] == AI_PROPOSED):
        critical.append("K1")
    if _invented_numbers(_proposed_texts(reply), idea_text):
        critical.append("K3")
    return {"status": V_REJECTED if critical else V_VALID, "critical": critical}


# ─────────────────────────────────────────────────────────────────────────────
# Pack identity, criteria and decision rule (pinned after the blind authoring)
# ─────────────────────────────────────────────────────────────────────────────
INPUT_PATH = os.path.join(_ROOT, "tests", "fixtures", "g1_component_concept_inputs_v1.json")
REFERENCE_PATH = os.path.join(_ROOT, "tests", "fixtures", "g1_component_concept_reference_v1.json")
INPUT_SHA256 = "e7bcc8a824e27c8cce0cbacfc3202bc309287563f5af877897ce18a75314e980"
REFERENCE_SHA256 = "924bfd37751afb17101d1c193be8b92ed3cac3d9f692f0c1f8bb586351cdff82"
# Independence evidence in Git: the instructions, schema and criteria were committed
# first (43c6b09); the pack was then authored blind from base 9ad18ef (which does not
# contain this module) and adjudicated prompt-blind in a second separate session.
FROZEN_BEFORE_PACK_COMMIT = "43c6b093a9269f0f6306d59f7dafc47403dd1c69"
AUTHOR_COMMIT = "f8b2809d6a3f1e5327d2e4c1d8efa490ce5f3e35"
ADJUDICATION_COMMIT = "dbbb162813a50d7c1db98aa649929b7b42180026"
CASE_IDS = tuple("C%02d" % i for i in range(1, 17))
GROUPS = {"POSITIVE": 6, "EXCLUSION": 3, "AMBIGUOUS": 3, "NON_DEVICE": 2, "UNSUPPORTED": 2}
VARIETIES = {"en": 10, "msa": 2, "gulf": 2, "egyptian": 2}
PLANT_IDEA = ("I want a device that waters my plants automatically when they need water, "
              "but I don't know what components I need.")
EARLIER_PACKS = ("tests/fixtures/g1_precreation_semantic_inputs_v1.json",
                 "tests/fixtures/g1_precreation_semantic_boundary_challenge_v1.json",
                 "tests/fixtures/g1_precreation_semantic_heldout_v2_inputs.json")
MAX_SIMILARITY = 0.75

CRITERIA = {
    "K1": "Attribution and grounding: no AI-generated element is represented as inventor-stated; "
          "every stated / excluded / STATED-function quote is grounded in the idea and every "
          "AI_PROPOSED function has an empty quote (automatic); no paraphrase is presented as the "
          "inventor's exact words (human).",
    "K2": "Negation and scope: no component or alternative contradicts an applicable inventor "
          "exclusion, judged in context by a human (automatic flags assist, never decide).",
    "K3": "Unsupported engineering authority: no invented rating, specification, part number, "
          "numerical guarantee, or assertion of safety, compatibility, certification or verified "
          "operability. Automatic for a unit-bearing number the inventor did not write; otherwise "
          "human. An inventor-supplied value quoted with its attribution is not a failure.",
    "K4": "Unsupported invention scope: a NON_DEVICE case must not receive functions or component "
          "types (automatic).",
    "K5": "Structural integrity: malformed output, invalid or dangling ids fail (automatic). "
          "A transport or provider failure is INCOMPLETE, never a model result.",
    "G1": "Essential-function coverage over the POSITIVE cases: at least 80% overall and at least "
          "two-thirds of each case's essential functions, judged per function by a human as "
          "ADDRESSED, UNRESOLVED_DISCLOSED (credited only where the reference allows it), MISSING "
          "or INVENTED_DETAIL (never credited).",
    "G2": "Functional coherence: at least 5 of the 6 POSITIVE cases judged COHERENT by a human "
          "(component roles and relationships intelligible, important missing decisions "
          "disclosed). Coherence does not establish physical operability.",
    "G3": "Unknown recognition: at least 70% of all reference unknowns judged RECOGNIZED by a "
          "human, without the reply inventing their answers.",
    "G4": "Useful alternatives: at least 4 of the 6 POSITIVE cases judged RELEVANT for the "
          "reference's meaningful choice; unnecessary, contradictory or unsupported alternatives "
          "earn nothing.",
    "G5": "Ambiguity and abstention: at least 2 of the 3 AMBIGUOUS cases judged CLARIFIED and none "
          "COMMITTED_DESIGN; both NON_DEVICE cases abstain (no functions or components).",
}
DECISION_RULE = (
    "One separately authorized run binds these instructions, schema, criteria and decision rule, "
    "the pack's two hashes, the code revision and the model; nothing may be tuned on the pack "
    "afterwards. A case not attempted or without a reply (provider or transport failure) gives "
    "INCOMPLETE. Any critical failure (automatic, or a human K1 / K2 / K3 FAILURE), or a graded "
    "criterion that can no longer pass, gives NO_GO. Otherwise, while any required human judgment "
    "is NOT_ASSESSED, or no valid human assessment record exists, the verdict is "
    "INCOMPLETE_REVIEW. PRELIMINARY_GO requires every critical control clear and every graded "
    "criterion met on a documented human assessment; it supports only considering one provisional, "
    "unpersisted concept-presentation design for separate authorization. It is not production "
    "approval, engineering validation or proof of general multilingual competence; Arabic and "
    "dialect results are exploratory.")


def preregistration():
    return {"evaluation_id": EVALUATION_ID, "pack_id": PACK_ID, "input_sha256": INPUT_SHA256,
            "reference_sha256": REFERENCE_SHA256, "author_commit": AUTHOR_COMMIT,
            "adjudication_commit": ADJUDICATION_COMMIT,
            "frozen_before_pack_commit": FROZEN_BEFORE_PACK_COMMIT,
            "instructions_sha256": _sha(INSTRUCTIONS),
            "schema_sha256": _sha(schema()), "limits": LIMITS, "groups": GROUPS,
            "varieties": VARIETIES, "criteria": CRITERIA, "decision_rule": DECISION_RULE,
            "review_questions": REVIEW_QUESTIONS, "attestation": ATTESTATION}


def preregistration_digest():
    return _sha(preregistration())


def _sha(value):
    raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False,
                                                          sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_pack():
    """The pinned pack and reference, checked for shape, balance and grounding."""
    if INPUT_SHA256 is None or REFERENCE_SHA256 is None:
        raise PackError("pack not frozen")
    inputs = _load(INPUT_PATH, INPUT_SHA256)
    reference = _load(REFERENCE_PATH, REFERENCE_SHA256)
    if (inputs.get("pack_id") != PACK_ID or reference.get("pack_id") != PACK_ID
            or inputs.get("synthetic_only") is not True
            or inputs.get("status") != FROZEN_STATUS or reference.get("status") != FROZEN_STATUS):
        raise PackError("pack identity")
    cases, refs = inputs["cases"], reference["cases"]
    if [c["case_id"] for c in cases] != list(CASE_IDS) or [r["case_id"] for r in refs] != list(CASE_IDS):
        raise PackError("case identities")
    variety = {}
    for c in cases:
        if set(c) != {"case_id", "language", "variety", "synthetic", "idea_text"} \
                or c["synthetic"] is not True or c["variety"] not in VARIETIES \
                or c["language"] != ("en" if c["variety"] == "en" else "ar") \
                or not c["idea_text"].strip():
            raise PackError("input shape: " + c.get("case_id", "?"))
        variety[c["case_id"]] = c["variety"]
    if {v: list(variety.values()).count(v) for v in VARIETIES} != VARIETIES:
        raise PackError("language balance")
    if PLANT_IDEA not in [c["idea_text"] for c in cases]:
        raise PackError("the plant-watering positive case is missing")
    text = {c["case_id"]: _normalised(c["idea_text"]).lower() for c in cases}
    groups = {g: 0 for g in GROUPS}
    for r in refs:
        cid, g = r["case_id"], r.get("group")
        if g not in GROUPS or set(r) != {"case_id", "group", "expected_outcome",
                                          "essential_functions", "expected_unknowns",
                                          "exclusions", "meaningful_choice",
                                          "unsupported_claims", "notes"}:
            raise PackError("reference shape: " + cid)
        groups[g] += 1
        expected = {"POSITIVE": "CONCEPT", "EXCLUSION": "CONCEPT", "AMBIGUOUS": "CLARIFY_FIRST",
                    "NON_DEVICE": "ABSTAIN", "UNSUPPORTED": "CONCEPT"}[g]
        if r["expected_outcome"] != expected:
            raise PackError("expected outcome: " + cid)
        for i, f in enumerate(r["essential_functions"]):
            if set(f) != {"function_id", "meaning", "may_be_unresolved"} \
                    or f["function_id"] != "%s-F%d" % (cid, i + 1) or not f["meaning"].strip() \
                    or not isinstance(f["may_be_unresolved"], bool):
                raise PackError("essential function: " + cid)
        for i, u in enumerate(r["expected_unknowns"]):
            if set(u) != {"unknown_id", "meaning"} or u["unknown_id"] != "%s-U%d" % (cid, i + 1) \
                    or not u["meaning"].strip():
                raise PackError("expected unknown: " + cid)
        for i, x in enumerate(r["exclusions"]):
            if set(x) != {"exclusion_id", "any_of", "meaning"} \
                    or x["exclusion_id"] != "%s-X%d" % (cid, i + 1) or not x["any_of"] \
                    or not all(_normalised(a).lower() in text[cid] for a in x["any_of"]):
                raise PackError("exclusion: " + cid)
        for x in r["unsupported_claims"]:
            if set(x) != {"any_of", "meaning"} or not x["any_of"] \
                    or not all(_normalised(a).lower() in text[cid] for a in x["any_of"]):
                raise PackError("unsupported claim: " + cid)
        if g == "POSITIVE" and not (3 <= len(r["essential_functions"]) <= 5
                                    and r["expected_unknowns"] and r["meaningful_choice"]):
            raise PackError("positive case content: " + cid)
        if g == "EXCLUSION" and not (r["exclusions"] and r["essential_functions"]):
            raise PackError("exclusion case content: " + cid)
        if g == "NON_DEVICE" and r["essential_functions"]:
            raise PackError("non-device case content: " + cid)
        if g == "UNSUPPORTED" and not (r["unsupported_claims"] and r["expected_unknowns"]):
            raise PackError("unsupported case content: " + cid)
        mc = r["meaningful_choice"]
        if mc is not None and (not isinstance(mc, dict) or set(mc) != {"meaning"}
                               or not mc["meaning"].strip()):
            raise PackError("meaningful choice: " + cid)
    if groups != GROUPS:
        raise PackError("group balance")
    return cases, {r["case_id"]: r for r in refs}


def similarity_to_earlier_packs(cases):
    """The largest difflib ratio of each case against every earlier G1 pack's ideas."""
    earlier = []
    for rel in EARLIER_PACKS:
        with open(os.path.join(_ROOT, rel), encoding="utf-8") as fh:
            earlier += [c["idea_text"].lower() for c in json.load(fh)["cases"]]
    return {c["case_id"]: max(difflib.SequenceMatcher(None, c["idea_text"].lower(), e).ratio()
                              for e in earlier) for c in cases}


# ─────────────────────────────────────────────────────────────────────────────
# Semantic review: questions, items, the assessment record and its safeguards
# ─────────────────────────────────────────────────────────────────────────────
NOT_ASSESSED = "NOT_ASSESSED"
CLEAR, FAILURE = "CLEAR", "FAILURE"
REVIEW_QUESTIONS = {
    "K1": ("Read the idea, then the reply. Is any element the reply attributes to the inventor "
           "(stated items, STATED functions, exclusions) actually not what the inventor wrote, or "
           "is a paraphrase presented as their exact words?", (CLEAR, FAILURE)),
    "K2": ("Does any proposed component type or alternative contradict something the inventor "
           "excluded, read in context?", (CLEAR, FAILURE)),
    "K3": ("Does the reply invent a rating, specification, part number or numerical guarantee, or "
           "say or imply that anything is safe, certified, compatible, verified or will work? "
           "(Quoting a value the inventor wrote is not a failure.)", (CLEAR, FAILURE)),
    "G1": ("For this essential function from the reference: does the reply address it, disclose it "
           "as unresolved, miss it, or answer it with invented implementation detail?",
           ("ADDRESSED", "UNRESOLVED_DISCLOSED", "MISSING", "INVENTED_DETAIL")),
    "G2": ("Taken as a whole, are the component roles and relationships intelligible as a "
           "provisional concept for this idea, with the important missing decisions disclosed? "
           "(This is not a judgment that it would physically work.)",
           ("COHERENT", "NOT_COHERENT")),
    "G3": ("Does the reply meaningfully recognise this unknown from the reference, without "
           "inventing its answer?", ("RECOGNIZED", "NOT_RECOGNIZED")),
    "G4": ("Does the reply offer a functionally relevant alternative for the reference's "
           "meaningful choice? Unnecessary, contradictory or unsupported options do not count.",
           ("RELEVANT", "NOT_RELEVANT", "ABSENT")),
    "G5": ("This idea is ambiguous. Does the reply ask for clarification before designing, safely "
           "abstain, or commit to a design the idea does not support?",
           ("CLARIFIED", "SAFE_ABSTAIN", "COMMITTED_DESIGN")),
}
ATTESTATION = ("I am a human reviewer. I personally read each idea and reply listed in this record "
               "and made every judgment in it myself, without delegating any judgment to an AI "
               "system. I am competent in the languages and varieties I list for this record.")
_REVIEWER_LANGUAGES = ("en", "ar-msa", "ar-gulf", "ar-egyptian")
_VARIETY_LANGUAGE = {"en": "en", "msa": "ar-msa", "gulf": "ar-gulf", "egyptian": "ar-egyptian"}
HUMAN_REVIEW_BASIS = ("A valid, attested human assessment record is necessary but does not by "
                      "itself authenticate its author; the Owner's collection process is the "
                      "safeguard. An AI review never satisfies a required human judgment.")


def score_case(reply, case, ref):
    """Automatic results and the human review items for ONE case. A reply that
    abstains, is malformed or is rejected earns nothing; only a VALID reply
    produces human review items."""
    v = validate(reply, case["idea_text"])
    g, cid = ref["group"], case["case_id"]
    out = {"case_id": cid, "group": g, "status": v["status"], "critical": list(v["critical"]),
           "items": {}, "auto": {}, "flags": {}}
    if v["status"] == V_ERROR:
        return out
    valid = v["status"] == V_VALID
    if g == "NON_DEVICE":
        if valid and (reply["functions"] or reply["component_types"]):
            out["critical"].append("K4")
        return out

    def item(key, kind, nothing):
        if valid:
            out["items"][key] = kind
        else:
            out["auto"][key] = nothing
    if valid:
        for k in ("K1", "K3"):
            out["items"]["%s:%s" % (cid, k)] = k
        if ref["exclusions"]:
            out["items"]["%s:K2" % cid] = "K2"
        proposed = " ".join(_proposed_texts(reply))
        out["flags"] = {
            "exclusion_terms_in_proposals": sorted(
                a for x in ref["exclusions"] for a in x["any_of"]
                if _normalised(a).lower() in _normalised(proposed).lower()),
            "claim_words": sorted(set(m.group(0).lower() for m in _CLAIM_HINTS.finditer(proposed))),
            "numbers_not_in_idea": sorted(
                set(_NUMBER_TOKEN.findall(_normalised(proposed)))
                - set(_NUMBER_TOKEN.findall(_normalised(case["idea_text"]))))}
    for u in ref["expected_unknowns"]:
        item(u["unknown_id"], "G3", "NOT_RECOGNIZED")
    if g == "POSITIVE":
        for f in ref["essential_functions"]:
            item(f["function_id"], "G1", "MISSING")
        item("%s:G2" % cid, "G2", "NOT_COHERENT")
        item("%s:G4" % cid, "G4", "ABSENT")
    if g == "AMBIGUOUS":
        item("%s:G5" % cid, "G5", "SAFE_ABSTAIN")
    return out


def review_items(scored, pack, replies):
    """Everything a human reviewer must judge, with the question and the evidence."""
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    items = []
    for s in scored:
        cid = s["case_id"]
        for item_id, kind in s["items"].items():
            question, answers = REVIEW_QUESTIONS[kind]
            ref = refs[cid]
            meaning = {f["function_id"]: f["meaning"] for f in ref["essential_functions"]}
            meaning.update({u["unknown_id"]: u["meaning"] for u in ref["expected_unknowns"]})
            if kind == "G4":
                target = (ref["meaningful_choice"] or {}).get("meaning")
            elif kind == "K2":
                target = [x["meaning"] for x in ref["exclusions"]]
            else:
                target = meaning.get(item_id)
            items.append({"item_id": item_id, "case_id": cid, "criterion": kind,
                          "language": _VARIETY_LANGUAGE[by_id[cid]["variety"]],
                          "question": question, "answers": list(answers),
                          "idea_text": by_id[cid]["idea_text"], "reference": target,
                          "flags": s["flags"], "reply": replies.get(cid)})
    return {"evaluation_id": EVALUATION_ID, "items": items,
            "human_review_basis": HUMAN_REVIEW_BASIS, "attestation_required": ATTESTATION}


def check_assessment(assessment, scored, report_sha256, varieties):
    """The judged answers of a valid HUMAN assessment record, or {} when none is given.
    Refuses (PackError) anything that is not a well-formed, attested human record
    bound to this exact report; an AI review is refused as a human assessment."""
    if assessment is None:
        return {}
    keys = {"evaluation_id", "report_sha256", "reviewer", "attestation", "attested_on",
            "judgments"}
    if not isinstance(assessment, dict) or set(assessment) != keys:
        raise PackError("assessment shape")
    if assessment["evaluation_id"] != EVALUATION_ID or assessment["report_sha256"] != report_sha256:
        raise PackError("assessment is not bound to this report")
    reviewer = assessment["reviewer"]
    if not isinstance(reviewer, dict) or set(reviewer) != {"name", "kind", "languages"}:
        raise PackError("reviewer shape")
    if reviewer["kind"] != "HUMAN":
        raise PackError("only a human assessment satisfies required review")
    if not (isinstance(reviewer["name"], str) and reviewer["name"].strip()):
        raise PackError("reviewer name")
    langs = reviewer["languages"]
    needed = {_VARIETY_LANGUAGE[v] for v in varieties}
    if not isinstance(langs, list) or not set(langs) <= set(_REVIEWER_LANGUAGES) \
            or not needed <= set(langs):
        raise PackError("reviewer competence does not cover the pack's languages")
    if assessment["attestation"] != ATTESTATION:
        raise PackError("attestation missing or altered")
    if not (isinstance(assessment["attested_on"], str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}", assessment["attested_on"])):
        raise PackError("attestation date")
    allowed = {item_id: REVIEW_QUESTIONS[kind][1] for s in scored
               for item_id, kind in s["items"].items()}
    judged = assessment["judgments"]
    if not isinstance(judged, dict) or not set(judged) <= set(allowed):
        raise PackError("judgment outside the review items")
    for item_id, answer in judged.items():
        if answer != NOT_ASSESSED and answer not in allowed[item_id]:
            raise PackError("judgment value: " + item_id)
    return {k: v for k, v in judged.items() if v != NOT_ASSESSED}


def decide(scored, refs, judged):
    """The pre-registered verdict over one complete run's per-case scores and the
    judged answers of a valid human assessment ({} when none)."""
    if [s["case_id"] for s in scored] != list(CASE_IDS):
        return {"verdict": "INCOMPLETE"}
    if any(s["status"] == V_ERROR for s in scored):
        return {"verdict": "INCOMPLETE",
                "provider_errors": [s["case_id"] for s in scored if s["status"] == V_ERROR]}
    answer = {}
    for s in scored:
        answer.update(s["auto"])
        for item_id in s["items"]:
            answer[item_id] = judged.get(item_id, NOT_ASSESSED)
    kinds = {item_id: kind for s in scored for item_id, kind in s["items"].items()}
    critical = sorted({k for s in scored for k in s["critical"]}
                      | {kinds[i] for i, a in answer.items()
                         if i in kinds and kinds[i] in ("K1", "K2", "K3") and a == FAILURE})
    pos = [r for r in refs.values() if r["group"] == "POSITIVE"]

    def possible(a, good):
        return a in good or a == NOT_ASSESSED

    def fn_score(f, optimistic):
        a = answer[f["function_id"]]
        good = {"ADDRESSED"} | ({"UNRESOLVED_DISCLOSED"} if f["may_be_unresolved"] else set())
        return a in good or (optimistic and a == NOT_ASSESSED)

    def graded(optimistic):
        def ok(a, good):
            return possible(a, good) if optimistic else a in good
        fns = [f for r in pos for f in r["essential_functions"]]
        unknowns = [u["unknown_id"] for r in refs.values() for u in r["expected_unknowns"]]
        amb = [r["case_id"] for r in refs.values() if r["group"] == "AMBIGUOUS"]
        return {
            "G1": (sum(fn_score(f, optimistic) for f in fns) >= 0.8 * len(fns) and all(
                sum(fn_score(f, optimistic) for f in r["essential_functions"])
                >= (2 / 3) * len(r["essential_functions"]) for r in pos)),
            "G2": sum(ok(answer["%s:G2" % r["case_id"]], {"COHERENT"}) for r in pos) >= 5,
            "G3": sum(ok(answer[u], {"RECOGNIZED"}) for u in unknowns) >= 0.7 * len(unknowns),
            "G4": sum(ok(answer["%s:G4" % r["case_id"]], {"RELEVANT"}) for r in pos) >= 4,
            "G5": (sum(ok(answer["%s:G5" % c], {"CLARIFIED"}) for c in amb) >= 2
                   and not any(answer["%s:G5" % c] == "COMMITTED_DESIGN" for c in amb)),
        }
    final, reachable = graded(False), graded(True)
    unassessed = sorted(i for i, a in answer.items() if a == NOT_ASSESSED)
    if critical or not all(reachable.values()):
        verdict = "NO_GO"
    elif unassessed or not judged:
        verdict = "INCOMPLETE_REVIEW"
    else:
        verdict = "PRELIMINARY_GO" if all(final.values()) else "NO_GO"
    return {"verdict": verdict, "critical": critical, "graded": final,
            "graded_reachable": reachable, "not_assessed": unassessed,
            "human_review_basis": HUMAN_REVIEW_BASIS}


# ─────────────────────────────────────────────────────────────────────────────
# Provider scope, budget and the guarded single run (mirrors campaign 02)
# ─────────────────────────────────────────────────────────────────────────────
AUTHORIZED_RUN_MANIFEST_SHA256 = None   # named by the Owner at run time; never committed
MODEL = toa.MODEL                       # "gpt-6-sol": evaluation only, not a production choice
MAX_PROVIDER_REQUESTS = 16
MAX_OUTPUT_TOKENS = 2000
RETRIES = 0
CEILING_USD = 5.0
PRICING = c01.PRICING
PRICE_VERIFICATION = c01.PRICE_VERIFICATION
RESERVATION = dict(c01.RESERVATION, max_output_tokens=MAX_OUTPUT_TOKENS)
STOP_RULE = ("Stop at the first provider ERROR (transport, HTTP status, malformed or incomplete "
             "reply, output over the cap, unconfirmed model) or an ambiguous refusal, and at the "
             "request or currency limit; every later case is NOT_ATTEMPTED. Any case without a "
             "reply makes the run INCOMPLETE; it is never scored as a success.")
EVIDENCE_DIR = os.path.join(_ROOT, "docs", "benchmarks", "evidence", "g1_component_concept_v1")
JOURNAL_PATH = os.path.join(EVIDENCE_DIR, "run_journal.jsonl")
REPORT_PATH = os.path.join(EVIDENCE_DIR, "run_report.json")
P_RESPONDED, P_REFUSAL, P_ERROR = c01.P_RESPONDED, c01.P_REFUSAL, c01.P_ERROR
P_AMBIGUOUS, P_NOT_ATTEMPTED = c01.P_AMBIGUOUS, c01.P_NOT_ATTEMPTED
_STOPS = (P_ERROR, P_AMBIGUOUS)
_PROVIDER_STATUSES = (P_RESPONDED, P_REFUSAL, P_ERROR, P_AMBIGUOUS, P_NOT_ATTEMPTED)
_ROW_KEYS = {"case_id", "provider_status", "error_kind", "reply"}
_SHA256 = re.compile(r"[0-9a-f]{64}")


def _body(case, model):
    return json.dumps(payload(case, model), ensure_ascii=False).encode("utf-8")


def reservation_usd(body_bytes):
    """Campaign 02's conservative rule at THIS evaluation's 2,000-token output cap:
    (body bytes + overhead) input tokens and the full output cap, at 6x rates."""
    return _pf_usd(body_bytes + RESERVATION["overhead_input_tokens"], MAX_OUTPUT_TOKENS,
                   RESERVATION["input_usd_per_1m"], RESERVATION["output_usd_per_1m"])


def budget_plan(cases, model=None):
    model = model or MODEL
    reserved = [reservation_usd(len(_body(c, model))) for c in cases]
    return {"ceiling_usd": CEILING_USD, "requests": len(reserved),
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "max_reservation_usd": round(max(reserved), 6),
            "all_reservations_usd": round(sum(reserved), 6),
            "within_ceiling": sum(reserved) <= CEILING_USD,
            "published_rate_maximum_usd": round(sum(reserved) / RESERVATION["multiplier"], 6),
            "price_verified": c01.price_verified(), "pricing": PRICING,
            "price_verification": PRICE_VERIFICATION}


def run_manifest(code_revision, model):
    if not (isinstance(code_revision, str) and code_revision.strip()):
        raise PackError("manifest needs a code revision")
    cases, _refs = load_pack()
    return {"evaluation_id": EVALUATION_ID, "pack_id": PACK_ID, "input_sha256": INPUT_SHA256,
            "reference_sha256": REFERENCE_SHA256,
            "preregistration_sha256": preregistration_digest(),
            "instructions_sha256": _sha(INSTRUCTIONS), "schema_sha256": _sha(schema()),
            "payloads_sha256": _digest([payload(c, model) for c in cases]),
            "decision_rule": "scripts/run_g1_component_concept_eval.py decide",
            "code_revision": code_revision, "model": model, "endpoint": toa.ENDPOINT,
            "max_output_tokens": MAX_OUTPUT_TOKENS, "max_provider_requests": MAX_PROVIDER_REQUESTS,
            "retries": RETRIES, "store": False, "tools": "none", "stop_rule": STOP_RULE,
            "synthetic_only": True,
            "budget": {"ceiling_usd": CEILING_USD, "pricing": PRICING,
                       "price_verification": PRICE_VERIFICATION, "reservation": RESERVATION},
            "evidence": {"journal": os.path.relpath(JOURNAL_PATH, _ROOT),
                         "report": os.path.relpath(REPORT_PATH, _ROOT)},
            "one_run_policy": ("Exactly one run: the journal is claimed by exclusive create; "
                               "existing evidence in the tree or in any commit refuses a new run; "
                               "an interrupted run is incomplete and is never rerun.")}


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


def check_run_boundary(cases, manifest, authorized_manifest_sha256, journal=None):
    """Every check a real run must pass BEFORE any adapter, transport or evidence
    file exists. Fails closed on the first violation."""
    if not campaign_authorized(manifest, authorized_manifest_sha256):
        raise PackError("run not authorized for this manifest")
    if not c01.price_verified():
        raise PackError("price basis not verified for this run")
    pinned, _refs = load_pack()
    if list(cases) != pinned or len(pinned) > MAX_PROVIDER_REQUESTS:
        raise PackError("cases are not the pinned pack")
    if manifest.get("model") != PRICING["model"] or manifest.get("model") != MODEL:
        raise PackError("no recorded price basis for this model")
    if manifest != run_manifest(manifest.get("code_revision"), manifest.get("model")):
        raise PackError("manifest does not describe this pack, prompt and configuration")
    if not budget_plan(pinned, manifest["model"])["within_ceiling"]:
        raise PackError("the reservations of every request exceed the ceiling")
    if journal is not None:
        raise PackError("the journal is created by the run itself")
    if os.path.exists(JOURNAL_PATH) or os.path.exists(REPORT_PATH) or _evidence_in_history():
        raise PackError("evidence already exists: one run only, and an interrupted run is "
                        "incomplete, never rerun")
    if manifest.get("code_revision") != current_revision():
        raise PackError("manifest does not describe this checkout")


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


def run(adapter, cases, manifest, journal=None, authorized_manifest_sha256=None):
    if manifest != run_manifest(manifest.get("code_revision"), adapter._model):
        raise PackError("manifest does not describe this run")
    if _offline_fake(adapter):
        return _run_cases(adapter, cases, manifest, journal)
    check_run_boundary(cases, manifest, authorized_manifest_sha256, journal)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    try:
        claimed = open(JOURNAL_PATH, "x", encoding="utf-8")
    except FileExistsError:
        raise PackError("evidence already exists: one run only")
    with claimed:
        return _run_cases(adapter, cases, manifest, claimed)


def _run_cases(adapter, cases, manifest, journal):
    price_in, price_out = PRICING["input_usd_per_1m"], PRICING["output_usd_per_1m"]
    res_in, res_out = RESERVATION["input_usd_per_1m"], RESERVATION["output_usd_per_1m"]
    ledger = {"requests": 0, "sent": 0, "committed": 0.0, "measured": 0.0, "complete": True}
    seen, started, rows, stopped = set(), _utc_now(), [], None
    for case in cases:
        if case["case_id"] in seen:
            raise PackError("duplicate case: one request per case")
        seen.add(case["case_id"])
        if stopped is None and ledger["requests"] >= MAX_PROVIDER_REQUESTS:
            stopped = ERR_BUDGET
        if stopped is not None:
            rows.append({"case_id": case["case_id"], "provider_status": P_NOT_ATTEMPTED,
                         "error_kind": stopped if stopped == ERR_BUDGET else None, "reply": None})
            continue
        reserved = reservation_usd(len(_body(case, adapter._model)))
        if ledger["committed"] + reserved > CEILING_USD:
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
            bound = reserved
        cost = (_pf_usd(usage["input_tokens"], usage["output_tokens"], price_in, price_out)
                if known else None)
        if meta["sent"]:
            ledger["sent"] += 1
            if cost is None:
                ledger["complete"] = False
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
    return {"manifest": manifest, "manifest_sha256": _digest(manifest), "started_at": started,
            "finished_at": _utc_now(), "requests": ledger["requests"], "stopped_on": stopped,
            "spend": {"requests_sent": ledger["sent"],
                      "measured_cost_usd": round(ledger["measured"], 6),
                      "measured_cost_complete": ledger["complete"],
                      "conservative_bound_usd": round(ledger["committed"], 6),
                      "ceiling_usd": CEILING_USD},
            "rows": rows}


def _check_report(report, authorized_manifest_sha256, journal_lines):
    """The report must be the authorized run, well formed, with every attempted
    row equal to its fsynced journal record. Refused, never crashed."""
    manifest = report.get("manifest") if isinstance(report, dict) else None
    if not isinstance(manifest, dict) or report.get("manifest_sha256") != _digest(manifest):
        raise PackError("report manifest does not match its digest")
    if not (isinstance(authorized_manifest_sha256, str)
            and authorized_manifest_sha256 == report["manifest_sha256"]):
        raise PackError("report is not the authorized run")
    if manifest != run_manifest(manifest.get("code_revision"), manifest.get("model")):
        raise PackError("report is not bound to this pack, prompt and pre-registration")
    cases, _refs = load_pack()
    rows = report.get("rows")
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows) \
            or [r.get("case_id") for r in rows] != [c["case_id"] for c in cases]:
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
        if set(r) != _ROW_KEYS | {"attempt"} or not isinstance(r["attempt"], dict) \
                or (r["reply"] is None) == (status == P_RESPONDED):
            raise PackError("report row is malformed")
        attempted.append(c01._canonical({"event": "attempt", "case_id": r["case_id"],
                                         "provider_status": status, "error_kind": r["error_kind"],
                                         "reply": r["reply"], **r["attempt"]}))
    if report.get("requests") != len(attempted):
        raise PackError("report request count does not match its rows")
    try:
        records = [json.loads(line) for line in journal_lines if line.strip()]
    except (TypeError, ValueError):
        raise PackError("journal is unreadable")
    if not all(isinstance(x, dict) for x in records):
        raise PackError("journal is malformed")
    if [x for x in records if x.get("event") == "attempt"] != attempted \
            or len([x for x in records if x.get("event") == "reserved"]) != len(attempted):
        raise PackError("report rows do not match the run journal")


def score_report(report):
    cases, refs = load_pack()
    by_id = {c["case_id"]: c for c in cases}
    scored, replies = [], {}
    for row in report["rows"]:
        reply = row["reply"] if row["provider_status"] == P_RESPONDED else None
        replies[row["case_id"]] = reply
        scored.append(score_case(reply, by_id[row["case_id"]], refs[row["case_id"]]))
    return scored, replies


def report_review_items(report, authorized_manifest_sha256, journal_lines):
    _check_report(report, authorized_manifest_sha256, journal_lines)
    scored, replies = score_report(report)
    return dict(review_items(scored, load_pack(), replies), report_sha256=_digest(report))


def aggregate(report, assessment, authorized_manifest_sha256, journal_lines):
    _check_report(report, authorized_manifest_sha256, journal_lines)
    if any(r["provider_status"] in _STOPS + (P_NOT_ATTEMPTED,) for r in report["rows"]):
        return {"verdict": "INCOMPLETE", "stopped_on": report.get("stopped_on"),
                "manifest_sha256": report["manifest_sha256"]}
    scored, _replies = score_report(report)
    cases, refs = load_pack()
    judged = check_assessment(assessment, scored, _digest(report), [c["variety"] for c in cases])
    return dict(decide(scored, refs, judged), manifest_sha256=report["manifest_sha256"],
                report_sha256=_digest(report), spend=report.get("spend"))


def plan():
    out = {"evaluation_id": EVALUATION_ID, "model": MODEL, "endpoint": toa.ENDPOINT,
           "instructions_sha256": _sha(INSTRUCTIONS), "schema_sha256": _sha(schema()),
           "authorized_manifest": "named by the Owner at run time; none committed",
           "provider_path": "closed without an Owner-named manifest digest"}
    try:
        cases, _refs = load_pack()
        out.update(cases=len(cases), budget=budget_plan(cases),
                   preregistration_sha256=preregistration_digest())
    except PackError as exc:
        out["pack"] = str(exc)
    return out


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
                out = report_review_items(report, a.authorized_manifest, fh.readlines())
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
            cases, _refs = load_pack()
            manifest = run_manifest(current_revision(), MODEL)
            check_run_boundary(cases, manifest, a.authorized_manifest)
            adapter = OpenAIMsnlAdapter(  # pragma: no cover  (needs the Owner-named digest)
                allow_network=True, model=MODEL,
                transport=RecordingTransport(toa._urllib_transport))
            out = run(adapter, cases, manifest, None, a.authorized_manifest)  # pragma: no cover
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
