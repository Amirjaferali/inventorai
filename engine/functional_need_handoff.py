"""FUNCTIONAL-NEED-TO-CAPABILITY-HANDOFF-01 — read-only functional-role projection.

What it is: a pure, deterministic reading of the inventor's own statements
(their original idea text and their active answers) that PROPOSES which of
three closed functional roles the inventor asked their invention to perform:
WATERING, FAN and SCREEN_SUPPORT. Every proposal is ``SYSTEM_PROPOSED``: it is
InventorAI's reading of the inventor's words, never a confirmed requirement,
an engineering input, a selected component or a design result.

What it is not: open-ended language understanding, a semantic model or a new
concept registry. The R3-C registry (``engine.semantic_registry``) is reused,
not widened: its Arabic normalization is applied character by character so
every quote keeps its original offsets, and its registered unknown surfaces
(with the English markers of ``engine.progression_loop``) mark the inventor's
explicit "I don't know how". The role words below are a closed table owned
here and read by nothing else.

Semantic rule (Lead correction): a role is PROPOSED only on positive evidence.
In one clause, a first-person want ("I want", "we need", "أريد", "أبي",
"ودي"...) must come before the role word with only a closed set of words
between them (function words, device nouns, a few adjectives, the role's own
words), and the role word must govern its object: only connector words ("for
my", "the", "حق", "على") may stand between them, and an English object may
not merely modify a following noun ("TV room"). Generic nouns ("device", "جهاز") are never intent, so a description of
someone else's device is not the inventor's request. A negation that directly
governs the want or the role word reads NEGATED. Any other negation in the
sentence, a reversing word ("stop", "avoid", "instead", "يمنع", "بدل"), a
hypothetical before the want, a past or third-person want, a question, or an
"I am not sure" before the role word ABSTAINS. "Without" excludes only what it
governs: "without a pump" keeps the role, "without watering" negates it. Words
these tables do not list are not read at all, so unlisted phrasing produces no
proposal rather than a guessed one.

Pure: no I/O, no clock, no state, no persistence, no model or provider call.
"""
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
import re
import unicodedata

from engine.progression_loop import _ACKNOWLEDGED_UNKNOWN_MARKERS
from engine.semantic_registry import (
    ACKNOWLEDGED_UNKNOWN_SURFACES, _AR_PROCLITICS, normalize_ar)

GRAMMAR_VERSION = "functional_roles_v1"
INTERPRETATION_STATUS = "SYSTEM_PROPOSED"

ROLE_WATERING = "WATERING"
ROLE_FAN = "FAN"
ROLE_SCREEN_SUPPORT = "SCREEN_SUPPORT"
ROLES = (ROLE_WATERING, ROLE_FAN, ROLE_SCREEN_SUPPORT)

AFFIRMED = "AFFIRMED"
NEGATED = "NEGATED"
ABSTAINED = "ABSTAINED"

PROPOSED = "PROPOSED"
CONFLICTING = "CONFLICTING"

SOURCE_IDEA = "IDEA"
SOURCE_ANSWER = "ANSWER"

OBJECT_NONE = "NONE"

# The existing engineering owners a role may be RELATED to. Readiness is never
# held here: the web layer reads it from each owner's own gate. CAP-12 is not
# related to support design, and THERM-01 is not a room-cooling method, so
# neither appears. A role with no related owner still shows what no InventorAI
# method covers.
CAP13_CONDITIONAL_REACTIONS = "CAP13_CONDITIONAL_REACTIONS"
CAP09_EXPERIMENT_PLANNING = "CAP09_EXPERIMENT_PLANNING"
ROLE_CAPABILITY_REFERENCES = {
    ROLE_WATERING: (CAP09_EXPERIMENT_PLANNING,),
    ROLE_FAN: (CAP09_EXPERIMENT_PLANNING,),
    ROLE_SCREEN_SUPPORT: (CAP13_CONDITIONAL_REACTIONS,),
}

