"""
Per-experiment owner-defined success criteria (planning metadata only).

A user opens /session/<sid>/success-criteria, enters/edits one criterion per
currently-generated Prototype & Test Plan experiment, saves, and sees each
criterion in FDC-001 as explicitly user-defined. Criteria are NEVER graded,
validated, claimed met, or written to the ILT-002 transcript, and they never
change progression, maturity, gaps, Evidence, experiment IDs, or plan text.
"""
from tests.csrf_client import csrf_client
import os, sys, uuid, dataclasses
import copy
import html
import re

import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.idea_state import (
    IdeaState, Gap, Evidence, AcknowledgedUnknown, SuccessCriterion,
    CLOSED, REASONED, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
)
from engine.deliverable_assembler import assemble_deliverable
from web.app import app, SESSION_STORE, MAX_CRITERION_LENGTH

PREFIX = "criterion__"
REQUIRED = "Owner-defined criterion required."


def _gap(s, gap_type, *evidence, status=CLOSED):
    g = Gap(gap_type=gap_type, status=status, opened_at=0)
    for c in evidence:
        g.evidence.append(Evidence(c, REASONED, 1))
    s.gaps.append(g)
    return g


def _seed(unknown="I do not know how many wrong attempts should trigger lockout",
          assumption="the stored code must stay secret for the lock to work",
          mech="a keypad enters a code and on a match the controller drives a bolt"):
    sid = "sc-" + uuid.uuid4().hex[:8]
    s = IdeaState(idea_id=sid)
    s.domain = "electronics_electrical"; s.domain_signal = "electronics_electrical"
    s.maturity_level = 2; s.current_stage = 3
    if unknown:
        s.acknowledged_unknowns.append(AcknowledgedUnknown(
            iteration=5, gap_context=ASSUMPTION_INVENTORY, verbatim=unknown,
            category_basis="explicit"))
    if assumption:
        _gap(s, ASSUMPTION_INVENTORY, assumption)
    if mech:
        s.known_problem = Evidence("a clear lock problem statement", REASONED, 0)
        s.known_mechanism = Evidence(mech, REASONED, 0)
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": []}
    return sid, s


def _ids(s):
    return [it["experiment_id"]
            for it in assemble_deliverable(s)["section_11_prototype_test_plan"]["items"]]


def _snap(s):
    return (s.maturity_level, [(g.gap_type, g.status) for g in s.gaps],
            getattr(s.known_mechanism, "quality", None), s.iteration,
            len(s.acknowledged_unknowns))


def _post(client, sid, mapping):
    return client.post(f"/session/{sid}/success-criteria",
                       data={PREFIX + k: v for k, v in mapping.items()},
                       follow_redirects=False)


# === Data model (1-4) =======================================================

def test_1_new_state_has_empty_success_criteria():
    assert IdeaState(idea_id="x").success_criteria == {}


def test_2_existing_construction_backward_compatible():
    s = IdeaState(idea_id="x")          # no success_criteria arg
    assert isinstance(s.success_criteria, dict) and s.success_criteria == {}
    dataclasses.asdict(s)                # must not raise


def test_3_criteria_distinct_from_evidence_and_gaps():
    _, s = _seed()
    eid = _ids(s)[0]
    s.success_criteria[eid] = SuccessCriterion("my target")
    # not in any Evidence / gap evidence / acknowledged unknown
    assert all(getattr(e, "content", None) != "my target"
               for g in s.gaps for e in g.evidence)
    assert all(u.verbatim != "my target" for u in s.acknowledged_unknowns)


def test_4_criteria_do_not_alter_maturity_or_progression():
    _, s = _seed()
    before = _snap(s)
    s.success_criteria[_ids(s)[0]] = SuccessCriterion("a target")
    assert _snap(s) == before


# === Stable identity (5-8) ==================================================

