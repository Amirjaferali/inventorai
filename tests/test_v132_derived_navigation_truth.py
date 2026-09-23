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
"""
import os
import re

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


def test_stage_eighteen_is_entered_and_still_completes_nothing():
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
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "routing",
               r"(?i)CURRENT MASTER ROADMAP STAGE: Stage 18",
               r"`STAGE 18 STARTED: YES`",
               r"`STAGE 18 COMPLETE: NO`",
               r"`FIRST BOUNDED CAP-01 INCREMENT: OWNER-AUTHORIZED`",
               r"FULL CAP-01 / FULL STG:\s*NOT\s+AUTHORIZED",
               r"`D13 RESEARCH: REMAINS CLOSED`",
               r"(?i)Stage 18\s+remains PARTIAL",
               r"(?i)checkbox stays unticked",
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
                 r"STAGE 18 COMPLETE: YES",
                 # tight on purpose: "entering Stage 18 is not the next
                 # obligation discharged" is TRUE and must stay sayable, so the
                 # forbidden shape is the predicate, not the bare co-occurrence
                 r"Stage 18\s+(is|was|has been)\s+(COMPLETE|COMPLETED|CLOSED|DISCHARGED)\b",
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
    assert re.search(r"^- \[ \] \*\*18 — D13/CAP-01 guidance:",
                     _read(ROADMAP), re.M), "stage 18 checkbox is not empty"


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
    for path in (ROADMAP, CHECKLIST, CONTRACT, __file__):
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

        _needs(deps[15], path, "stage 15",
               r"PARTIAL / DEFERRED",
               r"Phase[- ]7 integration/interface foundation",
               r"(?i)EXISTS",
               r"IRL ownership is NOT wholly absent",
               r"per-project integration evidence",
               r"durable subsystem identity",
               r"inbound/write-import",
               r"async/vendor integration",
               r"T2-E")
        _rejects(deps[15], path, "stage 15",
                 r"CAP-12", r"CAP-13", r"WS-PFV-001",
                 r"foundation (is |does not |)(absent|missing)",
                 r"no IRL ownership",
                 r"IRL ownership is wholly absent",
                 r"ownership (is|remains) absent")

        _needs(deps[16], path, "stage 16",
               r"DEFERRED",
               r"Stage 13 technical measurement",
               r"Stage 15 integration axis",
               r"Stage 14 is relevant IF manufacturing participates")


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
    r"STAGE 18: (COMPLETE|COMPLETED)",
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
    assert "**CURRENT STAGE:** Stage 18" in checklist
    # AMENDED at the Stage-17 product-depth disposition: Stage 11 joins this
    # list. It was routed PAST, not completed, so its old current-stage wording
    # must now sit inside a supersession note exactly like a completed stage's.
    for stage in (9, 10, 11):
        for match in re.finditer(r"CURRENT STAGE:\*{0,2} Stage %d" % stage,
                                 checklist):
            window = checklist[max(0, match.start() - 600):match.start()]
            assert "SUPERSEDED" in window.upper(), (
                "the checklist still reads Stage %d as the current stage"
                % stage)
    # AMENDED post-PR-#678: Stage 18 is ENTERED, so "Stage 18 if authorized" is
    # history now. The live frontier must say so, and the old wording may survive
    # only inside the supersession note that preserves it.
    assert "CURRENT PRODUCT-DEPTH FRONTIER: Stage 18 — ENTERED / PARTIAL" in checklist
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
    for pat in (r"`STAGE 18 STARTED: YES`", r"`STAGE 18 COMPLETE: NO`",
                r"FIRST BOUNDED CAP-01 INCREMENT: OWNER-AUTHORIZED",
                r"FULL CAP-01\s*/\s*FULL STG: NOT AUTHORIZED",
                r"`D13 RESEARCH: REMAINS CLOSED`",
                r"(?i)Stage 18 stays \*\*PARTIAL\*\*",
                r"(?i)this entry routes and does not\s+authorize",
                r"electronics_electrical` only",
                r"(?i)FIRST\s+authorized profile, not the definition of CAP-01",
                r"(?i)`mechanical` remains a fully activated"):
        assert re.search(pat, block, re.S), ("current-position", "MISSING", pat)
    for pat in (r"STAGE 18 STARTED: NO", r"STAGE 18 COMPLETE: YES",
                r"(?i)mechanical[^.]{0,60}unsupported"):
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
                r"`STAGE 18 COMPLETE: NO`",
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
    )
    for text, sentence in stale:
        for m in re.finditer(re.escape(sentence), text):
            window = text[max(0, m.start() - 400):m.start()]
            assert "Superseded" in window or "SUPERSEDED" in window, (
                "live stale Stage-18 wording survives", sentence)
    assert "Stage 18 is ENTERED / PARTIAL" in roadmap
    assert "Stage 20 remains a recorded future capability, NOT AUTHORIZED" in roadmap
    assert "Stages 20–27 preserved, NOT ENTERED / NOT AUTHORIZED" in checklist
    raw_checklist = _read(CHECKLIST)
    assert _absent(raw_checklist, "Stages 18–27 preserved, not entered / not authorized")
    assert _absent(raw_checklist, "Stages 19–27 preserved, not entered / not authorized")
    assert "Stages 20–27 preserved, not entered / not authorized" in raw_checklist
    row = [l for l in raw_checklist.splitlines() if l.startswith("| 4 | 16–20 |")]
    assert len(row) == 1 and "18 entered / partial" in row[0], row
    assert "19 entered / not complete" in row[0], row
    assert "19 entered for foundation / contract work only" not in row[0], row
    assert "16, 18–20 not authorized" not in row[0]
    assert "16, 19–20 not authorized" not in row[0]
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
    contract itself is guarded by the test below."""
    merge = "d75075b01e79909ba98ac695abb4f8969e14f753"
    token = ("SECOND BOUNDED CAP-01 RESEARCH-DIRECTION INCREMENT: OWNER-AUTHORIZED / "
             "IMPLEMENTED / MERGED / POST-MERGE VERIFIED — PR #679 — merge " + merge)
    for path, routing in _surfaces("current-routing"):
        assert token in routing, path
        assert "`STAGE 18 COMPLETE: NO`" in routing, path
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
    assert _absent(head, "ACTIVE CONTRACT: NONE") and _absent(head, "ACTIVE CONTRACT: PRESENT")
    assert _absent(head, "no successor Stage is started")
    assert "no further CAP-01 implementation is authorized" in head
    assert "Stage 18 remains STARTED / PARTIAL / NOT COMPLETE" in head
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
    assert _absent(_current(STATE, "current-position"), "ACTIVE CONTRACT: NONE")
    flat_checklist = _flat(CHECKLIST)
    for m in re.finditer(re.escape("NONE AUTHORIZED — `ACTIVE CONTRACT: NONE`"), flat_checklist):
        assert "Superseded" in flat_checklist[max(0, m.start() - 60):m.start()], (
            "a live NONE-AUTHORIZED subtask survives the Stage-19 entry contract")
    raw_checklist = _read(CHECKLIST)
    assert "NO FURTHER CAP-01 IMPLEMENTATION IS CURRENTLY AUTHORIZED" in raw_checklist
    assert re.search(r"^ACTIVE CONTRACT: NONE$", raw_checklist, re.M) is None


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
_S19_CONTRACT = ("`ACTIVE CONTRACT: STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION "
                 "— IMPLEMENTATION-01 ONLY`")
