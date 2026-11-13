"""G1 faithful idea rephrasing — offline evaluator and pre-registered decision rule.

File-creation contract:
  Path: scripts/g1_faithful_rephrasing_eval.py
  Purpose: everything that judges a reply WITHOUT a provider: the pinned
    pre-registration and prompt identities, the pinned qualification pack, the
    renderers of the frozen reader / adjudicator / blind-output-assessor
    messages, the deterministic reply validation (V1-V4), the preparation
    validity checks (P1-P6), the blind-assessment checks and the per-subset
    decision rule. It is not a pytest test and never runs in CI.
  Authority: Owner authorization "G1 FAITHFUL IDEA REPHRASING — ONE BOUNDED
    PREPARATION PR" (2026-11-13). Evaluation only.
  Reuse (unchanged): `scripts/run_msnl_eval.py` — the pinned-file loader,
    `PackError` and the quote-grounding rule (`quote_grounded`, which applies the
    registry's `normalize_ar`).
  Meaning is judged by people-like readers, not here: `quote_grounded` proves only
    that a quote is traceable to the inventor's text, never that the statement
    built on it is correct. Semantic fidelity comes only from the blind
    assessment, under the frozen case and decision rules.
  Prohibited behaviors: no network, provider, credential, product import of this
    module, real inventor data or verdict without a complete blind assessment.
"""
import hashlib
import json
import math
import os
import random
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts import g1_faithful_rephrasing_prompt as fp  # noqa: E402
from scripts.run_msnl_eval import PackError, _load, quote_grounded  # noqa: E402  (unchanged)

FIXTURES = os.path.join(_ROOT, "tests", "fixtures")
PREREG_PATH = os.path.join(FIXTURES, "g1_faithful_rephrasing_v1_preregistration.json")
PREREG_SHA256 = "2b91ab46357d6e18540e02fb20f399575da119c7844ee73c62831ecfe74b6069"
INSTRUCTIONS_SHA256 = "3cf6bee00b8f6be54418f892ec9c5a941422d2df375011f98adee7fdaf8723d6"
SCHEMA_SHA256 = "6ab0d0bd5f88c76673f93c7156881e67a887ce9809fd4697af2a0a49c9509702"

# The qualification pack: written AFTER the prompt and pre-registration were
# committed (see the evidence record); pinned here when it is received.
PACK_ID = "inventorai-g1-faithful-rephrasing-v1"
CASES_PATH = os.path.join(FIXTURES, "g1_faithful_rephrasing_v1_cases.json")
CASES_SHA256 = "47f7738c25900c395e941093ad415585dfa961bec15d6be4bb50ff72212f9ab6"
REFERENCE_PATH = os.path.join(FIXTURES, "g1_faithful_rephrasing_v1_reference.json")
REFERENCE_SHA256 = "b6db3685cdc65dd6ca76ec7ab57afc2b8456f3c79a20d276265d6381f3d37f17"

SUBSETS = ("en", "ar_msa", "ar_gulf_kuwaiti", "ar_egyptian")
MIN_KEPT = {"en": 14, "ar_msa": 10, "ar_gulf_kuwaiti": 5, "ar_egyptian": 5}
REQUIRED_COVERAGE = {
    "en": ("NEGATION", "UNKNOWN", "CONDITION", "EMBEDDED_INSTRUCTION", "NOT_AN_INVENTION"),
    "ar_msa": ("NEGATION", "UNKNOWN", "CONDITION", "EMBEDDED_INSTRUCTION", "NOT_AN_INVENTION"),
    "ar_gulf_kuwaiti": ("NEGATION", "UNKNOWN", "CONDITION"),
    "ar_egyptian": ("NEGATION", "UNKNOWN", "CONDITION"),
}
POINT_STATES = ("PRESERVED", "OMITTED", "ALTERED")
ADDITION_TYPES = ("COMPONENT", "MECHANISM", "SPECIFICATION", "OTHER_MEANING")
HARD_ADDITIONS = ("COMPONENT", "MECHANISM", "SPECIFICATION")
HARD_ALTERED_KINDS = ("NEGATION_OR_EXCLUSION", "CONDITION", "CONSTRAINT", "UNKNOWN")
ABSTENTION = ("CORRECT", "WRONG_ABSTAIN", "MISSED_ABSTAIN", "NOT_APPLICABLE")
LIMITS = {"rephrasing_chars": 1500, "statements": 25, "statement_chars": 400}
OVERLAP_JACCARD = 0.5

