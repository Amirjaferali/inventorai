"""BOARD-ENCLOSURE-CONDITIONAL-REGION-BOUND-01 — the derived minimum usable-region dimension.

Synthetic data only. Method contract §3A: for a MET or NOT MET evaluation of the EXISTING board-enclosure
planar clearance declaration, and only then, each axis shows the exact minimum usable-region dimension
``board + 2c`` that meets the declared condition with the declared board, clearance, centered placement and
applicability held fixed, and the additional region dimension ``max(0, minimum - region)``. What is pinned:
  * the arithmetic against an INDEPENDENT oracle: the minimum from the original margin relation
    (``region - 2 x margin``) and the additional dimension as twice the per-side shortfall, never the
    implementation checked against itself; equality, c = 0, one / both axes failing, a board larger than the
    region, satisfied axes, the representation extremes and a bound beyond the entry grammar (shown exactly,
    flagged, never truncated); the 99.9 / 0.1 decimal boundary decided exactly;
  * no bound for MISSING INFORMATION, INAPPLICABLE, COULD NOT BE COMPUTED, NEEDS RECONFIRMATION (component,
    participation, method version), a withdrawn declaration or an unreadable history;
  * the governed consequence: its own artifact section and version, every version-1 section, the method
    version and the declaration-contract version unchanged (so no stored declaration is relabelled or asked
    to be reconfirmed), the English meaning lines equal to the artifact word for word;
  * the shared output: page, report and PDF agree in English and Arabic; the outcome, margins, sketch and
    revision identity are unchanged by the bound; an earlier report keeps its own snapshot; nothing stored.
"""
import html as _html
import re
from fractions import Fraction

import pytest

import web.app as appmod
from engine import deterministic_calculation as dc
from engine import mechanical_planar_clearance as pcc
from engine import mechanical_planar_clearance_method as method
from tests.test_board_enclosure_planar_clearance import (  # noqa: F401  (fixtures)
    APPLIES, BINDING, _correct_decl, _declare, _ev, _outcome, _page, _revisions, _digests,
    _rows, _save, _setup, _web, client, store)
from tests.test_component_inventory_correct_withdraw import _correct
from tests.test_stage15_integrated_invention_entry import _pdf_source
from web import planar_clearance as view_mod
from web import ui_text


def _bound(result):
    return [(a["axis"], a["region_min_text"], a["additional_text"], a["increase_needed"],
             a["region_min_enterable"]) for a in result["axes"]]


def _oracle(values):
    """Independent of the bound code: the minimum region from the ORIGINAL margin relation
    (margin = (R - B)/2 - c, so the region with zero margin is R - 2 x margin) and the additional
    dimension as twice the per-side shortfall."""
    board_x, board_y, region_x, region_y, c = (Fraction(v) for v in values)
    out = []
    for axis, board, region in (("x", board_x, region_x), ("y", board_y, region_y)):
        margin = (region - board) / 2 - c
        shortfall = -margin if margin < 0 else Fraction(0)
        out.append((axis, region - 2 * margin, 2 * shortfall))
    return out


# ==========================================================================
# 1. arithmetic against the independent oracle
# ==========================================================================
def test_b01_the_declared_example_and_its_correction():
    r = _ev(("84", "50", "86", "56", "2"))
    assert r["outcome"] == pcc.OUTCOME_NOT_MET
    assert [a["margin_text"] for a in r["axes"]] == ["-1", "1"]
    # a per-side shortfall of 1 mm is a TOTAL region increase of 2 mm, not 1 mm
    assert _bound(r) == [("x", "88", "2", True, True), ("y", "54", "0", False, True)]
    assert r["axes"][0]["shortfall_text"] == "1" and r["axes"][0]["region_text"] == "86"
    assert r["axes"][1]["region_text"] == "56"          # 56 stays; 54 is never a target
    assert r["region_bound"] == {"consequence_id": pcc.REGION_BOUND_ID,
                                 "consequence_version": pcc.REGION_BOUND_VERSION}
    r = _ev(("84", "50", "88", "56", "2"))               # the inventor's own correction
    assert r["outcome"] == pcc.OUTCOME_MET
    assert [a["margin_text"] for a in r["axes"]] == ["0", "1"]
    assert _bound(r) == [("x", "88", "0", False, True), ("y", "54", "0", False, True)]


