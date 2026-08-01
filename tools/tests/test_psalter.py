"""Tests for the per-edition record of where a printed psalter departs.

The tracked Clementine declared `numbering: vulgate`, printed nine psalms the
tracked concordance numbers differently, and carried a verse-alias table that was
a two-column header and nothing else. `Bible.verse('Ps', 115, 10)` returned *in
atriis domus Domini* — the last verse of the psalm under the first verse's
number, real Latin at a correct-looking reference, and nothing counted it a
failure. Two things are held here. The readings themselves, so a correction
cannot be undone silently; and the check that derives the obligation from the
text, because an empty table that nothing questions is indistinguishable from a
table nobody wrote.
"""

from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _projection as projection  # noqa: E402
import _psalter as psalter  # noqa: E402

CLEMENTINE = "clementine-vulgate"
CPDV = "catholic-public-domain-version"
AMERICAN = "douay-rheims-american-1899"


def reset() -> None:
    for cached in (
        psalter.printed,
        psalter.departures,
        psalter._witness_aliases,
    ):
        cached.cache_clear()


def rows_of(edition: str) -> dict[str, dict[str, str]]:
    numbering, _ = psalter.EDITIONS[edition]
    return {row["cited_locus"]: row for row in psalter.derive_aliases(edition, numbering)}


class Reading(unittest.TestCase):
    """What the declarations say, read against the verses they were taken from."""

    def setUp(self) -> None:
        reset()

    def test_the_two_restarted_psalms_are_renumbered_verse_for_verse(self):
        """The whole-psalm offsets, which made every verse of both resolve wrongly."""
        for edition in (CLEMENTINE, CPDV, AMERICAN):
            with self.subTest(edition=edition):
                rows = rows_of(edition)
                for cited, target in (
                    ("Ps.115.10", "Ps.115.1"), ("Ps.115.19", "Ps.115.10"),
                    ("Ps.147.12", "Ps.147.1"), ("Ps.147.20", "Ps.147.9"),
                ):
                    self.assertEqual(rows[cited]["resolves_to"], target)
                    self.assertEqual(rows[cited]["kind"], "renumbered")

    def test_the_clementine_resolves_the_psalm_that_named_this_defect(self):
        """Vulgate 115:10 is *Credidi*, not *in atriis domus Domini*."""
        sys.path.insert(0, str(ROOT / "tools"))
        from importlib.machinery import SourceFileLoader
        from importlib.util import module_from_spec, spec_from_loader

        loader = SourceFileLoader("index_bible", str(ROOT / "tools" / "index-bible"))
        module = module_from_spec(spec_from_loader("index_bible", loader))
        loader.exec_module(module)
        _, where = psalter.EDITIONS[CLEMENTINE]
        bible = module.Bible(psalter.WORKS / where)
        self.assertTrue(bible.verse("Ps", 115, 10).startswith("Alleluja. Credidi"))
        self.assertTrue(bible.verse("Ps", 115, 19).startswith("in atriis domus Domini"))
        self.assertTrue(bible.verse("Ps", 147, 12).startswith("Alleluja. Lauda, Jerusalem"))

    def test_a_merged_last_verse_resolves_to_the_verse_carrying_it(self):
        """The 1962 communion *Notas mihi fecisti vias vitae* is cited Psalm 15:11."""
        rows = rows_of(CLEMENTINE)
        self.assertEqual(rows["Ps.15.11"]["resolves_to"], "Ps.15.10")
        self.assertEqual(rows["Ps.15.11"]["kind"], "merged-verse")
        self.assertEqual(rows["Ps.125.7"]["resolves_to"], "Ps.125.6")
        self.assertEqual(rows["Ps.135.27"]["resolves_to"], "Ps.135.26")

    def test_a_displaced_verse_refuses_and_its_neighbours_do_not(self):
        """Psalm 42:5 is divided between this edition's 4 and 5; neither carries it."""
        for edition in (CLEMENTINE, CPDV):
            with self.subTest(edition=edition):
                rows = rows_of(edition)
                self.assertEqual(rows["Ps.42.5"]["resolves_to"], "")
                self.assertEqual(rows["Ps.42.5"]["kind"], "numbering-not-recorded")
                self.assertEqual(rows["Ps.42.4"]["resolves_to"], "Ps.42.4")
                self.assertEqual(rows["Ps.42.6"]["resolves_to"], "Ps.42.5")

    def test_the_public_domain_version_psalm_thirteen_stood_three_numbers_out(self):
        """Its 13:7 was the Vulgate's 13:4 — real text, wrong verse, cited by 1962."""
        rows = rows_of(CPDV)
        self.assertEqual(rows["Ps.13.7"]["resolves_to"], "Ps.13.10")
        self.assertEqual(rows["Ps.13.4"]["resolves_to"], "Ps.13.7")

    def test_a_split_whose_printed_run_starts_elsewhere_refuses(self):
        """The public-domain Psalm 92:1 is the psalm's Latin title, not its first verse."""
        rows = rows_of(CPDV)
        self.assertEqual(rows["Ps.92.1"]["resolves_to"], "")
        self.assertEqual(rows["Ps.92.1"]["kind"], "numbering-not-recorded")
        self.assertEqual(rows["Ps.92.2"]["resolves_to"], "Ps.92.4")

    def test_a_split_whose_printed_run_starts_at_the_cited_number_writes_no_row(self):
        """Refusing there would take away text the edition carries at the number cited.

        Psalm 19:9 is one verse in the concordance's witness and two here, and the
        first of the two opens the text cited. The divergence is recorded — it is
        a `split` in the projection — and resolution is left alone.
        """
        self.assertNotIn("Ps.19.9", rows_of(CLEMENTINE))
        _, where = psalter.EDITIONS[CLEMENTINE]
        rows = projection.project(psalter.WORKS / where.rsplit("/artifacts", 1)[0], "vulgate")
        splits = [row for row in rows if row.kind == "split"]
        self.assertEqual([row.cited_locus for row in splits], ["Ps.19.9"])
        self.assertTrue(all(row.resolves_to == "" for row in splits))

    def test_the_numbering_is_stated_by_two_tracked_artifacts(self):
        """Psalm 28:11 and Psalm 150:6 are Vulgate numbers the concordance cannot hold.

        Its rows must be equal-length runs in both systems, so its Vulgate column
        follows the Hebrew wherever the Vulgate divides a verse the Hebrew joins.
        Both numbers are cited and both are recorded in the witness edition's own
        alias table, so the extent is read from the two together — and the three
        editions that print them are not departing at all.
        """
        self.assertEqual(psalter.system_extent(28), (1, 11))
        self.assertEqual(psalter.system_extent(150), (1, 6))
        self.assertEqual(psalter._psalms.psalm_extent(28, "vulgate"), (1, 10))
        for edition in (CLEMENTINE, CPDV, AMERICAN):
            with self.subTest(edition=edition):
                _, where = psalter.EDITIONS[edition]
                self.assertNotIn(28, psalter.obligations(where, "vulgate"))
                self.assertNotIn(150, psalter.obligations(where, "vulgate"))


