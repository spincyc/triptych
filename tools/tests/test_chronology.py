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

    def test_chronology_is_authored_in_one_system_only(self) -> None:
        refuses(
            self,
            "chronology is authored in",
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
        self.assertTrue(answer.assertions[0].inherited)
        self.assertEqual(answer.status, "inherited")

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
        self.assertIsInstance(answer, _chronology.Unresolved)
        self.assertEqual(answer.status, "textually-distinct")
        self.assertIn("Ecclesiasticus", answer.reason)

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
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("Dan.13.1", "test", "world-english-catholic"),
            root=book.root,
        )
        self.assertIsInstance(answer, _chronology.Unresolved)
        self.assertEqual(answer.status, "textually-distinct")
        self.assertIn("no correspondence is recorded", answer.reason)

    def test_an_unknown_system_refuses_with_a_reason(self) -> None:
        book = corpus(self)
        answer = _chronology.chronology(
            _chronology.parse_locus("Gen.1.1", "test", "septuagint"), root=book.root
        )
        self.assertIsInstance(answer, _chronology.Unresolved)
        self.assertEqual(answer.status, "not-alignable")
        self.assertIn("no concordance", answer.reason)

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
            {run.status for run in matthew}, {"inherited"}
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

    def test_the_system_chronology_is_authored_in_is_the_one_projections_use(self) -> None:
        # Two names for one choice is one way of finding out later that they
        # had stopped agreeing.
        self.assertEqual(_chronology.CANONICAL_SYSTEM, _projection.CANONICAL)

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


if __name__ == "__main__":
    unittest.main()
