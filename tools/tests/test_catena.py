"""The catena's scripture edge: what it refuses, and that it refuses honestly.

The refusals are the point. A catena that renders a lead as a text, or a work
under a title naming a tenth of it, or a psalm verse against whichever edition
happens to be open, is worse than an empty page, so each of those is tested
here against a fixture built for it rather than against whatever the repository
happens to hold today.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _catena  # noqa: E402
import _projection  # noqa: E402

BOOK_INDEX = (
    "ordinal\ttoken\tfile\ttestament\tdouay_title\tmodern_name\t"
    "missal_latin_abbreviation\talternate_names\n"
    "1\tGen\t01-genesis.tsv\told\tThe Book of Genesis\tGenesis\tGen.\tGen.;Gn\n"
    "2\tRom\t52-romans.tsv\tnew\tThe Epistle to the Romans\tRomans\tRom.\tRom.\n"
    "3\tPs\t21-psalms.tsv\told\tThe Book of Psalms\tPsalms\tPs.\tPs.\n"
)


class CatenaFixture(unittest.TestCase):
    """A repository just large enough to answer one question at a time."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.write(
            "src/sources/works/catholic-church/vulgata-clementina/editions/"
            "ebible-latvuc/artifacts/book-index-fcad78c2/book-index.tsv",
            BOOK_INDEX,
        )
        for chapter, verses in ((1, 31), (2, 25), (3, 24)):
            self.write(
                f"src/sources/bibles/clementine-vulgate/chapters/Gen/{chapter}.json",
                json.dumps(
                    {
                        "book": "Gen",
                        "chapter": chapter,
                        "verses": {str(n): "text" for n in range(1, verses + 1)},
                    }
                ),
            )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/work.toml",
            """
            schema = 1
            record_type = "work"
            id = "work.augustine.de-civitate-dei"
            title = "De civitate Dei"
            responsible = "Augustine of Hippo"
            work_type = "patristic-treatise"
            """,
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/edition.toml",
            """
            schema = 1
            record_type = "edition"
            id = "edition.augustine.de-civitate-dei.dods-1871"
            work_id = "work.augustine.de-civitate-dei"
            title = "The City of God"
            language = "en"
            publication = "Edinburgh, 1871"
            """,
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
            "artifacts/body/artifact.toml",
            """
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.dods-1871.body"
            edition_id = "edition.augustine.de-civitate-dei.dods-1871"
            artifact_type = "normalized-text"
            media_type = "text/plain; charset=utf-8"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Published in 1871."
            """,
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
            "passages/11.7.toml",
            """
            schema = 1
            record_type = "passage"
            id = "passage.augustine.de-civitate-dei.dods-1871.11.7"
            edition_id = "edition.augustine.de-civitate-dei.dods-1871"
            artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"
            locus = "11.7"
            states = ["cataloged", "acquired", "inspected"]
            context = "The nature of the first days."
            text = "And first of all, indeed, light was made by the word of God."
            """,
        )
        self.write_aliases()
        self.write_index()
        self.write_edges()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
        return path

    def write_aliases(self, extra: str = "") -> None:
        self.write(
            "src/sources/commentary/work-aliases.yaml",
            f"""
            schema: triptych-commentary-work-aliases/v1
            groups:
            - author: Augustine of Hippo
              work: De civitate Dei
              titles:
              - de civitate dei
              - the city of god
            {extra}
            """,
        )

    def write_index(self) -> None:
        self.write(
            "src/sources/commentary/passage-commentary-index.yaml",
            """
            schema: triptych-commentary-work-index/v1
            passages:
            - passage: Genesis 1
              works:
              - author: Basil the Great
                title: Homiliae in Hexaemeron
                date: 379
                confidence: 1.0
            """,
        )

    def write_edges(self, **overrides: object) -> None:
        fragment = {
            "passage_id": "passage.augustine.de-civitate-dei.dods-1871.11.7",
            "work_id": "work.augustine.de-civitate-dei",
            "work_alias": {"author": "Augustine of Hippo", "work": "De civitate Dei"},
            "text_date": 417,
            "text_date_basis": "Books XI-XIV were issued about 417.",
            "numbering": "vulgate",
            "extent": {
                "token": "Gen",
                "first_chapter": 1,
                "first_verse": 3,
                "last_chapter": 1,
                "last_verse": 5,
            },
            "basis": "The excerpt expounds the making of light.",
        }
        fragment.update(overrides)
        import yaml

        self.write(
            "src/sources/commentary/fragment-loci.yaml",
            yaml.safe_dump(
                {
                    "schema": _catena.SCHEMA,
                    "updated": "2026-07-31",
                    "numbering": "vulgate",
                    "fragments": [fragment],
                },
                sort_keys=False,
            ),
        )

    def errors(self) -> list[str]:
        return _catena.validate(self.root)


