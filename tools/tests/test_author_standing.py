"""The author-standing registry: one row per person, every standing cited.

A study's two-author rule means nothing if "Father or saint" is whatever the
harvest's model tagged. These tests keep the one record of standing honest: the
tracked registry validates and covers every liturgical commentary and every
published lane author, and a sandbox registry is refused for a standing outside
the closed set, a basis citing nothing or citing a record the library does not
have, a name given to two people, and a censure that does not say what it
censured.
"""
from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _standing  # noqa: E402


class TrackedRegistryTests(unittest.TestCase):
    def test_the_tracked_registry_validates(self) -> None:
        self.assertEqual(_standing.validate(ROOT), [])

    def test_every_commentary_author_and_lane_author_has_a_row(self) -> None:
        report = _standing.report(ROOT)
        self.assertEqual(report["uncovered"], {"liturgical_commentaries": [], "lane_authors": []})

    def test_lookups_by_namespace_and_by_name(self) -> None:
        registry = _standing.Registry(ROOT)
        self.assertEqual(registry.for_work("work.augustine-of-hippo.sermones")["id"], "augustine")
        self.assertEqual(registry.for_name("  st   AUGUSTINE ")["id"], "augustine")
        self.assertEqual(registry.for_work("work.ildefonso-schuster.the-sacramentary")["standing"], "blessed")
        self.assertIsNone(registry.for_name("Origen"))

    def test_the_recorded_censures(self) -> None:
        registry = _standing.Registry(ROOT)
        self.assertEqual(registry.by_id["amalarius-of-metz"]["censures"][0]["year"], "838")
        self.assertEqual(registry.by_id["theodoret-of-cyrus"]["censures"][0]["year"], "553")

    def test_the_continuator_is_his_own_person(self) -> None:
        registry = _standing.Registry(ROOT)
        self.assertEqual(registry.by_id["lucien-fromage"]["standing"], "ecclesiastical-writer")
        self.assertEqual(registry.for_work("work.prosper-gueranger.the-liturgical-year")["id"], "prosper-gueranger")


class SandboxRegistryTests(unittest.TestCase):
    ROW = """\
        [[persons]]
        id = "rupert-of-deutz"
        namespaces = ["rupert-of-deutz"]
        name = "Rupert of Deutz"
        names = ["Rupert of Deutz"]
        died = "1135"
        standing = "ecclesiastical-writer"
        standing_basis = "Abbot of Deutz."
        basis_sources = ["https://www.newadvent.org/cathen/07694a.htm"]
        confession = "Catholic"
        """

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        work = self.root / "src/sources/works/rupert-of-deutz/de-divinis-officiis"
        work.mkdir(parents=True)
        (work / "work.toml").write_text('id = "work.rupert-of-deutz.de-divinis-officiis"\n', encoding="utf-8")

    def errors(self, rows: str) -> list[str]:
        path = self.root / _standing.REGISTRY_RELATIVE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            'schema = "triptych-author-standing/v1"\nrecord_type = "author-standing"\n'
            'audited_on = "2026-09-22"\n\n' + textwrap.dedent(rows),
            encoding="utf-8",
        )
        return _standing.validate(self.root)

    def test_a_well_formed_row_validates(self) -> None:
        self.assertEqual(self.errors(self.ROW), [])

    def test_a_standing_outside_the_set_is_refused(self) -> None:
        errors = self.errors(self.ROW.replace('"ecclesiastical-writer"', '"saintly"'))
        self.assertTrue(any("standing is 'saintly'" in e for e in errors), errors)

    def test_a_basis_citing_nothing_is_refused(self) -> None:
        errors = self.errors(self.ROW.replace('["https://www.newadvent.org/cathen/07694a.htm"]', "[]"))
        self.assertTrue(any("basis_sources" in e for e in errors), errors)

    def test_a_cited_record_the_library_lacks_is_refused(self) -> None:
        errors = self.errors(
            self.ROW.replace('"https://www.newadvent.org/cathen/07694a.htm"', '"work.rupert-of-deutz.no-such-work"')
        )
        self.assertTrue(any("not a record in the library" in e for e in errors), errors)

    def test_a_cited_record_the_library_has_is_accepted(self) -> None:
        self.assertEqual(
            self.errors(
                self.ROW.replace(
                    '"https://www.newadvent.org/cathen/07694a.htm"', '"work.rupert-of-deutz.de-divinis-officiis"'
                )
            ),
            [],
        )

    def test_one_name_for_two_people_is_refused(self) -> None:
        second = self.ROW.replace('id = "rupert-of-deutz"', 'id = "someone-else"').replace(
            'namespaces = ["rupert-of-deutz"]', "namespaces = []"
        ).replace('name = "Rupert of Deutz"', 'name = "Rupert of Deutz"')
        errors = self.errors(self.ROW + "\n" + second)
        self.assertTrue(any("one name, one person" in e for e in errors), errors)

    def test_a_namespace_the_library_lacks_is_refused(self) -> None:
        errors = self.errors(self.ROW.replace('namespaces = ["rupert-of-deutz"]', 'namespaces = ["rupertus"]'))
        self.assertTrue(any("namespace 'rupertus'" in e for e in errors), errors)

    def test_an_unknown_field_is_refused(self) -> None:
        errors = self.errors(self.ROW.replace('confession = "Catholic"', 'confession = "Catholic"\nrole = "saintly"'))
        self.assertTrue(any("unknown fields: role" in e for e in errors), errors)

    def test_a_censure_must_say_what_it_censured(self) -> None:
        errors = self.errors(
            self.ROW
            + '\n[[persons.censures]]\nbody = "a synod"\nyear = "838"\nsource = "https://www.newadvent.org/cathen/01376b.htm"\n'
        )
        self.assertTrue(any("states no point" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