@pytest.mark.parametrize("values", [
    ("84", "50", "86", "56", "2"),
    ("10", "10", "12", "12", "1"),                  # exact equality on both axes
    ("10", "10", "10", "10", "0"),                  # c = 0, touching
    ("10", "10", "9", "20", "0"),                   # board larger than the region on X
    ("30", "30", "20", "20", "1"),                  # both axes fail
    ("10", "10", "14", "14", "1"),                  # both axes already met
    ("10", "10", "11.9998", "12", "1"),             # one-ten-thousandth short
    ("0.0001", "0.0001", "0.0001", "0.0001", "0"),  # smallest admitted values
    ("999999.9999", "999999.9999", "999999.9999", "999999.9999", "0"),   # largest, equality
    ("999999.9997", "1", "999999.9999", "1", "0.0001"),  # minimum exactly at the entry limit
])
def test_b02_matrix_agrees_with_the_independent_oracle(values):
    r = _ev(values)
    assert r["outcome"] in (pcc.OUTCOME_MET, pcc.OUTCOME_NOT_MET)
    for item, (axis, minimum, additional) in zip(r["axes"], _oracle(values)):
        assert item["axis"] == axis
        assert item["region_min"] == minimum and item["additional"] == additional
        assert item["region_min_text"] == pcc.format_exact(minimum)
        assert item["increase_needed"] == (additional > 0) == (not item["met"])
        assert item["region_min_enterable"] is True
    # the outcome is the original decision, untouched by the bound
    assert r["outcome"] == ("MET" if all(a["met"] for a in r["axes"]) else "NOT_MET")


def test_b03_a_bound_beyond_the_entry_range_is_exact_and_flagged():
    r = _ev(("999999.9999", "1", "999999.9999", "3", "999999.9999"))
    assert r["outcome"] == pcc.OUTCOME_NOT_MET
    x, y = r["axes"]
    assert x["region_min_text"] == "2999999.9997" and x["additional_text"] == "1999999.9998"
    assert x["region_min_enterable"] is False and pcc.parse_value(x["region_min_text"]) is None
    assert y["region_min_text"] == "2000000.9998" and y["region_min_enterable"] is False
    # just past the limit by one ten-thousandth
    r = _ev(("999999.9999", "1", "999999.9999", "1", "0.0001"))
    assert r["axes"][0]["region_min_text"] == "1000000.0001"
    assert r["axes"][0]["region_min_enterable"] is False
    assert [a["margin_text"] for a in r["axes"]] == ["-0.0001", "-0.0001"]   # outcome kept


def test_b04_the_decimal_boundary_is_exact():
    below = _ev(("99.9", "50", "100.0999", "56", "0.1"))
    at = _ev(("99.9", "50", "100.1", "56", "0.1"))
    assert below["outcome"] == "NOT_MET" and at["outcome"] == "MET"
    assert below["axes"][0]["region_min"] == Fraction("100.1") == at["axes"][0]["region_min"]
    assert below["axes"][0]["region_min_text"] == "100.1" == at["axes"][0]["region_min_text"]
    assert below["axes"][0]["additional_text"] == "0.0001"
    assert at["axes"][0]["additional_text"] == "0" and at["axes"][0]["margin_text"] == "0"
    # the binary path cancels to a tiny negative; neither the decision nor the bound uses it
    assert float(Fraction("100.1")) - float(Fraction("99.9")) - 2 * 0.1 < 0


def test_b05_the_cross_check_against_the_margin_fails_closed(monkeypatch):
    values = {r: Fraction(t) for r, t in zip(pcc.VALUE_ROLES, ("84", "50", "86", "56", "2"))}
    exact = pcc.exact_margins(values)
    assert pcc.region_bound(values, exact)["x"] == {"minimum": 88, "additional": 2}
    with pytest.raises(ArithmeticError):
        pcc.region_bound(values, dict(exact, margin_x=exact["margin_x"] + Fraction(1, 10 ** 4)))

    def broken(values, exact):
        raise ArithmeticError("forced")
    monkeypatch.setattr(pcc, "region_bound", broken)
    r = _ev(("84", "50", "86", "56", "2"))
    assert (r["outcome"], r["owner_reason"], r["axes"], r["region_bound"]) == (
        "COULD_NOT_BE_COMPUTED", dc.EXECUTION_INTEGRITY_FAILURE, None, None)


