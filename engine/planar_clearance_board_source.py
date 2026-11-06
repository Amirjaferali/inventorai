"""BOARD-OUTLINE-SOURCE-BINDING-01 - the board-outline source reader (inbound adapter).

ONE pure, hardened reader of ONE KiCad 10.0.8 board file (board-file format
``20260206``) that the inventor chose to have inspected. It returns the ONE
rectangle written in the file's ``Edge.Cuts`` layer as exact decimals, or ONE
closed refusal code. It is the inbound counterpart of the outbound CAD adapter
(``engine/planar_clearance_cad_export.py``) and owns nothing else: the offer, the
inventor's declaration and its lifecycle stay with the Stage-15 owner
(``engine/subsystem_model.py``); the comparison stays with the Mechanical method.

Admitted (and only this): exactly one ``gr_rect``, or exactly four ``gr_line``
forming one closed axis-aligned rectangle (F1 of the #933 proof), at the board's
top level on ``Edge.Cuts``, each with exactly the observed KiCad 10.0.8 fields.
Everything else on ``Edge.Cuts`` - anywhere, footprints included - is refused, and
nothing is approximated, rounded, rotated or inferred.

Hardening: the size is capped; SHA-256 is taken over the raw bytes before any
decoding; the text must be strict UTF-8 without NUL or other control characters;
the hand-written tokenizer consumes the whole input, terminates every string and
escape, balances every parenthesis and bounds the depth, token count and atom
length; there is exactly one ``kicad_pcb`` root and exactly one ``version`` field;
numbers are plain finite decimals (no sign other than a leading minus, no
exponent) of bounded magnitude and precision. Refusals carry a closed code only
and never echo file content.

Synthetic-qualified scope: the evidence is ``docs/benchmarks/evidence/
kicad10_format_qualification_v1`` (PR #936). No KiCad 7 or other version, no
KiCad executable, no network, no clock, no randomness, no store.
"""
import hashlib
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

# --- identities stored with every file-linked declaration (bump on any change) --------------
ACCEPTED_FORMAT_VERSION = "20260206"
FORMAT_ID = "kicad-board/" + ACCEPTED_FORMAT_VERSION
READER_ID = "kicad-board-outline-reader/1"
RULE_ID = "edge-cuts-one-rectangle/1"
SOURCE_KIND = "kicad_pcb"
TOOL_VERSION = "10.0.8"

# --- bounds (resource limits, not physical ratings) ----------------------------------------
MAX_FILE_BYTES = 128 * 1024 - 4 * 1024   # the request cap stays 128 KiB; multipart overhead
MAX_DEPTH = 32
MAX_TOKENS = 40000
MAX_ATOM_CHARS = 2048
MAX_EDGE_SHAPES = 8
COORD_INTEGER_DIGITS = 6
COORD_FRACTION_DIGITS = 6
# the declared value representation of the Mechanical method (6 integer, 4 fraction digits)
DIM_INTEGER_DIGITS = 6
DIM_FRACTION_DIGITS = 4

# --- closed refusal codes ----------------------------------------------------------------
TOO_LARGE = "TOO_LARGE"
EMPTY = "EMPTY"
NOT_UTF8 = "NOT_UTF8"
CONTROL_CHARACTER = "CONTROL_CHARACTER"
MALFORMED = "MALFORMED"
TOO_DEEP = "TOO_DEEP"
TOO_MANY_TOKENS = "TOO_MANY_TOKENS"
ATOM_TOO_LONG = "ATOM_TOO_LONG"
NOT_KICAD_BOARD = "NOT_KICAD_BOARD"
VERSION_MISSING = "VERSION_MISSING"
VERSION_NOT_ACCEPTED = "VERSION_NOT_ACCEPTED"
FIELD_NOT_ALLOWED = "FIELD_NOT_ALLOWED"
FIELD_MALFORMED = "FIELD_MALFORMED"
NUMBER_NOT_PLAIN = "NUMBER_NOT_PLAIN"
OUTLINE_MISSING = "OUTLINE_MISSING"
TOO_MANY_OUTLINE_SHAPES = "TOO_MANY_OUTLINE_SHAPES"
UNSUPPORTED_OUTLINE = "UNSUPPORTED_OUTLINE"
NOT_ONE_RECTANGLE = "NOT_ONE_RECTANGLE"
DIMENSION_NOT_REPRESENTABLE = "DIMENSION_NOT_REPRESENTABLE"
REFUSAL_CODES = (TOO_LARGE, EMPTY, NOT_UTF8, CONTROL_CHARACTER, MALFORMED, TOO_DEEP,
                 TOO_MANY_TOKENS, ATOM_TOO_LONG, NOT_KICAD_BOARD, VERSION_MISSING,
                 VERSION_NOT_ACCEPTED, FIELD_NOT_ALLOWED, FIELD_MALFORMED, NUMBER_NOT_PLAIN,
                 OUTLINE_MISSING, TOO_MANY_OUTLINE_SHAPES, UNSUPPORTED_OUTLINE,
                 NOT_ONE_RECTANGLE, DIMENSION_NOT_REPRESENTABLE)

