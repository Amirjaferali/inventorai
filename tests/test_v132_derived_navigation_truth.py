"""v1.32 derived-navigation truth guards: roadmap + operating checklist.

File: tests/test_v132_derived_navigation_truth.py
Purpose: keep the two DERIVED navigation artifacts —
`docs/governance/INVENTORAI_MASTER_EXECUTION_ROADMAP.md` and
`docs/governance/INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md` — from
regressing into authority, losing their structure, or teaching a successor a
procedure that yields a wrong answer. These are repository doc-invariant
checks in the established convention; no runtime code is involved.
Input contract: run under pytest from the repository root; reads the two
artifacts, plus a repository-wide scan for one withdrawn SHA literal.
Output contract: 45 Stage IDs and 28 tracking IDs survive with no duplicates
and no renumbering; nine groups survive; both artifacts declare themselves
non-authoritative; the scheduler is never described as deployed or activated;
the historical FCORA FAIL and its separate differential clearance both
survive and no FCORA PASS is invented; the live-tip procedure resolves the
fetched authoritative ref rather than trusting local HEAD; no external
engineering provider is named as adopted; and the withdrawn spliced deployed
SHA appears nowhere in the repository.
Prohibited behaviors: MUST NOT weaken to pass; MUST NOT grant either artifact
authority it does not have.

Live truth vs preserved history: the CURRENT-authority guards (the live material
invariants and the current-state guard) enforce material, merge-invariant truth
only. They never require a PR number, merge / head / tree SHA, ancestry chain,
review verdict, post-merge verification result or pre-/post-merge lifecycle
wording: Git/GitHub own that transient identity. An implementation candidate can
therefore carry the durable post-integration truth itself, and a merge alone
never needs a follow-up current-truth PR. Per-delivery "delivered history"
guards may still pin identities that ALREADY exist as preserved history; no
guard may require the identity of a delivery that has not merged yet.
"""
import hashlib
import os
import re
import sys

import pytest

ROADMAP = os.path.join("docs", "governance",
                       "INVENTORAI_MASTER_EXECUTION_ROADMAP.md")
CHECKLIST = os.path.join("docs", "governance",
                         "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md")

# The withdrawn literal is assembled at runtime so that this guard does not
# itself reintroduce the thing it forbids.
_WITHDRAWN_DEPLOYED_SHA = "06bf3632ae9914732e945" + "5965f551955c5d4a8c1"
_REAL_PR663_MERGE = "06bf3632ae9914732e945f00f5ff9f130aea57a0"

# Same reason, same convention: the tracking identifier that was minted without
# authority and withdrawn is assembled at runtime, so the guard forbidding it
# does not put a live copy of it back into the repository it scans.
_UNAUTHORIZED_MINTED_ID = "WATCH-" + "02"


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ==========================================================================
# Structure: 9 groups / 45 stages / 28 tracking IDs
# ==========================================================================
def test_roadmap_preserves_nine_groups():
    groups = re.findall(r"^### Group (\d) — Stages", _read(ROADMAP), re.M)
    assert groups == [str(n) for n in range(1, 10)], groups


def test_roadmap_preserves_forty_five_stage_ids():
    ids = [int(x) for x in
           re.findall(r"^- \[[ x]\] \*\*(\d+) —", _read(ROADMAP), re.M)]
    assert len(ids) == 45, len(ids)
    assert sorted(ids) == list(range(1, 46)), sorted(ids)   # no gaps, no dupes


def test_roadmap_preserves_twenty_eight_tracking_ids():
    section = _read(ROADMAP).split("## 9. Current Master Checklist")[1]
    section = section.split("## 10.")[0]
    ids = [int(x) for x in re.findall(r"^\| *(\d+) \|", section, re.M)]
    assert len(ids) == 28, len(ids)
    assert sorted(ids) == list(range(1, 29)), sorted(ids)


# ==========================================================================
# Neither artifact may become authority
# ==========================================================================
def test_checklist_declares_itself_non_authoritative():
    text = _read(CHECKLIST)
    assert "DERIVED OPERATING CHECKLIST — NOT EXECUTION AUTHORITY" in text
    assert "does not replace Git" in text
    assert "does not replace Owner decisions" in text
    # the hierarchy must place this file at the bottom, not the top
    assert "Git / live repository state" in text
    assert "conflicts resolve upward" in re.sub(r"\s+", " ", text).lower()


def test_roadmap_declares_itself_non_authoritative():
    text = _read(ROADMAP)
    assert "DERIVED NAVIGATION — NOT EXECUTION AUTHORITY" in text
    assert "control and this file is the stale one" in \
        re.sub(r"\s+", " ", text).lower()


# ==========================================================================
# Live-tip procedure: resolve the fetched ref, never trust local HEAD
# ==========================================================================
def test_live_tip_procedure_resolves_the_fetched_authoritative_ref():
    """A successful fetch does not move the checkout.

    The earlier procedure ran `git fetch` and then `git rev-parse HEAD`, which
    reports the local checkout and can silently be reported as the live tip.
    The corrected procedure must resolve the remote-tracking ref explicitly and
    compare it against HEAD.
    """
    text = _read(CHECKLIST)
    branch = "feature/atomic-json-session-persistence"
    assert "git fetch origin %s" % branch in text
    assert "git rev-parse refs/remotes/origin/%s" % branch in text
    assert "git rev-parse refs/remotes/origin/%s^{tree}" % branch in text
    assert "git rev-list --left-right --count" in text
    normalized = re.sub(r"\s+", " ", text)
    assert ("The fetched authoritative ref is the current authority" in
            normalized)
    assert "never report a local HEAD as the live tip" in normalized
    assert "A successful fetch does not change your checkout" in normalized


def test_recorded_baseline_is_not_presented_as_a_permanent_pin():
    normalized = re.sub(r"\s+", " ", _read(CHECKLIST))
    assert ("This is evidence of one moment and is expected to go stale. It is "
            "not a permanent pin" in normalized)


# ==========================================================================
# Truth boundaries that must never collapse
# ==========================================================================
def test_scheduler_never_described_as_deployed_or_activated():
    for path in (ROADMAP, CHECKLIST):
        normalized = re.sub(r"\s+", " ", _read(path))
        assert "NOT DEPLOYED" in normalized, path
        assert "NOT LIVE-ACTIVATED" in normalized, path
        for claim in ("scheduler is deployed", "scheduler is live",
                      "scheduler is running", "scheduled backup is running",
                      "backups run daily"):
            assert claim not in normalized.lower(), (path, claim)


def test_fcora_history_and_clearance_both_survive_without_a_pass():
    for path in (ROADMAP, CHECKLIST):
        normalized = re.sub(r"\s+", " ", _read(path))
        assert "C — FCORA FAIL" in normalized, path
        assert "DIFFERENTIAL RECHECK PASS" in normalized, path
        assert "No FCORA PASS exists" in normalized or \
            "no FCORA PASS exists" in normalized, path


def test_no_external_engineering_provider_named_as_adopted():
    text = _read(ROADMAP).lower()
    for vendor in ("ansys", "solidworks", "matlab", "comsol", "altium",
                   "kicad", "autodesk", "siemens nx", "simulink", "abaqus",
                   "ltspice", "fusion 360"):
        assert vendor not in text, vendor


# ==========================================================================
# Deployed-SHA hygiene: the withdrawn literal stays out of the repository
# ==========================================================================
def test_withdrawn_spliced_deployed_sha_absent_from_repository():
    """The spliced SHA exists nowhere in Git and must not be reintroduced.

    It was relayed once as an exact full deployed SHA, having been formed by
    widening an abbreviated provider identity. Repository identity and provider
    identity are separate evidence classes; a literal produced by mixing them
    is not evidence of anything and is not preserved even as a quotation.
    """
    hits = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs
                   if d not in (".git", "__pycache__", "node_modules")]
        for name in files:
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8") as fh:
                    if _WITHDRAWN_DEPLOYED_SHA in fh.read():
                        hits.append(path)
            except (UnicodeDecodeError, OSError):
                continue
    assert hits == [], hits


def test_repository_merge_sha_is_labeled_as_repository_evidence():
    state = os.path.join("docs", "governance", "CURRENT_PROJECT_STATE.md")
    normalized = re.sub(r"\s+", " ", _read(state))
    assert "**Repository PR #663 merge SHA:** `%s`" % _REAL_PR663_MERGE in normalized
    assert "Provider exact deployed SHA: NOT VERIFIED IN THIS SESSION" in normalized
    assert "Never infer an exact full provider SHA" in normalized


# ==========================================================================
# Stage 7 / T2-G bounded closure (Owner acceptance, 2026-09-20)
#
# These guards exist because closure is exactly where residuals get lost. A
# stage that reads COMPLETED must still carry the obligations its closure did
# NOT discharge, and the preserved residuals must be readable as preserved —
# not merely absent from a list that no longer mentions them.
# ==========================================================================
CONTRACT = os.path.join("docs", "governance", "ACTIVE_INCREMENT_CONTRACT.md")
REGISTER = os.path.join("docs", "governance", "DEFERRED_OBLIGATIONS_REGISTER.md")
CAPABILITIES = os.path.join("docs", "governance",
                            "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md")
STATE = os.path.join("docs", "governance", "CURRENT_PROJECT_STATE.md")


def _flat(path):
    return re.sub(r"\s+", " ", _read(path))


# ==========================================================================
# Current-state blocks
#
# Every CURRENT-state claim in these three documents lives inside a fenced
# block the documents declare themselves:
#
#     <!-- CURRENT-BLOCK: name -->  ...  <!-- END CURRENT-BLOCK: name -->
#
# Guards assert against the fenced block, never against the whole file, and
# preserved history lives OUTSIDE the fences. That separation is the point.
# A file-wide substring sweep is satisfied by any superseded sentence still
# sitting in the document as legitimate history, which is how the routing
# guard in this file was wrong-but-green three times running, and how an
# independent mutation review later showed nineteen more inversions passing:
# the token was always somewhere in the file, just not where it mattered.
# ==========================================================================
CURRENT_BLOCKS = ("current-routing", "stages-13-16-dependencies",
                  "stage-17-disposition", "stage-18-semantic-normalization",
                  "d3-fk-hardening", "material-residuals")

_OPEN = "<!-- CURRENT-BLOCK: %s -->"
_CLOSE = "<!-- END CURRENT-BLOCK: %s -->"

# Markers that identify preserved history. None may appear inside a fence.
_HISTORY_MARKERS = ("Superseded wording, preserved", "SUPERSEDED 20",
                    "preserved verbatim", "Prior line, preserved",
                    "Superseded 20")


def _current(path, name):
    """The whitespace-flattened text of ONE fenced current-state block."""
    raw = _read(path)
    o, c = _OPEN % name, _CLOSE % name
    assert raw.count(o) == 1, (path, name, "open fence not unique")
    assert raw.count(c) == 1, (path, name, "close fence not unique")
    i = raw.index(o) + len(o)
    j = raw.index(c, i)
    return re.sub(r"\s+", " ", raw[i:j])


def _surfaces(name):
    """(path, current block) for all three routing surfaces."""
    return tuple((path, _current(path, name))
                 for path in (ROADMAP, CHECKLIST, CONTRACT))


def _needs(block, path, label, *patterns):
    """Every pattern must be present, case-sensitively, in this block."""
    for pat in patterns:
        assert re.search(pat, block, re.S), (path, label, "MISSING", pat)


def _rejects(block, path, label, *patterns):
    """No pattern may appear. This is what catches a REVERSAL, as opposed to
    a deletion: negating a safeguard in place leaves every token intact."""
    for pat in patterns:
        m = re.search(pat, block, re.I | re.S)
        assert m is None, (path, label, "FORBIDDEN", pat, m.group(0))


def _only_negated(block, path, term, negators=("no ", "not ", "never ")):
    """Every occurrence of `term` must be negated where it stands.

    "no SQLite trigger" and "a SQLite trigger is required" contain the same
    token; only the words in front of it carry the rule.
    """
    for m in re.finditer(re.escape(term), block, re.I):
        lead = block[max(0, m.start() - 12):m.start()].lower()
        assert any(n in lead for n in negators), (
            path, term, "NOT NEGATED", block[max(0, m.start() - 40):m.end()])


def _roadmap_section(heading):
    """One roadmap `### ` section, whitespace-flattened."""
    raw = _read(ROADMAP)
    start = raw.index("### " + heading)
    end = raw.find("\n### ", start + 1)
    return re.sub(r"\s+", " ", raw[start:len(raw) if end == -1 else end])


def test_stage_seven_reads_completed_within_its_bounded_scope():
    roadmap = _flat(ROADMAP)
    assert "STAGE 7 / T2-G: COMPLETED \u2705 WITHIN ITS BOUNDED T2-G SCOPE." in roadmap
    # the stage checkbox itself must be ticked, not merely described
    assert re.search(r"^- \[x\] \*\*7 — T2-G:\*\*",
                     _read(ROADMAP), re.M), "stage 7 checkbox not ticked"
    assert "STAGE 7 / T2-G: COMPLETED WITHIN ITS BOUNDED T2-G SCOPE." in _flat(CONTRACT)


def test_bounded_closure_is_never_stated_as_full_capability():
    """Closing a bounded slice is not delivering the capability."""
    for path in (ROADMAP, REGISTER):
        flat = _flat(path).lower()
        assert "not full semantic-adaptivity capability" in flat or \
            "capability not complete" in flat, path
    for claim in ("t2-g is complete", "t2-g capability complete",
                  "semantic adaptive questioning is complete",
                  "full t2-g capability delivered"):
        for path in (ROADMAP, CHECKLIST, CONTRACT, REGISTER):
            assert claim not in _flat(path).lower(), (path, claim)


def test_n1_and_n2_read_satisfied_in_the_authority_not_only_the_navigation():
    contract = _flat(CONTRACT)
    assert "`N-1` single-sentence mixed answers vetoed | **SATISFIED**" in contract
    assert "`N-2` terse genuine explanations missed | **SATISFIED**" in contract


def test_r1_r2_r3_are_preserved_and_never_silently_dropped():
    """Each must remain findable AND be labeled preserved, in the register
    that owns them and in the derived navigation that routes to them."""
    register = _flat(REGISTER)
    for rid in ("`R1`", "`R2`", "`R3`"):
        assert rid in register, rid
    assert "PRESERVED AS SEPARATE FUTURE RESIDUALS" in register
    assert "PRESERVED at its own applicable gate" in register
    # closure must not be described as discharging them
    for path in (ROADMAP, CHECKLIST, CONTRACT, REGISTER):
        flat = _flat(path)
        for claim in ("R1 is closed", "R2 is closed", "R3 is closed",
                      "R1/R2/R3 closed", "R1, R2 and R3 are discharged"):
            assert claim not in flat, (path, claim)
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        assert "Preserved, not discharged" in _flat(path) or \
            "PRESERVED, NOT DISCHARGED" in _flat(path), path


def test_n3_through_n6_keep_their_triggers():
    for path in (CONTRACT, REGISTER):
        flat = _flat(path)
        assert "`N-3`\u2013`N-6`" in flat or "`N-3`-`N-6`" in flat, path


def test_legacy_migration_is_closed_under_explicit_adoption_only():
    register = _flat(REGISTER)
    assert "**CLOSED / SATISFIED \u2014 2026-09-20 Owner Stage 7 closure acceptance.**" in register
    assert "Policy B \u2014 EXPLICIT CONFIRMED MIGRATION is preserved" in register
    # the rejected alternative must stay rejected wherever closure is stated
    for path in (CONTRACT, ROADMAP, REGISTER):
        flat = _flat(path).lower()
        assert "automatic migration on open" in flat, path
        assert "rejected" in flat, path
    for claim in ("projects are migrated automatically",
                  "migration runs on open", "all projects now run the current rules"):
        for path in (ROADMAP, CHECKLIST, CONTRACT, REGISTER):
            assert claim not in _flat(path).lower(), (path, claim)


def test_the_arabic_contrast_observation_is_recorded_without_a_new_lifecycle():
    """`ولكن` is a disclosed non-blocking observation, not a new obligation.

    It must be findable in governance (the source already disclosed it), must
    state its safe failure direction, and must not acquire a row, gate or
    return trigger of its own.
    """
    prefixed = "\u0648\u0644\u0643\u0646"
    register = _flat(REGISTER)
    contract = _flat(CONTRACT)
    assert prefixed in register and prefixed in contract
    for flat in (register, contract):
        assert "under-progress on a true answer" in flat
        assert "never unearned support" in flat
    # no separate lifecycle
    assert "not a repair obligation" in contract.lower()
    assert "not a gate" in contract.lower()
    # and it must not have been implemented under a documentation authorization
    with open(os.path.join("engine", "answer_stance.py"), encoding="utf-8") as fh:
        stance = fh.read()
    assert '_T2G2_CONTRAST_AR = ("\u0644\u0643\u0646", "\u0644\u0643\u0646\u0651")' in stance, (
        "the Arabic contrast vocabulary must be unchanged by a documentation cut")


def test_every_surface_declares_the_same_current_state_blocks():
    """The fences are themselves part of the contract.

    A guard scoped to a block is only as good as the block boundary, so the
    boundaries are asserted first: all three surfaces declare the same set,
    every fence is balanced, and — the load-bearing half — NO preserved-history
    marker may sit inside a fence. That invariant is what makes every guard
    below mean "the CURRENT document says this", rather than "the token exists
    somewhere in 1500 lines of preserved amendments".
    """
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        raw = _read(path)
        opened = re.findall(r"<!-- CURRENT-BLOCK: (\S+) -->", raw)
        closed = re.findall(r"<!-- END CURRENT-BLOCK: (\S+) -->", raw)
        assert opened == closed, (path, opened, closed)
        assert sorted(opened) == sorted(CURRENT_BLOCKS), (path, opened)
        for name in CURRENT_BLOCKS:
            body = _current(path, name)
            assert body.strip(), (path, name, "empty current block")
            for marker in _HISTORY_MARKERS:
                assert marker not in body, (path, name, "history inside fence",
                                            marker)


def test_stage_eighteen_is_complete_for_the_current_scope_and_routing_past_completes_nothing():
    """The CURRENT routing, asserted where preserved history cannot reach it.

    This guard has been wrong-but-green four times, and the shape never
    changed: it asserted a routing sentence that was still in the documents as
    legitimate preserved history, so closing the stage it named left the
    assertion passing while it pointed at the wrong stage. "Stage 8" after
    Stage 8 closed, "Stage 9" after the Stage-9 disposition, "Stage 10" after
    the Stage-10 differential, and most recently a live checklist sentence
    still calling Stage 11 next while the current-position area routed to 18.

    A fifth variant of the same failure is now closed here. The Owner
    authorized ONE bounded first CAP-01 increment, which makes "Stage 18 is the
    NEXT executable stage" and "`STAGE 18 STARTED: NO`" false as present truth
    while both sentences remain legitimate preserved history a few lines below
    the fence. So the guard flips with the fact: entry is required, the stale
    pre-authorization wording is forbidden INSIDE the fence, and the two claims
    that entry does NOT license — stage completion and full CAP-01/STG — are
    required to stay explicitly denied. One authorized slice is not the stage.

    Stage 11 is asserted unchanged for a reason that matters: it was routed
    PAST, not completed. Routing forward must never read as a discharge, and
    entering Stage 18 discharges nothing behind it either.
    """
    # AMENDED at the Stage 18 closure (2026-10-01): the guard flips with the fact once more. Stage 18 is
    # COMPLETE for the current Mechanical + Electrical / Electronics scope only, the sequential marker is
    # Stage 19 for navigation only, and routing past Stages 11, 13, 14, 16 and 17 completes none of them.
    # AMENDED at the Stage 19 closure (2026-10-01): the marker is Stage 20 for navigation only; the Stage-18
    # closure's own token survives as true history in its delivered record.
    # AMENDED at the Stage 20 closure (2026-10-01): the marker is Stage 21 for navigation only; the Stage-19
    # closure's own `NO STAGE-20 …` token survives as true history in its delivered record.
    # AMENDED at the Stage 21 closure (2026-10-01): the marker was Stage 22 for navigation only.
    # AMENDED at the Stage 22 closure (2026-10-01): the marker is Stage 23 (NOT ENTERED) for navigation only; the
    # Stage-21 closure's own `NO STAGE-22 …` token survives as true history in its delivered record.
    # AMENDED at the Stage 23 closure (2026-10-02): the marker is Stage 24 (NOT ENTERED) for navigation only and
    # Stage 23 is COMPLETE for its bounded four-axis scope; the Stage-22 closure's `NO STAGE-23 …` stays history.
    # AMENDED at the Stage 24 closure (2026-10-04): the marker is Stage 25 (NOT ENTERED) for navigation only and
    # Stage 24 is COMPLETE for its bounded CAP-12 Form Mock-up Advisory Slice 1 scope; the Stage-23 closure's
    # `NO STAGE-24 …` stays history in its delivered record.
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "routing",
               r"(?i)CURRENT MASTER ROADMAP STAGE: Stage 25",
               re.escape(_S24_COMPLETE), re.escape(_NO_S25),
               re.escape(_S23_COMPLETE), re.escape(_NO_S24),
               re.escape("`STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE + DECISION ROOM SCOPE`"),
               re.escape("`NO STAGE-23 IMPLEMENTATION AUTHORIZED BY STAGE-22 CLOSURE`"),
               re.escape("`STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE`"),
               re.escape("`NO STAGE-22 IMPLEMENTATION AUTHORIZED BY STAGE-21 CLOSURE`"),
               re.escape("`STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE`"),
               re.escape("`NO STAGE-21 IMPLEMENTATION AUTHORIZED BY STAGE-20 CLOSURE`"),
               re.escape("`STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE`"),
               re.escape("`NO STAGE-20 IMPLEMENTATION AUTHORIZED BY STAGE-19 CLOSURE`"),
               re.escape("`STAGE 18: COMPLETE — CURRENT MECHANICAL + ELECTRICAL / ELECTRONICS SCOPE`"),
               re.escape("`NO STAGE-19 IMPLEMENTATION AUTHORIZED BY STAGE-18 CLOSURE`"),
               # ROTATED at the Stage 16 closure: Stage 16 is COMPLETE for its bounded scope and no longer routed past
               r"routing past Stages 11, 13, 14 and 17 completes none of them",
               r"`FIRST BOUNDED CAP-01 INCREMENT: OWNER-AUTHORIZED`",
               r"FULL CAP-01 / FULL STG:\s*NOT\s+AUTHORIZED",
               r"`D13 RESEARCH: REMAINS CLOSED`",
               # AMENDED at the Stage 22 closure: no routed stage is ENTERED / unticked any more; the last one
               # (Stage 22) is ticked for its bounded scope only, and that scope limit must stay stated
               r"the Stage-22 checkbox is ticked for the current bounded decision trace \+ decision room scope only",
               r"`STAGE 11 STARTED: NO`",
               r"Stage 11[^.]{0,200}DEFERRED",
               r"routed\s+PAST, not completed",
               r"routing past a deferred stage never completes it")
        _rejects(routing, path, "routing",
                 r"Stage 11[^.]{0,80}\bis the next\b",
                 r"next Master Roadmap stage: Stage 11",
                 r"STAGE 11 STARTED: YES",
                 # the pre-authorization wording is history now, not current text
                 r"STAGE 18 STARTED: NO",
                 r"Stage 18 is `NOT AUTHORIZED FOR IMPLEMENTATION`",
                 # entry is not completion, and the slice is not the capability
                 r"STAGE 18 COMPLETE: YES", r"`STAGE 18 COMPLETE: NO`",
                 # tight on purpose: "entering Stage 18 is not the next
                 # obligation discharged" is TRUE and must stay sayable, so the
                 # forbidden shape is the predicate, not the bare co-occurrence;
                 # only the scoped completion is true
                 r"Stage 18\s+(is|was|has been)\s+(COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b"
                 r"(?!\s+for\s+the\s+current\s+Mechanical)",
                 r"Stage 18[^.]{0,30}\bmarked (complete|completed|closed)\b",
                 r"FULL (CAP-01|STG)[^.]{0,40}: *AUTHORIZED",
                 r"D13 RESEARCH: (REOPENED|OPEN)",
                 r"Stage 11[^.]{0,80}\b(COMPLETED|DISCHARGED|CLOSED)\b")
    # every surviving "Stage N is next" sentence, for every already-routed-past
    # stage, must be marked superseded — in the navigation AND in the authority.
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        flat = _flat(path)
        for stale in ("Next Master Roadmap stage: Stage 7",
                      "Next Master Roadmap stage: Stage 8",
                      "Next Master Roadmap stage: Stage 9",
                      "Next Master Roadmap stage: Stage 10",
                      "Next Master Roadmap stage: Stage 11",
                      "is the next Master Roadmap stage"):
            for match in re.finditer(re.escape(stale), flat):
                window = flat[max(0, match.start() - 600):match.start()]
                assert "SUPERSEDED" in window.upper(), (
                    "a live sentence still routes to a routed-past stage in %s: %s"
                    % (path, stale))
    # completing or dispositioning one stage never starts the next. Stage 18 is
    # now ENTERED, so the live subtask line must name the ONE authorized bounded
    # increment AND keep the wider scope gated — "entered" is not "open season".
    flat_checklist = _flat(CHECKLIST)
    assert "ONE Owner-authorized bounded Stage-18 / CAP-01 first guidance" in flat_checklist
    assert "every wider CAP-01/STG scope still does" in flat_checklist
    assert "Stage 11 still requires its own explicit mandate" in flat_checklist
    assert "completing the Stage-17 product-depth work" in flat_checklist
    # and neither stage's checkbox has been ticked by routing
    assert re.search(r"^- \[ \] \*\*11 — T1-C′/A2 human evidence:",
                     _read(ROADMAP), re.M), "stage 11 checkbox is not empty"
    # Stage 18's checkbox is ticked for the current Mechanical + Electrical / Electronics scope only
    assert re.search(r"^- \[x\] \*\*18 — D13/CAP-01 guidance:",
                     _read(ROADMAP), re.M), "stage 18 checkbox is not ticked"


# The safeguard set, as one canonical run. Asserting the whole run at once is
# what catches a NEGATION: "no shadow-first operation" keeps every token and
# breaks the sequence. Asserting the items individually would not.
SAFEGUARD_RUN = (
    "shadow-first operation \u00b7 pinned model / version \u00b7 confidence boundary \u00b7 "
    "fail-closed behaviour \u00b7 deterministic fallback \u00b7 provider-neutral architecture \u00b7 "
    "no automatic concept creation \u00b7 the model is NEVER the final decision owner \u00b7 "
    "no automatic readiness promotion \u00b7 no unsupported engineering conclusion \u00b7 "
    "AUDITABILITY / PROVENANCE \u00b7 PRIVACY / DATA BOUNDARY")

_ARROW = "\u2192"
PROVENANCE_CHAIN = ("source input %s normalization proposal %s selected canonical concept"
                    % (_ARROW, _ARROW))


def test_the_stage_eighteen_semantic_normalization_note_survives_routing():
    """The carried note, asserted as MEANING rather than as vocabulary.

    An independent mutation review showed the previous version of this guard
    staying green while the note was flipped to AUTHORIZED, while shadow-first
    was negated in place, while the privacy duty became "need not determine",
    and while the auditability and privacy paragraphs were reduced to their
    own labels. Every one of those keeps the words and reverses the rule,
    which is why presence checks cannot be the whole contract.

    So: the status line is asserted as a line, the safeguards as one
    uninterrupted run, both material safeguards as their operative sentences,
    and the reversals are forbidden by name.
    """
    for path, note in _surfaces("stage-18-semantic-normalization"):
        _needs(note, path, "semantic-normalization",
               # PRESERVED / NOT AUTHORIZED / NOT IMPLEMENTED, as one statement
               r"PRESERVED[^.]{0,40}[\u00b7/]\s*NOT AUTHORIZED\s*[\u00b7/]\s*NOT IMPLEMENTED",
               r"BEGINNING of Stage 18",
               re.escape(SAFEGUARD_RUN),
               # auditability/provenance, as substance
               r"Where privacy permits, preserve enough attributable",
               re.escape(PROVENANCE_CHAIN),
               # privacy/data boundary, as an obligation
               r"Before ANY external model/provider integration",
               r"must determine",
               r"may be transmitted outside\s+InventorAI",
               r"privacy, security and retention boundary",
               # preservation only
               r"no provider is selected",
               r"no provider is integrated",
               r"no live privacy policy is defined here")
        _rejects(note, path, "semantic-normalization",
                 # status reversal
                 r"LAYER:?\s*(PRESERVED\s*[\u00b7/]\s*)?AUTHORIZED\b",
                 r"\bIS AUTHORIZED\b", r"\b(NOW|ALREADY) IMPLEMENTED\b",
                 r"IMPLEMENTATION AUTHORIZED: YES",
                 # safeguard reversal
                 r"\bno[t]? shadow-first",
                 r"\bno[t]? pinned model",
                 r"\bno[t]? fail-closed",
                 r"\bno[t]? deterministic fallback",
                 r"\bnot provider-neutral",
                 r"automatic concept creation is (allowed|permitted)",
                 r"automatic readiness promotion is (allowed|permitted)",
                 # decision ownership reversal
                 r"provider may decide",
                 r"(model|provider) (is|becomes) the final decision owner",
                 # privacy duty reversal
                 r"need not determine", r"is not required to determine",
                 r"may determine whether")


# The parts of this module split into their own files for CI shard balance stay inside the scan below.
_SPLIT_FILES = tuple(os.path.join(os.path.dirname(__file__), "test_v132_derived_navigation_truth_%s.py" % part)
                     for part in ("live_truth_reversals", "live_truth_reversals_continued",
                                  "authority_and_stage28_proofs"))


def test_the_carried_stage_18_note_carries_no_tracking_identifier():
    """A tracking identifier is GRANTED, not assumed by whoever writes it up.

    The Owner handover preserved the multilingual semantic-normalization
    concept and assigned it no ID. One was minted anyway, withdrawn on review,
    and a mutation then showed a DIFFERENT synthetic identifier sliding in
    unnoticed — forbidding one literal proves nothing about the next one.

    So this is a positive contract instead: the carried note is titled by an
    exact approved descriptive heading, with no identifier attached at either
    end, and no identifier-shaped token may appear in that title at all.
    """
    approved = ("Carried into Stage 18 \u2014 Multilingual Semantic Normalization "
                "Layer")
    # the roadmap records it as a heading, and the heading must match exactly
    roadmap_note = _current(ROADMAP, "stage-18-semantic-normalization")
    m = re.match(r"\s*### (.+?)\s+\*\*PRESERVED", roadmap_note)
    assert m, roadmap_note[:160]
    assert m.group(1) == approved, m.group(1)
    # the derived surfaces record it as a bold lead-in label, same rule
    for path in (CHECKLIST, CONTRACT):
        note = _current(path, "stage-18-semantic-normalization")
        m = re.search(r"\*\*(CARRIED INTO STAGE 18 [^*:]*):", note)
        assert m, (path, note[:160])
        label = m.group(1).strip()
        assert label == ("CARRIED INTO STAGE 18 \u2014 MULTILINGUAL SEMANTIC "
                         "NORMALIZATION LAYER"), (path, label)
    # ...and nothing identifier-shaped anywhere in any of those titles
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        note = _current(path, "stage-18-semantic-normalization")
        title = note[:note.index("PRESERVED")]
        bad = re.search(r"\b[A-Z][A-Z0-9]{1,9}-\d+\b", title)
        assert bad is None, (path, "identifier minted in the title",
                             bad.group(0) if bad else None)
    # the withdrawn literal stays gone, and the two authorized WATCH IDs stay
    for path in (ROADMAP, CHECKLIST, CONTRACT, __file__, *_SPLIT_FILES):
        assert _UNAUTHORIZED_MINTED_ID not in _read(path), path
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        minted = set(re.findall(r"WATCH-\d+", _read(path)))
        assert minted == {"WATCH-01", "WATCH-04"}, (path, sorted(minted))


def _stage_deps(path):
    """The Stages 13–16 block, split into one entry PER STAGE.

    Scoping per stage is what makes a SWAP fail: moving Stage 14's
    dependencies under Stage 15 keeps every token in the block and changes
    what the document says about both stages.
    """
    block = _current(path, "stages-13-16-dependencies")
    out = {}
    for part in re.split(r"(?=STAGE 1[3-6] \u2014)", block):
        m = re.match(r"STAGE (1[3-6]) \u2014", part)
        if m:
            out[int(m.group(1))] = part
    return out


def test_stages_thirteen_to_sixteen_keep_their_own_dependencies():
    """Four stages, four dependency sets — not one shared blocker.

    Collapsing them onto T2-E reads as though a single unblock would clear all
    four. It would not, and a successor trusting that summary works the wrong
    dependency for a quarter. Each stage is therefore asserted inside its own
    slice, and each slice forbids the OTHER stages' dependencies, so a swap is
    caught from both directions.
    """
    for path, block in _surfaces("stages-13-16-dependencies"):
        _needs(block, path, "13-16",
               r"(?i)T2-E is NOT the sole dependency of all four")
        deps = _stage_deps(path)
        assert sorted(deps) == [13, 14, 15, 16], (path, sorted(deps))

        _needs(deps[13], path, "stage 13",
               r"PARTIAL / DEFERRED",
               r"Technical evidence-sufficiency exists",
               r"T2-E", r"INSUFFICIENT_EVIDENCE")
        _rejects(deps[13], path, "stage 13",
                 r"CAP-12", r"WS-PFV-001", r"Phase[- ]7")

        _needs(deps[14], path, "stage 14",
               r"PARTIAL / DEFERRED",
               r"CAP-12", r"CAP-13", r"WS-PFV-001", r"T2-E")
        _rejects(deps[14], path, "stage 14",
                 r"Phase[- ]7", r"inbound/write-import")

        # Stage 15 (2026-10-01): entered through bounded slices (Slice 1 DELIVERED, PR #718) and COMPLETE
        # for the current Mechanical + Electrical / Electronics scope through the closure; the Phase-7
        # residuals stay recorded as Phase-7 dependencies, never discharged by the closure.
        _needs(deps[15], path, "stage 15",
               r"COMPLETE FOR THE CURRENT MECHANICAL \+ ELECTRICAL / ELECTRONICS SCOPE \(2026-10-01\)",
               r"Integrated Invention Entry & Durable Subsystem Composition Slice 1 is DELIVERED — PR #718 "
               r"— merge `3f3546a279c7f7020744bcbfee957de84ac2e136`\*\* \(post-merge identity / content "
               r"verification PASS",
               r"no IRL level, no complete integration readiness",
               r"Integration Evidence & IRL-Compatible View Closure are DELIVERED",
               r"it claims no IRL level or score, no validated integration and no\s+engineering compatibility",
               r"D4 stays the future compatibility gate",
               r"no N-domain or arbitrary-domain\s+integration is claimed",
               r"Phase-7 residuals remain Phase 7 and are NOT discharged here",
               r"wider interface/dependency evidence\*\* \(validated subsystem/interface\s+integration evidence "
               r"beyond the delivered scope\)",
               r"beyond the\s+delivered bounded\s+Mechanical \+ Electrical / Electronics use case",
               r"Phase[- ]7 integration/interface foundation",
               r"(?i)EXISTS",
               r"IRL ownership is NOT wholly absent",
               r"per-project integration evidence",
               r"durable subsystem identity",
               r"inbound/write-import",
               r"async/vendor integration",
               r"T2-E")
        _rejects(deps[15], path, "stage 15",
                 r"PARTIAL / DEFERRED", r"IMPLEMENTED CANDIDATE", r"PR PENDING",
                 r"(?<!no )(?<!not )engineering compatibility (is |was )?(established|confirmed|proven)",
                 r"ENTERED / PARTIAL / NOT COMPLETE THROUGH ONE BOUNDED SLICE",
                 r"(?i)wider Stage-15 work remains DEFERRED",
                 r"STAGE 15 — [^.]{0,40}: (?:ENTERED / )?COMPLETE\b(?! FOR THE CURRENT MECHANICAL)",
                 r"STAGE 15 — COMPLETE\b(?! FOR THE CURRENT MECHANICAL)",
                 r"(?<!no )(?<!not )\bIRL level \d",
                 r"(?<!no )(?<!not )full IRL (capability )?(is |was )?(authorized|complete|delivered)",
                 r"CAP-12", r"CAP-13", r"WS-PFV-001",
                 r"foundation (is |does not |)(absent|missing)",
                 r"no IRL ownership",
                 r"IRL ownership is wholly absent",
                 r"ownership (is|remains) absent")

        # ROTATED at the Stage 16 closure (2026-10-06): Stage 16 is COMPLETE for the current bounded Technical +
        # Integration evidence-sufficiency composition scope only; its own dependencies stay recorded for any future
        # level-based or validated SRL composition, which stays NOT AUTHORIZED; the DEFERRED status survives only in the
        # superseded note, and Stages 13 and 14 above stay PARTIAL / DEFERRED.
        live16 = _live_only(deps[16])
        _needs(live16, path, "stage 16",
               r"COMPLETE FOR THE CURRENT BOUNDED TECHNICAL \+ INTEGRATION EVIDENCE-SUFFICIENCY COMPOSITION SCOPE ONLY "
               r"\(2026-10-06\)",
               _tok(_S16_COMPLETE), _tok(_S16C_DELIVERED), _tok(_S16_SRL_NO),
               r"Stage 13 technical measurement",
               r"Stage 15 integration axis",
               r"independently visible and never aggregated",
               r"PR #\d+",
               r"Stage 14 is relevant IF manufacturing participates",
               r"needs its own later evidence and authorization")
        _rejects(live16, path, "stage 16",
                 r"DEFERRED", r"PARTIAL", r"CAP-12", r"WS-PFV-001", r"Phase[- ]7",
                 r"(?<!no )(?<!NO )\bSRL (?:level|score) (?:\d|is\b)", r"weakest[- ]axis (?:is|was) (?:computed|identified)")
        assert re.search(r"\*\(Superseded 2026-10-06 by the Stage 16 closure, preserved so the change is visible rather "
                         r"than silent: this block (?:read|recorded) [^)]*Stage 16 as (?:SRL-compatible composition )?"
                         r"DEFERRED", _after_fence(path, "stages-13-16-dependencies")), path


def test_the_d3_fk_hardening_note_survives_with_its_conditions():
    """The FK note, asserted as operative direction rather than vocabulary.

    A mutation review showed the previous guard green while the SQLite trigger
    became required, legacy-migration compatibility was deleted, defence-in-
    depth retention was reversed and fresh/migrated parity disappeared. Each
    of those keeps the words "SQLite trigger", "legacy", "owner/store" in the
    file and reverses what the note actually says.

    So both escape conditions, both prohibitions, every at-adoption duty and
    the one preserved possibility are asserted in the block, the trigger term
    is required to be negated wherever it appears, and the reversals are
    forbidden by name.
    """
    for path, fk in _surfaces("d3-fk-hardening"):
        _needs(fk, path, "fk",
               # current enforcement, and that it is EQUAL across databases
               r"(?i)owner/store",
               r"(?i)fresh and migrated",
               r"(?i)(SAME effective owner/store enforcement|"
               r"applied identically on fresh and migrated)",
               # the two prohibitions
               r"(?i)no fresh-only",
               r"(?i)no unequal",
               r"(?i)no SQLite trigger",
               # the two escape conditions, both of them
               r"(?i)safely rebuil(t|d)",
               r"(?i)(ALL existing databases|for \*\*ALL\*\*)",
               r"PostgreSQL",
               # the at-adoption duties
               r"(?i)preserve all existing rows",
               r"(?i)preserve D1 lifecycle semantics",
               r"(?i)preserve D2 quantitative semantics",
               r"(?i)preserve D3 linkage semantics",
               r"(?i)legacy migration compatibility",
               r"(?i)retain owner/store validation as defence-in-depth",
               # the preserved possibility, with the boundary that keeps it one
               r"POSSIBLE FUTURE DEFENSE-IN-DEPTH: automated integrity audit",
               r"DO NOT BUILD IT NOW SOLELY BECAUSE IT IS POSSIBLE",
               r"not a new implementation mandate")
        _rejects(fk, path, "fk",
                 r"SQLite trigger (is|are) required",
                 r"(add|introduce)e?s? a SQLite trigger",
                 r"SQLite trigger (must|should|shall) be added",
                 r"fresh-only (FK|foreign key) (is|may be) (added|permitted|allowed)",
                 r"(drop|remove|discard|no longer retain) owner/store",
                 r"owner/store validation (may|can) be (removed|dropped)",
                 r"owner/store validation is (replaced|superseded)",
                 r"(build|implement) (the |an )?automated integrity audit now")
        # "no SQLite trigger" and "a SQLite trigger is required" share a token;
        # only the words in front of it carry the rule.
        _only_negated(fk, path, "SQLite trigger")
        _only_negated(fk, path, "fresh-only")
    # the roadmap also states that enforcement moved rather than vanished
    assert "Enforcement is relocated, not absent." in _current(
        ROADMAP, "d3-fk-hardening")


# Each residual, with the disposition that IS the residual. A name kept beside
# a changed disposition is the same loss as a deleted name, so both halves are
# asserted, and the contradicting dispositions are forbidden in the same clause.
RESIDUALS = (
    ("T1-A\u2032", r"\*\*T1-A\u2032\*\*", r"OPEN",
     r"\b(CLOSED|DISCHARGED|PASSED|COMPLETED)\b"),
    ("RUN-004", r"\*\*RUN-004\*\*", r"NOT AUTHORIZED", r"\b(APPROVED|PERMITTED)\b"),
    ("T2-C\u2032", r"\*\*T2-C\u2032\*\*", r"PARTIAL", r"\b(CLOSED|COMPLETE|PASS)\b"),
    ("real user value", r"\*\*REAL USER VALUE\*\*", r"UNEVIDENCED",
     r"\b(VALIDATED|PROVEN|EVIDENCED\b(?<!UNEVIDENCED))"),
    ("product differentiation", r"\*\*PRODUCT DIFFERENTIATION\*\*", r"UNEVIDENCED",
     r"\b(VALIDATED|PROVEN)\b"),
    ("Stage 11 / T1-C\u2032 / A2", r"\*\*Stage 11 / `T1-C\u2032` / A2\*\*",
     r"DEFERRED / NOT STARTED", r"\b(COMPLETED|DISCHARGED)\b"),
    ("CEHR", r"\*\*CEHR\*\*", r"DEFERRED, NOT CANCELLED", r"\b(CLOSED|DISCHARGED)\b"),
    ("Route-B", r"\*\*Route-B\*\*", r"PRESERVED",
     r"\b(CLOSED|CANCELLED|DISCHARGED)\b"),
    ("G-4-A", r"\*\*G-4-A\*\*", r"CURRENT / NOT FIXED", r"\bNOW FIXED\b"),
    ("G-4-B", r"\*\*G-4-B Mechanism B\*\*", r"DEFERRED",
     r"\b(CLOSED|COMPLETED|FIXED)\b"),
    ("HICR", r"\*\*HICR\*\*", r"PRESERVED", r"\b(CLOSED|CANCELLED|DISCHARGED)\b"),
    ("PRE-FCORA", r"\*\*PRE-FCORA\*\*", r"PRESERVED",
     r"\b(CLOSED|CANCELLED|DISCHARGED)\b"),
    ("T2-A", r"\*\*T2-A random-skip debt\*\*", r"PRESERVED",
     r"\b(CLOSED|DISCHARGED)\b"),
    ("T2-D", r"\*\*T2-D observations\*\*", r"PRESERVED", r"\b(CLOSED|DISCHARGED)\b"),
    ("PR #640", r"\*\*PR #640 findings\*\*", r"PRESERVED",
     r"\b(CLOSED|DISCHARGED)\b"),
    ("N-3\u2013N-6", r"\*\*`N-3`\u2013`N-6`\*\*", r"PRESERVED",
     r"\b(CLOSED|DISCHARGED)\b"),
    ("Stages 13\u201316", r"\*\*Stages 13\u201316\*\*", r"PRESERVED",
     r"\b(DISCHARGED|CLOSED)\b"),
    ("readiness ceiling", r"\*\*READINESS CEILING\*\*",
     r"INSUFFICIENT_EVIDENCE.{0,120}NOT\s+CURRENTLY AUTHORIZED",
     r"\b(PASS|PROMOTED|SUFFICIENT_EVIDENCE)\b"),
    ("deployment", r"\*\*DEPLOYMENT\*\*", r"NOT AUTHORIZED", r"\bAPPROVED\b"),
    ("public release", r"\*\*PUBLIC RELEASE\*\*", r"NOT AUTHORIZED", r"\bAPPROVED\b"),
    ("paid activation", r"\*\*PAID ACTIVATION\*\*", r"NOT AUTHORIZED", r"\bAPPROVED\b"),
    ("Stage 44", r"\*\*Stage 44 lineage gate\*\*", r"PRESERVED",
     r"\b(CLOSED|DISCHARGED|SATISFIED)\b"),
    ("Stage 45", r"\*\*Stage 45 deployment gate\*\*", r"PRESERVED",
     r"\b(CLOSED|DISCHARGED|SATISFIED)\b"),
    ("WATCH-01", r"\*\*WATCH-01\b[^*]*\*\*", r"NOT YET IMPLEMENTED",
     r"\b(IMPLEMENTED\b(?<!NOT YET IMPLEMENTED)|DELIVERED|BUILT)"),
    ("WATCH-04", r"\*\*WATCH-04\b[^*]*\*\*", r"PRESERVED",
     r"\b(RETIRED|CLOSED|SUPERSEDED)\b"),
)


def _residual_clauses(path):
    """The residual block, split into one clause per residual.

    The roadmap writes them as list items and the derived surfaces as a
    mid-dot run; both split cleanly, and splitting is what keeps one
    residual's disposition from vouching for its neighbour's.
    """
    block = _current(path, "material-residuals")
    parts = re.split(r"\s+\u00b7\s+|\s+-\s+(?=\*\*)", block)
    return [c for c in parts if c.strip()]


def test_no_material_residual_is_silently_discharged():
    """Every residual keeps BOTH its name and its disposition.

    The earlier version of this guard checked names inside a fixed 2000-
    character window. A mutation review then flipped CEHR to cancelled,
    Route-B to closed and WATCH-01 to implemented, and deleted HICR outright,
    with the suite staying green: the names were all still there, and the
    window was an arbitrary boundary rather than the block's own.

    So the block is parsed at its declared fence, split per residual, and each
    one must carry its accepted disposition in its OWN clause while the
    contradicting dispositions are forbidden there.
    """
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        clauses = _residual_clauses(path)
        for label, name_pat, required, forbidden in RESIDUALS:
            owned = [c for c in clauses if re.search(name_pat, c)]
            assert owned, (path, label, "residual name is gone")
            assert any(re.search(required, c, re.S) for c in owned), (
                path, label, "disposition lost", owned[:1])
            for c in owned:
                m = re.search(forbidden, c)
                assert m is None, (path, label, "disposition contradicted",
                                   m.group(0), c[:160])


def test_stage_seventeen_product_depth_is_not_commercial_readiness():
    """The full accepted Stage-17 conjunction, not any one half of it.

    A mutation review showed the previous guard green while the commercial
    conclusion flipped to YES, while readiness read COMPLETE, while depth read
    SHALLOW, while the topic count read 1 / 15 and while product-depth
    completion was inverted — because older historical Stage-17 text elsewhere
    in the documents satisfied every broad assertion.

    Scoped to the current Stage-17 fence, the whole conjunction is asserted and
    each inversion is forbidden. Product depth complete is not commercial
    validation, and a surface recording the first without the second is exactly
    the drift this guard exists to catch.
    """
    for path, st17 in _surfaces("stage-17-disposition"):
        _needs(st17, path, "stage 17",
               r"PRODUCT-DEPTH WORK: COMPLETED FOR THE CURRENT AUTHORIZED PRODUCT SCOPE",
               r"`D1: MERGED`", r"`D2: MERGED`", r"`D3: MERGED`",
               r"`PRE-D1/D2/D3 DEPTH: MODERATE`",
               r"`POST-D1/D2/D3 DEPTH: MODERATE-DEEP`",
               r"`TOPICS SUFFICIENTLY DEEP: 15 / 15`",
               r"`ADDITIONAL STAGE-17 PRODUCT-DEPTH IMPLEMENTATION: NOT JUSTIFIED`",
               r"COMMERCIAL READINESS: PARTIAL",
               r"`VALIDATED COMMERCIAL CONCLUSION: NO`",
               r"`READINESS CEILING: INSUFFICIENT_EVIDENCE`",
               r"Stage 17 is NOT commercially closed",
               r"Commercial Readiness is NOT asserted as passing",
               r"no market validation", r"no demand validation",
               r"no product-market-fit proof",
               r"no validated differentiation",
               r"no first-sale readiness")
        _rejects(st17, path, "stage 17",
                 r"VALIDATED COMMERCIAL CONCLUSION: YES",
                 r"COMMERCIAL READINESS: (COMPLETE|PASS|COMPLETED)",
                 r"COMMERCIAL READINESS PASS",
                 r"\bSHALLOW\b",
                 r"TOPICS SUFFICIENTLY DEEP: (?!15 ?/ ?15)",
                 r"PRODUCT-DEPTH WORK: NOT COMPLETED",
                 r"STAGE 17 NOT COMPLETED",
                 r"PRODUCT-MARKET FIT: ESTABLISHED",
                 r"DEMAND: VALIDATED",
                 r"READINESS CEILING: (?!INSUFFICIENT_EVIDENCE)")
    # Stage 17 is NOT closed: its checkbox stays empty
    assert re.search(r"^- \[ \] \*\*17 — Market Reality / Commercial Readiness:",
                     _read(ROADMAP), re.M), "stage 17 checkbox is not empty"


# Claims that are false everywhere, in current text and in preserved history
# alike. Scoping a FORBIDDEN pattern to a block is strictly weaker than
# scoping it to the file: a mutation review flipped the commercial conclusion
# in a Stage-17 sentence that sits OUTSIDE the current fence, and a
# block-scoped guard had nothing to say about it. Required patterns stay
# fenced; forbidden ones do not need to be.
NEVER_TRUE_ANYWHERE = (
    r"VALIDATED COMMERCIAL CONCLUSION: YES",
    r"COMMERCIAL READINESS: (PASS|COMPLETE|COMPLETED)",
    r"COMMERCIAL READINESS PASS",
    r"MANUFACTURABILITY CONCLUSION: YES",
    r"PRODUCT-MARKET FIT: ESTABLISHED",
    r"DEMAND: VALIDATED",
    r"READINESS CEILING: SUFFICIENT_EVIDENCE",
    r"STAGE 11 STARTED: YES",
    # `STAGE 18 STARTED: YES` was on this list until the Owner authorized the
    # first bounded CAP-01 increment, at which point it became TRUE. What entry
    # still does not license takes its place: completing the stage, authorizing
    # full CAP-01/STG, reopening D13, or activating another domain's profile.
    r"STAGE 18 COMPLETE: YES",
    # the Stage 18 closure made the SCOPED completion true; an unscoped one stays false everywhere
    r"STAGE 18: (COMPLETE|COMPLETED)(?! — CURRENT MECHANICAL \+ ELECTRICAL / ELECTRONICS SCOPE)",
    r"STAGE 19 COMPLETE: YES",
    # the Stage 19 closure made the SCOPED completion true; an unscoped one stays false everywhere
    r"STAGE 19: (COMPLETE|COMPLETED)(?! — CURRENT PLANNING-ONLY SCOPE)",
    r"STAGE 20 COMPLETE: YES",
    # the Stage 20 closure made the SCOPED completion true; an unscoped one stays false everywhere
    r"STAGE 20: (COMPLETE|COMPLETED)(?! — CURRENT OWNER-DECLARED ASSUMPTION SCOPE)",
    r"STAGE 21 COMPLETE: YES",
    # the Stage 21 closure made the SCOPED completion true; an unscoped one stays false everywhere
    r"STAGE 21: (COMPLETE|COMPLETED)(?! — CURRENT OWNER-DECLARED CONTRADICTION SCOPE)",
    r"STAGE 22 COMPLETE: YES",
    # the Stage 22 closure made the SCOPED completion true; an unscoped one stays false everywhere
    r"STAGE 22: (COMPLETE|COMPLETED)(?! — CURRENT BOUNDED DECISION TRACE \+ DECISION ROOM SCOPE)",
    r"STAGE 23 COMPLETE: YES", r"STAGE 23: ENTERED",
    # the Stage 23 closure made the SCOPED completion true; an unscoped one stays false everywhere
    r"STAGE 23: (COMPLETE|COMPLETED)(?! — CURRENT BOUNDED FOUR-AXIS READINESS-SNAPSHOT SCOPE ONLY)",
    r"STAGE 24 COMPLETE: YES",
    # the Stage 24 closure made the SCOPED completion true; an unscoped one stays false everywhere
    r"STAGE 24: (COMPLETE|COMPLETED)(?! — CURRENT BOUNDED CAP-12 FORM MOCK-UP ADVISORY SLICE 1 SCOPE ONLY)",
    # the delivered CAP-12 Form Mock-up Advisory Slice 1 made the SCOPED entry true; an unscoped one stays false
    r"STAGE 24: ENTERED(?! / PARTIAL — CAP-12 FORM MOCK-UP ADVISORY SLICE 1 ONLY)",
    r"STAGE 25 COMPLETE: YES", r"STAGE 25: (COMPLETE|COMPLETED)",
    # the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1 made the SCOPED entry true; an unscoped
    # entry, full CAP-13, a further method / consumer or a unit conversion stays false everywhere
    r"STAGE 25: ENTERED(?! / PARTIAL — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1 ONLY)",
    r"FULL CAP-13: AUTHORIZED", r"(?:FURTHER|SECOND) CAP-13 (?:METHOD|CONSUMER|SLICE)S?: AUTHORIZED",
    r"CAP-13 UNIT CONVERSION: AUTHORIZED",
    r"FULL CAP-12: AUTHORIZED", r"FURTHER CAP-12 SLICES: AUTHORIZED",
    r"FULL CAP-06: AUTHORIZED", r"FULL EIGHT-AXIS CAP-06: (?!NOT IMPLEMENTED / NOT CLOSED)",
    r"FULL (CAP-05|CAP-07): AUTHORIZED",
    r"(AUTOMATIC / AI CONTRADICTION DETECTION|SYSTEM_INFERRED CONTRADICTION WRITER): AUTHORIZED",
    r"FULL (CAP-08|CAP-10): AUTHORIZED",
    r"FULL (CAP-09|WS-PFV-001): AUTHORIZED", r"RESULT OUTCOME / PASS-FAIL JUDGEMENT: AUTHORIZED",
    r"FULL (CAP-01|STG)[^.\n]{0,40}: *AUTHORIZED",
    r"CAP-01: FULLY AUTHORIZED",
    r"D13 RESEARCH: (REOPENED|OPEN)\b",
    r"(DEPLOYMENT|PUBLIC RELEASE|PAID ACTIVATION): AUTHORIZED",
    r"T1-A′: (CLOSED|PASSED)",
    r"RUN-004: AUTHORIZED",
)


def test_the_forbidden_claims_are_absent_from_every_surface():
    """Some claims are false in current text AND in preserved history.

    No amendment these documents preserve ever asserted a validated commercial
    conclusion, a readiness PASS or an authorized deployment, so there is no
    legitimate historical sentence for these patterns to belong to. Forbidding
    them file-wide therefore costs nothing and closes the gap a block-scoped
    guard leaves: a mutation review flipped the commercial conclusion in a
    Stage-17 line sitting just outside the current fence, and every fenced
    assertion stayed green because the fence was not where the lie was.
    """
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        flat = _flat(path)
        for pat in NEVER_TRUE_ANYWHERE:
            m = re.search(pat, flat)
            assert m is None, (path, "FORBIDDEN CLAIM", pat,
                               m.group(0) if m else None)


def test_stage_eight_is_closed_by_disposition_not_by_repair():
    """Closure must never read as a repair, in any of the four surfaces."""
    roadmap, contract, register = (_flat(ROADMAP), _flat(CONTRACT),
                                   _flat(REGISTER))
    assert re.search(r"^- \[x\] \*\*8 — EN↔AR divergence:", _read(ROADMAP), re.M), (
        "stage 8 checkbox is not ticked")
    for flat in (roadmap, contract, register):
        assert "MECHANISM A: CURRENT / NOT FIXED" in flat or \
            "Mechanism A** — `CURRENT / NOT FIXED`" in flat or \
            "Mechanism A stays CURRENT / NOT FIXED" in flat or \
            "MECHANISM A: CURRENT / NOT\nFIXED" in flat
    # both merges are recorded as the closure evidence
    for flat in (roadmap, contract, register):
        assert "PR #667" in flat
        assert "PR #668" in flat
    # and the forbidden readings are absent everywhere.
    #
    # Scanned NEGATION-AWARE, following the P10-IR1 precedent for "no refund".
    # These surfaces deliberately say what is NOT claimed — "no claim is made
    # that ... Arabic generally fails" — and a bare substring scan would read
    # that disclaimer as the claim it exists to deny. The negated forms are
    # stripped first, then the bare claim must be gone.
    _NEGATIONS = (
        r"(?:no claim is made that|no claim of|none that|nor that|"
        r"(?:is |are )?not a claim that|it does not (?:say|claim)|"
        r"do(?:es)? not claim|never claims?)[^.]{0,80}?"
    )
    for path in (ROADMAP, CHECKLIST, CONTRACT, REGISTER):
        flat = _flat(path).lower()
        for claim in ("mechanism a is fixed", "mechanism a fixed",
                      "mechanism a repaired", "mechanism b closed",
                      "full en↔ar parity achieved", "parity achieved",
                      "arabic is inferior", "arabic generally fails",
                      "run-004 authorized", "stage 9 started",
                      "t1-a′ passed", "stage 7 reopened"):
            stripped = re.sub(_NEGATIONS + re.escape(claim), "", flat)
            assert claim not in stripped, (path, claim)


def test_the_stage_eight_residuals_are_preserved_not_discharged():
    """Closing the stage discharges none of them."""
    register, contract = _flat(REGISTER), _flat(CONTRACT)
    for flat in (register, contract):
        assert "OPEN / DEFERRED" in flat            # Mechanism B
        assert "R7 PF#1" in flat                    # unregistered-wording residual
        assert "NOT ESTABLISHED" in flat            # no safe bounded repair
    assert "NON-BLOCKING" in register.upper()       # dual activation
    # exactly one EN↔AR row — closure must not have forked a second one
    rows = [line for line in _read(REGISTER).splitlines()
            if line.startswith("| **EN↔AR SUBSTANTIVE-ASSESSMENT OUTCOME DIVERGENCE")]
    assert len(rows) == 1, len(rows)


def _contract_stage8_block():
    """The CURRENT Stage-8 authority block only.

    Scoped deliberately. `RUN-004` and `T1-A′` appear dozens of times in this
    file's preserved history, so a whole-file presence check would stay green
    with the boundary deleted from the block that is supposed to carry it —
    the same defect class as the Stage-8 routing guard above.
    """
    text = _read(CONTRACT)
    start = text.index('<a id="current-authority--stage-8-en-ar-divergence-closure"></a>')
    end = text.index('<a id="current-authority--stage-7-t2g-bounded-closure"></a>', start)
    return re.sub(r"\s+", " ", text[start:end])


def _checklist_current_stage_block():
    """The CURRENT '## E. Current Stage / current subtask' section only."""
    text = _read(CHECKLIST)
    start = text.index("## E. Current Stage")
    end = text.index("## F.", start)
    return re.sub(r"\s+", " ", text[start:end])


def test_the_stage_nine_boundary_survives_closure():
    """T1-A′ is not promoted by Stage-8 closure, and its history stands."""
    block = _contract_stage8_block()
    checklist_block = _checklist_current_stage_block()
    boundary = "no `RUN-004`, no fourth S2 run, no new human experiment by default"
    for flat in (block, checklist_block):
        assert boundary in flat, (
            "the standing Stage-9 boundary sentence is missing: %s" % flat[:90])
    assert "NEVER PASSED" in checklist_block.upper()
    assert "never passed and never closed" in block.lower()
    # the Stage-8 block must also carry its own residual truths
    for fragment in ("CURRENT / NOT FIXED", "OPEN / DEFERRED", "R7 PF#1"):
        assert fragment in block, fragment


def test_mechanism_b_is_not_recorded_closed_in_the_register_row():
    """Scoped to the EN↔AR row itself, not the whole register."""
    row = [line for line in _read(REGISTER).splitlines()
           if line.startswith("| **EN↔AR SUBSTANTIVE-ASSESSMENT OUTCOME DIVERGENCE")]
    assert len(row) == 1
    flat = re.sub(r"\s+", " ", row[0])
    assert "`MECHANISM B: OPEN / DEFERRED`" in flat
    assert "MECHANISM A: CURRENT / NOT FIXED" in flat
    lowered = flat.lower()
    for claim in ("mechanism b closed", "mechanism b is closed",
                  "mechanism b resolved"):
        assert claim not in lowered, claim


def test_the_superseded_stage_seven_wording_survives_as_history():
    """Preserve + supersede: the PARTIAL states must stay readable."""
    contract = _flat(CONTRACT)
    assert "Status: PARTIAL T2-G \u2014 migration path DELIVERED AS A CANDIDATE; merge not authorized." \
        in contract
    assert "`N-1` and `N-2` open pending bounded acceptance" in contract
    assert "SUPERSEDED AS CURRENT STATUS (Stage 7 closure, 2026-09-20)" in contract
    roadmap = _flat(ROADMAP)
    assert ("Still open: N-1/N-2 pending bounded acceptance, R1/R2/R3, and the "
            "three-version legacy-migration disposition.") in roadmap
    assert _flat(CHECKLIST).count("Superseded") >= 1


def test_the_closure_claims_no_release_deployment_or_activation():
    for path in (ROADMAP, CONTRACT):
        flat = _flat(path)
        assert "PUBLIC RELEASE: NOT AUTHORIZED" in flat, path
        assert "DEPLOYMENT: NOT AUTHORIZED" in flat, path
        assert "PAID ACTIVATION: NOT AUTHORIZED" in flat, path


# ==========================================================================
# N. Stage 9 / T1-A′ disposition (Owner acceptance, 2026-09-20)
#
# Stage 9 is a DISPOSITION task, and that is exactly where a reader — human or
# successor agent — loses the thread: the stage completes while the obligation
# it dispositioned stays open. A ticked Stage-9 checkbox next to a `T1-A′` that
# has never passed and never closed is correct, and it is also the single most
# misreadable state in this roadmap. These guards keep the two halves bound
# together, so that no surface can carry the completion without the residual.
#
# Every check below is SCOPED to a current block — the Stage-9 authority block,
# the Stage-9 roadmap amendment, the checklist's current-stage section, or the
# `T1-A′` register row itself. A whole-file scan would stay green on this file
# set purely from preserved history, which is the F-1 defect class this suite
# has already been corrected for twice.
# ==========================================================================
def _contract_stage9_block():
    """The CURRENT Stage-9 authority block only."""
    text = _read(CONTRACT)
    start = text.index('<a id="current-authority--stage-9-t1a-prime-disposition"></a>')
    end = text.index('<a id="current-authority--stage-8-en-ar-divergence-closure"></a>',
                     start)
    return re.sub(r"\s+", " ", text[start:end])


def _roadmap_stage9_block():
    """The CURRENT Stage-9 routing override only, not the amendments below it."""
    text = _read(ROADMAP)
    start = text.index("## Current routing override — v1.32 Stage 9 disposition amendment")
    end = text.index("## Current routing override — v1.32 Stage 8 closure amendment",
                     start)
    return re.sub(r"\s+", " ", text[start:end])


def _register_t1a_prime_row():
    """The single `T1-A′` closure row, as one flattened table line."""
    rows = [line for line in _read(REGISTER).splitlines()
            if line.startswith("| T1-A′ closure — S2 release-value criteria met |")]
    assert len(rows) == 1, ("the T1-A′ row must stay single, not forked", len(rows))
    assert len(rows[0].split("|")) - 2 == 8, "the T1-A′ row lost or gained a cell"
    return rows[0]


def test_the_stage_nine_task_completes_without_closing_the_obligation():
    """The completion and the openness must travel together, in every surface."""
    contract, roadmap = _contract_stage9_block(), _roadmap_stage9_block()
    checklist, row = (_checklist_current_stage_block(),
                      re.sub(r"\s+", " ", _register_t1a_prime_row()))
    # the stage checkbox is ticked ...
    assert re.search(r"^- \[x\] \*\*9 — T1-A′ disposition:\*\*",
                     _read(ROADMAP), re.M), "stage 9 checkbox is not ticked"
    # ... and each current surface states the completion AND the openness
    assert "| **STAGE 9 (the disposition task)** | **COMPLETED — DISPOSITION A** |" in contract
    assert "| **T1-A′ (the obligation)** | **OPEN** |" in contract
    assert "**`STAGE 9 — T1-A′ DISPOSITION: COMPLETED ✅ — DISPOSITION A.`**" in roadmap
    assert "**`T1-A′ ITSELF REMAINS OPEN. IT HAS NOT PASSED AND HAS NOT CLOSED.`**" in roadmap
    assert "**The Stage-9 DISPOSITION TASK is COMPLETED ✅ (Disposition A)**" in checklist
    assert "The Stage-9 *disposition task* is COMPLETED; **this obligation is NOT.**" in row
    # the never-passed / never-closed history is stated, not merely implied
    for flat in (contract, row):
        assert "`HAS EVER PASSED: NO`" in flat
        assert "`HAS EVER CLOSED: NO`" in flat
    assert "It has never passed and never closed." in checklist
    for flat in (contract, roadmap, checklist, row):
        assert "CLOSURE EVIDENCE: NOT MET" in flat


def test_no_completed_stage_is_left_reading_as_the_current_stage():
    """A stage that completed must not still read as current, anywhere.

    The superseded wording for each completed stage is preserved deliberately,
    so presence alone proves nothing. Each occurrence must sit inside a
    supersession note. Stage 9 and Stage 10 are both checked, because each was
    the current stage at a previous synchronization and each left its wording
    behind.
    """
    checklist = _flat(CHECKLIST)
    # AMENDED at the Stage 18 closure: the marker was Stage 19, for navigation only; AMENDED again at the Stage 19
    # closure: the marker was Stage 20, for navigation only, and Stage 19 joins the list below; AMENDED again at the
    # Stage 20 closure: the marker was Stage 21, for navigation only, and Stage 20 joins the list below; AMENDED again
    # at the Stage 21 closure: the marker was Stage 22, for navigation only, and Stage 21 joins the list below; AMENDED
    # again at the Stage 22 closure: the marker was Stage 23 (NOT ENTERED), for navigation only, and Stage 22 joins;
    # AMENDED again at the Stage 23 closure: the marker was Stage 24 (NOT ENTERED), and Stage 23 joins the list;
    # AMENDED again at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 is ENTERED / PARTIAL;
    # AMENDED again at the Stage 24 closure: the marker is Stage 25 (NOT ENTERED), and Stage 24 joins the list below;
    # AMENDED again at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 is ENTERED / PARTIAL
    assert ("**CURRENT STAGE:** Stage 25 — CAP-13 thickness / specification / safety capability — ENTERED / PARTIAL — "
            "NAVIGATION ONLY." in checklist)
    assert "**CURRENT STAGE:** Stage 25 — CAP-13 thickness / specification / safety capability — NOT ENTERED" not in checklist
    # AMENDED at the Stage-17 product-depth disposition: Stage 11 joins this
    # list. It was routed PAST, not completed, so its old current-stage wording
    # must now sit inside a supersession note exactly like a completed stage's.
    for stage in (9, 10, 11, 18, 19, 20, 21, 22, 23, 24):
        for match in re.finditer(r"CURRENT STAGE:\*{0,2} Stage %d" % stage,
                                 checklist):
            window = checklist[max(0, match.start() - 600):match.start()]
            assert "SUPERSEDED" in window.upper(), (
                "the checklist still reads Stage %d as the current stage"
                % stage)
    # AMENDED post-PR-#678: Stage 18 is ENTERED, so "Stage 18 if authorized" is
    # history now. The live frontier must say so, and the old wording may survive
    # only inside the supersession note that preserves it.
    # AMENDED at the Stage 23 closure: the frontier is Stage 24, Stage 23 COMPLETE for its bounded four-axis scope;
    # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 ENTERED / PARTIAL, row still unticked;
    # AMENDED at the Stage 24 closure: the frontier is Stage 25 (NOT ENTERED), Stage 24 COMPLETE for its bounded scope;
    # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED / PARTIAL
    assert ("CURRENT PRODUCT-DEPTH FRONTIER: Stage 25 — ENTERED / PARTIAL — NAVIGATION ONLY (`MASTER ROADMAP SEQUENTIAL "
            "MARKER: STAGE 25 — ENTERED / PARTIAL — NAVIGATION ONLY`; `NO STAGE-25 IMPLEMENTATION AUTHORIZED BY STAGE-24 "
            "CLOSURE`; `STAGE 25 — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1: DELIVERED`; `STAGE 25: ENTERED / PARTIAL "
            "— CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1 ONLY`; `FULL CAP-13: NOT AUTHORIZED`); Stage 24 — COMPLETE "
            "for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only, checkbox ticked for that scope "
            "only") in checklist
    assert "Stage 23 — COMPLETE for the current bounded four-axis Readiness Snapshot scope" in checklist
    assert "Stage 22 — COMPLETE for the current bounded decision trace + decision room scope" in checklist
    assert "Stage 21 — COMPLETE for the current Owner-declared contradiction scope" in checklist
    assert "Stage 20 — COMPLETE for the current Owner-declared assumption scope" in checklist
    assert "Stage 19 — COMPLETE for the current planning-only scope" in checklist
    assert "Stage 18 — COMPLETE for the current Mechanical + Electrical / Electronics scope" in checklist
    for match in re.finditer(r"Stage 18 if authorized", checklist):
        window = checklist[max(0, match.start() - 200):match.start()]
        assert "Superseded" in window, "a live 'Stage 18 if authorized' frontier survives"
    # and the frontier must not read as a discharge of what it routed past
    assert "Stage 11 stays DEFERRED and undischarged" in checklist


def test_the_t1a_prime_closure_criterion_is_preserved_and_unbranched():
    """§15.7 must be quoted intact, with no Stage-8-style acceptance branch.

    Stage 8 closed a row that carried an explicit acceptance branch. This row
    does not, and the guard exists so the precedent cannot be transferred by a
    later editor who remembers only that "the last one was accepted".
    """
    row = _register_t1a_prime_row()
    criterion = ("authorized verification run meeting §15.7 criteria, "
                 "Owner-adjudicated")
    assert row.split("|")[-2].strip() == criterion, (
        "the closure-evidence cell was rewritten")
    flat_row = re.sub(r"\s+", " ", row)
    assert ("NO acceptance/disclosure path analogous to the EN↔AR row is "
            "added here") in flat_row
    contract = _contract_stage9_block()
    assert '*"%s."*' % criterion in contract
    assert ("No acceptance/disclosure path analogous to Stage 8 is added to "
            "this row") in contract
    assert "no acceptance/disclosure path analogous to Stage 8 is added" in \
        _roadmap_stage9_block()


def test_the_t1a_prime_residual_is_carried_forward_not_erased():
    """Routing to Stage 10 must not drop the residual on the way."""
    assert ("**CARRIED RESIDUAL, NEVER TO BE ERASED BY ROUTING FORWARD — "
            "`T1-A′`: `OPEN` · `FRB` · `RELEASE-VALUE CRITERIA NOT MET` · "
            "`CLOSURE EVIDENCE: NOT MET`.**") in _checklist_current_stage_block()
    assert "T1-A′ travels forward as a carried residual" in _contract_stage9_block()
    assert "travels forward as a carried residual" in _roadmap_stage9_block()
    assert ("this row travels forward as a carried residual and must not be "
            "erased by routing onward") in re.sub(r"\s+", " ",
                                                  _register_t1a_prime_row())
    # the Group 2 state line must still show the obligation, not just the tick
    assert "`T1-A′` travels forward as a carried residual" in _flat(ROADMAP)


def test_the_disposition_creates_no_run_authority():
    """Completing Stage 9 arms nothing: no RUN-004, no fourth S2 run."""
    for flat in (_contract_stage9_block(), _roadmap_stage9_block(),
                 _checklist_current_stage_block(),
                 re.sub(r"\s+", " ", _register_t1a_prime_row())):
        assert "FOURTH S2 RUN / RUN-004: NOT AUTHORIZED" in flat, flat[:90]
    for flat in (_contract_stage9_block(), _roadmap_stage9_block(),
                 _checklist_current_stage_block()):
        assert "`THIRD S2 RUN: CONSUMED`" in flat
        assert "NEW HUMAN EXPERIMENT: NOT AUTHORIZED" in flat
    assert "`STAGE 10 STARTED: NO`" in _contract_stage9_block()
    assert "`STAGE 10 STARTED: NO`" in _roadmap_stage9_block()


def test_the_failed_criteria_and_the_absent_comparison_stay_recorded():
    """The specific evidence findings, not a summary word, must survive."""
    contract, roadmap = _contract_stage9_block(), _roadmap_stage9_block()
    checklist, row = (_checklist_current_stage_block(),
                      re.sub(r"\s+", " ", _register_t1a_prime_row()))
    assert "**No Full Pass — 0 of 8.**" in contract
    assert "**no Full Pass, 0 of 8**" in roadmap
    assert "No Full Pass (0 of 8)" in checklist
    assert "**no Full Pass, 0 of 8**" in row
    assert "**Criteria 5 and 6 FAIL in all 8 records.**" in contract
    for flat in (roadmap, checklist):
        assert "criteria 5 and 6 FAIL in all 8" in flat
    assert "**criteria 5 and 6 FAIL in all 8**" in row
    assert "**Candidate representation / platform-side comparison: ABSENT**" in contract
    for flat in (roadmap, checklist):
        assert "platform-side candidate comparison ABSENT" in flat
    assert "platform-side comparison ABSENT" in row
    # the remediations are recorded as true AND as insufficient
    for flat in (contract, roadmap, row):
        assert "insufficient" in flat.lower() or "remain insufficient" in flat.lower()


def test_the_stage_nine_forbidden_claims_are_absent():
    """The eleven readings this disposition must never be turned into.

    Scanned NEGATION-AWARE, as the Stage-8 guard is: these surfaces state what
    is NOT true, and a bare substring scan would read the denial as the claim.

    One literal exemption, stated rather than silently tolerated: the register
    row's NAME is "T1-A′ closure — S2 release-value criteria met" — it names the
    condition the row is open against. That exact row-name string is removed
    before scanning; no other literal is exempted. Three negation SHAPES are
    then stripped generically, each documented at its line below.
    """
    _NEGATIONS = (
        r"(?:no claim is made that|no claim of|none that|nor that|"
        r"(?:is |are )?not a claim that|it does not (?:say|claim)|"
        r"do(?:es)? not claim|never claims?|"
        r"no (?:record|run|case|result)s?)[^.]{0,80}?"
    )
    _ROW_NAME = "t1-a′ closure — s2 release-value criteria met"
    for path in (ROADMAP, CHECKLIST, CONTRACT, REGISTER):
        flat = _flat(path).lower().replace(_ROW_NAME, "")
        for claim in (
                # 1-2: the obligation closed / passed
                "t1-a′ closed", "t1-a′ is closed", "t1-a′ has closed",
                "t1-a′ passed", "t1-a′ has passed",
                # 3: release-value criteria met
                "release-value criteria met", "release-value criteria are met",
                # 4: a Full Pass
                "full pass achieved", "achieved a full pass",
                "full pass in 8/8", "a full pass was reached",
                # 5: Stage 9 still current
                "stage 9 remains the current stage",
                "stage 9 is still the current stage",
                # 6: Stage 10 started by this synchronization
                "stage 10 started: yes", "stage 10 has started",
                "stage 10 is underway", "stage 10 has begun",
                # 7-8: run authority
                "run-004 authorized", "run-004 is authorized",
                "fourth s2 run authorized", "fourth s2 run is authorized",
                # 9: criteria 5 or 6 passed
                "criteria 5 and 6 passed", "criterion 5 passed",
                "criterion 6 passed", "criteria 5 and 6 pass",
                # 10: platform-side comparison exists
                "platform-side comparison exists",
                "platform-side candidate comparison exists",
                "platform-side candidate comparison is implemented",
                # 11: the residual gone
                "t1-a′ is no longer a residual",
                "t1-a′ no longer travels forward",
                "the t1-a′ residual is discharged"):
            # two negation shapes are stripped before the scan:
            #   prefix   — "no claim is made that <claim>"
            #   trailing — "<claim>: no", the boundary-table form these
            #              documents use, e.g. "`T1-A′ CLOSED: NO`"
            # (the third, adjacent shape is applied below.)
            stripped = re.sub(_NEGATIONS + re.escape(claim), "", flat)
            stripped = re.sub(re.escape(claim) + r":?\s*(?:no\b|not\b)",
                              "", stripped)
            #   adjacent — "no <claim>", stripped with ZERO slack so that a
            #              distant "no" cannot excuse a positive claim
            stripped = re.sub(r"\*{0,2}no\*{0,2}\s+" + re.escape(claim), "",
                              stripped)
            assert claim not in stripped, (path, claim)


# ==========================================================================
# O. Stage 10 / T2-C′ differential product-value assessment (Owner, 2026-09-20)
#
# The same trap as Stage 9, one level further on: a DIFFERENTIAL task completes
# while the thing it assessed is unchanged. A ticked Stage-10 checkbox beside a
# `T2-C′` that still reads PARTIAL is correct, and a reader who takes the tick
# for a verdict gets the product's maturity exactly backwards. These guards
# keep the completion bound to the verdict, and keep four things that are easy
# to round off from being rounded off:
#
#   * material product change  is not  proven user value
#   * candidate REPRESENTATION is not  candidate COMPARISON
#   * a new Mechanical domain  is not  Electronics-equivalent depth
#   * capture surfaces         are not validated conclusions
#
# Scoped to current blocks throughout, for the reason given in §N.
# ==========================================================================
def _contract_stage10_block():
    """The CURRENT Stage-10 authority block only."""
    text = _read(CONTRACT)
    start = text.index('<a id="current-authority--stage-10-t2c-prime-differential"></a>')
    end = text.index('<a id="current-authority--stage-9-t1a-prime-disposition"></a>',
                     start)
    return re.sub(r"\s+", " ", text[start:end])


def _roadmap_stage10_block():
    """The CURRENT Stage-10 routing override only."""
    text = _read(ROADMAP)
    start = text.index("## Current routing override — v1.32 Stage 10 differential amendment")
    end = text.index("## Current routing override — v1.32 Stage 9 disposition amendment",
                     start)
    return re.sub(r"\s+", " ", text[start:end])


def _register_stage10_gate():
    """The CURRENT Stage-10 maintenance-gate paragraph in the register.

    Scoped on its own, because it is a second place the verdict is stated and
    a whole-file check would let one of the two drift while the other held.
    """
    text = _read(REGISTER)
    start = text.index("**LATEST MAINTENANCE GATE — STAGE 10 / T2-C′ DIFFERENTIAL")
    end = text.index("**LATEST MAINTENANCE GATE — STAGE 9 /", start)
    return re.sub(r"\s+", " ", text[start:end])


def _register_t2c_prime_row():
    """The single Tier-2 row that already carries `T2-C′`.

    Asserted single and eight-celled because the Owner decision forbids
    inventing a second T2-C′ row, and a fork is exactly how that happens.
    """
    rows = [line for line in _read(REGISTER).splitlines()
            if line.startswith("| T2-A WS6 quantified-requirements extension;")]
    assert len(rows) == 1, ("the Tier-2 T2-C′ row must stay single", len(rows))
    assert len(rows[0].split("|")) - 2 == 8, "the Tier-2 row lost or gained a cell"
    return rows[0]


def test_the_stage_ten_differential_completes_without_changing_the_verdict():
    """The completion and the PARTIAL verdict must travel together."""
    contract, roadmap = _contract_stage10_block(), _roadmap_stage10_block()
    checklist, row = (_checklist_current_stage_block(),
                      re.sub(r"\s+", " ", _register_t2c_prime_row()))
    assert re.search(r"^- \[x\] \*\*10 — T2-C′ differential assessment:\*\*",
                     _read(ROADMAP), re.M), "stage 10 checkbox is not ticked"
    assert ("| **STAGE 10 (the differential assessment)** | "
            "**COMPLETED — DISPOSITION B** |") in contract
    assert ("| **T2-C′ (the product-value state)** | "
            "**PARTIAL — updated differential recorded** |") in contract
    assert ("**`STAGE 10 — T2-C′ DIFFERENTIAL PRODUCT-VALUE ASSESSMENT: "
            "COMPLETED ✅ — DISPOSITION B.`**") in roadmap
    assert ("**`T2-C′ PRODUCT-VALUE CONCLUSION REMAINS PARTIAL. IT HAS NOT "
            "PASSED AND IS NOT FULLY CLOSED.`**") in roadmap
    assert "**this row is NOT closed and `T2-C′` did NOT pass.**" in row
    # the verdict is stated twice in the register — in the row and in the
    # Stage-10 maintenance gate — and BOTH must carry it, so neither can drift
    # while the other holds.
    gate = _register_stage10_gate()
    for flat in (row, gate):
        assert "`VERDICT: PARTIAL UNCHANGED`" in flat
        assert "`POST-WS16 FACTUAL PREMISES: MATERIALLY UPDATED`" in flat
    assert "`STAGE-10 DIFFERENTIAL: COMPLETED — DISPOSITION B`" in gate
    assert "NO new row was created and NO row was closed" in gate
    for flat in (contract, roadmap, checklist, row):
        assert "PASS: NO" in flat
        assert "FULLY CLOSED: NO" in flat


def test_the_controlling_ws16_baseline_is_preserved_not_rewritten():
    """Electronics-only baseline, PDVG-01's PARTIAL, both intact."""
    contract, roadmap = _contract_stage10_block(), _roadmap_stage10_block()
    row = re.sub(r"\s+", " ", _register_t2c_prime_row())
    for flat in (contract, roadmap, row):
        assert "electronics/electrical" in flat.lower(), flat[:90]
        assert "MECHANICAL WS16 BASELINE: NONE" in flat
        assert "**`PARTIAL`, not `ADEQUATE`**" in flat
    assert "PDVG-01" in contract and "PDVG-01" in roadmap and "PDVG-01" in row


def test_representation_is_never_recorded_as_comparison():
    """The G-3 distinction, in every current surface."""
    contract, roadmap = _contract_stage10_block(), _roadmap_stage10_block()
    checklist, row = (_checklist_current_stage_block(),
                      re.sub(r"\s+", " ", _register_t2c_prime_row()))
    for flat in (contract, roadmap, checklist, row):
        assert "CANDIDATE REPRESENTATION" in flat
        assert "PLATFORM-SIDE CANDIDATE COMPARISON: ABSENT" in flat
    # and the historical RUN-002 result is not re-opened by it
    for flat in (contract, roadmap, checklist):
        lowered = flat.lower()
        assert "criteria 5 or 6 now pass" in lowered, (
            "the do-not-infer sentence is missing")


def test_mechanical_is_never_recorded_as_equivalent_to_electronics():
    """A new domain is not equivalent depth, and the uncertainty stays open."""
    contract, roadmap = _contract_stage10_block(), _roadmap_stage10_block()
    checklist, row = (_checklist_current_stage_block(),
                      re.sub(r"\s+", " ", _register_t2c_prime_row()))
    for flat in (contract, roadmap, checklist, row):
        assert "DEPTH EQUIVALENCE" in flat and "NOT ESTABLISHED" in flat, flat[:90]
    for flat in (contract, roadmap, row):
        assert "UNCERTAIN PRODUCT-VALUE SIGNIFICANCE" in flat
        # neither direction may be claimed
        lowered = flat.lower()
        assert "defect proven" in lowered and "parity proven" in lowered


def test_capture_surfaces_are_never_promoted_to_conclusions():
    """FEATURE EXISTS ≠ EVIDENCE EXISTS ≠ VALIDATED CONCLUSION EXISTS."""
    contract, checklist = _contract_stage10_block(), _checklist_current_stage_block()
    for flat in (contract, checklist):
        assert "FEATURE EXISTS" in flat and "VALIDATED CONCLUSION" in flat
        assert "INSUFFICIENT_EVIDENCE" in flat
    assert "VALIDATED COMMERCIAL CONCLUSION: NO" in contract or \
        "`VALIDATED COMMERCIAL CONCLUSION: NO`" in checklist
    assert "MANUFACTURABILITY CONCLUSION: NO" in contract or \
        "`MANUFACTURABILITY CONCLUSION: NO`" in checklist
    # the runtime ceiling itself, not only the prose about it
    with open(os.path.join("engine", "readiness_snapshot.py"), encoding="utf-8") as fh:
        snapshot = fh.read()
    assert "EMITTABLE_DISPOSITIONS = (DISPOSITION_INSUFFICIENT_EVIDENCE,)" in snapshot, (
        "the readiness ceiling must not be widened by a documentation cut")


def test_mcp_stays_deferred_with_no_trigger_and_no_row():
    contract, roadmap = _contract_stage10_block(), _roadmap_stage10_block()
    checklist = _checklist_current_stage_block()
    for flat in (contract, roadmap, checklist):
        assert "TRIGGER: NOT FOUND" in flat
        assert "NOT AUTHORIZED" in flat
    assert "MCP CURRENT STATUS: DEFERRED RECOMMENDATION ONLY" in contract
    assert "REQUIRED FOR T2-C′ DISPOSITION: NO" in checklist
    # no MCP implementation may have arrived under a documentation authorization
    for directory in ("engine", "web"):
        for name in sorted(os.listdir(directory)):
            assert "mcp" not in name.lower(), (directory, name)


def test_stage_eleven_is_next_and_starts_nothing():
    contract, roadmap = _contract_stage10_block(), _roadmap_stage10_block()
    checklist = _checklist_current_stage_block()
    for flat in (contract, roadmap):
        assert ("**Next Master Roadmap stage: Stage 11 — T1-C′ / A2 human "
                "evidence.** `STAGE 11 STARTED: NO`") in flat
    assert "**`STAGE 11 STARTED: NO`**" in checklist
    # the human-evidence conditions travel with the routing
    for flat in (contract, roadmap, checklist):
        assert "consent/custody" in flat
        assert "separate authorization" in flat


def test_the_t1a_prime_residual_survives_stage_ten():
    """Stage 10 discharges nothing that Stage 9 left open."""
    contract, row = (_contract_stage10_block(),
                     re.sub(r"\s+", " ", _register_t1a_prime_row()))
    checklist = _checklist_current_stage_block()
    for flat in (contract, checklist, row):
        assert "OPEN" in flat and "FRB" in flat
        assert "CLOSURE EVIDENCE: NOT MET" in flat
    assert "RUN-004: NOT AUTHORIZED" in contract
    # the Stage-9 T1-A′ guards must still hold on their own blocks
    assert "`HAS EVER PASSED: NO`" in row


def test_the_stage_ten_forbidden_claims_are_absent():
    """The fourteen readings this differential must never be turned into.

    Negation-aware, with the same three shapes §N documents, and the same
    single literal exemption for the register row's own name.

    One alternative is added beyond §N's vocabulary: "none of these/this/
    them/which", which is the form these Stage-10 surfaces use to deny exactly
    the claims below ("none of which is REAL USER VALUE PROVEN"). It is added
    here rather than in §N so that §N's scanner stays byte-identical to the
    one its own mutation run proved.
    """
    _NEGATIONS = (
        r"(?:no claim is made that|no claim of|none that|nor that|"
        r"none of (?:these|this|them|which)|"
        r"(?:is |are )?not a claim that|it does not (?:say|claim)|"
        r"do(?:es)? not claim|never claims?|"
        r"no (?:record|run|case|result)s?)[^.]{0,80}?"
    )
    _ROW_NAME = "t1-a′ closure — s2 release-value criteria met"
    for path in (ROADMAP, CHECKLIST, CONTRACT, REGISTER):
        flat = _flat(path).lower().replace(_ROW_NAME, "")
        for claim in (
                # Stage 11 started
                "stage 11 started: yes", "stage 11 has started",
                "stage 11 is underway", "stage 11 has begun",
                # T2-C′ passed or closed
                "t2-c′ pass: yes", "t2-c′ passed", "t2-c′ is closed",
                "t2-c′ fully closed: yes", "t2-c′ has closed",
                # value and differentiation proven
                "real user value proven", "user value is proven",
                "product differentiation proven", "differentiation is proven",
                # mechanical equivalence
                "mechanical is equivalent to electronics",
                "mechanical depth equivalence: yes",
                "equivalent electronics/mechanical depth",
                # comparison
                "candidate comparison now exists",
                "platform-side candidate comparison now exists",
                # T1-A′
                "t1-a′ closed", "t1-a′ passed",
                # run authority
                "run-004 authorized", "run-004 is authorized",
                # MCP
                "mcp is required", "mcp implementation authorized",
                "mcp authorized: yes",
                # readiness promotions
                "readiness pass", "commercial readiness pass",
                "manufacturing readiness pass",
                "readiness: pass_with_conditions"):
            stripped = re.sub(_NEGATIONS + re.escape(claim), "", flat)
            # the trailing shape also admits the copula these surfaces use:
            # "<claim> is NOT claimed", alongside §N's "<claim>: no".
            stripped = re.sub(
                re.escape(claim)
                + r"(?::|\s+(?:is|are|was|were))?\s*(?:no\b|not\b)",
                "", stripped)
            stripped = re.sub(r"\*{0,2}no\*{0,2}\s+" + re.escape(claim), "",
                              stripped)
            assert claim not in stripped, (path, claim)


# ==========================================================================
# Stage 18 entry: the bounded authorization, and what it does NOT unlock
# ==========================================================================
def test_the_current_state_file_routes_to_the_entered_stage_and_authorizes_nothing():
    """CLAUDE.md sends every agent to this file's CURRENT entry, and that entry
    sits at the head of 6000 lines of preserved history. So it is fenced like
    the other surfaces, and the fence must carry the entry fact WITHOUT
    carrying authority: the mandate lives in the contract, and this file routes.
    """
    block = _current(STATE, "current-position")
    for pat in (re.escape("`STAGE 18: COMPLETE — CURRENT MECHANICAL + ELECTRICAL / ELECTRONICS SCOPE`"),
                # AMENDED at the Stage 19 closure: Stage 19 complete for its scope, the marker is Stage 20
                re.escape("`STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE`"),
                # AMENDED at the Stage 20 / 21 / 22 closures: each complete for its scope, the marker is Stage 23
                re.escape("`STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE`"),
                re.escape("`STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE`"),
                re.escape("`STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE + DECISION ROOM SCOPE`"),
                # AMENDED at the Stage 23 closure: Stage 23 complete for its bounded scope, the marker is Stage 24
                re.escape("`STAGE 23: COMPLETE — CURRENT BOUNDED FOUR-AXIS READINESS-SNAPSHOT SCOPE ONLY`"),
                # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 ENTERED / PARTIAL;
                # AMENDED at the Stage 24 closure: Stage 24 complete for its bounded scope, the marker is Stage 25;
                # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED / PARTIAL
                re.escape("`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 25 — ENTERED / PARTIAL — NAVIGATION ONLY`"),
                re.escape("`STAGE 25 — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1: DELIVERED`"),
                re.escape("`STAGE 25: ENTERED / PARTIAL — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1 ONLY`"),
                re.escape("`FULL CAP-13: NOT AUTHORIZED`"),
                re.escape("`STAGE 24 — CAP-12 FORM MOCK-UP ADVISORY SLICE 1: DELIVERED`"),
                re.escape("`STAGE 24: COMPLETE — CURRENT BOUNDED CAP-12 FORM MOCK-UP ADVISORY SLICE 1 SCOPE ONLY`"),
                re.escape("`NO STAGE-25 IMPLEMENTATION AUTHORIZED BY STAGE-24 CLOSURE`"),
                r"FIRST BOUNDED CAP-01 INCREMENT: OWNER-AUTHORIZED",
                r"FULL CAP-01\s*/\s*FULL STG: NOT AUTHORIZED",
                r"`D13 RESEARCH: REMAINS CLOSED`",
                r"Stage 18 is now \*\*COMPLETE for the current Mechanical \+ Electrical / Electronics scope\*\*",
                r"(?i)this entry routes and does not\s+authorize",
                r"electronics_electrical` only",
                r"(?i)FIRST\s+authorized profile, not the definition of CAP-01",
                r"(?i)`mechanical` remains a fully activated"):
        assert re.search(pat, block, re.S), ("current-position", "MISSING", pat)
    for pat in (r"STAGE 18 STARTED: NO", r"STAGE 18 COMPLETE: YES", r"`STAGE 18 COMPLETE: NO`",
                r"Stage 18 stays \*\*PARTIAL\*\*", r"(?i)mechanical[^.]{0,60}unsupported"):
        assert re.search(pat, block, re.I | re.S) is None, ("current-position",
                                                            "FORBIDDEN", pat)
    # the stale ACTIVE CONTRACT: NONE claim may survive ONLY as preserved history
    flat = _flat(STATE)
    for m in re.finditer(r"`ACTIVE CONTRACT: NONE` stands", flat):
        window = flat[max(0, m.start() - 400):m.start()]
        assert "Superseded" in window or "preserved" in window, (
            "a live ACTIVE CONTRACT: NONE claim survives the bounded authorization")


def test_the_capability_register_records_one_bounded_exception_not_a_general_opening():
    """The register carried TWO blanket "all eighteen are NOT AUTHORIZED"
    statements plus a CAP-01 row saying the same. One bounded authorization
    makes all three false as written, and the tempting repair — deleting the
    blanket — would read as though every recorded capability opened at once.

    So the contract is: the exception is named, it is scoped to ONE increment,
    the blanket survives for everything else, and CAP-01's full future scope is
    NOT trimmed down to the size of its first slice.
    """
    flat = _flat(CAPABILITIES)
    for pat in (r"two bounded deterministic Stage-18 CAP-01 guidance increments",
                r"first IMPLEMENTED / MERGED /\s*POST-MERGE VERIFIED \(PR #678\)",
                r"research-direction addendum likewise IMPLEMENTED / MERGED / POST-MERGE\s*VERIFIED \(PR #679",
                r"(?i)(does|do) NOT authorize full CAP-01 / full STG",
                r"(?i)CAP-02 \u2026 CAP-18, which remain `RECORDED \u2014 NOT AUTHORIZED",
                r"`FULL CAP-01 / FULL STG: NOT AUTHORIZED`",
                r"`D13 RESEARCH: REMAINS CLOSED`",
                r"`STAGE 18: COMPLETE — CURRENT\s+MECHANICAL \+ ELECTRICAL / ELECTRONICS SCOPE`",
                r"(?i)intended full future scope of CAP-01 above is NOT reduced",
                r"(?i)Domain activation is NOT CAP-01 profile availability",
                r"(?i)a missing profile, never an unsupported domain"):
        assert re.search(pat, flat, re.S), ("capability register", "MISSING", pat)
    # the blanket must still bind everything the exception does not name
    assert re.search(r"All capabilities recorded here \(CAP-01 \u2026 CAP-18\) share the "
                     r"status \*\*`RECORDED \u2014 NOT AUTHORIZED FOR\s+IMPLEMENTATION`\*\*",
                     flat), "the general non-authorization statement was deleted"
    for pat in (r"CAP-0[2-9][^|]{0,80}\| *RECORDED \u2014 AUTHORIZED",
                r"(?i)all eighteen capabilities[^.]{0,60}are now authorized",
                r"(?i)CAP-01[^.]{0,40}FULLY AUTHORIZED"):
        assert re.search(pat, flat, re.I | re.S) is None, ("capability register",
                                                           "FORBIDDEN", pat)
    # CAP-01's preserved future scope is the thing most at risk of being trimmed
    for kept in ("exact unresolved technical subproblem", "suggested search terms",
                 "required measurements/tests/", "what the system can and cannot verify",
                 r"appropriate specialist\s+category only when necessary and "
                 r"evidence-supported"):
        assert re.search(kept, flat), ("CAP-01 future scope trimmed", kept)


def test_the_integration_invariants_are_recorded_as_practice_not_as_a_gate():
    """Recorded on BOTH derived surfaces, and recorded as operating practice.

    The failure this guards against is the one that produced it: a first slice
    silently becoming the architecture, and a new capability quietly absorbing
    an owner that already exists. The second failure mode is the cure becoming
    the disease — an anti-drift note growing into another approval stage. So
    the invariants are required by substance, and gate language is forbidden.
    """
    # Slice the two sections. Scanning the whole 1500-line file for gate language
    # would report the roadmap's OTHER, legitimate gates; the question here is
    # only whether THIS section became one.
    raw_roadmap = _read(ROADMAP)
    assert "### 8C. Cross-stage capability-integration invariants" in raw_roadmap
    i = raw_roadmap.index("### 8C. Cross-stage capability-integration invariants")
    roadmap = re.sub(r"\s+", " ", raw_roadmap[i:raw_roadmap.index("\n## 9.", i)])
    raw_checklist = _read(CHECKLIST)
    j = raw_checklist.index("Cross-stage capability-integration invariants (14")
    checklist = re.sub(r"\s+", " ", raw_checklist[j:raw_checklist.index("\n---", j)])
    for text in (roadmap, checklist):
        for pat in (r"EXISTING OWNER FIRST",
                    r"PRODUCE ONCE",
                    r"CAPABILITY OWNERSHIP DOES NOT COLLAPSE|never absorbs its responsibility|"
                    r"absorbs its responsibility|ownership does not collapse",
                    r"FIRST IMPLEMENTATION \u2260 PERMANENT ARCHITECTURE",
                    r"(?i)ADAPTER LIMITATION",
                    r"(?i)permanent generated-output language authority",
                    r"(?i)CAP-06[^.]{0,80}(PRESENTATION|readiness PRESENTATION)",
                    r"(?i)CAP-07[^.]{0,80}COMPOSITION",
                    r"(?i)Technical Realization"):
            assert re.search(pat, text, re.S), ("integration invariants", "MISSING", pat)
        # It must never become another approval stage. "it is NOT a new approval
        # gate" is the point of the section, so the scan is negation-aware and
        # asks whether a negator governs the phrase, not whether one co-occurs.
        for pat in (r"new (approval|authorization) gate",
                    r"must be approved before", r"requires sign-?off",
                    r"may not proceed until"):
            for m in re.finditer(pat, text, re.I):
                head = text[max(0, m.start() - 70):m.start()].lower()
                assert any(n in head for n in ("not ", "no ", "never", "isn't",
                                               "is not", "creates no")), (
                    "integration invariants", "became a gate", pat,
                    text[max(0, m.start() - 70):m.end() + 20])
    # and the roadmap says in terms that it creates none of the usual artifacts
    assert re.search(r"(?i)create no Stage, Workstream, tracking ID, register, "
                     r"authorization\s+gate or approval step", roadmap)


def _absent(text, needle):
    """``needle not in text`` as a plain bool. Asserting ``not in`` directly over a
    whole flattened governance document makes pytest build an ndiff of that
    document on failure — quadratic, and long enough on these files to stall a CI
    run instead of reporting the failure. A bool keeps a failing guard fast."""
    return needle not in text


def test_post_pr_678_stage_18_status_is_current_on_every_live_surface():
    """PR #678 made four live sentences false at once, and each stayed green
    because nothing asserted it: the roadmap's Group-4 state ("Stages 18–20 ...
    NOT AUTHORIZED ... zero merged runtime code"), the checklist's
    Technology-Deepening position and machine record ("Stages 18–27 ... not
    entered"), and the checklist's Group table ("16, 18–20 not authorized").

    Each old sentence is legitimate HISTORY and stays preserved, so presence
    proves nothing either way. The contract is: every surviving copy sits inside a
    supersession note, the corrected current sentence is present, Stages 19–27
    stay not-entered, and the first slice's merge fact rides beside the guarded
    OWNER-AUTHORIZED token rather than replacing it.
    """
    merge = "84c45cec89f5348f279c591dd739ded0d0db24b3"
    roadmap, checklist = _flat(ROADMAP), _flat(CHECKLIST)
    stale = (
        (roadmap, "Stage 16 and Stages 18–20 remain recorded future capabilities, NOT AUTHORIZED"),
        (roadmap, "Stages 18–20 are the first three Technology Deepening stages and have zero merged runtime code"),
        (checklist, "Stages 18–27 preserved, NOT ENTERED / NOT AUTHORIZED"),
        # made history in turn by the Stage-19 entry contract (2026-09-23)
        (roadmap, "Stages 19 and 20 remain recorded future capabilities, NOT AUTHORIZED"),
        (checklist, "Stages 19–27 preserved, NOT ENTERED / NOT AUTHORIZED"),
        # made history in turn by the CAP-10 Slice 1 entry of Stage 21 (2026-09-26)
        (checklist, "Stages 20–27 preserved, NOT ENTERED / NOT AUTHORIZED"),
        # made history in turn by the CAP-08 Slice 1 entry of Stage 20 (2026-09-26)
        (roadmap, "Stage 20 remains a recorded future capability, NOT AUTHORIZED"),
        (checklist, "Stage 20 and Stages 22–27 preserved, NOT ENTERED / NOT AUTHORIZED"),
        # made history in turn by the CAP-05 + CAP-07 Slice 1 entry of Stage 22 (2026-09-26)
        (checklist, "Stages 22–27 preserved, NOT ENTERED / NOT AUTHORIZED"),
        (roadmap, "Stages 22–25 remain recorded, NOT AUTHORIZED, zero merged runtime code"),
        # made history in turn by the Stage 22 closure (2026-10-01)
        (roadmap, "**Stage 21 is ENTERED / PARTIAL**"),
        (roadmap, "**Stage 22 is ENTERED / PARTIAL** (2026-09-26)"),
        # made history in turn by the Stage 23 closure (2026-10-02)
        (roadmap, "Stages 23–25 remain recorded, NOT AUTHORIZED, zero merged runtime code"),
        (checklist, "Stages 23–27 preserved, NOT ENTERED / NOT AUTHORIZED"),
    )
    for text, sentence in stale:
        for m in re.finditer(re.escape(sentence), text):
            window = text[max(0, m.start() - 400):m.start()]
            assert "Superseded" in window or "SUPERSEDED" in window, (
                "live stale Stage-18 wording survives", sentence)
    assert "Stage 18 is ENTERED / PARTIAL" in roadmap
    assert "**Stage 20 is ENTERED / PARTIAL** (2026-09-26)" in roadmap
    # AMENDED at the Stage 23 closure: Stage 23 is complete for its bounded four-axis scope; 24–27 stay preserved;
    # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 ENTERED / PARTIAL, 25–27 preserved
    # AMENDED at the Stage 24 closure: Stage 24 COMPLETE for its bounded scope; 25–27 preserved;
    # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED / PARTIAL; 26–27
    # AMENDED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: Stage 27 ENTERED / PARTIAL;
    # Stage 26 preserved
    assert ("**Stage 23 COMPLETE for the current bounded four-axis Readiness Snapshot scope only (full CAP-06 NOT "
            "AUTHORIZED); Stage 24 COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only "
            "(full CAP-12 NOT AUTHORIZED; further CAP-12 slices NOT AUTHORIZED); Stage 25 ENTERED / PARTIAL through its "
            # AMENDED at the Stage 27 closure: Stage 27 COMPLETE for its current bounded scope only
            "delivered CAP-13 Two-Support Static Reactions Slice 1 only (full CAP-13 NOT AUTHORIZED); Stage 27 COMPLETE for "
            "the current bounded THERM-01 single-path temperature-difference scope only (full THERM-01 NOT "
            "AUTHORIZED); Stage 26 preserved, NOT ENTERED / NOT AUTHORIZED") in checklist
    assert "**Stage 22 is ENTERED / PARTIAL** (2026-09-26)" in roadmap
    # AMENDED at the Stage 22 closure: the Group 5 state reads Stage 21 and Stage 22 COMPLETE for their scopes
    assert ("**Stage 22 is COMPLETE (2026-10-01) for the current bounded decision trace + decision room scope**"
            in roadmap)
    assert "**Stage 21 is COMPLETE (2026-10-01) for the current Owner-declared contradiction scope**" in roadmap
    # AMENDED at the Stage 23 closure: the Group 5 state reads Stage 23 COMPLETE for its bounded four-axis scope
    assert ("**Stage 23 is COMPLETE (2026-10-02) for the current bounded four-axis Readiness Snapshot scope only**"
            in roadmap)
    # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 ENTERED / PARTIAL, Stage 25 recorded;
    # AMENDED at the Stage 24 closure: the Group 5 state reads Stage 24 COMPLETE for its bounded scope, Stage 25 recorded
    assert ("**Group state — UPDATED 2026-10-04 (Stage 24 closure):** **Stage 24 is COMPLETE (2026-10-04) for the "
            "current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only**") in roadmap
    # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED / PARTIAL
    assert ("**Stage 25 is ENTERED / PARTIAL (2026-10-08) through its delivered CAP-13 Two-Support Static Reactions "
            "Slice 1 ONLY (checkbox unticked; Stage 25 NOT complete; `FULL CAP-13: NOT AUTHORIZED`)**") in roadmap
    assert ("**Stage 25 remains recorded, NOT ENTERED, NOT AUTHORIZED, zero merged runtime code**"
            not in _live_only(roadmap))
    assert ("**Stage 24 is ENTERED / PARTIAL (2026-10-03) through its delivered CAP-12 Form Mock-up Advisory Slice 1 "
            "ONLY") not in _live_only(roadmap)
    raw_checklist = _read(CHECKLIST)
    assert _absent(raw_checklist, "Stages 18–27 preserved, not entered / not authorized")
    assert _absent(raw_checklist, "Stages 19–27 preserved, not entered / not authorized")
    assert _absent(raw_checklist, "Stages 20–27 preserved, not entered / not authorized")
    assert _absent(raw_checklist, "Stage 20 and Stages 22–27 preserved, not entered / not authorized")
    assert _absent(raw_checklist, "Stages 22–27 preserved, not entered / not authorized")
    assert _absent(raw_checklist, "Stages 23–27 preserved, not entered / not authorized")
    # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 entered / partial; 25–27 preserved
    assert _absent(raw_checklist, "Stages 24–27 preserved, not entered / not authorized")
    # AMENDED at the Stage 24 closure: Stage 24 complete for its bounded scope
    assert _absent(raw_checklist, "Stage 24 entered / partial — CAP-12 Form Mock-up Advisory Slice 1 delivered")
    assert re.search(r"^Stage 24 complete for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only; full "
                     r"CAP-12 not authorized$", raw_checklist, re.M)
    # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 entered / partial
    assert _absent(raw_checklist, "Stages 25–27 preserved, not entered / not authorized\n")
    assert re.search(r"^Stage 25 entered / partial — CAP-13 Two-Support Static Reactions Slice 1 delivered; full CAP-13 "
                     r"not authorized$", raw_checklist, re.M)
    # AMENDED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: Stage 27 entered / partial
    assert _absent(raw_checklist, "Stages 26–27 preserved, not entered / not authorized\n")
    assert re.search(r"^Stage 26 preserved, not entered / not authorized$", raw_checklist, re.M)
    # AMENDED at the Stage 27 closure: Stage 27 complete for its current bounded scope only
    assert re.search(r"^Stage 27 complete for the current bounded THERM-01 single-path temperature-difference scope only; "
                     r"full THERM-01 not authorized$", raw_checklist, re.M)
    assert _absent(raw_checklist, "Stage 27 entered / partial — THERM-01 Single-Path Temperature-Difference Slice 1 "
                   "delivered; full THERM-01 not authorized\n")
    row5 = [l for l in raw_checklist.splitlines() if l.startswith("| 5 | 21–25 |")]
    # AMENDED at the Stage 22 closure: Stage 22 is complete for the current bounded decision trace + decision room scope
    assert len(row5) == 1 and ("22 COMPLETE for the current bounded decision trace + decision room scope — checkbox "
                               "ticked for that scope only") in row5[0], row5
    assert "22 entered / partial" not in row5[0], row5
    # AMENDED at the Stage 23 closure: Stage 23 is complete for the current bounded four-axis scope only
    assert ("23 COMPLETE for the current bounded four-axis Readiness Snapshot scope only — checkbox ticked for "
            "that scope only") in row5[0], row5
    assert "23 not entered" not in row5[0], row5
    # AMENDED at the Stage 24 closure: Stage 24 is complete for the current bounded CAP-12 Form Mock-up Advisory scope
    assert ("24 COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only — checkbox ticked for "
            "that scope only") in row5[0], row5
    assert "24 ENTERED / PARTIAL" not in _live_only(row5[0]), row5
    # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED / PARTIAL only
    assert ("25 ENTERED / PARTIAL through the delivered CAP-13 Two-Support Static Reactions Slice 1 only — checkbox stays "
            "unticked; Stage 25 is NOT complete") in row5[0], row5
    assert "25 not entered" not in _live_only(row5[0]), row5
    assert "CAP-05 + CAP-07 Slice 1 — read-only decision trace + project context panel; delivered, PR #706" in row5[0]
    assert "Slice 2 — Actionable Decision Room Summary; delivered, PR #707" in row5[0], row5
    assert "current bounded action" not in row5[0], row5
    assert "22–25 not authorized" not in row5[0], row5
    row = [l for l in raw_checklist.splitlines() if l.startswith("| 4 | 16–20 |")]
    assert len(row) == 1 and "18 COMPLETE for the current Mechanical + Electrical / Electronics scope" in row[0], row
    # AMENDED at the Stage 19 closure: Stage 19 is complete for the current planning-only scope only
    assert "19 COMPLETE for the current planning-only scope — checkbox ticked for that scope only" in row[0], row
    assert "19 entered / not complete" not in row[0], row
    assert "19 entered for foundation / contract work only" not in row[0], row
    assert "16, 18–20 not authorized" not in row[0]
    assert "16, 19–20 not authorized" not in row[0]
    assert "16, 20 not authorized" not in row[0]
    # AMENDED at the Stage 20 closure: Stage 20 is complete for the current Owner-declared assumption scope only
    assert "20 COMPLETE for the current Owner-declared assumption scope — checkbox ticked for that scope only" in row[0], row
    assert "20 entered / partial (CAP-08 Slice 1 only" not in row[0], row
    # the first slice's merge fact beside the guarded token, on every fence
    for path, routing in _surfaces("current-routing"):
        i = routing.index("FIRST BOUNDED CAP-01 INCREMENT")
        near = routing[i:i + 260]
        assert "IMPLEMENTED / MERGED / POST-MERGE VERIFIED" in near, path
        assert "PR #678" in near and merge in near, path
        assert ("SECOND BOUNDED CAP-01 RESEARCH-DIRECTION INCREMENT: OWNER-AUTHORIZED"
                in routing), path
    # and the contract no longer calls the merged PR #678 candidate "this candidate"
    contract = _flat(CONTRACT)
    assert _absent(contract, "synchronized to that same truth in this candidate")
    assert "synchronized to that same truth in the PR #678 candidate, merged" in contract


def test_second_increment_status_is_merge_truth_and_the_none_contract_is_superseded():
    """PR #679 merged, so the pre-merge semantics this guard used to require are
    now false in the other direction. "Implemented in candidate / not yet
    authoritative" understates a merged, post-merge-verified increment exactly as
    "in implementation" once understated a finished one. The merge fact must be on
    every fence, every pre-merge phrase must be gone from live text, and with both
    bounded increments delivered and no successor mandate the live contract was
    NONE. The Owner's Stage-19 entry contract (2026-09-23) replaced that
    declaration, so the NONE text must now survive ONLY as superseded history —
    and the Stage-18 facts it carried must survive as present truth. The Stage-19
    contract itself is guarded by the test below. A NEW, separate `ACTIVE CONTRACT: NONE` is
    live again after PR #714 (no increment authorized after Mechanical Technical Deepening
    Slice 1); that declaration is guarded by the Slice-1 test below, and the post-#679
    wording must still never return."""
    merge = "d75075b01e79909ba98ac695abb4f8969e14f753"
    token = ("SECOND BOUNDED CAP-01 RESEARCH-DIRECTION INCREMENT: OWNER-AUTHORIZED / "
             "IMPLEMENTED / MERGED / POST-MERGE VERIFIED — PR #679 — merge " + merge)
    for path, routing in _surfaces("current-routing"):
        assert token in routing, path
        assert "`STAGE 18: COMPLETE — CURRENT MECHANICAL + ELECTRICAL / ELECTRONICS SCOPE`" in routing, path
    assert token in _current(STATE, "current-position")
    for path in (ROADMAP, CHECKLIST, CONTRACT, STATE, CAPABILITIES):
        flat = _flat(path)
        assert _absent(flat, "OWNER-AUTHORIZED / IN IMPLEMENTATION"), path
        for m in re.finditer(r"SECOND BOUNDED CAP-01 RESEARCH-DIRECTION INCREMENT:[^`]{0,160}", flat):
            assert "IN CANDIDATE" not in m.group(0) and "NOT YET" not in m.group(0), (path, m.group(0))
        for phrase in ("implemented in candidate, not yet authoritative",
                       "implemented in candidate and not yet authoritative"):
            assert _absent(flat, phrase), (path, phrase)
    # the post-PR-#679 declaration survives as SUPERSEDED history, never as live text
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert _absent(head, "Both Owner-authorized bounded Stage-18 / CAP-01 increments are delivered")
    assert _absent(head, "ACTIVE CONTRACT: PRESENT")
    assert _absent(head, "no successor Stage is started")
    assert ("no further CAP-01 implementation is authorized beyond the delivered Mechanical and "
            "Electrical slices") in head
    assert "no further CAP-01 implementation is authorized," not in head
    assert "Stage 18 is COMPLETE for the current Mechanical + Electrical / Electronics scope: its two bounded" in head
    contract = _read(CONTRACT)
    i = contract.index("## Current authority — post-PR-#679: no active contract")
    heading = contract[i:contract.index("\n", i)]
    assert "SUPERSEDED (2026-09-23)" in heading, heading
    section = re.sub(r"\s+", " ", contract[i:contract.index("## Current authority", i + 5)])
    for pat in (r"FURTHER CAP-01 IMPLEMENTATION\*\* \| \*\*NOT CURRENTLY AUTHORIZED",
                r"STARTED: YES` · `COMPLETE: NO` · \*\*PARTIAL", r"typed\s+technical-parameter inputs"):
        assert re.search(pat, section), pat
    live = re.sub(r"\*\(Superseded.*?\)\*", "", _flat(CONTRACT))
    assert _absent(live, "This is the live mandate."), "a live-mandate claim survives outside history"
    assert _absent(live, "**ACTIVE CONTRACT: NONE.** Both"), "the NONE declaration is still live"
    assert _absent(live, "Stage 19 is not begun"), "a live Stage-19-not-begun claim survives"
    assert _absent(live, "`ACTIVE CONTRACT: NONE` is recorded in the section above")
    assert _absent(_current(STATE, "current-position"),
                   "ACTIVE CONTRACT: NONE` — **no further CAP-01 implementation is")
    flat_checklist = _flat(CHECKLIST)
    for m in re.finditer(re.escape("NONE AUTHORIZED — `ACTIVE CONTRACT: NONE`"), flat_checklist):
        assert "Superseded" in flat_checklist[max(0, m.start() - 60):m.start()], (
            "a live NONE-AUTHORIZED subtask survives the Stage-19 entry contract")
    raw_checklist = _read(CHECKLIST)
    assert ("NO FURTHER CAP-01 IMPLEMENTATION IS AUTHORIZED BEYOND THE DELIVERED MECHANICAL "
            "AND ELECTRICAL SLICES") in raw_checklist
    assert re.search(r"^NO FURTHER CAP-01 IMPLEMENTATION IS CURRENTLY AUTHORIZED$",
                     raw_checklist, re.M) is None
    # ROTATED at the Stage 35 closure: exactly one plain-text NONE line is live again, directly under the Electrical
    # delivery line and followed by the next-increment, next-step and Stage-35 closure lines and the Slice-2 delivery
    # line (identity optional); no plain-text Stage-35 active-increment line survives, and no plain-text Stage-15
    # contract line survives
    assert len(re.findall(r"^ACTIVE CONTRACT: NONE$", raw_checklist, re.M)) == 1
    for retired in _S35_ACTIVE_ONLY:
        assert re.search(r"^" + re.escape(retired.strip("`")) + r"$", raw_checklist, re.M) is None, retired
    assert re.search(r"^ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1: DELIVERED" + _DELIVERY_IDENTITY
                     + "".join(r"\n" + re.escape(t.strip("`")) for t in _S16C_TOKENS)      # ROTATED at Stage 16
                     + r"\nSTAGE 15 CLOSURE: DELIVERED"
                     + _DELIVERY_IDENTITY + r"\nSTAGE 15 SLICE 4: DELIVERED"
                     + _DELIVERY_IDENTITY + r"\nSTAGE 15 SLICE 3: DELIVERED"
                     + _DELIVERY_IDENTITY + r"\nSTAGE 15 SLICE 2: DELIVERED"
                     + _DELIVERY_IDENTITY + r"$", raw_checklist, re.M)
    assert re.search(r"^ACTIVE CONTRACT: STAGE 15", raw_checklist, re.M) is None


def test_group_two_reads_completed_with_its_residuals_carried():
    """Group 2's checkboxes are all ticked, so calling it the current frontier is
    false — but ticking them discharged neither carried residual. The row must say
    both, and Group 3 must remain the earliest group holding an unticked stage."""
    rows = [l for l in _read(CHECKLIST).splitlines() if l.startswith("| 2 | 6–10 |")]
    assert len(rows) == 1, rows
    row = rows[0]
    assert "ALL STAGES COMPLETED" in row
    assert "T1-A′ OPEN / FRB" in row and "T2-C′ PARTIAL" in row
    assert "EARLIEST INCOMPLETE" not in row and "current frontier**" not in row
    for pat in (r"(?i)discharged(?! neither)", r"(?i)\bCLOSED\b", r"T1-A′ (CLOSED|PASSED)"):
        assert not re.search(pat, row), (pat, row)
    assert "**CURRENT EARLIEST GROUP HOLDING AN UNTICKED STAGE:** Group 3" in _read(CHECKLIST)


# ==========================================================================
# Stage 19 entry: the WS-PFV-001 / CAP-09 FOUNDATION CONTRACT, and what it does NOT unlock
# ==========================================================================
# SLICE-02 is DELIVERED (PR #683) and superseded as the live contract by MSNL
# Step 1 (2026-09-24). Its two former live tokens are now FORBIDDEN on every live
# surface; they may survive only as preserved, visibly superseded history.
_S19_FORMER_CONTRACT = ("ACTIVE CONTRACT: STAGE 19 / CAP-09 SLICE-02 — DURABLE USER-WRITTEN "
                        "MEASUREMENT METHOD ONLY")
_S19_FORMER_ONLY = ("AUTHORIZED IMPLEMENTATION: CAP-09 SLICE-02 — DURABLE USER-WRITTEN "
                    "MEASUREMENT METHOD")
_S19_ENTERED = "`STAGE 19: ENTERED / NOT COMPLETE`"
_S19_SLICE_02 = ("`CAP-09 SLICE-02: DELIVERED — PR #683 — merge "
                 "8778e2f8d40fd2dbdcc25b89a3a7221aec6d3f60`")
_S19_DELIVERED = "`DURABLE SUCCESS-CRITERION REMEDIATION: DELIVERED — PR #682`"
_S19_NOT_FULL = ("`FULL CAP-09: NOT AUTHORIZED`", "`FULL WS-PFV-001: NOT AUTHORIZED`")


def _section(raw, anchor):
    """The whitespace-flattened text of ONE contract section, located by its
    anchor (never by position, so a later current section cannot hide it)."""
    i = raw.index('<a id="%s"></a>' % anchor)
    j = raw.index("\n## Current authority", raw.index("## Current authority", i) + 5)
    return re.sub(r"\s+", " ", raw[i:j])


def test_stage_19_foundation_rules_still_bind_after_implementation_01():
    """The Stage-19 FOUNDATION contract (PR #681) is delivered history now, but
    its rules are what keep IMPLEMENTATION-01 narrow: dependency 3 satisfied for
    planning-only entry and nothing wider, Section 11 + SuccessCriterion as the
    one planning owner, no parallel store, a plan is never evidence, and the
    domain-independence boundary. Those must survive the supersession — only the
    two rows the implementation authorization made false are marked superseded.
    """
    top = _section(_read(CONTRACT), "current-authority--stage-19-cap09-foundation-contract")
    _needs(top, CONTRACT, "stage-19 foundation",
           r"DELIVERED \(PR #681\); SUPERSEDED as current authority by IMPLEMENTATION-01",
           r"\*\*SATISFIED FOR PLANNING-ONLY CAP-09 ENTRY — nothing wider\*\*",
           r"does \*\*NOT\*\* satisfy dependency 3 for any broader WS-PFV-001 capability: "
           r"validation, result capture, readiness, physical validation or status",
           r"\*\*Section 11 \"Prototype & Test Plan\" \+ `SuccessCriterion`\*\*",
           r"\*\*must extend and consume these\*\*",
           r"no parallel experiment store, no parallel experiment engine, and no duplicate "
           r"evidence, validation or readiness ownership",
           r"\*\*PLANNING METADATA ONLY\*\*",
           r"Experiment PLAN ≠ Evidence · Experiment PLAN ≠ Validation Result · "
           r"Experiment PLAN ≠ Readiness",
           r"`NOT EXECUTED / NO RESULT RECORDED`",
           r"\*\*MUST be durable before it is presented as a saved-project capability\*\*",
           r"No parallel experiment database or store may be created",
           r"`PASS / PARTIAL / FAIL / INCONCLUSIVE`",
           r"no `WS-PFV == electronics` invariant and no `CAP-09 == electronics` invariant",
           r"`mechanical` remains an ACTIVE InventorAI domain",
           # the two rows the implementation made false, visibly superseded
           r"CAP-09 PRODUCT IMPLEMENTATION\*\* \| \*\(Superseded 2026-09-23",
           r"SCHEMA / PERSISTENCE IMPLEMENTATION\*\* \| \*\(Superseded 2026-09-23")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "stage-19 foundation",
             r"\*\*ACTIVE CONTRACT: STAGE 19 / CAP-09 FOUNDATION CONTRACT ONLY\.\*\*",
             r"dependency 3[^.]{0,60}SATISFIED FOR (ALL|EVERY|FULL|WS-PFV-001 IMPLEMENTATION)")


def test_stage_19_implementation_01_rules_still_bind_after_slice_02():
    """IMPLEMENTATION-01 (PR #682) is delivered history now, but its rules are
    exactly what SLICE-02 reuses: the EXISTING SuccessCriterion made durable in
    the same store, one atomic delta, truthful outcome, no progression coupling.
    They must survive the supersession; only its ACTIVE CONTRACT line becomes
    visibly superseded history."""
    top = _section(_read(CONTRACT), "current-authority--stage-19-cap09-durable-success-criterion")
    _needs(top, CONTRACT, "implementation-01",
           r"DELIVERED \(PR #682\); SUPERSEDED as current authority by SLICE-02",
           r"\*\*No longer the current authority\.\*\*",
           r"\*\*AUTHORIZED IMPLEMENTATION\*\* \| \*\*DURABLE SUCCESS-CRITERION REMEDIATION — "
           r"IMPLEMENTATION-01 / CORRECTION-01\*\*",
           r"\*\*FULL CAP-09\*\* \| `NOT AUTHORIZED`",
           r"\*\*FULL WS-PFV-001\*\* \| `NOT AUTHORIZED`",
           r"It is \*\*not\*\* full CAP-09, it is \*\*not\*\* full WS-PFV-001",
           r"no second semantic owner",
           r"The v1 identity algorithm is unchanged",
           r"the existing `SqliteRecordStore`, in the SAME database",
           r"`prototype_plan_metadata \(project_id, experiment_id, success_criterion\)`",
           r"identity `\(project_id, experiment_id\)` and a foreign key to `projects`",
           r"no provenance, no experiment definition, no source or plan text, no Evidence, result, "
           r"validation, readiness or PASS / PARTIAL / FAIL / INCONCLUSIVE value",
           r"`ProjectRecordContract`\. The criterion is planning metadata attached AFTER "
           r"reconstruction\. It is never replayed and never a progression input",
           r"validated against CURRENT durable project truth",
           r"The whole delta commits in ONE transaction or rolls back entirely",
           r"never reported as a failed save",
           r"Store failure and corruption fail closed with no partial set",
           r"never falls back to session-only saving",
           r"\*\*Editing does not require writable progression state\.\*\*",
           r"cold, not resumed, or already complete",
           r"never reopens progression, never changes maturity, stage or gaps",
           r"\*\*Planning-metadata corruption does not govern core progression\.\*\*",
           r"never blocks cold entry, writable resume, an answer correction",
           r"\*\*Section-11 consumers fail closed\.\*\*",
           r"never repaired or collapsed into an empty collection",
           r"A NUL anywhere in a criterion is invalid input",
           r"unreadable means the outcome is unknown",
           r"F-09, F-10 and F-11 are NOT part of CORRECTION-01",
           r"No parallel experiment store, second database",
           r"No Evidence, experiment-result or validation-result capture")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "implementation-01",
             r"\*\*ACTIVE CONTRACT: STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION",
             r"stays view-only", r"Continue the project to change",
             r"FULL (CAP-09|WS-PFV-001)\W{0,8}(IS )?AUTHORIZED\b",
             r"STAGE 19 COMPLETE: YES", r"STAGE 19: COMPLETE")


def _tok(token):
    """A backticked routing token, tolerant only of line wrapping."""
    return re.escape(token).replace(r"\ ", r"\s+")


# The transient Git/GitHub identity a delivered-status token may carry: " — PR #<n> — merge <sha>".
_DELIVERY_IDENTITY = r"(?:\s+—\s+PR\s+#\d+\s+—\s+merge\s+[0-9a-f]{40})?"


def _status(token):
    """A backticked DELIVERED status token as a live requirement: the status itself is required,
    the PR / merge identity after it is optional (Git/GitHub own it)."""
    status = re.sub(r" — PR #\d+ — merge [0-9a-f]{40}(?=`$)", "", token)
    assert status.endswith(": DELIVERED`"), token
    return _tok(status[:-1]) + _DELIVERY_IDENTITY + "`"


def _status_line(token):
    """The same requirement for a plain-text checklist line (no backticks)."""
    return _status(token)[1:-1]


def _live_only(text):
    """Text with every visibly superseded note removed."""
    return re.sub(r"\*\(Superseded.*?\)\*", "", text)


def _after_fence(path, name):
    """Everything after a current block's closing fence, whitespace-flattened. Superseded notes
    are searched here as a whole, never inside a fixed-size window that each new delivery would
    have to widen."""
    raw = _read(path)
    return re.sub(r"\s+", " ", raw[raw.index(_CLOSE % name):])


# A live surface may never present SLICE-02 as the current contract again.
# The pre-Stage-19 `ACTIVE CONTRACT: NONE` forms (post-PR-#679) must never return to a live
# surface. A NONE declaration is live again only as the post-PR-#714 one, which always names
# PR #714 beside it; a bare NONE without that delivery fact is the stale form.
_PRE_S19_NONE = (r"\*\*ACTIVE CONTRACT: NONE\.\*\* Both",
                 r"NONE AUTHORIZED — `ACTIVE CONTRACT: NONE`",
                 r"`ACTIVE CONTRACT: NONE` stands",
                 r"ACTIVE CONTRACT: NONE` — \*\*no further CAP-01 implementation is",
                 # AMENDED at the Stage 20 closure: the live NONE now names the Stage-20 closure as its nearby
                 # delivery fact (the PR #714 / #716 / #718 facts moved further down the longer token line);
                 # AMENDED at the Stage 21 / Stage 22 closures: the Stage-21 / Stage-22 closure fact counts as well
                 # AMENDED at Stage 28 Qualification Slice 1: the post-Slice-1 delivery fact counts as well
                 # AMENDED at Stage 28 Qualification Slice 2: the post-Slice-2 delivery fact counts as well
                 # AMENDED at Stage 28 Optional Part Slice 1: the post-Optional-Part-Slice-1 delivery fact counts as well
                 # AMENDED at Stage 28 Optional Part Slice 2: the post-Optional-Part-Slice-2 delivery fact counts as well
                 # AMENDED at Stage 30 Part Safeguards Slice 1: the post-Stage-30-Slice-1 delivery fact counts as well
                 # AMENDED at the Stage 30 closure: the post-Stage-30-closure delivery fact counts as well
                 r"ACTIVE CONTRACT: NONE(?!.{0,1500}(?:PR[ -]#71[468]|Stage[ -]2[012][ -]closure|"
                 r"Stage[ -]28[ -]Qualification[ -]Slice[ -][12]|Stage[ -]28[ -]Optional[ -]Part[ -]Slice[ -][12]|"
                 # AMENDED at the Stage 28 part-only enablement: the post-enablement delivery fact counts as well
                 r"Stage[ -]30[ -]Part[ -]Safeguards[ -]Slice[ -]1|Stage[ -]30[ -]closure|Part[ -]Only[ -]Enablement|"
                 # AMENDED at the Stage 28 closure: the post-Stage-28-closure delivery fact counts as well
                 r"Stage[ -]28[ -]closure|"
                 # AMENDED at the Stage 23 closure: the post-Stage-23-closure delivery fact counts as well
                 r"Stage[ -]23[ -]closure|"
                 # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: its delivery fact counts as well
                 r"Stage[ -]24[ -]—[ -]CAP-12[ -]Form[ -]Mock-up[ -]Advisory[ -]—[ -]Slice[ -]1|"
                 # AMENDED at the Stage 35 closure: the post-Stage-35-closure delivery fact counts as well
                 r"Stage[ -]35[ -]closure|"
                 # AMENDED at the Stage 36 closure: the post-Stage-36-closure delivery fact counts as well
                 r"Stage[ -]36[ -]closure|"
                 # AMENDED at the Stage 16 closure: the post-Stage-16-closure delivery fact counts as well
                 r"Stage[ -]16[ -]closure|"
                 # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: its delivery fact
                 r"Stage[ -]25[ -]—[ -]CAP-13[ -]Two-Support[ -]Static[ -]Reactions[ -]—[ -]Slice[ -]1|"
                 r"post-Stage-25-CAP-13-Slice-1|"
                 # AMENDED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: its delivery fact
                 r"Stage[ -]27[ -]—[ -]THERM-01[ -]Single-Path[ -]Temperature-Difference[ -]—[ -]Slice[ -]1|"
                 r"post-Stage-27-THERM-01-Slice-1))")


_SLICE_02_LIVE_REVERSALS = (
    re.escape(_S19_FORMER_CONTRACT).replace(r"\ ", r"\s+"),
    re.escape(_S19_FORMER_ONLY).replace(r"\ ", r"\s+"),
    r"only authorized implementation is CAP-09 SLICE-02",
    r"SLICE-02 is the (live|current|active) (contract|mandate|implementation)")


def test_stage_19_slice_02_is_delivered_history_and_still_bounded():
    """SLICE-02 authorized ONE thing — the inventor's own measurement method per
    EXISTING Section-11 experiment, durable in a narrowly typed sibling sidecar
    of the same store — and PR #683 delivered it. The guard advances with the
    fact instead of freezing the old routing: the slice must read DELIVERED and
    visibly superseded as the live contract, every bounded-scope rule of the
    delivered section must survive verbatim, and no live surface may present it
    as the active contract again. Delivering a slice still opens nothing: full
    CAP-09, full WS-PFV-001, Variable and the other CAP-09 fields stay NOT
    AUTHORIZED, and Stage 19 stays ENTERED / NOT COMPLETE.
    """
    contract = _read(CONTRACT)
    top = _section(contract, "current-authority--stage-19-cap09-slice-02-measurement-method")
    _needs(top, CONTRACT, "slice-02 delivered",
           r"Measurement Method \(Owner authorization, 2026-09-23\) — DELIVERED \(PR #683\); "
           r"SUPERSEDED as current authority by MSNL Step 1",
           r"\*\*No longer the current authority\.\*\* SLICE-02 was delivered by PR #683 "
           r"\(merge `8778e2f8d40fd2dbdcc25b89a3a7221aec6d3f60`\)",
           r"Every rule below still binds",
           r"`ENTERED / NOT COMPLETE` — checkbox stays unticked",
           r"\*\*DELIVERED IMPLEMENTATION\*\* \| \*\*CAP-09 SLICE-02 — DURABLE USER-WRITTEN "
           r"MEASUREMENT METHOD\*\* — `DELIVERED — PR #683`",
           r"\*\*DURABLE SUCCESS-CRITERION REMEDIATION\*\* \| `DELIVERED — PR #682`",
           r"\*\*FULL CAP-09\*\* \| `NOT AUTHORIZED`",
           r"\*\*FULL WS-PFV-001\*\* \| `NOT AUTHORIZED`",
           r"It is \*\*not\*\* full CAP-09, it is \*\*not\*\* full WS-PFV-001",
           r"still no second semantic owner",
           r"The v1 identity algorithm, experiment ordering and source priority are unchanged",
           r"`what_to_observe`, which the method never replaces or combines with",
           r"the existing `SqliteRecordStore`, in the SAME database",
           r"`prototype_measurement_methods \(project_id, experiment_id, measurement_method\)`",
           r"`prototype_plan_metadata` is NOT widened",
           r"never a measurement, result, Evidence, validation outcome, readiness value or "
           r"progression input",
           r"Section 11 stays composed in ONE place",
           r"committed in ONE transaction",
           r"reading back the COMPLETE submitted delta of both concepts",
           r"An unresolved transaction is never read as committed truth \(IR-01\)",
           r"UNKNOWN publishes nothing",
           r"editing needs no writable progression state",
           r"never remapped, and reattaches only by its exact id",
           r"never govern core progression",
           r"Variable \(still blocked by the missing typed experiment-parameter model",
           r"No Domain Capability Profile, no new domain",
           r"F-09 was not part of SLICE-02; the Owner separately authorized ONE bounded F-09 "
           r"planning-form recovery fix",
           r"durable line endings are unchanged",
           r"`STAGE 11 / A2: DEFERRED / UNDISCHARGED`",
           r"`STAGE 15 \(IRL\): PRESERVED — MUST NOT BE LOST`", r"`T2-E: DEFERRED`",
           r"`CI OPTIMIZATION: SEPARATE / NOT IMPLEMENTED`",
           r"`STARTED: YES` · `COMPLETE: NO` · \*\*PARTIAL\*\* — unchanged",
           r"FURTHER CAP-01 IMPLEMENTATION\*\* \| \*\*NOT CURRENTLY AUTHORIZED")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "slice-02 delivered",
             r"\*\*ACTIVE CONTRACT: STAGE 19 / CAP-09 SLICE-02",
             r"\*\*AUTHORIZED IMPLEMENTATION\*\* \| \*\*CAP-09 SLICE-02",
             r"FULL (CAP-09|WS-PFV-001)\W{0,8}(IS )?AUTHORIZED\b",
             r"VARIABLE\W{0,8}(IS )?AUTHORIZED\b",
             r"STAGE 19 COMPLETE: YES", r"STAGE 19: COMPLETE",
             r"IMPLEMENTED IN CANDIDATE", r"NOT YET AUTHORITATIVE",
             r"FULL (CAP-01|STG)[^.|]{0,40}: *AUTHORIZED")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    # AMENDED at the Stage 19 closure (2026-10-01): Stage 19 is COMPLETE for the current planning-only scope only;
    # the delivered-slice facts and every limit still bind, and the pre-closure ENTERED status is history.
    for path, block in live_surfaces:
        _needs(block, path, "stage-19 live", _tok(_S19_COMPLETE), _tok(_S19_SLICE_02),
               _tok(_S19_DELIVERED), *(_tok(t) for t in _S19_NOT_FULL),
               r"Section 11 \+\s+`SuccessCriterion` stay the canonical planning\s+owner",
               r"[Aa]\s+formal\s+(experimental\s+)?variable\s+model,\s+a\s+Result\s+outcome\s+/\s+pass-fail\s+"
               r"judgement\s+and\s+every\s+other\s+CAP-09\s+field\s+"
               r"stay\s+NOT\s+AUTHORIZED")
        _rejects(block, path, "stage-19 live", *_SLICE_02_LIVE_REVERSALS, _tok(_S19_ENTERED),
                 r"\bVariable, Result and every other CAP-09 field stay",
                 r"no CAP-09\s+implementation beyond Slice 3 is currently authorized",
                 r"Variable, hypothesis and every other CAP-09 field stay\s+NOT AUTHORIZED",
                 r"no further CAP-09\s+implementation is currently authorized",
                 *_PRE_S19_NONE, r"FOUNDATION CONTRACT ONLY",
                 r"ENTERED FOR FOUNDATION", r"CAP-09 PRODUCT IMPLEMENTATION",
                 r"IMPLEMENTATION-01 ONLY",
                 r"FULL (CAP-09|WS-PFV-001)\W{0,8}(IS )?AUTHORIZED\b",
                 r"VARIABLE\W{0,8}(IS )?AUTHORIZED\b",
                 r"STAGE 19 COMPLETE: YES", r"Stages 19–27 preserved",
                 r"IMPLEMENTED IN CANDIDATE", r"NOT YET AUTHORITATIVE")
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "stage-19 routing",
               r"The Stage-19 checkbox is ticked for the current planning-only\s+scope\s+only",
               r"completing Stage 19 completes nothing in Stage 20 or any other Stage",
               r"entering Stage 19 completed nothing in Stage 18",
               r"no CAP-09\s+implementation beyond Slice 4, the Result Event Slice 1 and the Stage 19 closure is "
               r"currently authorized")
    # CLAUDE.md records the delivery and does not route to the slice
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    for needle in ("is COMPLETE for the current planning-only scope (Stage 19 closure, above)",
                   "the durable SuccessCriterion remediation (PR #682) and CAP-09 SLICE-02, the "
                   "durable user-written measurement method (PR #683), are delivered",
                   "SLICE-02 is not the active contract",
                   "Full CAP-09 and full WS-PFV-001 are NOT AUTHORIZED",
                   "no other Stage is authorized"):
        assert needle in head, needle
    for stale in ("FOUNDATION CONTRACT ONLY", "NOT STARTED / NOT AUTHORIZED YET",
                  "Both Owner-authorized bounded Stage-18 / CAP-01 increments are delivered",
                  "IMPLEMENTATION-01 ONLY",
                  _S19_FORMER_CONTRACT, "The only authorized implementation is CAP-09 SLICE-02"):
        assert _absent(head, stale), stale
    # the checklist machine record keeps every bounded fact, and no SLICE-02 contract line
    raw_checklist = _read(CHECKLIST)
    for line in ("STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE",
                 "CAP-09 SLICE-02: DELIVERED — PR #683 — merge "
                 "8778e2f8d40fd2dbdcc25b89a3a7221aec6d3f60",
                 "DURABLE SUCCESS-CRITERION REMEDIATION: DELIVERED — PR #682",
                 "FORMAL EXPERIMENTAL VARIABLE MODEL / RESULT / OTHER CAP-09 FIELDS: NOT AUTHORIZED",
                 "CRITERIA EDITING: NO WRITABLE PROGRESSION STATE REQUIRED",
                 "PLANNING-METADATA CORRUPTION: DOES NOT GOVERN CORE PROGRESSION",
                 "SECTION-11 CONSUMERS: FAIL CLOSED WHEN DURABLE CRITERIA CANNOT BE READ",
                 "FULL CAP-09: NOT AUTHORIZED", "FULL WS-PFV-001: NOT AUTHORIZED",
                 # rotated with the Mechanical slices: after PR #714 the plain-text boundary
                 # names the delivered Mechanical slices instead of a blanket denial
                 "NO FURTHER CAP-01 IMPLEMENTATION IS AUTHORIZED BEYOND THE DELIVERED MECHANICAL AND "
                 "ELECTRICAL SLICES"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    for gone in ("ACTIVE CONTRACT: STAGE 19 / CAP-09 FOUNDATION CONTRACT ONLY",
                 "ACTIVE CONTRACT: STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION "
                 "— IMPLEMENTATION-01 ONLY",
                 "CAP-09 PRODUCT IMPLEMENTATION: NOT STARTED / NOT AUTHORIZED YET",
                 _S19_FORMER_CONTRACT, _S19_FORMER_ONLY):
        assert re.search(r"^" + re.escape(gone) + r"$", raw_checklist, re.M) is None, gone
    live_checklist = re.sub(r"\*\(Superseded.*?\)\*", "", _flat(CHECKLIST))
    assert _absent(live_checklist, "**CURRENT SUBTASK:** STAGE 19 / CAP-09 SLICE-02")
    assert _absent(live_checklist, "the only authorized implementation is CAP-09 SLICE-02")
    # the roadmap row: delivered, still bounded; ticked by the Stage 19 closure for the planning-only scope only
    rows = re.findall(r"^- \[x\] \*\*19 — WS-PFV-001/CAP-09:\*\*.*$", _read(ROADMAP), re.M)
    assert len(rows) == 1, "stage 19 row missing, duplicated or unticked"
    row = rows[0]
    assert "**COMPLETE (2026-10-01) for the current planning-only scope — checkbox ticked for that scope only:**" in row
    assert "**ENTERED (2026-09-23):**" in row
    assert ("CAP-09 SLICE-02, one inventor-written measurement method per existing experiment, "
            "durable in the same project store, is delivered (PR #683)") in row
    assert ("no CAP-09 implementation beyond Slice 4, the Result Event Slice 1 and the Stage 19 closure is currently "
            "authorized") in row
    assert "is delivered (PR #682)" in row
    assert "full CAP-09 and full WS-PFV-001 NOT AUTHORIZED" in row
    assert "satisfied for planning-only CAP-09 entry, and for nothing wider" in row
    live_row = re.sub(r"\*\(Superseded.*?\)\*", "", row)
    assert _absent(live_row, "the ONLY authorized implementation is CAP-09 SLICE-02"), live_row
    assert _absent(live_row, "no further CAP-09 implementation is currently authorized"), live_row
    assert _absent(live_row, "beyond Slice 3 is currently authorized"), live_row
    # AMENDED at the Stage 20 closure: the Stage 20 row is ticked by its own closure, never by a CAP-09 slice
    assert re.search(r"^- \[x\] \*\*20 — CAP-08:", _read(ROADMAP), re.M), "stage 20 row changed"
    # the register records FIVE bounded CAP-09 exceptions, not an opening of CAP-09
    register = _read(CAPABILITIES)
    reg_rows = [l for l in register.splitlines() if l.startswith("| CAP-09 Experiment Designer |")]
    assert len(reg_rows) == 2, reg_rows
    for r in reg_rows:
        assert "RECORDED — NOT AUTHORIZED, except one bounded" in r, r
        assert "durable SuccessCriterion remediation" in r, r
        assert "SLICE-02 durable measurement method" in r, r
        assert "Slice 3 durable Test Hypothesis (delivered, PR #711)" in r, r
        assert "Slice 4 durable Test Variable / Condition (delivered, PR #712)" in r, r
        assert "Result Event Slice 1 append-only owner-stated result history (delivered)" in r, r
        assert ("the bounded Stage 19 closure read-only execution-state disclosure (delivered; Stage 19 COMPLETE for "
                "the current planning-only scope)") in r, r
    flat_register = _flat(CAPABILITIES)
    assert ("It does NOT authorize full CAP-09, full WS-PFV-001 or a formal experimental "
            "variable model") in flat_register
    # AMENDED at the Stage 19 closure: the closure is the sixth bounded exception
    assert "**with SIX bounded exceptions**" in flat_register
    for stale in ("**with FIVE bounded exceptions**", "**with FOUR bounded exceptions**",
                  "**with THREE bounded exceptions**"):
        assert stale not in flat_register, stale
    assert "(delivered, PR #712, merge `c0faedcd3bff317d9439a7561c220a6ca97f7f4a`); (5) CAP-09 Result Event" \
        in flat_register
    assert "and (6) the Stage 19 — Experiment Execution-State Disclosure — Closure (delivered)" in flat_register
    assert "Astra architecture and UX / behaviour reviews PASS, PR / merge pending" not in flat_register
    assert ("OWNER-STATED / UNVALIDATED with no automatic judgement (delivered)") in flat_register
    assert ("`BOUNDED OWNER-DEFINED TEST VARIABLE / CONDITION: AUTHORIZED WITHIN CAP-09 SLICE 4` · "
            "`FORMAL EXPERIMENTAL VARIABLE MODEL: NOT AUTHORIZED`") in flat_register
    # Result RECORDING is delivered; only the outcome / judgement stays unauthorized
    assert "`RESULT OUTCOME / PASS-FAIL JUDGEMENT: NOT AUTHORIZED`" in flat_register
    assert ("A Failure Criterion as a new inventor field and Risks as CAP-09 fields are NOT "
            "authorized") in flat_register
    assert ("Result, a Failure Criterion as a new inventor field and Risks as CAP-09 fields are "
            "NOT authorized") not in flat_register
    assert ("Variable, Result, a Failure Criterion as a new inventor field and Risks as CAP-09 "
            "fields are NOT authorized") not in flat_register
    assert "Variable, hypothesis, risks and a result category are NOT authorized" not in flat_register
    assert "`FULL CAP-09: NOT AUTHORIZED` · `FULL WS-PFV-001: NOT AUTHORIZED`" in flat_register


# ==========================================================================
# MSNL Step 1: the live contract is READ-ONLY adjudication, never implementation
# ==========================================================================
_MSNL_CONTRACT = ("`ACTIVE CONTRACT: MSNL STEP 1 — READ-ONLY ARCHITECTURE / DATA-FLOW "
                  "ADJUDICATION ONLY`")
_MSNL_NOT_YET = "`MSNL IMPLEMENTATION: NOT YET AUTHORIZED`"
_TARGET_AWARE = ("`TARGET-AWARE QUESTION / ANSWER BINDING: COMPLETE — PR #690 — merge "
                 "ca9311029f30ea66ceae28f5dda5c5e6dd4e2b4a`")

# Every way the read-only step could be misread as something wider. Each is an
# affirmative predicate, so the required negations ("no provider selection", "not
# yet authorized", "is not OWNER_STATED") stay sayable while a reversal fails.
_MSNL_REVERSALS = (
    r"MSNL (runtime |implementation )?(is|has been) (now )?(authorized|implemented|active|activated)\b",
    r"MSNL IMPLEMENTATION\W{0,8}(IS )?(AUTHORIZED|IMPLEMENTED|ACTIVE)\b",
    r"runtime MSNL (implementation )?(is|has been) (authorized|permitted|allowed)",
    r"(?<!no )provider (is|has been|was) (selected|integrated|adopted|activated|chosen)",
    r"(model|LLM) calls? (is|are) (authorized|permitted|allowed|enabled)",
    r"(may|can|is allowed to|are allowed to) (send|transmit)[^.]{0,60}(outside InventorAI|externally)",
    r"SYSTEM_INFERRED[^.]{0,40}\b(is|becomes) (authoritative|persisted|OWNER_STATED)",
    r"automatic concept creation (is|becomes) (allowed|permitted|authorized)",
    r"(readiness|maturity|validation) promotion (is|becomes) (allowed|permitted|authorized)",
    r"AUTONOMOUS TECHNICAL ORCHESTRATION\W{0,8}(IS )?(AUTHORIZED|ACTIVE|ACTIVATED|CURRENT)\b",
    r"question (hiding|reduction)[^.;]{0,30}\b(is|are) (authorized|allowed|permitted|active)",
    r"STAGE 18 COMPLETE: YES", r"STAGE 19 COMPLETE: YES",
    # the Stage 19 closure made ONLY the planning-only-scoped completion true
    r"STAGE 19: COMPLETE(?! — CURRENT PLANNING-ONLY SCOPE)",
    r"Stage 18\s+(is|was|has been)\s+(COMPLETE|COMPLETED|CLOSED)\b(?!\s+for\s+the\s+current\s+Mechanical)",
    r"Stage 19\s+(is|was|has been)\s+(COMPLETE|COMPLETED|CLOSED)\b(?!\s+for\s+the\s+current\s+planning-only)",
    r"FULL (CAP-09|WS-PFV-001)\W{0,8}(IS )?AUTHORIZED\b",
    r"\bStage (4[6-9]|[5-9]\d)\b", r"\bSTAGE (4[6-9]|[5-9]\d)\b")


_PH1_CONTRACT = ("`ACTIVE CONTRACT: PROVENANCE HARDENING STEP 1 — ASSERTION SOURCE / VALIDATION "
                 "BOUNDARY ONLY`")
_MSNL_SHADOW = ("`MSNL LOCAL-ONLY SHADOW FOUNDATION: DELIVERED — PR #693 — merge "
                "319b702678a1785e117c018f87cf171d5cbf2c9d`")
_MSNL_PACK = ("`MSNL EVALUATION PACK V1: DELIVERED — PR #694 — merge "
              "c5f59093eafbccce8ff9e947d40c46f3ae86915f`")
_EXTERNAL_MSNL_NO = "`EXTERNAL / PROVIDER MSNL: NOT AUTHORIZED`"
_DURABLE_SI_NO = "`DURABLE SYSTEM_INFERRED WRITER: NOT AUTHORIZED`"

# Every way Provenance Hardening Step 1 could be misread as something wider,
# on top of every MSNL reversal (which stay forbidden: the MSNL boundary did
# not relax because the live contract advanced).
_PH1_REVERSALS = _MSNL_REVERSALS + (
    r"DURABLE SYSTEM_INFERRED WRITER\W{0,8}(IS )?(AUTHORIZED|ACTIVE|IMPLEMENTED)\b",
    r"VALIDATION-AWARD WRITER\W{0,8}(IS )?(AUTHORIZED|ACTIVE|IMPLEMENTED)\b",
    r"READINESS USE OF SYSTEM INFERENCE\W{0,8}(IS )?(AUTHORIZED|ACTIVE)\b",
    r"EXTERNAL / PROVIDER MSNL\W{0,8}(IS )?(AUTHORIZED|ACTIVE|IMPLEMENTED)\b",
    r"(OD-3|OD-4)\W{0,4}(is )?(decided|DECIDED|resolved)\b",
    r"SYSTEM_INFERRED[^.]{0,40}\b(may|can) (be persisted|become durable|count toward readiness)",
    r"(DEPLOYMENT|PUBLIC RELEASE|PAID ACTIVATION)\W{0,8}(IS )?AUTHORIZED\b",
    re.escape(_MSNL_CONTRACT), re.escape(_MSNL_NOT_YET))


def test_msnl_step_1_is_delivered_history_and_its_safety_rules_still_bind():
    """MSNL Step 1 (read-only adjudication) was delivered, and the Owner then
    authorized exactly two bounded MSNL deliveries — the local-only shadow
    foundation (PR #693) and the synthetic Evaluation Pack V1 (PR #694). The
    guard advances with the fact instead of freezing the old routing: Step 1
    reads DELIVERED and visibly superseded, while every MSNL safety rule it
    recorded still binds verbatim and no reversal may appear. Nothing here
    authorizes a provider, a model call, data transmission, durable system
    inference or any wider MSNL.
    """
    contract = _read(CONTRACT)
    top = _section(contract, "current-authority--msnl-step-1-read-only-adjudication")
    _needs(top, CONTRACT, "msnl step 1 delivered",
           r"adjudication \(Owner authorization, 2026-09-24\) — DELIVERED; SUPERSEDED as current "
           r"authority by Provenance Hardening Step 1",
           r"\*\*No longer the current authority\.\*\*",
           r"Every rule below still binds",
           r"EXISTING Stage-18 semantic-normalization item",
           r"\*\*Not authorized by this step:\*\* runtime MSNL implementation; external LLM / "
           r"provider integration; provider selection; spend commitment; sending user / project "
           r"/ invention data externally; live model calls; new persisted SYSTEM_INFERRED truth; "
           r"state mutation; gap closure; maturity / readiness / validation promotion; new "
           r"concept creation; autonomous technical orchestration; question hiding or "
           r"reduction; new domain activation\.",
           r"L1–L4 repairs are not reopened",
           r"Mechanical default-visible Path-N set remains \*\*10 questions\*\*",
           r"\*\*A hidden question must never mean a hidden unknown\*\*",
           r"\*\*no durable or authoritative system-generated technical inference may be "
           r"activated\*\*",
           r"SYSTEM_INFERRED is not OWNER_STATED",
           r"SYSTEM_INFERRED \+ UNVALIDATED until independently supported",
           r"pre-Target-Aware reader does not load sixteen-field rows",
           r"No repair and no migration now")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "msnl step 1 delivered",
             *_MSNL_REVERSALS, r"\*\*ACTIVE CONTRACT: MSNL STEP 1")
    # the carried Stage-18 note: its nine rules bind every later step verbatim
    for path, note in _surfaces("stage-18-semantic-normalization"):
        _needs(note, path, "msnl note",
               r"NOT AUTHORIZED\s*[·/]\s*NOT IMPLEMENTED as implementation",
               r"ONLY A LOCAL-ONLY SHADOW FOUNDATION \(PR #693\) AND A SYNTHETIC EVALUATION\s+PACK "
               r"\(PR #694\) DELIVERED; EXTERNAL / PROVIDER / DURABLE MSNL NOT AUTHORIZED",
               r"that authorized no runtime, no provider, no model call and no data transmission",
               r"capture is OFF by\s+default and its sink discards — no provider, no persistence, "
               r"no inference authority",
               r"evaluation pack is synthetic only",
               r"\*\*\(1\) shadow / proposal first\*\* — before provenance hardening, MSNL output "
               r"may only propose a normalization and never becomes authoritative project truth",
               r"\*\*\(2\) closed concept vocabulary\*\* — map natural-language input only to "
               r"existing governed canonical concepts, never inventing one",
               r"\*\*\(3\) precision first\*\* — a false semantic attribution is more dangerous "
               r"than an abstention",
               r"\*\*\(4\) abstain is safe\*\* — low confidence or ambiguity returns ABSTAIN / "
               r"NO-MAPPING, never a classification forced to raise coverage",
               r"\*\*\(5\) fail closed with deterministic fallback\*\* — when MSNL abstains or "
               r"fails, the existing deterministic engine stays functional and authoritative",
               r"\*\*\(6\) provider neutrality\*\* — no binding to one vendor or model",
               r"\*\*\(7\) no decision authority\*\* — MSNL never decides gap status, maturity, "
               r"readiness, validation, evidence truth, specialist completion or commercial "
               r"readiness",
               r"source input → normalization proposal → candidate canonical concept → "
               r"disposition",
               r"\*\*\(9\) privacy / data minimization\*\* — before ANY external provider "
               r"integration, determine what invention / project / user data may leave InventorAI, "
               r"the minimum needed, retention, security, provider handling and the applicable "
               r"privacy boundary, and never send whole-project context merely because it is "
               r"technically convenient")
        _rejects(note, path, "msnl note", *_MSNL_REVERSALS,
                 r"MSNL output (may|can) (become|be) (authoritative|project truth)",
                 r"(must|should|may) force a classification",
                 r"MSNL (may|can) (decide|invent)",
                 r"(may|can) send whole-project context")


def test_provenance_hardening_step_1_is_delivered_history_and_its_rules_still_bind():
    """Provenance Hardening Step 1 was delivered (PR #695). The guard advances
    with the fact: the section reads DELIVERED and visibly superseded, its
    boundary rules still bind verbatim, and it may never again present itself
    as the live contract or read as anything wider than it was.
    """
    contract = _read(CONTRACT)
    top = _section(contract, "current-authority--provenance-hardening-step-1")
    _needs(top, CONTRACT, "ph1 delivered",
           r"boundary \(Owner authorization, 2026-09-25\) — DELIVERED \(PR #695\); SUPERSEDED as "
           r"current authority by the Autonomous Technical Orchestration synthetic shadow "
           r"evaluation foundation",
           r"\*\*No longer the current authority\.\*\*",
           r"Step 1 was delivered \(PR #695, merge `6c413c54684b0eff6d1d0db205b3ccc82d99bc06`\)",
           r"Every rule below still binds",
           r"provenance precondition of the EXISTING Stage-18 semantic-normalization item",
           r"\*\*Not authorized by this step:\*\* a durable SYSTEM_INFERRED writer; a new "
           r"proposal carrier or any proposal persistence; any validation-award writer; any "
           r"readiness-policy change or readiness use of system inference; cross-source "
           r"supersession;",
           r"OWNER_STATED is not true; SYSTEM_INFERRED is not validated; EXPERT_SUPPLIED is "
           r"not SPECIALIST_REVIEWED; EXTERNAL_EVIDENCE is not EMPIRICALLY_DEMONSTRATED or "
           r"INDEPENDENTLY_VERIFIED",
           r"`specialist_required` is not `specialist_reviewed`; `evidence_requested` is not "
           r"`evidence_exists`",
           r"what may be represented is not what any writer may award",
           r"Mechanical default-visible Path-N set remains \*\*10 questions\*\*")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "ph1 delivered",
             *_PH1_REVERSALS, r"\*\*ACTIVE CONTRACT: PROVENANCE HARDENING STEP 1")


_ATO_CONTRACT = ("`ACTIVE CONTRACT: AUTONOMOUS TECHNICAL ORCHESTRATION — SYNTHETIC SHADOW "
                 "EVALUATION FOUNDATION — IMPLEMENTATION 01`")
_PH1_DELIVERED = ("`PROVENANCE HARDENING STEP 1: DELIVERED — PR #695 — merge "
                  "6c413c54684b0eff6d1d0db205b3ccc82d99bc06`")
_ATO_NO_CHANGE = "`DETERMINISTIC LOCAL ORCHESTRATION: NO-CHANGE / DIFFERENT TRIGGER REQUIRED`"
_ATO_D123 = "`OWNER DECISIONS D1 / D2 / D3: APPROVED FOR SYNTHETIC EXTERNAL EVALUATION ONLY`"
_ATO_REAL_NO = "`REAL INVENTION DATA: NOT AUTHORIZED FOR EXTERNAL TRANSMISSION`"
_ATO_OD = "`OD-2 / OD-3 / OD-4: UNDECIDED — NOT REQUIRED`"

# Every way the synthetic foundation could be misread as something wider, on
# top of every MSNL / Provenance Hardening reversal (none of which relaxed).
_ATO_REVERSALS = _PH1_REVERSALS + (
    re.escape(_PH1_CONTRACT),
    r"REAL (INVENTOR|INVENTION|USER|PROJECT) DATA\W{0,8}(IS |ARE )?(AUTHORIZED|PERMITTED|ALLOWED)\b",
    r"real (inventor|invention|user|project) data (may|can) (be sent|leave|be transmitted)",
    r"(production|permanent) (provider|vendor)[^.]{0,20}\b(decided|selected|chosen)\b",
    r"live[- ]product (call path|model call)s?[^.]{0,20}\b(is|are) (authorized|enabled|active)",
    r"FIRST REAL SYNTHETIC PROVIDER RUN\W{0,8}(IS )?(AUTHORIZED|DONE|COMPLETE)",
    r"(proposal|orchestration output)s? (is|are|becomes?) (authoritative|evidence|OWNER_STATED|"
    r"persisted|validated)\b",
    r"hosted CI (may|can|will) (call|reach|use) (the network|a provider|OpenAI)",
    r"(OD-2)\W{0,4}(is )?(decided|DECIDED|resolved)\b")


def test_ato_synthetic_shadow_foundation_is_delivered_history_and_its_rules_still_bind():
    """The Autonomous Technical Orchestration synthetic shadow evaluation
    foundation was delivered (PR #696; PR #697 / PR #698 followed; the synthetic
    canary, RUN 01 and RUN 01A were performed). The guard advances with the
    fact: the section reads DELIVERED and visibly superseded, every boundary
    rule still binds, and it may never again present itself as the live
    contract or read as anything wider than it was.
    """
    contract = _read(CONTRACT)
    top = _section(contract, "current-authority--ato-synthetic-shadow-evaluation-foundation")
    _needs(top, CONTRACT, "ato delivered",
           r"Implementation 01 \(Owner decisions D1 / D2 / D3, 2026-09-25\) — DELIVERED \(PR "
           r"#696\); SUPERSEDED as current authority by Safe Question Reduction Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #696, merge `96b7ba1773216ba0a1350a116341f6746360321c`",
           r"PR #697, merge `5f464c8cfa93648e66787d04eb3a09298a458cb3`",
           r"PR #698, merge `49aa5003f90349c8ea62aca36aa10a19c33e3c6f`",
           r"Every rule below still binds except where Slice 1 states otherwise",
           r"EPHEMERAL, PROPOSAL-ONLY and NON-AUTHORITATIVE — conceptually SYSTEM_INFERRED \+ "
           r"UNVALIDATED and written nowhere",
           r"\*\*SYNTHETIC PROVIDER RUNS\*\* \| `PERFORMED` — managed-credential canary; RUN 01 "
           r"over the committed 55-case synthetic pack; RUN 01A bounded stability diagnostic\. "
           r"Synthetic only; no real invention data\. Any further run needs its own Lead "
           r"authorization",
           r"\*\*REAL INVENTION DATA\*\* \| `NOT AUTHORIZED FOR EXTERNAL TRANSMISSION`",
           r"`OpenAI API · gpt-6-sol` — not a production-provider decision and not a permanent "
           r"vendor selection",
           r"one closed credential mode: `env` \(an explicit key or `OPENAI_API_KEY`\) or "
           r"`managed_proxy` \(`--managed-credential`: the process reads and sends no key; the "
           r"managed egress proxy supplies it\)",
           r"Hosted CI stays network-free and uses fakes and the NullAdapter only",
           r"A proposal is never OWNER_STATED, Evidence, validated truth, readiness, maturity, "
           r"gap closure, specialist review, empirical demonstration or a final design decision",
           r"The deterministic core remains the authority",
           r"a hidden question must never mean a hidden unknown")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "ato delivered",
             *_ATO_REVERSALS, r"FIRST REAL SYNTHETIC PROVIDER RUN\*\* \| `NOT YET",
             r"a credential from `OPENAI_API_KEY`\);",
             r"\*\*ACTIVE CONTRACT: AUTONOMOUS TECHNICAL ORCHESTRATION")


_SQR1_CONTRACT = "`ACTIVE CONTRACT: SAFE QUESTION REDUCTION — SLICE 1 — PF:Q2 NON-OWNER NEED ROUTING ONLY`"
_SQR1_DELIVERED = ("`SAFE QUESTION REDUCTION — SLICE 1: DELIVERED — PR #701 — merge "
                   "34c0fc372f7374488acda03514e279119b735bc5`")
_SQR1_RECOVERY = ("`WEAK-PF RECOVERY: DELIVERED — PR #702 — merge "
                  "20f27e5100cf9d475ae68d73da7cc17b2ecbf241`")
_ATO_DELIVERED = ("`AUTONOMOUS TECHNICAL ORCHESTRATION SYNTHETIC SHADOW EVALUATION FOUNDATION: "
                  "DELIVERED — PR #696 — merge 96b7ba1773216ba0a1350a116341f6746360321c`")
_SQR1_REVERSALS = tuple(
    p for p in _ATO_REVERSALS
    if not p.startswith(r"DURABLE SYSTEM_INFERRED WRITER")) + (
    re.escape(_ATO_CONTRACT),
    r"DURABLE SYSTEM_INFERRED WRITER\W{0,8}(IS )?(AUTHORIZED|ACTIVE|IMPLEMENTED)\b(?! ONLY)",
    r"(BOUNDARY_AMBIGUITY|BA)[: ]Q[34] (is |are )?(routed|suppressed|hidden)",
    r"(routed|routing) (need|requirement)s? (is|are) (solved|resolved|satisfied|validated)",
    r"specialist (input )?(is|has been) (assigned|provided|reviewed)",
    r"MECHANISM_COMPLETENESS (is|becomes) (routable|parkable|risk-acceptable)",
    r"FIRST REAL SYNTHETIC PROVIDER RUN\W{0,8}`?NOT YET",
    r"first real synthetic provider run needs")


def test_safe_question_reduction_slice_1_is_delivered_history_and_its_rules_still_bind():
    """Safe Question Reduction Slice 1 was delivered (PR #701; the bounded weak-PF
    recovery PR #702 followed). The guard advances with the fact: the section
    reads DELIVERED and visibly superseded, every routing rule still binds, the
    live surfaces carry the delivered tokens, and it may never again present
    itself as the live contract or read as anything wider than it was.
    """
    contract = _read(CONTRACT)
    top = _section(contract, "current-authority--safe-question-reduction-slice-1")
    _needs(top, CONTRACT, "sqr1 delivered",
           r"PF:Q2 non-Owner need routing only \(Owner / Lead authorization, 2026-09-26\) — "
           r"DELIVERED \(PR #701; PR #702 followed\); SUPERSEDED as current authority by CAP-10 "
           r"Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #701, merge `34c0fc372f7374488acda03514e279119b735bc5`",
           r"PR #702, merge `20f27e5100cf9d475ae68d73da7cc17b2ecbf241`",
           r"Every rule below still binds except where CAP-10 Slice 1 states otherwise",
           r"`mechanical:PHYSICAL_FEASIBILITY:Q2` ONLY → `SPECIALIST`",
           r"NEW routing-aware projects: \*\*9\*\* · every existing project: \*\*10\*\*, unchanged",
           r"`ONE NARROW EXCEPTION — deterministic NeedRoutingRevision rows \(ROUTE / RETRACT\) "
           r"only`; every other system-inference writer stays NOT AUTHORIZED",
           r"MECHANISM_COMPLETENESS is never routable, parkable or risk-acceptable",
           r"Removing mandatory Owner answering is not a solved requirement",
           r"is a maturity exception, never a discharge: the routed need stays outstanding and "
           r"unresolved",
           r"rendering never writes")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "sqr1 delivered",
             *_SQR1_REVERSALS, r"\*\*ACTIVE CONTRACT: SAFE QUESTION REDUCTION")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "sqr1 delivered live", _tok(_SQR1_DELIVERED),
               _tok(_SQR1_RECOVERY), _tok(_ATO_DELIVERED), _tok(_PH1_DELIVERED),
               _tok(_ATO_REAL_NO), _tok(_ATO_OD), _tok(_MSNL_SHADOW), _tok(_MSNL_PACK),
               _tok(_EXTERNAL_MSNL_NO),
               r"EXISTING Stage-18\s+semantic-normalization block",
               r"not a new\s+Master Roadmap Stage",
               r"SYSTEM_INFERRED \+ UNVALIDATED and\s+written\s+nowhere",
               r"not\s+a\s+production-provider\s+decision",
               r"OD-3\s+undecided", r"OD-4\s+undecided")
        _rejects(block, path, "sqr1 delivered live", *_SQR1_REVERSALS)
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "sqr1 delivered routing", _tok(_TARGET_AWARE),
               r"ONLY mechanical PHYSICAL_FEASIBILITY:Q2 to specialist input",
               r"the only authorized durable SYSTEM_INFERRED\s+writer",
               r"it hides no unknown and reduces no\s+other question")
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    for needle in ("Safe Question Reduction Slice 1 — the next item of the protected sequence "
                   "recorded in the EXISTING Stage-18 semantic-normalization block, which creates "
                   "no new Master Roadmap Stage — is DELIVERED (PR #701, merge "
                   "`34c0fc372f7374488acda03514e279119b735bc5`",
                   "PR #702, merge `20f27e5100cf9d475ae68d73da7cc17b2ecbf241`",
                   "while the requirement stays outstanding",
                   "a durable SYSTEM_INFERRED writer (other than the deterministic NeedRouting "
                   "record of Slice 1)",
                   "no question reduction beyond Slice 1",
                   "Real invention data is NOT AUTHORIZED FOR EXTERNAL TRANSMISSION."):
        assert needle in head, needle
    raw_checklist = _read(CHECKLIST)
    for line in ("SAFE QUESTION REDUCTION — SLICE 1: DELIVERED — PR #701 — merge "
                 "34c0fc372f7374488acda03514e279119b735bc5",
                 "WEAK-PF RECOVERY: DELIVERED — PR #702 — merge "
                 "20f27e5100cf9d475ae68d73da7cc17b2ecbf241",
                 "MECHANICAL MANDATORY OWNER-VISIBLE QUESTIONS: 9 ON NEW ROUTING-AWARE PROJECTS "
                 "— 10 ON EXISTING PROJECTS",
                 "DURABLE SYSTEM_INFERRED WRITER: NOT AUTHORIZED — EXCEPT DETERMINISTIC NEED "
                 "ROUTING (SLICE 1)"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    assert re.search(r"^ACTIVE CONTRACT: SAFE QUESTION REDUCTION", raw_checklist, re.M) is None
    rows = re.findall(r"^- \[x\] \*\*18 — D13/CAP-01 guidance:\*\*.*$", _read(ROADMAP), re.M)
    assert len(rows) == 1, "stage 18 row missing, duplicated or not ticked (Stage 18 closure)"
    assert ("Safe Question Reduction Slice 1 — mechanical PF:Q2 routed to specialist input on "
            "new routing-aware projects while the requirement stays outstanding — is delivered "
            "(PR #701; the bounded weak-PF recovery PR #702 followed), and the current bounded "
            "action has moved to Stage 21 / CAP-10 Slice 1") in rows[0]


_CAP10_CONTRACT = ("`ACTIVE CONTRACT: CAP-10 SLICE 1 — OWNER-DECLARED CONTRADICTION BETWEEN "
                   "TWO RECORDED ANSWERS`")
_CAP10_DELIVERED = ("`CAP-10 SLICE 1: DELIVERED — PR #703 — merge "
                    "963132ddb78faae58625cd942e44a48e00ba531e`")
_CAP10_REVERSALS = _SQR1_REVERSALS + (
    re.escape(_SQR1_CONTRACT),
    r"FULL CAP-10\W{0,8}(IS )?AUTHORIZED\b",
    # AMENDED at the Stage 21 closure: ONLY the Owner-declared-contradiction-scoped completion is true
    r"STAGE 21(:| IS)?\W{0,4}COMPLETE\b(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?(?:— CURRENT OWNER-DECLARED "
    r"CONTRADICTION SCOPE|for the current Owner-declared contradiction scope))",
    r"CAP-10 (is |slice 1 is )?complete\b",
    r"SYSTEM_INFERRED CONTRADICTION WRITER\W{0,8}(IS )?(AUTHORIZED|ACTIVE)\b",
    r"\b(AI|automatically) detect(s|ed)\b",
    r"contradictions? (is |are )?(validated|verified|resolved)\b(?! or)",
    r"(?<!no )(?<!never )(winner|answer) (is )?(chosen|selected|picked)\b",
    r"Stage 46")


def test_cap10_slice_1_is_delivered_history_and_its_rules_still_bind():
    """CAP-10 Slice 1 (Stage 21) was delivered (PR #703). The guard advances with
    the fact: the section reads DELIVERED and visibly superseded, every rule
    still binds, the live surfaces carry the delivered token, and the slice may
    never again present itself as the live contract or read as anything wider
    than it was. AMENDED at the Stage 21 closure: Stage 21 is COMPLETE for the
    current Owner-declared contradiction scope only, through this slice and its
    own closure; full CAP-10 stays NOT AUTHORIZED.
    """
    contract = _read(CONTRACT)
    top = _section(contract, "current-authority--cap10-slice-1")
    _needs(top, CONTRACT, "cap10 delivered",
           r"Owner-declared contradiction between two recorded answers \(Owner / Lead "
           r"authorization, 2026-09-26\) — DELIVERED \(PR #703\); SUPERSEDED as current "
           r"authority by CAP-08 Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #703, merge `963132ddb78faae58625cd942e44a48e00ba531e`",
           r"Every rule below still binds except where CAP-08 Slice 1 states otherwise",
           r"Stage 21 / CAP-10 is ENTERED / PARTIAL through this one bounded slice",
           r"one `contradiction_declared` record with a canonical `contradiction_endpoints` "
           r"pair — no parallel durable contradiction store",
           r"`OWNER_STATED` / `OWNER_INPUT` · `UNVALIDATED` only",
           r"\*\*SYSTEM_INFERRED CONTRADICTION WRITER\*\* \| `NONE — NOT AUTHORIZED`",
           r"nothing is detected automatically or by AI, the contradiction is not validated, "
           r"no winner is chosen and nothing is resolved",
           r"becomes inactive — never \"resolved\" — once either answer is corrected")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "cap10 delivered",
             *_CAP10_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-10 SLICE 1")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "cap10 delivered live", _tok(_CAP10_DELIVERED),
               _tok(_S21_COMPLETE), _tok("`FULL CAP-10: NOT AUTHORIZED`"),
               _tok("`SYSTEM_INFERRED CONTRADICTION WRITER: NOT AUTHORIZED`"),
               _tok(_SQR1_DELIVERED), _tok(_SQR1_RECOVERY),
               r"OWNER_STATED, UNVALIDATED\s+`contradiction_declared`\s+record",
               r"no\s+gap,\s+maturity,\s+progression,\s+scoring\s+or\s+NeedRouting\s+authority")
        _rejects(block, path, "cap10 delivered live", *_CAP10_REVERSALS,
                 re.escape(_CAP10_CONTRACT))
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "cap10 delivered routing",
               r"the Stage-21 checkbox is ticked for the current Owner-declared contradiction scope only",
               r"entering Stage 21 completed nothing in Stages 18–20")
        _rejects(routing, path, "cap10 delivered routing", r"The Stage-21 checkbox stays\s+unticked")
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    for needle in ("CAP-10 Slice 1 — Stage 21 / CAP-10 ENTERED / PARTIAL through the "
                   "Owner-declared contradiction between two recorded answers",
                   "no automatic or AI detection, no validation, no winner, no resolution, no "
                   "SYSTEM_INFERRED contradiction writer) — is DELIVERED (PR #703, merge "
                   "`963132ddb78faae58625cd942e44a48e00ba531e`)"):
        assert needle in head, needle
    assert "ACTIVE CONTRACT: CAP-10 SLICE 1" not in head
    raw_checklist = _read(CHECKLIST)
    for line in ("CAP-10 SLICE 1: DELIVERED — PR #703 — merge "
                 "963132ddb78faae58625cd942e44a48e00ba531e",
                 "STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE",
                 "FULL CAP-10: NOT AUTHORIZED",
                 "SYSTEM_INFERRED CONTRADICTION WRITER: NOT AUTHORIZED",
                 "Stage 21 entered / partial — CAP-10 Slice 1 only (Owner-declared contradiction "
                 "between two recorded answers; delivered, PR #703); full CAP-10 not "
                 "authorized"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    assert re.search(r"^ACTIVE CONTRACT: CAP-10 SLICE 1", raw_checklist, re.M) is None
    # the row is ticked by the Stage 21 closure for the current Owner-declared contradiction scope only
    rows = re.findall(r"^- \[x\] \*\*21 — CAP-10:\*\*.*$", _read(ROADMAP), re.M)
    assert len(rows) == 1, "stage 21 row missing, duplicated or unticked"
    assert "**ENTERED / PARTIAL (2026-09-26):** CAP-10 Slice 1" in rows[0]
    assert "Delivered (PR #703, merge `963132ddb78faae58625cd942e44a48e00ba531e`)." in rows[0]
    assert "Full CAP-10 NOT AUTHORIZED." in rows[0]
    assert "the checkbox stays unticked" not in _live_only(rows[0])
    for pat in _CAP10_REVERSALS:
        assert re.search(pat, rows[0], re.I) is None, pat
    register = _flat(os.path.join("docs", "governance",
                                  "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"))
    assert "CAP-10 Slice 1 (Stage 21, 2026-09-26)" in register
    assert "`FULL CAP-10: NOT AUTHORIZED`" in register


_CAP08_CONTRACT = ("`ACTIVE CONTRACT: CAP-08 SLICE 1 — OWNER-DECLARED ASSUMPTION → ANSWER "
                   "DEPENDENCY`")
_CAP08_REVERSALS = (
    re.escape(_CAP10_CONTRACT), re.escape(_SQR1_CONTRACT),
    r"FULL CAP-08\W{0,8}(IS )?AUTHORIZED\b",
    # AMENDED at the Stage 20 closure: ONLY the Owner-declared-assumption-scoped completion is true
    r"STAGE 20(:| IS)?\W{0,4}COMPLETE\b(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?(?:— CURRENT OWNER-DECLARED ASSUMPTION "
    r"SCOPE|for the current Owner-declared assumption scope))",
    r"CAP-08 (is |slice 1 is )?complete\b",
    r"(AUTOMATIC|AI) (/ AI )?DEPENDENCY INFERENCE\W{0,8}(IS )?(AUTHORIZED|ACTIVE)\b",
    r"\b(AI|automatically) infer(s|red)? (the )?dependenc",
    r"dependenc(y|ies) (is |are )?inferred\b",
    r"(?<!nothing is )inferred (automatically|by AI)\b",
    r"dependenc(y|ies) (is |are )?(validated|verified|confirmed|rejected|resolved)\b",
    r"(?<!no )(?<!never )evidence-needed metadata (is |are )?recorded\b",
    r"(?<!no )(?<!never )(readiness|progression) authority\b(?! and)",
    r"Stage 46")


_CAP08_DELIVERED = ("`CAP-08 SLICE 1: DELIVERED — PR #704 — merge "
                    "56eea683138a7880e836c7d577faf3f289beb22b`")


def test_cap08_slice_1_is_delivered_history_and_its_rules_still_bind():
    """CAP-08 Slice 1 (Stage 20) was delivered (PR #704). The guard advances with
    the fact: the section reads DELIVERED and visibly superseded, every rule
    still binds, the live surfaces carry the delivered token, and the slice may
    never again present itself as the live contract or read as anything wider
    than it was. AMENDED at the Stage 20 closure: Stage 20 is COMPLETE for the
    current Owner-declared assumption scope only, through this slice and its own
    closure; full CAP-08 stays NOT AUTHORIZED.
    """
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--cap08-slice-1"))
    _needs(top, CONTRACT, "cap08 delivered",
           r"Owner-declared assumption → answer dependency \(Owner / Lead authorization, "
           r"2026-09-26\) — DELIVERED \(PR #704\); SUPERSEDED as current authority by Stage 22 "
           r"/ CAP-05 \+ CAP-07 Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #704, merge `56eea683138a7880e836c7d577faf3f289beb22b`",
           r"Every rule below still binds except where Stage 22 / CAP-05 \+ CAP-07 Slice 1 "
           r"states otherwise",
           r"Stage 20 / CAP-08 is ENTERED / PARTIAL through this one bounded slice",
           r"one `assumption_dependency_declared` record per DIRECTED edge "
           r"\(`assumption_record_id` → `dependent_answer_record_id`\) — no parallel durable "
           r"dependency graph",
           r"`OWNER_STATED` / `OWNER_INPUT` · `UNVALIDATED` only · no evidence-needed metadata",
           r"\*\*AUTOMATIC / AI DEPENDENCY INFERENCE\*\* \| `NONE — NOT AUTHORIZED`",
           r"recorded previously, but none is currently active",
           r"the same identity with different material fails closed")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "cap08 delivered",
             *_CAP08_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-08 SLICE 1")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "cap08 delivered live", _tok(_CAP08_DELIVERED),
               _tok(_S20_COMPLETE), _tok("`FULL CAP-08: NOT AUTHORIZED`"),
               _tok("`AUTOMATIC / AI DEPENDENCY INFERENCE: NOT AUTHORIZED`"),
               _tok(_CAP10_DELIVERED),
               r"OWNER_STATED, UNVALIDATED\s+`assumption_dependency_declared`\s+record\s+per"
               r"\s+directed\s+assumption\s+→\s+answer\s+edge",
               r"no\s+readiness,\s+gap,\s+maturity,\s+progression,\s+scoring,\s+NeedRouting"
               r"\s+or\s+validation-award\s+authority")
        _rejects(block, path, "cap08 delivered live", *_CAP08_REVERSALS,
                 re.escape(_CAP08_CONTRACT))
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "cap08 delivered routing",
               r"the Stage-20 checkbox is ticked for the current Owner-declared assumption scope only",
               r"entering Stage 20 completed nothing in Stages 18–19")
        _rejects(routing, path, "cap08 delivered routing", r"The Stage-20 checkbox stays\s+unticked")
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    for needle in ("CAP-08 Slice 1 — Stage 20 / CAP-08 ENTERED / PARTIAL through the "
                   "Owner-declared assumption → answer dependency",
                   "is DELIVERED (PR #704, merge `56eea683138a7880e836c7d577faf3f289beb22b`)"):
        assert needle in head, needle
    assert "ACTIVE CONTRACT: CAP-08 SLICE 1" not in head
    raw_checklist = _read(CHECKLIST)
    for line in ("CAP-08 SLICE 1: DELIVERED — PR #704 — merge "
                 "56eea683138a7880e836c7d577faf3f289beb22b",
                 "STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE",
                 "FULL CAP-08: NOT AUTHORIZED",
                 "AUTOMATIC / AI DEPENDENCY INFERENCE: NOT AUTHORIZED",
                 "Stage 20 entered / partial — CAP-08 Slice 1 only (Owner-declared assumption → "
                 "answer dependency; delivered, PR #704); full CAP-08 not authorized"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    assert re.search(r"^ACTIVE CONTRACT: CAP-08 SLICE 1", raw_checklist, re.M) is None
    # the row is ticked by the Stage 20 closure for the current Owner-declared assumption scope only
    rows = re.findall(r"^- \[x\] \*\*20 — CAP-08:\*\*.*$", _read(ROADMAP), re.M)
    assert len(rows) == 1, "stage 20 row missing, duplicated or unticked"
    assert "**ENTERED / PARTIAL (2026-09-26):** CAP-08 Slice 1" in rows[0]
    assert "Delivered (PR #704, merge `56eea683138a7880e836c7d577faf3f289beb22b`)." in rows[0]
    assert "Full CAP-08 NOT AUTHORIZED." in rows[0]
    assert "the checkbox stays unticked" not in _live_only(rows[0])
    for pat in _CAP08_REVERSALS:
        assert re.search(pat, rows[0], re.I) is None, pat
    register = _flat(os.path.join("docs", "governance",
                                  "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"))
    assert "CAP-08 Slice 1 (Stage 20, 2026-09-26)" in register
    assert "`FULL CAP-08: NOT AUTHORIZED`" in register


_STAGE22_CONTRACT = ("`ACTIVE CONTRACT: CAP-05 + CAP-07 SLICE 1 — READ-ONLY DECISION TRACE + "
                     "PROJECT CONTEXT PANEL`")
_STAGE22_REVERSALS = (
    re.escape(_CAP08_CONTRACT), re.escape(_CAP10_CONTRACT), re.escape(_SQR1_CONTRACT),
    r"FULL CAP-0[57]\W{0,8}(IS )?AUTHORIZED\b",
    # AMENDED at the Stage 22 closure: ONLY the bounded-decision-trace + decision-room-scoped completion is true
    r"STAGE 22(:| IS)?\W{0,4}COMPLETE\b(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?(?:— CURRENT BOUNDED DECISION TRACE "
    r"\+ DECISION ROOM SCOPE|for the current bounded decision trace \+ decision room scope))",
    r"CAP-0[57] (is |slice 1 is )?complete\b",
    r"(?<!no )(?<!not )(best|recommended) (alternative|option) (is )?(selected|chosen|shown)\b",
    r"(?<!no )confidence score (is )?(shown|computed|recorded)\b",
    r"(?<!no )(?<!not )(supports|undermines) (this|the|a) (decision|alternative)\b",
    r"project context (is )?(linked to|evidence for)\b",
    r"(?<!no )decision relationships? (is |are )?inferred\b",
    r"Stage 46")


_STAGE22_SLICE1_DELIVERED = ("`CAP-05 + CAP-07 SLICE 1: DELIVERED — PR #706 — merge "
                             "f391fc530b9b828b54e56fb9f73e56ef6a7ce6e4`")


def test_stage22_slice_1_is_delivered_history_and_its_rules_still_bind():
    """Stage 22 / CAP-05 + CAP-07 Slice 1 was delivered (PR #706). Its section
    reads DELIVERED and visibly superseded, every rule still binds, the live
    surfaces carry the delivered token and never again "PR / merge pending"."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--stage22-slice-1"))
    _needs(top, CONTRACT, "stage22 slice1 delivered",
           r"Read-only decision trace \+ project context panel \(Owner / Lead authorization, "
           r"2026-09-26\) — DELIVERED \(PR #706\); SUPERSEDED as current authority by Stage 22 "
           r"/ CAP-05 \+ CAP-07 Slice 2",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #706, merge `f391fc530b9b828b54e56fb9f73e56ef6a7ce6e4`",
           r"Every rule below still binds except where Slice 2 states otherwise",
           r"Status: DELIVERED \(PR #706\)",
           r"explicitly NOT LINKED to any specific decision",
           r"\*\*DECISION LINKAGE / INFERENCE\*\* \| `NONE`",
           r"\*\*EVIDENCE STRENGTH / CONFIDENCE / RECOMMENDATION\*\* \| `NONE`")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "stage22 slice1 delivered",
             *_STAGE22_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-05 \+ CAP-07 SLICE 1",
             r"INDEPENDENT UX-BEHAVIOUR REVIEW PASS — PR / merge pending")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "stage22 slice1 delivered live", _tok(_STAGE22_SLICE1_DELIVERED),
               r"explicitly\s+NOT\s+LINKED\s+to\s+any\s+specific\s+decision")
        _rejects(block, path, "stage22 slice1 delivered live",
                 re.escape(_STAGE22_CONTRACT),
                 r"(?<!CAP-0[24] )(?<!CAP-11 )SLICE 1: IMPLEMENTED — INDEPENDENT UX / BEHAVIOUR REVIEW PASS — "
                 r"PR / MERGE PENDING")
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert "Slice 1 — DELIVERED (PR #706, merge `f391fc530b9b828b54e56fb9f73e56ef6a7ce6e4`)" in head
    assert "ACTIVE CONTRACT: CAP-05 + CAP-07 SLICE 1" not in head
    assert "its PR / merge is pending. CAP-08" not in head
    raw_checklist = _read(CHECKLIST)
    assert re.search(r"^CAP-05 \+ CAP-07 SLICE 1: DELIVERED — PR #706 — merge "
                     r"f391fc530b9b828b54e56fb9f73e56ef6a7ce6e4$", raw_checklist, re.M)
    assert re.search(r"^ACTIVE CONTRACT: CAP-05 \+ CAP-07 SLICE 1", raw_checklist, re.M) is None
    # AMENDED at the Stage 22 closure: the row is ticked for the current bounded decision trace + decision room scope
    rows = re.findall(r"^- \[x\] \*\*22 — CAP-05 \+ CAP-07:\*\*.*$", _read(ROADMAP), re.M)
    assert len(rows) == 1
    assert "Delivered (PR #706, merge `f391fc530b9b828b54e56fb9f73e56ef6a7ce6e4`)." in rows[0]


_STAGE22_SLICE2_CONTRACT = ("`ACTIVE CONTRACT: CAP-05 + CAP-07 SLICE 2 — ACTIONABLE DECISION "
                            "ROOM SUMMARY`")
_STAGE22_SLICE2_STATUS = ("`SLICE 2: IMPLEMENTED — CORRECTION 01 — INDEPENDENT UX / BEHAVIOUR "
                          "VERIFICATION PASS — PR / MERGE PENDING`")
_STAGE22_SLICE2_REVERSALS = _STAGE22_REVERSALS + (
    re.escape(_STAGE22_CONTRACT),
    r"(?<!no )(?<!not )actions? (is |are )?(ranked|prioriti[sz]ed)\b",
    r"(?<!no )(?<!not )(STAGE 23|Stage 23)(:| is)?\W{0,4}(ENTERED|AUTHORIZED)\b",
    # AMENDED at the Stage 23 closure: the negated token `NO SINGLE READINESS SCORE …` is not a score claim
    r"(?<!no )(?<!no single )readiness score\b")


_STAGE22_SLICE2_DELIVERED = ("`CAP-05 + CAP-07 SLICE 2: DELIVERED — PR #707 — merge "
                             "d5068f83d46bdf2b3b28ceeb3f0e4e78fd32cdbe`")


def test_stage22_slice_2_is_delivered_history_and_its_rules_still_bind():
    """Stage 22 / CAP-05 + CAP-07 Slice 2 was delivered (PR #707, merge
    d5068f8). Its section reads DELIVERED and visibly superseded, every rule
    still binds, the live surfaces carry the delivered token and never again
    "PR / merge pending" or the Slice 2 contract as current. AMENDED at the
    Stage 22 closure: Stage 22 is COMPLETE for the current bounded decision
    trace + decision room scope only, through Slices 1–2 and its own closure
    with no product change; full CAP-05 / CAP-07 stay NOT AUTHORIZED."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--stage22-slice-2"))
    _needs(top, CONTRACT, "stage22 slice2 delivered",
           r"Actionable Decision Room Summary \(Owner / Lead authorization, 2026-09-26\) — "
           r"DELIVERED \(PR #707\); SUPERSEDED as current authority by CAP-04 Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #707, merge `d5068f83d46bdf2b3b28ceeb3f0e4e78fd32cdbe`",
           r"Every rule below still binds except where CAP-04 Slice 1 states otherwise",
           r"TARGETED INDEPENDENT VERIFICATION PASS — DELIVERED \(PR #707\)",
           r"`OWNER_EXECUTABLE`, `SPECIALIST_REQUIRED`, `EMPIRICAL_EVIDENCE_REQUIRED`, "
           r"`SYSTEM_DERIVABLE`",
           r"reused unchanged; no action ranking is created",
           r"\*\*DECISION LINKAGE\*\* \| `NONE`",
           r"\*\*RECOMMENDATION / CONFIDENCE / EVIDENCE STRENGTH / READINESS\*\* \| `NONE`",
           r"\*\*FORM / QUESTION / ROUTE / WRITER / PERSISTENCE\*\* \| `NONE`")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "stage22 slice2 delivered",
             *_STAGE22_SLICE2_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-05 \+ CAP-07 SLICE 2",
             r"PR / merge pending")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "stage22 slice2 delivered live", _tok(_STAGE22_SLICE2_DELIVERED),
               _tok("`STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE + DECISION ROOM SCOPE`"),
               _tok("`FULL CAP-05: NOT AUTHORIZED`"),
               _tok("`FULL CAP-07: NOT AUTHORIZED`"),
               r"grouped\s+strictly\s+by\s+its\s+responsibility\s+tokens")
        _rejects(block, path, "stage22 slice2 delivered live",
                 re.escape(_STAGE22_SLICE2_CONTRACT), re.escape(_STAGE22_SLICE2_STATUS),
                 *_STAGE22_SLICE2_REVERSALS)
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "stage22 slice2 routing",
               r"the Stage-22 checkbox is ticked for the current bounded decision trace \+ decision room scope only",
               r"entering Stage 22 completed nothing in Stages 18–21")
        _rejects(routing, path, "stage22 slice2 routing", r"The Stage-22 checkbox stays\s+unticked",
                 _tok("`STAGE 22: ENTERED / PARTIAL`"))
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("Slice 2 — DELIVERED (PR #707, merge `d5068f83d46bdf2b3b28ceeb3f0e4e78fd32cdbe`)"
            in head)
    # AMENDED at the Stage 22 closure: entry is history; completion is scoped to the bounded closure
    assert "Stage 22 / CAP-05 + CAP-07 was ENTERED / PARTIAL through bounded slices" in head
    assert "Stage 22 / CAP-05 + CAP-07 is ENTERED / PARTIAL" not in head
    assert "ACTIVE CONTRACT: CAP-05 + CAP-07 SLICE 2" not in head
    assert "PR / merge is pending. Slice 1" not in head
    assert ("the former Stage-22 CAP-05 + CAP-07 Slice 2, the former Stage-22 CAP-05 + CAP-07 "
            "Slice 1, CAP-08 Slice 1, CAP-10 Slice 1" in claude)
    raw_checklist = _read(CHECKLIST)
    for line in ("STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE + DECISION ROOM SCOPE",
                 _STAGE22_SLICE2_DELIVERED.strip("`"),
                 "FULL CAP-05: NOT AUTHORIZED", "FULL CAP-07: NOT AUTHORIZED",
                 # AMENDED at the Stage 23 closure: Stage 23 is complete for its bounded four-axis scope;
                 # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 entered / partial
                 # AMENDED at the Stage 24 closure: Stage 24 complete for its bounded scope
                 "Stage 24 complete for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only; full CAP-12 "
                 "not authorized",
                 # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 entered /
                 # partial for that slice only; 26–27 preserved
                 "Stage 25 entered / partial — CAP-13 Two-Support Static Reactions Slice 1 delivered; full CAP-13 not "
                 "authorized",
                 # AMENDED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: Stage 27 entered /
                 # partial for that slice only; 26 preserved
                 "Stage 26 preserved, not entered / not authorized",
                 # AMENDED at the Stage 27 closure: Stage 27 complete for its current bounded scope only
                 "Stage 27 complete for the current bounded THERM-01 single-path temperature-difference scope only; full "
                 "THERM-01 not authorized"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    for stale in ("ACTIVE CONTRACT: CAP-05 + CAP-07 SLICE 2", _STAGE22_SLICE2_STATUS.strip("`"),
                  "STAGE 22: ENTERED / PARTIAL — CAP-05 + CAP-07 SLICES 1–2 ONLY"):
        assert re.search(r"^" + re.escape(stale), raw_checklist, re.M) is None, stale
    roadmap = _read(ROADMAP)
    # the row is ticked by the Stage 22 closure for the current bounded decision trace + decision room scope only
    rows = re.findall(r"^- \[x\] \*\*22 — CAP-05 \+ CAP-07:\*\*.*$", roadmap, re.M)
    assert len(rows) == 1, "stage 22 row missing, duplicated or unticked"
    row = re.sub(r"\*\(Superseded.*?\)\*", "", rows[0])
    assert "**Slice 2 (2026-09-26):** an Actionable Decision Room Summary" in row
    assert "Delivered (PR #707, merge `d5068f83d46bdf2b3b28ceeb3f0e4e78fd32cdbe`)." in row
    assert "PR / merge pending" not in row
    assert "Full CAP-05 and full CAP-07 NOT AUTHORIZED." in row
    assert "the checkbox stays unticked" not in row
    for pat in _STAGE22_SLICE2_REVERSALS:
        assert re.search(pat, row, re.I) is None, pat
    register = _flat(os.path.join("docs", "governance",
                                  "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"))
    assert "Slice 2 (2026-09-26; delivered, PR #707) adds a read-only" in register
    assert "SLICE 2 AUTHORIZED" not in register
    assert "`FULL CAP-05: NOT AUTHORIZED`" in register
    assert "`FULL CAP-07: NOT AUTHORIZED`" in register


_CAP04_CONTRACT = "`ACTIVE CONTRACT: CAP-04 SLICE 1 — ACTIONABLE GAP PACK`"
_CAP04_STATUS = ("`CAP-04 SLICE 1: IMPLEMENTED — INDEPENDENT UX / BEHAVIOUR REVIEW PASS — PR / "
                 "MERGE PENDING`")
_CAP04_REVERSALS = _STAGE22_SLICE2_REVERSALS + (
    re.escape(_STAGE22_SLICE2_CONTRACT),
    r"FULL CAP-04\W{0,8}(IS )?AUTHORIZED\b",
    r"CAP-04 (is |slice 1 is )?complete\b",
    r"(?<!no )(?<!not )CAP-06\W{0,8}(IS )?(ACTIVE|ACTIVATED|AUTHORIZED)\b",
    r"(?<!no )(?<!not )(gaps?|packs?|actions?) (is |are )?(ranked|scored|prioriti[sz]ed)\b",
    r"(?<!no )(?<!not )(pack|action pack) (is |counts as )?evidence\b",
    r"(?<!no )(?<!not )(pack|action pack) closes (a|the) gap\b")


_CAP04_DELIVERED = ("`CAP-04 SLICE 1: DELIVERED — PR #708 — merge "
                    "78f6a73113ff9eaa9c5e0941b2bd857595899404`")


def test_cap04_slice_1_is_delivered_history_and_its_rules_still_bind():
    """CAP-04 Slice 1 was delivered (PR #708, merge 78f6a73). Its section reads
    DELIVERED and visibly superseded, every rule still binds, full CAP-04 stays
    NOT AUTHORIZED, and no live surface presents it as the current contract or
    as "PR / merge pending" again."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--cap04-slice-1"))
    _needs(top, CONTRACT, "cap04 slice1 delivered",
           r"Actionable Gap Pack \(Owner / Lead authorization, 2026-09-27\) — DELIVERED "
           r"\(PR #708\); SUPERSEDED as current authority by CAP-02 Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #708, merge `78f6a73113ff9eaa9c5e0941b2bd857595899404`",
           r"Every rule below still binds except where CAP-02 Slice 1 states otherwise",
           r"material findings: NONE — DELIVERED \(PR #708\)",
           r"It creates no new Master Roadmap Stage, Stage 23 is NOT ENTERED, and full CAP-04 is "
           r"NOT AUTHORIZED",
           r"a RETRACTED route does not render; a route / policy mismatch fails closed",
           r"\*\*RANKING / SCORE / SEVERITY / FEASIBILITY / READINESS / PROGRESSION\*\* \| `NONE`")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "cap04 slice1 delivered",
             *_CAP04_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-04 SLICE 1", r"PR / merge pending")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "cap04 slice1 delivered live", _tok(_CAP04_DELIVERED),
               _tok("`FULL CAP-04: NOT AUTHORIZED`"),
               r"an\s+ACCEPTED_RISK\s+gap\s+gets\s+no\s+pack\s+and\s+stays\s+explicitly\s+not\s+"
               r"resolved\s+and\s+not\s+validated",
               r"a\s+RETRACTED\s+route\s+does\s+not\s+render")
        _rejects(block, path, "cap04 slice1 delivered live", re.escape(_CAP04_CONTRACT),
                 re.escape(_CAP04_STATUS), *_CAP04_REVERSALS)
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("CAP-04 Slice 1 — DELIVERED (PR #708, merge "
            "`78f6a73113ff9eaa9c5e0941b2bd857595899404`; full CAP-04 NOT AUTHORIZED)" in head)
    assert "ACTIVE CONTRACT: CAP-04 SLICE 1" not in head
    assert "the former CAP-04 Slice 1, the former Stage-22 CAP-05 + CAP-07 Slice 2" in claude
    raw_checklist = _read(CHECKLIST)
    for line in (_CAP04_DELIVERED.strip("`"), "FULL CAP-04: NOT AUTHORIZED"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    for stale in ("ACTIVE CONTRACT: CAP-04 SLICE 1", _CAP04_STATUS.strip("`")):
        assert re.search(r"^" + re.escape(stale), raw_checklist, re.M) is None, stale
    register = _flat(os.path.join("docs", "governance",
                                  "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"))
    assert "CAP-04 Slice 1 — Actionable Gap Pack (2026-09-27; no new Master Roadmap Stage)" in register
    assert "progression authority. Delivered (PR #708). `FULL CAP-04: NOT AUTHORIZED`." in register
    assert "Actionable Gap Pack (implemented, review PASS, PR / merge pending)" not in register


_CAP02_CONTRACT = ("`ACTIVE CONTRACT: CAP-02 SLICE 1 — PROJECT COMPASS / SIMPLIFIED ONE-STEP "
                   "JOURNEY`")
_CAP02_STATUS = ("`CAP-02 SLICE 1: IMPLEMENTED — INDEPENDENT UX / BEHAVIOUR REVIEW PASS — PR / "
                 "MERGE PENDING`")
_CAP02_REVERSALS = _CAP04_REVERSALS + (
    re.escape(_CAP04_CONTRACT),
    r"FULL CAP-02\W{0,8}(IS )?AUTHORIZED\b",
    r"CAP-02 (is |slice 1 is )?complete\b",
    r"(?<!ONE )(?<!one )(two|second|multiple) primary (journey )?(action|CTA)s?\b(?! ?(is|are) (not|never))",
    r"(?<!no )(?<!not )(report|PDF) (gains|shows|carries) the (Project )?Compass\b")


_CAP02_DELIVERED = ("`CAP-02 SLICE 1: DELIVERED — PR #709 — merge "
                    "a9e46e57e1d9595fdc92af0bb508ee3fd141c9ea`")


def test_cap02_slice_1_is_delivered_history_and_its_rules_still_bind():
    """CAP-02 Slice 1 was delivered (PR #709, merge a9e46e5). Its section reads
    DELIVERED and visibly superseded, every rule still binds (ONE primary
    journey action), full CAP-02 stays NOT AUTHORIZED, and no live surface
    presents it as the current contract or as "PR / merge pending" again."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--cap02-slice-1"))
    _needs(top, CONTRACT, "cap02 slice1 delivered",
           r"Simplified One-Step Journey \(Owner / Lead authorization, 2026-09-27\) — "
           r"DELIVERED \(PR #709\); SUPERSEDED as current authority by CAP-11 Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #709, merge `a9e46e57e1d9595fdc92af0bb508ee3fd141c9ea`",
           r"Every rule below still binds except where CAP-11 Slice 1 states otherwise",
           r"material findings: NONE — DELIVERED \(PR #709\)",
           r"exactly ONE primary journey action \(a protected product rule\)",
           r"\*\*REPORT / PDF\*\* \| unchanged — not part of this slice")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "cap02 slice1 delivered",
             *_CAP02_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-02 SLICE 1", r"PR / merge pending")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "cap02 slice1 delivered live", _tok(_CAP02_DELIVERED),
               _tok("`FULL CAP-02: NOT AUTHORIZED`"),
               r"exactly\s+ONE\s+primary\s+journey\s+action")
        _rejects(block, path, "cap02 slice1 delivered live", re.escape(_CAP02_CONTRACT),
                 re.escape(_CAP02_STATUS), *_CAP02_REVERSALS)
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("CAP-02 Slice 1 — DELIVERED (PR #709, merge "
            "`a9e46e57e1d9595fdc92af0bb508ee3fd141c9ea`; full CAP-02 NOT AUTHORIZED)" in head)
    assert "ACTIVE CONTRACT: CAP-02 SLICE 1" not in head
    assert "the former CAP-02 Slice 1, the former CAP-04 Slice 1" in claude
    raw_checklist = _read(CHECKLIST)
    for line in (_CAP02_DELIVERED.strip("`"), "FULL CAP-02: NOT AUTHORIZED"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    for stale in ("ACTIVE CONTRACT: CAP-02 SLICE 1", _CAP02_STATUS.strip("`")):
        assert re.search(r"^" + re.escape(stale), raw_checklist, re.M) is None, stale
    register = _flat(os.path.join("docs", "governance",
                                  "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"))
    assert "action; session only. Delivered (PR #709). `FULL CAP-02: NOT AUTHORIZED`." in register
    assert "Slice 1 Project Compass (implemented, review PASS, PR / merge pending)" not in register


_CAP11_CONTRACT_PATH = os.path.join("docs", "governance",
                                    "CAP11_EVIDENCE_DETAILS_ENTRY_CONTRACT.md")
_CAP11_CONTRACT = "`ACTIVE CONTRACT: CAP-11 SLICE 1 — EVIDENCE DETAILS`"
_CAP11_STATUS = ("`CAP-11 SLICE 1: IMPLEMENTED — INDEPENDENT UX / BEHAVIOUR REVIEW PASS — PR / "
                 "MERGE PENDING`")
_CAP11_REVERSALS = _CAP02_REVERSALS + (
    re.escape(_CAP02_CONTRACT),
    r"FULL CAP-11\W{0,8}(IS )?AUTHORIZED\b",
    r"CAP-11 (is |slice 1 is )?complete\b",
    r"(?<!no )(?<!not )(?<!never )(combined|overall) (evidence )?(score|rank|ranking|tier)\b",
    r"(?<!no )(?<!not )evidence (score|strength score|tier) (is )?(shown|computed|displayed)\b",
    r"(?<!no )(?<!not )validation writer (is )?(authorized|added|active)\b")


_CAP11_DELIVERED = ("`CAP-11 SLICE 1: DELIVERED — PR #710 — merge "
                    "7d2e9ab011a0bbf17b577f354e2b47ab09114add`")


def test_cap11_slice_1_is_delivered_history_and_its_rules_still_bind():
    """CAP-11 Slice 1 — Evidence Details — was delivered (PR #710, merge
    7d2e9ab). Its section reads DELIVERED and visibly superseded, every rule
    still binds (three independent axes, no combined score, no writer or
    readiness authority), full CAP-11 stays NOT AUTHORIZED, and no live surface
    presents it as the current contract or as "PR / merge pending" again."""
    assert os.path.isfile(_CAP11_CONTRACT_PATH)
    cap11 = _read(_CAP11_CONTRACT_PATH)
    for needle in ("# CAP-11 — EVIDENCE QUALITY LADDER",
                   "## ENTRY CONTRACT + SLICE 1 — EVIDENCE DETAILS",
                   "**FULL CAP-11: NOT AUTHORIZED.**"):
        assert needle in cap11, needle
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--cap11-slice-1"))
    _needs(top, CONTRACT, "cap11 slice1 delivered",
           r"Evidence Details \(Owner approval of the CAP-11 entry contract, 2026-09-27\) — "
           r"DELIVERED \(PR #710\); SUPERSEDED as current authority by CAP-09 Slice 3",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #710, merge `7d2e9ab011a0bbf17b577f354e2b47ab09114add`",
           r"Every rule below still binds except where CAP-09 Slice 3 states otherwise",
           r"material findings: NONE — DELIVERED \(PR #710\)",
           re.escape("`docs/governance/CAP11_EVIDENCE_DETAILS_ENTRY_CONTRACT.md`"),
           r"Stage 23 is NOT ENTERED, CAP-06 is NOT ACTIVATED, and FULL CAP-11 is NOT AUTHORIZED",
           r"report Section 2 \(Known Problem, Known Mechanism\) and the PDF only",
           r"three rows — Form, Source, Validation",
           r"stay independent; no provenance or Form value grants validation",
           r"\*\*SCORE / RANK / TIER / CONFIDENCE / CROSS-AXIS LADDER\*\* \| `NONE`",
           r"\*\*WRITERS / PROMOTION / READINESS AUTHORITY\*\* \| `NONE`",
           r"Section 9, the session page, safety signals, Commercial / Manufacturing evidence")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "cap11 slice1 delivered",
             *_CAP11_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-11 SLICE 1", r"PR / merge pending")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "cap11 slice1 delivered live", _tok(_CAP11_DELIVERED),
               _tok("`FULL CAP-11: NOT AUTHORIZED`"),
               r"CAP11_EVIDENCE_DETAILS_ENTRY_CONTRACT\.md",
               r"THREE\s+independent\s+rows\s+—\s+Form,\s+Source\s+and\s+Validation",
               r"never\s+combined\s+into\s+a\s+score",
               r"no\s+validation,\s+provenance,\s+quality\s+or\s+promotion\s+writer\s+and\s+no\s+"
               r"readiness\s+authority",
               r"Section\s+9,\s+the\s+session\s+page")
        _rejects(block, path, "cap11 slice1 delivered live", re.escape(_CAP11_CONTRACT),
                 _tok(_CAP11_STATUS), *_CAP11_REVERSALS)
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("CAP-11 Slice 1 — DELIVERED (PR #710, merge "
            "`7d2e9ab011a0bbf17b577f354e2b47ab09114add`; full CAP-11 NOT AUTHORIZED)" in head)
    assert "ACTIVE CONTRACT: CAP-11 SLICE 1" not in head
    assert "the former CAP-11 Slice 1, the former CAP-02 Slice 1" in claude
    raw_checklist = _read(CHECKLIST)
    for line in (_CAP11_DELIVERED.strip("`"), "FULL CAP-11: NOT AUTHORIZED"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    for stale in ("ACTIVE CONTRACT: CAP-11 SLICE 1", _CAP11_STATUS.strip("`")):
        assert re.search(r"^" + re.escape(stale), raw_checklist, re.M) is None, stale
    register = _flat(os.path.join("docs", "governance",
                                  "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"))
    assert "CAP-11 Slice 1 — Evidence Details (2026-09-27; no new Master Roadmap Stage)" in register
    assert "The recorded long-term ladder hierarchy above is NOT implemented" in register
    assert ("Delivered (PR #710, merge `7d2e9ab011a0bbf17b577f354e2b47ab09114add`). "
            "`FULL CAP-11: NOT AUTHORIZED`.") in register
    assert "Evidence Details under the approved entry contract (implemented, review PASS, PR / " \
        "merge pending)" not in register


_CAP09S3_CONTRACT = "`ACTIVE CONTRACT: CAP-09 SLICE 3 — OWNER-DEFINED TEST HYPOTHESIS`"
_CAP09S3_STATUS = ("`CAP-09 SLICE 3: IMPLEMENTED — UX / BEHAVIOUR REVIEW PASS — ASTRA "
                   "ARCHITECTURE REVIEW PASS — PR / MERGE PENDING`")
_CAP09S3_REVERSALS = _CAP11_REVERSALS + (
    re.escape(_CAP11_CONTRACT),
    r"FULL (CAP-09|WS-PFV-001)\W{0,8}(IS )?AUTHORIZED\b",
    r"\bVARIABLE\W{0,8}(IS )?AUTHORIZED\b",
    r"\bRESULT\W{0,8}(IS )?AUTHORIZED\b",
    r"(?<!no )(?<!not )Test Hypothesis (is|counts as|becomes|creates) (an? )?"
    r"(Evidence|test result|result|validation|validated|readiness)\b",
    r"planning (save|transaction)[^.]{0,60}\b(non-atomic|not atomic|partial(ly)? commit)",
    r"STAGE 23\W{0,8}(IS )?ENTERED\b",
    r"CAP-06\W{0,8}(IS )?(ACTIVATED|ACTIVE)\b",
    r"STAGE 19\W{0,8}(IS )?COMPLETE\b(?!\s+(?:— CURRENT PLANNING-ONLY SCOPE|for the current planning-only scope))",
    r"CAP-11 SLICE 1: IMPLEMENTED")


_CAP09S3_DELIVERED = ("`CAP-09 SLICE 3: DELIVERED — PR #711 — merge "
                      "e393e29cd0ba4f568cf1fd1a0d4c2e0e7742eabd`")


def test_cap09_slice_3_is_delivered_history_and_its_rules_still_bind():
    """CAP-09 Slice 3 — Owner-defined Test Hypothesis — was delivered (PR #711,
    merge e393e29). Its section reads DELIVERED and visibly superseded, its
    rules still bind, and no live surface presents it as the current contract
    or as "PR / merge pending" again."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--cap09-slice-3"))
    _needs(top, CONTRACT, "cap09 slice3 delivered",
           r"Owner-Defined Test Hypothesis \(Owner / Lead authorization, 2026-09-27\) — "
           r"DELIVERED \(PR #711\); SUPERSEDED as current authority by CAP-09 Slice 4",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #711, merge `e393e29cd0ba4f568cf1fd1a0d4c2e0e7742eabd`",
           r"Every rule below still binds except where CAP-09 Slice 4 states otherwise",
           r"material findings: NONE — DELIVERED \(PR #711\)",
           r"\*\*IDENTITY\*\* \| the canonical `experiment_id` stays the only experiment identity",
           r"`prototype_test_hypotheses` \(project_id, experiment_id, inventor-authored text only\)",
           r"PLANNING METADATA ONLY — never generated, inferred or graded; no Evidence, test "
           r"result, confirmed / rejected hypothesis, validation, readiness")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "cap09 slice3 delivered",
             *_CAP09S3_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-09 SLICE 3", r"PR / merge pending")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "cap09 slice3 delivered live", _tok(_CAP09S3_DELIVERED),
               r"what\s+they\s+expect\s+to\s+happen\s+in\s+that\s+experiment",
               r"`prototype_test_hypotheses`")
        _rejects(block, path, "cap09 slice3 delivered live", re.escape(_CAP09S3_CONTRACT),
                 _tok(_CAP09S3_STATUS), _tok("`VARIABLE: NOT AUTHORIZED`"))
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("CAP-09 Slice 3 — DELIVERED (PR #711, merge "
            "`e393e29cd0ba4f568cf1fd1a0d4c2e0e7742eabd`)") in head
    assert "ACTIVE CONTRACT: CAP-09 SLICE 3" not in head
    assert "the former CAP-09 Slice 3, the former CAP-11 Slice 1" in claude
    raw_checklist = _read(CHECKLIST)
    assert re.search(r"^" + re.escape(_CAP09S3_DELIVERED.strip("`")) + r"$", raw_checklist, re.M)
    for stale in ("ACTIVE CONTRACT: CAP-09 SLICE 3", _CAP09S3_STATUS.strip("`"),
                  "VARIABLE / RESULT / OTHER CAP-09 FIELDS: NOT AUTHORIZED"):
        assert re.search(r"^" + re.escape(stale), raw_checklist, re.M) is None, stale


_CAP09S4_CONTRACT = "`ACTIVE CONTRACT: CAP-09 SLICE 4 — OWNER-DEFINED TEST VARIABLE / CONDITION`"
_CAP09S4_STATUS = ("`CAP-09 SLICE 4: IMPLEMENTED — ASTRA ARCHITECTURE REVIEW PASS — UX / "
                   "BEHAVIOUR REVIEW PASS — PR / MERGE PENDING`")
_CAP09S4_BOUNDED = ("`BOUNDED OWNER-DEFINED TEST VARIABLE / CONDITION: AUTHORIZED WITHIN CAP-09 "
                    "SLICE 4`")
_CAP09S4_FORMAL_NO = "`FORMAL EXPERIMENTAL VARIABLE MODEL: NOT AUTHORIZED`"
_CAP09S4_REVERSALS = _CAP09S3_REVERSALS + (
    re.escape(_CAP09S3_CONTRACT),
    r"CAP-09 SLICE 3: IMPLEMENTED",
    r"FORMAL (EXPERIMENTAL )?VARIABLE MODEL\W{0,8}(IS )?AUTHORIZED\b",
    r"(?<!no )(?<!not )Test Variable / Condition (is|counts as|becomes|creates) (an? )?"
    r"(Evidence|test result|result|validation|validated|readiness)\b",
    r"(?<!not )(?<!never )(parsed|inferred|generated) into (a )?formal",
    r"CAP-09 SLICE 4\W{0,8}(IS )?NOT AUTHORIZED",
    r"TEST VARIABLE / CONDITION\W{0,8}NOT AUTHORIZED")


_CAP09S4_DELIVERED = ("`CAP-09 SLICE 4: DELIVERED — PR #712 — merge "
                      "c0faedcd3bff317d9439a7561c220a6ca97f7f4a`")


def test_cap09_slice_4_is_delivered_history_and_its_rules_still_bind():
    """CAP-09 Slice 4 — Owner-defined Test Variable / Condition — was delivered
    (PR #712, merge c0faedc). Its section reads DELIVERED and visibly superseded,
    its rules still bind, and no live surface presents it as the current contract
    or as "PR / merge pending" again."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--cap09-slice-4"))
    _needs(top, CONTRACT, "cap09 slice4 delivered",
           r"Owner-Defined Test Variable / Condition \(Owner / Lead authorization, 2026-09-27\) — "
           r"DELIVERED \(PR #712\); SUPERSEDED as current authority by Mechanical CAP-01 Open-Gap "
           r"Technical Context",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #712, merge `c0faedcd3bff317d9439a7561c220a6ca97f7f4a`",
           r"Every rule below still binds except where Mechanical CAP-01 Open-Gap Technical "
           r"Context states otherwise",
           r"material findings: NONE — DELIVERED \(PR #712, merge "
           r"`c0faedcd3bff317d9439a7561c220a6ca97f7f4a`\)",
           r"\*\*INVENTOR PLANNING SET\*\* \| four concepts: Success Criterion, Test Hypothesis, "
           r"Test Variable / Condition, Measurement Method",
           r"\*\*IDENTITY\*\* \| the canonical `experiment_id` stays the only experiment "
           r"identity; no variable_id",
           r"`prototype_test_variables` \(project_id, experiment_id, inventor-authored text only\)",
           r"up to four submitted concept deltas atomically",
           r"two- and three-concept callers stay compatible",
           r"\*\*NO FORMAL SCIENTIFIC AUTHORITY\*\*",
           re.escape(_CAP09S4_BOUNDED), re.escape(_CAP09S4_FORMAL_NO),
           r"\*\*Deferred / not authorized:\*\* a formal experimental variable model")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "cap09 slice4 delivered",
             *_CAP09S4_REVERSALS, r"\*\*ACTIVE CONTRACT: CAP-09 SLICE 4", r"PR / merge pending")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "cap09 slice4 delivered live", _tok(_CAP09S4_DELIVERED),
               _tok(_CAP09S4_BOUNDED), _tok(_CAP09S4_FORMAL_NO),
               _tok("`FULL CAP-09: NOT AUTHORIZED`"), _tok("`FULL WS-PFV-001: NOT AUTHORIZED`"),
               _tok("`RESULT OUTCOME / PASS-FAIL JUDGEMENT: NOT AUTHORIZED`"), _tok(_CAP09S3_DELIVERED), _tok(_S19_COMPLETE),
               r"CAP-09\s+Slice\s+4\s+\(delivered\):\s+for\s+each\s+CURRENT\s+Section-11\s+experiment",
               r"what\s+they\s+intend\s+to\s+change,\s+compare\s+or\s+set\s+differently\s+in\s+"
               r"that\s+test",
               r"`prototype_test_variables`",
               r"up\s+to\s+four\s+submitted\s+concept\s+deltas\s+atomically",
               r"A\s+formal\s+experimental\s+variable\s+model")
        _rejects(block, path, "cap09 slice4 delivered live", *_CAP09S4_REVERSALS,
                 re.escape(_CAP09S4_CONTRACT), _tok(_CAP09S4_STATUS),
                 _tok("`VARIABLE: NOT AUTHORIZED`"),
                 r"Test Variable / Condition, below — was separately Owner-authorized",
                 r"Test Variable / Condition per current experiment \(current bounded action")
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("CAP-09 Slice 4 — DELIVERED (PR #712, merge "
            "`c0faedcd3bff317d9439a7561c220a6ca97f7f4a`)") in head
    assert "ACTIVE CONTRACT: CAP-09 SLICE 4" not in head
    assert "CAP-09 Slice 4 (above) is the current bounded action" not in head
    assert "the former CAP-09 Slice 4, the former CAP-09 Slice 3" in claude
    raw_checklist = _read(CHECKLIST)
    assert re.search(r"^" + re.escape(_CAP09S4_DELIVERED.strip("`")) + r"$", raw_checklist, re.M)
    for stale in ("ACTIVE CONTRACT: CAP-09 SLICE 4", _CAP09S4_STATUS.strip("`"),
                  "NO FURTHER CAP-01 IMPLEMENTATION IS CURRENTLY AUTHORIZED"):
        assert re.search(r"^" + re.escape(stale), raw_checklist, re.M) is None, stale
    # the row is ticked by the Stage 19 closure for the current planning-only scope only
    [row] = re.findall(r"^- \[x\] \*\*19 — WS-PFV-001/CAP-09:\*\*.*$", _read(ROADMAP), re.M)
    assert ("CAP-09 Slice 4, one inventor-written free-text Test Variable / Condition per "
            "current experiment, durable in the same project store as planning metadata only, "
            "is delivered (PR #712, merge `c0faedcd3bff317d9439a7561c220a6ca97f7f4a`)") in row
    live_row = row[:row.index("*(Superseded")]
    assert "is the current bounded action" not in live_row
    assert ("no CAP-09 implementation beyond Slice 4, the Result Event Slice 1 and the Stage 19 closure is currently "
            "authorized") in live_row


_MECH_CAND = "99f6b91185c0a1766e48e2abe0efde629b939ab1"
_MECH_CONTRACT = "`ACTIVE CONTRACT: MECHANICAL CAP-01 — OPEN-GAP TECHNICAL CONTEXT`"
_MECH_STATUS = ("`MECHANICAL CAP-01 OPEN-GAP TECHNICAL CONTEXT: OWNER-AUTHORIZED — IMPLEMENTED "
                "(candidate " + _MECH_CAND + ") — INDEPENDENT NON-AUTHORING REVIEW PASS — "
                "MATERIAL FINDINGS: NONE — PR / MERGE PENDING`")
_MECH_NO_PROFILE = "`MECHANICAL DOMAIN-LEVEL CHECKLIST PROFILE: NOT AUTHORIZED`"
_MECH_BOUNDARY = ("`NO FURTHER CAP-01 IMPLEMENTATION IS AUTHORIZED BEYOND THE DELIVERED MECHANICAL AND "
                  "ELECTRICAL SLICES`")
_MECH_MERGE = "225c0d36e6cfa97a25cd58c671b7c4f090627fb5"
_MECH_DELIVERED = ("`MECHANICAL CAP-01 OPEN-GAP TECHNICAL CONTEXT: DELIVERED — PR #713 — merge "
                   + _MECH_MERGE + "`")
# Boundaries the Mechanical line of work keeps whatever its lifecycle: never a full or
# domain-level Mechanical CAP-01 profile, a D13 Mechanical package, a new domain
# activation, engineering analysis, a feasibility proof or a completed Stage 18.
_MECH_BOUNDARY_REVERSALS = _CAP09S4_REVERSALS + (
    re.escape(_CAP09S4_CONTRACT),
    r"CAP-09 SLICE 4: IMPLEMENTED",
    r"MECHANICAL (DOMAIN-LEVEL )?(CHECKLIST )?PROFILE\W{0,8}(IS )?AUTHORIZED\b",
    r"FULL MECHANICAL CAP-01\W{0,8}(IS )?AUTHORIZED\b",
    r"D13 MECHANICAL PACKAGE\W{0,8}(IS )?AUTHORIZED\b",
    r"NEW DOMAIN ACTIVATION\W{0,8}(IS )?AUTHORIZED\b",
    r"(?<!not )(?<!no )(?<!never )(FEA|stress|fatigue|GD&T|tolerance) (analysis|verification)"
    r"\W{0,8}(IS )?(PROVIDED|PERFORMED|AUTHORIZED)\b",
    r"(?<!never implies the mechanism has been )shown physically feasible",
    r"STAGE 18 COMPLETE: YES",
    r"NO FURTHER CAP-01 IMPLEMENTATION IS CURRENTLY AUTHORIZED",
    r"simply has no authorized CAP-01 profile yet")
# Forms that would present the DELIVERED Mechanical CAP-01 slice as live again.
_MECH_LIVE_FORMS = (
    re.escape(_MECH_CONTRACT), _tok(_MECH_STATUS),
    r"CURRENT BOUNDED ACTION — Stage 18 / Mechanical CAP-01",
    r"Open-Gap\s+Technical\s+Context\s+is\s+the\s+current\s+bounded\s+action",
    r"Open-Gap\s+Technical\s+Context\s+current\s+bounded\s+action",
    r"Open-Gap\s+Technical\s+Context\s+\(current\s+bounded\s+action",
    r"current\s+bounded\s+action:\s+Mechanical\s+CAP-01",
    r"OPEN-GAP TECHNICAL CONTEXT: OWNER-AUTHORIZED — IMPLEMENTED",
    r"Open-Gap Technical Context[^.]{0,120}PR NOT OPENED")


def test_mechanical_cap01_open_gap_context_is_delivered_history_and_its_rules_still_bind():
    """Mechanical CAP-01 — Open-Gap Technical Context — was delivered (PR #713, merge
    225c0d3; post-merge identity / content verification PASS). Its contract section
    reads DELIVERED and visibly superseded by Mechanical Technical Deepening Slice 1,
    its boundaries still bind, and no live surface presents it as the current
    contract, as "PR / merge pending" or as "merge NOT PERFORMED" again."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ",
                 _section(contract, "current-authority--mechanical-cap01-open-gap-context"))
    _needs(top, CONTRACT, "mechanical cap01 delivered",
           r"Open-Gap Technical Context \(Owner / Lead authorization, 2026-09-27\) — DELIVERED "
           r"\(PR #713\); SUPERSEDED as current authority by Mechanical Technical Deepening Slice "
           r"1 — Force, Moment & Pressure Fundamentals",
           r"\*\*No longer the current authority\.\*\*",
           r"PR #713, merge `" + _MECH_MERGE + r"`; post-merge identity / content verification "
           r"PASS",
           r"Every rule below still binds except where Mechanical Technical Deepening Slice 1 "
           r"states otherwise",
           r"material findings: NONE \(risk LEVEL 2 — MEDIUM; independent full regression 8544 "
           r"passed, 1 skipped, 1 xfailed, 0 failed\) / DELIVERED \(PR #713, merge `"
           + _MECH_MERGE + r"`\)",
           r"\*\*BINDING\*\* \| exact canonical `IdeaState\.gaps\[\]\.gap_type` \+ `\.status`",
           r"the D13 Electronics package \(`research/d13-tkp-pkg-001`\) is NOT a Mechanical source",
           r"\*\*OWNERSHIP\*\* \| Path-N remains the question-serving owner; CAP-04 remains the "
           r"action / responsibility / required-input / closure / routed-need owner",
           re.escape(_MECH_NO_PROFILE), r"`FULL CAP-01 / FULL STG: NOT AUTHORIZED`")
    live_top = re.sub(r"\*\(Superseded.*?\)\*", "", top)
    _rejects(live_top, CONTRACT, "mechanical cap01 delivered", *_MECH_BOUNDARY_REVERSALS,
             r"\*\*ACTIVE CONTRACT: MECHANICAL CAP-01", r"PR NOT OPENED", r"PR / merge pending",
             r"merge NOT PERFORMED")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "mechanical cap01 delivered live", _tok(_MECH_DELIVERED),
               _tok(_MECH_NO_PROFILE), _tok(_MECH_BOUNDARY),
               r"Mechanical\s+CAP-01\s+Open-Gap\s+Technical\s+Context\s+\(delivered",
               r"one\s+short\s+explanatory\s+context\s+per\s+CURRENT\s+\(OPEN\s+/\s+PARTIAL\)\s+"
               r"canonical\s+Mechanical\s+gap",
               r"not\s+a\s+full\s+Mechanical\s+CAP-01\s+profile")
        _rejects(block, path, "mechanical cap01 delivered live", *_MECH_BOUNDARY_REVERSALS,
                 *_MECH_LIVE_FORMS)
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "mechanical cap01 delivered routing",
               r"\*\*DELIVERED — Stage 18 / Mechanical CAP-01 — Open-Gap Technical Context \(inside "
               r"Stage 18; no new Master\s+Roadmap Stage\):\*\*",
               _tok("`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"),
               r"the\s+D13\s+Electronics\s+package\s+is\s+not\s+a\s+Mechanical\s+source",
               r"Path-N\s+and\s+CAP-04\s+ownership\s+unchanged",
               r"NO\s+Electronics-style\s+domain-level\s+checklist\s+profile")
    # CLAUDE.md: delivered PR #713 truth; the Mechanical contract is superseded, not live
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    for needle in ("Mechanical CAP-01 — Open-Gap Technical Context — DELIVERED (PR #713, merge `"
                   + _MECH_MERGE + "`; post-merge identity / content verification PASS)",
                   "the bounded Mechanical Open-Gap Technical Context is delivered (PR #713)",
                   "Mechanical still has NO Electronics-style domain-level checklist profile"):
        assert needle in head, needle
    for gone in ("ACTIVE CONTRACT: MECHANICAL CAP-01", _MECH_CAND, "PR NOT OPENED — PR / merge pending",
                 "the bounded Mechanical Open-Gap Technical Context (above) is its current bounded "
                 "action"):
        assert gone not in head, gone
    assert "the former Mechanical CAP-01 Open-Gap Technical Context, the former CAP-09 Slice 4" in claude
    # checklist plain-text mirrors: delivered line present, the live lines gone
    raw_checklist = _read(CHECKLIST)
    assert re.search(r"^" + re.escape(_MECH_DELIVERED.strip("`")) + r"$", raw_checklist, re.M)
    for stale in (_MECH_CONTRACT.strip("`"), _MECH_STATUS.strip("`")):
        assert re.search(r"^" + re.escape(stale) + r"$", raw_checklist, re.M) is None, stale
    live_checklist = re.sub(r"\*\(Superseded.*?\)\*", "", _flat(CHECKLIST))
    for pat in _MECH_LIVE_FORMS:
        assert re.search(pat, live_checklist) is None, pat
    assert "**CURRENT SUBTASK:** MECHANICAL CAP-01" not in live_checklist
    # the roadmap Stage-18 row and group state: delivered, never current again
    roadmap = _read(ROADMAP)
    [row] = re.findall(r"^- \[x\] \*\*18 — D13/CAP-01 guidance:\*\*.*$", roadmap, re.M)
    live_row = row[:row.index("*(Superseded")]
    assert ("(NOT a Mechanical domain-level checklist profile) — is delivered (PR #713, merge `"
            + _MECH_MERGE + "`)") in live_row
    assert "delivered (PR #713), and then as Mechanical Technical Deepening Slice 1" in live_row
    for pat in _MECH_LIVE_FORMS:
        assert re.search(pat, live_row) is None, pat
    group = re.sub(r"\*\(Superseded.*?\)\*", "", _flat(ROADMAP))
    assert ("the bounded Mechanical CAP-01 Open-Gap Technical Context is delivered (PR #713, merge `"
            + _MECH_MERGE + "`)") in group
    # the register and the state: delivered, never "PR / merge pending"
    register = _flat(CAPABILITIES)
    for needle in ("ONE bounded gap-scoped Mechanical CAP-01 Open-Gap Technical Context (DELIVERED — "
                   "PR #713, merge `" + _MECH_MERGE + "`; not a Mechanical domain-level checklist "
                   "profile)",
                   "the Mechanical Open-Gap Technical Context: DELIVERED (PR #713, merge `"
                   + _MECH_MERGE + "`)",
                   "**and one Owner-authorized bounded gap-scoped Mechanical Open-Gap Technical "
                   "Context** (delivered, PR #713;",
                   "one bounded gap-scoped Mechanical Open-Gap Technical Context (delivered, PR #713)"):
        assert needle in register, needle
    assert _MECH_CAND not in register
    state = _current(STATE, "current-position")
    for needle in ("Mechanical CAP-01 — Open-Gap Technical Context — delivered, PR #713",
                   "`mechanical` remains a fully activated",
                   "NO Electronics-style domain-level CAP-01 checklist profile and NOW has the "
                   "separately authorized gap-scoped Mechanical Open-Gap Technical Context "
                   "(delivered, PR #713)"):
        assert needle in state, needle


_TD1_CAND = "e56e32def45346944eecab9982dfb572fa5764f3"
_TD1_TREE = "8157eacf5b012d153534b5901aacd9c30abfa26d"
_TD1_MERGE = "dd445183a110da4ef707226e3ff9121f6c315e5b"
_TD1_CONTRACT = ("`ACTIVE CONTRACT: MECHANICAL TECHNICAL DEEPENING SLICE 1 — FORCE, MOMENT & "
                 "PRESSURE FUNDAMENTALS`")
_TD1_STATUS = ("`MECHANICAL TECHNICAL DEEPENING SLICE 1: OWNER-AUTHORIZED — IMPLEMENTED (final "
               "candidate " + _TD1_CAND + ") — INDEPENDENT NON-AUTHORING REVIEW COMPLETE — PASS — "
               "NO MATERIAL FINDINGS REMAIN — PR / MERGE PENDING`")
_TD1_DELIVERED = ("`MECHANICAL TECHNICAL DEEPENING SLICE 1: DELIVERED — PR #714 — merge "
                  + _TD1_MERGE + "`")
_NONE_LIVE = "`ACTIVE CONTRACT: NONE`"
_NO_TD_SUBTASK = "`NO CURRENT AUTHORIZED TECHNICAL DEEPENING SUBTASK`"
_TD1_NEXT_NO = "`NEXT TECHNICAL DEEPENING SLICE: NOT AUTHORIZED`"
# A live surface may never present the DELIVERED Mechanical Slice 1 as the live contract, as
# pending or as the current bounded action / subtask.
_TD1_LIVE_FORMS = (
    re.escape(_TD1_CONTRACT), _tok(_TD1_STATUS),
    r"\*\*ACTIVE CONTRACT: MECHANICAL TECHNICAL DEEPENING",
    r"MECHANICAL TECHNICAL DEEPENING SLICE 1: OWNER-AUTHORIZED",
    r"CURRENT BOUNDED ACTION — Stage 18 / Mechanical Technical Deepening",
    r"Mechanical Technical Deepening Slice 1(?: — Force, Moment & Pressure Fundamentals)?"
    r"(?: \(above\))? (?:is (?:its |the )?)?current bounded action",
    r"current bounded action(?: is|:) Mechanical Technical Deepening",
    r"CURRENT SUBTASK:\*\* MECHANICAL TECHNICAL DEEPENING",
    r"Mechanical Technical Deepening Slice 1[^.;]{0,160}(PR NOT OPENED|merge NOT PERFORMED|"
    r"PR / MERGE PENDING)",
    r"BEYOND THE CURRENTLY AUTHORIZED MECHANICAL")
# The stale post-PR-#714 no-active-contract forms, which must survive ONLY as superseded history.
# Generic no-active-contract forms: forbidden in the SUPERSEDED post-PR-#714 section's live text.
_NONE_GENERIC_FORMS = (
    re.escape(_NONE_LIVE), _tok(_NO_TD_SUBTASK), r"\*\*ACTIVE CONTRACT: NONE\.\*\*",
    r"no current authorized Technical Deepening subtask", r"no product increment is currently authorized")
# The post-PR-#714-SPECIFIC NONE forms, which must never return live (a later NONE — post-PR-#716 —
# is its own live declaration, guarded below).
_POST714_NONE_FORMS = (
    r"NO ACTIVE CONTRACT — post-PR-#714", r"CURRENT SUBTASK:\*\* NONE — NO CURRENT",
    r"no subsequent increment is authorized \(`ACTIVE CONTRACT: NONE`\)", r"\(post-PR-#714;",
    r"\*\*ACTIVE CONTRACT: NONE\.\*\* Mechanical Technical Deepening Slice 1")
_TD1_REVERSALS = _MECH_BOUNDARY_REVERSALS + _MECH_LIVE_FORMS + _TD1_LIVE_FORMS + (
    r"(?<!no )(?<!not )project(-specific)? calculation (is )?(performed|provided|shown)",
    r"(?<!no )applicability (is )?(inferred|decided|determined)",
    r"(?<!not )(satisfies|closes) (the )?(exact )?(CURRENT )?(canonical )?PHYSICAL_FEASIBILITY",
    r"(physical )?feasibility (is )?(proven|established|confirmed|shown)\b",
    r"FULL CAP-01 / FULL STG: AUTHORIZED",
    r"STAGE 18: (ENTERED / )?COMPLETE", r"roadmap is complete\b(?<!NOT mean the roadmap is complete)",
    r"(Stage 15|IRL) implementation (is )?authorized")


def _live_surfaces():
    surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    surfaces.append((STATE, _current(STATE, "current-position")))
    return surfaces


def test_mechanical_td_slice1_is_delivered_history_and_the_post_714_none_is_superseded():
    """Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals — stays
    DELIVERED history (PR #714, merge dd44518; post-merge identity / content verification PASS)
    with every rule still recorded. The post-PR-#714 `ACTIVE CONTRACT: NONE` declaration was true
    until the Owner authorized the Electrical slice; it survives ONLY as visibly superseded
    history, never as a live contract, a "no current subtask" claim or a live plain-text line."""
    contract = _read(CONTRACT)
    none = re.sub(r"\s+", " ", _section(contract, "current-authority--post-pr-714-no-active-contract"))
    _needs(none, CONTRACT, "post-714 none superseded",
           r"## Current authority — post-PR-#714: no active contract \(2026-09-28\) — SUPERSEDED "
           r"\(2026-09-28\) by Electrical / Electronics Technical Deepening Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"\*\(Superseded 2026-09-28, preserved so the change is visible rather than silent: this "
           r"opened \"\*\*ACTIVE CONTRACT: NONE\.\*\* Mechanical Technical Deepening Slice 1",
           r"\*\*STAGE 18\*\* \| `STARTED: YES` · `COMPLETE: NO` · \*\*ENTERED / PARTIAL / NOT "
           r"COMPLETE\*\*; its roadmap checkbox stays unticked",
           re.escape(_TD1_DELIVERED), r"T = F × L⊥; F₁L₁ = F₂L₂; F = pA; N·m; Pa / kPa")
    live_none = re.sub(r"\*\(Superseded.*?\)\*", "", none)
    _rejects(live_none, CONTRACT, "post-714 none superseded", *_NONE_GENERIC_FORMS, *_POST714_NONE_FORMS)
    # the Slice-1 section: delivered, visibly superseded, every rule still recorded
    top = re.sub(r"\s+", " ",
                 _section(contract, "current-authority--mechanical-td-slice1-force-moment-pressure"))
    _needs(top, CONTRACT, "mechanical td1 delivered",
           r"Force, Moment & Pressure Fundamentals \(Owner / Lead authorization, 2026-09-28\) — "
           r"DELIVERED \(PR #714\); SUPERSEDED as current authority",
           r"\*\*No longer the current authority\.\*\* Mechanical Technical Deepening Slice 1 was "
           r"delivered \(PR #714, merge `" + _TD1_MERGE + r"`; post-merge identity / content "
           r"verification PASS\)",
           r"at that time no subsequent increment was authorized",
           r"itself now superseded by Electrical / Electronics Technical Deepening Slice 1",
           r"Every rule below still binds\.",
           r"OWNER-AUTHORIZED / IMPLEMENTED — final candidate `" + _TD1_CAND + r"` \(tree `"
           + _TD1_TREE + r"`",
           r"/ DELIVERED \(PR #714, merge `" + _TD1_MERGE + r"`\) / deployment and release NOT "
           r"AUTHORIZED",
           r"simple perpendicular torque / moment \(T = F × L⊥\); ideal static moment balance "
           r"\(F₁L₁ = F₂L₂\); uniform pressure over an effective area \(F = pA\); SI unit discipline "
           r"\(N·m; Pa / kPa\)",
           r"\*\*TRUTH BOUNDARY\*\* \| reference fundamentals only",
           r"\*\*SOURCES\*\* \| governed Mechanical provenance mechanical:PR006–PR011",
           r"mechanical:PR001–PR005 unchanged", re.escape(_TD1_DELIVERED), re.escape(_MECH_DELIVERED))
    live_top = re.sub(r"\*\(Superseded.*?\)\*", "", top)
    _rejects(live_top, CONTRACT, "mechanical td1 delivered", *_TD1_REVERSALS)
    _rejects(live_top, CONTRACT, "mechanical td1 delivered", r"no subsequent increment is\s+authorized, so",
             r"the section above declares ACTIVE CONTRACT: NONE")
    # every live surface still records the Mechanical delivery and none carries the stale NONE
    for path, block in _live_surfaces():
        _needs(block, path, "mechanical td1 live history", _tok(_TD1_DELIVERED),
               _tok(_MECH_DELIVERED), _tok(_MECH_NO_PROFILE),
               r"Mechanical\s+Technical\s+Deepening\s+Slice\s+1\s+\(delivered\)\.\s+Mechanical\s+"
               r"only:\s+for\s+the\s+exact\s+CURRENT\s+canonical\s+PHYSICAL_FEASIBILITY\s+gap",
               r"T\s+=\s+F\s+×\s+L⊥", r"mechanical:PR006–PR011")
        _rejects(block, path, "mechanical td1 live history", *_TD1_LIVE_FORMS, *_POST714_NONE_FORMS)
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "mechanical td1 routing",
               _tok("`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"),
               r"\*\*DELIVERED — Stage 18 / Mechanical Technical Deepening Slice 1 — Force, Moment & "
               r"Pressure Fundamentals \(inside Stage 18; no new Master Roadmap Stage\):\*\*")
    # CLAUDE.md: the delivery is recorded; NONE is only a named superseded declaration
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals — DELIVERED "
            "(PR #714, merge `" + _TD1_MERGE + "`; post-merge identity / content verification PASS)") in head
    for pat in _POST714_NONE_FORMS + _TD1_LIVE_FORMS:
        assert re.search(pat, head, re.I | re.S) is None, pat
    assert ("the former post-PR-#716 `ACTIVE CONTRACT: NONE`, the former Electrical / Electronics "
            "Technical Deepening Slice 1, the former post-PR-#714 `ACTIVE CONTRACT: NONE`, the former "
            "Mechanical Technical Deepening Slice 1,") in claude
    # checklist plain text: the delivery line stays, the NONE lines are gone
    raw_checklist = _read(CHECKLIST)
    assert re.search(r"^" + re.escape(_TD1_DELIVERED.strip("`")) + r"$", raw_checklist, re.M)
    for stale in (_TD1_CONTRACT.strip("`"), _TD1_STATUS.strip("`")):
        assert re.search(r"^" + re.escape(stale) + r"$", raw_checklist, re.M) is None, stale
    live_checklist = re.sub(r"\*\(Superseded.*?\)\*", "", _flat(CHECKLIST))
    for pat in _TD1_LIVE_FORMS + (r"CURRENT SUBTASK:\*\* NONE — NO CURRENT", r"NO ACTIVE CONTRACT — post-PR-#714"):
        assert re.search(pat, live_checklist) is None, pat
    # roadmap row 18 and group state: delivered, never NONE again
    roadmap = _read(ROADMAP)
    [row] = re.findall(r"^- \[x\] \*\*18 — D13/CAP-01 guidance:\*\*.*$", roadmap, re.M)
    live_row = row[:row.index("*(Superseded")]
    assert ("Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals, four "
            "source-backed reference fundamentals for a current PHYSICAL_FEASIBILITY gap (no "
            "calculation, applicability inference or feasibility conclusion) — is delivered (PR #714, "
            "merge `" + _TD1_MERGE + "`; post-merge identity / content verification PASS") in live_row
    for pat in _POST714_NONE_FORMS + _TD1_LIVE_FORMS:
        assert re.search(pat, live_row) is None, pat
    group = re.sub(r"\*\(Superseded.*?\)\*", "", _flat(ROADMAP))
    assert ("Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals is "
            "delivered (PR #714, merge `" + _TD1_MERGE + "`)") in group
    register = _flat(CAPABILITIES)
    for needle in ("ONE bounded Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure "
                   "Fundamentals (DELIVERED — PR #714, merge `" + _TD1_MERGE + "`; four source-backed "
                   "reference fundamentals only)",
                   "A fourth bounded slice — Mechanical Technical Deepening Slice 1 — Force, Moment & "
                   "Pressure Fundamentals: DELIVERED (PR #714, merge `" + _TD1_MERGE + "`)"):
        assert needle in register, needle
    assert "ACTIVE CONTRACT: NONE" not in register


_EL_CAND = "10e2210dc2f427f2feeee80ea808ca8d91387ad0"
_EL_TREE = "b4b9831e36b386919569922aa365d61b152c8a68"
_EL_MERGE = "11564b235b056aaf12ca9d5596418f43a2d7e61c"
_EL_CONTRACT = ("`ACTIVE CONTRACT: ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1 — BASIC "
                "ELECTRICAL REFERENCE FUNDAMENTALS`")
_EL_STATUS = ("`ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1: OWNER-AUTHORIZED — IMPLEMENTED "
              "(candidate " + _EL_CAND + ") — INDEPENDENT NON-AUTHORING REVIEW COMPLETE — PASS WITH "
              "NON-BLOCKING OBSERVATIONS — PR NOT OPENED / MERGE NOT PERFORMED`")
_EL_DELIVERED = ("`ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1: DELIVERED — PR #716 — merge "
                 + _EL_MERGE + "`")
_EL_FUTURE_NO = ("`MECHATRONICS / ROBOTICS / IOT / DRONE / RENEWABLE / SATELLITE IMPLEMENTATION: NOT "
                 "AUTHORIZED`")
_EL_INTEG_NO = "`ELECTRICAL ↔ MECHANICAL / MECHATRONICS INTEGRATION: NOT AUTHORIZED`"
# Forms that would present the DELIVERED Electrical slice as live again: the live contract, the
# pre-merge status, the current bounded action / subtask, a pending PR / merge.
_EL_LIVE_FORMS = (
    re.escape(_EL_CONTRACT), _tok(_EL_STATUS),
    r"\*\*ACTIVE CONTRACT: ELECTRICAL",
    r"ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1: OWNER-AUTHORIZED",
    r"CURRENT BOUNDED ACTION — Stage 18 / Electrical",
    r"Electrical / Electronics Technical Deepening Slice 1(?: — Basic Electrical Reference Fundamentals)?"
    r"(?: \(above\))? (?:is (?:its |the )?)?current bounded action",
    r"Electrical / Electronics Technical Deepening Slice 1 \(current bounded action\)",
    r"CURRENT SUBTASK:\*\* ELECTRICAL",
    r"Electrical / Electronics Technical Deepening Slice 1[^.;]{0,160}(PR NOT OPENED|merge NOT "
    r"PERFORMED|PR / MERGE PENDING|PR / merge pending)",
    r"AND THE CURRENT ELECTRICAL SLICE", r"current Electrical slice")
def test_electrical_td_slice1_is_delivered_history_and_its_rules_still_bind():
    """Electrical / Electronics Technical Deepening Slice 1 — Basic Electrical Reference
    Fundamentals — is DELIVERED (PR #716, merge 11564b2; post-merge identity / content
    verification PASS) with every reviewed rule still recorded: exact binding
    electronics_electrical + PHYSICAL_FEASIBILITY + OPEN / PARTIAL, exactly three reference
    claims, the source / IP boundary and the non-blocking review observations. Its pre-merge
    contract survives ONLY as visibly superseded history."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--electrical-td-slice1-basic-reference"))
    _needs(top, CONTRACT, "electrical td1 delivered",
           r"Basic Electrical Reference Fundamentals \(Owner / Lead authorization, 2026-09-28\) — DELIVERED "
           r"\(PR #716\); SUPERSEDED as current authority by the post-PR-#716 no-active-contract declaration",
           r"\*\*No longer the current authority\.\*\* Electrical / Electronics Technical Deepening Slice 1 was "
           r"delivered \(PR #716, merge `" + _EL_MERGE + r"`; post-merge identity / content verification PASS\)",
           r"Every rule below still binds\.",
           r"\*\(Superseded 2026-09-29, preserved so the change is visible rather than silent: this opened "
           r"\"\*\*ACTIVE CONTRACT: ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1 — BASIC ELECTRICAL "
           r"REFERENCE FUNDAMENTALS\.\*\*\" and recorded the slice as \"PR NOT OPENED / merge NOT PERFORMED",
           r"OWNER-AUTHORIZED / IMPLEMENTED — candidate `" + _EL_CAND + r"` \(tree `" + _EL_TREE + r"`",
           r"INDEPENDENT NON-AUTHORING REVIEW COMPLETE — PASS WITH NON-BLOCKING OBSERVATIONS",
           r"/ DELIVERED \(PR #716, merge `" + _EL_MERGE + r"`\) / deployment and release NOT AUTHORIZED",
           r"the trusted domain `electronics_electrical` in exact state OPEN or PARTIAL",
           r"exactly three source-backed reference fundamentals: V = I × R \(Ohm's-law / resistive "
           r"reference\); P = V × I \(basic power reference\); SI unit discipline \(V / A / Ω / W\)",
           r"no applicability inference, no project calculation, no gap closure, no compatibility verdict, "
           r"no safe-limit determination, no component / power / battery sizing, no circuit-operation proof, "
           r"no electrical-safety conclusion, no readiness / progression / validation effect",
           r"official status ARCHIVE — Canceled, effective April 2016",
           r"DOE source notation E = IR and P = IE, normalized by InventorAI to V = IR and P = VI",
           r"NIST SP 811 Appendix B\.9, bounded unit facts only \(V / A / Ω / W\)",
           r"OpenStax EXCLUDED; IEC / IPC \(PR001 / PR002\) are NOT the authority for these claims",
           r"N-1 source URL traceability", r"O-1 equation wrapping / separator",
           r"O-2 Arabic electrical \"rating\" terminology", r"القيم الاسمية",
           r"O-3 Electronics PF gap-context host — CLOSED, NO DEFECT",
           r"pre-merge current-truth lag CLOSED / RESOLVED by the post-PR-#716 closure",
           re.escape(_EL_DELIVERED), r"`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`",
           re.escape(_TD1_DELIVERED), re.escape(_MECH_BOUNDARY),
           r"\*\*Deferred / not authorized:\*\* any next slice beyond this Electrical slice")
    live_top = re.sub(r"\*\(Superseded.*?\)\*", "", top)
    _rejects(live_top, CONTRACT, "electrical td1 delivered", *_EL_LIVE_FORMS,
             r"PR NOT OPENED", r"merge NOT PERFORMED")
    # every live surface records the Electrical delivery and its bounded scope
    for path, block in _live_surfaces():
        _needs(block, path, "electrical td1 live history", _tok(_EL_DELIVERED),
               _tok("`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"),
               r"Electrical\s+/\s+Electronics\s+Technical\s+Deepening\s+Slice\s+1\s+\(delivered\)\.\s+"
               r"Electrical\s+/\s+Electronics\s+only:\s+for\s+the\s+exact\s+CURRENT\s+canonical\s+"
               r"electronics_electrical\s+PHYSICAL_FEASIBILITY\s+gap\s+in\s+exact\s+state\s+OPEN\s+or\s+PARTIAL",
               r"V\s+=\s+I\s+×\s+R", r"P\s+=\s+V\s+×\s+I", r"V\s+/\s+A\s+/\s+Ω\s+/\s+W",
               r"electronics_electrical:PR004–PR007",
               r"ARCHIVE\s+—\s+Canceled,\s+effective\s+April\s+2016",
               r"Reference\s+fundamentals\s+only:\s+no\s+applicability\s+inference,\s+no\s+project\s+"
               r"calculation,\s+no\s+gap\s+closure,\s+no\s+compatibility\s+verdict,\s+no\s+safe-limit\s+"
               r"determination,\s+no\s+component\s+/\s+power\s+/\s+battery\s+sizing,\s+no\s+"
               r"circuit-operation\s+proof,\s+no\s+electrical-safety\s+conclusion",
               r"Delivered\s+in\s+PR\s+#716\s+\(merge\s+`" + _EL_MERGE + r"`;\s+reviewed\s+candidate\s+`"
               + _EL_CAND + r"`\s+preserved\s+in\s+ancestry\)")
        _rejects(block, path, "electrical td1 live history", *_EL_LIVE_FORMS)
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "electrical td1 routing",
               r"\*\*DELIVERED — Stage 18 / Electrical / Electronics Technical Deepening Slice 1 — Basic "
               r"Electrical Reference Fundamentals \(inside Stage 18; no new Master Roadmap Stage\):\*\*")
    # CLAUDE.md, roadmap, register: delivered; the pre-merge forms are gone from live text
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    assert ("Electrical / Electronics Technical Deepening Slice 1 — Basic Electrical Reference Fundamentals "
            "— is DELIVERED (PR #716, merge `" + _EL_MERGE + "`; post-merge identity / content verification "
            "PASS; independent non-authoring review COMPLETE — PASS WITH NON-BLOCKING OBSERVATIONS)") in head
    for pat in _EL_LIVE_FORMS:
        assert re.search(pat, head, re.I | re.S) is None, pat
    assert ("the former post-PR-#716 `ACTIVE CONTRACT: NONE`, the former Electrical / Electronics Technical "
            "Deepening Slice 1, the former post-PR-#714 `ACTIVE CONTRACT: NONE`,") in claude
    raw_checklist = _read(CHECKLIST)
    assert re.search(r"^" + re.escape(_EL_DELIVERED.strip("`")) + r"$", raw_checklist, re.M)
    for stale in (_EL_CONTRACT.strip("`"), _EL_STATUS.strip("`")):
        assert re.search(r"^" + re.escape(stale) + r"$", raw_checklist, re.M) is None, stale
    live_checklist = re.sub(r"\*\(Superseded.*?\)\*", "", _flat(CHECKLIST))
    for pat in _EL_LIVE_FORMS:
        assert re.search(pat, live_checklist) is None, pat
    roadmap = _read(ROADMAP)
    [row] = re.findall(r"^- \[x\] \*\*18 — D13/CAP-01 guidance:\*\*.*$", roadmap, re.M)
    live_row = row[:row.index("*(Superseded")]
    assert ("Electrical / Electronics Technical Deepening Slice 1 — Basic Electrical Reference Fundamentals, "
            "three source-backed reference fundamentals for a current Electronics PHYSICAL_FEASIBILITY gap (no "
            "calculation, applicability inference, compatibility, sizing or safety conclusion) — is delivered "
            "(PR #716, merge `" + _EL_MERGE + "`; post-merge identity / content verification PASS") in live_row
    for pat in _EL_LIVE_FORMS:
        assert re.search(pat, live_row) is None, pat
    register = _flat(CAPABILITIES)
    for needle in ("ONE bounded Electrical / Electronics Technical Deepening Slice 1 — Basic Electrical "
                   "Reference Fundamentals (DELIVERED — PR #716, merge `" + _EL_MERGE + "`",
                   "A fifth bounded slice — Electrical / Electronics Technical Deepening Slice 1 — Basic "
                   "Electrical Reference Fundamentals: DELIVERED (PR #716, merge `" + _EL_MERGE + "`)",
                   "(delivered, PR #716, merge `" + _EL_MERGE + "`; full CAP-01/STG still NOT AUTHORIZED)",
                   "and Electrical / Electronics Technical Deepening Slice 1 (delivered, PR #716)"):
        assert needle in register, needle
    for pat in (_EL_CAND + r"[^|]{0,200}PR / merge pending", r"PR / MERGE PENDING"):
        assert re.search(pat, register) is None, pat


_S15_IMPL = "90322f146a56099a2e6647ba0c53e5195963d41c"
_S15_IMPL_TREE = "fc3c7890284ca873f26c4b16a29e4bee2649714f"
_S15_HEAD = "41d06a27ed657a1bf6460c638655f0a6de5447a0"
_S15_TREE = "02b8c1244000820d2202be905d7325c35af4bc5c"
_S15_SYNC = "be6ab2c14be34e49300444b4c6c5104e2f9bdf0a"
_S15_MERGE = "3f3546a279c7f7020744bcbfee957de84ac2e136"
_S15_MTREE = "c8f201bd4117fd210683fffbd06da8e1a695847a"
_S15_BASE = "c525f037a23dae16a317fc12d449ce1586852ae1"
# the pre-merge Stage-15 tokens: history only after PR #718
_S15_CONTRACT = "`ACTIVE CONTRACT: STAGE 15 — INTEGRATED INVENTION ENTRY & DURABLE SUBSYSTEM COMPOSITION — SLICE 1`"
_S15_STATUS = ("`STAGE 15 SLICE 1: OWNER-AUTHORIZED — IMPLEMENTATION COMPLETE CANDIDATE (implementation "
               + _S15_IMPL + ", F1 / IR01-A correction " + _S15_HEAD + ") — INDEPENDENT ARCHITECTURE + "
               "IMPLEMENTATION REVIEW CYCLE COMPLETE — F1-CLOSED — PR NOT OPENED / MERGE NOT PERFORMED`")
_S15_HEAD_TOK = "`CURRENT REVIEWED PRODUCT HEAD: " + _S15_HEAD + " (tree " + _S15_TREE + ")`"
# the post-merge tokens
_S15_DELIVERED = "`STAGE 15 SLICE 1: DELIVERED — PR #718 — merge " + _S15_MERGE + "`"
_S15_PM = "`POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"
_S15_REVIEW = ("`FINAL INDEPENDENT REVIEW: TARGETED PASS WITH NON-BLOCKING OBSERVATIONS — F1-CLOSED — IR01-B "
               "CORRECTED / NO REMAINING MATERIAL DEFECT`")
_S15_ANC = ("`STAGE 15 SLICE 1 ANCESTRY: implementation " + _S15_IMPL + ", F1 / IR01-A correction " + _S15_HEAD
            + ", current-truth sync / PR head " + _S15_SYNC + ", merge " + _S15_MERGE + "`")
_S15_ENTERED = "`STAGE 15: ENTERED / PARTIAL / NOT COMPLETE`"     # history only after the Stage 15 closure
# Stage 15 closure (2026-10-01): STAGE 15 — COMPLETE for the current Mechanical + Electrical / Electronics scope only.
_S15_COMPLETE = "`STAGE 15: COMPLETE — CURRENT MECHANICAL + ELECTRICAL / ELECTRONICS SCOPE`"
_S15_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 18 — ENTERED / PARTIAL / NOT COMPLETE`"
_S15_NOT = ("`ANOTHER STAGE-15 SLICE: NOT AUTHORIZED`", "`FULL STAGE 15 / IRL: NOT AUTHORIZED`",
            "`IRL SCORING / LEVELS: NOT AUTHORIZED`",
            "`FULL D4 / CROSS-DOMAIN COMPATIBILITY EVALUATION: NOT AUTHORIZED`",
            "`ANALYSIS-FOCUS SWITCHING: NOT AUTHORIZED`", "`MECHATRONICS DOMAIN PACK: NOT AUTHORIZED`",
            "`ROBOTICS / IOT / DRONE / RENEWABLE / SATELLITE IMPLEMENTATION: NOT AUTHORIZED`")
# The live Stage-15 exclusions after the closure: no further slice, no validated IRL / IRL level, no D4
# evaluation, no N-domain integration, Phase-7 residuals stay Phase 7 (`FULL STAGE 15 / IRL` is history only).
_S15C_NOT = ("`ANOTHER STAGE-15 SLICE: NOT AUTHORIZED`", "`VALIDATED IRL / IRL LEVEL CLAIM: NOT AUTHORIZED`",
             "`N-DOMAIN / ARBITRARY-DOMAIN INTEGRATION: NOT AUTHORIZED`",
             "`PHASE-7 INTEGRATION RESIDUALS: REMAIN PHASE 7`", "`IRL SCORING / LEVELS: NOT AUTHORIZED`",
             "`FULL D4 / CROSS-DOMAIN COMPATIBILITY EVALUATION: NOT AUTHORIZED`",
             "`ANALYSIS-FOCUS SWITCHING: NOT AUTHORIZED`", "`MECHATRONICS DOMAIN PACK: NOT AUTHORIZED`",
             "`ROBOTICS / IOT / DRONE / RENEWABLE / SATELLITE IMPLEMENTATION: NOT AUTHORIZED`")
_NONE718 = "`ACTIVE CONTRACT: NONE`"
_NEXT_INC_NO = "`NEXT PRODUCT INCREMENT: NOT AUTHORIZED`"
_NEXT_STEP = "`NEXT STEP: LEAD-CONTROLLED NEXT-INCREMENT REASSESSMENT`"     # history only after the Stage 18 closure
# Stage 18 closure (2026-10-01): STAGE 18 — COMPLETE for the current Mechanical + Electrical / Electronics scope only;
# the sequential marker moves to Stage 19 for NAVIGATION ONLY — the closure authorizes no Stage-19 implementation.
_S18_COMPLETE = "`STAGE 18: COMPLETE — CURRENT MECHANICAL + ELECTRICAL / ELECTRONICS SCOPE`"
_S18C_DELIVERED = "`STAGE 18 CLOSURE: DELIVERED`"
_S19_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 19 — ENTERED / NOT COMPLETE — NAVIGATION ONLY`"
_NO_S19 = "`NO STAGE-19 IMPLEMENTATION AUTHORIZED BY STAGE-18 CLOSURE`"
_MSNL_FUTURE = "`MSNL: FUTURE / DEFERRED / NOT ACTIVATED`"
_NEXT_STAGE_STEP = "`NEXT STEP: LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT`"
# Stage 19 closure (2026-10-01): STAGE 19 — COMPLETE for the current planning-only scope only; the sequential marker
# moves to Stage 20 for NAVIGATION ONLY — the closure authorizes no Stage-20 implementation. The Stage-18 closure's
# own `NO STAGE-19 IMPLEMENTATION ...` token stays TRUE history inside its delivered record.
_S19_COMPLETE = "`STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE`"
_S19C_DELIVERED = "`STAGE 19 CLOSURE: DELIVERED`"
_S20_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 20 — ENTERED / PARTIAL — NAVIGATION ONLY`"
_NO_S20 = "`NO STAGE-20 IMPLEMENTATION AUTHORIZED BY STAGE-19 CLOSURE`"
_S19_LIMITS = ("`FULL CAP-09: NOT AUTHORIZED`", "`FULL WS-PFV-001: NOT AUTHORIZED`",
               "`RESULT OUTCOME / PASS-FAIL JUDGEMENT: NOT AUTHORIZED`",
               "`FORMAL EXPERIMENTAL VARIABLE MODEL: NOT AUTHORIZED`")
# Stage 20 closure (2026-10-01): STAGE 20 — COMPLETE for the current Owner-declared assumption scope only; the
# sequential marker moves to Stage 21 for NAVIGATION ONLY — the closure authorizes no Stage-21 implementation. The
# Stage-19 closure's own `NO STAGE-20 IMPLEMENTATION ...` token stays TRUE history inside its delivered record.
_S20_COMPLETE = "`STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE`"
_S20C_DELIVERED = "`STAGE 20 CLOSURE: DELIVERED`"
_S21_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 21 — ENTERED / PARTIAL — NAVIGATION ONLY`"
_NO_S21 = "`NO STAGE-21 IMPLEMENTATION AUTHORIZED BY STAGE-20 CLOSURE`"
_S20_LIMITS = ("`FULL CAP-08: NOT AUTHORIZED`", "`FULL CAP-10: NOT AUTHORIZED`")
# Stage 21 closure (2026-10-01): STAGE 21 — COMPLETE for the current Owner-declared contradiction scope only; the
# sequential marker moves to Stage 22 for NAVIGATION ONLY — the closure authorizes no Stage-22 implementation. The
# Stage-20 closure's own `NO STAGE-21 IMPLEMENTATION ...` token stays TRUE history inside its delivered record.
_S21_COMPLETE = "`STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE`"
_S21C_DELIVERED = "`STAGE 21 CLOSURE: DELIVERED`"
_S22_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 22 — ENTERED / PARTIAL — NAVIGATION ONLY`"
_NO_S22 = "`NO STAGE-22 IMPLEMENTATION AUTHORIZED BY STAGE-21 CLOSURE`"
_S21_LIMITS = ("`FULL CAP-10: NOT AUTHORIZED`", "`AUTOMATIC / AI CONTRADICTION DETECTION: NOT AUTHORIZED`",
               "`SYSTEM_INFERRED CONTRADICTION WRITER: NOT AUTHORIZED`")
# Stage 22 closure (2026-10-01): STAGE 22 — COMPLETE for the current bounded decision trace + decision room scope
# only, recorded with NO PRODUCT CHANGE (the delivered CAP-05 + CAP-07 Slices 1–2 are its whole basis); the sequential
# marker moves to Stage 23 (NOT ENTERED) for NAVIGATION ONLY — the closure authorizes no Stage-23 implementation and
# activates no CAP-06. The Stage-21 closure's own `NO STAGE-22 IMPLEMENTATION ...` token stays TRUE history inside its
# delivered record.
_S22_COMPLETE = "`STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE + DECISION ROOM SCOPE`"
_S22C_DELIVERED = "`STAGE 22 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`"
_S23_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 23 — NOT ENTERED — NAVIGATION ONLY`"
_NO_S23 = "`NO STAGE-23 IMPLEMENTATION AUTHORIZED BY STAGE-22 CLOSURE`"
_S22_LIMITS = ("`FULL CAP-05: NOT AUTHORIZED`", "`FULL CAP-07: NOT AUTHORIZED`")
# Stage 23 closure (2026-10-02): STAGE 23 — COMPLETE for the current bounded four-axis Readiness Snapshot scope ONLY,
# recorded with NO PRODUCT CHANGE (the existing user-facing snapshot is its whole basis); full CAP-06 stays NOT
# AUTHORIZED and its eight-axis expansion is not implemented or closed; the sequential marker moves to Stage 24
# (NOT ENTERED) for NAVIGATION ONLY. The Stage-22 closure's own `NO STAGE-23 IMPLEMENTATION ...` token stays TRUE
# history inside its delivered record.
_S23_COMPLETE = "`STAGE 23: COMPLETE — CURRENT BOUNDED FOUR-AXIS READINESS-SNAPSHOT SCOPE ONLY`"
_S23C_DELIVERED = "`STAGE 23 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`"
_S23_LIMITS = ("`CURRENT READINESS SNAPSHOT AXES: TECHNICAL / COMMERCIAL / MANUFACTURING / INTEGRATION`",
               "`NO SINGLE READINESS SCORE OR HIDDEN WEIGHTING AUTHORIZED`", "`FULL CAP-06: NOT AUTHORIZED`",
               "`FULL EIGHT-AXIS CAP-06: NOT IMPLEMENTED / NOT CLOSED`")
# AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1 (2026-10-03, recorded in its after-merge form):
# Stage 24 is ENTERED / PARTIAL for that slice ONLY (checkbox unticked, NOT complete); the marker stays on Stage 24;
# ACTIVE CONTRACT returns to NONE; full CAP-12 stays NOT AUTHORIZED and Stage 25 NOT AUTHORIZED. The pre-slice
# NOT-ENTERED forms become stale on every live surface. The Stage-23 closure's own `NO STAGE-24 IMPLEMENTATION ...`
# token stays TRUE history inside its delivered record.
_S24_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 24 — ENTERED / PARTIAL — NAVIGATION ONLY`"
_NO_S24 = "`NO STAGE-24 IMPLEMENTATION AUTHORIZED BY STAGE-23 CLOSURE`"
_S24_DELIVERED = "`STAGE 24 — CAP-12 FORM MOCK-UP ADVISORY SLICE 1: DELIVERED`"
_S24_PARTIAL = "`STAGE 24: ENTERED / PARTIAL — CAP-12 FORM MOCK-UP ADVISORY SLICE 1 ONLY`"
_S24_LIMITS = ("`FULL CAP-12: NOT AUTHORIZED`", "`STAGE 25: NOT AUTHORIZED`")
_S24_PRE_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 24 — NOT ENTERED — NAVIGATION ONLY`"
# After the delivered Slice 1 a live surface may no longer carry the pre-slice Stage-24 NOT-ENTERED state.
_S24C_STALE = (_tok(_S24_PRE_MARKER), _tok("`STAGE 24: NOT ENTERED`"),
               r"Stage 24 NOT ENTERED — navigation only", r"NO ACTIVE CONTRACT — post-Stage-23-closure",
               r"\(post-Stage-23-closure;")
# AMENDED at the Stage 24 closure (2026-10-04): STAGE 24 — COMPLETE for the current bounded CAP-12 Form Mock-up Advisory
# Slice 1 scope ONLY (checkbox ticked for that scope only); the marker is Stage 25 (NOT ENTERED) for navigation only;
# ACTIVE CONTRACT stays NONE; full CAP-12, further CAP-12 slices, CAP-13 activation and Stage 25 stay NOT AUTHORIZED. The
# ENTERED / PARTIAL forms become stale on every live surface; the Stage-23 closure's `NO STAGE-24 …` token and the
# Slice-1 DELIVERED token stay TRUE history.
_S24_COMPLETE = "`STAGE 24: COMPLETE — CURRENT BOUNDED CAP-12 FORM MOCK-UP ADVISORY SLICE 1 SCOPE ONLY`"
_S24C_DELIVERED = "`STAGE 24 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`"
# ROTATED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1 (2026-10-08): the live marker is Stage 25
# — ENTERED / PARTIAL; the pre-slice NOT-ENTERED marker survives as _S25_PRE_MARKER (history only). The Stage-24 closure's
# `NO STAGE-25 …` token stays TRUE history; its CAP-13 / Stage-25 limits (`CAP-13: NOT ACTIVATED`, `STAGE 25: NOT
# ENTERED`, `STAGE 25: NOT AUTHORIZED`) are no longer live and leave _S24C_LIMITS.
_S25_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 25 — ENTERED / PARTIAL — NAVIGATION ONLY`"
_S25_PRE_MARKER = "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 25 — NOT ENTERED — NAVIGATION ONLY`"
_NO_S25 = "`NO STAGE-25 IMPLEMENTATION AUTHORIZED BY STAGE-24 CLOSURE`"
_S24C_LIMITS = ("`FULL CAP-12: NOT AUTHORIZED`", "`FURTHER CAP-12 SLICES: NOT AUTHORIZED`")
# After the Stage 24 closure a live surface may no longer carry the ENTERED / PARTIAL Stage-24 state or marker.
_S24CL_STALE = (_tok(_S24_MARKER), _tok(_S24_PARTIAL), r"CURRENT MASTER ROADMAP STAGE: Stage 24\b",
                r"Stage 24 ENTERED / PARTIAL — navigation only", r"Stage 24 is ENTERED / PARTIAL",
                r"checkbox stays unticked; Stage 24 is NOT complete",
                r"MASTER ROADMAP SEQUENTIAL MARKER:? is (?:now )?Stage 24 for navigation only",
                r"NO ACTIVE CONTRACT — post-Stage-24-CAP-12-Slice-1", r"\(post-Stage-24-CAP-12-Slice-1;")
# ADVANCED at the Stage 35 first bounded slice (2026-10-05): the live contract is the Stage 35 first bounded structured
# invention disclosure export slice; Stage 35 is ENTERED / PARTIAL for that slice ONLY — not delivered, not complete,
# not closed, its merge and closure not authorized — and its roadmap checkbox stays unticked (23 of 45 rows stay
# unticked). The post-Stage-24-closure `ACTIVE CONTRACT: NONE`, with its next-increment and next-step tokens, survives
# only as superseded history. Git / GitHub own the slice's branch, PR, commit, CI and merge state, so no PR number or
# SHA is pinned here.
# ADVANCED at the delivery of the Stage 35 first bounded slice (2026-10-05): the slice is DELIVERED and no merge
# authorization is pending any more; Stage 35 stays ENTERED / PARTIAL, NOT complete and NOT closed, the active contract
# stays the slice until a separate Owner closure decision, row 35 stays unticked and 23 of 45 rows stay unticked. The
# pre-merge wording (merge authorization NO, NOT DELIVERED, the candidate identity) survives only as superseded history.
_S35_NAME = "Stage 35 — Structured Invention Disclosure Export — First Bounded Product Slice"
_S35_CONTRACT = "STAGE 35 — FIRST BOUNDED STRUCTURED INVENTION DISCLOSURE EXPORT SLICE"
_S35_HEADING = "## Current authority — " + _S35_NAME + " (Owner authorization, 2026-10-05)"
_S35_ACTIVE = "`ACTIVE CONTRACT: " + _S35_CONTRACT + "`"
_S35_BOLD = "**ACTIVE CONTRACT: " + _S35_CONTRACT + ".**"
_S35_ENTERED = "`STAGE 35: ENTERED / PARTIAL — FIRST BOUNDED SLICE ONLY`"
_S35_FURTHER_NO = "`FURTHER PRODUCT INCREMENT: NOT AUTHORIZED`"
_S35_FACTS = (_S35_ENTERED, "`STAGE 35 OWNER IMPLEMENTATION AUTHORIZATION: YES`",
              "`STAGE 35 FIRST BOUNDED SLICE IMPLEMENTATION: EXISTS`", "`STAGE 35 FIRST BOUNDED SLICE: DELIVERED`",
              "`STAGE 35: NOT COMPLETE`", "`STAGE 35: NOT CLOSED`",
              "`STAGE 35 CLOSURE: NOT AUTHORIZED`", "`LATER STAGE-35 SLICES: NOT AUTHORIZED`")
_S35_LIMITS = ("`STAGE 35 PDF / EMAIL DELIVERY / API EXPOSURE / EXTERNAL TRANSFER / AI OR PROVIDER CALLS: NOT AUTHORIZED`",
               "`PATENT-CLAIM DRAFTING / PATENTABILITY / FTO / LEGAL-VALIDITY CONCLUSIONS: NOT AUTHORIZED`")
# The live token sequence, in surface order; the checklist's plain-text state block carries the same lines.
_S35_TOKENS = (_S35_ACTIVE,) + _S35_FACTS + _S35_LIMITS + (_S35_FURTHER_NO,)
# ADVANCED at the Stage 35 closure (2026-10-05): STAGE 35 — COMPLETE for the current bounded Structured Invention
# Disclosure Export first-slice scope ONLY (row 35 ticked for that scope only; 22 of 45 rows stay unticked), recorded with
# no product change; ACTIVE CONTRACT is NONE again with its next-increment and next-step tokens; the first bounded slice
# stays DELIVERED; later Stage-35 slices, PDF / e-mail / API / external transfer / AI or provider use and patent-claim /
# patentability / FTO / legal-validity conclusions stay NOT AUTHORIZED; the legal-adviser / release triggers stay
# preserved; Stage 36 stays NOT ENTERED and NOT AUTHORIZED; the MASTER ROADMAP SEQUENTIAL MARKER is unchanged. The
# Stage-35 active-increment wording survives only as superseded history. Git / GitHub own the closure's PR, merge and
# review identity, so no PR number or SHA is pinned here.
_NONE_BOLD = "**ACTIVE CONTRACT: NONE.**"
_S35C_NAME = "Stage 35 — Structured Invention Disclosure Export — Closure"
_S35C_HEADING = "## Current authority — post-Stage-35-closure: no active contract (2026-10-05)"
_S35C_DELIVERED = "`STAGE 35 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`"
_S35_COMPLETE = "`STAGE 35: COMPLETE — CURRENT BOUNDED STRUCTURED INVENTION DISCLOSURE EXPORT FIRST-SLICE SCOPE ONLY`"
_S35_SLICE_DELIVERED = "`STAGE 35 FIRST BOUNDED SLICE: DELIVERED`"
_S35_LATER_NO = "`LATER STAGE-35 SLICES: NOT AUTHORIZED`"
_S35_TRIGGERS = "`STAGE 35 LEGAL-ADVISER / RELEASE TRIGGERS: PRESERVED`"
_S36_NOT = ("`STAGE 36: NOT ENTERED`", "`STAGE 36: NOT AUTHORIZED`")
# ROTATED at the Stage 36 closure: the Stage 35 closure facts no longer include the Stage-36 NOT-ENTERED tokens
_S35C_FACTS = ((_S35C_DELIVERED, _S35_COMPLETE, _S35_SLICE_DELIVERED, _S35_LATER_NO) + _S35_LIMITS + (_S35_TRIGGERS,))
# The live token sequence, in surface order; the checklist's plain-text state block carries the same lines.
_S35C_TOKENS = (_NONE718, _NEXT_INC_NO, _NEXT_STAGE_STEP) + _S35C_FACTS
# The Stage-35 active-increment tokens that the closure retired (the slice delivery, later-slice and limit tokens stay).
_S35_ACTIVE_ONLY = tuple(t for t in _S35_TOKENS if t not in _S35C_TOKENS)
# After the Stage 35 closure a live surface may no longer carry the Stage-35 active-increment state, its pre-merge
# status or the post-Stage-24-closure NONE heading.
_S35C_STALE = tuple(_tok(t) for t in _S35_ACTIVE_ONLY) + (
    r"ACTIVE CONTRACT: STAGE 35\b", r"ACTIVE BOUNDED PRODUCT INCREMENT — Stage 35",
    r"is the active bounded product increment", r"ONE Owner-authorized bounded product increment is\s+active",
    r"Stage 35 is ENTERED / PARTIAL", r"Stage 35 ENTERED / PARTIAL —",
    r"active contract stays (?:this|that) first bounded slice", r"until a separate Owner closure decision",
    r"Stage 35 roadmap checkbox stays UNTICKED", r"closure authorization NO",
    r"the Owner has since separately authorized ONE bounded product increment",
    r"After the Stage 24 closure the Owner separately authorized ONE bounded product increment",
    r"Before it, no product increment was authorized after Stage 24",
    r"NO ACTIVE CONTRACT — post-Stage-24-closure", r"\(post-Stage-24-closure;",
    r"STAGE 35 MERGE AUTHORIZATION: NO", r"STAGE 35 FIRST BOUNDED SLICE: NOT DELIVERED",
    r"merge authorization NO", r"first bounded slice only[,;] NOT delivered", r"owns (?:its|the) candidate identity",
    r"its merge needs its own Lead / Owner decision")
# Stage 35 is COMPLETE for its current bounded first-slice scope ONLY: an unscoped or global completion, a stage-level
# delivery / merge claim, a reopened or undone closure, the slice back to not delivered, an authorized later slice, a
# lifted exclusion, dropped legal-adviser / release triggers or a Stage-36 advance is a reversal of the live truth.
_S35C_REVERSALS = (
    r"STAGE 35: (?!COMPLETE — CURRENT BOUNDED STRUCTURED INVENTION DISCLOSURE EXPORT FIRST-SLICE SCOPE ONLY\b)",
    r"STAGE 35 COMPLETE: YES", r"STAGE 35 CLOSURE: (?!DELIVERED — NO PRODUCT CHANGE REQUIRED\b)",
    r"STAGE 35 FIRST BOUNDED SLICE: (?!DELIVERED\b)", r"STAGE 35 MERGE AUTHORIZATION: ",
    # kept from the active-increment state: a reversed owner authorization or implementation token stays a reversal
    # (their affirmative forms are retired, stale tokens above)
    r"STAGE 35 OWNER IMPLEMENTATION AUTHORIZATION: (?!YES\b)", r"STAGE 35 FIRST BOUNDED SLICE IMPLEMENTATION: (?!EXISTS\b)",
    r"(?<!no )(?<!not )\bStage[- ]35 merge (?:is |was |has been )?authorized\b",
    r"LATER STAGE-35 SLICES: (?!NOT AUTHORIZED)", r"FURTHER PRODUCT INCREMENT: (?!NOT AUTHORIZED)",
    r"NEXT PRODUCT INCREMENT: (?!NOT AUTHORIZED)", r"AI OR PROVIDER CALLS: (?!NOT AUTHORIZED)",
    r"LEGAL-VALIDITY CONCLUSIONS: (?!NOT AUTHORIZED)", r"LEGAL-ADVISER / RELEASE TRIGGERS: (?!PRESERVED\b)",
    r"Stage 35\s+(?:is|was|has been)\s+(?:now\s+)?(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b"
    r"(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?for\s+(?:the|its)\s+current\s+bounded\b)",
    r"Stage 35\s+(?:is|was|has been)\s+(?:now\s+)?(?:fully|globally)\s+(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b",
    r"Stage 35\s+(?:is|was|has been)\s+(?:now\s+)?(?:DELIVERED|MERGED)\b",
    r"Stage 35 COMPLETE\b(?!\s+for\s+(?:the|its)\s+current\s+bounded\b)",
    r"(?<!no )(?<!not )\blater Stage[- ]35 slices? (?:is |are |was |were |has been |have been )?(?:now )?authorized\b",
    # ROTATED at the Stage 36 closure: Stage 36 is COMPLETE for its current no-live-AI / provider scope only, so only
    # that status token, a scoped completion and no implementation authorization are live truth
    r"STAGE 36: (?!COMPLETE — CURRENT NO-LIVE-AI / PROVIDER SCOPE ONLY\b)",
    r"Stage 36\s+(?:is|was|has been)\s+(?:now\s+)?(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b"
    r"(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?for\s+(?:the|its)\s+current\s+no-live-AI\b)",
    r"Stage 36\s+(?:is|was|has been)\s+(?:now\s+)?(?:fully|globally)\s+(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b",
    r"Stage 36\s+(?:is|was|has been)\s+(?:now\s+)?(?:ENTERED|AUTHORIZED|DELIVERED|IMPLEMENTED|ACTIVATED)\b",
    r"Stage 36 COMPLETE\b(?!\s+for\s+(?:the|its)\s+current\s+no-live-AI\b)",
    r"(?<!NO )STAGE-36 IMPLEMENTATION (?:IS )?AUTHORIZED",
    r"(?<!no )(?<!not )\bStage-36 (?:work|implementation) (?:is |was |has been )?(?:now )?authorized\b")
# ADVANCED at the Stage 36 closure (2026-10-05): STAGE 36 — COMPLETE for the current no-live-AI / provider scope ONLY
# (row 36 ticked for that scope only; 21 of 45 rows stay unticked), recorded with no product change; ACTIVE CONTRACT stays
# NONE; no production live AI / provider selection exists and none is active; CAP-15 / CAP-17 stay RECORDED — NOT AUTHORIZED FOR
# IMPLEMENTATION; the External Engineering Tools direction stays PLANNED / DEFERRED with no provider selected; a future
# live AI / provider selection or External Engineering Tools activation needs a fresh Stage-36 reassessment and separate
# authorization; Stage 37 stays NOT ENTERED and NOT AUTHORIZED; the MASTER ROADMAP SEQUENTIAL MARKER is unchanged. The
# Stage 35 closure's Stage-36 NOT-ENTERED tokens and the post-Stage-35-closure NONE survive only as history.
_S36C_NAME = "Stage 36 — CAP-15 + CAP-17 — Closure"
_S36C_HEADING = "## Current authority — post-Stage-36-closure: no active contract (2026-10-05)"
_S36C_DELIVERED = "`STAGE 36 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`"
_S36_COMPLETE = "`STAGE 36: COMPLETE — CURRENT NO-LIVE-AI / PROVIDER SCOPE ONLY`"
_S36_LIMITS = ("`PRODUCTION LIVE AI / PROVIDER: NOT SELECTED — NOT ACTIVE`",
               "`CAP-15 / CAP-17: RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`",
               "`EXTERNAL ENGINEERING TOOLS: PLANNED / DEFERRED — NO PROVIDER SELECTED`",
               "`FUTURE LIVE AI / PROVIDER SELECTION OR EXTERNAL ENGINEERING TOOLS ACTIVATION: FRESH STAGE-36 "
               "REASSESSMENT + SEPARATE AUTHORIZATION REQUIRED`")
_S37_NOT = ("`STAGE 37: NOT ENTERED`", "`STAGE 37: NOT AUTHORIZED`")
_S36C_FACTS = (_S36C_DELIVERED, _S36_COMPLETE) + _S36_LIMITS + _S37_NOT
# The live token sequence, in surface order; the checklist's plain-text state block carries the same lines.
_S36C_TOKENS = (_NONE718, _NEXT_INC_NO, _NEXT_STAGE_STEP) + _S36C_FACTS + _S35C_FACTS
# After the Stage 36 closure a live surface may no longer carry the Stage-36 NOT-ENTERED state or the
# post-Stage-35-closure NONE heading.
_S36C_STALE = (_tok(_S36_NOT[0]), _tok(_S36_NOT[1]), r"NO ACTIVE CONTRACT — post-Stage-35-closure",
               r"\(post-Stage-35-closure;", r"Stage 36 stays NOT ENTERED", r"Stage 36 is NOT ENTERED",
               r"Stage 36 NOT ENTERED")
# Stage 36 is COMPLETE for its current no-live-AI / provider scope ONLY: an undone closure, a selected or active
# production live AI / provider, an implemented CAP-15 / CAP-17, an activated External Engineering Tools direction, a
# waived fresh reassessment or a Stage-37 advance is a reversal of the live truth.
_S36C_REVERSALS = (
    r"STAGE 36 CLOSURE: (?!DELIVERED — NO PRODUCT CHANGE REQUIRED\b)",
    r"PRODUCTION LIVE AI / PROVIDER: (?!NOT SELECTED — NOT ACTIVE\b)",
    r"CAP-15 / CAP-17: (?!RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION\b)",
    r"EXTERNAL ENGINEERING TOOLS: (?!PLANNED / DEFERRED — NO PROVIDER SELECTED\b)",
    r"EXTERNAL ENGINEERING TOOLS ACTIVATION: (?!FRESH STAGE-36 REASSESSMENT \+ SEPARATE AUTHORIZATION REQUIRED\b)",
    r"(?<!no )\bproduction live AI / provider (?:is |has been )(?:now )?(?:selected|active)\b",
    r"(?<!no )(?<!not )\bCAP-1[57](?: / CAP-17)? (?:is |are |was |were |has been |have been )?(?:now )?"
    r"(?:implemented|activated)\b",
    r"STAGE 37: (?!NOT ENTERED\b|NOT AUTHORIZED\b)",
    r"Stage 37\s+(?:is|was|has been)\s+(?:now\s+)?(?:ENTERED|COMPLETE|AUTHORIZED)\b",
    r"(?<!NO )STAGE-37 IMPLEMENTATION (?:IS )?AUTHORIZED",
    r"(?<!no )(?<!not )\bStage-37 (?:work|implementation) (?:is |was |has been )?(?:now )?authorized\b")
# ADVANCED at the Stage 16 closure (2026-10-06): STAGE 16 — COMPLETE for the current bounded Technical + Integration
# evidence-sufficiency composition scope ONLY (row 16 ticked for that scope only; 20 of 45 rows stay unticked), recorded
# with no further product change after the Owner-authorized bounded presentation residual (the Technical-Row Focus-Scope
# Disclosure) was delivered; ACTIVE CONTRACT stays NONE; Technical and Integration stay independently visible from their own
# owners and nothing is aggregated; no SRL number or level, single score or weakest-axis computation exists or is
# authorized; Stages 13 and 14 stay PARTIAL / DEFERRED; the MASTER ROADMAP SEQUENTIAL MARKER is unchanged. The
# post-Stage-36-closure NONE and the "routing past … 16 and 17" wording survive only as history.
_S16C_NAME = "Stage 16 — SRL-Compatible Composition — Closure"
_S16_NAME = "Stage 16 — SRL-Compatible Composition — Technical-Row Focus-Scope Disclosure"
_S16C_HEADING = "## Current authority — post-Stage-16-closure: no active contract (2026-10-06)"
_S16C_DELIVERED = "`STAGE 16 CLOSURE: DELIVERED — NO FURTHER PRODUCT CHANGE REQUIRED`"
_S16_COMPLETE = "`STAGE 16: COMPLETE — CURRENT BOUNDED TECHNICAL + INTEGRATION EVIDENCE-SUFFICIENCY COMPOSITION SCOPE ONLY`"
_S16_DELIVERED = "`STAGE 16 — TECHNICAL-ROW FOCUS-SCOPE DISCLOSURE: DELIVERED`"
_S16_SRL_NO = "`SRL LEVEL / SINGLE SCORE / WEAKEST-AXIS COMPUTATION: NOT AUTHORIZED`"
_S13_14_PARTIAL = ("`STAGE 13: PARTIAL / DEFERRED`", "`STAGE 14: PARTIAL / DEFERRED`")
_S16C_FACTS = (_S16C_DELIVERED, _S16_COMPLETE, _S16_DELIVERED, _S16_SRL_NO) + _S13_14_PARTIAL
# ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1 (2026-10-08, recorded in its
# after-merge form): Stage 25 is ENTERED / PARTIAL for that slice ONLY (row 25 unticked, NOT complete; the count stays
# 25 of 45 ticked, 20 unticked); ACTIVE CONTRACT stays NONE; full CAP-13, any further method or consumer and any unit
# conversion stay NOT AUTHORIZED. The post-Stage-16-closure NONE heading and the pre-slice Stage-25 NOT-ENTERED forms
# survive only as history. Git / GitHub own the slice's PR and merge identity, so none is pinned here.
_S25_NAME = "Stage 25 — CAP-13 Two-Support Static Reactions — Slice 1"
_S25_HEADING = "## Current authority — post-Stage-25-CAP-13-Slice-1: no active contract (2026-10-08)"
_S25_DELIVERED = "`STAGE 25 — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1: DELIVERED`"
_S25_PARTIAL = "`STAGE 25: ENTERED / PARTIAL — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1 ONLY`"
_S25_FULL_NO = "`FULL CAP-13: NOT AUTHORIZED`"
_S25_FACTS = (_S25_DELIVERED, _S25_PARTIAL, _S25_FULL_NO, _S25_MARKER)
# The live token sequence, in surface order; the checklist's plain-text state block carries the same lines.
_S16C_TOKENS = (_NONE718, _NEXT_INC_NO, _NEXT_STAGE_STEP) + _S25_FACTS + _S16C_FACTS + _S36C_FACTS + _S35C_FACTS
# After the delivered Stage 25 slice a live surface may no longer carry the pre-slice Stage-25 / CAP-13 state.
_S25_STALE = (_tok(_S25_PRE_MARKER), _tok("`STAGE 25: NOT ENTERED`"), _tok("`STAGE 25: NOT AUTHORIZED`"),
              _tok("`CAP-13: NOT ACTIVATED`"), r"Stage 25 NOT ENTERED — navigation only",
              r"NO ACTIVE CONTRACT — post-Stage-16-closure", r"\(post-Stage-16-closure;",
              r"CURRENT MASTER ROADMAP STAGE: Stage 25 — CAP-13 thickness / specification / safety capability — NOT ENTERED",
              r"Stage 25 / CAP-13 stays NOT ENTERED and NOT AUTHORIZED", r"Stages 25–27 preserved")
# Stage 25 is ENTERED / PARTIAL for the Two-Support Static Reactions Slice 1 ONLY: an unscoped entry, any completion or
# closure, full CAP-13, a second method or consumer, a unit conversion or a broad CAP-13 activation is a reversal.
_S25_REVERSALS = (
    r"STAGE 25: (?!ENTERED / PARTIAL — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1 ONLY\b)",
    r"STAGE 25 COMPLETE: YES", r"STAGE 25 — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1: (?!DELIVERED\b)",
    r"FULL CAP-13: (?!NOT AUTHORIZED\b)",
    r"Stage 25\s+(?:is|was|has been)\s+(?:now\s+)?(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b",
    r"(?<!no )(?<!not )\b(?:a |any )?(?:second|another|further) (?:CAP-13 )?(?:method|consumer) "
    r"(?:is |was |has been )?(?:now )?(?:admitted|authorized)\b",
    r"(?<!no )(?<!not )\bunit conversion (?:is |was |has been )?(?:now )?(?:admitted|authorized|implemented)\b",
    r"(?<!no )(?<!not )\bCAP-13 (?:is |has been )(?:now )?(?:fully |globally )?(?:activated|authorized)\b")
# ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1 (2026-10-09, recorded in its
# after-merge form): Stage 27 is ENTERED / PARTIAL for that slice ONLY (row 27 unticked, NOT complete; the count stays 25
# of 45 ticked, 20 unticked); ACTIVE CONTRACT stays NONE; the MASTER ROADMAP SEQUENTIAL MARKER is unchanged (Stage 25);
# full THERM-01 stays NOT AUTHORIZED. The shared owner admits exactly two methods under the accepted Correction 02. The
# post-Stage-25-CAP-13-Slice-1 NONE heading survives only as history. Git / GitHub own the slice's PR and merge identity.
_S27_NAME = "Stage 27 — THERM-01 Single-Path Temperature-Difference — Slice 1"
# ROTATED at the Stage 27 closure (2026-10-09; documentation / current-truth only, no product change): the live NONE is
# post-Stage-27-closure and Stage 27 is COMPLETE for the current bounded THERM-01 single-path temperature-difference scope
# ONLY (row 27 ticked for that scope only; the count is 26 of 45 ticked, 19 unticked). The slice's ENTERED / PARTIAL token
# and the post-Stage-27-THERM-01-Slice-1 NONE heading survive only as history (_S27_PARTIAL, _S27_SLICE_HEADING).
_S27_SLICE_HEADING = "## Current authority — post-Stage-27-THERM-01-Slice-1: no active contract (2026-10-09)"
_S27_HEADING = "## Current authority — post-Stage-27-closure: no active contract (2026-10-09)"
_S27C_NAME = "Stage 27 — THERM-01 Single-Path Temperature-Difference — Closure"
_S27_DELIVERED = "`STAGE 27 — THERM-01 SINGLE-PATH TEMPERATURE-DIFFERENCE SLICE 1: DELIVERED`"
_S27_PARTIAL = "`STAGE 27: ENTERED / PARTIAL — THERM-01 SINGLE-PATH TEMPERATURE-DIFFERENCE SLICE 1 ONLY`"
_S27C_DELIVERED = "`STAGE 27 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`"
_S27_COMPLETE = "`STAGE 27: COMPLETE — CURRENT BOUNDED THERM-01 SINGLE-PATH TEMPERATURE-DIFFERENCE SCOPE ONLY`"
_S27_FULL_NO = "`FULL THERM-01: NOT AUTHORIZED`"
_S27_FACTS = (_S27C_DELIVERED, _S27_COMPLETE, _S27_DELIVERED, _S27_FULL_NO)
# After the Stage 27 closure a live surface may no longer carry the earlier NONE headings, the slice's ENTERED / PARTIAL
# state or the pre-slice "Stages 26–27 preserved" / Stage-27 NOT-ENTERED state.
_S27_STALE = (r"NO ACTIVE CONTRACT — post-Stage-25-CAP-13-Slice-1", r"\(post-Stage-25-CAP-13-Slice-1;",
              r"CURRENT SUBTASK:\*\* NONE \(post-Stage-25-CAP-13-Slice-1\)", _tok("`STAGE 27: NOT ENTERED`"),
              _tok("`STAGE 27: NOT AUTHORIZED`"), r"Stages 26–27 preserved", r"26–27 not authorized",
              r"NO ACTIVE CONTRACT — post-Stage-27-THERM-01-Slice-1", r"\(post-Stage-27-THERM-01-Slice-1;",
              r"CURRENT SUBTASK:\*\* NONE \(post-Stage-27-THERM-01-Slice-1\)", _tok(_S27_PARTIAL),
              r"Stage 27 (?:is )?NOT complete", r"Stage 27 ENTERED / PARTIAL", r"27 ENTERED / PARTIAL through")
# Stage 27 is ENTERED / PARTIAL for the THERM-01 Single-Path Temperature-Difference Slice 1 ONLY: an unscoped entry, any
# completion or closure, full THERM-01, a third method, a temperature / rating / margin claim or a unit conversion is a
# reversal.
# AMENDED at the Stage 27 closure: Stage 27 is COMPLETE for the current bounded scope ONLY; an unscoped completion or a
# closure that is not the documentation-only one stays a reversal.
_S27_REVERSALS = (
    r"STAGE 27: (?!COMPLETE — CURRENT BOUNDED THERM-01 SINGLE-PATH TEMPERATURE-DIFFERENCE SCOPE ONLY\b)",
    r"STAGE 27 COMPLETE: YES", r"STAGE 27 — THERM-01 SINGLE-PATH TEMPERATURE-DIFFERENCE SLICE 1: (?!DELIVERED\b)",
    r"STAGE 27 CLOSURE: (?!DELIVERED — NO PRODUCT CHANGE REQUIRED\b)",
    r"FULL THERM-01: (?!NOT AUTHORIZED\b)",
    r"Stage 27\s+(?:is|was|has been)\s+(?:now\s+)?(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b"
    r"(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?for\s+(?:the|its)\s+current\s+bounded\s+THERM-01)",
    r"Stage 27 (?:is |was )?complete for (?:all|every|any|arbitrary)",
    r"(?<!no )(?<!not )\bthermal engineering (?:is |has been )(?:now )?(?:complete|completed)\b",
    r"(?<!no )(?<!not )\b(?:a |any )?(?:third|another|further) (?:THERM-01 )?(?:method|consumer) "
    r"(?:is |was |has been )?(?:now )?(?:admitted|authorized)\b",
    r"(?<!no )(?<!not )\bTHERM-01 (?:is |has been )(?:now )?(?:fully |globally )?(?:activated|authorized)\b",
    r"(?<!no )(?<!not )\b(?:absolute|junction) temperature (?:is |was )?(?:now )?(?:computed|predicted|authorized)\b")
# After the Stage 16 closure a live surface may no longer carry the post-Stage-36-closure NONE heading, Stage 16 among
# the stages routed past, the deferred Stage-16 dependency status or the "Stages 13–16 remain PARTIAL / OPEN" intro.
_S16C_STALE = (r"NO ACTIVE CONTRACT — post-Stage-36-closure", r"\(post-Stage-36-closure;",
               r"routing past Stages 11, 13, 14, 16 and 17", r"STAGE 16 — SRL-COMPATIBLE COMPOSITION: DEFERRED",
               r"Stages 13[–-]16 remain PARTIAL / OPEN", r"Stage 16 is unchanged\.")
# Stage 16 is COMPLETE for its current bounded Technical + Integration evidence-sufficiency composition scope ONLY: an
# undone closure, an unscoped or global completion, an SRL number / level, single score or weakest-axis computation, or
# Stage 13 / Stage 14 advanced beyond PARTIAL / DEFERRED is a reversal of the live truth.
_S16C_REVERSALS = (
    r"STAGE 16 CLOSURE: (?!DELIVERED — NO FURTHER PRODUCT CHANGE REQUIRED\b)",
    r"STAGE 16: (?!COMPLETE — CURRENT BOUNDED TECHNICAL \+ INTEGRATION EVIDENCE-SUFFICIENCY COMPOSITION SCOPE ONLY\b)",
    r"STAGE 16 — TECHNICAL-ROW FOCUS-SCOPE DISCLOSURE: (?!DELIVERED\b)",
    r"SRL LEVEL / SINGLE SCORE / WEAKEST-AXIS COMPUTATION: (?!NOT AUTHORIZED\b)",
    r"STAGE 1[34]: (?!PARTIAL / DEFERRED\b)",
    r"Stage 16\s+(?:is|was|has been)\s+(?:now\s+)?(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b"
    r"(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?for\s+(?:the|its)\s+current\s+bounded\s+Technical\b)",
    r"Stage 16\s+(?:is|was|has been)\s+(?:now\s+)?(?:fully|globally)\s+(?:COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b",
    r"Stage 16 COMPLETE\b(?!\s+for\s+(?:the|its)\s+current\s+bounded\s+Technical\b)",
    r"Stages? 1[34](?: and 1[34])?\s+(?:is|are|was|were|has been|have been)\s+(?:now\s+)?(?:COMPLETE|COMPLETED|CLOSED)\b",
    r"(?<!no )(?<!not )(?<!No )\b(?:an? )?SRL (?:number|level|score) (?:is |was |has been )?(?:now )?"
    r"(?:computed|calculated|assigned|authorized|implemented)\b",
    r"(?<!no )(?<!not )\bweakest[- ]axis (?:calculation|computation) (?:is |was |has been )?(?:now )?"
    r"(?:computed|implemented|authorized)\b",
    r"(?<!NO )STAGE-16 (?:FURTHER )?IMPLEMENTATION (?:IS )?AUTHORIZED",
    r"(?<!no )(?<!not )\bfurther Stage-16 (?:/ SRL )?(?:work|implementation) (?:is |was |has been )?(?:now )?"
    r"authorized\b")


def _any_pr(needle):
    """A literal Stage-16 needle as a regex in which the placeholder "PR #N" stands for any PR number: Git / GitHub own
    the PR identity, so the live text is never required to carry one particular number."""
    return re.escape(needle).replace(re.escape("PR #N"), r"PR #\d+")


# After the Stage 23 closure a live surface may no longer carry the pre-closure Stage-23 marker or NONE position.
_S23C_STALE = (_tok(_S23_MARKER), r"CURRENT MASTER ROADMAP STAGE: Stage 23\b",
               r"Stage 23 NOT ENTERED — navigation only",
               r"MASTER ROADMAP SEQUENTIAL MARKER:? is (?:now )?Stage 23 for navigation only",
               r"NO ACTIVE CONTRACT — post-Stage-28-closure", r"\(post-Stage-28-closure;")
# After the Stage 22 closure a live surface may no longer carry the pre-closure Stage-22 status or marker.
_S22C_STALE = (_tok("`STAGE 22: ENTERED / PARTIAL`"), _tok(_S22_MARKER),
               r"CURRENT MASTER ROADMAP STAGE: Stage 22\b", r"Stage-22 checkbox stays unticked",
               r"Stage 22 ENTERED / PARTIAL — navigation only",
               r"MASTER ROADMAP SEQUENTIAL MARKER:? is (?:now )?Stage 22 for navigation only")
# Stage 30 closure (2026-10-02): STAGE 30 — COMPLETE for the current optional-part enablement safeguard scope ONLY,
# recorded with no further product change (Bounded Slice 1 is its product basis) and NOT a global Stage-30 discharge:
# a future domain or root activation needs a new proportional reassessment. The owner name is split out of every
# literal here so no governance needle reads as idea text in the Stage-28 vocabulary sweep.
_CL = "CONTROL-" + "LOOP"
_S30C_DELIVERED = "`STAGE 30 CLOSURE: DELIVERED — NO FURTHER PRODUCT CHANGE REQUIRED`"
_S30_COMPLETE = "`STAGE 30: COMPLETE — CURRENT %s PART-ENABLEMENT SAFEGUARD SCOPE ONLY`" % _CL
_S30_PREREQ = "`CURRENT %s PART-ENABLEMENT STAGE-30 PREREQUISITE: SATISFIED`" % _CL
_S30_NOT_GLOBAL = "`STAGE 30 IS NOT GLOBALLY DISCHARGED FOR FUTURE DOMAINS OR FUTURE ROOT ACTIVATIONS`"
_S30_FUTURE = "`FUTURE DOMAIN / ROOT-ACTIVATION STAGE-30 REASSESSMENT: STILL REQUIRED WHEN APPLICABLE`"
_S30_SAFETY = ("`CURRENT BOUNDED SAFETY DISPOSITION: OPTIONAL-PART ANSWERS EXCLUDED FROM AUTOMATED SAFETYSIGNAL "
               "DERIVATION — EXPLICITLY DISCLOSED`")
_S30_FUTURE_SAFETY = "`FUTURE PART-AWARE %s SAFETY CAPABILITY: SEPARATELY QUALIFIABLE — NOT PROHIBITED`" % _CL
_S30C_TOKENS = (_S30C_DELIVERED, _S30_COMPLETE, _S30_PREREQ, _S30_NOT_GLOBAL, _S30_FUTURE, _S30_SAFETY,
                _S30_FUTURE_SAFETY)
# ADVANCED at the Stage 28 part-only enablement: Stage 28 stays partial, the part is PART-ONLY enabled (exactly one
# allowlisted domain) and NOT root-activated. These replace the closure-time "not enabled / allowlist empty" facts.
# ADVANCED at the Stage 28 closure: Stage 28 is COMPLETE for its bounded optional-part scope only, NOT globally
# discharged, and the root-activation blockers stay preserved.
_S30C_KEPT = ("`STAGE 28: COMPLETE — CURRENT BOUNDED %s OPTIONAL-PART SCOPE ONLY`" % _CL,
              "`STAGE 28 CLOSURE: DELIVERED — NO FURTHER PRODUCT CHANGE REQUIRED`",
              "`STAGE 28 IS NOT GLOBALLY DISCHARGED FOR FUTURE ADDITIONAL DOMAINS`",
              "`FUTURE ROOT ACTIVATION BLOCKERS: PRESERVED — NOT WAIVED`",
              "`STAGE 28 — %s OPTIONAL PART — PART-ONLY ENABLEMENT: DELIVERED`" % _CL,
              "`%s PART ELIGIBILITY: ENABLED — PART-ONLY`" % _CL,
              "`_PART_ONLY_DOMAINS: %s ONLY`" % _CL.replace("-", "_"),
              "`%s ROOT ACTIVATION: NOT ENABLED`" % _CL)
# After the Stage 30 closure a live surface may no longer carry the pre-closure Stage-30 status, and no surface may
# widen the scope-qualified completion into a global one.
_S30C_STALE = (_tok("`STAGE 30: ENTERED / PARTIAL — %s PART-ENABLEMENT SAFEGUARDS ONLY`" % _CL),
               r"Stage 30 (?:is )?ENTERED / PARTIAL for (?:these|the)", r"Stage 30 is NOT complete",
               r"STAGE 30: COMPLETE(?! — CURRENT)", r"Stage 30 (?:is )?(?:globally discharged|COMPLETE\.)",
               # AMENDED at the Stage 28 part-only enablement: the pre-enablement current statements
               r"part enablement itself stays NOT AUTHORIZED", r"pre-authorizes no `\w+` part enablement",
               r"NO ACTIVE CONTRACT — post-Stage-30-closure", r"\(post-Stage-30-closure;",
               # AMENDED at the Stage 28 closure: the pre-closure current statements
               r"NO ACTIVE CONTRACT — post-Stage-28-Part-Only-Enablement", r"\(post-Stage-28-Part-Only-Enablement;",
               r"Stage 28 is NOT complete")
# After the Stage 21 closure a live surface may no longer carry the pre-closure Stage-21 status or marker.
_S21C_STALE = (_tok("`STAGE 21: ENTERED / PARTIAL`"), _tok("`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 21 — ENTERED / "
                                                         "PARTIAL — NAVIGATION ONLY`"),
               r"CURRENT MASTER ROADMAP STAGE: Stage 21\b", r"Stage-21 checkbox stays unticked",
               r"Stage 21 ENTERED / PARTIAL — navigation only",
               r"MASTER ROADMAP SEQUENTIAL MARKER:? is (?:now )?Stage 21 for navigation only")
# After the Stage 20 closure a live surface may no longer carry the pre-closure Stage-20 status or marker.
_S20C_STALE = (_tok("`STAGE 20: ENTERED / PARTIAL`"), _tok(_S20_MARKER),
               r"CURRENT MASTER ROADMAP STAGE: Stage 20\b", r"Stage-20 checkbox stays unticked",
               r"Stage 20 ENTERED / PARTIAL — navigation only",
               r"MASTER ROADMAP SEQUENTIAL MARKER:? is (?:now )?Stage 20 for navigation only")
# After the Stage 19 closure a live surface may no longer carry the pre-closure Stage-19 status or marker.
_S19C_STALE = (_tok("`STAGE 19: ENTERED / NOT COMPLETE`"), _tok(_S19_MARKER),
               r"CURRENT MASTER ROADMAP STAGE: Stage 19\b", r"Stage-19 checkbox stays unticked",
               r"Stage 19 ENTERED / NOT COMPLETE — navigation only",
               r"MASTER ROADMAP SEQUENTIAL MARKER:? is Stage 19 for navigation only")
# After the Stage 18 closure a live surface may no longer carry the pre-closure Stage-18 status, marker or next step.
_S18C_STALE = (r"`STAGE 18 COMPLETE: NO`", _tok("`STAGE 18: ENTERED / PARTIAL / NOT COMPLETE`"), _tok(_S15_MARKER),
               _tok(_NEXT_STEP), r"Stage 18 (?:stays|remains) (?:\*\*)?(?:ENTERED|PARTIAL|STARTED)",
               r"MASTER ROADMAP SEQUENTIAL MARKER:? Stage 18 stays")
# Pre-merge Stage-15 wording that may survive ONLY inside a visibly superseded note.
_S15_PREMERGE_FORMS = (
    # ROTATED at the Stage 35 first bounded slice: the live contract token was the Stage-35 one
    # ROTATED back at the Stage 35 closure: the live contract token is NONE again; any other active-contract token (the
    # Stage-35 one included) is a reversal
    r"ACTIVE CONTRACT: STAGE 15", r"`ACTIVE CONTRACT: (?!NONE`)", r"\bPR NOT OPENED\b", r"\bMERGE NOT PERFORMED\b",
    r"PR #718[^.;]{0,40}\bnot (yet )?(opened|merged)", r"\bPR PENDING\b", r"REVIEW COMPLETE / PR PENDING",
    r"IMPLEMENTATION:? COMPLETE CANDIDATE", r"IMPLEMENTED CANDIDATE",
    r"Slice 1 \(implementation complete candidate\)", r"CURRENT REVIEWED PRODUCT HEAD",
    r"CURRENT BOUNDED PRODUCT ACTION — Stage 15", r"current bounded product action is Stage 15")
# A live surface may never reverse the post-#718 truth.
_S15_CLOSE_REVERSALS = (
    r"\bF1(?:-| — | )(OPEN|REMAINS OPEN)\b", r"\bF1 (is|remains) (open|unresolved)\b",
    r"STAGE 15: (?:ENTERED / (?:PARTIAL / )?)?COMPLETE`", r"STAGE 15 COMPLETE: YES",
    # Stage 15 closure: complete ONLY for the current Mechanical + Electrical / Electronics scope — any
    # unscoped completion, a validated IRL, an IRL level or an N-domain claim stays a reversal.
    r"Stage 15\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b"
    r"(?!\s+for\s+the\s+current\s+Mechanical)",
    r"VALIDATED IRL / IRL LEVEL CLAIM: AUTHORIZED", r"N-DOMAIN / ARBITRARY-DOMAIN INTEGRATION: AUTHORIZED",
    r"PHASE-7 INTEGRATION RESIDUALS: (?!REMAIN PHASE 7)", r"STAGE 15 CLOSURE: (?!DELIVERED)",
    r"(?<!no )(?<!not )\bvalidated (IRL|integration) (is |was |has been )?(established|achieved|claimed)",
    r"Stage 15 (is |was )?complete for (all|every|any|arbitrary)",
    r"STAGE 18 COMPLETE: YES", r"STAGE 18: (?:ENTERED / (?:PARTIAL / )?)?COMPLETE`",
    # Stage 18 closure: complete ONLY for the current Mechanical + Electrical / Electronics scope; Stage 19 is the
    # marker for navigation only — its completion, an authorized Stage-19 implementation or an activated MSNL
    # stays a reversal.
    r"Stage 18\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b"
    r"(?!\s+for\s+the\s+current\s+Mechanical)",
    r"STAGE 19 COMPLETE: YES", r"STAGE 19: (?:ENTERED / )?COMPLETE`",
    # Stage 19 closure: complete ONLY for the current planning-only scope; Stage 20 is the marker for navigation
    # only — its completion or an authorized Stage-20 implementation stays a reversal, as do full CAP-09 /
    # WS-PFV-001, a result outcome and any validated-result, prototype-validation or feasibility claim.
    r"Stage 19\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED)\b"
    r"(?!\s+for\s+the\s+current\s+planning-only)",
    r"Stage 19 (is |was )?complete for (all|every|any|arbitrary)",
    r"(?<!NO )STAGE-19 IMPLEMENTATION (IS )?AUTHORIZED",
    r"STAGE 20 COMPLETE: YES", r"STAGE 20: (?:ENTERED / (?:PARTIAL / )?)?COMPLETE`",
    # Stage 20 closure: complete ONLY for the current Owner-declared assumption scope; Stage 21 is the marker for
    # navigation only — its completion or an authorized Stage-21 implementation stays a reversal, as do full CAP-08
    # / CAP-10 and any automatically resolved, validated or confirmed assumption.
    r"Stage 20\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED)\b"
    r"(?!\s+for\s+the\s+current\s+Owner-declared)",
    r"Stage 20 (is |was )?complete for (all|every|any|arbitrary)",
    r"(?<!NO )STAGE-20 IMPLEMENTATION (IS )?AUTHORIZED", r"STAGE 19 CLOSURE: (?!DELIVERED)",
    r"STAGE 21 COMPLETE: YES", r"STAGE 21: (?:ENTERED / (?:PARTIAL / )?)?COMPLETE`",
    # Stage 21 closure: complete ONLY for the current Owner-declared contradiction scope; Stage 22 is the marker
    # for navigation only — its completion, an authorized Stage-22 implementation, automatic / AI contradiction
    # detection or a SYSTEM_INFERRED contradiction writer stays a reversal.
    r"Stage 21\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED)\b"
    r"(?!\s+for\s+the\s+current\s+Owner-declared\s+contradiction)",
    r"Stage 21 (is |was )?complete for (all|every|any|arbitrary)",
    r"(?<!NO )STAGE-21 IMPLEMENTATION (IS )?AUTHORIZED", r"STAGE 20 CLOSURE: (?!DELIVERED)",
    r"STAGE 22 COMPLETE: YES", r"STAGE 22: (?:ENTERED / (?:PARTIAL / )?)?COMPLETE`",
    # Stage 22 closure: complete ONLY for the current bounded decision trace + decision room scope, with no product
    # change; Stage 23 is the marker for navigation only and NOT ENTERED — its entry or completion, an authorized
    # Stage-23 implementation, an activated CAP-06 or full CAP-05 / CAP-07 stays a reversal.
    r"Stage 22\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED)\b"
    r"(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?for\s+the\s+current\s+bounded\s+decision\s+trace)",
    r"Stage 22 (is |was )?complete for (all|every|any|arbitrary)",
    r"(?<!NO )STAGE-22 IMPLEMENTATION (IS )?AUTHORIZED", r"STAGE 21 CLOSURE: (?!DELIVERED)",
    # Stage 23 closure: complete ONLY for the current bounded four-axis Readiness Snapshot scope, with no product
    # change; Stage 24 is the marker for navigation only and NOT ENTERED — its entry or completion, an authorized
    # Stage-24 implementation, full CAP-06 or a claimed eight-axis CAP-06 stays a reversal.
    r"STAGE 23 COMPLETE: YES",
    r"STAGE 23: (?:ENTERED|COMPLETE(?! — CURRENT BOUNDED FOUR-AXIS READINESS-SNAPSHOT SCOPE ONLY))",
    r"Stage 23\s+(is|was|has been)\s+(now\s+)?ENTERED\b",
    r"Stage 23\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED)\b"
    r"(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?for\s+the\s+current\s+bounded\s+four-axis)",
    r"Stage 23 (is |was )?complete for (all|every|any|arbitrary)",
    r"(?<!NO )STAGE-23 IMPLEMENTATION (IS )?AUTHORIZED", r"STAGE 22 CLOSURE: (?!DELIVERED — NO PRODUCT CHANGE REQUIRED)",
    # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 is ENTERED / PARTIAL for that slice ONLY;
    # an unscoped entry, any completion or closure, or an authorized further Stage-24 implementation stays a reversal.
    r"STAGE 24 COMPLETE: YES",
    # AMENDED at the Stage 24 closure: the SCOPED completion is true; an unscoped completion, any Stage-25 entry or
    # completion, an authorized Stage-25 implementation or an authorized further CAP-12 slice stays a reversal.
    r"STAGE 24: (?:COMPLETE(?! — CURRENT BOUNDED CAP-12 FORM MOCK-UP ADVISORY SLICE 1 SCOPE ONLY)"
    r"|ENTERED(?! / PARTIAL — CAP-12 FORM MOCK-UP ADVISORY SLICE 1 ONLY))",
    r"Stage 24\s+(is|was|has been)\s+(now\s+)?ENTERED\b(?!\s*/\s*PARTIAL)",
    r"Stage 24\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED)\b"
    r"(?!\s+(?:\(\d{4}-\d{2}-\d{2}\)\s+)?for\s+(?:the|its)\s+current\s+bounded\s+CAP-12)",
    r"Stage 24 (is |was )?complete for (all|every|any|arbitrary)",
    r"(?<!NO )STAGE-24 IMPLEMENTATION (IS )?AUTHORIZED", r"STAGE 23 CLOSURE: (?!DELIVERED — NO PRODUCT CHANGE REQUIRED)",
    # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 is ENTERED / PARTIAL
    # for that slice ONLY; an unscoped entry, any completion or closure, or full CAP-13 stays a reversal.
    r"STAGE 25 COMPLETE: YES",
    r"STAGE 25: (?:COMPLETE|COMPLETED|ENTERED(?! / PARTIAL — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1 ONLY))",
    r"Stage 25\s+(is|was|has been)\s+(now\s+)?ENTERED\b(?!\s*/\s*PARTIAL)",
    r"Stage 25\s+(is|was|has been)\s+(now\s+)?(COMPLETE|COMPLETED|CLOSED)\b", r"FULL CAP-13: AUTHORIZED",
    r"(?<!NO )STAGE-25 IMPLEMENTATION (IS )?AUTHORIZED", r"STAGE 24 CLOSURE: (?!DELIVERED — NO PRODUCT CHANGE REQUIRED)",
    r"FULL CAP-12: AUTHORIZED", r"FURTHER CAP-12 SLICES: AUTHORIZED", r"`CAP-13: (?!NOT ACTIVATED`)",
    r"FULL CAP-06: AUTHORIZED", r"FULL EIGHT-AXIS CAP-06: (?!NOT IMPLEMENTED / NOT CLOSED)",
    r"`CAP-12: (?!NOT AUTHORIZED`)",
    r"FULL (CAP-05|CAP-07): AUTHORIZED", r"`CAP-06: (?!NOT ACTIVATED`)",
    r"(AUTOMATIC / AI CONTRADICTION DETECTION|SYSTEM_INFERRED CONTRADICTION WRITER): AUTHORIZED",
    r"FULL (CAP-08|CAP-10): AUTHORIZED",
    r"(?<!no )(?<!not )\bassumptions? (is |are |was |were |has been |have been )(automatically )?"
    r"(resolved|validated|confirmed)\b",
    r"FULL (CAP-09|WS-PFV-001): AUTHORIZED", r"RESULT OUTCOME / PASS-FAIL JUDGEMENT: AUTHORIZED",
    r"(?<!no )(?<!not )\b(prototype|experiment) (is |was |has been )(validated|proven)\b",
    r"(?<!no )(?<!not )\bfeasibility (is |was |has been )(established|proven|confirmed)\b", r"`MSNL: (?!FUTURE / DEFERRED / NOT ACTIVATED`)",
    r"(?<!no )(?<!not )\bMSNL (is |was )?(now )?(activated|implemented)\b",
    r"FULL STAGE 15 / IRL: AUTHORIZED",
    r"(?<!no )(?<!not )full IRL (capability )?(is |was )?(authorized|complete|delivered|established)",
    r"IRL SCORING / LEVELS: AUTHORIZED", r"(?<!no )(?<!not )\bIRL level \d",
    r"\bIRL level (exists|is assigned|is achieved|was achieved)",
    r"(?<!no )(?<!not )(integrated )?engineering compatibility (is |was |has been )?(established|confirmed|proven|verified)",
    r"(?<!no )(?<!not )integrated[- ](engineering )?validation (exists|is established|was performed|is complete)",
    r"both (domains|parts) (were|have been|are) (independently )?(evaluated|validated)",
    r"(other|non-focused) (part|domain)[^.;]{0,40}\b(has|have) been (independently )?(evaluated|validated)",
    r"MECHATRONICS DOMAIN PACK: AUTHORIZED",
    r"(?<!no )(?<!not )(?<!a )Mechatronics Domain Pack (is |was )?(authorized|exists|created)",
    r"ROBOTICS[^`]{0,60}: AUTHORIZED", r"(?<!not )(?<!no )Robotics implementation (is )?authorized",
    r"ANOTHER STAGE-15 SLICE: AUTHORIZED",
    r"(?<!no )(?<!not )(another|next|further|second) Stage-15 slice (is )?(authorized|approved)",
    r"NEXT PRODUCT INCREMENT: (?!NOT AUTHORIZED)", r"DEPLOYMENT / RELEASE: AUTHORIZED",
    r"(?<!not )(?<!no )\b(deployment|release) (is )?authorized\b",
    r"roadmap is complete\b(?<!NOT mean the roadmap is complete)", r"ROADMAP COMPLETE",
    r"MECHATRONICS INTEGRATION: NOT AUTHORIZED", r"CURRENT MASTER ROADMAP STAGE: Stage 15")
_S15_LIVE_FORBIDDEN = _S15_PREMERGE_FORMS + _S15_CLOSE_REVERSALS


def test_post_716_no_active_contract_is_superseded_history():
    """The post-PR-#716 `ACTIVE CONTRACT: NONE` was true until the Owner authorized Stage 15
    Slice 1 after the Lead-controlled Next-Increment Reassessment. It survives ONLY as visibly
    superseded history — never as a live contract, a live plain-text line, the live
    current-position entry or the CLAUDE.md head — and its Stage-18 / Electrical / Mechanical
    delivery facts stay true."""
    contract = _read(CONTRACT)
    none = re.sub(r"\s+", " ", _section(contract, "current-authority--post-pr-716-no-active-contract"))
    _needs(none, CONTRACT, "post-716 none superseded",
           r"## Current authority — post-PR-#716: no active contract \(2026-09-29\) — SUPERSEDED "
           r"\(2026-09-29\) by Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1",
           r"\*\*No longer the current authority\.\*\*",
           r"\*\(Superseded 2026-09-29, preserved so the change is visible rather than silent: this opened "
           r"\"\*\*ACTIVE CONTRACT: NONE\.\*\* Electrical / Electronics Technical Deepening Slice 1",
           r"That was true until the Owner authorized Stage 15 Slice 1",
           r"\*\*STAGE 18\*\* \| `STARTED: YES` · `COMPLETE: NO` · \*\*ENTERED / PARTIAL / NOT COMPLETE\*\*",
           re.escape(_EL_DELIVERED), re.escape(_TD1_DELIVERED),
           r"O-4 pre-merge current-truth lag — CLOSED / RESOLVED by this post-merge closure")
    live_none = re.sub(r"\*\(Superseded.*?\)\*", "", none)
    _rejects(live_none, CONTRACT, "post-716 none superseded", r"\*\*ACTIVE CONTRACT: NONE",
             r"`ACTIVE CONTRACT: NONE`", r"`NO CURRENT AUTHORIZED TECHNICAL DEEPENING SUBTASK`")
    # every routing surface preserves the old routing as a visible note right after its fence
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        after = _after_fence(path, "current-routing")
        assert ("*(Superseded 2026-09-29 by Stage 15 — Integrated Invention Entry & Durable Subsystem "
                "Composition — Slice 1, preserved so the change is visible rather than silent: the current "
                "routing read \"**NO ACTIVE CONTRACT — post-PR-#716 (2026-09-29)") in after, path
    after = _after_fence(STATE, "current-position")
    assert ("*(Superseded 2026-09-29 by Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — "
            "Slice 1, preserved so the change is visible rather than silent: the current-position entry read "
            "\"`ACTIVE CONTRACT: NONE` — no product increment is currently authorized (post-PR-#716 …)\"") in after
    flat_checklist = _flat(CHECKLIST)
    assert ("*(Superseded 2026-09-29 by Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — "
            "Slice 1, preserved — was: \"**CURRENT SUBTASK:** NONE (post-PR-#716)") in flat_checklist
    assert "**CURRENT SUBTASK:** NONE (post-PR-#716)" not in re.sub(r"\*\(Superseded.*?\)\*", "", flat_checklist)
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    assert "the former post-PR-#716 `ACTIVE CONTRACT: NONE`" in claude
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    # the live NONE in the head is the post-#718 one; the post-#716 wording never returns
    for stale in ("The last Owner-authorized bounded slice — Electrical / Electronics Technical Deepening Slice 1",
                  "may evaluate an Electrical ↔ Mechanical / Mechatronics integration slice"):
        assert stale not in head, stale


def test_stage15_slice1_is_delivered_history_and_its_rules_still_bind():
    """Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1 is DELIVERED
    (PR #718, merge 3f3546a; post-merge identity / content verification PASS) with every reviewed rule
    still recorded: ONE project → ONE scalar root `confirmed_domain` (the immutable initial analysis
    focus) → subsystems, the unchanged classifier, the durable OWNER_STATED / UNVALIDATED composition,
    the truthful scope disclosure, F1 CLOSED and S15-N1 / S15-N2 non-blocking. Its pre-merge contract
    (ACTIVE CONTRACT: STAGE 15 …, PR NOT OPENED, merge NOT PERFORMED) survives ONLY as visibly
    superseded history."""
    contract = _read(CONTRACT)
    top = re.sub(r"\s+", " ", _section(contract, "current-authority--stage15-integrated-invention-entry-slice1"))
    _needs(top, CONTRACT, "stage15 delivered",
           r"## Current authority — Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice "
           r"1 \(Owner authorization, 2026-09-29\) — DELIVERED \(PR #718\); SUPERSEDED as current authority by the "
           r"post-PR-#718 no-active-contract declaration",
           r"\*\*No longer the current authority\.\*\* Stage 15 — Integrated Invention Entry & Durable Subsystem "
           r"Composition — Slice 1 was delivered \(PR #718, merge `" + _S15_MERGE + r"`; post-merge identity / "
           r"content verification PASS\)",
           r"Every rule below still binds, and Stage 15 stays ENTERED / PARTIAL / NOT COMPLETE\.",
           r"\*\(Superseded 2026-09-29, preserved so the change is visible rather than silent: this opened "
           r"\"\*\*ACTIVE CONTRACT: STAGE 15 — INTEGRATED INVENTION ENTRY & DURABLE SUBSYSTEM COMPOSITION — SLICE "
           r"1\.\*\*\" and recorded the slice as \"IMPLEMENTATION: COMPLETE CANDIDATE … F1-CLOSED / PR NOT OPENED / "
           r"merge NOT PERFORMED\"\.\)\*",
           r"selected by the Owner-controlled Next-Increment Reassessment",
           r"Stage 15 is ENTERED / PARTIAL / NOT COMPLETE through exactly this slice \(checkbox unticked\)",
           r"The MASTER ROADMAP SEQUENTIAL MARKER stays `CURRENT MASTER ROADMAP STAGE: Stage 18 — D13 / "
           r"CAP-01` \(Stage 18 ENTERED / PARTIAL / NOT COMPLETE, checkbox unticked\)",
           r"does not complete, cancel or renumber Stage 18",
           r"OWNER AUTHORIZED: YES / IMPLEMENTED — original implementation commit `" + _S15_IMPL + r"` \(tree `"
           + _S15_IMPL_TREE + r"`; sole parent `" + _S15_BASE + r"`\)",
           r"F1 / IR01-A correction commit `" + _S15_HEAD + r"` \(sole parent `" + _S15_IMPL + r"`\)",
           r"FINAL REVIEWED PRODUCT HEAD `" + _S15_HEAD + r"` \(tree `" + _S15_TREE + r"`\)",
           r"INDEPENDENT ARCHITECTURE \+ IMPLEMENTATION REVIEW CYCLE COMPLETE — F1-CLOSED; product-attached "
           r"current-truth sync / PR head `" + _S15_SYNC + r"` \(tree `" + _S15_MTREE + r"`; sole parent `"
           + _S15_HEAD + r"`\) / DELIVERED \(PR #718, merge `" + _S15_MERGE + r"`; ordered parents `" + _S15_BASE
           + r"`, `" + _S15_SYNC + r"`; merge tree = PR-head tree\) / deployment and release NOT AUTHORIZED",
           r"ONE PROJECT → ONE scalar root `confirmed_domain` → ZERO OR MORE SUBSYSTEMS; MULTI-DOMAIN AT "
           r"SUBSYSTEM GRAIN; NO peer root `domains = \[\.\.\.\]`",
           r"`confirmed_domain` is the IMMUTABLE INITIAL ANALYSIS FOCUS \(`mechanical` or "
           r"`electronics_electrical`\) — NOT a claim that the whole invention belongs to that domain",
           r"AMBIGUOUS_TIE ≠ GENUINE MULTI-DOMAIN; `MULTI_DOMAIN_NEEDS_D4` is NOT manufactured",
           r"the composition is OWNER_STATED / UNVALIDATED and distinct from classification",
           r"ONE additive `project_subsystems` sidecar in the existing SQLite store; no backfill; no "
           r"destructive migration; old projects keep zero subsystem rows; `ProjectRecordContract` unchanged; "
           r"subsystem declarations are NOT AssertionRecords",
           r"the other part and the integration between the parts have NOT yet been independently evaluated "
           r"or validated; no automatic \"Mechatronics\" label",
           r"C\. FAIL — one material finding, F1 / P2 / IR01-A",
           r"B\. TARGETED PASS WITH NON-BLOCKING OBSERVATIONS — F1 CLOSED; IR01-B — CORRECTED / NO REMAINING "
           r"MATERIAL DEFECT",
           r"NO REMAINING MATERIAL FINDING; the ONE required independent architecture \+ implementation review "
           r"cycle is COMPLETE; no second architecture review is required",
           r"author full regression 8790 passed / 2 skipped / 1 xfailed / 0 failed / 0 errors",
           r"The independent full regression was ENVIRONMENT-LIMITED on Windows",
           r"the independent reviewer did NOT complete a clean full regression",
           r"hosted CI on the PR was the mandatory final full-suite merge gate — on PR #718 \(run 36597956066, "
           r"head `" + _S15_SYNC + r"`\) CI required, Verify candidate and RIG fast feedback all passed before the "
           r"merge",
           r"S15-N1 — stale `IdeaState\.subsystems` commentary",
           r"S15-N2 — the self-service structured export omits the subsystem composition — EXPORT-A — "
           r"ACCEPTABLE NON-BLOCKING OMISSION",
           r"subsystem names and functions are PRIVATE INVENTOR / PROJECT INFORMATION",
           r"\*\*Deferred / not authorized:\*\* another Stage-15 slice; full Stage-15 / IRL completion; IRL "
           r"scoring / levels; full D4 compatibility evaluation",
           r"Mechatronics remains a cross-domain integration perspective first, NOT automatically a Domain Pack",
           r"a Robotics capability assessment precedes any decision among reuse, composition, extension, a "
           r"bounded reasoning layer, a genuine separate domain or deferral",
           r"\*\(Superseded 2026-09-29, preserved — this token line began \"" + re.escape(_S15_CONTRACT),
           re.escape(_S15_DELIVERED), re.escape(_S15_PM), re.escape(_S15_REVIEW), re.escape(_S15_ANC),
           re.escape(_S15_ENTERED), re.escape(_S15_MARKER), *(re.escape(t) for t in _S15_NOT))
    live_top = re.sub(r"\*\(Superseded.*?\)\*", "", top)
    _rejects(live_top, CONTRACT, "stage15 delivered", *_S15_LIVE_FORBIDDEN)
    # every routing surface / the state file preserve the pre-merge routing as a visible note after the fence
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        after = _after_fence(path, "current-routing")
        assert ("*(Superseded 2026-09-29 by the post-PR-#718 closure, preserved so the change is visible rather "
                "than silent: the current routing read \"**CURRENT BOUNDED PRODUCT ACTION — Stage 15 / Integrated "
                "Invention Entry & Durable Subsystem Composition — Slice 1 (…):** `ACTIVE CONTRACT: STAGE 15 —") in after, path
        assert "That was true until PR #718 merged (merge `" + _S15_MERGE + "`).)*" in after, path
    after = _after_fence(STATE, "current-position")
    assert ("*(Superseded 2026-09-29 by the post-PR-#718 closure, preserved so the change is visible rather than "
            "silent: the current-position entry read \"" + _S15_CONTRACT + " — current bounded product action:") in after
    flat_checklist = _flat(CHECKLIST)
    assert ("*(Superseded 2026-09-29 by the post-PR-#718 closure, preserved — was: \"**CURRENT SUBTASK:** STAGE 15 "
            "— INTEGRATED INVENTION ENTRY & DURABLE SUBSYSTEM COMPOSITION — SLICE 1 (current bounded product "
            "action; …)") in flat_checklist
    raw_checklist = _read(CHECKLIST)
    for stale in (_S15_CONTRACT, _S15_STATUS, _S15_HEAD_TOK):
        assert re.search(r"^" + re.escape(stale.strip("`")) + r"$", raw_checklist, re.M) is None, stale
    # CLAUDE.md: the pre-merge contract is a named superseded declaration; the continuity rules still bind
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    assert ("the former post-PR-#718 `ACTIVE CONTRACT: NONE`, the "
            "former Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1 (pre-merge, "
            "\"PR NOT OPENED / merge NOT PERFORMED\"), the former post-PR-#716 `ACTIVE CONTRACT: NONE`,") in claude
    cont = claude[claude.index("## Lead execution continuity"):claude.index("### Lead Operating Method")]
    for needle in ("NO TECHNICAL DEPTH WITHOUT SOURCE AUTHORITY.", "UNKNOWN RIGHTS = DO NOT INGEST BY DEFAULT.",
                   "AI ANSWER ≠ SOURCE LICENSE.", "THE USER SUBMITS AN INVENTION, NOT A DOMAIN",
                   "NOT EVERY NAMED TECHNOLOGY REQUIRES A DOMAIN PACK",
                   "Robotics is NOT automatically a new Domain Pack", "no Robotics implementation is authorized now",
                   "a Robotics capability assessment precedes any Robotics decision",
                   "that reassessment selected Stage 15 — Integrated Invention Entry & Durable Subsystem "
                   "Composition — Slice 1, the FIRST real bounded Mechanical ↔ Electrical / Electronics "
                   "integrated-invention product slice, delivered in PR #718; it performs no full engineering "
                   "integration analysis",
                   "no Stage 15 implementation beyond the delivered bounded Integrated Invention Entry & Durable "
                   "Subsystem Composition Slice 1 (PR #718) and the Owner-authorized Subsystem Interface Declaration "
                   "& Verification Preparation Slice 2 (delivered, PR #720), Interface Verification Preparation "
                   "Metadata Slice 3 (delivered), Interface Verification Observation Event Slice 4 (delivered) and "
                   "the Integration Evidence & IRL-Compatible View Closure (delivered; Stage 15 COMPLETE for the "
                   "current Mechanical + Electrical / Electronics scope) is authorized now",
                   "is not a Mechatronics domain and applies no Mechatronics label",
                   "**WATCH — Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1 "
                   "(non-blocking, no repair cycle).**",
                   "(S15-N1) STALE `IdeaState.subsystems` COMMENTARY",
                   "(S15-N2) EXPORT OMITS THE COMPOSITION: EXPORT-A — ACCEPTABLE NON-BLOCKING OMISSION",
                   "The independent FULL regression was ENVIRONMENT-LIMITED on Windows",
                   "the slice is DELIVERED (PR #718, merge `" + _S15_MERGE[:7] + "`)",
                   "(O-3) carried invention text / reclassification — NO MATERIAL FINDING",
                   "(O-4) integrated-entry / clarification UX — NO MATERIAL FINDING",
                   "S15-N1 / S15-N2 are not fixed now; no repair cycle"):
        assert needle in cont, needle
    assert "hosted CI on the PR is the mandatory final full-suite merge gate" not in cont
    # the register records the delivered slice as NOT a CAP-01 slice
    register = _flat(CAPABILITIES)
    assert ("Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1 (DELIVERED — PR #718 "
            "— merge `" + _S15_MERGE + "`; post-merge identity / content verification PASS; independent "
            "architecture + implementation review cycle COMPLETE — F1-CLOSED) is NOT a CAP-01 slice, and neither "
            "is Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2") in register
    for pat in _S15_PREMERGE_FORMS:
        assert re.search(pat, register) is None, pat
    assert re.search(r"CAP-01[^|]{0,200}\| *RECORDED — AUTHORIZED", register) is None


def test_post_718_no_active_contract_is_superseded_history():
    """The post-PR-#718 `ACTIVE CONTRACT: NONE` was true until the Owner authorized Stage 15 Slice 2
    after the Lead-controlled Next-Increment Reassessment. It survives ONLY as visibly superseded
    history — never as a live contract, a live token line, the live current-position entry, the live
    checklist subtask or the CLAUDE.md head — and its Stage 15 Slice 1 delivery facts stay true."""
    contract = _read(CONTRACT)
    none = re.sub(r"\s+", " ", _section(contract, "current-authority--post-pr-718-no-active-contract"))
    _needs(none, CONTRACT, "post-718 none superseded",
           r"## Current authority — post-PR-#718: no active contract \(2026-09-29\) — SUPERSEDED \(2026-09-29\) "
           r"by Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2",
           r"\*\*No longer the current authority\.\*\*",
           r"\*\(Superseded 2026-09-29, preserved so the change is visible rather than silent: this opened "
           r"\"\*\*ACTIVE CONTRACT: NONE\.\*\* NO PRODUCT INCREMENT IS CURRENTLY AUTHORIZED\.",
           r"That was true until the Owner authorized Stage 15 Slice 2\.",
           r"\*\*ANCESTRY\*\* \| original implementation `" + _S15_IMPL + r"` → F1 / IR01-A correction `"
           + _S15_HEAD + r"` → product-attached current-truth sync / PR head `" + _S15_SYNC + r"` → merge `"
           + _S15_MERGE + r"`",
           r"\*\*STAGE 15\*\* \| \*\*ENTERED / PARTIAL / NOT COMPLETE\*\*",
           re.escape(_S15_DELIVERED), re.escape(_S15_PM), re.escape(_S15_ANC))
    live_none = re.sub(r"\*\(Superseded.*?\)\*", "", none)
    _rejects(live_none, CONTRACT, "post-718 none superseded", r"\*\*ACTIVE CONTRACT: NONE",
             r"`ACTIVE CONTRACT: NONE`", r"`NEXT PRODUCT INCREMENT: NOT AUTHORIZED`",
             r"`NEXT STEP: LEAD-CONTROLLED NEXT-INCREMENT REASSESSMENT`",
             r"`ANOTHER STAGE-15 SLICE: NOT AUTHORIZED`")
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        after = _after_fence(path, "current-routing")
        assert ("*(Superseded 2026-09-29 by Stage 15 — Subsystem Interface Declaration & Verification "
                "Preparation — Slice 2, preserved so the change is visible rather than silent: the current routing "
                "read \"**NO ACTIVE CONTRACT — post-PR-#718 (2026-09-29);") in after, path
    after = _after_fence(STATE, "current-position")
    assert ("*(Superseded 2026-09-29 by Stage 15 — Subsystem Interface Declaration & Verification Preparation — "
            "Slice 2, preserved so the change is visible rather than silent: the current-position entry read "
            "\"`ACTIVE CONTRACT: NONE` — no product increment is currently authorized (post-PR-#718 …)\"") in after
    flat_checklist = _flat(CHECKLIST)
    assert ("*(Superseded 2026-09-29 by Stage 15 — Subsystem Interface Declaration & Verification Preparation — "
            "Slice 2, preserved — was: \"**CURRENT SUBTASK:** NONE (post-PR-#718)") in flat_checklist
    assert "**CURRENT SUBTASK:** NONE (post-PR-#718)" not in re.sub(r"\*\(Superseded.*?\)\*", "", flat_checklist)
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    assert "the former post-PR-#718 `ACTIVE CONTRACT: NONE`" in claude
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    # the live NONE is the one after the delivered Stage 24 Slice 1, never the post-PR-#718 one (ADVANCED at the
    # Stage 30, Stage 28 and Stage 23 closures, and again at the delivered CAP-12 Form Mock-up Advisory Slice 1: the
    # last bounded increment is now that slice, recorded in its after-merge form)
    # ADVANCED at the Stage 24 closure: the last bounded closure is now the Stage 24 closure
    # ROTATED at the Stage 35 first bounded slice: the head opened with the live Stage-35 declaration
    # ROTATED at the Stage 35 closure: the head opens with the live NONE again; the Stage 35 closure is the last bounded
    # closure and the Stage 24 closure precedes it
    # ADVANCED at the Stage 36 closure: the Stage 36 closure is the last bounded closure, the Stage 35 closure precedes it
    # ADVANCED at the Stage 16 closure: the Stage 16 closure is the last bounded closure; the delivered Stage 16 residual
    # and the Stage 36 closure precede it
    # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: that slice is the last bounded
    # increment, recorded in its after-merge form; the Stage 16 closure precedes it
    # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: that slice is the last
    # bounded increment, recorded in its after-merge form; the Stage 25 slice precedes it
    # ROTATED at the Stage 27 closure: the Stage 27 closure is the last bounded closure; the Stage 27 slice precedes it
    assert head.startswith("## Current authority " + _NONE_BOLD + " NO PRODUCT INCREMENT IS CURRENTLY AUTHORIZED. The "
                           "last Owner-authorized bounded closure — " + _S27C_NAME + " — is DELIVERED with no product "
                           "change required, completing Stage 27 for the current bounded THERM-01 single-path "
                           "temperature-difference scope ONLY (" + "; ".join((_S27C_DELIVERED, _S27_COMPLETE, _S27_FULL_NO,
                                                                               _S25_MARKER))
                           + "; Git / GitHub own its PR, merge and review identity)")
    assert ("The preceding bounded increment — " + _S27_NAME + " — is DELIVERED (" + _S27_DELIVERED + "; Git / GitHub own "
            "its PR, merge and review identity): it entered Stage 27 as ENTERED / PARTIAL for that slice ONLY until the "
            "Stage 27 closure") in head
    assert ("The preceding bounded increment — " + _S25_NAME + " — is DELIVERED, entering Stage 25 as ENTERED / PARTIAL "
            "for that slice ONLY (" + "; ".join(_S25_FACTS) + "; Git / GitHub own its PR, merge and review identity)") in head
    assert ("The preceding bounded closure — " + _S16C_NAME + " — is DELIVERED with no further product change "
            "required") in head
    assert re.search(_any_pr("The preceding bounded increment — " + _S16_NAME + " — is DELIVERED (" + _S16_DELIVERED
                             + "; PR #N;"), head)
    assert ("The preceding bounded closure — " + _S36C_NAME + " — is DELIVERED with no product change required") in head
    assert ("The preceding bounded closure — " + _S35C_NAME + " — is DELIVERED with no product change required") in head
    assert ("The preceding bounded closure — Stage 24 — CAP-12 Form Mock-up Advisory — Closure — is "
            "DELIVERED with no product change required") in head
    assert _S35_BOLD not in head
    assert "post-PR-#718" not in head


_S2_BRANCH = "stage15/subsystem-interface-verification-01"
_S2_BASE = "a30b90ea2681b7affddbd6247ad29f0bde8912d8"
_S2_CONTRACT = ("`ACTIVE CONTRACT: STAGE 15 — SUBSYSTEM INTERFACE DECLARATION & VERIFICATION PREPARATION — "
                "SLICE 2`")
_S2_STATUS = ("`STAGE 15 SLICE 2: OWNER-AUTHORIZED — IMPLEMENTATION CANDIDATE — INDEPENDENT LEVEL-1 "
              "IMPLEMENTATION REVIEW PENDING (LEAD-ROUTED) — NOT MERGED`")
_S2_NOT = ("`ENGINEERING COMPATIBILITY ANALYSIS: NOT AUTHORIZED`",
           "`SUBSYSTEM-SPECIFIC GAP / EVIDENCE / READINESS ENGINES: NOT AUTHORIZED`",
           "`GENERIC RELATIONSHIP GRAPH / ENGINE: NOT AUTHORIZED`")
_S15_FIXED_NOT = _S15_NOT[1:]         # every Stage-15 exclusion except the post-#718 "another slice"
_S2_MERGE = "2418f7e583b3535d48970cf0989689bb2f8ef2ca"
_S2_HEAD = "fc3d47ed6184a54b0d2323910f6341e4bbf9b73f"
_S2_MTREE = "a4ffba8452d2945d4dabdaf14f3431695087ddb6"
_S2_DELIVERED = "`STAGE 15 SLICE 2: DELIVERED — PR #720 — merge " + _S2_MERGE + "`"
# Stage 15 Slice 3: delivered on its candidate (Priority-2 lifecycle) — identity optional, never required.
_S3_DELIVERED = "`STAGE 15 SLICE 3: DELIVERED`"
# CAP-09 Result Event Slice 1: delivered on its candidate (Priority-2 lifecycle) — identity optional.
_R1_DELIVERED = "`CAP-09 RESULT EVENT SLICE 1: DELIVERED`"
# Stage 15 Slice 4: delivered on its candidate (Priority-2 lifecycle) — identity optional.
_S4_DELIVERED = "`STAGE 15 SLICE 4: DELIVERED`"
# Stage 15 closure: delivered on its candidate (Priority-2 lifecycle) — identity optional.
_S15C_DELIVERED = "`STAGE 15 CLOSURE: DELIVERED`"
# After the closure a live surface may no longer carry the pre-closure Stage-15 status.
_S15C_STALE = (_tok(_S15_ENTERED), r"`FULL STAGE 15 / IRL: NOT AUTHORIZED`",
               r"Stage 15 and Stage 18 both stay ENTERED", r"Stage 15 stays ENTERED / PARTIAL / NOT COMPLETE",
               r"wider Stage-15 work (stays|remains) DEFERRED")
# Stage 15 Slice 4 records the inventor's own observation; a live surface may never read it as a verdict.
_S4_VERDICT = r"(?<!whether the )(?<!not )acceptance criterion (is|was|has been) (met|satisfied)"
_S2_REVIEW = "`STAGE 15 SLICE 2 FINAL INDEPENDENT REVIEW: PASS — F1 / F2 / F3 CLOSED`"
_S2_ANC = ("`STAGE 15 SLICE 2 ANCESTRY: implementation 470bb90004b17229206fdd17fe3eaf3dd7867939, render-reattachment "
           "test d2f16a16e0a7ac3f11b72c669970afad6dae0ff9, current-truth sync b61422b4f229668af792f2cbed2e5a770afae43b, "
           "F1 / F2 / F3 correction 7d965480ac721bd75d99e6a25b9c2549a1e85566, F3 residual correction / reviewed PR head "
           + _S2_HEAD + ", merge " + _S2_MERGE + "`")
# A live surface may never: present Slice 2 as a candidate / review pending / not merged or as the active
# contract, drop the post-#720 NONE, reopen Slice 1, mark Stage 15 / 18 complete or move the sequential
# marker, claim compatibility, verification or an IRL score / level, authorize deployment / release or
# (implicitly or explicitly) another Stage-15 slice.
_S2_CLOSE_REVERSALS = tuple(_S15_LIVE_FORBIDDEN) + (
    r"STAGE 15 SLICE 2: (?!DELIVERED)", r"ACTIVE CONTRACT: STAGE 15",
    r"Slice 2[^.;]{0,120}\bimplementation candidate\b", r"Slice-2 candidate",
    r"INDEPENDENT LEVEL-1 IMPLEMENTATION REVIEW PENDING", r"Slice 2[^.;]{0,160}\breview (is )?pending\b",
    r"Slice 2[^.;]{0,160}\bNOT MERGED\b", r"STAGE 15 SLICE 1: (?!DELIVERED)",
    r"ENGINEERING COMPATIBILITY ANALYSIS: AUTHORIZED",
    r"SUBSYSTEM-SPECIFIC GAP / EVIDENCE / READINESS ENGINES: AUTHORIZED",
    r"GENERIC RELATIONSHIP GRAPH / ENGINE: AUTHORIZED", r"\bIRL (score|scoring) (is |was )?(assigned|computed)",
    r"(?<!no )(?<!not )(the )?interaction (is|was|has been) (verified|validated|checked)\b",
    r"(?<!no )(?<!not )compatibility (is|was|has been) (established|verified|confirmed)\b",
    r"current bounded product action", r"CURRENT BOUNDED PRODUCT ACTION",
    # Stage 15 Slice 3 may never read as a candidate / pending / not merged / active contract on a live surface
    r"STAGE 15 SLICE 3: (?!DELIVERED)", r"Slice 3[^.;]{0,120}\bimplementation candidate\b",
    r"Slice 3[^.;]{0,160}\bNOT MERGED\b", r"Slice 3[^.;]{0,160}\breview (is )?pending\b",
    # CAP-09 Result Event Slice 1 may never read as pending / an active contract / an outcome writer
    r"CAP-09 RESULT EVENT SLICE 1: (?!DELIVERED)", r"ACTIVE CONTRACT: CAP-09",
    r"Result Event Slice 1[^.;]{0,160}\bNOT MERGED\b", r"`RESULT: NOT AUTHORIZED`",
    r"RESULT OUTCOME / PASS-FAIL JUDGEMENT: AUTHORIZED",
    # Stage 15 Slice 4 may never read as pending / an active contract / a verdict
    r"STAGE 15 SLICE 4: (?!DELIVERED)", r"Observation Event[^.;]{0,160}\bNOT MERGED\b",
    r"INTERFACE OBSERVATION VERDICT / CRITERION-MET JUDGEMENT: AUTHORIZED", _S4_VERDICT)


def _current_declaration(contract):
    """The ONE live `## Current authority` section, selected by the shared classifier below."""
    return _live_declaration(contract)[1]


def test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface():
    """CURRENT STATE, merge-invariant: Stage 23 — CAP-06 Four-Axis Readiness Snapshot — Closure is DELIVERED with NO
    PRODUCT CHANGE REQUIRED and STAGE 23 is COMPLETE for the current bounded four-axis Readiness Snapshot scope ONLY
    (checkbox ticked for that scope; the existing user-facing Readiness Snapshot is its whole basis); full CAP-06
    stays NOT AUTHORIZED and its eight-axis expansion is not implemented or closed; the MASTER ROADMAP SEQUENTIAL
    MARKER moves to Stage 24 (NOT ENTERED) for NAVIGATION ONLY. (Advanced at the Stage 23 closure; the Stage 22
    record follows.) Stage 22 — Decision Trace + Decision Room — Closure is DELIVERED with NO PRODUCT
    CHANGE REQUIRED and STAGE 22 is COMPLETE for the current bounded decision trace + decision room scope ONLY (checkbox
    ticked for that scope; the delivered basis is CAP-05 + CAP-07 Slices 1–2 only); the MASTER ROADMAP SEQUENTIAL
    MARKER moves to Stage 23 (NOT ENTERED) for NAVIGATION ONLY — the closure authorizes no Stage-23 implementation and
    activates no CAP-06 — and full CAP-05 / CAP-07, recommendation, winner selection, confidence / evidence-strength /
    readiness scoring and inferred decision linkage stay NOT AUTHORIZED. (Advanced from the Stage 21 closure guard at
    the Stage 22 closure; its own record follows.) Stage 21 — Owner-Declared Contradiction Visibility — Closure is DELIVERED and
    STAGE 21 is COMPLETE for the current Owner-declared contradiction scope ONLY (checkbox ticked for that scope); the
    MASTER ROADMAP SEQUENTIAL MARKER moves to Stage 22 for NAVIGATION ONLY — the closure authorizes no Stage-22
    implementation — and full CAP-10, automatic / AI contradiction detection and a SYSTEM_INFERRED contradiction
    writer stay NOT AUTHORIZED. (Advanced from the Stage 20 closure guard at the Stage 21 closure; its own record
    follows.) Stage 20 — Assumption Revision & Replacement — Closure is DELIVERED (after
    the Stage 19 closure, the Stage 18 closure, the Stage 15 closure, Stage 15 Slices 1-4 and CAP-09 Result Event
    Slice 1, still delivered), no product increment is authorized (`ACTIVE CONTRACT: NONE`) and STAGE 20 is COMPLETE
    for the current Owner-declared assumption scope ONLY (checkbox ticked for that scope). The MASTER ROADMAP
    SEQUENTIAL MARKER moves to Stage 21 for NAVIGATION ONLY — the closure authorizes no Stage-21 implementation —
    full CAP-08 / CAP-10 stay NOT AUTHORIZED; Stage 19 stays COMPLETE for the current planning-only scope only, full
    CAP-09 / WS-PFV-001, a result outcome and a formal variable model stay NOT AUTHORIZED; Stage 18 and Stage 15 stay
    COMPLETE for the current Mechanical + Electrical / Electronics scope only (their delivered facts still bind),
    MSNL stays FUTURE / DEFERRED / NOT ACTIVATED, full CAP-01 stays NOT AUTHORIZED, and no automatically resolved or
    validated assumption, validated result, prototype validation, feasibility, validated IRL, IRL score / level,
    compatibility, N-domain integration, deployment, release or further slice is claimed or authorized. (Advanced
    from the Stage 19 closure guard at the Stage 20 closure.) ROTATED at the Stage 35 first bounded slice: the live
    contract is no longer NONE but the Owner-authorized Stage 35 first bounded structured invention disclosure export
    slice — ENTERED / PARTIAL for that slice only, not delivered, not complete, not closed, its merge and closure not
    authorized, its checkbox unticked (23 of 45 rows unticked) — and the post-Stage-24-closure NONE survives only as
    superseded history. ADVANCED at the Stage 35 closure: Stage 35 is COMPLETE for the current bounded first-slice
    scope only (row 35 ticked for that scope only; 22 of 45 rows unticked) with no product change, the live contract
    is NONE again, the first bounded slice stays DELIVERED, later Stage-35 slices stay NOT AUTHORIZED, the
    legal-adviser / release triggers stay preserved and Stage 36 stays NOT ENTERED / NOT AUTHORIZED; the Stage-35
    active-increment wording survives only as superseded history. ADVANCED at the Stage 36 closure: Stage 36 is COMPLETE
    for the current no-live-AI / provider scope only (row 36 ticked for that scope only; 21 of 45 rows unticked) with no
    product change, the live contract stays NONE, CAP-15 / CAP-17 stay not authorized for implementation, the External
    Engineering Tools direction stays planned / deferred, a future live AI / provider selection or tools activation needs
    a fresh Stage-36 reassessment and Stage 37 stays NOT ENTERED / NOT AUTHORIZED; the Stage 35 closure's Stage-36
    NOT-ENTERED wording survives only as history. This guard requires no PR number, SHA, ancestry,
    review verdict or
    post-merge result: Git/GitHub own them, so the same text is correct on the candidate that carries it and after
    its merge."""
    assert _live_authority_problems() == []
    contract = _read(CONTRACT)
    heading = _live_declaration(contract)[0]
    # ROTATED at the Stage 35 first bounded slice: the live section was the Stage-35 declaration
    # ROTATED at the Stage 35 closure: the live section is the post-Stage-35-closure NONE declaration; the closure record
    # and the Stage 35 slice section (with its pre-merge note) follow it as preserved history
    # ROTATED at the Stage 36 closure: the live section is the post-Stage-36-closure NONE declaration
    # ROTATED at the Stage 16 closure: the live section was the post-Stage-16-closure NONE declaration
    # ROTATED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: the live section is the
    # post-Stage-25-CAP-13-Slice-1 NONE declaration; the post-Stage-16-closure NONE and the slice record follow as history
    # ROTATED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: the live section is the
    # post-Stage-27-THERM-01-Slice-1 NONE declaration; the post-Stage-25-CAP-13-Slice-1 NONE and the slice record follow
    # ROTATED at the Stage 27 closure: the live section is the post-Stage-27-closure NONE declaration; the closure record,
    # the post-Stage-27-THERM-01-Slice-1 NONE and the slice record follow as history
    assert heading == _S27_HEADING, heading
    assert (_S27_SLICE_HEADING + " — SUPERSEDED (2026-10-09) by " + _S27C_NAME) in contract
    assert ("## Current authority — " + _S27C_NAME + " (Owner authorization, 2026-10-09) — DELIVERED; SUPERSEDED as "
            "current authority by the post-Stage-27-closure no-active-contract declaration") in contract
    assert (_S25_HEADING + " — SUPERSEDED (2026-10-09) by " + _S27_NAME) in contract
    assert ("## Current authority — " + _S27_NAME + " (Owner authorization, 2026-10-09) — DELIVERED; SUPERSEDED as "
            "current authority by the post-Stage-27-THERM-01-Slice-1 no-active-contract declaration") in contract
    assert (_S16C_HEADING + " — SUPERSEDED (2026-10-08) by " + _S25_NAME) in contract
    assert ("## Current authority — " + _S25_NAME + " (Owner authorization, 2026-10-08) — DELIVERED; SUPERSEDED as "
            "current authority by the post-Stage-25-CAP-13-Slice-1 no-active-contract declaration") in contract
    assert "SUPERSEDED" not in heading and "DELIVERED" not in heading, heading
    top = _live_only(_current_declaration(contract))
    assert re.findall(_ACTIVE_BOLD, top) == ["NONE"], re.findall(_ACTIVE_BOLD, top)
    assert "*(Superseded" not in _current_declaration(contract)
    assert ("## Current authority — " + _S35C_NAME + " (Owner authorization, 2026-10-05) — DELIVERED; SUPERSEDED as "
            "current authority by the post-Stage-35-closure no-active-contract declaration") in contract
    assert (_S35_HEADING + " — DELIVERED; SUPERSEDED as current authority by the post-Stage-35-closure "
            "no-active-contract declaration") in contract
    assert ("*(Superseded 2026-10-05 by the delivery of the Stage 35 first bounded slice, preserved so the change is "
            "visible rather than silent: before it this section read \"… the first bounded implementation EXISTS") in contract
    # ADVANCED at the Stage 36 closure: its closure record and the superseded post-Stage-35-closure NONE lead history
    assert ("## Current authority — " + _S36C_NAME + " (Owner authorization, 2026-10-05) — DELIVERED; SUPERSEDED as "
            "current authority by the post-Stage-36-closure no-active-contract declaration") in contract
    assert (_S35C_HEADING + " — SUPERSEDED (2026-10-05) by " + _S36C_NAME) in contract
    # ADVANCED at the Stage 16 closure: its closure record and the superseded post-Stage-36-closure NONE lead history; the
    # delivered Stage 16 residual carried no contract section of its own (a Lead-accepted governance deviation)
    assert ("## Current authority — " + _S16C_NAME + " (Owner authorization, 2026-10-06) — DELIVERED; SUPERSEDED as "
            "current authority by the post-Stage-16-closure no-active-contract declaration") in contract
    assert (_S36C_HEADING + " — SUPERSEDED (2026-10-06) by " + _S16C_NAME) in contract
    order = [contract.index('<a id="current-authority--' + anchor + '"></a>') for anchor in (
        "post-stage27-closure-no-active-contract", "stage27-therm01-closure",
        "post-stage27-therm01-slice1-no-active-contract", "stage27-therm01-single-path-temperature-difference-slice1",
        "post-stage25-cap13-slice1-no-active-contract", "stage25-cap13-two-support-static-reactions-slice1",
        "post-stage16-closure-no-active-contract", "stage16-srl-composition-closure",
        "post-stage36-closure-no-active-contract", "stage36-cap15-cap17-closure",
        "post-stage35-closure-no-active-contract", "stage35-disclosure-export-closure",
        "stage35-disclosure-export-first-slice", "post-stage24-closure-no-active-contract")]
    assert order == sorted(order), order
    _needs(top, CONTRACT, "live none",
           r"\*\*ACTIVE CONTRACT: NONE\.\*\* NO PRODUCT INCREMENT IS CURRENTLY AUTHORIZED\.",
           # ADVANCED at the Stage 35 closure: the Stage 35 closure is the last bounded closure, the delivered first
           # bounded slice the preceding increment and the Stage 24 closure the preceding closure
           # ADVANCED at the Stage 36 closure: the Stage 36 closure is the last bounded closure, Stage 35's precedes it
           # ADVANCED at the Stage 16 closure: the Stage 16 closure is the last bounded closure; the delivered Stage 16
           # residual and the Stage 36 closure precede it
           # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: that slice is the last
           # bounded increment and the Stage 16 closure the preceding closure
           # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: that slice is the
           # last bounded increment and the Stage 25 slice the preceding one
           # ROTATED at the Stage 27 closure: the Stage 27 closure is the last bounded closure, the slice precedes it
           re.escape(_S27C_NAME) + r", the last Owner-authorized\s+bounded closure, is DELIVERED with no product change "
           r"required \(Git / GitHub own its PR, merge and review identity\): the Stage-27 row requirement",
           re.escape(_S27_NAME) + r", the preceding Owner-authorized\s+bounded increment, is DELIVERED \(Git / GitHub own "
           r"its PR, merge and review identity\): it entered Stage 27 as ENTERED / PARTIAL for\s+that slice ONLY until the "
           r"Stage 27 closure",
           r"\*\*STAGE 27 CLOSURE\*\* \| " + _tok(_S27C_DELIVERED),
           r"\*\*STAGE 27 / THERM-01 SLICE 1\*\* \| " + _tok(_S27_DELIVERED),
           r"\*\*STAGE 27\*\* \| " + _tok(_S27_COMPLETE) + r"; its checkbox is TICKED for that scope only; "
           + _tok(_S27_FULL_NO),
           r"no quantified uncertainty or tolerance is claimed; model applicability is bounded by declarations D-1 to D-6; "
           r"outside those conditions the method refuses or abstains; the result stays `UNVALIDATED` and is not evidence; "
           r"measurement or thermal-specialist confirmation stays required before any reliance",
           *(_tok(t) for t in _S27_FACTS),
           re.escape(_S25_NAME) + r", the preceding Owner-authorized\s+bounded increment, is DELIVERED \(Git / GitHub own "
           r"its PR, merge and review identity\): it entered Stage 25 as ENTERED / PARTIAL for\s+that slice ONLY",
           r"\*\*STAGE 25 / CAP-13 SLICE 1\*\* \| " + _tok(_S25_DELIVERED),
           r"\*\*STAGE 25\*\* \| " + _tok(_S25_PARTIAL) + r"; its checkbox stays UNTICKED; Stage 25 is NOT complete; "
           + _tok(_S25_FULL_NO),
           r"\*\*MARKER\*\* \| " + _tok(_S25_MARKER),
           *(_tok(t) for t in _S25_FACTS),
           r"Stage 16 — SRL-Compatible Composition\s+— Closure, the preceding Owner-authorized bounded closure, is "
           r"DELIVERED with no further product change required\b",
           r"Stage 16 is COMPLETE for the current bounded Technical \+ Integration evidence-sufficiency composition scope "
           r"ONLY and its checkbox is ticked for that scope only; \"without hiding the weakest material axis\" is "
           r"satisfied in that bounded scope by independent visible source truth and the explicit focus-scope "
           r"disclosure, and no weakest axis is computed;",
           r"each from its own canonical owner, independently visible and never aggregated",
           r"Stage 13 and Stage 14 stay PARTIAL / DEFERRED",
           re.escape(_S16_NAME) + r", the preceding Owner-authorized bounded increment, is DELIVERED \(PR #\d+;",
           r"\*\*STAGE 16 CLOSURE\*\* \| " + _tok(_S16C_DELIVERED) + r" — a current-truth closure after the delivered "
           r"bounded presentation residual",
           r"\*\*STAGE 16\*\* \| " + _tok(_S16_COMPLETE) + r"; its checkbox is TICKED for that scope only",
           r"\*\*STAGE 16 PRESENTATION RESIDUAL\*\* \| " + _tok(_S16_DELIVERED) + r" — PR #\d+",
           r"\*\*STAGE 16 NOT AUTHORIZED\*\* \| " + _tok(_S16_SRL_NO),
           r"\*\*STAGES 13 / 14\*\* \| " + _tok(_S13_14_PARTIAL[0]) + r" · " + _tok(_S13_14_PARTIAL[1]),
           *(_tok(t) for t in _S16C_FACTS),
           r"Stage 36 — CAP-15 \+ CAP-17\s+— Closure, the preceding Owner-authorized bounded closure, is DELIVERED with "
           r"no product change required\b",
           r"Stage 36 is COMPLETE for the current no-live-AI / provider scope ONLY and its checkbox is ticked for that "
           r"scope only; no production live AI / provider selection exists and none is active",
           r"CAP-15 / CAP-17 stay RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION; the External Engineering Tools "
           r"direction stays PLANNED / DEFERRED with no provider selected; a future live AI / provider selection or "
           r"External Engineering Tools activation needs a fresh Stage-36 reassessment and separate authorization; "
           r"Stage 37 stays NOT ENTERED and NOT AUTHORIZED\.",
           r"Stage 35 — Structured Invention Disclosure Export\s+— Closure, the preceding Owner-authorized bounded "
           r"closure, is DELIVERED with no product change required\b",
           r"\*\*STAGE 36 CLOSURE\*\* \| " + _tok(_S36C_DELIVERED) + r" — a current-truth closure with no product "
           r"change",
           r"\*\*STAGE 36\*\* \| " + _tok(_S36_COMPLETE) + r"; its checkbox is TICKED for that scope only",
           r"\*\*STAGE 36 NOT AUTHORIZED\*\* \| " + _tok(_S36_LIMITS[2]),
           r"\*\*STAGE 37\*\* \| " + _tok(_S37_NOT[0]) + r" · " + _tok(_S37_NOT[1]),
           *(_tok(t) for t in _S36C_FACTS),
           r"Stage 35 is COMPLETE for the current bounded first-slice scope ONLY and its checkbox is ticked for that "
           r"scope only; later Stage-35 slices stay NOT AUTHORIZED; PDF, e-mail artifact delivery, API exposure, "
           r"external transfer, AI / provider calls, patent-claim drafting and patentability / FTO / legal-validity "
           r"conclusions stay outside this closure and NOT AUTHORIZED; the legal-adviser review of the disclaimer "
           r"wording before any user release \(workstream contract §17, decision 9\) stays OPEN and the release "
           r"triggers stay preserved; Stage 36 was then NOT ENTERED and NOT AUTHORIZED\.",      # ROTATED at Stage 36
           re.escape(_S35_NAME) + r", the preceding Owner-authorized bounded increment, governed by the merged\s+"
           r"implementation contract",
           r"it entered Stage 35 as ENTERED / PARTIAL for that slice ONLY until the Stage 35 closure completed Stage "
           r"35 for that bounded scope",
           r"no export-history record and no retained export artifact",
           r"\*\*STAGE 35 CLOSURE\*\* \| " + _tok(_S35C_DELIVERED) + r" — a current-truth closure with no product "
           r"change",
           r"\*\*STAGE 35\*\* \| " + _tok(_S35_COMPLETE) + r"; its checkbox is TICKED for that scope only",
           r"\*\*STAGE 35 NOT AUTHORIZED\*\* \| " + _tok(_S35_LIMITS[0]),
           r"\*\*STAGE 35 PRESERVED TRIGGERS\*\* \| " + _tok(_S35_TRIGGERS),
           r"\*\*NEXT STEP\*\* \| LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT — READ-ONLY",
           # ROTATED at the Stage 36 closure; ADVANCED at the Stage 16 closure (no further Stage-16 / SRL work)
           r"it pre-authorizes no further Stage-16 / SRL work, no later Stage-35 slice, no CAP-15 / CAP-17 "
           r"implementation, no live AI / provider selection, no External Engineering Tools activation, no Stage-37 "
           r"work,",
           r"The only product increment authorized after it was the Stage 35 first bounded slice \(above\), completed "
           r"for that bounded scope by the Stage 35 closure \(above\), and the Stage 36 closure \(above\) then "
           r"completed Stage 36 for its current no-live-AI / provider scope only; the only product increment authorized "
           r"after that closure was the Stage 16 bounded presentation residual \(above\), delivered by PR #\d+ and "
           r"completed for its bounded scope by the Stage 16 closure \(above\); the only product increment authorized "
           r"after that closure was " + re.escape(_S25_NAME) + r" \(above\), delivered, entering Stage 25 as ENTERED / "
           # ADVANCED at the CAP13-THERM01-INTEGRATED-PART-01 current-truth sync: the Stage 27 slice, the Stage 27
           # closure and the delivered integrated-part increment follow the Stage 25 slice in the chain
           r"PARTIAL for that slice only; the only product increment authorized after it was " + re.escape(_S27_NAME)
           + r" \(above\), delivered, entering Stage 27 as ENTERED / PARTIAL for that slice only, and the Stage 27 "
           r"closure \(above\) then completed Stage 27 for its current bounded scope only with no product change; the "
           r"only product increment authorized after that closure was CAP13-THERM01-INTEGRATED-PART-01 \(below\), "
           # ADVANCED at ELECTRICAL-ENERGY-TIME-REFERENCE-01 (merge-effective delivery record): it follows the
           # integrated-part increment in the chain
           r"delivered \(PR #\d+\); the only product increment authorized after it was "
           r"ELECTRICAL-ENERGY-TIME-REFERENCE-01 \(below\), delivered \(PR #\d+\); "
           # ADVANCED at COMPONENT-INVENTORY-DECLARE-LIST-01 (merge-effective delivery record): it follows the
           # energy-time reference increment in the chain
           r"the only product increment authorized after it was COMPONENT-INVENTORY-DECLARE-LIST-01 \(below\), "
           r"delivered \(PR #\d+\); "
           # ADVANCED at 28-T1-SENSING-VALUE-THRESHOLD-01 (merge-effective delivery record): it follows the
           # component-inventory increment in the chain
           r"the only product increment authorized after it was 28-T1-SENSING-VALUE-THRESHOLD-01 \(below\), "
           r"delivered \(PR #\d+\); "
           # ADVANCED at 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 (merge-effective delivery record): it
           # follows the 28-T1 sensing reference increment in the chain
           r"the only product increment authorized after it was 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 \(below\), "
           r"delivered \(PR #\d+\); no subsequent product increment has been authorized\.",
           _tok(_NONE718), _tok(_NEXT_INC_NO), _tok(_NEXT_STAGE_STEP), *(_tok(t) for t in _S35C_FACTS),
           # ADVANCED at the Stage 30 closure: the Stage 30 closure is the last one, Stage 22's the preceding one
           # ADVANCED at the Stage 28 closure: the Stage 28 closure is now the last one, Stage 30's precedes it
           # ADVANCED at the Stage 23 closure: the Stage 23 closure is now the last one, Stage 28's precedes it
           # ADVANCED at the Stage 24 closure: the Stage 24 closure is now the last one, Stage 23's precedes it
           # ADVANCED at the Stage 35 closure: the Stage 35 closure is now the last one, Stage 24's precedes it
           r"Stage 24 — CAP-12 Form Mock-up Advisory\s+— Closure, the preceding Owner-authorized bounded closure, is "
           r"DELIVERED with no product change required\b",
           r"Stage 24 is COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope\s+ONLY, its "
           r"checkbox is ticked for that scope only, full CAP-12 stays NOT AUTHORIZED, further CAP-12 slices stay NOT "
           # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: the Stage 24 closure's
           # CAP-13 / Stage-25 limits read as history
           r"AUTHORIZED,\s+and the closure itself activated no CAP-13 and entered no Stage 25\.",
           r"\*\*STAGE 24 CLOSURE\*\* \| `STAGE 24 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED` — a "
           r"current-truth closure with no product change",
           r"Stage 23 — CAP-06 Four-Axis Readiness\s+Snapshot\s+— Closure, the preceding Owner-authorized bounded "
           r"closure, is DELIVERED with no product change required\b",
           r"Stage 23 is COMPLETE for the current bounded four-axis\s+Readiness Snapshot scope\s+ONLY; full CAP-06 "
           r"stays NOT AUTHORIZED and its eight-axis expansion is not implemented\s+or closed\.",
           r"Stage 28 — " + _CL.title() + r" Optional Part\s+— Closure, the preceding Owner-authorized "
           r"bounded closure, is DELIVERED with no further product change required\b",
           r"\*\*STAGE 23 CLOSURE\*\* \| `STAGE 23 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED` — a "
           r"current-truth closure with no product change",
           r"\*\*STAGE 23\*\* \| `STAGE 23: COMPLETE — CURRENT BOUNDED FOUR-AXIS READINESS-SNAPSHOT SCOPE ONLY`; "
           r"its checkbox is TICKED for that scope only",
           r"problem clarity, mechanism completeness, physical feasibility, evidence strength as its own axis, "
           r"assumption integrity, testability, prototype readiness and patent-disclosure readiness stay outside "
           r"this closure",
           r"Stage 30 — " + _CL.title() + r" Part-Enablement Safeguards\s+— Closure, the preceding Owner-authorized "
           r"bounded closure, is DELIVERED with no further product change required\b",
           r"Stage 22 — Decision Trace \+ Decision Room — Closure, the\s+preceding\s+Owner-authorized bounded "
           r"closure, is DELIVERED with no product change required\b",
           r"Stage 22 is\s+COMPLETE for the current bounded decision trace \+ decision room scope only; Stage 21 stays "
           r"COMPLETE for the current\s+Owner-declared contradiction scope only; Stage 20 stays COMPLETE for the "
           r"current Owner-declared assumption scope\s+only; Stage 19 stays COMPLETE for the current planning-only "
           r"scope only; Stage 18 and Stage 15 stay COMPLETE for the\s+current Mechanical \+ Electrical / Electronics "
           r"scope only\.",
           r"\*\*STAGE 22 CLOSURE\*\* \| `STAGE 22 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED` — a current-truth "
           r"closure with no product change",
           r"genuine closure gap NONE; architecture trigger NONE",
           r"\*\*STAGE 22\*\* \| `STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE \+ DECISION ROOM SCOPE`; its "
           r"checkbox is TICKED for that scope only; the delivered basis is CAP-05 \+ CAP-07 Slice 1 \(PR #\d+\) and "
           r"Slice 2 \(PR #\d+\) only",
           r"a project-context panel explicitly NOT LINKED to any specific decision",
           r"recommendation, best-option or winner selection, confidence, evidence-strength or readiness scoring, "
           r"inferred decision ↔ context linkage and AI decision advice stay NOT AUTHORIZED",
           # AMENDED at the Stage 24 closure: the marker row names Stage 25; `NO STAGE-24 …` stays true history
           r"\*\*MARKER\*\* \| " + _tok(_S25_MARKER) + "; " + _tok(_NO_S25),
           r"Stage 24 / CAP-12 \(bounded materials / manufacturing advice\) was entered only by the separately "
           r"Owner-authorized, delivered Form Mock-up Advisory Slice 1 and completed for that bounded scope only by "
           r"the Stage 24 closure",
           r"\*\*STAGE 24 / CAP-12 SLICE 1\*\* \| " + _tok(_S24_DELIVERED),
           r"\*\*STAGE 24\*\* \| " + _tok(_S24_COMPLETE) + r"; its checkbox is TICKED for that scope only",
           r"\*\*STAGE 21 CLOSURE\*\* \| `STAGE 21 CLOSURE: DELIVERED`",
           r"\*\*STAGE 21\*\* \| `STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE`; its checkbox "
           r"is TICKED for that scope only",
           r"withdrawal of a declaration, a resolution workflow, winner selection, validation and contradictions over "
           r"assumptions, quantities, commercial items, evidence, success criteria or decisions stay NOT AUTHORIZED",
           r"\*\*STAGE 20 CLOSURE\*\* \| `STAGE 20 CLOSURE: DELIVERED`",
           r"\*\*STAGE 20\*\* \| `STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE`; its checkbox is "
           r"TICKED for that scope only",
           r"append-only revision, append-only replacement and retained supersession history",
           r"automatic assumption detection or resolution, validation confirmation / rejection, impact scoring, risk "
           r"scoring or new CAP-08 risk fields, an inventor-authored evidence-needed field, decision linkage, dependency "
           r"transfer / propagation and AI inference stay NOT AUTHORIZED",
           r"\*\*STAGE 19 CLOSURE\*\* \| `STAGE 19 CLOSURE: DELIVERED`",
           r"\*\*STAGE 19\*\* \| `STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE`; its checkbox is TICKED for that "
           r"scope only",
           r"no scientific validity, validated result, prototype validation, readiness, risk resolution or feasibility "
           r"is claimed", r"`STAGE 18 CLOSURE: DELIVERED`",
           r"\*\*STAGE 18\*\* \| `STAGE 18: COMPLETE — CURRENT MECHANICAL \+ ELECTRICAL / ELECTRONICS SCOPE`; its "
           r"checkbox is TICKED for that scope only",
           r"full future CAP-01 \(typed parameters, calculations, specialist mapping, further domains\) stays NOT "
           r"AUTHORIZED", r"MSNL stays FUTURE / DEFERRED / NOT ACTIVATED",
           # ROTATED at the Stage 16 closure: Stage 16 is COMPLETE for its bounded scope and no longer routed past
           r"routing past Stages 11, 13, 14 and 17 completes none of them",
           r"\*\*STAGE 15\*\* \| `STAGE 15: COMPLETE — CURRENT MECHANICAL \+ ELECTRICAL / ELECTRONICS SCOPE`; its "
           r"checkbox is TICKED for that scope only",
           r"another Stage-15 slice is NOT AUTHORIZED", r"D4 stays the future compatibility gate",
           r"Phase-7 integration residuals remain Phase 7", r"no IRL score or level",
           r"delivered history never fills the active-contract slot",
           _tok(_S23C_DELIVERED), _tok(_S23_COMPLETE),
           *(_tok(t) for t in _S23_LIMITS), _tok(_S25_MARKER), _tok(_NO_S25), _tok(_S24C_DELIVERED),
           _tok(_S24_COMPLETE), _tok(_S24_DELIVERED), *(_tok(t) for t in _S24C_LIMITS), _tok(_S22C_DELIVERED),
           _tok(_S22_COMPLETE), *(_tok(t) for t in _S22_LIMITS), _status(_S21C_DELIVERED),
           _tok(_S21_COMPLETE), *(_tok(t) for t in _S21_LIMITS), _status(_S20C_DELIVERED),
           _tok(_S20_COMPLETE), _tok("`FULL CAP-08: NOT AUTHORIZED`"), _status(_S19C_DELIVERED),
           _tok(_S19_COMPLETE), *(_tok(t) for t in _S19_LIMITS), _status(_S18C_DELIVERED),
           _tok(_S18_COMPLETE), _tok(_MSNL_FUTURE), _status(_S15C_DELIVERED), _status(_S4_DELIVERED),
           _status(_R1_DELIVERED), _status(_S3_DELIVERED), _status(_S2_DELIVERED), _status(_S15_DELIVERED),
           _tok(_S15_COMPLETE), *(_tok(t) for t in _S15C_NOT + _S2_NOT))
    _rejects(top, CONTRACT, "live none", *_S2_CLOSE_REVERSALS, *_S15C_STALE, *_S18C_STALE, *_S19C_STALE,
             *_S20C_STALE, *_S21C_STALE, *_S22C_STALE, *_S23C_STALE, *_S24C_STALE, *_S24CL_STALE, *_S35C_STALE,
             *_S35C_REVERSALS, *_S36C_STALE, *_S36C_REVERSALS,
             *_S16C_STALE, *_S16C_REVERSALS, *_S25_STALE, *_S25_REVERSALS,
             *_S27_STALE, *_S27_REVERSALS)
    for path, block in _live_surfaces():
        _needs(block, path, "live none", _tok(_NONE718), _tok(_NEXT_INC_NO), _tok(_NEXT_STAGE_STEP),
               *(_tok(t) for t in _S35C_FACTS), *(_tok(t) for t in _S36C_FACTS), *(_tok(t) for t in _S16C_FACTS),
               _tok(_S23C_DELIVERED), _tok(_S23_COMPLETE), *(_tok(t) for t in _S23_LIMITS),
               _tok(_S25_MARKER), _tok(_NO_S25), _tok(_S24C_DELIVERED), _tok(_S24_COMPLETE), _tok(_S24_DELIVERED),
               *(_tok(t) for t in _S24C_LIMITS),
               _tok(_S22C_DELIVERED), _tok(_S22_COMPLETE),
               *(_tok(t) for t in _S22_LIMITS),
               _status(_S21C_DELIVERED), _tok(_S21_COMPLETE),
               *(_tok(t) for t in _S21_LIMITS[:2]),
               _status(_S20C_DELIVERED), _tok(_S20_COMPLETE), *(_tok(t) for t in _S20_LIMITS),
               _status(_S19C_DELIVERED), _tok(_S19_COMPLETE),
               *(_tok(t) for t in _S19_LIMITS),
               _status(_S18C_DELIVERED), _tok(_S18_COMPLETE), _tok(_MSNL_FUTURE),
               _status(_S15C_DELIVERED), _status(_S4_DELIVERED), _status(_R1_DELIVERED), _status(_S3_DELIVERED),
               _status(_S2_DELIVERED), _status(_S15_DELIVERED), _status(_EL_DELIVERED), _tok(_S15_COMPLETE),
               _tok(_NO_TD_SUBTASK), *(_tok(t) for t in _S15C_NOT + _S2_NOT),
               r"Stage\s+22\s+closure\s+\(delivered\)\.\s+No\s+product\s+change\s+was\s+required",
               r"grouped\s+strictly\s+by\s+the\s+canonical\s+Validation\s+Plan\s+responsibility\s+tokens",
               r"explicitly\s+NOT\s+LINKED\s+to\s+any\s+specific\s+decision",
               r"Full\s+CAP-05\s+and\s+full\s+CAP-07\s+stay\s+NOT\s+AUTHORIZED",
               r"Stage\s+21\s+closure\s+\(delivered\)\.\s+The\s+working\s+session\s+page\s+carries\s+ONE\s+"
               r"read-only\s+view\s+of\s+the\s+contradictions\s+the\s+inventor\s+declared",
               r"a\s+link\s+to\s+the\s+EXISTING\s+correction\s+form",
               r"No\s+longer\s+active:\s+one\s+of\s+its\s+two\s+answers\s+was\s+later\s+replaced\.\s+Kept\s+as\s+"
               r"history\.",
               r"a\s+derivation\s+failure\s+reads\s+unavailable,\s+never\s+\"none\"",
               r"Stage\s+20\s+closure\s+\(delivered\)\.\s+For\s+each\s+ACTIVE\s+Owner-declared\s+provisional\s+"
               r"assumption",
               r"inherits\s+the\s+gap\s+and\s+question\s+target\s+verbatim",
               r"\(no\s+transfer,\s+no\s+inferred\s+edge\)",
               r"Replace\s+is\s+refused\s+(while\s+the\s+target's\s+exact\s+question\s+is\s+a\s+CURRENT\s+outstanding|"
               r"for\s+a\s+CURRENT\s+outstanding)\s+routed\s+need",
               r"\(no\s+progression\s+iteration\s+ran",
               r"Stage\s+19\s+closure\s+\(delivered\)\.\s+For\s+each\s+CURRENT\s+Section-11\s+experiment",
               r"bound\s+only\s+by\s+the\s+canonical\s+`experiment_id`",
               r"never\s+\"no\s+result\"",
               r"Section-11\s+note\s+\(English\s+generated\s+content\s+in\s+both\s+UI\s+locales\)",
               r"Full\s+CAP-09\s+and\s+full\s+WS-PFV-001\s+stay\s+NOT\s+AUTHORIZED",
               r"Stage\s+18\s+closure\s+\(delivered\)\.\s+For\s+each\s+current\s+canonical\s+MECHANISM_COMPLETENESS",
               r"technical\s+next-steps\s+sub-view\s+owned\s+by\s+`web/cap01_guidance\.py`",
               r"the\s+canonical\s+questions\s+and\s+Path-N\s+stay\s+the\s+missing-information\s+owner",
               r"an\s+explicit\s+specialist\s+abstention",
               r"no\s+inventor\s+text,\s+answer,\s+keyword,\s+label,\s+signal\s+or\s+list\s+position",
               r"`CAP01_GAP_NEXT_STEPS`\s+traceability\s+table",
               r"No\s+value,\s+range,\s+threshold,\s+formula\s+selection,\s+calculation,\s+test\s+protocol,\s+pass\s+/\s+"
               r"fail\s+criterion",
               r"the\s+domain\s+packs\s+and\s+provenance\s+are\s+byte-unchanged",
               r"Research\s+Gate\s+3\s+prerequisites\s+applied\s+to\s+research-backed\s+knowledge\s+expansion",
               r"MSNL\s+stays\s+FUTURE\s+/\s+DEFERRED\s+/\s+NOT\s+ACTIVATED",
               r"Full\s+future\s+CAP-01\s+\(typed\s+parameters,\s+calculations,\s+specialist\s+mapping,\s+further\s+"
               r"domains\)\s+stays\s+NOT\s+AUTHORIZED",
               r"Stage\s+15\s+closure\s+\(delivered\)\.\s+For\s+each\s+durable\s+Owner-declared\s+interface",
               r"the\s+exact\s+dependent\s+and\s+depends-on\s+part\s+identities\s+are\s+persisted",
               r"exactly\s+ONE\s+immutable\s+interface\s+anchor",
               r"fourth\s+row,\s+Integration\s+—\s+INSUFFICIENT_EVIDENCE\s+only",
               r"Observations,\s+preparation\s+inputs\s+and\s+dependencies\s+are\s+never\s+converted\s+into\s+evidence",
               r"D4\s+stays\s+the\s+future\s+compatibility\s+gate",
               r"Phase-7\s+integration\s+residuals\s+remain\s+Phase\s+7",
               r"Stage\s+15\s+Slice\s+4\s+\(delivered\)\.\s+For\s+each\s+durable\s+Owner-declared\s+interface",
               r"InventorAI\s+does\s+not\s+decide\s+whether\s+the\s+acceptance\s+criterion\s+was\s+met",
               r"CAP-09\s+Result\s+Event\s+Slice\s+1\s+\(delivered\):\s+for\s+ONE\s+current\s+canonical",
               r"Stage\s+15\s+Slice\s+3\s+\(delivered\)\.\s+For\s+each\s+CURRENT\s+durable\s+Owner-declared",
               r"Stage\s+15\s+Slice\s+2\s+\(delivered\)\.\s+For\s+ONE\s+integrated\s+Mechanical",
               r"engineering\s+compatibility\s+has\s+NOT\s+been\s+established",
               r"Stage\s+15\s+Slice\s+1\s+\(delivered\)\.")
        _rejects(_live_only(block), path, "live none", *_S2_CLOSE_REVERSALS, *_S15C_STALE, *_S18C_STALE,
                 *_S19C_STALE, *_S20C_STALE, *_S21C_STALE, *_S22C_STALE, *_S23C_STALE, *_S24C_STALE,
                 *_S24CL_STALE, *_S35C_STALE, *_S35C_REVERSALS, *_S36C_STALE, *_S36C_REVERSALS,
                 *_S16C_STALE, *_S16C_REVERSALS, *_S25_STALE, *_S25_REVERSALS,
             *_S27_STALE, *_S27_REVERSALS)
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "live routing",
               # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 ENTERED / PARTIAL for it only;
               # AMENDED at the Stage 24 closure: the marker is Stage 25 (NOT ENTERED), Stage 24 COMPLETE for its scope
               # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED /
               # PARTIAL for that slice only
               r"(?i)CURRENT MASTER ROADMAP STAGE: Stage 25 — CAP-13 thickness / specification / safety capability — "
               r"ENTERED / PARTIAL — NAVIGATION ONLY",
               r"Stage 24 — CAP-12 bounded materials / manufacturing advice — is COMPLETE for the current bounded "
               r"CAP-12 Form Mock-up Advisory Slice 1 scope \(its checkbox is ticked for that scope only\)",
               r"Stage 25 / CAP-13 was entered only by the separately Owner-authorized, delivered " + re.escape(_S25_NAME),
               r"Stage 25 is ENTERED / PARTIAL for that slice ONLY — NOT complete, checkbox UNTICKED — and full CAP-13 "
               r"stays NOT AUTHORIZED",
               r"Stage 23 — CAP-06 multi-axis readiness dashboard — is COMPLETE for the current bounded four-axis "
               r"Readiness Snapshot scope \(its checkbox is ticked for that scope only\)",
               r"Stage 22 — CAP-05 decision trace \+ CAP-07 decision room — is COMPLETE for the current bounded "
               r"decision trace \+ decision room scope \(its checkbox is ticked for that scope only\)",
               r"Stage 21 — CAP-10 contradiction detector — is COMPLETE for the current Owner-declared contradiction "
               r"scope \(its checkbox is ticked for that scope only\)",
               r"Stage 20 — CAP-08 assumption register — is COMPLETE for the current Owner-declared assumption scope "
               r"\(its checkbox is ticked for that scope only\)",
               r"Stage 19 — WS-PFV-001 / CAP-09 experiment-plan designer — is COMPLETE for the current planning-only "
               r"scope \(its checkbox is ticked for that scope only\)",
               r"Stage 18 — D13 / CAP-01 structured technical guidance — is COMPLETE for the current Mechanical \+ "
               r"Electrical / Electronics scope \(its checkbox is ticked for that scope only\)",
               # ROTATED at the Stage 16 closure: Stage 16 is COMPLETE for its bounded scope, so it is no longer routed past
               r"routing past Stages 11, 13, 14 and 17 completes none of them",
               # ADVANCED at the Stage 30 closure: the head now also names Stage 30 COMPLETE for its bounded scope
               # ADVANCED at the Stage 28 part-only enablement: the head also names the part-only enablement
               # ADVANCED at the Stage 23 closure: the head now leads with Stage 23 COMPLETE for its bounded scope
               # ADVANCED at the delivered CAP-12 Form Mock-up Advisory Slice 1: the head leads with that delivery
               # ADVANCED at the Stage 24 closure: the head leads with Stage 24 COMPLETE for its bounded scope
               # ROTATED at the Stage 35 first bounded slice: the head named the active Stage-35 increment first
               # ROTATED at the Stage 35 closure: the head is NO ACTIVE CONTRACT again and leads with Stage 35 COMPLETE
               # for its bounded first-slice scope
               # ADVANCED at the Stage 36 closure: the head leads with Stage 36 COMPLETE for its bounded scope
               # ADVANCED at the Stage 16 closure: the head leads with Stage 16 COMPLETE for its bounded scope
               # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: the head leads with
               # Stage 25 ENTERED / PARTIAL through that slice only
               # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: the head leads
               # with Stage 27 ENTERED / PARTIAL through that slice only, then Stage 25
               # ROTATED at the Stage 27 closure: the head leads with Stage 27 COMPLETE for its bounded scope
               r"\*\*NO ACTIVE CONTRACT — post-Stage-27-closure \(2026-10-09\); Stage 27 COMPLETE for the current bounded "
               r"THERM-01 single-path temperature-difference scope only; Stage 25 ENTERED / PARTIAL "
               r"through its delivered CAP-13 Two-Support Static Reactions Slice 1 only; Stage 16 COMPLETE for the current "
               r"bounded Technical \+ Integration evidence-sufficiency composition scope only; Stage 36 COMPLETE for the "
               r"current no-live-AI / provider scope only; Stage 35 COMPLETE for the current "
               r"bounded first-slice scope only; Stage 24 COMPLETE for the current bounded CAP-12 Form Mock-up Advisory "
               r"Slice 1 scope only; Stage 23 COMPLETE for the current bounded four-axis Readiness Snapshot scope only;",
               # WIDENED at the Stage 16 closure (length only): the head now also leads with the Stage 16 clause
               # WIDENED at the delivered Stage 27 / THERM-01 slice (length only): the head also leads with the Stage 27 clause
               r"\*\*NO ACTIVE CONTRACT — [^*]{0,1200}; Stage 22 COMPLETE for the current bounded "
               r"decision trace \+ "
               r"decision room scope; Stage 21 COMPLETE for the current Owner-declared contradiction "
               r"scope; Stage 20 COMPLETE for the current Owner-declared assumption scope; Stage 19 COMPLETE for the "
               r"current planning-only scope; Stage 18 COMPLETE for the current Mechanical \+ Electrical / Electronics "
               r"scope; Stage 15 COMPLETE for the current Mechanical \+ Electrical / Electronics scope; Stage 25 "
               r"ENTERED / PARTIAL — navigation only:\*\*",
               # ADVANCED at Stage 28 Qualification Slices 1 and 2 and Optional Part Slices 1 and 2: the last delivery
               # is now Optional Part Slice 2
               # ADVANCED at Stage 30 Part Safeguards Slice 1: the last delivery is now that Stage-30 slice
               # ADVANCED at the Stage 30 closure: the last delivery is now the Stage 30 closure
               # ADVANCED at the Stage 28 part-only enablement: the last delivery is now that enablement
               # ADVANCED at the Stage 28 closure: the last delivery is now the Stage 28 closure
               # ADVANCED at the Stage 23 closure: the last delivery is now the Stage 23 closure
               # ADVANCED at the delivered CAP-12 Form Mock-up Advisory Slice 1: the last delivery is now that slice
               # ADVANCED at the Stage 24 closure: the last delivery is now the Stage 24 closure
               # ROTATED at the Stage 35 first bounded slice: the Stage-35 increment was the active one
               # ROTATED at the Stage 35 closure: no product increment is authorized after the Stage 35 closure; the
               # delivered first bounded slice precedes it and the Stage 24 closure follows
               # ADVANCED at the Stage 36 closure: no product increment is authorized after the Stage 36 closure; the
               # Stage 35 closure, whose Stage-36 statement is now history, precedes it
               # ADVANCED at the Stage 16 closure: no product increment is authorized after the Stage 16 closure; the
               # delivered Stage 16 residual and the Stage 36 closure precede it
               # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: no product
               # increment is authorized after that slice; the Stage 16 closure precedes it
               # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: no product
               # increment is authorized after that slice; the Stage 25 slice precedes it
               # ROTATED at the Stage 27 closure: no product increment is authorized after the Stage 27 closure; the slice
               # precedes it
               # ADVANCED at the CAP13-THERM01-INTEGRATED-PART-01 current-truth sync: no product increment is
               # authorized after that delivered increment; the Stage 27 closure precedes it
               # ADVANCED at ELECTRICAL-ENERGY-TIME-REFERENCE-01 (merge-effective delivery record): no product
               # increment is authorized after it; the integrated-part increment precedes it
               # ADVANCED at COMPONENT-INVENTORY-DECLARE-LIST-01 (merge-effective delivery record): no product
               # increment is authorized after it; the energy-time reference increment precedes it
               # ADVANCED at 28-T1-SENSING-VALUE-THRESHOLD-01 (merge-effective delivery record): no product
               # increment is authorized after it; the component-inventory increment precedes it
               # ADVANCED at 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 (merge-effective delivery record): no
               # product increment is authorized after it; the 28-T1 sensing reference increment precedes it
               r"No product increment is authorized after 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 \(delivered: PR #\d+; "
               r"[^)]*non-focused required part questions[^)]*recording only[^)]*no Stage entered, completed or "
               r"reopened; effective only on the verified merge of PR #\d+\) or after the preceding "
               r"28-T1-SENSING-VALUE-THRESHOLD-01 \(delivered: PR #\d+; "
               r"[^)]*value versus above-threshold indication[^)]*explanation only[^)]*no Stage entered, completed or "
               r"reopened; effective only on the verified merge of PR #\d+\) or after the preceding "
               r"COMPONENT-INVENTORY-DECLARE-LIST-01 \(delivered: PR #\d+; "
               r"[^)]*declare and list only[^)]*one OWNER_STATED / UNVALIDATED record per physical component[^)]*no "
               r"Stage entered, completed or reopened; effective only on the verified merge of PR #\d+\) or after the "
               r"preceding ELECTRICAL-ENERGY-TIME-REFERENCE-01 \(delivered: PR #\d+; "
               r"[^)]*constant P[^)]*reference only, no calculation; no Stage entered, completed or reopened; effective "
               r"only on the verified merge of PR #\d+\) or after the preceding "
               r"CAP13-THERM01-INTEGRATED-PART-01 \(delivered: PR #\d+, merge "
               r"`[0-9a-f]{40}`; [^)]*eligibility to offer only, never applicability, "
               r"validation or safety; no Stage entered, completed or reopened\) or after the preceding "
               + re.escape(_S27C_NAME) + r" \(delivered: Stage 27 is "
               r"COMPLETE for the current bounded THERM-01 single-path temperature-difference scope only with no product "
               r"change[^)]*; full THERM-01 NOT AUTHORIZED\) or after the preceding " + re.escape(_S27_NAME)
               + r" \(delivered: ONE optional, "
               r"advisory, non-binding, request-local calculation on a project whose durable root domain is "
               r"`electronics_electrical`.*?; it entered Stage 27 as ENTERED / PARTIAL until the Stage 27 closure; full "
               r"THERM-01 stays NOT AUTHORIZED\) or after the preceding " + re.escape(_S25_NAME) + r" \(delivered: ONE optional, "
               r"advisory, non-binding, request-local calculation on a project whose durable root domain is `mechanical`"
               r".*?; Stage 25 ENTERED / PARTIAL through it only, NOT complete; full CAP-13 stays NOT AUTHORIZED\) or "
               r"after the preceding " + re.escape(_S16C_NAME) + r" \(delivered: Stage 16 is "
               r"COMPLETE for the current bounded Technical \+ Integration evidence-sufficiency composition scope only "
               r"with no further product change — closure gap NONE after the delivered bounded presentation residual: "
               r"[^)]*\(s\); no single score, weighting, composite, overall readiness result, weakest-axis calculation, SRL "
               r"number or level, engineering compatibility conclusion or validated system-readiness conclusion; Stage "
               r"13 and Stage 14 stay PARTIAL / DEFERRED\) or after the preceding " + re.escape(_S16_NAME)
               + r" \(delivered by PR #\d+: ONE Owner-authorized bounded presentation-only residual[^)]*\(s\)[^)]*\) or "
               r"after the preceding " + re.escape(_S36C_NAME) + r" \(delivered: Stage 36 is "
               r"COMPLETE for the current no-live-AI / provider scope only with no product change — closure gap NONE: "
               r"[^)]*; Stage 37 stays NOT ENTERED and NOT AUTHORIZED\) or after the preceding " + re.escape(_S35C_NAME)
               + r" \(delivered: Stage 35 is "
               r"COMPLETE for the current bounded first-slice scope only with no product change — closure gap NONE — "
               r"[^)]*; Stage 36 was then NOT ENTERED and NOT AUTHORIZED\) or after the preceding " + re.escape(_S35_NAME)
               + r" \(delivered: for ONE authenticated owner and ONE owned project[^)]*\) or after Stage 24 — CAP-12 "
               r"Form Mock-up Advisory — Closure "
               r"\(delivered: [^)]*\) or after the preceding Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1 "
               r"\(delivered: [^)]*\) or after the preceding Stage 23 — CAP-06 Four-Axis Readiness Snapshot — "
               r"Closure \(delivered: [^)]*\)\. Stage 22 is COMPLETE for the current bounded decision trace \+ decision "
               r"room scope only",
               r"\*\*DELIVERED — Stage 24 / CAP-12 Form Mock-up Advisory — Closure \(completes Stage 24 for the current "
               r"bounded CAP-12 Form Mock-up Advisory Slice 1 scope ONLY with no product change",
               r"\*\*DELIVERED — Stage 23 / CAP-06 Four-Axis Readiness Snapshot — Closure \(completes Stage 23 for "
               r"the current bounded four-axis Readiness Snapshot scope ONLY with no product change",
               r"\*\*DELIVERED — Stage 22 / Decision Trace \+ Decision Room — Closure \(completes Stage 22 for the "
               r"current bounded decision trace \+ decision room scope with no product change",
               r"the Stage-22 checkbox is ticked for the current bounded decision trace \+ decision room scope only",
               r"\*\*DELIVERED — Stage 21 / Owner-Declared Contradiction Visibility — Closure \(completes Stage 21 "
               r"for the current Owner-declared contradiction scope",
               r"the Stage-21 checkbox is ticked for the current Owner-declared contradiction scope only",
               r"\*\*DELIVERED — Stage 20 / Assumption Revision & Replacement — Closure \(completes Stage 20 for the "
               r"current Owner-declared assumption scope",
               r"The Stage-20 checkbox is ticked for the current Owner-declared assumption scope only|the Stage-20 "
               r"checkbox is ticked for the current Owner-declared assumption scope only",
               r"\*\*DELIVERED — Stage 19 / Experiment Execution-State Disclosure — Closure \(completes Stage 19 for "
               r"the current planning-only scope",
               # ROTATED at the Stage 35 closure: the next step is the Lead-controlled reassessment again
               r"The next step is a LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT: read-only planning / selection "
               r"over live repository and product evidence until the Owner separately authorizes another product "
               r"increment\. It pre-authorizes no further Stage-16 / SRL work, no later Stage-35 slice, no CAP-15 / CAP-17 "
               r"implementation, no live AI / provider selection, no External Engineering Tools activation, no Stage-37 "
               r"work,",      # ROTATED at 36; ADVANCED at the Stage 16 closure
               r"the legal-adviser review of the disclaimer wording before any user release and the release triggers "
               r"stay preserved",
               # AMENDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 is ENTERED /
               # PARTIAL for that slice only and nothing is complete beyond the scoped completions
               # AMENDED at the delivered Stage 27 / THERM-01 slice: Stage 27 ENTERED / PARTIAL leads the parenthetical
               # AMENDED at the Stage 27 closure: Stage 27 COMPLETE for its current bounded scope leads the parenthetical
               r"Stage 25 or any other Stage is complete, or that any other Stage is entered \(Stage 27 is COMPLETE for "
               r"its current bounded THERM-01 single-path temperature-difference scope only; Stage 25 is ENTERED / "
               r"PARTIAL for its CAP-13 Two-Support Static Reactions Slice 1 only; Stage 24 is COMPLETE for its current bounded "
               r"CAP-12 Form Mock-up Advisory Slice 1 scope only; Stage 35 is COMPLETE for its current bounded "
               r"first-slice scope only; Stage 36 is COMPLETE for its current no-live-AI / provider scope only; Stage 16 is "
               r"COMPLETE for its current bounded Technical \+ Integration evidence-sufficiency composition scope only\)",
               # ADDED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: its record leads
               # ADDED at the Stage 27 closure: its closure record leads the delivered list; the slice record follows
               r"\*\*DELIVERED — Stage 27 / THERM-01 Single-Path Temperature-Difference — Closure \(completes Stage 27 for "
               r"the current bounded THERM-01 single-path temperature-difference scope ONLY with no product change; full "
               r"THERM-01 NOT AUTHORIZED",
               r"\*\*DELIVERED — Stage 27 / THERM-01 Single-Path Temperature-Difference — Slice 1 \(it entered Stage 27 "
               r"as ENTERED / PARTIAL for that slice ONLY until the Stage 27 closure; full THERM-01 NOT "
               r"AUTHORIZED",
               # ADDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: its record leads the list
               r"\*\*DELIVERED — Stage 25 / CAP-13 Two-Support Static Reactions — Slice 1 \(it entered Stage 25 as "
               r"ENTERED / PARTIAL for that slice ONLY; Stage 25 NOT complete, checkbox UNTICKED; full CAP-13 NOT "
               r"AUTHORIZED",
               # ADDED at the Stage 16 closure: its closure record and the delivered residual lead the delivered list
               r"\*\*DELIVERED — Stage 16 / SRL-Compatible Composition — Closure \(completes Stage 16 for the current "
               r"bounded Technical \+ Integration evidence-sufficiency composition scope ONLY with no further product "
               r"change; no SRL level, score or weakest-axis computation; Stages 13 and 14 stay PARTIAL / DEFERRED",
               r"\*\*DELIVERED — Stage 16 / SRL-Compatible Composition — Technical-Row Focus-Scope Disclosure \(PR #\d+; "
               r"ONE Owner-authorized bounded presentation-only residual; it entered no other Stage\):\*\* "
               + _tok(_S16_DELIVERED),
               r"\*\*DELIVERED — Stage 36 / CAP-15 \+ CAP-17 — Closure \(completes Stage 36 for the current no-live-AI "
               r"/ provider scope ONLY with no product change",
               r"\*\*DELIVERED — Stage 35 / Structured Invention Disclosure Export — Closure \(completes Stage 35 for "
               r"the current bounded first-slice scope ONLY with no product change",
               r"\*\*DELIVERED — Stage 35 / Structured Invention Disclosure Export — First Bounded Product Slice \(it "
               r"entered Stage 35 as ENTERED / PARTIAL for that slice ONLY until the Stage 35 closure",
               r"\*\*DELIVERED — Stage 18 / Gap-Scoped Technical Next-Step Guidance — Closure \(completes Stage 18 for "
               r"the current Mechanical \+ Electrical / Electronics scope",
               r"\*\*DELIVERED — Stage 15 / Integration Evidence & IRL-Compatible View — Closure",
               r"\*\*DELIVERED — Stage 15 / Interface Verification Observation Event — Slice 4",
               r"\*\*DELIVERED — CAP-09 Result Event Slice 1 \(inside Stage 19",
               r"\*\*DELIVERED — Stage 15 / Interface Verification Preparation Metadata — Slice 3",
               r"\*\*DELIVERED — Stage 15 / Subsystem Interface Declaration & Verification Preparation — Slice 2",
               r"\*\*DELIVERED — Stage 15 / Integrated Invention Entry & Durable Subsystem Composition — Slice 1")
        marker = re.search(r"(?i)CURRENT MASTER ROADMAP STAGE: Stage 25", routing).start()
        # ROTATED at the Stage 35 closure: the NO ACTIVE CONTRACT head is live again; no active-increment head
        # survives, and the two Stage-35 delivered records lead the delivered list
        # ADVANCED at the Stage 36 closure: the Stage 36 closure record leads them
        # ADVANCED at the Stage 16 closure: the Stage 16 closure record and the delivered residual lead them
        assert marker < routing.index("**NO ACTIVE CONTRACT — "), path
        assert "**ACTIVE BOUNDED PRODUCT INCREMENT — " not in _live_only(routing), path
        assert routing.index("**DELIVERED — Stage 16 / SRL-Compatible Composition — Closure") < routing.index(
            "**DELIVERED — Stage 16 / SRL-Compatible Composition — Technical-Row Focus-Scope Disclosure"), path
        assert routing.index("**DELIVERED — Stage 16 / SRL-Compatible Composition — Technical-Row Focus-Scope "
                             "Disclosure") < routing.index("**DELIVERED — Stage 36 / CAP-15 + CAP-17 — Closure"), path
        assert routing.index("**DELIVERED — Stage 36 / CAP-15 + CAP-17 — Closure") < routing.index(
            "**DELIVERED — Stage 35 / Structured Invention Disclosure Export — Closure"), path
        assert routing.index("**DELIVERED — Stage 35 / Structured Invention Disclosure Export — Closure") < routing.index(
            "**DELIVERED — Stage 35 / Structured Invention Disclosure Export — First Bounded Product Slice"), path
        assert routing.index("**DELIVERED — Stage 35 / Structured Invention Disclosure Export — First Bounded Product "
                             "Slice") < routing.index("**DELIVERED — Stage 24 / CAP-12 Form Mock-up Advisory — Closure"), path
        assert routing.index("**DELIVERED — Stage 24 / CAP-12 Form Mock-up Advisory — Closure") < routing.index(
            "**DELIVERED — Stage 23 / CAP-06 Four-Axis"), path
        assert routing.index("**DELIVERED — Stage 23 / CAP-06 Four-Axis") < routing.index(
            "**DELIVERED — Stage 28 / " + _CL.title() + " Optional Part — Closure"), path
        assert routing.index("**DELIVERED — Stage 22 / Decision Trace") < routing.index(
            "**DELIVERED — Stage 21 / Owner-Declared Contradiction"), path
        assert routing.index("**DELIVERED — Stage 21 / Owner-Declared Contradiction") < routing.index(
            "**DELIVERED — Stage 20 / Assumption Revision"), path
        assert routing.index("**DELIVERED — Stage 20 / Assumption Revision") < routing.index(
            "**DELIVERED — Stage 19 / Experiment Execution-State"), path
        assert routing.index("**DELIVERED — Stage 19 / Experiment Execution-State") < routing.index(
            "**DELIVERED — Stage 18 / Gap-Scoped"), path
        assert routing.index("**DELIVERED — Stage 18 / Gap-Scoped") < routing.index(
            "**DELIVERED — Stage 15 / Integration Evidence"), path
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        after = _after_fence(path, "current-routing")
        # ADVANCED at the Stage 16 closure: the post-Stage-36-closure NONE routing is preserved history
        assert ("*(Superseded 2026-10-06 by " + _S16C_NAME + ", preserved so the change is visible rather than silent: "
                "the current routing read \"**NO ACTIVE CONTRACT — post-Stage-36-closure (2026-10-05); Stage 36 "
                "COMPLETE for the current no-live-AI / provider scope only; …:** " + _NONE718 + " · " + _NEXT_INC_NO + " · "
                + _NEXT_STAGE_STEP + " · " + _S36C_DELIVERED + " · …\"") in after, path
        assert re.search(_any_pr("\"… routing past Stages 11, 13, 14, 16 and 17 completes none of them\", with Stage 16 "
                                 "unticked and recorded as DEFERRED. That was true until the Owner authorized the Stage "
                                 "16 bounded presentation residual (delivered by PR #N) and the Stage 16 closure.)*"),
                         after), path
        # ADVANCED at the Stage 36 closure: the post-Stage-35-closure NONE routing is preserved history
        assert ("*(Superseded 2026-10-05 by " + _S36C_NAME + ", preserved so the change is visible rather than silent: "
                "the current routing read \"**NO ACTIVE CONTRACT — post-Stage-35-closure (2026-10-05); Stage 35 "
                "COMPLETE for the current bounded first-slice scope only; …:** " + _NONE718 + " · " + _NEXT_INC_NO + " · "
                + _NEXT_STAGE_STEP + " · " + _S35C_DELIVERED + " · … · " + _S36_NOT[0] + " · " + _S36_NOT[1]) in after, path
        assert "That was true until the Owner authorized the Stage 36 closure.)*" in after, path
        # ADVANCED at the Stage 35 closure: the Stage-35 active-increment routing is preserved history
        assert ("*(Superseded 2026-10-05 by " + _S35C_NAME + ", preserved so the change is visible rather than silent: "
                "the current routing read \"**ACTIVE BOUNDED PRODUCT INCREMENT — " + _S35_NAME + " (Owner-authorized "
                "2026-10-05); Stage 35 ENTERED / PARTIAL — first bounded slice only, first bounded slice DELIVERED, "
                "Stage 35 NOT complete, NOT closed; …:** " + _S35_ACTIVE + " · " + _S35_ENTERED) in after, path
        assert "That was true until the Owner authorized the Stage 35 closure.)*" in after, path
        # ADVANCED at the delivery of the first bounded slice: the pre-merge Stage-35 routing is preserved history
        assert ("*(Superseded 2026-10-05 by the delivery of the Stage 35 first bounded slice, preserved so the change is "
                "visible rather than silent: the current routing read \"**ACTIVE BOUNDED PRODUCT INCREMENT — " + _S35_NAME
                + " (Owner-authorized 2026-10-05); Stage 35 ENTERED / PARTIAL — first bounded slice only, NOT delivered, "
                "NOT complete, NOT closed; …:** … `STAGE 35 MERGE AUTHORIZATION: NO` · `STAGE 35 FIRST BOUNDED SLICE: NOT "
                "DELIVERED` · …\"") in after, path
        # ROTATED at the Stage 35 first bounded slice: the post-Stage-24-closure NONE routing is preserved history
        assert ("*(Superseded 2026-10-05 by " + _S35_NAME + ", preserved so the change is visible rather than silent: "
                "the current routing read \"**NO ACTIVE CONTRACT — post-Stage-24-closure (2026-10-04); Stage 24 "
                "COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only; … Stage 25 NOT "
                "ENTERED — navigation only:** `ACTIVE CONTRACT: NONE` · `NEXT PRODUCT INCREMENT: NOT AUTHORIZED` · "
                "`NEXT STEP: LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT` · …\"") in after, path
        assert ("That was true until the Owner authorized the Stage 35 first bounded slice.)*") in after, path
        assert ("*(Superseded 2026-10-04 by Stage 24 — CAP-12 Form Mock-up Advisory — Closure, preserved so the change "
                "is visible rather than silent: the current routing read \"**NO ACTIVE CONTRACT — "
                "post-Stage-24-CAP-12-Slice-1 (2026-10-03);") in after, path
        assert ("*(Superseded 2026-10-02 by Stage 23 — CAP-06 Four-Axis Readiness Snapshot — Closure, preserved so the "
                "change is visible rather than silent: the current routing read \"**NO ACTIVE CONTRACT — "
                "post-Stage-28-closure (2026-10-02);") in after, path
        assert ("*(Superseded 2026-10-01 by Stage 22 — Decision Trace + Decision Room — Closure, preserved so the change "
                "is visible rather than silent: the current routing read \"**NO ACTIVE CONTRACT — post-Stage-21-closure "
                "(2026-10-01); Stage 21 COMPLETE for the current Owner-declared contradiction scope; Stage 20 COMPLETE for "
                "the current Owner-declared assumption scope; Stage 19 COMPLETE for the current planning-only scope; Stage "
                "18 COMPLETE for the current Mechanical + Electrical / Electronics scope; Stage 15 COMPLETE for the current "
                "Mechanical + Electrical / Electronics scope; Stage 22 ENTERED / PARTIAL — navigation only:**") in after, path
        assert ("*(Superseded 2026-10-01 by Stage 21 — Owner-Declared Contradiction Visibility — Closure, preserved so "
                "the change is visible rather than silent: the current routing read \"**NO ACTIVE CONTRACT — "
                "post-Stage-20-closure (2026-10-01); Stage 20 COMPLETE for the current Owner-declared assumption scope; "
                "Stage 19 COMPLETE for the current planning-only scope; Stage 18 COMPLETE for the current Mechanical + "
                "Electrical / Electronics scope; Stage 15 COMPLETE for the current Mechanical + Electrical / Electronics "
                "scope; Stage 21 ENTERED / PARTIAL — navigation only:**") in after, path
        assert ("*(Superseded 2026-10-01 by Stage 20 — Assumption Revision & Replacement — Closure, preserved so the "
                "change is visible rather than silent: the current routing read \"**NO ACTIVE CONTRACT — "
                "post-Stage-19-closure (2026-10-01); Stage 19 COMPLETE for the current planning-only scope; Stage 18 "
                "COMPLETE for the current Mechanical + Electrical / Electronics scope; Stage 15 COMPLETE for the current "
                "Mechanical + Electrical / Electronics scope; Stage 20 ENTERED / PARTIAL — navigation only:**") in after, path
        assert ("*(Superseded 2026-10-01 by Stage 19 — Experiment Execution-State Disclosure — Closure, preserved so "
                "the change is visible rather than silent: the current routing read \"**NO ACTIVE CONTRACT — "
                "post-Stage-18-closure (2026-10-01); Stage 18 COMPLETE for the current Mechanical + Electrical / "
                "Electronics scope; Stage 15 COMPLETE for the current Mechanical + Electrical / Electronics scope; Stage "
                "19 ENTERED / NOT COMPLETE — navigation only:**") in after, path
        assert ("*(Superseded 2026-10-01 by Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure, preserved so "
                "the change is visible rather than silent: the current routing read \"**NO ACTIVE CONTRACT — "
                "post-Stage-15-closure (2026-10-01); Stage 15 COMPLETE for the current Mechanical + Electrical / "
                "Electronics scope; Stage 18 stays ENTERED / PARTIAL / NOT COMPLETE:**") in after, path
        assert ("*(Superseded 2026-10-01 by Stage 15 — Integration Evidence & IRL-Compatible View — Closure, "
                "preserved so the change is visible rather than silent: the current routing read \"**NO ACTIVE "
                "CONTRACT — post-Stage-15-Slice-4 (2026-09-30); Stage 15 and Stage 18 both stay ENTERED / PARTIAL / "
                "NOT COMPLETE:** …\"") in after, path
        note = _current(path, "stage-18-semantic-normalization")
        assert ("**STAGE-18 CLOSURE RECONCILIATION (2026-10-01) — `MSNL: FUTURE / DEFERRED / NOT ACTIVATED`.**"
                in note), path
        for needle in ("MSNL was NOT a Stage-18 completion blocker",
                       "Stage 18 completion neither implements it nor attaches it to a new Stage",
                       "any activation still needs its own Owner authorization and data boundary"):
            assert needle in note, (path, needle)
    state = _current(STATE, "current-position")
    # ROTATED at the Stage 35 first bounded slice: the current position named the active Stage-35 increment
    # ROTATED at the Stage 35 closure: the current position is NONE again, post-Stage-35-closure
    # ADVANCED at the Stage 36 closure: the current position is post-Stage-36-closure; the Stage 35 closure follows it
    # ADVANCED at the Stage 16 closure: the current position is post-Stage-16-closure; the delivered Stage 16 residual and
    # the Stage 36 closure follow it
    # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: the current position is
    # post-Stage-25-CAP-13-Slice-1; the Stage 16 closure follows it ("before it")
    # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: the current position is
    # post-Stage-27-THERM-01-Slice-1; the Stage 25 slice follows it ("before it")
    # ROTATED at the Stage 27 closure: the current position is post-Stage-27-closure; the Stage 27 slice follows it
    assert re.match(r" \*\*Current position \([^)]{0,40}\): `ACTIVE CONTRACT: NONE` — no product increment is "
                    r"currently authorized \(post-Stage-27-closure; " + re.escape(_S27C_NAME) + r" — delivered with no "
                    r"product change required: Stage 27 is COMPLETE for the current bounded THERM-01 single-path "
                    r"temperature-difference scope only, checkbox ticked for that scope only — ", state)
    assert re.search(r"; before it, " + re.escape(_S27_NAME) + r" — delivered: it entered Stage 27 as ENTERED / PARTIAL "
                     r"for that slice only until the Stage 27 closure — ", state)
    assert re.search(r"; full THERM-01 NOT AUTHORIZED; before it, " + re.escape(_S25_NAME) + r" — delivered: "
                     r"Stage 25 is ENTERED / PARTIAL for that slice only, checkbox unticked, NOT complete — ", state)
    assert re.search(r"; full CAP-13 NOT AUTHORIZED; before it, " + re.escape(_S16C_NAME) + r" — delivered with no "
                    r"further product change required: Stage 16 is COMPLETE for the current bounded Technical \+ "
                    r"Integration evidence-sufficiency composition scope only, checkbox ticked for that scope only", state)
    for needle in ("Stage 13 and Stage 14 stay PARTIAL / DEFERRED; no Stage-16 SRL engine and no level-based SRL work is "
                   "authorized; " + _S16_NAME + " — delivered (PR #N): ONE Owner-authorized bounded presentation-only "
                   "residual",
                   "no engine, owner, composer, persistence, schema, score or SRL level; " + _S36C_NAME + " — delivered "
                   "with no product change required: Stage 36 is COMPLETE for the current no-live-AI / provider scope "
                   "only, checkbox ticked for that scope only"):
        assert re.search(_any_pr(needle), state), needle
    # ADVANCED at Stage 28 Qualification Slices 1 and 2: the current position is post-Slice-2; the Stage-22 facts follow
    # it (split around the owner name so these governance needles never read as control-loop idea text)
    # ADVANCED at Stage 28 Optional Part Slice 1: the current position is post-Optional-Part-Slice-1
    # ADVANCED at Stage 28 Optional Part Slice 2: the current position is post-Optional-Part-Slice-2
    # ADVANCED at Stage 30 Part Safeguards Slice 1: the current position is post-Stage-30-Slice-1
    # ADVANCED at the Stage 30 closure: the current position is post-Stage-30-closure, Slice 1 follows it
    # ADVANCED at the Stage 28 part-only enablement: the current position is post-enablement, the closure follows it
    # ADVANCED at the Stage 28 closure: the current position is post-Stage-28-closure, the enablement follows it
    # ADVANCED at the Stage 23 closure: the current position is post-Stage-23-closure, the Stage 28 closure follows it
    # ADVANCED at the delivered CAP-12 Form Mock-up Advisory Slice 1: the current position is post-Slice-1, the
    # Stage 23 closure follows it
    # ADVANCED at the Stage 24 closure: the current position is post-Stage-24-closure, Slice 1 follows it
    # ROTATED at the Stage 35 first bounded slice: the Stage-24-closure state was the one the Stage-35 increment
    # succeeded
    # ROTATED at the Stage 35 closure: the Stage 35 closure and the delivered first bounded slice lead; the Stage 24
    # closure follows them
    for needle in ("; " + _S35C_NAME + " — delivered with no product change required: Stage 35 is COMPLETE for the "
                   "current bounded first-slice scope only, checkbox ticked for that scope only",
                   "Stage 37 stays NOT ENTERED and NOT AUTHORIZED; " + _S35C_NAME + " — delivered",
                   "Stage 35 — Structured Invention Disclosure Export — First Bounded Product Slice — delivered: it "
                   "entered Stage 35 as ENTERED / PARTIAL for that slice only until the Stage 35 closure — for ONE "
                   "authenticated owner and ONE owned project",
                   "the legal-adviser review of the disclaimer wording before any user release and the release triggers "
                   "stay preserved; Stage 36 was then NOT ENTERED and NOT AUTHORIZED",      # ROTATED at Stage 36
                   "no retained export artifact; Stage 24 — CAP-12 Form Mock-up Advisory — "
                   "Closure — delivered with no "
                   "product change required: Stage 24 is COMPLETE for the current bounded CAP-12 Form Mock-up Advisory "
                   "Slice 1 scope only, checkbox ticked for that scope only",
                   "Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1 — delivered: it entered Stage 24 as ENTERED / "
                   "PARTIAL for that slice only until the Stage 24 closure",
                   "full CAP-12 stays NOT AUTHORIZED; at its delivery CAP-13 was not activated and Stage 25 not "
                   "authorized; Stage 23 — "
                   "CAP-06 Four-Axis Readiness Snapshot — Closure — delivered with "
                   "no product change required: Stage 23 is COMPLETE for the current bounded four-axis Readiness "
                   "Snapshot scope only, checkbox ticked for that scope only",
                   "full CAP-06 stays NOT AUTHORIZED and its eight-axis expansion is not implemented or closed; "
                   "Stage 28 — " + _CL.title() + " Optional Part — Closure — delivered with no further product "
                   "change",
                   "Part-Enablement Safeguards — Closure — delivered with no further product change: Stage 30 is "
                   "COMPLETE for the current ",
                   "Part-Enablement Safeguards — Bounded Slice 1 — delivered: saved ",
                   "Optional Part — Slice 2 — delivered: the dormant part-scoped governed question service",
                   "Optional Part — Slice 1 — delivered: the dormant optional-part foundation",
                   "was then NOT part-enabled and is NOT root-activated; Stage 28 — Bounded ",
                   "Concept Owner — Qualification Slice 2 — delivered: one documents-only qualification record",
                   "pack P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS for its bounded concept-level scope only, NOT activated",
                   "Qualification Slice 1 — delivered under the Owner-accepted Stage-28 qualification contract: one "
                   "standalone ",
                   "owner qualified, NOT root-activated;",
                   "Stage 22 — CAP-05 decision trace + CAP-07 decision room — is COMPLETE for "
                   "the current bounded decision trace + decision room scope only, checkbox ticked for that scope only; "
                   "this does NOT mean the roadmap, Stage 23 or any other Stage is complete or entered or that a next "
                   "slice is authorized (full CAP-05 / full CAP-07 stay NOT AUTHORIZED), and it claims no "
                   "recommendation, winner, confidence, evidence-strength or readiness scoring, inferred decision ↔ "
                   "context linkage or new decision lifecycle)",
                   "Stage 22 — Decision Trace + Decision Room — Closure — delivered with no product change required",
                   "Stage 21 — CAP-10 contradiction detector — stays COMPLETE for the current Owner-declared "
                   "contradiction scope only (full CAP-10 NOT AUTHORIZED)",
                   "Stage 21 — Owner-Declared Contradiction Visibility — Closure — delivered",
                   "Stage 20 — CAP-08 assumption register — stays COMPLETE for the current Owner-declared assumption "
                   "scope only (full CAP-08 NOT AUTHORIZED)",
                   "Stage 20 — Assumption Revision & Replacement — Closure — delivered",
                   "Stage 19 — WS-PFV-001 / CAP-09 — stays COMPLETE for the current planning-only scope only "
                   "(Experiment Execution-State Disclosure — Closure — delivered; full CAP-09 / full WS-PFV-001 stay NOT "
                   "AUTHORIZED)",
                   # ROTATED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED /
                   # PARTIAL through that slice only
                   "MASTER ROADMAP SEQUENTIAL MARKER: STAGE 25 — ENTERED / PARTIAL — NAVIGATION ONLY (NO STAGE-25 "
                   "IMPLEMENTATION AUTHORIZED BY STAGE-24 CLOSURE stays true history; Stage 25 / CAP-13 was entered only "
                   "by the separately Owner-authorized, delivered CAP-13 Two-Support Static Reactions Slice 1; full CAP-13 "
                   "NOT AUTHORIZED; Stage 24 / CAP-12 was entered only by the separately Owner-authorized, delivered Form "
                   "Mock-up Advisory Slice 1 and completed for that bounded scope only by the Stage 24 closure; full "
                   # ROTATED at the Stage 16 closure: Stage 16 is no longer routed past
                   "CAP-12 NOT AUTHORIZED; routing past Stages 11, 13, 14 and 17 completes none of them)",
                   "next step: a LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT — read-only planning / selection "
                   # ADVANCED at the Stage 16 closure: no further Stage-16 / SRL work is authorized either
                   # ADVANCED at the delivered Stage 25 / CAP-13 slice: no further Stage-25 / CAP-13 work either
                   # ADVANCED at the delivered Stage 27 / THERM-01 slice: no further Stage-27 / THERM-01 work either
                   "until the Owner separately authorizes another product increment (no further Stage-27 / THERM-01 "
                   "slice, method, consumer or unit conversion, no full THERM-01, no further Stage-25 / CAP-13 "
                   "method, consumer or unit conversion, no full CAP-13, no further Stage-16 / SRL work, "
                   "no later Stage-35 slice, no CAP-15 / CAP-17 implementation, no Stage-37 work and no further "
                   "Stage-24 / CAP-12 slice is authorized)",
                   "Stage 18 — D13 / CAP-01 — stays COMPLETE for the current Mechanical + Electrical / Electronics "
                   "scope only (Gap-Scoped Technical Next-Step Guidance — Closure — delivered; MSNL stays FUTURE / "
                   "DEFERRED / NOT ACTIVATED",
                   "Stage 15 — entered through Slice 1, ",
                   "stays COMPLETE for the current Mechanical + Electrical / Electronics scope only",
                   "Stage 15 — Integration Evidence & IRL-Compatible View — Closure — delivered",
                   "Stage 15 — Interface Verification Observation Event — Slice 4 — delivered",
                   "CAP-09 Result Event Slice 1 — delivered",
                   "Stage 15 — Interface Verification Preparation Metadata — Slice 3 — delivered",
                   "Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2 — delivered",
                   "it establishes no compatibility, IRL level or readiness",
                   "Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1 — delivered",
                   "Stage 15 is COMPLETE for the current Mechanical + Electrical / Electronics scope, checkbox ticked "
                   "for that scope only",
                   "another Stage-15 slice, validated IRL, IRL scoring / levels",
                   "Phase-7 integration residuals remain Phase 7",
                   "Stage 18 is now **COMPLETE for the current Mechanical + Electrical / Electronics scope**"):
        assert needle in state, needle
    after = _after_fence(STATE, "current-position")
    # ADVANCED at the Stage 16 closure: the post-Stage-36-closure NONE position is preserved history
    assert ("*(Superseded 2026-10-06 by " + _S16C_NAME + ", preserved so the change is visible rather than silent: the "
            "current-position entry read \"`ACTIVE CONTRACT: NONE` — no product increment is currently authorized "
            "(post-Stage-36-closure; " + _S36C_NAME + " — delivered with no product change required: …)\" with \"… "
            "routing past Stages 11, 13, 14, 16 and 17 completes none of them …\" and Stage 16 then unticked.") in after
    assert re.search(_any_pr("That was true until the Owner authorized the Stage 16 bounded presentation residual "
                             "(delivered by PR #N) and the Stage 16 closure.)*"), after)
    # ADVANCED at the Stage 36 closure: the post-Stage-35-closure NONE position is preserved history
    assert ("*(Superseded 2026-10-05 by " + _S36C_NAME + ", preserved so the change is visible rather than silent: the "
            "current-position entry read \"`ACTIVE CONTRACT: NONE` — no product increment is currently authorized "
            "(post-Stage-35-closure; " + _S35C_NAME + " — delivered with no product change required: …; Stage 36 stays NOT "
            "ENTERED and NOT AUTHORIZED; …)\"") in after
    assert "That was true until the Owner authorized the Stage 36 closure.)*" in after
    # ADVANCED at the Stage 35 closure: the Stage-35 active-increment position is preserved history
    assert ("*(Superseded 2026-10-05 by " + _S35C_NAME + ", preserved so the change is visible rather than silent: the "
            "current-position entry read \"" + _S35_ACTIVE + " — ONE Owner-authorized bounded product increment is "
            "active: " + _S35_NAME + " (Stage 35 is ENTERED / PARTIAL for this first bounded slice ONLY: …") in after
    assert "That was true until the Owner authorized the Stage 35 closure.)*" in after
    # ADVANCED at the delivery of the first bounded slice: the pre-merge Stage-35 position is preserved history
    assert ("*(Superseded 2026-10-05 by the delivery of the Stage 35 first bounded slice, preserved so the change is "
            "visible rather than silent: the current-position entry read \"… the first bounded implementation EXISTS (PR "
            "#") in after
    assert ("merge authorization NO; NOT delivered, NOT complete and NOT closed; …\" and its tokens included "
            "\"`STAGE 35 MERGE AUTHORIZATION: NO` · `STAGE 35 FIRST BOUNDED SLICE: NOT DELIVERED`\".") in after
    # ROTATED at the Stage 35 first bounded slice: the post-Stage-24-closure NONE position is preserved history
    assert ("*(Superseded 2026-10-05 by " + _S35_NAME + ", preserved so the change is visible rather than silent: the "
            "current-position entry read \"`ACTIVE CONTRACT: NONE` — no product increment is currently authorized "
            "(post-Stage-24-closure; Stage 24 — CAP-12 Form Mock-up Advisory — Closure — delivered with no product "
            "change required …)\"") in after
    assert ("*(Superseded 2026-10-04 by Stage 24 — CAP-12 Form Mock-up Advisory — Closure, preserved so the change is "
            "visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no product "
            "increment is currently authorized (post-Stage-24-CAP-12-Slice-1; Stage 24 — CAP-12 Form Mock-up Advisory "
            "— Slice 1 — delivered: Stage 24 is ENTERED / PARTIAL for that slice only, checkbox unticked, NOT complete "
            "…)\"") in after
    assert ("*(Superseded 2026-10-03 by Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1, preserved so the change is "
            "visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no product "
            "increment is currently authorized (post-Stage-23-closure; …)\"") in after
    assert ("*(Superseded 2026-10-02 by Stage 23 — CAP-06 Four-Axis Readiness Snapshot — Closure, preserved so the "
            "change is visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no "
            "product increment is currently authorized (post-Stage-28-closure …)\"") in after
    assert ("*(Superseded 2026-10-01 by Stage 22 — Decision Trace + Decision Room — Closure, preserved so the change is "
            "visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no product "
            "increment is currently authorized (post-Stage-21-closure …)\"") in after
    assert ("*(Superseded 2026-10-01 by Stage 21 — Owner-Declared Contradiction Visibility — Closure, preserved so the "
            "change is visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no "
            "product increment is currently authorized (post-Stage-20-closure …)\"") in after
    assert ("*(Superseded 2026-10-01 by Stage 20 — Assumption Revision & Replacement — Closure, preserved so the "
            "change is visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no "
            "product increment is currently authorized (post-Stage-19-closure …)\"") in after
    assert ("*(Superseded 2026-10-01 by Stage 19 — Experiment Execution-State Disclosure — Closure, preserved so the "
            "change is visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no "
            "product increment is currently authorized (post-Stage-18-closure …)\"") in after
    assert ("*(Superseded 2026-10-01 by Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure, preserved so the "
            "change is visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — no "
            "product increment is currently authorized (post-Stage-15-closure …)\"") in after
    assert ("*(Superseded 2026-10-01 by Stage 15 — Integration Evidence & IRL-Compatible View — Closure, preserved "
            "so the change is visible rather than silent: the current-position entry read \"`ACTIVE CONTRACT: NONE` — "
            "no product increment is currently authorized (post-Stage-15-Slice-4 …)\"") in after
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    # ADVANCED at the Stage 30 closure: the Stage 30 closure is now the last one; Stage 22's is the preceding one
    # ADVANCED at the Stage 28 closure: the Stage 28 closure is now the last one; Stage 30's precedes it
    # ADVANCED at the Stage 23 closure: the Stage 23 closure is now the last one; Stage 28's precedes it
    # ADVANCED at the delivered CAP-12 Form Mock-up Advisory Slice 1: that slice is the last increment; the Stage 23
    # closure precedes it
    # ADVANCED at the Stage 24 closure: the Stage 24 closure is the last one; the Slice 1 increment precedes it
    # ROTATED at the Stage 35 first bounded slice: the head opened with the live Stage-35 declaration
    # ROTATED at the Stage 35 closure: the head opens with the live NONE, the Stage 35 closure as the last bounded
    # closure, the delivered first bounded slice as the preceding increment and the Stage 24 closure before it
    # ADVANCED at the Stage 36 closure: the Stage 36 closure is the last bounded closure; the Stage 35 closure, the
    # delivered first bounded slice and the Stage 24 closure precede it
    # ADVANCED at the Stage 16 closure: the Stage 16 closure is the last bounded closure; the delivered Stage 16 residual,
    # the Stage 36 closure, the Stage 35 closure and the earlier closures precede it
    # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: that slice is the last bounded
    # increment, recorded in its after-merge form; the Stage 16 closure precedes it
    # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: that slice is the last
    # bounded increment, recorded in its after-merge form; the Stage 25 slice precedes it
    # ROTATED at the Stage 27 closure: the Stage 27 closure is the last bounded closure; the Stage 27 slice precedes it
    assert head.startswith("## Current authority " + _NONE_BOLD + " NO PRODUCT INCREMENT IS CURRENTLY AUTHORIZED. The "
                           "last Owner-authorized bounded closure — " + _S27C_NAME + " — is DELIVERED with no product "
                           "change required, completing Stage 27 for the current bounded THERM-01 single-path "
                           "temperature-difference scope ONLY (" + "; ".join((_S27C_DELIVERED, _S27_COMPLETE, _S27_FULL_NO,
                                                                               _S25_MARKER))
                           + "; Git / GitHub own its PR, merge and review identity)")
    assert ("The preceding bounded increment — " + _S27_NAME + " — is DELIVERED (" + _S27_DELIVERED + "; Git / GitHub own "
            "its PR, merge and review identity): it entered Stage 27 as ENTERED / PARTIAL for that slice ONLY until the "
            "Stage 27 closure") in head
    assert ("The preceding bounded increment — " + _S25_NAME + " — is DELIVERED, entering Stage 25 as ENTERED / PARTIAL "
            "for that slice ONLY (" + "; ".join(_S25_FACTS) + "; Git / GitHub own its PR, merge and review identity)") in head
    assert ("The preceding bounded closure — " + _S16C_NAME + " — is DELIVERED with no further "
            "product change required, completing Stage 16 for the current bounded Technical + Integration "
            "evidence-sufficiency composition scope ONLY (" + "; ".join(_S16C_FACTS) + "; Git / GitHub own "
            "its PR, merge and review identity).") in head
    assert ("\"without hiding the weakest material axis\" is satisfied in that bounded scope by independent visible source "
            "truth and the explicit focus-scope disclosure, and no weakest axis is computed;") in head
    assert re.search(_any_pr("The preceding bounded increment — " + _S16_NAME + " — is DELIVERED (" + _S16_DELIVERED
                             + "; PR #N; Git / GitHub own its merge and review identity)"), head)
    assert ("The preceding bounded closure — " + _S36C_NAME + " — is DELIVERED with no product change required, "
            "completing Stage 36 for the current no-live-AI / provider scope ONLY") in head
    assert ("The preceding bounded closure — " + _S35C_NAME + " — is DELIVERED with no product change required, "
            "completing Stage 35 for the current bounded first-slice scope ONLY") in head
    assert re.findall(_ACTIVE_BOLD, head) == ["NONE"]
    assert ("The preceding bounded increment — " + _S35_NAME + " — is DELIVERED (" + _S35_SLICE_DELIVERED + "; governed "
            "by the merged implementation contract `docs/governance/STAGE35_DISCLOSURE_EXPORT_FIRST_SLICE_IMPLEMENTATION_"
            "CONTRACT.md`; it entered Stage 35 as ENTERED / PARTIAL for that slice ONLY until the Stage 35 closure") in head
    assert ("The preceding bounded closure — Stage 24 — CAP-12 Form Mock-up Advisory — Closure — is DELIVERED with no "
            "product change required, completing Stage 24 for the current bounded CAP-12 Form Mock-up Advisory Slice 1 "
            "scope ONLY") in head
    assert re.search(_any_pr("the only increment authorized after that closure — the Stage 35 first bounded slice (above) — is DELIVERED, "
            "and the Stage 35 closure (above) then completed Stage 35 for that bounded first-slice scope only with no "
            "product change, and the Stage 36 closure (above) then completed Stage 36 for its current no-live-AI / "
            "provider scope only with no product change; the only increment authorized after that closure — the Stage "
            "16 bounded presentation residual (above) — is DELIVERED (PR #N), and the Stage 16 closure (above) then "
            "completed Stage 16 for its current bounded Technical + Integration evidence-sufficiency composition scope "
            # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: it follows the Stage 16
            # closure in the chain
            "only with no further product change; the only increment authorized after that closure — " + _S25_NAME
            + " (above) — is DELIVERED, entering Stage 25 as ENTERED / PARTIAL for that slice only; "
            # ADVANCED at the delivered Stage 27 / THERM-01 slice: it follows the Stage 25 slice in the chain
            "the only increment authorized after it — " + _S27_NAME + " (above) — is DELIVERED, entering Stage 27 as "
            # ADVANCED at the Stage 27 closure: the closure then completed Stage 27 for its current bounded scope
            "ENTERED / PARTIAL for that slice only, and the Stage 27 closure (above) then completed Stage 27 for its "
            "current bounded THERM-01 single-path temperature-difference scope only with no product change; "
            # ADVANCED at the CAP13-THERM01-INTEGRATED-PART-01 current-truth sync: the delivered integrated-part
            # increment follows the Stage 27 closure in the chain
            "the only increment authorized after that closure — CAP13-THERM01-INTEGRATED-PART-01 (above) — is "
            # ADVANCED at ELECTRICAL-ENERGY-TIME-REFERENCE-01 (merge-effective delivery record): it follows the
            # integrated-part increment in the chain
            "DELIVERED (PR #N); the only increment authorized after it — ELECTRICAL-ENERGY-TIME-REFERENCE-01 (above) "
            # ADVANCED at COMPONENT-INVENTORY-DECLARE-LIST-01 (merge-effective delivery record): it follows the
            # energy-time reference increment in the chain
            "— is DELIVERED (PR #N); the only increment authorized after it — COMPONENT-INVENTORY-DECLARE-LIST-01 "
            # ADVANCED at 28-T1-SENSING-VALUE-THRESHOLD-01 (merge-effective delivery record): it follows the
            # component-inventory increment in the chain
            "(above) — is DELIVERED (PR #N); the only increment authorized after it — "
            "28-T1-SENSING-VALUE-THRESHOLD-01 (above) — is DELIVERED (PR #N); "
            # ADVANCED at 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 (merge-effective delivery record): it
            # follows the 28-T1 sensing reference increment in the chain
            "the only increment authorized after it — 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 (above) — is DELIVERED "
            "(PR #N); no subsequent increment has been authorized."), head)
    # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED / PARTIAL
    # ADVANCED at the delivered Stage 27 / THERM-01 slice: Stage 27 ENTERED / PARTIAL leads
    # ROTATED at the Stage 27 closure: Stage 27 COMPLETE for its current bounded scope leads
    assert ("ACTIVE CONTRACT: NONE — no product increment is authorized and no other Stage is authorized (Stage 27 is "
            "COMPLETE for its current bounded THERM-01 single-path temperature-difference scope only; Stage 25 is "
            "ENTERED / PARTIAL for its delivered CAP-13 Two-Support Static Reactions Slice 1 only; Stage 16 is "
            "COMPLETE for its current bounded Technical + Integration evidence-sufficiency composition scope only; Stage "
            "35 is COMPLETE for its current bounded first-slice scope only; Stage 36 is COMPLETE for its current "
            "no-live-AI / provider scope only; Stage 37 is NOT ENTERED)") in head
    assert ("Stage 16 closure (delivered; a current-truth closure with no further product change; completes Stage 16 for "
            "the current bounded Technical + Integration evidence-sufficiency composition scope ONLY; Stages 13 and 14 "
            "stay PARTIAL / DEFERRED; no SRL level, score or weakest-axis computation; the MASTER ROADMAP SEQUENTIAL "
            "MARKER is unchanged):") in head
    # AMENDED at the delivered Stage 27 / THERM-01 slice: Stage 27 ENTERED / PARTIAL leads the parenthetical
    # AMENDED at the Stage 27 closure: Stage 27 COMPLETE for its current bounded scope leads the parenthetical
    assert ("Stage 25 or any other Stage is complete, or that any other Stage is entered (Stage 27 is COMPLETE for its "
            "current bounded THERM-01 single-path temperature-difference scope only; Stage 25 is ENTERED / "
            "PARTIAL for its CAP-13 Two-Support Static Reactions Slice 1 only; Stage 24 is COMPLETE for its current bounded CAP-12 "
            "Form Mock-up Advisory Slice 1 scope only; Stage 35 is COMPLETE for its current bounded first-slice scope "
            "only; Stage 36 is COMPLETE for its current no-live-AI / provider scope only; Stage 16 is COMPLETE for its "
            "current bounded Technical + Integration evidence-sufficiency composition scope only)") in head
    assert ("Stage 36 closure (delivered; a current-truth closure with no product change; completes Stage 36 for the "
            "current no-live-AI / provider scope ONLY; CAP-15 / CAP-17 stay NOT AUTHORIZED FOR IMPLEMENTATION; Stage 37 "
            "stays NOT ENTERED and NOT AUTHORIZED; the MASTER ROADMAP SEQUENTIAL MARKER is unchanged):") in head
    assert ("Stage 35 closure (delivered; a current-truth closure with no product change; completes Stage 35 for the "
            "current bounded first-slice scope ONLY; later Stage-35 slices stay NOT AUTHORIZED; Stage 36 was then NOT "
            "ENTERED and NOT AUTHORIZED; the MASTER ROADMAP SEQUENTIAL MARKER is unchanged):") in head
    assert ("The preceding bounded increment — Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1 — is DELIVERED "
            "(`STAGE 24 — CAP-12 FORM MOCK-UP ADVISORY SLICE 1: DELIVERED`; it entered Stage 24 as ENTERED / PARTIAL "
            "for that slice ONLY until the Stage 24 closure") in head
    assert ("The preceding bounded closure — Stage 23 — CAP-06 Four-Axis Readiness Snapshot — Closure — is DELIVERED "
            "with no product change required") in head
    assert ("The preceding bounded closure — Stage 28 — " + _CL.title() + " Optional Part — Closure — is DELIVERED "
            "with no further product change required") in head
    assert ("The preceding bounded closure — Stage 30 — " + _CL.title() + " Part-Enablement Safeguards — Closure — "
            "is DELIVERED with no further product change required") in head
    assert ("The preceding bounded closure — Stage 22 — Decision Trace + Decision Room — Closure — is DELIVERED with "
            "no product change required") in head
    assert re.search(r"STAGE 22 — COMPLETE for the current bounded decision trace \+ decision room scope only \(`STAGE "
                     r"22: COMPLETE — CURRENT BOUNDED DECISION TRACE \+ DECISION ROOM SCOPE`; checkbox ticked for that "
                     r"scope only; delivered basis: CAP-05 \+ CAP-07 Slices 1–2, PR #\d+ and PR #\d+, only\);", head)
    for needle in ("only); STAGE 21 stays "
                   "COMPLETE for the current Owner-declared contradiction scope only (`STAGE 21: COMPLETE — "
                   "CURRENT OWNER-DECLARED CONTRADICTION SCOPE`); STAGE 20 stays "
                   "COMPLETE for the current Owner-declared assumption scope only (`STAGE 20: COMPLETE — CURRENT "
                   "OWNER-DECLARED ASSUMPTION SCOPE`); STAGE 19 stays COMPLETE for the current planning-only scope only "
                   "(`STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE`); STAGE 18 stays COMPLETE for the current "
                   "Mechanical + Electrical / Electronics scope only (`STAGE 18: COMPLETE — CURRENT MECHANICAL + "
                   "ELECTRICAL / ELECTRONICS SCOPE`).",
                   # AMENDED at the Stage 24 closure: the marker is Stage 25 (NOT ENTERED); `NO STAGE-24 …` stays history
                   # AMENDED at the delivered Stage 25 / CAP-13 slice: Stage 25 ENTERED / PARTIAL; `NO STAGE-25 …` history
                   "`MASTER ROADMAP SEQUENTIAL MARKER: STAGE 25 — ENTERED / PARTIAL — NAVIGATION ONLY`; NO STAGE-25 "
                   "IMPLEMENTATION AUTHORIZED BY STAGE-24 CLOSURE stays true history (the Stage 24 closure itself "
                   "authorized no Stage-25 work and activated no CAP-13; Stage 25 / CAP-13 was entered only by the "
                   "separately Owner-authorized, delivered " + _S25_NAME + "; " + _S25_DELIVERED + "; " + _S25_PARTIAL
                   + "; " + _S25_FULL_NO + "); `NO STAGE-24 IMPLEMENTATION "
                   "AUTHORIZED BY STAGE-23 CLOSURE` stays true history (the Stage 23 closure itself authorized no "
                   "Stage-24 work; Stage 24 / CAP-12 was entered only by the separately Owner-authorized, delivered "
                   "Form Mock-up Advisory Slice 1 and completed for that bounded scope only by the Stage 24 closure; "
                   "`STAGE 24 — CAP-12 FORM MOCK-UP ADVISORY SLICE 1: DELIVERED`; `STAGE 24: COMPLETE — CURRENT "
                   "BOUNDED CAP-12 FORM MOCK-UP ADVISORY SLICE 1 SCOPE ONLY`; `FULL CAP-12: NOT AUTHORIZED`; `FURTHER "
                   # ROTATED at the Stage 16 closure: Stage 16 is no longer routed past
                   "CAP-12 SLICES: NOT AUTHORIZED`); routing past Stages 11, 13, 14 and 17 completes none of them.",
                   _S24C_DELIVERED, _S24_COMPLETE, *_S24C_LIMITS,
                   "Stage 24 closure (delivered; a current-truth closure with no product change; completes Stage 24 for "
                   "the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope ONLY; full CAP-12 and further CAP-12 "
                   "slices stay NOT AUTHORIZED; CAP-13 stays NOT ACTIVATED; the MASTER ROADMAP SEQUENTIAL MARKER moves "
                   "to Stage 25 for navigation only)",
                   "The preceding bounded increment — Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1 — is DELIVERED.",
                   _S23C_DELIVERED, _S23_COMPLETE, *_S23_LIMITS,
                   "Stage 23 closure (delivered; a current-truth closure with no product change; completes Stage 23 "
                   "for the current bounded four-axis Readiness Snapshot scope ONLY; full CAP-06 stays NOT "
                   "AUTHORIZED; the MASTER ROADMAP SEQUENTIAL MARKER moves to Stage 24 for navigation only)",
                   "The preceding bounded closure — Stage 28 — " + _CL.title() + " Optional Part — Closure — is "
                   "DELIVERED.",
                   "`FULL CAP-05: NOT AUTHORIZED`", "`FULL CAP-07: NOT AUTHORIZED`",
                   "`STAGE 22 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`",
                   "Stage 22 closure (delivered; completes Stage 22 for the current bounded decision trace + decision "
                   "room scope with no product change, no new Master Roadmap Stage)",
                   "The preceding bounded slice — Stage 21 — Owner-Declared Contradiction Visibility — Closure — is "
                   "DELIVERED.",
                   "`FULL CAP-10: NOT AUTHORIZED`", "`AUTOMATIC / AI CONTRADICTION DETECTION: NOT AUTHORIZED`",
                   "`SYSTEM_INFERRED CONTRADICTION WRITER: NOT AUTHORIZED`",
                   "Stage 21 closure (delivered; completes Stage 21 for the current Owner-declared contradiction scope, "
                   "no new Master Roadmap Stage)",
                   "The preceding bounded slice — Stage 20 — Assumption Revision & Replacement — Closure — is "
                   "DELIVERED.",
                   "`FULL CAP-08: NOT AUTHORIZED`",
                   # ROTATED at the Stage 35 closure: the next step is the Lead-controlled reassessment again
                   "The next step is a LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT — read-only planning / selection "
                   "over live repository and product evidence until the Owner separately authorizes another product "
                   # ADVANCED at the Stage 16 closure: no further Stage-16 / SRL work is pre-authorized either
                   "increment; it pre-authorizes no further Stage-16 / SRL work, no later Stage-35 slice, no CAP-15 / "
                   "CAP-17 implementation, no live AI / provider selection, no External Engineering Tools activation, no "
                   "Stage-37 work,",
                   "Stage 20 closure (delivered; completes Stage 20 for the current Owner-declared assumption scope, no "
                   "new Master Roadmap Stage)",
                   "Revise runs no progression, replay or reconstruction.",
                   "malformed → reconstruction fails closed.",
                   "The preceding bounded slice — Stage 19 — Experiment Execution-State Disclosure — Closure — is "
                   "DELIVERED.",
                   "Stage 20 closure (delivered; completes Stage 20 for the current Owner-declared assumption scope, no "
                   "new Master Roadmap Stage)",
                   "Stage 19 closure (delivered; completes Stage 19 for the current planning-only scope, no new Master "
                   "Roadmap Stage)",
                   "The Section-11 note (English generated content in both UI locales)",
                   "The preceding bounded slice — Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure — is "
                   "DELIVERED.",
                   "Stage 18 closure (delivered; completes Stage 18 for the current Mechanical + Electrical / "
                   "Electronics scope, no new Master Roadmap Stage)",
                   "the information still missing (summarized only from the gap's own canonical questions, which with "
                   "Path-N stay the owner)",
                   "MSNL stays FUTURE / DEFERRED / NOT ACTIVATED (not a Stage-18 blocker)",
                   "Full future CAP-01 (typed parameters, calculations, specialist mapping, further domains) stays NOT "
                   "AUTHORIZED.",
                   "The preceding bounded slice — Stage 15 — Integration Evidence & IRL-Compatible View — Closure — is "
                   "DELIVERED.",
                   "Stage 15 closure (delivered; completes Stage 15 for the current Mechanical + Electrical / "
                   "Electronics scope",
                   "observations, preparation and dependencies are never converted into evidence",
                   "Phase-7 integration residuals remain Phase 7",
                   "The preceding bounded slice — Stage 15 — Interface Verification Observation Event — Slice 4 — is "
                   "DELIVERED.",
                   "Stage 15 Slice 4 (delivered; a bounded continuation inside the then-open Stage-15",
                   "InventorAI does not decide whether the acceptance criterion was met",
                   "The preceding bounded slice — Stage 19 / CAP-09 — Result Event Slice 1 — is DELIVERED",
                   "CAP-09 Result Event Slice 1 (delivered; inside Stage 19, no new Master Roadmap Stage",
                   "The preceding bounded slice — Stage 15 — Interface Verification Preparation Metadata — Slice 3",
                   "all three recorded means only that the inputs are recorded",
                   "Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2 — is DELIVERED",
                   "It verifies nothing: engineering compatibility has NOT been established.",
                   "Another Stage-15 slice, engineering compatibility analysis",
                   "deployment and release NOT AUTHORIZED",
                   "Stage 15 is now COMPLETE for the current Mechanical + Electrical / Electronics scope (checkbox "
                   "ticked for that scope only",
                   "Stage 18 — D13 / CAP-01 — is COMPLETE for the current Mechanical + Electrical / Electronics scope "
                   "(checkbox ticked for that scope only; the Stage 18 closure above), and the MASTER ROADMAP "
                   "SEQUENTIAL MARKER is now Stage 25 for navigation only (the Stage 24 closure above)",
                   "Stage 18 is COMPLETE for the current Mechanical + Electrical / Electronics scope: its two bounded "
                   "Electronics CAP-01 increments are delivered",
                   # AMENDED at the Stage 24 closure: the marker is Stage 25; Stage 24 COMPLETE for its bounded scope
                   # AMENDED at the delivered Stage 25 / CAP-13 slice: Stage 25 ENTERED / PARTIAL through it only
                   "the Master Roadmap sequential marker is Stage 25 for navigation only (NO STAGE-25 IMPLEMENTATION "
                   "AUTHORIZED BY STAGE-24 CLOSURE stays true history; Stage 25 is now ENTERED / PARTIAL through its "
                   "delivered CAP-13 Two-Support Static Reactions Slice 1 only; the Stage-23 closure's NO STAGE-24 "
                   "IMPLEMENTATION AUTHORIZED BY STAGE-23 CLOSURE stays true history); Stage 24 — CAP-12 Form Mock-up "
                   "Advisory — Slice 1 is delivered",
                   "Stage 24 — CAP-12 Form Mock-up Advisory — Closure is delivered with no product change required, and "
                   "Stage 24 is COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only",
                   "Stage 23 is COMPLETE for the current bounded four-axis Readiness Snapshot scope only (FULL CAP-06 "
                   "NOT AUTHORIZED; the eight-axis expansion is not implemented or closed)",
                   "Stage 22 is COMPLETE for the current bounded decision trace + decision room scope through its "
                   "delivered Slices 1–2 and its closure",
                   "Stage 20 is COMPLETE for the current Owner-declared assumption scope through CAP-08 Slice 1 and its "
                   "closure; Stage 21 is COMPLETE for the current Owner-declared contradiction scope through CAP-10 Slice "
                   "1 and its closure"):
        assert needle in head, needle
    for pat in (_S2_CLOSE_REVERSALS + _S15C_STALE + _S18C_STALE + _S19C_STALE + _S20C_STALE + _S21C_STALE
                + _S22C_STALE + _S23C_STALE + _S24C_STALE + _S24CL_STALE + _S35C_STALE + _S35C_REVERSALS
                + _S36C_STALE + _S36C_REVERSALS + _S16C_STALE + _S16C_REVERSALS + _S25_STALE + _S25_REVERSALS
                + _S27_STALE + _S27_REVERSALS):
        assert re.search(pat, head, re.I | re.S) is None, pat
    # ROTATED at the Stage 35 first bounded slice: the post-Stage-24-closure NONE is a named superseded declaration
    # ADVANCED at the Stage 35 closure: the Stage 35 first bounded slice and the Stage 35 closure lead the list
    # ADVANCED at the Stage 36 closure: the post-Stage-35-closure NONE and the Stage 36 closure lead it
    # ADVANCED at the Stage 16 closure: the post-Stage-36-closure NONE and the Stage 16 closure lead it
    assert "**WATCH — Stage 36 closure (non-blocking, no repair cycle).**" in claude
    assert "**WATCH — Stage 16 closure (non-blocking, no repair cycle).**" in claude
    # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: the post-Stage-16-closure NONE
    # leads the superseded declarations
    # ADVANCED at the delivered Stage 27 / THERM-01 slice: the post-Stage-25-CAP-13-Slice-1 NONE and the Stage 25 slice lead
    # ADVANCED at the Stage 27 closure: the post-Stage-27-THERM-01-Slice-1 NONE and the Stage 27 slice lead
    assert ("*(Superseded current-authority declarations — the former post-Stage-27-THERM-01-Slice-1 `ACTIVE CONTRACT: "
            "NONE`, the former " + _S27_NAME + ", the former post-Stage-25-CAP-13-Slice-1 `ACTIVE CONTRACT: "
            "NONE`, the former " + _S25_NAME + ", the former post-Stage-16-closure `ACTIVE CONTRACT: NONE`, the "
            "former post-Stage-36-closure `ACTIVE CONTRACT: NONE`, the "
            "former " + _S16C_NAME + ", the former post-Stage-35-closure `ACTIVE CONTRACT: NONE`, the "
            "former " + _S36C_NAME + ", the former " + _S35_NAME + ", the former " + _S35C_NAME
            + ", the former post-Stage-24-closure `ACTIVE CONTRACT: NONE`, the former post-Stage-24-CAP-12-Slice-1 "
            "`ACTIVE CONTRACT: NONE`") in claude
    assert "**WATCH — Stage 35 closure (non-blocking, no repair cycle).**" in claude
    assert "the former post-Stage-28-closure `ACTIVE CONTRACT: NONE`" in claude
    # ADVANCED at the Stage 24 closure: the post-Slice-1 NONE and the Stage 24 closure itself are now history
    assert "the former post-Stage-24-CAP-12-Slice-1 `ACTIVE CONTRACT: NONE`" in claude
    assert "the former Stage 24 — CAP-12 Form Mock-up Advisory — Closure" in claude
    assert "the former post-Stage-21-closure `ACTIVE CONTRACT: NONE`" in claude
    assert "the former post-Stage-20-closure `ACTIVE CONTRACT: NONE`" in claude
    assert "the former post-Stage-19-closure `ACTIVE CONTRACT: NONE`" in claude
    assert "the former post-Stage-18-closure `ACTIVE CONTRACT: NONE`" in claude
    assert "the former post-Stage-15-closure `ACTIVE CONTRACT: NONE`" in claude
    assert "the former post-Stage-15-Slice-4 `ACTIVE CONTRACT: NONE`" in claude
    cont = claude[claude.index("## Lead execution continuity"):claude.index("### Lead Operating Method")]
    for pat in (r"FIRED and evaluated at Stage 15 Slice 2",
                r"Evaluated at Stage 15 Slice 2: NO SHARED GENERIC RELATIONSHIP MODEL",
                r"Closure \(delivered; Stage 15 COMPLETE for the current Mechanical \+ Electrical / Electronics "
                r"scope; no further Stage-15 slice is authorized\)",
                r"NOT FIRED by Stage 15 Slice 3", r"FIRED and evaluated at Stage 15 Slice 4",
                r"NOT FIRED by Stage 15 Slice 4", r"Evaluated at the Stage 15 closure",
                r"NOT FIRED by the Stage 15 closure",
                r"\*\*WATCH — Stage 15 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"\*\*WATCH — Stage 18 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"\*\*WATCH — Stage 19 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"\*\*WATCH — Stage 20 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"\*\*WATCH — Stage 21 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"\*\*WATCH — Stage 22 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"\*\*WATCH — Stage 23 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"\*\*WATCH — Stage 24 closure \(non-blocking, no repair cycle\)\.\*\*",
                r"Evaluated at the Stage 20\s+closure",
                r"The Stage 18 closure \(2026-10-01\) neither used nor required MSNL: MSNL stays FUTURE / DEFERRED / "
                r"NOT ACTIVATED"):
        assert re.search(pat, cont), pat
    assert "(the current implementation candidate)" not in cont
    flat_checklist, raw_checklist = _flat(CHECKLIST), _read(CHECKLIST)
    # ADVANCED at Stage 28 Qualification Slices 1 and 2: the delivered slices now lead the delivered history
    # ADVANCED at the Stage 30 closure: the closure now leads, Stage 30 COMPLETE for its bounded scope only
    # ADVANCED at the Stage 23 closure: the Stage 23 closure now leads, Stage 23 COMPLETE for its bounded scope only
    # ADVANCED at Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1: the delivered slice now leads, Stage 24 ENTERED / PARTIAL
    # ADVANCED at the Stage 24 closure: the closure now leads, Stage 24 COMPLETE for its bounded scope only
    # ROTATED at the Stage 35 first bounded slice: the live subtask was the Stage-35 increment
    # ROTATED at the Stage 35 closure: the live subtask is NONE again; the Stage 35 closure, the delivered first bounded
    # slice, the Stage 24 closure and the earlier deliveries follow it
    # ADVANCED at the Stage 36 closure: the Stage 36 closure leads the delivered history
    # ADVANCED at the Stage 16 closure: the Stage 16 closure and the delivered Stage 16 residual lead the delivered history
    # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: the slice leads the subtask;
    # Stage 25 ENTERED / PARTIAL for it only; the Stage 16 closure follows
    # ADVANCED at the delivered Stage 27 / THERM-01 slice: the slice leads the subtask; the Stage 25 slice follows
    # ROTATED at the Stage 27 closure: the closure leads the subtask; the Stage 27 slice follows
    subtask_head = (r"\*\*CURRENT SUBTASK:\*\* NONE \(post-Stage-27-closure\) — NO PRODUCT INCREMENT IS "
                    r"CURRENTLY AUTHORIZED — " + re.escape(_S27C_NAME) + r" DELIVERED \([^)]*\) — STAGE 27 COMPLETE for "
                    r"the current bounded THERM-01 single-path temperature-difference scope only — "
                    + re.escape(_S27_NAME) + r" DELIVERED \([^)]*\) — Stage 27 was ENTERED / "
                    r"PARTIAL for that slice only until the Stage 27 closure — "
                    + re.escape(_S25_NAME) + r" DELIVERED \([^)]*\) — STAGE 25 ENTERED / "
                    r"PARTIAL for that slice only, checkbox UNTICKED, NOT complete; full CAP-13 NOT AUTHORIZED — "
                    + re.escape(_S16C_NAME) + r" DELIVERED \(no further product change required; "
                    r"closure gap NONE after PR #\d+; no SRL level, score or weakest-axis computation; Stages 13 and 14 "
                    r"stay PARTIAL / DEFERRED\) — STAGE 16 COMPLETE for the current bounded Technical \+ Integration "
                    r"evidence-sufficiency composition scope only — " + re.escape(_S16_NAME) + r" DELIVERED \(PR #\d+; "
                    r"[^)]*\) — " + re.escape(_S36C_NAME) + r" DELIVERED \([^)]*\) — STAGE 36 COMPLETE for the "
                    r"current no-live-AI / provider scope only — " + re.escape(_S35C_NAME) + r" DELIVERED \([^)]*\) — "
                    r"STAGE 35 COMPLETE for the "
                    r"current bounded first-slice scope only — " + re.escape(_S35_NAME) + r" DELIVERED \([^)]*\) — "
                    r"Stage 35 was ENTERED / PARTIAL for that slice only until the Stage 35 closure — "
                    r"Stage 24 — CAP-12 Form Mock-up Advisory — Closure DELIVERED \([^)]*\) — STAGE 24 COMPLETE for the "
                    r"current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only — "
                    r"Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1 DELIVERED \([^)]*\) — STAGE 24 was ENTERED / "
                    r"PARTIAL for that slice only until the Stage 24 closure — "
                    r"Stage 23 — CAP-06 Four-Axis Readiness Snapshot — Closure DELIVERED \([^)]*\) — STAGE 23 "
                    r"COMPLETE for the current bounded four-axis Readiness Snapshot scope only — "
                    r"Stage 28 — " + _CL.title() + r" Optional Part — Closure DELIVERED \([^)]*\) — STAGE 28 COMPLETE for "
                    r"the current bounded " + _CL.lower() + r" optional-part scope only — "
                    r"Stage 28 — " + _CL.title() + r" Optional Part — Part-Only Enablement DELIVERED \([^)]*\) — "
                    r"Stage 30 — " + _CL.title() + r" Part-Enablement Safeguards — Closure DELIVERED \([^)]*\) — "
                    r"STAGE 30 COMPLETE for the current " + _CL.lower() + r" part-enablement safeguard scope only — "
                    r"Stage 30 — Control-Loop Part-Enablement Safeguards — Bounded Slice 1 DELIVERED \([^)]*\) — "
                    r"Stage 28 — Control-Loop Optional Part — Slice 2 DELIVERED \([^)]*\) — "
                    r"Stage 28 — Control-Loop Optional Part — Slice 1 DELIVERED \([^)]*\) — "
                    r"Stage 28 — Bounded Control-Loop Concept Owner — Qualification Slice 2 DELIVERED \([^)]*\) — "
                    r"Stage 28 — Bounded Control-Loop Concept Owner — Qualification Slice 1 DELIVERED \([^)]*\) — "
                    r"Stage 22 — Decision Trace \+ Decision Room — Closure DELIVERED \(no product change required\) — "
                    r"STAGE 22 COMPLETE for the current bounded decision trace \+ decision room scope — "
                    r"Stage 21 — Owner-Declared Contradiction Visibility — Closure DELIVERED — STAGE 21 COMPLETE for "
                    r"the current Owner-declared contradiction scope — "
                    r"Stage 20 — Assumption Revision & Replacement — Closure DELIVERED — STAGE 20 COMPLETE for the "
                    r"current Owner-declared assumption scope — "
                    r"Stage 19 — Experiment Execution-State Disclosure — Closure DELIVERED — STAGE 19 COMPLETE for the "
                    r"current planning-only scope — "
                    r"Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure DELIVERED — STAGE 18 COMPLETE for the "
                    r"current Mechanical \+ Electrical / Electronics scope — "
                    r"Stage 15 — Integration Evidence & IRL-Compatible View — Closure DELIVERED — STAGE 15 COMPLETE "
                    r"for the current Mechanical \+ Electrical / Electronics scope — "
                    r"Stage 15 — Interface Verification Observation Event — Slice 4 DELIVERED — "
                    r"CAP-09 Result Event Slice 1 DELIVERED — Stage 15 — Interface Verification Preparation "
                    r"Metadata — Slice 3 DELIVERED — Stage 15 — "
                    r"Subsystem Interface Declaration & Verification Preparation — Slice 2 DELIVERED")
    [found] = [m.start() for m in re.finditer(subtask_head, flat_checklist)]
    subtask = flat_checklist[found:]
    subtask = subtask[:subtask.index("*(Superseded")]
    _needs(subtask, CHECKLIST, "live subtask", _tok(_NONE718), _tok(_NEXT_INC_NO), _tok(_NEXT_STAGE_STEP),
           *(_tok(t) for t in _S35C_FACTS), *(_tok(t) for t in _S36C_FACTS), *(_tok(t) for t in _S16C_FACTS), _tok(_S23C_DELIVERED), _tok(_S23_COMPLETE), *(_tok(t) for t in _S23_LIMITS),
           _tok(_S25_MARKER), _tok(_NO_S25), _tok(_S24C_DELIVERED), _tok(_S24_COMPLETE), _tok(_S24_DELIVERED),
           *(_tok(t) for t in _S24C_LIMITS),
           _tok(_S22C_DELIVERED), _tok(_S22_COMPLETE),
           *(_tok(t) for t in _S22_LIMITS),
           _status(_S21C_DELIVERED), _tok(_S21_COMPLETE),
           _status(_S20C_DELIVERED), _tok(_S20_COMPLETE),
           _status(_S19C_DELIVERED), _tok(_S19_COMPLETE),
           _status(_S18C_DELIVERED), _tok(_S18_COMPLETE), _tok(_MSNL_FUTURE),
           _status(_S15C_DELIVERED), _status(_S4_DELIVERED), _status(_R1_DELIVERED), _status(_S3_DELIVERED),
           _status(_S2_DELIVERED), _status(_S15_DELIVERED), _tok(_S15_COMPLETE),
           *(_tok(t) for t in _S15C_NOT + _S2_NOT),
           # ROTATED at the Stage 35 closure: no product increment is authorized after the Stage 35 closure
           # ADVANCED at the Stage 36 closure: ... after the Stage 36 closure; the Stage 35 closure precedes it
           # ADVANCED at the Stage 16 closure: ... after the Stage 16 closure; the delivered residual and Stage 36 precede it
           # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: ... after that slice; the
           # Stage 16 closure precedes it
           # ADVANCED at the delivered Stage 27 / THERM-01 slice: ... after that slice; the Stage 25 slice precedes it
           # ROTATED at the Stage 27 closure: ... after the Stage 27 closure; the slice precedes it
           # ADVANCED at the CAP13-THERM01-INTEGRATED-PART-01 current-truth sync: ... after that delivered increment;
           # the Stage 27 closure precedes it
           # ADVANCED at ELECTRICAL-ENERGY-TIME-REFERENCE-01 (merge-effective delivery record): ... after it; the
           # integrated-part increment precedes it
           # ADVANCED at COMPONENT-INVENTORY-DECLARE-LIST-01 (merge-effective delivery record): ... after it; the
           # energy-time reference increment precedes it
           # ADVANCED at 28-T1-SENSING-VALUE-THRESHOLD-01 (merge-effective delivery record): ... after it; the
           # component-inventory increment precedes it
           # ADVANCED at 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 (merge-effective delivery record): ... after it;
           # the 28-T1 sensing reference increment precedes it
           r"No product increment is authorized after 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01 \(delivered; PR #\d+; "
           r"[^)]*non-focused required part questions with part-local safety signals; recording only; no Stage "
           r"change; effective only on merge\) or after the preceding 28-T1-SENSING-VALUE-THRESHOLD-01 "
           r"\(delivered; PR #\d+; "
           r"[^)]*value versus above-threshold indication; explanation only[^)]*no Stage change; effective only on "
           r"merge\) or after the preceding COMPONENT-INVENTORY-DECLARE-LIST-01 \(delivered; PR #\d+; "
           r"[^)]*one record per component, parts referenced; declared only, not validated; no Stage change; effective "
           r"only on merge\) or after the preceding ELECTRICAL-ENERGY-TIME-REFERENCE-01 \(delivered; PR #\d+; "
           r"[^)]*constant P only; reference only; no Stage change; effective only on merge\) or after the preceding "
           r"CAP13-THERM01-INTEGRATED-PART-01 \(delivered; PR #\d+; [^)]*"
           r"eligibility to offer only; methods and semantics unchanged; no Stage change\) or after the preceding "
           + re.escape(_S27C_NAME) + r" \(delivered; Stage 27 COMPLETE for "
           r"the current bounded THERM-01 single-path temperature-difference scope only with no product change; full "
           r"THERM-01 NOT AUTHORIZED\) or after the preceding "
           + re.escape(_S27_NAME) + r" \(delivered; [^)]*; it entered Stage 27 as ENTERED "
           r"/ PARTIAL until the Stage 27 closure; full THERM-01 NOT AUTHORIZED\) or after the preceding "
           + re.escape(_S25_NAME) + r" \(delivered; [^)]*; Stage 25 ENTERED "
           r"/ PARTIAL through it only, NOT complete; full CAP-13 NOT AUTHORIZED\) or after the preceding "
           + re.escape(_S16C_NAME) + r" \(delivered; Stage 16 COMPLETE for "
           r"the current bounded Technical \+ Integration evidence-sufficiency composition scope only with no further "
           r"product change; no SRL level, score or weakest-axis computation; Stages 13 and 14 PARTIAL / DEFERRED\) or "
           r"after the preceding " + re.escape(_S16_NAME) + r" \(delivered; PR #\d+; one conditional Technical-row "
           r"focus-scope line on integrated inventions; no engine, owner, persistence, score or SRL level\) or after the "
           r"preceding " + re.escape(_S36C_NAME) + r" \(delivered; Stage 36 COMPLETE "
           r"for the current no-live-AI / provider scope only with no product change; no production live AI / provider "
           r"selected or active;",
           r"Stage 36 then NOT ENTERED / NOT AUTHORIZED\) or after the preceding " + re.escape(_S35_NAME),
           r"or after the preceding " + re.escape(_S35C_NAME) + r" \(delivered; Stage 35 COMPLETE "
           r"for the current bounded first-slice scope only with no product change; later Stage-35 slices NOT "
           r"AUTHORIZED;",
           r"or after the preceding " + re.escape(_S35_NAME) + r" \(delivered; scope: for ONE authenticated owner",
           r"or after Stage 24 — CAP-12 Form Mock-up Advisory — Closure "
           r"\(delivered; Stage 24 COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only",
           # AMENDED at the delivered Stage 25 / CAP-13 slice: Stage 25 ENTERED / PARTIAL leads the parenthetical
           # AMENDED at the delivered Stage 27 / THERM-01 slice: Stage 27 ENTERED / PARTIAL leads the parenthetical
           # AMENDED at the Stage 27 closure: Stage 27 COMPLETE for its current bounded scope leads the parenthetical
           r"\(Stage 27 is COMPLETE for its current bounded THERM-01 single-path temperature-difference scope only; Stage 25 is "
           r"ENTERED / PARTIAL for its CAP-13 Two-Support Static Reactions Slice 1 only; Stage 24 is "
           r"COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope only; Stage 35 is "
           r"COMPLETE for its current bounded first-slice scope only; Stage 36 is COMPLETE for its current no-live-AI / "
           r"provider scope only; Stage 16 is COMPLETE for its current bounded Technical \+ Integration "
           r"evidence-sufficiency composition scope only\)",      # ADVANCED at the Stage 16 closure
           r"the next step is a LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT \(read-only planning / selection until "
           # ADVANCED at the delivered Stage 27 / THERM-01 slice: no further Stage-27 / THERM-01 work either
           r"the Owner separately authorizes another product increment; no further Stage-27 / THERM-01 slice, method, "
           r"consumer or unit conversion, no full THERM-01, no further Stage-25 / CAP-13 method, consumer "
           r"or unit conversion, no full CAP-13, no further Stage-16 / SRL work, no later "
           r"Stage-35 slice, no CAP-15 / CAP-17 implementation and no Stage-37 work is authorized\)\.",
           r"or after the preceding Stage 24 — CAP-12 Form Mock-up Advisory — Slice 1 \(delivered; Stage 24 was then "
           r"ENTERED / PARTIAL for that slice only", r"or after the preceding Stage 23 closure \(delivered;")
    _rejects(subtask, CHECKLIST, "live subtask", *_S2_CLOSE_REVERSALS, *_S15C_STALE, *_S18C_STALE, *_S19C_STALE,
             *_S20C_STALE, *_S21C_STALE, *_S22C_STALE, *_S23C_STALE, *_S24C_STALE, *_S24CL_STALE, *_S35C_STALE,
             *_S35C_REVERSALS, *_S36C_STALE, *_S36C_REVERSALS,
             *_S16C_STALE, *_S16C_REVERSALS, *_S25_STALE, *_S25_REVERSALS,
             *_S27_STALE, *_S27_REVERSALS)
    # ADVANCED at the Stage 16 closure: the post-Stage-36-closure NONE subtask is preserved history
    assert ("*(Superseded 2026-10-06 by " + _S16C_NAME + ", preserved — was: \"**CURRENT SUBTASK:** NONE "
            "(post-Stage-36-closure) — NO PRODUCT INCREMENT IS CURRENTLY AUTHORIZED — " + _S36C_NAME + " DELIVERED (…) — "
            "…\" with Stage 16 then unticked and recorded as DEFERRED.)*") in flat_checklist
    # ADVANCED at the Stage 36 closure: the post-Stage-35-closure NONE subtask is preserved history
    assert ("*(Superseded 2026-10-05 by " + _S36C_NAME + ", preserved — was: \"**CURRENT SUBTASK:** NONE "
            "(post-Stage-35-closure) — NO PRODUCT INCREMENT IS CURRENTLY AUTHORIZED — " + _S35C_NAME + " DELIVERED (…; "
            "Stage 36 NOT ENTERED / NOT AUTHORIZED) — …\" with " + _S36_NOT[0] + " · " + _S36_NOT[1]) in flat_checklist
    # ADVANCED at the Stage 35 closure: the Stage-35 active-increment subtask is preserved history
    assert ("*(Superseded 2026-10-05 by " + _S35C_NAME + ", preserved — was: \"**CURRENT SUBTASK:** STAGE 35 — FIRST "
            "BOUNDED STRUCTURED INVENTION DISCLOSURE EXPORT SLICE (Owner-authorized 2026-10-05) — Stage 35 ENTERED / "
            "PARTIAL — first bounded slice only; first bounded slice DELIVERED; Stage 35 NOT complete, NOT closed;") in (
        flat_checklist)
    # ADVANCED at the delivery of the first bounded slice: the pre-merge Stage-35 subtask is preserved history
    assert ("*(Superseded 2026-10-05 by the delivery of the Stage 35 first bounded slice, preserved — was: \"**CURRENT "
            "SUBTASK:** STAGE 35 — FIRST BOUNDED STRUCTURED INVENTION DISCLOSURE EXPORT SLICE … — Stage 35 ENTERED / "
            "PARTIAL — first bounded slice only; NOT delivered, NOT complete, NOT closed;") in flat_checklist
    # ROTATED at the Stage 35 first bounded slice: the post-Stage-24-closure NONE subtask is preserved history
    assert ("*(Superseded 2026-10-05 by " + _S35_NAME + ", preserved — was: \"**CURRENT SUBTASK:** NONE "
            "(post-Stage-24-closure) — NO PRODUCT INCREMENT IS CURRENTLY AUTHORIZED — Stage 24 — CAP-12 Form Mock-up "
            "Advisory — Closure DELIVERED (…) — …\" with `ACTIVE CONTRACT: NONE` · `NEXT PRODUCT INCREMENT: NOT "
            "AUTHORIZED` · `NEXT STEP: LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT`") in flat_checklist
    for line in [t.strip("`") for t in _S16C_TOKENS + (_S23C_DELIVERED, _S23_COMPLETE,
                                        _S25_MARKER, _NO_S25, _S24C_DELIVERED, _S24_COMPLETE, _S24_DELIVERED,
                                        _S22C_DELIVERED,
                                        _S22_COMPLETE, _S21_COMPLETE,
                                        _S20_COMPLETE, _S19_COMPLETE, _S18_COMPLETE, _MSNL_FUTURE, _S15_COMPLETE)
                 + _S24C_LIMITS + _S23_LIMITS + _S22_LIMITS + _S21_LIMITS + _S20_LIMITS + _S19_LIMITS[:2] + _S15C_NOT
                 + _S2_NOT]:
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    for token in (_S21C_DELIVERED, _S20C_DELIVERED, _S19C_DELIVERED, _S18C_DELIVERED, _S15C_DELIVERED, _S4_DELIVERED, _S3_DELIVERED, _S2_DELIVERED,
                  _S15_DELIVERED):
        assert re.search(r"^" + _status_line(token) + r"$", raw_checklist, re.M), token
    for stale in (_S2_CONTRACT.strip("`"), _S2_STATUS.strip("`"), _S15_ENTERED.strip("`"),
                  "FULL STAGE 15 / IRL: NOT AUTHORIZED", _S15_MARKER.strip("`"), _NEXT_STEP.strip("`"),
                  "STAGE 18 COMPLETE: NO", "STAGE 18: ENTERED / PARTIAL / NOT COMPLETE", _S19_MARKER.strip("`"),
                  _NO_S19.strip("`"), "STAGE 19: ENTERED / NOT COMPLETE", _S20_MARKER.strip("`"),
                  _NO_S20.strip("`"), "STAGE 20: ENTERED / PARTIAL — CAP-08 SLICE 1 ONLY", _S21_MARKER.strip("`"),
                  _NO_S21.strip("`"), "STAGE 21: ENTERED / PARTIAL — CAP-10 SLICE 1 ONLY", _S22_MARKER.strip("`"),
                  _NO_S22.strip("`"), "STAGE 22: ENTERED / PARTIAL — CAP-05 + CAP-07 SLICES 1–2 ONLY",
                  _S23_MARKER.strip("`"), _NO_S23.strip("`"), "STAGE 23: NOT ENTERED", "CAP-06: NOT ACTIVATED",
                  _S24_PRE_MARKER.strip("`"), _NO_S24.strip("`"), "STAGE 24: NOT ENTERED",
                  # AMENDED at the Stage 24 closure: the ENTERED / PARTIAL forms are stale lines too
                  _S24_MARKER.strip("`"), _S24_PARTIAL.strip("`"),
                  # ROTATED at the Stage 35 first bounded slice: the post-Stage-24-closure NONE lines were stale
                  # ROTATED at the Stage 35 closure: the NONE lines are live again; the retired Stage-35 active-increment
                  # lines are stale
                  *(t.strip("`") for t in _S35_ACTIVE_ONLY),
                  # ADVANCED at the Stage 36 closure: the Stage 35 closure's Stage-36 NOT-ENTERED lines are stale
                  *(t.strip("`") for t in _S36_NOT),
                  # ADVANCED at the delivery of the first bounded slice: its pre-merge status lines are stale too
                  "STAGE 35 MERGE AUTHORIZATION: NO", "STAGE 35 FIRST BOUNDED SLICE: NOT DELIVERED"):
        assert re.search(r"^" + re.escape(stale) + r"$", raw_checklist, re.M) is None, stale
    # ROTATED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: Stage 25 ENTERED / PARTIAL
    assert ("**CURRENT PRODUCT-DEPTH FRONTIER: Stage 25 — ENTERED / PARTIAL — NAVIGATION ONLY (`MASTER ROADMAP SEQUENTIAL "
            "MARKER: STAGE 25 — ENTERED / PARTIAL — NAVIGATION ONLY`;") in flat_checklist
    roadmap = _read(ROADMAP)
    numbers = [int(n) for n in re.findall(r"^- \[[ x]\] \*\*(\d+) — ", roadmap, re.M)]
    assert sorted(numbers) == list(range(1, 46)), numbers
    # Stages 15 and 18 are ticked (COMPLETE for the current Mechanical + Electrical / Electronics scope), Stage 19
    # (COMPLETE for the current planning-only scope) and Stage 20 (COMPLETE for the current Owner-declared assumption
    # scope) and Stage 21 (COMPLETE for the current Owner-declared contradiction scope) and Stage 22 (COMPLETE for the
    # current bounded decision trace + decision room scope) and Stage 23 (COMPLETE for the current bounded four-axis
    # Readiness Snapshot scope) and Stage 24 (COMPLETE for the current bounded CAP-12 Form Mock-up Advisory Slice 1
    # scope); the stages routed past (11, 13, 14, 16, 17) and the navigation-only, NOT ENTERED Stage 25 stay unticked
    # ADVANCED at the Stage 35 closure: Stage 35 (COMPLETE for the current bounded first-slice scope) is ticked too
    # ADVANCED at the Stage 36 closure: Stage 36 (COMPLETE for the current no-live-AI / provider scope) is ticked too;
    # Stage 37 stays unticked
    # ADVANCED at the Stage 16 closure: Stage 16 (COMPLETE for the current bounded Technical + Integration
    # evidence-sufficiency composition scope) is ticked too; Stages 13 and 14 (PARTIAL / DEFERRED) stay unticked
    # ADVANCED at the Stage 27 closure: Stage 27 (COMPLETE for the current bounded THERM-01 single-path
    # temperature-difference scope) is ticked too
    for n in (15, 16, 18, 19, 20, 21, 22, 23, 24, 27, 35, 36):
        assert re.search(r"^- \[ \] \*\*%d — " % n, roadmap, re.M) is None, n
    for n in (11, 13, 14, 17, 25, 37):
        assert re.search(r"^- \[ \] \*\*%d — " % n, roadmap, re.M), n
    # ADDED at the Stage 35 first bounded slice (row 35 then unticked, 23 of 45 rows unticked); ADVANCED at the Stage 35
    # closure (22 of 45 unticked); ADVANCED at the Stage 36 closure (21 of 45 unticked); ADVANCED at the Stage 16 closure:
    # row 16 is ticked for its bounded scope only and the roadmap keeps exactly 20 of its 45 rows unticked — the remaining
    # stages are exactly 11, 13, 14, 17, 25, 26, 27, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 44 and 45
    # ADVANCED at the Stage 27 closure: row 27 is ticked for its bounded scope only; 26 of 45 ticked, 19 unticked
    assert len(re.findall(r"^- \[ \] \*\*\d+ — ", roadmap, re.M)) == 19
    assert len(re.findall(r"^- \[x\] \*\*\d+ — ", roadmap, re.M)) == 26
    # ADDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: row 25 stays UNTICKED and records
    # the scoped ENTERED / PARTIAL entry only; the count stays 25 ticked / 20 unticked
    [row25] = re.findall(r"^- \[ \] \*\*25 — CAP-13:\*\*.*$", roadmap, re.M)
    assert ("**ENTERED / PARTIAL (2026-10-08) through the delivered CAP-13 Two-Support Static Reactions Slice 1 ONLY — "
            "checkbox stays UNTICKED; Stage 25 is NOT complete:**") in row25
    assert _S25_PARTIAL in row25 and _S25_FULL_NO in row25
    assert [int(n) for n in re.findall(r"^- \[ \] \*\*(\d+) — ", roadmap, re.M)] == [
        11, 13, 14, 17, 25, 26, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 44, 45]
    # ADDED at the Stage 27 closure: row 27 is ticked for the current bounded THERM-01 single-path temperature-difference
    # scope only, names its closure, records the uncertainty selection and keeps full THERM-01 NOT AUTHORIZED
    [row27] = re.findall(r"^- \[x\] \*\*27 — THERM-01:\*\*.*$", roadmap, re.M)
    live27 = _live_only(row27)
    assert ("**COMPLETE (2026-10-09) for the current bounded THERM-01 single-path temperature-difference scope ONLY — "
            "checkbox ticked for that scope only:** " + _S27C_DELIVERED + " · " + _S27_COMPLETE + " · " + _S27_FULL_NO) in live27
    for needle in ("no quantified uncertainty or tolerance is claimed", "bounded by declarations D-1 to D-6",
                   "the method refuses or abstains", "measurement or thermal-specialist confirmation stays required",
                   "broader thermal engineering is NOT implied", "Stage 25 stays ENTERED / PARTIAL"):
        assert needle in live27, needle
    assert _S27_PARTIAL not in live27 and "NOT complete" not in live27
    # ADDED at the Stage 16 closure: row 16 is ticked for the current bounded Technical + Integration evidence-sufficiency
    # composition scope only, names its closure and the delivered residual, keeps Stages 13 / 14 PARTIAL / DEFERRED and
    # computes no SRL level, single score or weakest axis
    [row16] = re.findall(r"^- \[x\] \*\*16 — SRL-compatible composition:\*\*.*$", roadmap, re.M)
    live16 = _live_only(row16)
    assert ("**COMPLETE (2026-10-06) for the current bounded Technical + Integration evidence-sufficiency composition "
            "scope ONLY — checkbox ticked for that scope only:** " + _S16_COMPLETE + " through the Owner-authorized "
            + _S16C_NAME + " (" + _S16C_DELIVERED + ") after the delivered bounded presentation-only residual "
            + _S16_NAME + " (" + _S16_DELIVERED + "; PR #") in live16
    for needle in (_S16_SRL_NO, *_S13_14_PARTIAL, "each from its own canonical owner and independently visible",
                   "insufficiency is never hidden by aggregation",
                   "on an integrated invention the Technical row states that it reflects only the selected initial "
                   "analysis focus",
                   "\"Without hiding the weakest axis\" is satisfied in this bounded scope by that independent visible "
                   "source truth and the explicit focus-scope disclosure; no weakest axis is computed.",
                   "no single score, weighting, composite, overall readiness result, SRL number or level, engineering "
                   "compatibility conclusion or validated system-readiness conclusion, and no SRL engine",
                   "Stage 15 keeps its bounded completion and Stage 17 its partial truth",
                   "full TRL, MRL and SRL, positive readiness and validated Technical or Integration evidence stay NOT "
                   "AUTHORIZED"):
        assert needle in live16, needle
    for stale in ("checkbox stays UNTICKED", "ENTERED / PARTIAL", "NOT complete", "DEFERRED.", "weakest axis is "
                  "identified", "SRL level is"):
        assert stale not in live16, stale
    # ADDED at the Stage 36 closure: row 36 is ticked for the current no-live-AI / provider scope only and names its
    # closure, its limits and the fresh-reassessment condition
    [row36] = re.findall(r"^- \[x\] \*\*36 — CAP-15 \+ CAP-17:\*\*.*$", roadmap, re.M)
    live36 = _live_only(row36)
    assert ("**COMPLETE (2026-10-05) for the current no-live-AI / provider scope ONLY — checkbox ticked for that scope "
            "only:** " + _S36_COMPLETE + " through the Owner-authorized " + _S36C_NAME) in live36
    for needle in (_S36C_DELIVERED, *_S36_LIMITS, *_S37_NOT, "deterministic gates remain final",
                   "provider abstraction and prompt/model configuration only if live AI use is selected"):
        assert needle in live36, needle
    for stale in ("checkbox stays UNTICKED", "ENTERED / PARTIAL", "NOT complete", "STAGE 36: NOT ENTERED"):
        assert stale not in live36, stale
    # ADDED at the Stage 35 closure: row 35 is ticked for the current bounded first-slice scope only, names its closure,
    # its limits and its preserved triggers, and keeps no live ENTERED / PARTIAL wording
    [row35] = re.findall(r"^- \[x\] \*\*35 — Patent export:\*\*.*$", roadmap, re.M)
    live35 = _live_only(row35)
    assert ("**COMPLETE (2026-10-05) for the current bounded first-slice scope ONLY — checkbox ticked for that scope "
            "only:** " + _S35_COMPLETE + " through the Owner-authorized " + _S35C_NAME) in live35
    # ROTATED at the Stage 36 closure: row 35's Stage-36 NOT-ENTERED tokens are history ("was then")
    for needle in (_S35C_DELIVERED, _S35_SLICE_DELIVERED, _S35_LATER_NO, *_S35_LIMITS, _S35_TRIGGERS,
                   "Stage 36 was then NOT ENTERED / NOT AUTHORIZED (the later Stage 36 closure completed Stage 36 for "
                   "its current no-live-AI / provider scope only)",
                   "documentation assistance only; no patentability, FTO or legal-validity claim"):
        assert needle in live35, needle
    for stale in ("checkbox stays UNTICKED", "ENTERED / PARTIAL", "NOT complete", *_S36_NOT):
        assert stale not in live35, stale
    # AMENDED at the Stage 24 closure: row 24 is ticked for the current bounded CAP-12 Form Mock-up Advisory Slice 1
    # scope only, names its closure and its limits, and keeps no live ENTERED / PARTIAL wording
    [row24] = re.findall(r"^- \[x\] \*\*24 — CAP-12:\*\*.*$", roadmap, re.M)
    live24 = _live_only(row24)
    assert ("**COMPLETE (2026-10-04) for the current bounded CAP-12 Form Mock-up Advisory Slice 1 scope ONLY — checkbox "
            "ticked for that scope only:** " + _S24_COMPLETE) in live24
    for needle in (_S24C_DELIVERED, *_S24C_LIMITS, "NO STAGE-25 IMPLEMENTATION AUTHORIZED BY STAGE-24 CLOSURE",
                   "CAP-12 and CAP-13 remain separate", "no final specification claim"):
        assert needle in live24, needle
    for stale in ("checkbox stays UNTICKED", "Stage 24 is NOT complete", _S24_PARTIAL):
        assert stale not in live24, stale
    [row15] = re.findall(r"^- \[x\] \*\*15 — IRL-compatible view:\*\*.*$", roadmap, re.M)
    live15 = _live_only(row15)
    assert "the Owner-authorized Stage 15 — Integration Evidence & IRL-Compatible View — Closure (delivered" in live15
    assert ("**COMPLETE (2026-10-01) for the current Mechanical + Electrical / Electronics scope — checkbox ticked "
            "for that scope only:**") in live15
    assert "Phase-7 integration residuals remain Phase 7" in live15
    assert "no further Stage-15 slice is authorized" in live15
    for stale in ("checkbox stays unticked", "wider Stage-15 work stays DEFERRED", "ENTERED / PARTIAL / NOT COMPLETE"):
        assert stale not in live15, stale
    [row18] = re.findall(r"^- \[x\] \*\*18 — D13/CAP-01 guidance:\*\*.*$", roadmap, re.M)
    live18 = _live_only(row18)
    for needle in ("**COMPLETE (2026-10-01) for the current Mechanical + Electrical / Electronics scope — checkbox "
                   "ticked for that scope only:** `STAGE 18: COMPLETE — CURRENT MECHANICAL + ELECTRICAL / ELECTRONICS "
                   "SCOPE` through the Owner-authorized Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure "
                   "(delivered",
                   "Research Gate 3 reconciliation: its prerequisites applied to research-backed knowledge expansion",
                   "Research Gate 3 is not reopened", "MSNL stays FUTURE / DEFERRED / NOT ACTIVATED",
                   "NO STAGE-19 IMPLEMENTATION AUTHORIZED BY STAGE-18 CLOSURE",
                   "routing past Stages 11, 13, 14, 16 and 17 completes none of them",
                   "that reassessment then selected Stage 15 — Subsystem Interface Declaration & Verification "
                   "Preparation — Slice 2, delivered",
                   "the next reassessment then selected CAP-09 Result Event Slice 1 (Stage 19), delivered",
                   "the next reassessment then selected Stage 15 — Integration Evidence & IRL-Compatible View — "
                   "Closure, delivered, which completes Stage 15 for the current Mechanical + Electrical / Electronics "
                   "scope",
                   "the next reassessment then selected Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure, "
                   "delivered, which completes Stage 18 for the current Mechanical + Electrical / Electronics scope",
                   "no product increment is currently authorized and the next step is a Lead-controlled next-stage "
                   "closure reassessment"):
        assert needle in live18, needle
    for stale in ("checkbox stays unticked", "Stage 18 stays ENTERED", "leaves Stage 18 ENTERED",
                  "the next step is a Lead-controlled Next-Increment Reassessment"):
        assert stale not in live18, stale
    [row19] = re.findall(r"^- \[x\] \*\*19 — WS-PFV-001/CAP-09:\*\*.*$", roadmap, re.M)
    live19 = _live_only(row19)
    for needle in ("**COMPLETE (2026-10-01) for the current planning-only scope — checkbox ticked for that scope only:** "
                   "`STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE` through the Owner-authorized Stage 19 — "
                   "Experiment Execution-State Disclosure — Closure (delivered",
                   "`FULL CAP-09: NOT AUTHORIZED`", "`FULL WS-PFV-001: NOT AUTHORIZED`",
                   "`RESULT OUTCOME / PASS-FAIL JUDGEMENT: NOT AUTHORIZED`",
                   "`FORMAL EXPERIMENTAL VARIABLE MODEL: NOT AUTHORIZED`",
                   "it claims no scientific validity, validated result, prototype validation, readiness, risk "
                   "resolution or feasibility",
                   "NO STAGE-20 IMPLEMENTATION AUTHORIZED BY STAGE-19 CLOSURE",
                   "satisfied for planning-only CAP-09 entry, and for nothing wider"):
        assert needle in live19, needle
    for stale in ("checkbox stays unticked", "NO STAGE-19 IMPLEMENTATION AUTHORIZED BY STAGE-18 CLOSURE",
                  "**ENTERED / NOT COMPLETE (2026-09-23):**"):
        assert stale not in live19, stale
    # the CAP-09 failure / risk / variable limits are reconciled in the stage description, never widened
    assert ("Stage-19 closure reconciliation (2026-10-01): for the current planning-only scope the failure side is the "
            "existing generated `failure_or_revision_condition` (no separate Failure Criterion field)") in roadmap
    # the historical Research Gate 3 language is preserved, and reconciled rather than erased
    assert "Research Gate 3 appointments and activation remain prerequisites; AI is not technical authority." in roadmap
    assert "and any future research-backed knowledge expansion stays separately gated by them" in roadmap
    [row20] = re.findall(r"^- \[x\] \*\*20 — CAP-08:\*\*.*$", roadmap, re.M)
    live20 = _live_only(row20)
    for needle in ("**COMPLETE (2026-10-01) for the current Owner-declared assumption scope — checkbox ticked for that "
                   "scope only:** `STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE` through the "
                   "Owner-authorized Stage 20 — Assumption Revision & Replacement — Closure (delivered",
                   "`FULL CAP-08: NOT AUTHORIZED`",
                   "NO STAGE-21 IMPLEMENTATION AUTHORIZED BY STAGE-20 CLOSURE",
                   "append-only revision, append-only replacement and retained supersession history",
                   "**ENTERED / PARTIAL (2026-09-26):** CAP-08 Slice 1"):
        assert needle in live20, needle
    for stale in ("checkbox stays unticked",):
        assert stale not in live20, stale
    [row21] = re.findall(r"^- \[x\] \*\*21 — CAP-10:\*\*.*$", roadmap, re.M)
    live21 = _live_only(row21)
    for needle in ("**COMPLETE (2026-10-01) for the current Owner-declared contradiction scope — checkbox ticked for "
                   "that scope only:** `STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE` through the "
                   "Owner-authorized Stage 21 — Owner-Declared Contradiction Visibility — Closure (delivered",
                   "`FULL CAP-10: NOT AUTHORIZED`", "`AUTOMATIC / AI CONTRADICTION DETECTION: NOT AUTHORIZED`",
                   "`SYSTEM_INFERRED CONTRADICTION WRITER: NOT AUTHORIZED`",
                   "NO STAGE-22 IMPLEMENTATION AUTHORIZED BY STAGE-21 CLOSURE",
                   "**ENTERED / PARTIAL (2026-09-26):** CAP-10 Slice 1"):
        assert needle in live21, needle
    assert "the checkbox stays unticked" not in live21
    [row22] = re.findall(r"^- \[x\] \*\*22 — CAP-05 \+ CAP-07:\*\*.*$", roadmap, re.M)
    live22 = _live_only(row22)
    for needle in ("**COMPLETE (2026-10-01) for the current bounded decision trace + decision room scope — checkbox "
                   "ticked for that scope only:** `STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE + DECISION ROOM "
                   "SCOPE` through the Owner-authorized Stage 22 — Decision Trace + Decision Room — Closure (delivered "
                   "with no product change required — `STAGE 22 CLOSURE: DELIVERED — NO PRODUCT CHANGE REQUIRED`",
                   "`FULL CAP-05: NOT AUTHORIZED`", "`FULL CAP-07: NOT AUTHORIZED`",
                   "NO STAGE-23 IMPLEMENTATION AUTHORIZED BY STAGE-22 CLOSURE",
                   "**ENTERED / PARTIAL (2026-09-26):** CAP-05 + CAP-07 Slice 1"):
        assert needle in live22, needle
    assert "the checkbox stays unticked" not in live22
    [row23] = re.findall(r"^- \[x\] \*\*23 — CAP-06:\*\*.*$", roadmap, re.M)
    live23 = _live_only(row23)
    for needle in ("**COMPLETE (2026-10-02) for the current bounded four-axis Readiness Snapshot scope ONLY — "
                   "checkbox ticked for that scope only:** `STAGE 23: COMPLETE — CURRENT BOUNDED FOUR-AXIS "
                   "READINESS-SNAPSHOT SCOPE ONLY` through the Owner-authorized Stage 23 — CAP-06 Four-Axis Readiness "
                   "Snapshot — Closure (delivered with no product change required — `STAGE 23 CLOSURE: DELIVERED — NO "
                   "PRODUCT CHANGE REQUIRED`", *_S23_LIMITS,
                   "no weighting, score, percentage, average, composite, ranking, weakest-axis calculation, "
                   "threshold aggregate or overall pass / fail",
                   "NO STAGE-24 IMPLEMENTATION AUTHORIZED BY STAGE-23 CLOSURE"):
        assert needle in live23, needle
    for live in (live15, live18, live19, live20, live21, live22, live23):
        for pat in (_S2_CLOSE_REVERSALS + _S15C_STALE + _S18C_STALE + _S19C_STALE + _S20C_STALE + _S21C_STALE
                    + _S22C_STALE + _S23C_STALE):
            assert re.search(pat, live, re.I) is None, pat
    register = _flat(CAPABILITIES)
    assert "Nor is Stage 15 — Integration Evidence & IRL-Compatible View — Closure (delivered" in register
    assert "A sixth bounded slice — Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure: delivered" in register
    for token in (_S18_COMPLETE, _S19_COMPLETE, _NO_S20, _S20_COMPLETE, _NO_S21, _S21_COMPLETE, _NO_S22,
                  _S22_COMPLETE, _NO_S23, _S22C_DELIVERED, _S23_COMPLETE, _S23C_DELIVERED, _S24_MARKER, _NO_S24,
                  "`FULL CAP-06: NOT AUTHORIZED`", "`FULL EIGHT-AXIS CAP-06: NOT IMPLEMENTED / NOT CLOSED`"):
        assert token in register, token
    assert "and (2) the Stage 21 — Owner-Declared Contradiction Visibility — Closure (delivered)" in register
    assert "the Stage 22 — Decision Trace + Decision Room — Closure (delivered with no product change required" in register
    assert _S21_MARKER not in _live_only(register)
    assert _S22_MARKER not in _live_only(register)
    assert _S23_MARKER not in _live_only(register)
    assert "(6) the Stage 19 — Experiment Execution-State Disclosure — Closure (delivered)" in register
    assert "and (2) the Stage 20 — Assumption Revision & Replacement — Closure (delivered)" in register
    assert "`STAGE 18 COMPLETE: NO`" not in _live_only(register)
    assert _S19_MARKER not in _live_only(register)
    assert _S20_MARKER not in _live_only(register)
    assert ("nor by the Stage 18 closure: full future CAP-01 (typed parameters, calculations, specialist mapping, "
            "further domains) stays NOT AUTHORIZED") in register
    assert "current Owner-authorized implementation candidate, not merged" not in register


def test_stage15_slice2_delivery_record_is_preserved_history():
    """PRESERVED HISTORY (not a live prerequisite): the Stage 15 Slice 2 contract section stays a visibly
    superseded, DELIVERED record with every rule still binding, and the pre-merge candidate wording it
    replaced survives only inside superseded notes. The identities pinned here already exist in history."""
    contract = _read(CONTRACT)
    s2 = re.sub(r"\s+", " ", _section(contract, "current-authority--stage15-subsystem-interface-slice2"))
    _needs(s2, CONTRACT, "slice2 delivered section",
           r"## Current authority — Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2 "
           r"\(Owner authorization, 2026-09-29\) — DELIVERED \(PR #720\); SUPERSEDED as current authority by the "
           r"post-PR-#720 no-active-contract declaration",
           r"\*\*No longer the current authority\.\*\*", r"Every rule below still binds",
           r"\*\(Superseded 2026-09-29, preserved so the change is visible rather than silent: this opened "
           r"\"\*\*ACTIVE CONTRACT: STAGE 15 — SUBSYSTEM INTERFACE DECLARATION & VERIFICATION PREPARATION — "
           r"SLICE 2\.\*\*\"",
           r"DELIVERED \(PR #720, merge `" + _S2_MERGE + r"`",
           r"\*\*SEMANTIC OWNER\*\* \| `engine/subsystem_model\.py`",
           r"completing the preparation does not verify the interaction or establish compatibility; no risk row",
           _tok(_S2_DELIVERED), _tok(_S2_REVIEW), _tok(_S2_ANC))
    _rejects(_live_only(s2), CONTRACT, "slice2 delivered section", *_S2_CLOSE_REVERSALS)
    none720 = re.sub(r"\s+", " ", _section(contract, "current-authority--post-pr-720-no-active-contract"))
    _needs(none720, CONTRACT, "post-720 none superseded",
           r"^<a id=\"current-authority--post-pr-720-no-active-contract\"></a> ## Current authority — post-PR-#720: "
           r"no active contract \(2026-09-29\) — SUPERSEDED \(2026-09-30\) by Stage 15 — Interface Verification "
           r"Preparation Metadata — Slice 3 ",
           r"\*\*No longer the current authority\.\*\*",
           r"\*\(Superseded 2026-09-30, preserved so the change is visible rather than silent: this opened ")
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        assert ("*(Superseded 2026-09-29 by the post-PR-#720 closure, preserved so the change is visible rather "
                "than silent: the current routing read \"**CURRENT BOUNDED PRODUCT ACTION — Stage 15 / Subsystem "
                "Interface Declaration & Verification Preparation — Slice 2 (…):**") in _after_fence(path, "current-routing"), path
    assert ("*(Superseded 2026-09-29 by the post-PR-#720 closure, preserved so the change is visible rather than "
            "silent: the current-position entry read \"" + _S2_CONTRACT) in _after_fence(STATE, "current-position")
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    assert ("the former Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2 "
            "(pre-merge, \"IMPLEMENTATION CANDIDATE … NOT MERGED\")") in claude
    assert ("*(Superseded 2026-09-29 by the post-PR-#720 closure, preserved — was: \"**CURRENT SUBTASK:** STAGE 15 — "
            "SUBSYSTEM INTERFACE DECLARATION & VERIFICATION PREPARATION — SLICE 2 (current bounded product action; "
            "implementation candidate; …)\"") in _flat(CHECKLIST)


def test_source_ip_boundary_invention_first_and_portfolio_reassessment_are_continuity_only():
    """The Owner-accepted Technical Knowledge & IP Source Boundary, the invention-first
    multi-domain principle, the Mechatronics / Robotics planning direction and the shared-vs-
    private knowledge boundary live in the EXISTING CLAUDE.md continuity section; they create no
    gate, document, program, domain, Stage or capability, and the portfolio order is re-assessed
    rather than permanently hard-coded."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    cont = claude[claude.index("## Lead execution continuity"):claude.index("### Lead Operating Method")]
    for needle in ("NO TECHNICAL DEPTH WITHOUT SOURCE AUTHORITY.",
                   "NO SOURCE INGESTION WITHOUT A KNOWN AND COMPATIBLE USE BASIS.",
                   "UNKNOWN RIGHTS = DO NOT INGEST BY DEFAULT.", "AI ANSWER ≠ SOURCE LICENSE.",
                   "define the exact claim; identify the required technical authority; verify the "
                   "original source; verify the source-use basis; bind the source only to the claims it "
                   "actually supports",
                   "Availability on the public internet is not permission for commercial reuse",
                   "free-to-read / Open Access does not automatically mean commercial reuse is permitted",
                   "attribution alone does not cure an incompatible license",
                   "never substitute a technically weaker open source for a standard-specific "
                   "compliance / certification claim",
                   "access does NOT authorize copying protected prose, tables, figures, datasets or "
                   "other protected expression",
                   "Third-party material inside an otherwise usable source is treated separately",
                   "no source endorsement may be implied",
                   "SEARCH BY TECHNICAL CLAIM / TECHNICAL NEED, NOT MERELY BY DOMAIN NAME.",
                   "shared knowledge does NOT erase domain-specific technical authority",
                   "THE USER SUBMITS AN INVENTION, NOT A DOMAIN",
                   "A Domain Pack is an internal governed source of technical authority, not "
                   "automatically a separate user-facing product",
                   "NOT EVERY NAMED TECHNOLOGY REQUIRES A DOMAIN PACK",
                   "first treated as a cross-domain integration perspective, not automatically a "
                   "duplicated technical domain",
                   "no generic Mechatronics framework is built ahead of an actual product slice",
                   "Robotics is NOT automatically a new Domain Pack",
                   "Mechanical / Electrical knowledge is never duplicated inside a Robotics container",
                   "no Robotics implementation is authorized now",
                   "SHARED GOVERNED TECHNICAL KNOWLEDGE stays separate from PRIVATE INVENTOR / PROJECT "
                   "INFORMATION",
                   "Portfolio sequencing is RE-ASSESSED, not a permanently hard-coded order",
                   "the NEXT REASSESSMENT considers the smallest real Electrical ↔ Mechanical / "
                   "Mechatronics integration slice",
                   "a Robotics capability assessment precedes any Robotics decision",
                   "**NEXT TRIGGER — source-rights architecture (future architecture decision, not "
                   "current implementation).**",
                   "unknown-rights fail-closed behaviour", "Do not build it now.",
                   "**FUTURE RELEASE TRIGGER — ONE bounded THIRD-PARTY CONTENT & IP RELEASE CHECK.**",
                   "Platform acceptance is NOT InventorAI IP clearance.",
                   "not a recurring governance program",
                   "**WATCH — Electrical / Electronics Technical Deepening Slice 1 (non-blocking, no "
                   "repair cycle).**"):
        assert needle in cont, needle
    # the old fixed sequence survives only as superseded roadmap history, never in CLAUDE.md
    assert "Current priority: Mechanical deepening now" not in claude
    for pat in (r"(?i)(?<!not )(?<!no )(Mechatronics|Robotics) (implementation |domain )?(is|are) "
                r"(now )?(AUTHORIZED|ACTIVATED)\b",
                r"(?i)source-rights architecture[^.]{0,60}\b(is|was) (built|implemented|authorized)\b",
                r"(?i)\b(is|as) a (governance|approval) gate\b"):
        assert re.search(pat, cont) is None, pat
    roadmap = _read(ROADMAP)
    # Stage 15 is ticked (COMPLETE for the current Mechanical + Electrical / Electronics scope); ADVANCED at the
    # Stage 28 closure: 28 is ticked for its bounded optional-part scope only
    rows = {n: re.search(r"^- \[x\] \*\*" + n + r" — .*$", roadmap,
                         re.M).group(0) for n in ("15", "28")}
    live28 = re.sub(r"\*\(Superseded.*?\)\*", "", rows["28"])
    assert "Current priority" not in live28 and "in that planning order" not in live28
    assert "no permanently hard-coded sequence" in live28
    assert "Robotics is NOT automatically a new Domain Pack" in live28
    assert "Mechatronics is first treated as a cross-domain integration perspective" in rows["15"]
    live15 = re.sub(r"\*\(Superseded.*?\)\*", "", rows["15"])
    assert ("no Stage 15 implementation is authorized beyond the ONE delivered bounded slice and the "
            "Owner-authorized Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2") \
        in live15
    assert "no Stage 15 implementation is authorized now" not in live15
    assert ("that reassessment selected Stage 15 Slice 1, the FIRST real bounded Mechanical ↔ Electrical / "
            "Electronics integrated-invention product slice, which performs no full engineering integration "
            "analysis") in live15


def test_read_before_build_and_multi_domain_deepening_are_operating_method_not_gates():
    """Two continuity rules extend EXISTING CLAUDE.md paragraphs and create no
    gate: READ BEFORE BUILD / REUSE BEFORE CREATE is the Lead's own bounded
    overlap check (not a mandatory executor round, approval stage or governance
    gate), and the multi-domain Technical Deepening rule is a design principle
    that authorizes no new domain activation and no Stage 28 / 30 / 31 work;
    the roadmap rows for those stages stay unticked and unchanged in kind. The
    Owner-accepted portfolio / integration direction is recorded in the same
    paragraph as planning direction only, and the one-time prompt audit is
    recorded COMPLETE (not a live trigger) with the `or True` WATCH closed."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    cont = claude[claude.index("## Lead execution continuity"):
                  claude.index("### Lead Operating Method")]
    lead = cont[cont.index("**Lead and executor.**"):cont.index("**Review routing.**")]
    for needle in ("**READ BEFORE BUILD / REUSE BEFORE CREATE** is the Lead's standing method",
                   "normally directly, because the Lead has repository access",
                   "what already exists, the canonical owner(s), the reusable seam(s) and the "
                   "genuinely missing product delta",
                   "A separate Claude / executor read-only round is not the default prerequisite",
                   "ALREADY EXISTS → DO NOT BUILD A DUPLICATE",
                   "PARTIAL → reuse / extend the existing owner and implement only the missing "
                   "delta",
                   "ABSENT → implementation may be proposed within Owner-authorized scope",
                   "It is an operating method bounded to the proposed change — not a governance "
                   "gate, approval stage, mandatory extra agent round or historical reconstruction "
                   "requirement"):
        assert needle in lead, needle
    claims = lead.replace("not a governance gate, approval stage, mandatory extra agent round or "
                          "historical reconstruction requirement", "")
    for pat in (r"(?i)READ BEFORE BUILD[^.]{0,160}\b(mandatory|approval) (gate|stage|round)\b",
                r"(?i)\b(is|as) a (governance|approval) gate\b"):
        assert re.search(pat, claims) is None, pat
    dom = cont[cont.index("**Domain-scaling boundary.**"):cont.index("**Human-study boundary.**")]
    for needle in ("not the permanent InventorAI domain ceiling",
                   "Domain Pack Conformance Validator",
                   "that validator is NEXT TRIGGER, not authorized implementation",
                   "**Multi-domain Technical Deepening continuity rule (design / continuity "
                   "principle only; it authorizes NO new domain activation and no Stage 28 / 30 / "
                   "31 implementation).**",
                   "exactly two runtime-activated specialist domains (`electronics_electrical`, "
                   "`mechanical`)",
                   "ONE shared extensible technical architecture PLUS independently governed "
                   "domain-specific technical knowledge, never duplicated parallel technical "
                   "systems per domain",
                   "domain pack presence ≠ runtime activation",
                   "registered ≠ supported ≠ activated",
                   "domain activation does not authorize arbitrary technical guidance",
                   "every technical statement requires governed domain / source authority",
                   "D13 Electronics knowledge is NOT Mechanical or other-domain technical "
                   "authority",
                   "shared architecture does NOT imply identical semantics or identical gap sets "
                   "across domains",
                   "do not hard-code technical-depth architecture around today's Electronics + "
                   "Mechanical only",
                   "do not prematurely build a giant generic technical framework",
                   "generalize only the shared seam a real product slice justifies",
                   "must not require rewriting the product core",
                   "Stage 28 (IoT → Drone / Unmanned → Renewable, with Satellite / Space-System "
                   "as the preserved later Stage-28 subitem)",
                   "Stage 30 (cross-domain safeguards before new-domain activation)",
                   "Stage 31 (future IoT technical depth)"):
        assert needle in dom, needle
    claims = dom.replace("it authorizes NO new domain activation and no Stage 28 / 30 / 31 "
                         "implementation", "")
    for pat in (r"(?i)(?<!no )(?<!not )new domain activation (is )?authorized",
                r"(?i)Stage (28|30|31)[^.]{0,40}\b(AUTHORIZED|ENTERED|STARTED|ACTIVATED)\b",
                r"(?i)(IoT|drone|renewable|satellite)[^.]{0,40}\b(ACTIVATED|AUTHORIZED)\b"):
        assert re.search(pat, claims) is None, pat
    roadmap = _read(ROADMAP)
    # ADVANCED at the Stage 30 closure: row 30 is ticked for the current optional-part enablement safeguard scope
    # ONLY (never globally); rows 28 and 31 stay unticked
    # ADVANCED at the Stage 28 closure: row 28 is ticked for its bounded optional-part scope ONLY; row 31 stays open
    for stage in ("31 — IoT architecture:",):
        assert re.search(r"^- \[ \] \*\*" + re.escape(stage), roadmap, re.M), stage
    assert re.search(r"^- \[x\] \*\*28 — Additional-domain program:\*\*[^\n]*\*\*COMPLETE \(2026-10-02\) for the "
                     r"current bounded " + _CL.lower() + r" optional-part scope ONLY — checkbox ticked for that scope "
                     r"only:\*\*", roadmap, re.M), "28 — Additional-domain program:"
    assert re.search(r"^- \[x\] \*\*30 — Cross-domain safeguards:\*\*[^\n]*\*\*COMPLETE \(2026-10-02\) for the "
                     r"current " + _CL.lower() + r" part-enablement safeguard scope ONLY — checkbox ticked for that "
                     r"scope only:\*\*", roadmap, re.M), "30 — Cross-domain safeguards:"
    # the Owner-accepted portfolio / integration direction extends the SAME paragraph and
    # is planning direction only: no domain, Stage, slice or Stage 15 work is authorized
    for needle in ("**Owner-accepted portfolio / integration direction (planning direction only; it "
                   "authorizes no domain, Stage or slice).**",
                   "Shared InventorAI architecture + independently governed domain-specific knowledge "
                   "+ truthful domain-specific depth + shared evidence / gap / validation / decision "
                   "architecture",
                   "Technical depth and cross-domain integration are BOTH necessary: depth must not "
                   "become isolated parallel domain systems, and integration must not become a "
                   "generic framework built ahead of real use cases",
                   "shared project / subsystem / interface / dependency / evidence reasoning while "
                   "each domain keeps authority over its own technical truth",
                   "Stage 15 / IRL stays the existing roadmap home for subsystem interfaces, "
                   "cross-domain dependencies, integration evidence and durable subsystem identity / "
                   "persistence when required",
                   "no Stage 15 implementation is authorized beyond the bounded Stage 15 — Integrated "
                   "Invention Entry & Durable Subsystem Composition — Slice 1 (delivered, PR #718) and the "
                   "Owner-authorized Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2 "
                   "(delivered, PR #720) and the Owner-authorized Stage 15 — Interface Verification Preparation "
                   "Metadata — Slice 3 (delivered) and the Owner-authorized Stage 15 — Interface Verification "
                   "Observation Event — Slice 4 (delivered) and the Owner-authorized Stage 15 — Integration "
                   "Evidence & IRL-Compatible View — Closure (delivered; Stage 15 COMPLETE for the current "
                   "Mechanical + Electrical / Electronics scope; no further Stage-15 slice is authorized) and no new "
                   "integration Stage or capability is created",
                   "Portfolio sequencing is RE-ASSESSED, not a permanently hard-coded order",
                   "Add → Qualify → Activate → Establish Useful Baseline → Deepen — a preferred "
                   "model, not a universal mandatory lifecycle",
                   "Satellite / Space keeps its Stage-28 direction and does NOT require a full new "
                   "Domain Pack first",
                   "composition / orchestration, extension of existing capabilities, a smaller "
                   "space-specific reasoning layer, a true new domain only if justified, or deferral",
                   "composition / smaller reasoning stays preferred first",
                   "they remain in the FUTURE-DOMAIN REASSESSMENT POOL",
                   "without product value, overlap assessment, source maturity and explicit Owner "
                   "authorization",
                   "Stage 30 cross-domain safeguards stay mandatory before any NEW domain activation "
                   "and are reviewed proportionally to the actual proposed domain and the shared "
                   "boundaries it affects",
                   "not a recurring full-project governance audit, a mandatory whole-history review "
                   "or automatic re-validation of unrelated domains",
                   "No new domain activation is authorized."):
        assert needle in dom, needle
    # every Satellite "full new Domain Pack" mention is a denial of that requirement
    packs = list(re.finditer(r"(?i)\brequires? a full new Domain Pack", dom))
    assert packs, "the Satellite exception must be stated"
    for m in packs:
        assert dom[max(0, m.start() - 9):m.start()] == "does NOT ", dom[m.start() - 40:m.end()]
    # Software / Medical Device stay outside the active sequence and are never activated
    for pat in (r"(?i)(Software|Medical Device)[^.]{0,80}\b(is|are) (in|part of) the active "
                r"execution sequence",
                r"(?i)(Software|Medical Device)[^.:]{0,40}\bACTIVATED\b"):
        assert re.search(pat, dom) is None, pat
    assert "are NOT in the active execution sequence" in dom
    # Stage 30 proportionality: every recurring / whole-history mention is negated
    for word in ("recurring", "whole-history"):
        hits = [m.start() for m in re.finditer(word, dom)]
        assert hits, word
        for at in hits:
            assert re.search(r"(?i)\bnot a\b|\bnor\b|, a mandatory", dom[max(0, at - 80):at]), \
                dom[at - 80:at + 20]
    # roadmap Stage 15 / 28 / 30 rows carry the same planning direction; 28 stays unticked, Stage 15 is ticked for
    # the current Mechanical + Electrical / Electronics scope only and (ADVANCED at the Stage 30 closure) Stage 30
    # for the current optional-part enablement safeguard scope only
    rows = {n: re.search(r"^- \[x\] \*\*" + n + r" — .*$", roadmap,
                         re.M).group(0) for n in ("15", "28", "30")}
    assert "no Stage 15 implementation is authorized now" in rows["15"]
    assert "Add → Qualify → Activate → Establish Useful Baseline → Deepen" in rows["28"]
    assert "does NOT require a full new Domain Pack first" in rows["28"]
    assert "future-domain reassessment pool, outside the active sequence" in rows["28"]
    assert "proportional to the actual proposed domain and the shared boundaries it affects" in rows["30"]
    # the one-time prompt audit FIRED and is COMPLETE; the `or True` WATCH is CLOSED
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    for needle in ("**COMPLETE — one-time read-only prompt audit (the former NEXT TRIGGER, fired after "
                   "Mechanical CAP-01 closed).**",
                   "PASS — NO MATERIAL PROMPT ISSUE; no governance cycle is required",
                   "Its non-blocking hygiene findings stay natural-touch only",
                   "It is not a recurring gate or a prerequisite for any slice",
                   "**CLOSED — Mechanical CAP-01 test-hygiene WATCH.**",
                   "were replaced with real assertions on the natural touch by Mechanical Technical "
                   "Deepening Slice 1; nothing remains open"):
        assert needle in watch, needle
    for gone in ("**NEXT TRIGGER — one read-only prompt audit after Mechanical CAP-01 closes.**",
                 "**WATCH — Mechanical CAP-01 test hygiene (non-blocking, no repair cycle).**",
                 "Remove or replace them on the next natural touch of that test file"):
        assert gone not in watch, gone
    assert re.search(r"(?i)NEXT TRIGGER[^.]{0,80}prompt[- ]audit", watch) is None

def test_cap09_slice_3_watch_is_non_blocking_continuity_only():
    """The CAP-09 Slice 3 UX review observations stay a non-blocking WATCH with
    no repair cycle."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    s3 = watch[watch.index("**WATCH — CAP-09 Slice 3 (non-blocking, no repair cycle).**"):]
    s3 = s3[:s3.index("**WATCH — CAP-09 Slice 4")]
    for needle in ("Test Hypothesis stays planning metadata only",
                   "browser `<title>`", "wording polish only",
                   "`.user-hypothesis` does not", "visual consistency only",
                   "may reorder in the PDF renderer", "not a Slice-3 defect",
                   "no overflow and no material usability defect",
                   "comprehension review PASS — polish only",
                   "\"فرضية الاختبار (Test Hypothesis)\""):
        assert needle in s3, needle
    assert "Variable and Result stay NOT AUTHORIZED" not in s3


def test_cap09_slice_4_watch_is_non_blocking_continuity_only():
    """The CAP-09 Slice 4 UX review observations stay a non-blocking WATCH with
    no repair cycle."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    s4 = watch[watch.index("**WATCH — CAP-09 Slice 4 (non-blocking, no repair cycle).**"):]
    for needle in ("Test Variable / Condition stays opaque planning metadata; a formal "
                   "experimental variable model and Result stay NOT AUTHORIZED",
                   "(A) `UI_TITLE_SUCCESS`", "wording polish only",
                   "(B) Variable text keeps visible line breaks via pre-wrap",
                   "consistency polish only",
                   "(C) The identical save / clear guidance repeats for all four editable fields",
                   "no overflow and no material comprehension defect",
                   "(D) The intro's conceptual order differs from the card order",
                   "(E) At 390 px the two-row variable textarea can visually clip",
                   "placeholder only",
                   "(F) Adversarial neutral-heavy mixed-direction text may reorder",
                   "no Slice-4 repair cycle",
                   "\"متغيّر / شرط الاختبار (Test Variable / Condition)\""):
        assert needle in s4, needle


def test_cap11_watch_is_non_blocking_continuity_only():
    """The CAP-11 review observations stay a non-blocking WATCH with no repair
    cycle; LEGACY_UNSPECIFIED is never reclassified to remove the contrast."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    cap11 = watch[watch.index("**WATCH — CAP-11 Slice 1 (non-blocking, no repair cycle).**"):]
    for needle in ("Form, Source and Validation stay three independent axes; no combined score or "
                   "ranking is authorized",
                   "\"Source metadata not available\" beside a Known Mechanism showing \"You\"",
                   "do not reclassify LEGACY_UNSPECIFIED to remove the contrast",
                   "\"تقرير مباشر (Asserted)\"", "\"إفادة مباشرة\"", "language polish only",
                   "pre-existing language limitation, not a CAP-11 defect"):
        assert needle in cap11, needle
    assert "**Owner language policy (2026-09-27): Arabic-first UX, not Arabic-only terminology.**" \
        in watch


def test_cap02_watch_is_non_blocking_continuity_only():
    """The CAP-02 review observations stay a non-blocking WATCH with no repair
    cycle, and the ONE-primary-action rule is kept as a protected product rule."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    cap02 = watch[watch.index("**WATCH — CAP-02 Slice 1 (non-blocking, no repair cycle).**"):]
    for needle in ("Exactly ONE primary journey action stays a protected product rule",
                   "about 300 px lower on desktop", "below the first 390 px mobile viewport",
                   "do not undo the Compass now",
                   "still reads \"Next Development Step\" but lands on the Compass row \"Why it "
                   "matters now\"",
                   "\"What You Have Marked as Not Yet Known\"",
                   "\"Details for each open gap\"",
                   "\"Specialist input pending: 1\" before any answer",
                   "stay acceptable under the language policy above"):
        assert needle in cap02, needle
    assert "**Owner language policy (2026-09-27): Arabic-first UX, not Arabic-only terminology.**" \
        in watch


def test_arabic_first_language_policy_and_cap04_watch_are_continuity_only():
    """The Owner language policy — Arabic-first UX, not Arabic-only terminology —
    lives in the EXISTING CLAUDE.md language-direction owner and authorizes no
    live MSNL / LLM / provider use; the CAP-04 review observations stay a
    non-blocking WATCH with no repair cycle."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    lang = watch[watch.index("**NEXT TRIGGER — language direction.**"):
                 watch.index("**Preserved states.**")]
    for needle in (
            "**Owner language policy (2026-09-27): Arabic-first UX, not Arabic-only terminology.**",
            "Arabic UX chrome, navigation, explanatory prose and user guidance are normally Arabic",
            "MAY stay English where translation would reduce technical precision, "
            "recognizability, professional meaning or readability",
            "no forced literal translation for language purity",
            "First-use bilingual labeling is encouraged",
            "خطة التحقق (Validation Plan)",
            "Inventor-authored content stays verbatim",
            "WITHOUT silently changing canonical technical terminology or meaning",
            "The policy does NOT authorize live MSNL, LLM or provider use",
            "does not let long English explanatory prose replace Arabic UX"):
        assert needle in lang, needle
    for pat in (r"(?<!NOT )authori[sz]es? (live )?(MSNL|LLM|provider)",
                r"(?<!no )(?<!NOT )(live|external) (LLM|provider|MSNL) (use )?(is )?AUTHORIZED\b"):
        assert re.search(pat, lang) is None, pat
    cap04 = watch[watch.index("**WATCH — CAP-04 Slice 1 (non-blocking, no repair cycle).**"):]
    for needle in ("UNDETERMINED / clarifying information", "two responsibility lines",
                   "(\"Practical feasibility\")", "(\"Physical Feasibility\")",
                   "\"acquisition route\" may be jargon",
                   "do not replace the single Next Development Step",
                   "precise English technical terminology itself is not a defect"):
        assert needle in cap04, needle


def test_lead_operating_method_and_watchlist_are_preserved_as_continuity_only():
    """The Lead Operating Method (Product-Build First / Evidence-Driven) and the
    current Lead Watchlist live in CLAUDE.md as successor continuity: every rule
    is present, the successor rule binds, and every deferred / trigger-based item
    stays deferred — none is read as authorized."""
    raw = _read("CLAUDE.md")
    assert "\n### Lead Operating Method — Product-Build First / Evidence-Driven\n" in raw
    claude = re.sub(r"\s+", " ", raw)
    method = claude[claude.index("### Lead Operating Method"):
                    claude.index("## Historical material and substantive boundaries")]
    for needle in (
            "It adds no authority level, boot step, approval gate or implementation "
            "authorization",
            "**A. Product-Build First.**", "**B. Evidence-driven sequencing.**",
            "The Master Roadmap is navigation, not automatic execution order",
            "**C. Meaningful vertical slices.**", "**D. Quality is preserved.**",
            "never weakens truthfulness, security, mandatory CI, required testing or "
            "material independent review",
            "**E. Review routing by material risk.**", "No reviewer is added ritually",
            "**F. No reopening without new evidence.**", "**G. No review recursion.**",
            "**H. Immutable reviewed candidate.**", "**I. Test proportionality.**",
            "never FULL for reassurance",
            "The newest mandatory hosted CI on the exact final PR head stays authoritative",
            "**J. C1-Lite** is advisory developer tooling, not a merge gate",
            "FP-01 / FP-02 / FP-15", "`superseded_by is None`",
            "**K. Success metric.**",
            "PR, document and test counts alone are not product progress",
            "**L. Successor rule.** A successor Lead MUST reconstruct and follow this "
            "Operating Method before choosing its first new action",
            "without new material evidence or a new Owner decision"):
        assert needle in method, needle
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    for needle in (
            "none of it authorizes work", "RIG (advisory only; FULL and mandatory CI keep "
            "authority)", "**RIG-3A PREMATURE / BLOCKED** under the current file-level topology",
            "RIG-4 DEFERRED / PREMATURE", "RIG-6 NOT READY",
            "**RIG-7 MCP read interface DEFERRED, NOT CANCELLED.**",
            "RIG-8 living project knowledge and RIG-9 optional wiki / visual layer FUTURE / "
            "TRIGGER-BASED", "No separate RIG-R roadmap",
            "**C1-Lite** DELIVERED / ADVISORY",
            "**Acceleration-window C2** — deeper Agent Context / RIG-5 integration after "
            "C1-Lite, not any older identifier named C2 — DEFERRED, NOT CANCELLED",
            "The Acceleration Window is CLOSED",
            "**MCP** implementation DEFERRED; trigger NOT FOUND; authorization NO",
            "no generic command execution",
            "**NEXT TRIGGER — shared declared-action primitive.**",
            "Evaluation only; a capability without such a write path does not fire it",
            "**NEXT TRIGGER — analytical relationship primitive.**",
            "No generic graph in advance; separate from the declared-action trigger",
            "**NEXT TRIGGER — language direction.**",
            "proves no general dialect support", "CURRENT LIMITATION",
            "no universal-dialect claim",
            "It never gains authority over canonical technical concepts, readiness, validation, "
            "feasibility, progression, state mutation, evidence promotion or decision selection",
            "fails closed to the deterministic fallback",
            "External / provider MSNL and any external transmission of real invention, project "
            "or user data remain NOT AUTHORIZED",
            # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1: full CAP-12 stays NOT AUTHORIZED
            "FULL CAP-12 NOT AUTHORIZED and CAP-13 NOT ACTIVATED, distinct",
            "**WATCH — Stage 22 Slice 2 (non-blocking, no repair cycle).**"):
        assert needle in watch, needle
    for pat in (r"MCP (implementation )?(is )?AUTHORIZED\b(?<!NOT AUTHORIZED)",
                r"RIG-3A (is )?(READY|AUTHORIZED|ACTIVE)\b",
                r"(C2|RIG-7|MCP)[^.]{0,20}\bCANCELLED\b(?<!NOT CANCELLED)",
                r"(?<!no )(?<!NOT )(live|external) (LLM|provider|MSNL) (is )?AUTHORIZED\b"):
        assert re.search(pat, watch) is None, pat


def test_continuity_addendum_lenses_cap06_and_fraud_routing_authorize_nothing():
    """Continuity addendum: the three product-deepening axes and the
    Domain Profile → … → Readiness direction are a lens, not authority; the
    BUILD … SHIP lens is non-gating; FULL CAP-06 is PREMATURE / NOT AUTHORIZED NOW (the bounded four-axis
    Stage-23 scope is delivered) and
    not cancelled; production abuse / fraud routes through the EXISTING PSRR /
    Stage 38 / Stage 40 owners with no new gate, no provider selection and no
    deployment, payment or paid-activation authority."""
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    method = claude[claude.index("### Lead Operating Method"):
                    claude.index("## Historical material and substantive boundaries")]
    for needle in (
            "**M. Product-deepening lens (direction, not authority).**",
            "**technical deepening**", "**analytical deepening**", "**domain extensibility**",
            "not its permanent ceiling",
            "Domain Profile → Technical Deepening → Analytical Deepening → Evidence / "
            "Validation → Decisions → Readiness",
            "it authorizes no generic graph, new domain, new schema, CAP-06, CAP-11, CAP-12, "
            "CAP-13 or any other capability",
            "**N. Sequencing lens (non-gating).**",
            "BUILD, DEEPEN, CONNECT, SIMPLIFY, ACCELERATE, PROVE, SCALE or SHIP",
            "no fixed sequence and no approval gate"):
        assert needle in method, needle
    watch = claude[claude.index("**Current Lead Watchlist (2026-09-26).**"):
                   claude.index("**Successor Lead (mandatory).**")]
    for needle in (
            # AMENDED at the Stage 23 closure: the bounded four-axis scope is delivered; FULL CAP-06 stays premature
            "**CAP-06 — Multi-Axis Invention Readiness Dashboard: the CURRENT bounded four-axis Stage-23 scope is "
            "DELIVERED / COMPLETE; FULL CAP-06 stays PREMATURE / NOT AUTHORIZED NOW, not cancelled.**",
            "The full eight-axis CAP-06 expansion",
            "CAP-11 evidence strength, Patent Export / patent-disclosure readiness, "
            "WS-PFV-001 / prototype readiness",
            "Build no misleading partial \"full dashboard\"",
            "**Production abuse / fraud — routed through the EXISTING PSRR + Stage 38 + Stage 40 "
            "owners; no new workstream or gate.**",
            "credential stuffing", "chargeback / dispute responsibility",
            "GitHub / CI protects code-change and merge integrity and does not replace "
            "application security",
            "InventorAI keeps authorization, project / account ownership, session security",
            "No provider is selected; no payment implementation, deployment, public release or "
            "paid activation is authorized"):
        assert needle in watch, needle
    negation = ("No provider is selected; no payment implementation, deployment, public release "
                "or paid activation is authorized")
    claims = watch.replace(negation, "")
    for pat in (r"CAP-06[^.]{0,40}\bCANCELLED\b(?<!not cancelled)",
                r"(?<!no )(?<!NOT )(payment|deployment|paid activation) (is )?authorized\b"):
        assert re.search(pat, claims, re.I) is None, pat
    rows = re.findall(r"^- \[ \] \*\*40 — Payment provider:\*\*.*$", _read(ROADMAP), re.M)
    assert len(rows) == 1
    assert ("the existing PSRR / Stage-38 / Stage-40 path must explicitly account for the "
            "production-abuse / fraud surface") in rows[0]
    assert "no new gate, no provider selected, nothing authorized" in rows[0]


# ==========================================================================
# LIVE MATERIAL INVARIANTS — merge-invariant current-authority truth
#
# One slice-agnostic owner of what must be true on every live authority surface,
# whatever delivery is current: exactly one live declaration, one consistent
# active contract across every surface, correct Stage 15 / 18 status and
# sequential marker, and no false completion, compatibility, verification, IRL,
# deployment / release, successor or domain claim. It reads no PR number, SHA,
# ancestry, review verdict or post-merge result, and it forbids the pre-merge
# lifecycle wording that becomes false the moment a candidate merges — so an
# implementation candidate carries its own final-state truth and a merge alone
# never needs a follow-up current-truth PR.
# ==========================================================================
_LIVE_CLAIM_REVERSALS = _S15_CLOSE_REVERSALS + (
    r"\bIRL (score|scoring) (is |was |has been )?(assigned|computed|achieved)",
    r"(?<!no )(?<!not )(the )?interactions? (is|are|was|were|has been|have been) (verified|validated|checked)\b",
    r"(?<!no )(?<!not )compatibility (is|was|has been) (established|verified|confirmed)\b",
    r"ENGINEERING COMPATIBILITY ANALYSIS: AUTHORIZED",
    r"FULL CAP-01 / FULL STG: AUTHORIZED",
    r"(IOT|DRONE|RENEWABLE|SATELLITE)[^`.;]{0,60}: AUTHORIZED",
    r"NEW DOMAIN ACTIVATION: AUTHORIZED",
    r"(?<!no )(?<!not )new domain activation (is |was )?authorized",
    # AMENDED at the Stage 19 closure: the live marker was Stage 20; AMENDED again at the Stage 20 closure: the live
    # marker is Stage 21. A preserved delivery heading may still close with "(…; the … MARKER stays Stage 18)" or
    # "(…; the … MARKER moves to Stage 19 / 20 for navigation only)".
    # AMENDED again at the Stage 21 closure: the live marker was Stage 22; AMENDED again at the Stage 22 closure: the
    # live marker was Stage 23 (NOT ENTERED); AMENDED again at the Stage 23 closure: the live marker is Stage 24 (NOT
    # ENTERED), and the preserved Stage 28 / 30 delivery headings still read "… MARKER stays Stage 23 …".
    # AMENDED again at the Stage 24 closure: the live marker is Stage 25 (NOT ENTERED); the preserved Stage 23 closure
    # heading still reads "… MARKER moves to Stage 24 for navigation only)".
    r"CURRENT MASTER ROADMAP STAGE: Stage (?!25\b)\d+",
    r"MASTER ROADMAP SEQUENTIAL MARKER(?::| is| moves to| becomes)? Stage (?!25\b)\d+\b(?! for navigation only\))",
    r"MASTER ROADMAP SEQUENTIAL MARKER stays Stage (?!2[34]\b)\d+\b(?!\))",
    _S4_VERDICT, r"INTERFACE OBSERVATION VERDICT / CRITERION-MET JUDGEMENT: AUTHORIZED") + _S35C_REVERSALS + (
    _S36C_REVERSALS + _S16C_REVERSALS)
# Lifecycle states that are true only BEFORE a merge. On a live surface they make the authoritative
# text false the moment the candidate merges, which is what used to force a closure PR.
_PREMERGE_LIFECYCLE = (
    r"\bIMPLEMENTATION (COMPLETE )?CANDIDATE\b", r"\bIMPLEMENTED CANDIDATE\b", r"\bIN CANDIDATE\b",
    r"\bPR NOT OPENED\b", r"\bMERGE NOT PERFORMED\b", r"\bNOT MERGED\b", r"\bPR PENDING\b",
    r"\bPR / MERGE PENDING\b", r"\bREVIEW (IS )?PENDING\b", r"\bcurrent bounded product action\b",
    r"\bCURRENT REVIEWED PRODUCT HEAD\b")
_ACTIVE_BOLD = r"\*\*ACTIVE CONTRACT: ([^*]+?)\.\*\*"
_ACTIVE_TOKEN = r"`ACTIVE CONTRACT: ([^`]+)`"


# ---- F1: every `## Current authority` record is classified by its own repository wording ----------
# A record runs from one `## Current authority` heading to the NEXT `## Current authority` heading (or
# EOF): ordinary `##` headings inside that interval stay part of the record and are inspected with it.
# A record is HISTORICAL only when its OWN heading ends with an affirmative status segment in the
# repository's heading convention — " — DELIVERED[ (…)][; SUPERSEDED as current authority by …]",
# " — SUPERSEDED (<date>) by …" or " — SUPERSEDED FOR PRESENT ROUTING BY …"; a negated or referential
# SUPERSEDED ("NOT SUPERSEDED", "(previous mandate SUPERSEDED)") is not a status. Ten declarations
# written before that convention are allowed ONLY under their exact existing heading, each exactly once
# and never first. Every other record is LIVE, and exactly one LIVE record — the first — must exist; an
# extra, unclassifiable record fails closed.
_HISTORICAL_HEADING = (r" — (?:DELIVERED(?: \([^)]*\))?(?:; SUPERSEDED as current authority by .+)?"
                       r"|SUPERSEDED \(\d{4}-\d{2}-\d{2}\) by .+|SUPERSEDED FOR PRESENT ROUTING BY .+)$")
_LEGACY_UNMARKED_AUTHORITY_HEADINGS = frozenset({
    "## Current authority — Stage 10 / T2-C′ differential product-value assessment (Owner acceptance, 2026-09-20)",
    "## Current authority — post-PR-664 declaration (v1.32 synchronization, 2026-09-19)",
    "## Current authority — MG-8: truthful capture of the seed problem statement",
    "## Current authority — T3-A \"Project record\": narrowed input-history rendering",
    "## Current authority — T2-G legacy migration: explicit confirmed adoption",
    "## Current authority — T2-D contextual question feedback (Stage 6)",
    "## Current authority — T2-G partial versioned mechanism slice (Stage 7)",
    "## Current authority — T2-G-2 concise and mixed mechanism explanations (Stage 7)",
    "## Current authority — T2-E Option B + T2-F (one combined bounded candidate)",
    "## Current authority — T1-D + residual T2-B′ (one combined bounded candidate)",
})


def _authority_sections(contract):
    """[(heading, flattened record, kind)] for EVERY `## Current authority` record, in file order; kind
    is "live", "historical" or "legacy". A record ends only at the next `## Current authority` heading
    or EOF, never at an ordinary `##` heading."""
    starts = [m.start() for m in re.finditer(r"^## Current authority", contract, re.M)] + [len(contract)]
    sections = []
    for s, e in zip(starts, starts[1:]):
        heading = contract[s:contract.index("\n", s)]
        kind = ("historical" if re.search(_HISTORICAL_HEADING, heading)
                else "legacy" if heading in _LEGACY_UNMARKED_AUTHORITY_HEADINGS else "live")
        sections.append((heading, re.sub(r"\s+", " ", contract[s:e]), kind))
    return sections


def _live_declaration(contract):
    """(heading, flattened section) of the ONE live authority section; ValueError otherwise."""
    sections = _authority_sections(contract)
    live = [s for s in sections if s[2] == "live"]
    if len(live) != 1:
        raise ValueError("%d live current-authority sections, exactly one required: %s"
                         % (len(live), [s[0] for s in live]))
    if not sections or sections[0][2] != "live":
        raise ValueError("the first current-authority section is not the live one")
    legacy = [s[0] for s in sections if s[2] == "legacy"]
    if len(legacy) != len(set(legacy)):
        raise ValueError("a legacy authority heading is duplicated")
    return live[0][0], live[0][1]


# ---- F2: no newly authored post-merge / post-integration success claim on a live surface ----------
# A candidate carries the durable final-state truth, but it cannot truthfully claim that its merge or
# post-merge verification has already happened; that evidence belongs to Git/GitHub and a read-only
# check. Every such claim on a live surface must be a LEGACY claim, owned by its complete preserved
# record: on the same live surface, the whole delivery record that carries it (transient PR / merge
# identity ignored) plus the COMPLETE claim must be exactly one of the records below, and no more often
# than it occurs there. A record starts only at a structural boundary — a list separator, a table cell,
# a sentence end or (prose) a clause end — never at Markdown emphasis, so a new subject, a plain or
# formatted wrapper ("This candidate:", "**New delivery:**") or a borrowed tail of an old subject stays
# in the record and fails. A claim runs to its closing backtick (token) or its clause end (prose), so a
# trailing qualifier ("PASS for New delivery Omega") stays in the claim and fails. Omission is always
# valid; nothing requires the wording.
_POST_MERGE_CLAIM = (r"\bPOST[- ](?:MERGE|INTEGRATION)\b[^.;`()]{0,60}?\b(?:PASS(?:ED)?|VERIFIED|CONFIRMED|"
                     r"SUCCEEDED)\b|\b(?:MERGE|INTEGRATION)(?: IDENTITY)? VERIFICATION\s*:\s*PASS\b|"
                     r"\b(?:MERGED?|INTEGRAT(?:ED|ION)) (?:AND |& )?(?:VERIFIED|CONFIRMED)\b")
_RECORD_SEPARATORS = (" · ", " | ", ". ")
_SENTENCE_SEPARATORS = ("; ",)
_CLAUSE_ENDS = (";", ")", ". ", " · ", " | ")
_PM_TOKEN = " · `POST-MERGE IDENTITY / CONTENT VERIFICATION: PASS`"
_PM_PROSE = "post-merge identity / content verification PASS"
_S15_DELIVERED_HEADING = " (a bounded {} the already-open Stage-15 integration obligation; no new Master Roadmap Stage; the " \
            "MASTER ROADMAP SEQUENTIAL MARKER stays Stage 18):** "
_S18_DELIVERED_HEADING = " (inside Stage 18; no new Master Roadmap Stage):** "
_CAP01_RECORDS = {
    "`FIRST BOUNDED CAP-01 INCREMENT: OWNER-AUTHORIZED` · `IMPLEMENTED / MERGED / POST-MERGE VERIFIED`": 1,
    "`SECOND BOUNDED CAP-01 RESEARCH-DIRECTION INCREMENT: OWNER-AUTHORIZED / IMPLEMENTED / MERGED / POST-MERGE "
    "VERIFIED`": 1,
    "`STAGE 15 SLICE 1: DELIVERED`" + _PM_TOKEN: 1,
    "`STAGE 15 SLICE 2: DELIVERED`" + _PM_TOKEN: 1,
}
_ROUTING_RECORDS = dict(_CAP01_RECORDS, **{
    "**DELIVERED — Stage 15 / Subsystem Interface Declaration & Verification Preparation — Slice 2"
    + _S15_DELIVERED_HEADING.format("continuation inside") + "`STAGE 15 SLICE 2: DELIVERED`" + _PM_TOKEN: 1,
    "**DELIVERED — Stage 15 / Integrated Invention Entry & Durable Subsystem Composition — Slice 1"
    + _S15_DELIVERED_HEADING.format("re-entry into") + "`STAGE 15 SLICE 1: DELIVERED`" + _PM_TOKEN: 1,
    "**DELIVERED — Stage 18 / Electrical / Electronics Technical Deepening Slice 1 — Basic Electrical Reference "
    "Fundamentals" + _S18_DELIVERED_HEADING + "`ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1: DELIVERED`" + _PM_TOKEN: 1,
    "**DELIVERED — Stage 18 / Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals"
    + _S18_DELIVERED_HEADING + "`MECHANICAL TECHNICAL DEEPENING SLICE 1: DELIVERED`" + _PM_TOKEN: 1,
    "**DELIVERED — Stage 18 / Mechanical CAP-01 — Open-Gap Technical Context" + _S18_DELIVERED_HEADING
    + "`MECHANICAL CAP-01 OPEN-GAP TECHNICAL CONTEXT: DELIVERED`" + _PM_TOKEN: 1,
})
_LEGACY_POST_MERGE_RECORDS = {
    "routing:" + ROADMAP: _ROUTING_RECORDS,
    "routing:" + CHECKLIST: _ROUTING_RECORDS,
    "routing:" + CONTRACT: _ROUTING_RECORDS,
    "declaration:" + CONTRACT: {
        "`STAGE 15 SLICE 1: DELIVERED`" + _PM_TOKEN: 1,
        "`STAGE 15 SLICE 2: DELIVERED`" + _PM_TOKEN: 1,
        # the post-Stage-15-Slice-3 declaration's Slice-2 row carries no post-merge claim (its token line
        # still does, preserved from the post-PR-#720 declaration)
    },
    "position:" + STATE: dict(_CAP01_RECORDS, **{
        "`ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1: DELIVERED`" + _PM_TOKEN: 1,
        "`MECHANICAL TECHNICAL DEEPENING SLICE 1: DELIVERED`" + _PM_TOKEN: 1,
        "Stage 15 — Subsystem Interface Declaration & Verification Preparation — Slice 2 — delivered, " + _PM_PROSE: 1,
        "Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1 — delivered, " + _PM_PROSE: 1,
        "Electrical / Electronics Technical Deepening Slice 1 — Basic Electrical Reference Fundamentals — "
        "delivered, " + _PM_PROSE: 1,
        "Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals — delivered, " + _PM_PROSE: 1,
    }),
    "head:CLAUDE.md": {
        "The preceding bounded slice — Stage 15 — Subsystem Interface Declaration & "
        "Verification Preparation — Slice 2 — is DELIVERED (" + _PM_PROSE: 1,
        "Stage 15 — Integrated Invention Entry & Durable Subsystem Composition — Slice 1 is DELIVERED ("
        + _PM_PROSE: 1,
        "Electrical / Electronics Technical Deepening Slice 1 — Basic Electrical Reference Fundamentals — is "
        "DELIVERED (" + _PM_PROSE: 1,
        "Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals — DELIVERED ("
        + _PM_PROSE: 1,
        "Mechanical CAP-01 — Open-Gap Technical Context — DELIVERED (" + _PM_PROSE: 1,
    },
}


def _claim_record(before):
    """The complete delivery record a claim at the end of `before` belongs to. A claim inside a backticked
    token belongs to that token's record; a claim token without a subject (`…MERGED / …` or a bare PASS
    token) also owns the complete token before it. A token record starts only at a list / table
    separator or a sentence end; a prose record may also start at a clause boundary (`; `). Markdown
    emphasis is never a boundary, so formatted wrapper text stays in the record."""
    cut, token = len(before), before.count("`") % 2 == 1
    if token:
        cut = before.rfind("`")
        if ":" not in before[cut:]:
            prev = re.search(r"`[^`]*` · $", before[:cut])
            if prev:
                cut = prev.start()
    separators = _RECORD_SEPARATORS if token else _RECORD_SEPARATORS + _SENTENCE_SEPARATORS
    starts = [before.rfind(s, 0, cut) + len(s) for s in separators if before.rfind(s, 0, cut) != -1]
    return before[max(starts, default=0):]


def _without_transient_identity(text):
    """Flattened text with PR numbers / merge SHAs removed from delivery records."""
    text = re.sub(r"\s+—\s+PR\s+#\d+\s+—\s+merge\s+[0-9a-f]{40}", "", text)
    return re.sub(r"PR #\d+,? \(?merge `[0-9a-f]{40}`;\s*", "", text)


def _claim_end(flat, m):
    """End of the COMPLETE claim that `m` starts: its semantic clause end. A closing backtick is only
    formatting — it never ends the claim — so a claim inside a token runs through that backtick AND on
    to the next clause boundary, and any trailing qualifier (inside or after the token) belongs to it."""
    start = m.end()
    if flat[:m.start()].count("`") % 2:
        close = flat.find("`", m.end())
        start = len(flat) if close == -1 else close + 1
    ends = [flat.find(s, start) for s in _CLAUSE_ENDS]
    return min((e for e in ends if e != -1), default=len(flat))


def _unsupported_post_merge_claims(texts):
    problems, used = [], {}
    for label, text in texts.items():
        flat = _without_transient_identity(text)
        allowed = _LEGACY_POST_MERGE_RECORDS.get(label, {})
        for m in re.finditer(_POST_MERGE_CLAIM, flat, re.I):
            record = _claim_record(flat[:m.start()]) + flat[m.start():_claim_end(flat, m)]
            if record not in allowed:
                problems.append("%s: unsupported post-merge success claim in record %r" % (label, record))
            else:
                used[(label, record)] = used.get((label, record), 0) + 1
    for (label, record), count in used.items():
        if count > _LEGACY_POST_MERGE_RECORDS[label][record]:
            problems.append("%s: legacy post-merge record %r repeated %d times (preserved record: %d)"
                            % (label, record, count, _LEGACY_POST_MERGE_RECORDS[label][record]))
    return problems


def _fenced_text(raw, name):
    o, c = _OPEN % name, _CLOSE % name
    if raw.count(o) != 1 or raw.count(c) != 1:
        raise ValueError(name + " fence is not unique")
    i = raw.index(o) + len(o)
    return re.sub(r"\s+", " ", raw[i:raw.index(c, i)])


def _live_authority_texts(read):
    """{label: live text} for every current-authority surface, superseded notes removed."""
    texts = {"routing:" + path: _live_only(_fenced_text(read(path), "current-routing"))
             for path in (ROADMAP, CHECKLIST, CONTRACT)}
    texts["position:" + STATE] = _live_only(_fenced_text(read(STATE), "current-position"))
    heading, declaration = _live_declaration(read(CONTRACT))
    texts["heading:" + CONTRACT] = heading
    texts["declaration:" + CONTRACT] = _live_only(declaration)
    claude = re.sub(r"\s+", " ", read("CLAUDE.md"))
    texts["head:CLAUDE.md"] = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    return texts


def _live_authority_problems(read=None):
    """Every material live-authority violation; [] when the live truth holds."""
    try:
        texts = _live_authority_texts(read or _read)
    except ValueError as exc:
        return ["live authority structure unreadable: %s" % exc]
    problems = []
    heading = texts.pop("heading:" + CONTRACT)
    if re.search(r"SUPERSEDED|DELIVERED", heading):
        problems.append("the first current-authority section is marked as history: " + heading)
    declared = re.findall(_ACTIVE_BOLD, texts["declaration:" + CONTRACT])
    if len(declared) != 1:
        problems.append("the live contract section holds %d declarations, not exactly one" % len(declared))
    current = declared[0] if len(declared) == 1 else None
    if re.findall(_ACTIVE_BOLD, texts["head:CLAUDE.md"]) != [current]:
        problems.append("CLAUDE.md does not declare the same single active contract")
    fenced = [label for label in texts if label.split(":")[0] in ("routing", "position", "declaration")]
    for label in fenced:
        text = texts[label]
        tokens = set(re.findall(_ACTIVE_TOKEN, text))
        if tokens != {current}:
            problems.append("%s: active-contract tokens %s disagree with %r" % (label, sorted(tokens), current))
        if current == "NONE" and "`NEXT PRODUCT INCREMENT: NOT AUTHORIZED`" not in text:
            problems.append(label + ": NONE without `NEXT PRODUCT INCREMENT: NOT AUTHORIZED`")
        for token in (_S23_COMPLETE, _S22_COMPLETE, _S21_COMPLETE, _S20_COMPLETE, _S19_COMPLETE, _S18_COMPLETE,
                      _S15_COMPLETE, _S25_MARKER, _NO_S25, *_S23_LIMITS,
                      # AMENDED at the delivered CAP-12 Form Mock-up Advisory Slice 1; AMENDED at the Stage 24 closure
                      _S24_DELIVERED, _S24C_DELIVERED, _S24_COMPLETE, *_S24C_LIMITS):
            if token not in text:
                problems.append(label + ": missing " + token)
        if _S15_ENTERED in text:
            problems.append(label + ": stale " + _S15_ENTERED)
        for pat in _S18C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-18-closure status " + pat)
        for pat in _S19C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-19-closure status " + pat)
        for pat in _S20C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-20-closure status " + pat)
        for pat in _S21C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-21-closure status " + pat)
        for pat in _S22C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-22-closure status " + pat)
        for pat in _S23C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-23-closure status " + pat)
        for pat in _S24C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-24-Slice-1 status " + pat)
        for pat in _S24CL_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-24-closure status " + pat)
        for token in _S30C_TOKENS + _S30C_KEPT:
            if token not in text:
                problems.append(label + ": missing Stage-30 closure fact " + token)
        for pat in _S30C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-30-closure status " + pat)
        if label.startswith("routing") and not re.search(r"(?i)CURRENT MASTER ROADMAP STAGE: Stage 25\b", text):
            problems.append(label + ": the Stage-25 navigation marker is missing")
        # ADVANCED at the Stage 35 first bounded slice: every surface carried the Stage-35 status and limits
        # ADVANCED at the Stage 35 closure: every surface carries the live next step, the Stage-35 closure facts,
        # limits and preserved triggers, the Stage-36 exclusion, and none of the retired Stage-35 active-increment
        # wording (the NONE token and the next-increment exclusion are checked above)
        for token in (_NEXT_STAGE_STEP,) + _S35C_FACTS:
            if token not in text:
                problems.append(label + ": missing Stage-35 closure fact " + token)
        for pat in _S35C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale Stage-35 active-increment wording " + pat)
        # ADVANCED at the Stage 36 closure: every surface carries the Stage-36 closure facts, limits and the Stage-37
        # exclusion, and none of the Stage 35 closure's retired Stage-36 NOT-ENTERED wording
        for token in _S36C_FACTS:
            if token not in text:
                problems.append(label + ": missing Stage-36 closure fact " + token)
        for pat in _S36C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-36-closure wording " + pat)
        # ADVANCED at the Stage 16 closure: every surface carries the Stage-16 closure facts, the SRL exclusion and the
        # Stage-13 / Stage-14 PARTIAL / DEFERRED status, and none of the pre-Stage-16-closure wording
        for token in _S16C_FACTS:
            if token not in text:
                problems.append(label + ": missing Stage-16 closure fact " + token)
        for pat in _S16C_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-16-closure wording " + pat)
        # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: every surface carries its
        # delivered / ENTERED / PARTIAL facts and none of the pre-slice Stage-25 NOT-ENTERED wording
        for token in _S25_FACTS:
            if token not in text:
                problems.append(label + ": missing Stage-25 slice fact " + token)
        for pat in _S25_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-25-slice wording " + pat)
        # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: every surface carries
        # its delivered / ENTERED / PARTIAL facts and none of the pre-slice NONE or Stage-27 NOT-ENTERED wording
        for token in _S27_FACTS:
            if token not in text:
                problems.append(label + ": missing Stage-27 slice fact " + token)
        for pat in _S27_STALE:
            if re.search(pat, text):
                problems.append(label + ": stale pre-Stage-27-slice wording " + pat)
    for needle in (*_S27_FACTS, *_S25_FACTS, "NO STAGE-25 IMPLEMENTATION AUTHORIZED BY STAGE-24 CLOSURE",
                   "NO STAGE-24 IMPLEMENTATION AUTHORIZED BY STAGE-23 CLOSURE", _S23_COMPLETE,
                   _S23C_DELIVERED, *_S23_LIMITS,
                   "STAGE 22: COMPLETE — CURRENT BOUNDED DECISION TRACE + DECISION ROOM SCOPE",
                   "STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE",
                   "STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE",
                   "STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE", *_S30C_TOKENS, *_S30C_KEPT,
                   _S24_DELIVERED, _S24C_DELIVERED, _S24_COMPLETE, *_S24C_LIMITS, *_S35C_FACTS, _NEXT_INC_NO,
                   _NEXT_STAGE_STEP, *_S36C_FACTS, *_S16C_FACTS):
        if needle not in texts["head:CLAUDE.md"]:
            problems.append("head:CLAUDE.md: missing " + needle)
    for pat in _S16C_STALE:
        if re.search(pat, texts["head:CLAUDE.md"]):
            problems.append("head:CLAUDE.md: stale pre-Stage-16-closure wording " + pat)
    for pat in _S25_STALE:
        if re.search(pat, texts["head:CLAUDE.md"]):
            problems.append("head:CLAUDE.md: stale pre-Stage-25-slice wording " + pat)
    for pat in _S27_STALE:
        if re.search(pat, texts["head:CLAUDE.md"]):
            problems.append("head:CLAUDE.md: stale pre-Stage-27-slice wording " + pat)
    for pat in _S36C_STALE:
        if re.search(pat, texts["head:CLAUDE.md"]):
            problems.append("head:CLAUDE.md: stale pre-Stage-36-closure wording " + pat)
    for pat in _S35C_STALE:
        if re.search(pat, texts["head:CLAUDE.md"]):
            problems.append("head:CLAUDE.md: stale Stage-35 active-increment wording " + pat)
    for pat in _S23C_STALE + _S24C_STALE + _S24CL_STALE:
        if re.search(pat, texts["head:CLAUDE.md"]):
            problems.append("head:CLAUDE.md: stale pre-Stage-23-closure / pre-Stage-24 status " + pat)
    for pat in _S30C_STALE:
        if re.search(pat, texts["head:CLAUDE.md"]):
            problems.append("head:CLAUDE.md: stale pre-Stage-30-closure status " + pat)
    for label, text in texts.items():
        # ADVANCED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: its reversals are live claims
        # ADVANCED at the delivered Stage 27 / THERM-01 Single-Path Temperature-Difference Slice 1: so are its reversals
        for pat in _LIVE_CLAIM_REVERSALS + _PREMERGE_LIFECYCLE + _S25_REVERSALS + _S27_REVERSALS:
            m = re.search(pat, text, re.I | re.S)
            if m:
                problems.append("%s: forbidden live claim %r" % (label, m.group(0)))
    return problems + _unsupported_post_merge_claims(texts)


def test_live_material_invariants_hold():
    assert _live_authority_problems() == []


def test_stage30_closure_is_scope_qualified_and_discharges_nothing_else():
    """The Stage 30 closure ticks row 30 for the current optional-part enablement safeguard scope ONLY, records it as
    NO global discharge (a future domain or root activation needs a new proportional reassessment) and keeps the
    safety exclusion as the current bounded disposition, not a prohibition; Stage 28 stays unticked; the part-only
    allowlist stays empty in the engine source; every replaced live statement survives as a superseded note. The
    same facts on every live surface are enforced by _live_authority_problems above."""
    roadmap = _read(ROADMAP)
    rows = re.findall(r"^- \[x\] \*\*30 — Cross-domain safeguards:\*\*.*$", roadmap, re.M)
    assert len(rows) == 1, "the Stage 30 checkbox is not ticked"
    for needle in ("checkbox ticked for that scope only:** " + _S30_COMPLETE, *_S30C_TOKENS,
                   "needs a NEW proportional Stage-30 reassessment at that future gate; no universal waiver",
                   "part enablement needed its own exact Owner authorization"):
        assert needle in rows[0], needle
    # ADVANCED at the Stage 28 closure: row 28 is ticked for its bounded optional-part scope only
    assert re.search(r"^- \[x\] \*\*28 — Additional-domain program:\*\*", roadmap, re.M), "Stage 28 row"
    assert ("Stage 30 is COMPLETE for the current " + _CL.lower() + " part-enablement safeguard scope only — checkbox "
            "ticked for that scope only — and NOT globally discharged") in _flat(ROADMAP)
    # ADVANCED at the Stage 28 part-only enablement: the allowlist lists exactly the optional part
    assert re.search(r'^_PART_ONLY_DOMAINS = frozenset\(\{"' + _CL.lower().replace("-", "_") + r'"\}\)$',
                     _read("engine/domain_activation.py"), re.M)
    note = ("*(Superseded 2026-10-02 by Stage 30 — " + _CL.title() + " Part-Enablement Safeguards — Closure, preserved "
            "so the change is visible rather than silent: the ")
    for path in (ROADMAP, CHECKLIST, CONTRACT):
        assert note + "current routing read \"**NO ACTIVE CONTRACT — post-Stage-30-Part-Safeguards-Slice-1" in _after_fence(
            path, "current-routing"), path
    assert note + "current-position entry read" in _after_fence(STATE, "current-position")


_LIVE_DOCS = (ROADMAP, CHECKLIST, CONTRACT, STATE, CAPABILITIES, "CLAUDE.md")


def _other_identity(raw):
    """The same text with every PR number and 40-hex identity replaced by a different one."""
    raw = re.sub(r"\b[0-9a-f]{40}\b", lambda m: hashlib.sha1(m.group(0).encode()).hexdigest(), raw)
    return re.sub(r"(PR ?-?#)(\d+)", lambda m: m.group(1) + "9" + m.group(2), raw)


def _without_identity(raw):
    """The same text written the way a candidate writes it: delivered status tokens and lines carry no
    PR / merge identity."""
    return re.sub(r" — PR #\d+ — merge [0-9a-f]{40}(?=`|$)", "", raw, flags=re.M)


@pytest.mark.parametrize("transform", [_other_identity, _without_identity], ids=["changed", "absent"])
def test_transient_identity_is_never_a_live_prerequisite(monkeypatch, transform):
    """Changing or omitting every PR number / SHA on every live document changes no live verdict, so
    recording the identity a merge creates never needs a repository current-truth mutation."""
    real = _read
    docs = {path: transform(real(path)) for path in _LIVE_DOCS}
    assert docs[CONTRACT] != real(CONTRACT)
    fake = lambda path: docs[path] if path in docs else real(path)       # noqa: E731
    assert _live_authority_problems(fake) == []
    monkeypatch.setattr(sys.modules[__name__], "_read", fake)
    test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()
    assert _live_authority_problems() == []


def _span(raw, region):
    if region == "head":
        return 0, raw.index("*(Superseded")
    if region == "declaration":
        i = raw.index("## Current authority")
        return i, raw.index("\n## Current authority", i + 5)
    i = raw.index(_OPEN % region)
    return i, raw.index(_CLOSE % region, i)


def _mutate(path, region, old, new, every=None):
    raw = _read(path)
    i, j = _span(raw, region)
    k = raw.find(old, i, j)
    assert k != -1, (path, region, old)
    if every == "all":                   # replace every occurrence inside the region
        return {path: raw[:i] + raw[i:j].replace(old, new) + raw[j:]}
    return {path: raw[:k] + new + raw[k + len(old):]}


# ROTATED at the Stage 35 first bounded slice: the routing / position / declaration anchor was the live Stage-35 status
# token and the head / declaration anchor the live Stage-35 bold declaration
# ROTATED back at the Stage 35 closure: the routing / position / declaration anchor is the live
# `NEXT STEP: LEAD-CONTROLLED NEXT-STAGE CLOSURE REASSESSMENT` token again and the head / declaration anchor is the live
# `**ACTIVE CONTRACT: NONE.**`
_NS = _NEXT_STAGE_STEP
