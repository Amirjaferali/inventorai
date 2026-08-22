"""Governed bilingual semantic registry — PVCG-R3-I.

File path      : engine/semantic_registry.py
Purpose        : hold the committed, diffable, deterministic registry of
                 governed concepts and their registered English/Arabic
                 surfaces, and decide — by table lookup only — which concepts
                 an input activates. Implements the structure frozen by
                 docs/governance/PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md §5
                 (AUTHORITATIVE, PR #551, merge 7b7aa2f1…).
Input contract : plain ``str`` inputs plus a governed gap type / domain id.
Output contract: ``activated_concepts`` returns a frozenset of ``concept_id``
                 strings; the other public helpers return ``bool`` or an
                 explicit basis string. Every helper is fail-closed: a
                 non-string, an unknown gap type, or an unknown domain yields
                 the empty / False result.
Prohibited     : state mutation, I/O, clock read, randomness, network call,
                 model call, filesystem access at decision time, stemming,
                 lemmatization, root extraction, fuzzy matching, edit distance,
                 transliteration inference, statistical tokenization, and any
                 dependency beyond the standard-library ``re`` and
                 ``unicodedata``.

WHAT THIS IS, STATED TRUTHFULLY
-------------------------------
This is a REGISTERED BILINGUAL CONCEPT MAPPING. It is not a semantic model, not
a translator, and not a language understander. Two inputs are governed-equivalent
for a gap when they activate the SAME registered concept set for that gap
(R3-C §5.3) — equivalence is a property of registered activation and of nothing
else. Wording that is not registered is, by definition, not governed-equivalent,
and the R2 fail-closed direction applies unchanged: uncertain equivalence is NOT
satisfaction. That residual — unregistered wording in either language — is a
KNOWN BOUND of R3, not a defect concealed here.

ENGLISH IS NEVER WIDENED BY THIS MODULE
---------------------------------------
Every English surface registered below is already an intent marker of the SAME
gap family in ``engine.gap_relevance`` (or, for the structural classes, already
an entry of the corresponding English table in ``engine.progression_loop`` /
the committed domain packs). The English surfaces exist here to DECLARE the
equivalence class and its provenance, never to add English recognition. The
invariant is machine-checked by ``tests/test_pvcg_r3i_semantic_stability.py``.
"""

import re
import unicodedata

from engine.idea_state import (
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
)

WORD = "word"
PHRASE = "phrase"

# ─────────────────────────────────────────────────────────────────────────────
# 1. BOUNDED NORMALIZATION (R3-C §9)
# ─────────────────────────────────────────────────────────────────────────────
# §9.1 Latin/English: NO normalization is added by R3. N-1 measured 8/8 English
# variants already materially stable, so any Latin casing/punctuation/Unicode
# folding here would be unjustified surface area. The only case handling applied
# to Latin text is the ``.lower()`` the CALLERS already performed before R3.
#
# §9.2 Arabic: exactly four transformations, each authorized and each with its
# necessity demonstrated by execution in the R3-I evidence:
#
#   NFC                      — authorized outright (canonical form; the
#                              prerequisite for any stable comparison).
#   Tatweel (U+0640) removal — authorized on demonstrated necessity.
#   Harakat / combining-mark  — authorized on demonstrated necessity.
#     removal
#   Alef variants أ إ آ ٱ → ا — authorized on demonstrated necessity.
#
# DELIBERATELY NOT IMPLEMENTED, because R3-C does NOT authorize them by default
# and R3 is not an Arabic-normalization project:
#   teh marbuta ة → ه            — lossy; needs a collision analysis + a
#                                  separate governed decision.
#   yeh ي ↔ alef maqsura ى        — same condition.
#   Arabic-Indic digits → ASCII  — NOT authorized; no evidence of necessity.
# Adding any of the three above requires a new governed decision, not a code
# change here.

_TATWEEL = "\u0640"  # ـ  ARABIC TATWEEL

#: The harakat (short vowels, tanween, shadda, sukun, superscript alef).
#: Explicit and finite. Deliberately EXCLUDES U+0653 maddah, U+0654 hamza
#: above and U+0655 hamza below, because those are hamza-carrier marks whose
#: removal would change letter identity — an unauthorized fold (§9.2).
_HARAKAT = frozenset(
    "\u064B"  # ً  fathatan
    "\u064C"  # ٌ  dammatan
    "\u064D"  # ٍ  kasratan
    "\u064E"  # َ  fatha
    "\u064F"  # ُ  damma
    "\u0650"  # ِ  kasra
    "\u0651"  # ّ  shadda
    "\u0652"  # ْ  sukun
    "\u0670"  # ٰ  superscript alef
)

#: Alef variants folded to bare alef. Explicit and finite — never a range scan.
_ALEF_VARIANTS = {
    "أ": "ا",  # أ  alef with hamza above
    "إ": "ا",  # إ  alef with hamza below
    "آ": "ا",  # آ  alef with madda above
    "ٱ": "ا",  # ٱ  alef wasla
}


def normalize_ar(text):
    """Return ``text`` under the four authorized Arabic transformations.

    Pure and deterministic. Applied to BOTH the input and the registered
    surfaces, so the comparison is symmetric by construction. Non-Arabic
    characters are affected only by NFC, which is identity for ASCII.
    """
    if not isinstance(text, str):
        return ""
    # (1) Unicode NFC — canonical composition.
    out = unicodedata.normalize("NFC", text)
    # (2) Tatweel removal — a pure elongation glyph carrying no meaning.
    out = out.replace(_TATWEEL, "")
    # (3) Harakat removal — an EXPLICIT, finite set, never a blanket
    #     category scan. A general "drop every Mn mark on the NFD form" rule
    #     is WRONG here: the hamza carriers ئ ؤ decompose into a base letter
    #     plus a combining hamza, so a blanket strip silently rewrites ئ→ي and
    #     ؤ→و. That is a yeh/alef-maqsura-class letter fold, which R3-C §9.2
    #     does NOT authorize. Only the vowel/gemination marks are removed.
    out = "".join(c for c in out if c not in _HARAKAT)
    # (4) Alef-variant folding — explicit table, four entries.
    if any(v in out for v in _ALEF_VARIANTS):
        out = "".join(_ALEF_VARIANTS.get(c, c) for c in out)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 2. TOKEN BOUNDARY (R3-C §9.3)