# ---------------------------------------------------------------------------
# Closed tables. Latin surfaces are lower case; Arabic surfaces are written in
# their normalized form (normalize_ar: no harakat or tatweel, bare alef).
# A word matches a token exactly, or after ONE declared Arabic proclitic
# (the registry's own list, same length guard); no suffix is ever removed.
# ---------------------------------------------------------------------------
_ROLE_TRIGGERS = {
    ROLE_WATERING: frozenset({
        "water", "waters", "watering", "waterer", "irrigate", "irrigates",
        "irrigating", "irrigation",
        "يسقي", "تسقي", "اسقي", "نسقي", "سقي", "سقاية", "ري", "يروي", "تروي",
        "يسجي", "تسجي", "اسجي", "يرش", "ترش"}),
    ROLE_FAN: frozenset({
        "fan", "fans", "مروحة", "مروحه", "مراوح", "بنكة", "بنكه", "پنكة", "پنكه"}),
    ROLE_SCREEN_SUPPORT: frozenset({
        "stand", "stands", "holder", "holders", "support", "supports", "hold",
        "holds", "raise", "raises", "riser", "mount", "mounts", "bracket",
        "lift", "lifts",
        "حامل", "حاملة", "يحمل", "تحمل", "يرفع", "ترفع", "رفع", "قاعدة",
        "ستاند", "يثبت", "تثبت", "تثبيت", "يسند", "مسند", "يشيل", "تشيل",
        "يعلق", "تعلق"}),
}
_ROLE_OBJECTS = {
    ROLE_WATERING: {
        "PLANTS": frozenset({
            "plant", "plants", "pot", "pots", "planter", "planters", "seedling",
            "seedlings", "flower", "flowers",
            "نبات", "نباتات", "نبتة", "نبته", "نباتاتي", "نبتتي", "زرع", "زرعي",
            "زرعة", "شتلة", "شتلات", "ورد", "زهور", "اصيص", "اصص"}),
        "GARDEN": frozenset({
            "garden", "lawn", "grass", "yard", "حديقة", "حديقتي", "حديقه",
            "عشب", "ثيل", "حشيش"}),
    },
    ROLE_FAN: {
        "ROOM": frozenset({"room", "bedroom", "غرفة", "غرفه", "غرفتي", "حجرة",
                           "حجرتي"}),
        "DEVICE": frozenset({"laptop", "computer", "pc", "لابتوب", "كمبيوتر",
                             "حاسوب", "حاسب"}),
    },
    ROLE_SCREEN_SUPPORT: {
        "SCREEN": frozenset({"screen", "screens", "monitor", "monitors",
                             "display", "displays", "شاشة", "شاشه", "شاشتي",
                             "مونيتر", "شاشات"}),
        "TV": frozenset({"tv", "television", "تلفزيون", "تلفاز", "تلفزيوني"}),
    },
}
#: Roles whose trigger alone, without an object word, may still be proposed.
#: For them any object word later in the clause only keys the proposal.
_OBJECT_OPTIONAL = frozenset({ROLE_FAN})
#: English "fan" also means admirer; it is read only with an air / switching
#: word in the same clause, or when a negation governs it (Arabic "مروحة" is
#: unambiguous).
_EN_FAN_CONTEXT = frozenset({
    "air", "cool", "cools", "cooling", "blow", "blows", "blowing", "spin",
    "spins", "temperature", "hot", "heat", "automatic", "automatically",
    "switch", "switches", "turns", "ceiling", "room", "bedroom", "laptop",
    "computer"})
#: English "water(s)" is also a noun ("how much water", "the water in the
#: pot"): read as the role only right after one of these words.
_EN_WATER_VERB_BEFORE = frozenset({
    "to", "that", "which", "it", "will", "can", "should", "automatically",
    "also", "i", "we", "would", "could"})
_EN_WATER_NOUN_VERBS = frozenset({"water", "waters"})

#: Words that may stand between a role word and its object.
_CONNECTORS = frozenset({
    "for", "of", "my", "the", "a", "an", "our", "your", "all", "up", "both",
    "حق", "على", "فوق", "الى", "كل", "مال"})

#: English words that may sit between a connector and the object ("my
#: computer screen", "the indoor plants").
_EN_MODIFIERS = frozenset({
    "computer", "laptop", "pc", "desktop", "desk", "indoor", "house", "home",
    "small", "big", "new", "old", "office", "kitchen", "balcony", "potted",
    "little", "wide", "heavy", "main", "second", "tv", "garden"})
#: Nouns after which an object word is only a modifier ("monitor cable").
_EN_OBJECT_MODIFIED = frozenset({
    "cable", "cables", "cord", "cords", "wire", "wires", "remote", "remotes",
    "light", "lights", "lamp", "brightness", "cover", "case", "protector",
    "cleaner", "port", "ports", "settings", "speaker", "speakers", "glasses"})