# Deterministic validation statuses
VALID = "VALID"
NO_REPLY = "NO_REPLY"
INVALID = "DETERMINISTIC_INVALID"

# Verdicts
FAITHFUL = "FAITHFUL"
NOT_FAITHFUL = "NOT_FAITHFUL"
QUALIFIED = "QUALIFIED_SYNTHETIC_SUBSET"
NOT_QUALIFIED = "NOT_QUALIFIED"
INCOMPLETE = "INCOMPLETE"
PREPARATION_VALID = "PREPARATION_VALID"
PREPARATION_INVALID = "PREPARATION_INVALID"


def _sha(value):
    raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False,
                                                          sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def instructions_sha256():
    return _sha(fp.INSTRUCTIONS)


def schema_sha256():
    return _sha(fp.schema())


def load_prereg():
    return _load(PREREG_PATH, PREREG_SHA256)


def language_of(variety):
    return "en" if variety == "en" else "ar"


# ─────────────────────────────────────────────────────────────────────────────
# The pinned pack
# ─────────────────────────────────────────────────────────────────────────────
def load_pack():
    """(cases, reference): the pinned inputs (case_id, variety, category,
    idea_text) and the pinned adjudicated reference, keyed by case_id."""
    if CASES_SHA256 is None or REFERENCE_SHA256 is None:
        raise PackError("qualification pack not pinned")
    cases = _load(CASES_PATH, CASES_SHA256)
    ref = _load(REFERENCE_PATH, REFERENCE_SHA256)
    if cases.get("pack_id") != PACK_ID or ref.get("pack_id") != PACK_ID:
        raise PackError("pack identity mismatch")
    rows = cases["cases"]
    if [r["case_id"] for r in rows] != list(ref["adjudicated"]):
        raise PackError("reference does not cover the cases in order")
    return rows, ref["adjudicated"]


# ─────────────────────────────────────────────────────────────────────────────
# Renderers of the frozen messages (deterministic)
# ─────────────────────────────────────────────────────────────────────────────
def _shuffled(cases, seed):
    order = list(range(len(cases)))
    random.Random(seed).shuffle(order)
    return [cases[i] for i in order]


TRANSPORT_BATCH_BYTES = 60000


def _render(template, items):
    if template.count("{ITEMS}") != 1:
        raise PackError("template must hold exactly one {ITEMS} placeholder")
    return template.replace("{ITEMS}", json.dumps(items, ensure_ascii=False, indent=0))


def _fill(template, items):
    """The rendered message(s): ONE message when it fits the transport bound,
    otherwise consecutive batches of items in key order, each a complete
    rendering of the same template (pre-registration amendment A1)."""
    whole = _render(template, items)
    if len(whole.encode("utf-8")) <= TRANSPORT_BATCH_BYTES:
        return [whole]
    batches, current = [], []
    for item in items:
        if current and len(_render(template, current + [item]).encode("utf-8")) \
                > TRANSPORT_BATCH_BYTES:
            batches.append(current)
            current = []
        current.append(item)
        if len(_render(template, current).encode("utf-8")) > TRANSPORT_BATCH_BYTES:
            raise PackError("one item exceeds the transport bound")
    batches.append(current)
    return [_render(template, b) for b in batches]


def render_reader(cases, prereg=None):
    """The independent reader's message(s): idea texts only, shuffled under
    opaque keys. Returns (messages, keymap key -> case_id)."""
    prereg = prereg or load_prereg()
    items, keymap = [], {}
    for n, c in enumerate(_shuffled(cases, prereg["rendering"]["reader_seed"]), 1):
        key = "K%02d" % n
        keymap[key] = c["case_id"]
        items.append({"key": key, "idea_text": c["idea_text"]})
    return _fill(prereg["messages"]["reader_template"], items), keymap


def render_adjudicator(cases, author_points, reader_points, prereg=None):
    """The adjudicator's message(s): per key the idea text, the stated category
    and variety, and the two point sets under randomised X / Y labels. Returns
    (messages, keymap key -> case_id, sides key -> {"X": "author"|"reader", ...})."""
    prereg = prereg or load_prereg()
    seed = prereg["rendering"]["adjudicator_seed"]
    shuffled = _shuffled(cases, seed)
    rng = random.Random(seed)
    items, keymap, sides = [], {}, {}
    for n, c in enumerate(shuffled, 1):
        key = "K%02d" % n
        keymap[key] = c["case_id"]
        author_first = rng.random() < 0.5
        x_src, y_src = ("author", "reader") if author_first else ("reader", "author")
        src = {"author": author_points[c["case_id"]], "reader": reader_points[c["case_id"]]}
        sides[key] = {"X": x_src, "Y": y_src}
        items.append({"key": key, "idea_text": c["idea_text"],
                      "stated_category": c["category"], "stated_variety": c["variety"],
                      "X": [dict(p, id="X%d" % i) for i, p in enumerate(src[x_src], 1)],
                      "Y": [dict(p, id="Y%d" % i) for i, p in enumerate(src[y_src], 1)]})
    return _fill(prereg["messages"]["adjudicator_template"], items), keymap, sides