# ─────────────────────────────────────────────────────────────────────────────
# Arabic attaches proclitics without a space, so a naive substring rule over
# Arabic surfaces would over-match far more aggressively than the English word
# tables do. R2's T-1b lesson is applied literally: a phrase→word containment
# argument is UNSOUND, so word surfaces are matched by TOKEN and phrase surfaces
# by SUBSTRING, and the two are never mixed.
#
# For WORD surfaces one declared proclitic may be removed, and the REMAINDER
# MUST THEN EQUAL THE REGISTERED SURFACE EXACTLY. This is an exact table lookup
# after removing one string from a closed, explicitly declared list — it is not
# stemming, not morphology, not affix analysis, and it never inspects the
# remainder for structure. No suffix is ever removed: suffix stripping would be
# morphology and is prohibited by §9.4.
_AR_PROCLITICS = (
    "وال",  # وال  "and the"
    "بال",  # بال  "with the"
    "كال",  # كال  "like the"
    "فال",  # فال  "so the"
    "لل",        # لل   "for the"
    "ال",        # ال   "the"
    "و",              # و    "and"
    "ف",              # ف    "so/then"
    "ب",              # ب    "with/by"
    "ك",              # ك    "like"
    "ل",              # ل    "for/to"
)

#: A word surface shorter than this is never matched through a stripped
#: proclitic. Guards against a short surface being reached from an unrelated
#: token merely because its first letter happens to be a proclitic.
_MIN_PROCLITIC_SURFACE_LEN = 3

#: Letter runs. ``[^\W\d_]`` is Unicode-aware, so this tokenizes Arabic and
#: Latin identically and never splits inside a word.
_TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def _tokens(normalized_text):
    return frozenset(_TOKEN_RE.findall(normalized_text))


def _word_matches(surface, tokens):
    """True when a registered WORD surface is present as a whole token."""
    if surface in tokens:
        return True
    if len(surface) < _MIN_PROCLITIC_SURFACE_LEN:
        return False
    for token in tokens:
        for proclitic in _AR_PROCLITICS:
            if token.startswith(proclitic) and token[len(proclitic):] == surface:
                return True
    return False


def _surface_matches(surface, mode, normalized_text, tokens):
    if mode == PHRASE:
        return surface in normalized_text
    return _word_matches(surface, tokens)


# ─────────────────────────────────────────────────────────────────────────────
# 3. THE GOVERNED CONCEPT INVENTORY (R3-C §5.1)
# ─────────────────────────────────────────────────────────────────────────────
# Every record carries the five §5.1 fields. ``provenance`` names the governed
# question in ``engine.progression_loop.QUESTIONS`` the concept is drawn from —
# a concept with no governed-question provenance MUST NOT be registered, and
# inventing a concept no governed question expresses is prohibited (§5.6).
#
# ``owner`` is EXACTLY ONE gap family (§5.1/2). Where a concept would plausibly
# belong to two families it is NOT registered at all, and the fail-closed
# direction applies. Those deliberate omissions are recorded in
# ``COLLISION_DISPOSITIONS`` below so the decision is auditable rather than
# invisible.


class Concept(tuple):
    """A governed concept. Immutable, diffable, no behaviour beyond access."""

    __slots__ = ()

    def __new__(cls, concept_id, owner, provenance, en, ar):
        return tuple.__new__(cls, (concept_id, owner, provenance,
                                   tuple(en), tuple(ar)))

    concept_id = property(lambda self: self[0])
    owner = property(lambda self: self[1])
    provenance = property(lambda self: self[2])
    en_surfaces = property(lambda self: self[3])
    ar_surfaces = property(lambda self: self[4])


_MC_Q1 = "MECHANISM_COMPLETENESS/Q1 'Describe specifically HOW your invention works … the physical or functional steps it takes.'"
_MC_Q2 = "MECHANISM_COMPLETENESS/Q2 'What are the individual components or actions inside your mechanism? Name each one and what it does.'"
_PF_Q1 = "PHYSICAL_FEASIBILITY/Q1 'What physical principle does your mechanism rely on?'"
_PF_Q2 = "PHYSICAL_FEASIBILITY/Q2 'Does your invention consume or manage energy? … approximate power requirement and source?'"
_PF_Q3 = "PHYSICAL_FEASIBILITY/Q3 'What are the physical limits or constraints your mechanism must operate within?'"
_BA_Q1 = "BOUNDARY_AMBIGUITY/Q1 'What does your invention specifically NOT do or NOT cover? State at least one clear boundary.'"
_BA_Q2 = "BOUNDARY_AMBIGUITY/Q2 'Name one existing approach that is similar to yours. What makes yours different…'"
_BA_Q3 = "BOUNDARY_AMBIGUITY/Q3 '… would it still be your invention? What is the core that cannot be replaced?'"
_PM_Q1 = "PROBLEM_MECHANISM_FIT/Q1 '… describe the problem you are trying to solve. What is happening for the person or system…'"
_PM_Q2 = "PROBLEM_MECHANISM_FIT/Q2 'Why does your mechanism solve this problem rather than a different approach?'"
_PM_Q3 = "PROBLEM_MECHANISM_FIT/Q3 'Are there situations or conditions where your mechanism would not solve this problem…'"
_AI_Q1 = "ASSUMPTION_INVENTORY/Q1 'What are you taking for granted about your mechanism that you have not yet tested or verified?'"
_AI_Q2 = "ASSUMPTION_INVENTORY/Q2 'For each assumption you named, would your mechanism still work if that assumption turned out to be wrong?'"
_EG_Q1 = "EXPERTISE_GAP_AWARENESS/Q1 'What areas of technical knowledge would someone need to actually build or implement your mechanism?'"
_EG_Q2 = "EXPERTISE_GAP_AWARENESS/Q2 '… which ones represent genuine gaps where you would need to learn more or bring in someone else?'"

