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

Semantic rule (Lead correction): a role is PROPOSED only on positive evidence —
a role word, its object and an intent word in the same clause, with no
negation, hypothetical, question or "without" governing it. A recognised negation of the
intent or the role reads NEGATED; any other negation, a hypothetical or a
missing intent word ABSTAINS. An unlisted negation is therefore not "caught":
it fails only because the clause then lacks support, and wording this table
does not register is not read at all.

Pure: no I/O, no clock, no state, no persistence, no model or provider call.
"""
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
        "يسجي", "تسجي", "اسجي"}),
    ROLE_FAN: frozenset({
        "fan", "fans", "مروحة", "مروحه", "مراوح", "بنكة", "بنكه", "پنكة", "پنكه"}),
    ROLE_SCREEN_SUPPORT: frozenset({
        "stand", "stands", "holder", "holders", "support", "supports", "hold",
        "holds", "raise", "raises", "riser", "mount", "mounts", "bracket",
        "حامل", "حاملة", "يحمل", "تحمل", "يرفع", "ترفع", "رفع", "قاعدة",
        "ستاند", "يثبت", "تثبيت", "يسند", "مسند", "يشيل", "تشيل"}),
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
_OBJECT_OPTIONAL = frozenset({ROLE_FAN})
#: English "fan" also means admirer; it is read only with an air / switching
#: word in the same clause (Arabic "مروحة" is unambiguous).
_EN_FAN_CONTEXT = frozenset({
    "air", "cool", "cools", "cooling", "blow", "blows", "blowing", "spin",
    "spins", "temperature", "hot", "heat", "automatic", "automatically",
    "switch", "switches", "turns", "ceiling", "room", "bedroom", "laptop",
    "computer"})

#: English words that are also ordinary nouns ("a glass of water"): read as
#: the role only when an object word of that role follows within three words
#: ("water my plants").
_EN_NOUN_VERBS = {ROLE_WATERING: frozenset({"water", "waters"})}
_NOUN_VERB_REACH = 3

_INTENT_WORDS = frozenset({
    "want", "wants", "need", "needs", "idea", "invention", "device", "system",
    "machine", "gadget", "build", "building", "make", "making", "design",
    "designing", "create", "creating", "plan",
    "اريد", "نريد", "يريد", "ارغب", "نرغب", "احتاج", "نحتاج", "فكرتي", "فكرة",
    "اختراع", "اختراعي", "جهاز", "جهازا", "نظام", "نظاما", "الة", "اصمم",
    "اصنع", "نصنع", "ابي", "ابغى", "ابغي", "ودي", "بدي", "ابا"})
_NEGATION_WORDS = frozenset({
    "not", "no", "never", "dont", "doesnt", "wont", "cannot", "cant",
    "لا", "لن", "لم", "ليس", "ليست", "لست", "ما", "مش", "مو", "مب", "موب"})
_HYPOTHETICAL_WORDS = frozenset({
    "if", "whether", "maybe", "perhaps", "might", "wonder", "imagine", "suppose",
    "لو", "اذا", "ربما", "يمكن", "هل", "قد", "لعل", "عسى", "جان"})
_WITHOUT_WORDS = frozenset({"without", "بدون", "بلا", "دون"})
#: A clause ends at punctuation or at one of these contrastive words.
_CLAUSE_WORDS = frozenset({"but", "however", "لكن", "ولكن", "لكني", "لكنني", "بس"})
_SENTENCE_END = frozenset(".!?؟؛;\n")
_CLAUSE_END = _SENTENCE_END | frozenset(",،")
_WITHOUT_REACH = 3
_NEGATION_REACH = 2

_TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
_COMBINING_HAMZA = frozenset({"ٓ", "ٔ", "ٕ"})


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


def _object_follows(words, i, role):
    return any(_match(w, surfaces)
               for surfaces in _ROLE_OBJECTS[role].values()
               for w in words[i + 1:i + 1 + _NOUN_VERB_REACH])


def _match(token, surfaces):
    if token in surfaces:
        return True
    for proclitic in _AR_PROCLITICS:
        rest = token[len(proclitic):]
        if token.startswith(proclitic) and len(rest) >= 3 and rest in surfaces:
            return True
    return False


def _boundaries(normalized, ends):
    cuts = [0]
    for i, ch in enumerate(normalized):
        if ch in ends:
            cuts.append(i + 1)
    cuts.append(len(normalized))
    return cuts


def _spans(normalized, tokens, ends, words):
    """``(start, end)`` normalized spans cut at ``ends`` characters and before
    any token in ``words``."""
    cuts = set(_boundaries(normalized, ends))
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


def _polarity(tokens, t_index, o_index, negation_free_tokens, question):
    """The polarity of one role mention inside its clause (token lists).
    ``question``: the clause's sentence ends with a question mark."""
    words = [t for _s, _e, t in tokens]
    anchors = {t_index} | ({o_index} if o_index is not None else set())
    intent = [i for i, w in enumerate(words) if w in _INTENT_WORDS]
    # "بدون ما ألمسها" ("without me touching it"): a negation particle right
    # after a "without" word belongs to that construction, not to the want.
    negations = [i for i, w in enumerate(words)
                 if w in _NEGATION_WORDS and i in negation_free_tokens
                 and not (i > 0 and words[i - 1] in _WITHOUT_WORDS)]
    targets = set(intent) | anchors
    for n in negations:
        if any(n < k <= n + _NEGATION_REACH for k in targets):
            return NEGATED
    if negations or question:
        return ABSTAINED
    # A hypothetical before the want governs it ("لو كان فيه جهاز يسقي...");
    # after the want it states when the function acts ("a fan that turns on if
    # the room gets hot", "...إذا صار الجو حار").
    first_intent = intent[0] if intent else len(words)
    if any(w in _HYPOTHETICAL_WORDS for w in words[:first_intent]):
        return ABSTAINED
    for i, w in enumerate(words):
        if w in _WITHOUT_WORDS and any(i < k <= i + _WITHOUT_REACH for k in anchors):
            return NEGATED
    return AFFIRMED if intent else ABSTAINED


