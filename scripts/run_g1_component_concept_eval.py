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
PACK_ID = "inventorai-g1-component-concept-heldout-02"
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
    "Keep two things strictly apart. stated: only what the person actually wrote, each with a "
    "source_quote copied from the idea (kind FUNCTION, COMPONENT, CONSTRAINT, VALUE or CONTEXT). "
    "Everything else is your proposal.\n"
    "functions: what the invention would need to do. origin STATED only when the person wrote it, "
    "with a source_quote; otherwise origin AI_PROPOSED with an empty source_quote. Use resolution "
    "UNRESOLVED when a function depends on information the person has not given.\n"
    "component_types: generic kinds of part that could perform the functions (a kind of part, not "
    "a product, brand, model or part number), each serving one or more function ids, always "
    "attribution AI_PROPOSED and status UNVERIFIED.\n"
    "relationships: how components or functions conceptually connect, kind SIGNAL, POWER, FLOW or "
    "MECHANICAL. A relationship is a conceptual connection, never a claim that parts are "
    "compatible.\n"
    "alternatives: for a function where a genuinely different approach exists, its options. "
    "missing_information: decisions or facts the person has not given that the design depends on. "
    "clarification_questions: questions a nontechnical person can answer.\n"
    "excluded_by_inventor: anything the person says the invention must not have or use, quoted from "
    "the idea; never propose a component that contradicts it.\n"
    "Never invent ratings, sizes, quantities, part numbers or other specifications; quote a number "
    "only if the person wrote it. Never say or imply that anything is safe, certified, compatible, "
    "guaranteed, tested, verified or will work. If the person asks for something that cannot be "
    "promised, record it as missing information, not as achieved.\n"
    "Outcome: when you can describe a provisional concept, use RESPONDED with at least one function "
    "and at least one component type. If it is unclear what the invention is or does, ask first: "
    "give clarification_questions and do not commit to a design (RESPONDED without component types, "
    "or ABSTAIN). If the text describes no invention to build, or only an object the person does "
    "not design, use ABSTAIN, never RESPONDED with empty lists.\n"
    "Format rules (a reply that breaks one is rejected): ids are S1, S2, ... for stated, F1, F2, "
    "... for functions and C1, C2, ... for component_types: one capital letter and a number from 1 "
    "to 99, each id used once. serves lists one or more existing F ids. A relationship joins two "
    "different existing S, F or C ids. for_function is an existing F id. At most %(stated)d stated "
    "items, %(functions)d functions, %(component_types)d component types, %(relationships)d "
    "relationships, %(alternatives)d alternatives with 1 to %(options)d options each, "
    "%(missing_information)d missing_information items, %(clarification_questions)d "
    "clarification_questions and %(excluded_by_inventor)d excluded_by_inventor items. Every text "
    "is at most %(item_chars)d characters. Every non-empty source_quote is copied character for "
    "character from the idea (same capitalisation, punctuation and apostrophes) and contains at "
    "least two words. With outcome ABSTAIN, every list is empty except missing_information and "
    "clarification_questions." % LIMITS)
# The format rules above are generated from LIMITS and _ID, which the validator enforces, so the
# instructions and the checks cannot disagree (G1-1/2 correction M1).



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
    r"(?<![\w.])(\d+(?:[.,]\d+)?)\s*(?:mm|cm|m|km|ml|l|v|mv|kv|(?-i:A)|ma|w|kw|mw|wh|kwh|mah|ah|"
    r"hz|khz|mhz|ghz|rpm|nm|n|kg|g|mg|bar|psi|pa|kpa|db|lm|lux|°c|°f|c\b|%|"
    r"ملم|مم|سم|متر|لتر|مل|فولت|واط|أمبير|امبير|كجم|كغ|غرام|جرام)(?![\w])",
    re.IGNORECASE)
_NUMBER_TOKEN = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?(?![\d])")
# Arabic-Indic / Persian digits compare equal to ASCII digits and a decimal comma to
# a decimal point, so an inventor's own value is never read as invented.
_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹٫", "01234567890123456789.")


def _numbers(text):
    return {n.replace(",", ".") for n in _NUMBER_TOKEN.findall(_normalised(text).translate(_DIGITS))}
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
                or not all(isinstance(x, str) and x in ids["functions"] for x in c["serves"]) \
                or (c["attribution"], c["status"]) != (AI_PROPOSED, UNVERIFIED):
            return False
    for r in reply["relationships"]:
        if not (isinstance(r["kind"], str) and isinstance(r["from"], str)
                and isinstance(r["to"], str)) \
                or r["kind"] not in RELATIONSHIP_KINDS or r["from"] not in nodes or r["to"] not in nodes \
                or r["from"] == r["to"]:
            return False
    for a in reply["alternatives"]:
        if not isinstance(a["for_function"], str) or a["for_function"] not in ids["functions"] \
                or not isinstance(a["options"], list) \
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
    stated = _numbers(idea_text)                  # whole numbers, never substrings
    out = []
    for t in texts:
        for m in _UNIT_NUMBER.finditer(_normalised(t).translate(_DIGITS)):
            if m.group(1).replace(",", ".") not in stated:
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
# The held-out QUALIFICATION pack: authored blind and adjudicated prompt-blind AFTER the
# corrected instructions, schema and criteria were committed (pinned when frozen).
INPUT_PATH = os.path.join(_ROOT, "tests", "fixtures", "g1_component_concept_heldout_v2_inputs.json")
REFERENCE_PATH = os.path.join(_ROOT, "tests", "fixtures",
                              "g1_component_concept_heldout_v2_reference.json")