CONCEPTS = (
    # ── MECHANISM_COMPLETENESS ───────────────────────────────────────────────
    Concept("MC-STEP", MECHANISM_COMPLETENESS, _MC_Q1,
            (("step", WORD), ("steps", WORD)),
            (("خطوة", WORD), ("خطوات", WORD))),
    Concept("MC-STAGE", MECHANISM_COMPLETENESS, _MC_Q1,
            (("stage", WORD), ("stages", WORD)),
            (("مرحلة", WORD), ("مراحل", WORD))),
    Concept("MC-SEQUENCE", MECHANISM_COMPLETENESS, _MC_Q1,
            (("sequence", WORD),),
            (("تسلسل", WORD), ("تتابع", WORD))),
    Concept("MC-PROCESS", MECHANISM_COMPLETENESS, _MC_Q1,
            (("process", WORD), ("procedure", WORD)),
            (("عملية", WORD), ("اجراء", WORD))),
    Concept("MC-COMPONENT", MECHANISM_COMPLETENESS, _MC_Q2,
            (("component", WORD), ("components", WORD),
             ("part", WORD), ("parts", WORD)),
            (("مكون", WORD), ("مكونات", WORD), ("جزء", WORD), ("اجزاء", WORD))),
    Concept("MC-MODULE", MECHANISM_COMPLETENESS, _MC_Q2,
            (("module", WORD), ("modules", WORD),
             ("subsystem", WORD), ("subsystems", WORD)),
            (("وحدة", WORD), ("وحدات", WORD), ("نظام فرعي", PHRASE))),
    Concept("MC-ROTATE", MECHANISM_COMPLETENESS, _MC_Q2,
            (("rotates", WORD), ("rotate", WORD)),
            (("يدور", WORD), ("تدور", WORD), ("دوران", WORD))),
    Concept("MC-DRIVE", MECHANISM_COMPLETENESS, _MC_Q2,
            (("drives", WORD), ("drive", WORD),
             ("moves", WORD), ("move", WORD)),
            (("يدفع", WORD), ("تدفع", WORD), ("يحرك", WORD), ("تحرك", WORD))),
    Concept("MC-OPEN", MECHANISM_COMPLETENESS, _MC_Q2,
            (("opens", WORD), ("open", WORD)),
            (("يفتح", WORD), ("تفتح", WORD), ("فتح", WORD))),
    Concept("MC-CLOSE", MECHANISM_COMPLETENESS, _MC_Q2,
            (("closes", WORD), ("close", WORD)),
            (("يغلق", WORD), ("تغلق", WORD), ("اغلاق", WORD))),
    Concept("MC-CONVERT", MECHANISM_COMPLETENESS, _MC_Q2,
            (("converts", WORD), ("convert", WORD)),
            (("يحول", WORD), ("تحول", WORD), ("تحويل", WORD))),
    Concept("MC-MEASURE", MECHANISM_COMPLETENESS, _MC_Q2,
            (("measures", WORD), ("measure", WORD)),
            (("يقيس", WORD), ("تقيس", WORD), ("قياس", WORD))),
    Concept("MC-DETECT", MECHANISM_COMPLETENESS, _MC_Q2,
            (("detects", WORD), ("detect", WORD),
             ("senses", WORD), ("sense", WORD)),
            (("يكشف", WORD), ("تكشف", WORD),
             ("يستشعر", WORD), ("تستشعر", WORD))),
    Concept("MC-SEND", MECHANISM_COMPLETENESS, _MC_Q2,
            (("sends", WORD), ("send", WORD),
             ("transmits", WORD), ("transmit", WORD)),
            (("يرسل", WORD), ("ترسل", WORD), ("ارسال", WORD))),
    Concept("MC-RECEIVE", MECHANISM_COMPLETENESS, _MC_Q2,
            (("receives", WORD), ("receive", WORD)),
            (("يستقبل", WORD), ("تستقبل", WORD))),
    Concept("MC-TRIGGER", MECHANISM_COMPLETENESS, _MC_Q2,
            (("triggers", WORD), ("trigger", WORD),
             ("activates", WORD), ("activate", WORD),
             ("actuates", WORD), ("actuate", WORD)),
            (("يشغل", WORD), ("تشغل", WORD),
             ("ينشط", WORD), ("تنشط", WORD))),
    Concept("MC-LATCH", MECHANISM_COMPLETENESS, _MC_Q2,
            (("latch", WORD), ("latches", WORD)),
            (("مزلاج", WORD),)),
    Concept("MC-HOW-IT-WORKS", MECHANISM_COMPLETENESS, _MC_Q1,
            (("how it works", PHRASE), ("works by", PHRASE),
             ("step by step", PHRASE)),
            (("كيف يعمل", PHRASE), ("يعمل عن طريق", PHRASE),
             ("خطوة بخطوة", PHRASE))),

    # ── PHYSICAL_FEASIBILITY ────────────────────────────────────────────────
    Concept("PF-PRINCIPLE", PHYSICAL_FEASIBILITY, _PF_Q1,
            (("principle", WORD), ("principles", WORD), ("physics", WORD)),
            (("مبدا", WORD), ("مبادئ", WORD), ("فيزياء", WORD))),
    Concept("PF-ENERGY", PHYSICAL_FEASIBILITY, _PF_Q2,
            (("energy", WORD),),
            (("طاقة", WORD),)),
    Concept("PF-CONSUME", PHYSICAL_FEASIBILITY, _PF_Q2,
            (("consumes", WORD), ("consume", WORD), ("consumption", WORD)),
            (("يستهلك", WORD), ("تستهلك", WORD), ("استهلاك", WORD))),
    Concept("PF-POWER-REQUIREMENT", PHYSICAL_FEASIBILITY, _PF_Q2,
            (("power requirement", PHRASE), ("power requirements", PHRASE),
             ("power consumption", PHRASE), ("power source", PHRASE)),
            (("متطلبات الطاقة", PHRASE), ("مصدر الطاقة", PHRASE),
             ("استهلاك الطاقة", PHRASE))),
    Concept("PF-BATTERY", PHYSICAL_FEASIBILITY, _PF_Q2,
            (("battery", WORD), ("batteries", WORD), ("supply", WORD)),
            (("بطارية", WORD), ("بطاريات", WORD))),
    Concept("PF-TEMPERATURE", PHYSICAL_FEASIBILITY, _PF_Q3,
            (("temperature", WORD), ("thermal", WORD), ("heat", WORD)),
            (("حرارة", WORD), ("حراري", WORD))),
    Concept("PF-FREQUENCY", PHYSICAL_FEASIBILITY, _PF_Q3,
            (("frequency", WORD),),
            (("تردد", WORD),)),
    Concept("PF-MATERIAL", PHYSICAL_FEASIBILITY, _PF_Q3,
            (("material", WORD), ("materials", WORD)),
            (("مادة", WORD), ("مواد", WORD))),
    Concept("PF-CONSTRAINT", PHYSICAL_FEASIBILITY, _PF_Q3,
            (("constraint", WORD), ("constraints", WORD),
             ("tolerance", WORD), ("tolerances", WORD)),
            (("قيد", WORD), ("قيود", WORD), ("تحمل", WORD))),
    Concept("PF-PHYSICAL-LIMIT", PHYSICAL_FEASIBILITY, _PF_Q3,
            (("physical limit", PHRASE), ("physical limits", PHRASE),
             ("operating limit", PHRASE), ("operating range", PHRASE),
             ("temperature range", PHRASE)),
            (("الحدود الفيزيائية", PHRASE), ("حدود التشغيل", PHRASE),
             ("نطاق الحرارة", PHRASE))),
    Concept("PF-CAPACITY", PHYSICAL_FEASIBILITY, _PF_Q3,
            (("capacity", WORD), ("efficiency", WORD),
             ("feasible", WORD), ("feasibility", WORD)),
            (("سعة", WORD), ("كفاءة", WORD), ("جدوى", WORD))),

    # ── BOUNDARY_AMBIGUITY ──────────────────────────────────────────────────
    # Bare نطاق is NOT registered: it renders both BOUNDARY_AMBIGUITY "scope"
    # and PHYSICAL_FEASIBILITY "range", and registering it leaked the PF phrase
    # نطاق الحرارة into BOUNDARY_AMBIGUITY. Disambiguated phrases only (§10.2/1).
    Concept("BA-SCOPE", BOUNDARY_AMBIGUITY, _BA_Q1,
            (("boundary", WORD), ("boundaries", WORD), ("scope", WORD)),
            (("نطاق الاختراع", PHRASE), ("حدود الاختراع", PHRASE))),
    Concept("BA-NOT-COVER", BOUNDARY_AMBIGUITY, _BA_Q1,
            (("not cover", PHRASE), ("not intended", PHRASE)),
            (("لا يغطي", PHRASE), ("لا تغطي", PHRASE),
             ("غير مخصص", PHRASE))),
    Concept("BA-EXCLUDE", BOUNDARY_AMBIGUITY, _BA_Q1,
            (("exclude", WORD), ("excludes", WORD),
             ("excluded", WORD), ("excluding", WORD)),
            (("يستثني", WORD), ("تستثني", WORD), ("استثناء", WORD))),
    Concept("BA-DIFFERENT", BOUNDARY_AMBIGUITY, _BA_Q2,
            (("different", WORD), ("differs", WORD), ("differ", WORD),
             ("difference", WORD), ("differences", WORD),
             ("distinct", WORD), ("unlike", WORD)),
            (("مختلف", WORD), ("يختلف", WORD), ("تختلف", WORD),
             ("اختلاف", WORD))),
    Concept("BA-EXISTING", BOUNDARY_AMBIGUITY, _BA_Q2,
            (("existing", WORD), ("alternative", WORD),
             ("alternatives", WORD), ("competitor", WORD),
             ("competitors", WORD)),
            (("بديل", WORD), ("بدائل", WORD), ("منافس", WORD),
             ("الموجودة", WORD), ("القائمة", WORD))),
    Concept("BA-CORE-IRREPLACEABLE", BOUNDARY_AMBIGUITY, _BA_Q3,
            (("core", WORD), ("essential", WORD),
             ("irreplaceable", WORD), ("cannot be replaced", PHRASE)),
            # لا يمكن استبداله is a proper substring of لا يمكن استبدالها, so
            # the masculine form already matches the feminine input. Carrying
            # both would leave a structurally shadowed entry that can never be
            # independently operative (the R2 T-1b category); one entry is the
            # honest inventory.
            (("جوهر", WORD), ("اساسية", WORD), ("اساسي", WORD),
             ("لا يمكن استبداله", PHRASE))),
    Concept("BA-LIMITATION", BOUNDARY_AMBIGUITY, _BA_Q1,
            (("limitation", WORD), ("limitations", WORD),
             ("restricted", WORD), ("restricts", WORD)),
            (("محدودية", WORD), ("قصور", WORD))),

    # ── PROBLEM_MECHANISM_FIT ───────────────────────────────────────────────
    Concept("PM-PROBLEM", PROBLEM_MECHANISM_FIT, _PM_Q1,
            (("problem", WORD), ("problems", WORD),
             ("issue", WORD), ("issues", WORD)),
            (("مشكلة", WORD), ("مشاكل", WORD), ("مشكلات", WORD))),
    Concept("PM-USER", PROBLEM_MECHANISM_FIT, _PM_Q1,
            (("user", WORD), ("users", WORD), ("person", WORD),
             ("people", WORD), ("customer", WORD), ("customers", WORD)),
            (("مستخدم", WORD), ("مستخدمين", WORD), ("المستخدمون", WORD),
             ("الشخص", WORD))),
    Concept("PM-SUFFER", PROBLEM_MECHANISM_FIT, _PM_Q1,
            (("pain", WORD), ("suffer", WORD), ("suffers", WORD),
             ("struggle", WORD), ("struggles", WORD), ("matters", WORD)),
            (("يعاني", WORD), ("يعانون", WORD), ("معاناة", WORD),
             ("صعوبة", WORD))),
    Concept("PM-SOLVE", PROBLEM_MECHANISM_FIT, _PM_Q2,
            (("solves", WORD), ("solve", WORD), ("solved", WORD),
             ("solving", WORD), ("addresses", WORD)),
            (("يحل", WORD), ("تحل", WORD), ("حل", WORD), ("يعالج", WORD))),
    Concept("PM-RATHER-THAN", PROBLEM_MECHANISM_FIT, _PM_Q2,
            (("rather than", PHRASE), ("instead of", PHRASE),
             ("right fit", PHRASE)),
            (("بدلا من", PHRASE), ("عوضا عن", PHRASE))),
    Concept("PM-SITUATION", PROBLEM_MECHANISM_FIT, _PM_Q3,
            (("situation", WORD), ("situations", WORD),
             ("scenario", WORD), ("scenarios", WORD),
             ("condition", WORD), ("conditions", WORD)),
            (("حالة", WORD), ("حالات", WORD), ("ظروف", WORD),
             ("سيناريو", WORD))),
    Concept("PM-UNSUITABLE", PROBLEM_MECHANISM_FIT, _PM_Q3,
            (("unsuitable", WORD), ("suited", WORD), ("suitable", WORD),
             ("would not solve", PHRASE), ("less well", PHRASE)),
            (("غير مناسب", PHRASE), ("مناسبة", WORD), ("ملائم", WORD),
             ("لن يحل", PHRASE))),

    # ── ASSUMPTION_INVENTORY ────────────────────────────────────────────────
    Concept("AI-ASSUME", ASSUMPTION_INVENTORY, _AI_Q1,
            (("assume", WORD), ("assumes", WORD), ("assumed", WORD),
             ("assuming", WORD), ("presume", WORD), ("presumes", WORD),
             ("presumed", WORD)),
            (("افترض", WORD), ("نفترض", WORD), ("تفترض", WORD))),
    Concept("AI-ASSUMPTION", ASSUMPTION_INVENTORY, _AI_Q1,
            (("assumption", WORD), ("assumptions", WORD),
             ("hypothesis", WORD), ("hypotheses", WORD)),
            (("افتراض", WORD), ("افتراضات", WORD), ("فرضية", WORD))),
    # Arabic negation is a SEPARATE word ("غير"), so the negative sense lives in
    # the phrase, never in the bare participle: registering bare "مختبر"
    # (= tested) would invert the concept's meaning. Phrase mode only.
    Concept("AI-UNVERIFIED", ASSUMPTION_INVENTORY, _AI_Q1,
            (("unverified", WORD), ("untested", WORD),
             ("unproven", WORD), ("unconfirmed", WORD)),
            (("غير مختبر", PHRASE), ("غير متحقق", PHRASE),
             ("غير مثبت", PHRASE))),
    Concept("AI-TAKE-FOR-GRANTED", ASSUMPTION_INVENTORY, _AI_Q1,
            (("take for granted", PHRASE), ("taking for granted", PHRASE),
             ("taken for granted", PHRASE), ("granted", WORD)),
            (("امرا مسلما به", PHRASE), ("مسلمات", WORD))),
    Concept("AI-EXPECT", ASSUMPTION_INVENTORY, _AI_Q2,
            (("expect", WORD), ("expects", WORD), ("expected", WORD),
             ("believe", WORD), ("believed", WORD)),
            (("اتوقع", WORD), ("نتوقع", WORD), ("اعتقد", WORD))),
    Concept("AI-TURNED-OUT-WRONG", ASSUMPTION_INVENTORY, _AI_Q2,
            (("turned out to be wrong", PHRASE),),
            (("كان خاطئا", PHRASE), ("تبين خطؤه", PHRASE))),

    # ── EXPERTISE_GAP_AWARENESS ─────────────────────────────────────────────
    Concept("EG-EXPERTISE", EXPERTISE_GAP_AWARENESS, _EG_Q1,
            (("expertise", WORD), ("expert", WORD), ("experts", WORD),
             ("experience", WORD), ("experienced", WORD)),
            (("خبرة", WORD), ("خبير", WORD), ("خبراء", WORD))),
    Concept("EG-KNOWLEDGE", EXPERTISE_GAP_AWARENESS, _EG_Q1,
            (("knowledge", WORD), ("background", WORD)),
            (("معرفة", WORD), ("معارف", WORD), ("خلفية", WORD))),
    Concept("EG-SKILL", EXPERTISE_GAP_AWARENESS, _EG_Q1,
            (("skill", WORD), ("skills", WORD),
             ("competence", WORD), ("competency", WORD),
             ("qualified", WORD)),
            (("مهارة", WORD), ("مهارات", WORD), ("كفاءات", WORD))),
    Concept("EG-DISCIPLINE", EXPERTISE_GAP_AWARENESS, _EG_Q1,
            (("discipline", WORD), ("disciplines", WORD),
             ("engineering", WORD), ("engineer", WORD), ("engineers", WORD)),
            (("تخصص", WORD), ("تخصصات", WORD), ("الهندسة", WORD),
             ("مهندس", WORD))),
    Concept("EG-SPECIALIST", EXPERTISE_GAP_AWARENESS, _EG_Q2,
            (("specialist", WORD), ("specialists", WORD),
             ("consult", WORD), ("consultant", WORD),
             ("mentor", WORD), ("hire", WORD), ("professional", WORD)),
            (("اخصائي", WORD), ("متخصص", WORD), ("استشاري", WORD))),
    Concept("EG-LEARN", EXPERTISE_GAP_AWARENESS, _EG_Q2,
            (("learn", WORD), ("learning", WORD),
             ("training", WORD), ("trained", WORD),
             ("familiar", WORD), ("unfamiliar", WORD)),
            (("اتعلم", WORD), ("تعلم", WORD), ("تدريب", WORD))),
    Concept("EG-BRING-IN", EXPERTISE_GAP_AWARENESS, _EG_Q2,
            (("bring in", PHRASE), ("need help", PHRASE),
             ("someone else", PHRASE), ("would need to learn", PHRASE)),
            (("الاستعانة", WORD), ("افتقر", WORD), ("ينقصني", WORD))),
)


