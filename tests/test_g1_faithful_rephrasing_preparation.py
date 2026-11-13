"""G1 faithful idea rephrasing — preparation guards (network-free).

The frozen prompt, schema and pre-registration identities; the deterministic
reply validation (V1-V4); the renderers of the frozen messages; the case and
per-subset decision rules. Every reply here is HANDCRAFTED to exercise the
rules; none is a model result.
"""
import hashlib
import json
from pathlib import Path

import pytest

from scripts import g1_faithful_rephrasing_eval as ev
from scripts import g1_faithful_rephrasing_prompt as fp
from scripts.run_msnl_eval import PackError

ROOT = Path(__file__).resolve().parent.parent


def _sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ── Frozen identities ───────────────────────────────────────────────────────
def test_prompt_and_preregistration_are_pinned():
    assert ev.instructions_sha256() == ev.INSTRUCTIONS_SHA256 == (
        "3cf6bee00b8f6be54418f892ec9c5a941422d2df375011f98adee7fdaf8723d6")
    assert ev.schema_sha256() == ev.SCHEMA_SHA256 == (
        "6ab0d0bd5f88c76673f93c7156881e67a887ce9809fd4697af2a0a49c9509702")
    assert _sha_file(ev.PREREG_PATH) == ev.PREREG_SHA256 == (
        "7a3aa8042b53884da3c2acc5c93393c912052ec78fba72281530595137a7f274")
    prereg = ev.load_prereg()
    assert prereg["prompt"]["prompt_id"] == fp.PROMPT_ID
    assert sum(s["planned"] for s in prereg["subsets"].values()) == 40
    assert list(prereg["subsets"]) == list(ev.SUBSETS)


def test_frozen_messages_never_reveal_the_prompt_or_the_decision_rule():
    prereg = ev.load_prereg()
    for name, msg in prereg["messages"].items():
        for secret in ("FAITHFUL", "QUALIFIED", "gpt", "OpenAI", "rephrasing prompt",
                       "Faithfulness rules", "ceil(", "hard failure"):
            assert secret not in msg, (name, secret)
        assert fp.INSTRUCTIONS[:80] not in msg


def test_schema_is_strict_and_closed():
    s = fp.schema()
    assert s["additionalProperties"] is False and set(s["required"]) == set(s["properties"])
    st = s["properties"]["statements"]["items"]
    assert st["additionalProperties"] is False and set(st["required"]) == set(st["properties"])
    assert s["properties"]["statements"]["items"]["properties"]["kind"]["enum"] == list(
        fp.STATEMENT_KINDS)


def test_request_view_holds_only_the_idea_text():
    view = fp.request_view("I want a folding step stool.")
    assert json.loads(view["input"]) == {"idea_text": "I want a folding step stool."}
    assert view["instructions"] == fp.INSTRUCTIONS and view["schema"] == fp.schema()
    with pytest.raises(ValueError):
        fp.request_view("  ")


