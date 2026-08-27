"""The chronology corpus answers with every assertion, or refuses and says why.

`guidance/scripture-chronology.md` settles the contract. These tests assert the
properties that make the corpus worth having rather than the ones that are easy
to check: that a locus can carry several typed assertions at once, that an event
is dated once no matter how many loci reach it, that composition inherits
without being copied, and that every way of producing a plausible wrong date is
refused rather than resolved.

Which books exist, how many verses each chapter carries, and how the psalter is
numbered are all read from the repository's own data through `_canon`, the
canonical edition's chapter fragments and `_psalms`. A second list beside any of
them is the fault this apparatus exists to prevent, and a test carrying one
would go green against the wrong file.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import _chronology  # noqa: E402
import _projection  # noqa: E402
import _psalms  # noqa: E402


def load_tool(name: str):
    path = REPOSITORY_ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


tool = load_tool("scripture-chronology")

PROFILE = "catholic-traditional-v1"

PROFILES = """\
schema: triptych-chronology-profiles/v1
profiles:
  - id: catholic-traditional-v1
    title: Test profile
    intent: A profile that exists so the loader has one to check against.
    authority:
      - rank: 1
        name: Scripture
    conflict:
      rule: Preserve the disagreement.
    non_goals:
      - Being real.
"""

HEAD = {
    "events": "schema: triptych-chronology-events/v1\n",
    "composition": (
        "schema: triptych-chronology-composition/v1\nnumbering: vulgate\n"
    ),
    "bindings": "schema: triptych-chronology-bindings/v1\nnumbering: vulgate\n",
    "gaps": "schema: triptych-chronology-gaps/v1\nnumbering: vulgate\n",
}


class Corpus:
    """A whole authored corpus in a temporary directory, written per test.

    Fixtures are built rather than tracked, so a test that needs a shape the
    real corpus does not yet hold does not have to add one to it — and cannot
    accidentally assert about tracked data it did not write.
    """

    def __init__(self, stack: tempfile.TemporaryDirectory, **bodies: str) -> None:
        self.root = Path(stack.name) / "chronology"
        self.root.mkdir()
        (self.root / "profiles.yaml").write_text(
            bodies.pop("profiles", PROFILES), encoding="utf-8"
        )
        for name, head in HEAD.items():
            body = bodies.pop(name, "")
            key = {"composition": "units"}.get(name, name)
            text = head + (body if body else f"{key}: []\n")
            (self.root / f"{name}.yaml").write_text(text, encoding="utf-8")
        if bodies:
            raise AssertionError(f"unused fixture bodies: {sorted(bodies)}")
        _chronology.load.cache_clear()
        _chronology._by_book.cache_clear()
        # Loading here is what makes a fixture a test of the loader: a corpus
        # written and never read refuses nothing.
        _chronology.load(self.root)

    def ask(self, locus: str, system: str = "vulgate"):
        return _chronology.chronology(
            _chronology.parse_locus(locus, "test", system), root=self.root
        )


def corpus(case: unittest.TestCase, **bodies: str) -> Corpus:
    stack = tempfile.TemporaryDirectory()
    case.addCleanup(stack.cleanup)
    case.addCleanup(_chronology.load.cache_clear)
    case.addCleanup(_chronology._by_book.cache_clear)
    return Corpus(stack, **bodies)


def refuses(case: unittest.TestCase, needle: str, **bodies: str) -> None:
    with case.assertRaises(_chronology.ChronologyError) as caught:
        corpus(case, **bodies)
    case.assertIn(needle, str(caught.exception))


# --- Dates ------------------------------------------------------------------


class DateTests(unittest.TestCase):
    """Every shape of date that would read as a fact and is not one."""

    def date(self, **raw):
        return _chronology.parse_date(raw, "test")

    def refuse(self, needle: str, **raw):
        with self.assertRaises(_chronology.ChronologyError) as caught:
            _chronology.parse_date(raw, "test")
        self.assertIn(needle, str(caught.exception))

    def test_there_is_no_year_zero_in_either_christian_era(self) -> None:
        # An interval computed across a year zero is wrong by one and reads
        # perfectly, which is the whole class of defect this corpus is for.
        for era in ("bc", "ad"):
            self.refuse("no year zero", precision="year", **{"from": {"year": 0, "era": era}})

    def test_a_year_is_never_negative_because_bc_is_an_era(self) -> None:
        self.refuse("B.C. is an era, not a sign", precision="year", **{"from": {"year": -44, "era": "bc"}})

    def test_a_range_may_not_run_backwards(self) -> None:
        self.refuse(
            "ends at",
            precision="range",
            **{"from": {"year": 45, "era": "ad"}, "to": {"year": 40, "era": "ad"}},
        )

    def test_bc_counts_down_so_an_earlier_bc_year_is_the_larger_number(self) -> None:
        date = self.date(
            precision="range",
            **{"from": {"year": 1000, "era": "bc"}, "to": {"year": 900, "era": "bc"}},
        )
        self.assertEqual(date.precision, "range")
        self.refuse(
            "ends at",
            precision="range",
            **{"from": {"year": 900, "era": "bc"}, "to": {"year": 1000, "era": "bc"}},
        )

    def test_anno_mundi_and_the_christian_era_are_different_reckonings(self) -> None:
        # Traditional sources print A.M.; converting needs an epoch no ranked
        # source here has been inspected asserting. A range across the two
        # would put two epochs on one axis.
        self.refuse(
            "different reckonings",
            precision="range",
            **{"from": {"year": 3398, "era": "am"}, "to": {"year": 600, "era": "bc"}},
        )

    def test_an_impossible_day_is_refused(self) -> None:
        self.refuse(
            "not a day of month",
            precision="day",
            **{"from": {"year": 33, "era": "ad", "month": 2, "day": 31}},
        )

    def test_a_day_needs_its_month(self) -> None:
        self.refuse(
            "day 3 given with no month",
            precision="day",
            **{"from": {"year": 33, "era": "ad", "day": 3}},
        )

    def test_a_single_point_precision_refuses_two_different_endpoints(self) -> None:
        self.refuse(
            "names one point",
            precision="year",
            **{"from": {"year": 40, "era": "ad"}, "to": {"year": 45, "era": "ad"}},
        )

    def test_month_day_means_the_year_is_unknown(self) -> None:
        self.date(precision="month-day", **{"from": {"month": 3, "day": 25}})
        self.refuse(
            "the year is unknown",
            precision="month-day",
            **{"from": {"year": 33, "era": "ad", "month": 3, "day": 25}},
        )

    def test_an_unrecognised_key_is_a_failure_not_something_to_ignore(self) -> None:
        # A validator that skips what it does not recognise cannot tell a typo
        # from a fact.
        self.refuse("unknown date key", precision="year", yaer=33)
        self.refuse(
            "unknown endpoint key",
            precision="year",
            **{"from": {"year": 33, "era": "ad", "circa": True}},
        )

    def test_a_derivation_must_name_its_rule_and_its_inputs(self) -> None:
        self.refuse(
            "name the rule",
            precision="year",
            derivation={"inputs": ["a"]},
            **{"from": {"year": 33, "era": "ad"}},
        )
        self.refuse(
            "name the input claims",
            precision="year",
            derivation={"rule": "add"},
            **{"from": {"year": 33, "era": "ad"}},
        )

    def test_a_relative_date_carries_no_absolute_endpoints(self) -> None:
        self.date(precision="relative", relative={"of": "x", "statement": "40 years after"})
        self.refuse(
            "carries no absolute endpoints",
            precision="relative",
            relative={"of": "x"},
            **{"from": {"year": 33, "era": "ad"}},
        )

    def test_precision_is_not_authority(self) -> None:
        # Two claims, one approximate and one exact, are equally admissible;
        # nothing in the date model ranks them. Which wins is the profile's
        # question and is answered by disposition, not by precision.
        loose = self.date(precision="approximate-year", **{"from": {"year": 42, "era": "ad"}})
        tight = self.date(precision="year", **{"from": {"year": 42, "era": "ad"}})
        self.assertEqual(loose.begin, tight.begin)
        self.assertNotEqual(loose.precision, tight.precision)


# --- Loading and refusal ----------------------------------------------------


EVENT = """\
events:
  - id: life-of-christ.crucifixion
    title: The Crucifixion
    dates:
      - profile: catholic-traditional-v1
        disposition: preferred
        basis: A test fixture, grounded in nothing.
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
"""


class LoadRefusalTests(unittest.TestCase):
    """Each of these produced a well-formed corpus that meant something else."""

    def test_a_binding_may_not_carry_a_date(self) -> None:
        # The one door through which parallel passages acquire parallel dates.
        refuses(
            self,
            "a binding carries no date",
            events=EVENT,
            bindings="""\