# ─────────────────────────────────────────────────────────────────────────────
# 4. STRUCTURAL CLASSES (R3-C §5.4)
# ─────────────────────────────────────────────────────────────────────────────
# Eligibility alone does not close D-2: the ASSERTED ceiling is produced by
# assess_response, not by addresses_gap. These two classes are what make the
# quality tier reachable for a registered Arabic answer.

#: Arabic counterparts of the English ``_CAUSAL_STRUCTURE_PATTERNS`` role in
#: ``engine.progression_loop``. Each entry names the English construction it
#: mirrors — it adds no new causal construction, and the English table is NOT
#: touched. Matched as PHRASE (substring) on normalized text: these are
#: connective/verb constructions that legitimately attach clitics, and a token
#: rule would miss the attached forms the English table matches by substring
#: too ("when " / "causes" are substrings in the English table).
CAUSAL_SURFACES = (
    ("عندما", "when "),
    ("حين", "when "),
    ("اذا", "if "),
    ("بعد ان", "after "),
    ("قبل ان", "before "),
    ("حتى", "until "),
    ("بمجرد", "once / as soon as "),
    ("يسبب", "causes"),
    ("تسبب", "causes"),
    ("ينتج", "produces"),
    ("تنتج", "produces"),
    ("يؤدي الى", "results in / leads to"),
    ("تؤدي الى", "results in / leads to"),
    ("يحول", "converts / transforms"),
    ("تحول", "converts / transforms"),
    ("ينقل", "transfers"),
    ("تنقل", "transfers"),
    ("يقيس", "measures"),
    ("تقيس", "measures"),
    ("يحسب", "calculates"),
    ("تحسب", "calculates"),
    ("يقارن", "compares"),
    ("تقارن", "compares"),
    ("يتجاوز", "exceeds"),
    ("تتجاوز", "exceeds"),
    ("يقفل", "locks"),
    ("تقفل", "locks"),
    ("يحرر", "releases"),
    ("تحرر", "releases"),
    ("يدفع", "pushes"),
    ("تدفع", "pushes"),
    ("يسحب", "pulls"),
    ("تسحب", "pulls"),
    ("يمنع", "blocks"),
    ("تمنع", "blocks"),
    ("يدور", "rotates"),
    ("تدور", "rotates"),
    ("من اجل", "in order to"),
    ("لكي", "in order to"),
    ("بحيث", "so that"),
    ("مما يعني", "which means"),
    ("مما يسبب", "which causes"),
    ("ثم", "then "),
)

