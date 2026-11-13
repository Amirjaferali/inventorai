# -*- coding: utf-8 -*-
"""Test-only seam: G1 FAITHFUL-READBACK STATEMENT-REJECTION PROOF.

Shows ONE preserved reply of the merged G1 faithful-rephrasing campaign (#978)
in its native format (``rephrasing`` + ``statements``) beside the inventor's own
words, and lets the inventor say «ليس هذا ما أقصده» about ONE AI-authored
statement. Nothing here is mounted on a production route; no production module
imports it. It reuses, unchanged:

* the committed campaign report (pinned by its SHA-256) and the frozen pack;
* the faithful-rephrasing deterministic validator (``validate_reply``);
* the #975 interaction pattern: one-use HMAC-bound tokens over the exact
  displayed reading (``web.app._canonical_message`` / ``_answer_secret``),
  stale / replayed / tampered input refused, nothing persisted, and the
  inventor's description kept exactly as written.

A rejected statement is shown as rejected and never counts as confirmed
meaning; a confirmation covers the remaining statements as a reading of
intended meaning only. No reply is reshaped and no AI wording ever becomes
the inventor's description.
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
from scripts import g1_faithful_rephrasing_eval as ev
from scripts.g1_faithful_rephrasing_eval import VALID, validate_reply

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(_ROOT, "docs", "benchmarks", "evidence", "g1_faithful_rephrasing_v1",
                           "campaign_report.json")
REPORT_SHA256 = "3cc29443131c358855eafb4136d787740bcd5d7c86f85c123793fa568530695c"
CASES_USED = ("ar_gulf_kuwaiti-03", "ar_msa-01")
DOMAIN = "g1-faithful-readback-proof-v1"
SHOWN, REJECTED = "SHOWN", "REJECTED"
CONFIRMATION_SCOPE = "reading of intended meaning only"
AI_AUTHORED, INVENTOR_AUTHORED = "AI_AUTHORED", "INVENTOR_STATED"
_PENDING = {}


class ProofError(Exception):
    pass


def preserved(case_id):
    """(idea_text, reply, case) for ONE case, from the committed report as it
    is. The report must match its pinned digest; the case comes from the
    frozen, digest-checked pack."""
    if case_id not in CASES_USED:
        raise ProofError("case not used by this proof")
    with open(REPORT_PATH, "rb") as fh:
        raw = fh.read()
    if hashlib.sha256(raw).hexdigest() != REPORT_SHA256:
        raise ProofError("campaign report does not match its pinned digest")
    report = json.loads(raw.decode("utf-8"))
    cases, _ref = ev.load_pack()
    case = next(c for c in cases if c["case_id"] == case_id)
    row = next(r for r in report["rows"] if r["case_id"] == case_id)
    if row["provider_status"] != "RESPONDED":
        raise ProofError("no preserved reply for this case")
    return case["idea_text"], copy.deepcopy(row["reply"]), case


@dataclasses.dataclass(frozen=True)
class Statement:
    index: int
    kind: str
    text: str
    quote: str
    status: str


@dataclasses.dataclass(frozen=True)
class Readback:
    idea_text: str
    case_id: str
    reply: dict = dataclasses.field(compare=False, hash=False)
    reply_digest: str
    rephrasing: str
    statements: tuple
    rejected: tuple

    @property
    def remaining(self):
        return tuple(s.index for s in self.statements if s.status != REJECTED)


def build(idea_text, reply, case, rejected=()):
    """The readback, or None: the faithful-rephrasing validator must accept
    the reply as it is; only a REPHRASED reply has statements to show; every
    rejected index must name one of its statements, once."""
    if not isinstance(idea_text, str) or not idea_text.strip() or not isinstance(case, dict) \
            or case.get("idea_text") != idea_text:
        return None
    status, _reasons = validate_reply(reply, case)
    if status != VALID or reply["outcome"] != "REPHRASED":
        return None
    n = len(reply["statements"])
    if any(not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < n for i in rejected) \
            or len(set(rejected)) != len(rejected):
        return None
    rejected = tuple(sorted(rejected))
    statements = tuple(Statement(i, s["kind"], s["text"], s["source_quote"],
                                 REJECTED if i in rejected else SHOWN)
                       for i, s in enumerate(reply["statements"]))
    return Readback(idea_text=idea_text, case_id=case["case_id"], reply=copy.deepcopy(reply),
                    reply_digest=_digest(json.dumps(reply, sort_keys=True, ensure_ascii=False)),
                    rephrasing=reply["rephrasing"], statements=statements, rejected=rejected)


def _digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sig(nonce, rb):
    msg = appmod._canonical_message(DOMAIN, nonce, _digest(rb.idea_text), rb.reply_digest,
                                    rb.case_id, ",".join(str(i) for i in rb.rejected))
    return hmac.new(appmod._answer_secret(), msg, hashlib.sha256).hexdigest()


def issue(rb):
    """One-use token for ONE displayed readback, or None."""
    if not isinstance(rb, Readback):
        return None
    nonce = secrets.token_urlsafe(16)
    _PENDING[nonce] = True
    return nonce + "." + _sig(nonce, rb)


def resolve(token, rb, idea_text, case, action, index=None):
    """Act on a displayed readback ONCE, or return None without saying why
    (unknown / replayed token, stale idea text, tampered reading, invalid
    action or index). ``reject_statement`` returns a NEW readback in which
    that one statement is rejected and every other keeps its status;
    ``confirm`` covers the statements not rejected, as a reading of intended
    meaning only. Nothing is persisted and no project is created."""
    if not isinstance(token, str) or not isinstance(rb, Readback) \
            or action not in ("reject_statement", "confirm"):
        return None
    nonce, _, sig = token.partition(".")
    if not nonce or not sig or not _PENDING.get(nonce):
        return None
    if idea_text != rb.idea_text or not hmac.compare_digest(sig, _sig(nonce, rb)):
        return None
    if build(rb.idea_text, rb.reply, case, rb.rejected) != rb:
        return None
    if action == "reject_statement":
        if not isinstance(index, int) or isinstance(index, bool) or index in rb.rejected:
            return None
        new = build(rb.idea_text, rb.reply, case, rb.rejected + (index,))
        if new is None:
            return None
        _PENDING.pop(nonce, None)
        return {"action": "reject_statement", "readback": new, "token": issue(new),
                "rejected_by": INVENTOR_AUTHORED, "recorded": False}
    _PENDING.pop(nonce, None)
    return {"action": "confirm", "scope": CONFIRMATION_SCOPE,
            "confirmed_statements": rb.remaining, "rejected_statements": rb.rejected,
            "idea_origin": INVENTOR_AUTHORED, "idea_text": rb.idea_text,
            "recorded": False, "creates_project": False}


# ─────────────────────────────────────────────────────────────────────────────
# Presentation (fragment only; never mounted on a production page)
# ─────────────────────────────────────────────────────────────────────────────
TEXT_AR = {
    "title": "كيف قرأ InventorAI فكرتك",
    "badge": "قراءة كتبها الذكاء الاصطناعي، غير مُتحقَّق منها",
    "intro": "تأكّد أنها تطابق ما تقصده. هذا اختياري، ويمكنك أيضاً أن تبدأ مباشرة.",
    "your_words": "وصفك كما كتبته أنت تماماً",
    "rephrasing": "إعادة صياغة كتبها الذكاء الاصطناعي",
    "statements": "عبارات كتبها الذكاء الاصطناعي، كلٌّ منها بجانب كلماتك التي استند إليها",
    "ai_statement": "كتبها الذكاء الاصطناعي",
    "quote": "كلماتك كما كتبتها",
    "ai_quote": "اقتباس الذكاء الاصطناعي من كلماتك",
    "reject": "ليس هذا ما أقصده",
    "rejected": "رفضتَ هذه العبارة: ليست ما تقصده، ولن تُحسب ضمن المعنى الذي تؤكّده.",
    "confirm": "نعم، باقي العبارات هو ما أقصده",
    "boundary": ("تساعدك هذه القراءة فقط على التأكد من أن InventorAI فهم ما تقصده. وهي ليست فحصاً هندسياً، "
                 "ولا تُحفظ، ويبقى وصفك كما كتبته تماماً."),
}


def render(rb):
    """The Arabic fragment for ONE readback. Every AI-authored text and every
    inventor-authored text carries its own visible label."""
    t, e = TEXT_AR, html.escape
    out = ['<section class="g1-faithful-readback" dir="rtl" lang="ar" data-case="%s">' % e(rb.case_id),
           '<h2>%s</h2><p class="badge" data-ai-label>%s</p><p>%s</p>' % (e(t["title"]), e(t["badge"]), e(t["intro"])),
           '<h3>%s</h3><blockquote data-author="inventor" data-inventor-words><bdi>%s</bdi></blockquote>'
           % (e(t["your_words"]), e(rb.idea_text)),
           '<h3>%s</h3><p data-author="ai" data-rephrasing><bdi>%s</bdi></p>' % (e(t["rephrasing"]), e(rb.rephrasing)),
           '<h3>%s</h3><ol data-statements>' % e(t["statements"])]
    for s in rb.statements:
        own = s.quote in rb.idea_text
        label = t["quote"] if own else t["ai_quote"]
        if s.status == REJECTED:
            body = '<del><bdi>%s</bdi></del>' % e(s.text)
            tail = '<p data-rejected-note>%s</p>' % e(t["rejected"])
        else:
            body = '<bdi>%s</bdi>' % e(s.text)
            tail = '<button type="button" data-reject="%d">%s</button>' % (s.index, e(t["reject"]))
        out.append('<li data-statement="%d" data-status="%s">'
                   '<p data-author="ai"><span class="who">%s:</span> %s</p>'
                   '<p data-author="%s"><span class="who">%s:</span> «<bdi>%s</bdi>»</p>%s</li>'
                   % (s.index, s.status.lower(), e(t["ai_statement"]), body,
                      "inventor" if own else "ai", e(label), e(s.quote), tail))
    out.append('</ol><p data-boundary>%s</p>' % e(t["boundary"]))
    out.append('<button type="button" data-confirm>%s</button></section>' % e(t["confirm"]))
    return "".join(out)
