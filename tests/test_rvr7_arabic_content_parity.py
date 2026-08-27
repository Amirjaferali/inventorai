"""RVR-7 — committed Arabic content parity (content layer).

Authority: the authoritative RVR-7 Implementation Path Manifest Freeze
(`docs/governance/RVR_7_IMPLEMENTATION_PATH_MANIFEST_FREEZE_CANDIDATE.md`,
merged PR #588) and the Owner decisions it records — D-P6-18 BOUNDED, Q2 INCLUDE,
D-RVR7-1 Option A (Journey-Complete).

Scope of THIS module: the committed content itself — completeness of the Arabic
surface across the whole authorized journey scope, single-identity discipline, the
closed key allowlist, and the absence of any parallel registry. It inspects
committed artifacts and committed catalogues only.

Deliberately import-light, mirroring the discipline of
`tests/test_path_n_content_config_artifact.py`: no Flask, no test client, no
session route. The served-route evidence lives in
`tests/test_rvr7_web_arabic_serving.py`; the seam/sentinel evidence lives in
`tests/test_rvr7_render_edge_resolution.py`.
"""

import json
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "docs" / "governance" / "path_n_content_config"

ARABIC = re.compile("[؀-ۿ]")

DOMAIN_ARTIFACTS = {
    "electronics_electrical": CONFIG / "electronics_electrical_path_n_questions.json",
    "mechanical": CONFIG / "mechanical_path_n_questions.json",
}

# The Owner-decided Journey-Complete scope (D-RVR7-1 Option A), split by carrier:
# committed records carry their own Arabic; the rest are identity-keyed.
STAGE3_GAPS = ("PROBLEM_MECHANISM_FIT", "ASSUMPTION_INVENTORY",
               "EXPERTISE_GAP_AWARENESS")
STAGE2_GAPS = ("MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY",
               "BOUNDARY_AMBIGUITY")

ALLOWED_ENTRY_KEYS = {"question_id", "text", "text_ar"}


def _artifact(domain):
    with open(DOMAIN_ARTIFACTS[domain], encoding="utf-8") as fh:
        return json.load(fh)


def _entries(domain):
    return [e for v in _artifact(domain)["gaps"].values() for e in v]


# ---------------------------------------------------------------------------
# 1. Committed Path-N records — all 21 ids carry Arabic, under ONE identity
# ---------------------------------------------------------------------------

def test_all_21_committed_ids_have_arabic():
    total = 0
    missing = []
    for domain in DOMAIN_ARTIFACTS:
        for e in _entries(domain):
            total += 1
            if not (isinstance(e.get("text_ar"), str) and e["text_ar"].strip()):
                missing.append((domain, e.get("question_id")))
    assert total == 21, f"expected the 21 committed Path-N ids, found {total}"
    assert not missing, f"committed ids with no Arabic variant: {missing}"


def test_one_question_id_carries_both_language_surfaces():
    """ONE QUESTION_ID -> EN + AR content variant. The Arabic never gets its own
    id, and both surfaces are read from the SAME physical record."""
    for domain in DOMAIN_ARTIFACTS:
        for e in _entries(domain):
            assert isinstance(e["question_id"], str) and e["question_id"].strip()
            assert isinstance(e["text"], str) and e["text"].strip()
            assert isinstance(e["text_ar"], str) and e["text_ar"].strip()
            assert e["text"] != e["text_ar"]


def test_arabic_variant_is_actually_arabic_and_english_is_not():
    for domain in DOMAIN_ARTIFACTS:
        for e in _entries(domain):
            qid = e["question_id"]
            assert ARABIC.search(e["text_ar"]), f"{qid}: text_ar carries no Arabic"
            assert not ARABIC.search(e["text"]), f"{qid}: English surface drifted"


def test_entry_key_set_is_the_closed_allowlist():
    for domain in DOMAIN_ARTIFACTS:
        for e in _entries(domain):
            assert set(e).issubset(ALLOWED_ENTRY_KEYS), (domain, e.get("question_id"))
            assert {"question_id", "text"}.issubset(e)


def test_index_isomorphism_en_ar():
    """Arabic is index-isomorphic to English: same gap keys, same order, same
    count — the clamp/exhaustion position law is therefore identical."""
    for domain in DOMAIN_ARTIFACTS:
        gaps = _artifact(domain)["gaps"]
        for gap, variants in gaps.items():
            en = [e["question_id"] for e in variants]
            ar = [e["question_id"] for e in variants if e.get("text_ar")]
            assert en == ar, (domain, gap)


# ---------------------------------------------------------------------------
# 2. No parallel registry, no second content location, no runtime translation
# ---------------------------------------------------------------------------

def test_exactly_two_path_n_artifacts_exist():
    found = sorted(p.name for p in CONFIG.glob("*_path_n_questions.json"))
    assert found == ["electronics_electrical_path_n_questions.json",
                     "mechanical_path_n_questions.json"], found


def test_domain_artifact_mapping_stays_one_dimensional():
    """The bounded domain->artifact mapping gains no language axis; a
    domain x language mapping would BE a parallel registry."""
    from engine import path_n_questions as pnq
    assert set(pnq._DOMAIN_ARTIFACTS) == {"electronics_electrical", "mechanical"}
    for value in pnq._DOMAIN_ARTIFACTS.values():
        assert str(value).endswith("_path_n_questions.json")