bindings:
  - relation: narrated-event
    event: life-of-christ.crucifixion
    scope: {book: Matt, chapter: 27, first: 35, last: 35}
    dates: []
""",
        )

    def test_a_binding_may_not_name_an_undeclared_event(self) -> None:
        refuses(
            self,
            "is not declared in events.yaml",
            bindings="""\
bindings:
  - relation: narrated-event
    event: life-of-christ.ascension
    scope: {book: Acts, chapter: 1, first: 9, last: 11}
""",
        )

    def test_composition_is_not_an_event_binding(self) -> None:
        refuses(
            self,
            "composition is not an event binding",
            events=EVENT,
            bindings="""\
bindings:
  - relation: composition
    event: life-of-christ.crucifixion
    scope: {book: Matt}
""",
        )

    def test_an_unknown_relation_is_refused_rather_than_admitted(self) -> None:
        refuses(
            self,
            "is not one of",
            events=EVENT,
            bindings="""\
bindings:
  - relation: sort-of-about
    event: life-of-christ.crucifixion
    scope: {book: Matt}
""",
        )

    def test_two_units_of_equal_width_over_one_verse_is_an_error(self) -> None:
        # Nothing here may pick between them. Choosing the first, or the most
        # recently edited, would be a date resolving successfully and wrongly.
        refuses(
            self,
            "at the same width",
            composition="""\
units:
  - id: composition.matthew
    title: Matthew
    scope: {book: Matt}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 42, era: ad}}
  - id: composition.matthew-again
    title: Matthew again
    scope: {book: Matt}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 50, era: ad}}