def test_5_criterion_stored_by_experiment_id():
    sid, s = _seed()
    eid = _ids(s)[0]
    _post(csrf_client(app), sid, {eid: "alarm within the user-chosen window"})
    assert s.success_criteria[eid].criterion == "alarm within the user-chosen window"
    assert s.success_criteria[eid].provenance == "user_defined"


def test_6_regenerated_plan_reattaches_to_correct_experiment():
    sid, s = _seed()
    eid = _ids(s)[1]
    s.success_criteria[eid] = SuccessCriterion("attach here only")
    items = assemble_deliverable(s)["section_11_prototype_test_plan"]["items"]
    for it in items:
        if it["experiment_id"] == eid:
            assert it["success_criterion"] == "attach here only"
            assert it["success_criterion_provenance"] == "user_defined"
        else:
            assert it["success_criterion"] == REQUIRED


def test_7_list_order_does_not_misattach():
    _, s = _seed()
    ids = _ids(s)
    s.success_criteria[ids[2]] = SuccessCriterion("third only")
    items = assemble_deliverable(s)["section_11_prototype_test_plan"]["items"]
    captured = {it["experiment_id"]: it["success_criterion_status"] for it in items}
    assert captured[ids[2]] == "captured"
    assert captured[ids[0]] == "required" and captured[ids[1]] == "required"


def test_8_two_assumption_experiments_hold_different_criteria():
    sid, s = _seed(unknown=None, assumption=None, mech=None)
    _gap(s, ASSUMPTION_INVENTORY,
         "first assumption about cold-weather battery longevity",
         "second assumption about radio range through concrete")
    ids = _ids(s)
    assert len(ids) == 2
    _post(csrf_client(app), sid, {ids[0]: "crit A", ids[1]: "crit B"})
    assert s.success_criteria[ids[0]].criterion == "crit A"
    assert s.success_criteria[ids[1]].criterion == "crit B"


# === GET page (9-13) ========================================================

def test_9_10_11_12_get_lists_experiments_and_distinguishes_from_result():
    sid, s = _seed()
    ids = _ids(s)
    s.success_criteria[ids[0]] = SuccessCriterion("prefilled target one")
    body = csrf_client(app).get(f"/session/{sid}/success-criteria").get_data(as_text=True)
    # 9: lists all current experiments
    for it in assemble_deliverable(s)["section_11_prototype_test_plan"]["items"]:
        assert it["experiment_title"] in body
        assert (PREFIX + it["experiment_id"]) in body          # 11: input per experiment
    assert "prefilled target one" in body                       # 10: own criterion prefilled
    low = body.lower()
    assert "not a test result" in low or "not validate" in low  # 12: criterion != result


def test_13_unknown_session_redirects():
    r = csrf_client(app).get("/session/does-not-exist/success-criteria",
                              follow_redirects=False)
    assert r.status_code == 302
    assert "/session/" not in r.headers.get("Location", "")


# === POST (14-23) ===========================================================

def test_14_valid_criterion_saved():
    sid, s = _seed()
    r = _post(csrf_client(app), sid, {_ids(s)[0]: "a saved target"})
    assert r.status_code == 302
    assert s.success_criteria[_ids(s)[0]].criterion == "a saved target"


def test_15_criterion_can_be_edited():
    sid, s = _seed(); eid = _ids(s)[0]
    c = csrf_client(app)
    _post(c, sid, {eid: "first"})
    _post(c, sid, {eid: "second edited"})
    assert s.success_criteria[eid].criterion == "second edited"


def test_16_whitespace_trimmed_internal_preserved():
    sid, s = _seed(); eid = _ids(s)[0]
    _post(csrf_client(app), sid, {eid: "   keep  inner   spacing   "})
    assert s.success_criteria[eid].criterion == "keep  inner   spacing"


def test_17_whitespace_only_removes_criterion():
    sid, s = _seed(); eid = _ids(s)[0]
    c = csrf_client(app)
    _post(c, sid, {eid: "present"})
    assert eid in s.success_criteria
    _post(c, sid, {eid: "    "})
    assert eid not in s.success_criteria


