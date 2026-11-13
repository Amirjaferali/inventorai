# -*- coding: utf-8 -*-
"""G1-1/2 correction-inclusion proof (synthetic, test-only).

Question: in ONE English journey, can an inventor write a correction in their
own words on the optional idea readback, choose to include that sentence in
the description that starts the project, and then use it in an engineering
step without typing it again?

Three paths are compared from project creation to the board-enclosure
clearance page, through the REAL application routes:
  SKIP     the inventor writes the correction but chooses not to include it;
  INCLUDE  the inventor previews the description and explicitly includes
           their own sentence;
  DIRECT   the inventor types the same sentence directly into the start form.

What is REAL here (unchanged production code, real HTTP requests):
  /start with the existing integrated declaration and project creation; the
  interaction, component and participation declarations; the clearance page
  and its literal-source aid (#929, which reads only the inventor's own text);
  the existing save path, evaluation and store.
What is SIMULATED (test-only, never mounted on a production page):
  * the AI reading is a CONSTRUCTED reply written for this proof, not a
    provider output, validated by the unchanged #928 validator;
  * the readback, its one-use binding and its correction come from the #975
    test seam (``tests/g1_intent_readback_proof.py``); #975's ``correct``
    action requires a part exclusion, so the remark-only correction and the
    include / skip step below are a small test-only extension of that seam;
  * the clearance page's script fills empty fields in a browser; here the
    inventor's chosen values and the aid's proposed note are submitted
    directly through the same form fields.
Nothing here changes production behaviour, and no AI wording ever becomes
part of the inventor's description.
"""
import hashlib
import hmac
import html as _html
import os
import re
import sqlite3

import pytest

import tests.g1_intent_readback_proof as rp
import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from scripts.run_g1_precreation_semantic_eval import AI_PROPOSED, UNVERIFIED
from tests.test_board_enclosure_planar_clearance import _margin_cells, _outcome
from tests.test_g1_pcc_literal_source_aid import (  # noqa: F401  (fixture)
    _aid_chunk, _body, _form_chunk, _project, _submit, _url, client)
from web import planar_clearance as aid

# ─────────────────────────────────────────────────────────────────────────────
# Synthetic inputs (no real inventor data)
# ─────────────────────────────────────────────────────────────────────────────
ORIGINAL = ("A small weather display for my balcony: a circuit board inside a plastic "
            "enclosure, with enough room around the board.")
REMARK = "The board is 84 x 50 mm."            # the inventor's own words, typed once
SOURCE = {"case_id": "CI01",
          "evidence_ref": "constructed for this proof; NOT a provider output"}
READING = {
    "outcome": "RESPONDED",
    "stated_function": [{"text": "A weather display for a balcony.",
                         "source_quote": "A small weather display for my balcony"}],
    "stated_parts": [
        {"text": "A circuit board", "source_quote": "a circuit board",
         "candidate_concept": "electronics_electrical"},
        {"text": "A plastic enclosure", "source_quote": "a plastic enclosure",
         "candidate_concept": "mechanical"}],
    "negated_or_excluded": [],
    "unknowns": ["The board's size is not stated."],
    "clarification_questions": [],
    "ai_suggestions": [],
    "composition_suggestion": "SUGGEST_INTEGRATED",
}
# The same reading, but the AI itself proposes a board size. That number must
# never be attributed to the inventor or reach the description.
AI_DIMENSION = dict(READING, ai_suggestions=[
    {"text": "A typical board for this would be 80 x 50 mm.",
     "attribution": AI_PROPOSED, "status": UNVERIFIED}])
VALUES_REST = ("90", "60", "2")                # region X, region Y, margin: unchanged inputs

INVENTOR_STATED = rp.INVENTOR_ORIGIN
_DOMAIN = "g1-correction-inclusion-proof-v1"
_PENDING = {}                                  # nonce -> True; in-memory, one use


# ─────────────────────────────────────────────────────────────────────────────
# Test-only extension of the #975 seam: remark-only correction, preview and an
# explicit include / skip decision. One-use, bound to the exact readback.
# ─────────────────────────────────────────────────────────────────────────────
def _sig(nonce, rb, stage):
    msg = appmod._canonical_message(
        _DOMAIN, stage, nonce, rp._digest(rb.idea_text),
        rp._digest(repr(sorted(rb.reply.items()))), rb.source[0], rb.source[1],
        ",".join(str(i) for i in rb.excluded), rp._digest(rb.remark))
    return hmac.new(appmod._answer_secret(), msg, hashlib.sha256).hexdigest()