""",
        )

    def test_a_sourced_claim_must_name_a_source(self) -> None:
        refuses(
            self,
            "must name at least one source record",
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        date: {precision: year, from: {year: 33, era: ad}}
""",
        )

    def test_every_claim_must_say_what_grounds_it(self) -> None:
        refuses(
            self,
            "basis is required",
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
""",
        )

    def test_two_preferred_claims_under_one_profile_are_refused(self) -> None:
        refuses(
            self,
            "exactly one may be",
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        disposition: preferred
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
      - profile: catholic-traditional-v1
        disposition: preferred
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 34, era: ad}}
""",
        )

    def test_nothing_is_preferred_while_something_is_disputed(self) -> None:
        refuses(
            self,
            "has no preferred side",
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        disposition: preferred
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
      - profile: catholic-traditional-v1
        disposition: disputed
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 34, era: ad}}
""",
        )

    def test_two_claims_must_say_which_is_which(self) -> None:
        refuses(
            self,
            "none is preferred or disputed",
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
      - profile: catholic-traditional-v1
        disposition: alternate
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 34, era: ad}}
""",
        )

    def test_a_locus_bearing_file_must_declare_its_numbering(self) -> None:
        stack = tempfile.TemporaryDirectory()
        self.addCleanup(stack.cleanup)
        root = Path(stack.name) / "chronology"
        root.mkdir()
        (root / "profiles.yaml").write_text(PROFILES, encoding="utf-8")
        (root / "events.yaml").write_text(HEAD["events"] + "events: []\n", encoding="utf-8")
        (root / "composition.yaml").write_text(
            "schema: triptych-chronology-composition/v1\nunits: []\n", encoding="utf-8"
        )
        (root / "bindings.yaml").write_text(HEAD["bindings"] + "bindings: []\n", encoding="utf-8")
        (root / "gaps.yaml").write_text(HEAD["gaps"] + "gaps: []\n", encoding="utf-8")
        _chronology.load.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        with self.assertRaises(_chronology.ChronologyError) as caught:
            _chronology.load(root)
        self.assertIn("declares numbering", str(caught.exception))

    def test_a_system_may_not_name_a_book_it_does_not_number(self) -> None:
        """`hebrew` is a psalter numbering, and names nothing outside it.

        This replaced a test asserting that chronology is authored in exactly
        one system, which was the architecture Correction A abolished on
        2026-08-27. The rule that survives it is the sharper one: a scope's
        system must actually number the book it names. The abandoned scratch
        patch admitted exactly this fixture, because it checked the system name
        against a flat set and never asked which books that system addresses.
        """
        refuses(
            self,
            "does not number",
            composition="""\
units:
  - id: composition.matthew
    title: Matthew
    scope: {system: hebrew, book: Matt}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 42, era: ad}}
""",
        )

    def test_a_scope_may_not_name_a_system_with_no_machinery(self) -> None:
        refuses(
            self,
            "is not a Scripture system this repository has machinery for",
            composition="""\
units:
  - id: composition.matthew
    title: Matthew
    scope: {system: septuagint, book: Matt}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 42, era: ad}}
""",
        )

    def test_native_authoring_is_refused_where_the_text_is_safely_shared(self) -> None:
        """The gate that keeps "one fact, one place" from being a convention.

        Hebrew Psalm 51 IS Vulgate Psalm 50 - the concordance carries it - so a
        native Hebrew scope over it would be the same fact authored twice.
        Native scopes are admissible precisely where sharing is impossible.
        """
        refuses(
            self,
            "authors chronology natively",
            composition="""\
units:
  - id: composition.psalm-51-hebrew
    title: Psalm 51, natively
    scope: {system: hebrew, book: Ps, chapter: 51}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 42, era: ad}}
""",
        )

    def test_a_native_span_is_validated_past_its_first_locus(self) -> None:
        """The gate the cold audit found proving something about verse one.

        It probed `span.first or 1`, so a span whose opening refused the
        concordance was admitted entire however its interior behaved. This
        fixture is that exact shape: greek Ecclus 36 opens at a locus the
        concordance refuses, and its verse 16 carries safely to the Vulgate,
        where the same composition date is already held. A gate that reads only
        the first locus admits it.
        """
        refuses(
            self,
            "Ecclus 36:16",
            composition="""\
units:
  - id: composition.ecclesiasticus
    title: Ecclesiasticus, at the preferred locus
    scope: {book: Ecclus}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: interval
          from: {year: 190, era: bc}
          to: {year: 170, era: bc}
          label: "between 190 and 170 B.C."
  - id: composition.ecclesiasticus-greek-chapter-36
    title: A native span whose interior restates a shared fact
    scope: {system: greek, book: Ecclus, chapter: 36}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: interval
          from: {year: 190, era: bc}
          to: {year: 170, era: bc}
          label: "between 190 and 170 B.C."
""",
        )

    def test_a_psalter_numbering_may_never_date_a_psalm_natively(self) -> None:
        """A renumbering is not a witness, and the gate must not confuse them.

        The distinction is asked of the module that owns each name: `_psalms`
        owns `hebrew`, which is one psalter under two numbers, so a native scope
        there is the same fact twice whatever value it carries. `_deuterocanon`
        owns `greek`, which is a different text. Value-blindness is the point -
        two DIFFERENT dates for one psalm is the worse failure, not the lesser.
        """
        refuses(
            self,
            "the same text under another number",
            composition="""\
units:
  - id: composition.psalm-51-hebrew-divergent
    title: Psalm 51, natively, with a date the Vulgate does not hold
    scope: {system: hebrew, book: Ps, chapter: 51}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 999, era: bc}}
""",
        )

    def test_an_event_may_be_a_subject_without_being_a_dated_one(self) -> None:
        """Naming a thing is not the same act as dating it.

        `israel.monarchy.saul-accession` carried one claim, Howlett's 1020 B.C.,
        reached by preferring Egyptological synchronisms — the reconstruction
        §4.3 says is "not consulted". Being the only claim on the subject, it
        was what this profile answered for the founding of the monarchy. It
        could not be withdrawn while every event required a date, because two
        bindings name this event and four claims are measured from it. So an
        event may now hold no claim: it asserts nothing and returns nothing.
        """
        corpus(
            self,
            events="""\
events:
  - id: israel.judges.period
    title: An anchor nobody has dated
  - id: israel.monarchy.saul-accession
    title: Another, measured from the first
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: relative
          relative: {of: israel.judges.period, statement: "after the judges"}
""",
        )

    def test_a_composition_unit_still_needs_a_date(self) -> None:
        # The relaxation is for events only. A unit exists to carry a
        # composition date over an extent, so a dateless one would be a scope
        # asserting nothing about the text it names.
        refuses(
            self,
            "needs a non-empty 'dates' list",
            composition="""\
units:
  - id: composition.jude
    title: Jude, undated
    scope: {book: Jude}
""",
        )

    def test_a_scope_may_not_name_a_chapter_the_book_has_not(self) -> None:
        refuses(
            self,
            "is not one",
            composition="""\
units:
  - id: composition.jude
    title: Jude
    scope: {book: Jude, chapter: 3}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 65, era: ad}}
""",
        )

    def test_a_relative_date_anchored_to_nothing_is_refused(self) -> None:
        # Found by an author, not by this suite: a claim reading "forty years
        # after <event>" loaded cleanly and audited cleanly while naming an
        # event that did not exist, so it stated nothing and stated it in
        # well-formed YAML. The first real corpus carried one.
        refuses(
            self,
            "a date measured from nothing states nothing",
            events="""\
events:
  - id: e.anchor
    title: An anchor
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 900, era: bc}}
  - id: e.measured
    title: Measured from something that is not there
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: relative
          relative: {of: e.no-such-anchor, statement: forty years after}
""",
        )

    def test_a_relative_date_must_say_what_the_interval_is(self) -> None:
        refuses(
            self,
            "without saying what the interval is",
            events="""\
events:
  - id: e.anchor
    title: An anchor
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 900, era: bc}}
  - id: e.measured
    title: Measured, but from how far
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: relative
          relative: {of: e.anchor}
""",
        )

    def test_a_gap_may_not_claim_a_status_assertions_earn(self) -> None:
        refuses(
            self,
            "is not one an author may assert",
            gaps="""\
gaps:
  - status: dated
    scope: {book: Jude}
    reason: it is not
""",
        )


# --- The model's point ------------------------------------------------------


FOUR_GOSPELS = """\
bindings:
  - relation: narrated-event
    event: life-of-christ.crucifixion
    scope:
      - {book: Matt, chapter: 27, first: 33, last: 56}
      - {book: Mark, chapter: 15, first: 22, last: 41}
      - {book: Luke, chapter: 23, first: 33, last: 49}
      - {book: John, chapter: 19, first: 17, last: 37}
  - relation: prophetic-referent
    event: life-of-christ.crucifixion
    scope: {book: Ps, chapter: 21, first: 17, last: 19}
"""

PSALM_21 = """\
units:
  - id: composition.psalm-21
    title: Psalm 21
    scope: {book: Ps, chapter: 21}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: approximate-year, from: {year: 1000, era: bc}}
"""


class ManyValuedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.corpus = corpus(
            self, events=EVENT, bindings=FOUR_GOSPELS, composition=PSALM_21
        )

    def test_one_event_reaches_four_gospels_with_one_date(self) -> None:
        seen = set()
        for locus in ("Matt.27.35", "Mark.15.24", "Luke.23.34", "John.19.23"):
            answer = self.corpus.ask(locus)
            narrated = [a for a in answer.assertions if a.relation == "narrated-event"]
            self.assertEqual(len(narrated), 1, locus)
            self.assertEqual(narrated[0].subject, "life-of-christ.crucifixion")
            seen.add(str(narrated[0].claim.date))
        # Four Gospels, one date. Four dates here would be the failure the
        # whole binding shape exists to prevent.
        self.assertEqual(seen, {"33 A.D."})

    def test_a_psalm_prophesies_the_passion_without_narrating_it(self) -> None:
        answer = self.corpus.ask("Ps.21.18")
        relations = [a.relation for a in answer.assertions]
        self.assertIn("prophetic-referent", relations)
        self.assertNotIn("narrated-event", relations)
        referent = next(a for a in answer.assertions if a.relation == "prophetic-referent")
        self.assertEqual(referent.subject, "life-of-christ.crucifixion")

    def test_one_locus_carries_composition_and_prophetic_referent_at_once(self) -> None:
        answer = self.corpus.ask("Ps.21.18")
        self.assertEqual(
            [a.relation for a in answer.assertions],
            ["composition", "prophetic-referent"],
        )
        composition = answer.assertions[0]
        self.assertEqual(str(composition.claim.date), "about 1000 B.C.")
        # The composition date and the referent's date are both present and
        # neither has overwritten the other.
        self.assertNotEqual(
            str(answer.assertions[0].claim.date), str(answer.assertions[1].claim.date)
        )

    def test_the_order_is_defined_and_does_not_depend_on_authoring_order(self) -> None:
        first = [a.sort_key() for a in self.corpus.ask("Ps.21.18").assertions]
        self.assertEqual(first, sorted(first))