EDGE_LAYER = "Edge.Cuts"
# The closed, version-specific field shapes observed in KiCad 10.0.8 output. Each field
# maps to (min, max) occurrences; its arity and types are checked by ``_check_field``.
_SHAPE_FIELDS = {
    ACCEPTED_FORMAT_VERSION: {
        "gr_rect": {"start": (1, 1), "end": (1, 1), "stroke": (1, 1), "fill": (1, 1),
                    "layer": (1, 1), "uuid": (0, 1), "tstamp": (0, 1), "locked": (0, 1)},
        "gr_line": {"start": (1, 1), "end": (1, 1), "stroke": (1, 1),
                    "layer": (1, 1), "uuid": (0, 1), "tstamp": (0, 1), "locked": (0, 1)},
    },
}
_STROKE_TYPES = frozenset({"default", "solid"})
_COORD = re.compile(r"-?(0|[1-9][0-9]{0,%d})(\.[0-9]{1,%d})?\Z"
                    % (COORD_INTEGER_DIGITS - 1, COORD_FRACTION_DIGITS), re.ASCII)
_WIDTH = re.compile(r"(0|[1-9][0-9]{0,%d})(\.[0-9]{1,%d})?\Z"
                    % (COORD_INTEGER_DIGITS - 1, COORD_FRACTION_DIGITS), re.ASCII)
_ESCAPES = {'"': '"', "\\": "\\", "n": "\n", "t": "\t", "r": "\r"}
_DELIMS = frozenset('()"')


class Refused(Exception):
    """The file is not one admitted rectangle. ``code`` is one of ``REFUSAL_CODES``;
    the message never contains file content."""

    def __init__(self, code):
        if code not in REFUSAL_CODES:
            code = MALFORMED
        super().__init__(code)
        self.code = code


class _Str(str):
    """A quoted string token (distinct from a bare atom)."""


@dataclass(frozen=True)
class BoardOutline:
    """What one inspection found: the raw-byte identity of the file and the exact
    outline dimensions along the FILE's own x and y axes (canonical decimal text)."""
    source_sha256: str
    source_size: int
    format_id: str
    reader_id: str
    rule_id: str
    file_x: str
    file_y: str


def _tokens(text):
    """Strict tokenizer: ``(``, ``)``, quoted strings with closed escapes, bare atoms.
    Whitespace is space, tab, CR or LF only. Every byte is consumed."""
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if ch in " \t\r\n":
            i += 1
            continue
        if len(out) >= MAX_TOKENS:
            raise Refused(TOO_MANY_TOKENS)
        if ch == "(" or ch == ")":
            out.append(ch)
            i += 1
        elif ch == '"':
            i += 1
            buf = []
            while True:
                if i >= n:
                    raise Refused(MALFORMED)          # unterminated string
                c = text[i]
                if c == '"':
                    i += 1
                    break
                if c == "\\":
                    if i + 1 >= n or text[i + 1] not in _ESCAPES:
                        raise Refused(MALFORMED)      # unknown or unterminated escape
                    buf.append(_ESCAPES[text[i + 1]])
                    i += 2
                else:
                    buf.append(c)
                    i += 1
                if len(buf) > MAX_ATOM_CHARS:
                    raise Refused(ATOM_TOO_LONG)
            out.append(_Str("".join(buf)))
        else:
            j = i
            while j < n and text[j] not in _DELIMS and text[j] not in " \t\r\n":
                j += 1
                if j - i > MAX_ATOM_CHARS:
                    raise Refused(ATOM_TOO_LONG)
            out.append(text[i:j])
            i = j
    return out


def _tree(tokens):
    """ONE root list consuming every token, depth at most ``MAX_DEPTH``."""
    if not tokens or tokens[0] != "(":
        raise Refused(NOT_KICAD_BOARD)
    stack, root = [], None
    for k, tok in enumerate(tokens):
        if tok == "(":
            if root is not None and not stack:
                raise Refused(MALFORMED)              # a second top-level value
            if len(stack) >= MAX_DEPTH:
                raise Refused(TOO_DEEP)
            node = []
            if stack:
                stack[-1].append(node)
            else:
                root = node
            stack.append(node)
        elif tok == ")":
            if not stack:
                raise Refused(MALFORMED)
            stack.pop()
        else:
            if not stack:
                raise Refused(MALFORMED)              # an atom outside the root
            stack[-1].append(tok)
    if stack:
        raise Refused(MALFORMED)                      # unbalanced parentheses
    return root