class ExtentTests(CatenaFixture):
    def test_a_well_formed_edge_validates(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_an_extent_in_another_numbering_is_refused(self) -> None:
        self.write_edges(numbering="hebrew")
        self.assertIn("Rule 3", " ".join(self.errors()))

    def test_an_extent_past_the_canonical_last_verse_is_refused(self) -> None:
        self.write_edges(
            extent={
                "token": "Gen",
                "first_chapter": 1,
                "first_verse": 3,
                "last_chapter": 1,
                "last_verse": 99,
            }
        )
        self.assertIn("past the canonical last verse 31", " ".join(self.errors()))

    def test_an_unknown_book_is_refused(self) -> None:
        self.write_edges(
            extent={
                "token": "Enoch",
                "first_chapter": 1,
                "first_verse": 1,
                "last_chapter": 1,
                "last_verse": 1,
            }
        )
        self.assertIn("which the canonical edition does not carry", " ".join(self.errors()))

    def test_an_extent_that_ends_before_it_begins_is_refused(self) -> None:
        self.write_edges(
            extent={
                "token": "Gen",
                "first_chapter": 2,
                "first_verse": 1,
                "last_chapter": 1,
                "last_verse": 1,
            }
        )
        self.assertIn("ends before it begins", " ".join(self.errors()))


class IdentityTests(CatenaFixture):
    def test_an_unresolvable_work_alias_is_refused(self) -> None:
        self.write_edges(
            work_alias={"author": "Augustine of Hippo", "work": "Confessiones"}
        )
        self.assertIn("resolves to no group", " ".join(self.errors()))

    def test_the_two_identity_spaces_must_agree_on_the_author(self) -> None:
        self.write_aliases(
            extra="""
            - author: Someone Else
              work: De civitate Dei
              titles:
              - de civitate dei
            """
        )
        self.write_edges(
            work_alias={"author": "Someone Else", "work": "De civitate Dei"}
        )
        self.assertIn("the two identity spaces disagree", " ".join(self.errors()))

    def test_a_missing_passage_record_is_refused(self) -> None:
        self.write_edges(passage_id="passage.augustine.de-civitate-dei.dods-1871.99.9")
        self.assertIn("is not a passage record", " ".join(self.errors()))

    def test_a_container_edition_cannot_supply_the_label(self) -> None:
        """The live NPNF defect, reduced: a passage whose edition is an anthology.

        Derived from the container, Basil's Hexaemeron would be labelled with the
        NPNF volume's `responsible`, which is Philip Schaff. The check exists so
        that a false author is a build failure rather than a rendered claim.
        """
        self.write(
            "src/sources/works/npnf/volume-8/work.toml",
            """
            schema = 1
            record_type = "work"
            id = "work.npnf.volume-8"
            title = "NPNF Second Series, Volume VIII"
            responsible = "Philip Schaff and Henry Wace"
            work_type = "patristic-translation-anthology"
            """,
        )
        self.write(
            "src/sources/works/npnf/volume-8/editions/new-york-1895/edition.toml",
            """
            schema = 1
            record_type = "edition"
            id = "edition.npnf.volume-8.new-york-1895"
            work_id = "work.npnf.volume-8"
            title = "NPNF 2-8"
            language = "en"
            publication = "New York, 1895"
            """,
        )
        self.write(
            "src/sources/works/npnf/volume-8/editions/new-york-1895/"
            "artifacts/text/artifact.toml",
            """
            schema = 1
            record_type = "artifact"
            id = "artifact.npnf.volume-8.new-york-1895.text"
            edition_id = "edition.npnf.volume-8.new-york-1895"
            artifact_type = "web-text"
            media_type = "text/plain; charset=utf-8"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Published in 1895."
            """,
        )
        self.write(
            "src/sources/works/npnf/volume-8/editions/new-york-1895/"
            "passages/basil-1.2.toml",
            """
            schema = 1
            record_type = "passage"
            id = "passage.npnf.volume-8.new-york-1895.basil-1.2"
            edition_id = "edition.npnf.volume-8.new-york-1895"
            artifact_id = "artifact.npnf.volume-8.new-york-1895.text"
            locus = "Basil of Caesarea, Homiliae in Hexaemeron I.2"
            states = ["cataloged", "acquired", "inspected"]
            context = "Basil on In the beginning."
            text = "In the beginning God made heaven and earth."
            """,
        )
        self.write_aliases(
            extra="""
            - author: Basil the Great
              work: Homiliae in Hexaemeron
              titles:
              - homiliae in hexaemeron
              - hexaemeron
            """
        )
        self.write_edges(
            passage_id="passage.npnf.volume-8.new-york-1895.basil-1.2",
            work_id="work.npnf.volume-8",
            work_alias={"author": "Basil the Great", "work": "Homiliae in Hexaemeron"},
        )
        joined = " ".join(self.errors())
        self.assertIn("the two identity spaces disagree", joined)


class RightsTests(CatenaFixture):
    def test_an_unpublishable_artifact_never_reaches_the_page(self) -> None:
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
            "artifacts/body/artifact.toml",
            """
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.dods-1871.body"
            edition_id = "edition.augustine.de-civitate-dei.dods-1871"
            artifact_type = "normalized-text"
            media_type = "text/plain; charset=utf-8"
            storage = "restricted"
            rights_status = "all-rights-reserved"
            rights_basis = "A modern critical edition."
            """,
        )
        self.assertIn("which may not be published", " ".join(self.errors()))

    def test_a_fragment_reaching_no_artifact_carries_no_licence(self) -> None:
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
            "passages/11.7.toml",
            """
            schema = 1
            record_type = "passage"
            id = "passage.augustine.de-civitate-dei.dods-1871.11.7"
            edition_id = "edition.augustine.de-civitate-dei.dods-1871"
            locus = "11.7"
            states = ["cataloged"]
            context = "The nature of the first days."
            """,
        )
        self.assertIn("carries no licence", " ".join(self.errors()))

    def test_a_fragment_without_a_locator_is_refused(self) -> None:
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
            "passages/11.7.toml",
            """
            schema = 1
            record_type = "passage"
            id = "passage.augustine.de-civitate-dei.dods-1871.11.7"
            edition_id = "edition.augustine.de-civitate-dei.dods-1871"
            artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"
            locus = ""
            states = ["cataloged"]
            context = "The nature of the first days."
            """,
        )
        self.assertIn("has no locator", " ".join(self.errors()))


