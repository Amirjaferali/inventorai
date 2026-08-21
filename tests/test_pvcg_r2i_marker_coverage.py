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
                   entry; cross-family exclusivity for the same probes; a sound
                   PHRASE-to-PHRASE substring proof for the only entries that
                   may be excluded; and structural guards on the tables.
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

SECOND WITHDRAWN CLAIM (T-1b)
-----------------------------
The first version of this file excluded ELEVEN entries from behavioural coverage,
asserting that each "contains another entry of its own family, so every text
containing it necessarily contains the companion". **That proof was unsound for
the nine PHRASE -> WORD cases and is withdrawn.** Phrase markers are matched by
SUBSTRING; word markers are matched by TOKEN. A phrase can therefore match inside
a larger alphanumeric run in which the companion token is dissolved — e.g.
"ztake for grantedz" contains the phrase but tokenises to {ztake, for, grantedz},
so no "granted" token exists and the phrase alone decides eligibility. All nine
were re-measured at the rejected SHA `58ef3971…`, confirmed to flip
`addresses_gap` when removed, and are now OPERATIVE with isolated probes.

Only PHRASE -> PHRASE containment survives as a universal shadow, because both
sides use the same substring rule. Exactly two remain, each independently
re-verified: `power requirements` -> `power requirement` and `physical limits` ->
`physical limit`. This is a classification and coverage repair; the relevance
algorithm itself is unchanged and was never at fault.
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
    """Return a same-family PHRASE that every text containing `entry` must also
    contain, or None.

    WITHDRAWN AND CORRECTED (T-1b). The earlier version of this helper also
    returned a same-family WORD whose token appeared in the entry text, and the
    suite asserted from that that the entry could never decide eligibility. That
    was UNSOUND and is withdrawn: phrase markers match by SUBSTRING while word
    markers match by TOKEN, so a phrase can match inside a larger alphanumeric
    run in which the companion token is dissolved and therefore absent. Example:
    "ztake for grantedz" contains the phrase "take for granted" as a substring
    but tokenises to {ztake, for, grantedz} — no "granted" token. The phrase
    alone decides eligibility there.

    Only PHRASE -> PHRASE containment is a sound universal shadow, because both
    sides are matched by the same substring rule: if the shorter phrase is a
    substring of the longer, then every text containing the longer necessarily
    contains the shorter.
    """
    if entry not in DECLARED_PHRASES.get(gap_type, ()):
        return None
    for other in DECLARED_PHRASES.get(gap_type, ()):
        if other != entry and other in entry:
            return other
    return None


def _probe_variants(entry, gap_type):
    """Candidate isolating probes for `entry`, most natural first.

    For a phrase, a second variant wraps the phrase in adjacent word characters.
    That preserves the phrase substring exactly while dissolving any companion
    word token, which is what makes an isolated probe possible for the nine
    entries T-1b reclassified as operative.
    """
    yield f"{CARRIER} {entry}."
    if entry in DECLARED_PHRASES.get(gap_type, ()):
        yield f"{CARRIER} z{entry}z."


def _build_probes():
    """Generate one isolated probe per entry.

    Raises at import (collection failure) if a probe cannot be isolated for a
    reason other than a proven structural companion — an unisolated probe is
    false coverage and must never be silently accepted.
    """
    operative, shadowed = [], []
    for gap_type, entry, kind in _all_entries():
        isolated = None
        last = None
        for probe in _probe_variants(entry, gap_type):
            last = probe
            foreign = {
                other: _family_hits(probe, other)
                for other in GOVERNED_GAP_TYPES if other != gap_type
            }
            foreign = {k: v for k, v in foreign.items() if v}
            if foreign:
                raise AssertionError(
                    "probe generation failed: the candidate probe for "
                    f"{gap_type}/{entry!r} carries markers of another family: "
                    f"{foreign}. An unisolated probe would let a marker-removal "
                    "mutant survive."
                )
            if _family_hits(probe, gap_type) == {entry}:
                isolated = probe
                break
        if isolated is not None:
            operative.append((gap_type, entry, kind, isolated))
            continue
        companion = _necessary_companion(entry, gap_type)
        if companion is None:
            raise AssertionError(
                "probe generation failed: no isolating probe could be built for "
                f"{gap_type}/{entry!r} (last attempt carried "
                f"{sorted(_family_hits(last, gap_type))}) and it has no sound "
                "phrase-to-phrase structural companion. It must not be silently "
                "excluded from coverage."
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
    def test_shadow_is_phrase_to_phrase_substring_containment(
            self, gap_type, entry, kind, companion):
        """The ONLY sound universal shadow: both sides are phrases, matched by
        the same substring rule, and the companion is a substring of the entry.
        Every text containing `entry` therefore contains `companion`, for every
        input — so removing `entry` cannot change any verdict.

        Phrase -> WORD containment is explicitly NOT accepted here (T-1b): word
        markers match by token, so a phrase can match inside a larger
        alphanumeric run where the companion token is dissolved."""
        assert kind == "phrase", (
            f"{entry!r} is a {kind}; only phrases may be structurally shadowed"
        )
        assert companion in DECLARED_PHRASES[gap_type], (
            f"companion {companion!r} is not a phrase — phrase-to-word "
            "containment does not establish a universal shadow"
        )
        assert companion != entry
        assert companion in entry, (
            f"{entry!r} does not contain {companion!r} as a substring"
        )

    @pytest.mark.parametrize("gap_type,entry,kind,companion", SHADOWED_ENTRIES,
                             ids=_ids(SHADOWED_ENTRIES))
    def test_shadow_survives_token_dissolving_attack(self, gap_type, entry,
                                                     kind, companion):
        """Adversarial check of the shadow: even when surrounding word tokens
        are dissolved, the companion phrase is still matched, so the entry is
        genuinely never the sole reason for eligibility."""
        for probe in (f"{CARRIER} {entry}.",
                      f"{CARRIER} z{entry}z.",
                      f"{CARRIER} abc{entry}xyz."):
            assert companion in _family_hits(probe, gap_type)
            assert addresses_gap(probe, gap_type) is True

    def test_no_phrase_to_word_shadow_claim_survives(self):
        """Guards the T-1b repair itself: no entry may be excluded from
        behavioural coverage on phrase-to-word grounds ever again."""
        for gap_type, entry, kind, companion in SHADOWED_ENTRIES:
            assert companion not in DECLARED_WORDS[gap_type], (
                f"{entry!r} is excluded on a phrase-to-word companion "
                f"({companion!r}) — that reasoning is unsound"
            )


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
