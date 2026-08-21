"""PVCG-R2-I — single-marker coverage for the gap-relevance tables.

File path        : tests/test_pvcg_r2i_marker_coverage.py
Purpose          : close the mutation-adequacy gap found by independent review of
                   the rejected candidate `2f2897ce…`. Every operative entry in
                   `engine.gap_relevance` that can independently produce an
                   `addresses_gap(...) is True` decision gets a focused probe
                   whose eligibility DEPENDS on that entry, so removing the entry
                   makes a test fail.
Governing        : docs/governance/PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md
                   (AUTHORITATIVE, PR #548) §4, §6, §9.
Input contract   : the public predicate `engine.gap_relevance.addresses_gap` and
                   the declared marker tables, read ONLY to enumerate what must
                   be covered. No Flask, no database, no network, no filesystem.
Output contract  : one parameterized positive probe per independently operative
                   entry; cross-family exclusivity for the same probes; a
                   structural non-operativity proof for every excluded entry;
                   and structural guards on the tables themselves.
Prohibited       : asserting on line numbers or on any implementation detail
                   other than the declared marker tables; probes that are not
                   isolated (a probe containing a second same-family entry would
                   let a marker-removal mutant survive — that is exactly the
                   defect being repaired, so generation FAILS AT COLLECTION when
                   isolation cannot be established).

WHY THIS FILE EXISTS — the withdrawn claim
------------------------------------------
The rejected candidate reported two surviving supplementary mutants as
"EQUIVALENT MUTANTS" on the basis that they produced no verdict change across a
10-answer x 6-gap corpus. **That inference was unsound and is withdrawn.** A
finite corpus cannot establish equivalence over the input space. Independent
review demonstrated real live-seam behaviour changes from single-marker removals
that the previous suite did not detect. Equivalence is now claimed ONLY where it
is proven structurally over all inputs (see `SHADOWED_ENTRIES`), never by corpus
sampling.
"""

import re

import pytest

from engine.gap_relevance import (
    GOVERNED_GAP_TYPES, addresses_gap, _INTENT_WORDS, _INTENT_PHRASES,
)

#: DECLARED MARKER INVENTORY — the behavioural contract this file pins.
#: Probes are generated from THIS declaration, never from the live tables, so
#: deleting a marker from `engine.gap_relevance` leaves its probe in place and
#: the probe fails. Regenerating this literal from the live tables would defeat
#: the guard; it must only be edited deliberately, alongside a governed change.
DECLARED_WORDS = {
    "ASSUMPTION_INVENTORY": (
        "assume", "assumed", "assumes", "assuming", "assumption",
        "assumptions", "believe", "believed", "expect", "expected", "expects",
        "granted", "hypotheses", "hypothesis", "presume", "presumed",
        "presumes", "unconfirmed", "unproven", "untested", "unverified",
    ),
    "BOUNDARY_AMBIGUITY": (
        "alternative", "alternatives", "beyond", "boundaries", "boundary",
        "compared", "comparison", "competitor", "competitors", "core",
        "differ", "difference", "differences", "different", "differs",
        "distinct", "distinguishes", "essential", "exclude", "excluded",
        "excludes", "excluding", "existing", "irreplaceable", "limitation",
        "limitations", "outside", "prior", "replace", "replaceable",
        "replaced", "replacing", "restricted", "restricts", "scope",
        "uncovered", "unlike", "versus", "vs", "whereas",
    ),
    "EXPERTISE_GAP_AWARENESS": (
        "background", "competence", "competency", "consult", "consultant",
        "discipline", "disciplines", "engineer", "engineering", "engineers",
        "experience", "experienced", "expert", "expertise", "experts",
        "familiar", "hire", "knowledge", "learn", "learning", "mentor",
        "professional", "qualified", "skill", "skills", "specialist",
        "specialists", "trained", "training", "unfamiliar",
    ),
    "MECHANISM_COMPLETENESS": (
        "activate", "activates", "actuate", "actuates", "amplifies",
        "amplify", "close", "closes", "compare", "compares", "component",
        "components", "compute", "computes", "connect", "connects", "convert",
        "converts", "detect", "detects", "disconnect", "disconnects", "drive",
        "drives", "filters", "latch", "latches", "measure", "measures",
        "module", "modules", "move", "moves", "open", "opens", "part",
        "parts", "procedure", "process", "receive", "receives", "rotate",
        "rotates", "send", "sends", "sense", "senses", "sequence", "stage",
        "stages", "step", "steps", "subsystem", "subsystems", "switch",
        "switches", "transmit", "transmits", "trigger", "triggers",
    ),
    "PHYSICAL_FEASIBILITY": (
        "amp", "ampere", "amperes", "amps", "batteries", "battery",
        "capacitive", "capacity", "constraint", "constraints", "consume",
        "consumes", "consumption", "draw", "draws", "efficiency", "energy",
        "feasibility", "feasible", "frequency", "heat", "hz", "inductive",
        "joule", "joules", "khz", "magnetic", "material", "materials", "mhz",
        "milliamp", "milliamps", "milliwatt", "milliwatts", "optical",
        "physics", "principle", "principles", "rated", "rating", "resistive",
        "supply", "temperature", "thermal", "tolerance", "tolerances", "watt",
        "watts", "withstand",
    ),
    "PROBLEM_MECHANISM_FIT": (
        "addresses", "condition", "conditions", "customer", "customers",
        "issue", "issues", "matters", "pain", "people", "person", "problem",
        "problems", "scenario", "scenarios", "situation", "situations",
        "solve", "solved", "solves", "solving", "struggle", "struggles",
        "suffer", "suffers", "suitable", "suited", "unsuitable", "user",
        "users",
    ),
}