class TitleCoverageTests(unittest.TestCase):
    """Rule 8, measured against the repository's own alias table."""

    def test_the_four_groups_whose_title_names_less_than_they_reach(self) -> None:
        failures = {(author, work) for author, work, _ in _catena.failing_groups(ROOT)}
        self.assertIn(("Thomas Aquinas", "Super Epistolam ad Romanos lectura"), failures)
        self.assertIn(
            ("Theophylact of Ohrid", "Expositio in epistulam ad Romanos"), failures
        )
        # Two more than guidance/catena.md records, both real.
        self.assertIn(("Albert the Great", "Commentarii in Amos prophetam"), failures)
        self.assertIn(("Theodoret of Cyrus", "Commentarius in Ieremiam"), failures)
        self.assertEqual(len(failures), 4)

    def test_every_declared_book_form_names_a_real_token(self) -> None:
        self.assertEqual(_catena.undeclared_form_tokens(ROOT), [])

    def test_a_title_naming_no_book_claims_none(self) -> None:
        forms = _catena.book_forms(ROOT)
        group = {
            "work": "De civitate Dei",
            "titles": ["de civitate dei", "commentary on genesis"],
        }
        self.assertEqual(_catena.title_covers_group(group, forms), "")

    def test_a_personal_name_qualifying_a_title_is_not_a_second_book(self) -> None:
        forms = _catena.book_forms(ROOT)
        self.assertEqual(
            _catena._books_named("in apocalypsim iohannis libri xii", forms), {"Apoc"}
        )
        self.assertEqual(
            _catena._books_named("expositio in lamentationes hieremiae", forms), {"Lam"}
        )
        self.assertEqual(
            _catena._books_named("commentaria in evangelium sancti iohannis", forms),
            {"John"},
        )


