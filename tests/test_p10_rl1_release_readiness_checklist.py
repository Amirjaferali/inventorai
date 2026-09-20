"""P10-RL1 — Release-Readiness Checklist: structural invariants.

File: tests/test_p10_rl1_release_readiness_checklist.py
Purpose: keep `docs/governance/PHASE_10_RELEASE_READINESS_CHECKLIST.md` — the
readiness TRUTH SURFACE — from silently regressing into an approval artifact
or an overclaiming one. Governance doc-invariant tests in the established
repository convention (P10-RL1 changes no runtime code).
Output contract: the canonical artifact exists exactly once; the status
vocabulary is bounded and defined; every checklist row carries source
traceability; the load-bearing distinctions stay visible (foundations ≠
production readiness; PSRR registered/triggered/executed/GO distinct;
deployment distinct; paid activation blocked; adviser/provider/commercial
items never marked implemented/selected; SEC2 residual gaps and the DEP1
point-in-time + test-only-dependency nuances preserved).
Prohibited: weakening to pass; fabricating readiness.
"""
import glob
import os
import re
import unicodedata

from tests import current_truth_contract as contract

CHECKLIST = os.path.join("docs", "governance",
                         "PHASE_10_RELEASE_READINESS_CHECKLIST.md")

STATUSES = ("IMPLEMENTED LOCAL FOUNDATION", "OPEN",
            "DEFERRED — EXTERNAL ADVISER REQUIRED", "PROVIDER-DEPENDENT",
            "COMMERCIAL DECISION REQUIRED", "PSRR-TIME", "DEPLOYMENT-TIME",
            "BLOCKED")


def _text():
    with open(CHECKLIST, encoding="utf-8") as fh:
        return fh.read()


def _norm():
    return re.sub(r"\s+", " ", _text())


def test_canonical_checklist_exists_exactly_once():
    assert os.path.isfile(CHECKLIST)
    rivals = [p for p in glob.glob(os.path.join("docs", "**", "*.md"),
                                   recursive=True)
              if re.search(r"(RELEASE|LAUNCH|GO_?LIVE).*CHECKLIST",
                           os.path.basename(p), re.I)]
    assert rivals == [CHECKLIST.replace(os.sep, "/")] or rivals == [CHECKLIST]


def test_not_an_approval_gate():
    text = _norm()
    assert "RELEASE READINESS CHECKLIST FOUNDATION ≠ RELEASE APPROVAL" in text
    assert ("PSRR GO/NO-GO remains a separate future gate before first "
            "public production deployment." in text)
    assert "owns no decision" in text            # truth index, not policy owner


def test_status_vocabulary_defined_and_bounded():
    text = _text()
    for status in STATUSES:
        assert status in text, status
    for vague in ("mostly ready", "nearly complete", "almost done",
                  "low risk", "probably ready"):
        assert vague not in text.lower(), vague


def test_every_checklist_row_has_source_traceability():
    """Every table row (RL-* item) must cite at least one repository path or
    a registered governance identifier in its source column."""
    rows = [l for l in _text().splitlines() if re.match(r"\| RL-[A-G]\d", l)]
    assert len(rows) >= 40, "expected the full obligation inventory"
    for row in rows:
        assert re.search(
            r"(docs/|web/|engine/|scripts/|tests/|P10-|P8-|P5-|P7-|OD-|PSRR|"
            r"D-P8-PL-01|D-PSRR-01|LQ-|TQ-)", row), row


def test_psrr_states_distinct_and_current():
    """The four PSRR states stay distinct, and the CURRENT one is stated.

    REPAIRED (v1.32). This guard previously pinned `PSRR TRIGGERED: NO`. That
    was true before OD-FR1 and before the application-layer tranche was
    authorized and executed; afterwards the pin forced the truth surface to
    keep asserting something false, and collapsed the three genuinely separate
    facts — trigger condition, execution progress, and GO — into one flag. It
    now requires each to be stated separately and truthfully, and confines the
    old pin to superseded context (see the test below).
    """
    text = _norm()
    for state in ("PSRR REGISTERED", "PSRR TRIGGERED", "PSRR EXECUTED",
                  "PSRR GO/NO-GO"):
        assert state in text, state
    # trigger condition: met — an event that happened, not an authorization
    assert "PSRR TRIGGER CONDITION: MET (OD-FR1)" in text
    # execution: begun but bounded — never stated as complete
    assert "PSRR EXECUTION: BEGUN — APPLICATION-LAYER TRANCHE ONLY" in text
    assert "PSRR REMAINING:" in text
    # completion and GO remain separate, and neither is established
    assert "PSRR NOT COMPLETE" in text
    assert "PSRR GO ELIGIBLE: NOT ESTABLISHED" in text
    assert "PSRR = GO: NOT ESTABLISHED — no GO and no NO-GO exists" in text
    # and the checklist still owns no part of the gate
    assert "this checklist does not trigger it" in text