#: Arabic surfaces for the ALREADY-COMMITTED per-domain substance signals.
#: One-to-one with an existing pack signal — this adds NO new signal concept,
#: NO pack edit, and NO domain-capability change (R3-C §5.4, §13.2). The packs
#: and ``engine/domain_rules.py`` stay byte-identical; these surfaces live here
#: and are merely CONSULTED alongside the pack signals.
SUBSTANCE_SURFACES = {
    "mechanical": {
        "piston": ("مكبس",),
        "spring": ("نابض", "زنبرك"),
        "valve": ("صمام",),
        "gear": ("ترس", "تروس"),
        "lever": ("ذراع", "رافعة"),
        "hydraulic": ("هيدروليكي", "هيدروليك"),
        "pneumatic": ("هوائي", "نيوماتي"),
        "pressure": ("ضغط",),
        "torque": ("عزم",),
        "compression": ("انضغاط",),
        "seal": ("حشية",),
        "bearing": ("محمل",),
        "actuator": ("مشغل",),
        "mechanism": ("الية",),
        "friction": ("احتكاك",),
    },
    "electronics_electrical": {
        "sensor": ("حساس", "مستشعر"),
        "microcontroller": ("متحكم",),
        "motor": ("محرك",),
        "pump": ("مضخة",),
        "relay": ("مرحل",),
        "display": ("شاشة",),
        "battery": ("بطارية",),
        "chip": ("رقاقة",),
        "resistor": ("مقاومة",),
        "capacitor": ("مكثف",),
        "transistor": ("ترانزستور",),
        "voltage": ("جهد",),
        "current": ("تيار",),
        "frequency": ("تردد",),
        "signal": ("اشارة",),
        "threshold": ("عتبة",),
        "filter": ("مرشح",),
        "data": ("بيانات",),
        "digital": ("رقمي",),
        "analog": ("تناظري",),
        "protocol": ("بروتوكول",),
        "infrared": ("الاشعة تحت الحمراء",),
        "ultrasonic": ("فوق صوتي",),
    },
}

