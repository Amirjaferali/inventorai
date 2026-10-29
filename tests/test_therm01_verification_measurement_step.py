"""THERM01-VERIFICATION-MEASUREMENT-STEP-01 — ONE verification-PREPARATION block on
the THERM-01 temperature-difference page.

Under the fixed disclosure of a SUCCESSFUL numerical ΔT result, and nowhere else, the
page shows "How to check this estimate": what a meaningful physical check would have
to establish. Points 1 to 4 and the assumption note restate class-level measurement
facts of NIST SP 400-86 (provenance electronics_electrical:PR028 / PR029); the
same-boundary / same-conditions condition and the comparison step (point 5) are
InventorAI-authored guidance, attributed as such. Verification preparation, not
validation: no input, no stored measurement, no comparison, no pass / fail, no
tolerance, no criterion, no instrument; the calculation, its artifacts, declarations,
screen, refusal order, eligibility and UNVALIDATED status are unchanged. Synthetic
data only.
"""
import hashlib
import html as _html
import json
import os
import re
import sqlite3
from pathlib import Path

import pytest

import web.app as webapp
from web import cap01_guidance, ui_text
from engine import therm01_temperature_difference as therm
from tests.cap01_heat_path_verification_addition import (
    HPV_CLAIM as CLAIM, HPV_CLAIMS as CLAIMS, HPV_GROUP as GROUP, HPV_NOTE as NOTE,
    HPV_RECORDS as RECORDS, HPV_SLUG as SLUG, HPV_STEM as STEM,
    without_heat_path_verification_addition)
from tests.test_cap12_form_mockup_advisory import _client_for, _start, SEED, ELEC_FORM
from tests.test_cap13_therm01_integrated_part_eligibility import ELEC, MECH, _integrated
from tests.test_therm01_temperature_difference import _form, _evaluate, URL, elec  # noqa: F401

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / "domains" / "electronics_electrical" / "domain.json"
PROVENANCE = ROOT / "domains" / "domain_provenance.json"
CONTRACT = ROOT / "docs" / "governance" / "STAGE27_THERM01_CONDUCTION_TEMPERATURE_DIFFERENCE_METHOD_CONTRACT.md"

# Canonical digests at base 98de1685f2a02d3cd3b263b03ed950d12ab5489f (before this slice).
_PRE_PACK_DIGEST = "e8f686d2d6c04d5f86cc4495c6123a21af18e06ac7dbc3625fdf83b65aa35625"
_PRE_PROVENANCE_DIGEST = "646329cb322a64261b5bcccb855ce6905dfa559d4002794c48b0f3e10ba3cb8b"
# The THERM-01 authority files this slice must leave byte-identical.
_THERM01_FILES = {
    "docs/governance/therm01_content_config/conduction_temperature_difference_single_path_v1.json":
        "c9e94f6999d166b0ce00b11eea4142f8b3a6c6e3c8afe1d77acafdf0828c1a08",
    # content version 12 after calc/units Corrections 10, 11 and 12 (DC-CONSTANT-CURRENT-CHARGE-01,
    # PWM-AVERAGE-VOLTAGE-01, MECHANICAL-NATURAL-FREQUENCY-01);
    # the THERM-01 method record and its unit records inside it are unchanged
    "docs/governance/deterministic_calculation_config/deterministic_calculation_owner_v1.json":
        "ef4b6ad68960f76107c919aad185c4ff12027c3b2a1511e59f5602fb75758401",
    "engine/therm01_conduction_method.py":
        "bff126a49c612b59104311185b19681974e9442f26179f98c6da66ff891acb4c",
    "engine/therm01_temperature_difference.py":
        "79d751e73189b4d22ac64de82b44927c0a4213278c65913d40b9db97023a8869",
}
KEYS = ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "ASSUMPTION", "BOUNDARY", "SOURCE")
BLOCK_RE = re.compile(r'<section class="box" data-therm01-verification="([^"]+)".*?</section>', re.S)
NIST_URL = "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication400-86.pdf"