def test_ws10_intent_registries_carry_no_arabic_and_stay_english_audit_prose():
    """The WS10 registries are audit metadata that is never displayed; their
    `language: en` stays truthful and they are NOT a second content location."""
    for name in ("electronics_electrical_question_intent_registry.json",
                 "mechanical_question_intent_registry.json"):
        raw = (CONFIG / name).read_text(encoding="utf-8")
        assert not ARABIC.search(raw), name
        assert json.loads(raw)["metadata"]["language"] == "en"


def test_ws10_source_id_set_equality_still_holds():
    """WS10 D11: registry ids and artifact ids remain exactly equal, so no
    Arabic id was minted anywhere."""
    from engine.question_intent_registry import load_question_intent_registry
    for domain in DOMAIN_ARTIFACTS:
        reg_rel = f"docs/governance/path_n_content_config/{domain}_question_intent_registry.json"
        src_rel = f"docs/governance/path_n_content_config/{domain}_path_n_questions.json"
        registry = load_question_intent_registry(Path(reg_rel), Path(src_rel))
        reg_ids = {r.question_id for r in registry.list_records()}
        art_ids = {e["question_id"] for e in _entries(domain)}
        assert reg_ids == art_ids, domain


def test_no_runtime_translation_dependency():
    """No translation library, service call or model invocation was introduced on
    any authorized runtime path."""
    banned = ("googletrans", "deep_translator", "translate(", "Translator(",
              "translation_api", "openai", "anthropic")
    for rel in ("engine/path_n_questions.py", "web/ui_text.py", "web/app.py"):
        src = (REPO / rel).read_text(encoding="utf-8").lower()
        for needle in banned:
            assert needle.lower() not in src, f"{rel} references {needle!r}"


# ---------------------------------------------------------------------------
# 3. Journey-Complete: the non-record substantive asks are covered too
# ---------------------------------------------------------------------------

def test_every_special_substantive_identity_has_arabic():
    from web import ui_text
    required = (ui_text.RVR7_STALL_REFRAME, ui_text.RVR7_EXHAUSTED_EXIT_PROMPT,
                ui_text.RVR7_INTAKE_QUESTION, ui_text.RVR7_CLOSING_Q)
    missing = [k for k in required
               if not (ui_text.RVR7_SUBSTANTIVE_AR.get(k) or "").strip()]
    assert not missing, f"special substantive identities with no Arabic: {missing}"


def test_every_reachable_stage3_generic_ask_has_arabic():
    from web import ui_text
    from engine.progression_loop import QUESTIONS
    missing = []
    for gap in STAGE3_GAPS:
        for index in range(len(QUESTIONS[gap])):
            identity = ui_text.rvr7_generic_identity(gap, index)
            if not (ui_text.RVR7_SUBSTANTIVE_AR.get(identity) or "").strip():
                missing.append(identity)
    assert not missing, f"reachable Stage-3 asks with no Arabic: {missing}"


def test_latent_stage2_generic_asks_are_deliberately_absent():
    """D-RVR7-1 does NOT activate future-domain latent questions. The Stage-2
    generic variants are unreachable in both activated domains (every activated
    domain's artifact covers all three Stage-2 gaps), so including them would
    silently widen the authorized scope."""
    from web import ui_text
    from engine.path_n_questions import get_served_question
    for domain in DOMAIN_ARTIFACTS:
        for gap in STAGE2_GAPS:
            assert get_served_question(gap, 0, domain=domain) is not None, (domain, gap)
    leaked = [k for k in ui_text.RVR7_SUBSTANTIVE_AR
              if any(k.startswith(f"GENERIC:{g}:") for g in STAGE2_GAPS)]
    assert not leaked, f"latent Stage-2 asks leaked into RVR-7 scope: {leaked}"


def test_substantive_catalogue_is_exactly_the_authorized_scope():
    from web import ui_text
    from engine.progression_loop import QUESTIONS
    expected = {ui_text.RVR7_STALL_REFRAME, ui_text.RVR7_EXHAUSTED_EXIT_PROMPT,
                ui_text.RVR7_INTAKE_QUESTION, ui_text.RVR7_CLOSING_Q}
    for gap in STAGE3_GAPS:
        for index in range(len(QUESTIONS[gap])):
            expected.add(ui_text.rvr7_generic_identity(gap, index))
    assert set(ui_text.RVR7_SUBSTANTIVE_AR) == expected


def test_generated_output_surfaces_received_no_arabic_implementation():
    """Generated substantive output stays OUTSIDE RVR-7 (Owner decision). The
    Increment-3 next-development-step and the deliverable assembler must remain
    untouched by this increment."""
    for rel in ("engine/idea_development_outputs.py", "engine/deliverable_assembler.py"):
        raw = (REPO / rel).read_text(encoding="utf-8")
        assert not ARABIC.search(raw), f"{rel} acquired Arabic content"


# ---------------------------------------------------------------------------
# 4. Module discipline (mirrors the committed artifact module's own guard)
# ---------------------------------------------------------------------------

def test_this_module_has_no_web_framework_dependency():
    source = Path(__file__).read_text(encoding="utf-8")
    body = source.split("def test_this_module_has_no_web_framework_dependency", 1)[0]
    assert ("import " + "flask") not in body.lower()
    assert ("test_" + "client") not in body