class ProjectionRefusalTests(unittest.TestCase):
    """Rule 4 — where the projection refuses, the page must refuse too.

    Genesis reaches no refusal, so the path is exercised against the psalter,
    which is where the refusals actually live. Sixteen psalms are recorded
    `displaced`: their verse numbers correspond and their body boundaries do
    not, and the projection deliberately declines to say where the boundary
    moves. A page that fell back to the same verse number would be giving
    precisely the wrong answer dressed as the right one.
    """

    def test_the_projection_records_displaced_psalms_and_resolves_none_of_them(self) -> None:
        rows = _projection.displaced_psalms()
        self.assertEqual(len(rows), 16)
        for row in rows:
            self.assertEqual(row.kind, "displaced")
            self.assertEqual(row.resolves_to, "")

    def test_a_displaced_psalm_is_a_refusal_the_page_can_render(self) -> None:
        rows = {row.cited_locus: row for row in _projection.displaced_psalms()}
        some = next(iter(sorted(rows)))
        self.assertTrue(some.startswith("Ps."))
        self.assertIn("cannot say where it moves to", rows[some].note)

    def test_the_canonical_system_is_the_one_the_edge_declares(self) -> None:
        data = _catena.load_edges(ROOT)
        self.assertEqual(data["numbering"], _projection.CANONICAL)


class ChapterDerivationTests(unittest.TestCase):
    """The derivation lives in the browser's model; this replays it there."""

    def test_the_solved_chapter_cases_replay_under_node(self) -> None:
        errors, skipped = _catena.replay_solved_chapters(ROOT)
        self.assertEqual(errors, [])
        if skipped:
            self.skipTest(skipped)

    def test_a_fragment_spanning_chapters_stands_under_both(self) -> None:
        model = ROOT / _catena.MODEL_RELATIVE
        harness = (
            "const m={exports:{}};"
            "new Function('module','exports',require('fs').readFileSync(process.argv[1],'utf8'))"
            "(m,m.exports);"
            "const f=[{id:'a',extent:{token:'Gen',first_chapter:1,first_verse:1,"
            "last_chapter:2,last_verse:2}}];"
            "process.stdout.write(JSON.stringify(["
            "m.exports.fragmentsOnChapter(f,1).length,"
            "m.exports.fragmentsOnChapter(f,2).length,"
            "m.exports.fragmentsOnChapter(f,3).length,"
            "m.exports.formatExtent(f[0].extent,'Genesis')]));"
        )
        try:
            result = subprocess.run(
                ["node", "-e", harness, str(model)],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            self.skipTest("node is not installed")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [1, 1, 0, "Genesis 1:1-2:2"])


class BlockedTests(CatenaFixture):
    def test_a_blocked_fragment_may_not_also_be_rendered(self) -> None:
        import yaml

        path = self.root / "src/sources/commentary/fragment-loci.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["blocked"] = [
            {
                "passage_ids": ["passage.augustine.de-civitate-dei.dods-1871.11.7"],
                "work_alias": {
                    "author": "Augustine of Hippo",
                    "work": "De civitate Dei",
                },
                "reason": "A reason.",
                "fix": "A fix.",
            }
        ]
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        self.assertIn("blocked or held, never both", " ".join(self.errors()))


class LeadTests(CatenaFixture):
    def test_the_confidence_never_leaves_the_generator(self) -> None:
        """Rule 2, enforced where a page cannot undo it.

        Once a work's fragments are held, its L1 confidence is irrelevant for
        presence. Dropping the column at generation is the same guard
        `bibles.json` uses against a licensed edition: a page cannot show what
        it was never sent.
        """
        leads = _catena.leads_for_book(self.root, "Gen", "Genesis")
        self.assertEqual(list(leads), ["1"])
        for work in leads["1"]:
            self.assertNotIn("confidence", work)
        self.assertEqual(leads["1"][0]["author"], "Basil the Great")


if __name__ == "__main__":
    unittest.main()