def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _pack():
    return json.loads(PACK.read_text(encoding="utf-8"))


def _records():
    return json.loads(PROVENANCE.read_text(encoding="utf-8"))["records"]


def _visible(fragment):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def _block(page):
    found = BLOCK_RE.findall(page)
    assert len(found) <= 1, found
    m = BLOCK_RE.search(page)
    return m.group(0) if m else None


def _success(client, sid, **kw):
    r = client.post(URL % sid, data=_form(**kw))
    assert r.status_code == 200
    return r.get_data(as_text=True)


def _dump():
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return list(connection.iterdump())


# ---------------------------------------------------------------------------
# 1. the pure accessor
# ---------------------------------------------------------------------------

def test_a01_accessor_builds_the_one_prose_only_group_with_its_assumption_note():
    view = cap01_guidance.heat_path_verification_preparation()
    assert view is not None and view["group_id"] == GROUP and view["prose_only"] is True
    assert [c["claim_id"] for c in view["claims"]] == list(CLAIMS)
    assert view["title_key"] == STEM + "TITLE" and view["assumption_key"] == STEM + "ASSUMPTION"
    assert view["claims"][0]["text_key"] == STEM + "ITEM_1_TEXT"
    assert GROUP in cap01_guidance._FUNDAMENTALS_PROSE_ONLY_GROUPS


@pytest.mark.parametrize("missing", KEYS)
def test_a02_accessor_is_all_or_nothing_on_its_own_copy(monkeypatch, missing):
    real = ui_text.has_string
    monkeypatch.setattr(ui_text, "has_string", lambda key: False if key == STEM + missing else real(key))
    assert cap01_guidance.heat_path_verification_preparation() is None


def test_a03_accessor_reads_nothing_and_takes_no_input():
    import inspect
    assert inspect.signature(cap01_guidance.heat_path_verification_preparation).parameters == {}


# ---------------------------------------------------------------------------
# 2. visibility: a successful result only
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", ["en", "ar"])
def test_v01_success_page_shows_the_block_under_the_disclosure_with_its_full_copy(elec, lang):
    client, _aid, sid = elec
    if lang == "ar":
        assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    page = _success(client, sid)
    assert 'data-therm01-result="success"' in page
    block = _block(page)
    assert block is not None and SLUG in block
    assert page.index("data-therm01-disclosure") < page.index("data-therm01-verification")
    text = _visible(block)
    for key in KEYS:
        expected = ui_text.text(STEM + key, lang)
        for part in expected.split("\n\n"):
            # direction isolation wraps Latin runs in their own elements, which
            # the tag stripper turns into spaces: compare whitespace-free
            assert re.sub(r"\s+", "", _visible(_html.escape(part))) in re.sub(r"\s+", "", text), (key, part[:60])
    assert len(re.findall(r"<li>", block)) == 5
    assert "data-therm01-verify-assumption" in block and "data-therm01-verify-boundary" in block
    assert "<details data-therm01-verify-source>" in block
    other = "ar" if lang == "en" else "en"
    assert ui_text.text(STEM + "TITLE", other) not in page
    # the fixed disclosure and status are untouched by the block's presence
    assert page.count("data-therm01-disclosure") == 1
    assert "UNVALIDATED" in _visible(re.search(r'<p class="copy" data-therm01-status>.*?</p>', page, re.S).group(0))


def test_v02_the_block_carries_no_control_and_no_identifier():
    client, _aid, sid = elec_fixture()
    block = _block(_success(client, sid))
    for forbidden in ("<input", "<button", "<form", "<a ", "href=", "<select", "<textarea"):
        assert forbidden not in block
    for token in RECORDS + (GROUP, CLAIM, "PR028", "PR029"):
        assert token not in _visible(block)


def elec_fixture():
    c, aid = _client_for("therm01-verify@example.com")
    return c, aid, _start(c, ELEC_FORM)


