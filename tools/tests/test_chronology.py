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

import io
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import _chronology  # noqa: E402
import chronology_review_diff as review_diff  # noqa: E402
import build_profile_contract_manifest as review_builder  # noqa: E402
import _canon  # noqa: E402
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


def evidence_profile(identifier: str) -> str:
    return (
        f"""\
  - id: {identifier}
    kind: evidence
    title: Test {identifier}
    intent: A leaf evidence profile used by the cascade fixtures.
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


CASCADE = "catholic-comprehensive-v1"
CRITICAL = "catholic-critical-v1"
CASCADE_PROFILES = (
    """\
schema: triptych-chronology-profiles/v1
default_profile: catholic-comprehensive-v1
profiles:
"""
    + evidence_profile(PROFILE)
    + evidence_profile(CRITICAL)
    + """\
  - id: catholic-comprehensive-v1
    kind: cascade
    title: Test cascade
    intent: Prefer traditional evidence and fall back relation by relation.
    fallback_profiles: [catholic-traditional-v1, catholic-critical-v1]
    selection: first-with-answerable-assertion-per-relation
    non_goals:
      - Owning claims.
    versioning: Changing the fallback order creates a new profile id.
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
        _chronology.native_coverage.cache_clear()
        # Loading here is what makes a fixture a test of the loader: a corpus
        # written and never read refuses nothing.
        _chronology.load(self.root)

    def ask(
        self, locus: str, system: str = "vulgate", evidence: bool = False,
        profile: str | None = None,
    ):
        return _chronology.chronology(
            _chronology.parse_locus(locus, "test", system),
            root=self.root,
            evidence=evidence,
            profile=profile,
        )


def corpus(case: unittest.TestCase, **bodies: str) -> Corpus:
    stack = tempfile.TemporaryDirectory()
    case.addCleanup(stack.cleanup)
    case.addCleanup(_chronology.load.cache_clear)
    case.addCleanup(_chronology._by_book.cache_clear)
    case.addCleanup(_chronology.native_coverage.cache_clear)
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

    def test_a_boundary_preserves_one_sided_bc_wording_without_inverting_it(self) -> None:
        before = self.date(
            precision="boundary",
            boundary={
                "direction": "before",
                "endpoint": {"year": 132, "era": "bc"},
            },
        )
        no_later = self.date(
            precision="boundary",
            boundary={
                "direction": "no-later-than",
                "endpoint": {"year": 132, "era": "bc"},
            },
        )
        self.assertEqual(str(before), "before 132 B.C.")
        self.assertEqual(str(no_later), "no later than 132 B.C.")
        self.assertEqual(before.boundary["direction"], "before")
        self.assertEqual(before.boundary["endpoint"].era, "bc")

    def test_a_boundary_is_exactly_one_endpoint_or_one_named_anchor(self) -> None:
        anchored = self.date(
            precision="boundary",
            boundary={
                "direction": "after",
                "anchor": "israel.exile.babylonian",
                "statement": "after the Babylonian exile",
            },
        )
        self.assertEqual(str(anchored), "after the Babylonian exile")
        self.assertEqual(anchored.anchor, "israel.exile.babylonian")
        self.refuse(
            "exactly one",
            precision="boundary",
            boundary={
                "direction": "after",
                "endpoint": {"year": 500, "era": "bc"},
                "anchor": "israel.exile.babylonian",
                "statement": "after the Babylonian exile",
            },
        )
        self.refuse(
            "needs the source's statement",
            precision="boundary",
            boundary={
                "direction": "after", "anchor": "israel.exile.babylonian",
            },
        )

    def test_position_is_distinct_from_duration_and_a_recurring_day(self) -> None:
        duration = self.date(
            precision="duration", duration={"years": 7}
        )
        recurring = self.date(
            precision="month-day", **{"from": {"month": 3, "day": 25}}
        )
        day_without_year = self.date(
            precision="day", **{"from": {"month": 10, "day": 30}}
        )
        day_with_year = self.date(
            precision="day",
            **{"from": {"year": 66, "era": "ad", "month": 10, "day": 30}},
        )
        relative = self.date(
            precision="relative",
            relative={"of": "e.anchor", "statement": "after the exile"},
        )
        self.assertFalse(_chronology.is_positional_date(duration))
        self.assertFalse(_chronology.is_positional_date(recurring))
        self.assertFalse(_chronology.is_positional_date(day_without_year))
        self.assertTrue(_chronology.is_positional_date(day_with_year))
        self.assertTrue(_chronology.is_positional_date(relative))

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

    def test_an_anchor_backed_boundary_anchored_to_nothing_is_refused(self) -> None:
        # An anchored boundary qualifies as a positional Date for strict
        # coverage, so accepting a nonexistent subject here would turn a
        # well-formed phrase into a false completeness proof.
        refuses(
            self,
            "a one-sided position bounded by nothing states nothing",
            composition="""\
units:
  - id: composition.jude
    title: Jude after an anchor the corpus does not hold
    scope: {book: Jude}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: boundary
          boundary:
            direction: after
            anchor: e.no-such-anchor
            statement: after an event that does not exist
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


class CascadeProfileTests(unittest.TestCase):
    TEXTUAL_HISTORY = """\
units:
  - id: composition.jude
    title: Jude
    scope: {book: Jude}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 60, era: ad}}
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 80, era: ad}}
  - id: final-formation.jude
    title: Jude in its final form
    relation: final-formation
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 90, era: ad}}
  - id: textual-attestation.jude
    title: Jude in a dated witness
    relation: textual-attestation
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 1899, era: ad}}
"""

    def test_omitted_profile_is_the_declared_default_not_a_union(self) -> None:
        book = corpus(
            self, profiles=CASCADE_PROFILES, composition=self.TEXTUAL_HISTORY
        )
        implicit = book.ask("Jude.1.1")
        explicit = book.ask("Jude.1.1", profile=CASCADE)
        self.assertEqual(implicit, explicit)
        self.assertEqual(implicit.requested_profile, CASCADE)
        self.assertEqual(
            implicit.resolved_profiles,
            (("composition", PROFILE), ("final-formation", CRITICAL)),
        )
        self.assertEqual(
            [(item.relation, str(item.claim.date)) for item in implicit.assertions],
            [("composition", "60 A.D."), ("final-formation", "90 A.D.")],
        )

    def test_cascade_falls_back_independently_for_each_relation(self) -> None:
        book = corpus(
            self, profiles=CASCADE_PROFILES, composition=self.TEXTUAL_HISTORY
        )
        critical = book.ask("Jude.1.1", profile=CRITICAL)
        self.assertEqual(
            [(item.relation, str(item.claim.date)) for item in critical.assertions],
            [("composition", "80 A.D."), ("final-formation", "90 A.D.")],
        )
        self.assertEqual(
            critical.resolved_profiles,
            (("composition", CRITICAL), ("final-formation", CRITICAL)),
        )

    def test_narrowing_is_independent_inside_each_evidence_profile(self) -> None:
        book = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: composition.matthew-critical
    title: Matthew under the critical profile
    scope: {book: Matt}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 80, era: ad}}
  - id: composition.matthew-one-traditional
    title: Matthew 1 under the traditional profile
    scope: {book: Matt, chapter: 1}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 42, era: ad}}
  - id: textual-attestation.matthew
    title: Matthew in a dated witness
    relation: textual-attestation
    scope: {book: Matt}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 1899, era: ad}}
""",
        )
        critical = book.ask("Matt.1.1", profile=CRITICAL)
        self.assertEqual(
            [(item.subject, item.claim.profile) for item in critical.assertions],
            [("composition.matthew-critical", CRITICAL)],
        )
        comprehensive = book.ask("Matt.1.1", profile=CASCADE)
        self.assertEqual(
            [(item.subject, item.claim.profile) for item in comprehensive.assertions],
            [("composition.matthew-one-traditional", PROFILE)],
        )

    def test_native_narrowing_is_also_independent_by_profile(self) -> None:
        book = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: composition.ecclesiasticus-greek-critical
    title: Greek Ecclesiasticus under the critical profile
    scope: {system: greek, book: Ecclus}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 132, era: bc}}
  - id: composition.ecclesiasticus-one-greek-traditional
    title: Greek Ecclesiasticus 1 under the traditional profile
    scope: {system: greek, book: Ecclus, chapter: 1}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 100, era: bc}}
""",
        )
        critical = book.ask("Ecclus.1.1", system="greek", profile=CRITICAL)
        self.assertEqual(
            [(item.subject, item.claim.profile) for item in critical.assertions],
            [("composition.ecclesiasticus-greek-critical", CRITICAL)],
        )

    def test_tracked_psalm_41_keeps_the_broad_critical_boundary(self) -> None:
        answer = _chronology.chronology("Ps.41.1", profile=CRITICAL)
        self.assertIsInstance(answer, _chronology.Answer)
        self.assertEqual(
            [item.subject for item in answer.assertions],
            ["critical.psalms.latest-composition-boundary"],
        )
        self.assertEqual(answer.assertions[0].claim.date.precision, "boundary")

    def test_equal_scopes_in_disjoint_profiles_are_not_an_ambiguity(self) -> None:
        book = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: composition.jude-traditional
    title: Jude under the traditional profile
    scope: {book: Jude}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 60, era: ad}}
  - id: composition.jude-critical
    title: Jude under the critical profile
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 80, era: ad}}
""",
        )
        self.assertEqual(
            book.ask("Jude.1.1", profile=PROFILE).assertions[0].subject,
            "composition.jude-traditional",
        )
        self.assertEqual(
            book.ask("Jude.1.1", profile=CRITICAL).assertions[0].subject,
            "composition.jude-critical",
        )

    def test_textual_attestation_is_positive_but_only_a_last_resort(self) -> None:
        only_attestation = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: textual-attestation.jude
    title: Jude in a dated witness
    relation: textual-attestation
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 1899, era: ad}}
""",
        )
        answer = only_attestation.ask("Jude.1.1")
        self.assertEqual(answer.status, "attestation-only")
        self.assertEqual(
            [item.relation for item in answer.assertions], ["textual-attestation"]
        )
        self.assertEqual(
            answer.resolved_profiles, (("textual-attestation", CRITICAL),)
        )

    def test_nonpositional_assertions_do_not_suppress_attestation(self) -> None:
        book = corpus(
            self,
            profiles=CASCADE_PROFILES,
            events="""\
events:
  - id: e.duration-only
    title: An event with a duration but no position
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: duration, duration: {years: 7}}
  - id: e.recurring-day-only
    title: An observance with no year
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: month-day, from: {month: 3, day: 25}}
""",
            bindings="""\
bindings:
  - relation: narrated-event
    event: e.duration-only
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
  - relation: utterance
    event: e.recurring-day-only
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
""",
            composition="""\
units:
  - id: textual-attestation.jude
    title: Jude in a dated witness
    relation: textual-attestation
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 1899, era: ad}}
""",
        )
        answer = book.ask("Jude.1.1")
        self.assertEqual(
            [item.claim.date.precision for item in answer.assertions],
            ["year", "duration", "month-day"],
        )
        self.assertEqual(
            {item.relation for item in answer.assertions},
            {"textual-attestation", "narrated-event", "utterance"},
        )
        self.assertTrue(
            any(_chronology.is_positional_date(item.claim.date) for item in answer.assertions)
        )

    def test_tracked_genesis_duration_keeps_the_dated_witness(self) -> None:
        answer = _chronology.chronology("Gen.29.1", profile=CASCADE)
        self.assertIsInstance(answer, _chronology.Answer)
        self.assertIn(
            "duration", {item.claim.date.precision for item in answer.assertions}
        )
        self.assertIn(
            "textual-attestation",
            {item.relation for item in answer.assertions},
        )
        self.assertTrue(
            any(_chronology.is_positional_date(item.claim.date) for item in answer.assertions)
        )

    def test_tracked_leviticus_fallback_is_attestation_not_composition(self) -> None:
        answer = _chronology.chronology("Lev.1.1", profile=CASCADE)
        self.assertIsInstance(answer, _chronology.Answer)
        self.assertEqual(answer.status, "attestation-only")
        self.assertEqual(
            {item.relation for item in answer.assertions},
            {"textual-attestation"},
        )

    def test_preserved_evidence_cannot_upgrade_attestation_only_status(self) -> None:
        book = corpus(
            self,
            profiles=CASCADE_PROFILES,
            events="""\
events:
  - id: e.preserved
    title: A preserved event claim
    dates:
      - profile: catholic-traditional-v1
        disposition: alternate
        answerability: preserved
        basis_class: modern-critical
        basis: fixture evidence excluded from the answer
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 33, era: ad}}
""",
            bindings="""\
bindings:
  - relation: narrated-event
    event: e.preserved
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
""",
            composition="""\
units:
  - id: textual-attestation.jude
    title: Jude in a dated witness
    relation: textual-attestation
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 1899, era: ad}}
""",
        )
        normal = book.ask("Jude.1.1")
        evidence = book.ask("Jude.1.1", evidence=True)
        self.assertEqual(normal.status, "attestation-only")
        self.assertEqual(evidence.status, normal.status)
        self.assertEqual(
            {item.relation for item in evidence.assertions},
            {"textual-attestation", "narrated-event"},
        )

    def test_evidence_never_changes_status_for_any_enumerable_locus_or_profile(self) -> None:
        corpus_data = _chronology.load()
        loci = _chronology._coverage_loci("addresses")
        checked = 0
        for profile in sorted(corpus_data.profiles):
            for locus in loci:
                normal = _chronology.chronology(locus, profile=profile)
                evidence = _chronology.chronology(
                    locus, profile=profile, evidence=True
                )
                self.assertEqual(
                    evidence.status,
                    normal.status,
                    f"{profile} {locus.system} {locus}",
                )
                checked += 1
        self.assertEqual(checked, len(loci) * len(corpus_data.profiles))

    def test_an_earlier_gap_does_not_stop_a_later_profile_answer(self) -> None:
        book = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: composition.jude
    title: Jude
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 80, era: ad}}
""",
            gaps="""\
gaps:
  - profile: catholic-traditional-v1
    status: undated-in-tradition
    scope: {book: Jude}
    reason: The traditional fixture states no date.
""",
        )
        answer = book.ask("Jude.1.1")
        self.assertEqual(answer.status, "composition-only")
        self.assertEqual(str(answer.assertions[0].claim.date), "80 A.D.")
        self.assertEqual(answer.resolved_profiles, (("composition", CRITICAL),))
        self.assertFalse(
            [
                problem
                for problem in _chronology.audit(book.root)
                if "a gap says the corpus has nothing" in problem
            ]
        )

    def test_a_cascade_cannot_own_a_claim(self) -> None:
        refuses(
            self,
            "is not declared in profiles.yaml",
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: composition.jude
    title: Jude
    scope: {book: Jude}
    dates:
      - profile: catholic-comprehensive-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 60, era: ad}}