def test_old_psrr_untriggered_pin_only_survives_as_labeled_history():
    """`PSRR TRIGGERED: NO` may no longer be stated as present truth."""
    text = _norm()
    for match in re.finditer(r"PSRR TRIGGERED: NO", text):
        window = text[max(0, match.start() - 400):match.start()]
        assert "SUPERSEDED" in window, (
            "this pin may appear ONLY inside preserved superseded text: %s"
            % text[max(0, match.start() - 200):match.end() + 80])


def test_deployment_and_paid_activation_remain_blocked():
    text = _norm()
    assert "DEPLOYMENT AUTHORIZED: NO" in text
    assert "PAID ACTIVATION AUTHORIZED: NO" in text
    # Narrow pin update (Phase-10 formal closure gate): the original
    # "PHASE 10 CLOSURE ELIGIBLE NOW: NO" pin was factually superseded by the
    # Owner-accepted P10-CL0 eligibility determination and the OD-P10-CL0-STRUCTURE
    # Option-2 decision (PR #538). The protective purpose is preserved by pinning
    # the closure-truth line that still forbids reading closure as approval.
    assert "PHASE-10 CLOSURE ≠ RELEASE APPROVAL" in text


def test_foundations_never_imply_production_readiness():
    text = _norm()
    assert ("does NOT imply production readiness" in text)
    assert "local ≠ production backup readiness" in text
    for forbidden in ("release ready", "production ready", "launch ready",
                      "all security complete", "all legal complete",
                      "PSRR complete", "privacy compliant", "GDPR compliant",
                      "tax compliant", "dependencies secure",
                      "all vulnerabilities resolved", "monitoring active"):
        assert forbidden.lower() not in text.lower(), forbidden


def test_sec2_residual_gaps_visible():
    text = _norm()
    assert "transport-bounded ONLY" in text
    assert 'NOT "all inputs fully hardened"' in text


def test_dep1_point_in_time_and_test_only_dependency_visible():
    text = _norm()
    assert "POINT-IN-TIME ONLY" in text
    assert "NO continuous scanning" in text
    assert "NO auto-remediation" in text
    assert "tests/requirements-draft-l2.txt" in text
    assert "NOT covered by that audit run" in text


# --------------------------------------------------------------------------
# PROVIDER-DEPENDENT rows: explicit machine-readable state, by immutable ID,
# read only from the CURRENT-TRUTH region.
#
# DESIGN RESET (v1.32). Earlier versions of this guard tried to infer a row's
# state from its English prose — first by keyword, then by stripping Markdown
# shapes, then with a semantic claim classifier. Each attempt was over-
# engineered and still unsafe: free prose has synonyms, negation scope,
# subjects and conjunctions, and a guard that must understand all of that is
# a guard that will be wrong. The prose is no longer authority for anything.
#
# Each owned row now carries two structured elements and they ARE the row's
# machine truth: one CURRENT STATE marker from a bounded vocabulary, and one
# {…} field block of six YES/NO/N/A fields. Deterministic invariants bind
# marker to fields. The prose after them is explanatory only and is not read
# for state. History lives outside the region and is never read at all.
# --------------------------------------------------------------------------
_PD_CURRENT_STATES = (
    "NOT SELECTED",
    "SELECTED / NOT PROVISIONED",
    "PROVISIONED / NOT COMPLETE",
    "IMPLEMENTED / NOT DEPLOYED",
    "DEPLOYED / NOT COMPLETE",
)

