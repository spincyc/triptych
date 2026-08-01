"""A recension is a base plus its departures, and never a second copy of it.

`guidance/recensions.md` was written before any data moved, because the shape is
cheap to choose and expensive to change once a second calendar exists in the
tree. Its Rule 2 says a recension is stored as its departures from a base; its
Rule 2a separates attestation from residence, so a text lives once and the
printings that attest it are recorded per printing; its Rule 3 says a departure
that cannot be established is recorded `unrecorded` and never silently falls
back to the base.

The reason those rules are worth a mechanism rather than a convention is on the
record. This repository held four Sundays' orations twice, and the copies had
already drifted five ways with nothing comparing them. A second full calendar
would have been the largest such copy in the tree — 490 masses and 2,312
propers restated to change a tenth of them.

So the rules held here are the ones that make a departure safe to trust: it
names a mass the base actually holds, it says which of the seven kinds it is, it
says what established it, and it can carry more than one kind at once because
the Triduum is where one liturgy departs several ways simultaneously. The last
test is the one that matters most: an entry the recension says nothing about
must arrive stamped with the calendar it was read from, so a page can tell
"attested in both printings" from "attested only in the 1962 printing" instead
of claiming the stronger one for free.
"""

from __future__ import annotations

import sys
import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402

BASE = """\
schema: triptych-calendar-masses/v1
edition: A Missal
edition_short: Base
calendar: base
sections:
  seasonal:
    kind: seasonal
    masses:
    - key: kept
      name: Kept
      registry: '1'
      season: lent
      propers:
      - name: Collect
        source: composed
        text: Oremus.
    - key: gone
      name: Gone
      registry: '2'
      season: lent
      propers:
      - name: Collect
        source: composed
        text: Abibit.
    - key: shifted
      name: Shifted
      registry: '3'
      season: lent
      propers:
      - name: Collect
        source: composed
        text: Movetur.
"""


def recension(rows: str, header: str = "") -> str:
    return (
        "schema: triptych-calendar-masses/v1\n"
        "edition: An Older Missal\n"
        "edition_short: Older\n"
        "calendar: older\n"
        "text_from: base\n"
        + ("" if header == "-" else "stands_before: some-act-1955\n")
        + (header if header != "-" else "")
        + "sections:\n  seasonal:\n    kind: seasonal\n    masses:\n"
        + textwrap.indent(textwrap.dedent(rows), "    ")
    )