#: Pack signals deliberately given NO Arabic surface, with the reason. Recorded
#: so the coverage decision is auditable rather than an unexplained omission.
#: None of these is a gap in equivalence: each is written in Latin script in
#: Arabic technical prose, so it already matches the existing pack signal.
SUBSTANCE_NO_ARABIC_SURFACE = {
    "arduino": "vendor name, written in Latin script in Arabic prose",
    "esp": "vendor name, written in Latin script in Arabic prose",
    "raspberry": "vendor name, written in Latin script in Arabic prose",
    "led": "initialism, written in Latin script in Arabic prose",
    "ic": "initialism, written in Latin script in Arabic prose",
    "ble": "initialism, written in Latin script in Arabic prose",
    "mqtt": "protocol initialism, written in Latin script in Arabic prose",
    "uart": "protocol initialism, written in Latin script in Arabic prose",
    "i2c": "protocol initialism, written in Latin script in Arabic prose",
    "spi": "protocol initialism, written in Latin script in Arabic prose",
    "wifi": "protocol name, written in Latin script in Arabic prose",
    "bluetooth": "protocol name, written in Latin script in Arabic prose",
    "hall": "eponym (Hall effect), written in Latin script in Arabic prose",
    "piezoelectric": "the Arabic term embeds the Latin-script root in practice",
    "capacitive": "adjectival form of 'capacitor', already covered by مكثف",
    "reads": "English verb signal; the Arabic verb class is covered by CAUSAL_SURFACES",
    "sends": "English verb signal; covered by CAUSAL_SURFACES / MC-SEND",
    "detects": "English verb signal; covered by MC-DETECT",
    "measures": "English verb signal; covered by CAUSAL_SURFACES / MC-MEASURE",
    "activates": "English verb signal; covered by MC-TRIGGER",
    "triggers": "English verb signal; covered by MC-TRIGGER",
    "converts": "English verb signal; covered by CAUSAL_SURFACES / MC-CONVERT",
    "transmits": "English verb signal; covered by MC-SEND",
    "receives": "English verb signal; covered by MC-RECEIVE",
    "processes": "English verb signal; no one-to-one Arabic noun surface registered",
    "samples": "English verb signal; no one-to-one Arabic noun surface registered",
    "outputs": "English verb signal; no one-to-one Arabic noun surface registered",
    "controls": "English verb signal; no one-to-one Arabic noun surface registered",
    "monitors": "English verb signal; no one-to-one Arabic noun surface registered",
    "calculates": "English verb signal; covered by CAUSAL_SURFACES",
}