# The provider-dependent inventory this guard owns, by IMMUTABLE row ID.
# Enumerated on purpose: a row may not escape validation by having its
# dependency label, status text or category text edited.
_PROVIDER_ROW_IDS = (
    "RL-B2", "RL-B3", "RL-B4", "RL-B6",
    "RL-C2", "RL-C3", "RL-C5",
    "RL-E4", "RL-E5", "RL-E7",
    "RL-F1", "RL-F2", "RL-F3", "RL-F4", "RL-F5", "RL-F6",
)

_FIELD_NAMES = ("SELECTED", "PROVISIONED", "IMPLEMENTED", "DEPLOYED",
                "LIVE_ACTIVATED", "COMPLETE")
_FIELD_VALUES = {
    "SELECTED": ("YES", "NO", "N/A"),
    "PROVISIONED": ("YES", "NO", "N/A"),
    "IMPLEMENTED": ("YES", "NO", "N/A"),
    "DEPLOYED": ("YES", "NO", "N/A"),
    "LIVE_ACTIVATED": ("YES", "NO", "N/A"),
    "COMPLETE": ("YES", "NO"),
}

_GATE = re.compile(r"(INFRA-G1-R1|OD-INFRA-\d|OD-CJ1|P8-I4|OD-J2|OD-DR1|P10-BR1)")

# Deterministic marker → field invariants. Each entry names the values a
# field MAY take under that state; a field not listed is unconstrained.
# COMPLETE is constrained to NO under every state because no completion
# state exists in the vocabulary.
_INVARIANTS = {
    "NOT SELECTED": {
        "SELECTED": ("NO",),
        "PROVISIONED": ("NO", "N/A"),
        "IMPLEMENTED": ("NO", "N/A"),
        "DEPLOYED": ("NO", "N/A"),
        "LIVE_ACTIVATED": ("NO", "N/A"),
        "COMPLETE": ("NO",),
    },
    "SELECTED / NOT PROVISIONED": {
        "SELECTED": ("YES",),
        "PROVISIONED": ("NO",),
        "DEPLOYED": ("NO",),
        "LIVE_ACTIVATED": ("NO",),
        "COMPLETE": ("NO",),
    },
    "PROVISIONED / NOT COMPLETE": {
        "SELECTED": ("YES", "N/A"),
        "PROVISIONED": ("YES",),
        # deployment fields reflect actual evidence, not implication — but a
        # live-activated subject would belong under a later state
        "LIVE_ACTIVATED": ("NO", "N/A"),
        "COMPLETE": ("NO",),
    },
    "IMPLEMENTED / NOT DEPLOYED": {
        "SELECTED": ("YES", "N/A"),
        "IMPLEMENTED": ("YES",),
        "DEPLOYED": ("NO",),
        "LIVE_ACTIVATED": ("NO",),
        "COMPLETE": ("NO",),
    },
    "DEPLOYED / NOT COMPLETE": {
        "SELECTED": ("YES", "N/A"),
        "PROVISIONED": ("YES", "N/A"),
        "IMPLEMENTED": ("YES", "N/A"),
        "DEPLOYED": ("YES",),
        # LIVE_ACTIVATED reflects actual truth independently
        "COMPLETE": ("NO",),
    },
}



# --------------------------------------------------------------------------
# The authoritative contract parser.
#
# HARDENED (v1.32 structural-parser pass). The earlier parser used findall()
# to pull "a" marker and "a" {…} block from anywhere in the cell. That let a
# malformed first marker be rescued by a later valid one, and let a malformed
# outer block hide a valid inner block that findall's [^{}]* happily matched.
# This parser reads the contract from ONE fixed location - the start of the
# cell - and validates the WHOLE structure: prefix, block, flatness,
# delimiters, exact field set, and the absence of any second machine
# declaration in the remaining prose. It never searches, never falls back,
# and never picks a best match. Malformed means malformed.
# --------------------------------------------------------------------------
_PREFIX = "CURRENT STATE: "

# --------------------------------------------------------------------------
# ONE lexical grammar for machine declarations.
#
# HARDENED (v1.32 lexical pass). The block parser split entries on ":" and
# stripped whitespace, so it accepted "COMPLETE : NO"; the trailing detector
# looked for the narrower literal "complete:" and therefore let
# "COMPLETE : YES", "current state : completed" and "_COMPLETE: YES_" survive
# in the prose after the block. Two grammars, one gap. There is now exactly
# one recognizer, and both the authoritative block and the trailing scan
# read it. Anything the block could accept, the scan must see.
#
# A machine declaration is: a declaration boundary (not embedded in a word
# or a hyphenated human label), bounded Markdown emphasis, a machine KEY,
# bounded emphasis, bounded whitespace, a colon. Case-insensitive. So
# "Owner-SELECTED: Render" is one hyphenated word and is NOT a declaration,
# while "SELECTED: YES", " selected : yes", "_SELECTed: YES_" and
# "**SELECTED : YES**" all are.
# --------------------------------------------------------------------------
_MACHINE_KEYS = ("CURRENT STATE",) + _FIELD_NAMES