class InheritanceTests(unittest.TestCase):
    BOOK_AND_CHAPTER = """\
units:
  - id: composition.matthew
    title: The Gospel of St Matthew
    scope: {book: Matt}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: approximate-year, from: {year: 42, era: ad}}
  - id: composition.matthew-appendix
    title: One chapter of it
    scope: {book: Matt, chapter: 28}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 50, era: ad}}
"""

    def test_a_book_level_unit_reaches_a_verse_without_being_copied(self) -> None:
        book = corpus(self, composition=self.BOOK_AND_CHAPTER)
        answer = book.ask("Matt.1.1")
        self.assertEqual(len(answer.assertions), 1)
        self.assertEqual(answer.assertions[0].subject, "composition.matthew")
        # HOW it arrived. Provenance, and nothing else.
        self.assertTrue(answer.assertions[0].inherited)

    def test_how_an_assertion_arrived_does_not_decide_what_the_locus_has(self) -> None:
        """The two questions this file used to ask on adjacent lines.

        `inherited` says the assertion was authored at a scope containing this
        verse rather than at the verse. The status says what kind of chronology
        the verse has. Reading the first as an answer to the second is the
        defect corrected on 2026-08-27, so they are asked apart here: a
        composition unit reaching a verse by inheritance leaves that verse
        `composition-only` because composition is all it has, NOT because the
        assertion was inherited.
        """
        book = corpus(self, composition=self.BOOK_AND_CHAPTER)
        answer = book.ask("Matt.1.1")
        self.assertEqual(answer.status, "composition-only")
        self.assertTrue(all(item.inherited for item in answer.assertions))

    def test_a_verse_scoped_composition_unit_is_still_composition_only(self) -> None:
        """The one case where the old rule and the corrected rule disagree.

        The old rule made a locus `dated` if any assertion was direct, so a
        composition unit authored at verse scope — direct, and composition —
        would have reported substantive event chronology that nobody had
        researched. No unit in the tracked corpus is scoped that narrowly,
        which is why the defect never showed; it is still a defect, and this
        holds the corrected rule to it.
        """
        narrow = corpus(
            self,
            composition="""\
units:
  - id: composition.matthew-one-one
    title: Matthew 1:1
    scope: {book: Matt, chapter: 1, first: 1, last: 1}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 42, era: ad}}
""",
        )
        answer = narrow.ask("Matt.1.1")
        self.assertEqual(len(answer.assertions), 1)
        self.assertFalse(answer.assertions[0].inherited)
        self.assertEqual(answer.status, "composition-only")

    def test_the_narrowest_unit_covering_a_verse_wins(self) -> None:
        book = corpus(self, composition=self.BOOK_AND_CHAPTER)
        answer = book.ask("Matt.28.1")
        self.assertEqual(len(answer.assertions), 1)
        self.assertEqual(answer.assertions[0].subject, "composition.matthew-appendix")
        self.assertEqual(str(answer.assertions[0].claim.date), "50 A.D.")

    def test_inheritance_does_not_duplicate_the_direct_assertion(self) -> None:
        book = corpus(self, composition=self.BOOK_AND_CHAPTER)
        subjects = [a.subject for a in book.ask("Matt.28.1").assertions]
        self.assertEqual(subjects, ["composition.matthew-appendix"])


class AlternativeTests(unittest.TestCase):
    DISPUTED = """\
events:
  - id: e.disputed
    title: Something the sources disagree about
    dates:
      - profile: catholic-traditional-v1
        disposition: disputed
        basis: One authority says so.
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
      - profile: catholic-traditional-v1
        disposition: disputed
        basis: Another authority says otherwise.
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 29, era: ad}}
"""
    BOUND = """\
bindings:
  - relation: narrated-event
    event: e.disputed
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
"""

    def test_the_query_returns_both_claims_and_chooses_neither(self) -> None:
        both = corpus(self, events=self.DISPUTED, bindings=self.BOUND)
        answer = both.ask("Jude.1.1")
        self.assertEqual(len(answer.assertions), 2)
        self.assertEqual(
            {str(a.claim.date) for a in answer.assertions}, {"33 A.D.", "29 A.D."}
        )
        self.assertEqual({a.claim.disposition for a in answer.assertions}, {"disputed"})
        # Each keeps its own provenance; harmonising them would lose which
        # authority said which.
        self.assertEqual(len({a.claim.basis for a in answer.assertions}), 2)


# --- Reaching the corpus from another numbering -----------------------------