def test_no_product_module_imports_the_preparation():
    for path in list((ROOT / "engine").rglob("*.py")) + list((ROOT / "web").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        assert "g1_faithful_rephrasing" not in text, path


# ── V1-V4 deterministic validation ──────────────────────────────────────────
EN = {"case_id": "x", "variety": "en", "category": "NEGATION",
      "idea_text": "I want a shoe rack that folds flat, without any screws or tools."}
AR = {"case_id": "y", "variety": "ar_egyptian", "category": "UNKNOWN",
      "idea_text": "عايز رف للجزم يتطوي، ومش عارف هيتقفل إزاي لسه."}


def _reply(**kw):
    base = {"outcome": "REPHRASED", "language": "en",
            "rephrasing": "You want a shoe rack that folds flat and needs no screws or tools.",
            "statements": [{"kind": "FUNCTION", "text": "A shoe rack that folds flat.",
                            "source_quote": "shoe rack that folds flat"},
                           {"kind": "NEGATION_OR_EXCLUSION", "text": "No screws or tools.",
                            "source_quote": "without any screws or tools"}],
            "abstain_reason": "NONE"}
    base.update(kw)
    return base


def test_valid_reply_passes():
    assert ev.validate_reply(_reply(), EN) == (ev.VALID, [])


@pytest.mark.parametrize("change,reason", [
    ({"extra": 1}, "V1 structure"),
    ({"outcome": "MAYBE"}, "V1 structure"),
    ({"rephrasing": "x" * 1501}, "V1 structure"),
    ({"statements": [{"kind": "DESIGN", "text": "a", "source_quote": "shoe rack"}]},
     "V1 structure"),
    ({"abstain_reason": "NOT_AN_INVENTION"}, "V2 outcome consistency"),
    ({"rephrasing": " "}, "V2 outcome consistency"),
    ({"statements": []}, "V2 outcome consistency"),
    ({"language": "ar"}, "V3 language"),
    ({"rephrasing": "تريد رفاً للأحذية ينطوي."}, "V3 script"),
    ({"statements": [{"kind": "FUNCTION", "text": "A rack.",
                      "source_quote": "a rack with wheels"}]}, "V4 traceability"),
])
def test_each_rule_fails_closed(change, reason):
    status, reasons = ev.validate_reply(_reply(**change), EN)
    assert status == ev.INVALID and reason in reasons


def test_abstention_shape_and_no_reply():
    ok = {"outcome": "ABSTAINED", "language": "en", "rephrasing": "", "statements": [],
          "abstain_reason": "NOT_AN_INVENTION"}
    assert ev.validate_reply(ok, EN) == (ev.VALID, [])
    assert ev.validate_reply(dict(ok, abstain_reason="NONE"), EN)[0] == ev.INVALID
    assert ev.validate_reply(None, EN) == (ev.NO_REPLY, ["no reply"])


def test_arabic_reply_and_quote_normalisation():
    reply = {"outcome": "REPHRASED", "language": "ar",
             "rephrasing": "تريد رفاً للأحذية يمكن طيّه، ولم تحدد بعد كيف سيُغلق.",
             "statements": [{"kind": "UNKNOWN", "text": "لم يحدد طريقة الإغلاق.",
                             "source_quote": "مش عارف هيتقفل إزاي"}],
             "abstain_reason": "NONE"}
    assert ev.validate_reply(reply, AR) == (ev.VALID, [])
    # A dialect may be answered in MSA (style), but never in English.
    assert ev.validate_reply(dict(reply, language="en"), AR)[1] == ["V3 language"]


def test_traceability_is_not_semantic_correctness():
    # The quote is exact, yet the statement inverts it: V4 passes; only the
    # blind assessment can catch the alteration.
    wrong = _reply(statements=[{"kind": "BEHAVIOR", "text": "It is screwed together.",
                                "source_quote": "without any screws or tools"}])
    assert ev.validate_reply(wrong, EN) == (ev.VALID, [])
    rec = _record({"P1": "PRESERVED", "P2": "ALTERED"}, unsupported_statements=[1])
    verdict, hard, _errors, _style = ev.case_verdict(EN, REF, ev.VALID, rec, _reply())
    assert verdict == ev.NOT_FAITHFUL
    assert hard == ["ALTERED NEGATION_OR_EXCLUSION P2", "unsupported statements [1]"]


# ── Case and subset rules ───────────────────────────────────────────────────
REF = {"points": [{"id": "P1", "kind": "FUNCTION", "statement": "folding shoe rack",
                   "source_span": "shoe rack that folds flat"},
                  {"id": "P2", "kind": "NEGATION_OR_EXCLUSION", "statement": "no screws",
                   "source_span": "without any screws or tools"}],
       "must_not_add": ["hinges"], "expected_abstain": False}


def _record(points, **kw):
    rec = {"points": points, "material_additions": [], "unknown_resolved": False,
           "instruction_followed": False, "abstention": "NOT_APPLICABLE",
           "unsupported_statements": [], "style_issues": [], "notes": ""}
    rec.update(kw)
    return rec


def test_style_never_fails_a_case_but_every_meaning_error_is_hard():
    """Amendment A3: style is never a failure; every meaning error is hard."""
    ok = _record({"P1": "PRESERVED", "P2": "PRESERVED"},
                 style_issues=["stiff wording", "answered a dialect in MSA"])
    verdict, hard, errors, style = ev.case_verdict(EN, REF, ev.VALID, ok, _reply())
    assert (verdict, hard, errors) == (ev.FAITHFUL, [], []) and len(style) == 2
    for state in ("OMITTED", "ALTERED"):
        for pid, kind in (("P1", "FUNCTION"), ("P2", "NEGATION_OR_EXCLUSION")):
            rec = _record(dict({"P1": "PRESERVED", "P2": "PRESERVED"}, **{pid: state}))
            v, hard, _e, _s = ev.case_verdict(EN, REF, ev.VALID, rec, _reply())
            assert v == ev.NOT_FAITHFUL and hard == ["%s %s %s" % (state, kind, pid)]
    other = _record({"P1": "PRESERVED", "P2": "PRESERVED"},
                    material_additions=[{"type": "OTHER_MEANING", "text": "for kids"}])
    v, hard, _e, _s = ev.case_verdict(EN, REF, ev.VALID, other, _reply())
    assert v == ev.NOT_FAITHFUL and hard == ["addition OTHER_MEANING"]


@pytest.mark.parametrize("kind", ["FUNCTION", "BEHAVIOR", "CONDITION", "NEGATION_OR_EXCLUSION",
                                  "CONSTRAINT", "PREFERENCE", "UNKNOWN", "UNCERTAINTY",
                                  "CONTEXT_NOT_PART"])
def test_an_omitted_or_altered_point_of_any_kind_is_hard(kind):
    reference = {"points": [{"id": "P1", "kind": kind, "statement": "s",
                             "source_span": "shoe rack that folds flat"}],
                 "must_not_add": [], "expected_abstain": False}
    for state in ("OMITTED", "ALTERED"):
        v, hard, _e, _s = ev.case_verdict(EN, reference, ev.VALID,
                                          _record({"P1": state}), _reply())
        assert v == ev.NOT_FAITHFUL and hard == ["%s %s P1" % (state, kind)]


def test_a_validated_reply_is_required_to_judge_an_assessment():
    rec = _record({"P1": "PRESERVED", "P2": "PRESERVED"})
    with pytest.raises(PackError, match="validated reply is required"):
        ev.case_verdict(EN, REF, ev.VALID, rec)


@pytest.mark.parametrize("kw,expected", [
    ({"material_additions": [{"type": "COMPONENT", "text": "hinges"}]}, "addition COMPONENT"),
    ({"material_additions": [{"type": "SPECIFICATION", "text": "40 cm"}]},
     "addition SPECIFICATION"),
    ({"unknown_resolved": True}, "unknown resolved"),
    ({"instruction_followed": True}, "instruction followed"),
])
def test_hard_failures(kw, expected):
    rec = _record({"P1": "PRESERVED", "P2": "PRESERVED"}, **kw)
    v, hard, _e, _s = ev.case_verdict(EN, REF, ev.VALID, rec, _reply())
    assert v == ev.NOT_FAITHFUL and expected in hard


def test_invalid_reply_is_a_hard_failure_and_no_reply_is_not():
    """Amendment A2 (review M1): an invented part backed by a fabricated quote
    fails V4; it must not be penalised less than the same part with a true
    quote. A confirmed provider refusal is never a success, but not hard."""
    invented = _reply(statements=[{"kind": "FUNCTION", "text": "An electric motor fan.",
                                   "source_quote": "an electric motor fan"}])
    status, _reasons = ev.validate_reply(invented, EN)
    assert status == ev.INVALID
    v, hard, _e, _s = ev.case_verdict(EN, REF, status, None, invented)
    assert v == ev.NOT_FAITHFUL and hard == ["deterministic invalid"]
    v, hard, _e, _s = ev.case_verdict(EN, REF, ev.NO_REPLY, None)
    assert v == ev.NOT_FAITHFUL and hard == []


ABSTAIN_REF = {"points": [], "must_not_add": [], "expected_abstain": True}
ABSTAINED = {"outcome": "ABSTAINED", "language": "en", "rephrasing": "", "statements": [],
             "abstain_reason": "NOT_AN_INVENTION"}


@pytest.mark.parametrize("reply,reference,derived", [
    (ABSTAINED, ABSTAIN_REF, "CORRECT"),
    (None, ABSTAIN_REF, "MISSED_ABSTAIN"),          # REPHRASED
    (ABSTAINED, REF, "WRONG_ABSTAIN"),
    (None, REF, "NOT_APPLICABLE"),
])
def test_abstention_is_derived_not_judged(reply, reference, derived):
    """Amendment A2 (review M2): an assessor value cannot hide a restated non-idea."""
    reply = reply or _reply()
    assert ev.derived_abstention(reply, reference) == derived
    rec = _record({p["id"]: "PRESERVED" for p in reference["points"]}, abstention=derived)
    verdict, hard, _e, _s = ev.case_verdict(EN, reference, ev.VALID, rec, reply)
    assert (verdict == ev.FAITHFUL) == (derived in ("CORRECT", "NOT_APPLICABLE"))
    assert ("missed abstention" in hard) == (derived == "MISSED_ABSTAIN")
    for other in ("CORRECT", "WRONG_ABSTAIN", "MISSED_ABSTAIN", "NOT_APPLICABLE"):
        if other != derived:
            with pytest.raises(PackError, match="abstention"):
                ev.case_verdict(EN, reference, ev.VALID, dict(rec, abstention=other), reply)


def test_assessment_must_judge_every_reference_point():
    keymap = {"R01": "x"}
    good = {"R01": _record({"P1": "PRESERVED", "P2": "PRESERVED"})}
    ev.check_assessment(good, keymap, {"x": REF})
    for bad in ({"R01": _record({"P1": "PRESERVED"})},
                {"R01": _record({"P1": "PRESERVED", "P2": "FINE"})},
                {"R01": dict(_record({"P1": "PRESERVED", "P2": "PRESERVED"}), extra=1)},
                {"R02": _record({"P1": "PRESERVED", "P2": "PRESERVED"})}):
        with pytest.raises(PackError):
            ev.check_assessment(bad, keymap, {"x": REF})


# ── Renderers ───────────────────────────────────────────────────────────────
CASES = [{"case_id": "en-%02d" % i, "variety": "en", "category": "PLAIN",
          "idea_text": "I want a sturdy folding step stool number %d." % i} for i in range(1, 6)]


def test_reader_message_carries_only_idea_texts_and_is_deterministic():
    msgs, keymap = ev.render_reader(CASES)
    assert ev.render_reader(CASES) == (msgs, keymap) and len(msgs) == 1
    msg = msgs[0]
    assert sorted(keymap.values()) == [c["case_id"] for c in CASES]
    for word in ("PLAIN", "en-01", "category", "variety\": \"en"):
        assert word not in msg.split("== TEXTS ==")[1]
    assert msg.startswith(ev.load_prereg()["messages"]["reader_template"].split("{ITEMS}")[0])


def test_adjudicator_message_randomises_sides():
    pts = {c["case_id"]: [{"kind": "FUNCTION", "statement": "a stool",
                           "source_span": "folding step stool"}] for c in CASES}
    msgs, keymap, sides = ev.render_adjudicator(CASES, pts, pts)
    assert ev.render_adjudicator(CASES, pts, pts) == (msgs, keymap, sides)
    assert all(set(s.values()) == {"author", "reader"} for s in sides.values())
    assert all("author" not in m.split("== ITEMS ==")[1] for m in msgs)


def test_transport_batching_splits_in_key_order_with_the_same_template():
    """Amendment A1: a rendering over the bound is delivered as consecutive
    complete renderings of the SAME template; content and keys never change."""
    big = [{"case_id": "en-%02d" % i, "variety": "en", "category": "PLAIN",
            "idea_text": ("I want a sturdy folding step stool number %d. " % i) * 40}
           for i in range(1, 41)]
    msgs, keymap = ev.render_reader(big)
    template = ev.load_prereg()["messages"]["reader_template"]
    assert len(msgs) > 1 and all(len(m.encode()) <= ev.TRANSPORT_BATCH_BYTES for m in msgs)
    head = template.split("{ITEMS}")[0]
    keys = []
    for m in msgs:
        assert m.startswith(head)
        keys += [x["key"] for x in json.loads(m[len(head):])]
    assert keys == sorted(keymap) and len(keys) == 40
    first, second, third = ev.load_prereg()["amendments"]
    assert first["id"] == "A1" and "before the adjudicator was engaged" in first["stage"]
    assert second["id"] == "A2" and "before any provider request or model output" in second["stage"]
    assert third["id"] == "A3" and "before any provider request or model output" in third["stage"]
    assert "Any of: an ALTERED point" in third["replaced_text"]


# ── The pinned pack and its independent authoring ──────────────────────────
EVIDENCE = ROOT / "docs" / "benchmarks" / "evidence" / "g1_faithful_rephrasing_v1_authoring"


def _authoring_record():
    return json.loads((EVIDENCE / "authoring_record.json").read_text(encoding="utf-8"))


def _evidence(prefix):
    texts = _authoring_record()["texts"]
    return [texts[k] for k in sorted(texts) if k.startswith(prefix)]


def test_pack_is_pinned_and_matches_the_plan():
    cases, ref = ev.load_pack()
    assert (_sha_file(ev.CASES_PATH), _sha_file(ev.REFERENCE_PATH)) == (
        ev.CASES_SHA256, ev.REFERENCE_SHA256)
    prereg = ev.load_prereg()
    for subset, plan in prereg["plan"].items():
        got = {}
        for c in cases:
            if c["variety"] == subset:
                got[c["category"]] = got.get(c["category"], 0) + 1
        assert got == plan, subset
    assert len({c["idea_text"] for c in cases}) == 40


def test_preparation_is_valid():
    cases, ref = ev.load_pack()
    prep = ev.preparation_checks(cases, ref)
    assert prep["verdict"] == ev.PREPARATION_VALID, prep
    assert prep["P6_overlap"] == [] and prep["P5_reference_defects"] == []


def _unwrap(delivered):
    """A cross-session follow-up arrives inside the transport's envelope: a
    preface, then the message with every line indented by four spaces."""
    start = delivered.index(">", delivered.index("<cross-session-message")) + 1
    body = delivered[start:delivered.index("</cross-session-message>")]
    body = body[body.index("    You are an INDEPENDENT"):]
    return "\n".join(l[4:] if l.startswith("    ") else l for l in body.split("\n")).rstrip()


def test_every_session_received_exactly_the_frozen_rendering():
    cases, _adjudicated = ev.load_pack()
    ref = json.loads(Path(ev.REFERENCE_PATH).read_text(encoding="utf-8"))
    prereg = ev.load_prereg()
    assert _evidence("author_user_") == [prereg["messages"]["author"]]
    reader_msgs, _ = ev.render_reader(cases)
    assert _evidence("reader_user_") == reader_msgs
    author_pts = {cid: r["points"] for cid, r in ref["author"].items()}
    reader_pts = {cid: r["points"] for cid, r in ref["reader"].items()}
    adj_msgs, keymap, sides = ev.render_adjudicator(cases, author_pts, reader_pts)
    received = _evidence("adjudicator_user_")
    assert len(received) == len(adj_msgs) == 2
    assert received[0] == adj_msgs[0]           # the session's first message
    assert _unwrap(received[1]) == adj_msgs[1]  # a follow-up, inside the transport envelope
    assert keymap == ref["adjudication"]["keymap"] and sides == ref["adjudication"]["sides"]


def test_the_prompt_was_frozen_before_any_case_existed():
    record = _authoring_record()
    assert record["prompt_freeze_commit"].startswith("5624f3c8")
    assert set(record["sha256"]) == set(record["texts"]) and len(record["texts"]) == 8
    for name, text in record["texts"].items():
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == record["sha256"][name]
    # No case text appears in the frozen prompt module.
    cases, _ref = ev.load_pack()
    prompt_src = (ROOT / "scripts" / "g1_faithful_rephrasing_prompt.py").read_text(encoding="utf-8")
    for c in cases:
        assert c["idea_text"][:40] not in prompt_src