DECLARED_PHRASES = {
    "ASSUMPTION_INVENTORY": (
        "take for granted", "taking for granted", "taken for granted",
        "turned out to be wrong",
    ),
    "BOUNDARY_AMBIGUITY": (
        "does not", "doesn't", "not cover", "not intended", "as opposed to",
        "cannot be replaced",
    ),
    "EXPERTISE_GAP_AWARENESS": (
        "bring in", "need help", "would need to learn", "do not know how",
        "don't know how", "someone else",
    ),
    "MECHANISM_COMPLETENESS": (
        "how it works", "works by", "in order to", "step by step",
    ),
    "PHYSICAL_FEASIBILITY": (
        "power requirement", "power requirements", "power consumption",
        "power source", "temperature range", "operating range",
        "physical limit", "physical limits", "operating limit",
    ),
    "PROBLEM_MECHANISM_FIT": (
        "rather than", "instead of", "right fit", "less well",
        "would not solve",
    ),
}


# A neutral carrier sentence that contains NO marker of ANY governed family.
# Verified at generation time and again by an explicit test.
CARRIER = "the inventor wrote one short line about the widget"

_WORD_RE = re.compile(r"[a-z0-9]+")


def _family_hits(text, gap_type):
    """Every declared entry of `gap_type` present in `text`."""
    lowered = text.lower()
    tokens = set(_WORD_RE.findall(lowered))
    hits = {p for p in DECLARED_PHRASES.get(gap_type, ()) if p in lowered}
    hits |= {w for w in DECLARED_WORDS[gap_type] if w in tokens}
    return hits


def _all_entries():
    """(gap_type, entry, kind) for every DECLARED entry, in a stable order.

    Sourced from DECLARED_WORDS / DECLARED_PHRASES — deliberately NOT from the
    live tables, so a marker deleted from the implementation still has a probe
    and that probe fails.
    """
    for gap_type in sorted(DECLARED_WORDS):
        for word in DECLARED_WORDS[gap_type]:
            yield gap_type, word, "word"
        for phrase in DECLARED_PHRASES.get(gap_type, ()):
            yield gap_type, phrase, "phrase"