class Validation(unittest.TestCase):
    """A declaration that has stopped describing the library must not load."""

    def setUp(self) -> None:
        reset()
        self.declared = dict(psalter.DEPARTURES)
        self.addCleanup(self.restore)

    def restore(self) -> None:
        psalter.DEPARTURES.clear()
        psalter.DEPARTURES.update(self.declared)
        reset()

    def load(self, edition: str, entries: tuple) -> str:
        psalter.DEPARTURES[edition] = entries
        reset()
        with self.assertRaises(psalter.PsalterError) as caught:
            psalter.departures(edition, psalter.EDITIONS[edition][0])
        return str(caught.exception)

    def find(self, edition: str, psalm: int, relation: str) -> int:
        for index, entry in enumerate(self.declared[edition]):
            if entry.psalm == psalm and entry.relation == relation:
                return index
        raise AssertionError(f"no {relation} row for Psalm {psalm} in {edition}")

    def doctored(self, edition: str, index: int, **fields) -> tuple:
        rows = list(self.declared[edition])
        rows[index] = rows[index]._replace(**fields)
        return tuple(rows)

    def test_an_undeclared_divergence_is_refused(self):
        """The check that was missing. Nothing else notices an empty alias table."""
        problem = self.load(CLEMENTINE, ())
        self.assertIn("Psalm 15 prints verses 1-10", problem)
        self.assertIn("no departure is declared for it", problem)

    # Psalm 100 runs 1-8 in the numbering and 1-8 in this edition, so a
    # declaration for it is internally consistent and still uncalled for.
    AGREES = (
        psalter.Departure(
            100, psalter.IDENTITY, (1, 7), (1, 7),
            "a psalm for david himself mercy and",
            "psalmus ipsi david misericordiam et judicium cantabo", "",
        ),
        psalter.Departure(
            100, psalter.MERGED, (8, 8), (8, 8),
            "in the morning i put to death",
            "in matutino interficiebam omnes peccatores terrae ut", "invented",
        ),
    )

    def test_a_declaration_for_a_psalm_that_does_not_diverge_is_refused(self):
        """Self-cleaning: a record that has stopped being needed fails too."""
        rows = tuple(self.declared[CLEMENTINE]) + self.AGREES
        self.assertIn("remove the declaration", self.load(CLEMENTINE, rows))

    def test_an_opening_the_text_does_not_print_is_refused(self):
        where = self.find(CLEMENTINE, 115, psalter.RENUMBER)
        problem = self.load(
            CLEMENTINE, self.doctored(CLEMENTINE, where, printed_opening="in atriis domus")
        )
        self.assertIn("is recorded as opening", problem)

    def test_a_run_that_overruns_its_psalm_is_refused(self):
        """Neither ceiling is typed, so a run cannot overrun one without being caught."""
        where = self.find(CLEMENTINE, 147, psalter.RENUMBER)
        problem = self.load(
            CLEMENTINE, self.doctored(CLEMENTINE, where, cited=(12, 21), printed=(1, 10))
        )
        self.assertIn("but the cited extent is", problem)

    def test_a_psalm_left_partly_unruled_is_refused(self):
        where = self.find(CLEMENTINE, 125, psalter.IDENTITY)
        problem = self.load(
            CLEMENTINE, self.doctored(CLEMENTINE, where, cited=(1, 4), printed=(1, 4))
        )
        self.assertIn("unaccounted for", problem)

    def test_two_runs_claiming_one_verse_are_refused(self):
        rows = list(self.declared[CLEMENTINE])
        rows.append(rows[self.find(CLEMENTINE, 135, psalter.IDENTITY)])
        self.assertIn("claimed twice", self.load(CLEMENTINE, tuple(rows)))

    def test_a_departure_without_a_reason_is_refused(self):
        where = self.find(CLEMENTINE, 15, psalter.MERGED)
        self.assertIn(
            "must say what it found",
            self.load(CLEMENTINE, self.doctored(CLEMENTINE, where, note="")),
        )

    def test_a_renumbering_of_unequal_runs_is_refused(self):
        where = self.find(CLEMENTINE, 115, psalter.RENUMBER)
        self.assertIn(
            "runs of equal length",
            self.load(CLEMENTINE, self.doctored(CLEMENTINE, where, printed=(1, 9))),
        )

    def test_a_psalm_declared_wholly_at_identity_is_refused(self):
        """A declaration that asserts nothing is a record with no content."""
        agreeing = (
            self.AGREES[0]._replace(cited=(1, 8), printed=(1, 8)),
        )
        rows = tuple(self.declared[CLEMENTINE]) + agreeing
        self.assertIn("every run agrees", self.load(CLEMENTINE, rows))


