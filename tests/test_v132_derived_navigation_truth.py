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


def test_stage_nine_is_the_next_stage_and_authorizes_nothing():
    """The CURRENT next stage, asserted so preserved history cannot satisfy it.

    The earlier version of this guard asserted "Next Master Roadmap stage:
    Stage 8." That sentence is still in the roadmap — correctly, as preserved
    Stage-7-amendment history — so once Stage 8 closed the assertion would have
    stayed green while pointing at the wrong stage. It now asserts the current
    routing AND that no live sentence still routes to Stage 8: the Stage-8
    wording must survive only inside an explicit supersession note.
    """
    roadmap, checklist, contract = (_flat(ROADMAP), _flat(CHECKLIST),
                                    _flat(CONTRACT))
    assert "Next Master Roadmap stage: Stage 9" in roadmap
    assert "Next Master Roadmap stage: Stage 9" in contract
    assert "Stage 9" in checklist
    # every surviving "Stage 8 is next" sentence must be marked superseded
    for flat, path in ((roadmap, ROADMAP), (checklist, CHECKLIST)):
        for match in re.finditer(r"Next Master Roadmap stage: Stage 8", flat):
            window = flat[max(0, match.start() - 600):match.start()]
            assert "SUPERSEDED" in window.upper(), (
                "a live sentence still routes to Stage 8 in %s" % path)
    # closing one stage never starts the next
    assert "Stage 9 requires its own explicit mandate" in checklist
    assert "Closing Stage 8 starts nothing" in contract or \
        "Closing Stage 8 starts nothing" in checklist


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