_CONTRACTION_RE = re.compile(r"\b(does|do|won|can)n?['\u2019]t\b")
_CONTRACTIONS = {"do": "dont", "does": "doesnt", "won": "wont", "can": "cant"}


def _english_contractions(normalized):
    """Fold "don't" / "doesn't" / "won't" / "can't" into one negation token so
    the negation reach is measured in words. Same length, so every offset in
    the normalized text stays valid."""
    def fold(m):
        word = _CONTRACTIONS[m.group(1)]
        return word + " " * (len(m.group(0)) - len(word))
    return _CONTRACTION_RE.sub(fold, normalized)


def _statement_mentions(kind, ref, text):
    if not isinstance(text, str) or not text.strip():
        return []
    normalized, index = _normalize_with_offsets(text)
    unknown = _unknown_spans(normalized)
    folded = _english_contractions(normalized)
    assert len(folded) == len(normalized)
    tokens = [(m.start(), m.end(), m.group()) for m in _TOKEN_RE.finditer(folded)]
    mentions = []
    sentences = _spans(folded, tokens, _SENTENCE_END, frozenset())
    for c_start, c_end in _spans(folded, tokens, _CLAUSE_END, _CLAUSE_WORDS):
        clause_tokens = [t for t in tokens if c_start <= t[0] and t[1] <= c_end]
        words = [t[2] for t in clause_tokens]
        free = {i for i, t in enumerate(clause_tokens)
                if not any(u0 <= t[0] < u1 for u0, u1 in unknown)}
        sentence = next(((a, b) for a, b in sentences if a <= c_start < b),
                        (c_start, c_end))
        uncertainty = next(((u0, u1) for u0, u1 in unknown
                            if sentence[0] <= u0 < sentence[1]), None)
        question = folded[sentence[0]:sentence[1]].rstrip()[-1:] in ("?", "؟")
        for role in ROLES:
            triggers = [i for i, w in enumerate(words)
                        if _match(w, _ROLE_TRIGGERS[role])
                        and not (w in _EN_NOUN_VERBS.get(role, ())
                                 and not _object_follows(words, i, role))]
            if not triggers:
                continue
            if role == ROLE_FAN and any(w in ("fan", "fans") for w in words) \
                    and not any(w in _EN_FAN_CONTEXT for w in words) \
                    and not any(_match(w, _ROLE_TRIGGERS[role] - {"fan", "fans"})
                                for w in words):
                continue
            objects = [(key, i) for key, surfaces in _ROLE_OBJECTS[role].items()
                       for i, w in enumerate(words) if _match(w, surfaces)]
            if not objects:
                if role not in _OBJECT_OPTIONAL:
                    continue
                objects = [(OBJECT_NONE, None)]
            seen = set()
            for key, o_index in objects:
                if key in seen:
                    continue
                seen.add(key)
                t_index = triggers[0]
                tok = clause_tokens[t_index]
                mentions.append(RoleMention(
                    role=role, object_key=key,
                    polarity=_polarity(clause_tokens, t_index, o_index, free,
                                       question),
                    clause=_quote(text, index, kind, ref, c_start, c_end),
                    trigger=_quote(text, index, kind, ref, tok[0], tok[1]),
                    method_uncertainty=(
                        _quote(text, index, kind, ref, *uncertainty)
                        if uncertainty else None)))
    return mentions


def project_functional_roles(statements):
    """Project the inventor's statements onto the three closed roles.

    ``statements``: iterable of ``(source_kind, source_ref, text)`` — the
    original idea text and the inventor's active answers, verbatim. Returns a
    ``Handoff``: one ``ProposedRole`` per (role, object) with at least one
    AFFIRMED mention — ``CONFLICTING`` when the SAME role and object are also
    NEGATED somewhere — and the count of mentions it abstained on. Statements
    about different objects never conflict. Never raises on bad input."""
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
            affirmed = tuple(m.clause for m in same if m.polarity == AFFIRMED)
            negated = tuple(m.clause for m in same if m.polarity == NEGATED)
            unknown = tuple(m.method_uncertainty for m in same
                            if m.polarity == AFFIRMED and m.method_uncertainty)
            roles.append(ProposedRole(
                role=role, object_key=key,
                status=CONFLICTING if negated else PROPOSED,
                interpretation_status=INTERPRETATION_STATUS,
                groundings=affirmed, negations=negated,
                method_uncertainties=unknown))
    return Handoff(
        grammar_version=GRAMMAR_VERSION, roles=tuple(roles),
        abstained=sum(1 for m in mentions if m.polarity == ABSTAINED),
        mentions=tuple(mentions))
