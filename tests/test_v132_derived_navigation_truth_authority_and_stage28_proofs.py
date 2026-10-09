"""v1.32 derived-navigation truth guards — live-authority F1 / F2 proofs and Stage 28 named assessments.

Split out of tests/test_v132_derived_navigation_truth.py unchanged, for CI shard balance only
(scripts/ci_full_suite.py places whole files): the live-authority owners pin no transient identity, the F1 / F2
adversarial proofs, and the Stage 28 named-assessment regressions. The owners, documents and helpers stay in the
original module; `_read` is read and patched on that module (`_nav`) so the current-state guard sees the mutated
documents exactly as before the split.
"""

import re

import pytest

import test_v132_derived_navigation_truth as _nav
from test_v132_derived_navigation_truth import (
    CHECKLIST, CONTRACT, ROADMAP, STATE, _HISTORICAL_HEADING, _LEGACY_POST_MERGE_RECORDS,
    _LEGACY_UNMARKED_AUTHORITY_HEADINGS, _LIVE_CLAIM_REVERSALS, _LIVE_DOCS, _NONE_BOLD, _NS, _POST_MERGE_CLAIM,
    _PREMERGE_LIFECYCLE, _after_fence, _authority_sections, _claim_end, _claim_record, _live_authority_problems,
    _live_authority_texts, _live_declaration, _mutate, _span, _status, _unsupported_post_merge_claims,
    _without_identity, _without_transient_identity,
)


def test_the_live_authority_owners_pin_no_transient_identity():
    import inspect
    sources = [inspect.getsource(f) for f in (
        _live_authority_texts, _live_authority_problems, _status, _after_fence, _authority_sections,
        _live_declaration, _unsupported_post_merge_claims, _without_transient_identity, _claim_record, _claim_end,
        _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface)]
    sources.append(repr((_LIVE_CLAIM_REVERSALS, _PREMERGE_LIFECYCLE, _HISTORICAL_HEADING, _POST_MERGE_CLAIM)))
    legacy = repr((sorted(_LEGACY_UNMARKED_AUTHORITY_HEADINGS), sorted(_LEGACY_POST_MERGE_RECORDS.items())))
    assert re.search(r"\b[0-9a-f]{40}\b", legacy) is None and re.search(r"PR ?-?#\d", legacy) is None
    for source in sources:
        assert re.search(r"\b[0-9a-f]{40}\b", source) is None
        assert re.search(r"PR ?-?#\d", source) is None
        assert re.search(r"\[:\d{3,}\]", source) is None
        for word in ("POST-MERGE", "post-merge identity", "REVIEW: PASS", "ANCESTRY", "merge tree"):
            assert word not in source, word


# ---- F1 / F2 adversarial proofs ----------------------------------------------------------------------
def _assert_rejected(monkeypatch, docs, name):
    """Both the live-invariant owner and the current-state guard must reject these documents."""
    real = _nav._read
    fake = lambda p: docs[p] if p in docs else real(p)                   # noqa: E731
    assert _live_authority_problems(fake), name
    monkeypatch.setattr(_nav, "_read", fake)
    with pytest.raises((AssertionError, ValueError)):
        _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()


def _assert_accepted(monkeypatch, docs, name):
    real = _nav._read
    fake = lambda p: docs[p] if p in docs else real(p)                   # noqa: E731
    assert _live_authority_problems(fake) == [], name
    monkeypatch.setattr(_nav, "_read", fake)
    _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()


def _second_heading(contract):
    """Start of the section that follows the live one."""
    live_heading = _live_declaration(contract)[0]
    i = contract.index(live_heading)
    return contract.index("\n## ", i + 5) + 1


_EXTRA_SECTIONS = {
    "successor contract": "## Current authority — successor increment\n\n**ACTIVE CONTRACT: STAGE 15 — SLICE 3.**\n\n",
    "second none": ("## Current authority — another declaration\n\n**ACTIVE CONTRACT: NONE.** NO PRODUCT INCREMENT IS "
                    "CURRENTLY AUTHORIZED.\n\n"),
    "deployment": ("## Current authority — release\n\n**ACTIVE CONTRACT: NONE.** Deployment is authorized. Release "
                   "is authorized.\n\n"),
    "astra example": ("## Current authority — successor increment\n\n**ACTIVE CONTRACT: STAGE 15 — SLICE 3.**\n\n"
                      "Deployment is authorized.\n\n"),
}


@pytest.mark.parametrize("where", ["after the live declaration", "appended later"])
@pytest.mark.parametrize("name", sorted(_EXTRA_SECTIONS))
def test_f1_a_second_live_authority_section_is_rejected(monkeypatch, where, name):
    contract = _nav._read(CONTRACT)
    section = _EXTRA_SECTIONS[name]
    if where == "after the live declaration":
        k = _second_heading(contract)
        mutated = contract[:k] + section + contract[k:]
    else:
        mutated = contract.rstrip("\n") + "\n\n" + section
    with pytest.raises(ValueError, match="live current-authority sections"):
        _live_declaration(mutated)
    _assert_rejected(monkeypatch, {CONTRACT: mutated}, name)


