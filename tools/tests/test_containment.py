"""Containment: what the library holds of a commentary lead, through its containers.

The defect this guards against is a false absence. A sweep that asked each lead
by its own work record reported Aquinas's commentary on Matthew as not held
while the Venice tomus that prints it entire sat in the library, three review
rounds running. So the first tests are that a holding reached only through a
container is surfaced, that a container whose extent stops short of the passage
says so instead of claiming it, and that a lead nothing joins is reported as
having no holding rather than silently dropped. The rest are the check that
keeps the inventory true: a container nobody entered, an entry naming a record
the library does not have, and an extent that does not parse are each refused.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _containment  # noqa: E402

BOOK_INDEX = (
    "ordinal\ttoken\tfile\ttestament\tdouay_title\tmodern_name\t"
    "missal_latin_abbreviation\talternate_names\n"
    "19\tPs\t19-psalms.tsv\told\tThe Book of Psalms\tPsalms\tPs.\tPs.\n"
    "47\tMatt\t47-matthew.tsv\tnew\tThe Holy Gospel according to St. Matthew\tMatthew\tMatth.\tMt\n"
)

# The records a sweep meets: a Migne volume holding part of a work that also has
# its own record, and a collected-works tome holding a work that has none.
PL37 = "work.migne.pl-37"
TOMUS = "work.aquinas.tomus-3"
ENARRATIONES = "work.augustine.enarrationes"


class ContainmentFixture(unittest.TestCase):
    """A library of three works, an index of three leads, and an inventory."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.addCleanup(self.forget)
        self.write(
            "src/sources/works/catholic-church/vulgata-clementina/editions/"
            "ebible-latvuc/artifacts/book-index-fcad78c2/book-index.tsv",
            BOOK_INDEX,
        )
        for token, chapter, verses in (
            ("Ps", 1, 6), ("Ps", 20, 14), ("Ps", 79, 13), ("Ps", 80, 20),
            ("Ps", 81, 16), ("Ps", 95, 13), ("Ps", 150, 6),
            ("Matt", 9, 38), ("Matt", 28, 20),
        ):
            self.write(
                f"src/sources/bibles/clementine-vulgate/chapters/{token}/{chapter}.json",
                json.dumps({"book": token, "chapter": chapter,
                            "verses": {str(n): "text" for n in range(1, verses + 1)}}),
            )
        self.work(PL37, "Patrologiae cursus completus, Series Latina, volume 37",
                  "Jacques-Paul Migne", "collected-volume",
                  "Containing Augustine's Enarrationes in Psalmos, Psalms 80-150.")
        self.artifact(PL37, "paris-1845", "scan", "remote")
        self.work(TOMUS, "Opera, tomus tertius: Commentaria in Evangelia S. Matthaei et S. Ioannis",
                  "Thomas Aquinas; collected edition", "collected-works-volume",
                  "Holding Aquinas's lectures on Matthew and on John.")
        self.artifact(TOMUS, "venice-1745", "raw-ocr", "tracked")
        self.work(ENARRATIONES, "Enarrationes in Psalmos", "Augustine of Hippo",
                  "patristic-psalm-exposition-collection", "Augustine's expositions.")
        self.artifact(ENARRATIONES, "npnf-8", "digital-text", "tracked")
        self.write(
            "src/sources/commentary/passage-commentary-index.yaml",
            """
            schema: triptych-commentary-work-index/v1
            numbering: vulgate
            passages:
            - passage: Psalms 95
              works:
              - {author: Augustine of Hippo, title: Enarrationes in Psalmos, confidence: 1.0}
            - passage: Matthew 9
              works:
              - {author: Thomas Aquinas, title: Super Evangelium S. Matthaei lectura, confidence: 1.0}
              - {author: Nobody, title: Lost Commentary, confidence: 0.3}
            """,
        )
        self.write(
            "src/sources/commentary/work-aliases.yaml",
            """
            schema: triptych-commentary-work-aliases/v1
            groups:
            - author: Augustine of Hippo
              work: Enarrationes in Psalmos
              titles: [enarrationes in psalmos, expositions on the psalms]
            - author: Thomas Aquinas
              work: Super Evangelium S. Matthaei lectura
              titles: [super evangelium s. matthaei lectura, super matthaeum]
            """,
        )
        self.write(
            "src/sources/commentary/fragment-loci.yaml",
            "schema: triptych-commentary-fragment-loci/v1\nnumbering: vulgate\nfragments: []\n",
        )
        self.write_inventory()

    # -- the fixture's own writing -----------------------------------------

    def forget(self) -> None:
        _containment._CATALOGS.pop(self.root, None)
        _containment._IDENTITIES.pop(self.root, None)

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
        self.forget()
        return path

    def work(self, work_id: str, title: str, responsible: str, work_type: str, description: str) -> None:
        namespace, slug = work_id.split(".")[1:3]
        self.write(
            f"src/sources/works/{namespace}/{slug}/work.toml",
            f"""
            schema = 1
            record_type = "work"
            id = "{work_id}"
            title = "{title}"
            responsible = "{responsible}"
            work_type = "{work_type}"
            languages = ["la"]
            description = "{description}"
            """,
        )

    def artifact(self, work_id: str, edition: str, kind: str, storage: str) -> str:
        namespace, slug = work_id.split(".")[1:3]
        edition_id = f"edition.{namespace}.{slug}.{edition}"
        artifact_id = f"artifact.{namespace}.{slug}.{edition}.{kind}"
        base = f"src/sources/works/{namespace}/{slug}/editions/{edition}"
        self.write(
            f"{base}/edition.toml",
            f"""
            schema = 1
            record_type = "edition"
            id = "{edition_id}"
            work_id = "{work_id}"
            title = "{edition}"
            language = "la"
            """,
        )
        self.write(
            f"{base}/artifacts/{kind}/artifact.toml",
            f"""
            schema = 2
            record_type = "artifact"
            id = "{artifact_id}"
            edition_id = "{edition_id}"
            artifact_type = "{kind}"
            media_type = "text/plain"
            storage = "{storage}"
            """,
        )
        return artifact_id

    def pin(self, work_id: str) -> str:
        namespace, slug = work_id.split(".")[1:3]
        path = self.root / f"src/sources/works/{namespace}/{slug}/work.toml"
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def write_inventory(
        self,
        pl37_extent: str = '["Psalms 80-150"]',
        extra: str = "",
        pl37_id: str = PL37,
        pl37_extra: str = "",
    ) -> None:
        self.write(
            "src/sources/inventories/source-containment-v1.toml",
            f"""
            schema = "triptych-source-containment/v1"
            record_type = "source-containment"
            audited_on = "2026-09-22"
            numbering = "vulgate"

            [shapes]
            work_types = ["collected-volume", "collected-works-volume"]
            description_patterns = []
            artifact_patterns = ['\\bwhole volume\\b']

            [[containers]]
            id = "{pl37_id}"
            manifest_sha256 = "{self.pin(PL37)}"
            status = "resolved"
            basis = "Description."

            [[containers.constituents]]
            author = "Augustine of Hippo"
            title = "Enarrationes in Psalmos"
            work_id = "{ENARRATIONES}"
            scripture = {pl37_extent}
            basis = "Description."
            {pl37_extra}

            [[containers]]
            id = "{TOMUS}"
            manifest_sha256 = "{self.pin(TOMUS)}"
            status = "resolved"
            basis = "Description."

            [[containers.constituents]]
            author = "Thomas Aquinas"
            title = "Super Evangelium S. Matthaei lectura"
            whole = true
            basis = "Description."
            {extra}
            """,
        )

    # -- asking ------------------------------------------------------------

    def holdings(self, author: str, title: str, citation: dict) -> dict:
        found = _containment.Holdings(self.root)
        return found.for_work(author, title, None, found.books.passage_spans(citation))

    @staticmethod
    def psalm(chapter: int, last: int | None = None) -> dict:
        return {"book": "Psalms",
                "ranges": [{"begin": {"chapter": chapter}, "end": {"chapter": last or chapter}}]}


