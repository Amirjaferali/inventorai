"""MG-8 bounded fix — the seed problem statement is captured truthfully.

`MG8-BOUNDED-FIX-IMPLEMENT-01` (Owner-authorized; adopts the read-only
adjudication `MG8-CURRENT-TIP-ADJUDICATION-01`, recommendation A — FIX).

Before the repair a problem statement typed at `/start` was stored verbatim in
the reconstruction envelope yet never captured as the problem carrier, because
the level-0 establishment branch gated capture on `quality >= REASONED` alone
and representative problem prose assesses ASSERTED as a rule. Downstream, the
package reported that no problem statement was established, the evidence
registry lost its problem slot, the problem-derived functional requirement
disappeared, the statement never entered safety-signal derivation, and the
saved-project page asked the inventor to share a problem they had just typed.

These tests prove the repair AND its invariants: capture carries the TRUE
assessed quality, capture alone never promotes maturity or touches the gap
lifecycle, the seed still never becomes a ledger record, replay reproduces the
same carrier, and the no-statement wording is preserved for states that really
have none. Every fixture is synthetic; no real project data is used.
"""
import copy
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine.deliverable_assembler import (
    _completeness, _resolved_problem, assemble_deliverable,
)
from engine.idea_state import (
    ASSERTED, Evidence, Gap, IdeaState, MECHANISM_COMPLETENESS, OPEN, REASONED,
)
from engine.progression_loop import assess_response, run_iteration
from engine.safety_signal import _inventor_texts
from engine.session_reconstruction import reconstruct_readonly_state
from tests.csrf_client import csrf_client

# (A) a representative problem-shaped seed: the class that reproduced MG-8.
SEED_PROBLEM = ("People in wheelchairs cannot cross the raised doorway step at "
                "my house. A folding ramp and hinge would help.")
# (B) a causal seed that already captured correctly before the repair.
SEED_REASONED = ("The problem is that wheelchair users cannot cross the raised "
                 "doorway step, so my folding ramp bridges it because the hinge "
                 "lets the panel rotate flat and the latch locks it under load.")
MECH_ANSWER = ("(1) unfolding: the operator lifts the handle and the panel "
               "rotates on the hinge until flat. (2) locking: the toggle latch "
               "snaps over the center rib and holds the panel rigid because the "
               "rib transfers load into the frame rail.")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db = str(tmp_path / "mg8.sqlite")
    monkeypatch.setenv("INVENTORAI_DB_PATH", db)
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod, db


def _start(c, seed, domain="mechanical"):
    r = c.post("/start", data={"idea": seed, "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _raw(c, sid, lang=None):
    if lang:
        assert c.post("/ui-language", data={"lang": lang}).status_code in (302, 303)
    body = c.get(f"/session/{sid}").get_data(as_text=True)
    if lang:
        c.post("/ui-language", data={"lang": "en"})
    return body


def _answer(c, sid, text):
    token = _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))
    r = c.post(f"/session/{sid}", data={"response": text,
                                        "answer_token": token,
                                        "action": "answered"})
    assert r.status_code == 302
    return r


def _fresh(idea_id="mg8"):
    s = IdeaState(idea_id=idea_id)
    s.domain = "mechanical"
    s.domain_signal = "mechanical"
    s.path = "N"
    return s


def _rows(db, sid, table):
    con = sqlite3.connect(db)
    try:
        return con.execute(
            f"SELECT COUNT(*) FROM {table} WHERE project_id=?", (sid,)).fetchone()[0]
    finally:
        con.close()


# ==========================================================================
# A — the seed that previously reproduced MG-8 is now captured, truthfully
# ==========================================================================
def test_a_problem_shaped_seed_is_captured_with_its_true_quality(client):
    c, appmod, db = client
    assert assess_response(SEED_PROBLEM, "mechanical") == ASSERTED   # the class
    sid = _start(c, SEED_PROBLEM)
    state = appmod.SESSION_STORE[sid]["state"]
    # captured — the defect is repaired
    assert state.idea_summary == SEED_PROBLEM
    # with the TRUE quality: nothing is promoted
    assert state.idea_summary_quality == ASSERTED
    # the durable seed is unchanged and still verbatim
    inputs = appmod._get_store().load_reconstruction_inputs(sid)
    assert inputs["seed_idea_text"] == SEED_PROBLEM
    # the evidence gate itself is untouched: an ASSERTED statement is NOT
    # promoted into the canonical problem evidence carrier
    assert state.known_problem is None