# ==========================================================================
# 2. no bound outside MET / NOT MET
# ==========================================================================
def test_b06_no_bound_for_missing_inapplicable_or_failed_execution():
    r = _ev(("84", "50", "86", "unknown", "2"))
    assert r["outcome"] == "MISSING_INFORMATION" and r["axes"] is None and r["region_bound"] is None
    r = _ev(("84", "50", "86", "56", None))
    assert r["outcome"] == "MISSING_INFORMATION" and r["region_bound"] is None
    answers = list(APPLIES)
    answers[3] = pcc.ANSWER_DOES_NOT_APPLY
    r = _ev(("84", "50", "86", "56", "2"), tuple(answers))
    assert r["outcome"] == "INAPPLICABLE" and r["region_bound"] is None
    answers[3] = None
    r = _ev(("84", "50", "86", "56", "2"), tuple(answers))
    assert r["outcome"] == "MISSING_INFORMATION" and r["region_bound"] is None
    wrong = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    r = pcc.evaluate({"values": dict(zip(pcc.VALUE_ROLES, ("84", "50", "86", "56", "2"))),
                      "region_description": "x",
                      "applicability": dict(zip(pcc.DECLARATION_IDS, APPLIES))}, wrong)
    assert r["outcome"] == "COULD_NOT_BE_COMPUTED" and r["region_bound"] is None

    def liar(board_x, board_y, region_x, region_y, c):
        return {"margin_x": 5.0, "margin_y": 5.0}
    liar.__module__, liar.__qualname__ = method.evaluate.__module__, method.evaluate.__qualname__
    r = pcc.evaluate({"values": dict(zip(pcc.VALUE_ROLES, ("84", "50", "86", "56", "2"))),
                      "region_description": "x",
                      "applicability": dict(zip(pcc.DECLARATION_IDS, APPLIES))},
                     dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, liar))
    assert r["outcome"] == "COULD_NOT_BE_COMPUTED" and r["region_bound"] is None


def test_b07_no_bound_when_the_binding_is_stale_or_withdrawn(store):
    pid, subs, ifc, b, e, x = _setup(store)
    _declare(store, pid, ifc, b, e)
    view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
    assert view["state"] == view_mod.STATE_CURRENT and view["evaluation"]["region_bound"]
    _correct(store, pid, b, 0, "Board v2", "Holds the parts")          # component changed
    view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
    assert view["state"] == view_mod.STATE_RECONFIRM and view["evaluation"] is None
    _correct_decl(store, pid, ifc, b, e, "k-rebind", ("84", "50", "86", "56", "2"))
    store.set_interface_participation(pid, ifc, [b, x], [b, e, x])     # participation lost
    view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
    assert view["state"] == view_mod.STATE_RECONFIRM and view["evaluation"] is None


def test_b08_a_method_version_mismatch_is_not_bypassed(store):
    pid, subs, ifc, b, e, _x = _setup(store)
    _declare(store, pid, ifc, b, e)
    store._conn.execute("UPDATE planar_clearance_revisions SET method_version = '0.9'")
    view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
    assert view["state"] == view_mod.STATE_RECONFIRM and view["evaluation"] is None


