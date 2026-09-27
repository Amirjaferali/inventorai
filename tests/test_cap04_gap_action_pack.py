"""CAP-04 Slice 1 — the Actionable Gap Pack.

One read-only package per CURRENT unresolved gap of the canonical Requirement
Landscape, joining that gap's Validation Plan step and any routed need of the
exact same gap (by ``(gap_type, question_id)`` identity only). It asks nothing,
writes nothing, closes nothing and ranks nothing; a derivation that cannot be
trusted reads "unavailable", never "no gaps".

Synthetic data only. The one committed routing policy (mechanical
PHYSICAL_FEASIBILITY:Q2, SPECIALIST) is used as-is; an EVIDENCE route has no
committed policy, so it is exercised through a bounded fixture at the public
``routing_policies`` seam.
"""
import copy
import html
import re

import pytest

import engine.path_n_questions as pnq
import engine.validation_plan as vp
from engine.gap_action_pack import GapActionPackError, derive_gap_action_packs
from engine.idea_development_outputs import derive_next_development_step
from engine.idea_state import (
    ACCEPTED_RISK, CLOSED, OPEN, PARTIAL, Gap, IdeaState,
    BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY)
from engine.need_routing import (
    NeedRoutingRevision, OPERATION_RETRACT, OPERATION_ROUTE)
from engine.requirement_landscape import derive_requirement_landscape
from web.ui_text import UI_STRINGS, text

PF_QID = "mechanical:PHYSICAL_FEASIBILITY:Q2"
PF_POLICY = next(p for g, q, p in pnq.routing_policies("mechanical")
                 if (g, q) == (PHYSICAL_FEASIBILITY, PF_QID))


def _state(*gaps, domain="mechanical"):
    s = IdeaState(idea_id="cap04")
    s.domain = domain
    s.gaps = [Gap(gap_type=g, status=st, opened_at=0) for g, st in gaps]
    return s


def _rev(gap, qid, op=OPERATION_ROUTE, required="SPECIALIST", policy_ref=None,
         seq=0, supersedes=None):
    return NeedRoutingRevision(
        project_id="cap04", routing_seq=seq, gap_type=gap, question_id=qid,
        after_assertion_seq=-1, operation=op,
        required_input=required if op == OPERATION_ROUTE else None,
        policy_ref=policy_ref or PF_POLICY.policy_ref, supersedes_seq=supersedes,
        provenance="SYSTEM_INFERRED", event_key="nr:cap04:%s:%s:%s:%d" % (
            gap, qid, op, seq))


def _packs(state):
    return {p.gap_type: p for p in derive_gap_action_packs(state).packs}


# ---------------------------------------------------------------------------
# A–E: which gaps get a pack
# ---------------------------------------------------------------------------

def test_a_no_unresolved_gap_is_an_empty_result():
    result = derive_gap_action_packs(_state((MECHANISM_COMPLETENESS, CLOSED)))
    assert result.packs == () and result.accepted_risk_gap_types == ()


def test_b_open_gap_gets_one_pack_from_the_canonical_owners():
    s = _state((PHYSICAL_FEASIBILITY, OPEN))
    [pack] = derive_gap_action_packs(s).packs
    [req] = [r for r in derive_requirement_landscape(s).requirements
             if r.primary_anchor.anchor_kind == "gap"]
    [step] = [st for st in vp.derive_validation_plan(s).steps
              if st.provenance.anchor_kind == "gap"]
    assert pack.gap_state == "OPEN" and pack.source_status == req.source_status
    assert pack.display_label == req.primary_anchor.display_label
    assert pack.action_statement == req.resolving_action.statement
    assert pack.action_statement == "Address the open gap: Physical Feasibility."
    assert (pack.responsibility, pack.evidence_category, pack.closure_condition) == (
        step.responsibility, step.evidence_category, step.closure_condition)
    assert pack.routed_needs == ()