# First-person intent. English: a want / build verb right after "i" / "we"
# (fillers allowed between), or "my / our idea / invention". Arabic: the
# first-person forms themselves.
_EN_INTENT_VERBS = frozenset({
    "want", "need", "like", "plan", "build", "building", "make", "making",
    "design", "designing", "create", "creating"})
_EN_SUBJECTS = frozenset({"i", "we"})
_EN_FILLERS = frozenset({"really", "also", "just", "would", "d", "am", "m", "re",
                         "are", "still", "only", "do"})
_EN_OWN_IDEA = (frozenset({"my", "our"}), frozenset({"idea", "invention", "project"}))
_AR_INTENT = frozenset({
    "اريد", "نريد", "ارغب", "نرغب", "احتاج", "نحتاج", "اصمم", "نصمم", "اصنع",
    "نصنع", "ابي", "نبي", "ابغى", "ابغي", "نبغى", "ودي", "بدي", "ابا", "اسوي",
    "نسوي", "فكرتي", "اختراعي", "اود", "نود"})
#: ما joined to a first-person want, as commonly written in Gulf Arabic.
_AR_FUSED_NEGATED_INTENT = frozenset({
    "مابي", "ماابي", "مابغى", "ماابغى", "مابغي", "ماودي", "مااريد", "مانبي"})

_NEGATION_WORDS = frozenset({
    "not", "no", "never", "cannot",
    "لا", "لن", "لم", "ليس", "ليست", "لست", "ما", "مش", "مو", "مب", "موب", "ابدا",
    "ماني", "مانيب"})
#: Words that reverse or deny the request without being a negation particle.
_REVERSING_WORDS = frozenset({
    "stop", "stops", "stopping", "prevent", "prevents", "preventing", "avoid",
    "avoids", "avoiding", "refuse", "refuses", "nothing", "nobody", "neither",
    "nor", "instead", "remove", "removes", "removing", "hate", "against",
    "rather", "replace",
    "يوقف", "توقف", "يمنع", "تمنع", "امنع", "ارفض", "نرفض", "بدل", "بدلا",
    "عوضا", "يزيل", "تزيل", "ازيل", "اكره", "يبطل"})
#: The only words that may stand between the want and the role word
#: ("I want [to build] [a small] [device] [that] waters", "أبي [جهاز] [عشان]
#: يسقي"). Any other word there ("quit", "sell", "get rid of", "أشيل",
#: "أوقف") means the want governs something else, so the clause abstains.
_EN_PATH = frozenset({
    "to", "a", "an", "the", "my", "our", "some", "that", "which", "it", "will",
    "can", "should", "would", "could", "automatically", "automatic", "device",
    "system", "gadget", "machine", "thing", "something", "tool", "small",
    "simple", "smart", "new", "little", "wooden", "cooling", "electric",
    "portable", "adjustable", "desk", "desktop", "tabletop", "self", "is", "be",
    "and", "also", "really", "just", "build", "make", "design", "create",
    "building", "making", "designing", "creating", "me", "one", "sturdy",
    "solar", "for"})
_AR_PATH = frozenset({
    "ان", "جهاز", "جهازا", "نظام", "نظاما", "الة", "شي", "شيء", "شيئا", "حاجة",
    "حاجه", "تلقائي", "تلقائيا", "ذكي", "ذكيا", "ذكيه", "صغير", "صغيرا",
    "صغيره", "خشبي", "خشبيا", "بسيط", "بسيطا", "اسوي", "نسوي", "اصنع", "نصنع",
    "اصمم", "نصمم", "ابني", "نبني", "لي", "هو", "يكون", "عشان", "حتى", "كي",
    "لكي", "يقدر", "تقدر", "يستطيع", "اوتوماتيكي", "اوتوماتيك", "كهربائي"})
_PATH_BASE = (_EN_PATH | _AR_PATH | _EN_INTENT_VERBS | _AR_INTENT | _EN_SUBJECTS
              | _EN_FILLERS)
#: English words that may follow an object word; any other word means the
#: object only modifies it ("TV channel", "monitor team", "TV room").
_EN_OBJECT_FOLLOW = frozenset({
    "and", "or", "to", "that", "which", "when", "while", "so", "on", "in", "at",
    "with", "from", "up", "every", "each", "during", "by", "above", "under",
    "without", "whenever", "because", "if", "as", "using", "for", "of",
    "automatically", "daily", "regularly", "too", "also", "but", "is", "are",
    "will", "should", "can", "it", "safely", "level", "higher", "high", "off",
    "here", "there", "all", "properly", "steady", "stable", "nicely"})