# --------------------------------------------------------------------------
# Horizontal whitespace, normalized ONCE before the grammar sees anything.
#
# HARDENED (v1.32 Unicode-whitespace pass). The recognizer matched only ASCII
# space and tab around the colon, so "COMPLETE\u00A0: YES" (NBSP),
# "DEPLOYED\u202F: YES" (narrow NBSP) and "CURRENT STATE\u2009: completed"
# (thin space) slipped past the trailing scan. Every horizontal space
# character - Unicode general category Zs, plus TAB - is now folded to one
# ASCII space before either consumer runs, character for character, so
# offsets are preserved and both the block parser and the trailing scan see
# the same normalized text. Line-breaking characters (LF, CR, VT, FF, NEL,
# LINE SEPARATOR, PARAGRAPH SEPARATOR) are NOT horizontal whitespace and are
# left untouched: a declaration cannot be assembled across a line break.
# --------------------------------------------------------------------------
_HORIZONTAL_SPACE = frozenset(
    [chr(c) for c in range(0x10000) if unicodedata.category(chr(c)) == "Zs"]
    + ["\t"])
# the enumerated class from the hardening instruction must be fully covered
assert _HORIZONTAL_SPACE.issuperset(
    "\u0020\u0009\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005"
    "\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000")
assert not _HORIZONTAL_SPACE.intersection("\n\r\x0b\x0c\u0085\u2028\u2029")


def normalize_horizontal_space(text):
    """Fold every horizontal space character to ASCII space, 1:1."""
    return "".join(" " if ch in _HORIZONTAL_SPACE else ch for ch in text)


_DECLARATION = re.compile(
    r"(?<![A-Za-z0-9_-])"                       # declaration boundary
    r"(?P<lead>[*_`]*)[ \t]*"                    # bounded leading emphasis
    r"(?P<key>current[ \t]+state|selected|provisioned|implemented|deployed"
    r"|live_activated|complete)"
    r"(?P<trail>[*_`]*)[ \t]*:",                 # emphasis, whitespace, colon
    re.IGNORECASE)


def recognize_machine_declarations(text):
    """Every machine declaration in `text`, as (canonical_key, match).

    This is the single source of lexical truth for the contract: the block
    parser uses it to read a field entry, and the trailing scan uses it to
    find a forbidden second declaration. They cannot disagree.
    """
    found = []
    for match in _DECLARATION.finditer(normalize_horizontal_space(text)):
        key = re.sub(r"[ \t]+", " ", match.group("key")).upper()
        found.append((key, match))
    return found


class ContractError(AssertionError):
    """A row's machine contract is malformed. It is not interpreted further."""


