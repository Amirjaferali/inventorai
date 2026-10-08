"""v1.32 derived-navigation truth guards — live-truth reversal proofs.

Split out of tests/test_v132_derived_navigation_truth.py unchanged, for CI shard balance only
(scripts/ci_full_suite.py places whole files): every material reversal and the Stage 35 / 16 / 36 checkbox and
count drift must be rejected by the live-invariant owner and the current-state guard. The owners, documents and
helpers stay in the original module; `_read` is read and patched on that module (`_nav`) so the current-state guard
sees the mutated documents exactly as before the split.
"""

import re

import pytest

import test_v132_derived_navigation_truth as _nav
from test_v132_derived_navigation_truth import (
    CHECKLIST, CONTRACT, ROADMAP, STATE, _NEXT_INC_NO, _NONE718, _NONE_BOLD, _NS, _S13_14_PARTIAL, _S15_COMPLETE,
    _S15_ENTERED, _S16C_DELIVERED, _S16_COMPLETE, _S16_DELIVERED, _S16_SRL_NO, _S18_COMPLETE, _S19_COMPLETE,
    _S20_COMPLETE, _S21_COMPLETE, _S22_COMPLETE, _S23_COMPLETE, _S24_COMPLETE, _S24_PARTIAL, _S24_PRE_MARKER,
    _S35C_DELIVERED, _S35_ACTIVE, _S35_BOLD, _S35_COMPLETE, _S35_ENTERED, _S35_LATER_NO, _S35_LIMITS, _S35_NAME,
    _S35_SLICE_DELIVERED, _S35_TRIGGERS, _S36C_DELIVERED, _S36_COMPLETE, _S36_LIMITS, _S36_NOT, _S37_NOT,
    _S25_DELIVERED, _S25_FULL_NO, _S25_PARTIAL, _S25_PRE_MARKER, _live_authority_problems, _mutate,
)