def _decode(data):
    if not isinstance(data, (bytes, bytearray)):
        raise Refused(MALFORMED)
    if len(data) == 0:
        raise Refused(EMPTY)
    if len(data) > MAX_FILE_BYTES:
        raise Refused(TOO_LARGE)
    if b"\x00" in data:
        raise Refused(CONTROL_CHARACTER)
    try:
        text = bytes(data).decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise Refused(NOT_UTF8)
    for ch in text:
        o = ord(ch)
        if (o < 0x20 and ch not in "\t\r\n") or 0x7F <= o <= 0x9F or o == 0xFEFF:
            raise Refused(CONTROL_CHARACTER)
    return text


def _head(node):
    return node[0] if node and isinstance(node[0], str) and not isinstance(node[0], _Str) else None


def _names_edge(node):
    """True when this list is a ``layer`` / ``layers`` field naming Edge.Cuts."""
    return (_head(node) in ("layer", "layers")
            and any(isinstance(a, str) and a == EDGE_LAYER for a in node[1:]))


def _plain(text, pattern):
    if isinstance(text, _Str) or not isinstance(text, str) or not pattern.match(text):
        raise Refused(NUMBER_NOT_PLAIN)
    try:
        value = Decimal(text)
    except InvalidOperation:
        raise Refused(NUMBER_NOT_PLAIN)
    if not value.is_finite():
        raise Refused(NUMBER_NOT_PLAIN)
    return value


def _check_field(name, field):
    """Exact arity, types and nesting of one allowed field; returns a point for
    ``start`` / ``end``."""
    args = field[1:]
    if name in ("start", "end"):
        if len(args) != 2:
            raise Refused(FIELD_MALFORMED)
        return (_plain(args[0], _COORD), _plain(args[1], _COORD))
    if name == "layer":
        if len(args) != 1 or not isinstance(args[0], _Str) or args[0] != EDGE_LAYER:
            raise Refused(FIELD_MALFORMED)
        return None
    if name == "stroke":
        if len(args) != 2 or not all(isinstance(a, list) for a in args):
            raise Refused(FIELD_MALFORMED)
        heads = sorted(_head(a) or "" for a in args)
        if heads != ["type", "width"]:
            raise Refused(FIELD_MALFORMED)
        for sub in args:
            if len(sub) != 2 or isinstance(sub[1], list):
                raise Refused(FIELD_MALFORMED)
            if _head(sub) == "width":
                _plain(sub[1], _WIDTH)
            elif isinstance(sub[1], _Str) or sub[1] not in _STROKE_TYPES:
                raise Refused(FIELD_MALFORMED)
        return None
    if name == "fill":
        if len(args) != 1 or isinstance(args[0], (list, _Str)) or args[0] != "no":
            raise Refused(FIELD_MALFORMED)
        return None
    if name in ("uuid", "tstamp"):
        if len(args) != 1 or not isinstance(args[0], str) or isinstance(args[0], list) \
                or len(args[0]) > 64:
            raise Refused(FIELD_MALFORMED)
        return None
    if name == "locked":
        if len(args) != 1 or isinstance(args[0], (list, _Str)) or args[0] not in ("yes", "no"):
            raise Refused(FIELD_MALFORMED)
        return None
    raise Refused(FIELD_NOT_ALLOWED)


def _shape(node, allowed):
    """The ``start`` and ``end`` points of one admitted shape, every field checked."""
    fields = allowed.get(_head(node))
    if fields is None:
        raise Refused(UNSUPPORTED_OUTLINE)
    counts, points = {}, {}
    for child in node[1:]:
        name = _head(child) if isinstance(child, list) else None
        if name is None or name not in fields:
            raise Refused(FIELD_NOT_ALLOWED)
        counts[name] = counts.get(name, 0) + 1
        point = _check_field(name, child)
        if point is not None:
            points[name] = point
    for name, (low, high) in fields.items():
        if not low <= counts.get(name, 0) <= high:
            raise Refused(FIELD_MALFORMED)          # missing, duplicated or conflicting
    return points["start"], points["end"]


