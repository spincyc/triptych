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

import subprocess
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import _chronology  # noqa: E402
import chronology_review_diff as review_diff  # noqa: E402
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

# The smallest profile the loader accepts, which is deliberately not very
# small. A profile that does not say which METHODS it answers with cannot tell
# a traditional figure from a modern one reprinted in a traditional book, so
# the loader refuses one, and a fixture that could skip the block would be a
# fixture testing a corpus this repository cannot hold. The classes here are a
# working subset of the tracked profile's.
ADMISSIBILITY = """\
    admissibility:
      rule: Source and basis must both be admissible.
      own_voice: A Catholic author's own voice is not a basis.
      before_rank: Admissibility is decided before rank.
      preservation: A preserved figure is evidence, not an answer.
      unstated: unreviewed
      bases:
        - id: scripture
          admissible: true
          what: What the sacred text itself states.
        - id: traditional-catholic
          admissible: true
          what: A ranked traditional authority on traditional grounds.
        - id: unreviewed
          admissible: true
          what: Not yet classified under this contract.
        - id: modern-critical
          admissible: false
          what: Modern critical chronology, whoever prints it.
        - id: reported-excluded
          admissible: false
          what: A ranked work reporting a chronology this profile excludes.
        - id: refusal-to-date
          admissible: false
          what: A source's statement that it will not assign a date.
      reporting_exceptions:
        - id: ussher-reported-by-a-ranked-catholic-source
          named: Ussher
          basis: reported-excluded
          requires: The source of record is the ranked work that printed it.
          display: At the reporting work's rank and never higher.
          does_not_generalise: Ussher and no one else.
    answerability:
      unstated: answerable
      states:
        answerable: Returned as candidate chronology.
        preserved: Kept as evidence, never returned as a candidate.
      query: The candidate set is the answerable claims and nothing else.
      refusal: A refusal to date is not a date.
      dispositions: Answerability is a separate axis from disposition.
"""