_MATERIAL_REVERSALS = {
    # Stage 15 closure: dropping the scope, or reopening the stage, is a reversal of the live truth.
    "stage 15 complete": (CHECKLIST, "current-routing", _S15_COMPLETE, "`STAGE 15: COMPLETE`"),
    "stage 15 reopened": (ROADMAP, "current-routing", _S15_COMPLETE, _S15_ENTERED),
    "stage 15 complete in prose": (STATE, "current-position", _NS, _NS + " Stage 15 is complete."),
    # Stage 18 closure: dropping the scope, reopening the stage, moving the marker, completing Stage 19 or
    # authorizing Stage-19 implementation / MSNL is a reversal of the live truth.
    "stage 18 complete": (ROADMAP, "current-routing", _S18_COMPLETE, "`STAGE 18 COMPLETE: YES`"),
    "stage 18 unscoped": (CHECKLIST, "current-routing", _S18_COMPLETE, "`STAGE 18: COMPLETE`"),
    "stage 18 reopened": (CONTRACT, "current-routing", _S18_COMPLETE, "`STAGE 18 COMPLETE: NO`"),
    "stage 18 partial in prose": (STATE, "current-position", _NS, _NS + " Stage 18 remains PARTIAL."),
    "marker moved": (CONTRACT, "current-routing", "CURRENT MASTER ROADMAP STAGE: Stage 25",
                     "CURRENT MASTER ROADMAP STAGE: Stage 26"),
    "marker moved in position": (STATE, "current-position", "MASTER ROADMAP SEQUENTIAL MARKER: STAGE 25",
                                 "MASTER ROADMAP SEQUENTIAL MARKER: STAGE 24"),
    "marker back in prose": (CHECKLIST, "current-routing", _NS, _NS + " The MASTER ROADMAP SEQUENTIAL MARKER stays "
                             "Stage 18."),
    "stage 19 complete": (ROADMAP, "current-routing", _NS, _NS + " `STAGE 19: COMPLETE`"),
    "stage 19 implementation": (STATE, "current-position", _NS, _NS + " Stage-19 implementation authorized."),
    # Stage 19 closure: dropping the scope, reopening Stage 19, completing Stage 20, authorizing Stage-20
    # implementation or full CAP-09, or recording a result outcome is a reversal of the live truth.
    "stage 19 unscoped": (CHECKLIST, "current-routing", _S19_COMPLETE, "`STAGE 19: COMPLETE`"),
    "stage 19 reopened": (CONTRACT, "current-routing", _S19_COMPLETE, "`STAGE 19: ENTERED / NOT COMPLETE`"),
    "stage 19 marker back": (CHECKLIST, "current-routing", _NS, _NS + " The MASTER ROADMAP SEQUENTIAL MARKER is "
                             "Stage 19 for navigation only."),
    "stage 20 complete": (ROADMAP, "current-routing", _NS, _NS + " `STAGE 20: COMPLETE`"),
    "stage 20 implementation": (STATE, "current-position", _NS, _NS + " Stage-20 implementation authorized."),
    "full cap-09": (CONTRACT, "declaration", _NS, _NS + " `FULL CAP-09: AUTHORIZED`"),
    "result outcome": ("CLAUDE.md", "head", _NONE_BOLD,
                       _NONE_BOLD + " `RESULT OUTCOME / PASS-FAIL JUDGEMENT: AUTHORIZED`"),
    "prototype validated": (STATE, "current-position", _NS, _NS + " The prototype has been validated."),
    # Stage 20 closure: dropping the scope, reopening Stage 20, completing Stage 21, authorizing Stage-21
    # implementation or full CAP-08 / CAP-10, or claiming an automatically resolved assumption is a reversal.
    "stage 20 unscoped": (CHECKLIST, "current-routing", _S20_COMPLETE, "`STAGE 20: COMPLETE`"),
    "stage 20 reopened": (CONTRACT, "current-routing", _S20_COMPLETE, "`STAGE 20: ENTERED / PARTIAL`"),
    "stage 20 marker back": (CHECKLIST, "current-routing", _NS, _NS + " The MASTER ROADMAP SEQUENTIAL MARKER is "
                             "Stage 20 for navigation only."),
    "stage 21 complete": (ROADMAP, "current-routing", _NS, _NS + " `STAGE 21: COMPLETE`"),
    "stage 21 implementation": (STATE, "current-position", _NS, _NS + " Stage-21 implementation authorized."),
    "full cap-08": (CONTRACT, "declaration", _NS, _NS + " `FULL CAP-08: AUTHORIZED`"),
    "full cap-10": ("CLAUDE.md", "head", _NONE_BOLD,
                    _NONE_BOLD + " `FULL CAP-10: AUTHORIZED`"),
    "assumption auto-resolved": (STATE, "current-position", _NS, _NS + " The assumption was automatically resolved."),
    # Stage 21 closure: dropping the scope, reopening Stage 21, completing Stage 22, authorizing Stage-22
    # implementation, automatic / AI detection or a SYSTEM_INFERRED contradiction writer is a reversal.
    "stage 21 unscoped": (CHECKLIST, "current-routing", _S21_COMPLETE, "`STAGE 21: COMPLETE`"),
    "stage 21 reopened": (CONTRACT, "current-routing", _S21_COMPLETE, "`STAGE 21: ENTERED / PARTIAL`"),
    "stage 21 marker back": (CHECKLIST, "current-routing", _NS, _NS + " The MASTER ROADMAP SEQUENTIAL MARKER is "
                             "Stage 21 for navigation only."),
    "stage 22 complete": (ROADMAP, "current-routing", _NS, _NS + " `STAGE 22: COMPLETE`"),
    "stage 22 implementation": (STATE, "current-position", _NS, _NS + " Stage-22 implementation authorized."),
    "ai contradiction detection": (CONTRACT, "declaration", _NS,
                                   _NS + " `AUTOMATIC / AI CONTRADICTION DETECTION: AUTHORIZED`"),
    "system-inferred contradiction writer": ("CLAUDE.md", "head", _NONE_BOLD,
                                             _NONE_BOLD + " `SYSTEM_INFERRED CONTRADICTION WRITER: "
                                             "AUTHORIZED`"),
    # Stage 22 closure: dropping the scope, reopening Stage 22, moving the marker back, entering or implementing Stage
    # 23, activating CAP-06 or opening full CAP-05 / CAP-07 is a reversal.
    "stage 22 unscoped": (CHECKLIST, "current-routing", _S22_COMPLETE, "`STAGE 22: COMPLETE`"),
    "stage 22 reopened": (CONTRACT, "current-routing", _S22_COMPLETE, "`STAGE 22: ENTERED / PARTIAL`"),
    "stage 22 marker back": (CHECKLIST, "current-routing", _NS, _NS + " The MASTER ROADMAP SEQUENTIAL MARKER is "
                             "Stage 22 for navigation only."),
    "stage 23 entered": (ROADMAP, "current-routing", _NS, _NS + " `STAGE 23: ENTERED`"),
    "stage 23 implementation": (STATE, "current-position", _NS, _NS + " Stage-23 implementation authorized."),
    "full cap-05": (CONTRACT, "declaration", _NS, _NS + " `FULL CAP-05: AUTHORIZED`"),
    "cap-06 activated": ("CLAUDE.md", "head", _NONE_BOLD,
                         _NONE_BOLD + " `CAP-06: ACTIVATED`"),
    # Stage 23 closure: dropping the four-axis scope, reopening Stage 23, moving the marker back, entering or
    # implementing Stage 24, authorizing full CAP-06 or claiming the eight-axis CAP-06 is a reversal.
    "stage 23 unscoped": (CHECKLIST, "current-routing", _S23_COMPLETE, "`STAGE 23: COMPLETE`"),
    "stage 23 reopened": (CONTRACT, "current-routing", _S23_COMPLETE, "`STAGE 23: ENTERED / PARTIAL`"),
    "stage 23 marker back": (CHECKLIST, "current-routing", _NS, _NS + " The MASTER ROADMAP SEQUENTIAL MARKER is "
                             "Stage 23 for navigation only."),
    # INVERTED at the delivered CAP-12 Form Mock-up Advisory Slice 1: Stage 24 is now legitimately ENTERED / PARTIAL,
    # so the reversal is a return to the pre-slice NOT-ENTERED state or marker on a live surface.
    "stage 24 back to not entered": (ROADMAP, "current-routing", _NS, _NS + " `STAGE 24: NOT ENTERED`"),
    "stage 24 marker back": (STATE, "current-position", _NS, _NS + " " + _S24_PRE_MARKER),
    "stage 24 implementation": (STATE, "current-position", _NS, _NS + " Stage-24 implementation authorized."),
    # AMENDED at the Stage 24 closure: Stage 24 is COMPLETE for its bounded scope and the marker is Stage 25 (NOT
    # ENTERED); unscoping or reopening Stage 24, moving the marker back, entering Stage 25 or authorizing Stage-25
    # implementation, full CAP-12, a further CAP-12 slice or CAP-13 activation is a reversal of the live truth.
    "stage 24 unscoped": (CHECKLIST, "current-routing", _S24_COMPLETE, "`STAGE 24: COMPLETE`"),
    "stage 24 reopened": (CONTRACT, "current-routing", _S24_COMPLETE, _S24_PARTIAL),
    "stage 24 partial marker back": (CHECKLIST, "current-routing", _NS, _NS + " The MASTER ROADMAP SEQUENTIAL "
                                     "MARKER is Stage 24 for navigation only."),
    "stage 25 entered": (ROADMAP, "current-routing", _NS, _NS + " `STAGE 25: ENTERED`"),
    "stage 25 implementation": (STATE, "current-position", _NS, _NS + " Stage-25 implementation authorized."),
    "full cap-12": (CONTRACT, "declaration", _NS, _NS + " `FULL CAP-12: AUTHORIZED`"),
    "further cap-12 slice": (ROADMAP, "current-routing", _NS, _NS + " `FURTHER CAP-12 SLICES: AUTHORIZED`"),
    "cap-13 activated": ("CLAUDE.md", "head", _NONE_BOLD,
                         _NONE_BOLD + " `CAP-13: ACTIVATED`"),
    "full cap-06": (CONTRACT, "declaration", _NS, _NS + " `FULL CAP-06: AUTHORIZED`"),
    "eight-axis cap-06 claimed": ("CLAUDE.md", "head", _NONE_BOLD,
                                  _NONE_BOLD + " `FULL EIGHT-AXIS CAP-06: IMPLEMENTED`"),
    "msnl activated": (CONTRACT, "declaration", _NS, _NS + " `MSNL: ACTIVATED`"),
    # ROTATED at the Stage 35 first bounded slice: the anchors were the further-increment exclusion and the Stage-35
    # contract token; ROTATED back at the Stage 35 closure: the next-increment exclusion and the NONE token
    "successor increment": (STATE, "current-position", _NEXT_INC_NO, "`NEXT PRODUCT INCREMENT: AUTHORIZED`"),
    "successor contract on one surface": (ROADMAP, "current-routing", _NONE718,
                                          "`ACTIVE CONTRACT: STAGE 15 — SLICE 3`"),
    "compatibility established": (CHECKLIST, "current-routing", "engineering compatibility has NOT been established",
                                  "engineering compatibility has been established"),
    "interaction verified": (STATE, "current-position", _NS, _NS + " The interaction has been verified."),
    "irl level": (ROADMAP, "current-routing", _NS, _NS + " IRL level 3 is assigned."),
    "irl score": (CONTRACT, "declaration", _NS, _NS + " An IRL score is assigned."),
    "deployment authorized": (CONTRACT, "declaration", _NS, _NS + " Deployment is authorized."),
    "release authorized": ("CLAUDE.md", "head", _NONE_BOLD,
                           _NONE_BOLD + " Release is authorized."),
    "another stage-15 slice": (CHECKLIST, "current-routing", "`ANOTHER STAGE-15 SLICE: NOT AUTHORIZED`",
                               "`ANOTHER STAGE-15 SLICE: AUTHORIZED`"),
    "new domain": (STATE, "current-position", _NS, _NS + " `NEW DOMAIN ACTIVATION: AUTHORIZED`"),
    "live section marked as history": (CONTRACT, "declaration", "no active contract",
                                       "no active contract — SUPERSEDED"),
    "second live declaration": (CONTRACT, "declaration", _NS,
                                _NS + " **ACTIVE CONTRACT: STAGE 15 — SLICE 1.**"),
    "claude declares a historical contract": ("CLAUDE.md", "head", _NONE_BOLD,
                                              "**ACTIVE CONTRACT: STAGE 15 — SUBSYSTEM INTERFACE DECLARATION & "
                                              "VERIFICATION PREPARATION — SLICE 2.**"),
    "pre-merge lifecycle live": (STATE, "current-position", _NS, _NS + " Stage 15 Slice 2 is NOT MERGED."),
    "candidate wording live": (ROADMAP, "current-routing", _NS, _NS + " IMPLEMENTATION CANDIDATE."),
    "stage status dropped": (CONTRACT, "current-routing", _S18_COMPLETE, "`STAGE 18 STATUS`", "all"),
    "observation read as a verdict": (STATE, "current-position", _NS,
                                      _NS + " The acceptance criterion was met."),
    "observation verdict authorized": (CHECKLIST, "current-routing",
                                       "`INTERFACE OBSERVATION VERDICT / CRITERION-MET JUDGEMENT: NOT AUTHORIZED`",
                                       "`INTERFACE OBSERVATION VERDICT / CRITERION-MET JUDGEMENT: AUTHORIZED`"),
    # ADDED at the Stage 35 first bounded slice; ROTATED at the Stage 35 closure: the Stage-35 active contract back on
    # any one surface, the active-increment heading or prose back, Stage 35 back to ENTERED / PARTIAL or NOT COMPLETE,
    # an unscoped or global completion, a stage-level delivery claim, the slice back to not delivered, a pending merge
    # authorization, the closure undone, a later slice authorized, a lifted exclusion, dropped legal-adviser / release
    # triggers or a Stage-36 advance is a reversal of the live truth.
    "stage 35 contract restored in the position": (STATE, "current-position", _NONE718, _S35_ACTIVE),
    "stage 35 contract restored in the routing": (CHECKLIST, "current-routing", _NONE718, _S35_ACTIVE),
    "stage 35 contract restored in the declaration": (CONTRACT, "declaration", _NONE_BOLD, _S35_BOLD),
    "stage 35 contract restored in the head": ("CLAUDE.md", "head", _NONE_BOLD, _S35_BOLD),
    "active increment heading restored": (ROADMAP, "current-routing", "**NO ACTIVE CONTRACT — post-Stage-25-CAP-13-Slice-1 "
                                          "(2026-10-08); ", "**ACTIVE BOUNDED PRODUCT INCREMENT — " + _S35_NAME
                                          + " (Owner-authorized 2026-10-05); "),
    "stale active-increment prose back": (CHECKLIST, "current-routing", _NS,
                                          _NS + " " + _S35_NAME + " is the active bounded product increment."),
    "stale closure-pending prose back": (STATE, "current-position", _NS, _NS + " The active contract stays this first "
                                         "bounded slice until a separate Owner closure decision."),
    "stage 35 back to entered": (CONTRACT, "current-routing", _S35_COMPLETE, _S35_ENTERED),
    "stage 35 not complete": (ROADMAP, "current-routing", _S35_COMPLETE, "`STAGE 35: NOT COMPLETE`"),
    "stage 35 unscoped": (CHECKLIST, "current-routing", _S35_COMPLETE, "`STAGE 35: COMPLETE`"),
    "stage 35 closed unscoped": (CONTRACT, "current-routing", _S35_COMPLETE, "`STAGE 35: CLOSED`"),
    "stage 35 back to not entered": (STATE, "current-position", _S35_COMPLETE, "`STAGE 35: NOT ENTERED`"),
    "stage 35 complete globally in prose": (STATE, "current-position", _NS, _NS + " Stage 35 is complete."),
    "stage 35 fully complete in prose": (CONTRACT, "declaration", _NS,
                                         _NS + " Stage 35 is fully complete for every scope."),
    "stage 35 delivered in prose": ("CLAUDE.md", "head", _NONE_BOLD, _NONE_BOLD + " Stage 35 is delivered."),
    "stage 35 slice back to not delivered": (CHECKLIST, "current-routing", _S35_SLICE_DELIVERED,
                                             "`STAGE 35 FIRST BOUNDED SLICE: NOT DELIVERED`"),
    "stage 35 pre-merge status in prose": (CONTRACT, "declaration", _NS, _NS + " merge authorization NO; NOT delivered."),
    "stage 35 merge authorization back": (ROADMAP, "current-routing", _NS,
                                          _NS + " `STAGE 35 MERGE AUTHORIZATION: NO`"),
    "stage 35 merge authorized": (STATE, "current-position", _NS, _NS + " `STAGE 35 MERGE AUTHORIZATION: YES`"),
    "stage 35 owner authorization reversed": (ROADMAP, "current-routing", _NS,
                                              _NS + " `STAGE 35 OWNER IMPLEMENTATION AUTHORIZATION: NO`"),
    "stage 35 closure undone": (CONTRACT, "current-routing", _S35C_DELIVERED, "`STAGE 35 CLOSURE: NOT AUTHORIZED`"),
    "stage 35 closure dropped in the position": (STATE, "current-position", _S35C_DELIVERED,
                                                 "`STAGE 35 CLOSURE: NOT DELIVERED`"),
    "later stage-35 slice": (STATE, "current-position", _S35_LATER_NO, "`LATER STAGE-35 SLICES: AUTHORIZED`"),
    "later stage-35 slice in prose": (ROADMAP, "current-routing", _NS, _NS + " Later Stage-35 slices are authorized."),
    "stage 35 pdf / provider": (CHECKLIST, "current-routing", _S35_LIMITS[0],
                                _S35_LIMITS[0].replace(": NOT AUTHORIZED", ": AUTHORIZED")),
    "patent claims": ("CLAUDE.md", "head", _NONE_BOLD,
                      _NONE_BOLD + " " + _S35_LIMITS[1].replace(": NOT AUTHORIZED", ": AUTHORIZED")),
    "legal-adviser / release triggers dropped": (CONTRACT, "declaration", _S35_TRIGGERS,
                                                 "`STAGE 35 LEGAL-ADVISER / RELEASE TRIGGERS: WAIVED`"),
    "stage 36 implementation": (STATE, "current-position", _NS, _NS + " Stage-36 implementation authorized."),
    # ADDED at the Stage 36 closure (the Stage 35 closure's "stage 36 entered / authorized" cases rotate to the closure
    # state): Stage 36 back to NOT ENTERED or unscoped, an undone closure, the post-Stage-35-closure head back, a
    # selected / active production live AI / provider, an implemented CAP-15 / CAP-17, activated External Engineering
    # Tools, a waived fresh reassessment or a Stage-37 advance is a reversal of the live truth.
    "stage 36 back to not entered": (ROADMAP, "current-routing", _S36_COMPLETE, _S36_NOT[0]),
    "stage 36 not authorized back": (STATE, "current-position", _S36_COMPLETE, _S36_NOT[1]),
    "stage 36 unscoped": (CHECKLIST, "current-routing", _S36_COMPLETE, "`STAGE 36: COMPLETE`"),
    "stage 36 complete globally in prose": (STATE, "current-position", _NS, _NS + " Stage 36 is complete."),
    "stage 36 fully complete in prose": (CONTRACT, "declaration", _NS,
                                         _NS + " Stage 36 is fully complete for every scope."),
    "stage 36 not-entered prose back": (CONTRACT, "declaration", _NS,
                                        _NS + " Stage 36 stays NOT ENTERED and NOT AUTHORIZED."),
    "stage 36 closure undone": (CONTRACT, "current-routing", _S36C_DELIVERED, "`STAGE 36 CLOSURE: NOT AUTHORIZED`"),
    "post-stage-35 none head back": (ROADMAP, "current-routing", "**NO ACTIVE CONTRACT — post-Stage-25-CAP-13-Slice-1 "
                                     "(2026-10-08); ", "**NO ACTIVE CONTRACT — post-Stage-35-closure (2026-10-05); "),
    "live provider selected": (STATE, "current-position", _S36_LIMITS[0],
                               "`PRODUCTION LIVE AI / PROVIDER: SELECTED — ACTIVE`"),
    "live provider active in prose": (ROADMAP, "current-routing", _NS,
                                      _NS + " The production live AI / provider is active."),
    "cap-15 / cap-17 implemented": (CHECKLIST, "current-routing", _S36_LIMITS[1], "`CAP-15 / CAP-17: IMPLEMENTED`"),
    "cap-17 implemented in prose": ("CLAUDE.md", "head", _NONE_BOLD, _NONE_BOLD + " CAP-17 is implemented."),
    "external tools activated": (CONTRACT, "declaration", _S36_LIMITS[2], "`EXTERNAL ENGINEERING TOOLS: ACTIVE`"),
    "fresh reassessment waived": (ROADMAP, "current-routing", _S36_LIMITS[3],
                                  _S36_LIMITS[3].replace("FRESH STAGE-36 REASSESSMENT + SEPARATE AUTHORIZATION "
                                                         "REQUIRED", "NOT REQUIRED")),
    "stage 37 entered": (ROADMAP, "current-routing", _S37_NOT[0], "`STAGE 37: ENTERED`"),
    "stage 37 authorized": (STATE, "current-position", _S37_NOT[1], "`STAGE 37: AUTHORIZED`"),
    "stage 37 implementation": (CHECKLIST, "current-routing", _NS, _NS + " Stage-37 implementation authorized."),
    # ADDED at the Stage 16 closure: an undone closure or residual, Stage 16 back to deferred, unscoped or globally
    # complete, the post-Stage-36-closure head back, Stage 16 routed past again, an SRL number / level, single score or
    # weakest-axis computation, Stage 13 / Stage 14 advanced beyond PARTIAL / DEFERRED, or further Stage-16 work
    # authorized is a reversal of the live truth.
    "stage 16 closure undone": (CONTRACT, "current-routing", _S16C_DELIVERED, "`STAGE 16 CLOSURE: NOT AUTHORIZED`"),
    "stage 16 residual undone": (CHECKLIST, "current-routing", _S16_DELIVERED,
                                 "`STAGE 16 — TECHNICAL-ROW FOCUS-SCOPE DISCLOSURE: NOT DELIVERED`"),
    "stage 16 back to deferred": (ROADMAP, "current-routing", _S16_COMPLETE, "`STAGE 16: DEFERRED`"),
    "stage 16 unscoped": (STATE, "current-position", _S16_COMPLETE, "`STAGE 16: COMPLETE`"),
    "stage 16 complete globally in prose": (STATE, "current-position", _NS, _NS + " Stage 16 is complete."),
    "stage 16 fully complete in prose": (CONTRACT, "declaration", _NS,
                                         _NS + " Stage 16 is fully complete for every scope."),
    "post-stage-36 none head back": (ROADMAP, "current-routing", "**NO ACTIVE CONTRACT — post-Stage-25-CAP-13-Slice-1 "
                                     "(2026-10-08); ", "**NO ACTIVE CONTRACT — post-Stage-36-closure (2026-10-05); "),
    "stage 16 routed past again": (CONTRACT, "current-routing", "routing past Stages 11, 13, 14 and 17",
                                   "routing past Stages 11, 13, 14, 16 and 17"),
    "srl computation authorized": (ROADMAP, "current-routing", _S16_SRL_NO,
                                   "`SRL LEVEL / SINGLE SCORE / WEAKEST-AXIS COMPUTATION: AUTHORIZED`"),
    "srl level computed in prose": (STATE, "current-position", _NS, _NS + " An SRL level is computed."),
    "weakest axis computed in prose": (CHECKLIST, "current-routing", _NS,
                                       _NS + " The weakest-axis calculation is implemented."),
    "stage 13 complete": (CONTRACT, "declaration", _S13_14_PARTIAL[0], "`STAGE 13: COMPLETE`"),
    "stage 14 complete": (STATE, "current-position", _S13_14_PARTIAL[1], "`STAGE 14: COMPLETE`"),
    "stages 13 and 14 complete in prose": (ROADMAP, "current-routing", _NS, _NS + " Stages 13 and 14 are complete."),
    "further stage 16 work authorized": (CHECKLIST, "current-routing", _NS,
                                         _NS + " and further Stage-16 / SRL work is authorized."),
    # ADDED at the delivered Stage 25 / CAP-13 Two-Support Static Reactions Slice 1: an undone slice, Stage 25 back to
    # NOT ENTERED, the pre-slice marker or NONE head back, an unscoped or completed Stage 25, full CAP-13, a second method
    # or consumer, a unit conversion or a broad CAP-13 activation is a reversal of the live truth.
    "stage 25 slice undone": (CHECKLIST, "current-routing", _S25_DELIVERED,
                              "`STAGE 25 — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1: NOT DELIVERED`"),
    "stage 25 back to not entered": (STATE, "current-position", _NS, _NS + " `STAGE 25: NOT ENTERED`"),
    "stage 25 pre-slice marker back": (CHECKLIST, "current-routing", _NS, _NS + " " + _S25_PRE_MARKER),
    "stage 25 complete": (ROADMAP, "current-routing", _S25_PARTIAL, "`STAGE 25: COMPLETE`"),
    "stage 25 complete in prose": (CONTRACT, "declaration", _NS, _NS + " Stage 25 is complete."),
    "full cap-13 authorized": (CONTRACT, "declaration", _S25_FULL_NO, "`FULL CAP-13: AUTHORIZED`"),
    "second cap-13 method admitted in prose": (ROADMAP, "current-routing", _NS,
                                               _NS + " A second CAP-13 method is admitted."),
    "cap-13 consumer added in prose": (CHECKLIST, "current-routing", _NS, _NS + " Another consumer is authorized."),
    "unit conversion authorized in prose": (STATE, "current-position", _NS, _NS + " Unit conversion is authorized."),
    "cap-13 broadly activated": ("CLAUDE.md", "head", _NONE_BOLD, _NONE_BOLD + " CAP-13 is fully activated."),
    "post-stage-16 none head back": (ROADMAP, "current-routing", "**NO ACTIVE CONTRACT — post-Stage-25-CAP-13-Slice-1 "
                                     "(2026-10-08); ", "**NO ACTIVE CONTRACT — post-Stage-16-closure (2026-10-06); "),
}

