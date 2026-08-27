"""RVR-7 — render-edge / identity-based resolution (engine + seam layer).

Authority: the authoritative RVR-7 Implementation Path Manifest Freeze (PR #588),
architecture §5.A-§5.F.

What this module proves: the engine stays language-blind; the display identity is
named FORWARD from canonical state and never by reverse-looking-up text; and every
sentinel and serving decision (S1, S2, S3, S4, W2-B, W2-C) behaves identically
whatever language is displayed — because the engine never sees a language at all.
"""

import hashlib
import inspect
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
ARABIC = re.compile("[؀-ۿ]")

DOMAINS = ("electronics_electrical", "mechanical")
STAGE2 = ("MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY")
STAGE3 = ("PROBLEM_MECHANISM_FIT", "ASSUMPTION_INVENTORY", "EXPERTISE_GAP_AWARENESS")
ALL_GAPS = STAGE2 + STAGE3


# ---------------------------------------------------------------------------
# 1. The engine is language-blind — structurally, not by convention
# ---------------------------------------------------------------------------

def test_progression_loop_is_byte_unchanged_by_rvr7():
    """Q2 shape B: the governed English prompt constants stay engine-owned and the
    file is not touched for language. Its digest is still the one the three P9
    modules pin, which `tests/test_w2b_amc_consumers.py` independently re-checks."""
    digest = hashlib.sha256(
        (REPO / "engine" / "progression_loop.py").read_bytes()).hexdigest()
    pinned = set()
    pin_re = re.compile(r'"engine/progression_loop\.py":\s*"([0-9a-f]{64})"')
    for rel in ("tests/test_p9_mech_i3_signal_quality.py",
                "tests/test_p9_mech_i4_boundary_corpus.py",
                "tests/test_p9_mech_i5_question_sufficiency.py"):
        match = pin_re.search((REPO / rel).read_text(encoding="utf-8"))
        assert match, rel
        pinned.add(match.group(1))
    assert pinned == {digest}