#: Arabic counterparts of ``_ACKNOWLEDGED_UNKNOWN_MARKERS`` in
#: ``engine.progression_loop``. EXPLICIT inventor-marked uncertainty ONLY —
#: exactly mirroring the English rule that the bare technical word "unknown"
#: must never match. Each entry names the English marker it mirrors. PHRASE
#: mode: these are multi-word negations, and Arabic negation is a separate
#: particle, so substring on normalized text is the correct and safe rule.
ACKNOWLEDGED_UNKNOWN_SURFACES = (
    ("لا اعرف", "i do not know"),
    ("لا اعلم", "i do not know"),
    ("لست متاكدا", "i am not sure"),
    ("لست متاكد", "i am not sure"),
    ("لم احدد", "i have not yet determined"),
    ("لم اقرر", "i have not decided"),
    ("لم ابحث", "i have not yet researched"),
    ("لا يزال غير معروف", "it is still unknown"),
    ("ليس معروفا بعد", "this is not yet known"),
)

#: Deliberate collision dispositions (R3-C §10.2/1–3). A concept a governed
#: question expresses in more than one family is registered to exactly ONE
#: owner or NOT registered at all. These are the not-registered decisions.
COLLISION_DISPOSITIONS = {
    "حدود (bare 'limits/boundaries')":
        "NOT REGISTERED — genuinely ambiguous between BOUNDARY_AMBIGUITY "
        "('boundary') and PHYSICAL_FEASIBILITY ('physical limits'). Fail "
        "closed; the disambiguated phrases الحدود الفيزيائية (PF) and نطاق "
        "(BA) carry the two senses separately.",
    "لا اعرف كيف ('do not know how')":
        "NOT REGISTERED for EXPERTISE_GAP_AWARENESS even though the English "
        "phrases 'do not know how' / \"don't know how\" are EGA intent "
        "markers. Registering it would let a declared unknown create "
        "eligibility from an Arabic surface R3 itself introduced. Fail "
        "closed; the acknowledged-unknown track still records it.",
    "معرفة vs اعرف":
        "DISTINCT TOKENS after normalization — EG-KNOWLEDGE registers معرفة "
        "(knowledge); the unknown marker uses اعرف. No overlap.",
    "نطاق (bare 'scope/range')":
        "NOT REGISTERED — renders BOUNDARY_AMBIGUITY 'scope' AND "
        "PHYSICAL_FEASIBILITY 'range'. Measured: registering it made the PF "
        "phrase نطاق الحرارة activate BOUNDARY_AMBIGUITY. Fail closed; "
        "BA-SCOPE carries the disambiguated phrases نطاق الاختراع / حدود "
        "الاختراع instead.",
    "تشغيل (verbal noun 'operation/running')":
        "NOT REGISTERED — a generic verbal noun that matches far more broadly "
        "than the English trigger/activate verbs MC-TRIGGER mirrors. The "
        "finite verb forms يشغل / تشغل / ينشط / تنشط are registered instead.",
    "ضغط (pressure) vs يضغط (presses)":
        "DISTINCT TOKENS. ضغط is a mechanical SUBSTANCE surface, not an "
        "intent concept, so the two classes cannot collide.",
}


# ─────────────────────────────────────────────────────────────────────────────
# 5. DERIVED INDEXES + IMPORT-TIME VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
# The registry is validated when the module loads, so a malformed or colliding
# entry fails LOUDLY at import rather than silently degrading recognition.

class RegistryError(ValueError):
    """A malformed or colliding registry entry. Never caught internally."""


