# -*- coding: utf-8 -*-
"""G1 faithful-readback statement-rejection proof (test-only, offline).

Two preserved replies of the merged faithful-rephrasing campaign (#978), as
they are: ``ar_gulf_kuwaiti-03`` (statement 1 says «أحيانًا» where the inventor
wrote «دايماً»; the Kuwaiti subset stays NOT_QUALIFIED) and the faithful
control ``ar_msa-01``. The readback, its tokens and the rejection are the
test-only seam ``tests/g1_faithful_readback_proof.py``; the project start, the
domain choice and the stored seed are the real product path.
"""
import os
import re
import sqlite3

import pytest

import tests.g1_faithful_readback_proof as fr
import web.app as appmod
from tests.test_g1_pcc_literal_source_aid import client  # noqa: F401  (fixture)

KUWAITI, CONTROL = "ar_gulf_kuwaiti-03", "ar_msa-01"
ELEC = "electronics_electrical"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _shown(case_id):
    idea, reply, case = fr.preserved(case_id)
    rb = fr.build(idea, reply, case)
    assert rb is not None
    return idea, reply, case, rb


def _li(html_text, index):
    m = re.search(r'<li data-statement="%d".*?</li>' % index, html_text, re.S)
    assert m, index
    return m.group(0)


def _start(c, idea):
    """The real start path: the description and the inventor's own domain
    choice and confirmation; returns the stored seed exactly as kept."""
    r = c.post("/start", data={"idea": idea, "domain_choice": ELEC, "domain_confirm": ELEC},
               follow_redirects=False)
    assert r.status_code == 302 and "/session/" in r.headers["Location"]
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    return appmod._get_store().load_reconstruction_inputs(sid)["seed_idea_text"]


def _dump():
    appmod._get_store()
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return "\n".join(conn.iterdump())
    finally:
        conn.close()


# ── The preserved replies, unchanged ────────────────────────────────────────
def test_the_replies_are_the_committed_ones_in_their_native_format():
    for case_id in (KUWAITI, CONTROL):
        idea, reply, case = fr.preserved(case_id)
        assert set(reply) == {"outcome", "language", "rephrasing", "statements", "abstain_reason"}
        assert fr.validate_reply(reply, case) == (fr.VALID, [])
    idea, reply, case = fr.preserved(KUWAITI)
    first = reply["statements"][0]
    assert "أحيانًا" in first["text"] and "دايماً" in first["source_quote"]
    assert first["source_quote"] in idea and "دايماً" in idea
    assert "أحيانًا" not in reply["rephrasing"] and "دايماً" not in reply["rephrasing"]


def test_a_changed_report_is_refused(monkeypatch):
    monkeypatch.setattr(fr, "REPORT_SHA256", "0" * 64)
    with pytest.raises(fr.ProofError):
        fr.preserved(KUWAITI)
    with pytest.raises(fr.ProofError):
        fr.preserved("en-01")


# ── Who wrote what ─────────────────────────────────────────────────────────
def test_every_text_is_labelled_with_its_author():
    idea, reply, case, rb = _shown(KUWAITI)
    page = fr.render(rb)
    assert '<blockquote data-author="inventor" data-inventor-words><bdi>%s</bdi>' % idea in page
    assert '<p data-author="ai" data-rephrasing><bdi>%s</bdi></p>' % reply["rephrasing"] in page
    for i, s in enumerate(reply["statements"]):
        li = _li(page, i)
        assert '<p data-author="ai"><span class="who">كتبها الذكاء الاصطناعي:</span> <bdi>%s</bdi>' \
            % s["text"] in li
        assert '<p data-author="inventor"><span class="who">كلماتك كما كتبتها:</span> «<bdi>%s</bdi>»' \
            % s["source_quote"] in li
    first = _li(page, 0)
    assert first.index("أحيانًا") < first.index("دايماً")       # the AI statement beside its source