def test_v03_a_plain_get_shows_no_block(elec):
    client, _aid, sid = elec
    page = client.get(URL % sid).get_data(as_text=True)
    assert "data-therm01-verification" not in page and ui_text.text(STEM + "TITLE", "en") not in page


@pytest.mark.parametrize("case", ["screen_yes", "declaration_not_applying", "invalid_number",
                                  "missing_value", "malformed"])
def test_v04_every_refusal_abstention_and_malformed_request_shows_no_block(elec, case):
    client, _aid, sid = elec
    if case == "screen_yes":
        data = _form(screen={"cryogenic": therm.SCREEN_YES})
    elif case == "declaration_not_applying":
        data = _form(decl={"single_path": therm.ANSWER_DOES_NOT_APPLY})
    elif case == "invalid_number":
        data = _form(P="abc")
    elif case == "missing_value":
        data = _form(P="")
    else:
        data = {"unrelated": "1"}
    r = client.post(URL % sid, data=data)
    page = r.get_data(as_text=True)
    assert r.status_code == (400 if case == "malformed" else 200)
    assert "data-therm01-result-value" not in page
    assert "data-therm01-verification" not in page
    assert ui_text.text(STEM + "TITLE", "en") not in page


def test_v05_an_ineligible_mechanical_root_shows_no_block_and_no_result():
    c, _aid = _client_for("therm01-verify-mech@example.com")
    sid = _start(c, {"idea": SEED, "domain_confirm": "mechanical"})
    page = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-therm01-result-value" not in page and "data-therm01-verification" not in page


@pytest.mark.parametrize("focus", [ELEC, MECH])
def test_v06_an_integrated_project_shows_the_block_for_its_declared_electronics_part(focus):
    c, _aid = _client_for("therm01-verify-%s@example.com" % focus)
    sid = _integrated(c, focus)
    page = _success(c, sid)
    assert 'data-therm01-result="success"' in page and _block(page) is not None


def test_v07_viewing_a_successful_result_writes_nothing(elec):
    client, _aid, sid = elec
    before = _dump()
    _success(client, sid)
    _success(client, sid)
    assert _dump() == before


# ---------------------------------------------------------------------------
# 3. wording: same boundaries, no validation by agreement
# ---------------------------------------------------------------------------

def test_w01_the_comparison_is_conditioned_on_the_same_boundaries_and_conditions():
    en_intro = ui_text.text(STEM + "INTRO", "en")
    en_steps = ui_text.text(STEM + "ITEM_1_TEXT", "en").split("\n\n")
    assert len(en_steps) == 5
    assert "same path" in en_intro and "thermal boundaries" in en_intro and "same operating conditions" in en_intro
    assert en_steps[4].startswith("Only when those boundaries and conditions correspond")
    assert "InventorAI's own" in en_steps[4]
    ar_intro = ui_text.text(STEM + "INTRO", "ar")
    ar_steps = ui_text.text(STEM + "ITEM_1_TEXT", "ar").split("\n\n")
    assert len(ar_steps) == 5 and ar_steps[4].startswith("وفقط عندما تتطابق تلك الحدود والظروف")
    assert "للمسار نفسه" in ar_intro and "حدوده الحرارية" in ar_intro and "ظروف التشغيل نفسها" in ar_intro


def test_w02_no_numerical_agreement_is_presented_as_validation_or_suitability():
    joined = " ".join(ui_text.text(STEM + key, "en") for key in KEYS).lower()
    for forbidden in ("is validated", "validates the", "confirms the model", "verified", "verifies",
                      "passes", "within tolerance", "acceptable", "is correct", "proves"):
        assert forbidden not in joined, forbidden
    assert "would not by itself validate the model" in joined
    assert "does not make the result above validated" in joined
    assert "stays unvalidated and not evidence" in joined
    ar = " ".join(ui_text.text(STEM + key, "ar") for key in KEYS)
    assert "ولا يعني توافق الرقمين وحده صحة النموذج" in ar
    assert "لا يجعل النتيجة أعلاه مُتحقَّقًا منها" in ar