def test_f1_legacy_headings_cannot_be_copied_or_lead_and_live_cannot_be_hidden(monkeypatch):
    contract = _nav._read(CONTRACT)
    legacy = sorted(_LEGACY_UNMARKED_AUTHORITY_HEADINGS)[0]
    copied = contract.rstrip("\n") + "\n\n" + legacy + "\n\n**ACTIVE CONTRACT: STAGE 15 — SLICE 3.**\n"
    _assert_rejected(monkeypatch, {CONTRACT: copied}, "copied legacy heading")
    i = contract.index("## Current authority")
    leading = contract[:i] + legacy + "\n\n**ACTIVE CONTRACT: STAGE 15 — SLICE 3.**\n\n" + contract[i:]
    _assert_rejected(monkeypatch, {CONTRACT: leading}, "legacy heading placed first")
    heading = _live_declaration(contract)[0]
    hidden = contract.replace(heading, heading + " — SUPERSEDED", 1)
    _assert_rejected(monkeypatch, {CONTRACT: hidden}, "live section relabelled as history")


def test_f1_every_existing_authority_section_is_classified():
    sections = _authority_sections(_nav._read(CONTRACT))
    kinds = [s[2] for s in sections]
    assert kinds.count("live") == 1 and kinds[0] == "live"
    assert kinds.count("legacy") == len(_LEGACY_UNMARKED_AUTHORITY_HEADINGS)
    assert {s[0] for s in sections if s[2] == "legacy"} == _LEGACY_UNMARKED_AUTHORITY_HEADINGS
    assert kinds.count("historical") >= 30
    for heading, _text, kind in sections:
        assert kind != "historical" or re.search(_HISTORICAL_HEADING, heading), heading


_PM = "`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"
_F2_NEW_CLAIMS = {
    "new candidate token": " `STAGE 15 SLICE 3: DELIVERED` · " + _PM,
    "this candidate": " This candidate: POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS.",
    "bare token": " " + _PM,
    "prose pass": " Post-merge verification PASS for this slice.",
    "post-integration": " `POST-INTEGRATION VERIFICATION: PASS`",
    "merge verification": " Merge verification: PASS.",
    "post-merge verified": " The delivery was post-merge verified",
    "merged and verified": " Stage 15 Slice 3 was merged and verified.",
}


@pytest.mark.parametrize("name", sorted(_F2_NEW_CLAIMS))
@pytest.mark.parametrize("path, region", [(STATE, "current-position"), (ROADMAP, "current-routing"),
                                          (CONTRACT, "declaration"), ("CLAUDE.md", "head")])
def test_f2_a_newly_authored_post_merge_claim_is_rejected(monkeypatch, path, region, name):
    anchor = _NONE_BOLD if region in ("declaration", "head") else _NS      # ROTATED back at the Stage 35 closure
    docs = _mutate(path, region, anchor, anchor + _F2_NEW_CLAIMS[name])
    _assert_rejected(monkeypatch, docs, name)


def test_f2_a_legacy_claim_cannot_be_reassigned_or_copied(monkeypatch):
    legacy = "`STAGE 15 SLICE 2: DELIVERED — PR #720 — merge "
    raw = _nav._read(ROADMAP)
    i, j = _span(raw, "current-routing")
    k = raw.index(legacy, i, j)
    reassigned = raw[:k] + "`STAGE 15 SLICE 3: DELIVERED" + raw[raw.index("`", k + 1):]
    _assert_rejected(monkeypatch, {ROADMAP: reassigned}, "reassigned to a new subject")
    copied = _mutate(STATE, "current-position", _NS, _NS + " `STAGE 15 SLICE 2: DELIVERED` · " + _PM)
    _assert_rejected(monkeypatch, copied, "legacy claim copied beyond the preserved record")


def test_f2_omission_and_identity_removal_stay_valid(monkeypatch):
    # a candidate adds its own delivery with NO post-merge wording
    candidate = _mutate(STATE, "current-position", _NS, _NS + " `NEW BOUNDED SLICE: DELIVERED`")
    _assert_accepted(monkeypatch, candidate, "candidate without post-merge wording")
    monkeypatch.undo()
    # the whole repository with every legacy post-merge claim removed (post-merge state, no such wording)
    claims = (r"\s+·\s+`POST-MERGE\s+IDENTITY\s+/\s+CONTENT\s+VERIFICATION:\s+PASS`|;?\s*post-merge\s+identity\s+/\s+"
              r"content\s+verification\s+PASS|\s+/\s+POST-MERGE\s+VERIFIED")
    bare = {path: re.sub(claims, "", _nav._read(path)) for path in _LIVE_DOCS}
    texts = _live_authority_texts(lambda p: bare[p] if p in bare else _nav._read(p))
    assert not any(re.search(_POST_MERGE_CLAIM, text, re.I) for text in texts.values())
    _assert_accepted(monkeypatch, bare, "no post-merge wording on any live surface")
    monkeypatch.undo()
    # transient identity removed from delivered tokens (candidate form)
    _assert_accepted(monkeypatch, {path: _without_identity(_nav._read(path)) for path in _LIVE_DOCS}, "identity absent")


