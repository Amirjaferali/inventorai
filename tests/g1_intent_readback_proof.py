# -*- coding: utf-8 -*-
"""G1-AI-INTENT-READBACK-CONSUMER-PROOF-01: TEST-ONLY proof seam.

An optional, source-bound pre-creation readback of an AI reading of the
inventor's idea, built ONLY from preserved provider replies (#928 campaign 02)
and constructed fixtures, so it can be compared with the existing /start path.
It is not a product capability: no route, template, store, provider call or
production module imports it. It reuses, unchanged:

* the #928 deterministic validator (``validate``): every quote must be copied
  from the idea text, concepts come from the closed governed list, and the
  mechanical-and-electrical suggestion is admitted only when both kinds of part
  remain;
* the #941 binding pattern: a domain-separated HMAC on the existing app secret
  and canonical encoding, one use, failing closed without saying why.

What the inventor can do with a readback: confirm that it reads their intended
meaning (scope: meaning only, never engineering, origin or progression),
reject it (it disappears and nothing changes), or mark one listed part as "not
part of my invention" with an optional remark kept verbatim. The idea text is
never rewritten, nothing is saved or recorded, nothing is pre-filled, and no
AI text ever reaches ``integrate_response`` or the ledger.
"""
import copy
import dataclasses
import hashlib
import hmac
import html
import json
import os
import secrets

import web.app as appmod
from scripts.run_g1_precreation_semantic_eval import SUGGEST_INTEGRATED, V_VALID, validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(ROOT, "tests", "fixtures", "g1_ai_intent_readback_proof_v1.json")
DOMAIN = "g1-precreation-intent-readback-proof-v1"
READING_ORIGIN = "AI_PROPOSED"
READING_STATUS = "UNQUALIFIED_SYNTHETIC_NOT_CHECKED"
INVENTOR_ORIGIN = "INVENTOR_STATED"
CONFIRMATION_SCOPE = "INTENDED_MEANING_ONLY"
ACTIONS = ("confirm", "reject", "correct")
_PENDING = {}                       # nonce -> True; in-memory, one use, test-only