def test_w03_the_boundary_excludes_every_verification_mechanism():
    boundary = ui_text.text(STEM + "BOUNDARY", "en").lower()
    for word in ("input", "stores no measurement", "compares nothing", "tolerance", "acceptance criterion",
                 "pass or fail", "uncertainty", "test duration", "safe limit", "rating or margin",
                 "measurement procedure", "instrument or sensor", "calibrate"):
        assert word in boundary, word


def test_w04_attribution_separates_nist_facts_from_inventorai_integration():
    source = ui_text.text(STEM + "SOURCE", "en")
    assert "points 1 to 4" in source and NIST_URL in source and "400-86" in source
    assert "semiconductor devices and packages" in source
    assert "InventorAI's own guidance, not statements of NIST" in source
    assert "not imply that NIST or the authors have reviewed or endorsed" in source
    ar = ui_text.text(STEM + "SOURCE", "ar")
    assert NIST_URL in ar and "النقاط 1 إلى 4" in ar and "وليسا من أقوال NIST" in ar
    assumption = ui_text.text(STEM + "ASSUMPTION", "en")
    assert "uniformly heated region" in assumption and "does not change with operating conditions" in assumption


def test_w05_every_key_exists_in_both_languages_and_differs():
    for key in KEYS:
        en, ar = ui_text.text(STEM + key, "en"), ui_text.text(STEM + key, "ar")
        assert en.strip() and ar.strip() and en != ar
        assert ui_text.has_string(STEM + key)


# ---------------------------------------------------------------------------
# 4. THERM-01 itself is unchanged
# ---------------------------------------------------------------------------

def test_u01_the_authority_files_of_the_calculation_are_byte_identical():
    for rel, expected in _THERM01_FILES.items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected, rel


@pytest.mark.parametrize("P,R,expected", [("10", "2.5", 25.0), ("3", "4", 12.0), ("0.5", "0.5", 0.25)])
def test_u02_the_numerical_result_is_the_plain_product_as_before(P, R, expected):
    evaluation = _evaluate(P=P, R_theta=R)
    assert evaluation["outcome"] == therm.OUTCOME_SUCCESS
    out = evaluation["result"]["outputs"]["delta_T"]
    assert out["value"] == expected and out["unit"] == "K"


def test_u03_declarations_screen_and_fields_are_the_governed_set():
    assert set(therm.DECLARATION_IDS) == {"steady_state", "single_path", "uniform_one_dimensional_flow",
                                          "constant_area", "constant_resistance", "total_resistance"}
    assert len(therm.DECLARATION_IDS) == 6
    assert len(therm.SCREEN_ITEMS) == 10 and len(therm.VALUE_ROLES) == 2


# ---------------------------------------------------------------------------
# 5. pack, provenance and placement
# ---------------------------------------------------------------------------

def test_p01_pack_minus_exactly_this_addition_equals_the_base_pack():
    pack = _pack()
    assert _digest(without_heat_path_verification_addition(pack)) == _PRE_PACK_DIGEST
    groups = [g for g in pack["reference_fundamentals"] if g["group_id"] == GROUP]
    assert len(groups) == 1 and groups[0]["applicable_gap_type"] == "PHYSICAL_FEASIBILITY"
    (claim,) = groups[0]["claims"]
    assert claim["claim_id"] == CLAIM
    assert (claim["source_ref"], claim["source_use_policy_ref"]) == RECORDS
    for phrase in ("where the heat is generated", "one stated, fixed location", "calibrated over the temperature range",
                   "spatially uniform heated region", "independent of operating conditions", "NIST SP 400-86",
                   "semiconductor devices and packages", "states no numeric criterion"):
        assert phrase in claim["fact"], phrase
    for phrase in ("Verification-PREPARATION only", "ONLY consumer is the THERM-01", "SUCCESSFUL numerical ΔT",
                   "InventorAI-authored integration guidance, NOT claims of NIST", "No measured-value input",
                   "never treated as validation", "stays UNVALIDATED", "unchanged"):
        assert phrase in claim["limitation"], phrase
    note = pack["_governance_notes"][NOTE]
    for phrase in ("THERM01-VERIFICATION-MEASUREMENT-STEP-01", "PR028", "PR029", "NOT executor-performed",
                   "ONLY consumer is the THERM-01", "NOT a CAP-09 group", "InventorAI-authored",
                   "PR001–PR027 are unchanged"):
        assert phrase in note, phrase