# ---- residual F1-A / F1-B / F2 proofs ----------------------------------------------------------------
def _in_live_interval(contract, block):
    """`contract` with `block` inserted inside the live record, just before the next authority heading."""
    i = contract.index(_live_declaration(contract)[0])
    k = contract.index("\n## Current authority", i + 5) + 1
    return contract[:k] + block + contract[k:]


_ORDINARY_H2 = {
    "review example": "## Release authorization\n\n**ACTIVE CONTRACT: STAGE 15 — SLICE 3.**\n\nDeployment is authorized.\n\n",
    "second contract": "## Notes\n\n**ACTIVE CONTRACT: STAGE 16 — SLICE 1.**\n\n",
    "deployment": "## Operations\n\nDeployment is authorized.\n\n",
    "release": "## Operations\n\nRelease is authorized.\n\n",
    "successor": "## Next increment\n\n`NEXT PRODUCT INCREMENT: AUTHORIZED` · `ANOTHER STAGE-15 SLICE: AUTHORIZED`\n\n",
}


@pytest.mark.parametrize("name", sorted(_ORDINARY_H2))
def test_f1a_an_ordinary_heading_cannot_hide_live_authority(monkeypatch, name):
    mutated = _in_live_interval(_nav._read(CONTRACT), _ORDINARY_H2[name])
    assert _ORDINARY_H2[name].split("\n")[0] in _live_declaration(mutated)[1]
    _assert_rejected(monkeypatch, {CONTRACT: mutated}, name)


def test_f1a_legitimate_ordinary_subsections_stay_green(monkeypatch):
    benign = "## Notes\n\nThe declaration above is unchanged; nothing further is authorized.\n\n"
    _assert_accepted(monkeypatch, {CONTRACT: _in_live_interval(_nav._read(CONTRACT), benign)}, "benign subsection")
    # existing records already span ordinary `##` headings (e.g. the historical-authority entries)
    spans = [text for _h, text, _k in _authority_sections(_nav._read(CONTRACT)) if " ## " in text]
    assert spans


_BODY = "\n\n**ACTIVE CONTRACT: STAGE 15 — SLICE 3.**\n\nDeployment is authorized.\n"


@pytest.mark.parametrize("heading", [
    "## Current authority — successor increment — NOT SUPERSEDED",
    "## Current authority — successor increment (previous mandate SUPERSEDED)",
    "## Current authority — successor increment — references a SUPERSEDED contract",
    "## Current authority — successor increment — UNSUPERSEDED",
    "## Current authority — successor increment — SUPERSEDED contract replaced",
    "## Current authority — successor (the DELIVERED Slice 2 is superseded)",
])
def test_f1b_a_negated_or_referential_status_is_not_historical(monkeypatch, heading):
    mutated = _nav._read(CONTRACT).rstrip("\n") + "\n\n" + heading + _BODY
    assert [k for h, _t, k in _authority_sections(mutated) if h == heading] == ["live"]
    _assert_rejected(monkeypatch, {CONTRACT: mutated}, heading)


@pytest.mark.parametrize("heading", [
    "## Current authority — Stage 99 example slice (Owner authorization, 2026-10-01) — DELIVERED",
    "## Current authority — Stage 99 example slice (Owner authorization, 2026-10-01) — DELIVERED; SUPERSEDED as "
    "current authority by the next declaration",
    "## Current authority — example: no active contract (2026-10-01) — SUPERSEDED (2026-10-02) by Stage 99",
])
def test_f1b_a_genuinely_self_labelled_historical_record_is_accepted(monkeypatch, heading):
    mutated = _nav._read(CONTRACT).rstrip("\n") + "\n\n" + heading + "\n\nPreserved history.\n"
    assert [k for h, _t, k in _authority_sections(mutated) if h == heading] == ["historical"]
    _assert_accepted(monkeypatch, {CONTRACT: mutated}, heading)