INPUT_SHA256 = "c083db315a7aa4ada00dcac2e54f42cbb861d08cf9a74f2dd505268199270576"
REFERENCE_SHA256 = "b3ddd17e45e3d14aa9e176496994ce285984a127ae5dffa83f1e98eaf3bac0f6"
FROZEN_BEFORE_PACK_COMMIT = "43bb93b5f4662553b21362cd93c514b9e1bd7363"   # corrected candidate
AUTHOR_COMMIT = "2da3ffea0522f5818a5bd3e04dc3b5f9d1b3a291"
ADJUDICATION_COMMIT = "ccf3b91f5a0dc30fcfb79dddc95ef54853d49a1e"
CASE_IDS = tuple("Q%02d" % i for i in range(1, 17))
# Owner disposition (2026-11-05): Q01 is the predeclared diagnostic anchor, the exact
# Owner-specified plant-watering idea the approved design requires; it is shared with the
# development pack. The pack is 15 newly authored cases plus this one known case; it is NOT
# claimed that all 16 are independently novel, and every verdict carries this disclosure.
DIAGNOSTIC_ANCHOR_CASE = "Q01"
PACK_DISCLOSURE = ("15 newly authored held-out cases plus one predeclared diagnostic anchor "
                   "(Q01, the Owner-specified plant-watering idea) that is shared with the "
                   "development pack; Q01 is not an independently novel case, and any result "
                   "must be interpreted with that limitation.")

# The DEVELOPMENT pack (v1): authored blind (f8b2809) against the first freeze (43c6b09),
# adjudicated twice prompt-blind (dbbb162, eedcdb2) and reconciled. The Execution Lead saw
# it before the instructions and criteria were corrected, so it is development evidence
# ONLY and is never a held-out qualification of the corrected candidate.
DEV_PACK_ID = "inventorai-g1-component-concept-01"
DEV_INPUT_PATH = os.path.join(_ROOT, "tests", "fixtures", "g1_component_concept_inputs_v1.json")
DEV_REFERENCE_PATH = os.path.join(_ROOT, "tests", "fixtures",
                                  "g1_component_concept_reference_v1.json")
DEV_INPUT_SHA256 = "e7bcc8a824e27c8cce0cbacfc3202bc309287563f5af877897ce18a75314e980"
DEV_REFERENCE_SHA256 = "701e5d01ee82395f977d19a7eeed387461d401de92e4df49cb598bdc9baa98a2"
DEV_CASE_IDS = tuple("C%02d" % i for i in range(1, 17))
DEV_COMMITS = {"first_freeze": "43c6b093a9269f0f6306d59f7dafc47403dd1c69",
               "author": "f8b2809d6a3f1e5327d2e4c1d8efa490ce5f3e35",
               "adjudication_1": "dbbb162813a50d7c1db98aa649929b7b42180026",
               "adjudication_2": "eedcdb269fcdbbca01cb2da61fa0a88110ccf475"}
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
    "K4": "Unsupported invention scope: a NON_DEVICE case must return outcome ABSTAIN; any "
          "RESPONDED reply, even with empty lists, fails (automatic).",
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
          "COMMITTED_DESIGN; an ambiguous case may otherwise safely abstain.",
    "G6": "Concept delivery: every POSITIVE, EXCLUSION and UNSUPPORTED case returns a VALID "
          "RESPONDED reply with at least one function and at least one component type "
          "(automatic). An ABSTAIN or an empty concept on such a case fails, so exclusion and "
          "unsupported-claim handling must be shown, not avoided.",
}
CONCEPT_GROUPS = ("POSITIVE", "EXCLUSION", "UNSUPPORTED")
DECISION_RULE = (
    "One separately authorized run binds these instructions, schema, criteria and decision rule, "
    "the pack's two hashes, the code revision and the model; nothing may be tuned on the pack "
    "afterwards. A case not attempted or without a reply (provider or transport failure) gives "
    "INCOMPLETE. Any critical failure (automatic, or a human K1 / K2 / K3 FAILURE), or a graded "
    "criterion (G1-G6) that can no longer pass, gives NO_GO. Otherwise, while any required human judgment "
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
            "diagnostic_anchor_case": DIAGNOSTIC_ANCHOR_CASE, "pack_disclosure": PACK_DISCLOSURE,
            "development_pack": {"pack_id": DEV_PACK_ID, "input_sha256": DEV_INPUT_SHA256,
                                 "reference_sha256": DEV_REFERENCE_SHA256, "commits": DEV_COMMITS,
                                 "status": "development evidence only, never a qualification"},
            "id_patterns": {k: v.pattern for k, v in _ID.items()},
            "schema_sha256": _sha(schema()), "limits": LIMITS, "groups": GROUPS,
            "varieties": VARIETIES, "criteria": CRITERIA, "decision_rule": DECISION_RULE,
            "review_questions": REVIEW_QUESTIONS, "attestation": ATTESTATION}