def test_18_unknown_experiment_id_rejected():
    sid, s = _seed()
    before = dict(s.success_criteria)
    r = _post(csrf_client(app), sid, {"exp_v1_acknowledged_unknown_" + "0"*32: "x"})
    assert r.status_code == 400
    assert s.success_criteria == before


def test_19_stale_experiment_id_rejected():
    sid, s = _seed()
    stale_id = "exp_v1_reasoned_leading_claim_" + "a"*32   # not in current plan
    r = _post(csrf_client(app), sid, {stale_id: "x"})
    assert r.status_code == 400
    assert stale_id not in s.success_criteria


def test_20_over_limit_rejected_without_partial_save():
    sid, s = _seed(); ids = _ids(s)
    r = _post(csrf_client(app), sid,
              {ids[0]: "ok", ids[1]: "a" * (MAX_CRITERION_LENGTH + 1)})
    assert r.status_code == 400
    assert ids[0] not in s.success_criteria          # the valid one was NOT saved
    assert ids[1] not in s.success_criteria


def test_21_multiple_criteria_saved_in_one_request():
    sid, s = _seed(); ids = _ids(s)
    _post(csrf_client(app), sid, {ids[0]: "c0", ids[1]: "c1", ids[2]: "c2"})
    assert [s.success_criteria[i].criterion for i in ids] == ["c0", "c1", "c2"]


def test_22_no_transcript_entry_written():
    sid, s = _seed(); eid = _ids(s)[0]
    path = f"/tmp/ilt002_transcript_{sid}.jsonl"
    if os.path.exists(path):
        os.remove(path)
    _post(csrf_client(app), sid, {eid: "no transcript please"})
    assert not os.path.exists(path)
    assert SESSION_STORE[sid]["transcript"] == []


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_experiment_context_matches_current_payload_without_state_change(lang):
    from web.ui_text import text
    sid, state = _seed(unknown='Unknown <img src=x> العربية & details')
    client = csrf_client(app)
    with client.session_transaction() as session:
        session['ui_lang'] = lang
    items = assemble_deliverable(state)['section_11_prototype_test_plan']['items']
    before = copy.deepcopy(state.__dict__)
    response = client.get(f'/session/{sid}/success-criteria')
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert response.headers['Cache-Control'] == 'no-store'
    cards = body.split('<div class="exp">')[1:]
    assert len(cards) == len(items)
    for card, item in zip(cards, items):
        eid = item['experiment_id']
        values = [html.unescape(value) for value in re.findall(r'<dd dir="auto">(.*?)</dd>', card, re.S)]
        assert values == [item[key] for key in ('objective', 'minimum_prototype',
                                               'what_to_observe', 'failure_or_revision_condition')]
        assert f'name="criterion__{eid}"' in card
        assert f'id="criterion-guidance-{eid}"' in card
        assert text('UI_SC_LIMIT', lang).format(limit=MAX_CRITERION_LENGTH) in card
        assert text('UI_SC_SAVE_CLEAR', lang) in card
        assert '<details class="experiment-context">' in card
    assert '<img src=x>' not in body
    assert '<script' not in body
    assert state.__dict__ == before


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_empty_plan_and_rejection_preserve_context_contract(lang):
    sid, state = _seed(unknown=None, assumption=None, mech=None)
    client = csrf_client(app)
    with client.session_transaction() as session:
        session['ui_lang'] = lang
    body = client.get(f'/session/{sid}/success-criteria').get_data(as_text=True)
    assert 'class="experiment-context"' not in body
    assert 'name="criterion__' not in body
    sid, state = _seed()
    eid = _ids(state)[0]
    state.success_criteria[eid] = SuccessCriterion('existing target')
    state.success_criteria['stale-id'] = SuccessCriterion('preserved stale target')
    before = copy.deepcopy(state.__dict__)
    response = _post(client, sid, {eid: 'x' * (MAX_CRITERION_LENGTH + 1)})
    assert response.status_code == 400
    body = response.get_data(as_text=True)
    assert 'class="experiment-context"' in body
    assert 'class="stale"' in body
    assert 'existing target</textarea>' in body
    assert state.__dict__ == before