#: Words that dispose of or replace something ("the stand ... removed",
#: "... to be cancelled", "حامل الشاشة يتشال"): the clause abstains. "off"
#: and «تطفي» are not here, because an automatic fan that "turns off" or
#: «تطفي نفسها» is a real function; a definite "the fan ... turned off" is
#: caught by the existing-item rule below. "away" and "gone" are not here
#: either ("while I am away"); "taken away" and "the stand gone" are caught by
#: "taken" and by the existing-item rule.
_DISPOSAL_WORDS = frozenset({
    "removed", "taken", "replaced", "cancelled", "canceled",
    "thrown", "deleted", "discarded", "dismantled", "sold",
    "يتشال", "ينشال", "تنشال", "تتشال", "ينقل", "تنقل", "يتنقل", "ينرمى",
    "ينباع", "يتباع", "ينلغى", "يلغى", "تلغى", "يختفي", "تختفي", "ارميه", "ارميها", "ارميهم"})
#: English role nouns. After "the" / "my" / "our" / "your" (or an Arabic role
#: noun with ال-) they name an EXISTING item, which a want then changes; they
#: count only when "that" / "which" / "to" / "for" and a role or object word
#: follow ("I want the stand to hold my monitor").
_EN_ROLE_NOUNS = frozenset({
    "stand", "stands", "holder", "holders", "riser", "bracket", "fan", "fans",
    "waterer", "support", "mount"})
_EN_DEFINITE = frozenset({"the", "my", "our", "your"})
#: Arabic role NOUNS (never verbs: «يسقي النباتات» is a request).
_AR_ROLE_NOUNS = frozenset({
    "حامل", "حاملة", "مروحة", "مروحه", "مراوح", "بنكة", "بنكه", "پنكة", "پنكه",
    "قاعدة", "ستاند", "مسند"})
_RELATIVE_WORDS = frozenset({"that", "which", "to", "for", "اللي", "الذي", "التي"})
_AR_ARTICLE = ("وال", "بال", "فال", "كال", "ال")
_AR_OBJECT_PRONOUNS = ("ها", "هم", "ه")
#: A following sentence that only retracts the request.
_RETRACTION_WORDS = frozenset({
    "nope", "scratch", "kidding", "joking", "forget", "nevermind",
    "انس", "انسى", "انسي", "امزح", "اتغشمر"})

#: A want marked as past or as someone else's.
_PAST_WORDS = frozenset({"used", "was", "were", "كنت", "كان", "كانت", "كنا"})
_HYPOTHETICAL_WORDS = frozenset({
    "if", "whether", "maybe", "perhaps", "might", "wonder", "imagine", "suppose",
    "لو", "اذا", "ربما", "يمكن", "هل", "قد", "لعل", "عسى", "جان"})
_WITHOUT_WORDS = frozenset({"without", "بدون", "بلا", "دون", "غير"})
#: A clause ends at punctuation or at one of these contrastive words.
#: Words that mark an "I don't know" as being about how the function works.
_HOW_WORDS = frozenset({"how", "كيف", "شلون", "الطريقة", "طريقة"})
_CLAUSE_WORDS = frozenset({"but", "however", "لكن", "ولكن", "لكني", "لكنني", "بس"})
_SENTENCE_END = frozenset(".!?؟؛;\n")
_CLAUSE_END = _SENTENCE_END | frozenset(",،")
_WITHOUT_REACH = 3
_NEGATION_REACH = 2

_ALL_OBJECT_WORDS = tuple(surfaces for objects in _ROLE_OBJECTS.values()
                          for surfaces in objects.values())
#: "be" is deliberately absent: "the stand to be gone" names an existing item.
_ALL_ROLE_WORDS = tuple(_ROLE_TRIGGERS.values()) + _ALL_OBJECT_WORDS + (
    frozenset({"hold", "keep"}),)
_ALL_TRIGGER_WORDS = tuple(_ROLE_TRIGGERS.values())
_TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
_COMBINING_HAMZA = frozenset({"ٓ", "ٔ", "ٕ"})
_CONTRACTION_RE = re.compile(r"\b[^\W\d_]+n['’]t\b")


@dataclass(frozen=True)
class Quote:
    """An exact slice of one inventor statement: ``text[start:end] == quote``."""
    source_kind: str
    source_ref: str
    start: int
    end: int
    quote: str