def preregistration_digest():
    return _sha(preregistration())


def _sha(value):
    raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False,
                                                          sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_pack(development=False):
    """The pinned pack and reference, checked for shape, balance and grounding. The
    default is the held-out qualification pack; ``development=True`` loads the v1
    development pack, which is evidence only and never a qualification."""
    if development:
        paths = (DEV_INPUT_PATH, DEV_INPUT_SHA256, DEV_REFERENCE_PATH, DEV_REFERENCE_SHA256)
        pack_id, case_ids = DEV_PACK_ID, DEV_CASE_IDS
    else:
        paths = (INPUT_PATH, INPUT_SHA256, REFERENCE_PATH, REFERENCE_SHA256)
        pack_id, case_ids = PACK_ID, CASE_IDS
    if paths[1] is None or paths[3] is None:
        raise PackError("pack not frozen")
    inputs = _load(paths[0], paths[1])
    reference = _load(paths[2], paths[3])
    if (inputs.get("pack_id") != pack_id or reference.get("pack_id") != pack_id
            or inputs.get("synthetic_only") is not True
            or inputs.get("status") != FROZEN_STATUS or reference.get("status") != FROZEN_STATUS):
        raise PackError("pack identity")
    cases, refs = inputs["cases"], reference["cases"]
    if [c["case_id"] for c in cases] != list(case_ids) or [r["case_id"] for r in refs] != list(case_ids):
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


def similarity_to_earlier_packs(cases, include_development=True):
    """The largest difflib ratio of each case against every earlier G1 pack's ideas and,
    by default, the v1 development pack. The Owner-specified plant-watering idea is the
    one text both component-concept packs must contain; it is compared with the
    campaign packs only."""
    def ideas(rel):
        with open(os.path.join(_ROOT, rel), encoding="utf-8") as fh:
            return [c["idea_text"].lower() for c in json.load(fh)["cases"]]
    earlier = [t for rel in EARLIER_PACKS for t in ideas(rel)]
    dev = ideas(os.path.relpath(DEV_INPUT_PATH, _ROOT)) if include_development else []
    out = {}
    for c in cases:
        pool = earlier + ([] if c["idea_text"] == PLANT_IDEA else dev)
        out[c["case_id"]] = max(difflib.SequenceMatcher(None, c["idea_text"].lower(), e).ratio()
                                for e in pool)
    return out


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
    out["concept_delivered"] = bool(valid and reply["functions"] and reply["component_types"])
    if g == "NON_DEVICE":
        if valid:                      # RESPONDED, whatever it contains: only ABSTAIN passes
            out["critical"].append("K4")
        return out

    # An abstention earns no concept credit, but what it DOES say is still judged by a
    # human: clarification questions (G5: "requests clarification first") and missing
    # information (G3), with K3 over its text. Malformed / rejected replies earn nothing.
    abstained = v["status"] == V_ABSTAIN
    asks = abstained and bool(reply["clarification_questions"])
    lists_unknowns = abstained and bool(reply["missing_information"])

    def item(key, kind, nothing, human_if=False):
        if valid or human_if:
            out["items"][key] = kind
        else:
            out["auto"][key] = nothing
    if abstained and (asks or lists_unknowns):
        out["items"]["%s:K3" % cid] = "K3"
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
            "numbers_not_in_idea": sorted(_numbers(proposed) - _numbers(case["idea_text"]))}
    for u in ref["expected_unknowns"]:
        item(u["unknown_id"], "G3", "NOT_RECOGNIZED", human_if=lists_unknowns)
    if g == "POSITIVE":
        for f in ref["essential_functions"]:
            item(f["function_id"], "G1", "MISSING")
        item("%s:G2" % cid, "G2", "NOT_COHERENT")
        item("%s:G4" % cid, "G4", "ABSENT")
    if g == "AMBIGUOUS":
        item("%s:G5" % cid, "G5", "SAFE_ABSTAIN", human_if=asks)
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
            "G6": all(s.get("concept_delivered") for s in scored if s["group"] in CONCEPT_GROUPS),
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
            "human_review_basis": HUMAN_REVIEW_BASIS, "pack_disclosure": PACK_DISCLOSURE}


# ─────────────────────────────────────────────────────────────────────────────
# PROSPECTIVE EVIDENCE-TRACED ASSESSMENT METHOD (v2) — G1-1/2 qualification repair
# ─────────────────────────────────────────────────────────────────────────────
# Authority: Owner / Execution Lead instruction "G1-1/2 PROSPECTIVE EVALUATION
# IMPLEMENTATION" (2026-11-06). PROSPECTIVE ONLY. Everything above this banner — the
# frozen candidate instructions, schema, references, criteria, thresholds, review
# questions, attestation, `score_case`, `review_items`, `check_assessment` and `decide` —
# is the v1 method of the one executed run (evidence `2f6925bd`) and is NOT changed; v1
# stays the only basis of that run's result (INCOMPLETE_REVIEW). This section reuses the
# v1 validator and per-case scorer (`validate`, `score_case`: the same automatic K1-K5 /
# G6 results and the same review-item ids) and replaces only how the human-judged G1 /
# G3 / G4 items are labelled, evidenced and credited, adds a predeclared central-outcome
# rule, and keeps assessment modes apart:
#   * DIAGNOSTIC — an evidence-traced assessment by an agent, an AI-assisted human or a
#     human, for learning about the instrument; its result is never a qualification;
#   * FORMAL — only a HUMAN reviewer under the UNCHANGED v1 attestation, on annotations
#     declared before any output existed. An AI-assisted formal basis is NOT available:
#     adopting one is an open Owner decision.
# A pointer check proves only that the cited text exists in the reply at that place: it
# never proves that the text satisfies the reference item. That stays the attributed
# assessor's judgment. Nothing here is imported by the product; no provider is called.
METHOD_V2_ID = "g1-component-concept-evidence-traced-method"
METHOD_V2_VERSION = "2.0"
EVALUATION_ID_V2 = "g1-component-concept-qualification-02"
V1_PREREGISTRATION_SHA256 = "97b5d9e17b49b57b2038da2bc305556e96d6fb68568c95cc11da4483a3eaec0c"