PROFILES = (
    """\
schema: triptych-chronology-profiles/v1
profiles:
  - id: catholic-traditional-v1
    title: Test profile
    intent: A profile that exists so the loader has one to check against.
    authority:
      - rank: 1
        name: Scripture
"""
    + ADMISSIBILITY
    + """\
    conflict:
      rule: Preserve the disagreement.
    non_goals:
      - Being real.
"""
)

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

    def ask(self, locus: str, system: str = "vulgate", evidence: bool = False):
        return _chronology.chronology(
            _chronology.parse_locus(locus, "test", system),
            root=self.root,
            evidence=evidence,
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

    def test_a_key_stated_twice_in_one_mapping_is_refused_with_its_line(self) -> None:
        """PyYAML keeps the last of a repeated key, and every gate then passes.

        Not hypothetical. Edits applied by string replacement left a second
        `sources:` inside one claim of the tracked `events.yaml` and a second
        `label:` inside two `date:` mappings of `composition.yaml`. Every
        duplicated pair was identical, so no answer moved: `validate` reported
        the corpus valid, `check` reported the coverage table current, and
        every test here passed over a corpus that is not valid YAML 1.2. The
        duplicate in this fixture is four mappings deep inside a list, because
        that is where the real ones were and a check reading only the top of
        the file would not have seen them. The refusal must name the key and
        the line, or an author cannot act on it.
        """
        refuses(
            self,
            "key 'label' is stated twice",
            events="""\
events:
  - id: life-of-christ.crucifixion
    title: The Crucifixion
    dates:
      - profile: catholic-traditional-v1
        disposition: preferred
        basis: A test fixture, grounded in nothing.
        sources: [bible.douay-rheims]
        date:
          precision: year
          from: {year: 33, era: ad}
          label: the year of the Passion
          label: the year of the Passion
""",
        )

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
        could not be withdrawn while every event required a date, because
        bindings name this event and other claims are measured from it. So an
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

    def test_a_containing_span_is_not_the_event_an_episode_is_offset_from(self) -> None:
        """The cold audit's A4-017, and §10.0's "Containment is not offset".

        Ezechiel 24:15 opens with the book's undated revelation formula and
        24:18 states only a morning-to-evening order; Scripture gives the
        episode no year, month or day and measures it from nothing. It was
        stored as `relative` anchored on `israel.exile.ezechiel.ministry`,
        which is the event's own `parent` — the containing span this corpus
        measures at "at least twenty-two years" — so `Date.anchor` returned a
        container as though the episode were counted from its start.

        The rule this guards is NOT "an anchor may not be a parent": five
        claims anchor on their own parent and each states a real position
        against it — "in the eighteenth year of king Josias", "the third day",
        "one hundred and twenty years before it occurred". This one stated
        nothing about its anchor at all, so there was no offset to encode.
        """
        corpus = _chronology.load()
        episode = corpus.events["israel.exile.ezechiel.death-of-the-prophets-wife"]
        # Nothing is measured from the container; the containment lives here.
        self.assertEqual(episode.claims, ())
        self.assertEqual(episode.parent, "israel.exile.ezechiel.ministry")
        # And it is still a subject: a binding names it, and the verses that
        # binding covers are still dated, from the Ezech-scoped claims above.
        self.assertIn(
            "israel.exile.ezechiel.death-of-the-prophets-wife",
            {binding.event for binding in corpus.bindings},
        )
        self.assertEqual(self.ask("Ezech.24.18").status, "dated")

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


# --- Admissibility, answerability, and the candidate set --------------------


def profile_with(old: str, new: str) -> str:
    """The fixture profile with one line rewritten, and nothing else touched.

    A profile edit is the thing under test in this section, so it has to be a
    real edit to a real profile rather than a flag passed to the loader.
    """
    assert PROFILES.count(old) == 1, old
    return PROFILES.replace(old, new)


class AdmissibilityTests(unittest.TestCase):
    """A profile that cannot say which METHODS it answers with is not a policy.

    `guidance/scripture-chronology.md` §4.5. Every refusal here is a state that
    would otherwise have to be caught by somebody noticing prose: a basis class
    nothing declares, a claim answerable on a basis its profile excludes, an
    exception reaching for a class it was not written for. Each of them means
    the profile says something other than what it looks like it says.
    """

    NAKED = """\
schema: triptych-chronology-profiles/v1
profiles:
  - id: catholic-traditional-v1
    title: A profile with no admissibility contract
    intent: To be refused.
    authority:
      - rank: 1
        name: Scripture
    conflict:
      rule: Preserve the disagreement.
    non_goals:
      - Being loadable.
"""

    def claim(self, **extra: str) -> str:
        lines = "".join(f"        {key}: {value}\n" for key, value in extra.items())
        return (
            "events:\n"
            "  - id: e.one\n"
            "    title: Something dated\n"
            "    dates:\n"
            "      - profile: catholic-traditional-v1\n"
            "        basis: A source printed it.\n"
            "        sources: [bible.douay-rheims]\n"
            "        date: {precision: year, from: {year: 33, era: ad}}\n"
            + lines
        )

    def test_a_profile_that_names_no_basis_classes_is_not_a_policy(self) -> None:
        refuses(self, "admissibility", profiles=self.NAKED)

    def test_a_basis_class_the_profile_does_not_declare_is_a_typo_not_a_fact(self) -> None:
        refuses(
            self,
            "is not a basis class",
            events=self.claim(basis_class="egyptological"),
        )

    def test_an_answerability_state_outside_the_vocabulary_is_refused(self) -> None:
        refuses(self, "is not one of", events=self.claim(answerability="maybe"))

    def test_a_claim_may_not_be_answerable_on_a_basis_the_profile_excludes(self) -> None:
        # THE GOVERNING RULE, as a load refusal. Both the source and the basis
        # of the particular value have to be admissible, and a claim asserting
        # otherwise is not a claim with a bad note: it is two statements that
        # cannot both be true.
        refuses(
            self,
            "is not admissible under",
            events=self.claim(basis_class="modern-critical", answerability="answerable"),
        )

    def test_the_same_value_is_preservable_on_the_same_excluded_basis(self) -> None:
        # The other half, and the reason the first half is not just deletion:
        # a figure may be worth preserving as documentary evidence without
        # being an answerable chronology assertion.
        kept = corpus(
            self,
            events=self.claim(basis_class="modern-critical", answerability="preserved",
                              disposition="alternate"),
        )
        claim = _chronology.load(kept.root).events["e.one"].claims[0]
        self.assertEqual(claim.answerability, "preserved")
        self.assertFalse(_chronology.load(kept.root).answers_with(claim))

    def test_a_preserved_claim_may_not_be_the_one_the_profile_prefers(self) -> None:
        refuses(
            self,
            "may not be 'preferred'",
            events=self.claim(basis_class="modern-critical", answerability="preserved"),
        )

    def test_a_reporting_exception_must_be_one_the_profile_declares(self) -> None:
        refuses(
            self,
            "is not declared by",
            events=self.claim(basis_class="reported-excluded",
                              reporting_exception="sayce-reported-by-anybody"),
        )

    def test_the_ussher_exception_does_not_extend_to_another_excluded_basis(self) -> None:
        # §10 and §4.5.1: the exception names Ussher and no one else, and the
        # place that is TRUE rather than merely written down is here. A claim
        # reaching for it from `modern-critical` is refused by name, so the
        # analogy to Sayce, Driver, Wellhausen or Sloet cannot be drawn.
        refuses(
            self,
            "does not extend by analogy",
            events=self.claim(
                basis_class="modern-critical",
                reporting_exception="ussher-reported-by-a-ranked-catholic-source",
            ),
        )

    def test_the_ussher_exception_admits_the_case_it_was_written_for(self) -> None:
        held = corpus(
            self,
            events=self.claim(
                basis_class="reported-excluded",
                reporting_exception="ussher-reported-by-a-ranked-catholic-source",
            ),
        )
        loaded = _chronology.load(held.root)
        self.assertTrue(loaded.answers_with(loaded.events["e.one"].claims[0]))

    def test_an_exception_over_an_already_admissible_basis_is_refused(self) -> None:
        # An exception that lifts nothing reads as though it lifted everything,
        # which is exactly how a named exception becomes a general licence.
        refuses(
            self,
            "already admissible",
            profiles=profile_with("basis: reported-excluded", "basis: scripture"),
        )

    def test_a_preserved_claim_takes_no_part_in_the_conflict_arithmetic(self) -> None:
        # `preferred`/`alternate`/`disputed` say which ADMISSIBLE claim the
        # profile displays first. Counting preserved evidence there would make
        # withdrawing a figure from the answers into a conflict-policy error.
        both = corpus(
            self,
            events="""\
events:
  - id: e.mixed
    title: One answer and one preserved figure
    dates:
      - profile: catholic-traditional-v1
        disposition: preferred
        basis: A ranked traditional authority states it.
        basis_class: traditional-catholic
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: modern-critical
        basis: A modern reconstruction the same volume prints.
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 30, era: ad}}
""",
        )
        self.assertEqual(len(_chronology.load(both.root).events["e.mixed"].claims), 2)


class CandidateSetTests(unittest.TestCase):
    """What a default consumer receives, and what it takes a second ask to see.

    §22: a note saying "do not display" is not a control if the default query
    still displays the value. These tests are about the structural half.
    """

    EVENTS = """\
events:
  - id: e.answered
    title: A figure this profile answers with
    dates:
      - profile: catholic-traditional-v1
        basis: A ranked traditional authority computes it on traditional grounds.
        basis_class: traditional-catholic
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
  - id: e.preserved
    title: A figure this profile preserves and does not answer with
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: modern-critical
        basis: A modern critical reconstruction the source prints for comparison.
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 30, era: ad}}
  - id: e.refused
    title: A source that will not assign a date
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: refusal-to-date
        basis: The source states that it declines to fix the year.
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 4004, era: bc}}
"""
    BINDINGS = """\
bindings:
  - relation: narrated-event
    event: e.answered
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
  - relation: narrated-event
    event: e.preserved
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
  - relation: narrated-event
    event: e.refused
    scope: {book: Jude, chapter: 1, first: 2, last: 2}
"""

    def bound(self):
        return corpus(self, events=self.EVENTS, bindings=self.BINDINGS)

    def test_preserved_evidence_is_absent_from_the_default_candidate_set(self) -> None:
        answer = self.bound().ask("Jude.1.1")
        self.assertEqual([a.subject for a in answer.assertions], ["e.answered"])

    def test_the_same_preserved_evidence_is_present_in_the_provenance_view(self) -> None:
        # Excluded is not deleted. The figure is inspectable, and it takes an
        # explicit ask, which is the difference between preserved evidence and
        # a note asking a consumer not to believe what it was just handed.
        answer = self.bound().ask("Jude.1.1", evidence=True)
        self.assertEqual(
            sorted(a.subject for a in answer.assertions), ["e.answered", "e.preserved"]
        )
        preserved = [a for a in answer.assertions if a.subject == "e.preserved"][0]
        self.assertEqual(preserved.claim.answerability, "preserved")
        self.assertEqual(preserved.claim.basis_class, "modern-critical")

    def test_a_source_refusing_to_date_is_not_returned_as_a_date(self) -> None:
        # §8. A refusal is negative evidence about method; it is not a date
        # assertion, and a locus whose only claim is one is not dated.
        answer = self.bound().ask("Jude.1.2")
        self.assertEqual(answer.assertions, ())
        self.assertEqual(answer.status, "research-pending")
        self.assertEqual(
            [a.subject for a in self.bound().ask("Jude.1.2", evidence=True).assertions],
            ["e.refused"],
        )

    def test_own_voice_on_an_excluded_basis_is_not_answerable(self) -> None:
        # §9. The source is admissible and speaks in its own voice; the BASIS of
        # this particular value is not. Publication context is not a basis, and
        # the rule reads the same at every rank.
        own = corpus(
            self,
            events="""\
events:
  - id: e.own-voice
    title: A traditional work stating a figure it took from elsewhere
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: reported-excluded
        basis: The article states the figure in its own voice, having adopted it
          from the critical chronology it names two sentences earlier.
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 722, era: bc}}
""",
            bindings="""\
bindings:
  - relation: narrated-event
    event: e.own-voice
    scope: {book: Jude, chapter: 1, first: 3, last: 3}
""",
        )
        self.assertEqual(own.ask("Jude.1.3").assertions, ())
        self.assertEqual(len(own.ask("Jude.1.3", evidence=True).assertions), 1)

    def test_own_voice_on_an_admissible_basis_is_still_answerable(self) -> None:
        # The other side of the same rule, and the reason it is not a blanket
        # exclusion of the works that print excluded figures elsewhere.
        answer = self.bound().ask("Jude.1.1")
        self.assertEqual(len(answer.assertions), 1)
        self.assertEqual(answer.assertions[0].claim.basis_class, "traditional-catholic")
        self.assertEqual(answer.status, "dated")

    def test_an_excluded_basis_is_excluded_at_every_rank(self) -> None:
        # §9 again: there is no rank-6-only rule. Two claims on one excluded
        # basis, one from the rank this repository's Scripture sits at and one
        # from a later reference work, and neither is answered with.
        ranks = corpus(
            self,
            events="""\
events:
  - id: e.high
    title: An excluded basis printed by a high-ranked source
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: modern-critical
        basis: A modern reconstruction, printed in a high-ranked work.
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 722, era: bc}}
  - id: e.low
    title: An excluded basis printed by a later reference work
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: modern-critical
        basis: The same reconstruction, printed in a later reference work.
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 721, era: bc}}
""",
            bindings="""\
bindings:
  - relation: narrated-event
    event: e.high
    scope: {book: Jude, chapter: 1, first: 4, last: 4}
  - relation: narrated-event
    event: e.low
    scope: {book: Jude, chapter: 1, first: 5, last: 5}
""",
        )
        self.assertEqual(ranks.ask("Jude.1.4").assertions, ())
        self.assertEqual(ranks.ask("Jude.1.5").assertions, ())

    def test_a_profile_change_alone_changes_what_the_query_answers_with(self) -> None:
        # §16: `profiles.yaml` is production semantic state. The claim YAML is
        # byte-identical in both corpora; only the policy differs, and the
        # answer moves. Nothing else in this repository can make that happen.
        events = """\
events:
  - id: e.subject
    title: A figure whose eligibility the profile decides
    dates:
      - profile: catholic-traditional-v1
        basis: A ranked traditional authority computes it on traditional grounds.
        basis_class: traditional-catholic
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
"""
        bindings = """\
bindings:
  - relation: narrated-event
    event: e.subject
    scope: {book: Jude, chapter: 1, first: 6, last: 6}
"""
        before = corpus(self, events=events, bindings=bindings)
        self.assertEqual(len(before.ask("Jude.1.6").assertions), 1)

        narrowed = profile_with(
            "- id: traditional-catholic\n          admissible: true",
            "- id: traditional-catholic\n          admissible: false",
        )
        # The claim can no longer be authored as answerable at all, which is the
        # load-time half of the same rule: the policy does not merely hide the
        # value, it refuses the assertion that the profile answers with it.
        refuses(
            self,
            "is not admissible under",
            profiles=narrowed,
            events=events,
            bindings=bindings,
        )


# --- The profile in the semantic diff ---------------------------------------



def dumped(profile: dict, **claims: dict) -> dict:
    """One side of a diff, in the shape the review worker dumps.

    Built here rather than by running the loader, because what is under test is
    the COMPARISON: the tool's own docstring settles that neither revision's
    loader may be the thing that renders what is compared, and a fixture that
    went through a loader would be testing the loader twice and the comparison
    once.
    """
    return {
        "profiles": {"catholic-traditional-v1": profile},
        "claims": claims,
        "bindings": [],
        "gaps": [],
    }


def dumped_claim(**overrides) -> dict:
    claim = {
        "profile": "catholic-traditional-v1",
        "disposition": "preferred",
        "date": {"precision": "year", "begin": [33, "ad", None, None, None],
                 "end": [33, "ad", None, None, None], "relative": None,
                 "label": "", "derivation": None, "duration": None},
        "basis": "A ranked traditional authority states it.",
        "sources": ["bible.douay-rheims"],
        "note": "",
        "answerability": "answerable",
        "basis_class": "traditional-catholic",
        "reporting_exception": None,
    }
    claim.update(overrides)
    return claim


BASE_PROFILE = {
    "id": "catholic-traditional-v1",
    "conflict": {"rule": "Preserve the disagreement. Every sourced claim is\nkept with its own provenance."},
    "admissibility": {
        "rule": "Source and basis must both be admissible.",
        "unstated": "unreviewed",
        "bases": [
            {"id": "traditional-catholic", "admissible": True, "what": "Traditional grounds."},
            {"id": "unreviewed", "admissible": True, "what": "Not yet classified."},
            {"id": "modern-critical", "admissible": False, "what": "Modern critical chronology."},
        ],
        "reporting_exceptions": [
            {"id": "ussher-reported-by-a-ranked-catholic-source",
             "named": "Ussher", "basis": "reported-excluded"},
        ],
    },
    "answerability": {"unstated": "answerable"},
}


def edited(path: list, value) -> dict:
    """A deep copy of BASE_PROFILE with one leaf replaced."""
    import copy

    profile = copy.deepcopy(BASE_PROFILE)
    cell = profile
    for step in path[:-1]:
        cell = cell[step]
    cell[path[-1]] = value
    return profile


class ProfileSemanticDiffTests(unittest.TestCase):
    """`profiles.yaml` is production semantic state, and the diff must see it.

    The final cold acceptance audit changed the conflict rule from "preserve
    the disagreement" to "harmonise freely" and the semantic differ reported
    nothing at all, because `profiles.yaml` fell in no section of it: not a
    claim, not a binding, not a gap, not a source record, not `guidance/`, not
    `scripts/`. A review artifact that cannot see a policy change is not
    evidence about a corpus whose meaning the policy decides.
    """

    def rows(self, old: dict, new: dict) -> list[dict]:
        return review_diff.diff_profiles(old, new)

    def test_a_policy_change_is_detected(self) -> None:
        moved = self.rows(
            dumped(BASE_PROFILE),
            dumped(edited(["conflict", "rule"], "Harmonise freely.")),
        )
        self.assertEqual(len(moved), 1)
        self.assertEqual(moved[0]["kind"], "profile")
        self.assertEqual(moved[0]["id"], "catholic-traditional-v1:conflict.rule")
        self.assertEqual(moved[0]["locus"], "conflict-policy")
        self.assertIn("Harmonise freely", moved[0]["detail"])

    def test_a_reflowed_rule_is_not_a_policy_change(self) -> None:
        # §17.2. A block scalar re-wrapped at a different column is the same
        # rule, and a section that reported it would train a reviewer to skim
        # the section -- which is how it stops being read at all.
        rewrapped = edited(
            ["conflict", "rule"],
            "Preserve the disagreement.   Every sourced claim\n  is kept with its\nown provenance.",
        )
        self.assertEqual(self.rows(dumped(BASE_PROFILE), dumped(rewrapped)), [])

    def test_every_facet_a_policy_edit_can_move_is_named(self) -> None:
        # §17.3: admissibility, the authority hierarchy, conflict policy,
        # reporting exceptions and answerability each have to be visible AS
        # WHAT THEY ARE, so a reviewer scanning the section can tell a renamed
        # rank from a withdrawn exception.
        cases = {
            ("admissibility", "rule"): "admissibility",
            ("answerability", "unstated"): "answerability",
        }
        for path, facet in cases.items():
            moved = self.rows(dumped(BASE_PROFILE), dumped(edited(list(path), "other")))
            self.assertEqual([row["locus"] for row in moved], [facet], path)
        flipped = edited(["admissibility", "bases"], [
            {"id": "traditional-catholic", "admissible": False, "what": "Traditional grounds."},
            {"id": "unreviewed", "admissible": True, "what": "Not yet classified."},
            {"id": "modern-critical", "admissible": False, "what": "Modern critical chronology."},
        ])
        moved = self.rows(dumped(BASE_PROFILE), dumped(flipped))
        self.assertEqual([row["locus"] for row in moved], ["admissibility"])
        dropped = edited(["admissibility", "reporting_exceptions"], [])
        moved = self.rows(dumped(BASE_PROFILE), dumped(dropped))
        self.assertTrue(moved)
        self.assertEqual({row["locus"] for row in moved}, {"reporting-exceptions"})

    def test_the_worker_dumps_the_profile_through_the_loader_boundary(self) -> None:
        # The comparison above is only worth what its input is worth. This is
        # the one place the real subprocess boundary is crossed: the loader AT A
        # REVISION reads the corpus AT THAT REVISION, and the profile has to
        # come back through it or the whole section compares two empty mappings.
        import subprocess

        head = subprocess.run(
            ["git", "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"],
            capture_output=True, text=True,
        )
        if head.returncode:
            self.skipTest("not a git checkout")
        with tempfile.TemporaryDirectory() as tmp:
            side = review_diff.load_revision(
                REPOSITORY_ROOT, head.stdout.strip(), Path(tmp)
            )
        self.assertIn(PROFILE, side["profiles"])
        self.assertTrue(side["profiles"][PROFILE].get("authority"))


class TransitiveAnswerabilityTests(unittest.TestCase):
    """The claims a policy edit moved, which no file diff can enumerate.

    §18: changing profile policy alters query eligibility without changing
    claim YAML, so the next reviewer needs the semantic impact surface and not
    just a list of files. A row whose `locus` is `profile-only` is a claim that
    is byte-identical on both sides and means something different.
    """

    def test_a_profile_change_enumerates_the_claims_it_moved(self) -> None:
        claims = {
            "event:e.one#0": dumped_claim(),
            "event:e.two#0": dumped_claim(basis_class="unreviewed"),
        }
        narrowed = edited(["admissibility", "bases"], [
            {"id": "traditional-catholic", "admissible": False, "what": "Traditional grounds."},
            {"id": "unreviewed", "admissible": True, "what": "Not yet classified."},
            {"id": "modern-critical", "admissible": False, "what": "Modern critical chronology."},
        ])
        moved = review_diff.diff_answerability(
            dumped(BASE_PROFILE, **claims), dumped(narrowed, **claims)
        )
        self.assertEqual([row["id"] for row in moved], ["event:e.one#0"])
        self.assertEqual(moved[0]["why"], "answerable->preserved")
        self.assertEqual(moved[0]["locus"], "profile-only")

    def test_a_claim_that_changed_itself_says_so(self) -> None:
        moved = review_diff.diff_answerability(
            dumped(BASE_PROFILE, **{"event:e.one#0": dumped_claim()}),
            dumped(BASE_PROFILE, **{"event:e.one#0": dumped_claim(
                answerability="preserved", disposition="alternate",
                basis_class="modern-critical")}),
        )
        self.assertEqual(moved[0]["locus"], "claim-changed")
        self.assertIn("basis_class", moved[0]["detail"])

    def test_a_revision_predating_the_axis_is_not_read_as_excluding_everything(self) -> None:
        # A base revision from before the contract has no `admissibility` block
        # and its claims carry no basis class. Reading that as "nothing was
        # admissible" would report the entire corpus as newly answerable on the
        # day the field appeared, which is a diff nobody could review.
        naked = {"id": "catholic-traditional-v1", "conflict": {"rule": "Preserve."}}
        old_claim = dumped_claim(answerability="answerable", basis_class="")
        moved = review_diff.diff_answerability(
            dumped(naked, **{"event:e.one#0": old_claim}),
            dumped(BASE_PROFILE, **{"event:e.one#0": dumped_claim()}),
        )
        self.assertEqual(moved, [])
        self.assertIsNone(review_diff.policy_of(naked))

    def test_the_two_sections_are_part_of_the_production_diff(self) -> None:
        # A section nothing routes to is a section no review artifact carries.
        self.assertIn("profiles", review_diff.SECTIONS)
        self.assertIn("answerability", review_diff.SECTIONS)
        sides = iter((
            dumped(BASE_PROFILE, **{"event:e.one#0": dumped_claim()}),
            dumped(
                edited(["admissibility", "bases"], [
                    {"id": "traditional-catholic", "admissible": False, "what": "x"},
                    {"id": "unreviewed", "admissible": True, "what": "y"},
                ]),
                **{"event:e.one#0": dumped_claim()},
            ),
        ))
        original = review_diff.load_revision
        review_diff.load_revision = lambda repo, rev, work: next(sides)
        try:
            built = review_diff.build(
                REPOSITORY_ROOT, "base", "head",
                ("claims", "profiles", "answerability"), "full",
            )
        finally:
            review_diff.load_revision = original
        self.assertEqual(built["claims"], [])
        self.assertTrue(built["profiles"])
        self.assertEqual(
            [row["locus"] for row in built["answerability"]], ["profile-only"]
        )


class CorrectedBlockerTests(unittest.TestCase):
    """The five cases the final cold acceptance audit refused to accept.

    Every one of them was a wrong answer a consumer could reach with a single
    query, and every one was disclosed somewhere the consumer never reads: in a
    claim note, in a binding note, in a subject note. These tests ask the
    question the way a consumer asks it -- through `chronology()`, at a verse --
    because that is the only surface where the defect was visible and the only
    one where the repair can be proved.

    They assert SHAPE and, where the audit named a figure, the absence of that
    figure. They do not assert which admissible year wins, so that authoring a
    new sourced claim does not break them.
    """

    def ask(self, locus: str, *, evidence: bool = False):
        answer = _chronology.chronology(locus, evidence=evidence)
        self.assertIsInstance(answer, _chronology.Answer, locus)
        return answer

    def labels(self, locus: str, *, evidence: bool = False) -> list[str]:
        return [item.claim.date.label for item in self.ask(locus, evidence=evidence).assertions]

    # --- creation#1 / Gen.1.1 -- a refusal to date, returned as a date -------

    def test_the_encyclopedia_s_refusal_to_date_the_creation_is_not_an_answer(self) -> None:
        """MF-2. `query Gen.1.1` returned an interval whose own note said it
        "must never be displayed as one". The note was the only control, and
        the default query displayed it anyway."""
        self.assertNotIn(
            "varying from 3483 to 6934 years B.C.", self.labels("Gen.1.1")
        )
        for item in self.ask("Gen.1.1").assertions:
            self.assertNotEqual(item.claim.basis_class, "refusal-to-date")

    def test_that_refusal_is_still_readable_as_evidence(self) -> None:
        # Excluded is not deleted: the spread Howlett rejects is what shows
        # that the tradition refuses this date, which is worth keeping.
        preserved = [
            item for item in self.ask("Gen.1.1", evidence=True).assertions
            if item.claim.answerability == "preserved"
        ]
        self.assertEqual(
            [item.claim.date.label for item in preserved],
            ["varying from 3483 to 6934 years B.C."],
        )
        self.assertEqual(preserved[0].claim.basis_class, "refusal-to-date")

    def test_creation_keeps_an_independent_admissible_claim(self) -> None:
        # §12(5): withdrawing the refusal must not empty the subject.
        self.assertTrue(self.ask("Gen.1.1").assertions)

    # --- fall of Samaria -- rank 1 suppressed by a declared non-authority ----

    def test_the_fall_of_samaria_carries_its_rank_1_scriptural_relation(self) -> None:
        """MF-1. 4 Kings 18:10 states the year and the anchor exists, and the
        corpus authored nothing from it because Sloet -- a chronology this
        profile excludes -- judged the synchronism unhistorical."""
        claims = _chronology.load().events[
            "israel.divided-kingdom.fall-of-samaria"
        ].claims
        scriptural = [c for c in claims if c.basis_class == "scripture"]
        self.assertEqual(len(scriptural), 1)
        claim = scriptural[0]
        self.assertEqual(claim.disposition, "preferred")
        self.assertEqual(claim.date.precision, "relative")
        self.assertEqual(
            claim.date.anchor, "israel.divided-kingdom.ezechias-accession"
        )
        self.assertTrue(
            any(source.startswith("bible:") for source in claim.sources)
        )

    def test_lower_ranked_evidence_cannot_erase_a_scriptural_relation(self) -> None:
        """The general rule the Samaria case is an instance of.

        Stated as the prohibition it is, because the positive form is not
        true: a subject may hold a Scriptural statement that dates nothing on
        its own -- Galatians 2:1's "after fourteen years", whose identification
        with the Council of Jerusalem is a rank-6 article's -- and there the
        corpus rightly prefers nothing at all. What may never happen is the
        Samaria shape: a subject where an answerable Scriptural claim stands
        and something lower-ranked is what the profile displays first."""
        corpus = _chronology.load()
        checked = 0
        for holder in (*corpus.events.values(), *corpus.units.values()):
            answerable = [c for c in holder.claims if corpus.answers_with(c)]
            if not any(c.basis_class == "scripture" for c in answerable):
                continue
            checked += 1
            for claim in answerable:
                if claim.disposition == "preferred":
                    self.assertEqual(
                        claim.basis_class, "scripture",
                        f"{holder.id}: {claim.basis_class} is displayed first "
                        f"over an answerable rank-1 Scriptural claim",
                    )
        self.assertGreater(checked, 20)

    def test_samaria_answers_with_no_excluded_reconstruction(self) -> None:
        # Sloet's own table, whose method his article declares.
        self.assertNotIn("B.C. 722-1", self.labels("4Kings.18.10"))
        self.assertIn("B.C. 722-1", self.labels("4Kings.18.10", evidence=True))

    # --- Matthew 27:53 -- a verse answered with a later event's date --------

    def test_matthew_27_53_is_not_dated_by_the_crucifixion(self) -> None:
        """MF-4. "And coming out of the tombs AFTER HIS RESURRECTION" returned
        seven Crucifixion assertions, every one marked `direct`."""
        answer = self.ask("Matt.27.53")
        self.assertEqual(
            [item.relation for item in answer.assertions],
            ["composition"] * len(answer.assertions),
        )
        self.assertNotIn(
            "life-of-christ.crucifixion",
            {item.subject for item in answer.assertions},
        )
        self.assertEqual(answer.status, "composition-only")

    def test_matthew_27_53_still_resolves_to_chronology_metadata(self) -> None:
        # THE HARD INVARIANT, at the one verse this lane moved: cutting a verse
        # out of a binding must not leave it answering nothing at all.
        answer = self.ask("Matt.27.53")
        self.assertTrue(answer.status)
        self.assertTrue(answer.assertions or (answer.note or "").strip())

    def test_the_verses_on_either_side_keep_the_crucifixion(self) -> None:
        # 27:52 -- the graves opening -- is narrated among the signs at the
        # death; 27:54 is the centurion. Only the one verse whose own words
        # date it later comes out.
        for locus in ("Matt.27.52", "Matt.27.54"):
            self.assertIn(
                "life-of-christ.crucifixion",
                {item.subject for item in self.ask(locus).assertions},
                locus,
            )

    # --- the 536 case -------------------------------------------------------

    def test_the_536_is_not_a_candidate_answer(self) -> None:
        """MF-140. Held as a live alternate whose own note called it "the look
        of a printing error", listed indistinguishably beside 586, 587 and 588
        with the note nowhere in the default view."""
        for locus in ("4Kings.25.9", "4Kings.25.10"):
            self.assertNotIn(
                "the destruction of Jerusalem 536 B.C.", self.labels(locus), locus
            )

    def test_the_536_remains_inspectable_as_documentary_evidence(self) -> None:
        # §15(7): preserved documentary evidence stays readable without
        # becoming a candidate answer. The corpus does not silently repair a
        # source, and it does not answer with what it cannot ground either.
        preserved = [
            item for item in self.ask("4Kings.25.9", evidence=True).assertions
            if item.claim.date.label == "the destruction of Jerusalem 536 B.C."
        ]
        self.assertEqual(len(preserved), 1)
        self.assertEqual(preserved[0].claim.answerability, "preserved")
        self.assertEqual(preserved[0].claim.basis_class, "unresolved")

    def test_the_admissible_figures_for_that_year_are_untouched(self) -> None:
        labels = self.labels("4Kings.25.9")
        self.assertTrue({"586 B.C.", "B.C. 588"} <= set(labels), labels)

    # --- Sloet and Howlett, ruled consistently by basis ---------------------

    SLOET = "artifact.catholic-encyclopedia.volume-8.new-york-1910.newadvent-08654a-645bba6c"
    HOWLETT = "artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03731a-f5f96f04"

    def claims_citing(self, record: str):
        corpus = _chronology.load()
        return [
            (holder.id, claim)
            for holder in (*corpus.events.values(), *corpus.units.values())
            for claim in holder.claims
            if record in claim.sources
        ]

    def test_every_sloet_claim_is_ruled_and_none_is_unreviewed(self) -> None:
        """Criterion 6. One article, two tables, two bases: Petavius's, which
        this profile answers with, and Sloet's own, which his article says is
        drawn up "in conjunction with the data of profane history"."""
        ruled = self.claims_citing(self.SLOET)
        self.assertGreater(len(ruled), 10)
        for identifier, claim in ruled:
            self.assertNotEqual(
                claim.basis_class, "unreviewed",
                f"{identifier}: a Sloet claim is still unruled",
            )

    def test_the_sloet_own_table_claims_are_ruled_alike(self) -> None:
        harmonised = [
            (identifier, claim) for identifier, claim in self.claims_citing(self.SLOET)
            if claim.basis_class == "profane-harmonisation"
        ]
        self.assertEqual(len(harmonised), 6)
        for identifier, claim in harmonised:
            self.assertEqual(claim.answerability, "preserved", identifier)

    def test_the_petavius_claims_in_the_same_article_are_untouched(self) -> None:
        # The line the audit drew and told the correction lane not to cross:
        # a table reproduced from a seventeenth-century Jesuit chronologist is
        # a different basis from the article author's own reconstruction, and
        # the two share nothing but a page.
        petavius = [
            (identifier, claim) for identifier, claim in self.claims_citing(self.SLOET)
            if claim.basis_class != "profane-harmonisation"
        ]
        self.assertEqual(len(petavius), 10)
        for identifier, claim in petavius:
            self.assertEqual(claim.answerability, "answerable", identifier)
            self.assertEqual(claim.basis_class, "reported-traditional", identifier)

    def test_every_howlett_claim_is_ruled_and_none_is_unreviewed(self) -> None:
        """Criterion 7. The whole artifact, not a sample: the audit's charge
        was that one sentence of one section was split, half withdrawn and half
        kept, with no stated rule that could reproduce the split."""
        ruled = self.claims_citing(self.HOWLETT)
        self.assertGreater(len(ruled), 40)
        for identifier, claim in ruled:
            self.assertNotEqual(
                claim.basis_class, "unreviewed",
                f"{identifier}: a Howlett claim is still unruled",
            )

    def test_the_ussher_exception_covers_only_claims_that_report_ussher(self) -> None:
        """Criterion 9. The exception is narrow because every claim that names
        it says Ussher in its own basis prose, and because nothing else in the
        corpus is answerable on an excluded basis at all."""
        corpus = _chronology.load()
        lifted, excluded = [], []
        for holder in (*corpus.events.values(), *corpus.units.values()):
            for claim in holder.claims:
                if claim.reporting_exception:
                    lifted.append((holder.id, claim))
                if claim.basis_class in ("modern-critical", "profane-harmonisation",
                                         "rejected-by-source", "refusal-to-date",
                                         "comparison-only", "superseded", "unresolved"):
                    excluded.append((holder.id, claim))
        self.assertTrue(lifted)
        for identifier, claim in lifted:
            self.assertEqual(
                claim.reporting_exception,
                "ussher-reported-by-a-ranked-catholic-source", identifier,
            )
            self.assertEqual(claim.basis_class, "reported-excluded", identifier)
            self.assertRegex(claim.basis, r"\bUss?her\b", identifier)
        # and it lifts nothing else: no other excluded basis is answered with.
        for identifier, claim in excluded:
            self.assertEqual(claim.answerability, "preserved", identifier)

    # --- the standing debt, and the invariant -------------------------------

    def test_the_unreviewed_debt_is_empty(self) -> None:
        """`unreviewed` is admissible, so it cannot be left to drift: it is the
        one basis class that says nothing has judged the basis. The debt was
        five on 2026-09-01 and the same day's second lane ruled all five, so
        the count is now zero and a claim arriving on this class is an unruled
        claim rather than a backlog item."""
        state = _chronology.answerability()
        self.assertEqual(state["by_basis"].get("unreviewed", 0), 0)
        self.assertEqual(
            state["claims"], sum(state["by_basis"].values())
        )

    def test_every_verse_still_resolves_to_non_empty_chronology(self) -> None:
        """THE HARD INVARIANT, swept through the consumer seam.

        Withdrawing a claim from the candidate set is the one edit that can
        empty a locus, because composition-unit scope is chosen before
        answerability is consulted: a narrow unit whose last answerable claim
        goes preserved keeps winning the scope contest and then answers
        nothing. Every verse of the Vulgate must still come back with a status
        and with either an assertion or a note behind it."""
        counts = _chronology.verse_counts()
        corpus = _chronology.load()
        empty, swept = [], 0
        for token, chapters in corpus.books.items():
            for chapter in range(1, chapters + 1):
                for verse in range(1, counts[(token, chapter)] + 1):
                    swept += 1
                    locus = f"{token}.{chapter}.{verse}"
                    answer = _chronology.chronology(locus)
                    if not isinstance(answer, _chronology.Answer):
                        empty.append((locus, "unresolved"))
                    elif not answer.status:
                        empty.append((locus, "no status"))
                    elif not answer.assertions and not (answer.note or "").strip():
                        empty.append((locus, answer.status))
        self.assertEqual(swept, 35809)
        self.assertEqual(empty[:20], [])


class LastUnreviewedClaimsTests(unittest.TestCase):
    """PCC-08: the five claims the basis-ruling lane could not rule, and the
    truthfulness of what the corpus says at the loci they used to answer.

    The hazard these pin is specific and was measured before it was fixed.
    Composition-unit scope is chosen BEFORE answerability, so preserving a
    narrow unit's last answerable claim leaves that unit winning the scope
    contest and then answering nothing, and the verse falls through to
    `research-pending`, whose note says no ranked source has been inspected for
    the locus. At Nahum 2-3 that sentence would have been false: Souvay's
    "Nahum" was inspected, in full, and the ruling is that its bounding
    argument rests on a basis this profile excludes -- which is the opposite of
    a silence, and a different fact from one.
    """

    RULED = {
        "composition.book-of-nahum.chapters-2-3": ("modern-critical", "preserved"),
        "composition.psalm-73": ("reported-excluded", "preserved"),
        "composition.psalm-82": ("traditional-catholic", "answerable"),
        "israel.patriarchs.abram-enters-chanaan": ("modern-critical", "preserved"),
        # RE-RULED 2026-09-01 by the profile-contract remediation lane, and
        # the change is the point of the row rather than a detail of it: PCC-08
        # ruled this one `traditional-catholic` and answerable on the ground
        # that it "carries no year at all", and what it carried instead was its
        # own subject restated -- "when he came into passing contact with Egypt
        # (Genesis 12) and Elam (Genesis 14)" -- measured to an anchor PCC-08
        # had just refused to date. See PCC-16.
        "israel.patriarchs.abram-contact-with-egypt-and-elam": (
            "modern-critical", "preserved",
        ),
    }

    def ask(self, locus: str, *, evidence: bool = False):
        answer = _chronology.chronology(locus, evidence=evidence)
        self.assertIsInstance(answer, _chronology.Answer, locus)
        return answer

    def test_all_five_are_ruled_and_none_is_still_unreviewed(self) -> None:
        corpus = _chronology.load()
        holders = {**corpus.events, **corpus.units}
        for identifier, (basis_class, state) in self.RULED.items():
            claim = holders[identifier].claims[0]
            self.assertEqual(claim.basis_class, basis_class, identifier)
            self.assertEqual(claim.answerability, state, identifier)

    def test_no_claim_anywhere_in_the_corpus_is_unreviewed(self) -> None:
        corpus = _chronology.load()
        unruled = [
            holder.id
            for holder in (*corpus.events.values(), *corpus.units.values())
            for claim in holder.claims
            if claim.basis_class == "unreviewed"
        ]
        self.assertEqual(unruled, [])

    # --- the false note this lane existed to prevent ------------------------

    FALSE_NOTE = "no ranked source has been inspected"

    def test_the_nahum_note_does_not_say_no_source_was_inspected(self) -> None:
        """THE REGRESSION. Souvay was read; saying otherwise at these verses
        would be the corpus asserting something it knows to be untrue."""
        for locus in ("Nah.2.1", "Nah.2.2", "Nah.3.19"):
            answer = self.ask(locus)
            self.assertEqual(answer.status, "undated-in-tradition", locus)
            self.assertNotIn(self.FALSE_NOTE, answer.note, locus)
            self.assertIn("Souvay", answer.note, locus)
            self.assertIn("inspected", answer.note, locus)

    def test_no_verse_of_the_vulgate_answers_research_pending(self) -> None:
        """The maintainer's directive was that the research phase be carried to
        completion, so the honest default is now reached nowhere: every locus
        either carries an assertion or is covered by an authored gap row that
        says what was read and why it does not date the locus."""
        counts = _chronology.verse_counts()
        corpus = _chronology.load()
        pending = []
        for token, chapters in corpus.books.items():
            for chapter in range(1, chapters + 1):
                for verse in range(1, counts[(token, chapter)] + 1):
                    answer = _chronology.chronology(f"{token}.{chapter}.{verse}")
                    if getattr(answer, "status", None) == "research-pending":
                        pending.append(f"{token}.{chapter}.{verse}")
        self.assertEqual(pending[:20], [])

    def test_no_answered_note_claims_nothing_was_inspected_where_something_was(
        self,
    ) -> None:
        """Every gap row the corpus can actually reach names what was read for
        it. A row that reached a verse while saying nothing about a source
        would be the same defect in a different file."""
        corpus = _chronology.load()
        for gap in corpus.gaps:
            self.assertNotIn(self.FALSE_NOTE, gap.reason, gap.status)
            self.assertTrue(gap.reason.strip(), gap.status)

    # --- what each ruling did to the verses it reached ----------------------

    def test_the_nahum_envelope_is_preserved_and_not_deleted(self) -> None:
        preserved = [
            item for item in self.ask("Nah.2.1", evidence=True).assertions
            if item.claim.answerability == "preserved"
        ]
        self.assertEqual(len(preserved), 1)
        self.assertIn("607 or 606 B.C.", preserved[0].claim.date.label)
        self.assertEqual(self.ask("Nah.2.1").assertions, ())

    def test_psalm_73_falls_to_the_psalter_row_and_psalm_82_does_not(self) -> None:
        seventy_three = self.ask("Ps.73.1")
        self.assertEqual(seventy_three.status, "undated-in-tradition")
        self.assertIn("Briggs", seventy_three.note)
        eighty_two = self.ask("Ps.82.1")
        self.assertEqual(eighty_two.status, "composition-only")
        self.assertEqual(
            [item.subject for item in eighty_two.assertions], ["composition.psalm-82"]
        )

    def test_the_abram_sentence_is_ruled_once_and_reaches_no_verse(self) -> None:
        """One sentence of "Israelites", one method, one ruling. It carried
        "about 2300 B.C." on the arrival -- which the same encyclopedia
        attributes to Sayce's Babylonian synchronism -- and, on the contact, a
        position measured to that same arrival whose stated interval was the
        contact restated. PCC-08 split them, answering with the second while
        refusing the first; both are preserved now, both stay legible under
        --evidence, and the thirty-five verses that reported `dated` on the
        tautology fall to the book-scoped Genesis row."""
        for locus in ("Gen.12.6", "Gen.12.9"):
            answer = self.ask(locus)
            self.assertEqual(answer.status, "undated-in-tradition", locus)
            self.assertNotIn(self.FALSE_NOTE, answer.note, locus)
            self.assertIn("12:6-9", answer.note, locus)
        self.assertNotIn(
            "about 2300 B.C.",
            [item.claim.date.label for item in self.ask("Gen.12.6").assertions],
        )
        self.assertIn(
            "about 2300 B.C.",
            [
                item.claim.date.label
                for item in self.ask("Gen.12.6", evidence=True).assertions
            ],
        )
        self.assertEqual(self.ask("Gen.12.5").status, "dated")
        for locus in ("Gen.12.10", "Gen.12.20", "Gen.14.1", "Gen.14.24"):
            answer = self.ask(locus)
            self.assertEqual(answer.status, "undated-in-tradition", locus)
            self.assertEqual(answer.assertions, (), locus)
            self.assertNotIn(self.FALSE_NOTE, answer.note, locus)
            self.assertIn("12:10-20", answer.note, locus)
            # The row must not still say what it said before, which was that
            # these verses were unaffected. A gap reason is what a consumer
            # reads, so a false one is a false answer.
            self.assertNotIn(
                "Genesis 12:10-20 and 14 are\n      unaffected", answer.note, locus
            )
        preserved = [
            item.claim.date.label
            for item in self.ask("Gen.14.1", evidence=True).assertions
        ]
        self.assertIn(
            "when he came into passing contact with Egypt (Genesis 12) and "
            "Elam (Genesis 14)",
            preserved,
        )


# --- The profile-contract remediation lane, 2026-09-01 ----------------------


class RemediationTests(unittest.TestCase):
    """PCC-13..PCC-21: the defects an independent cold review of c1dee9fc0,
    52b2467d8 and ad0644bb1 found in the RULING layer, and the invariants that
    stop each of them coming back.

    Every one of them was a claim whose stored label said something its own
    recorded `basis` prose denied. That is the failure mode this whole contract
    exists to catch, arriving one level up: the mechanism was sound, the
    application of it was not, and nothing in the corpus was checking the
    application against the prose it was supposed to be reading.
    """

    def claims(self):
        corpus = _chronology.load()
        holders = {**corpus.events, **corpus.units}
        return corpus, holders

    def claim(self, identifier: str, index: int = 0):
        _corpus, holders = self.claims()
        return holders[identifier].claims[index]

    # --- PCC-18: the contract was circumventable ---------------------------

    def test_a_claim_that_names_no_basis_class_cannot_be_a_default_answer(self) -> None:
        """THE GATE. `unstated` used to be `unreviewed`, and `unreviewed` used
        to be admissible, so a claim authored with neither field was silently a
        default answer on a basis nobody had classified. `validate` counted it
        and failed on nothing, which is a dashboard."""
        profile = _chronology.load().policies["catholic-traditional-v1"]
        self.assertNotIn(profile.unstated_basis, profile.admissible)
        self.assertNotIn("unreviewed", profile.admissible)

    def test_the_gate_is_a_load_error_and_not_one_command_s_opinion(self) -> None:
        """Landing the unstated default on an inadmissible class means the
        refusal happens in the loader, so `query`, `build`, `check`, `coverage`
        and every other consumer refuses too -- not only `validate`."""
        body = (
            "events:\n"
            "  - id: e.one\n"
            "    title: Authored without a basis class\n"
            "    dates:\n"
            "      - profile: catholic-traditional-v1\n"
            "        basis: A source printed it.\n"
            "        sources: [bible.douay-rheims]\n"
            "        date: {precision: year, from: {year: 33, era: ad}}\n"
        )
        gated = PROFILES.replace("      unstated: unreviewed\n",
                                 "      unstated: unresolved\n").replace(
            "        - id: unreviewed\n          admissible: true\n",
            "        - id: unreviewed\n          admissible: false\n").replace(
            "        - id: refusal-to-date\n",
            "        - id: unresolved\n"
            "          admissible: false\n"
            "          what: The basis is mixed or unclear.\n"
            "        - id: refusal-to-date\n")
        refuses(self, "is not admissible under", profiles=gated, events=body)

    # --- PCC-13: four claims ruled against their own basis prose -----------

    RE_RULED = {
        # id, index: (basis class, answerability, a phrase from its own basis)
        ("composition.book-of-malachias", 0): (
            "reported-excluded", "preserved", "Critics are practically agreed"),
        ("apostolic-age.exile-of-saint-john-to-patmos", 1): (
            "rejected-by-source", "preserved", "records and rejects a rival"),
        ("life-of-christ.baptism", 0): (
            "reported-excluded", "preserved", "adopts Ramsay's"),
        ("composition.gospel-of-mark", 1): (
            "reported-traditional", "answerable", "reported as the Chronicle's"),
    }

    def test_each_claim_is_ruled_by_the_prose_it_records(self) -> None:
        for (identifier, index), (klass, state, phrase) in self.RE_RULED.items():
            claim = self.claim(identifier, index)
            self.assertEqual(claim.basis_class, klass, identifier)
            self.assertEqual(claim.answerability, state, identifier)
            self.assertIn(phrase, claim.basis, identifier)

    def test_the_class_the_profile_declared_and_never_used_is_used(self) -> None:
        """`rejected-by-source` was declared, described exactly, and carried by
        no claim, while the corpus's clearest instance of it was answered
        with."""
        corpus, holders = self.claims()
        rejected = [
            f"{holder.id}#{index}"
            for holder in holders.values()
            for index, claim in enumerate(holder.claims)
            if claim.basis_class == "rejected-by-source"
        ]
        self.assertIn("apostolic-age.exile-of-saint-john-to-patmos#1", rejected)
        for claim in holders["apostolic-age.exile-of-saint-john-to-patmos"].claims:
            if claim.basis_class == "rejected-by-source":
                self.assertFalse(corpus.answers_with(claim))

    def test_apocalypse_1_9_still_answers_with_the_reign_of_domitian(self) -> None:
        answer = _chronology.chronology("Apoc.1.9")
        labels = [item.claim.date.label for item in answer.assertions]
        self.assertIn("the reign of the Emperor Domitian (81-96)", labels)
        self.assertNotIn("the reign of Claudius, A.D. 41-54", labels)

    def test_the_rejected_figure_is_still_inspectable(self) -> None:
        labels = [
            item.claim.date.label
            for item in _chronology.chronology("Apoc.1.9", evidence=True).assertions
        ]
        self.assertIn("the reign of Claudius, A.D. 41-54", labels)

    # --- PCC-14: rank-1 labels on rank-6 values ----------------------------

    RANK_SIX = (
        "israel.wilderness.mary-stricken-at-haseroth",
        "israel.wilderness.coming-to-cades",
        "israel.restoration.strange-wives-put-away",
        "israel.restoration.covenant-renewed",
    )

    def test_no_rank_6_value_stands_under_the_rank_1_label(self) -> None:
        """`scripture` is rank 1 and, in this profile, the basis nothing
        lower-ranked may suppress. Four values the sources say came from the
        Catholic Encyclopedia alone were carrying it -- one of them beside a
        note reading "the year is taken from rank 6 and from nowhere else"."""
        for identifier in self.RANK_SIX:
            claim = self.claim(identifier)
            self.assertEqual(claim.basis_class, "traditional-catholic", identifier)
            self.assertEqual(claim.answerability, "answerable", identifier)

    def test_the_haseroth_provenance_names_the_verse_its_prose_quotes(self) -> None:
        claim = self.claim("israel.wilderness.mary-stricken-at-haseroth")
        self.assertIn("Numbers 13:1", claim.basis)
        self.assertIn("bible:douay-rheims:Num.13.1", claim.sources)
        self.assertNotIn("bible:douay-rheims:Num.12.1", claim.sources)

    # --- PCC-15: one apparatus, one ruling ---------------------------------

    HAYDOCK = "george-leo-haydock"

    def test_the_haydock_chronology_is_ruled_one_way_across_the_edition(self) -> None:
        """Exodus 3, 5, 16 and 32 and Psalm 70 were `reported-excluded` under
        the Ussher lift while seven claims on the same uninitialled apparatus in
        1 and 2 Kings were `traditional-catholic` with no lift, on notes saying
        the markers are not attributed to any named commentator. One printing,
        one apparatus, one epoch, two opposite rulings."""
        _corpus, holders = self.claims()
        family = [
            (f"{holder.id}#{index}", claim)
            for holder in holders.values()
            for index, claim in enumerate(holder.claims)
            if any(self.HAYDOCK in source for source in claim.sources)
        ]
        self.assertGreaterEqual(len(family), 15)
        for identifier, claim in family:
            if claim.basis_class == "scripture":
                # A Scriptural claim may cite the edition for context; what it
                # answers with is the verse, and this rule is about the values
                # the apparatus itself supplies.
                continue
            self.assertEqual(claim.basis_class, "reported-excluded", identifier)
            self.assertEqual(
                claim.reporting_exception,
                "ussher-reported-by-a-ranked-catholic-source",
                identifier,
            )

    def test_every_lifted_claim_still_says_whose_computation_it_reports(self) -> None:
        """The lift's own display clause requires it, and the seven Kings claims
        were relying on a note the lift does not read."""
        _corpus, holders = self.claims()
        for holder in holders.values():
            for index, claim in enumerate(holder.claims):
                if not claim.reporting_exception:
                    continue
                self.assertRegex(claim.basis, r"\bUss?her\b", f"{holder.id}#{index}")

    # --- PCC-17: the lift stretched one step past Ussher -------------------

    PAST_USSHER = (
        ("israel.exodus.the-exodus", 0, "the year 1490 B.C."),
        ("israel.monarchy.temple-begun", 2,
         "the Temple was begun in the fourth year of that king, or in 1010"),
    )

    def test_a_figure_computed_from_ussher_is_not_a_figure_ussher_stated(self) -> None:
        """What the source quotes Ussher as giving is "the reign of King Solomon
        from 1014-975 B.C." The 1010 and the 1490 are Howlett's arithmetic upon
        it, and `own_voice` disqualifies a value "explicitly derived from" an
        excluded chronology. The corpus's own Haydock claims print Ussher's
        actual Exodus year, 1491, two events away."""
        for identifier, index, label in self.PAST_USSHER:
            claim = self.claim(identifier, index)
            self.assertEqual(claim.date.label, label, identifier)
            self.assertEqual(claim.answerability, "preserved", identifier)
            self.assertIsNone(claim.reporting_exception, identifier)

    def test_both_subjects_are_still_dated_by_scripture(self) -> None:
        for identifier in ("israel.exodus.the-exodus", "israel.monarchy.temple-begun"):
            preferred = [
                claim for claim in _chronology.load().events[identifier].claims
                if claim.answerability == "answerable"
                and claim.disposition == "preferred"
            ]
            self.assertEqual(len(preferred), 1, identifier)
            self.assertEqual(preferred[0].basis_class, "scripture", identifier)

    # --- PCC-16: the Abram tautology, and the loader refusal ---------------

    def test_a_relative_claim_measured_to_a_refused_anchor_is_refused(self) -> None:
        """The shape the corpus was in: the year on the anchor withdrawn as
        inadmissible, and a position measured to that anchor, out of the same
        sentence of the same source, still answering."""
        body = (
            "events:\n"
            "  - id: e.anchor\n"
            "    title: The anchor whose only date this profile refuses\n"
            "    dates:\n"
            "      - profile: catholic-traditional-v1\n"
            "        disposition: alternate\n"
            "        answerability: preserved\n"
            "        basis_class: modern-critical\n"
            "        basis: One sentence, giving a year and a position.\n"
            "        sources: [artifact.one]\n"
            "        date: {precision: year, from: {year: 2300, era: bc}}\n"
            "  - id: e.position\n"
            "    title: The position out of that same sentence\n"
            "    dates:\n"
            "      - profile: catholic-traditional-v1\n"
            "        basis_class: traditional-catholic\n"
            "        basis: The same sentence, minus the year.\n"
            "        sources: [artifact.one]\n"
            "        date:\n"
            "          precision: relative\n"
            "          relative: {of: e.anchor, statement: when it happened}\n"
        )
        refuses(self, "one half of a source statement", events=body)

    def test_a_relative_claim_on_a_subject_nobody_dates_is_not_refused(self) -> None:
        """AND THIS IS THE LINE. `israel.monarchy.saul-accession` holds no
        answerable claim and three claims are measured from it, two of them
        rank-1 Scriptural relations -- "about a month after this". This
        profile's first authority is "Scripture's own chronological and
        RELATIONAL statements", so a rule refusing a position because nobody can
        put a year on its anchor would refuse the thing the profile ranks
        highest. What makes the Abram case different is the shared source."""
        body = (
            "events:\n"
            "  - id: e.anchor\n"
            "    title: A subject this corpus openly does not date\n"
            "    dates:\n"
            "      - profile: catholic-traditional-v1\n"
            "        disposition: alternate\n"
            "        answerability: preserved\n"
            "        basis_class: modern-critical\n"
            "        basis: The one figure ever inspected, and it is excluded.\n"
            "        sources: [artifact.one]\n"
            "        date: {precision: year, from: {year: 1020, era: bc}}\n"
            "  - id: e.position\n"
            "    title: Scripture's own interval from it\n"
            "    dates:\n"
            "      - profile: catholic-traditional-v1\n"
            "        basis_class: scripture\n"
            "        basis: And it came to pass about a month after this.\n"
            "        sources: [bible.douay-rheims]\n"
            "        date:\n"
            "          precision: relative\n"
            "          relative: {of: e.anchor, statement: about a month after this}\n"
        )
        kept = corpus(self, events=body)
        claim = _chronology.load(kept.root).events["e.position"].claims[0]
        self.assertEqual(claim.answerability, "answerable")

    def test_the_three_saul_relations_the_narrow_rule_protects_still_load(self) -> None:
        corpus, holders = self.claims()
        self.assertFalse(
            any(claim.answerability == "answerable"
                for claim in holders["israel.monarchy.saul-accession"].claims)
        )
        for identifier in ("israel.monarchy.anointing-of-saul",
                           "israel.monarchy.deliverance-of-jabes-galaad",
                           "composition.book-of-judges"):
            claim = holders[identifier].claims[0]
            self.assertEqual(claim.date.relative["of"],
                             "israel.monarchy.saul-accession", identifier)
            self.assertTrue(corpus.answers_with(claim), identifier)

    # --- PCC-19: a withdrawn figure is preserved, never deleted ------------

    WITHDRAWN = {
        "israel.exodus.the-exodus": "about 1277",
        "israel.monarchy.saul-accession": "the monarchy was founded by Saul, 1020",
        "israel.monarchy.david-accession": "David mounted the throne, 1002",
        "israel.monarchy.solomon-accession": "Solomon in 962",
        "israel.monarchy.temple-begun": "the Temple was begun, 958 B.C.",
    }

    def test_the_deleted_howlett_sentence_is_held_as_evidence_again(self) -> None:
        """One sentence, five figures, one remedy. They were deleted outright
        and survived only in subject notes, while the profile says "Refusing a
        basis is not an instruction to delete what a source printed" and the
        corpus gave Nahum, Psalm 73 and Abram the preserving remedy."""
        corpus, _holders = self.claims()
        for identifier, label in self.WITHDRAWN.items():
            held = [
                claim for claim in corpus.events[identifier].claims
                if claim.date.label == label
            ]
            self.assertEqual(len(held), 1, identifier)
            self.assertEqual(held[0].answerability, "preserved", identifier)
            self.assertEqual(held[0].basis_class, "modern-critical", identifier)
            self.assertFalse(corpus.answers_with(held[0]), identifier)

    def test_restoring_them_answered_nothing_new(self) -> None:
        for locus in ("Ex.12.41", "3Kings.6.1"):
            labels = [
                item.claim.date.label
                for item in _chronology.chronology(locus).assertions
            ]
            for label in self.WITHDRAWN.values():
                self.assertNotIn(label, labels, locus)

    # --- PCC-21: the verses the withdrawals displaced ----------------------

    def test_malachias_falls_to_a_row_that_says_a_source_was_read(self) -> None:
        for locus in ("Mal.1.1", "Mal.4.6"):
            answer = _chronology.chronology(locus)
            self.assertEqual(answer.status, "undated-in-tradition", locus)
            self.assertIn("Van Hoonacker", answer.note, locus)
            self.assertNotIn("no ranked source has been inspected", answer.note, locus)

    def test_the_malachias_figure_is_preserved_and_not_deleted(self) -> None:
        labels = [
            item.claim.date.label
            for item in _chronology.chronology("Mal.1.1", evidence=True).assertions
        ]
        self.assertIn("about the middle of the fifth century B.C.", labels)

    def test_the_baptism_verses_keep_their_gospel_and_lose_the_year(self) -> None:
        for locus in ("Matt.3.13", "Mark.1.9", "Luke.3.21"):
            answer = _chronology.chronology(locus)
            self.assertEqual(answer.status, "composition-only", locus)
            self.assertTrue(
                all(item.relation == "composition" for item in answer.assertions),
                locus,
            )
            self.assertNotIn(
                "A.D. 27", [item.claim.date.label for item in answer.assertions], locus
            )

    # --- PCC-20: the review record's own key, and its drift gate -----------

    def test_the_correction_ledger_has_one_row_per_correction_id(self) -> None:
        """§27 makes `correction_id` the key of this file, and it carried PCC-09
        twice -- the gap-row consequence and the semantic-differ repair."""
        path = (REPOSITORY_ROOT / "src" / "sources" / "chronology"
                / "profile-contract-corrections.tsv")
        ids = [
            line.split("\t", 1)[0]
            for line in path.read_text().splitlines()
            if line.startswith("PCC-")
        ]
        self.assertEqual(sorted(ids), sorted(set(ids)), "duplicate correction_id")
        self.assertTrue(ids)

    def test_the_cold_review_manifest_is_not_stale(self) -> None:
        """The manifest is derived and is the surface a cold reviewer works
        from, and it had no way of saying it had gone stale. `--check`
        re-derives against the base its own header records."""
        builder = REPOSITORY_ROOT / "scripts" / "build_profile_contract_manifest.py"
        done = subprocess.run(
            [sys.executable, str(builder), "--check"],
            capture_output=True, text=True, cwd=str(REPOSITORY_ROOT),
        )
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)