def _parse_contract(cell):
    """Parse `cell` as `<state>. {<six fields>} <prose>` from its start.

    Returns (state, fields). Raises ContractError on any structural fault.
    Nothing after the closing delimiter may carry machine meaning.
    """
    # 0. one representation for both consumers: horizontal space folded 1:1
    cell = normalize_horizontal_space(cell)

    # 1. bounded leading whitespace only (table-cell padding)
    body = cell
    stripped = body.lstrip(" ")
    if len(body) - len(stripped) > 3:
        raise ContractError("too much leading whitespace before the contract")
    body = stripped

    # 2. authoritative prefix at the very start
    if not body.startswith(_PREFIX):
        raise ContractError("cell does not begin with the CURRENT STATE prefix")
    body = body[len(_PREFIX):]

    # 3. the state runs to the first period and must be exact vocabulary
    dot = body.find(".")
    if dot == -1:
        raise ContractError("CURRENT STATE is not terminated by a period")
    state = body[:dot]
    if state not in _PD_CURRENT_STATES:
        raise ContractError("unknown or malformed CURRENT STATE: %r" % state)
    body = body[dot + 1:]

    # 4. the field block must come immediately next (one optional space)
    if body.startswith(" "):
        body = body[1:]
    if not body.startswith("{"):
        raise ContractError("field block must immediately follow the state")
    body = body[1:]

    # 5. flat, closed block: no nested open before the close, and exactly one
    #    close - the remainder may contain no delimiter of either kind
    close = body.find("}")
    nested = body.find("{")
    if close == -1:
        raise ContractError("field block is not closed")
    if nested != -1 and nested < close:
        raise ContractError("nested opening delimiter inside the field block")
    block, rest = body[:close], body[close + 1:]
    if "{" in rest or "}" in rest:
        raise ContractError("stray or additional block delimiter after the "
                            "authoritative field block")

    # 6. exactly the six known fields, each once, each with a valid value.
    #    An entry is read with the SAME recognizer the trailing scan uses;
    #    the block then additionally requires the canonical spelling - an
    #    upper-case key with no emphasis - so the block is a strict subset of
    #    what the recognizer detects, never a superset.
    fields = {}
    for entry in block.split(";"):
        declarations = recognize_machine_declarations(entry)
        if len(declarations) != 1:
            raise ContractError("malformed field entry: %r" % entry)
        name, match = declarations[0]
        if entry[:match.start()].strip(" \t"):
            raise ContractError("malformed field entry: %r" % entry)
        if match.group("lead") or match.group("trail") \
                or match.group("key") != name:
            raise ContractError("non-canonical field key in block: %r" % entry)
        if name not in _FIELD_NAMES:
            raise ContractError("unknown field: %r" % name)
        if name in fields:
            raise ContractError("duplicate field: %r" % name)
        value = entry[match.end():].strip(" \t")
        if value not in _FIELD_VALUES[name]:
            raise ContractError("invalid value for %s: %r" % (name, value))
        fields[name] = value
    missing = [name for name in _FIELD_NAMES if name not in fields]
    if missing:
        raise ContractError("missing fields: %r" % missing)

    # 7. the prose may carry no second machine declaration of any kind -
    #    any case, any bounded whitespace around the colon, any bounded
    #    emphasis - not even "just an example". Same recognizer as step 6.
    extra = recognize_machine_declarations(rest)
    if extra:
        raise ContractError(
            "duplicate or ambiguous machine declaration in prose: %r"
            % extra[0][1].group(0))

    return state, fields


def _release_current_truth():
    """The explicit CURRENT-TRUTH:RELEASE-READINESS region."""
    return contract.region(_text(), "RELEASE-READINESS")


def _row(row_id):
    """Locate a row by its IMMUTABLE ID, inside the current-truth region."""
    prefix = "| %s |" % row_id
    matches = [line for line in _release_current_truth().splitlines()
               if line.startswith(prefix)]
    assert len(matches) == 1, (
        "row %s must appear exactly once inside the CURRENT-TRUTH region, "
        "found %d" % (row_id, len(matches)))
    return matches[0]


def _cells(row):
    cells = row.split("|")
    assert len(cells) >= 7, row
    return cells


def _row_truth(row):
    """The row's own CURRENT TRUTH cell - where its machine contract lives."""
    return _cells(row)[5]


def _row_contract(row_id):
    try:
        return _parse_contract(_row_truth(_row(row_id)))
    except ContractError as exc:
        raise AssertionError("%s: %s" % (row_id, exc))


def _row_state(row_id):
    return _row_contract(row_id)[0]


def _row_fields(row_id):
    return _row_contract(row_id)[1]


# --------------------------------------------------------------------------
# Parser unit tests on synthetic cells - the structural failure class itself,
# independent of the live document.
# --------------------------------------------------------------------------
_VALID_BLOCK = ("{SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; "
                "DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO}")
_VALID_CELL = " CURRENT STATE: PROVISIONED / NOT COMPLETE. " + _VALID_BLOCK + \
              " Owner-SELECTED: Render (OD-INFRA-1); one live backup object exists "

