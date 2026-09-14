"""G-3 — bounded decision-value repair.

Authoritative contract: docs/governance/G3_BOUNDED_DECISION_VALUE_REPAIR_CONTRACT_CANDIDATE.md
(authoritative via PR #598). Authoritative Owner decisions: OD-G3-1-WITHDRAWAL,
OD-G3-2-REFINEMENT and the OD-W2-DW-LIFT permission-(3) reading, recorded in
docs/governance/OWNER_DECISION_REGISTER.md (authoritative via PR #599).

The frozen §6.0 distinction these tests enforce:

  A. BOUNDED RENDERED ALTERNATIVE SET  — what the inventor can see, a
     user-withdrawn alternative included; derived from the ledger.
  B. FDC COMPARISON-ELIGIBLE CANDIDATE SET — `DecisionRecord.candidates`;
     a user withdrawal REMOVES the alternative from it (D-G3-1).

Visibility alone must create no decision-semantic consequence (A-24).
"""
from tests.csrf_client import csrf_client
import os, re, sys, html, copy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "g3.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod


SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
QUESTION = "Which latch mechanism should hold the ramp flat?"
ALT_A = "Toggle latch"
ALT_B = "Spring-loaded pin"
REASON = "not robust enough under repeated load"


def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _token(c, sid):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return html.unescape(m.group(1))


def _ledger(appmod, sid, disposition):
    st = appmod.SESSION_STORE[sid]["state"]
    return [r for r in st.assertions if r.disposition == disposition]


def _ctx(c, appmod, sid):
    c.post(f"/session/{sid}/decision/declare-context",
           data={"content": QUESTION, "answer_token": _token(c, sid)})
    return _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0].record_id


def _declare(c, sid, root, content):
    return c.post(f"/session/{sid}/decision/declare-alternative", data={
        "content": content, "context_root": root,
        "answer_token": _token(c, sid)})


def _refine(c, sid, head_id, content):
    return c.post(f"/session/{sid}/decision/refine-alternative", data={
        "content": content, "supersedes_record_id": head_id,
        "answer_token": _token(c, sid)})


def _withdraw(c, sid, head_id, reason=""):
    return c.post(f"/session/{sid}/decision/withdraw-alternative", data={
        "supersedes_record_id": head_id, "reason": reason,
        "answer_token": _token(c, sid)})


def _view(appmod, sid):
    from engine.decision_composition import decision_capture_view
    return decision_capture_view(appmod.SESSION_STORE[sid]["state"])


def _records(appmod, sid):
    from engine.decision_composition import compose_decision_records
    return compose_decision_records(appmod.SESSION_STORE[sid]["state"])


def _two_alts_one_withdrawn(c, appmod, sid, reason=REASON):
    """ALT_A declared and left active; ALT_B declared then withdrawn."""
    root = _ctx(c, appmod, sid)
    _declare(c, sid, root, ALT_A)
    _declare(c, sid, root, ALT_B)
    alts = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)
    b = [r for r in alts if r.content == ALT_B][0]
    _withdraw(c, sid, b.record_id, reason)
    return root, b.record_id


def _alt(view_ctx, name):
    for a in view_ctx["alternatives"]:
        if a["name"] == name:
            return a
    return None


# --- A-4a / A-5 — rendered boundedness and no silent disappearance -----------

def test_a4a_a5_withdrawn_alternative_stays_in_the_rendered_set(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    v = _view(appmod, sid)[0]
    names = [a["name"] for a in v["alternatives"]]
    assert names == [ALT_A, ALT_B], names          # exactly once each, ledger order
    assert _alt(v, ALT_B)["lifecycle_state"] == "withdrawn"
    assert _alt(v, ALT_A)["lifecycle_state"] == "active"


def test_a4a_no_fabricated_or_duplicated_entry(client):
    c, appmod = client
    sid = _start(c)
    root = _ctx(c, appmod, sid)
    v = _view(appmod, sid)[0]
    assert v["alternatives"] == []                 # declared nothing -> renders nothing
    _declare(c, sid, root, ALT_A)
    head = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)[0]
    _refine(c, sid, head.record_id, ALT_A + " with locking spring")
    v = _view(appmod, sid)[0]
    roots = [a["root"] for a in v["alternatives"]]
    assert roots == [head.record_id]               # a refinement is not a new entry