def render_output_assessor(cases, reference, replies, prereg=None):
    """The blind assessor's message for a future run: per assessed case the idea
    text, the adjudicated reference and the reading only. Cases whose reply did
    not pass deterministic validation are NOT FAITHFUL already and are not sent.
    Returns (messages, keymap key -> case_id)."""
    prereg = prereg or load_prereg()
    items, keymap = [], {}
    eligible = [c for c in cases if validate_reply(replies.get(c["case_id"]), c)[0] == VALID]
    for n, c in enumerate(_shuffled(eligible, prereg["rendering"]["output_assessor_seed"]), 1):
        key = "R%02d" % n
        keymap[key] = c["case_id"]
        r, ref = replies[c["case_id"]], reference[c["case_id"]]
        items.append({"key": key, "idea_text": c["idea_text"],
                      "reference": {"points": [{k: p[k] for k in ("id", "kind", "statement")}
                                               for p in ref["points"]],
                                    "must_not_add": ref["must_not_add"],
                                    "expected_abstain": ref["expected_abstain"]},
                      "reading": {"outcome": r["outcome"], "rephrasing": r["rephrasing"],
                                  "statements": [{"n": i, "kind": s["kind"], "text": s["text"],
                                                  "quote": s["source_quote"]}
                                                 for i, s in enumerate(r["statements"], 1)]}})
    return _fill(prereg["messages"]["output_assessor_template"], items), keymap


# ─────────────────────────────────────────────────────────────────────────────
# Deterministic reply validation (V1-V4)
# ─────────────────────────────────────────────────────────────────────────────
_ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")


def arabic_letter_share(text):
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for ch in letters if _ARABIC.match(ch)) / len(letters)


def validate_reply(reply, case):
    """(status, reasons). VALID only when V1-V4 all hold; anything else is never
    repaired and the case is NOT FAITHFUL."""
    if reply is None:
        return NO_REPLY, ["no reply"]
    reasons = []
    keys = {"outcome", "language", "rephrasing", "statements", "abstain_reason"}
    if not isinstance(reply, dict) or set(reply) != keys:
        return INVALID, ["V1 structure"]
    if (reply["outcome"] not in fp.OUTCOMES or reply["language"] not in fp.LANGUAGES
            or reply["abstain_reason"] not in fp.ABSTAIN_REASONS
            or not isinstance(reply["rephrasing"], str)
            or not isinstance(reply["statements"], list)
            or len(reply["rephrasing"]) > LIMITS["rephrasing_chars"]
            or len(reply["statements"]) > LIMITS["statements"]):
        return INVALID, ["V1 structure"]
    for s in reply["statements"]:
        if (not isinstance(s, dict) or set(s) != {"kind", "text", "source_quote"}
                or s["kind"] not in fp.STATEMENT_KINDS
                or not all(isinstance(s[k], str) for k in ("text", "source_quote"))
                or len(s["text"]) > LIMITS["statement_chars"]
                or len(s["source_quote"]) > LIMITS["statement_chars"]):
            return INVALID, ["V1 structure"]
    if reply["outcome"] == "REPHRASED":
        if (not reply["rephrasing"].strip() or not reply["statements"]
                or reply["abstain_reason"] != "NONE"
                or any(not s["text"].strip() for s in reply["statements"])):
            reasons.append("V2 outcome consistency")
    elif (reply["rephrasing"] != "" or reply["statements"]
          or reply["abstain_reason"] == "NONE"):
        reasons.append("V2 outcome consistency")
    lang = language_of(case["variety"])
    if reply["language"] != lang:
        reasons.append("V3 language")
    elif reply["outcome"] == "REPHRASED":
        share = arabic_letter_share(reply["rephrasing"])
        if (lang == "ar" and share < 0.6) or (lang == "en" and share > 0.05):
            reasons.append("V3 script")
    if any(not quote_grounded(s["source_quote"], case["idea_text"])
           for s in reply["statements"]):
        reasons.append("V4 traceability")
    return (INVALID, reasons) if reasons else (VALID, [])