def test_23_only_planning_metadata_changes_in_session():
    sid, s = _seed(); eid = _ids(s)[0]
    before = _snap(s)
    _post(csrf_client(app), sid, {eid: "target"})
    assert _snap(s) == before                        # maturity/gaps/evidence/iteration unchanged
    assert eid in s.success_criteria


# === Deliverable output (24-30) =============================================

def test_24_missing_criterion_displays_required():
    _, s = _seed()
    items = assemble_deliverable(s)["section_11_prototype_test_plan"]["items"]
    assert all(it["success_criterion"] == REQUIRED for it in items)


def test_25_captured_criterion_displays_user_defined():
    sid, s = _seed(); eid = _ids(s)[0]
    s.success_criteria[eid] = SuccessCriterion("homeowner hears the alarm in time")
    body = csrf_client(app).get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "Success criterion — user-defined:" in body
    assert "homeowner hears the alarm in time" in body


def test_26_user_numbers_verbatim_not_claimed_valid():
    sid, s = _seed(); eid = _ids(s)[0]
    s.success_criteria[eid] = SuccessCriterion("alarm sounds within 30 seconds")
    body = csrf_client(app).get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "alarm sounds within 30 seconds" in body          # number shown verbatim
    assert "Success criterion — user-defined:" in body       # labeled as the user's target
    low = body.lower()
    # the criterion must not be presented as achieved/validated/approved
    for w in ("criterion met", "criterion was met", "criterion validated",
              "criterion approved", "expert-confirmed"):
        assert w not in low


def test_27_no_criterion_described_as_met():
    sid, s = _seed(); eid = _ids(s)[0]
    s.success_criteria[eid] = SuccessCriterion("works reliably")
    pkg = assemble_deliverable(s)["section_11_prototype_test_plan"]
    for it in pkg["items"]:
        assert it["success_criterion_status"] in ("captured", "required")  # never 'met'


def test_28_stale_criteria_preserved_and_surfaced():
    sid, s = _seed()
    stale_id = "exp_v1_acknowledged_unknown_" + "f"*32       # not generated now
    s.success_criteria[stale_id] = SuccessCriterion("orphaned target text")
    pkg = assemble_deliverable(s)["section_11_prototype_test_plan"]
    assert pkg["stale_criteria_notice"]
    assert any(x["experiment_id"] == stale_id and x["criterion"] == "orphaned target text"
               for x in pkg["stale_criteria"])
    # not reattached to any current experiment
    assert all(it["success_criterion"] != "orphaned target text" for it in pkg["items"])
    body = csrf_client(app).get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "no longer matches a current proposed experiment" in body


def test_29_criteria_do_not_change_generation_order_ids_or_text():
    _, s = _seed()
    before = assemble_deliverable(s)["section_11_prototype_test_plan"]
    base = [(it["experiment_id"], it["experiment_title"], it["objective"],
             it["minimum_prototype"]) for it in before["items"]]
    s.success_criteria[before["items"][0]["experiment_id"]] = SuccessCriterion("t")
    after = assemble_deliverable(s)["section_11_prototype_test_plan"]
    assert [(it["experiment_id"], it["experiment_title"], it["objective"],
             it["minimum_prototype"]) for it in after["items"]] == base