class TrackedTables(unittest.TestCase):
    """The tracked alias rows must be what this module derives, and say so in four columns."""

    def setUp(self) -> None:
        reset()

    def test_every_edition_matches_its_derivation(self):
        for edition, (numbering, where) in sorted(psalter.EDITIONS.items()):
            if edition == psalter.WITNESS_EDITION:
                continue
            with self.subTest(edition=edition):
                found = sorted((psalter.WORKS / where).glob("verse-aliases-*/verse-aliases.tsv"))
                self.assertEqual(len(found), 1)
                with found[0].open(encoding="utf-8", newline="") as handle:
                    tracked = [
                        {key: row[key] or "" for key in psalter.ALIAS_COLUMNS}
                        for row in csv.DictReader(handle, delimiter="\t")
                        if row["cited_locus"].split(".")[0] == psalter.PSALMS_TOKEN
                    ]
                self.assertEqual(
                    tracked,
                    psalter.derive_aliases(edition, numbering),
                    f"{edition}: run `python3 scripts/_psalter.py {edition}`",
                )

    def test_every_alias_table_carries_all_four_columns(self):
        """A two-column header cannot record a departure, and read as though it had.

        That is what the Clementine's table was: `cited_locus` and `resolves_to`
        and no `kind` or `note`, so an edition recording no departures and one
        that could not record any looked exactly alike.
        """
        for edition, (_, where) in sorted(psalter.EDITIONS.items()):
            with self.subTest(edition=edition):
                found = sorted((psalter.WORKS / where).glob("verse-aliases-*/verse-aliases.tsv"))
                self.assertEqual(len(found), 1)
                with found[0].open(encoding="utf-8", newline="") as handle:
                    columns = tuple(csv.reader(handle, delimiter="\t").__next__())
                self.assertEqual(columns, psalter.ALIAS_COLUMNS)

    def test_a_table_missing_the_kind_column_is_refused(self):
        import tempfile

        with tempfile.TemporaryDirectory(dir=ROOT / "build") as where:
            root = Path(where)
            (root / "artifacts" / "verse-aliases-0000dead").mkdir(parents=True)
            (root / "artifacts" / "verse-aliases-0000dead" / "verse-aliases.tsv").write_text(
                "cited_locus\tresolves_to\n", encoding="utf-8"
            )
            with self.assertRaises(projection.ProjectionError) as caught:
                projection.alias_rows(root)
        self.assertIn("every table must carry", str(caught.exception))

    def test_the_hebrew_editions_leave_sixteen_psalms_undecidable(self):
        """Reported rather than passed over: an unchecked psalm must not read as checked."""
        self.assertEqual(len(psalter.undecided("hebrew")), 16)
        self.assertEqual(psalter.undecided("vulgate"), [])
        for edition in ("king-james-version", "revised-version-1895",
                        "world-english-bible-catholic"):
            with self.subTest(edition=edition):
                numbering, where = psalter.EDITIONS[edition]
                self.assertEqual(psalter.obligations(where, numbering), {})


if __name__ == "__main__":
    unittest.main()