class HoldingsTests(ContainmentFixture):
    """What discover reports beside each lead."""

    def test_a_work_held_only_inside_a_container_is_reported_held(self) -> None:
        """The run's miss, exactly: no record of its own, printed entire in a tome."""
        matthew = {"book": "Matthew", "ranges": [{"begin": {"chapter": 9, "verse": 1},
                                                  "end": {"chapter": 9, "verse": 8}}]}
        found = self.holdings("Thomas Aquinas", "Super Evangelium S. Matthaei lectura", matthew)
        self.assertEqual(found["status"], _containment.HELD_IN_CONTAINER)
        self.assertEqual(found["direct"], [])
        self.assertEqual([row["container_id"] for row in found["containers"]], [TOMUS])
        self.assertEqual(found["containers"][0]["passage"], _containment.WHOLE_WORK)
        self.assertEqual(found["containers"][0]["artifact_storage"], {"tracked": 1})

    def test_a_passage_inside_a_containers_extent_is_claimed(self) -> None:
        found = self.holdings("Augustine of Hippo", "Enarrationes in Psalmos", self.psalm(95))
        self.assertEqual(found["status"], _containment.HELD)
        self.assertEqual([d["work_id"] for d in found["direct"]], [ENARRATIONES])
        self.assertEqual(found["containers"][0]["passage"], _containment.INSIDE)

    def test_a_passage_outside_a_containers_extent_is_not_claimed(self) -> None:
        """PL 37 holds Psalms 80-150; Psalm 20 is in PL 36, which is not held."""
        found = self.holdings("Augustine of Hippo", "Enarrationes in Psalmos", self.psalm(20))
        self.assertEqual(found["containers"][0]["passage"], _containment.OUTSIDE)
        self.assertNotEqual(found["containers"][0]["passage"], _containment.INSIDE)

    def test_a_passage_straddling_the_extent_is_only_partly_claimed(self) -> None:
        found = self.holdings("Augustine of Hippo", "Enarrationes in Psalmos", self.psalm(79, 81))
        self.assertEqual(found["containers"][0]["passage"], _containment.PARTIALLY)

    def test_a_work_with_no_holding_says_so(self) -> None:
        found = self.holdings("Nobody", "Lost Commentary", self.psalm(95))
        self.assertEqual(found, {"status": _containment.NONE, "direct": [], "containers": []})

    def test_a_part_does_not_stand_in_for_a_whole_the_container_names(self) -> None:
        """A container naming the lead answers for it; a part reached by work_id does not."""
        self.write_inventory(pl37_extra=f"""
            [[containers.constituents]]
            author = "Augustine of Hippo"
            title = "Enarratio in Psalmum 1"
            work_id = "{ENARRATIONES}"
            scripture = ["Psalms 1"]
            basis = "A part."
        """)
        found = self.holdings("Augustine of Hippo", "Enarrationes in Psalmos", self.psalm(95))
        titles = [row["constituent"]["title"] for row in found["containers"]]
        self.assertEqual(titles, ["Enarrationes in Psalmos"])