def _necessary_companion(entry, gap_type):
    """Return a same-family entry that EVERY text containing `entry` must also
    contain, or None. This is a structural fact about the entries themselves —
    it holds for all inputs, not for a sampled corpus."""
    tokens = set(_WORD_RE.findall(entry))
    for other in DECLARED_WORDS[gap_type]:
        if other != entry and other in tokens:
            return other
    for other in DECLARED_PHRASES.get(gap_type, ()):
        if other != entry and other in entry:
            return other
    return None


def _build_probes():
    """Generate one isolated probe per entry.

    Raises at import (collection failure) if a probe cannot be isolated for a
    reason other than a proven structural companion — an unisolated probe is
    false coverage and must never be silently accepted.
    """
    operative, shadowed = [], []
    for gap_type, entry, kind in _all_entries():
        probe = f"{CARRIER} {entry}."
        own = _family_hits(probe, gap_type)
        foreign = {
            other: _family_hits(probe, other)
            for other in GOVERNED_GAP_TYPES if other != gap_type
        }
        foreign = {k: v for k, v in foreign.items() if v}
        if foreign:
            raise AssertionError(
                "probe generation failed: the isolated probe for "
                f"{gap_type}/{entry!r} also carries markers of another family: "
                f"{foreign}. Fix the carrier or the marker tables — an "
                "unisolated probe would let a marker-removal mutant survive."
            )
        if own == {entry}:
            operative.append((gap_type, entry, kind, probe))
            continue
        companion = _necessary_companion(entry, gap_type)
        if companion is None or own != {entry, companion}:
            raise AssertionError(
                "probe generation failed: the probe for "
                f"{gap_type}/{entry!r} carries same-family markers {sorted(own)} "
                "with no single structural companion explaining it. It cannot "
                "be used as isolated coverage."
            )
        shadowed.append((gap_type, entry, kind, companion))
    return operative, shadowed


#: Entries that CAN independently decide eligibility — each needs a probe.
OPERATIVE_PROBES, SHADOWED_ENTRIES = _build_probes()

#: Bare domain vocabulary. PVCG-R2-C §4 declares these insufficient on their own,
#: so none of them may ever make an answer eligible for any gap.
GENERIC_TECHNICAL_NOUNS = (
    "sensor", "relay", "capacitor", "resistor", "transistor", "microcontroller",
    "voltage", "current", "signal", "circuit", "board", "chip", "led", "motor",
    "battery", "wire", "diode", "inductor", "enclosure", "device",
)

#: Bare causal connectives — likewise insufficient on their own (§4).
BARE_CAUSAL_CONNECTIVES = (
    "because", "therefore", "since", "thus", "hence", "so", "as a result",
)


def _ids(rows):
    return [f"{gap}-{kind}-{entry.replace(' ', '_')}" for gap, entry, kind, *_ in rows]