def test_c_partial_gap_stays_unresolved_and_gets_a_truthful_pack():
    [pack] = derive_gap_action_packs(_state((BOUNDARY_AMBIGUITY, PARTIAL))).packs
    assert pack.gap_state == "PARTIAL"
    assert pack.source_status == "partially addressed"


def test_d_closed_gap_gets_no_pack_and_accepted_risk_is_never_resolved():
    s = _state((MECHANISM_COMPLETENESS, CLOSED), (BOUNDARY_AMBIGUITY, ACCEPTED_RISK),
               (PHYSICAL_FEASIBILITY, OPEN))
    result = derive_gap_action_packs(s)
    assert [p.gap_type for p in result.packs] == [PHYSICAL_FEASIBILITY]
    assert result.accepted_risk_gap_types == (BOUNDARY_AMBIGUITY,)


def test_e_one_pack_per_gap_type_in_the_landscape_order():
    s = _state((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, PARTIAL),
               (MECHANISM_COMPLETENESS, OPEN))
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=PARTIAL, opened_at=1))
    packs = derive_gap_action_packs(s).packs
    gap_order = [r.primary_anchor.anchor_reference
                 for r in derive_requirement_landscape(s).requirements
                 if r.primary_anchor.anchor_kind == "gap"]
    assert [p.gap_type for p in packs] == gap_order
    assert len({p.gap_type for p in packs}) == len(packs) == 3
    # the collapsed PF pair keeps the landscape's "any OPEN" state
    assert {p.gap_type: p.gap_state for p in packs}[PHYSICAL_FEASIBILITY] == "OPEN"


# ---------------------------------------------------------------------------
# F–K: routed needs
# ---------------------------------------------------------------------------

def test_f_active_specialist_route_joins_its_exact_gap():
    s = _state((PHYSICAL_FEASIBILITY, OPEN))
    s.need_routing = [_rev(PHYSICAL_FEASIBILITY, PF_QID)]
    [need] = _packs(s)[PHYSICAL_FEASIBILITY].routed_needs
    assert need.available and need.required_input == "SPECIALIST"
    assert need.responsibility == vp.SPECIALIST_REQUIRED
    assert (need.need_text, need.need_text_ar) == (PF_POLICY.need_text,
                                                   PF_POLICY.need_text_ar)
    [step] = [st for st in vp.derive_validation_plan(s).steps
              if st.provenance.reference == "routing:%s:%s" % (PHYSICAL_FEASIBILITY, PF_QID)]
    assert (need.evidence_category, need.closure_condition) == (
        step.evidence_category, step.closure_condition)


def test_g_evidence_route_through_a_bounded_policy_fixture(monkeypatch):
    qid = "fixture:BOUNDARY_AMBIGUITY:Q9"
    policy = pnq.RoutingPolicy(
        required_input="EVIDENCE", policy_ref="fixture-evidence-v1",
        need_text="A boundary measurement is needed.",
        need_text_ar="يلزم قياس للحدود.", owner_input_prompt="x",
        owner_input_prompt_ar="س")
    monkeypatch.setattr(pnq, "routing_policies",
                        lambda domain: ((BOUNDARY_AMBIGUITY, qid, policy),))
    s = _state((BOUNDARY_AMBIGUITY, OPEN))
    s.need_routing = [_rev(BOUNDARY_AMBIGUITY, qid, required="EVIDENCE",
                           policy_ref="fixture-evidence-v1")]
    [need] = _packs(s)[BOUNDARY_AMBIGUITY].routed_needs
    assert need.available and need.required_input == "EVIDENCE"
    assert need.responsibility == vp.EMPIRICAL_EVIDENCE_REQUIRED
    assert need.need_text_ar == "يلزم قياس للحدود."


def test_h_retracted_route_does_not_render():
    s = _state((PHYSICAL_FEASIBILITY, OPEN))
    s.need_routing = [_rev(PHYSICAL_FEASIBILITY, PF_QID, seq=0),
                      _rev(PHYSICAL_FEASIBILITY, PF_QID, op=OPERATION_RETRACT, seq=1,
                           supersedes=0)]
    assert _packs(s)[PHYSICAL_FEASIBILITY].routed_needs == ()