MODE_DIAGNOSTIC, MODE_FORMAL = "DIAGNOSTIC", "FORMAL"
ASSESSOR_KINDS = ("AGENT", "AI_ASSISTED_HUMAN", "HUMAN")
INSUFFICIENT_EVIDENCE, DISPUTED = "INSUFFICIENT_EVIDENCE", "DISPUTED"
INTENT_CLEAR, INTENT_AMBIGUOUS = "CLEAR", "AMBIGUOUS"
G1_V2 = ("ADDRESSED", "OPEN_DECISION_DISCLOSED", "ACKNOWLEDGED_ONLY", "MISSING",
         "INVENTED_DETAIL")
G4_COVERED, G4_PARTIAL = "REFERENCE_CHOICE_COVERED", "REFERENCE_CHOICE_PARTIAL"
G4_OTHER_VALID = "DIFFERENT_VALID_ALTERNATIVE"
G4_V2 = (G4_COVERED, G4_PARTIAL, G4_OTHER_VALID, "NOT_RELEVANT", "ABSENT")

REVIEW_QUESTIONS_V2 = dict(REVIEW_QUESTIONS)
REVIEW_QUESTIONS_V2.update({
    "G1": ("Match this reference function by MEANING across the whole reply (functions, component "
           "roles, relationships, alternatives, missing information, questions), never by its "
           "local id. ADDRESSED: the meaning is present and at least one role, relationship or "
           "flow provisionally performs it (open implementation choices are fine). "
           "OPEN_DECISION_DISCLOSED: the meaning is present and the reply says the MEANS depends "
           "on a named, unresolved fact or choice, with nothing performing it yet. "
           "ACKNOWLEDGED_ONLY: the need is only mentioned (context, a generic part, a general "
           "missing-information line). MISSING: nothing. INVENTED_DETAIL: answered with "
           "unsupported specifications. The model's own `resolution` field is never evidence. "
           "For an operating-context need (e.g. outdoors), the exposure itself must be "
           "represented: power, range or general 'conditions' do not represent it, and no "
           "proven protection or rating is required.", G1_V2),
    "G3": ("Does a SPECIFIC missing-information item, clarification question or alternative name "
           "this same unknown fact or decision? A general statement recognises only the unknowns "
           "it actually names; one element counts for several unknowns only if it names each.",
           ("RECOGNIZED", "NOT_RECOGNIZED")),
    "G4": ("For the reference's PREDECLARED choice and its two options: does one alternatives "
           "entry offer options for the same functional purpose that cover BOTH options "
           "(REFERENCE_CHOICE_COVERED), only one of them (REFERENCE_CHOICE_PARTIAL), or does the "
           "reply instead offer a different but legitimate alternative for another purpose or "
           "another dimension (DIFFERENT_VALID_ALTERNATIVE: recorded as valid, not a model "
           "failure, but no reference-coverage credit)? NOT_RELEVANT: unnecessary, contradictory "
           "or unsupported options. ABSENT: no alternatives.", G4_V2),
})
CREDITED_V2 = {"G1": ("ADDRESSED",), "G3": ("RECOGNIZED",), "G4": (G4_COVERED,)}
# Labels that must cite reply evidence (a claim that something IS in the reply).
_EVIDENCE_REQUIRED = {"G1": ("ADDRESSED", "OPEN_DECISION_DISCLOSED", "ACKNOWLEDGED_ONLY",
                             "INVENTED_DETAIL"),
                      "G3": ("RECOGNIZED",), "G4": (G4_COVERED, G4_PARTIAL, G4_OTHER_VALID,
                                                    "NOT_RELEVANT"),
                      "K1": (FAILURE,), "K2": (FAILURE,), "K3": (FAILURE,),
                      "G5": ("CLARIFIED", "COMMITTED_DESIGN")}
# Where the evidence for a label may come from (None: anywhere in the reply).
_EVIDENCE_SECTIONS = {("G3", "RECOGNIZED"): ("missing_information", "clarification_questions",
                                             "alternatives"),
                      ("G4", G4_COVERED): ("alternatives",), ("G4", G4_PARTIAL): ("alternatives",),
                      ("G4", G4_OTHER_VALID): ("alternatives",),
                      ("G5", "CLARIFIED"): ("clarification_questions",)}