def test_b09_web_states_without_a_comparison_show_no_bound(client, monkeypatch):
    sid, ifc, ids = _web(client)
    body = _save(client, sid, ifc, ids, values=("84", "50", "86", "56", ""),
                 unknown=("c",)).get_data(as_text=True)
    assert _outcome(body) == ["MISSING_INFORMATION"] and "data-pcc-region-bound" not in body
    answers = list(APPLIES)
    answers[0] = pcc.ANSWER_DOES_NOT_APPLY
    body = _save(client, sid, ifc, ids, answers=answers).get_data(as_text=True)
    assert _outcome(body) == ["INAPPLICABLE"] and "data-pcc-region-bound" not in body
    # withdrawn: history only, no bound anywhere
    from tests.test_board_enclosure_planar_clearance import _fields
    page = _page(client, sid, ifc).get_data(as_text=True)
    data = _fields(page, form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    page = _page(client, sid, ifc).get_data(as_text=True)
    assert "data-pcc-withdrawn-only" in page and "data-pcc-region-bound" not in page
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert "data-pcc-region-bound" not in report

    def unreadable(self, project_id):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(type(appmod._get_store()), "load_planar_clearance", unreadable)
    page = _page(client, sid, ifc).get_data(as_text=True)
    assert "data-pcc-unavailable" in page and "data-pcc-region-bound" not in page


# ==========================================================================
# 3. the governed consequence and version compatibility
# ==========================================================================
def test_b10_the_consequence_is_governed_and_versioned_without_relabelling():
    artifact = pcc.load_artifact()
    assert artifact["artifact_version"] == "2"
    bound = artifact["region_bound"]
    assert (bound["consequence_id"], bound["consequence_version"]) == (
        "mechanical:planar_centered_rectangular_clearance/region_bound", "1")
    # the method and declaration-contract versions a stored declaration names are unchanged
    assert (pcc.METHOD_ID, pcc.METHOD_VERSION, pcc.DECLARATION_VERSION) == (
        "mechanical:planar_centered_rectangular_clearance", "1.0", "planar-clearance-declaration/1")
    assert method.METHOD_VERSION == "1.0" and (method.METHOD_ID, "1.0") in dc.ADMITTED_METHODS
    # every version-1 section keeps its accepted digest
    for section in ("method", "numeric_domain", "declarations", "limitations", "disclosure",
                    "sources"):
        assert pcc._section_digest(artifact[section]) == pcc._SEMANTIC_DIGESTS[section]
    for edit in (lambda a: a["region_bound"]["statements"].pop(),
                 lambda a: a["region_bound"].__setitem__("consequence_version", "2"),
                 lambda a: a["region_bound"]["statements"].__setitem__(4, "It is verified."),
                 lambda a: a.pop("region_bound"),
                 lambda a: a.__setitem__("artifact_version", "1")):
        changed = pcc.load_artifact()
        edit(changed)
        with pytest.raises(pcc.PlanarClearanceKnowledgeError):
            pcc.validate_artifact(changed)


def test_b11_english_meaning_lines_are_the_artifact_word_for_word():
    statements = pcc.load_artifact()["region_bound"]["statements"]
    assert [ui_text.text("UI_PCC_BOUND_MEANING_%d" % n, "en")
            for n in range(1, len(statements) + 1)] == statements
    assert not ui_text.has_string("UI_PCC_BOUND_MEANING_%d" % (len(statements) + 1))
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_PCC_BOUND_")]:
        assert ui_text.text(key, "ar") != ui_text.text(key, "en")
    # a satisfied axis is never offered as a size to shrink to
    assert "not a suggestion to make the region smaller" in ui_text.text("UI_PCC_BOUND_NO_INCREASE", "en")


def test_b12_a_declaration_saved_before_the_consequence_is_current_not_reconfirmed(store):
    pid, subs, ifc, b, e, _x = _setup(store)
    _declare(store, pid, ifc, b, e)
    row = store._conn.execute(
        "SELECT method_id, method_version, declaration_version FROM planar_clearance_revisions"
    ).fetchone()
    assert tuple(row) == (pcc.METHOD_ID, "1.0", "planar-clearance-declaration/1")
    view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
    assert view["state"] == view_mod.STATE_CURRENT and view["issues"] == []
    cols = [r[1] for r in store._conn.execute("PRAGMA table_info(planar_clearance_revisions)")]
    assert not any(word in col for col in cols for word in ("bound", "region_min", "additional"))


# ==========================================================================
# 4. page, report and PDF in English and Arabic
# ==========================================================================
def _bound_cells(body):
    return {"min": re.findall(r"data-pcc-bound-min>([^<]*)<", body),
            "add": re.findall(r"data-pcc-bound-additional>([^<]*)<", body),
            "cur": re.findall(r"data-pcc-bound-current>([^<]*)<", body),
            "note": re.findall(r'data-pcc-bound-note="(\w+)"', body)}


def _clean(text):
    return " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", text)).split())


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_b13_the_journey_page_report_and_pdf_agree(client, monkeypatch, lang):
    sid, ifc, ids = _web(client)
    first = _page(client, sid, ifc, lang=lang).get_data(as_text=True)
    assert "data-pcc-region-bound" not in first                       # nothing before a declaration
    body = _save(client, sid, ifc, ids).get_data(as_text=True)
    expected = {"min": ["88 mm", "54 mm"], "add": ["2 mm", "0 mm"], "cur": ["86 mm", "56 mm"],
                "note": ["increase", "none"]}
    assert _outcome(body) == ["NOT_MET"] and _bound_cells(body) == expected
    assert re.findall(r"data-pcc-margin>([^<]*)<", body) == ["-1 mm", "1 mm"]
    text = _clean(body)
    assert ui_text.text("UI_PCC_BOUND_HEADING", lang) in text
    assert ui_text.text("UI_PCC_BOUND_NO_INCREASE", lang) in text
    assert ui_text.text("UI_PCC_BOUND_INCREASE", lang) in text
    for n in range(1, 7):
        assert ui_text.text("UI_PCC_BOUND_MEANING_%d" % n, lang) in text
    assert "%s 1" % pcc.REGION_BOUND_ID in text
    assert "data-pcc-bound-beyond-range" not in body
    # every bound number is LTR-isolated
    for attr in ("data-pcc-bound-min", "data-pcc-bound-additional", "data-pcc-bound-current"):
        assert len(re.findall(r'<bdi dir="ltr"[^>]*%s>' % attr, body)) == 2
    # the bound sits beside the result: outcome, sketch and identity are unchanged
    assert "data-pcc-diagram" in body and "data-pcc-dg-overlap" in body
    old_digest, old_rev = _digests(body)[0], _revisions(body)
    report_old = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    pdf_old = _pdf_source(client, sid, monkeypatch)
    for doc in (report_old, pdf_old):
        assert _outcome(doc) == ["NOT_MET"] and _bound_cells(doc) == expected
        assert _digests(doc) == [old_digest]
    # the inventor explicitly corrects region X to 88: a new revision, MET, margins 0 / 1
    body = _save(client, sid, ifc, ids, values=("84", "50", "88", "56", "2")).get_data(as_text=True)
    assert _outcome(body) == ["MET"]
    assert re.findall(r"data-pcc-margin>([^<]*)<", body) == ["0 mm", "1 mm"]
    assert _bound_cells(body) == {"min": ["88 mm", "54 mm"], "add": ["0 mm", "0 mm"],
                                  "cur": ["88 mm", "56 mm"], "note": ["none", "none"]}
    assert _revisions(body) == ["1"] and old_rev == ["0"] and _digests(body)[0] != old_digest
    report_new = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert _outcome(report_new) == ["MET"] and _revisions(report_new) == ["1"]
    # the earlier render keeps its own snapshot, outcome and bound
    assert _outcome(report_old) == ["NOT_MET"] and _revisions(report_old) == ["0"]
    assert old_digest in report_old and _bound_cells(report_old) == expected


def test_b14_the_report_bound_follows_the_document_language(client, monkeypatch):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    monkeypatch.setattr(appmod, "_deliverable_document_lang", lambda: "ar")
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    section = re.search(r"<section class=\"group\" data-pcc-report.*?</section>", report, re.S).group(0)
    assert ui_text.text("UI_PCC_BOUND_HEADING", "ar") in _clean(section)
    assert ui_text.text("UI_PCC_BOUND_HEADING", "en") not in _clean(section)
    assert _bound_cells(section)["min"] == ["88 mm", "54 mm"]


def test_b15_a_bound_beyond_the_entry_range_renders_its_limitation(client):
    sid, ifc, ids = _web(client)
    body = _save(client, sid, ifc, ids,
                 values=("999999.9999", "1", "999999.9999", "3", "999999.9999")).get_data(as_text=True)
    assert _outcome(body) == ["NOT_MET"]
    assert _bound_cells(body)["min"] == ["2999999.9997 mm", "2000000.9998 mm"]
    assert body.count("data-pcc-bound-beyond-range") == 2
    assert ui_text.text("UI_PCC_BOUND_BEYOND_RANGE", "en") in _clean(body)