def test_i_a_route_never_appears_under_another_gap():
    s = _state((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, OPEN))
    s.need_routing = [_rev(PHYSICAL_FEASIBILITY, PF_QID)]
    packs = _packs(s)
    assert len(packs[PHYSICAL_FEASIBILITY].routed_needs) == 1
    assert packs[BOUNDARY_AMBIGUITY].routed_needs == ()
    # a route whose gap has no unresolved pack is not turned into its own pack
    s2 = _state((BOUNDARY_AMBIGUITY, OPEN))
    s2.need_routing = [_rev(PHYSICAL_FEASIBILITY, PF_QID)]
    assert list(_packs(s2)) == [BOUNDARY_AMBIGUITY]


def test_j_no_route_invents_no_acquisition_method():
    [pack] = derive_gap_action_packs(_state((PHYSICAL_FEASIBILITY, OPEN))).packs
    assert pack.routed_needs == ()
    assert pack.evidence_category == "clarifying information"


@pytest.mark.parametrize("breakage", ["policy_ref", "required_input", "unknown_qid",
                                      "no_domain"])
def test_k_unreconcilable_route_fails_closed_without_guessing(breakage):
    s = _state((PHYSICAL_FEASIBILITY, OPEN))
    rev = _rev(PHYSICAL_FEASIBILITY, PF_QID)
    if breakage == "policy_ref":
        rev = _rev(PHYSICAL_FEASIBILITY, PF_QID, policy_ref="tampered")
    elif breakage == "required_input":
        rev = _rev(PHYSICAL_FEASIBILITY, PF_QID, required="EVIDENCE")
    elif breakage == "unknown_qid":
        rev = _rev(PHYSICAL_FEASIBILITY, "mechanical:PHYSICAL_FEASIBILITY:Q7")
    else:
        s.domain = None
    s.need_routing = [rev]
    [need] = _packs(s)[PHYSICAL_FEASIBILITY].routed_needs
    assert not need.available
    assert (need.need_text, need.need_text_ar, need.responsibility) == (None, None, None)


def test_structural_inconsistency_raises_instead_of_reporting_no_gaps(monkeypatch):
    s = _state((PHYSICAL_FEASIBILITY, OPEN))
    monkeypatch.setattr("engine.gap_action_pack.derive_validation_plan",
                        lambda state: vp.ValidationPlan(vp.OUTCOME_EMPTY, (), ()))
    with pytest.raises(GapActionPackError):
        derive_gap_action_packs(s)


# ---------------------------------------------------------------------------
# L–M, R: purity, determinism, owners unchanged
# ---------------------------------------------------------------------------

def test_l_m_r_pure_deterministic_and_owners_unchanged():
    s = _state((PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, PARTIAL))
    s.need_routing = [_rev(PHYSICAL_FEASIBILITY, PF_QID)]
    before = (copy.deepcopy(s.gaps), list(s.need_routing), copy.deepcopy(s.assertions),
              derive_requirement_landscape(s), vp.derive_validation_plan(s),
              derive_next_development_step(s))
    first = derive_gap_action_packs(s)
    assert derive_gap_action_packs(s) == first
    assert derive_gap_action_packs(copy.deepcopy(s)) == first
    assert (s.gaps, s.need_routing, s.assertions, derive_requirement_landscape(s),
            vp.derive_validation_plan(s), derive_next_development_step(s)) == before


def test_q_every_new_key_has_distinct_en_and_ar():
    keys = [k for k in UI_STRINGS if k.startswith("UI_GP_")]
    assert len(keys) >= 20
    for k in keys:
        en, ar = text(k, "en"), text(k, "ar")
        assert en.strip() and ar.strip() and en != ar, k
        assert re.search(r"[؀-ۿ]", ar), k


# ---------------------------------------------------------------------------
# N–P, Q: rendered surfaces
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "cap04.sqlite"))
    import web.app as appmod
    from tests.csrf_client import csrf_client
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod


SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")


def _answer(c, sid, value):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    data = {"response": value, "action": "answered",
            "answer_token": html.unescape(re.search(
                r'name="answer_token" value="([^"]+)"', page).group(1))}
    target = re.search(r'name="answer_target" value="([^"]*)"', page)
    if target:
        data["answer_target"] = html.unescape(target.group(1))
    c.post(f"/session/{sid}", data=data)


def _routed_project(c, appmod, lang="en"):
    from tests.test_safe_question_routing_pf_q2 import MECH
    with c.session_transaction() as session:
        session["ui_lang"] = lang
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for value in (MECH, MECH):
        _answer(c, sid, value)
    return sid


def _block(page, element_id, tag):
    m = re.search(r'<%s[^>]*\bid="%s"' % (tag, element_id), page)
    assert m, element_id
    depth, pos = 1, m.end()
    while depth:
        close = page.index("</%s>" % tag, pos)
        nested = re.compile(r"<%s\b" % tag).search(page, pos, close)
        if nested:
            depth, pos = depth + 1, nested.end()
        else:
            depth, pos = depth - 1, close + len(tag) + 3
    return page[m.start():pos]


FORBIDDEN = ("recommend", "severity", "priority", "ranked", "unsafe", "infeasible",
             "likely to fail", "test passed", "validated", "is ready", "approved",
             "laboratory", "supplier", "vendor")


def _no_controls(fragment):
    for tag in ("<form", "<input", "<textarea", "<select", "<button"):
        assert tag not in fragment, tag
    # no raw canonical token anywhere in the block, attributes included
    from tests.test_deliverable_hygiene import PROHIBITED_TOKENS
    for token in PROHIBITED_TOKENS:
        assert token not in fragment, token


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_n_q_session_pack_with_routed_need(client, lang):
    c, appmod = client
    sid = _routed_project(c, appmod, lang)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    block = _block(page, "gap-action-packs", "details")
    _no_controls(block)
    assert text("UI_GP_HEADING", lang) in block and text("UI_GP_INTRO", lang) in block
    assert 'data-gp-gap="physical-feasibility" data-gp-state="open"' in block
    assert text("UI_GP_STATE_OPEN", lang) in block
    assert html.escape("Address the open gap: Physical Feasibility.") in block
    route_text = PF_POLICY.need_text_ar if lang == "ar" else PF_POLICY.need_text
    assert html.escape(route_text) in block
    other = PF_POLICY.need_text if lang == "ar" else PF_POLICY.need_text_ar
    assert html.escape(other) not in block
    assert 'data-gp-resp="specialist-required"' in block
    assert text("UI_GP_RESP_SPECIALIST_REQUIRED", lang) in block
    assert text("UI_GP_AFTER", lang) in block
    for token in ("policy_ref", PF_POLICY.policy_ref, PF_QID, "routing_seq", "nr:"):
        assert token not in block, token
    hrefs = re.findall(r'href="([^"]*)"', block)
    assert hrefs == [f"/session/{sid}/deliverable#report-needs",
                     f"/session/{sid}/deliverable#report-validation-plan"]
    visible = html.unescape(re.sub(r"<[^>]+>", " ", block)).lower()
    for phrase in FORBIDDEN:
        assert phrase not in visible, phrase


def test_j_session_no_route_pack(client):
    c, appmod = client
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    block = _block(c.get(f"/session/{sid}").get_data(as_text=True),
                   "gap-action-packs", "details")
    assert 'data-gp-gap="mechanism-completeness"' in block
    assert text("UI_GP_NO_ROUTE", "en") in block
    assert "data-gp-route=" not in block


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_o_p_report_and_pdf_are_read_only_and_report_local(client, monkeypatch, lang):
    c, appmod = client
    sid = _routed_project(c, appmod, lang)
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    block = _block(report, "report-gap-action-packs", "div")
    _no_controls(block)
    assert "<details" not in block
    route_text = PF_POLICY.need_text_ar if lang == "ar" else PF_POLICY.need_text
    assert html.escape(route_text) in block
    hrefs = re.findall(r'href="([^"]*)"', block)
    assert hrefs == ["#report-needs", "#report-validation-plan"]
    for href in hrefs:
        assert f'id="{href[1:]}"' in report
    seen = {}
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: seen.setdefault("source", source) and b"%PDF-")
    c.post(f"/session/{sid}/deliverable.pdf", data={})
    pdf_block = _block(seen["source"], "report-gap-action-packs", "div")
    _no_controls(pdf_block)
    assert html.escape(route_text) in pdf_block