def _validate():
    seen_ids = set()
    owners = {MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
              PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY,
              EXPERTISE_GAP_AWARENESS}
    ar_owner = {}
    for c in CONCEPTS:
        if c.concept_id in seen_ids:
            raise RegistryError("duplicate concept_id: " + c.concept_id)
        seen_ids.add(c.concept_id)
        if c.owner not in owners:
            raise RegistryError("concept %s has no governed owner gap" % c.concept_id)
        if not c.provenance:
            raise RegistryError("concept %s has no governed-question provenance"
                                % c.concept_id)
        if not c.en_surfaces or not c.ar_surfaces:
            raise RegistryError("concept %s must carry both an English and an "
                                "Arabic surface set" % c.concept_id)
        for surface, mode in c.ar_surfaces:
            if mode not in (WORD, PHRASE):
                raise RegistryError("undeclared match_mode on %s" % c.concept_id)
            # Surfaces are compared against normalized input, so a surface that
            # is not already normalized could never match. Fail loud.
            if normalize_ar(surface) != surface:
                raise RegistryError(
                    "Arabic surface %r on %s is not in normalized form (expected %r)"
                    % (surface, c.concept_id, normalize_ar(surface)))
            if mode == WORD and " " in surface:
                raise RegistryError("word-mode surface %r on %s contains a space"
                                    % (surface, c.concept_id))
            # §10.2/3 — one concept, one owner: the SAME Arabic surface must
            # never be reachable from two gap families.
            prev = ar_owner.get(surface)
            if prev is not None and prev != c.owner:
                raise RegistryError(
                    "Arabic surface %r is registered to two gap families "
                    "(%s and %s)" % (surface, prev, c.owner))
            ar_owner[surface] = c.owner
    for surface, _mirrors in CAUSAL_SURFACES + ACKNOWLEDGED_UNKNOWN_SURFACES:
        if normalize_ar(surface) != surface:
            raise RegistryError("structural surface %r is not normalized" % surface)
    for domain_surfaces in SUBSTANCE_SURFACES.values():
        for signal, surfaces in domain_surfaces.items():
            for surface in surfaces:
                if normalize_ar(surface) != surface:
                    raise RegistryError(
                        "substance surface %r for signal %r is not normalized"
                        % (surface, signal))


_validate()

#: concept_id -> Concept
_BY_ID = {c.concept_id: c for c in CONCEPTS}
#: gap_type -> tuple of Concepts owned by that gap
_BY_OWNER = {}
for _c in CONCEPTS:
    _BY_OWNER.setdefault(_c.owner, []).append(_c)
_BY_OWNER = {k: tuple(v) for k, v in _BY_OWNER.items()}

#: The DECLARED inventory the test suite generates its probes from (R3-C
#: §10.3). Probes are generated from THIS declaration, never from the live
#: matcher tables, so deleting a registered surface leaves its probe in place
#: to fail rather than silently vanishing with the entry it protects.
DECLARED_INVENTORY = tuple(
    (c.concept_id, c.owner, surface, mode)
    for c in CONCEPTS for surface, mode in c.ar_surfaces
)

GOVERNED_OWNERS = tuple(sorted(_BY_OWNER))


# ─────────────────────────────────────────────────────────────────────────────
# 6. PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def activated_concepts(text, gap_type):
    """Return the set of concept_ids owned by ``gap_type`` that ``text`` activates.

    This is R3-C §5.2 ``activated(x, G)``: BOTH registered surface sets are
    consulted, so governed equivalence (§5.3) is decidable as set equality.
    Fail-closed on a non-string input or an unregistered gap type.
    """
    if not isinstance(text, str) or gap_type not in _BY_OWNER:
        return frozenset()
    normalized = normalize_ar(text.lower())
    tokens = _tokens(normalized)
    hits = []
    for concept in _BY_OWNER[gap_type]:
        for surface, mode in concept.ar_surfaces + concept.en_surfaces:
            if _surface_matches(surface, mode, normalized, tokens):
                hits.append(concept.concept_id)
                break
    return frozenset(hits)


def arabic_surface_activates(text, gap_type):
    """True when ``text`` carries a registered ARABIC surface of ``gap_type``.

    This is the ONLY hook ``engine.gap_relevance`` calls. It deliberately
    consults the Arabic surface sets alone, so R3 cannot widen English
    recognition by even one token — the English path stays exactly as PVCG-R2-I
    left it (R3-C §16.3).
    """
    if not isinstance(text, str) or gap_type not in _BY_OWNER:
        return False
    normalized = normalize_ar(text.lower())
    tokens = _tokens(normalized)
    for concept in _BY_OWNER[gap_type]:
        for surface, mode in concept.ar_surfaces:
            if _surface_matches(surface, mode, normalized, tokens):
                return True
    return False


def has_registered_causal_structure(text):
    """True when ``text`` carries a registered Arabic causal-structure surface.

    Mirrors the role of ``_CAUSAL_STRUCTURE_PATTERNS`` for Arabic. Adds no new
    causal construction and does not touch the English table.
    """
    if not isinstance(text, str):
        return False
    normalized = normalize_ar(text.lower())
    return any(surface in normalized for surface, _mirror in CAUSAL_SURFACES)


def substance_surface_present(text, domain):
    """True when ``text`` carries a registered Arabic surface of one of
    ``domain``'s ALREADY-COMMITTED substance signals.

    Consulted alongside — never instead of — the pack's own signals. Adds no
    signal to any pack and changes no domain capability.
    """
    if not isinstance(text, str):
        return False
    surfaces = SUBSTANCE_SURFACES.get(domain)
    if not surfaces:
        return False
    normalized = normalize_ar(text.lower())
    tokens = _tokens(normalized)
    for signal_surfaces in surfaces.values():
        for surface in signal_surfaces:
            mode = PHRASE if " " in surface else WORD
            if _surface_matches(surface, mode, normalized, tokens):
                return True
    return False


def detect_registered_unknown(text):
    """Return the registered Arabic unknown surface present in ``text``, or None.

    Explicit inventor-marked uncertainty ONLY. Returns the SURFACE so the
    caller can record a truthful ``category_basis``, exactly as the English
    marker path does. An acknowledged unknown never becomes satisfaction,
    never becomes REASONED, and never becomes DEMONSTRATED.
    """
    if not isinstance(text, str):
        return None
    normalized = normalize_ar(text.lower())
    for surface, _mirrors in ACKNOWLEDGED_UNKNOWN_SURFACES:
        if surface in normalized:
            return surface
    return None
