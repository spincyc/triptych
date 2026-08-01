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

import _canon  # noqa: E402
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
            languages = ["lat"]
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
            translators = ["Marcus Dods"]
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
            translators = ["Blomfield Jackson"]
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
        self.write(
            "src/sources/works/basil/hexaemeron/work.toml",
            """
            schema = 1
            record_type = "work"
            id = "work.basil.hexaemeron"
            title = "Homiliae in Hexaemeron"
            responsible = "Basil the Great"
            work_type = "patristic-homily-series"
            languages = ["grc"]
            """,
        )
        self.write_edges(
            passage_id="passage.npnf.volume-8.new-york-1895.basil-1.2",
            work_id="work.basil.hexaemeron",
            work_alias={"author": "Basil the Great", "work": "Homiliae in Hexaemeron"},
        )
        joined = " ".join(self.errors())
        # Undeclared, the container mismatch is an error naming the fix.
        self.assertIn("declare constituent_of", joined)

        # Declared, the fragment renders and the author still comes from the
        # work record rather than from the anthology's editors.
        self.write_edges(
            passage_id="passage.npnf.volume-8.new-york-1895.basil-1.2",
            work_id="work.basil.hexaemeron",
            work_alias={"author": "Basil the Great", "work": "Homiliae in Hexaemeron"},
            constituent_of="edition.npnf.volume-8.new-york-1895",
        )
        self.assertEqual(self.errors(), [])
        rows = _catena.fragments_for_book(self.root, "Gen")
        self.assertEqual(rows[0]["author"], "Basil the Great")
        self.assertEqual(
            rows[0]["container"], "edition.npnf.volume-8.new-york-1895"
        )

    def test_a_constituent_declaration_must_name_a_real_container(self) -> None:
        """The declaration may not be used to wave through an ordinary mismatch."""
        self.write(
            "src/sources/works/other/thing/work.toml",
            """
            schema = 1
            record_type = "work"
            id = "work.other.thing"
            title = "Something Else"
            responsible = "Someone"
            work_type = "patristic-treatise"
            """,
        )
        self.write_edges(work_id="work.other.thing", constituent_of=
                         "edition.augustine.de-civitate-dei.dods-1871")
        joined = " ".join(self.errors())
        self.assertIn("and not a container", joined)


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