def _load(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        raw = fh.read()
    return raw, json.loads(raw.decode("utf-8"))


def fixture():
    return json.loads(open(FIXTURE, encoding="utf-8").read())


def preserved(case_id):
    """(idea_text, preserved reply, source) for one #928 case, read from the
    hash-checked report and inputs; refuses any drift."""
    src = fixture()["preserved_source"]
    if case_id not in src["cases_used"]:
        raise ValueError("case not used by this proof")
    raw, report = _load(src["report"])
    raw_in, inputs = _load(src["inputs"])
    if hashlib.sha256(raw).hexdigest() != src["report_sha256"] \
            or hashlib.sha256(raw_in).hexdigest() != src["inputs_sha256"]:
        raise ValueError("preserved evidence drifted")
    idea = next(c["idea_text"] for c in inputs["cases"] if c["case_id"] == case_id)
    reply = next(r["reply"] for r in report["rows"] if r["case_id"] == case_id)
    return idea, reply, {"case_id": case_id, "evidence_ref": src["report"]}


def constructed(name):
    item = fixture()["constructed"][name]
    return item, {"case_id": name, "evidence_ref": FIXTURE[len(ROOT) + 1:]}


@dataclasses.dataclass(frozen=True)
class Part:
    text: str                       # the AI's wording (AI_PROPOSED)
    quote: str                      # the inventor's own words it rests on
    kind: str                       # governed concept id
    excluded_by_inventor: bool = False


@dataclasses.dataclass(frozen=True)
class Readback:
    idea_text: str
    reply: dict
    source: tuple
    excluded: tuple                 # part indexes the inventor said are not parts
    remark: str
    effective: str
    functions: tuple                # ((ai_text, quote), ...)
    parts: tuple                    # (Part, ...)
    unknowns: tuple                 # AI wording of what the inventor left open
    points_to_integrated: bool

    @property
    def origin(self):
        return READING_ORIGIN, READING_STATUS


def build(idea_text, reply, source, excluded=(), remark=""):
    """The readback, or None (UNAVAILABLE): no reply, a reply the #928
    validator does not accept, or an invalid correction. The inventor's
    exclusions are applied to a COPY before validation, so the existing V5 rule
    decides whether the mechanical-and-electrical pointer still applies."""
    if not isinstance(idea_text, str) or not idea_text.strip() or reply is None \
            or not isinstance(source, dict) or set(source) != {"case_id", "evidence_ref"}:
        return None
    if not isinstance(remark, str) or len(remark) > 300 or "\x00" in remark:
        return None
    parts_all = reply.get("stated_parts") if isinstance(reply, dict) else None
    if not isinstance(parts_all, list) or any(
            not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < len(parts_all)
            for i in excluded) or len(set(excluded)) != len(excluded):
        return None
    if validate(reply, idea_text)["status"] != V_VALID:
        return None
    kept = copy.deepcopy(reply)
    kept["stated_parts"] = [p for i, p in enumerate(reply["stated_parts"]) if i not in excluded]
    verdict = validate(kept, idea_text)
    if verdict["status"] != V_VALID:
        return None
    parts = tuple(Part(p["text"], p["source_quote"], p["candidate_concept"], i in excluded)
                  for i, p in enumerate(reply["stated_parts"]))
    return Readback(
        idea_text=idea_text, reply=copy.deepcopy(reply),
        source=(source["case_id"], source["evidence_ref"]),
        excluded=tuple(sorted(excluded)), remark=remark, effective=verdict["effective"],
        functions=tuple((f["text"], f["source_quote"]) for f in reply["stated_function"]),
        parts=parts, unknowns=tuple(reply["unknowns"]),
        points_to_integrated=verdict["effective"] == SUGGEST_INTEGRATED)


def _digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sig(nonce, rb):
    msg = appmod._canonical_message(
        DOMAIN, nonce, _digest(rb.idea_text),
        _digest(json.dumps(rb.reply, sort_keys=True, ensure_ascii=False)),
        rb.source[0], rb.source[1], ",".join(str(i) for i in rb.excluded), _digest(rb.remark))
    return hmac.new(appmod._answer_secret(), msg, hashlib.sha256).hexdigest()


def issue(rb):
    """One-use token for ONE displayed readback, or None."""
    if not isinstance(rb, Readback):
        return None
    nonce = secrets.token_urlsafe(16)
    _PENDING[nonce] = True
    return nonce + "." + _sig(nonce, rb)


def resolve(token, rb, idea_text, action, exclude_index=None, remark=""):
    """Act on a displayed readback ONCE, or return None without saying why:
    unknown / replayed token, a readback or idea text that changed since it was
    shown (stale), a tampered reading, or an invalid action. ``confirm``
    validates the reading of intended meaning only; ``reject`` drops it;
    ``correct`` returns a NEW readback (with a new token) in which the inventor's
    exclusion applies. Nothing is persisted or recorded."""
    if not isinstance(token, str) or not isinstance(rb, Readback) or action not in ACTIONS:
        return None
    nonce, _, sig = token.partition(".")
    if not nonce or not sig or not _PENDING.get(nonce):
        return None
    if idea_text != rb.idea_text or not hmac.compare_digest(sig, _sig(nonce, rb)):
        return None
    if build(rb.idea_text, rb.reply, {"case_id": rb.source[0], "evidence_ref": rb.source[1]},
             rb.excluded, rb.remark) != rb:
        return None
    _PENDING.pop(nonce, None)                                   # one use
    if action == "confirm":
        return {"action": "confirm", "scope": CONFIRMATION_SCOPE, "reading_origin": rb.origin,
                "idea_origin": INVENTOR_ORIGIN, "idea_text": rb.idea_text,
                "recorded": False, "creates_project": False}
    if action == "reject":
        return {"action": "reject", "shown": False, "recorded": False}
    new = build(rb.idea_text, rb.reply,
                {"case_id": rb.source[0], "evidence_ref": rb.source[1]},
                tuple(sorted(set(rb.excluded) | {exclude_index}))
                if isinstance(exclude_index, int) else (None,), remark)
    if new is None:
        return None
    return {"action": "correct", "readback": new, "token": issue(new),
            "remark_origin": INVENTOR_ORIGIN, "recorded": False}


# ─────────────────────────────────────────────────────────────────────────────
# Presentation (fragment only; never mounted on a production page)
# ─────────────────────────────────────────────────────────────────────────────
TEXT = {
    "en": {
        "title": "How InventorAI read your idea",
        "badge": "AI-proposed reading, not checked",
        "intro": "Check that this matches what you mean. It is optional: you can also start directly.",
        "your_words": "Your description, exactly as you wrote it",
        "for": "What your invention is for",
        "parts": "Parts of your invention that you mentioned",
        "quote": "your words",
        "kind_mechanical": "a mechanical part",
        "kind_electronics_electrical": "an electrical or electronic part",
        "kind_NO_GOVERNED_MAPPING": "a part InventorAI cannot place",
        "excluded": "You said this is not part of your invention",
        "remark": "Your remark, as written",
        "open": "Not decided yet",
        "open_note": "This stays open. You do not need to decide it to start, and InventorAI will not decide it for you.",
        "pointer": ("Your description mentions a mechanical part and an electrical or electronic part. If they work "
                    "together in your invention, the start page option \"My invention includes mechanical and "
                    "electrical/electronic parts that work together\" is the one that fits. InventorAI does not "
                    "tick it for you, and you name each part in your own words."),
        "no_pointer": "This reading does not point to the mechanical-and-electrical option.",
        "obstacle": ("Note: the mechanical-and-electrical option can only be chosen when a project is created; "
                     "adding it later needs a new project."),
        "boundary": ("This reading only helps you check that InventorAI understood what you mean. It is not an "
                     "engineering check, it is not saved, and your description stays exactly as you wrote it."),
        "confirm": "Yes, this is what I mean",
        "reject": "No, this is not what I mean",
        "not_part": "Not part of my invention",
    },
    "ar": {
        "title": "كيف قرأ InventorAI فكرتك",
        "badge": "قراءة مقترحة من الذكاء الاصطناعي، غير مُتحقَّق منها",
        "intro": "تأكّد أنها تطابق ما تقصده. هذا اختياري، ويمكنك أيضاً أن تبدأ مباشرة.",
        "your_words": "وصفك كما كتبته تماماً",
        "for": "الغرض من اختراعك",
        "parts": "أجزاء اختراعك التي ذكرتها",
        "quote": "كلماتك",
        "kind_mechanical": "جزء ميكانيكي",
        "kind_electronics_electrical": "جزء كهربائي أو إلكتروني",
        "kind_NO_GOVERNED_MAPPING": "جزء لا يستطيع InventorAI تصنيفه",
        "excluded": "قلتَ إن هذا ليس جزءاً من اختراعك",
        "remark": "ملاحظتك كما كتبتها",
        "open": "لم يُقرَّر بعد",
        "open_note": "يبقى هذا مفتوحاً. لا تحتاج إلى أن تقرّره لتبدأ، ولن يقرّره InventorAI نيابة عنك.",
        "pointer": ("يذكر وصفك جزءاً ميكانيكياً وجزءاً كهربائياً أو إلكترونياً. فإذا كانا يعملان معاً في اختراعك، "
                    "فخيار صفحة البدء «يتضمن اختراعي أجزاء ميكانيكية وكهربائية/إلكترونية تعمل معاً» هو المناسب. "
                    "لا يختاره InventorAI عنك، وأنت تسمّي كل جزء بكلماتك."),
        "no_pointer": "لا تشير هذه القراءة إلى خيار الأجزاء الميكانيكية والكهربائية.",
        "obstacle": ("ملاحظة: لا يمكن اختيار خيار الأجزاء الميكانيكية والكهربائية إلا عند إنشاء المشروع؛ "
                     "وإضافته لاحقاً تتطلب مشروعاً جديداً."),
        "boundary": ("تساعدك هذه القراءة فقط على التأكد من أن InventorAI فهم ما تقصده. وهي ليست فحصاً هندسياً، "
                     "ولا تُحفظ، ويبقى وصفك كما كتبته تماماً."),
        "confirm": "نعم، هذا ما أقصده",
        "reject": "لا، ليس هذا ما أقصده",
        "not_part": "ليس جزءاً من اختراعي",
    },
}


def render(rb, lang="en"):
    """An escaped, direction-isolated HTML fragment for ONE readback. Inventor
    words and AI words are always shown apart and labelled."""
    t = TEXT[lang]
    e = html.escape
    d = "rtl" if lang == "ar" else "ltr"
    out = ['<section class="g1-readback" lang="%s" dir="%s" data-readback-origin="%s">' % (lang, d, READING_ORIGIN),
           '<h2>%s</h2><p class="badge" data-ai-label>%s</p><p>%s</p>' % (e(t["title"]), e(t["badge"]), e(t["intro"])),
           '<h3>%s</h3><blockquote data-inventor-words><bdi>%s</bdi></blockquote>' % (e(t["your_words"]), e(rb.idea_text))]
    if rb.functions:
        out.append('<h3>%s</h3><ul>' % e(t["for"]))
        for text, quote in rb.functions:
            out.append('<li data-ai-text><bdi>%s</bdi> <small>(%s: «<bdi>%s</bdi>»)</small></li>'
                       % (e(text), e(t["quote"]), e(quote)))
        out.append('</ul>')
    shown = [(i, p) for i, p in enumerate(rb.parts) if not p.excluded_by_inventor]
    if shown:
        out.append('<h3>%s</h3><ul data-parts>' % e(t["parts"]))
        for i, p in shown:
            out.append('<li data-part="%d" data-kind="%s"><bdi data-ai-text>%s</bdi> — %s '
                       '<small>(%s: «<bdi>%s</bdi>»)</small> <button type="button" disabled>%s</button></li>'
                       % (i, e(p.kind), e(p.text), e(t["kind_" + p.kind]), e(t["quote"]), e(p.quote),
                          e(t["not_part"])))
        out.append('</ul>')
    for i, p in enumerate(rb.parts):
        if p.excluded_by_inventor:
            out.append('<p data-excluded="%d">%s: «<bdi>%s</bdi>»</p>' % (i, e(t["excluded"]), e(p.quote)))
    if rb.remark:
        out.append('<p data-inventor-remark>%s: «<bdi>%s</bdi>»</p>' % (e(t["remark"]), e(rb.remark)))
    for u in rb.unknowns:
        out.append('<p data-open><strong>%s:</strong> <bdi data-ai-text>%s</bdi> %s</p>'
                   % (e(t["open"]), e(u), e(t["open_note"])))
    if rb.points_to_integrated:
        out.append('<p data-pointer="integrated">%s</p>' % e(t["pointer"]))
    else:
        out.append('<p data-pointer="none">%s</p>' % e(t["no_pointer"]))
        if rb.unknowns:
            out.append('<p data-obstacle>%s</p>' % e(t["obstacle"]))
    out.append('<p data-boundary>%s</p>' % e(t["boundary"]))
    out.append('<p><button type="button" disabled>%s</button> <button type="button" disabled>%s</button></p>'
               % (e(t["confirm"]), e(t["reject"])))
    out.append('</section>')
    return "\n".join(out)