@dataclass(frozen=True)
class RoleMention:
    role: str
    object_key: str
    polarity: str
    clause: Quote
    trigger: Quote
    method_uncertainty: "Quote | None"


@dataclass(frozen=True)
class ProposedRole:
    role: str
    object_key: str
    status: str
    interpretation_status: str
    groundings: tuple
    negations: tuple
    related_statements: tuple
    method_uncertainties: tuple


@dataclass(frozen=True)
class Handoff:
    grammar_version: str
    roles: tuple
    abstained: int
    mentions: tuple


def _normalize_with_offsets(text):
    """``text`` lowered and normalized exactly as ``normalize_ar`` does, one
    original character at a time, with the original index of every output
    character — so a match can always be mapped back to the exact source."""
    chars, index = [], []
    for i, ch in enumerate(text):
        if ch in _COMBINING_HAMZA and chars:
            composed = unicodedata.normalize("NFC", chars[-1] + ch)
            if len(composed) == 1:
                chars[-1] = normalize_ar(composed)
            continue
        low = ch.lower()
        if len(low) != 1:
            low = ch
        folded = normalize_ar(low)
        if not folded:
            continue
        for out in folded:
            chars.append(out)
            index.append(i)
    return "".join(chars), index


def _fold_contractions(normalized):
    """Every "...n't" ("don't", "didn't", "wouldn't", "isn't") becomes the word
    "not", padded to the same length so every offset stays valid."""
    return _CONTRACTION_RE.sub(lambda m: "not".ljust(len(m.group(0))), normalized)


def _match(token, surfaces):
    if token in surfaces:
        return True
    for proclitic in _AR_PROCLITICS:
        rest = token[len(proclitic):]
        if token.startswith(proclitic) and len(rest) >= 3 and rest in surfaces:
            return True
    return False


def _is(token, words):
    """``token`` is in ``words`` itself or after one و / ف (short particles)."""
    return token in words or (len(token) > 1 and token[0] in "وف"
                              and token[1:] in words)


def _is_negation(words, i):
    if not _is(words[i], _NEGATION_WORDS):
        return False
    # "بدون ما ألمسها" ("without me touching it"): ما after a "without" word
    # belongs to that construction.
    return not (words[i] in ("ما",) and i > 0 and _is(words[i - 1], _WITHOUT_WORDS))


def _intent_positions(words):
    found = []
    for i, w in enumerate(words):
        if _is(w, _AR_INTENT) or _is(w, _AR_FUSED_NEGATED_INTENT):
            found.append(i)
        elif w in _EN_INTENT_VERBS:
            # "I want", "I'd like", "I really need"; also "I do not want",
            # whose negation is judged separately.
            j = i - 1
            while j >= 0 and (words[j] in _EN_FILLERS or words[j] in _NEGATION_WORDS):
                j -= 1
            if j >= 0 and words[j] in _EN_SUBJECTS and (
                    w != "like" or "would" in words[j:i] or "d" in words[j:i]):
                found.append(i)
        elif w in _EN_OWN_IDEA[1] and i > 0 and words[i - 1] in _EN_OWN_IDEA[0]:
            found.append(i)
    return found


def _object_for(role, words, t):
    """``(key, index)`` of the object the role word at ``t`` governs, or None."""
    objects = _ROLE_OBJECTS[role]

    def key_of(word):
        return next((k for k, surfaces in objects.items() if _match(word, surfaces)),
                    None)
    if role in _OBJECT_OPTIONAL:
        for j in range(t + 1, len(words)):
            k = key_of(words[j])
            if k:
                return k, j
        return None
    j = t + 1
    while j < len(words) and words[j] in _CONNECTORS:
        j += 1
    if j + 1 < len(words) and words[j] in _EN_MODIFIERS and key_of(words[j + 1]):
        j += 1                                    # "my computer screen"
    if j < len(words) and key_of(words[j]):
        # "my monitor cable", "my TV room": the object only modifies a noun
        if j + 1 < len(words) and (words[j + 1] in _EN_OBJECT_MODIFIED or (
                words[j].isascii() and words[j + 1].isascii()
                and words[j + 1] not in _EN_OBJECT_FOLLOW)):
            return None
        return key_of(words[j]), j
    # compound: "monitor stand", "plant waterer"
    if t > 0 and key_of(words[t - 1]):
        return key_of(words[t - 1]), t - 1
    return None