_POINTER = re.compile(r"(stated|functions|component_types|relationships|alternatives|"
                      r"missing_information|clarification_questions|excluded_by_inventor)"
                      r"\[(0|[1-9][0-9]?)\](?:\.options\[(0|[1-9][0-9]?)\])?\Z")
POINTER_RULE = ("A pointer names ONE reply element: `functions[i]` (its text), `stated[i]` (text), "
                "`excluded_by_inventor[i]` (text), `component_types[i]` (type), `relationships[i]` "
                "(rendered '<from> <KIND> <to>' with each end replaced by its component type or "
                "function text, so no model-local id appears), `alternatives[i].options[j]`, "
                "`missing_information[i]`, `clarification_questions[i]`. Its quote must equal that "
                "text exactly. A verified quote proves the text is there, not that it satisfies "
                "the reference item.")
ANNOTATION_RULE = (
    "Method annotations are part of the reference and are declared, and blind-adjudicated, "
    "BEFORE any output is seen: per case `intent` (CLEAR or AMBIGUOUS); `central` — the "
    "function ids that together are the inventor's intended outcome (required for a CLEAR "
    "POSITIVE case); `context_needs` — {function id: terms naming the operating exposure}; "
    "`unknown_terms` — {unknown id: terms}; `choices` — the predeclared trade-offs, each "
    "{for_meaning, options: [A, B]}. Terms are a NECESSARY lexical guard on credited evidence, "
    "never sufficient. Annotations written after outputs were seen are diagnostic only.")
CRITERIA_V2 = dict(CRITERIA)
CRITERIA_V2.update({
    "G1": "Essential-function coverage over the POSITIVE cases, by meaning: credited are "
          "ADDRESSED, and OPEN_DECISION_DISCLOSED only where the reference allows the function to "
          "remain unresolved; ACKNOWLEDGED_ONLY, MISSING and INVENTED_DETAIL never. At least 80% "
          "overall and at least two-thirds per case (thresholds unchanged), AND every central "
          "function of a CLEAR-intent case credited (central-outcome rule).",
    "G3": "Unknown recognition: at least 70% of all reference unknowns RECOGNIZED by a specific, "
          "evidenced element that names them (threshold unchanged).",
    "G4": "Reference-choice coverage: at least 4 of the 6 POSITIVE cases REFERENCE_CHOICE_COVERED "
          "(threshold unchanged); a DIFFERENT_VALID_ALTERNATIVE is reported as legitimate but "
          "earns no reference-coverage credit.",
})
DECISION_RULE_V2 = (
    "The v1 rule with these prospective changes: the human-judged G1 / G3 / G4 items use the v2 "
    "labels and credit table; every credited (and every evidence-claiming) judgment cites "
    "verified reply pointers; a CLEAR-intent POSITIVE case whose central function is not "
    "credited fails G1 whatever its coverage ratio, while an ambiguous case that validly asks "
    "or abstains is judged under G5 and is never a central omission; INSUFFICIENT_EVIDENCE and "
    "DISPUTED earn nothing and keep the review incomplete. DIAGNOSTIC mode reports the computed "
    "outcome only as DIAGNOSTIC_ONLY. FORMAL mode needs a HUMAN reviewer under the v1 "
    "attestation and annotations declared before outputs; PRELIMINARY_GO there still only "
    "supports considering one provisional, unpersisted concept-presentation design for separate "
    "authorization, never production activation.")
SEMANTIC_BASIS = ("Pointer checks verify only that each cited quotation exists at its place in the "
                  "reply. Whether that evidence satisfies a reference item is the judgment of the "
                  "named assessor and is attributed to them; it is never established by the "
                  "pointer check.")


def preregistration_v2():
    return {"method_id": METHOD_V2_ID, "method_version": METHOD_V2_VERSION,
            "evaluation_id": EVALUATION_ID_V2,
            "v1_preregistration_sha256": V1_PREREGISTRATION_SHA256,
            "criteria": CRITERIA_V2, "decision_rule": DECISION_RULE_V2,
            "review_questions": REVIEW_QUESTIONS_V2,
            "credited": CREDITED_V2, "pointer_rule": POINTER_RULE,
            "annotation_rule": ANNOTATION_RULE, "semantic_basis": SEMANTIC_BASIS,
            "modes": [MODE_DIAGNOSTIC, MODE_FORMAL], "assessor_kinds": list(ASSESSOR_KINDS),
            "attestation_formal": ATTESTATION}


def preregistration_v2_digest():
    return _sha(preregistration_v2())


def _terms_ok(terms):
    return isinstance(terms, list) and terms and all(isinstance(t, str) and t.strip()
                                                     for t in terms)