def _issue(rb, stage):
    nonce = rp.secrets.token_urlsafe(16)
    _PENDING[nonce] = stage
    return nonce + "." + _sig(nonce, rb, stage)


def _redeem(token, rb, idea_text, stage):
    """Consume a token for exactly this readback and idea text, or None."""
    if not isinstance(token, str) or not isinstance(rb, rp.Readback):
        return False
    nonce, _, sig = token.partition(".")
    if _PENDING.get(nonce) != stage or idea_text != rb.idea_text:
        return False
    if not hmac.compare_digest(sig, _sig(nonce, rb, stage)):
        return False
    if rp.build(rb.idea_text, rb.reply, {"case_id": rb.source[0], "evidence_ref": rb.source[1]},
                rb.excluded, rb.remark) != rb:
        return False
    _PENDING.pop(nonce)
    return True


def show(idea_text, reply):
    rb = rp.build(idea_text, reply, SOURCE)
    return rb, (_issue(rb, "shown") if rb else None)


def correct_with_remark(token, rb, idea_text, remark):
    """The inventor's correction in their own words, without excluding a part.
    Returns the corrected readback and a token to preview it, or None."""
    if not isinstance(remark, str) or not remark.strip() or len(remark) > 300:
        return None
    if not _redeem(token, rb, idea_text, "shown"):
        return None
    new = rp.build(rb.idea_text, rb.reply, {"case_id": rb.source[0],
                                            "evidence_ref": rb.source[1]},
                   rb.excluded, remark)
    return {"readback": new, "remark_origin": INVENTOR_STATED, "token": _issue(new, "corrected")}


def preview(rb):
    """What the description WOULD be if the inventor includes their remark:
    the original text and the remark, each verbatim and each the inventor's.
    No AI wording is ever a segment. None when there is no remark."""
    if not rb.remark.strip():
        return None
    separator = " " if rb.idea_text.rstrip()[-1:] in ".!?؟" else "\n"
    return {"segments": [(INVENTOR_STATED, rb.idea_text), (INVENTOR_STATED, rb.remark)],
            "description": rb.idea_text + separator + rb.remark}


def decide(token, rb, idea_text, choice):
    """The inventor's explicit choice. ``include`` returns the previewed
    description, ``skip`` the original text; anything else, a stale or
    replayed token, or a readback without a remark returns None. Nothing is
    stored and no project is created here."""
    if choice not in ("include", "skip") or preview(rb) is None:
        return None
    if not _redeem(token, rb, idea_text, "corrected"):
        return None
    return preview(rb)["description"] if choice == "include" else rb.idea_text


def _readback_with_remark(reply=READING, remark=REMARK):
    rb, token = show(ORIGINAL, reply)
    assert rb is not None and token
    corrected = correct_with_remark(token, rb, ORIGINAL, remark)
    assert corrected is not None and corrected["remark_origin"] == INVENTOR_STATED
    return corrected["readback"], corrected["token"]


# ─────────────────────────────────────────────────────────────────────────────
# One journey: from the description to the clearance page and the saved check
# ─────────────────────────────────────────────────────────────────────────────
def _journey(client, description):
    """Create the project through the real /start and reach the clearance page."""
    sid, ifc, ids = _project(client, description)
    seed = appmod._get_store().load_reconstruction_inputs(sid)["seed_idea_text"]
    body = _body(client.get(_url(sid, ifc)))
    return {"sid": sid, "ifc": ifc, "ids": ids, "seed": seed, "body": body,
            "aid": _aid_chunk(body), "offer": aid.aid_offer(
                aid.current_board_pair(seed, []), "en")}


def _save(client, j, board_x, board_y, note):
    r = _submit(client, j["sid"], j["ifc"], j["ids"], board_x, board_y, note)
    assert r.status_code == 200, _body(r)
    material = appmod._get_store().load_planar_clearance(j["sid"])["ledger"] \
        .active_for(j["ifc"]).current
    return {"outcome": _outcome(_body(r)), "margins": _margin_cells(_body(r)),
            "values": material.values_map(), "note": material.basis_map()["basis_board"]}