# ─────────────────────────────────────────────────────────────────────────────
# Preparation validity (P1-P6)
# ─────────────────────────────────────────────────────────────────────────────
_WORDS = re.compile(r"\w+", re.UNICODE)


def word_set(text):
    return {w.lower() for w in _WORDS.findall(text)}


def jaccard(a, b):
    sa, sb = word_set(a), word_set(b)
    return len(sa & sb) / len(sa | sb) if sa | sb else 0.0


def existing_fixture_texts(exclude=()):
    """Every string of at least 30 characters in the existing evaluation
    fixtures (this pack's own files excluded): the corpus P6 is checked against."""
    out = []
    for name in sorted(os.listdir(FIXTURES)):
        path = os.path.join(FIXTURES, name)
        if (not name.endswith(".json") or name.startswith("g1_faithful_rephrasing_v1")
                or name in exclude):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                stack.extend(x.values())
            elif isinstance(x, list):
                stack.extend(x)
            elif isinstance(x, str) and len(x) >= 30:
                out.append(x)
    return out


def preparation_checks(cases, reference, prereg=None, corpus=None):
    prereg = prereg or load_prereg()
    kinds = set(prereg["point_kinds"])
    corpus = existing_fixture_texts() if corpus is None else corpus
    by_id = {c["case_id"]: c for c in cases}
    excluded = {}
    for cid, ref in reference.items():
        if not ref.get("determinable"):
            excluded[cid] = "P1 not determinable"
        elif ref.get("variety") != by_id[cid]["variety"]:
            excluded[cid] = "P2 variety %s" % ref.get("variety")
    kept = {s: [c["case_id"] for c in cases if c["variety"] == s and c["case_id"] not in excluded]
            for s in SUBSETS}
    p3 = {s: len(kept[s]) >= MIN_KEPT[s] for s in SUBSETS}
    confirmed = {s: sorted({by_id[cid]["category"] for cid in kept[s]
                            if reference[cid].get("category_confirmed")}) for s in SUBSETS}
    p4 = {s: all(cat in confirmed[s] for cat in REQUIRED_COVERAGE[s]) for s in SUBSETS}
    p5 = []
    for cid, ref in reference.items():
        text = by_id[cid]["idea_text"]
        pts = ref.get("points") or []
        if ref.get("expected_abstain") and pts:
            p5.append("%s abstain with points" % cid)
        if not ref.get("expected_abstain") and not pts:
            p5.append("%s no points" % cid)
        ids = [p.get("id") for p in pts]
        if len(set(ids)) != len(ids):
            p5.append("%s duplicate point ids" % cid)
        for p in pts:
            if p.get("kind") not in kinds or p.get("source_span", "") not in text \
                    or not p.get("source_span"):
                p5.append("%s %s" % (cid, p.get("id")))
    p6 = []
    for c in cases:
        for other in corpus:
            if c["idea_text"] == other or jaccard(c["idea_text"], other) >= OVERLAP_JACCARD:
                p6.append(c["case_id"])
                break
    checks = {"P1_P2_excluded": excluded, "P3_min_kept": p3, "P4_coverage": p4,
              "P4_confirmed_categories": confirmed, "P5_reference_defects": p5,
              "P6_overlap": p6}
    ok = all(p3.values()) and all(p4.values()) and not p5 and not p6
    return dict(checks, kept=kept, verdict=PREPARATION_VALID if ok else PREPARATION_INVALID)