def check_annotations(annotations, refs, formal=False):
    """Validated method annotations {case_id: annotation} for `refs`; PackError otherwise."""
    if not isinstance(annotations, dict) or set(annotations) != {"declared_before_outputs",
                                                                 "provenance", "cases"}:
        raise PackError("annotations shape")
    if formal and annotations["declared_before_outputs"] is not True:
        raise PackError("formal assessment needs annotations declared before any output")
    cases = annotations["cases"]
    if not isinstance(cases, dict) or not set(cases) <= set(refs):
        raise PackError("annotations name unknown cases")
    keys = {"intent", "central", "context_needs", "unknown_terms", "choices"}
    for cid, a in cases.items():
        ref = refs[cid]
        fids = {f["function_id"] for f in ref["essential_functions"]}
        uids = {u["unknown_id"] for u in ref["expected_unknowns"]}
        if not isinstance(a, dict) or set(a) != keys or a["intent"] not in (INTENT_CLEAR,
                                                                              INTENT_AMBIGUOUS):
            raise PackError("annotation shape: " + cid)
        if (ref["group"] == "AMBIGUOUS") != (a["intent"] == INTENT_AMBIGUOUS):
            raise PackError("intent contradicts the case group: " + cid)
        if not isinstance(a["central"], list) or not set(a["central"]) <= fids:
            raise PackError("central functions: " + cid)
        if ref["group"] == "POSITIVE" and a["intent"] == INTENT_CLEAR and not a["central"]:
            raise PackError("a clear POSITIVE case needs its central outcome declared: " + cid)
        for field, ids in (("context_needs", fids), ("unknown_terms", uids)):
            if not isinstance(a[field], dict) or not set(a[field]) <= ids \
                    or not all(_terms_ok(t) for t in a[field].values()):
                raise PackError("%s: %s" % (field, cid))
        if not isinstance(a["choices"], list) or not all(
                isinstance(c, dict) and set(c) == {"for_meaning", "options"}
                and isinstance(c["options"], list) and len(c["options"]) == 2
                and all(isinstance(o, str) and o.strip() for o in c["options"])
                for c in a["choices"]):
            raise PackError("choices: " + cid)
    return cases


def resolve_pointer(reply, pointer):
    """The exact reply text a pointer names, or PackError. Relationship ends are rendered
    by their component type / function text, never by a model-local id."""
    m = _POINTER.match(pointer) if isinstance(pointer, str) else None
    if not m or not isinstance(reply, dict):
        raise PackError("pointer grammar")
    section, i, j = m.group(1), int(m.group(2)), m.group(3)
    items = reply.get(section)
    if not isinstance(items, list) or i >= len(items):
        raise PackError("pointer out of range: " + pointer)
    item = items[i]
    if section == "alternatives":
        if j is None or not isinstance(item.get("options"), list) or int(j) >= len(item["options"]):
            raise PackError("an alternative pointer names one option: " + pointer)
        return item["options"][int(j)]
    if j is not None:
        raise PackError("options index outside alternatives: " + pointer)
    if section in ("missing_information", "clarification_questions"):
        return item
    if section == "component_types":
        return item["type"]
    if section == "relationships":
        label = {c["id"]: c["type"] for c in reply.get("component_types", [])}
        label.update({f["id"]: f["text"] for f in reply.get("functions", [])})
        if item.get("from") not in label or item.get("to") not in label:
            raise PackError("dangling relationship: " + pointer)
        return "%s %s %s" % (label[item["from"]], item["kind"], label[item["to"]])
    return item["text"]


def _verified_evidence(reply, evidence):
    out = []
    if not isinstance(evidence, list):
        raise PackError("evidence must be a list")
    for e in evidence:
        if not isinstance(e, dict) or set(e) != {"pointer", "quote"}:
            raise PackError("evidence entry shape")
        if resolve_pointer(reply, e["pointer"]) != e["quote"]:
            raise PackError("quotation does not match the reply at " + str(e["pointer"]))
        out.append(e)
    return out


def _has_term(quotes, terms):
    low = " ".join(_normalised(q).lower() for q in quotes)
    return any(_normalised(t).lower() in low for t in terms)