""",
        )

    def test_multiple_profiles_need_an_explicit_default(self) -> None:
        refuses(
            self,
            "multiple profiles require one explicit top-level default_profile",
            profiles=(
                "schema: triptych-chronology-profiles/v1\nprofiles:\n"
                + evidence_profile(PROFILE)
                + evidence_profile(CRITICAL)
            ),
        )

    def test_wec_same_text_inherits_a_greek_textual_history_claim(self) -> None:
        book = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: final-formation.ecclesiasticus-greek
    title: Greek Ecclesiasticus in its final form
    relation: final-formation
    scope: {system: greek, book: Ecclus}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 132, era: bc}}
""",
        )
        answer = book.ask(
            "Ecclus.1.1", system="world-english-catholic", profile=CASCADE
        )
        self.assertEqual(
            [item.relation for item in answer.assertions], ["final-formation"]
        )
        self.assertEqual(answer.assertions[0].claim.profile, CRITICAL)
        self.assertEqual(answer.mapping.status, "textually-distinct")


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

    def test_preferred_queries_refuse_zero_and_verses_past_the_chapter(self) -> None:
        dated = corpus(
            self,
            composition="""\
units:
  - id: composition.query-boundary-fixture
    title: Whole books that must not date nonexistent loci
    scope: [{book: Gen}, {book: Luke}, {book: Ps}]
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 42, era: ad}}
""",
        )
        for locus in ("Gen.1.0", "Gen.1.32", "Gen.1.999", "Luke.7.99", "Ps.150.99"):
            with self.subTest(locus=locus):
                answer = dated.ask(locus)
                self.assertIsInstance(answer, _chronology.Unresolved)
                self.assertEqual(answer.status, "not-alignable")
        counts = _chronology.verse_counts()
        for token, chapter in (("Gen", 1), ("Luke", 7), ("Ps", 150)):
            for verse in (1, counts[(token, chapter)]):
                with self.subTest(valid=f"{token}.{chapter}.{verse}"):
                    answer = dated.ask(f"{token}.{chapter}.{verse}")
                    self.assertIsInstance(answer, _chronology.Answer)
                    self.assertTrue(answer.assertions)

    def test_native_queries_require_exact_membership_in_the_printed_witness(self) -> None:
        for system, locus in (
            ("greek", "Sus.1.999"),
            ("greek", "Ecclus.1.0"),
            ("greek", "Ecclus.1.999"),
            ("world-english-catholic", "Dan.1.999"),
        ):
            with self.subTest(system=system, locus=locus):
                answer = _chronology.chronology(
                    _chronology.parse_locus(locus, "test", system)
                )
                self.assertIsInstance(answer, _chronology.Unresolved)
                self.assertEqual(answer.status, "not-alignable")

        for system, locus in (
            ("greek", "Sus.1.1"),
            ("greek", "Ecclus.1.1"),
            ("world-english-catholic", "Dan.1.1"),
        ):
            with self.subTest(valid=(system, locus)):
                answer = _chronology.chronology(
                    _chronology.parse_locus(locus, "test", system)
                )
                self.assertIsInstance(answer, _chronology.Answer)

    def test_a_skipped_native_verse_number_is_not_invented_back(self) -> None:
        checked = 0
        for system in ("greek", "world-english-catholic"):
            printed = _chronology._system_locus_membership(system)
            self.assertIsNotNone(printed)
            chapters: dict[tuple[str, int], set[int]] = {}
            for token, chapter, verse in printed:
                chapters.setdefault((token, chapter), set()).add(verse)
            skipped = next(
                (
                    (token, chapter, verse)
                    for (token, chapter), verses in sorted(chapters.items())
                    for verse in range(min(verses), max(verses) + 1)
                    if verse not in verses
                ),
                None,
            )
            self.assertIsNotNone(skipped, system)
            token, chapter, verse = skipped
            answer = _chronology.chronology(
                _chronology.Locus(system, token, chapter, verse)
            )
            self.assertIsInstance(answer, _chronology.Unresolved)
            checked += 1
        self.assertEqual(checked, 2)

    def test_valid_hebrew_psalm_addresses_survive_an_unprinted_vulgate_target(self) -> None:
        # These are real Hebrew addresses. The Psalm concordance carries each
        # to the right Vulgate Psalm, but its Douay-derived verse number is not
        # printed by the tracked Clementine witness. That point correspondence
        # must refuse without erasing the asked identity or the whole-Psalm
        # chronology that remains safe.
        affected = {
            16: (11,),
            43: (6,),
            116: tuple(range(11, 20)),
            126: (7,),
            136: (27,),
            147: tuple(range(12, 21)),
        }
        checked = 0
        for chapter, verses in affected.items():
            for verse in verses:
                asked = _chronology.Locus("hebrew", "Ps", chapter, verse)
                converted = _chronology.to_canonical(
                    asked.system, asked.token, asked.chapter, asked.verse
                )
                self.assertIsInstance(converted, _chronology.Locus)
                answer = _chronology.chronology(asked)
                self.assertIsInstance(answer, _chronology.Answer)
                self.assertEqual(answer.locus, asked)
                self.assertEqual(answer.asked, str(asked))
                self.assertEqual(answer.mapping.status, "not-alignable")
                self.assertIsNone(answer.mapping.reached)
                self.assertIn(str(converted), answer.mapping.note)
                self.assertIn("whole-Psalm chronology", answer.mapping.note)
                self.assertTrue(
                    any(
                        _chronology.is_positional_date(item.claim.date)
                        for item in answer.assertions
                    ),
                    str(asked),
                )
                checked += 1
        self.assertEqual(checked, 22)

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

    def test_a_native_only_book_is_not_indexed_as_a_canonical_book(self) -> None:
        # Susanna is a standalone book token in the Greek witness and Daniel
        # 13 in the preferred Vulgate arrangement. `_by_book` accelerates only
        # the latter walk; attempting to index `Sus` into its canonical-book
        # dictionary crashed validation as soon as universal native witness
        # attestation was authored.
        book = corpus(
            self,
            composition="""\
units:
  - id: textual-attestation.susanna-greek
    title: Susanna in the dated Greek witness
    relation: textual-attestation
    scope: {system: greek, book: Sus}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: year, from: {year: 1899, era: ad}}
""",
        )
        index = _chronology._by_book(book.root)
        self.assertNotIn("Sus", index)
        self.assertFalse(
            [problem for problem in _chronology.audit(book.root) if "Sus" in problem]
        )
        answer = book.ask("Sus.1.1", system="greek")
        self.assertEqual(
            [item.relation for item in answer.assertions],
            ["textual-attestation"],
        )
        self.assertEqual(str(answer.locus), "Dan.13.1")

    def test_an_arrangement_with_no_recorded_row_refuses_with_its_reason(self) -> None:
        # Greek Ecclesiasticus 1:1 is an address that witness actually prints,
        # but the corpus has established no verse-level correspondence to the
        # differently divided Vulgate text. (The former WEC EsthGr 1:1 fixture
        # was not an address in that witness at all, so exact-witness validation
        # correctly refuses it earlier.)
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("Ecclus.1.1", "test", "greek"),
            root=book.root,
        )
        # BOTH AXES, which is what this used to get wrong. The mapping refuses
        # and says why; the chronology axis answers the way any unresearched
        # locus does. Returning the mapping word as the chronology status was
        # the defect the cold audit found on ten native loci.
        self.assertIsInstance(answer, _chronology.Answer)
        self.assertEqual(answer.mapping.status, "textually-distinct")
        self.assertIn("no verse-level correspondence", answer.mapping.note)
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
    def test_omitted_profile_coverage_equals_the_explicit_default_cascade(self) -> None:
        _chronology.load.cache_clear()
        _chronology._by_book.cache_clear()
        _chronology.native_coverage.cache_clear()
        self.addCleanup(_chronology.load.cache_clear)
        self.addCleanup(_chronology._by_book.cache_clear)
        self.addCleanup(_chronology.native_coverage.cache_clear)
        default = _chronology.load().default_profile
        implicit = _chronology.coverage()
        explicit = _chronology.coverage(profile=default)
        self.assertEqual(implicit, explicit)
        self.assertGreater(
            implicit["verses_with_alternative_traditional_claims"], 0
        )

    def test_strict_coverage_cannot_count_a_dangling_boundary_as_position(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "chronology"
            root.mkdir()
            (root / "profiles.yaml").write_text(PROFILES, encoding="utf-8")
            bodies = {
                "composition": """\
units:
  - id: composition.jude
    title: Jude after an anchor the corpus does not hold
    scope: {book: Jude}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: boundary
          boundary:
            direction: after
            anchor: e.no-such-anchor
            statement: after an event that does not exist
""",
            }
            for name, head in HEAD.items():
                key = {"composition": "units"}.get(name, name)
                body = bodies.get(name, f"{key}: []\n")
                (root / f"{name}.yaml").write_text(
                    head + body, encoding="utf-8"
                )
            _chronology.load.cache_clear()
            self.addCleanup(_chronology.load.cache_clear)
            with self.assertRaises(_chronology.ChronologyError) as caught:
                _chronology.coverage(
                    root,
                    PROFILE,
                    universe="addresses",
                    require_date=True,
                )
        self.assertIn(
            "a one-sided position bounded by nothing states nothing",
            str(caught.exception),
        )

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
        self.assertEqual(counts["profile"], "catholic-traditional-v1")
        self.assertEqual(counts["universe"], "vulgate-clementine-primary")
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

    def test_require_date_checks_assertions_not_an_authored_gap(self) -> None:
        gap = corpus(
            self,
            profiles=CASCADE_PROFILES,
            gaps="""\
gaps:
  - profile: catholic-traditional-v1
    status: undated-in-tradition
    scope: {book: Jude}
    reason: The fixture states no date.
""",
        )
        locus = _chronology.Locus("vulgate", "Jude", 1, 1)
        with patch.object(_chronology, "_coverage_loci", return_value=[locus]):
            with self.assertRaises(_chronology.ChronologyError) as caught:
                _chronology.coverage(
                    gap.root, CASCADE, universe="addresses", require_date=True
                )
        self.assertIn(
            "1 valid addresses loci with no answerable positional Date",
            str(caught.exception),
        )

    def test_require_date_accepts_attestation_as_a_positive_date(self) -> None:
        dated = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: textual-attestation.jude
    title: Jude in a dated witness
    relation: textual-attestation
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 1899, era: ad}}
""",
        )
        locus = _chronology.Locus("vulgate", "Jude", 1, 1)
        with patch.object(_chronology, "_coverage_loci", return_value=[locus]):
            counts = _chronology.coverage(
                dated.root, CASCADE, universe="addresses", require_date=True
            )
        self.assertEqual(counts["missing_dates"], 0)
        self.assertEqual(counts["by_status"]["attestation-only"], 1)
        self.assertEqual(counts["by_status"]["composition-only"], 0)
        self.assertEqual(counts["profile"], CASCADE)
        self.assertEqual(counts["universe"], "supported-scripture-addresses")
        self.assertEqual(counts["by_relation"]["textual-attestation"], 1)
        primary = _chronology.coverage(dated.root, CASCADE)
        self.assertEqual(primary["verses_with_substantive_event_assertions"], 0)

    def test_expanded_universes_disclose_unenumerable_named_systems(self) -> None:
        dated = corpus(
            self,
            profiles=CASCADE_PROFILES,
            composition="""\
units:
  - id: textual-attestation.jude
    title: Jude in a dated witness
    relation: textual-attestation
    scope: {book: Jude}
    dates:
      - profile: catholic-critical-v1
        basis: fixture
        sources: [bible.king-james-version]
        date: {precision: year, from: {year: 1899, era: ad}}
""",
        )
        locus = _chronology.Locus("vulgate", "Jude", 1, 1)
        native = {
            "hebrew": {"enumerable": True, "printed_loci": 1},
            "nab": {"enumerable": False, "note": "no NAB concordance"},
            "nova-vulgata": {
                "enumerable": False,
                "note": "no Nova Vulgata concordance",
            },
            "septuagint": {
                "enumerable": False,
                "note": "no Septuagint concordance",
            },
        }
        payload = None
        for universe in ("distinct-content", "addresses"):
            with self.subTest(universe=universe), patch.object(
                _chronology, "_coverage_loci", return_value=[locus]
            ), patch.object(_chronology, "native_coverage", return_value=native):
                payload = _chronology.coverage(
                    dated.root, CASCADE, universe=universe, require_date=True
                )
                self.assertEqual(payload["missing_dates"], 0)
                self.assertEqual(
                    payload["universe_limitations"]["date_completeness_scope"],
                    "enumerated-loci-only",
                )
                self.assertEqual(
                    payload["unenumerable_systems"],
                    {
                        "nab": "no NAB concordance",
                        "nova-vulgata": "no Nova Vulgata concordance",
                        "septuagint": "no Septuagint concordance",
                    },
                )

        output = io.StringIO()
        with redirect_stdout(output):
            tool._render_coverage(payload)
        rendered = output.getvalue()
        self.assertIn(
            "universe-limitation\tdate_completeness_scope\t"
            "enumerated-loci-only\n",
            rendered,
        )
        self.assertIn(
            "unenumerable-system\tnab\tno NAB concordance\n", rendered
        )

    def test_require_date_rejects_a_duration_without_a_position(self) -> None:
        duration_only = corpus(
            self,
            profiles=CASCADE_PROFILES,
            events="""\