def _is_trigger_verb(word):
    """A role trigger, optionally with one object pronoun («يرفعها»)."""
    forms = [word] + [word[:-len(p)] for p in _AR_OBJECT_PRONOUNS
                      if word.endswith(p) and len(word) - len(p) >= 3]
    return any(_match(f, s) for f in forms for s in _ALL_TRIGGER_WORDS)


def _existing_item(words, t):
    """The role word at ``t`` names an item the inventor already has ("the
    monitor stand", "my TV stand", "المروحة") rather than one to make —
    unless a relative clause gives it the role ("the stand that holds")."""
    w = words[t]
    definite = False
    if w in _EN_ROLE_NOUNS:
        j = t - 1
        while j >= 0 and any(_match(words[j], s) for s in _ALL_OBJECT_WORDS):
            j -= 1                                # "the monitor stand"
        definite = j >= 0 and words[j] in _EN_DEFINITE
    elif not w.isascii():
        definite = any(w.startswith(a) and len(w) - len(a) >= 3 for a in _AR_ARTICLE)
        nxt = words[t + 1] if t + 1 < len(words) else ""
        if not definite and _match(w, _AR_ROLE_NOUNS) and nxt.startswith("ال") and any(
                _match(nxt, s) for s in _ALL_OBJECT_WORDS):
            # construct form «حامل الشاشة», «مروحة الغرفة»: the item exists
            # unless a role verb follows the object, directly or right after
            # اللي / الذي / التي («اللي في الصالة يروح» only locates it)
            after = words[t + 2:t + 4]
            if after and after[0] in _RELATIVE_WORDS:
                after = after[1:]
            return not (after and _is_trigger_verb(after[0]))
    if not definite:
        return False
    after = words[t + 1:t + 3]
    return not (after and after[0] in _RELATIVE_WORDS and len(after) > 1 and any(
        _match(after[1], s) for s in _ALL_ROLE_WORDS))


def _cut_spans(normalized, tokens, ends, words):
    cuts = {0, len(normalized)}
    for i, ch in enumerate(normalized):
        if ch in ends:
            cuts.add(i + 1)
    for start, _end, token in tokens:
        if token in words:
            cuts.add(start)
    ordered = sorted(cuts)
    return [(a, b) for a, b in zip(ordered, ordered[1:]) if a < b]


def _unknown_spans(normalized):
    spans = []
    for marker in tuple(_ACKNOWLEDGED_UNKNOWN_MARKERS) + tuple(
            s for s, _m in ACKNOWLEDGED_UNKNOWN_SURFACES):
        needle = normalize_ar(marker.lower())
        start = normalized.find(needle)
        while start != -1:
            spans.append((start, start + len(needle)))
            start = normalized.find(needle, start + 1)
    return spans


def _quote(text, index, kind, ref, n_start, n_end):
    """Map a normalized span back to the original text, trimmed of outer
    whitespace and keeping any harakat or tatweel that belong to its last
    letter."""
    if n_start >= n_end:
        return None
    start = index[n_start]
    end = index[n_end - 1] + 1
    while end < len(text) and not text[end].isspace() and not text[end].isalnum() \
            and unicodedata.category(text[end]) in ("Mn", "Lm"):
        end += 1
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return Quote(kind, ref, start, end, text[start:end])


def _polarity(ctx, t, obj):
    """The polarity of the role word at clause position ``t`` (object at
    clause position ``obj`` or None). ``ctx`` holds the clause and sentence
    words and flags (see ``_statement_mentions``)."""
    words, free = ctx["words"], ctx["free"]
    anchors = {t} | ({obj} if obj is not None else set())
    intent = [i for i in _intent_positions(words) if i < t]
    fused = [i for i in intent if _is(words[i], _AR_FUSED_NEGATED_INTENT)]
    if fused:
        return NEGATED
    negations = [i for i in range(len(words)) if i in free and _is_negation(words, i)]
    targets = set(intent) | anchors
    if any(n < k <= n + _NEGATION_REACH for n in negations for k in targets):
        return NEGATED
    if negations or ctx["sentence_negated"] or ctx["next_sentence_negated"]:
        return ABSTAINED
    if ctx["question"] or ctx["unknown_before"](t) or ctx["reversing"]:
        return ABSTAINED
    first = intent[0] if intent else t
    if any(_is(w, _HYPOTHETICAL_WORDS) or w in _PAST_WORDS for w in words[:first]):
        return ABSTAINED
    for i, w in enumerate(words):
        if _is(w, _WITHOUT_WORDS) and any(i < k <= i + _WITHOUT_REACH for k in anchors):
            return NEGATED
    if not intent:
        return ABSTAINED
    if any(_match(w, _DISPOSAL_WORDS) for w in words):
        return ABSTAINED
    if ctx["existing_item"](t):
        return ABSTAINED
    # A closed positive path from the nearest want to the role word: only
    # listed function words, device nouns, adjectives, other wants and the
    # role's own object words (compounds) may stand between them.
    path_ok = ctx["path_words"]
    if all(_match(w, path_ok) for w in words[intent[-1] + 1:t]):
        return AFFIRMED
    return ABSTAINED