_S19_ENTERED = "`STAGE 19: ENTERED / NOT COMPLETE`"
_S19_ONLY = ("`AUTHORIZED IMPLEMENTATION: DURABLE SUCCESS-CRITERION REMEDIATION — "
             "IMPLEMENTATION-01 / CORRECTION-01`")
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


def test_stage_19_implementation_01_is_the_bounded_remediation_on_every_live_surface():
    """IMPLEMENTATION-01 authorizes ONE thing: the EXISTING SuccessCriterion made
    durable in the same project store. The failure modes keep every token in
    place: "an implementation is authorized" read as full CAP-09 or full
    WS-PFV-001, the durable sidecar read as a parallel experiment store, or the
    remediation read as evidence / result / readiness capture. So the guard
    requires the narrow wording AND rejects the widened predicate on the
    authority, all three routing fences, the current-position entry, CLAUDE.md,
    the checklist, the roadmap row and the capability register — and it records
    no merge/candidate lifecycle state that a merge would make false.
    """
    contract = _read(CONTRACT)
    first = contract.index("## Current authority")
    assert contract[first:].startswith(
        "## Current authority — Stage 19 / CAP-09 durable SuccessCriterion remediation "
        "— IMPLEMENTATION-01"), contract[first:first + 120]
    top = re.sub(r"\s+", " ", contract[first:contract.index("## Current authority", first + 5)])
    _needs(top, CONTRACT, "implementation-01",
           r"\*\*ACTIVE CONTRACT: STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION — "
           r"IMPLEMENTATION-01 ONLY\.\*\*",
           r"`ENTERED / NOT COMPLETE` — checkbox stays unticked",
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
           # CORRECTION-01: the corrected truth, and the rejected interpretation
           # kept only as superseded history
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
           r"No Evidence, experiment-result or validation-result capture",
           r"`STAGE 11 / A2: DEFERRED / UNDISCHARGED`",
           r"`STAGE 15 \(IRL\): PRESERVED — MUST NOT BE LOST`", r"`T2-E: DEFERRED`",
           r"`CI OPTIMIZATION: SEPARATE / NOT IMPLEMENTED`",
           r"`STARTED: YES` · `COMPLETE: NO` · \*\*PARTIAL\*\* — unchanged",
           r"FURTHER CAP-01 IMPLEMENTATION\*\* \| \*\*NOT CURRENTLY AUTHORIZED")
    _rejects(re.sub(r"\*\(Superseded.*?\)\*", "", top), CONTRACT, "implementation-01",
             r"stays view-only", r"Continue the project to change",
             r"FULL CAP-09[^.|]{0,20}\W{0,4}AUTHORIZED(?! )",
             r"FULL (CAP-09|WS-PFV-001)\W{0,8}(IS )?AUTHORIZED\b",
             r"STAGE 19 COMPLETE: YES", r"STAGE 19: COMPLETE",
             r"IMPLEMENTED IN CANDIDATE", r"NOT YET AUTHORITATIVE",
             r"FULL (CAP-01|STG)[^.|]{0,40}: *AUTHORIZED")
    live_surfaces = [(p, r) for p, r in _surfaces("current-routing")]
    live_surfaces.append((STATE, _current(STATE, "current-position")))
    for path, block in live_surfaces:
        _needs(block, path, "stage-19 live", re.escape(_S19_CONTRACT).replace(r"\ ", r"\s+"),
               re.escape(_S19_ENTERED).replace(r"\ ", r"\s+"),
               re.escape(_S19_ONLY).replace(r"\ ", r"\s+"),
               *(re.escape(t).replace(r"\ ", r"\s+") for t in _S19_NOT_FULL),
               r"Section 11 \+\s+`SuccessCriterion` stay the canonical planning\s+owner")
        _rejects(block, path, "stage-19 live",
                 r"ACTIVE CONTRACT: NONE", r"FOUNDATION CONTRACT ONLY",
                 r"ENTERED FOR FOUNDATION", r"CAP-09 PRODUCT IMPLEMENTATION",
                 r"STAGE 19 COMPLETE: YES", r"Stages 19–27 preserved",
                 r"IMPLEMENTED IN CANDIDATE", r"NOT YET AUTHORITATIVE")
    for path, routing in _surfaces("current-routing"):
        _needs(routing, path, "stage-19 routing", r"Stage-19 checkbox stays unticked",
               r"entering Stage 19 completes nothing in Stage 18")
    # CLAUDE.md routes to it first, and does not widen it
    claude = re.sub(r"\s+", " ", _read("CLAUDE.md"))
    head = claude[claude.index("## Current authority"):claude.index("*(Superseded")]
    for needle in ("ACTIVE CONTRACT: STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION "
                   "— IMPLEMENTATION-01 ONLY.",
                   "is ENTERED / NOT COMPLETE",
                   "The only authorized implementation is the durable SuccessCriterion remediation",
                   "Full CAP-09 and full WS-PFV-001 are NOT AUTHORIZED",
                   "no other Stage is authorized"):
        assert needle in head, needle
    for stale in ("FOUNDATION CONTRACT ONLY", "NOT STARTED / NOT AUTHORIZED YET",
                  "ACTIVE CONTRACT: NONE"):
        assert _absent(head, stale), stale
    # the checklist subtask and machine record, and the roadmap row
    flat_checklist, raw_checklist = _flat(CHECKLIST), _read(CHECKLIST)
    assert ("**CURRENT SUBTASK:** STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION — "
            "IMPLEMENTATION-01 ONLY") in flat_checklist
    for line in ("ACTIVE CONTRACT: STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION "
                 "— IMPLEMENTATION-01 ONLY",
                 "STAGE 19: ENTERED / NOT COMPLETE",
                 "AUTHORIZED IMPLEMENTATION: DURABLE SUCCESS-CRITERION REMEDIATION — "
                 "IMPLEMENTATION-01 / CORRECTION-01",
                 "CRITERIA EDITING: NO WRITABLE PROGRESSION STATE REQUIRED",
                 "PLANNING-METADATA CORRUPTION: DOES NOT GOVERN CORE PROGRESSION",
                 "SECTION-11 CONSUMERS: FAIL CLOSED WHEN DURABLE CRITERIA CANNOT BE READ",
                 "FULL CAP-09: NOT AUTHORIZED", "FULL WS-PFV-001: NOT AUTHORIZED",
                 "NO FURTHER CAP-01 IMPLEMENTATION IS CURRENTLY AUTHORIZED"):
        assert re.search(r"^" + re.escape(line) + r"$", raw_checklist, re.M), line
    for gone in ("ACTIVE CONTRACT: STAGE 19 / CAP-09 FOUNDATION CONTRACT ONLY",
                 "CAP-09 PRODUCT IMPLEMENTATION: NOT STARTED / NOT AUTHORIZED YET",
                 "ACTIVE CONTRACT: NONE"):
        assert re.search(r"^" + re.escape(gone) + r"$", raw_checklist, re.M) is None, gone
    rows = re.findall(r"^- \[ \] \*\*19 — WS-PFV-001/CAP-09:\*\*.*$", _read(ROADMAP), re.M)
    assert len(rows) == 1, "stage 19 row missing, duplicated or ticked"
    assert "**ENTERED / NOT COMPLETE (2026-09-23):**" in rows[0]
    assert "the ONLY authorized implementation is the durable SuccessCriterion remediation" in rows[0]
    assert "full CAP-09 and full WS-PFV-001 NOT AUTHORIZED" in rows[0]
    assert "satisfied for planning-only CAP-09 entry, and for nothing wider" in rows[0]
    assert re.search(r"^- \[ \] \*\*20 — CAP-08:", _read(ROADMAP), re.M), "stage 20 row changed"
    # the register records ONE bounded CAP-09 exception, not an opening of CAP-09
    register = _read(CAPABILITIES)
    reg_rows = [l for l in register.splitlines() if l.startswith("| CAP-09 Experiment Designer |")]
    assert len(reg_rows) == 2, reg_rows
    for r in reg_rows:
        assert "RECORDED — NOT AUTHORIZED, except one bounded" in r, r
        assert "durable SuccessCriterion remediation" in r, r
    flat_register = _flat(CAPABILITIES)
    assert "It does NOT authorize full CAP-09 or full WS-PFV-001" in flat_register
    assert "`FULL CAP-09: NOT AUTHORIZED` · `FULL WS-PFV-001: NOT AUTHORIZED`" in flat_register