def test_f1b_unmodified_repository_counts():
    kinds = [k for _h, _t, k in _authority_sections(_nav._read(CONTRACT))]
    # +2 at the Stage 15 closure: its own delivered record and the superseded post-Slice-4 NONE; +2 at the
    # Stage 18 closure: its own delivered record and the superseded post-Stage-15-closure NONE; +2 at the Stage 20
    # closure: its own delivered record and the superseded post-Stage-19-closure NONE; +2 at the Stage 21 closure:
    # its own delivered record and the superseded post-Stage-20-closure NONE; +2 at the Stage 22 closure: its own
    # delivered record and the superseded post-Stage-21-closure NONE
    # Stage 28 Qualification Slice 1: + the delivered Slice-1 record and the superseded post-Stage-22 NONE record
    # Stage 28 Qualification Slice 2: + the delivered Slice-2 record and the superseded post-Slice-1 NONE record
    # Stage 28 Optional Part Slice 1: + its delivered record and the superseded post-Qualification-Slice-2 NONE record
    # Stage 28 Optional Part Slice 2: + its delivered record and the superseded post-Optional-Part-Slice-1 NONE record
    # Stage 30 Part Safeguards Slice 1: + its delivered record and the superseded post-Optional-Part-Slice-2 NONE record
    # Stage 30 closure: + its delivered record and the superseded post-Stage-30-Part-Safeguards-Slice-1 NONE record
    # Stage 28 part-only enablement: + its delivered record and the superseded post-Stage-30-closure NONE record
    # Stage 28 closure: + its delivered record and the superseded post-Stage-28-Part-Only-Enablement NONE record
    # Stage 23 closure: + its delivered record and the superseded post-Stage-28-closure NONE record
    # Stage 24 / CAP-12 Form Mock-up Advisory Slice 1: + its delivered record and the superseded post-Stage-23 NONE record
    # Stage 24 closure: + its delivered record and the superseded post-Stage-24-CAP-12-Slice-1 NONE record
    # Stage 35 first bounded slice: + the superseded post-Stage-24-closure NONE record (the live record is the slice)
    # Stage 35 closure: + its delivered record and the superseded Stage 35 slice record (the live record is NONE again)
    # Stage 36 closure: + its delivered record and the superseded post-Stage-35-closure NONE record
    # Stage 16 closure: + its delivered record and the superseded post-Stage-36-closure NONE record (the delivered Stage 16
    # residual carried no contract section of its own)
    # Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: + its delivered record and the superseded
    # post-Stage-16-closure NONE record (recorded in its after-merge form; the live record is the post-slice NONE)
    # Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: + its delivered record and the superseded
    # post-Stage-25-CAP-13-Slice-1 NONE record (recorded in its after-merge form; the live record is the post-slice NONE)
    assert (kinds.count("live"), kinds.count("historical"), kinds.count("legacy")) == (1, 81, 10)


def _flat_doc(path):
    return re.sub(r"\s+", " ", _nav._read(path))


def _replace_once(text, old, new):
    assert old in text, old
    return text.replace(old, new, 1)


def _raw_replace(path, old, new):
    """One replacement in the RAW document, tolerant of the line wrapping inside `old`."""
    pattern = re.escape(old).replace(r"\ ", r"\s+")
    raw, n = re.subn(pattern, lambda _m: new, _nav._read(path), count=1)
    assert n == 1, old
    return raw


_S2_TOKEN_CLAIM = " · `POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"


def test_f2_existing_records_are_owned_and_counted_per_surface():
    assert _live_authority_problems() == []
    texts = _live_authority_texts(_nav._read)
    texts.pop("heading:" + CONTRACT)
    found = {}
    for label, text in texts.items():
        flat = _without_transient_identity(text)
        for m in re.finditer(_POST_MERGE_CLAIM, flat, re.I):
            key = (label, _claim_record(flat[:m.start()]) + flat[m.start():_claim_end(flat, m)])
            found[key] = found.get(key, 0) + 1
    assert found == {(label, record): n for label, records in _LEGACY_POST_MERGE_RECORDS.items()
                     for record, n in records.items()}


def test_f2_omega_cannot_inherit_a_vacated_allowance(monkeypatch):
    claude = _flat_doc("CLAUDE.md")
    vacated = _replace_once(claude, "post-merge identity / content verification PASS; reviewed", "reviewed")
    omega = _replace_once(vacated, _NONE_BOLD, _NONE_BOLD + " New delivery Omega — "
                          "Verification Preparation — Slice 2 — is DELIVERED (post-merge identity / content "
                          "verification PASS).")
    _assert_rejected(monkeypatch, {"CLAUDE.md": omega}, "omega")


def test_f2_a_new_subject_with_the_old_suffix_or_tail_fails(monkeypatch):
    vacated = _raw_replace(ROADMAP, "merge 2418f7e583b3535d48970cf0989689bb2f8ef2ca`" + _S2_TOKEN_CLAIM,
                           "merge 2418f7e583b3535d48970cf0989689bb2f8ef2ca`")
    suffix = _replace_once(vacated, _NS, _NS + " · `NEW STAGE 15 SLICE 2: DELIVERED`" + _S2_TOKEN_CLAIM)
    _assert_rejected(monkeypatch, {ROADMAP: suffix}, "same suffix, new subject")
    monkeypatch.undo()
    state = _flat_doc(STATE)
    tail = _replace_once(state, "; Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2 — "
                         "delivered", "; Omega — Stage 15 — Subsystem Interface Declaration & Verification Preparation"
                         " — Slice 2 — delivered")
    _assert_rejected(monkeypatch, {STATE: tail}, "whole old tail under a new subject")


def test_f2_a_this_candidate_wrapper_cannot_take_an_old_claim(monkeypatch):
    state = _flat_doc(STATE)
    vacated = _replace_once(state, _S2_TOKEN_CLAIM, "")
    wrapped = _replace_once(vacated, _NS, _NS + " · This candidate: `STAGE 15 SLICE 2: DELIVERED`" + _S2_TOKEN_CLAIM)
    _assert_rejected(monkeypatch, {STATE: wrapped}, "this candidate wrapper")