# ---------------------------------------------------------------------------
# The carrier and the generator itself must be trustworthy.
# ---------------------------------------------------------------------------
class TestProbeArchitecture:

    def test_carrier_contains_no_marker_of_any_family(self):
        for gap_type in GOVERNED_GAP_TYPES:
            assert _family_hits(CARRIER, gap_type) == set(), (
                f"carrier is contaminated for {gap_type}"
            )

    def test_carrier_is_not_eligible_for_any_gap(self):
        for gap_type in GOVERNED_GAP_TYPES:
            assert addresses_gap(CARRIER, gap_type) is False

    def test_isolation_validator_rejects_a_contaminated_probe(self):
        """Self-test: a probe carrying a second same-family marker must be
        detected. Without this, the coverage claim itself is unverified — and a
        hand-written probe silently carrying a second marker is precisely how
        the rejected candidate's coverage gap went unnoticed."""
        gap = "MECHANISM_COMPLETENESS"
        two = sorted(DECLARED_WORDS[gap])[:2]
        contaminated = f"{CARRIER} {two[0]} {two[1]}."
        assert _family_hits(contaminated, gap) == set(two)
        assert len(_family_hits(contaminated, gap)) > 1

    def test_every_declared_entry_is_classified_exactly_once(self):
        declared = [(g, e) for g, e, _ in _all_entries()]
        classified = ([(g, e) for g, e, _, _ in OPERATIVE_PROBES]
                      + [(g, e) for g, e, _, _ in SHADOWED_ENTRIES])
        assert sorted(declared) == sorted(classified)
        assert len(declared) == len(set(declared)), "duplicate entry declared"

    def test_live_tables_match_the_declared_inventory_exactly(self):
        """Fails on ANY marker removal, addition, or migration between
        families — including entries whose probes could not otherwise
        distinguish the change."""
        live_words = {g: tuple(sorted(_INTENT_WORDS[g])) for g in _INTENT_WORDS}
        declared_words = {g: tuple(sorted(v)) for g, v in DECLARED_WORDS.items()}
        assert live_words == declared_words
        live_phrases = {g: tuple(_INTENT_PHRASES.get(g, ()))
                        for g in _INTENT_WORDS}
        declared_phrases = {g: tuple(DECLARED_PHRASES.get(g, ()))
                            for g in DECLARED_WORDS}
        assert live_phrases == declared_phrases

    def test_declared_inventory_is_not_silently_empty(self):
        assert sum(len(v) for v in DECLARED_WORDS.values()) >= 200
        assert sum(len(v) for v in DECLARED_PHRASES.values()) >= 30

    def test_marker_tables_have_no_cross_family_duplicates(self):
        """A marker owned by two families would make cross-family exclusivity
        untestable and would blur which question an answer addresses."""
        seen = {}
        for gap_type, entry, _ in _all_entries():
            assert entry not in seen, (
                f"{entry!r} is declared by both {seen.get(entry)} and {gap_type}"
            )
            seen[entry] = gap_type

    def test_no_governed_gap_family_is_empty(self):
        for gap_type in GOVERNED_GAP_TYPES:
            assert _INTENT_WORDS[gap_type], f"{gap_type} word family is empty"
        assert set(GOVERNED_GAP_TYPES) == set(_INTENT_WORDS)


# ---------------------------------------------------------------------------
# Positive coverage: one isolated probe per independently operative entry.
# Removing that entry makes exactly this probe stop being eligible.
# ---------------------------------------------------------------------------
class TestSingleMarkerCoverage:

    @pytest.mark.parametrize("gap_type,entry,kind,probe", OPERATIVE_PROBES,
                             ids=_ids(OPERATIVE_PROBES))
    def test_entry_alone_makes_the_probe_eligible(self, gap_type, entry, kind,
                                                  probe):
        assert addresses_gap(probe, gap_type) is True, (
            f"{gap_type} {kind} {entry!r} does not carry its own probe"
        )

    @pytest.mark.parametrize("gap_type,entry,kind,probe", OPERATIVE_PROBES,
                             ids=_ids(OPERATIVE_PROBES))
    def test_entry_probe_is_not_eligible_for_any_other_gap(self, gap_type, entry,
                                                           kind, probe):
        """Catches a marker migrating to the wrong governed family."""
        for other in GOVERNED_GAP_TYPES:
            if other == gap_type:
                continue
            assert addresses_gap(probe, other) is False, (
                f"{gap_type} {kind} {entry!r} also satisfies {other}"
            )


