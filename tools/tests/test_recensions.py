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

COVERAGE = """\
recension_coverage:
  schema: triptych-recension-coverage/v1
  as_of: '2026-08-26'
  status: structural-only
  domains:
    calendar:
      state: structural-only
      basis: One fixture departure is established.
    precedence:
      state: unexamined
      basis: The fixture makes no precedence claim.
    propers:
      state: inherited-uncollated
      basis: Fixture text is carried only to exercise inheritance.
    commons:
      state: unexamined
      basis: The fixture makes no Common claim.
    ordinary:
      state: out-of-scope
      basis: The fixture does not model an Ordinary.
    ceremonies:
      state: structural-only
      basis: The fixture models only a structural departure.
  inheritance:
    source_calendar: base
    status: uncollated
    basis: Inherited entries exercise mechanics and do not assert collation.
  evidence:
  - id: fixture-structure
    domains: [calendar, ceremonies]
    grade: source-read
    record: records/fixture.toml
    basis: This synthetic fixture is the source for its own expected structure.
    witnesses: [synthetic-base]
  blockers:
  - id: fixture-not-a-corpus
    kind: scope-exclusion
    status: open
    record: records/fixture.toml
    requirement: This fixture is not a complete missal corpus.
"""


def recension(rows: str, header: str = "") -> str:
    return (
        "schema: triptych-calendar-masses/v1\n"
        "edition: An Older Missal\n"
        "edition_short: Older\n"
        "calendar: older\n"
        "text_from: base\n"
        + ("" if header == "-" else "stands_before: [some-act-1955, other-act-1955]\n")
        + (header if header != "-" else "")
        + COVERAGE
        + "sections:\n  seasonal:\n    kind: seasonal\n    masses:\n"
        + textwrap.indent(textwrap.dedent(rows), "    ")
    )