def test_f2_a_legacy_record_cannot_move_to_another_surface_or_exceed_its_count(monkeypatch):
    moved = _replace_once(_flat_doc(STATE), _NS, _NS + " · `MECHANICAL CAP-01 OPEN-GAP TECHNICAL CONTEXT: DELIVERED`"
                          + _S2_TOKEN_CLAIM)
    _assert_rejected(monkeypatch, {STATE: moved}, "record owned by another surface")
    monkeypatch.undo()
    claude = _flat_doc("CLAUDE.md")
    doubled = _replace_once(claude, _NONE_BOLD, _NONE_BOLD + " Mechanical CAP-01 — "
                            "Open-Gap Technical Context — DELIVERED (post-merge identity / content verification PASS).")
    _assert_rejected(monkeypatch, {"CLAUDE.md": doubled}, "record beyond its preserved count")


def test_f2_the_same_unchanged_record_may_move_within_its_surface(monkeypatch):
    vacated = _raw_replace(ROADMAP, "merge 2418f7e583b3535d48970cf0989689bb2f8ef2ca`" + _S2_TOKEN_CLAIM,
                           "merge 2418f7e583b3535d48970cf0989689bb2f8ef2ca`")
    moved = _replace_once(vacated, _NS, _NS + " · `STAGE 15 SLICE 2: DELIVERED`" + _S2_TOKEN_CLAIM)
    _assert_accepted(monkeypatch, {ROADMAP: moved}, "same record relocated")


# ---- F2 record-binding residual: Markdown wrappers and trailing qualifiers ------------------------------
_S2_TOKEN = "`STAGE 15 SLICE 2: DELIVERED`"


@pytest.mark.parametrize("wrapper", ["This candidate:", "**This candidate:**", "**New delivery:**",
                                     "**Successor:**", "_Successor:_", "***_This candidate_:***",
                                     "**This candidate:** *new delivery*"])
def test_f2_a_markdown_wrapper_stays_part_of_the_record(monkeypatch, wrapper):
    state = _flat_doc(STATE)
    vacated = _replace_once(state, _S2_TOKEN_CLAIM, "")
    wrapped = _replace_once(vacated, _NS, _NS + " · " + wrapper + " " + _S2_TOKEN + _S2_TOKEN_CLAIM)
    _assert_rejected(monkeypatch, {STATE: wrapped}, wrapper)
    assert any(wrapper in p for p in _live_authority_problems(lambda p: wrapped if p == STATE else _nav._read(p)))


_TRAILING = {
    "PASS for New delivery Omega": ("VERIFICATION: PASS`", "VERIFICATION: PASS for New delivery Omega`"),
    "PASS — New delivery Omega": ("VERIFICATION: PASS`", "VERIFICATION: PASS — New delivery Omega`"),
    "VERIFIED for candidate X": ("POST-MERGE VERIFIED", "POST-MERGE VERIFIED for candidate X"),
}


@pytest.mark.parametrize("name", sorted(_TRAILING))
def test_f2_a_trailing_qualifier_inside_the_token_is_part_of_the_claim(monkeypatch, name):
    old, new = _TRAILING[name]
    state = _replace_once(_flat_doc(STATE), old, new)
    _assert_rejected(monkeypatch, {STATE: state}, name)
    assert any(new.rstrip("`") in p for p in _live_authority_problems(lambda p: state if p == STATE else _nav._read(p)))


@pytest.mark.parametrize("qualifier", [" for New delivery Omega", " — candidate X", " (successor slice)"])
def test_f2_a_trailing_qualifier_in_prose_is_part_of_the_claim(monkeypatch, qualifier):
    claude = _replace_once(_flat_doc("CLAUDE.md"), "post-merge identity / content verification PASS; reviewed",
                           "post-merge identity / content verification PASS" + qualifier + "; reviewed")
    _assert_rejected(monkeypatch, {"CLAUDE.md": claude}, qualifier)


def test_f2_complete_claims_end_at_their_token_or_clause():
    token = "`X: DELIVERED` · `POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS for Omega` · `NEXT`"
    m = re.search(_POST_MERGE_CLAIM, token, re.I)
    assert token[m.start():_claim_end(token, m)] == "POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS for Omega`"
    prose = "Omega is DELIVERED (post-merge identity / content verification PASS for Omega; next clause"
    m = re.search(_POST_MERGE_CLAIM, prose, re.I)
    assert prose[m.start():_claim_end(prose, m)] == "post-merge identity / content verification PASS for Omega"


# ---- F2 semantic claim end: a closing backtick is formatting, not the end of the evidence clause ---------
_AFTER_TOKEN = {
    "PASS` for New delivery Omega": ("`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`", " for New delivery Omega"),
    "PASS` — New delivery Omega": ("`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`", " — New delivery Omega"),
    "PASS` (successor slice)": ("`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`", " (successor slice)"),
    "VERIFIED` for candidate X": ("MERGED / POST-MERGE VERIFIED — PR #678 — merge 84c45cec89f5348f279c591dd739ded0d0db24b3`",
                                  " for candidate X"),
}


@pytest.mark.parametrize("name", sorted(_AFTER_TOKEN))
def test_f2_a_qualifier_after_the_closing_backtick_is_part_of_the_claim(monkeypatch, name):
    token, qualifier = _AFTER_TOKEN[name]
    state = _replace_once(_flat_doc(STATE), token, token + qualifier)
    _assert_rejected(monkeypatch, {STATE: state}, name)
    assert any(qualifier.strip(" ()") in p for p in _live_authority_problems(lambda p: state if p == STATE else _nav._read(p)))