# The reversal cases are split for CI shard balance: the first half (by sorted name) runs here, the rest in
# tests/test_v132_derived_navigation_truth_live_truth_reversals_continued.py with the same test body.
_FIRST_HALF = (len(_MATERIAL_REVERSALS) + 1) // 2


@pytest.mark.parametrize("name", sorted(_MATERIAL_REVERSALS)[:_FIRST_HALF])
def test_every_material_reversal_is_caught(monkeypatch, name):
    path, region, old, new, *every = _MATERIAL_REVERSALS[name]
    real = _nav._read
    docs = _mutate(path, region, old, new, *every)
    fake = lambda p: docs[p] if p in docs else real(p)                   # noqa: E731
    assert _live_authority_problems(fake), name
    monkeypatch.setattr(_nav, "_read", fake)
    with pytest.raises(AssertionError):
        _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()


@pytest.mark.parametrize("name", ["stage 35 unticked", "another row ticked", "stage 35 row removed"])
def test_stage35_checkbox_and_count_drift_is_caught(monkeypatch, name):
    """ADDED at the Stage 35 first bounded slice; ROTATED at the Stage 35 closure: row 35 is ticked for the current
    bounded first-slice scope only, so unticking it, ticking any other open row or dropping it is checkbox / count drift
    the current-state guard rejects."""
    roadmap = _nav._read(ROADMAP)
    [row] = re.findall(r"^- \[x\] \*\*35 — .*$", roadmap, re.M)
    mutated = {"stage 35 unticked": roadmap.replace(row, row.replace("- [x]", "- [ ]", 1), 1),
               # ROTATED at the Stage 36 closure: row 36 is ticked now, so the next open row is 37
               "another row ticked": re.sub(r"^- \[ \] (\*\*37 — )", r"- [x] \1", roadmap, count=1, flags=re.M),
               "stage 35 row removed": roadmap.replace(row + "\n", "", 1)}[name]
    assert mutated != roadmap
    real = _nav._read
    monkeypatch.setattr(_nav, "_read", lambda p: mutated if p == ROADMAP else real(p))
    with pytest.raises(AssertionError):
        _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()