def test_no_language_signal_anywhere_in_the_engine():
    """No engine module may acquire a language parameter, a language state field,
    or user-facing Arabic content. Comments are excluded — only code is inspected."""
    offenders = []
    for path in sorted((REPO / "engine").glob("*.py")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            code = line.split("#", 1)[0]
            if re.search(r"\b(ui_lang|lang\s*=|lang\s*:)", code):
                offenders.append(f"{path.name}:{number}")
    assert not offenders, f"language signal reached the engine: {offenders}"


def test_progression_selectors_take_no_language_parameter():
    from engine.progression_loop import get_question, get_display_question
    from engine.path_n_questions import get_served_question, get_path_n_question
    for fn in (get_question, get_display_question,
               get_served_question, get_path_n_question):
        names = set(inspect.signature(fn).parameters)
        assert not (names & {"lang", "language", "ui_lang"}), fn.__name__


def test_english_selection_is_unchanged_for_every_reachable_position():
    """EN behaviour preserved: the pure selector and the display selector return
    exactly the committed English for every gap, index and domain."""
    from engine.progression_loop import get_question, get_display_question, QUESTIONS
    from engine.path_n_questions import get_path_n_question
    for domain in DOMAINS:
        for gap in ALL_GAPS:
            for index in range(0, 8):
                served = get_question(domain, gap, index, path="N")
                artifact = get_path_n_question(gap, index, domain=domain)
                expected = artifact if artifact is not None else QUESTIONS[gap][
                    min(index, len(QUESTIONS[gap]) - 1)]
                assert served == expected
                assert not ARABIC.search(get_display_question(
                    domain, gap, index, path="N"))


# ---------------------------------------------------------------------------
# 2. Forward identity resolution — and no reverse lookup
# ---------------------------------------------------------------------------

def test_identity_reproduces_the_engine_decision_everywhere():
    """The render-edge identity, resolved to its committed ENGLISH text, equals
    what `get_display_question` decided — for every reachable position."""
    from web.app import _rvr7_identity
    from engine.progression_loop import get_display_question, QUESTIONS
    from engine.progression_loop import _STALL_REFRAME, _EXHAUSTED_EXIT_PROMPT
    from web import ui_text
    checked = 0
    for domain in DOMAINS:
        for gap in ALL_GAPS:
            for index in range(0, 8):
                english = get_display_question(domain, gap, index, path="N")
                identity, served = _rvr7_identity(domain, gap, index, "N")
                if served is not None:
                    resolved = served.text
                elif identity == ui_text.RVR7_STALL_REFRAME:
                    resolved = _STALL_REFRAME
                elif identity == ui_text.RVR7_EXHAUSTED_EXIT_PROMPT:
                    resolved = _EXHAUSTED_EXIT_PROMPT
                else:
                    _, generic_gap, generic_index = identity.split(":", 2)
                    resolved = QUESTIONS[generic_gap][int(generic_index)]
                assert resolved == english, (domain, gap, index, identity)
                checked += 1
    assert checked == len(DOMAINS) * len(ALL_GAPS) * 8


def test_identity_never_derives_from_displayed_text():
    """Static evidence for the no-reverse-lookup rule: the resolver's own source
    consults canonical inputs only — it never receives or inspects the served text."""
    from web import app as webapp
    source = inspect.getsource(webapp._rvr7_identity)
    parameters = set(inspect.signature(webapp._rvr7_identity).parameters)
    assert parameters == {"domain", "gap_type", "iterations_open", "path",
                          "override_source", "w2c"}
    assert "text" not in parameters
    for banned in ("== english", "in english", "english.", ".text ==", "startswith(text"):
        assert banned not in source, banned


def test_forward_lookup_by_id_never_matches_on_text():
    from engine.path_n_questions import get_served_question, get_served_question_by_id
    served = get_served_question("BOUNDARY_AMBIGUITY", 0, domain="electronics_electrical")
    found = get_served_question_by_id("BOUNDARY_AMBIGUITY", served.question_id,
                                      domain="electronics_electrical")
    assert found is not None and found.question_id == served.question_id
    # The record's own TEXT is not an id and resolves to nothing.
    assert get_served_question_by_id("BOUNDARY_AMBIGUITY", served.text,
                                     domain="electronics_electrical") is None
    assert get_served_question_by_id("BOUNDARY_AMBIGUITY", served.text_ar,
                                     domain="electronics_electrical") is None


def test_display_resolution_is_english_unless_arabic_selected():
    from web.app import _rvr7_identity, _rvr7_display
    from engine.progression_loop import get_display_question
    for domain in DOMAINS:
        for gap in ALL_GAPS:
            for index in (0, 3, 5):
                english = get_display_question(domain, gap, index, path="N")
                identity, served = _rvr7_identity(domain, gap, index, "N")
                assert _rvr7_display(identity, served, english, "en") == english
                arabic = _rvr7_display(identity, served, english, "ar")
                assert ARABIC.search(arabic), (domain, gap, index)


def test_display_fails_closed_to_english_on_identity_mismatch():
    """If the resolver ever drifted from the engine, the forward verification
    catches it and English is served — never Arabic for the wrong ask."""
    from web.app import _rvr7_identity, _rvr7_display
    identity, served = _rvr7_identity("electronics_electrical",
                                      "BOUNDARY_AMBIGUITY", 0, "N")
    assert _rvr7_display(identity, served, "SOME OTHER ENGLISH ASK", "ar") == \
        "SOME OTHER ENGLISH ASK"


def test_missing_arabic_variant_falls_back_to_english_deterministically():
    from web.app import _rvr7_display
    from engine.path_n_questions import ServedQuestion
    bare = ServedQuestion(question_id="N-BA-1", text="EN ASK",
                          design_gap_id="BOUNDARY_AMBIGUITY", text_ar=None)
    assert _rvr7_display("PATHN:N-BA-1", bare, "EN ASK", "ar") == "EN ASK"
    assert _rvr7_display("GENERIC:PROBLEM_MECHANISM_FIT:99", None, "EN ASK", "ar") == "EN ASK"


# ---------------------------------------------------------------------------
# 3. Sentinels S1-S4 and the W2-B / W2-C decisions are language-invariant
# ---------------------------------------------------------------------------

def test_s1_exhaustion_timing_unchanged():
    """S1 clamps on English text on BOTH sides, so exhaustion fires at exactly the
    same iteration whatever is displayed."""
    from engine.progression_loop import (get_display_question, _STALL_REFRAME,
                                         _EXHAUSTED_EXIT_PROMPT)
    expected = {"electronics_electrical": {"BOUNDARY_AMBIGUITY": 3},
                "mechanical": {"PHYSICAL_FEASIBILITY": 2}}
    for domain, gaps in expected.items():
        for gap, first_reframe in gaps.items():
            for index in range(0, first_reframe):
                displayed = get_display_question(domain, gap, index, path="N")
                assert displayed not in (_STALL_REFRAME, _EXHAUSTED_EXIT_PROMPT)
            assert get_display_question(
                domain, gap, first_reframe, path="N") == _STALL_REFRAME
            assert get_display_question(
                domain, gap, first_reframe + 1, path="N") == _EXHAUSTED_EXIT_PROMPT


def test_s2_generic_clamped_repeat_behaviour_unchanged():
    """S2 stays inert on artifact-covered Stage-2 gaps (it yields to RVR-2's
    governed surface) and stays active on Stage-3 gaps."""
    from engine.progression_loop import get_question
    from engine.path_n_questions import get_path_n_question
    for domain in DOMAINS:
        for gap in STAGE2:
            assert get_path_n_question(gap, 4, domain=domain) is not None
        for gap in STAGE3:
            assert get_path_n_question(gap, 0, domain=domain) is None
            assert get_question(domain, gap, 3, path="N") == \
                get_question(domain, gap, 2, path="N")


def test_s3_lapsed_acceptance_comparison_is_english_on_both_sides():
    """S3 compares `get_question(..., 0)` against `get_display_question(...)`;
    both are English, so the trigger set cannot shift with the display language."""
    from engine.progression_loop import get_question, get_display_question
    for domain in DOMAINS:
        for gap in ALL_GAPS:
            for index in (0, 1, 3, 4):
                primary = get_question(domain, gap, 0, path="N")
                baseline = get_display_question(domain, gap, index, path="N")
                assert not ARABIC.search(primary)
                assert not ARABIC.search(baseline)


def test_s4_canonical_comparison_operates_on_english_only():
    """S4 gates W2-C on `question == _canonical_q`. The render edge localises
    AFTER that gate, so the comparison stays English-on-English and W2-C
    reachability is identical in both languages."""
    from web import app as webapp
    source = inspect.getsource(webapp.show_session)
    gate = source.index("_canonical_q = get_question(")
    localisation = source.index("question = _rvr7_display(")
    assert gate < localisation, (
        "language resolution must happen AFTER the S4 canonical comparison")


def test_w2b_candidate_identities_map_without_text():
    from web.app import _rvr7_identity
    from engine.progression_loop import (STALL_THRESHOLD, TRIGGER_LAPSED_ACCEPTANCE,
                                         TRIGGER_COMPLETED_INTENT_SKIP,
                                         TRIGGER_CRITICAL_UNRESOLVED)
    from web import ui_text
    from engine.path_n_questions import get_served_question
    for domain in DOMAINS:
        for gap in STAGE2:
            identity, served = _rvr7_identity(
                domain, gap, 5, "N", override_source=TRIGGER_LAPSED_ACCEPTANCE)
            assert served.question_id == get_served_question(
                gap, 0, domain=domain).question_id
            assert identity == "PATHN:" + served.question_id
            assert _rvr7_identity(domain, gap, 5, "N",
                                  override_source=TRIGGER_COMPLETED_INTENT_SKIP)[0] \
                == ui_text.RVR7_EXHAUSTED_EXIT_PROMPT
            assert _rvr7_identity(domain, gap, STALL_THRESHOLD, "N",
                                  override_source=TRIGGER_CRITICAL_UNRESOLVED)[0] \
                == ui_text.RVR7_STALL_REFRAME
            assert _rvr7_identity(domain, gap, STALL_THRESHOLD + 1, "N",
                                  override_source=TRIGGER_CRITICAL_UNRESOLVED)[0] \
                == ui_text.RVR7_EXHAUSTED_EXIT_PROMPT


def test_w2c_identity_is_preserved_through_the_render_edge():
    """W2-C already returns `IntentServing.question_id`; the render edge keeps it
    and resolves that record forward instead of reducing the decision to text."""
    from web.app import _rvr7_identity
    from engine.intent_serving import IntentServing
    from engine.path_n_questions import get_served_question
    canonical = get_served_question("MECHANISM_COMPLETENESS", 0,
                                    domain="electronics_electrical")
    adjusted = get_served_question("MECHANISM_COMPLETENESS", 2,
                                   domain="electronics_electrical")
    serving = IntentServing(adjusted.question_id, adjusted.text,
                            adjusted.design_gap_id, adjusted=True)
    identity, served = _rvr7_identity("electronics_electrical",
                                      "MECHANISM_COMPLETENESS", 0, "N", w2c=serving)
    assert identity == "PATHN:" + adjusted.question_id
    assert served.question_id != canonical.question_id
    assert served.text_ar == adjusted.text_ar


def test_q2_arabic_reachable_through_both_routes():
    """Q2 = INCLUDE proven through the S1 exhaustion route AND the W2-B trigger
    route, without `engine/progression_loop.py` being touched."""
    from web.app import _rvr7_identity, _rvr7_display
    from engine.progression_loop import (get_display_question, _STALL_REFRAME,
                                         _EXHAUSTED_EXIT_PROMPT, STALL_THRESHOLD,
                                         TRIGGER_COMPLETED_INTENT_SKIP,
                                         TRIGGER_CRITICAL_UNRESOLVED)
    english = get_display_question("electronics_electrical",
                                   "BOUNDARY_AMBIGUITY", 3, path="N")
    assert english == _STALL_REFRAME
    identity, served = _rvr7_identity("electronics_electrical",
                                      "BOUNDARY_AMBIGUITY", 3, "N")
    assert ARABIC.search(_rvr7_display(identity, served, english, "ar"))
    for source, index, english_text in (
            (TRIGGER_COMPLETED_INTENT_SKIP, 4, _EXHAUSTED_EXIT_PROMPT),
            (TRIGGER_CRITICAL_UNRESOLVED, STALL_THRESHOLD, _STALL_REFRAME),
            (TRIGGER_CRITICAL_UNRESOLVED, STALL_THRESHOLD + 2, _EXHAUSTED_EXIT_PROMPT)):
        identity, served = _rvr7_identity("electronics_electrical",
                                          "PROBLEM_MECHANISM_FIT", index, "N",
                                          override_source=source)
        assert ARABIC.search(_rvr7_display(identity, served, english_text, "ar"))


# ---------------------------------------------------------------------------
# 4. Reconstruction / determinism boundary
# ---------------------------------------------------------------------------

def test_reconstruction_version_and_module_untouched():
    from engine import session_reconstruction as sr
    assert sr.RECONSTRUCTION_VERSION == "p4-2-level1-recon-v1"
    source = (REPO / "engine" / "session_reconstruction.py").read_text(encoding="utf-8")
    assert not ARABIC.search(source)
    assert "lang" not in re.sub(r"#.*", "", source)


def test_reconstructed_banner_identity_comes_from_canonical_state():
    """Cold-load Arabic is derived from the reconstructed canonical state, never
    from the reconstructed English text."""
    from web import app as webapp
    source = inspect.getsource(webapp._rvr7_reconstructed_display)
    assert "select_next_gap(recon_state)" in source
    assert "iterations_open" in source
    for banned in ("== english", "english ==", "in english"):
        assert banned not in source


def test_canonical_state_and_persistence_carry_no_language():
    from engine.idea_state import IdeaState
    state = IdeaState(idea_id="rvr7-probe")
    assert not [f for f in vars(state) if "lang" in f.lower()]