def test_f2_a_closing_backtick_does_not_end_the_claim():
    text = "`X: DELIVERED` · `POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS` for New delivery Omega · `NEXT`"
    m = re.search(_POST_MERGE_CLAIM, text, re.I)
    assert text[m.start():_claim_end(text, m)] == ("POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS` for New "
                                                   "delivery Omega")
    text = "`X: DELIVERED` · `POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS` · `NEXT`"
    m = re.search(_POST_MERGE_CLAIM, text, re.I)
    assert text[m.start():_claim_end(text, m)] == "POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"


# ==========================================================================
# Stage 28 — named future technical-responsibility assessments (recorded 2026-10-05)
# ==========================================================================
# Documentation-only recording. Three PRIMARY named assessments sit beside 28-T1…28-T5 in the
# Stage-28 future portfolio under descriptive names, with no `28-T` number. One checker returns every
# material regression; the live documents must return none, and each guarded risk is proven caught.
_S28_NAMED = ("Wireless / RF Connectivity", "Battery / Electrochemical Energy Storage / BMS",
              "Perception / Edge Inference")
_S28_STATUS = "`RECORDED — PLANNING / NAVIGATION ONLY — NOT AUTHORIZED`"
_S28_INVARIANT = "`TECHNICAL RESPONSIBILITY ≠ PHYSICAL COMPONENT ≠ ROOT DOMAIN`"
_S28_NONE_LIVE = "none is implemented, qualified, activated, part-eligible or root-admissible"
_S28_NAMES_RE = "(?:" + "|".join(re.escape(n) for n in _S28_NAMED) + ")"
# ADDED at the Stage 16 closure sync (Owner-reconfirmed 2026-10-06): the cross-cutting Technical Deepening source / IP
# invariant recorded beside the named assessments — lawful reuse, not website accessibility, controls; unclear basis
# abstains; it covers every future Technical Deepening, not only Wireless / RF.
_S28_SOURCE_RULE = "`TECHNICAL DEEPENING SOURCE RULE: OPEN / LAWFULLY REUSABLE SOURCES ONLY`"
_S28_VIEWABLE = "`PUBLICLY VIEWABLE ≠ OPENLY REUSABLE`"
_S28_UNCLEAR = "`DEFER / ABSTAIN / UNABLE TO SUPPORT`"
_S28_SOURCE_NEEDLES = {
    "roadmap": ("only where an explicit lawful reuse basis is recorded",
                "Technical authority alone does not authorize copying, ingesting or republishing",
                "never ingested into governed technical content unless its license or permission clearly authorizes "
                "that use",
                "source-use / license basis, claim scope and limitations",
                "The rule applies proportionally across ALL future Technical Deepening", "not only Wireless / RF"),
    "checklist": ("a lawful, explicit source-use basis only",
                  "never ingested into governed technical content without a license or permission that clearly "
                  "authorizes it",
                  "source-use / license basis, claim scope and limitations",
                  "a cross-cutting invariant for ALL future Technical Deepening",
                  "28-T1…28-T5 and any later Technical Deepening", "not only Wireless / RF")}
_S28_SOURCE_SCOPE = ("Wireless / RF Connectivity", "Battery / Electrochemical Energy Storage / BMS",
                     "Perception / Edge Inference", "28-T1 Sensors", "28-T2 Embedded", "28-T3 Power Electronics",
                     "28-T4 PLC / Industrial Automation", "28-T5 Mechatronics / Robotics", "any later Technical Deepening")
_S28_SOURCE_REVERSALS = (
    r"TECHNICAL DEEPENING SOURCE RULE: (?!OPEN / LAWFULLY REUSABLE SOURCES ONLY\b)",
    r"PUBLICLY VIEWABLE\s*(?:=|==|is)\s*OPENLY REUSABLE",
    r"\b(?:free[- ]to[- ]read|publicly (?:viewable|available))\b[^.]{0,30}\b(?:is|means|counts as)\s+"
    r"(?:openly |lawfully )?reusable",
    r"(?:proprietary|standards-body|vendor)[^.]{0,120}\bmay be (?:freely )?(?:ingested|copied|republished)\b",
    r"(?<!never )\bingested into governed technical content (?:freely|without)",
    r"unclear[^.]{0,80}\b(?:may|can|should) (?:still )?(?:be )?(?:use|used|ingest|ingested|rely|relied)\b",
    r"(?:SOURCE RULE|source / IP (?:invariant|rule))[^.]{0,200}\bapplies only to\b",
    r"\brule applies only to Wireless")