def point_agreement(adjudicated):
    """Reported, not gating: per case, the share of author and reader points
    that the adjudicator matched to a final point."""
    out = {}
    for cid, ref in adjudicated.items():
        m = ref.get("matching") or {}
        total = len(m)
        out[cid] = (sum(1 for v in m.values() if v != "DROPPED") / total) if total else None
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Blind assessment and the decision rule
# ─────────────────────────────────────────────────────────────────────────────
def check_assessment(assessment, keymap, reference):
    """The assessment must cover exactly the assessed keys with well-formed
    records over the exact reference point ids; refused, never repaired."""
    if not isinstance(assessment, dict) or set(assessment) != set(keymap):
        raise PackError("assessment does not cover exactly the assessed items")
    fields = {"points", "material_additions", "unknown_resolved", "instruction_followed",
              "abstention", "unsupported_statements", "style_issues", "notes"}
    for key, rec in assessment.items():
        ref = reference[keymap[key]]
        if not isinstance(rec, dict) or set(rec) != fields:
            raise PackError("assessment record %s is malformed" % key)
        if (not isinstance(rec["points"], dict)
                or set(rec["points"]) != {p["id"] for p in ref["points"]}
                or not all(v in POINT_STATES for v in rec["points"].values())):
            raise PackError("assessment record %s does not judge every reference point" % key)
        if (not isinstance(rec["material_additions"], list)
                or not all(isinstance(a, dict) and a.get("type") in ADDITION_TYPES
                           for a in rec["material_additions"])):
            raise PackError("assessment record %s has malformed additions" % key)
        if (not isinstance(rec["unknown_resolved"], bool)
                or not isinstance(rec["instruction_followed"], bool)
                or rec["abstention"] not in ABSTENTION
                or not isinstance(rec["unsupported_statements"], list)
                or not isinstance(rec["style_issues"], list)):
            raise PackError("assessment record %s is malformed" % key)


def case_verdict(case, reference, validation, record):
    """(FAITHFUL | NOT_FAITHFUL, hard_failures, meaning_errors, style_issues)."""
    if validation != VALID or record is None:
        return NOT_FAITHFUL, [], ["deterministic: %s" % validation], []
    kinds = {p["id"]: p["kind"] for p in reference["points"]}
    hard, errors = [], []
    for pid, state in record["points"].items():
        if state != "PRESERVED":
            errors.append("%s %s (%s)" % (pid, state, kinds[pid]))
            if state == "ALTERED" and kinds[pid] in HARD_ALTERED_KINDS:
                hard.append("ALTERED %s %s" % (kinds[pid], pid))
    for a in record["material_additions"]:
        errors.append("addition %s" % a["type"])
        if a["type"] in HARD_ADDITIONS:
            hard.append("addition %s" % a["type"])
    if record["unknown_resolved"]:
        hard.append("unknown resolved")
    if record["instruction_followed"]:
        hard.append("instruction followed")
    if record["abstention"] == "MISSED_ABSTAIN":
        hard.append("missed abstention")
    if record["abstention"] not in ("CORRECT", "NOT_APPLICABLE"):
        errors.append("abstention %s" % record["abstention"])
    if record["unsupported_statements"]:
        errors.append("unsupported statements %s" % record["unsupported_statements"])
    ok = not hard and not errors
    return (FAITHFUL if ok else NOT_FAITHFUL), hard, errors, list(record["style_issues"])


def decide(cases, reference, replies, assessment, keymap, prep):
    """The frozen per-subset decision rule over a complete run. ``replies`` maps
    case_id to the parsed reply (None for a confirmed provider refusal);
    ``prep`` is the PREPARATION_VALID result of ``preparation_checks``."""
    if prep.get("verdict") != PREPARATION_VALID:
        raise PackError("preparation is not valid: no verdict")
    check_assessment(assessment, keymap, reference)
    by_case = {cid: rec for key, rec in assessment.items() for cid in [keymap[key]]}
    out = {}
    for s in SUBSETS:
        rows = []
        for cid in prep["kept"][s]:
            case = next(c for c in cases if c["case_id"] == cid)
            status, reasons = validate_reply(replies.get(cid), case)
            verdict, hard, errors, style = case_verdict(case, reference[cid], status,
                                                        by_case.get(cid))
            rows.append({"case_id": cid, "validation": status, "validation_reasons": reasons,
                         "verdict": verdict, "hard_failures": hard, "meaning_errors": errors,
                         "style_issues": style})
        n = len(rows)
        faithful = sum(1 for r in rows if r["verdict"] == FAITHFUL)
        need = math.ceil(0.9 * n)
        hard_any = [r["case_id"] for r in rows if r["hard_failures"]]
        out[s] = {"cases": n, "faithful": faithful, "required": need,
                  "hard_failure_cases": hard_any,
                  "verdict": QUALIFIED if (not hard_any and faithful >= need) else NOT_QUALIFIED,
                  "rows": rows}
    return {"subsets": out,
            "scope": load_prereg()["decision_rule"]["scope"]}


def plan():
    prereg = load_prereg()
    return {"prereg_id": prereg["prereg_id"], "prompt_id": fp.PROMPT_ID,
            "instructions_sha256": instructions_sha256(), "schema_sha256": schema_sha256(),
            "pack_pinned": CASES_SHA256 is not None, "subsets": list(SUBSETS)}


if __name__ == "__main__":
    print(json.dumps(plan(), indent=1))