class RecensionTest(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = TemporaryDirectory()
        self.root = Path(self._dir.name)
        (self.root / "base").mkdir()
        (self.root / "base" / "propers.yaml").write_text(BASE, encoding="utf-8")
        (self.root / "older").mkdir()
        self.addCleanup(self._dir.cleanup)

    def write(self, rows: str, header: str = "") -> None:
        (self.root / "older" / "propers.yaml").write_text(
            recension(rows, header), encoding="utf-8"
        )

    def masses(self) -> dict:
        return _calendars.mass_index(_calendars.load_document(self.root, "older"))

    def problems(self) -> list[str]:
        return _calendars.recension_problems(self.root, "older")

    # -- the shape ---------------------------------------------------------

    def test_a_calendar_with_no_base_is_returned_exactly_as_written(self):
        """The two existing calendars must be untouched by this path."""
        document = _calendars.load_document(self.root, "base")
        self.assertEqual(sorted(_calendars.mass_index(document)), ["gone", "kept", "shifted"])
        self.assertNotIn("recension", _calendars.mass_index(document)["kept"])

    def test_a_recension_inherits_every_entry_it_says_nothing_about(self):
        """Rule 2: the shared remainder has exactly one home, in the base."""
        self.write("""\
            - key: shifted
              name: Moved Elsewhere
              registry: '3'
              season: lent
              departure: moved
              basis: A decree says so.
            """)
        self.assertIn("kept", self.masses())
        self.assertEqual(self.masses()["kept"]["propers"][0]["text"], "Oremus.")

    def test_an_inherited_entry_says_which_printing_it_was_read_from(self):
        """Rule 2a: a text attested by only one printing says so."""
        self.write("""\
            - key: gone
              name: Gone
              registry: '2'
              season: lent
              departure: absent
              basis: Not in the witness.
            """)
        stamp = self.masses()["kept"]["recension"]
        self.assertEqual(stamp["text_from"], "base")
        self.assertFalse(stamp["stated"])
        self.assertEqual(stamp["kind"], "")

    # -- the seven kinds ---------------------------------------------------

    def test_absent_removes_the_mass_from_the_served_calendar(self):
        self.write("""\
            - key: gone
              name: Gone
              registry: '2'
              season: lent
              departure: absent
              basis: A whole-file search of the witness returns nothing.
            """)
        self.assertNotIn("gone", self.masses())
        self.assertEqual(self.problems(), [])

    def test_added_brings_a_mass_the_base_has_never_held(self):
        self.write("""\
            - key: extra
              name: Extra
              registry: '4'
              season: lent
              departure: added
              basis: The older book prints it.
              propers:
              - name: Collect
                source: composed
                text: Additur.
            """)
        self.assertIn("extra", self.masses())
        self.assertTrue(self.masses()["extra"]["recension"]["stated"])
        self.assertEqual(self.problems(), [])

    def test_moved_keeps_the_base_formulary_and_overlays_only_what_it_restates(self):
        """Saying the liturgy is the same one and reprinting it is the copy Rule 2 refuses."""
        self.write("""\
            - key: shifted
              name: Sabbato Sancto
              registry: '3'
              season: lent
              departure: moved
              basis: The decree moved it to the night.
            """)
        found = self.masses()["shifted"]
        self.assertEqual(found["name"], "Sabbato Sancto")
        self.assertEqual(found["propers"][0]["text"], "Movetur.")

    def test_unrecorded_carries_the_base_entry_but_never_silently(self):
        """Rule 3: it resolves to nothing claimed, not to the base as though checked."""
        self.write("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: unrecorded
              basis: The witnesses differ and no act was found.
            """)
        stamp = self.masses()["kept"]["recension"]
        self.assertEqual(stamp["kind"], "unrecorded")
        self.assertFalse(stamp["stated"])

    def test_replaced_lets_the_recension_state_its_own_entry(self):
        self.write("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: replaced
              basis: The older book prints another prayer.
              propers:
              - name: Collect
                source: composed
                text: Aliud.
            """)
        found = self.masses()["kept"]
        self.assertEqual(found["propers"][0]["text"], "Aliud.")
        self.assertTrue(found["recension"]["stated"])

    # -- one liturgy departing several ways at once ------------------------

    def test_a_row_carries_further_kinds_under_also(self):
        """The pre-1955 Holy Saturday is moved, renamed and replaced at once."""
        self.write("""\
            - key: shifted
              name: Sabbato Sancto
              registry: '3'
              season: lent
              departure: moved
              basis: Section 9 of the decree.
              also:
              - departure: replaced
                basis: Twelve prophecies against four lessons.
              - departure: renamed
                basis: The book prints DE VIGILIA PASCHALI beneath the day.
            """)
        stamp = self.masses()["shifted"]["recension"]
        self.assertEqual([row["kind"] for row in stamp["also"]], ["replaced", "renamed"])
        self.assertEqual(self.problems(), [])

    def test_also_may_not_repeat_the_primary_kind(self):
        self.write("""\
            - key: shifted
              name: Shifted
              registry: '3'
              season: lent
              departure: moved
              basis: A decree.
              also:
              - departure: moved
                basis: The same decree again.
            """)
        self.assertTrue(any("repeats the primary kind" in p for p in self.problems()))

    def test_every_also_row_is_held_to_the_primary_rows_standard(self):
        self.write("""\
            - key: shifted
              name: Shifted
              registry: '3'
              season: lent
              departure: moved
              basis: A decree.
              also:
              - departure: invented
                basis: Something.
            """)
        self.assertTrue(any("must be one of" in p for p in self.problems()))

    # -- the refusals ------------------------------------------------------

    def test_a_departure_naming_a_mass_the_base_lacks_is_refused(self):
        """Worse than a dangling pointer: it would remove a Mass that is not there."""
        self.write("""\
            - key: nowhere
              name: Nowhere
              registry: '9'
              season: lent
              departure: absent
              basis: Not in the witness.
            """)
        self.assertTrue(any("does not hold" in p for p in self.problems()))

    def test_added_may_not_name_a_mass_the_base_already_holds(self):
        self.write("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: added
              basis: The older book prints it.
              propers:
              - name: Collect
                source: composed
                text: Iterum.
            """)
        self.assertTrue(any("that is `replaced`, not `added`" in p for p in self.problems()))

    def test_an_unknown_departure_kind_is_refused(self):
        self.write("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: tweaked
              basis: Something changed.
            """)
        self.assertTrue(any("departure must be one of" in p for p in self.problems()))

    def test_a_departure_with_no_basis_is_refused(self):
        """A difference with no basis is a difference someone asserted."""
        self.write("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: absent
            """)
        self.assertTrue(any("states no basis" in p for p in self.problems()))

    def test_the_same_key_may_not_be_departed_in_twice(self):
        self.write("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: One reading.
            - key: kept
              name: Kept Again
              registry: '1'
              season: lent
              departure: moved
              basis: Another reading.
            """)
        self.assertTrue(any("stated twice" in p for p in self.problems()))

    def test_a_base_that_does_not_exist_is_refused(self):
        (self.root / "older" / "propers.yaml").write_text(
            recension("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """).replace("text_from: base", "text_from: nowhere"),
            encoding="utf-8",
        )
        self.assertTrue(any("no propers.yaml for" in p or "has no" in p for p in self.problems()))

    def test_a_mechanical_base_without_a_historical_claim_is_refused(self):
        """`text_from` records where text was transcribed; it is not a claim of descent."""
        self.write(
            """\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """,
            header="-",
        )
        self.assertTrue(any("stands_before" in p for p in self.problems()))


class TrackedRecensionTest(unittest.TestCase):
    """The recension this repository actually ships, held to its own rules."""

    root = ROOT / "src" / "sources" / "calendars"

    def test_the_pre_1955_recension_states_no_broken_departure(self):
        self.assertEqual(_calendars.recension_problems(self.root, "roman-pre-1955"), [])

    def test_it_departs_in_the_four_liturgies_the_design_named(self):
        document = _calendars.load_document(self.root, "roman-pre-1955", effective=False)
        stated = {str(m.get("key")) for _, _, m in _calendars.departures_of(document)}
        self.assertEqual(
            stated,
            {
                "palm-sunday",
                "blessing-of-palms",
                "mass-of-the-lords-supper",
                "good-friday",
                "easter-vigil",
            },
        )

    def test_it_carries_no_transcribed_text(self):
        """No source text routes through this file; every proper is a placeholder."""
        document = _calendars.load_document(self.root, "roman-pre-1955", effective=False)
        for _, _, mass in _calendars.departures_of(document):
            for proper in mass.get("propers") or []:
                self.assertEqual(proper.get("name"), "Placeholder", mass.get("key"))

    def test_it_serves_the_rest_of_the_year_from_a_named_printing(self):
        served = _calendars.mass_index(_calendars.load_document(self.root, "roman-pre-1955"))
        self.assertGreater(len(served), 400)
        self.assertEqual(served["advent-1"]["recension"]["text_from"], "roman-1962")

    def test_it_ships_no_rubrics_source_so_the_selector_cannot_offer_it(self):
        """The 1962 precedence table answers to the 1960 code and is not this book's."""
        self.assertFalse((self.root / "roman-pre-1955" / "rubrics.yaml").exists())


def _calendar_rubrics():
    """The `calendar-rubrics` tool, imported from a file with no `.py` suffix."""
    import importlib.machinery
    import importlib.util

    spec = importlib.util.spec_from_loader(
        "calendar_rubrics",
        importlib.machinery.SourceFileLoader("calendar_rubrics", str(ROOT / "tools" / "calendar-rubrics")),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OneWayToResolveADayTest(unittest.TestCase):
    """Every tool that reads a calendar reads the same derivation.

    `calendar-days` and `mass-propers` go through `_calendars.load_document`;
    `calendar-rubrics` used to parse `propers.yaml` itself. For the two
    non-recension calendars the two routes agree, which is why the divergence
    went unnoticed --- and for a recension they differ by four hundred and
    eighty-six masses, because a recension's file states only its departures.
    Rubrics read the short way would decide five days and be silent about the
    rest while the browser served all of them.
    """

    root = ROOT / "src" / "sources" / "calendars"

    def setUp(self) -> None:
        self.tool = _calendar_rubrics()

    def test_rubrics_see_every_mass_the_recension_serves(self):
        served = _calendars.mass_index(_calendars.load_document(self.root, "roman-pre-1955"))
        classified = self.tool.load_masses(self.root, "roman-pre-1955")
        # The Commune is formularies rather than days and `load_masses` drops it,
        # so the rubrics see fewer keys than the calendar serves; what matters is
        # that they see the inherited year and not the five departure rows.
        self.assertGreater(len(classified), 400)
        self.assertLessEqual(len(classified), len(served))
        self.assertIn("advent-1", classified)

    def test_a_recensions_formularies_include_the_ones_it_inherits(self):
        formularies = self.tool.all_formularies(self.root, "roman-pre-1955")
        self.assertIn("commune-virginum-1", formularies)
        self.assertIn("blessing-of-palms", formularies)

    def test_a_calendar_that_is_nobodys_recension_is_read_exactly_as_before(self):
        import yaml

        raw = yaml.safe_load(
            (self.root / "roman-1962" / "propers.yaml").read_text(encoding="utf-8")
        )
        direct = {
            str(mass["key"])
            for body in (raw.get("sections") or {}).values()
            for mass in ((body or {}).get("masses") or [])
            if isinstance(mass, dict) and mass.get("key")
        }
        self.assertEqual(self.tool.all_formularies(self.root, "roman-1962"), direct)


if __name__ == "__main__":
    unittest.main()
