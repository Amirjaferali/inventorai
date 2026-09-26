"""Stage 22 / CAP-05 + CAP-07 Slice 1 — read-only decision trace and the
separated project-context panel.

Three semantic classes are enforced:
  A. DIRECTLY LINKED — facts proven by the decision chains themselves (the
     per-alternative trace, lifecycle, withdrawal reason, the unchanged
     comparison / readiness truth);
  B. PROJECT CONTEXT — canonical project facts with NO decision linkage, shown
     in one panel outside every decision and alternative, each count from its
     own canonical owner, failure never shown as zero;
  C. NOT ELIGIBLE — anything that would need inference; never rendered.

Synthetic data only. Nothing here writes, persists or calls a model.
"""
import copy
import html
import json
import re

import pytest

from engine.decision_composition import (
    compose_decision_records, decision_capture_view, decision_trace_view,
    declare_alternative, declare_decision_context, refine_alternative,
    rendered_alternative_set, withdraw_alternative,
)
from engine.idea_state import (
    IdeaState, DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED, MECHANISM_COMPLETENESS,
    PHYSICAL_FEASIBILITY,
)
from engine.requirement_landscape import derive_requirement_landscape
from tests.csrf_client import csrf_client
from web.ui_text import text

QUESTION = "Which latch mechanism should hold the ramp flat?"
A1, A2, A3 = "Toggle latch", "Toggle latch, stainless", "Toggle latch, stainless, 2 mm"
B1 = "Spring-loaded pin"
C1, C2 = "Magnetic catch", "Magnetic catch with keeper"
REASON = "not robust enough under repeated load"


def _decision_state():
    """ctx; A declared + refined twice (active); B declared then withdrawn with
    a reason; C declared, refined, then withdrawn with NO reason."""
    s = IdeaState(idea_id="stage22")
    ctx = declare_decision_context(s, QUESTION).record_id
    a = declare_alternative(s, A1, ctx)
    b = declare_alternative(s, B1, ctx)
    a = refine_alternative(s, A2, a.record_id)
    c = declare_alternative(s, C1, ctx)
    a = refine_alternative(s, A3, a.record_id)
    withdraw_alternative(s, b.record_id, REASON)
    c = refine_alternative(s, C2, c.record_id)
    withdraw_alternative(s, c.record_id, "")
    return s, ctx


def _roots(s):
    alts = [r for r in s.assertions
            if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED
            and not r.supersedes]
    return [r.record_id for r in alts]


# ---------------------------------------------------------------------------
# A. the trace projection (engine)
# ---------------------------------------------------------------------------

def test_g_every_wording_appears_exactly_and_in_order():
    s, ctx = _decision_state()
    ra, rb, rc = _roots(s)
    trace = decision_trace_view(s)[ctx]
    assert list(trace) == [ra, rb, rc]
    assert [(e["kind"], e["content"]) for e in trace[ra]["events"]] == [
        ("declared", A1), ("refined", A2), ("refined", A3)]
    assert [(e["kind"], e["content"]) for e in trace[rc]["events"]] == [
        ("declared", C1), ("refined", C2), ("withdrawn", "")]
    # events carry their own ledger record ids, strictly in ledger order
    ids = [e["record_id"] for e in trace[ra]["events"]]
    assert ids == sorted(ids, key=lambda r: int(r[4:]))


def test_f_h_i_withdrawn_stays_visible_reason_verbatim_or_none():
    s, ctx = _decision_state()
    ra, rb, rc = _roots(s)
    trace = decision_trace_view(s)[ctx]
    assert trace[ra]["lifecycle_state"] == "active"
    assert trace[rb]["lifecycle_state"] == "withdrawn"
    assert trace[rc]["lifecycle_state"] == "withdrawn"
    assert trace[rb]["events"][-1] == {
        "kind": "withdrawn", "record_id": trace[rb]["events"][-1]["record_id"],
        "content": REASON, "iteration": 0}
    assert trace[rc]["events"][-1]["content"] == ""   # never invented