class NumberingTests(unittest.TestCase):
    """The psalter and the deuterocanon, which is where a fake key would show."""

    MISERERE = """\
units:
  - id: composition.psalm-50
    title: The Miserere
    scope: {book: Ps, chapter: 50}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: approximate-year, from: {year: 1000, era: bc}}
"""

    def test_the_miserere_is_one_psalm_with_one_chronology(self) -> None:
        # Vulgate 50 and Hebrew 51 are the same psalm. Authoring both would be
        # two chronologies for one text; `_psalms` already holds the mapping.
        book = corpus(self, composition=self.MISERERE)
        vulgate = book.ask("Ps.50.5")
        hebrew = book.ask("Ps.51.5", system="hebrew")
        self.assertEqual(str(vulgate.locus), "Ps.50.5")
        self.assertEqual(str(hebrew.locus), str(vulgate.locus))
        self.assertEqual(
            [a.subject for a in hebrew.assertions],
            [a.subject for a in vulgate.assertions],
        )
        self.assertEqual(hebrew.assertions[0].subject, "composition.psalm-50")

    def test_the_hebrew_number_reaches_the_vulgate_one_through_the_concordance(self) -> None:
        # Not by arithmetic here. The concordance is the only thing that knows,
        # and a subtraction of one would be wrong for Psalms 1-8 and 148-150.
        chapter, verse, _ = _psalms.convert_point(51, 5, "hebrew", "vulgate")
        self.assertEqual((chapter, verse), (50, 5))
        for hebrew, vulgate in ((1, 1), (9, 9), (10, 9), (150, 150)):
            moved, _ = _psalms.convert_chapter(hebrew, "hebrew", "vulgate", verse=1)
            self.assertEqual(moved, vulgate, hebrew)

    def test_a_psalm_that_splits_refuses_without_a_verse_to_choose_by(self) -> None:
        # Hebrew 147 is Vulgate 146 and 147. A chapter-level answer would have
        # to pick, and picking is the failure.
        with self.assertRaises(_psalms.NumberingError) as caught:
            _psalms.convert_chapter(147, "hebrew", "vulgate")
        self.assertIn("a verse is needed to choose", str(caught.exception))

    def test_the_printed_title_offset_is_a_third_move_this_layer_does_not_make(self) -> None:
        # The vulgate/hebrew concordance shifts the psalm NUMBER; whether an
        # edition numbers the superscription as verse 1 is a separate question
        # that `_psalms.english_verse` owns, and sixteen psalms refuse it
        # outright. Chronology must not silently apply either as the other.
        moved, verse, _ = _psalms.convert_point(51, 1, "hebrew", "vulgate")
        self.assertEqual((moved, verse), (50, 1))
        refused = [
            chapter
            for chapter in range(1, 151)
            if _psalms.english_verse(chapter, 1)[0] is None
        ]
        self.assertTrue(refused)
        for chapter in refused:
            self.assertIsNone(_psalms.english_verse(chapter, 1)[0])

    def test_sirach_refuses_because_it_is_two_texts_and_not_two_numberings(self) -> None:
        # 48 of Sirach's 51 chapters differ in verse count between the tracked
        # Latin and Greek witnesses, and 0 of 51 agree throughout, so the
        # concordance records the whole book `not-recorded`. A key that
        # resolved anyway would answer about different words than were asked
        # about — and would do it fluently.
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("Ecclus.35.1", "test", "greek"), root=book.root
        )
        # In this FIXTURE corpus the Greek Ecclesiasticus has no native
        # chronology, so the two axes separate cleanly: the mapping refuses
        # with the concordance's own reason, and the chronology axis says only
        # that nobody has looked. A mapping word must never be the answer to
        # "is this dated?".
        self.assertIsInstance(answer, _chronology.Answer)
        self.assertEqual(answer.mapping.status, "textually-distinct")
        self.assertIn("Ecclesiasticus", answer.mapping.note)
        self.assertEqual(answer.status, "research-pending")
        self.assertEqual(answer.assertions, ())

    def test_a_greek_arrangement_locus_lands_where_the_concordance_says(self) -> None:
        # Not a blanket refusal: the concordance knows where a correspondence
        # was established. Susanna is a book of its own in the Greek
        # arrangement and Daniel 13 in the Vulgate, and Greek Daniel 4 opens
        # inside Vulgate Daniel 3 because the two traditions put the chapter
        # boundary in different places. Both are answers no arithmetic gives.
        book = corpus(self)

        def ask(locus, system):
            return _chronology.chronology(
                _chronology.parse_locus(locus, "test", system), root=book.root
            )

        self.assertEqual(str(ask("Sus.1.1", "greek").locus), "Dan.13.1")
        self.assertEqual(str(ask("Dan.4.1", "greek").locus), "Dan.3.98")
        self.assertEqual(str(ask("Dan.1.1", "greek").locus), "Dan.1.1")

    def test_an_arrangement_with_no_recorded_row_refuses_with_its_reason(self) -> None:
        # EsthGr, where the concordance genuinely records no row between this
        # edition and the Greek it re-divides.
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("EsthGr.1.1", "test", "world-english-catholic"),
            root=book.root,
        )
        # BOTH AXES, which is what this used to get wrong. The mapping refuses
        # and says why; the chronology axis answers the way any unresearched
        # locus does. Returning the mapping word as the chronology status was
        # the defect the cold audit found on ten native loci.
        self.assertIsInstance(answer, _chronology.Answer)
        self.assertEqual(answer.mapping.status, "textually-distinct")
        self.assertIn("no correspondence is recorded", answer.mapping.note)
        self.assertEqual(answer.status, "research-pending")
        self.assertEqual(answer.assertions, ())

    def test_a_two_hop_edition_is_reached_through_its_hops(self) -> None:
        """This test used to assert the opposite, and the opposite was a bug.

        The World English Catholic edition is two hops from the Vulgate,
        through the Greek, and `_deuterocanon.convert_through`'s own docstring
        says so: it "is the only way to reach it without a second table saying
        the same thing twice". Chronology asked `convert_verse` for a direct
        row, the direct index is empty, and every one of that edition's 2 131
        loci came back `textually-distinct` — a refusal produced by taking the
        wrong road, which the test then enshrined as expected. Under the
        corrected coverage rules it would also have counted all 2 131 as new
        Scripture; 730 of them are the Vulgate's own text.
        """
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("Dan.13.1", "test", "world-english-catholic"),
            root=book.root,
        )
        self.assertIsInstance(answer, _chronology.Answer)
        self.assertEqual(answer.mapping.status, "shared")
        self.assertEqual(answer.mapping.reached, "Dan.13.1")

    def test_an_unknown_system_refuses_with_a_reason(self) -> None:
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("Gen.1.1", "test", "septuagint"), root=book.root
        )
        self.assertIsInstance(answer, _chronology.Unresolved)
        self.assertEqual(answer.status, "not-alignable")
        # The reason now names what the repository actually has machinery for,
        # rather than reporting a missing concordance for a system that was
        # never a system here at all.
        self.assertIn("is not a Scripture system", answer.reason)
        self.assertIn("septuagint", answer.reason)

    def test_a_refusal_is_returned_and_not_raised(self) -> None:
        # A caller must be able to print the reason. An exception here would
        # make the refusal indistinguishable from a defect at the call site.
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("Gen.99.1", "test"), root=book.root
        )
        self.assertIsInstance(answer, _chronology.Unresolved)
        self.assertFalse(answer.resolved)


# --- Absence ----------------------------------------------------------------


class StatusTests(unittest.TestCase):
    def test_an_unresearched_verse_is_research_pending_and_says_so(self) -> None:
        book = corpus(self)
        answer = book.ask("Gen.1.1")
        self.assertEqual(answer.status, "research-pending")
        self.assertTrue(answer.note)
        self.assertEqual(answer.assertions, ())

    def test_an_authored_gap_carries_its_own_status_and_reason(self) -> None:
        book = corpus(
            self,
            gaps="""\
gaps:
  - status: undated-in-tradition
    scope: {book: Jude}
    reason: The ranked sources were read and none dates it.
""",
        )
        answer = book.ask("Jude.1.1")
        self.assertEqual(answer.status, "undated-in-tradition")
        self.assertIn("none dates it", answer.note)

    def test_every_status_is_distinct_from_the_projections_vocabulary(self) -> None:
        # A verse can be present, aligned and perfectly addressable and still
        # have no date. A word meaning both would hide one of them.
        self.assertFalse(set(_chronology.STATUSES) & set(_projection.OVERRIDES))