def test_unavailable_never_reads_as_no_gaps(client, monkeypatch):
    c, appmod = client
    sid = _routed_project(c, appmod)

    def boom(state):
        raise GapActionPackError("broken")
    monkeypatch.setattr("engine.gap_action_pack.derive_gap_action_packs", boom)
    block = _block(c.get(f"/session/{sid}").get_data(as_text=True),
                   "gap-action-packs", "details")
    assert "data-gp-unavailable" in block and "data-gp-empty" not in block
    assert text("UI_GP_EMPTY", "en") not in block and "broken" not in block


def test_cold_read_only_view_is_unavailable_not_empty(client):
    c, appmod = client
    sid = _routed_project(c, appmod)
    appmod.SESSION_STORE.pop(sid)
    block = _block(c.get(f"/session/{sid}").get_data(as_text=True),
                   "gap-action-packs", "details")
    assert "data-gp-unavailable" in block and "data-gp-empty" not in block


def test_no_gap_state_renders_the_truthful_empty_state(client):
    import web.app as appmod
    s = _state((MECHANISM_COMPLETENESS, CLOSED))
    ctx = appmod._gap_action_packs_context(s, "en")
    assert (ctx["status"], ctx["packs"]) == ("available", [])


def _fake_pack_set(need):
    from engine.gap_action_pack import GapActionPack, GapActionPackSet
    return GapActionPackSet(packs=(GapActionPack(
        PHYSICAL_FEASIBILITY, "req:gap:" + PHYSICAL_FEASIBILITY, "Physical Feasibility",
        "OPEN", "open", "Address the open gap: Physical Feasibility.", "UNDETERMINED",
        "clarifying information", "Closed when ...", (need,)),), accepted_risk_gap_types=())


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_routed_need_missing_language_text_is_unavailable_not_blank(monkeypatch, lang):
    import web.app as appmod
    from engine.gap_action_pack import RoutedNeed
    need = RoutedNeed(PHYSICAL_FEASIBILITY, PF_QID, "SPECIALIST", True,
                      "SPECIALIST_REQUIRED", "specialist input", "Closed when ...",
                      "Only English" if lang == "en" else " ",
                      " " if lang == "en" else "عربي فقط")
    monkeypatch.setattr("engine.gap_action_pack.derive_gap_action_packs",
                        lambda state: _fake_pack_set(need))
    other = "ar" if lang == "en" else "en"
    routed = appmod._gap_action_packs_context(_state(), other)["packs"][0]["routed"][0]
    assert routed["available"] is False and routed["need_text"] is None
    assert routed["responsibility"] is None and routed["closure_condition"] is None
    ok = appmod._gap_action_packs_context(_state(), lang)["packs"][0]["routed"][0]
    assert ok["available"] is True and ok["need_text"].strip()


def test_unknown_required_input_fails_closed_to_unavailable(monkeypatch):
    import web.app as appmod
    from engine.gap_action_pack import RoutedNeed
    need = RoutedNeed(PHYSICAL_FEASIBILITY, PF_QID, "SOMETHING_ELSE", False,
                      None, None, None, None, None)
    monkeypatch.setattr("engine.gap_action_pack.derive_gap_action_packs",
                        lambda state: _fake_pack_set(need))
    ctx = appmod._gap_action_packs_context(_state(), "en")
    assert (ctx["status"], ctx["packs"]) == ("unavailable", [])