def test_trace_is_pure_deterministic_and_persists_nothing():
    s, _ = _decision_state()
    before = copy.deepcopy(s.assertions)
    first = decision_trace_view(s)
    assert decision_trace_view(s) == first
    assert decision_trace_view(copy.deepcopy(s)) == first
    assert s.assertions == before
    json.dumps(first)   # plain data, no live objects


def test_j_k_membership_comparison_and_readiness_match_existing_composition():
    s, ctx = _decision_state()
    trace = decision_trace_view(s)[ctx]
    rendered = rendered_alternative_set(s)[ctx]
    assert [e["root"] for e in rendered] == list(trace)
    assert {e["root"]: e["lifecycle_state"] for e in rendered} == {
        root: t["lifecycle_state"] for root, t in trace.items()}
    [view] = decision_capture_view(s)
    [record] = compose_decision_records(s)
    eligible = {c.candidate_id.rsplit("-", 1)[-1] for c in record.candidates}
    assert {a["root"] for a in view["alternatives"]
            if a["comparison_eligible"]} == eligible
    assert view["readiness_status"] == record.readiness_status
    assert view["blocking_reason_codes"] == [b.code for b in record.blocking_reasons]


def test_a_trace_reads_only_decision_chains():
    s, ctx = _decision_state()
    only = decision_trace_view(s)
    s.record_interaction("answered", "steel frame", gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("answered", "folds flat", gap_context=MECHANISM_COMPLETENESS)
    s.record_interaction("provisional_assumption", "pin carries the load",
                         gap_context=PHYSICAL_FEASIBILITY)
    s.record_contradiction_declaration(s.assertions[-3].record_id,
                                       s.assertions[-2].record_id)
    s.record_assumption_dependency_declarations(
        s.assertions[-2].record_id, [s.assertions[-4].record_id])
    assert decision_trace_view(s) == only
    assert set(only) == {ctx}


def test_no_context_question_history_is_exposed():
    s, ctx = _decision_state()
    s.record_interaction(DISPOSITION_DECISION_CONTEXT_DECLARED,
                         "Which latch should hold it flat and locked?",
                         supersedes=[ctx])
    [view] = decision_capture_view(s)
    assert view["question"] == "Which latch should hold it flat and locked?"
    trace = decision_trace_view(s)
    assert all(set(t) == {"root", "lifecycle_state", "events"}
               for alts in trace.values() for t in alts.values())
    assert QUESTION not in json.dumps(trace)


# ---------------------------------------------------------------------------
# B. project context (web presentation boundary)
# ---------------------------------------------------------------------------

def _ctx_rows(state):
    import web.app as webapp
    return {r["key"]: r for r in webapp._decision_project_context(state)}


def _project_state():
    s, ctx = _decision_state()
    s.domain = "mechanical"
    a = s.record_interaction("answered", "steel frame", gap_context=PHYSICAL_FEASIBILITY)
    b = s.record_interaction("answered", "folds flat", gap_context=MECHANISM_COMPLETENESS)
    p = s.record_interaction("provisional_assumption", "pin carries the load",
                             gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("unknown", "", gap_context=MECHANISM_COMPLETENESS)
    s.record_interaction("deferred", "", gap_context=MECHANISM_COMPLETENESS)
    s.record_interaction("evidence_requested", "", gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("specialist_requested", "", gap_context=PHYSICAL_FEASIBILITY)
    s.record_contradiction_declaration(a.record_id, b.record_id)
    s.record_assumption_dependency_declarations(p.record_id, [a.record_id])
    return s, a, b, p


def test_counts_come_from_each_canonical_owner_once():
    s, *_ = _project_state()
    rows = _ctx_rows(s)
    assert [r for r in rows] == [
        "declared_contradictions", "assumption_dependencies",
        "provisional_assumptions", "recorded_unknowns", "deferred_items",
        "pending_evidence", "pending_specialist", "open_gaps", "next_step"]
    counts = {k: (r["status"], r["count"]) for k, r in rows.items()}
    assert counts["declared_contradictions"] == ("items", 1)
    assert counts["assumption_dependencies"] == ("items", 1)
    assert counts["provisional_assumptions"] == ("items", 1)
    assert counts["recorded_unknowns"] == ("items", 1)
    assert counts["deferred_items"] == ("items", 1)
    # the requested records are counted ONLY through the landscape owner
    landscape = derive_requirement_landscape(s)
    kinds = [r.primary_anchor.anchor_kind for r in landscape.requirements]
    assert counts["pending_evidence"] == ("items", kinds.count("pending_evidence"))
    assert counts["pending_specialist"] == ("items", kinds.count("pending_specialist"))
    assert rows["open_gaps"]["count"] == len(s.get_open_gaps())


def test_legacy_system_contradiction_is_not_counted_as_declared():
    s, ctx = _decision_state()
    s.domain = "mechanical"
    a = s.record_interaction("answered", "x", gap_context=PHYSICAL_FEASIBILITY)
    b = s.record_interaction("answered", "y", gap_context=PHYSICAL_FEASIBILITY)
    s.mark_contradiction(a.record_id, b.record_id)
    assert _ctx_rows(s)["declared_contradictions"]["status"] == "empty"


def test_d_historical_declarations_never_read_as_never_recorded():
    s, a, b, p = _project_state()
    s.record_interaction("answered", "aluminium frame",
                         gap_context=PHYSICAL_FEASIBILITY, supersedes=[a.record_id])
    rows = _ctx_rows(s)
    assert rows["assumption_dependencies"]["status"] == "historical"
    assert rows["declared_contradictions"]["status"] == "historical"
    fresh = IdeaState(idea_id="fresh")
    fresh.domain = "mechanical"
    declare_decision_context(fresh, QUESTION)
    never = _ctx_rows(fresh)
    assert never["assumption_dependencies"]["status"] == "empty"
    assert never["declared_contradictions"]["status"] == "empty"


def test_e_projection_failure_is_unavailable_never_zero(monkeypatch):
    import web.app as webapp
    s, *_ = _project_state()

    def boom(*_a, **_k):
        raise RuntimeError("projection failed")
    monkeypatch.setattr(webapp, "_project_assumption_dependencies", boom)
    monkeypatch.setattr(webapp, "derive_requirement_landscape", boom)
    rows = _ctx_rows(s)
    for key in ("assumption_dependencies", "pending_evidence", "pending_specialist"):
        assert rows[key]["status"] == "unavailable"
        assert rows[key]["count"] is None
    assert rows["declared_contradictions"]["status"] == "items"


def test_no_decision_derives_no_panel():
    s = IdeaState(idea_id="nodecision")
    s.domain = "mechanical"
    s.record_interaction("provisional_assumption", "p", gap_context=PHYSICAL_FEASIBILITY)
    import web.app as webapp
    assert webapp._decision_project_context(s) == []


def test_landscape_is_derived_once_per_panel(monkeypatch):
    import web.app as webapp
    s, *_ = _project_state()
    calls = []
    real = webapp.derive_requirement_landscape
    monkeypatch.setattr(webapp, "derive_requirement_landscape",
                        lambda st: calls.append(1) or real(st))
    webapp._decision_project_context(s)
    assert len(calls) == 1


def test_cold_state_marks_live_only_categories_unavailable():
    s, *_ = _project_state()
    s.domain = None
    rows = _ctx_rows(s)
    for key in ("pending_evidence", "pending_specialist", "open_gaps", "next_step"):
        assert (rows[key]["status"], rows[key]["count"]) == ("unavailable", None)
    assert rows["provisional_assumptions"]["status"] == "items"


def test_p_decision_actions_still_create_no_landscape_row():
    s, _ = _decision_state()
    decision_ids = {r.record_id for r in s.assertions}
    for req in derive_requirement_landscape(s).requirements:
        assert req.primary_anchor.anchor_reference not in decision_ids


def test_m_every_new_key_has_distinct_en_and_ar():
    from web.ui_text import UI_STRINGS
    keys = [k for k in UI_STRINGS if k.startswith("UI_DT_")]
    assert len(keys) >= 20
    for k in keys:
        en, ar = text(k, "en"), text(k, "ar")
        assert en.strip() and ar.strip() and en != ar, k
        assert re.search(r"[؀-ۿ]", ar), k


# ---------------------------------------------------------------------------
# rendered surfaces (session / report / PDF)
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "s22.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod


SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")


def _token(c, sid):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    return html.unescape(re.search(r'name="answer_token" value="([^"]+)"', page).group(1))


def _journey(c, appmod, lang="en"):
    with c.session_transaction() as session:
        session["ui_lang"] = lang
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    c.post(f"/session/{sid}/decision/declare-context",
           data={"content": QUESTION, "answer_token": _token(c, sid)})
    state = appmod.SESSION_STORE[sid]["state"]
    ctx = [r for r in state.assertions
           if r.disposition == DISPOSITION_DECISION_CONTEXT_DECLARED][0].record_id
    for alt in (A1, B1):
        c.post(f"/session/{sid}/decision/declare-alternative", data={
            "content": alt, "context_root": ctx, "answer_token": _token(c, sid)})
    heads = {r.content: r.record_id for r in state.assertions
             if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED}
    c.post(f"/session/{sid}/decision/refine-alternative", data={
        "content": A2, "supersedes_record_id": heads[A1],
        "answer_token": _token(c, sid)})
    c.post(f"/session/{sid}/decision/withdraw-alternative", data={
        "supersedes_record_id": heads[B1], "reason": REASON,
        "answer_token": _token(c, sid)})
    return sid


def _element(page, element_id):
    """(start, end, inner html) of the element with ``element_id``, balancing
    nested tags of the same name."""
    m = re.search(r'<(\w+)[^>]*\bid="%s"' % re.escape(element_id), page)
    assert m, element_id
    tag, pos, depth = m.group(1), m.end(), 1
    opener, closer = re.compile(r"<%s\b" % tag), "</%s>" % tag
    while depth:
        nxt_close = page.index(closer, pos)
        nxt_open = opener.search(page, pos, nxt_close)
        if nxt_open:
            depth, pos = depth + 1, nxt_open.end()
        else:
            depth, pos = depth - 1, nxt_close + len(closer)
    return m.start(), pos, page[m.start():pos]


def _spans(page, pattern, tag):
    out = []
    for m in re.finditer(pattern, page):
        depth, pos = 1, m.end()
        while depth:
            close = page.index("</%s>" % tag, pos)
            nested = re.compile(r"<%s\b" % tag).search(page, pos, close)
            if nested:
                depth, pos = depth + 1, nested.end()
            else:
                depth, pos = depth - 1, close + len(tag) + 3
        out.append((m.start(), pos))
    return out


def _panel_outside_decisions(page, panel_id):
    start, end, _ = _element(page, panel_id)
    for s0, e0 in (_spans(page, r'<div class="w2a-context"', "div")
                   + _spans(page, r'<li class="g3-alternative', "li")):
        assert not (s0 <= start < e0), "project context rendered inside a decision"


FORBIDDEN_EN = ("supports this", "weakens", "evidence for", "evidence against",
                "confidence", "recommended", "best option", "right decision",
                "strong evidence", "weak evidence", "evidence score",
                "evidence quality", "affects this alternative", "validated",
                "is resolved")
FORBIDDEN_AR = ("الأفضل", "موصى", "درجة الثقة", "يدعم هذا", "دليل قوي", "دليل ضعيف")


def _visible(fragment):
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment)).lower()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_session_trace_panel_links_and_vocabulary(client, lang):
    c, appmod = client
    sid = _journey(c, appmod, lang)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    _, _, section = _element(page, "w2b-decision-capture")
    for wording in (A1, A2, B1, REASON):
        assert html.escape(wording) in section
    assert section.count('class="dt-history"') == 2
    assert 'class="dt-event dt-withdrawn"' in section
    assert text("UI_DT_CTX_HEADING", lang) in section
    _panel_outside_decisions(page, "decision-project-context")
    _, _, panel = _element(page, "decision-project-context")
    assert "<form" not in panel
    for href in re.findall(r'href="([^"]*)"', panel):
        assert href.startswith("#") and f'id="{href[1:]}"' in page, href
    words = _visible(section)
    for phrase in FORBIDDEN_EN + FORBIDDEN_AR:
        assert phrase.lower() not in words, phrase


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_l_report_and_pdf_link_only_report_local_sections(client, monkeypatch, lang):
    c, appmod = client
    sid = _journey(c, appmod, lang)
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    [(s0, e0)] = _spans(report, r'<section class="w2a-decisions"', "section")
    section = report[s0:e0]
    assert html.escape(A2) in section and html.escape(REASON) in section
    assert "<form" not in section and "<details" not in section
    _panel_outside_decisions(report, "report-decision-project-context")
    _, _, panel = _element(report, "report-decision-project-context")
    hrefs = re.findall(r'href="([^"]*)"', panel)
    assert hrefs, "expected at least one report-local link"
    for href in hrefs:
        assert href in ("#report-needs", "#report-next-steps"), href
        assert f'id="{href[1:]}"' in report
    words = _visible(section)
    for phrase in FORBIDDEN_EN + FORBIDDEN_AR:
        assert phrase.lower() not in words, phrase

    seen = {}
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: seen.setdefault("source", source) and b"%PDF-")
    c.post(f"/session/{sid}/deliverable.pdf", data={})
    source = seen["source"]
    assert text("UI_DT_CTX_HEADING", lang) in source
    assert html.escape(A2) in source
    for href in re.findall(r'href="([^"]*)"', source):
        assert href.startswith("#") and f'id="{href[1:]}"' in source, href