def test_p02_two_records_appended_after_pr027_and_every_other_record_unchanged():
    records = _records()
    ids = [r["record_id"] for r in records]
    i = ids.index("electronics_electrical:PR027")
    assert tuple(ids[i + 1:i + 3]) == RECORDS and ids[i + 3] == "mechanical:PR001"
    assert _digest([r for r in records if r["record_id"] not in RECORDS]) == _PRE_PROVENANCE_DIGEST


def test_p03_the_source_record_keeps_identity_location_context_and_exclusions():
    (record,) = [r for r in _records() if r["record_id"] == RECORDS[0]]
    assert record["url"] == NIST_URL and record["standard_number"] == "NIST SP 400-86"
    assert "Oettinger" in record["source_name"] and "Blackburn" in record["source_name"]
    for phrase in ("printed page 2", "pages 65–66", "PDF page 10", "PDF pages 73–74", "SRC-011", "run 4",
                   "NOT executor-performed", "HTTP 403", "semiconductor devices and packages",
                   "CLAIM MAPPING", "INVENTORAI-AUTHORED INTEGRATION (NOT a NIST claim)",
                   "third-party literature cited inside the publication is not relied on",
                   "no figure, table, numeric value, threshold or criterion"):
        assert phrase in record["version_or_edition"] + record["notes"], phrase
    assert record["cross_domain_usage"] == []


def test_p04_the_rights_record_is_claim_specific_and_broadens_no_earlier_record():
    (record,) = [r for r in _records() if r["record_id"] == RECORDS[1]]
    assert record["source_type"] == "source_use_policy"
    for phrase in ("not a legal opinion or legal determination", "electronics_electrical:PR028", "ONLY",
                   "17 U.S.C. § 105", "RESIDUAL UNCERTAINTY", "passage-level",
                   "PR007, PR011, PR015, PR023 and PR025 are NOT broadened", "attributed to InventorAI, never to NIST"):
        assert phrase in record["notes"], phrase


def test_p05_not_a_report_group_not_a_cap09_group_and_not_an_extension_row(elec):
    rows = [row for rows in cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS.values() for row in rows]
    assert all(row[0] != GROUP for row in rows)
    assert all(GROUP not in str(v) for v in cap01_guidance.CAP01_GAP_FUNDAMENTALS.values())
    assert GROUP not in cap01_guidance.CAP09_MEASUREMENT_REFERENCE_GROUPS
    client, _aid, sid = elec
    planning = client.get("/session/%s/success-criteria" % sid).get_data(as_text=True)
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    for page in (planning, report):
        assert SLUG not in page and ui_text.text(STEM + "TITLE", "en") not in page


def test_p06_the_contract_amendment_is_recorded_without_touching_the_method():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "## 9B. Verification-preparation block (amendment `THERM01-VERIFICATION-MEASUREMENT-STEP-01`" in text
    assert "`THERM01-VERIFICATION-MEASUREMENT-STEP-01 — OWNER-AUTHORIZED AMENDMENT`" in text
    assert "Inspection C (research stream, 2026-10-27" in text
    assert text.count("## 3. Method definition and derivation") == 1
    assert "ΔT = P × Rθ, the method\nidentity and version, declarations D-1 to D-6" in text
