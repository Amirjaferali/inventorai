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


def _flat(path):
    return re.sub(r"\s+", " ", _read(path))


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


def test_stage_eighteen_is_the_next_executable_stage_and_authorizes_nothing():
    """The CURRENT next stage, asserted so preserved history cannot satisfy it.

    This guard was wrong-but-green three times, and the shape of the failure was
    the same each time: it asserted a routing sentence that was still in the
    documents as legitimate preserved history, so closing the stage it named
    left the assertion passing while it pointed at the wrong stage. It asserted
    "Stage 8" after Stage 8 closed, "Stage 9" after the Stage-9 disposition
    completed, and "Stage 10" after the Stage-10 differential completed. Every
    version passed.

    So it asserts two things that cannot both survive a stale update: the
    CURRENT routing sentence must be present, AND every surviving sentence that
    routes to an already-routed-past stage must sit inside an explicit
    supersession note. The second half is what catches the drift — a document
    that has not been re-routed keeps a live stale sentence and fails here.

    Stage 11 joins that stale list at the Stage-17 product-depth disposition,
    and the reason matters: it was routed PAST, not completed. So this guard
    also asserts, separately, that every surface still calls it DEFERRED and
    still carries `STAGE 11 STARTED: NO`. Routing forward must never read as a
    discharge — that is the exact confusion these documents exist to prevent.
    """
    roadmap, checklist, contract = (_flat(ROADMAP), _flat(CHECKLIST),
                                    _flat(CONTRACT))
    assert "Next executable Master Roadmap stage: Stage 18" in roadmap
    assert "Next executable Master Roadmap stage: Stage 18" in contract
    assert "**CURRENT STAGE:** Stage 18" in checklist
    # every surviving "Stage N is next" sentence, for every already-routed-past
    # stage, must be marked superseded — in the navigation AND in the authority.
    for flat, path in ((roadmap, ROADMAP), (checklist, CHECKLIST),
                       (contract, CONTRACT)):
        for stale in ("Next Master Roadmap stage: Stage 7",
                      "Next Master Roadmap stage: Stage 8",
                      "Next Master Roadmap stage: Stage 9",
                      "Next Master Roadmap stage: Stage 10",
                      "Next Master Roadmap stage: Stage 11"):
            for match in re.finditer(re.escape(stale), flat):
                window = flat[max(0, match.start() - 600):match.start()]
                assert "SUPERSEDED" in window.upper(), (
                    "a live sentence still routes to a routed-past stage in %s: %s"
                    % (path, stale))
    # routing PAST Stage 11 is not completing it, and every surface must say so
    for flat, path in ((roadmap, ROADMAP), (checklist, CHECKLIST),
                       (contract, CONTRACT)):
        assert "`STAGE 11 STARTED: NO`" in flat, path
        assert "DEFERRED" in flat.upper(), path
    assert re.search(r"^- \[ \] \*\*11 — T1-C′/A2 human evidence:",
                     _read(ROADMAP), re.M), "stage 11 checkbox is not empty"
    # completing or dispositioning one stage never starts the next
    assert "Stage 18 requires its own separate mandate" in checklist
    assert "completing the Stage-17 product-depth work" in checklist
    assert "`STAGE 18 STARTED: NO`" in contract
    # and Stage 18 itself is still untouched
    assert re.search(r"^- \[ \] \*\*18 — D13/CAP-01 guidance:",
                     _read(ROADMAP), re.M), "stage 18 checkbox is not empty"


def test_stage_seventeen_product_depth_is_not_commercial_readiness():
    """The distinction the disposition turns on, guarded in all three surfaces.

    Product-depth work completing is not a Commercial Readiness PASS. A surface
    that records the first without carrying the second is the drift this guard
    exists to catch, so both must appear together and Stage 17 must stay
    unticked."""
    roadmap, checklist, contract = (_flat(ROADMAP), _flat(CHECKLIST),
                                    _flat(CONTRACT))
    for flat, path in ((roadmap, ROADMAP), (checklist, CHECKLIST),
                       (contract, CONTRACT)):
        assert "PRODUCT-DEPTH WORK" in flat.upper(), path
        assert "COMMERCIAL READINESS" in flat.upper(), path
        assert "VALIDATED COMMERCIAL CONCLUSION: NO" in flat, path
        assert "INSUFFICIENT_EVIDENCE" in flat, path
        # The denial must be PRESENT, not merely the claim absent: a surface
        # that simply omits the point teaches nothing. A blunt substring sweep
        # cannot tell "no product-market fit is claimed" from "product-market
        # fit", so the affirmative forms are what is forbidden.
        assert "Commercial Readiness is NOT asserted as passing" in flat \
            or "does **not** assert Commercial Readiness as passing" in flat, path
        for forbidden in ("COMMERCIAL READINESS: PASS",
                          "COMMERCIAL READINESS PASS \u2705",
                          "PRODUCT-MARKET FIT: ESTABLISHED",
                          "DEMAND: VALIDATED"):
            assert forbidden not in flat.upper(), (path, forbidden)
    # the remaining gaps stay with their owner and are not re-homed into Stage 17
    for flat, path in ((roadmap, ROADMAP), (contract, CONTRACT),
                       (checklist, CHECKLIST)):
        assert "T2-E" in flat, path
    # Stage 17 is NOT closed: its checkbox stays empty
    assert re.search(r"^- \[ \] \*\*17 — Market Reality / Commercial Readiness:",
                     _read(ROADMAP), re.M), "stage 17 checkbox is not empty"


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
    assert "CURRENT PRODUCT-DEPTH FRONTIER: Stage 18 if authorized" in checklist
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