class VoiceTests(CatenaFixture):
    """Whose words a fragment carries, and the two signals that must agree.

    The reader chooses between the author's own language and a translation of
    it, so every fragment has to answer which it is. The answer is derived from
    the work's language history against the edition's, and cross-checked
    against whether the edition names a translator, because each signal alone
    reads perfectly when it is wrong: an edition in Latin is Ambrose writing or
    Eustathius translating, and nothing in the word "Latin" tells them apart.
    """

    def edition(self, language: str, extra: str = "") -> None:
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/edition.toml",
            f"""
            schema = 1
            record_type = "edition"
            id = "edition.augustine.de-civitate-dei.dods-1871"
            work_id = "work.augustine.de-civitate-dei"
            title = "The City of God"
            language = "{language}"
            publication = "Edinburgh, 1871"
            {extra}
            """,
        )

    def work(self, languages: str) -> None:
        self.write(
            "src/sources/works/augustine/de-civitate-dei/work.toml",
            f"""
            schema = 1
            record_type = "work"
            id = "work.augustine.de-civitate-dei"
            title = "De civitate Dei"
            responsible = "Augustine of Hippo"
            work_type = "patristic-treatise"
            languages = {languages}
            """,
        )

    def test_the_english_of_a_latin_father_is_a_translation(self) -> None:
        rows = _catena.fragments_for_book(self.root, "Gen")
        self.assertEqual([row["voice"] for row in rows], [_catena.TRANSLATION])

    def test_the_latin_of_a_latin_father_is_his_own(self) -> None:
        self.edition("la")
        rows = _catena.fragments_for_book(self.root, "Gen")
        self.assertEqual([row["voice"] for row in rows], [_catena.ORIGINAL])
        self.assertEqual(self.errors(), [])

    def test_the_two_iso_code_spaces_are_folded_before_they_are_compared(self) -> None:
        """`lat` and `la` are one language, and comparing them raw is silent.

        The work records name a language in ISO 639-2/B and the edition records
        in 639-1. Left unfolded, Migne's Latin of a Latin father reads as a
        TRANSLATION of him — a well-formed answer, arrived at correctly, and
        wrong.
        """
        self.work('["lat"]')
        self.edition("la")
        self.assertEqual(
            _catena.voice_of({"languages": ["lat"]}, {"language": "la"}),
            _catena.ORIGINAL,
        )
        self.assertEqual(self.errors(), [])

    def test_a_language_the_table_does_not_know_is_an_error_not_a_guess(self) -> None:
        self.work('["tlh"]')
        joined = " ".join(self.errors())
        self.assertIn("LANGUAGE_EQUIVALENTS", joined)
        # And never silently a translation, which is what an unfoldable code
        # would become if it were simply dropped from the comparison.
        self.assertEqual(_catena.voice_of({"languages": ["tlh"]}, {"language": "la"}), "")

    def test_a_work_that_says_nothing_about_its_language_is_refused(self) -> None:
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
        self.assertIn("states no `languages`", " ".join(self.errors()))

    def test_a_translation_that_names_no_translator_is_refused(self) -> None:
        """The signal that would let a translation pass as the author's words."""
        self.edition("en")
        self.assertIn("names no translator", " ".join(self.errors()))

    def test_an_original_that_names_translators_is_refused(self) -> None:
        """And the same disagreement from the other side."""
        self.edition("la", 'translators = ["Marcus Dods"]')
        joined = " ".join(self.errors())
        self.assertIn("names Marcus Dods as translators", joined)

    def test_the_page_s_own_model_filters_on_the_voice(self) -> None:
        """One derivation again: the browser's file decides, not this test."""
        self.edition("la")
        # The emit runs the page's own model, so the fixture carries the real
        # one: a copy here would be the second derivation the arrangement
        # exists to stop.
        model = self.root / _catena.MODEL_RELATIVE
        model.parent.mkdir(parents=True, exist_ok=True)
        model.write_text(
            (ROOT / _catena.MODEL_RELATIVE).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        _catena.structure(self.root, self.root / "out")
        chapter = self.root / "out" / "structure" / "catena" / "01-gen" / "1.json"
        script = f"""
        const M = require({str(ROOT / 'src/web/browser/catena/catena-model.js')!r});
        const file = require({str(chapter)!r});
        const all = M.chapterFragments(file);
        console.log(JSON.stringify({{
          voices: M.chapterVoices(file).map((one) => one.key),
          original: all.filter((one) => M.matchesVoice(one, 'original')).length,
          english: all.filter((one) => M.matchesVoice(one, 'translation:en')).length,
          everything: all.filter((one) => M.matchesVoice(one, '')).length
        }}));
        """
        result = subprocess.run(
            ["node", "-e", textwrap.dedent(script)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            json.loads(result.stdout),
            {"voices": ["original"], "original": 1, "english": 0, "everything": 1},
        )


class TitleCoverageTests(unittest.TestCase):
    """Rule 8, measured against the repository's own alias table."""

    def test_the_group_whose_title_still_names_less_than_it_reaches(self) -> None:
        """One residual failure, and it is not one guidance/catena.md records.

        The design named two: Aquinas's and Theophylact's Pauline commentaries,
        each grouped correctly and each named after Romans. Both were fixed
        while this check was being written — the harvest was re-promoted and
        their canonical titles now name the whole Pauline corpus. Theodoret's
        remains: his commentary covers Jeremiah, Baruch and Lamentations and is
        filed under *Commentarius in Ieremiam*, so a catena would render his
        comment on Baruch under a title naming Jeremiah.
        """
        failures = {(author, work) for author, work, _ in _catena.failing_groups(ROOT)}
        self.assertIn(("Theodoret of Cyrus", "Commentarius in Ieremiam"), failures)
        self.assertEqual(len(failures), 1)

    def test_the_pauline_groups_the_design_named_now_pass(self) -> None:
        forms = _catena.book_forms(ROOT)
        import yaml

        groups = yaml.safe_load(
            (ROOT / _catena.ALIASES_RELATIVE).read_text(encoding="utf-8")
        )["groups"]
        for group in groups:
            if group["author"] in ("Thomas Aquinas", "Theophylact of Ohrid"):
                if "Pauli" in group["work"]:
                    self.assertEqual(_catena.title_covers_group(group, forms), "")

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
                "numbering": "vulgate",
                "extent": {
                    "token": "Gen",
                    "first_chapter": 1,
                    "first_verse": 3,
                    "last_chapter": 1,
                    "last_verse": 5,
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


class PathTests(CatenaFixture):
    """The path convention: canon order, lowercase, ordinal last, padded.

    `guidance/web-data.md` states it as one sentence — anything with an inherent
    order sorts in that order in a directory listing — and every part of it is
    derived from the tracked canon rather than typed. These test the derivation,
    because a hand-listed table beside a derived one is the restatement this
    repository has already been bitten by.
    """

    def test_a_book_is_numbered_by_its_place_in_the_canon(self) -> None:
        # The fixture carries chapters for Genesis alone, so the canon it can
        # enumerate is one book long — which is the point: the number is the
        # position in what was actually enumerated, not a constant beside it.
        self.assertEqual(_canon.path_forms(self.root), {"Gen": "01-gen"})
        # And against the repository's own canon, where the positions are real.
        forms = _canon.path_forms(ROOT)
        self.assertEqual(forms["Gen"], "01-gen")
        self.assertEqual(forms["Ps"], "21-ps")
        self.assertEqual(forms["1Cor"], "53-cor-1")
        self.assertEqual(forms["Apoc"], "73-apoc")

    def test_a_numbered_book_puts_its_ordinal_last(self) -> None:
        self.assertEqual(_canon._name_form("1Cor"), "cor-1")
        self.assertEqual(_canon._name_form("4Kings"), "kings-4")
        self.assertEqual(_canon._name_form("Gen"), "gen")

    def test_the_chapter_width_comes_from_the_longest_book(self) -> None:
        # The fixture's Genesis runs to three chapters, so one digit suffices;
        # the real canon reaches 150 and takes three. The width is derived
        # either way and never asserted.
        self.assertEqual(_canon.chapter_width(self.root), 1)
        self.assertEqual(_canon.chapter_name(7, 3), "007.json")

    def test_no_path_component_is_capitalised_or_begins_with_a_digit(self) -> None:
        for token, form in _canon.path_forms(self.root).items():
            self.assertEqual(form, form.lower(), token)
            name = form.split("-", 1)[1]
            self.assertFalse(name[0].isdigit(), token)

    def test_the_canon_is_reached_through_the_project_module(self) -> None:
        """The catena is a consumer of the canon, never its owner."""
        self.assertEqual(_catena.canon(self.root), _canon.books(self.root))


class StructureTests(CatenaFixture):
    """What a reader actually fetches, and what is deliberately not in it."""

    def setUp(self) -> None:
        super().setUp()
        # The emit derives the chapter view by running the page's own model, so
        # the fixture carries the real one rather than a stand-in: a copy here
        # would be the second derivation the whole arrangement exists to stop.
        model = self.root / _catena.MODEL_RELATIVE
        model.parent.mkdir(parents=True, exist_ok=True)
        model.write_text(
            (ROOT / _catena.MODEL_RELATIVE).read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    def emit(self) -> Path:
        out = self.root / "out"
        _catena.structure(self.root, out)
        return out / "structure" / "catena"

    def test_the_chapter_spine_carries_no_prose(self) -> None:
        directory = self.emit()
        spine = json.loads(
            (directory / "01-gen" / "1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(spine["fragments"]), 1)
        fragment = spine["fragments"][0]
        for absent in ("text", "basis", "date_basis"):
            self.assertNotIn(absent, fragment)
        self.assertGreater(fragment["text_words"], 0)
        # What the fragment shares with its edition is written once per file and
        # referenced, and the path to its words is composed from the file's one
        # statement of where words live.
        shared = spine["sources"][fragment["source"]]
        self.assertNotIn("author", fragment)
        self.assertTrue(shared["author"])
        text_path = spine["text_prefix"] + fragment["id"] + ".json"
        payload = json.loads(
            (self.root / "out" / text_path).read_text(encoding="utf-8")
        )
        self.assertIn("light", payload["text"])
        self.assertIn("light", payload["basis"])

    def test_two_fragments_of_one_edition_share_one_source_entry(self) -> None:
        """The spine states an edition once, however many fragments stand on it.

        The restatement it replaces was not small: on Genesis 1 the author, the
        work, the printing and the rights were written out 107 times, and every
        copy was a chance for two of them to disagree about one edition.
        """
        rows = [
            {"id": "a", "author": "X", "work": "W", "date": 400, "language": "la",
             "edition": "E", "edition_published": "P", "translators": [],
             "container": "", "rights": "public-domain", "locator": "1"},
            {"id": "b", "author": "X", "work": "W", "date": 400, "language": "la",
             "edition": "E", "edition_published": "P", "translators": [],
             "container": "", "rights": "public-domain", "locator": "2"},
            {"id": "c", "author": "X", "work": "W", "date": 415, "language": "la",
             "edition": "E", "edition_published": "P", "translators": [],
             "container": "", "rights": "public-domain", "locator": "3"},
        ]
        shared, slim = _catena._fold_shared(rows)
        self.assertEqual(len(shared), 2)
        self.assertEqual(slim[0]["source"], slim[1]["source"])
        self.assertNotEqual(slim[0]["source"], slim[2]["source"])
        self.assertEqual(shared[slim[2]["source"]]["date"], 415)

    def test_a_chapter_with_nothing_gets_no_file(self) -> None:
        directory = self.emit()
        # The fixture's fragment and its one lead both stand on Genesis 1.
        self.assertTrue((directory / "01-gen" / "1.json").is_file())
        self.assertFalse((directory / "01-gen" / "2.json").exists())
        index = json.loads((directory / "index.json").read_text(encoding="utf-8"))
        held = {book["token"]: book for book in index["held"]}
        self.assertEqual(held["Gen"]["present"], [1])
        self.assertEqual(held["Gen"]["path"], "structure/catena/01-gen/")

    def test_the_lead_stands_on_its_own_chapter_and_not_in_the_book(self) -> None:
        directory = self.emit()
        spine = json.loads(
            (directory / "01-gen" / "1.json").read_text(encoding="utf-8")
        )
        self.assertTrue(spine["leads"])
        self.assertNotIn("Gen.json", [path.name for path in directory.iterdir()])

    def test_a_file_left_behind_by_an_earlier_emit_is_removed(self) -> None:
        """An orphan is the failure that looks like success.

        The page would never ask for it and nothing would ever notice it was
        wrong, so the emit owns the directory and deletes what it did not write.
        """
        directory = self.emit()
        stale = directory / "01-gen" / "9.json"
        stale.write_text("{}", encoding="utf-8")
        orphan = directory / "text" / "passage.gone.json"
        orphan.write_text("{}", encoding="utf-8")
        self.emit()
        self.assertFalse(stale.exists())
        self.assertFalse(orphan.exists())

    def test_the_chapter_view_is_derived_by_the_page_s_own_model(self) -> None:
        """One derivation, and it is `catena-model.js`.

        Writing `first <= n <= last` in the generator as well would be the
        dangerous kind of second copy: the emitted chapter files would be
        derived by one rule while the page's own footer promised another.
        """
        model = self.root / _catena.MODEL_RELATIVE
        model.write_text("module.exports = {};", encoding="utf-8")
        with self.assertRaises(_catena.CatenaError):
            self.emit()


if __name__ == "__main__":
    unittest.main()