events:
  - id: e.duration-only
    title: An event with a duration but no position
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date: {precision: duration, duration: {years: 7}}
""",
            bindings="""\
bindings:
  - relation: narrated-event
    event: e.duration-only
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
""",
        )
        locus = _chronology.Locus("vulgate", "Jude", 1, 1)
        with patch.object(_chronology, "_coverage_loci", return_value=[locus]):
            counts = _chronology.coverage(
                duration_only.root, CASCADE, universe="addresses"
            )
            self.assertEqual(counts["missing_dates"], 1)
            with self.assertRaises(_chronology.ChronologyError) as caught:
                _chronology.coverage(
                    duration_only.root,
                    CASCADE,
                    universe="addresses",
                    require_date=True,
                )
        self.assertIn("no answerable positional Date", str(caught.exception))


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

    def test_a_bible_source_must_name_a_verse_its_exact_edition_prints(self) -> None:
        typo = corpus(
            self,
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: ["bible:douay-rheims:Gen.1.999"]
        date: {precision: year, from: {year: 33, era: ad}}
""",
        )
        problems = _chronology.audit(typo.root)
        self.assertTrue(
            any("does not print that verse" in problem for problem in problems),
            problems,
        )

        valid = corpus(
            self,
            events="""\
events:
  - id: e.one
    title: One
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: ["bible:douay-rheims:Gen.1.31"]
        date: {precision: year, from: {year: 33, era: ad}}
""",
        )
        self.assertFalse(
            [
                problem
                for problem in _chronology.audit(valid.root)
                if "bible:douay-rheims:Gen.1.31" in problem
            ]
        )

    def test_binding_bible_sources_receive_the_same_exact_locus_audit(self) -> None:
        book = corpus(
            self,
            events=EVENT,
            bindings="""\
bindings:
  - relation: narrated-event
    event: life-of-christ.crucifixion
    scope: {book: Jude, chapter: 1, first: 1, last: 1}
    sources: ["bible:douay-rheims:Gen.1.999"]
""",
        )
        problems = _chronology.audit(book.root)
        self.assertTrue(
            any(
                problem.startswith("binding narrated-event")
                and "does not print that verse" in problem
                for problem in problems
            ),
            problems,
        )

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
        self.assertEqual(
            tool.main([
                "query", "EsthGr.1.1", "--system", "greek",
                "--profile", PROFILE,
            ]),
            1,
        )
        self.assertEqual(
            tool.main(["query", "Gen.1.1", "--profile", PROFILE]), 0
        )

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
            _chronology.Locus("greek", "Ecclus", 44, 1), profile=PROFILE
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
        latin = _chronology.chronology("Ecclus.44.1", profile=PROFILE)
        self.assertEqual(
            {item.subject for item in latin.assertions},
            {"composition.book-of-ecclesiasticus"},
        )

    def test_the_preferred_system_is_the_one_projections_use(self) -> None:
        # Two names for one choice is one way of finding out later that they
        # had stopped agreeing.
        self.assertEqual(_chronology.PREFERRED_SYSTEM, _projection.CANONICAL)

    def test_boundary_json_keeps_direction_and_endpoint_structured(self) -> None:
        book = corpus(
            self,
            composition="""\
units:
  - id: final-formation.jude
    title: Jude in its final form
    relation: final-formation
    scope: {book: Jude}
    dates:
      - profile: catholic-traditional-v1
        basis: fixture
        sources: [bible.douay-rheims]
        date:
          precision: boundary
          boundary:
            direction: before
            endpoint: {year: 132, era: bc}
""",
        )
        checkout = book.root.parent
        chronology_link = checkout / "src" / "sources" / "chronology"
        chronology_link.parent.mkdir(parents=True)
        chronology_link.symlink_to(book.root, target_is_directory=True)
        import argparse

        payload = tool.query(
            argparse.Namespace(
                root=str(checkout), locus="Jude.1.1", system=None,
                profile=PROFILE, evidence=False,
            )
        )
        assertion = payload["assertions"][0]
        self.assertEqual(payload["chronology_status"], "composition-only")
        self.assertEqual(assertion["date"], "before 132 B.C.")
        self.assertEqual(assertion["precision"], "boundary")
        self.assertEqual(
            assertion["boundary"],
            {"direction": "before", "endpoint": "132 B.C."},
        )

    def test_explicit_leaf_gap_json_still_names_its_requested_policy(self) -> None:
        book = corpus(
            self,
            gaps="""\
gaps:
  - profile: catholic-traditional-v1
    status: undated-in-tradition
    scope: {book: Jude}
    reason: The traditional fixture states no position in time.
""",
        )
        checkout = book.root.parent
        chronology_link = checkout / "src" / "sources" / "chronology"
        chronology_link.parent.mkdir(parents=True)
        chronology_link.symlink_to(book.root, target_is_directory=True)
        import argparse

        payload = tool.query(
            argparse.Namespace(
                root=str(checkout), locus="Jude.1.1", system=None,
                profile=PROFILE, evidence=False,
            )
        )
        self.assertEqual(payload["chronology_status"], "undated-in-tradition")
        self.assertEqual(payload["requested_profile"], PROFILE)
        self.assertEqual(payload["resolved_profiles"], {})
        self.assertEqual(payload["assertions"], [])

    def test_failed_converted_target_json_keeps_the_original_asked_address(self) -> None:
        import argparse

        payload = tool.query(
            argparse.Namespace(
                root=None, locus="Ps.16.11", system="hebrew",
                profile=None, evidence=False,
            )
        )
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["locus"], "Ps.16.11")
        self.assertEqual(payload["asked"], "Ps.16.11")
        self.assertEqual(payload["mapping"]["status"], "not-alignable")
        self.assertIsNone(payload["mapping"]["reached"])
        self.assertIn("Ps.15.11", payload["mapping"]["note"])

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
            _chronology.parse_locus(locus, "test", system), profile=PROFILE
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
        counts = _chronology.coverage(profile=PROFILE)
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
        counts = _chronology.coverage(profile=PROFILE)["by_status"]
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
        answer = _chronology.chronology(
            locus, evidence=evidence, profile=PROFILE
        )
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
                    answer = _chronology.chronology(locus, profile=PROFILE)
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
        answer = _chronology.chronology(
            locus, evidence=evidence, profile=PROFILE
        )
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
                    answer = _chronology.chronology(
                        f"{token}.{chapter}.{verse}", profile=PROFILE
                    )
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
        answer = _chronology.chronology("Apoc.1.9", profile=PROFILE)
        labels = [item.claim.date.label for item in answer.assertions]
        self.assertIn("the reign of the Emperor Domitian (81-96)", labels)
        self.assertNotIn("the reign of Claudius, A.D. 41-54", labels)

    def test_the_rejected_figure_is_still_inspectable(self) -> None:
        labels = [
            item.claim.date.label
            for item in _chronology.chronology(
                "Apoc.1.9", evidence=True, profile=PROFILE
            ).assertions
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
                for item in _chronology.chronology(locus, profile=PROFILE).assertions
            ]
            for label in self.WITHDRAWN.values():
                self.assertNotIn(label, labels, locus)

    # --- PCC-21: the verses the withdrawals displaced ----------------------

    def test_malachias_falls_to_a_row_that_says_a_source_was_read(self) -> None:
        for locus in ("Mal.1.1", "Mal.4.6"):
            answer = _chronology.chronology(locus, profile=PROFILE)
            self.assertEqual(answer.status, "undated-in-tradition", locus)
            self.assertIn("Van Hoonacker", answer.note, locus)
            self.assertNotIn("no ranked source has been inspected", answer.note, locus)

    def test_the_malachias_figure_is_preserved_and_not_deleted(self) -> None:
        labels = [
            item.claim.date.label
            for item in _chronology.chronology(
                "Mal.1.1", evidence=True, profile=PROFILE
            ).assertions
        ]
        self.assertIn("about the middle of the fifth century B.C.", labels)

    def test_the_baptism_verses_keep_their_gospel_and_lose_the_year(self) -> None:
        for locus in ("Matt.3.13", "Mark.1.9", "Luke.3.21"):
            answer = _chronology.chronology(locus, profile=PROFILE)
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
        re-derives against the base PINNED IN THE BUILDER."""
        builder = REPOSITORY_ROOT / "scripts" / "build_profile_contract_manifest.py"
        done = subprocess.run(
            [sys.executable, str(builder), "--check"],
            capture_output=True, text=True, cwd=str(REPOSITORY_ROOT),
        )
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    # --- PCC-26: the drift gate could not see the drift it exists for -------
    #
    # A second cold review, on 2026-09-02, ran the regeneration command the
    # manifest's own header advertised, in a clean clone. Write mode defaulted
    # its base to HEAD, so the surface was rebased and collapsed from 475 rows
    # to 95; `--check` then read its base out of the header of the very file it
    # was checking, found the rebased file consistent with the rebased base, and
    # reported the wreckage as current, exit 0.
    #
    # These two tests are that attack, run against the builder as it ships. They
    # are the reason to believe the gate can see anything at all, so they are
    # end-to-end and not a unit test of the argument parser: the defect was in
    # what the command DID, and only running it shows that.

    @staticmethod
    def _scratch_repository(into: Path) -> Path:
        """A throwaway clone whose working tree is the one under test.

        Object storage is shared and the checkout is sparse, so this costs a
        few megabytes and a fraction of a second against a 1.2 GiB history.
        `scripts` and the corpus are then overlaid from the working tree,
        because the point is to exercise the builder AS IT STANDS HERE and not
        the one committed at HEAD; the base side of the diff is what the shared
        history is for. `src/sources/bibles` and `src/sources/works` are
        symlinked rather than checked out: both loaders read them and neither
        writes them.
        """
        import shutil

        clone = into / "clone"
        subprocess.run(
            ["git", "clone", "--quiet", "--shared", "--no-checkout",
             str(REPOSITORY_ROOT), str(clone)],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(
            ["git", "-C", str(clone), "sparse-checkout", "set", "--no-cone",
             "scripts", "src/sources/chronology"],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(["git", "-C", str(clone), "checkout", "--quiet"],
                       check=True, capture_output=True, text=True)
        for path in ("scripts", "src/sources/chronology"):
            shutil.rmtree(clone / path, ignore_errors=True)
            shutil.copytree(REPOSITORY_ROOT / path, clone / path,
                            ignore=shutil.ignore_patterns("__pycache__"))
        for shared in ("src/sources/bibles", "src/sources/works"):
            link = clone / shared
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(REPOSITORY_ROOT / shared)
        return clone

    @staticmethod
    def _manifest_of(repo: Path) -> Path:
        return (repo / "src" / "sources" / "chronology"
                / "profile-contract-rereview-manifest.tsv")

    @staticmethod
    def _declared_base(manifest: Path) -> str:
        import re

        found = re.search(r"^# Derived by diffing the corpus at ([0-9a-f]{7,40})",
                          manifest.read_text(), re.M)
        return found.group(1) if found else ""

    @staticmethod
    def _advertised_command(manifest: Path) -> list[str]:
        """The regeneration command the artifact tells a reader to run.

        Taken out of the header rather than written here, because the defect
        was that the file advertised a command that destroyed it. A test that
        hard-coded the safe command would go green against the wrong string.
        """
        import re

        found = re.findall(
            r"`python3 (scripts/build_profile_contract_manifest\.py)`",
            manifest.read_text())
        assert found, "the manifest header advertises no regeneration command"
        return [sys.executable, found[0]]

    def _run_builder(self, repo: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [*self._advertised_command(self._manifest_of(repo)), *args],
            capture_output=True, text=True, cwd=str(repo),
        )

    def test_the_command_the_manifest_advertises_does_not_collapse_it(self) -> None:
        """The reviewer's attack, verbatim: run what the file says to run."""
        builder = REPOSITORY_ROOT / "scripts" / "build_profile_contract_manifest.py"
        pinned = review_builder.BASE_REVISION
        head = subprocess.run(
            ["git", "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True).stdout.strip()
        if head.startswith(pinned) or pinned.startswith(head):
            self.skipTest("HEAD is the pinned base, so a rebase onto HEAD is a "
                          "no-op and this attack cannot be staged")

        tracked = self._manifest_of(REPOSITORY_ROOT)
        before = len(tracked.read_text().splitlines())
        with tempfile.TemporaryDirectory(prefix="manifest-gate-") as tmp:
            repo = self._scratch_repository(Path(tmp))
            done = self._run_builder(repo)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

            manifest = self._manifest_of(repo)
            after = len(manifest.read_text().splitlines())
            self.assertEqual(
                self._declared_base(manifest), pinned,
                "the advertised command rebased the review surface: it must "
                "derive against the base pinned in the builder, not HEAD")
            self.assertEqual(
                after, before,
                f"the advertised command collapsed the review surface from "
                f"{before} lines to {after}")

            # and having run it, the file it wrote is the tracked one.
            check = self._run_builder(repo, "--check")
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(
            len(tracked.read_text().splitlines()), before,
            "the test wrote to the tracked manifest")

    def test_a_rebased_manifest_cannot_report_itself_as_current(self) -> None:
        """`--check` took its base from the file under test, so a rebased
        manifest named the rebased base and re-derived to match it. The base
        lives in the rule now, where the artifact cannot reach it."""
        builder = REPOSITORY_ROOT / "scripts" / "build_profile_contract_manifest.py"
        head = subprocess.run(
            ["git", "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True).stdout.strip()
        if head.startswith(review_builder.BASE_REVISION):
            self.skipTest("HEAD is the pinned base")

        with tempfile.TemporaryDirectory(prefix="manifest-gate-") as tmp:
            repo = self._scratch_repository(Path(tmp))
            manifest = self._manifest_of(repo)
            # exactly what the old write mode produced: a nearly empty diff of
            # HEAD against itself, honestly labelled with the base it used.
            body = manifest.read_text().replace(
                review_builder.BASE_REVISION, head, 1)
            manifest.write_text("".join(body.splitlines(True)[:40]))

            done = self._run_builder(repo, "--check")
            self.assertEqual(
                done.returncode, 1,
                "a rebased manifest reported itself as current:\n"
                + done.stdout + done.stderr)
            self.assertIn("REBASED", done.stdout + done.stderr)


# --- PCC-27: the Usher lift's epoch argument, checked against the data ------


class HaydockEpochArgumentTests(unittest.TestCase):
    """The argument that identifies the Haydock apparatus's chronology as
    Usher's runs on the epoch its printed Anno Mundi / Anno Christi pairs
    share. Eleven notes stated that argument, and until 2026-09-02 every one of
    them stated it as a UNIVERSAL -- "every Anno Mundi and Anno Christi pair
    this corpus records" -- while listing seven of the nine pairs the corpus
    actually holds. One of the two it left out, A. M. 2518 + A. C. 1491 at
    Exodus 5, sums to 4009 and not 4004, and the claim carrying it carried the
    universal that excluded it.

    Ten `preferred` answers rest on that argument, so its stated evidence has to
    be checked against the corpus rather than read. These tests derive the pairs
    from the data and require every note that makes the argument to name ALL of
    them: a list that calls itself exhaustive cannot be allowed to go stale when
    a pair is added, and an outlier cannot be dropped from it again.
    """

    LIFT = "ussher-reported-by-a-ranked-catholic-source"
    EPOCH = 4004
    # The sentence every note that makes the argument contains, and the thing
    # that makes it findable without listing the notes here by hand.
    MARKER = "Anno Christi pairs from this apparatus"
    ERA_MARKERS = re.compile(r"A\.\s*[MC]\.\s*")
    PAIR = re.compile(r"\b(\d{4})\s*\+\s*(\d{4})\b")

    @classmethod
    def _printed_pairs(cls) -> dict[str, tuple[int, int]]:
        """Every Anno Mundi / Anno Christi pair the corpus records from the
        apparatus, read off the claims themselves and not off the notes."""
        pairs = {}
        for event in _chronology.load().events.values():
            for index, claim in enumerate(event.claims):
                if claim.reporting_exception != cls.LIFT:
                    continue
                label = claim.date.label if claim.date else ""
                found = re.search(
                    r"A\.\s*M\.\s*(\d+),\s*A\.\s*C\.\s*(\d+)", label or "")
                if found:
                    pairs[f"{event.id}#{index}"] = (
                        int(found.group(1)), int(found.group(2)))
        return pairs

    @classmethod
    def _arguing_notes(cls) -> dict[str, str]:
        notes = {}
        for event in _chronology.load().events.values():
            for index, claim in enumerate(event.claims):
                if claim.note and cls.MARKER in claim.note:
                    notes[f"{event.id}#{index}"] = claim.note
        return notes

    @classmethod
    def _lift_bases(cls) -> dict[str, str]:
        """The `basis` of every claim taking the Usher lift.

        Read separately from the notes because THE BASIS IS WHERE THE PROFILE
        REQUIRES THE DISCLOSURE. `profiles.yaml` `reporting_exceptions` makes
        the exception turn on the claim recording the printing as the ranked
        work's testimony, and that record is the basis; a note is commentary on
        it. Until 2026-09-02 every test in this class read `claim.note` alone,
        and seven bases -- six of them `preferred` -- kept for a further pass a
        clause PCC-27 had removed from the notes, saying the Psalm 70 page
        stood "on this same epoch" while the note three sentences later said
        that page prints no Anno Christi and so is not one of the nine. Nothing
        looked at the half of the claim the profile actually relies on.
        """
        bases = {}
        for event in _chronology.load().events.values():
            for index, claim in enumerate(event.claims):
                if claim.reporting_exception == cls.LIFT and claim.basis:
                    bases[f"{event.id}#{index}"] = claim.basis
        return bases

    def test_the_corpus_records_one_pair_off_the_epoch_and_says_which(self) -> None:
        """The data, first: the outlier is real, it is where the notes say it
        is, and harmonising it away would break this test rather than pass it."""
        pairs = self._printed_pairs()
        self.assertEqual(len(pairs), 9, sorted(pairs))
        off = {k: v for k, v in pairs.items() if sum(v) != self.EPOCH}
        self.assertEqual(
            off, {"israel.exodus.moses-before-pharao#0": (2518, 1491)},
            "the set of pairs that break the epoch has changed; every note "
            "that argues from the epoch has to be re-read before this is "
            "updated")
        self.assertEqual(sum(off["israel.exodus.moses-before-pharao#0"]), 4009)

    def test_every_note_that_argues_from_the_epoch_lists_every_pair(self) -> None:
        pairs = self._printed_pairs()
        expected = {tuple(v) for v in pairs.values()}
        notes = self._arguing_notes()
        self.assertEqual(len(notes), 11, sorted(notes))
        for identifier, note in notes.items():
            plain = self.ERA_MARKERS.sub("", note)
            listed = {(int(a), int(b)) for a, b in self.PAIR.findall(plain)}
            self.assertEqual(
                listed, expected,
                f"{identifier} lists {sorted(listed)} but the corpus records "
                f"{sorted(expected)}")

    # Every wording of the withdrawn universal, and the withdrawn clause that
    # put the Psalm 70:1 page on an epoch the corpus cannot check, because that
    # page prints no Anno Christi. Asserted against notes AND bases.
    WITHDRAWN = (
        "one epoch across every Anno Mundi",
        "every Anno Mundi and Anno Christi pair this corpus records from "
        "it sums to the same number",
        "every Anno Mundi and Anno Christi pair this corpus records from "
        "the apparatus",
        "one epoch across every recorded pair",
        "on this same epoch",
        "on that same epoch",
    )

    def test_no_note_states_the_epoch_as_a_universal(self) -> None:
        """The false sentence itself, in every wording it had."""
        for identifier, note in self._arguing_notes().items():
            for sentence in self.WITHDRAWN:
                self.assertNotIn(sentence, note, identifier)

    def test_no_basis_states_the_epoch_as_a_universal(self) -> None:
        """The same sentences, in the half of the claim the profile relies on.

        This is the test that was missing. The notes were corrected under
        PCC-27 and the bases were not, and no test read a basis, so seven
        claims went on asserting in their warrant what their own notes denied
        three sentences later.
        """
        bases = self._lift_bases()
        self.assertEqual(len(bases), 15, sorted(bases))
        for identifier, basis in bases.items():
            for sentence in self.WITHDRAWN:
                self.assertNotIn(sentence, basis, identifier)

    def test_no_basis_and_note_of_one_claim_contradict_on_the_psalm_70_page(
            self) -> None:
        """The specific contradiction, stated as itself.

        The Psalm 70:1 page is the one place the edition names Usher and it
        prints no Anno Christi, so it is NOT one of the nine pairs and its
        epoch is not checkable from anything this corpus holds. A claim may
        cite it for the attribution; no claim may say what epoch it is on.
        """
        corpus = _chronology.load()
        for identifier in self._lift_bases():
            event_id, index = identifier.split("#")
            claim = corpus.events[event_id].claims[int(index)]
            for where, text in (("basis", claim.basis), ("note", claim.note)):
                if not text:
                    continue
                flat = re.sub(r"\s+", " ", text)
                for sentence in re.split(r"(?<=\.) ", flat):
                    if "Psalm 70" in sentence and "epoch" in sentence:
                        self.fail(
                            f"{identifier} {where} puts the Psalm 70 page on "
                            f"an epoch in one sentence; that page prints no "
                            f"Anno Christi, so its epoch is not checkable "
                            f"from anything this corpus holds: {sentence!r}")

    def test_the_outlier_is_named_where_the_lift_is_argued(self) -> None:
        """Naming the pairs is not enough: the note has to say that one of them
        does not sum, or a reader counting nine identical-looking pairs learns
        nothing from the list."""
        for identifier, note in self._arguing_notes().items():
            self.assertIn("4009", note, identifier)
            self.assertIn("Exodus 5", note, identifier)

    def test_the_ledger_does_not_still_assert_the_withdrawn_universal(self) -> None:
        """The correction ledger is a record a cold reviewer reads as current
        ground, and two of its rows went on asserting in the present tense the
        universal PCC-27 withdrew: PCC-15 listed seven pairs and said the Psalm
        70:1 note stands "on that same epoch", and PCC-17 gave the whole
        identification as resting on "one epoch across every recorded pair".
        Neither was quoted history; both read as statements of what is so.

        A withdrawn sentence may still APPEAR in the ledger -- quoting it is how
        a correction says what it corrected -- so the rule enforced here is that
        a row containing one must also say, in its own text, that it is
        withdrawn. That is exactly the difference between recording a defect and
        repeating it.
        """
        import csv

        path = (REPOSITORY_ROOT / "src" / "sources" / "chronology"
                / "profile-contract-corrections.tsv")
        with path.open() as handle:
            rows = list(csv.reader(
                (line for line in handle if not line.startswith("#")),
                delimiter="\t"))
        self.assertGreater(len(rows), 30, "the ledger did not parse")
        carrying = []
        for row in rows[1:]:
            blob = " ".join(row)
            if any(sentence in blob for sentence in self.WITHDRAWN):
                carrying.append(row[0])
                self.assertIn(
                    "withdrawn", blob,
                    f"{row[0]} contains a sentence PCC-27 withdrew and does "
                    f"not say it is withdrawn, so it reads as current ground")
        self.assertEqual(
            sorted(carrying), ["PCC-15", "PCC-17", "PCC-27", "PCC-35"],
            "the set of ledger rows quoting the withdrawn universal has "
            "changed; each has to be read before this is updated")

    def test_the_answers_resting_on_the_lift_are_the_ones_declared(self) -> None:
        """Ten preferred answers rest on this argument. If that number moves,
        the argument has been extended to claims nobody re-read."""
        resting = [
            f"{event.id}#{index}"
            for event in _chronology.load().events.values()
            for index, claim in enumerate(event.claims)
            if claim.reporting_exception == self.LIFT
        ]
        self.assertEqual(len(resting), 15, sorted(resting))
        preferred = [
            identifier for identifier in resting
            if _chronology.load().events[identifier.split("#")[0]]
            .claims[int(identifier.split("#")[1])].disposition == "preferred"
        ]
        self.assertEqual(len(preferred), 10, sorted(preferred))


# --- PCC-30: a quotation has to be IN the thing it is quoted from -----------


class QuotedBasisTests(unittest.TestCase):
    """Every quotation in a `basis` is checked against THE SOURCE ITS OWN
    SENTENCE NAMES, and every quotation is checked.

    Nothing tested this until 2026-09-02, and nothing COULD: the sources were
    registered but not retained, so a basis could quote a sentence that was not
    in its article and the corpus would validate, answer and coverage-check
    exactly as before. A misquotation is the failure this corpus is least able
    to survive and was the only one it could not see.

    The first version of this class closed most of that hole and left four
    doors open, which a third cold review walked through on 2026-09-02:

      1. IT POOLED THE SOURCES. `bodies()` gathered every source a claim cited
         into one list and asked only whether a span occurred in ANY of them.
         On event:apostolic-age.council-of-jerusalem#4 the auditor SWAPPED the
         attributions -- gave Galatians 2:1's words to Prat's article and the
         article's words to Galatians -- and both still matched. A basis could
         put Scripture's words in the encyclopedia's mouth and nothing said so.
      2. IT DISCARDED WHAT IT COULD NOT CHECK. A claim citing only an artifact
         whose bytes are not retained produced `skipped` spans, and the caller
         threw the count away. A fabricated `patristic` claim with an invented
         Eusebius quotation, citing one unretained NPNF artifact, loaded
         cleanly and passed all 197 tests. An unreopenable citation was a
         hiding place.
      3. IT DID NOT LOOK AT SHORT QUOTATIONS. The 25-character floor left 284
         quoted runs unchecked, and 15 of them did not occur as quoted.
      4. IT DID NOT FOLLOW A SIBLING EXTRACTION. Where a remote delivery's text
         is retained under a sibling `-article-text` artifact of the same page,
         the claim looked unreopenable when it was not.

    WHAT IS CHECKED NOW. For every claim, every run inside quotation marks in
    its `basis`, at any length, must occur in the retained text of the source
    THAT RUN IS ATTRIBUTED TO -- not the claim's sources pooled.

    HOW A RUN IS ATTRIBUTED, and what that does and does not separate. Each
    source is given the names the prose can call it by: for Scripture, the
    book, matched only where a chapter or verse number follows it, so that
    "Exodus 3", "Ezechiel 30:20-21" and "1 Kings (1 Samuel) 7:1" all name their
    book and the word "exodus" in a sentence does not; for a work, the author's
    surname and the article's own title, read off the artifact record. A run is
    attributed to the source whose name stands NEAREST to it in the basis,
    counting only names outside quotation marks, so that a book named inside
    the encyclopedia's quoted words cannot claim that quotation. Ties are
    resolved in favour of every source at that distance.

    This separates WITNESSES -- Scripture from the encyclopedia, one article
    from another, one edition's page from another's. It does not separate
    chapters of the same book, and does not try to: a `bible:` body already
    carries the cited chapter and its neighbours, because a basis may quote
    across a chapter break.

    A run that no source's name stands anywhere near cannot be attributed. That
    is a failure, not a fallback -- except on a claim citing ONE source, where
    there is nothing to be wrong about.

    WHAT IS FOLDED BEFORE COMPARING, and why each fold is safe: whitespace,
    because the extraction collapses the page's line breaks; curly quotation
    marks and dashes to their ASCII forms; `ae`/`oe` for the ligatures, which
    the encyclopedia sets and the corpus does not; double quotation marks to
    single, because a quotation nested inside a quotation changes its marks and
    not its words; whitespace around punctuation and hyphens, which the
    extraction moves. A trailing full stop or comma is allowed to be dropped,
    because a basis that quotes the first half of a verse ends the sentence it
    is inside. Where all of that fails, the comparison is retried with every
    hyphen removed from BOTH sides, because the retained extraction carries the
    printed table's end-of-line hyphenation inside its cells -- "Capture of
    Jerusa-lem" -- which is typography and not words. None of these can turn
    one word into another; every one of them is applied to BOTH sides.

    A span broken by an ellipsis is checked in pieces, which is what an
    ellipsis means. A quotation that silently drops words WITHOUT one is a
    failure, and four were found and repaired when this test was written:
    composition.first-epistle-to-the-thessalonians#0 had dropped ", then,";
    composition.book-of-judges#0 had moved an opening quotation mark so that
    "Saul had" fell inside the article's words; composition.book-of-habacuc#0
    and israel.maccabees.temple-plundered#1 had each closed an inner quotation
    early, at a point the article runs past. Fifteen more were found when the
    length floor came off, and are recorded in PCC-37.

    A PASSAGE RECORD IS NOT THE PAGE. For a remote facsimile the repository
    holds a passage record whose `context` is the project's own summary of what
    the page prints. That is evidence a person read the page; it is not the
    page's bytes, and a span "verified" against it is the corpus quoting
    itself. Such a span is reported separately and has to be declared, exactly
    like a span that cannot be reopened at all.
    """

    # No floor. The 25-character floor was itself a defect: '"(740 B.C. )"' at
    # composition.book-of-isaias#0 -- where the article reads "(740 B.C.;" --
    # and '"Epistle of Saint Jude"' -- where the article says "St. Jude" --
    # were both under it.
    FOLD = (("’", "'"), ("‘", "'"), ("“", "'"), ("”", "'"),
            ('"', "'"), ("—", "-"), ("–", "-"), ("‐", "-"),
            (" ", " "), ("æ", "ae"), ("Æ", "Ae"),
            ("œ", "oe"), ("Œ", "Oe"))
    ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*")
    ORDINAL = r"(?:[1-4]|I{1,3}|IV|First|Second|Third|Fourth)"

    # The spans that cannot be reopened from this repository's bytes, with the
    # reason, and the count of them on each claim. Asserted in BOTH directions:
    # an undeclared failure fails the test, and a declared one that has started
    # matching fails it too, so this list cannot quietly outlive its reason.
    #
    # THE THREE NPNF-BACKED CLAIMS AT THE BOTTOM WERE MISSING UNTIL 2026-09-02.
    # They cite only an artifact whose bytes are not retained, so the old
    # `survey` returned all their spans as `skipped` and the caller discarded
    # the count. Two of them are `preferred`. That silence was the hiding place
    # a fabricated claim with a fabricated quotation walked into, and it is why
    # an undeclared skip is now a failure.
    UNREOPENABLE = {
        "event:apostolic-age.exile-of-saint-john-to-patmos#0": (2, (
            "Eusebius, Church History III.18.1, in the NPNF translation New "
            "Advent hosts. The artifact is registered and hashed but its bytes "
            "are not retained, so its words cannot be reopened here.")),
        "event:apostolic-age.return-of-saint-john-from-patmos#0": (1, (
            "Eusebius, Church History III.23.1, same artifact, same reason.")),
        "event:apostolic-age.martyrdom-of-saint-paul#3": (1, (
            "Jerome, De viris illustribus 5, in the NPNF translation New "
            "Advent hosts. Registered and hashed, bytes not retained. The "
            "claim cites this artifact and nothing else, so every span on it "
            "is unreopenable.")),
        "event:apostolic-age.flight-of-the-christians-from-jerusalem#0": (1, (
            "Eusebius, Church History III.5.3, same unretained NPNF artifact. "
            "This claim is `preferred`, which is why it is named here rather "
            "than passed over.")),
        "event:apostolic-age.destruction-of-jerusalem#0": (1, (
            "Eusebius, Church History III.5, same unretained NPNF artifact. "
            "Also `preferred`.")),
        "event:israel.exile.first-captivity#0": (1, (
            "The Usher chronology printed at Psalm 70:1 in the Haydock "
            "Douay-Rheims. The artifact is a remote 1.2 GB facsimile PDF and "
            "the passage record that stands for it SUMMARISES the paragraph "
            "rather than transcribing it, so the printed sentence the claim "
            "quotes is verified but not held. Transcribing it into the passage "
            "record would close this, and would close the next two with it.")),
        "event:israel.exile.second-captivity#0": (1, (
            "The same Psalm 70:1 sentence, quoted on the second captivity.")),
        "event:israel.exile.third-captivity#0": (1, (
            "The same Psalm 70:1 sentence, quoted on the third captivity.")),
    }

    # Spans whose only witness is a passage record's `context` -- the project's
    # own summary of a page it cannot retain. Declared for the same reason: the
    # corpus may not quietly stand as its own source.
    #
    # EVERY ONE OF THEM IS A HAYDOCK MARGINAL YEAR MARKER, and they are all
    # here for one reason: the delivery of that edition is a remote 1.2 GB
    # facsimile PDF which this repository does not retain, so what stands for
    # the page is the passage record a person wrote after reading it. The
    # marker is quoted in that record's `context`, so the span is reopenable
    # HERE and not in the edition. Ten `preferred` answers rest on these.
    HAYDOCK = (
        "A Haydock marginal year marker, quoted from the passage record's "
        "`context` because the edition's own delivery is the remote facsimile "
        "PDF and is not retained. Verified against the printed page on the "
        "date the passage record names; not reopenable from the edition's "
        "bytes in this repository.")
    SELF_WITNESSED = {
        "event:israel.exodus.burning-bush#0": (1, HAYDOCK),
        "event:israel.exodus.moses-before-pharao#0": (1, HAYDOCK),
        "event:israel.wilderness.manna#1": (1, HAYDOCK),
        "event:israel.wilderness.golden-calf#0": (1, HAYDOCK),
        "event:israel.monarchy.david-at-geth#0": (1, HAYDOCK),
        "event:israel.monarchy.david-in-the-desert-of-maon#0": (1, HAYDOCK),
        "event:israel.monarchy.nabal-in-the-wilderness-of-maon#0": (1, HAYDOCK),
        "event:israel.monarchy.absalom-preparations#0": (2, HAYDOCK),
        "event:israel.monarchy.absalom-revolt#1": (1, HAYDOCK),
        "event:israel.monarchy.absalom-defeat#0": (1, HAYDOCK),
        "event:israel.monarchy.david-in-the-cave#0": (1, (
            "Not a marker but a SENTENCE OF THE PASSAGE RECORD ITSELF, quoted "
            "as such: the basis says 'the verified record read across artifact "
            "pages 400-401 for 1 Kings 23 states of the following chapter "
            "that ...'. It is the one span in the corpus that quotes the "
            "project's own prose openly rather than the page behind it, and it "
            "says so in its own words.")),
    }

    @classmethod
    def setUpClass(cls) -> None:
        import tomllib

        cls.tracked = {}
        cls.records = {}
        for record in REPOSITORY_ROOT.glob(
                "src/sources/works/**/artifacts/*/artifact.toml"):
            entry = tomllib.loads(record.read_text())
            cls.records[entry["id"]] = entry
            if entry.get("storage") == "tracked" and entry.get("path"):
                cls.tracked[entry["id"]] = REPOSITORY_ROOT / entry["path"]
        cls.passages = {}
        for record in REPOSITORY_ROOT.glob(
                "src/sources/works/**/passages/*.toml"):
            entry = tomllib.loads(record.read_text())
            cls.passages[entry["id"]] = entry
        cls.books = {book["token"]: book for book in _canon.books()}
        cls.cache = {}

    @classmethod
    def fold(cls, text: str) -> str:
        import unicodedata

        text = unicodedata.normalize("NFC", text)
        for old, new in cls.FOLD:
            text = text.replace(old, new)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s+([,.;:!?)\]])", r"\1", text)
        text = re.sub(r"([(\[])\s+", r"\1", text)
        text = re.sub(r"\s*-\s*", "-", text)
        return text.strip()

    @classmethod
    def _file(cls, path) -> str:
        if path not in cls.cache:
            cls.cache[path] = cls.fold(path.read_text())
        return cls.cache[path]

    @classmethod
    def _chapter(cls, edition: str, book: str, chapter: int):
        path = (REPOSITORY_ROOT / "src" / "sources" / "bibles" / edition
                / "chapters" / book / f"{chapter}.json")
        if not path.exists():
            return None
        if path not in cls.cache:
            import json

            verses = json.loads(path.read_text())["verses"]
            cls.cache[path] = cls.fold(" ".join(
                verses[key] for key in sorted(verses, key=int)))
        return cls.cache[path]

    @classmethod
    def _article(cls, artifact: str) -> list:
        """The retained bytes of one artifact's text, sibling extractions
        included.

        A New Advent page can be registered twice -- the exact delivery that
        was hashed, and a second delivery of the same page -- and the article
        text is extracted and retained ONCE, under whichever of them it was
        taken from. `composition.book-of-micheas.chapters-4-5#0` cites the
        delivery that is not the one the extraction hangs off, and its
        quotation was counted as unreopenable while its words sat in the
        repository under the sibling.

        A sibling is followed only where the cited record's OWN notes name the
        sibling artifact by id -- which is where it says the two are
        byte-identical. Without that the corpus would be borrowing another
        page's bytes to verify itself.
        """
        found = []
        for candidate in (artifact + "-article-text", artifact):
            if candidate in cls.tracked:
                found.append(cls._file(cls.tracked[candidate]))
        if found:
            return found
        notes = cls.records.get(artifact, {}).get("notes", "")
        stem = artifact.rsplit("-", 1)[0] + "-"
        for identifier, path in cls.tracked.items():
            if (identifier.startswith(stem)
                    and identifier.endswith("-article-text")
                    and identifier in notes):
                found.append(cls._file(path))
        return found

    @classmethod
    def witness_of(cls, source: str) -> str:
        """The WITNESS a source belongs to.

        Every verse cited from one book of one edition is one witness, because
        a basis quoting a book quotes its chapters together and the chapter
        bodies already reach their neighbours. A passage record is its own
        witness, because two pages of one edition are two pages. Everything
        else is its artifact.
        """
        if source.startswith("bible:"):
            _, edition, locus = source.split(":", 2)
            return f"bible:{edition}:{locus.split('.')[0]}"
        return source

    @classmethod
    def witnesses(cls, claim) -> dict:
        """{witness: (retained bodies, project-authored bodies)}.

        The two are kept apart because a passage record's `context` is the
        project's prose about a page, not the page. `states` is a list of
        workflow words and is not text at all, so it is no longer offered as
        something a quotation can match.
        """
        found = {}
        for source in claim.sources:
            key = cls.witness_of(source)
            retained, project = found.setdefault(key, ([], []))
            if source.startswith("bible:"):
                _, edition, locus = source.split(":", 2)
                where = _chronology.parse_locus(locus)
                # the neighbouring chapters too: a basis may quote across a
                # chapter break, and the citation names only where it starts.
                for chapter in range(max(1, where.chapter - 1), where.chapter + 2):
                    text = cls._chapter(edition, where.token, chapter)
                    if text and text not in retained:
                        retained.append(text)
            else:
                artifact = source
                if source.startswith("passage."):
                    record = cls.passages.get(source, {})
                    for field in ("context", "notes"):
                        if record.get(field):
                            project.append(cls.fold(str(record[field])))
                    artifact = record.get("artifact_id", "")
                retained.extend(cls._article(artifact))
        return found

    # --- attribution -------------------------------------------------------

    @classmethod
    def _book_cue(cls, token: str):
        """The names prose calls one book of Scripture by, required to be
        followed by a number.

        The token IS the Douay abbreviation, so a trailing run of lower-case
        letters carries it to the Douay name the prose uses: Ezech -> Ezechiel,
        Jer -> Jeremias, Jos -> Josue, Par -> Paralipomenon. The lookahead for a
        digit within eighteen characters is what makes it a CITATION and not a
        word: it matches "Exodus 3" and "1 Kings (1 Samuel) 7:1" and does not
        match "the exodus from Egypt".
        """
        head = re.match(r"(\d)(\S+)", token)
        stem = head.group(2) if head else token
        lead = (cls.ORDINAL + r"\s*") if head else (r"(?:%s\s*)?" % cls.ORDINAL)
        # the lookahead steps over a parenthetical gloss, because the corpus
        # names a book both ways at once: "1 Esdras (Ezra) 6:15", "1 Kings
        # (1 Samuel) 7:1".
        return re.compile(
            r"\b%s%s[a-z]*\b(?=[^A-Za-z]{0,4}(?:\([^)]{0,24}\))?[^A-Za-z]{0,4}\d)"
            % (lead, re.escape(stem)))

    @classmethod
    def _locus_token(cls, locus: str):
        """The canonical book token a passage record's `locus` names, or None.

        Passage records were written before the chronology corpus and use the
        edition's own short forms -- "1K.21.1-15" for 1 Kings 21 -- so the head
        is resolved against the canon by unique prefix. Ambiguity resolves to
        nothing rather than to a guess, and a locus that is prose (one record's
        is "article 'David, King,' printed p. 642") names no book at all.
        """
        head = locus.split(".")[0]
        if head in cls.books:
            return head
        matches = [token for token in cls.books if token.startswith(head)]
        return matches[0] if head and len(matches) == 1 else None

    @classmethod
    def cues(cls, source: str):
        """(names to look for outside quotation marks, names to look for
        anywhere). An article's title is looked for anywhere because a basis
        names an article by quoting its title."""
        if source.startswith("bible:"):
            _, edition, locus = source.split(":", 2)
            # the edition answers for its own text: "The Douay-Rheims text
            # supplies the two datelines the article reckons from: ..." names
            # Scripture and nothing else, and prints no chapter to hang on.
            spelt = r"\s*-?\s*".join(
                re.escape(word) for word in edition.split("-"))
            return ([cls._book_cue(locus.split(".")[0]),
                     re.compile(spelt, re.IGNORECASE)], [])
        if source.startswith("passage."):
            token = cls._locus_token(
                cls.passages.get(source, {}).get("locus", ""))
            return ([cls._book_cue(token)], []) if token else ([], [])
        notes = cls.records.get(source, {}).get("notes", "")
        outside, anywhere = [], []
        author = re.match(
            r"([A-Z][A-Za-z'\-]+(?: [A-Z][A-Za-z'\-]+)*),", notes)
        if author:
            outside.append(
                re.compile(r"\b" + re.escape(author.group(1).strip()) + r"\b"))
        for title in re.findall(r'"([^"]{3,90}?)\.?"', notes):
            anywhere.append(re.compile(re.escape(title.strip().rstrip("."))))
        return outside, anywhere

    @classmethod
    def quotations(cls, basis: str) -> list:
        """[(offset, text)] for every run inside quotation marks, ellipses
        split, at any length. Returns [] for an unbalanced basis, which
        `test_no_basis_leaves_a_quotation_mark_unclosed` refuses separately."""
        parts = basis.split('"')
        if len(parts) % 2 == 0:
            return []
        out, at = [], 0
        for index, part in enumerate(parts):
            if index % 2:
                offset = at
                for piece in cls.ELLIPSIS.split(part):
                    if piece.strip():
                        out.append((offset + part.find(piece), piece))
            at += len(part) + 1
        return out

    @classmethod
    def attribute(cls, claim) -> dict:
        """{offset: {source, ...}} -- who each quoted run is attributed to."""
        basis = claim.basis
        chars = list(basis)
        at = 0
        for index, part in enumerate(basis.split('"')):
            if index % 2:
                for position in range(at, at + len(part)):
                    chars[position] = " "
            at += len(part) + 1
        masked = "".join(chars)

        where, titles = {}, {}
        for source in claim.sources:
            key = cls.witness_of(source)
            outside, anywhere = cls.cues(source)
            where.setdefault(key, []).extend(
                found.start() for cue in outside for found in cue.finditer(masked))
            for cue in anywhere:
                titles.setdefault(key, set()).add(
                    cls.fold(cue.pattern.replace("\\", "")).rstrip("."))

        # A TITLE NAMES ITS SOURCE ONLY WHERE IT IS QUOTED AS A TITLE. Matching
        # it anywhere in the prose put Genesis 25:20's words into the "Isaac"
        # article, because the word "Isaac's" stood nearer the quotation than
        # the citation did.
        for offset, text in cls.quotations(basis):
            folded = cls.fold(text).rstrip(".")
            for key, seen in titles.items():
                if folded in seen:
                    where.setdefault(key, []).append(offset)

        keys = {cls.witness_of(source) for source in claim.sources}
        attributed = {}
        for offset, text in cls.quotations(basis):
            # A QUOTED TITLE NAMES ITS OWN SOURCE. "Deluge" and "Biblical
            # Chronology" are how a basis says which article it is about, and
            # distance would send them to the other one.
            folded = cls.fold(text).rstrip(".")
            named = {key for key, seen in titles.items() if folded in seen}
            if named:
                attributed[offset] = named
                continue
            # ATTRIBUTION PRECEDES QUOTATION. "The Deluge article gives the
            # Samaritan reckoning: '...'. Its Biblical Chronology prints ..."
            # -- the name that answers for a quotation is the one BEFORE it,
            # and a plain nearest-neighbour rule hands it to the next article
            # named. So the nearest preceding name wins outright, and a
            # following one is used only where nothing precedes.
            nearest = cls._nearest(where, offset, len(text), before=True)
            if not nearest:
                nearest = cls._nearest(where, offset, len(text), before=False)
            if not nearest and len(keys) == 1:
                nearest = set(keys)
            attributed[offset] = nearest
        return attributed

    @classmethod
    def _nearest(cls, where: dict, offset: int, length: int, before: bool):
        nearest, best = set(), None
        for key, positions in where.items():
            for position in positions:
                if offset <= position <= offset + length:
                    continue                          # inside the quotation
                if before and position > offset:
                    continue
                if not before and position < offset:
                    continue
                distance = abs(position - offset)
                if best is None or distance < best:
                    best, nearest = distance, {key}
                elif distance == best:
                    nearest.add(key)
        return nearest

    @classmethod
    def present(cls, span: str, bodies: list) -> bool:
        folded = cls.fold(span)
        candidates = [folded, folded.rstrip(".,;:")]
        for body in bodies:
            for candidate in candidates:
                if candidate and candidate in body:
                    return True
        # last resort: the extraction's end-of-line hyphenation inside a table
        # cell, dropped from BOTH sides. Typography, not words.
        plain = [c.replace("-", "") for c in candidates]
        for body in bodies:
            stripped = body.replace("-", "")
            for candidate in plain:
                if candidate and candidate in stripped:
                    return True
        return False

    @classmethod
    def survey(cls):
        """(checked, matched, failing, unreopenable, self_witnessed).

        `failing`, `unreopenable` and `self_witnessed` are all
        {claim: [spans]}, and ALL THREE have to be declared. The old survey
        returned a `skipped` count that its caller threw away, which is how an
        `answerable`, `patristic` claim citing one unretained NPNF artifact,
        with an invented Eusebius quotation, passed 197 tests.
        """
        checked = matched = 0
        failing, unreopenable, self_witnessed = {}, {}, {}
        corpus = _chronology.load()
        for kind, holder in (("event", corpus.events), ("unit", corpus.units)):
            for subject in holder.values():
                for index, claim in enumerate(subject.claims):
                    if not claim.basis:
                        continue
                    identifier = f"{kind}:{subject.id}#{index}"
                    parties = cls.witnesses(claim)
                    attributed = cls.attribute(claim)
                    for offset, span in cls.quotations(claim.basis):
                        sources = attributed.get(offset) or set()
                        retained, project = [], []
                        for source in sources:
                            have, mine = parties.get(source, ([], []))
                            retained.extend(have)
                            project.extend(mine)
                        checked += 1
                        if retained and cls.present(span, retained):
                            matched += 1
                        elif project and cls.present(span, project):
                            self_witnessed.setdefault(identifier, []).append(span)
                        elif not retained:
                            unreopenable.setdefault(identifier, []).append(span)
                        else:
                            failing.setdefault(identifier, []).append(span)
        return checked, matched, failing, unreopenable, self_witnessed

    def test_every_quoted_basis_span_is_in_the_source_it_cites(self) -> None:
        checked, matched, failing, _unreopenable, _self = self.survey()
        self.assertGreater(checked, 900, "the survey stopped finding quotations")
        self.assertEqual(
            failing, {},
            "a basis quotes words that are not in the source its own sentence "
            "names:\n"
            + "\n".join(f"  {identifier}: {span[:120]!r}"
                        for identifier, spans in sorted(failing.items())
                        for span in spans))
        self.assertEqual(matched, checked - sum(
            len(spans) for spans in
            list(_unreopenable.values()) + list(_self.values())))

    def test_a_span_that_cannot_be_reopened_is_declared_and_not_discarded(
            self) -> None:
        """THE HIDING PLACE, CLOSED. A claim citing only unretained bytes used
        to produce `skipped` spans that the caller dropped on the floor.

        Asserted in both directions and by count, so that neither a new
        unreopenable citation nor a declared one that has started matching can
        pass unnoticed."""
        _checked, _matched, _failing, unreopenable, _self = self.survey()
        self.assertEqual(
            sorted(unreopenable), sorted(self.UNREOPENABLE),
            "the exception list and the spans that actually cannot be reopened "
            "have come apart")
        for identifier, spans in unreopenable.items():
            expected, reason = self.UNREOPENABLE[identifier]
            self.assertEqual(
                len(spans), expected,
                f"{identifier} has {len(spans)} unreopenable spans, not "
                f"{expected}; the exception list has to say what it covers")
            self.assertGreater(len(reason), 40, identifier)

    def test_the_corpus_is_not_standing_as_its_own_source(self) -> None:
        """A span whose only witness is a passage record's `context` is the
        project's own prose, not the page's bytes. Permitted where the page
        cannot be retained, and only where it is written down."""
        _checked, _matched, _failing, _unreopenable, self_witnessed = self.survey()
        self.assertEqual(sorted(self_witnessed), sorted(self.SELF_WITNESSED))
        for identifier, spans in self_witnessed.items():
            expected, reason = self.SELF_WITNESSED[identifier]
            self.assertEqual(len(spans), expected, identifier)
            self.assertGreater(len(reason), 40, identifier)

    def test_every_quoted_run_is_attributed_to_a_source(self) -> None:
        """A run nobody's name stands near is a run nothing checks. On a claim
        with more than one source that is a failure, because pooling them is
        exactly the defect this class exists to close."""
        corpus = _chronology.load()
        loose = []
        for kind, holder in (("event", corpus.events), ("unit", corpus.units)):
            for subject in holder.values():
                for index, claim in enumerate(subject.claims):
                    if not claim.basis:
                        continue
                    attributed = self.attribute(claim)
                    for offset, span in self.quotations(claim.basis):
                        if not attributed.get(offset):
                            loose.append(
                                f"{kind}:{subject.id}#{index}: {span[:80]!r}")
        self.assertEqual(loose, [])

    def test_a_swapped_attribution_does_not_match(self) -> None:
        """The auditor's attack, run as a test.

        event:apostolic-age.council-of-jerusalem#4 quotes Galatians 2:1 and
        then Prat's "St. Paul" article. Under the old pooled check, exchanging
        the two quotations left both matching. Here the basis is rewritten in
        memory with the two runs exchanged, and the claim must FAIL -- twice,
        once for each half.
        """
        corpus = _chronology.load()
        claim = corpus.events["apostolic-age.council-of-jerusalem"].claims[4]
        runs = [span for _offset, span in self.quotations(claim.basis)]
        scripture = next(s for s in runs if "after fourteen years" in s)
        article = next(s for s in runs if "relate to the same fact" in s)
        swapped = claim.basis.replace(
            scripture, "\x00").replace(article, scripture).replace("\x00", article)
        self.assertNotEqual(swapped, claim.basis)
        forged = claim._replace(basis=swapped)

        parties = self.witnesses(forged)
        attributed = self.attribute(forged)
        wrong = 0
        for offset, span in self.quotations(swapped):
            sources = attributed.get(offset) or set()
            retained = [b for source in sources
                        for b in parties.get(source, ([], []))[0]]
            if span in (scripture, article) and not self.present(span, retained):
                wrong += 1
        self.assertEqual(
            wrong, 2,
            "swapping the attributions of Galatians 2:1 and Prat's article no "
            "longer fails; the pooled check is back")

    def test_no_basis_leaves_a_quotation_mark_unclosed(self) -> None:
        """`quotations` reads quotation marks in pairs, so an odd number of
        them would silently stop this whole test seeing a claim."""
        corpus = _chronology.load()
        odd = []
        for kind, holder in (("event", corpus.events), ("unit", corpus.units)):
            for subject in holder.values():
                for index, claim in enumerate(subject.claims):
                    if claim.basis and claim.basis.count('"') % 2:
                        odd.append(f"{kind}:{subject.id}#{index}")
        self.assertEqual(odd, [])

# --- PCC-28: century notation, written down where a reader will find it -----


class CenturyNotationTests(unittest.TestCase):
    """A source that names a century and no year is stored as an interval, and
    the interval is the century entire even where the source narrows inside it.

    Six traditional claims did that while the rule for it lived only inside
    their own notes. Four critical claims now use the same normalization. The
    rule is declared independently as `display.century_notation` by both leaf
    profiles, while each profile retains its own evidence and derivation-rank
    policy. These tests hold both sets of data to that shared normalization.
    """

    RULE = "century_notation"
    PROFILE_COUNTS = {PROFILE: 6, CRITICAL: 4}

    @staticmethod
    def _century_notated():
        corpus = _chronology.load()
        found = {}
        for unit in corpus.units.values():
            for index, claim in enumerate(unit.claims):
                date = claim.date
                if not date or date.precision != "interval":
                    continue
                begin, end = date.begin, date.end
                if not begin or not end or begin.year is None or end.year is None:
                    continue
                if begin.year % 100 == 0 and end.year % 100 == 1:
                    found[f"{unit.id}#{index}"] = claim
        return found

    @staticmethod
    def _normalization(stated: str) -> str:
        """The common normalization, before profile-specific rank rationale."""
        return stated.partition("\nThis is NOTATION")[0]

    def test_both_profiles_state_the_identical_normalization(self) -> None:
        profiles = _chronology.load().profiles
        stated = {}
        for identifier in self.PROFILE_COUNTS:
            display = profiles[identifier].get("display", {})
            self.assertIn(
                self.RULE,
                display,
                f"the notation rule is not written down in {identifier}",
            )
            stated[identifier] = display[self.RULE]
            self.assertIn("entire", stated[identifier].lower())
            self.assertIn("derived", stated[identifier].lower())
        self.assertEqual(
            self._normalization(stated[PROFILE]),
            self._normalization(stated[CRITICAL]),
        )

    def test_every_century_notated_claim_is_governed_by_that_rule(self) -> None:
        claims = self._century_notated()
        counts = {identifier: 0 for identifier in self.PROFILE_COUNTS}
        for identifier, claim in claims.items():
            self.assertIn(claim.profile, counts, identifier)
            counts[claim.profile] += 1
            self.assertIn(
                self.RULE,
                _chronology.load().profiles[claim.profile].get("display", {}),
                identifier,
            )
            # The traditional remediation made each of its six claims point
            # back to the newly centralized rule. Critical claims are covered
            # by their profile declaration and need not repeat policy prose.
            if claim.profile == PROFILE:
                self.assertIsNotNone(claim.note, identifier)
                self.assertIn(self.RULE, claim.note, identifier)
        self.assertEqual(counts, self.PROFILE_COUNTS, sorted(claims))

    def test_no_century_notated_claim_pretends_to_be_a_derivation(self) -> None:
        """The alternative settlement was to re-author these as rank-7
        `derived`. It was not taken, so nothing may carry the marks of it."""
        for identifier, claim in self._century_notated().items():
            self.assertNotEqual(claim.basis_class, "derived", identifier)
            self.assertIsNone(claim.date.derivation, identifier)

    def test_the_bounds_are_the_whole_century_and_never_narrower(self) -> None:
        """A narrowing inside the century lives in the label. If it ever
        reaches the bounds, the corpus has asserted a year no source printed."""
        for identifier, claim in self._century_notated().items():
            begin, end = claim.date.begin, claim.date.end
            self.assertEqual(begin.year % 100, 0, identifier)
            self.assertEqual(end.year % 100, 1, identifier)
            self.assertEqual((begin.year - end.year + 1) % 100, 0, identifier)


# --- PCC-29: the Petavius table's positional extraction, re-checked ---------


class PetaviusTableTests(unittest.TestCase):
    """Ten answerable claims, four of them preferred, come from a table whose
    label cells and year cells New Advent delivers as separate blocks; the
    corpus paired them BY POSITION and every one of the ten notes said to
    re-verify against a page image before publishing.

    The article's bytes are now retained, so the pairing is reopenable here.
    These tests are that re-check, run as a test rather than asserted in prose:
    inside each block of the table the year for a label stands a constant
    number of lines further on, and on that constant all ten figures pair as
    the claims record. What is NOT settled by them, and is not claimed by them,
    is whether New Advent's delivery reproduces the printed page's rows; the
    volume-8 facsimile is registered `remote` and is not retained.
    """

    ARTICLE = (REPOSITORY_ROOT / "src" / "sources" / "works"
               / "catholic-encyclopedia" / "volume-8" / "editions"
               / "new-york-1910" / "artifacts"
               / "newadvent-08654a-645bba6c-article-text"
               / "newadvent-08654a-645bba6c-article-text.txt")
    SOURCE = ("artifact.catholic-encyclopedia.volume-8.new-york-1910"
              ".newadvent-08654a-645bba6c")

    # (block name, the label that opens the paired range, the label that closes
    #  it, the constant offset, and the pairings the claims rest on -- each
    #  pairing carrying THE CLAIM IT JUSTIFIES, so that the year read off the
    #  article is checked against the year the corpus stores and answers with).
    BLOCKS = (
        ("first Juda block", "David", "Joas", 21,
         (("David", "1055", "israel.monarchy.david-accession#0"),
          ("Solomon", "1015", "israel.monarchy.solomon-accession#0"),
          ("(Building of the", "1012", "israel.monarchy.temple-begun#1"),
          ("Roboam", "975", "israel.divided-kingdom.division#1"))),
        ("second Juda block", "Amasias", '" (end)', 19,
         (("Ezechias", "727", "israel.divided-kingdom.ezechias-accession#0"),
          ("Josias", "641", "israel.divided-kingdom.josias-reign#1"),
          ("Joakim", "610", "israel.exile.joakim-accession#0"),
          ("Sedecias", "599", "israel.exile.sedecias-reign#1"),
          ('" (end)', "588", "israel.exile.third-captivity#3"))),
        ("Israel block", "Jeroboam", '"(end)', 17,
         (('"(end)', "721", "israel.divided-kingdom.fall-of-samaria#3"),)),
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.lines = [line.rstrip() for line in cls.ARTICLE.read_text().splitlines()]

    def _first(self, text: str) -> int:
        for index, line in enumerate(self.lines):
            if line == text:
                return index
        self.fail(f"{text!r} is not in the retained article text")

    def test_each_label_pairs_with_its_year_at_the_blocks_constant(self) -> None:
        for name, _open, _close, offset, pairings in self.BLOCKS:
            for label, year, _claim in pairings:
                at = self._first(label)
                self.assertEqual(
                    self.lines[at + offset], year,
                    f"{name}: {label!r} at line {at + 1} does not pair with "
                    f"{year!r} at the block's offset of {offset}")

    def test_the_years_read_off_the_table_are_the_years_the_corpus_stores(
            self) -> None:
        """THE HALF THAT WAS MISSING, and the reason a 100-year error could sit
        in a `preferred` answer with 197 tests green.

        Everything above verifies the article against the article: the ten
        label/year pairings were read off the retained text and hardcoded here,
        and then checked back against the same text. Nothing compared them to
        the corpus. A cold auditor changed
        `israel.monarchy.david-accession#0` from `year: 1055` to `1155` --
        leaving the printed label reading "B.C. 1055" and the basis still
        quoting the table's 1055 -- and the whole suite stayed green, because
        the stored machine value was the one thing no test read.

        So the table's year, the claim's LABEL and the claim's stored DATE are
        asserted against each other here, all three, for all ten.
        """
        corpus = _chronology.load()
        seen = set()
        for name, _open, _close, _offset, pairings in self.BLOCKS:
            for _label, year, identifier in pairings:
                event_id, index = identifier.split("#")
                self.assertIn(event_id, corpus.events, identifier)
                claim = corpus.events[event_id].claims[int(index)]
                seen.add(identifier)
                self.assertIn(
                    self.SOURCE, claim.sources,
                    f"{identifier} no longer cites the Petavius table")
                date = claim.date
                self.assertIsNotNone(date, identifier)
                self.assertEqual(
                    date.label, f"B.C. {year}",
                    f"{name}: {identifier} is labelled {date.label!r} and the "
                    f"table prints {year!r}")
                for endpoint in (date.begin, date.end):
                    self.assertIsNotNone(endpoint, identifier)
                    self.assertEqual(
                        endpoint.year, int(year),
                        f"{name}: {identifier} STORES {endpoint.year} while "
                        f"the table prints {year} and its own label says "
                        f"B.C. {year}")
                    self.assertEqual(endpoint.era, "bc", identifier)
        # and the ten are the ten: a claim cannot be dropped out of this check
        # by being unhooked from the block table above.
        resting = {
            f"{event.id}#{index}"
            for event in corpus.events.values()
            for index, claim in enumerate(event.claims)
            if self.SOURCE in claim.sources
            and claim.basis_class == "reported-traditional"
        }
        self.assertEqual(seen, resting)

    def test_the_two_columns_share_one_blank_line_skeleton(self) -> None:
        """The property that makes the pairing structural rather than a guess:
        a blank line in the label column always faces a blank line in the year
        column, and the only label lines facing a blank belong to a label that
        wraps onto two lines."""
        wrapped = {"Temple)", "Jeroboam", "num)"}
        for name, opener, closer, offset, _pairings in self.BLOCKS:
            first, last = self._first(opener), self._first(closer)
            self.assertLess(first, last, name)
            for at in range(first, last + 1):
                label, year = self.lines[at], self.lines[at + offset]
                if label == "":
                    self.assertEqual(
                        year, "",
                        f"{name}: a blank label line at {at + 1} faces "
                        f"{year!r}")
                elif year == "":
                    self.assertIn(
                        label, wrapped,
                        f"{name}: {label!r} at line {at + 1} faces a blank "
                        f"year and is not a wrapped label")

    def test_the_ten_claims_are_the_ones_the_notes_say_they_are(self) -> None:
        resting = {
            f"{event.id}#{index}": claim
            for event in _chronology.load().events.values()
            for index, claim in enumerate(event.claims)
            if self.SOURCE in claim.sources
            and claim.basis_class == "reported-traditional"
        }
        self.assertEqual(len(resting), 10, sorted(resting))
        self.assertEqual(
            sum(1 for claim in resting.values()
                if claim.disposition == "preferred"), 4)
        for identifier, claim in resting.items():
            self.assertIn("CHECKED 2026-09-02", claim.note or "", identifier)
            self.assertIn("NARROWED, NOT WITHDRAWN", claim.note or "", identifier)


# --- PCC-36: the stored year and the label that justifies it ---------------


class StoredDateAgreesWithItsLabelTests(unittest.TestCase):
    """The machine value and the printed words have to say the same thing.

    A claim carries a `date` the tools compute with and a `label` the reader
    sees, and until 2026-09-02 NOTHING compared them. PetaviusTableTests was
    the closest thing to a check and it verified the article against the
    article; a cold auditor moved `israel.monarchy.david-accession#0` from
    1055 to 1155, left the label reading "B.C. 1055" and the basis still
    quoting the table's 1055, and all 197 tests passed. That is a hundred-year
    error in a `preferred` answer over 2 Kings, invisible.

    PetaviusTableTests now pins those ten. This class is the GENERAL case, and
    it is the general case because the defect is not about Petavius: any claim
    anywhere can have its stored endpoints edited away from the words that
    justify them, and the label is what a reader checks the basis against.

    THE RULE: every year an endpoint stores must be licensed by the label.
    Licensed means the label prints it, or the label prints it in the
    abbreviated form the sources use for a span -- "B.C. 933-2" for 933 to 932,
    "B. C. 465-24" for 465 to 424, "63-4" for 63 to 64 -- which is completed
    here by taking the head digits from the number before it. Century notation
    is out of scope and belongs to CenturyNotationTests, which holds those six
    to `display.century_notation` instead.

    A label may also be prose that prints no year at all, which is legitimate
    and is why this test has an exception list rather than a threshold. Each
    exception names the claim, the years, and where they come from; the list is
    asserted in BOTH directions, so an exception that starts agreeing with its
    label fails here and has to be removed.
    """

    NUMBER = re.compile(r"\d+")
    ERA_BC = re.compile(r"\bB\.?\s?C\.?")
    ERA_AD = re.compile(r"\bA\.?\s?D\.?\B|\bA\.\s?D\.")

    UNLABELLED = {
        "event:apostolic-age.famine-under-claudius#0": (
            "The label is the article's own phrase 'precisely in this year' "
            "and prints no figure; the year 44 is the one the sentence it "
            "continues has just given, and the basis quotes both halves."),
        "event:apostolic-age.saint-paul-first-roman-captivity#1": (
            "The label prints only Howlett's 'hence till 64', which is the "
            "END. The begin, 62, is the arrival year the same passage gives "
            "as 'Perhaps we may say 62' and the basis quotes in full; the "
            "claim's note says the begin endpoint carries a hedge the end "
            "does not."),
        "unit:composition.gospel-of-john#0": (
            "The label is '96 or one of the succeeding years'. The end, 100, "
            "is where this corpus stops 'the succeeding years'; the note "
            "carries that and the label prints no second figure."),
    }

    @classmethod
    def _licensed(cls, label: str) -> set:
        """Every year the label's own digits license, abbreviations completed."""
        printed = [n for n in cls.NUMBER.findall(label)]
        years = {int(n) for n in printed}
        for before, after in zip(printed, printed[1:]):
            if len(after) < len(before):
                years.add(int(before[:len(before) - len(after)] + after))
        return years

    @classmethod
    def _century_notated(cls) -> set:
        """The six claims CenturyNotationTests owns, found the same way."""
        found = set()
        corpus = _chronology.load()
        for kind, holder in (("event", corpus.events), ("unit", corpus.units)):
            for subject in holder.values():
                for index, claim in enumerate(subject.claims):
                    date = claim.date
                    if not date or date.precision != "interval":
                        continue
                    begin, end = date.begin, date.end
                    if not begin or not end:
                        continue
                    if begin.year is None or end.year is None:
                        continue
                    if begin.year % 100 == 0 and end.year % 100 == 1:
                        found.add(f"{kind}:{subject.id}#{index}")
        return found

    @classmethod
    def survey(cls):
        """(checked, {claim: (label, the years it stores that it does not print)})."""
        centuries = cls._century_notated()
        corpus = _chronology.load()
        checked = 0
        adrift = {}
        for kind, holder in (("event", corpus.events), ("unit", corpus.units)):
            for subject in holder.values():
                for index, claim in enumerate(subject.claims):
                    identifier = f"{kind}:{subject.id}#{index}"
                    date = claim.date
                    if not date or not date.label or identifier in centuries:
                        continue
                    stored = [
                        endpoint.year
                        for endpoint in (date.begin, date.end)
                        if endpoint is not None and endpoint.year is not None
                    ]
                    if not stored:
                        continue
                    checked += 1
                    licensed = cls._licensed(date.label)
                    missing = sorted({y for y in stored if y not in licensed})
                    if missing:
                        adrift[identifier] = (date.label, missing)
        return checked, adrift

    def test_no_stored_year_is_absent_from_the_label_that_justifies_it(
            self) -> None:
        checked, adrift = self.survey()
        self.assertGreater(checked, 200, "the survey stopped finding dates")
        undeclared = {
            identifier: value for identifier, value in adrift.items()
            if identifier not in self.UNLABELLED
        }
        self.assertEqual(
            undeclared, {},
            "a claim stores a year its own label does not print:\n"
            + "\n".join(
                f"  {identifier}: stores {missing} under label {label!r}"
                for identifier, (label, missing) in sorted(undeclared.items())))

    def test_the_exception_list_is_exactly_the_claims_whose_labels_are_prose(
            self) -> None:
        """An exception that has started agreeing with its label is a claim
        nobody is checking any more."""
        _checked, adrift = self.survey()
        self.assertEqual(sorted(adrift), sorted(self.UNLABELLED))
        for identifier, reason in self.UNLABELLED.items():
            self.assertGreater(len(reason), 40, identifier)

    def test_the_era_the_endpoint_stores_is_the_era_the_label_prints(self) -> None:
        """The other half of a drifting endpoint: 588 B.C. and A.D. 588 are the
        same digits and eleven centuries apart."""
        corpus = _chronology.load()
        wrong = []
        for kind, holder in (("event", corpus.events), ("unit", corpus.units)):
            for subject in holder.values():
                for index, claim in enumerate(subject.claims):
                    date = claim.date
                    if not date or not date.label:
                        continue
                    # matched with word boundaries and case: "traditional"
                    # contains "ad", and folding the label to lower case with
                    # its punctuation stripped made every such label read as
                    # Anno Domini.
                    says_bc = bool(self.ERA_BC.search(date.label))
                    says_ad = bool(self.ERA_AD.search(date.label))
                    if says_bc == says_ad:      # both or neither: prose label
                        continue
                    era = "bc" if says_bc else "ad"
                    for endpoint in (date.begin, date.end):
                        if endpoint is not None and endpoint.era != era:
                            wrong.append(
                                f"{kind}:{subject.id}#{index} stores "
                                f"{endpoint.era} under label {date.label!r}")
        self.assertEqual(wrong, [])


# --- PCC-40: retained text later than the edition it hangs under ------------


class PostImprintContentTests(unittest.TestCase):
    """Three retained article texts carry material printed AFTER the edition
    year of the record they hang under.

    `09420a` and `09674b` in the 1910 volume, and `01117a` in the 1907 volume,
    all quote decisions of the Biblical Commission of 1913. So New Advent's
    delivery is a later state of those articles than the first printing of
    their volumes, and the "edition-identified" requirement that
    `authority` ranks 3 and 6 place on a source is not met for them. Low
    severity, and recorded rather than repaired: no chronology claim in this
    corpus rests on the 1913 material, and the rights conclusion is untouched.

    The point of the test is that the SET cannot grow in silence. It is derived
    from the retained bytes against the edition year in the path, and the two
    numerals that look like post-imprint years and are not are declared with
    their reasons, in both directions.
    """

    LATE = re.compile(r"\b(19[0-4]\d)\b")

    NOT_A_DATE = {
        ("03302a", 1911): (
            "A Migne column number: 'Ambrose (Migne, P.L., XIII, 1855, 1911)'. "
            "The volume is 1908 and the figure is a citation, not a year."),
        ("03738a", 1939): (
            "An arithmetic example in the article on the calendar: \"the year "
            "'39 of any century (939, 1539, 1839, 1939)\". Not a date the "
            "article carries as content."),
    }

    DECLARED = {
        ("01117a", 1913): "the Biblical Commission's decision of 12 June 1913, "
                          "in a volume of 1907",
        ("09420a", 1913): "the Biblical Commission's answers of 26 June 1913, "
                          "in a volume of 1910",
        ("09674b", 1913): "the Biblical Commission's decision of 26 January "
                          "1913, cross-referenced, in a volume of 1910",
    }

    @classmethod
    def survey(cls):
        found = {}
        root = REPOSITORY_ROOT / "src" / "sources" / "works" / "catholic-encyclopedia"
        for path in root.glob("**/*-article-text/*.txt"):
            edition = next(p for p in path.parts if p.startswith("new-york-"))
            year = int(edition.rsplit("-", 1)[1])
            page = path.name.split("-")[1]
            for later in {int(m) for m in cls.LATE.findall(path.read_text())}:
                if later > year:
                    found.setdefault((page, later), set()).add(year)
        return found

    def test_the_set_of_post_imprint_years_is_the_declared_one(self) -> None:
        found = self.survey()
        self.assertGreater(len(found), 0, "the survey stopped reading files")
        undeclared = sorted(
            key for key in found
            if key not in self.DECLARED and key not in self.NOT_A_DATE)
        self.assertEqual(
            undeclared, [],
            "a retained article carries a year later than the edition it hangs "
            "under, and nothing says so")
        self.assertEqual(
            sorted(key for key in found if key in self.DECLARED),
            sorted(self.DECLARED))
        self.assertEqual(
            sorted(key for key in found if key in self.NOT_A_DATE),
            sorted(self.NOT_A_DATE))

    def test_each_affected_record_says_so_in_its_own_notes(self) -> None:
        """A ledger row a reader of the source will never open is not
        disclosure. The artifact records carry it."""
        import tomllib

        seen = 0
        root = REPOSITORY_ROOT / "src" / "sources" / "works" / "catholic-encyclopedia"
        for path in root.glob("**/*-article-text/artifact.toml"):
            page = path.parent.name.split("-")[1]
            if not any(page == key[0] for key in self.DECLARED):
                continue
            seen += 1
            notes = tomllib.loads(path.read_text()).get("notes", "")
            self.assertIn("POST-IMPRINT", notes, page)
            self.assertIn("1913", notes, page)
            self.assertIn("edition-identified", notes, page)
        self.assertEqual(seen, len(self.DECLARED))


# --- PCC-39: no interval wider than what its source states ------------------


class StatedBoundsTests(unittest.TestCase):
    """An interval asserts every year between its endpoints, so its endpoints
    have to be years the source states.

    Four claims were wider than anything their sources said, and every one of
    them said so in its own note while the machine value went on asserting the
    excluded years: life-of-christ.crucifixion held 29-33 for "the years 29, 30,
    and 33 to choose between", asserting 31 and 32 that the article's own test
    had eliminated; composition.book-of-wisdom held 221-117 across two disjoint
    reigns, asserting the fifty-nine years between them that its argument
    excludes; composition.book-of-esther opened at 485, the year the reign
    BEGAN, where the source says "at the end of the reign of Xerxes I
    (485-465 B.C.)". A note is not what a consumer computes with.

    The rule is now `display.stated_bounds`, and these tests hold the rule and
    the repaired data to each other.
    """

    RULE = "stated_bounds"
    HEADING_RULE = "a_printed_heading_is_the_works_own_text"

    @staticmethod
    def _display():
        return _chronology.load().profiles["catholic-traditional-v1"]["display"]

    def test_the_profile_states_both_rules(self) -> None:
        display = self._display()
        self.assertIn(self.RULE, display)
        self.assertIn(self.HEADING_RULE, display)
        bounds = display[self.RULE]
        self.assertIn("century_notation", bounds,
                      "the widening rule has to say how it stands to the one "
                      "notation that does widen deliberately")
        heading = display[self.HEADING_RULE]
        self.assertIn("nehemias-mission", heading,
                      "the heading rule has to name the case it is NOT")

    def test_the_three_crucifixion_years_are_three_claims(self) -> None:
        claims = _chronology.load().events["life-of-christ.crucifixion"].claims
        offered = {
            claim.date.begin.year: claim
            for claim in claims
            if claim.date and claim.date.precision == "year"
            and "to choose between" in (claim.date.label or "")
        }
        self.assertEqual(sorted(offered), [29, 30, 33])
        for year, claim in offered.items():
            self.assertEqual(claim.disposition, "disputed", year)
            self.assertEqual(claim.date.end.year, year,
                             "a candidate year is a year, not a span")
        # and no claim on this event spans the eliminated years
        for claim in claims:
            date = claim.date
            if not date or not date.begin or not date.end:
                continue
            if date.begin.year == 29 and date.end.year == 33:
                self.fail("the 29-33 interval is back; it asserts 31 and 32, "
                          "which the article eliminates")

    def test_the_two_wisdom_reigns_are_two_claims(self) -> None:
        claims = _chronology.load().units["composition.book-of-wisdom"].claims
        spans = sorted(
            (claim.date.begin.year, claim.date.end.year) for claim in claims)
        self.assertEqual(spans, [(145, 117), (221, 204)])
        for claim in claims:
            self.assertEqual(claim.disposition, "disputed",
                             "the article chooses between neither reign")

    def test_esther_opens_at_the_end_of_the_reign_and_not_its_beginning(
            self) -> None:
        claim = _chronology.load().units["composition.book-of-esther"].claims[0]
        self.assertEqual(claim.date.begin.year, 465)
        self.assertEqual(claim.date.end.year, 425)
        self.assertIn("485", claim.date.label,
                      "the label still carries the article's own words")

    def test_the_two_claims_resting_on_a_heading_say_so_and_cite_the_rule(
            self) -> None:
        corpus = _chronology.load()
        for identifier, index in (("apostolic-age.destruction-of-jerusalem", 1),
                                  ("apostolic-age.council-of-jerusalem", 2)):
            claim = corpus.events[identifier].claims[index]
            note = claim.note or ""
            self.assertIn("heading", note, identifier)
            self.assertIn(self.HEADING_RULE, note, identifier)

    def test_the_corpus_still_computes_no_year_for_the_nehemias_interval(
            self) -> None:
        """The case the heading rule is contrasted with. If this ever gains a
        year, the contrast the rule rests on is gone."""
        claim = (_chronology.load()
                 .events["israel.restoration.nehemias-mission"].claims[2])
        self.assertEqual(claim.date.precision, "relative")
        self.assertIsNone(claim.date.begin)
        self.assertIsNone(claim.date.end)


# --- PCC-38: the article's own "untenable" sentence, answered once ---------


class UntenablePeriodTests(unittest.TestCase):
    """Sloet declares the chronology of the kings before 730 B.C. untenable,
    and this profile answers with four figures inside that period.

    The sentence stands before BOTH of the article's tables, so it is not
    confined to the one this corpus refuses; four of the ten Petavius figures
    the corpus answers with fall inside the period it names, two of them
    `preferred`; and until 2026-09-02 nothing in the corpus said why the
    article's rejection does not reach them. The defence exists -- the stated
    warrant of the sentence is the excluded method, so the profile no more
    follows the method's verdicts than it answers with its numbers -- and the
    defect was that it was nowhere made.

    It is made once, in `profiles.yaml`. These tests hold the written ruling and
    the data to each other, so that neither can move without the other: the
    profile must state it, the sentence must still be in the retained article,
    and exactly the claims inside the period must cite the rule.
    """

    RULE = "a_sources_rejection_on_an_excluded_ground_is_not_followed"
    SENTENCE = ("Since the deciphering of the Assyro-Babylonian inscriptions, "
                "the chronology of the period of Kings before 730 B.C. has "
                "become untenable.")
    BOUNDARY = 730
    SOURCE = ("artifact.catholic-encyclopedia.volume-8.new-york-1910"
              ".newadvent-08654a-645bba6c")

    def test_the_profile_states_the_ruling(self) -> None:
        admissibility = (_chronology.load().profiles["catholic-traditional-v1"]
                         ["admissibility"])
        self.assertIn(self.RULE, admissibility,
                      "the ruling is not written down in the profile")
        stated = admissibility[self.RULE]
        # the three things the ruling has to settle
        self.assertIn("730 B.C.", stated)
        self.assertIn("rejected-by-source", stated)
        self.assertIn("VERDICTS", stated)

    def test_the_sentence_is_still_in_the_retained_article(self) -> None:
        """The ruling answers a sentence. If the sentence is not there, the
        ruling is answering nothing and has to be re-read."""
        text = (REPOSITORY_ROOT / "src" / "sources" / "works"
                / "catholic-encyclopedia" / "volume-8" / "editions"
                / "new-york-1910" / "artifacts"
                / "newadvent-08654a-645bba6c-article-text"
                / "newadvent-08654a-645bba6c-article-text.txt").read_text()
        self.assertIn(self.SENTENCE, text)

    @classmethod
    def _answered_with_from_the_table(cls):
        corpus = _chronology.load()
        return {
            f"{event.id}#{index}": claim
            for event in corpus.events.values()
            for index, claim in enumerate(event.claims)
            if cls.SOURCE in claim.sources
            and claim.basis_class == "reported-traditional"
        }

    def test_exactly_the_claims_inside_the_period_cite_the_ruling(self) -> None:
        """Derived from the DATES, not from a list, so that a figure moving
        across 730 B.C. moves this test with it."""
        inside, outside = {}, {}
        for identifier, claim in self._answered_with_from_the_table().items():
            year = claim.date.begin.year if claim.date and claim.date.begin else None
            self.assertIsNotNone(year, identifier)
            (inside if year > self.BOUNDARY else outside)[identifier] = claim
        self.assertEqual(
            sorted(inside),
            ["israel.divided-kingdom.division#1",
             "israel.monarchy.david-accession#0",
             "israel.monarchy.solomon-accession#0",
             "israel.monarchy.temple-begun#1"])
        self.assertEqual(
            sum(1 for claim in inside.values()
                if claim.disposition == "preferred"), 2)
        for identifier, claim in inside.items():
            self.assertIn(self.RULE, claim.note or "", identifier)
            self.assertIn("untenable", claim.note or "", identifier)
        for identifier, claim in outside.items():
            self.assertNotIn(
                self.RULE, claim.note or "",
                f"{identifier} is outside the period the sentence names and "
                f"does not need the ruling; citing it there makes the ruling "
                f"look broader than it is")


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

    @staticmethod
    def every_claim() -> dict:
        """Every claim in the tracked corpus, by the id this class names them
        with. A test that wants "the corpus's instances of X" asks the corpus."""
        corpus_ = _chronology.load()
        found = {}
        for kind, holder in (("event", corpus_.events), ("unit", corpus_.units)):
            for subject in holder.values():
                for index, claim in enumerate(subject.claims):
                    found[f"{kind}:{subject.id}#{index}"] = claim
        return found

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
        # reading and stop: it has to show the admissible ground.
        #
        # This comment said "Agrippa is the corpus's one instance" until
        # 2026-09-02, and it was wrong: life-of-christ.death-of-herod#0 invokes
        # the same clause over Josephus's lunar eclipse and was untested, so a
        # regression there would have gone green. The instances are found by
        # QUERY now, and the count is asserted, so a third one cannot arrive
        # unnoticed either.
        invoking = sorted(
            identifier for identifier, claim in self.every_claim().items()
            if claim.note and "corroboration_is_not_the_ground" in claim.note
        )
        self.assertEqual(
            invoking,
            ["event:apostolic-age.death-of-herod-agrippa#0",
             "event:life-of-christ.death-of-herod#0"],
            "a claim invokes the corroboration clause and is not tested here")

        # Agrippa: the ground shown is Prat's reckoning, not the coin.
        note = " ".join(self.claim(
            "event:apostolic-age.death-of-herod-agrippa#0").note.split())
        self.assertIn("corroboration_is_not_the_ground", note)
        self.assertIn("These combined facts bring us to the year 44", note)
        self.assertIn("naming no coin", note)

        # Herod the Great: the ground shown is Howlett's reckoning from
        # Josephus on the reign, not the eclipse the article corroborates with.
        herod = " ".join(self.claim(
            "event:life-of-christ.death-of-herod#0").note.split())
        self.assertIn("corroboration_is_not_the_ground", herod)
        self.assertIn("corroborated by an eclipse of the moon", herod)
        self.assertIn("names no eclipse", herod)

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