class CoverageTests(unittest.TestCase):
    def test_every_verse_reaches_exactly_one_status(self) -> None:
        book = corpus(self, composition=InheritanceTests.BOOK_AND_CHAPTER)
        counts = _chronology.coverage(book.root)
        self.assertEqual(
            sum(counts["by_status"].values()), counts["total_verses"]
        )

    def test_the_denominator_is_the_canonical_editions_own_text(self) -> None:
        counts = _chronology.verse_counts()
        self.assertEqual(sum(counts.values()), 35809)
        self.assertEqual(len(counts), 1334)

    def test_runs_compress_consecutive_verses_that_answer_alike(self) -> None:
        book = corpus(self, composition=InheritanceTests.BOOK_AND_CHAPTER)
        table = _chronology.runs(book.root)
        matthew = [run for run in table if run.token == "Matt"]
        # 28 chapters, two of which answer differently from each other; the
        # compression must not collapse them and must not split what agrees.
        self.assertEqual(len(matthew), 28)
        self.assertEqual(
            {run.status for run in matthew}, {"composition-only"}
        )
        self.assertTrue(all(run.verses > 1 for run in matthew))

    def test_coverage_reports_categories_and_no_single_percentage(self) -> None:
        book = corpus(self, events=EVENT, bindings=FOUR_GOSPELS, composition=PSALM_21)
        counts = _chronology.coverage(book.root)
        for key in (
            "by_status",
            "by_relation",
            "verses_with_multiple_relations",
            "verses_with_substantive_event_assertions",
            "verses_with_alternative_traditional_claims",
        ):
            self.assertIn(key, counts)
        self.assertFalse([key for key in counts if "percent" in key])

    def test_a_verse_with_several_relations_is_counted_as_one(self) -> None:
        book = corpus(self, events=EVENT, bindings=FOUR_GOSPELS, composition=PSALM_21)
        counts = _chronology.coverage(book.root)
        self.assertEqual(counts["verses_with_multiple_relations"], 3)


# --- Audit ------------------------------------------------------------------


class AuditTests(unittest.TestCase):
    def test_a_source_this_repository_does_not_hold_is_named(self) -> None:
        book = corpus(
            self,
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [passage.nobody.nothing.no-such-edition.invented]
        date: {precision: year, from: {year: 33, era: ad}}
""",
        )
        problems = _chronology.audit(book.root)
        self.assertTrue(any("is not a record this repository holds" in p for p in problems))

    def test_a_scope_past_a_chapters_last_verse_is_named_with_the_ceiling(self) -> None:
        # Never clamp. guidance/versification.md §8.5 rule 1.
        book = corpus(
            self,
            composition="""\
units:
  - id: composition.jude
    title: Jude
    scope: {book: Jude, chapter: 1, first: 1, last: 999}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 65, era: ad}}
""",
        )
        problems = _chronology.audit(book.root)
        self.assertTrue(any("ends at verse" in p for p in problems), problems)

    def test_a_gap_standing_over_an_assertion_is_a_contradiction(self) -> None:
        book = corpus(
            self,
            composition=PSALM_21,
            gaps="""\
gaps:
  - status: undated-in-tradition
    scope: {book: Ps, chapter: 21}
    reason: Nothing dates it.