def test_30_sections_1_to_10_unchanged_by_criteria():
    _, s = _seed()
    before = assemble_deliverable(s)
    # trailing underscore so "section_1_" does not match "section_11_..."
    keys = tuple(f"section_{i}_" for i in range(1, 11))
    snap = {k: v for k, v in before.items() if k.startswith(keys)}
    assert len(snap) == 10
    s.success_criteria[_ids(s)[0]] = SuccessCriterion("t")
    after = assemble_deliverable(s)
    for k in snap:
        assert after[k] == snap[k]


# === Security & integrity (31-35) ===========================================

def test_31_html_is_escaped():
    sid, s = _seed(); eid = _ids(s)[0]
    s.success_criteria[eid] = SuccessCriterion("<script>alert(1)</script>")
    body = csrf_client(app).get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;" in body


def test_32_unknown_id_not_accepted():
    sid, s = _seed()
    r = _post(csrf_client(app), sid, {"totally_bogus_id": "x"})
    assert r.status_code == 400
    assert "totally_bogus_id" not in s.success_criteria


def test_33_34_35_no_evidence_gap_or_maturity_change():
    sid, s = _seed(); eid = _ids(s)[0]
    mech_q = s.known_mechanism.quality
    gap_status = [(g.gap_type, g.status) for g in s.gaps]
    maturity = s.maturity_level
    _post(csrf_client(app), sid, {eid: "target"})
    assert s.known_mechanism.quality == mech_q                 # 33: no quality upgrade
    assert [(g.gap_type, g.status) for g in s.gaps] == gap_status  # 34: no gap closed
    assert s.maturity_level == maturity                        # 35: no maturity change


# === POST atomicity & partial-submission contract ===========================

def test_atomic_reject_preserves_a_valid_field_when_another_is_unknown():
    sid, s = _seed(); ids = _ids(s)
    r = csrf_client(app).post(
        f"/session/{sid}/success-criteria",
        data={PREFIX + ids[0]: "a valid one",
              PREFIX + ("exp_v1_acknowledged_unknown_" + "9" * 32): "rogue"},
        follow_redirects=False)
    assert r.status_code == 400
    assert ids[0] not in s.success_criteria          # valid field NOT applied (atomic)


def test_omitted_field_leaves_existing_criterion_unchanged():
    sid, s = _seed(); ids = _ids(s)
    c = csrf_client(app)
    _post(c, sid, {ids[0]: "keep me", ids[1]: "and me"})
    # second request omits ids[0] entirely; updates only ids[1]
    c.post(f"/session/{sid}/success-criteria",
           data={PREFIX + ids[1]: "updated only"}, follow_redirects=False)
    assert s.success_criteria[ids[0]].criterion == "keep me"      # untouched
    assert s.success_criteria[ids[1]].criterion == "updated only"


def test_partial_valid_request_does_not_delete_other_criteria():
    sid, s = _seed(); ids = _ids(s)
    c = csrf_client(app)
    _post(c, sid, {ids[0]: "first", ids[1]: "second", ids[2]: "third"})
    _post(c, sid, {ids[1]: "second-edited"})        # only one field present
    assert s.success_criteria[ids[0]].criterion == "first"
    assert s.success_criteria[ids[2]].criterion == "third"
    assert s.success_criteria[ids[1]].criterion == "second-edited"


def test_repeated_identical_submission_is_idempotent():
    sid, s = _seed(); eid = _ids(s)[0]
    c = csrf_client(app)
    _post(c, sid, {eid: "stable target"})
    _post(c, sid, {eid: "stable target"})
    assert s.success_criteria[eid].criterion == "stable target"
    assert len(s.success_criteria) == 1


def test_rejected_submission_writes_no_transcript():
    sid, s = _seed()
    path = f"/tmp/ilt002_transcript_{sid}.jsonl"
    if os.path.exists(path):
        os.remove(path)
    r = _post(csrf_client(app), sid, {"exp_v1_bogus_" + "0" * 32: "x"})
    assert r.status_code == 400
    assert not os.path.exists(path)
    assert SESSION_STORE[sid]["transcript"] == []