def _stage28_named_assessment_problems(roadmap, checklist):
    """Every material regression of the named Stage-28 assessments; [] when the recording holds."""
    problems = []
    flat = {"roadmap": re.sub(r"\s+", " ", roadmap), "checklist": re.sub(r"\s+", " ", checklist)}
    for name in _S28_NAMED:                                                     # 1 + 2: name and status
        if "**%s** — %s" % (name, _S28_STATUS) not in flat["roadmap"]:
            problems.append("roadmap: %s lost its name or planning-only status" % name)
        if "- [ ] %s — %s" % (name, _S28_STATUS) not in checklist:
            problems.append("checklist: %s lost its name or planning-only status" % name)
    for label, text in flat.items():
        if _S28_NONE_LIVE not in text:                                          # 3: nothing live
            problems.append(label + ": the not-implemented / not-activated statement is missing")
        claim = re.search(_S28_NAMES_RE + r"(?: assessment)?(?: is| are|:)? (?:now )?(?:fully )?"
                          r"(?:implemented|qualified|activated|root-admissible|part-eligible|authorized)\b",
                          text, re.I)
        if claim:
            problems.append(label + ": live-status claim: " + claim.group(0))
        if _S28_INVARIANT not in text:                                          # 4: three meanings stay apart
            problems.append(label + ": the responsibility / component / root-domain invariant is missing")
        if re.search(r"technical responsibilit(?:y|ies)\s*(?:=|==|is|are)\s*(?:a |the )?physical (?:component|part)",
                     text, re.I):
            problems.append(label + ": technical responsibility equated with a physical component")
        for m in re.finditer(r"28-T(\d+)", text):                               # 5: no minted 28-T6/7/8…
            n = int(m.group(1))
            if n <= 5:
                continue
            ctx = text[max(0, m.start() - 5):m.end() + 17]
            if n != 6 or not ("NOT `28-T6`" in ctx or "`28-T6` does not exist" in ctx):
                problems.append(label + ": minted identifier " + m.group(0))
        if re.search(r"\bT[78]\b", text):
            problems.append(label + ": minted T7 / T8 label")
        if re.search(r"STAGE 28: COMPLETE(?! — CURRENT BOUNDED CONTROL-LOOP OPTIONAL-PART SCOPE ONLY)", text):
            problems.append(label + ": unscoped Stage-28 completion")   # 6: never globally discharged
        for m in re.finditer(r"globally discharged", text, re.I):
            if not re.search(r"not $", text[max(0, m.start() - 4):m.start()], re.I):
                problems.append(label + ": Stage-28 discharge claim: " + text[max(0, m.start() - 40):m.end()])
        if re.search(r"IoT(?: \([^)]*\))? (?:now |will |shall )?(?:owns?|absorbs?) (?:the )?(?:future )?(?:Wireless|RF)",
                     text, re.I):                                               # 7: IoT never owns RF
            problems.append(label + ": IoT owns or absorbs Wireless / RF truth")
        if re.search(r"Robotics (?:owns?|holds?) (?:the )?perception|(?<!second )Robotics-owned perception",
                     text, re.I):                                               # 8: no Robotics perception owner
            problems.append(label + ": Robotics owns a perception authority")
        for token in (_S28_SOURCE_RULE, _S28_VIEWABLE, _S28_UNCLEAR) + _S28_SOURCE_NEEDLES[label]:  # 9: source / IP
            if token not in text:
                problems.append(label + ": the Technical Deepening source / IP invariant lost: " + token)
        for pat in _S28_SOURCE_REVERSALS:
            m = re.search(pat, text, re.I)
            if m:
                problems.append(label + ": source / IP invariant reversed: " + m.group(0))
    if "`STAGE 28 IS NOT GLOBALLY DISCHARGED FOR FUTURE ADDITIONAL DOMAINS`" not in flat["roadmap"]:
        problems.append("roadmap: Stage 28 is no longer recorded as not globally discharged")
    if "They do not reopen or globally complete Stage 28" not in flat["roadmap"]:
        problems.append("roadmap: the named assessments no longer state they leave Stage 28 open")
    if "IoT (Stage 31) may CONSUME future Wireless / RF truth but must not own or absorb it." not in flat["roadmap"]:
        problems.append("roadmap: the Wireless / RF entry lost its IoT consume-not-absorb boundary")
    row31 = re.search(r"^- \[ \] \*\*31 — IoT architecture:\*\*.*$", roadmap, re.M)
    if not row31 or "IoT may CONSUME future Wireless / RF Connectivity truth" not in row31.group(0) \
            or "but must not own or absorb it." not in row31.group(0):
        problems.append("roadmap row 31: the consume-not-absorb Wireless / RF boundary is missing")
    rule = flat["roadmap"].find(_S28_SOURCE_RULE)                              # 9: cross-cutting scope
    rule_text = flat["roadmap"][rule:flat["roadmap"].find("**Secondary future portfolio notes", rule)] if rule >= 0 else ""
    for target in _S28_SOURCE_SCOPE:
        if target not in rule_text:
            problems.append("roadmap: the source / IP invariant no longer covers " + target)
    t5 = re.search(r"\*\*28-T5 — [^\n]*", roadmap)
    if not t5 or "never to a second Robotics-owned perception authority" not in t5.group(0):
        problems.append("roadmap 28-T5: the shared Perception / Edge Inference cross-reference is missing")
    return problems


def test_stage28_named_assessments_are_recorded_planning_only():
    assert _stage28_named_assessment_problems(_nav._read(ROADMAP), _nav._read(CHECKLIST)) == []