# ---------------------------------------------------------------------------
# Excluded entries: equivalence proven structurally, never by corpus sampling.
# ---------------------------------------------------------------------------
class TestStructurallyNonOperativeEntries:

    @pytest.mark.parametrize("gap_type,entry,kind,companion", SHADOWED_ENTRIES,
                             ids=_ids(SHADOWED_ENTRIES))
    def test_entry_can_never_decide_eligibility_alone(self, gap_type, entry,
                                                      kind, companion):
        """`companion` is contained in `entry` itself, so EVERY text containing
        `entry` contains `companion` too. Removing `entry` therefore cannot
        change any verdict for any input. This is a proof over the whole input
        space — not the corpus inference that was withdrawn."""
        assert companion != entry
        in_tokens = companion in set(_WORD_RE.findall(entry))
        in_text = companion in entry
        assert in_tokens or in_text, (
            f"{entry!r} does not structurally contain {companion!r}"
        )
        assert companion in _family_hits(f"{CARRIER} {entry}.", gap_type)
        assert addresses_gap(f"{CARRIER} {entry}.", gap_type) is True


# ---------------------------------------------------------------------------
# Negative guards: what must NEVER become a relevance marker.
# ---------------------------------------------------------------------------
class TestForbiddenUniversalMarkers:

    @pytest.mark.parametrize("noun", GENERIC_TECHNICAL_NOUNS)
    def test_domain_noun_is_never_a_universal_relevance_marker(self, noun):
        """A domain noun may be eligible ONLY for a family that explicitly
        declares it, and never for more than one.

        `battery` is such a case and it is legitimate: the PHYSICAL_FEASIBILITY
        question asks for "the approximate power requirement and source", so
        naming a power source addresses that question and no other. What §4
        forbids is domain vocabulary acting as a UNIVERSAL relevance signal —
        which is exactly what this test pins.
        """
        probe = f"{CARRIER} {noun}."
        eligible = {g for g in GOVERNED_GAP_TYPES if addresses_gap(probe, g)}
        declaring = {g for g in GOVERNED_GAP_TYPES if noun in DECLARED_WORDS[g]}
        assert eligible == declaring, (
            f"domain noun {noun!r} is eligible for {sorted(eligible)} but is "
            f"declared by {sorted(declaring)}"
        )
        assert len(eligible) <= 1, (
            f"domain noun {noun!r} is eligible for more than one gap family — "
            "PVCG-R2-C §4 forbids domain vocabulary as a universal signal"
        )

    def test_the_vast_majority_of_domain_nouns_are_eligible_for_nothing(self):
        undeclared = [n for n in GENERIC_TECHNICAL_NOUNS
                      if not any(n in DECLARED_WORDS[g] for g in GOVERNED_GAP_TYPES)]
        assert len(undeclared) >= len(GENERIC_TECHNICAL_NOUNS) - 1
        for noun in undeclared:
            probe = f"{CARRIER} {noun}."
            for gap_type in GOVERNED_GAP_TYPES:
                assert addresses_gap(probe, gap_type) is False, (
                    f"undeclared domain noun {noun!r} made {gap_type} eligible"
                )

    @pytest.mark.parametrize("connective", BARE_CAUSAL_CONNECTIVES)
    def test_bare_causal_connective_is_never_eligible_for_any_gap(self,
                                                                  connective):
        probe = f"{CARRIER} {connective} the widget."
        for gap_type in GOVERNED_GAP_TYPES:
            assert addresses_gap(probe, gap_type) is False, (
                f"bare connective {connective!r} made {gap_type} eligible — "
                "PVCG-R2-C §4 declares causal language insufficient on its own"
            )

    def test_a_pile_of_undeclared_nouns_and_connectives_is_still_not_eligible(self):
        """Signal density alone must not establish relevance for any gap (§4)."""
        undeclared = [n for n in GENERIC_TECHNICAL_NOUNS
                      if not any(n in DECLARED_WORDS[g] for g in GOVERNED_GAP_TYPES)]
        probe = (f"{CARRIER} " + " ".join(undeclared)
                 + " " + " ".join(BARE_CAUSAL_CONNECTIVES) + ".")
        for gap_type in GOVERNED_GAP_TYPES:
            assert addresses_gap(probe, gap_type) is False, (
                f"a dense pile of undeclared domain vocabulary and connectives "
                f"made {gap_type} eligible"
            )