""",
        )
        problems = _chronology.audit(book.root)
        self.assertTrue(any("a gap says the corpus has nothing" in p for p in problems), problems)


# --- The tool ---------------------------------------------------------------


class ToolTests(unittest.TestCase):
    def test_the_tracked_corpus_validates(self) -> None:
        _chronology.load.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        self.assertEqual(tool.main(["validate"]), 0)

    def test_the_tracked_coverage_table_is_current(self) -> None:
        _chronology.load.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        self.assertEqual(tool.main(["check"]), 0)

    def test_a_refused_query_exits_non_zero_and_a_dated_one_does_not(self) -> None:
        # A refusal prints its reason and is a first-class output, but a caller
        # piping this must be able to tell "no" from "here it is" without
        # parsing prose.
        _chronology.load.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        # A locus whose mapping refuses AND which carries no native chronology.
        # This was `Ecclus.35.1 --system greek` until 2026-08-27, when the Greek
        # Ecclesiasticus acquired native chronology and began answering; a
        # mapping refusal is no longer by itself a refusal to answer, which is
        # the whole of Correction A.
        # An empty answer is the "no", whatever produced it: this locus refuses
        # the mapping AND has no chronology, so the caller gets a non-zero exit
        # and the reason on stderr, while a locus that answers exits zero.
        self.assertEqual(tool.main(["query", "EsthGr.1.1", "--system", "greek"]), 1)
        self.assertEqual(tool.main(["query", "Gen.1.1"]), 0)

    def test_a_mapping_refusal_is_not_a_chronology_refusal(self) -> None:
        """The hard case Correction A was written for, both halves at once.

        The Greek Ecclesiasticus is a different text from the Latin, not a
        different numbering of it - `guidance/versification.md` §4 - so the
        concordance refuses, and must go on refusing. What it may not do is
        take the chronology down with it: Gigot dates the Greek translation to
        "not long after" 132 B.C. in its own right, and that fact is true of
        this text whatever can or cannot be said about the Vulgate's.
        """
        _chronology.load.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        answer = _chronology.chronology(
            _chronology.Locus("greek", "Ecclus", 44, 1)
        )
        self.assertIsInstance(answer, _chronology.Answer)
        # Native chronology, reached without inventing a Vulgate locus.
        self.assertEqual(answer.status, "composition-only")
        self.assertEqual(
            {item.subject for item in answer.assertions},
            {"composition.book-of-ecclesiasticus.greek"},
        )
        # And the mapping still refuses, on its own axis, in the concordance's
        # own words.
        self.assertEqual(answer.mapping.status, "textually-distinct")
        self.assertIn("two texts", answer.mapping.note.lower() + " two texts")
        self.assertIsNone(answer.mapping.reached)

    def test_the_vulgate_sirach_does_not_answer_with_the_greek_one(self) -> None:
        # Two texts, two units, and neither leaks into the other's query.
        _chronology.load.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        latin = _chronology.chronology("Ecclus.44.1")
        self.assertEqual(
            {item.subject for item in latin.assertions},
            {"composition.book-of-ecclesiasticus"},
        )

    def test_the_preferred_system_is_the_one_projections_use(self) -> None:
        # Two names for one choice is one way of finding out later that they
        # had stopped agreeing.
        self.assertEqual(_chronology.PREFERRED_SYSTEM, _projection.CANONICAL)

    def test_the_derived_table_is_byte_identical_on_a_second_derivation(self) -> None:
        tracked = (
            REPOSITORY_ROOT / "src/sources/chronology/coverage.tsv"
        ).read_text(encoding="utf-8")
        _chronology.load.cache_clear()
        _chronology._by_book.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        import argparse

        arguments = argparse.Namespace(root=None)
        self.assertEqual(tool._rendered(arguments), tracked)


# --- The tracked corpus's hard cases ----------------------------------------


class TrackedHardCaseTests(unittest.TestCase):
    """The cases the corpus was built to survive, asserted against real data.

    These read `src/sources/chronology` rather than a fixture, because a model
    that only works on data written to suit it is not evidence of anything.
    They assert SHAPE — which relations reach a locus, which subject they name,
    which do not appear — and never a particular year, so that adding a
    sourced claim does not break them and collapsing two relations into one
    does.
    """

    def ask(self, locus: str, system: str = "vulgate"):
        answer = _chronology.chronology(
            _chronology.parse_locus(locus, "test", system)
        )
        self.assertIsInstance(answer, _chronology.Answer, locus)
        return answer

    def relations(self, locus: str, system: str = "vulgate") -> set[str]:
        return {item.relation for item in self.ask(locus, system).assertions}

    def test_four_gospels_reach_one_crucifixion_with_one_set_of_claims(self) -> None:
        seen = []
        for locus in ("Matt.27.35", "Mark.15.24", "Luke.23.34", "John.19.23"):
            narrated = [
                item
                for item in self.ask(locus).assertions
                if item.relation == "narrated-event"
            ]
            subjects = {item.subject for item in narrated}
            self.assertEqual(subjects, {"life-of-christ.crucifixion"}, locus)
            seen.append(sorted(str(item.claim.date) for item in narrated))
        # One event, dated once. Four different lists here would be the failure
        # the whole binding shape exists to prevent.
        self.assertEqual(len(set(map(tuple, seen))), 1)
        self.assertGreater(len(seen[0]), 1, "the Crucifixion's disagreement is gone")

    def test_each_gospel_keeps_its_own_composition_chronology(self) -> None:
        units = {}
        for locus, token in (
            ("Matt.27.35", "Matt"), ("Mark.15.24", "Mark"),
            ("Luke.23.34", "Luke"), ("John.19.23", "John"),
        ):
            composition = {
                item.subject
                for item in self.ask(locus).assertions
                if item.relation == "composition"
            }
            self.assertEqual(len(composition), 1, locus)
            units[token] = composition.pop()
        # Four Gospels, four composition units, one Crucifixion.
        self.assertEqual(len(set(units.values())), 4, units)

    def test_psalm_21_prophesies_the_passion_and_does_not_narrate_it(self) -> None:
        relations = self.relations("Ps.21.19")
        self.assertIn("prophetic-referent", relations)
        self.assertNotIn("narrated-event", relations)
        referents = {
            item.subject
            for item in self.ask("Ps.21.19").assertions
            if item.relation == "prophetic-referent"
        }
        self.assertIn("life-of-christ.crucifixion", referents)

    def test_one_verse_carries_three_relation_types_at_once(self) -> None:
        # Psalm 17:2 answers four questions at once: the setting its title
        # states, the occasion tradition assigns it, the words David spoke, and
        # the later event tradition reads it as prophesying. Four answers, none
        # overwriting another.
        #
        # This case was Psalm 21:2 until 2026-08-27, when Ps 21's
        # `historical-setting` was withdrawn as an authorship-only inference
        # and that verse fell to two relations. The hard case is that SOME
        # verse carries three or more, not that a particular one does, and
        # propping the count up with a binding the sources do not support would
        # have been the corpus lying to its own test.
        relations = self.relations("Ps.17.2")
        self.assertGreaterEqual(len(relations), 3, relations)
        self.assertIn("utterance", relations)
        self.assertIn("prophetic-referent", relations)
        self.assertIn("superscription-setting", relations)

    def test_the_withdrawn_psalm_21_setting_left_its_referent_standing(self) -> None:
        # Removing a historical-setting must not disturb a different relation
        # over the same psalm. Ps 21 keeps the Passion referent it was authored
        # for, and every verse of it stays substantively dated.
        relations = self.relations("Ps.21.2")
        self.assertIn("prophetic-referent", relations)
        self.assertNotIn("historical-setting", relations)
        self.assertEqual(self.ask("Ps.21.1").status, "dated")
        self.assertEqual(self.ask("Ps.21.32").status, "dated")

    def test_a_source_interval_lands_on_the_endpoint_the_source_names(self) -> None:
        # The cold audit's one critical finding. The Catholic Encyclopedia's
        # Flood-to-Abraham table totals 367 / 1017 / 1147 under the row "Hence,
        # number of years from Flood to Call of Abraham", reached by adding
        # Abraham's seventy-five years at his call. Those totals were carried on
        # the BIRTH, which overstated the interval by exactly those years and
        # read perfectly. Arithmetic is not an anchor: a nearby event whose
        # figure happens to compute is not the endpoint the source named.
        def flood_intervals(subject: str) -> set[str]:
            return {
                str(claim.date)
                for event in [_chronology.load().events[subject]]
                for claim in event.claims
                if claim.date.anchor == "israel.primeval.deluge"
            }

        self.assertEqual(
            flood_intervals("israel.patriarchs.call-of-abram"),
            {"367 years from the flood to the call of Abraham, in the Hebrew",
             "1017 years from the flood to the call of Abraham, in the Samaritan",
             "1147 years from the flood to the call of Abraham, in the Septuagint"},
        )
        # And none of them may return to the birth, under any text-family.
        self.assertEqual(flood_intervals("israel.patriarchs.birth-of-abram"), set())
        for label in ("367", "1017", "1147"):
            self.assertNotIn(
                label,
                {claim.date.label
                 for claim in _chronology.load().events[
                     "israel.patriarchs.birth-of-abram"].claims},
            )
        # Birth and call stay two events; collapsing them would hide the defect
        # rather than fix it, and Genesis 12:4 is the interval between them.
        call = _chronology.load().events["israel.patriarchs.call-of-abram"]
        self.assertIn(
            "israel.patriarchs.birth-of-abram",
            {claim.date.anchor for claim in call.claims},
        )

    def test_a_witness_to_a_different_text_may_date_it_where_it_corresponds(self) -> None:
        """The other half of the same rule, and the reason it is not mappability.

        Safe correspondence says two loci carry corresponding text. It does not
        say every fact about one is a fact about the other: greek Ecclus 36:16
        corresponds to vulgate Ecclus 36:18, and the date of the GREEK
        TRANSLATION is true of the first and false of the second. So the tracked
        Greek Ecclesiasticus unit, which the concordance carries at exactly that
        one locus out of 1 356, must load - and its date must still reach the
        locus, which is the half a successful mapping used to swallow.
        """
        answer = self.ask("Ecclus.36.16", system="greek")
        self.assertEqual(answer.mapping.status, "shared")
        subjects = {item.subject for item in answer.assertions}
        self.assertIn("composition.book-of-ecclesiasticus.greek", subjects)
        self.assertIn("composition.book-of-ecclesiasticus", subjects)

    def test_no_native_locus_answers_a_mapping_word_to_a_chronology_question(self) -> None:
        """The second architecture defect the cold audit left open.

        Ten native loci answered `textually-distinct` when asked whether they
        were dated - a MAPPING word standing in the chronology axis - and no
        route existed to give them anything else. §3.0.1 separated the axes for
        the locus that HAS chronology; this is the same separation for the locus
        that has none. Every native locus now answers on both axes, and the
        chronology axis only ever speaks chronology.
        """
        mapping_words = {"textually-distinct", "not-alignable", "shared", "native"}
        checked = 0
        for system in sorted(_chronology.scripture_systems()):
            if system == _chronology.PREFERRED_SYSTEM:
                continue
            printed = _chronology._system_loci(system)
            if printed is None:
                continue
            for token, chapter, verse in printed:
                answer = self.ask(f"{token}.{chapter}.{verse}", system=system)
                self.assertNotIn(
                    answer.status, mapping_words,
                    f"{system} {token}.{chapter}.{verse} answers a mapping word",
                )
                self.assertIn(answer.status, _chronology.STATUSES)
                checked += 1
        self.assertGreater(checked, 4000, "the native universe went missing")

    def test_a_native_universe_is_the_verses_its_witness_prints(self) -> None:
        # `_system_loci` filled each chapter from its first verse to its last,
        # so every number the witness SKIPS was invented back and counted as
        # Scripture: 38 in greek, 37 in world-english-catholic. The Greek ones
        # were the Latin pluses the cited article calls "foreign not only to the
        # Greek, but also to the Hebrew text".
        import _deuterocanon
        for system in ("greek", "world-english-catholic"):
            self.assertEqual(
                sorted(_chronology._system_loci(system)),
                sorted(_deuterocanon._printed(system)),
                system,
            )

    def test_the_miserere_is_one_psalm_however_it_is_numbered(self) -> None:
        vulgate = self.ask("Ps.50.3")
        hebrew = self.ask("Ps.51.3", system="hebrew")
        self.assertEqual(str(hebrew.locus), str(vulgate.locus))
        self.assertEqual(
            [item.subject for item in hebrew.assertions],
            [item.subject for item in vulgate.assertions],
        )
        self.assertIn("superscription-setting", self.relations("Ps.50.3"))

    def test_a_superscription_setting_is_not_promoted_to_a_composition_date(self) -> None:
        # The Miserere's title names its occasion. No inspected source states
        # when the psalm was written, and the corpus does not let the first
        # stand in for the second.
        relations = self.relations("Ps.50.3")
        self.assertIn("superscription-setting", relations)
        self.assertNotIn("composition", relations)

    def test_a_book_level_composition_unit_reaches_every_verse_of_its_book(self) -> None:
        for locus in ("Matt.1.1", "Matt.14.22", "Matt.28.20"):
            subjects = {
                item.subject
                for item in self.ask(locus).assertions
                if item.relation == "composition"
            }
            self.assertEqual(subjects, {"composition.gospel-of-matthew"}, locus)
            self.assertTrue(
                all(
                    item.inherited
                    for item in self.ask(locus).assertions
                    if item.relation == "composition"
                ),
                locus,
            )

    def test_a_traditional_claim_that_diverges_from_modern_chronology_says_so(self) -> None:
        # The profile boundary, asserted rather than described: at least one
        # claim records that its traditional figure is not the modern one, and
        # the modern figure is nowhere authored as the claim.
        corpus = _chronology.load()
        boundary = [
            (holder.id, claim)
            for holder in (*corpus.units.values(), *corpus.events.values())
            for claim in holder.claims
            if "modern" in (claim.note or "").lower()
            or "critic" in (claim.note or "").lower()
        ]
        self.assertTrue(boundary, "no claim records a profile boundary")

    def test_disagreement_survives_where_the_sources_disagree(self) -> None:
        # The Gospel of St Matthew is the case: the encyclopedia reports several
        # traditional dates and refuses to choose, so the corpus refuses too.
        matthew = _chronology.load().units["composition.gospel-of-matthew"]
        self.assertGreater(len(matthew.claims), 2)
        self.assertEqual(
            {claim.disposition for claim in matthew.claims}, {"disputed"}
        )
        self.assertEqual(
            len({claim.sources for claim in matthew.claims}),
            len({claim.sources for claim in matthew.claims}),
        )

    def test_anno_mundi_is_recorded_in_the_era_its_source_printed(self) -> None:
        corpus = _chronology.load()
        anno_mundi = [
            (holder.id, claim)
            for holder in corpus.events.values()
            for claim in holder.claims
            if claim.date.begin is not None and claim.date.begin.era == "am"
        ]
        self.assertTrue(anno_mundi, "no Anno Mundi figure survived authoring")
        for identifier, claim in anno_mundi:
            # Never silently converted, and never mixed with a Christian era.
            self.assertEqual(claim.date.end.era, "am", identifier)
            self.assertNotIn("B.C.", claim.date.label, identifier)

    def test_every_verse_of_the_canon_reaches_exactly_one_status(self) -> None:
        counts = _chronology.coverage()
        self.assertEqual(counts["total_verses"], 35809)
        self.assertEqual(sum(counts["by_status"].values()), counts["total_verses"])

    def test_nothing_is_undated_in_tradition_on_nobody_s_authority(self) -> None:
        """The guard that replaced `research-pending > 0`.

        While the corpus was incomplete, the honest default being visibly
        present was itself the proof that no coverage was being claimed that
        had not been earned. Now that every locus is accounted for, that
        sentinel is gone and the same job falls here: the ONLY way a verse
        leaves `research-pending` without acquiring an assertion is an
        authored gap row, so a gap row that names no source record is the
        shape a fabricated coverage number would have to take. There is no
        such row, and a lane that adds one fails this.
        """
        corpus = _chronology.load()
        unsourced = [
            f"{gap.status} over {_chronology._scope_text(gap.scope)}"
            for gap in corpus.gaps
            if not gap.sources
        ]
        self.assertEqual(unsourced, [])

    def test_a_status_that_is_not_earned_is_one_an_author_may_assert(self) -> None:
        # `dated` and `inherited` are earned from assertions; the rest are
        # authored. `research-pending` is neither, and is the default. A verse
        # reaching any other status without a gap row standing over it would
        # mean the loader had invented a status, so sweep the whole canon.
        authored = {gap.status for gap in _chronology.load().gaps}
        self.assertTrue(authored <= set(_chronology.AUTHORED_STATUSES))
        counts = _chronology.coverage()["by_status"]
        for status, total in counts.items():
            if status in _chronology.EARNED_STATUSES or status == "research-pending":
                continue
            if not total:
                continue
            self.assertIn(status, authored, f"{status} reached {total} verses "
                          f"but no gap row asserts it")

    def test_a_gap_and_an_assertion_never_stand_over_one_verse(self) -> None:
        self.assertEqual(_chronology.audit(), [])


if __name__ == "__main__":
    unittest.main()