def _nothing_chosen(body):
    form = _form_chunk(body)
    assert not re.search(r"<input[^>]*\bchecked\b", form)
    assert not re.search(r"<option[^>]*\bselected\b", form)      # no board / enclosure chosen
    assert re.search(r'id="pcc-v-board_x"[^>]*value=""', form)
    assert re.search(r'id="pcc-v-board_y"[^>]*value=""', form)
    chunk = _aid_chunk(body)
    if chunk is not None:
        assert not re.search(r"<input[^>]*\bchecked\b", chunk)   # no axis order chosen


# ==========================================================================
# 1. the three paths
# ==========================================================================
def test_p1_skip_keeps_the_original_and_the_engineering_step_has_no_aid(client):
    rb, token = _readback_with_remark()
    description = decide(token, rb, ORIGINAL, "skip")
    assert description == ORIGINAL
    j = _journey(client, description)
    assert j["seed"] == ORIGINAL and j["aid"] is None and j["offer"] is None
    assert "84 x 50" not in j["body"]                       # the remark was not carried
    _nothing_chosen(j["body"])
    # The inventor can still reach the same result, but must type 84 and 50 again.
    manual = _save(client, j, "84", "50", "Measured with a ruler")
    assert manual["values"]["board_x"] == "84" and manual["values"]["board_y"] == "50"


def test_p2_include_carries_the_inventors_sentence_to_the_clearance_aid(client):
    rb, token = _readback_with_remark()
    p = preview(rb)
    assert p["segments"] == [(INVENTOR_STATED, ORIGINAL), (INVENTOR_STATED, REMARK)]
    assert p["description"] == ORIGINAL + " " + REMARK
    description = decide(token, rb, ORIGINAL, "include")
    assert description == p["description"]
    j = _journey(client, description)
    assert j["seed"] == ORIGINAL + " " + REMARK                  # stored exactly as included
    assert j["aid"] is not None
    assert _html.unescape(re.search(r"data-pcc-aid-passage>(.*?)</blockquote>", j["aid"], re.S)
                          .group(1)) == "The board is 84 x 50 mm"
    assert j["offer"]["source"] == aid.AID_SOURCE_IDEA
    assert [(o["order"], o["x"], o["y"]) for o in j["offer"]["orders"]] == [
        ("first_x", "84", "50"), ("first_y", "50", "84")]
    # The board, the enclosure, the axis order and the save stay the inventor's.
    _nothing_chosen(j["body"])
    chosen = j["offer"]["orders"][0]                             # the inventor picks first_x
    saved = _save(client, j, chosen["x"], chosen["y"], chosen["note"])
    assert saved["values"]["board_x"] == "84" and saved["values"]["board_y"] == "50"
    assert saved["note"] == ("From my original idea: “84 x 50 mm”; "
                             "I entered 84 as board X and 50 as board Y.")


def test_p3_direct_typing_gives_the_same_seed_aid_and_result_as_including(client):
    rb, token = _readback_with_remark()
    included = _journey(client, decide(token, rb, ORIGINAL, "include"))
    direct = _journey(client, ORIGINAL + " " + REMARK)            # typed in the start form
    assert included["seed"] == direct["seed"]
    assert included["offer"] == direct["offer"]
    a = _save(client, included, "84", "50", included["offer"]["orders"][0]["note"])
    b = _save(client, direct, "84", "50", direct["offer"]["orders"][0]["note"])
    assert a == b and a["outcome"] == ["MET"]


def test_p4_all_three_paths_reach_the_same_engineering_result(client):
    """The engineering outcome depends only on the values the inventor saves.
    SKIP needs the dimensions typed a second time; INCLUDE and DIRECT do not."""
    results, typed = {}, {}
    rb, token = _readback_with_remark()
    skip = _journey(client, decide(token, rb, ORIGINAL, "skip"))
    results["skip"] = _save(client, skip, "84", "50", "Measured with a ruler")
    typed["skip"] = [REMARK, "84", "50"]                         # remark, then both numbers again
    rb, token = _readback_with_remark()
    inc = _journey(client, decide(token, rb, ORIGINAL, "include"))
    results["include"] = _save(client, inc, "84", "50", inc["offer"]["orders"][0]["note"])
    typed["include"] = [REMARK]                                  # typed once, on the readback
    direct = _journey(client, ORIGINAL + " " + REMARK)
    results["direct"] = _save(client, direct, "84", "50", direct["offer"]["orders"][0]["note"])
    typed["direct"] = [REMARK]                                   # typed once, in the start form
    outcomes = {k: (v["outcome"], v["margins"], v["values"]) for k, v in results.items()}
    assert outcomes["skip"] == outcomes["include"] == outcomes["direct"]
    assert sum(map(len, typed["skip"])) > sum(map(len, typed["include"])) \
        == sum(map(len, typed["direct"]))