@pytest.mark.parametrize("name", ["stage 16 unticked", "another row ticked", "stage 16 row removed",
                                  "stage 13 ticked", "stage 14 ticked"])
def test_stage16_checkbox_and_count_drift_is_caught(monkeypatch, name):
    """ADDED at the Stage 16 closure: row 16 is ticked for the current bounded Technical + Integration
    evidence-sufficiency composition scope only, so unticking it, ticking any other open row (Stages 13 and 14 above all,
    which stay PARTIAL / DEFERRED) or dropping it is checkbox / count drift the current-state guard rejects."""
    roadmap = _nav._read(ROADMAP)
    [row] = re.findall(r"^- \[x\] \*\*16 — .*$", roadmap, re.M)
    mutated = {"stage 16 unticked": roadmap.replace(row, row.replace("- [x]", "- [ ]", 1), 1),
               "another row ticked": re.sub(r"^- \[ \] (\*\*17 — )", r"- [x] \1", roadmap, count=1, flags=re.M),
               "stage 16 row removed": roadmap.replace(row + "\n", "", 1),
               "stage 13 ticked": re.sub(r"^- \[ \] (\*\*13 — )", r"- [x] \1", roadmap, count=1, flags=re.M),
               "stage 14 ticked": re.sub(r"^- \[ \] (\*\*14 — )", r"- [x] \1", roadmap, count=1, flags=re.M)}[name]
    assert mutated != roadmap
    real = _nav._read
    monkeypatch.setattr(_nav, "_read", lambda p: mutated if p == ROADMAP else real(p))
    with pytest.raises(AssertionError):
        _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()


@pytest.mark.parametrize("name", ["stage 36 unticked", "another row ticked", "stage 36 row removed"])
def test_stage36_checkbox_and_count_drift_is_caught(monkeypatch, name):
    """ADDED at the Stage 36 closure: row 36 is ticked for the current no-live-AI / provider scope only, so unticking it,
    ticking any other open row or dropping it is checkbox / count drift the current-state guard rejects."""
    roadmap = _nav._read(ROADMAP)
    [row] = re.findall(r"^- \[x\] \*\*36 — .*$", roadmap, re.M)
    mutated = {"stage 36 unticked": roadmap.replace(row, row.replace("- [x]", "- [ ]", 1), 1),
               "another row ticked": re.sub(r"^- \[ \] (\*\*37 — )", r"- [x] \1", roadmap, count=1, flags=re.M),
               "stage 36 row removed": roadmap.replace(row + "\n", "", 1)}[name]
    assert mutated != roadmap
    real = _nav._read
    monkeypatch.setattr(_nav, "_read", lambda p: mutated if p == ROADMAP else real(p))
    with pytest.raises(AssertionError):
        _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()