def check_assessment_v2(record, scored, replies, refs, annotations, report_sha256, varieties):
    """Normalised {item_id: label} of ONE v2 assessment record, or PackError. Validates the
    shape, the mode / assessor / attestation boundary, every pointer and quotation, the
    evidence each label needs, the declared lexical guards and the G4 option map. It never
    decides whether evidence semantically satisfies an item (that is the assessor's)."""
    keys = {"evaluation_id", "method", "report_sha256", "mode", "assessor", "attestation",
            "attested_on", "judgments"}
    if not isinstance(record, dict) or set(record) != keys:
        raise PackError("v2 assessment shape")
    if record["evaluation_id"] != EVALUATION_ID_V2 \
            or record["method"] != [METHOD_V2_ID, METHOD_V2_VERSION] \
            or record["report_sha256"] != report_sha256:
        raise PackError("v2 assessment is not bound to this method and report")
    a = record["assessor"]
    if not isinstance(a, dict) or set(a) != {"kind", "name", "languages"} \
            or a["kind"] not in ASSESSOR_KINDS \
            or not (isinstance(a["name"], str) and a["name"].strip()) \
            or not isinstance(a["languages"], list):
        raise PackError("assessor shape")
    if record["mode"] == MODE_FORMAL:
        if a["kind"] != "HUMAN":
            raise PackError("FORMAL needs a HUMAN reviewer; an AI-assisted formal basis is an "
                            "open Owner decision")
        if record["attestation"] != ATTESTATION or not (
                isinstance(record["attested_on"], str)
                and re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["attested_on"])):
            raise PackError("FORMAL needs the unchanged v1 attestation")
        if not {_VARIETY_LANGUAGE[v] for v in varieties} <= set(a["languages"]):
            raise PackError("reviewer competence does not cover the pack's languages")
        cases = check_annotations(annotations, refs, formal=True)
    elif record["mode"] == MODE_DIAGNOSTIC:
        if record["attestation"] is not None or record["attested_on"] is not None:
            raise PackError("a DIAGNOSTIC record claims no attestation")
        cases = check_annotations(annotations, refs)
    else:
        raise PackError("mode")
    kinds = {i: k for s in scored for i, k in s["items"].items()}
    case_of = {i: s["case_id"] for s in scored for i in s["items"]}
    judged = record["judgments"]
    if not isinstance(judged, dict) or not set(judged) <= set(kinds):
        raise PackError("judgment outside the review items")
    out = {}
    for item_id, j in judged.items():
        kind, cid = kinds[item_id], case_of[item_id]
        if j == NOT_ASSESSED:
            continue
        if not isinstance(j, dict) or not {"judgment", "evidence", "rationale"} <= set(j) \
                or not set(j) <= {"judgment", "evidence", "rationale", "option_map"}:
            raise PackError("judgment entry shape: " + item_id)
        label = j["judgment"]
        if label not in REVIEW_QUESTIONS_V2[kind][1] + (INSUFFICIENT_EVIDENCE,):
            raise PackError("judgment value: " + item_id)
        if not (isinstance(j["rationale"], str) and j["rationale"].strip()):
            raise PackError("every judgment states its rationale: " + item_id)
        evidence = _verified_evidence(replies.get(cid), j["evidence"])
        if label in _EVIDENCE_REQUIRED.get(kind, ()) and not evidence:
            raise PackError("label %s needs reply evidence: %s" % (label, item_id))
        allowed = _EVIDENCE_SECTIONS.get((kind, label))
        if allowed and any(e["pointer"].split("[")[0] not in allowed for e in evidence):
            raise PackError("evidence from the wrong place for %s: %s" % (label, item_id))
        ann = cases.get(cid)
        quotes = [e["quote"] for e in evidence]
        if kind == "G1" and label in ("ADDRESSED", "OPEN_DECISION_DISCLOSED") and ann \
                and item_id in ann["context_needs"] \
                and not _has_term(quotes, ann["context_needs"][item_id]):
            raise PackError("an operating-context need is not credited without evidence naming "
                            "the exposure: " + item_id)
        if kind == "G3" and label == "RECOGNIZED" and ann and item_id in ann["unknown_terms"] \
                and not _has_term(quotes, ann["unknown_terms"][item_id]):
            raise PackError("the cited evidence does not name this unknown: " + item_id)
        if kind == "G4":
            _check_option_map(replies.get(cid), label, j.get("option_map"), item_id)
        elif "option_map" in j:
            raise PackError("option_map belongs to G4 only: " + item_id)
        out[item_id] = label
    return out


def _check_option_map(reply, label, option_map, item_id):
    if label in (G4_COVERED, G4_PARTIAL):
        if not isinstance(option_map, dict) or not set(option_map) <= {"A", "B"} or not option_map:
            raise PackError("REFERENCE_CHOICE labels map the reference options: " + item_id)
        for p in option_map.values():
            if not (isinstance(p, str) and ".options[" in p):
                raise PackError("an option map names alternative options: " + item_id)
            resolve_pointer(reply, p)
        if label == G4_COVERED:
            if set(option_map) != {"A", "B"} or option_map["A"] == option_map["B"] \
                    or option_map["A"].split(".")[0] != option_map["B"].split(".")[0]:
                raise PackError("COVERED maps both options within ONE alternatives entry: "
                                + item_id)
        elif len(option_map) != 1:
            raise PackError("PARTIAL maps exactly one reference option: " + item_id)
    elif option_map is not None:
        raise PackError("only REFERENCE_CHOICE labels carry an option map: " + item_id)


def reconcile_v2(normalised_records):
    """Merge several validated records: an item all records label alike keeps that label;
    any disagreement is DISPUTED (never credited), with every position kept."""
    labels, positions = {}, {}
    for rec in normalised_records:
        for item_id, label in rec.items():
            positions.setdefault(item_id, []).append(label)
    for item_id, seen in positions.items():
        labels[item_id] = seen[0] if len(set(seen)) == 1 else DISPUTED
    return labels, positions


def _credited(kind, label, function=None):
    if kind == "G1" and label == "OPEN_DECISION_DISCLOSED":
        return bool(function and function["may_be_unresolved"])
    return label in CREDITED_V2.get(kind, ())


_UNRESOLVED = (NOT_ASSESSED, INSUFFICIENT_EVIDENCE, DISPUTED)