# --- A-4b / D-G3-1 — visible, but NOT a comparison-set member ----------------

def test_a4b_withdrawn_is_not_a_comparison_member(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    v = _view(appmod, sid)[0]
    assert _alt(v, ALT_B)["comparison_eligible"] is False
    assert _alt(v, ALT_B)["candidate_id"] is None
    assert _alt(v, ALT_A)["comparison_eligible"] is True
    rec = _records(appmod, sid)[0]
    assert [x.name for x in rec.candidates] == [ALT_A]


# --- A-24 — visibility creates no decision-semantic consequence --------------

def test_a24_visibility_has_no_readiness_or_accounting_consequence(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    with_withdrawn = _records(appmod, sid)[0]
    # differential: a ledger that never contained the withdrawn chain at all
    st = appmod.SESSION_STORE[sid]["state"]
    stripped = copy.deepcopy(st)
    drop = {r.record_id for r in stripped.assertions
            if r.disposition in (DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
                                 DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN)
            and (r.content == ALT_B or r.content == REASON)}
    stripped.assertions = [r for r in stripped.assertions
                           if r.record_id not in drop]
    from engine.decision_composition import compose_decision_records
    without = compose_decision_records(stripped)[0]
    assert with_withdrawn.readiness_status == without.readiness_status
    assert ([b.to_dict() for b in with_withdrawn.blocking_reasons]
            == [b.to_dict() for b in without.blocking_reasons])
    assert ([c_.to_dict() for c_ in with_withdrawn.candidates]
            == [c_.to_dict() for c_ in without.candidates])


# --- A-23(b) — no fabricated dispose_candidate() equivalent ------------------

def test_a23b_no_disposition_is_fabricated_for_a_withdrawal(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    rec = _records(appmod, sid)[0]
    for cand in rec.candidates:
        assert cand.option_status == "active"
        assert cand.disposition_basis is None
        assert cand.disposition_reason is None
    # the record remains canonically valid on its own terms
    assert rec.readiness_status in (
        "insufficient_information", "blocked_by_evidence_gap",
        "comparison_in_progress", "decision_ready_for_owner_review")


# --- A-22 — withdrawal is never rendered as an evidence-based elimination ----

@pytest.mark.parametrize("lang", ["en", "ar"])
def test_a22_withdrawal_is_not_presented_as_elimination(client, lang):
    from web import ui_text
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    with c.session_transaction() as fs:
        fs["ui_lang"] = lang
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert ui_text.UI_STRINGS["UI_G3_STATE_WITHDRAWN"][lang] in page
    for banned in ("eliminated", "Eliminated", "ELIMINATED",
                   "technically_selected", "approved", "validated",
                   "certified", "production_ready"):
        assert banned not in page


# --- A-1 / A-2 — reachable on BOTH served routes -----------------------------

def test_a1_a2_per_alternative_state_on_session_and_deliverable(client):
    from web import ui_text
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    for url in (f"/session/{sid}", f"/session/{sid}/deliverable"):
        page = c.get(url).get_data(as_text=True)
        assert ALT_A in page and ALT_B in page, url
        assert ui_text.UI_STRINGS["UI_G3_STATE_WITHDRAWN"]["en"] in page, url
        assert ui_text.UI_STRINGS["UI_G3_STATE_ACTIVE"]["en"] in page, url
        assert REASON in page, url


# --- A-7 / A-8 — the withdrawal reason, verbatim or governed --------------

def test_a7_withdrawal_reason_renders_verbatim(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid, reason=REASON)
    v = _view(appmod, sid)[0]
    assert _alt(v, ALT_B)["withdrawal_reason"] == REASON
    assert REASON in c.get(f"/session/{sid}").get_data(as_text=True)


def test_a8_missing_reason_renders_the_governed_copy_not_invention(client):
    from web import ui_text
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid, reason="")
    v = _view(appmod, sid)[0]
    assert _alt(v, ALT_B)["withdrawal_reason"] == ""
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert ui_text.UI_STRINGS["UI_G3_REASON_NOT_RECORDED"]["en"] in page


def test_s2_withdraw_form_offers_a_reason_input(client):
    c, appmod = client
    sid = _start(c)
    root = _ctx(c, appmod, sid)
    _declare(c, sid, root, ALT_A)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    form = page.split('decision/withdraw-alternative')[1].split('</form>')[0]
    assert 'name="reason"' in form


# --- A-9 — candidate_not_yet_comparable, for members only --------------------

def test_a9_not_comparable_reason_names_members_only(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    rec = _records(appmod, sid)[0]
    named = [b.affected_candidate_id for b in rec.blocking_reasons
             if b.code == "candidate_not_yet_comparable"]
    assert named == [f"cand-pn-{rec.candidates[0].candidate_id.rsplit('-', 1)[-1]}"]
    v = _view(appmod, sid)[0]
    assert _alt(v, ALT_A)["not_comparable"] is True
    assert _alt(v, ALT_B)["not_comparable"] is False


# --- S-3 / D-G3-2 — evidence state from the chain, never a ClaimItem ---------

def test_s3_evidence_state_derives_from_the_candidate_chain(client):
    c, appmod = client
    sid = _start(c)
    root = _ctx(c, appmod, sid)
    _declare(c, sid, root, ALT_A)
    head = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)[0]
    v = _view(appmod, sid)[0]
    assert _alt(v, ALT_A)["evidence_state"] == "no_recorded_detail"
    assert _alt(v, ALT_A)["refinement_count"] == 0
    _refine(c, sid, head.record_id, ALT_A + " with a locking spring")
    v = _view(appmod, sid)[0]
    a = v["alternatives"][0]
    assert a["evidence_state"] == "recorded_detail"
    assert a["refinement_count"] == 1
    assert a["name"] == ALT_A + " with a locking spring"   # latest active head
    assert a["root"] == head.record_id                     # identity preserved


def test_d_g3_2_refinement_is_never_promoted_to_a_claim_item(client):
    c, appmod = client
    sid = _start(c)
    root = _ctx(c, appmod, sid)
    _declare(c, sid, root, ALT_A)
    head = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)[0]
    _refine(c, sid, head.record_id, ALT_A + " rated to 200 kg")
    rec = _records(appmod, sid)[0]
    assert rec.inputs == []
    assert rec.constraints == []
    assert rec.evidence == []
    assert rec.readiness_status == "insufficient_information"


# --- D-G3-1 — redeclaration founds a NEW root; no silent reactivation --------

def test_redeclaration_after_withdrawal_founds_a_new_root(client):
    c, appmod = client
    sid = _start(c)
    root, withdrawn_head = _two_alts_one_withdrawn(c, appmod, sid)
    _declare(c, sid, root, ALT_B)
    v = _view(appmod, sid)[0]
    entries = [a for a in v["alternatives"] if a["name"] == ALT_B]
    assert len(entries) == 2                       # the withdrawn one is still shown
    states = sorted(a["lifecycle_state"] for a in entries)
    assert states == ["active", "withdrawn"]
    assert entries[0]["root"] != entries[1]["root"]


# --- A-10 / A-11 — truthful no-decision, no fabricated comparison -----------

def test_a10_a11_no_ranking_winner_or_invented_reason(client):
    from web import ui_text
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    rec = _records(appmod, sid)[0]
    assert rec.readiness_status == "insufficient_information"
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert ui_text.UI_STRINGS["UI_W2A_READINESS_NOTE"]["en"] in page
    for banned in ("best option", "recommended option", "winner", "ranked",
                   "superior", "Rank "):
        assert banned not in page


# --- A-12 / A-13 / A-14 — determinism, reconstruction, no persistence -------

def test_a12_composition_is_byte_identical_across_runs(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    import json
    a = json.dumps(_view(appmod, sid), sort_keys=True)
    b = json.dumps(_view(appmod, sid), sort_keys=True)
    assert a == b
    r1 = [r.to_record_dict() for r in _records(appmod, sid)]
    r2 = [r.to_record_dict() for r in _records(appmod, sid)]
    assert r1 == r2


def test_a13_cold_reconstruction_reproduces_the_same_rendered_set(client):
    import json
    from engine.decision_composition import decision_capture_view
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    live = json.dumps(_view(appmod, sid), sort_keys=True)
    appmod.SESSION_STORE.clear()                   # force cold reconstruction
    page = c.get(f"/session/{sid}")
    assert page.status_code in (200, 302)
    st = appmod.SESSION_STORE[sid]["state"]
    assert json.dumps(decision_capture_view(st), sort_keys=True) == live


def test_a14_composed_state_is_not_persisted(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    st = appmod.SESSION_STORE[sid]["state"]
    for attr in ("decision_records", "decision_capture", "_composed",
                 "candidates", "rendered_alternatives"):
        assert not hasattr(st, attr), attr


# --- A-15 / A-16 — EN/AR substantive parity ---------------------------------

def test_a15_a16_en_ar_render_the_same_substantive_state(client):
    from web import ui_text
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    seen = {}
    for lang in ("en", "ar"):
        with c.session_transaction() as fs:
            fs["ui_lang"] = lang
        page = c.get(f"/session/{sid}").get_data(as_text=True)
        seen[lang] = page
        assert ALT_A in page and ALT_B in page          # never translated
        assert REASON in page                           # user text verbatim
        assert ui_text.UI_STRINGS["UI_G3_STATE_WITHDRAWN"][lang] in page
        assert ui_text.UI_STRINGS["UI_G3_STATE_ACTIVE"][lang] in page
        assert ui_text.UI_STRINGS["UI_G3_NOT_COMPARABLE"][lang] in page
    assert 'dir="rtl"' in seen["ar"] and 'lang="ar"' in seen["ar"]
    # no engine-generated English prose leaks into the Arabic surface
    assert "lacks inputs to be compared" not in seen["ar"]


def test_g3_ui_strings_are_governed_en_ar_pairs():
    from web import ui_text
    for key in ("UI_G3_STATE_ACTIVE", "UI_G3_STATE_WITHDRAWN",
                "UI_G3_REASON_LABEL", "UI_G3_REASON_NOT_RECORDED",
                "UI_G3_NOT_COMPARABLE", "UI_G3_EVIDENCE_NONE",
                "UI_G3_EVIDENCE_RECORDED", "UI_G3_WITHDRAW_REASON_LABEL",
                "UI_G3_HISTORY_NOTE"):
        pair = ui_text.UI_STRINGS[key]
        assert pair["en"].strip() and pair["ar"].strip()
        assert pair["en"] != pair["ar"]


# --- A-3 — cold read-only view: state shows, mutation forms suppressed -------

def test_a3_cold_readonly_shows_state_and_suppresses_forms(client):
    c, appmod = client
    sid = _start(c)
    _two_alts_one_withdrawn(c, appmod, sid)
    appmod.SESSION_STORE[sid]["state"].domain = None
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert ALT_A in page and ALT_B in page
    assert "decision/withdraw-alternative" not in page
    assert "decision/refine-alternative" not in page


# --- A-17 / A-20 / A-21 — ownership and untouched lanes ---------------------

def test_a17_single_decisionrecord_construction_path():
    import engine.decision_composition as dc, inspect
    src = inspect.getsource(dc)
    assert src.count("DecisionRecord(") == 1
    assert "class DecisionRecord" not in src
    assert "sqlite" not in src and "json.dump" not in src


# The single public wording replacement authorized by the bounded three-file
# wording repair over the A-20/A-21 pin below. It removes the prohibited internal
# vocabulary token `system-derived` from the inventor-facing Section 6 empty-state
# qualification. Nothing else in engine/deliverable_assembler.py may differ from
# the pin: the guard reconstructs the pinned blob with EXACTLY this substitution
# and demands byte-equality, so any further assembler change fails.
_A20_ASSEMBLER_APPROVED_OLD = (
    '    "No system-derived risks were identified from the current session '
    'state.\\n\\n"\n')
_A20_ASSEMBLER_APPROVED_NEW = (
    '    "No risks were identified by the system from the current session '
    'state.\\n\\n"\n')


# MG-8 bounded fix (`MG8-BOUNDED-FIX-IMPLEMENT-01`, Owner-authorized §5 pin
# amendment): the EXHAUSTIVE, ordered table of additional replacements allowed
# over the A-20/A-21 assembler pin, applied AFTER the A-20 wording replacement
# above. The guard reconstructs the pinned blob by applying the A-20 line and
# then every entry here, and still demands byte-equality, so any assembler
# change outside this table fails exactly as before. This is a bounded
# amendment for ONE defect, not a newer baseline and not a broad exemption.
#
# Previous behaviour (the pinned bytes): the level-0 maturity label claimed the
# problem SIGNAL was not established; the two level-0 verdict rationales told
# every inventor to provide a problem statement first; the completeness line
# said no problem statement was established; and the problem resolver wrapped
# `idea_summary` as REASONED unconditionally.
# Why MG-8 requires the change: the capture seam now records a problem
# statement whatever its assessed quality, so (a) the resolver must carry the
# TRUE quality or it would promote an ASSERTED statement, and (b) the three
# wordings above would otherwise tell an inventor who supplied a problem
# statement that none exists, and instruct them to supply it again.
# New behaviour: the resolver carries the recorded quality (legacy states,
# which have none, keep REASONED exactly as before); the level-0 label names
# the evidence threshold; and the rationale and completeness lines select a
# recorded-but-not-yet-established sentence ONLY when a statement is actually
# recorded, leaving the original no-statement sentences in place otherwise.
# Unrelated sections: every other section builder, verdict value, key set and
# rationale is byte-identical to the pin, which this guard proves.
_MG8_ASSEMBLER_SUBSTITUTIONS = (
    (  # [2]
        '    0: "Level 0 — Problem signal not yet established",\n',
        '    0: "Level 0 — Problem evidence not yet established",\n'),
    (  # [3]
        '        "Problem not yet established and open gaps recorded."),\n',
        '        "Problem not yet established and open gaps recorded."),\n'
        '}\n'
        '# MG-8: the two level-0 rationales above address an inventor who has supplied\n'
        '# NOTHING. When a problem statement HAS been recorded but has not reached the\n'
        '# evidence threshold, those words falsely instruct the inventor to provide what\n'
        '# they already provided, so the rationale below is used instead. The verdict\n'
        '# value, the key set and every other rationale are unchanged; only which of the\n'
        '# two truthful level-0 sentences is shown depends on the recorded state.\n'
        '_RECOMMENDATION_A_LEVEL0_RECORDED = {\n'
        '    False: ("BLOCK",\n'
        '        "A problem statement is recorded but has not yet reached the evidence "\n'
        '        "level needed to establish the problem. Strengthen it with specifics "\n'
        '        "before proceeding; it is not established evidence yet."),\n'
        '    True:  ("BLOCK",\n'
        '        "A problem statement is recorded but has not yet reached the evidence "\n'
        '        "level needed to establish the problem, and open gaps remain."),\n'),
    (  # [4]
        '        ("REVISE", "Insufficient evidence to recommend proceeding."))\n',
        '        ("REVISE", "Insufficient evidence to recommend proceeding."))\n'
        '    # MG-8: at level 0 ONLY, distinguish "a statement is recorded but is not yet\n'
        '    # established evidence" from "no statement was supplied". Same BLOCK verdict\n'
        '    # either way; no maturity, gap or eligibility input changes.\n'
        '    if key[0] == 0 and _resolved_problem(state) is not None:\n'
        '        verdict, rationale = _RECOMMENDATION_A_LEVEL0_RECORDED[key[1]]\n'),
    (  # [5]
        '        # idea_summary is captured only from a REASONED+ problem-establishment\n'
        '        # response; wrap it for uniform rendering. No quality is fabricated above\n'
        '        # what the capture path already guarantees.\n'
        '        return Evidence(content=summary, quality=REASONED, iteration=0)\n',
        "        # MG-8: the capture seam records the statement's TRUE assessed quality\n"
        '        # alongside it, so the wrapper carries that quality instead of assuming\n'
        '        # one. A legacy state has no recorded quality and could only have been\n'
        '        # captured at REASONED or better, so it keeps exactly its prior tier.\n'
        '        # Nothing is promoted: an ASSERTED statement renders as ASSERTED.\n'
        '        return Evidence(\n'
        '            content=summary,\n'
        '            quality=getattr(state, "idea_summary_quality", None) or REASONED,\n'
        '            iteration=0)\n'),
    (  # [6]
        '        return "PARTIAL — mechanism or boundaries still required"\n',
        '        return "PARTIAL — mechanism or boundaries still required"\n'
        '    # MG-8: an inventor who recorded a problem statement is never told that no\n'
        '    # problem statement exists; the honest difference is the evidence level.\n'
        '    if _resolved_problem(state) is not None:\n'
        '        return ("INCOMPLETE — problem statement recorded but not yet "\n'
        '                "established as evidence")\n'),
)


def test_a20_a21_dw_lane_and_assembler_untouched():
    import subprocess
    base = "f96c1900a0f5d0831a7654223ae4e008d4df961e"
    root = os.path.join(os.path.dirname(__file__), "..")

    # A-20/A-21, unchanged rule: the decision-workspace lane stays byte-identical
    # to the pin — no diff of any kind is tolerated.
    out = subprocess.run(["git", "diff", "--name-only", base, "--",
                          "engine/decision_workspace.py"],
                         capture_output=True, text=True, cwd=root)
    assert out.stdout.strip() == "", "engine/decision_workspace.py"

    # A-20/A-21, same pin, bounded exception: engine/deliverable_assembler.py is
    # still frozen against `base`; the ONLY authorized difference is the one-line
    # public wording replacement above. Reconstructing the pinned blob with that
    # exact substitution must reproduce the working file byte for byte. This is
    # not a broad exemption and not a newer baseline: any other assembler edit,
    # anywhere in the file, makes the reconstruction differ and fails the test.
    pinned = subprocess.run(
        ["git", "show", base + ":engine/deliverable_assembler.py"],
        capture_output=True, cwd=root)
    assert pinned.returncode == 0, "pinned engine/deliverable_assembler.py unavailable"
    pinned_text = pinned.stdout.decode("utf-8")
    assert pinned_text.count(_A20_ASSEMBLER_APPROVED_OLD) == 1, (
        "the pinned assembler no longer carries the exact authorized wording line")
    expected = pinned_text.replace(_A20_ASSEMBLER_APPROVED_OLD,
                                   _A20_ASSEMBLER_APPROVED_NEW)
    # MG-8 bounded amendment: apply the exhaustive authorized table, in order.
    # Each anchor must still occur exactly once, so a drifting pin fails loudly
    # instead of silently matching somewhere else.
    for _old, _new in _MG8_ASSEMBLER_SUBSTITUTIONS:
        assert expected.count(_old) == 1, (
            "an authorized MG-8 anchor is missing or no longer unique")
        expected = expected.replace(_old, _new)
    with open(os.path.join(root, "engine", "deliverable_assembler.py"),
              encoding="utf-8") as fh:
        actual = fh.read()
    assert actual == expected, "engine/deliverable_assembler.py"
