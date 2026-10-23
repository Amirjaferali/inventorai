"""Focused BMG guards for the request-local IDEA-TO-ENGINEERING-CONFIG-01."""
from dataclasses import FrozenInstanceError

from engine.cap13_functional_configuration import derive_provisional_fit, CANDIDATE


def test_arabic_original_idea_produces_sizing_envelope_not_design():
    idea = 'أريد رفع جسم صغير 3 سم فوق مكتبي وأبعاده 18 × 12 سم'
    result = derive_provisional_fit(idea)
    assert result is not None
    assert result.status == CANDIDATE
    assert (result.top_length, result.top_depth, result.size_unit) == ('18', '12', 'سم')
    assert (result.surface_lift, result.lift_unit) == ('3', 'سم')
    assert result.engineering_status == 'NOT_ASSESSED'
    assert result.source_excerpt == idea
    assert result.size_span == '18 × 12 سم'
    assert result.rise_span == 'رفع جسم صغير 3 سم'
    try:
        result.top_length = '1000'
        assert False, 'mutable candidate'
    except FrozenInstanceError:
        pass


def test_english_case_and_geometrical_change():
    a = derive_provisional_fit('I want to raise a small object 3 cm above my desk; dimensions 18 x 12 cm')
    b = derive_provisional_fit('I want to raise a wider object 3 cm above my desk; dimensions 28 x 16 cm')
    assert a and b
    assert (a.top_length, a.top_depth) == ('18', '12')
    assert (b.top_length, b.top_depth) == ('28', '16')
    assert a.source_digest != b.source_digest
    assert a.surface_lift == b.surface_lift == '3'


def test_arabic_digits_are_a_precise_representation_not_guessed():
    r = derive_provisional_fit('أريد رفع كتاب ٣ سم فوق طاولة وأبعاده ١٨ × ١٢ سم')
    assert r and (r.top_length, r.top_depth, r.surface_lift) == ('18', '12', '3')


def test_out_of_family_and_negated_intents_never_generate_candidate():
    for idea in (
        'Make a step people stand on it, raise 3 cm over a desk, dimensions 18 x 12 cm',
        "I don't want to lift this 3 cm on my desk, dimensions 18 x 12 cm",
        'لا أريد رفع صندوق 3 سم على المكتب أبعاده 18 × 12 سم',
        'I want to raise a person 3 cm on a desk, dimensions 18 x 12 cm',
        'I want to raise an object 3 cm on a wall; dimensions 18 x 12 cm',
    ):
        assert derive_provisional_fit(idea) is None


_AR_TAIL = ' فوق مكتبي وأبعاده 18 × 12 سم'


def test_negated_arabic_lift_requests_never_generate_candidate():
    # PR #848 review defect: «أن» between «لا أريد» and the verb escaped the
    # earlier negation pattern and produced a positive candidate.
    assert derive_provisional_fit('لا أريد أن أرفع جسما 3 سم فوق مكتبي وأبعاده 18 × 12 سم') is None
    for head in (
        'لا اريد ان ارفع جسما 3 سم',
        'لا أرغب في رفع جسم 3 سم',
        'لن أرفع جسما 3 سم',
        'لم أعد أريد أن أرفع جسما 3 سم',
        'ولا أريد أن أرفع جسما 3 سم',
        'أنا لا أريد أن أرفع جسما 3 سم',
        'ما أريد أن أرفع جسما 3 سم',
        'مش عايز أرفع جسم 3 سم',
        'لا يجب أن يرفع جسما 3 سم',
        'ليس المطلوب أن أرفع جسما 3 سم',
        'أريد أن أرفع جسما لا يزيد عن 3 سم',
        'لا أريد أن أرفع جسما ٣ سم',
    ):
        assert derive_provisional_fit(head + _AR_TAIL) is None, head


def test_negated_english_lift_requests_never_generate_candidate():
    for head in ("I don't need to raise a box 3 cm", "I won't raise a box 3 cm",
                 'I do not want to lift a box 3 cm', 'I cannot lift a box 3 cm'):
        assert derive_provisional_fit(
            head + ' above my desk; dimensions 18 x 12 cm') is None, head


def test_positive_arabic_forms_and_negation_in_another_sentence_still_match():
    for head in ('أريد أن أرفع جسما 3 سم', 'اريد ان ارفع جسما 3 سم',
                 'لا أريد أدوات. أريد أن أرفع جسما 3 سم'):
        result = derive_provisional_fit(head + _AR_TAIL)
        assert result is not None and result.surface_lift == '3', head
        assert (result.top_length, result.top_depth) == ('18', '12')


def test_missing_multiple_or_non_numeric_fields_fail_closed():
    cases = (
        'Raise an object above desk, dimensions 18 x 12 cm',
        'Raise 3 cm above desk, dimensions unknown',
        'Raise 3 cm above desk, dimensions 18 x 12 cm or 28 x 16 cm',
        'Raise 3 cm then raise 4 cm on desk, dimensions 18 x 12 cm',
        'Raise 0 cm above desk, dimensions 18 x 12 cm',
        'Raise 3 cm above desk, dimensions 0 x 12 cm',
        'Raise 3 cm above desk, dimensions 18 x 0 cm',
        'Raise 3 cm above desk, dimensions 999999 x 12 cm',
    )
    for item in cases:
        assert derive_provisional_fit(item) is None


def test_request_local_inert_pure_and_no_engineering_claim():
    idea = 'I want to lift a box 4 mm above a table, dimensions 210 x 180 mm'
    before = idea
    a = derive_provisional_fit(idea)
    b = derive_provisional_fit(idea)
    assert a == b and idea == before
    assert a.engineering_status == 'NOT_ASSESSED'
    assert a.top_length == '210' and a.top_depth == '180'
    assert a.fit_rule == 'TOP_PLAN_AT_LEAST_OBJECT_DIMENSIONS_NO_OVERHANG_CANDIDATE'
    assert derive_provisional_fit('') is None
    assert derive_provisional_fit(42) is None