def test_stage28_named_assessments_add_no_stage_and_keep_28_t1_to_t5():
    roadmap, checklist = _nav._read(ROADMAP), _nav._read(CHECKLIST)
    # ROTATED at the Stage 16 closure (row 16 ticked for its bounded scope only): 21 -> 20 unticked rows; the Stage 28
    # recording still adds zero top-level stages, so all 45 rows stay exactly 1..45
    assert len(re.findall(r"^- \[ \] \*\*\d+ — ", roadmap, re.M)) == 20
    assert sorted(int(n) for n in re.findall(r"^- \[[ x]\] \*\*(\d+) — ", roadmap, re.M)) == list(range(1, 46))
    for n, title in ((1, "Sensors, Instrumentation & Data Acquisition"), (2, "Embedded Systems & Firmware"),
                     (3, "Power Electronics & Motion Control"), (4, "PLC / Industrial Automation & Control"),
                     (5, "Mechatronics / Robotics — Shared Composition Reuse & Residual-Capability Reassessment")):
        assert roadmap.count("**28-T%d — %s.**" % (n, title)) == 1, n
        assert checklist.count("- [ ] 28-T%d — %s — %s" % (n, title, _S28_STATUS)) == 1, n


_S28_MUTATIONS = {
    "name disappears": ("roadmap", "**Perception / Edge Inference** — ", "**Computer Vision** — "),
    "status lost": ("checklist", "- [ ] Wireless / RF Connectivity — " + _S28_STATUS,
                    "- [ ] Wireless / RF Connectivity — `RECORDED`"),
    "activation claimed": ("roadmap", "**Wireless / RF Connectivity** — ",
                           "Wireless / RF Connectivity is activated. **Wireless / RF Connectivity** — "),
    "part-eligibility claimed": ("checklist", "- [ ] Perception / Edge Inference — ",
                                 "Perception / Edge Inference: part-eligible. - [ ] Perception / Edge Inference — "),
    "not-live statement dropped": ("checklist", _S28_NONE_LIVE, "they are recorded"),
    "responsibility = component": ("roadmap", _S28_INVARIANT,
                                   "`TECHNICAL RESPONSIBILITY = PHYSICAL COMPONENT ≠ ROOT DOMAIN`"),
    "28-T6 minted": ("roadmap", "**Wireless / RF Connectivity** — ", "**28-T6 — Wireless / RF Connectivity** — "),
    "28-T8 minted": ("checklist", "- [ ] Perception / Edge Inference — ", "- [ ] 28-T8 Perception / Edge Inference — "),
    "Stage 28 globally discharged": ("roadmap", "They do not reopen or globally complete Stage 28",
                                     "Stage 28 is now globally discharged; they complete Stage 28"),
    "IoT absorbs RF": ("roadmap", "IoT (Stage 31) may CONSUME future Wireless / RF truth",
                       "IoT (Stage 31) owns the Wireless / RF truth"),
    "row 31 boundary dropped": ("roadmap", " IoT may CONSUME future Wireless / RF Connectivity truth", " IoT"),
    "Robotics perception owner": ("roadmap", "never to a second Robotics-owned perception authority.\n",
                                  "and Robotics owns perception as its own authority.\n"),
    # ADDED with the cross-cutting Technical Deepening source / IP invariant
    "source rule weakened": ("roadmap", _S28_SOURCE_RULE, "`TECHNICAL DEEPENING SOURCE RULE: ANY PUBLIC SOURCE`"),
    "viewable equals reusable": ("checklist", _S28_VIEWABLE, "`PUBLICLY VIEWABLE = OPENLY REUSABLE`"),
    "free-to-read treated as reusable": ("roadmap", "the controlling principle is lawful reuse, not website "
                                         "accessibility", "free-to-read means reusable"),
    "lawful basis dropped": ("roadmap", "only where an explicit lawful reuse basis is recorded",
                             "that is publicly available"),
    "vendor text ingestion allowed": ("roadmap", "is never ingested into governed technical content unless its "
                                      "license or permission clearly authorizes that use",
                                      "may be ingested into governed technical content freely"),
    "checklist ingestion allowed": ("checklist", "never ingested into governed technical content without a license",
                                    "ingested into governed technical content without a license"),
    "unclear basis filled": ("checklist", _S28_UNCLEAR, "the best available source may still be used"),
    "rule narrowed to Wireless": ("roadmap", "The rule applies proportionally across ALL future Technical Deepening",
                                  "The rule applies only to Wireless / RF Connectivity"),
    "28-T3 dropped from source scope": ("roadmap", "28-T3 Power Electronics, ", ""),
    "checklist scope narrowed": ("checklist", "a cross-cutting invariant for ALL future Technical Deepening",
                                 "a Wireless / RF-only rule"),
}


@pytest.mark.parametrize("name", sorted(_S28_MUTATIONS))
def test_stage28_named_assessment_regressions_are_caught(name):
    doc, old, new = _S28_MUTATIONS[name]
    texts = {"roadmap": _nav._read(ROADMAP), "checklist": _nav._read(CHECKLIST)}
    assert texts[doc].count(old) >= 1, (name, "mutation anchor missing")
    texts[doc] = texts[doc].replace(old, new, 1)
    assert _stage28_named_assessment_problems(texts["roadmap"], texts["checklist"]), name