# ==========================================================================
# 2. attribution: an AI-proposed dimension is never the inventor's
# ==========================================================================
def test_a1_an_ai_suggested_size_never_reaches_the_description_or_the_aid(client):
    rb, token = show(ORIGINAL, AI_DIMENSION)
    assert rb is not None and "80 x 50 mm" in repr(rb.reply)
    # Confirming the reading confirms meaning only and keeps the description.
    confirmed = rp.resolve(rp.issue(rb), rb, ORIGINAL, "confirm")
    assert confirmed["idea_text"] == ORIGINAL and confirmed["recorded"] is False
    j = _journey(client, confirmed["idea_text"])
    assert j["aid"] is None and "80 x 50" not in j["body"]
    # There is nothing of the inventor's to include without a remark.
    assert preview(rb) is None and decide(token, rb, ORIGINAL, "include") is None


def test_a2_with_both_only_the_inventors_size_is_carried(client):
    rb, token = _readback_with_remark(reply=AI_DIMENSION)
    p = preview(rb)
    assert all(origin == INVENTOR_STATED for origin, _text in p["segments"])
    assert "80 x 50" not in p["description"] and "typical" not in p["description"]
    j = _journey(client, decide(token, rb, ORIGINAL, "include"))
    assert "80 x 50" not in j["seed"] and "80 x 50" not in j["body"]
    assert (j["offer"]["first"], j["offer"]["second"]) == ("84", "50")


def test_a3_no_ai_authored_wording_enters_the_description():
    """Every AI-authored text of the reading (functions, parts, unknowns,
    suggestions) stays out of the description; only the inventor's original
    text and remark are segments, each labelled the inventor's."""
    rb, token = _readback_with_remark(reply=AI_DIMENSION)
    assert rb.origin == (rp.READING_ORIGIN, rp.READING_STATUS)
    ai_texts = ([f["text"] for f in AI_DIMENSION["stated_function"]]
                + [p["text"] for p in AI_DIMENSION["stated_parts"]]
                + list(AI_DIMENSION["unknowns"])
                + [s["text"] for s in AI_DIMENSION["ai_suggestions"]])
    description = decide(token, rb, ORIGINAL, "include")
    assert description == ORIGINAL + " " + REMARK
    for text in ai_texts:
        assert text not in description, text


# ==========================================================================
# 3. binding and side effects
# ==========================================================================
def test_b1_stale_replayed_tampered_and_invalid_choices_are_refused():
    rb, token = show(ORIGINAL, READING)
    assert correct_with_remark(token, rb, ORIGINAL + " changed", REMARK) is None   # stale
    assert correct_with_remark(token, rb, ORIGINAL, " ") is None                   # empty remark
    corrected = correct_with_remark(token, rb, ORIGINAL, REMARK)
    assert corrected is not None
    assert correct_with_remark(token, rb, ORIGINAL, REMARK) is None                # replayed
    new, t2 = corrected["readback"], corrected["token"]
    assert decide(t2, new, ORIGINAL, "maybe") is None                               # invalid choice
    assert decide(t2 + "x", new, ORIGINAL, "include") is None                       # tampered
    assert decide(t2, new, ORIGINAL, "include") is not None
    assert decide(t2, new, ORIGINAL, "include") is None                             # one use


def _dump():
    appmod._get_store()
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as conn:
        return "\n".join(conn.iterdump())


def test_b2_the_readback_steps_write_nothing(client):
    before = _dump()
    rb, token = _readback_with_remark()
    assert decide(token, rb, ORIGINAL, "include") is not None
    assert _dump() == before


def test_b3_the_recognizer_locates_the_remark_and_nothing_in_the_original():
    assert aid.literal_board_pair(REMARK) == {"passage": "The board is 84 x 50 mm",
                                              "span": "84 x 50 mm", "first": "84",
                                              "second": "50", "unit": "mm"}
    assert aid.literal_board_pair(ORIGINAL) is None
    assert aid.literal_board_pair(AI_DIMENSION["ai_suggestions"][0]["text"]) is None
    assert pcc.is_admitted_value("board_x", "84") and pcc.is_admitted_value("board_y", "50")