_MALFORMED_CELLS = {
    "missing prefix, valid marker later":
        " Owner-SELECTED. Example: CURRENT STATE: PROVISIONED / NOT COMPLETE. " + _VALID_BLOCK,
    "malformed first state, valid later":
        " CURRENT STATE: COMPLETE! " + _VALID_BLOCK +
        " Previous example: CURRENT STATE: PROVISIONED / NOT COMPLETE.",
    "unknown state":
        " CURRENT STATE: MOSTLY DONE. " + _VALID_BLOCK,
    "punctuation-corrupted marker":
        " CURRENT STATE - PROVISIONED / NOT COMPLETE. " + _VALID_BLOCK,
    "lowercase duplicate declaration later":
        _VALID_CELL + " previous: current state: completed",
    "uppercase duplicate declaration later":
        _VALID_CELL + " PREVIOUS: CURRENT STATE: NOT SELECTED.",
    "two valid markers":
        _VALID_CELL + " CURRENT STATE: PROVISIONED / NOT COMPLETE. " + _VALID_BLOCK,
    "invalid first, valid second":
        " CURRENT STATE: DONE. {COMPLETE: YES} CURRENT STATE: NOT SELECTED. "
        "{SELECTED: NO; PROVISIONED: N/A; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO}",
    "missing block":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. prose only",
    "block not immediately after state":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. see below " + _VALID_BLOCK,
    "duplicated block":
        _VALID_CELL + " " + _VALID_BLOCK,
    "nested block":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: NO; COMPLETE: YES " + _VALID_BLOCK + "}",
    "malformed outer, valid inner":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: NO; COMPLETE: YES; " + _VALID_BLOCK + "}",
    "unclosed outer, valid inner":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: NO; " + _VALID_BLOCK,
    "unclosed block":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO prose",
    "stray close":
        _VALID_CELL + " } ",
    "wrong delimiter order":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. }SELECTED: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO{",
    "extra field":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO; RELEASED: YES}",
    "missing field":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; COMPLETE: NO}",
    "duplicate field":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; DEPLOYED: YES; LIVE_ACTIVATED: NO; COMPLETE: NO}",
    "malformed key":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO}",
    "malformed value":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: MAYBE; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO}",
    "COMPLETE: N/A (not permitted for COMPLETE)":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: N/A}",
    "field outside block":
        _VALID_CELL + " DEPLOYED: YES",
    "second block in prose":
        _VALID_CELL + " historically {DEPLOYED: YES}",
    "field-style declaration in prose":
        _VALID_CELL + " note - complete: yes as of Friday",
    # --- lexical class: spacing, tabs, case, emphasis after the block ---
    "spaced colon after block": _VALID_CELL + " COMPLETE : YES",
    "spaced DEPLOYED after block": _VALID_CELL + " DEPLOYED : YES",
    "tabbed lowercase after block": _VALID_CELL + " complete\t:\tyes",
    "spaced current state after block": _VALID_CELL + " current state : completed",
    "underscore-wrapped after block": _VALID_CELL + " _COMPLETE: YES_",
    "bold-wrapped spaced after block": _VALID_CELL + " **DEPLOYED : YES**",
    "SELECTED spaced after block": _VALID_CELL + " SELECTED : YES",
    "lowercase selected spaced after block": _VALID_CELL + " selected : yes",
    "mixed-case emphasised after block": _VALID_CELL + " _SELECTed: YES_",
    "bold SELECTED spaced after block": _VALID_CELL + " **SELECTED : YES**",
    "backtick-wrapped after block": _VALID_CELL + " `COMPLETE: YES`",
    "leading spaces duplicate": _VALID_CELL + "     DEPLOYED: YES",
    "tab-led duplicate": _VALID_CELL + "\tDEPLOYED:\tYES",
    "malformed first then spaced duplicate":
        " CURRENT STATE: COMPLETE! " + _VALID_BLOCK + " COMPLETE : NO",
    "emphasised key inside block":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {_SELECTED_: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO}",
    "lowercase key inside block":
        " CURRENT STATE: PROVISIONED / NOT COMPLETE. {selected: YES; PROVISIONED: YES; "
        "IMPLEMENTED: N/A; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO}",
    # --- Unicode horizontal whitespace around the colon, after the block ---
    "NBSP before colon": _VALID_CELL + " COMPLETE\u00A0: YES",
    "narrow NBSP before colon": _VALID_CELL + " COMPLETE\u202F: YES",
    "thin space before colon": _VALID_CELL + " COMPLETE\u2009: YES",
    "NBSP both sides": _VALID_CELL + " DEPLOYED\u00A0:\u00A0YES",
    "figure space both sides": _VALID_CELL + " SELECTED\u2007:\u2007YES",
    "ideographic space in CURRENT STATE": _VALID_CELL + " CURRENT STATE\u3000: COMPLETED",
    "lowercase + em space": _VALID_CELL + " complete\u2003: yes",
    "mixed case + hair space": _VALID_CELL + " Deployed\u200A: Yes",
    "bold-wrapped + NBSP": _VALID_CELL + " **COMPLETE\u00A0: YES**",
    "mixed ASCII and Unicode space": _VALID_CELL + " COMPLETE \u00A0\t: YES",
    "ogham space mark": _VALID_CELL + " PROVISIONED\u1680: YES",
    "medium mathematical space": _VALID_CELL + " LIVE_ACTIVATED\u205F: YES",
    "NBSP inside CURRENT STATE key": _VALID_CELL + " CURRENT\u00A0STATE: COMPLETED",
}