# ── The inventor's action and its effect ────────────────────────────────────
def test_rejecting_the_sometimes_statement():
    idea, reply, case, rb = _shown(KUWAITI)
    res = fr.resolve(fr.issue(rb), rb, idea, case, "reject_statement", 0)
    new = res["readback"]
    assert res["rejected_by"] == fr.INVENTOR_AUTHORED and res["recorded"] is False
    assert [s.status for s in rb.statements] == [fr.SHOWN] * 4
    assert [s.status for s in new.statements] == [fr.REJECTED, fr.SHOWN, fr.SHOWN, fr.SHOWN]
    assert [(s.text, s.quote) for s in new.statements] == [(s.text, s.quote) for s in rb.statements]
    page = fr.render(new)
    rejected = _li(page, 0)
    assert 'data-status="rejected"' in rejected and "<del><bdi>" in rejected and "أحيانًا" in rejected
    assert fr.TEXT_AR["rejected"] in rejected and "data-reject=" not in rejected
    for i in (1, 2, 3):
        li = _li(page, i)
        assert 'data-status="shown"' in li and 'data-reject="%d"' % i in li and "<del>" not in li
    done = fr.resolve(res["token"], new, idea, case, "confirm")
    assert done["confirmed_statements"] == (1, 2, 3) and done["rejected_statements"] == (0,)
    assert done["scope"] == fr.CONFIRMATION_SCOPE and done["creates_project"] is False
    assert done["idea_text"] == idea and done["idea_origin"] == fr.INVENTOR_AUTHORED


def test_confirming_without_a_rejection_covers_every_statement():
    idea, reply, case, rb = _shown(CONTROL)
    done = fr.resolve(fr.issue(rb), rb, idea, case, "confirm")
    assert done["confirmed_statements"] == (0, 1, 2) and done["rejected_statements"] == ()


def test_tokens_are_one_use_and_bound_to_the_displayed_reading():
    idea, reply, case, rb = _shown(KUWAITI)
    token = fr.issue(rb)
    assert fr.resolve(token, rb, idea + " ", case, "reject_statement", 0) is None       # stale
    assert fr.resolve(token, rb, idea, case, "reject_statement", 9) is None             # no such statement
    assert fr.resolve(token, rb, idea, case, "reject_statement", True) is None
    assert fr.resolve(token, rb, idea, case, "something_else") is None
    _, _, _, other = _shown(CONTROL)
    assert fr.resolve(token, other, other.idea_text, fr.preserved(CONTROL)[2], "confirm") is None
    first = fr.resolve(token, rb, idea, case, "reject_statement", 0)
    assert first is not None
    assert fr.resolve(token, rb, idea, case, "reject_statement", 0) is None             # replayed
    new = first["readback"]
    assert fr.resolve(first["token"], new, idea, case, "reject_statement", 0) is None   # already rejected


def test_a_tampered_reply_is_refused():
    idea, reply, case, rb = _shown(KUWAITI)
    token = fr.issue(rb)
    reply["statements"][0]["text"] = reply["statements"][0]["text"].replace("أحيانًا", "دايماً")
    tampered = fr.build(idea, reply, case)
    assert tampered is not None
    assert fr.resolve(token, tampered, idea, case, "confirm") is None


def test_an_invalid_reply_shows_nothing():
    idea, reply, case = fr.preserved(KUWAITI)
    reply["statements"][0]["source_quote"] = "الغاز دايماً يخلص بسرعة كبيرة"     # not the inventor's words
    assert fr.build(idea, reply, case) is None


# ── The seed: the review never changes the description ─────────────────────
def test_the_stored_seed_is_byte_identical_with_and_without_the_review(client):
    idea, reply, case, rb = _shown(KUWAITI)
    direct = _start(client, idea)
    before = _dump()
    res = fr.resolve(fr.issue(rb), rb, idea, case, "reject_statement", 0)
    fr.resolve(res["token"], res["readback"], idea, case, "confirm")
    assert _dump() == before                                       # the review writes nothing
    reviewed = _start(client, idea)
    assert reviewed.encode("utf-8") == direct.encode("utf-8") == idea.encode("utf-8")
    assert "دايماً" in reviewed and "أحيانًا" not in reviewed


def test_skipping_the_review_reaches_the_same_original_seed(client):
    idea, reply, case, rb = _shown(CONTROL)
    fr.issue(rb)                                                   # shown, then not acted on
    assert _start(client, idea).encode("utf-8") == idea.encode("utf-8")


def test_the_seam_has_no_production_caller():
    for top in ("web", "engine", "scripts"):
        for base, _dirs, files in os.walk(os.path.join(_ROOT, top)):
            for name in files:
                if name.endswith((".py", ".html")):
                    with open(os.path.join(base, name), encoding="utf-8") as fh:
                        assert "g1_faithful_readback_proof" not in fh.read(), name