def _statement_mentions(kind, ref, text):
    if not isinstance(text, str) or not text.strip():
        return []
    normalized, index = _normalize_with_offsets(text)
    unknown = _unknown_spans(normalized)
    folded = _fold_contractions(normalized)
    tokens = [(m.start(), m.end(), m.group()) for m in _TOKEN_RE.finditer(folded)]
    starts = [t[0] for t in tokens]
    all_words = [t[2] for t in tokens]

    def in_unknown(pos):
        # a token overlapping an unknown marker ("ولست متأكدا") belongs to it
        tok = tokens[bisect_right(starts, pos) - 1] if tokens else (pos, pos + 1)
        return any(tok[0] < u1 and u0 < tok[1] for u0, u1 in unknown)

    def token_range(a, b):
        return bisect_left(starts, a), bisect_left(starts, b)

    sentences = _cut_spans(folded, tokens, _SENTENCE_END, frozenset())
    sentence_info = []
    for s_start, s_end in sentences:
        lo, hi = token_range(s_start, s_end)
        negated = any(_is_negation(all_words, i) and not in_unknown(starts[i])
                      for i in range(lo, hi))
        first_negated = hi > lo and _is_negation(all_words, lo) \
            and not in_unknown(starts[lo])
        sentence_info.append({
            "range": (lo, hi), "negated": negated, "starts_negated": first_negated,
            # "Nope." / "Just kidding." / "انسَ الموضوع."
            "starts_retraction": any(_match(all_words[i], _RETRACTION_WORDS)
                                     for i in range(lo, min(hi, lo + 2))),
            "reversing": any(_is(all_words[i], _REVERSING_WORDS) for i in range(lo, hi)),
            "question": folded[s_start:s_end].rstrip()[-1:] in ("?", "؟")})
    sentence_starts = [a for a, _b in sentences]
    mentions = []
    for c_start, c_end in _cut_spans(folded, tokens, _CLAUSE_END, _CLAUSE_WORDS):
        lo, hi = token_range(c_start, c_end)
        if lo >= hi:
            continue
        clause_tokens = tokens[lo:hi]
        words = all_words[lo:hi]
        s_index = bisect_right(sentence_starts, c_start) - 1
        info = sentence_info[s_index]
        nxt = sentence_info[s_index + 1] if s_index + 1 < len(sentence_info) else None
        s_lo, s_hi = info["range"]
        clause_negations = sum(1 for i in range(lo, hi) if _is_negation(all_words, i)
                               and not in_unknown(starts[i]))
        sentence_negations = sum(1 for i in range(s_lo, s_hi)
                                 if _is_negation(all_words, i) and not in_unknown(starts[i]))
        s_end_pos = sentences[s_index][1]
        ctx = {
            "words": words,
            "free": {i for i, tok in enumerate(clause_tokens) if not in_unknown(tok[0])},
            "sentence_negated": sentence_negations > clause_negations,
            # "... my plants. Not really." / "No, I mean the garden."
            "next_sentence_negated": bool(nxt and (
                nxt["starts_negated"] or nxt["starts_retraction"])),
            "question": info["question"],
            "reversing": info["reversing"],
            "existing_item": lambda t, w=words: _existing_item(w, t),
            # "I am not sure about a device that...": doubt about the want
            "unknown_before": lambda t, c=clause_tokens: any(
                c_start <= u0 < c[t][0] for u0, _u1 in unknown),
        }
        s_start_pos = sentences[s_index][0]

        def uncertainty_for(t, c=clause_tokens, a=s_start_pos, e=s_end_pos,
                            cs=c_start):
            """The inventor's "I don't know" about HOW: after the want in the
            same sentence, or in an earlier clause when it is about how."""
            for u0, u1 in unknown:
                if c[t][1] <= u0 < e:
                    return u0, u1
                if a <= u0 < cs and _HOW_WORDS & set(folded[u1:u1 + 12].split()):
                    return u0, u1
            return None
        for role in ROLES:
            for t, w in enumerate(words):
                if not _match(w, _ROLE_TRIGGERS[role]):
                    continue
                if w in _EN_WATER_NOUN_VERBS and role == ROLE_WATERING and not (
                        t > 0 and words[t - 1] in _EN_WATER_VERB_BEFORE):
                    continue
                if role == ROLE_FAN and w in ("fan", "fans") and not (
                        any(x in _EN_FAN_CONTEXT for x in words)
                        or any(_is_negation(words, i) for i in range(max(0, t - 3), t))):
                    continue
                if role == ROLE_FAN and w in ("fan", "fans") and t > 0 \
                        and words[t - 1] == "to":
                    continue                      # "to fan the flames"
                found = _object_for(role, words, t)
                key, obj = found if found else (OBJECT_NONE, None)
                # the role's own words may stand on the path too: "a stand
                # that holds", "حاملًا يرفع" (with the accusative ـًا)
                own = _ROLE_TRIGGERS[role] | frozenset(
                    x + "ا" for x in _ROLE_TRIGGERS[role] if not x.isascii())
                ctx["path_words"] = _PATH_BASE | own | frozenset().union(
                    *_ROLE_OBJECTS[role].values())
                polarity = _polarity(ctx, t, obj)
                if key == OBJECT_NONE and role not in _OBJECT_OPTIONAL \
                        and polarity == AFFIRMED:
                    continue
                tok = clause_tokens[t]
                span = uncertainty_for(t) if polarity == AFFIRMED else None
                mentions.append(RoleMention(
                    role=role, object_key=key, polarity=polarity,
                    clause=_quote(text, index, kind, ref, c_start, c_end),
                    trigger=_quote(text, index, kind, ref, tok[0], tok[1]),
                    method_uncertainty=(_quote(text, index, kind, ref, *span)
                                        if span else None)))
                break
    return mentions