def case_findings_v2(scored_case, ref, annotation, labels):
    """Per-case v2 findings: function labels and credit, the central-outcome status, unknown
    credit and the reference-choice class. Pure; used by `decide_v2` and diagnostics."""
    cid = scored_case["case_id"]
    fns = {f["function_id"]: f for f in ref["essential_functions"]}
    label = lambda item_id: scored_case["auto"].get(item_id, labels.get(item_id, NOT_ASSESSED))
    functions = {fid: {"label": label(fid), "credited": _credited("G1", label(fid), f)}
                 for fid, f in fns.items() if fid in scored_case["items"]
                 or fid in scored_case["auto"]}
    central = "NOT_APPLICABLE"
    if annotation and annotation["intent"] == INTENT_CLEAR and annotation["central"] \
            and ref["group"] == "POSITIVE":
        if scored_case["status"] != V_VALID:
            central = "NOT_EVALUATED_NO_CONCEPT"        # G6 / K-rules govern a non-concept
        elif any(not functions[f]["credited"] and functions[f]["label"] in _UNRESOLVED
                 for f in annotation["central"]):
            central = "UNDETERMINED"
        elif all(functions[f]["credited"] for f in annotation["central"]):
            central = "REPRESENTED"
        else:
            central = "OMITTED"
    unknowns = {u["unknown_id"]: {"label": label(u["unknown_id"]),
                                  "credited": label(u["unknown_id"]) == "RECOGNIZED"}
                for u in ref["expected_unknowns"]}
    choice = label("%s:G4" % cid) if ref["group"] == "POSITIVE" else None
    return {"case_id": cid, "functions": functions, "central": central,
            "unknowns": unknowns, "choice": choice}


def decide_v2(scored, refs, annotations, labels, mode):
    """The v2 decision over one complete run's v1 per-case scores and normalised v2 labels.
    DIAGNOSTIC reports DIAGNOSTIC_ONLY with the computed outcome; FORMAL applies the rule."""
    if [s["case_id"] for s in scored] != list(CASE_IDS):
        return {"verdict": "INCOMPLETE"}
    if any(s["status"] == V_ERROR for s in scored):
        return {"verdict": "INCOMPLETE"}
    cases = annotations["cases"]
    kinds = {i: k for s in scored for i, k in s["items"].items()}
    findings = [case_findings_v2(s, refs[s["case_id"]], cases.get(s["case_id"]), labels)
                for s in scored]
    answer = {}
    for s in scored:
        answer.update(s["auto"])
        for item_id in s["items"]:
            answer[item_id] = labels.get(item_id, NOT_ASSESSED)
    critical = sorted({k for s in scored for k in s["critical"]}
                      | {kinds[i] for i, a in answer.items()
                         if kinds.get(i) in ("K1", "K2", "K3") and a == FAILURE})
    pos = [r for r in refs.values() if r["group"] == "POSITIVE"]
    by_case = {f["case_id"]: f for f in findings}

    def graded(optimistic):
        def got(kind, item_id, function=None):
            a = answer[item_id]
            return _credited(kind, a, function) or (optimistic and a in _UNRESOLVED)

        def ok(a, good):
            return a in good or (optimistic and a in _UNRESOLVED)
        fns = [f for r in pos for f in r["essential_functions"]]
        unknowns = [u["unknown_id"] for r in refs.values() for u in r["expected_unknowns"]]
        amb = [r["case_id"] for r in refs.values() if r["group"] == "AMBIGUOUS"]
        central_ok = all(by_case[r["case_id"]]["central"] not in ("OMITTED",)
                         and (optimistic or by_case[r["case_id"]]["central"] != "UNDETERMINED")
                         for r in pos)
        return {
            "G1": (sum(got("G1", f["function_id"], f) for f in fns) >= 0.8 * len(fns) and all(
                sum(got("G1", f["function_id"], f) for f in r["essential_functions"])
                >= (2 / 3) * len(r["essential_functions"]) for r in pos) and central_ok),
            "G2": sum(ok(answer["%s:G2" % r["case_id"]], {"COHERENT"}) for r in pos) >= 5,
            "G3": sum(got("G3", u) for u in unknowns) >= 0.7 * len(unknowns),
            "G4": sum(got("G4", "%s:G4" % r["case_id"]) for r in pos) >= 4,
            "G5": (sum(ok(answer["%s:G5" % c], {"CLARIFIED"}) for c in amb) >= 2
                   and not any(answer["%s:G5" % c] == "COMMITTED_DESIGN" for c in amb)),
            "G6": all(s.get("concept_delivered") for s in scored if s["group"] in CONCEPT_GROUPS),
        }
    final, reachable = graded(False), graded(True)
    unresolved = sorted(i for i, a in answer.items() if a in _UNRESOLVED)
    if critical or not all(reachable.values()):
        outcome = "NO_GO"
    elif unresolved:
        outcome = "INCOMPLETE_REVIEW"
    else:
        outcome = "PRELIMINARY_GO" if all(final.values()) else "NO_GO"
    result = {"critical": critical, "graded": final, "graded_reachable": reachable,
              "unresolved": unresolved,
              "central_omitted": sorted(f["case_id"] for f in findings
                                        if f["central"] == "OMITTED"),
              "different_valid_alternatives": sorted(
                  f["case_id"] for f in findings if f["choice"] == G4_OTHER_VALID),
              "semantic_basis": SEMANTIC_BASIS, "pack_disclosure": PACK_DISCLOSURE,
              "method": [METHOD_V2_ID, METHOD_V2_VERSION]}
    if mode == MODE_FORMAL:
        result["verdict"] = outcome
    else:
        result.update(verdict="DIAGNOSTIC_ONLY", diagnostic_outcome=outcome,
                      qualification="NOT A QUALIFICATION: diagnostic mode")
    return result


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
