"""v1.32 derived-navigation truth guards — live-truth reversal proofs, second half.

Split out of tests/test_v132_derived_navigation_truth_live_truth_reversals.py unchanged, for CI shard balance only
(scripts/ci_full_suite.py places whole files): the reversal cases after the first half (by sorted name) of
`_MATERIAL_REVERSALS`, under the same test name and body. `_read` is read and patched on the original module (`_nav`)
so the current-state guard sees the mutated documents exactly as before the split.
"""

import pytest

import test_v132_derived_navigation_truth as _nav
from test_v132_derived_navigation_truth import _live_authority_problems, _mutate
from test_v132_derived_navigation_truth_live_truth_reversals import _FIRST_HALF, _MATERIAL_REVERSALS


@pytest.mark.parametrize("name", sorted(_MATERIAL_REVERSALS)[_FIRST_HALF:])
def test_every_material_reversal_is_caught(monkeypatch, name):
    path, region, old, new, *every = _MATERIAL_REVERSALS[name]
    real = _nav._read
    docs = _mutate(path, region, old, new, *every)
    fake = lambda p: docs[p] if p in docs else real(p)                   # noqa: E731
    assert _live_authority_problems(fake), name
    monkeypatch.setattr(_nav, "_read", fake)
    with pytest.raises(AssertionError):
        _nav.test_stage22_closure_is_delivered_and_stage22_is_complete_on_every_live_surface()