def project_functional_roles(statements):
    """Project the inventor's statements onto the three closed roles.

    ``statements``: iterable of ``(source_kind, source_ref, text)`` — the
    original idea text and the inventor's active answers, verbatim. Returns a
    ``Handoff``: one ``ProposedRole`` per (role, object) with at least one
    AFFIRMED mention. It is ``CONFLICTING`` when the SAME role and object are
    also NEGATED somewhere. Other wording about the same role that was not read
    as a request (a rejection of the whole role, an unclear statement about the
    same object) is disclosed beside the proposal (``related_statements``)
    without being called a conflict. Statements about different objects never conflict. Never
    raises on bad input."""
    mentions = []
    try:
        items = list(statements or ())
    except TypeError:
        items = []
    for item in items:
        try:
            kind, ref, text = item
        except (TypeError, ValueError):
            continue
        mentions.extend(_statement_mentions(kind, ref, text))
    roles = []
    for role in ROLES:
        keys = []
        for m in mentions:
            if m.role == role and m.polarity == AFFIRMED and m.object_key not in keys:
                keys.append(m.object_key)
        for key in keys:
            same = [m for m in mentions if m.role == role and m.object_key == key]
            negated = tuple(m.clause for m in same if m.polarity == NEGATED)
            affirmed = {m.clause for m in same if m.polarity == AFFIRMED}
            # Other wording about this role that was not read as a request — a
            # rejection of the whole role, or an unclear statement about the
            # same object — is shown beside the proposal, never as a conflict.
            related = []
            for m in mentions:
                if m.role != role or m.polarity == AFFIRMED or m.clause in affirmed:
                    continue
                if m.polarity == NEGATED and m.object_key == key:
                    continue                      # already a conflict
                if m.object_key in (OBJECT_NONE, key) and m.clause not in related:
                    related.append(m.clause)
            roles.append(ProposedRole(
                role=role, object_key=key,
                status=CONFLICTING if negated else PROPOSED,
                interpretation_status=INTERPRETATION_STATUS,
                groundings=tuple(m.clause for m in same if m.polarity == AFFIRMED),
                negations=negated,
                related_statements=tuple(related),
                method_uncertainties=tuple(m.method_uncertainty for m in same
                                           if m.polarity == AFFIRMED
                                           and m.method_uncertainty)))
    return Handoff(
        grammar_version=GRAMMAR_VERSION, roles=tuple(roles),
        abstained=sum(1 for m in mentions if m.polarity == ABSTAINED),
        mentions=tuple(mentions))