def test_e_trace_and_panel_failures_render_unavailable_not_empty(client, monkeypatch):
    c, appmod = client
    sid = _journey(c, appmod)
    import engine.decision_composition as dc

    def boom(*_a, **_k):
        raise RuntimeError("derivation failed")
    monkeypatch.setattr(dc, "decision_trace_view", boom)
    # fail ONLY the panel's CAP-08 owner call (the CAP-08 view itself stays up)
    monkeypatch.setattr(appmod, "_DT_CATEGORIES", tuple(
        (key, boom if key == "assumption_dependencies" else owner, live)
        for key, owner, live in appmod._DT_CATEGORIES))
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    _, _, section = _element(page, "w2b-decision-capture")
    assert section.count(text("UI_DT_TRACE_UNAVAILABLE", "en")) == 2
    row = re.search(r'<li class="dt-ctx-row" data-dt-category="assumption_dependencies"'
                    r' data-dt-status="(\w+)">(.*?)</li>', section)
    assert row.group(1) == "unavailable"
    assert text("UI_DT_STATE_UNAVAILABLE", "en") in row.group(2)
    assert text("UI_DT_STATE_EMPTY", "en") not in row.group(2)


def test_n_cold_read_only_view_renders_trace_without_forms(client):
    c, appmod = client
    sid = _journey(c, appmod)
    appmod.SESSION_STORE.pop(sid)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    _, _, section = _element(page, "w2b-decision-capture")
    assert "<form" not in section
    assert html.escape(A2) in section and html.escape(REASON) in section
    assert 'data-dt-category="open_gaps" data-dt-status="unavailable"' in section


def test_o_canonical_package_carries_no_trace_or_context(client):
    c, appmod = client
    sid = _journey(c, appmod)
    _entry, package, *_ = appmod._deliverable_context(sid)
    dumped = json.dumps(package, default=str)
    for marker in ("decision_trace", "project_context", "dt-", A2):
        assert marker not in dumped, marker