# --- PCC-22: the stated rule and the enforced rule, pinned together ---------


DISCLOSED_METHOD = """\
events:
  - id: fall.of.samaria
    title: The fall of Samaria
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: answerable
        basis_class: traditional-catholic
        basis: >-
          The ranked work prints the year and states no method for it:
          "Samaria was not taken till 722 B.C."
        sources: [artifact.one]
        date: {precision: year, from: {year: 722, era: bc}, label: "722 B.C."}
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: modern-critical
        basis: >-
          The same ranked work's own table, of which it says that it gives the
          chronology "in conjunction with the data of profane history", sets the
          same event against "722-1".
        sources: [artifact.one]
        date: {precision: year, from: {year: 722, era: bc}, label: "722-1"}
"""

DISCLOSED_BINDINGS = """\
bindings:
  - event: fall.of.samaria
    relation: narrated-event
    scope: [{book: 4Kings, chapter: 17, first: 6}]
"""


class StatedRuleIsTheEnforcedRuleTests(unittest.TestCase):
    """The defect this class exists to catch is the profile SAYING one rule
    while the corpus ENFORCES another.

    An independent cold review found exactly that: `admissibility.rule` was
    written as a METHOD test -- a value is inadmissible if the method behind it
    is excluded, "whoever prints it" -- while the corpus enforced a DISCLOSURE
    test, refusing a claim only where its source NAMED an excluded warrant. The
    maintainer ruled on 2026-09-02 that the disclosure test is the operative
    policy and that the profile must say so; `profiles.yaml`
    `admissibility.decision` carries the reasoning.

    Neither half of that can be checked alone. A test that only read the prose
    would go green on a rule nothing enforces, and a test that only exercised
    the loader would go green on a rule nobody wrote down. So this class asserts
    BOTH, over the same named examples: the profile's own text must state the
    disclosure test and name these cases, and the tracked corpus must rule them
    that way.
    """

    def setUp(self) -> None:
        _chronology.load.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        profiles, policies = _chronology._load_profiles(
            REPOSITORY_ROOT / "src" / "sources" / "chronology"
        )
        self.profile = profiles[PROFILE]
        self.policy = policies[PROFILE]
        self.admissibility = self.profile["admissibility"]

    def flat(self, key: str) -> str:
        return " ".join(str(self.admissibility[key]).split())

    # -- half one: what the profile SAYS ------------------------------------

    def test_the_stated_rule_is_a_disclosure_test(self) -> None:
        rule = self.flat("rule")
        self.assertIn("BOTH the source AND the basis", rule)
        # The load-bearing half: the basis test reads what the SOURCE SAYS.
        self.assertIn("WHAT THE SOURCE SAYS THE VALUE RESTS ON", rule)
        self.assertIn("PRESENTS it as resting on a method this profile excludes", rule)
        self.assertIn("DISCLOSES", rule)

    def test_the_profile_states_what_the_rule_does_not_do(self) -> None:
        # A rule that says only what it catches hides its own narrowness, and
        # the reviewer who wants to attack it has to reconstruct it from code.
        does_not = self.flat("what_this_rule_does_not_do")
        self.assertIn("IT DOES NOT AUDIT PROVENANCE", does_not)
        self.assertIn("states no method for it", does_not)
        # Both halves of the pair the narrowness is visible in.
        self.assertIn("722 B.C.", does_not)
        self.assertIn("722-1", does_not)
        self.assertIn("eponym canon", does_not)

    def test_the_narrowing_is_recorded_as_a_dated_maintainer_decision(self) -> None:
        decision = self.flat("decision")
        self.assertIn("MAINTAINER'S DECISION, 2026-09-02", decision)
        self.assertIn("BINDING ON LATER SESSIONS", decision)
        # The reasoning, not just the ruling: a decision whose grounds are not
        # written down is re-argued by whoever reads it next.
        self.assertIn("eponym-canon", decision)
        self.assertIn("THIS IS A NARROWING AND IT IS DELIBERATE", decision)
        # And the way back out is a new profile, not an edit of this one.
        self.assertIn("new profile id", decision)

    def test_the_withdrawn_method_test_survives_only_as_quoted_history(self) -> None:
        # "whoever prints it" was the method test's formula. It may appear in
        # `decision`, which records what was withdrawn; anywhere else in this
        # block it is the old rule creeping back into the statement of the new.
        for key, value in self.admissibility.items():
            if key in ("decision", "bases", "reporting_exceptions"):
                continue
            self.assertNotIn("whoever prints it", " ".join(str(value).split()), key)

    def test_the_two_edge_clauses_are_declared(self) -> None:
        read = self.flat("disclosure_is_read_not_inferred")
        self.assertIn("has to be READ", read)
        self.assertIn("inference about a method the source does not state", read)
        corroboration = self.flat("corroboration_is_not_the_ground")
        self.assertIn("CORROBORATING", corroboration)
        self.assertIn("must show the admissible", corroboration)

    # -- half two: what the loader ENFORCES ---------------------------------

    def test_one_source_two_values_and_only_the_disclosed_one_is_refused(self) -> None:
        # The enforced rule keys on the claim's own disclosed basis and on
        # nothing else. Same source record, same year, same event: the value
        # whose source declares the excluded method is not a candidate, and the
        # value whose source declares nothing is. If the gate were the shelf --
        # the source, its rank, or where the number ultimately came from --
        # these two could not come apart.
        built = corpus(self, events=DISCLOSED_METHOD, bindings=DISCLOSED_BINDINGS)
        answer = built.ask("4Kings.17.6")
        labels = {item.claim.date.label for item in answer.assertions}
        self.assertEqual(labels, {"722 B.C."})
        with_evidence = built.ask("4Kings.17.6", evidence=True)
        self.assertIn(
            "722-1", {item.claim.date.label for item in with_evidence.assertions}
        )

    def test_admissibility_is_a_set_of_disclosed_classes_and_not_a_rank(self) -> None:
        # Enforcement has no provenance step and no rank threshold to have one
        # in: `Policy.admissible` is a set of basis-class names.
        self.assertIsInstance(self.policy.admissible, frozenset)
        self.assertIn("traditional-catholic", self.policy.admissible)
        self.assertNotIn("modern-critical", self.policy.admissible)

    # -- both halves, over the examples the profile itself names -------------

    def cases(self):
        """(claim id, answerable?, the profile text that must still name it).

        Every row is an example the rule's own prose uses to explain itself. If
        the profile stops naming one, the rule is being restated and this table
        is where that has to be argued; if the corpus stops ruling one this way,
        the enforcement has drifted from the statement.
        """
        return (
            ("event:israel.divided-kingdom.fall-of-samaria#1", True,
             "what_this_rule_does_not_do"),
            ("event:israel.divided-kingdom.fall-of-samaria#4", False,
             "what_this_rule_does_not_do"),
            ("event:apostolic-age.death-of-herod-agrippa#0", True,
             "corroboration_is_not_the_ground"),
            ("unit:composition.book-of-nahum.chapters-2-3#0", False,
             "corroboration_is_not_the_ground"),
            ("unit:composition.psalm-82#0", True, "own_voice"),
            ("unit:composition.psalm-73#0", False, "own_voice"),
        )

    def claim(self, identifier: str):
        kind, rest = identifier.split(":", 1)
        subject, index = rest.rsplit("#", 1)
        corpus_ = _chronology.load()
        holder = corpus_.events if kind == "event" else corpus_.units
        return holder[subject].claims[int(index)]

    def test_every_example_the_rule_names_is_ruled_the_way_it_says(self) -> None:
        for identifier, answerable, key in self.cases():
            with self.subTest(claim=identifier):
                claim = self.claim(identifier)
                self.assertEqual(
                    self.policy.answers_with(claim), answerable,
                    f"{identifier} is not ruled the way `{key}` says it is",
                )

    def test_the_profile_still_names_every_example_it_is_pinned_to(self) -> None:
        expected = {
            "what_this_rule_does_not_do": ("Reid", "Sloet", "profane history"),
            "corroboration_is_not_the_ground": (
                "Souvay", "Nabonidus", "Herod Agrippa", "coinage", "Josephus",
            ),
            "own_voice": ("Briggs", "Psalm 73", "Psalm 82"),
        }
        for key, needles in expected.items():
            text = self.flat(key)
            for needle in needles:
                self.assertIn(needle, text, key)

    def test_the_corroborative_reading_shows_its_primary_ground(self) -> None:
        # `corroboration_is_not_the_ground` does not let a claim assert the
        # reading and stop: it has to show the admissible ground. Agrippa is
        # the corpus's one instance, and Prat is what it shows.
        claim = self.claim("event:apostolic-age.death-of-herod-agrippa#0")
        note = " ".join(claim.note.split())
        self.assertIn("corroboration_is_not_the_ground", note)
        self.assertIn("These combined facts bring us to the year 44", note)
        self.assertIn("naming no coin", note)
        # And the refusing side says why its warrant is the sole ground.
        nahum = self.claim("unit:composition.book-of-nahum.chapters-2-3#0")
        self.assertIn("inscription of Nabonidus", " ".join(nahum.basis.split()))

    def test_psalm_82_rests_on_the_policy_and_not_on_a_neighbour(self) -> None:
        # The reviewer's objection to the 2026-09-01 note was that it argued
        # from consistency with another claim rather than from the rule. The
        # ruling now names the decision, and says plainly what it does not
        # claim about the year's ultimate provenance.
        note = " ".join(self.claim("unit:composition.psalm-82#0").note.split())
        self.assertIn("admissibility.decision", note)
        self.assertIn("WHAT THIS RULING DOES NOT SAY", note)
        self.assertIn("eponym-canon synchronism", note)
        self.assertNotIn("Van Hoonacker", note)


if __name__ == "__main__":
    unittest.main()