_VALID_CELLS = {
    "canonical": _VALID_CELL,
    "no padding": "CURRENT STATE: NOT SELECTED. {SELECTED: NO; PROVISIONED: N/A; "
                  "IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO}",
    "prose uses 'live' as adjective": _VALID_CELL + " the live backup object is live.",
    "prose names providers": _VALID_CELL + " Candidates: Stripe, Adyen, Tap; none selected.",
    "prose says NOT COMPLETE without a colon": _VALID_CELL + " release: NOT COMPLETE",
    "prose mentions deployment word without colon": _VALID_CELL + " it is not deployed anywhere",
    "deployed state": " CURRENT STATE: DEPLOYED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; "
                      "IMPLEMENTED: N/A; DEPLOYED: YES; LIVE_ACTIVATED: NO; COMPLETE: NO} prose",
    "implemented state": " CURRENT STATE: IMPLEMENTED / NOT DEPLOYED. {SELECTED: YES; PROVISIONED: N/A; "
                         "IMPLEMENTED: YES; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO} prose",
    # --- lexical class: human labels and plain words are not declarations ---
    "Owner-SELECTED label": _VALID_CELL + " Owner-SELECTED: Render",
    "owner-selected lowercase label": _VALID_CELL + " owner-selected: Resend",
    "word 'selected' without declaration syntax": _VALID_CELL + " no provider is selected here",
    "word 'complete' without declaration syntax": _VALID_CELL + " the work is not complete",
    "spaced colon inside block is tolerated": " CURRENT STATE: NOT SELECTED. {SELECTED : NO; PROVISIONED: N/A; "
        "IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE : NO} prose",
    "Owner-SELECTED with NBSP before colon is still a human label":
        _VALID_CELL + " Owner-SELECTED\u00A0: Cloudflare R2",
    "word-embedded key with NBSP is not a declaration": _VALID_CELL + " incomplete\u00A0: yes",
}


def test_contract_parser_rejects_every_malformed_structure():
    for label, cell in _MALFORMED_CELLS.items():
        try:
            _parse_contract(cell)
        except ContractError:
            continue
        raise AssertionError("parser accepted a malformed cell: %s" % label)


def test_declaration_grammar_folds_horizontal_space_but_not_line_breaks():
    """One normalized representation; line structure stays intact."""
    for space in ("\u00A0", "\u202F", "\u2009", "\u3000", "\t", "\u2007"):
        assert recognize_machine_declarations("COMPLETE" + space + ": YES"), repr(space)
        assert recognize_machine_declarations("current" + space + "state: x"), repr(space)
    for brk in ("\n", "\r", "\x0b", "\x0c", "\u0085", "\u2028", "\u2029"):
        assert not recognize_machine_declarations("COMPLETE" + brk + ": YES"), repr(brk)
        assert not recognize_machine_declarations("current" + brk + "state: x"), repr(brk)
    # the fold is length-preserving, so recognizer offsets are valid on input
    text = "x\u00A0COMPLETE\u3000: YES"
    assert len(normalize_horizontal_space(text)) == len(text)


def test_contract_parser_accepts_valid_structures():
    for label, cell in _VALID_CELLS.items():
        state, fields = _parse_contract(cell)
        assert state in _PD_CURRENT_STATES, label
        assert set(fields) == set(_FIELD_NAMES), label