class RecensionTest(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = TemporaryDirectory()
        repository = Path(self._dir.name)
        self.root = repository / "calendars"
        self.root.mkdir()
        inventories = repository / "inventories"
        inventories.mkdir()
        (inventories / _calendars.RECENSION_ACT_INVENTORY).write_text(
            'acts_schema = 1\nextends = "fixture-acts-base.toml"\n',
            encoding="utf-8",
        )
        (inventories / "fixture-acts-base.toml").write_text(
            "acts_schema = 1\n"
            "[[acts]]\nid = \"some-act-1955\"\n"
            "[[acts]]\nid = \"other-act-1955\"\n",
            encoding="utf-8",
        )
        records = repository / "records"
        records.mkdir()
        (records / "fixture.toml").write_text(
            'schema = "triptych-recension-test-fixture/v1"\n',
            encoding="utf-8",
        )
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

    def test_multi_hop_inheritance_keeps_the_terminal_text_residence(self):
        """A middle projection is not the printing from which its words were read."""
        (self.root / "middle").mkdir()
        (self.root / "middle" / "propers.yaml").write_text(
            "schema: triptych-calendar-masses/v1\n"
            "calendar: middle\n"
            "text_from: base\n"
            "sections: {}\n",
            encoding="utf-8",
        )
        (self.root / "leaf").mkdir()
        (self.root / "leaf" / "propers.yaml").write_text(
            "schema: triptych-calendar-masses/v1\n"
            "calendar: leaf\n"
            "text_from: middle\n"
            "sections: {}\n",
            encoding="utf-8",
        )
        mass = _calendars.mass_index(
            _calendars.load_document(self.root, "leaf")
        )["kept"]
        self.assertEqual(mass["recension"]["calendar"], "base")
        self.assertEqual(mass["recension"]["text_from"], "base")

    def test_multi_hop_overlay_keeps_the_terminal_text_residence(self):
        """Changing placement at the leaf does not relocate the inherited words."""
        (self.root / "middle").mkdir()
        (self.root / "middle" / "propers.yaml").write_text(
            "schema: triptych-calendar-masses/v1\n"
            "calendar: middle\n"
            "text_from: base\n"
            "sections: {}\n",
            encoding="utf-8",
        )
        (self.root / "leaf").mkdir()
        (self.root / "leaf" / "propers.yaml").write_text(
            "schema: triptych-calendar-masses/v1\n"
            "calendar: leaf\n"
            "text_from: middle\n"
            "sections:\n"
            "  seasonal:\n"
            "    masses:\n"
            "    - key: kept\n"
            "      name: Kept elsewhere\n"
            "      departure: moved\n"
            "      basis: A fixture act moved it.\n",
            encoding="utf-8",
        )
        mass = _calendars.mass_index(
            _calendars.load_document(self.root, "leaf")
        )["kept"]
        self.assertEqual(mass["name"], "Kept elsewhere")
        self.assertEqual(mass["recension"]["kind"], "moved")
        self.assertEqual(mass["recension"]["text_from"], "base")

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

    def test_act_history_stations_are_resolved_and_survive_the_stamp(self):
        self.write("""\
            - key: shifted
              name: Sabbato Sancto
              registry: '3'
              season: lent
              departure: moved
              act: some-act-1955
              basis: Section 9 of the decree.
              also:
              - departure: renamed
                act: other-act-1955
                basis: The later station records the renamed service.
            """)
        stamp = self.masses()["shifted"]["recension"]
        self.assertEqual(stamp["act"], "some-act-1955")
        self.assertEqual(stamp["also"][0]["act"], "other-act-1955")
        self.assertEqual(self.problems(), [])

    def test_act_history_stations_must_resolve(self):
        self.write("""\
            - key: shifted
              name: Shifted
              registry: '3'
              season: lent
              departure: moved
              act: invented-act-1955
              basis: A decree.
              also:
              - departure: renamed
                act: Not-an-id
                basis: A later station.
            """)
        problems = self.problems()
        self.assertTrue(any("act names unknown act 'invented-act-1955'" in row for row in problems))
        self.assertTrue(any("also act is not an act id" in row for row in problems))

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

    def test_historical_claim_must_name_an_act_in_the_authoritative_inventory(self):
        self.write(
            """\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """,
            header="stands_before: [invented-act-1955]\n",
        )
        self.assertTrue(
            any("stands_before names unknown act 'invented-act-1955'" in row for row in self.problems())
        )

    def test_historical_claim_is_a_nonempty_unique_list_of_act_ids(self):
        rows = """\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """
        for header in (
            "stands_before: some-act-1955\n",
            "stands_before: []\n",
            "stands_before: [some-act-1955, some-act-1955]\n",
            "stands_before: [some-act-1955, 2]\n",
        ):
            with self.subTest(header=header):
                self.write(rows, header=header)
                self.assertTrue(any("stands_before" in row for row in self.problems()))

    def test_indirect_inheritance_cycle_is_reported_without_recursing_forever(self):
        (self.root / "middle").mkdir()
        (self.root / "middle" / "propers.yaml").write_text(
            "schema: triptych-calendar-masses/v1\n"
            "calendar: middle\n"
            "text_from: older\n"
            "sections: {}\n",
            encoding="utf-8",
        )
        self.write(
            """\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """,
            header="text_from: middle\n",
        )
        with self.assertRaisesRegex(
            ValueError, "calendar recension inheritance cycle: older -> middle -> older"
        ):
            _calendars.load_document(self.root, "older")
        self.assertTrue(
            any("older -> middle -> older" in row for row in self.problems())
        )

    def test_a_recension_must_account_for_its_coverage(self):
        text = recension("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """).replace(COVERAGE, "")
        (self.root / "older" / "propers.yaml").write_text(text, encoding="utf-8")
        self.assertTrue(any("recension_coverage must be a mapping" in p for p in self.problems()))

    def test_coverage_inheritance_must_name_the_mechanical_base(self):
        text = recension("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """).replace("source_calendar: base", "source_calendar: another")
        (self.root / "older" / "propers.yaml").write_text(text, encoding="utf-8")
        self.assertTrue(any("must equal text_from 'base'" in p for p in self.problems()))

    def test_coverage_fields_and_evidence_grades_are_closed(self):
        text = recension("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """)
        text = text.replace(
            "  status: structural-only\n",
            "  status: structural-only\n  assumed_complete: true\n",
            1,
        ).replace("grade: source-read", "grade: trustworthy")
        (self.root / "older" / "propers.yaml").write_text(text, encoding="utf-8")
        problems = self.problems()
        self.assertTrue(any("unknown fields: assumed_complete" in p for p in problems))
        self.assertTrue(any(".grade must be one of" in p for p in problems))

    def test_coverage_records_and_ids_must_resolve(self):
        text = recension("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """).replace("records/fixture.toml", "records/not-there.toml", 1)
        text = text.replace("id: fixture-not-a-corpus", "id: Not an id", 1)
        (self.root / "older" / "propers.yaml").write_text(text, encoding="utf-8")
        problems = self.problems()
        self.assertTrue(any("names missing record 'records/not-there.toml'" in row for row in problems))
        self.assertTrue(any("id is not kebab-case: 'Not an id'" in row for row in problems))

    def test_coverage_as_of_must_be_a_real_calendar_date(self):
        text = recension("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """).replace("as_of: '2026-08-26'", "as_of: '2026-99-99'")
        (self.root / "older" / "propers.yaml").write_text(text, encoding="utf-8")
        self.assertTrue(any("is not a calendar date" in p for p in self.problems()))

    def test_complete_coverage_requires_every_domain_and_inheritance_complete(self):
        text = recension("""\
            - key: kept
              name: Kept
              registry: '1'
              season: lent
              departure: renamed
              basis: A reading.
            """).replace("status: structural-only", "status: complete", 1)
        (self.root / "older" / "propers.yaml").write_text(text, encoding="utf-8")
        problems = self.problems()
        self.assertTrue(any("domains are not complete" in p for p in problems))
        self.assertTrue(any("inheritance.status is not complete" in p for p in problems))
        self.assertTrue(any("complete but blockers remain" in p for p in problems))


class TrackedRecensionTest(unittest.TestCase):
    """The recension this repository actually ships, held to its own rules."""

    root = ROOT / "src" / "sources" / "calendars"

    def test_the_pre_1955_recension_states_no_broken_departure(self):
        self.assertEqual(_calendars.recension_problems(self.root, "roman-pre-1955"), [])

    def test_coverage_names_every_domain_and_the_uncollated_inheritance(self):
        document = _calendars.load_document(self.root, "roman-pre-1955", effective=False)
        coverage = document["recension_coverage"]
        self.assertEqual(coverage["status"], "structural-only")
        self.assertEqual(
            set(coverage["domains"]),
            set(_calendars.RECENSION_COVERAGE_DOMAINS),
        )
        self.assertEqual(coverage["domains"]["propers"]["state"], "none")
        self.assertEqual(coverage["domains"]["commons"]["state"], "inherited-uncollated")
        self.assertEqual(coverage["domains"]["precedence"]["state"], "partial")
        self.assertEqual(coverage["inheritance"]["source_calendar"], "roman-1962")
        self.assertEqual(coverage["inheritance"]["status"], "uncollated")
        advisory = document["advisory"].lower()
        self.assertIn("structural-only", advisory)
        self.assertIn("not a complete 1920 missal corpus", advisory)
        self.assertIn("six holy week departures", advisory)
        self.assertIn("st joseph the worker", advisory)
        self.assertIn("queenship of the blessed virgin mary", advisory)
        self.assertIn("roman-1962", advisory)
        self.assertIn("inherited and uncollated", advisory)
        self.assertIn(
            "implement-criteria-precedence",
            {row["id"] for row in coverage["blockers"]},
        )
        self.assertEqual(
            document["stands_before"],
            ["de-rubricis-simpliciorem-1955", "maxima-redemptionis-1955"],
        )

    def test_it_retains_the_sourced_departures_the_design_named(self):
        document = _calendars.load_document(self.root, "roman-pre-1955", effective=False)
        stated = {str(m.get("key")) for _, _, m in _calendars.departures_of(document)}
        self.assertLessEqual(
            {
                "palm-sunday",
                "blessing-of-palms",
                "chrism-mass",
                "mass-of-the-lords-supper",
                "good-friday",
                "easter-vigil",
                "s-ioseph-opificis-sponsi-beatae-mariae",
                "beatae-mariae-virginis-reginae",
            },
            stated,
        )

    def test_exact_post_1954_absences_are_source_bounded_and_not_served(self):
        raw = _calendars.load_document(self.root, "roman-pre-1955", effective=False)
        stated = {
            mass["key"]: (section, mass)
            for section, _, mass in _calendars.departures_of(raw)
        }
        expected = {
            "s-ioseph-opificis-sponsi-beatae-mariae":
                ("sanctoral", "05-01", "I", "sanctoral"),
            "beatae-mariae-virginis-reginae":
                ("marian", "05-31", "II", "marian"),
        }
        for key, (section, date, rank, kind) in expected.items():
            held_section, row = stated[key]
            self.assertEqual(held_section, section)
            self.assertEqual(row["departure"], "absent")
            self.assertEqual((row["date"], row["rank"], row["kind"]), (date, rank, kind))
            self.assertNotIn("act", row)
            basis = row["basis"]
            self.assertIn("missale-romanum-1962-facsimile-rights-v1.toml", basis)
            self.assertIn("St Pius X negative was corrected as false", basis)
        served = _calendars.mass_index(
            _calendars.load_document(self.root, "roman-pre-1955")
        )
        for key in expected:
            self.assertNotIn(key, served)

    def test_the_chrism_mass_is_not_served_under_this_recension(self):
        """The pre-1955 books print one Mass on Holy Thursday; `absent` removes it."""
        served = _calendars.mass_index(_calendars.load_document(self.root, "roman-pre-1955"))
        self.assertNotIn("chrism-mass", served)
        self.assertIn("mass-of-the-lords-supper", served)
        base = _calendars.mass_index(_calendars.load_document(self.root, "roman-1962"))
        self.assertIn("chrism-mass", base)

    def test_holy_week_gaps_are_typed_absences_not_placeholder_propers(self):
        """Structural departures never manufacture an appointed Proper slot."""
        document = _calendars.load_document(self.root, "roman-pre-1955", effective=False)
        holy_week = {
            "palm-sunday", "blessing-of-palms", "chrism-mass",
            "mass-of-the-lords-supper", "good-friday", "easter-vigil",
        }
        for _, _, mass in _calendars.departures_of(document):
            if mass.get("key") not in holy_week:
                continue
            self.assertNotIn("propers", mass, mass.get("key"))
            status = mass.get("text_status")
            self.assertIsInstance(status, dict, mass.get("key"))
            self.assertEqual(status.get("state"), "unavailable", mass.get("key"))
            self.assertEqual(
                status.get("scope"), "missal-formulary", mass.get("key")
            )
            self.assertEqual(
                [row.get("kind") for row in status.get("reasons") or []],
                ["witness-gap"],
                mass.get("key"),
            )

    def test_holy_week_departure_stations_are_exact(self):
        document = _calendars.load_document(self.root, "roman-pre-1955", effective=False)
        rows = {mass["key"]: mass for _, _, mass in _calendars.departures_of(document)}
        maxima = "maxima-redemptionis-1955"
        self.assertEqual(rows["palm-sunday"]["act"], maxima)
        self.assertEqual(rows["blessing-of-palms"]["act"], maxima)
        self.assertNotIn("act", rows["chrism-mass"])
        self.assertEqual(rows["mass-of-the-lords-supper"]["act"], maxima)
        self.assertEqual(rows["good-friday"]["act"], "editio-typica-1962")
        self.assertEqual(
            [(row["departure"], row.get("act")) for row in rows["good-friday"]["also"]],
            [("moved", maxima), ("renamed", maxima), ("unrecorded", "editio-typica-1962")],
        )
        self.assertEqual(rows["easter-vigil"]["act"], maxima)

    def test_it_serves_the_rest_of_the_year_from_a_named_printing(self):
        served = _calendars.mass_index(_calendars.load_document(self.root, "roman-pre-1955"))
        self.assertGreater(len(served), 400)
        self.assertEqual(served["advent-1"]["recension"]["text_from"], "roman-1962")

    def test_a_linearized_rubrics_source_discloses_its_limit(self):
        """A table-shaped approximation must not present itself as the five criteria."""
        path = self.root / "roman-pre-1955" / "rubrics.yaml"
        if not path.exists():
            return
        document = _calendars.read_yaml(path)
        advisory = str(document.get("advisory") or "").lower()
        self.assertIn("linearization", advisory)
        self.assertIn("not the rule itself", advisory)
        self.assertTrue(document.get("divergences"))


class RubricsSourcingRecordTest(unittest.TestCase):
    """The sourcing record's counts, checked against its own rows.

    This repository has held one census in three copies that all disagreed, and
    a hand-typed total beside the rows it totals is that defect in miniature.
    The counts stay in the file, because a reader wants them there; what stops
    them drifting is here.
    """

    path = ROOT / "src" / "sources" / "inventories" / "pre-1955-rubrics-sources-v1.toml"

    def setUp(self) -> None:
        import tomllib

        self.record = tomllib.loads(self.path.read_text(encoding="utf-8"))

    def test_the_counts_are_the_rows(self):
        counts = self.record["counts"]
        self.assertEqual(counts["findings_verified"], len(self.record["findings"]))
        self.assertEqual(counts["sources_located"], len(self.record["located"]))
        self.assertEqual(counts["books_still_wanted"], len(self.record["wanted"]))
        self.assertEqual(
            counts["repositories_searched"], len(self.record["repositories_searched"])
        )
        self.assertEqual(
            counts["sources_located_that_may_be_published"],
            sum(1 for row in self.record["located"] if row.get("may_publish_text") == "yes"),
        )

    def test_every_located_source_states_a_rights_position(self):
        allowed = {
            "public-domain-us-pre-1931",
            "holy-see-post-1929",
            "third-party-copyright",
            "mixed",
            "unresolved",
        }
        for row in [*self.record["located"], *self.record["held"]]:
            self.assertIn(row.get("rights"), allowed, row["id"])
            self.assertIn(row.get("may_publish_text"), {"yes", "no", "mixed", "unresolved"}, row["id"])

    def test_the_faithful_source_and_linearized_finding_aid_stay_distinct(self):
        """Shipping a bounded approximation does not claim criteria support."""
        shipped = (ROOT / "src" / "sources" / "calendars" / "roman-pre-1955" / "rubrics.yaml").exists()
        writable = self.record["counts"]["rubrics_sources_this_record_makes_writable"]
        linearized = self.record["counts"]["linearized_finding_aids_shipped"]
        self.assertEqual(writable, 0)
        self.assertEqual(linearized, int(shipped))
        if shipped:
            document = _calendars.read_yaml(
                ROOT / "src" / "sources" / "calendars" / "roman-pre-1955" / "rubrics.yaml"
            )
            advisory = str(document.get("advisory") or "").lower()
            self.assertIn("linearization", advisory)
            self.assertIn("not the rule itself", advisory)


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