def test_a_the_resolver_and_package_carry_the_true_quality(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    state = appmod.SESSION_STORE[sid]["state"]
    resolved = _resolved_problem(state)
    assert resolved is not None and resolved.content == SEED_PROBLEM
    assert resolved.quality == ASSERTED            # never REASONED by assumption
    package = assemble_deliverable(copy.deepcopy(state))
    s2 = package["section_2_invention_summary"]
    assert s2["known_problem"] is not None
    assert s2["known_problem"]["content"] == SEED_PROBLEM
    assert s2["known_problem"]["quality"] == "Asserted"
    assert s2["known_problem_note"] is None
    # evidence registry regains its problem slot, at the true quality
    registry = package["_session_meta"]["evidence_registry"]
    problem = [e for e in registry if e["evidence_id"] == "EV-001"]
    assert len(problem) == 1 and problem[0]["content"] == SEED_PROBLEM
    # the problem-derived functional requirement is present again
    reqs = package["section_4_requirements"]["requirements"]
    functional = [r for r in reqs if r["type"] == "functional"]
    assert len(functional) == 1
    assert functional[0]["evidence_id"] == "EV-001"
    assert functional[0]["evidence_quality"] == "Asserted"


def test_a_legacy_states_keep_their_prior_quality_exactly(client):
    """A state carrying `idea_summary` but no recorded quality could only have
    been captured at REASONED or better, so it renders exactly as before."""
    s = _fresh("mg8-legacy")
    s.idea_summary = "A folding ramp that bridges a raised doorway step."
    assert getattr(s, "idea_summary_quality", None) is None
    resolved = _resolved_problem(s)
    assert resolved is not None and resolved.quality == REASONED


# ==========================================================================
# B — the causal control seed is unchanged
# ==========================================================================
def test_b_reasoned_seed_behaviour_is_unchanged(client):
    c, appmod, db = client
    assert assess_response(SEED_REASONED, "mechanical") == REASONED
    sid = _start(c, SEED_REASONED)
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.idea_summary == SEED_REASONED
    assert state.idea_summary_quality == REASONED
    assert state.known_problem is not None          # as before the repair
    assert state.known_problem.quality == REASONED
    assert state.maturity_level == 1                # the existing transition
    package = assemble_deliverable(copy.deepcopy(state))
    assert package["section_2_invention_summary"]["known_problem"]["quality"] \
        == "Reasoned"


# ==========================================================================
# C — empty / invalid seed behaviour
# ==========================================================================
def test_c_empty_seed_creates_nothing_and_captures_nothing(client):
    c, appmod, db = client
    assert c.post("/start", data={"idea": "", "domain_confirm": "mechanical"}
                  ).status_code == 302          # redirected home, no session
    assert appmod.SESSION_STORE == {}
    # the engine seam itself never captures an empty response
    s = _fresh("mg8-empty")
    run_iteration(s, "")
    assert s.idea_summary is None and s.idea_summary_quality is None
    assert _resolved_problem(s) is None


def test_c_a_state_with_no_statement_keeps_the_no_statement_wording():
    """The repair must NOT rewrite the honest absence case: a state that truly
    carries no problem statement still says so, and still receives the original
    level-0 rationale that asks for one."""
    s = _fresh("mg8-absent")
    assert _resolved_problem(s) is None
    assert _completeness(s) == "INCOMPLETE — problem statement not yet established"
    package = assemble_deliverable(copy.deepcopy(s))
    rec = package["section_7_recommendations"]["category_a_proceed_revise_block"]
    assert rec["verdict"] == "BLOCK"
    assert rec["rationale"] == ("Problem not yet established. Provide a clear "
                                "problem statement first.")


def test_c_a_recorded_statement_is_never_told_to_supply_one(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.maturity_level == 0
    package = assemble_deliverable(copy.deepcopy(state))
    rec = package["section_7_recommendations"]["category_a_proceed_revise_block"]
    assert rec["verdict"] == "BLOCK"                      # verdict unchanged
    assert "Provide a clear problem statement first" not in rec["rationale"]
    assert "A problem statement is recorded" in rec["rationale"]
    assert _completeness(state) == ("INCOMPLETE — problem statement recorded "
                                    "but not yet established as evidence")
    body = " ".join(
        c.get(f"/session/{sid}/deliverable").get_data(as_text=True).split())
    assert "problem statement not yet established" not in body
    assert "Problem signal not yet established" not in body
    assert "Problem evidence has not yet been captured clearly." not in body


# ==========================================================================
# D — reconstruction parity
# ==========================================================================
def test_d_cold_reconstruction_reproduces_the_captured_carrier(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    _answer(c, sid, MECH_ANSWER)
    live = appmod.SESSION_STORE[sid]["state"]
    live_summary = live.idea_summary
    live_quality = live.idea_summary_quality
    live_maturity = live.maturity_level
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1 and session.review.reconstructed
    cold = session.state
    assert cold.idea_summary == live_summary == SEED_PROBLEM
    assert cold.idea_summary_quality == live_quality == ASSERTED
    assert cold.maturity_level == live_maturity
    # no durable field was added for any of this
    con = sqlite3.connect(db)
    try:
        columns = [r[1] for r in con.execute("PRAGMA table_info(projects)")]
        record_columns = [r[1] for r in con.execute("PRAGMA table_info(records)")]
    finally:
        con.close()
    assert "idea_summary" not in columns
    assert "idea_summary_quality" not in columns
    assert record_columns == ["project_id", "seq", "record_id", "payload",
                              "idempotency_key"]


def test_d_the_cold_page_renders_the_repaired_state(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    appmod.SESSION_STORE.clear()
    body = " ".join(
        c.get(f"/session/{sid}/deliverable").get_data(as_text=True).split())
    assert SEED_PROBLEM in body
    assert "Problem evidence has not yet been captured clearly." not in body


# ==========================================================================
# E — capture alone never promotes maturity or moves the gap lifecycle
# ==========================================================================
def test_e_capture_alone_does_not_promote_maturity(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.idea_summary is not None          # captured
    assert state.maturity_level == 0               # and NOT promoted
    assert state.known_problem is None
    # gap lifecycle parity: the level-0 render opens exactly the mechanism gap
    # it always opened — capture adds none and closes none
    assert [(g.gap_type, g.status) for g in state.gaps] == [
        ("MECHANISM_COMPLETENESS", "OPEN")]
    assert state.current_stage == 2


def test_e_the_transition_gate_still_requires_reasoned_problem_evidence():
    from engine.progression_loop import evaluate_transition
    s = _fresh("mg8-gate")
    run_iteration(s, SEED_PROBLEM)                 # ASSERTED seed
    assert s.idea_summary is not None
    can, reason = evaluate_transition(s)
    assert can is False and reason == "Problem not yet established"
    assert s.maturity_level == 0
    # the REASONED control still transitions exactly as before
    s2 = _fresh("mg8-gate-2")
    run_iteration(s2, SEED_REASONED)
    assert s2.known_problem is not None and s2.maturity_level == 1


def test_e_sibling_eligibility_and_ordering_are_untouched():
    """The in-gap guard still requires eligibility (relevance), and the level-0
    branch still refuses to promote an ASSERTED answer into `known_problem`."""
    s = _fresh("mg8-sibling")
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0))
    off_gap = ("(1) pricing: the subscription tier structure follows the "
               "regional purchasing-power distribution. (2) marketing: the "
               "campaign sequencing follows the seasonal demand cycle. "
               "(3) partnerships: the distribution agreements follow the "
               "retailer certification timeline.")
    run_iteration(s, off_gap)
    assert s.known_problem is None                 # relevance conjunct intact
    # and an in-gap REASONED answer still establishes it
    s2 = _fresh("mg8-sibling-2")
    s2.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0))
    run_iteration(s2, MECH_ANSWER)
    assert s2.known_problem is not None


def test_e_the_captured_statement_is_never_the_ledger_or_a_second_store(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    assert appmod.SESSION_STORE[sid]["state"].assertions == []
    assert _rows(db, sid, "records") == 0
    _answer(c, sid, MECH_ANSWER)
    # exactly one record for the one answer — the seed added none
    assert _rows(db, sid, "records") == 1
    contract = appmod._get_store().load_contract(sid)
    assert len(contract.assertions) == 1
    assert contract.assertions[0].content == MECH_ANSWER


# ==========================================================================
# F — the statement now participates in the EXISTING safety-signal derivation
# ==========================================================================
def test_f_the_captured_statement_enters_safety_signal_derivation(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    state = appmod.SESSION_STORE[sid]["state"]
    sources = dict(_inventor_texts(state))
    assert sources.get("idea_summary") == SEED_PROBLEM
    # the existing derivation is reused as-is: no second scanner exists
    import engine.safety_signal as safety
    import inspect
    source = inspect.getsource(safety)
    assert "MG-8" not in source and "mg8" not in source


# ==========================================================================
# G — the level-0 stage wording no longer asks for what was supplied
# ==========================================================================
def test_g_the_session_stage_line_is_truthful_in_both_languages(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    en = " ".join(_raw(c, sid).split())
    assert SEED_PROBLEM in en                       # the description is shown
    assert "Share your idea" not in en              # and not requested again
    assert "Your description is saved." in en
    ar = " ".join(_raw(c, sid, lang="ar").split())
    assert "وصفك محفوظ." in ar
    assert "شارك فكرتك" not in ar
    from web.gap_labels import get_maturity_label
    for lang in ("en", "ar"):
        meaning = get_maturity_label(0, lang)["meaning"]
        assert meaning and "validated" not in meaning.lower()


def test_g_no_surface_claims_the_statement_is_validated(client):
    c, appmod, db = client
    sid = _start(c, SEED_PROBLEM)
    package = assemble_deliverable(
        copy.deepcopy(appmod.SESSION_STORE[sid]["state"]))
    s2 = package["section_2_invention_summary"]
    assert s2["known_problem"]["quality"] == "Asserted"
    assert s2["known_problem"]["validation_status"] == "UNVALIDATED"
    body = " ".join(
        c.get(f"/session/{sid}/deliverable").get_data(as_text=True).split())
    for forbidden in ("problem validated", "problem verified", "problem established as fact"):
        assert forbidden not in body.lower()