def test_release_current_truth_region_is_well_formed():
    """Missing, duplicated or malformed region = failure, never a silent pass."""
    assert _release_current_truth().strip()


def test_owned_rows_are_found_by_immutable_id_not_by_label():
    """Relabelling a row must not remove it from this guard's inventory."""
    for row_id in _PROVIDER_ROW_IDS:
        assert _row(row_id).startswith("| %s |" % row_id)


def test_every_owned_row_declares_one_bounded_current_state():
    for row_id in _PROVIDER_ROW_IDS:
        assert _row_state(row_id) in _PD_CURRENT_STATES, row_id


def test_every_owned_row_carries_a_well_formed_field_block():
    for row_id in _PROVIDER_ROW_IDS:
        fields = _row_fields(row_id)
        assert set(fields) == set(_FIELD_NAMES), (row_id, fields)


def test_no_owned_row_can_claim_completion():
    """No completion state exists, and COMPLETE is NO on every owned row."""
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        for word in ("COMPLETE", "COMPLETED", "DONE", "FINISHED"):
            assert not re.search(r"(?<!NOT )\b%s\b" % word, state), (row_id, state)
        assert _row_fields(row_id)["COMPLETE"] == "NO", row_id


def test_row_fields_satisfy_their_state_invariants():
    """The deterministic marker → field contract, per state.

    This is the whole guard: a CURRENT STATE marker whose fields say
    something else fails here, and nothing in the explanatory prose can
    rescue or undermine it.
    """
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        fields = _row_fields(row_id)
        # an out-of-vocabulary marker (e.g. "COMPLETE") is a failure in its
        # own right, reported as one rather than as a lookup error
        assert state in _INVARIANTS, (row_id, "unknown CURRENT STATE", state)
        for name, allowed in _INVARIANTS[state].items():
            assert fields[name] in allowed, (
                row_id, state, name, fields[name], "allowed:", allowed)


def test_states_beyond_selection_cite_their_gate():
    """Anything past NOT SELECTED must name the decision that authorized it."""
    for row_id in _PROVIDER_ROW_IDS:
        if _row_state(row_id) == "NOT SELECTED":
            continue
        assert _GATE.search(_row(row_id)), row_id


def test_selected_rows_record_selection_in_fields_not_only_prose():
    """A SELECTED field must be YES wherever the marker says selected.

    The structured field is the truth; a provider name in prose is not.
    """
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        fields = _row_fields(row_id)
        if state == "NOT SELECTED":
            assert fields["SELECTED"] == "NO", row_id
        elif state in ("SELECTED / NOT PROVISIONED", "IMPLEMENTED / NOT DEPLOYED"):
            assert fields["SELECTED"] in ("YES", "N/A"), row_id


def test_owned_row_history_lives_outside_the_region():
    """Superseded row wording is preserved — and never inside current truth."""
    region = _release_current_truth()
    outside = contract.outside(_text(), "RELEASE-READINESS")
    assert "## Superseded row wording" in outside
    assert "SUPERSEDED v1.32" not in region, (
        "a preserved quotation must not sit inside the current-truth region")
    # and the history is genuinely retained, not deleted
    for row_id in ("RL-F1", "RL-F5", "RL-F6", "RL-G3"):
        assert "**%s**" % row_id in outside, row_id


def test_od_infra_4_recorded_as_decided_not_open():
    """A settled selection decision must not be reported as still open."""
    region = re.sub(r"\s+", " ", _release_current_truth())
    assert "OD-INFRA-4 DECISION: SATISFIED AS A SELECTION DECISION" in region
    assert "no dedicated third-party monitoring provider was adopted" in region
    # the remaining operations work must stay visible and separate
    assert "Nobody is notified when something breaks" in region
    # and OD-INFRA-4 must not be described as open anywhere current
    for stale in ("OD-INFRA-4 OPEN", "OD-INFRA-4 stays OPEN",
                  "OD-INFRA-4 remains OPEN"):
        assert stale not in region, stale


def test_adviser_items_not_marked_done():
    for line in _text().splitlines():
        if "DEFERRED — EXTERNAL ADVISER REQUIRED" in line:
            assert not re.search(
                r"\|\s*IMPLEMENTED LOCAL FOUNDATION\s*\+?\s*\|", line), line
    assert "NOT SELECTED" in _text()          # provider truth stated plainly