class CheckTests(ContainmentFixture):
    """The check `make check-sources` runs: three refusals and a clean pass."""

    def test_the_fixture_inventory_validates(self) -> None:
        self.assertEqual(_containment.validate(self.root), [])

    def test_a_container_with_no_entry_is_refused(self) -> None:
        self.work("work.migne.pl-26", "Patrologia Latina volume 26", "Jacques-Paul Migne",
                  "collected-volume", "Jerome's commentaries.")
        errors = _containment.validate(self.root)
        self.assertTrue(
            any("work.migne.pl-26 is container-shaped" in e and "has no containment entry" in e
                for e in errors),
            errors,
        )

    def test_a_whole_volume_artifact_with_no_entry_is_refused(self) -> None:
        """A layer filed under one constituent is a container too."""
        artifact_id = self.artifact(ENARRATIONES, "migne-pl-36", "ocr", "remote")
        path = next(self.root.glob("src/sources/works/*/*/editions/migne-pl-36/artifacts/ocr/artifact.toml"))
        path.write_text(path.read_text() + 'notes = "Complete OCR of the whole volume."\n')
        self.forget()
        errors = _containment.validate(self.root)
        self.assertTrue(any(f"{artifact_id} is container-shaped" in e for e in errors), errors)

    def test_an_entry_naming_an_unknown_record_is_refused(self) -> None:
        self.write_inventory(pl37_id="work.migne.no-such-volume")
        errors = _containment.validate(self.root)
        self.assertTrue(
            any("work.migne.no-such-volume, which is not a work or artifact record" in e
                for e in errors),
            errors,
        )

    def test_a_constituent_naming_an_unknown_work_is_refused(self) -> None:
        self.write_inventory(extra="""
            [[containers.constituents]]
            author = "Thomas Aquinas"
            title = "Super Evangelium S. Ioannis lectura"
            work_id = "work.aquinas.no-such-record"
            whole = true
            basis = "Description."
        """)
        errors = _containment.validate(self.root)
        self.assertTrue(any("work.aquinas.no-such-record" in e for e in errors), errors)

    def test_a_malformed_extent_is_refused(self) -> None:
        cases = {
            '["Psalms 80-151"]': "past its last chapter 150",
            '["Psalms 95:1-8"]': "gives a verse on one end only",
            '["Psalms 95:14"]': "past its last verse 13",
            '["Psalms 150-80"]': "ends before it begins",
            '["Nonesuch 1-2"]': "names no book of the canon",
            '["Psalms eighty"]': "is not of the form",
        }
        for extent, message in cases.items():
            with self.subTest(extent=extent):
                self.write_inventory(pl37_extent=extent)
                errors = _containment.validate(self.root)
                self.assertTrue(
                    any("malformed extent" in e and message in e for e in errors), errors
                )

    def test_a_record_changed_since_review_is_refused(self) -> None:
        """The pin is the snapshot: an edited container must be re-read."""
        path = self.root / "src/sources/works/migne/pl-37/work.toml"
        path.write_text(path.read_text() + 'alternate_titles = ["PL 37"]\n')
        self.forget()
        errors = _containment.validate(self.root)
        self.assertTrue(any("changed since this entry was reviewed" in e for e in errors), errors)

    def test_a_segment_into_a_container_must_be_listed(self) -> None:
        """A segment already proves containment; the entry has to agree with it."""
        other = "work.jerome.in-matthaeum"
        self.work(other, "Commentarii in Matthaeum", "Jerome", "biblical-commentary", "Jerome.")
        self.write(
            "src/sources/works/jerome/in-matthaeum/editions/pl/segments/cols.toml",
            f"""
            schema = 2
            record_type = "segment"
            id = "segment.jerome.in-matthaeum.pl.cols"
            edition_id = "edition.jerome.in-matthaeum.pl"
            artifact_id = "artifact.aquinas.tomus-3.venice-1745.raw-ocr"
            """,
        )
        self.write(
            "src/sources/works/jerome/in-matthaeum/editions/pl/edition.toml",
            f"""
            schema = 1
            record_type = "edition"
            id = "edition.jerome.in-matthaeum.pl"
            work_id = "{other}"
            title = "pl"
            language = "la"
            """,
        )
        errors = _containment.validate(self.root)
        self.assertTrue(
            any(f"shows {TOMUS} holds {other}" in e for e in errors), errors
        )

    def test_a_constituent_must_carry_the_indexs_own_title(self) -> None:
        """An alias title would never join, so the holding would go unreported."""
        self.write_inventory(extra="""
            [[containers.constituents]]
            author = "Thomas Aquinas"
            title = "Super Matthaeum"
            whole = true
            basis = "Description."
        """)
        errors = _containment.validate(self.root)
        self.assertTrue(
            any("calls that work 'Super Evangelium S. Matthaei lectura'" in e for e in errors),
            errors,
        )


class RepositoryInventoryTests(unittest.TestCase):
    """The tracked inventory itself: valid, and answering the run's misses."""

    def test_the_tracked_inventory_validates(self) -> None:
        self.assertEqual(_containment.validate(ROOT), [])

    def test_the_venice_tomus_answers_for_super_matthaeum(self) -> None:
        found = _containment.Holdings(ROOT)
        matthew = {"book": "Matthew", "ranges": [{"begin": {"chapter": 9, "verse": 1},
                                                  "end": {"chapter": 9, "verse": 8}}]}
        result = found.for_work(
            "Thomas Aquinas", "Super Evangelium S. Matthaei lectura", None,
            found.books.passage_spans(matthew),
        )
        self.assertIn(
            "work.thomas-aquinas.opera-editio-altera-veneta-tomus-3",
            [row["container_id"] for row in result["containers"]],
        )
        self.assertNotEqual(result["status"], _containment.NONE)


if __name__ == "__main__":
    unittest.main()
