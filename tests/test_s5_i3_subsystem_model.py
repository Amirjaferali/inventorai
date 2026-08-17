"""
tests/test_s5_i3_subsystem_model.py

§5-I3 — Subsystem + cross-domain project model foundation, governed by §5-C1
(D-S5-04: project stays generic, root confirmed_domain preserved, multi-domain at
the SUBSYSTEM grain; D-S5-05: minimum subsystem model) and consuming the §5-I2
activation policy.

Foundation only, additive and in-memory (no persistence/web/domain-pack change).
RED (base 04a9c4d): `engine.subsystem_model` does not exist and `IdeaState` carries
no subsystem foundation, so the cross-domain/subsystem semantics cannot be
represented. GREEN: one project may carry zero or more subsystems, each optionally
referencing a canonical domain — a reference is metadata only (never activates a
domain, never changes the root domain), and its support state resolves via §5-I2.
"""

import dataclasses
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.idea_state import IdeaState
from engine.domain_registry import load_registry
from engine import domain_activation as da
from engine import subsystem_model as sm


def _reg():
    return load_registry(os.path.join(os.path.dirname(__file__), "..", "domains"))


def _electronics_project():
    state = IdeaState(idea_id="p1")
    state.domain = "electronics_electrical"          # dynamic root domain (as web sets it)
    state.domain_signal = "electronics_electrical"
    return state


# --- Backward compatibility: absence of subsystem data preserves behavior ----

class TestBackwardCompatibility:
    def test_default_project_has_empty_subsystems(self):
        state = IdeaState(idea_id="p")
        assert sm.project_subsystems(state) == []

    def test_asdict_still_works(self):
        state = _electronics_project()
        dataclasses.asdict(state)  # must not raise

    def test_absent_subsystems_preserve_single_domain_behavior(self):
        state = _electronics_project()
        assert sm.project_subsystems(state) == []
        assert state.domain == "electronics_electrical"


# --- Root domain is preserved; subsystems are a separate grain ---------------

class TestRootDomainPreserved:
    def test_adding_subsystem_does_not_change_root_domain(self):
        state = _electronics_project()
        sm.add_subsystem(state, "sub-a", domain="mechanical")
        assert state.domain == "electronics_electrical"          # unchanged
        assert state.domain_signal == "electronics_electrical"

    def test_project_has_no_peer_root_domains_list(self):
        # D-S5-04: no `domains = [...]` peer-root list; the scalar stays scalar.
        state = _electronics_project()
        sm.add_subsystem(state, "sub-a", domain="mechanical")
        sm.add_subsystem(state, "sub-b", domain="software")
        assert isinstance(state.domain, str)
        assert not isinstance(state.domain, (list, tuple, set))

    def test_multiple_subsystem_domains_do_not_become_root(self):
        state = _electronics_project()
        sm.add_subsystem(state, "a", domain="mechanical")
        sm.add_subsystem(state, "b", domain="software")
        assert sm.subsystem_domains(state) == ["mechanical", "software"]
        assert state.domain == "electronics_electrical"


# --- Subsystem domain reference is metadata, never activation ----------------

class TestSubsystemReferenceIsNotActivation:
    def test_mechanical_subsystem_now_activated(self):
        # Mechanical Activation Execution Gate: mechanical is now really
        # activated in production. test_software_subsystem_not_activated below
        # covers the still-not-activated case generically.
        state = _electronics_project()
        sub = sm.add_subsystem(state, "a", domain="mechanical")
        assert sm.subsystem_support_state(sub, _reg()) == da.ACTIVATED
        assert sm.is_subsystem_domain_activated(sub, _reg()) is True

    def test_software_subsystem_not_activated(self):
        state = _electronics_project()
        sub = sm.add_subsystem(state, "a", domain="software")
        assert sm.subsystem_support_state(sub, _reg()) == da.RECOGNIZED_NOT_ACTIVATED
        assert sm.is_subsystem_domain_activated(sub, _reg()) is False

    def test_unknown_subsystem_domain_unsupported(self):
        state = _electronics_project()
        sub = sm.add_subsystem(state, "a", domain="banana")
        assert sm.subsystem_support_state(sub, _reg()) == da.UNKNOWN_OR_UNSUPPORTED
        assert sm.is_subsystem_domain_activated(sub, _reg()) is False

    def test_unknown_subsystem_domain_never_becomes_electronics(self):
        state = _electronics_project()
        sub = sm.add_subsystem(state, "a", domain="banana")
        assert sm.subsystem_support_state(sub, _reg()) != da.ACTIVATED
        assert state.domain == "electronics_electrical"

    def test_electronics_subsystem_reference_reports_activated(self):
        # Referencing the already-activated domain reports ACTIVATED (the reference
        # reports the domain's state; it does not itself grant activation).
        state = _electronics_project()
        sub = sm.add_subsystem(state, "a", domain="electronics_electrical")
        assert sm.subsystem_support_state(sub, _reg()) == da.ACTIVATED

    def test_subsystem_without_domain_reference_is_unsupported(self):
        state = _electronics_project()
        sub = sm.add_subsystem(state, "a")  # no domain reference
        assert sm.subsystem_support_state(sub, _reg()) == da.UNKNOWN_OR_UNSUPPORTED


# --- Cross-domain composition at the subsystem grain -------------------------

class TestCrossDomainComposition:
    def test_electronics_root_with_mixed_subsystem_domains(self):
        state = _electronics_project()
        sm.add_subsystem(state, "a", domain="electronics_electrical")
        sm.add_subsystem(state, "b", domain="mechanical")
        sm.add_subsystem(state, "c", domain="software")
        subs = sm.project_subsystems(state)
        assert len(subs) == 3
        states = [sm.subsystem_support_state(s, _reg()) for s in subs]
        # Mechanical Activation Execution Gate: mechanical is now activated.
        assert states == [da.ACTIVATED, da.ACTIVATED, da.RECOGNIZED_NOT_ACTIVATED]
        activated = [s for s in subs if sm.is_subsystem_domain_activated(s, _reg())]
        assert [s.domain for s in activated] == ["electronics_electrical", "mechanical"]

    def test_empty_subsystem_collection(self):
        state = _electronics_project()
        assert sm.subsystem_domains(state) == []


# --- Subsystem descriptor contract (minimum) ---------------------------------

class TestSubsystemDescriptor:
    def test_subsystem_has_id_and_optional_domain(self):
        sub = sm.Subsystem(subsystem_id="s1", domain="mechanical")
        assert sub.subsystem_id == "s1"
        assert sub.domain == "mechanical"

    def test_subsystem_domain_defaults_to_none(self):
        sub = sm.Subsystem(subsystem_id="s1")
        assert sub.domain is None