def _f1_rectangle(segments):
    """F1 (#933): exactly four distinct proper sides forming ONE closed rectangle -
    two horizontal sides at different heights spanning exactly the full width and two
    vertical sides at different positions spanning exactly the full height."""
    horizontal, vertical = [], []
    for (ax, ay), (bx, by) in segments:
        if ax == bx and ay == by:
            raise Refused(NOT_ONE_RECTANGLE)
        if ay == by:
            horizontal.append((min(ax, bx), max(ax, bx), ay))
        elif ax == bx:
            vertical.append((min(ay, by), max(ay, by), ax))
        else:
            raise Refused(NOT_ONE_RECTANGLE)
    if len(horizontal) != 2 or len(vertical) != 2:
        raise Refused(NOT_ONE_RECTANGLE)
    bottom, top = sorted(horizontal, key=lambda h: h[2])
    left, right = sorted(vertical, key=lambda v: v[2])
    x0, x1, y0, y1 = left[2], right[2], bottom[2], top[2]
    if x0 == x1 or y0 == y1:
        raise Refused(NOT_ONE_RECTANGLE)
    for lo, hi, _at in (bottom, top):
        if (lo, hi) != (x0, x1):
            raise Refused(NOT_ONE_RECTANGLE)
    for lo, hi, _at in (left, right):
        if (lo, hi) != (y0, y1):
            raise Refused(NOT_ONE_RECTANGLE)
    return x1 - x0, y1 - y0


def _canonical(value):
    """Exact canonical decimal text of a positive dimension, or a refusal: never
    rounded. It must fit the Mechanical method's declared representation."""
    if value <= 0:
        raise Refused(NOT_ONE_RECTANGLE)
    text = format(value.normalize(), "f")
    whole, _, frac = text.partition(".")
    if len(frac) > DIM_FRACTION_DIGITS or len(whole) > DIM_INTEGER_DIGITS:
        raise Refused(DIMENSION_NOT_REPRESENTABLE)
    return text


def read_board_outline(data):
    """Inspect ONE board file's raw bytes. Returns ``BoardOutline`` or raises
    ``Refused`` with a closed code. Pure: no I/O, no clock, no randomness."""
    if isinstance(data, (bytes, bytearray)) and len(data) > MAX_FILE_BYTES:
        raise Refused(TOO_LARGE)
    digest = hashlib.sha256(bytes(data)).hexdigest() \
        if isinstance(data, (bytes, bytearray)) else None
    text = _decode(data)
    root = _tree(_tokens(text))
    if _head(root) != "kicad_pcb":
        raise Refused(NOT_KICAD_BOARD)
    versions = [c for c in root[1:] if isinstance(c, list) and _head(c) == "version"]
    if not versions:
        raise Refused(VERSION_MISSING)
    if len(versions) != 1 or len(versions[0]) != 2 or isinstance(versions[0][1], (list, _Str)):
        raise Refused(FIELD_MALFORMED)
    allowed = _SHAPE_FIELDS.get(versions[0][1])      # strict dispatch on the ONE version
    if allowed is None:
        raise Refused(VERSION_NOT_ACCEPTED)
    # Exhaustive Edge.Cuts walk: every list anywhere whose layer field names Edge.Cuts.
    # Only a top-level gr_rect / gr_line may; anything else (footprint graphics, arcs,
    # circles, polygons, curves, dimensions, zones, nested shapes) is refused.
    edge, stack = [], [(root, 0)]
    while stack:
        node, depth = stack.pop()
        for child in node[1:]:
            if not isinstance(child, list):
                continue
            if _names_edge(child):
                if not (depth == 1 and any(node is e for e in edge)):
                    raise Refused(UNSUPPORTED_OUTLINE)
                continue
            if depth == 0 and any(isinstance(g, list) and _names_edge(g) for g in child[1:]):
                edge.append(child)
                if len(edge) > MAX_EDGE_SHAPES:
                    raise Refused(TOO_MANY_OUTLINE_SHAPES)
            stack.append((child, depth + 1))
    if not edge:
        raise Refused(OUTLINE_MISSING)
    shapes = [(_head(n), _shape(n, allowed)) for n in edge]
    kinds = sorted({k for k, _ in shapes})
    if kinds == ["gr_rect"] and len(shapes) == 1:
        (x1, y1), (x2, y2) = shapes[0][1]
        width, height = abs(x2 - x1), abs(y2 - y1)
    elif kinds == ["gr_line"] and len(shapes) == 4:
        width, height = _f1_rectangle([pts for _k, pts in shapes])
    else:
        raise Refused(NOT_ONE_RECTANGLE)
    return BoardOutline(source_sha256=digest, source_size=len(data), format_id=FORMAT_ID,
                        reader_id=READER_ID, rule_id=RULE_ID,
                        file_x=_canonical(width), file_y=_canonical(height))
