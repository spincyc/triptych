"""The catena's scripture edge: what it refuses, and that it refuses honestly.

The refusals are the point. A catena that renders a lead as a text, or a work
under a title naming a tenth of it, or a psalm verse against whichever edition
happens to be open, is worse than an empty page, so each of those is tested
here against a fixture built for it rather than against whatever the repository
happens to hold today.
"""
from __future__ import annotations

import copy
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
        # Catholic eligibility is explicit fixture evidence, not a production
        # fallback when a miniature repository lacks its standing registry.
        import tomllib
        import _standing
        registry = tomllib.loads((ROOT / _standing.REGISTRY_RELATIVE).read_text())
        standing = [f'schema = {json.dumps(registry["schema"])}',
                    f'record_type = {json.dumps(registry["record_type"])}',
                    f'audited_on = {json.dumps(registry["audited_on"])}']
        for person in registry["persons"]:
            if person["id"] not in {"augustine", "basil-of-caesarea"}:
                continue
            standing.append("[[persons]]")
            for key in ("id", "name", "names", "died", "standing", "standing_basis", "basis_sources", "confession"):
                standing.append(f"{key} = {json.dumps(person[key])}")
        self.write(_standing.REGISTRY_RELATIVE.as_posix(), "\n".join(standing))
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


class EnglishVersionTests(unittest.TestCase):
    def setUp(self):
        self.sources = _catena.Sources({}, {"latin": {"language": "la"}, "english": {"language": "en"}},
                                      {}, {}, {"source": {"edition_id": "latin"}, "target": {"edition_id": "english"}})
        extent = dict(token="Gen", first_chapter=1, first_verse=2, last_chapter=1, last_verse=5)
        self.source = {"passage_id": "source", "work_id": "one", "extent": extent,
                       "english_versions": [{"passage_id": "target", "coverage": "excerpt", "basis": "Section II."}]}
        self.target = {"passage_id": "target", "work_id": "one", "extent": extent.copy()}

    def errors(self):
        return _catena._english_version_errors(self.sources, [self.source, self.target])

    def test_checked_excerpt(self):
        self.assertEqual(self.errors(), [])

    def test_mismatched_work_language_and_extent(self):
        for changes in [{"work_id": "two"}, {"passage_id": "missing"},
                        {"extent": {**self.target["extent"], "first_verse": 6, "last_verse": 7}}]:
            with self.subTest(changes=changes):
                self.assertTrue(_catena._english_version_errors(self.sources, [self.source, {**self.target, **changes}]))
        self.sources.editions["english"]["language"] = "la"
        self.assertTrue(self.errors())

    def test_partial_locus_cannot_be_advertised_as_a_whole_english_version(self):
        self.target["extent"]["last_verse"] = 2
        self.assertEqual(self.errors(), [])
        self.source["english_versions"][0]["coverage"] = "whole"
        self.assertIn("must cover the full source locus", " ".join(self.errors()))

    def test_incomplete_or_repeated_attestation(self):
        link, = self.source["english_versions"]
        for versions in [[], [link, link], [{**link, "basis": ""}], [{**link, "coverage": "unknown"}]]:
            with self.subTest(versions=versions):
                self.source["english_versions"] = versions
                self.assertTrue(self.errors())


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
    def test_unreviewed_author_fails_admission_and_cannot_emit_text(self) -> None:
        path = self.root / "src/sources/works/augustine/de-civitate-dei/work.toml"
        path.write_text(path.read_text().replace("Augustine of Hippo", "Unreviewed writer"))
        self.assertTrue(any("commentator scope is unreviewed" in error for error in self.errors()))
        self.assertEqual(_catena.fragments_for_book(self.root, "Gen"), [])

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

    def test_a_fragment_whose_passage_carries_no_text_is_refused(self) -> None:
        """Rule 1: a fragment the page cannot show the words of does not render.

        Everything else about it is sound — a locator, an edition, a
        public-domain artifact, a date and an extent — which is exactly why
        nothing else refused it: Sermo 50 reached Matthew 9 as a fragment that
        opened onto nothing.
        """
        self.assertEqual(self.errors(), [])
        for empty in ('', 'text = ""', 'text = "   "'):
            with self.subTest(text=empty or "(absent)"):
                self.write(
                    "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
                    "passages/11.7.toml",
                    f"""
                    schema = 1
                    record_type = "passage"
                    id = "passage.augustine.de-civitate-dei.dods-1871.11.7"
                    edition_id = "edition.augustine.de-civitate-dei.dods-1871"
                    artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"
                    locus = "11.7"
                    states = ["cataloged", "acquired", "inspected"]
                    context = "The nature of the first days."
                    {empty}
                    """,
                )
                errors = self.errors()
                self.assertEqual(
                    [one for one in errors if "has no text" in one],
                    errors,
                    "the missing text is the only fault in this fixture",
                )
                self.assertEqual(len(errors), 1)
                self.assertIn("passage.augustine.de-civitate-dei.dods-1871.11.7", errors[0])


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
        if language != "en":
            # Moving the fixture off English makes the work one the absence
            # record owes an answer about; these tests are about the voice and
            # not about that, so the answer is supplied.
            self.write(
                "src/sources/commentary/translation-absences.yaml",
                f"""
                schema: {_catena.ABSENCES_SCHEMA}
                updated: "2026-08-01"
                absences:
                - work_id: work.augustine.de-civitate-dei
                  language: en
                  finding: in-copyright
                  checked_on: "2026-08-01"
                  reason: "Taylor's is of 1982."
                  aliases_searched: [De civitate Dei]
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


class AbsenceTests(CatenaFixture):
    """That a language a work does not reach is recorded, and stays true.

    The reason this is checked rather than trusted is the pressure it relieves.
    A reader without Latin who is shown two fragments of ninety-nine and told
    nothing reads the page as broken, and the fix that suggests itself is for
    this project to supply the English — which is the one thing it must never
    do. So the absence is data, and the data has to be right.
    """

    def absences(self, body: str) -> None:
        self.write(
            "src/sources/commentary/translation-absences.yaml",
            f"""
            schema: {_catena.ABSENCES_SCHEMA}
            updated: "2026-08-01"
            absences:
            {body}
            """,
        )

    def latin_only(self) -> None:
        """Move the fixture's one fragment onto a Latin edition of a Latin work."""
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/edition.toml",
            """
            schema = 1
            record_type = "edition"
            id = "edition.augustine.de-civitate-dei.dods-1871"
            work_id = "work.augustine.de-civitate-dei"
            title = "De civitate Dei, Migne"
            language = "la"
            publication = "Paris, 1841"
            """,
        )

    def test_a_work_held_in_no_english_needs_a_row_saying_why(self) -> None:
        self.latin_only()
        self.assertIn("no row here says why", " ".join(self.errors()))

    def test_the_row_discharges_it(self) -> None:
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: in-copyright
              checked_on: "2026-08-01"
              reason: "Taylor's is of 1982."
              aliases_searched: [De civitate Dei, The City of God]
            """
        )
        self.assertEqual(self.errors(), [])

    def test_a_partial_that_is_not_prose_is_refused_rather_than_coerced(self) -> None:
        """V7 §10. `str(row.get("partial") or "")` accepted a mapping, a list,
        a number and a flag alike and turned each into a sentence — and the
        page then printed whichever it got as "Partly public domain — …",
        which is a claim about somebody's rights composed out of a value
        nobody wrote. The contract is a string; anything else is a malformed
        record."""
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: partial-public-domain
              checked_on: "2026-08-01"
              reason: "Only the preface is out of copyright."
              aliases_searched: [De civitate Dei]
              partial:
                offer: "a mapping, not a sentence"
            """
        )
        self.assertIn("records a partial that is not text (dict)",
                      " ".join(self.errors()))

    def test_a_reason_that_is_not_prose_is_refused_rather_than_coerced(self) -> None:
        """The same coercion, on the field beside it."""
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: in-copyright
              checked_on: "2026-08-01"
              reason: [not, a, sentence]
              aliases_searched: [De civitate Dei]
            """
        )
        self.assertIn("records a reason that is not text (list)",
                      " ".join(self.errors()))

    def test_a_partial_detached_from_its_finding_is_refused(self) -> None:
        """V7 §10. `partial` REFINES a finding and never establishes one, so a
        partial standing beside a finding that licenses no offer is a record
        contradicting itself. The browser already declines to print it; the
        record is refused where it is written rather than silently dropped."""
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: in-copyright
              checked_on: "2026-08-01"
              reason: "A living author's rendering."
              aliases_searched: [De civitate Dei]
              partial: "an offer beside a closed finding"
            """
        )
        self.assertIn("only partial-public-domain licenses an offer",
                      " ".join(self.errors()))

    def test_a_partial_under_its_own_finding_is_emitted_as_written(self) -> None:
        """And the correction refuses nothing the corpus really holds."""
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: partial-public-domain
              checked_on: "2026-08-01"
              reason: "Only the preface is out of copyright."
              aliases_searched: [De civitate Dei]
              partial: "the   1893    preface"
            """
        )
        self.assertEqual(self.errors(), [])
        served = _catena.absent_by_work(self.root)
        self.assertEqual(
            served["work.augustine.de-civitate-dei"],
            [{"language": "en", "finding": "partial-public-domain",
              "reason": "Only the preface is out of copyright.",
              "partial": "the 1893 preface"}],
            "the offer is whitespace-collapsed and otherwise as written")

    def test_an_absence_the_library_contradicts_is_refused(self) -> None:
        """The way this file rots: the English lands and the note stays.

        Nothing else in the repository compares the two, so the page would go on
        telling a reader that a translation does not exist while serving it.
        """
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: none-published
              checked_on: "2026-08-01"
              reason: "Nobody ever put it into English."
              aliases_searched: [De civitate Dei]
            """
        )
        self.assertIn(
            "delete the row rather than publishing a text the page says does not exist",
            " ".join(self.errors()),
        )

    def test_a_row_naming_no_work_record_is_refused(self) -> None:
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: in-copyright
              checked_on: "2026-08-01"
              reason: "Taylor's is of 1982."
              aliases_searched: [De civitate Dei]
            - work_id: work.nobody.nothing
              language: en
              finding: none-published
              checked_on: "2026-08-01"
              reason: "There is no such work."
              aliases_searched: [nothing]
            """
        )
        self.assertIn("names no work record", " ".join(self.errors()))

    def test_a_finding_outside_the_closed_list_is_refused(self) -> None:
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: probably-not
              checked_on: "2026-08-01"
              reason: "A feeling."
              aliases_searched: [De civitate Dei]
            """
        )
        self.assertIn("is not one of", " ".join(self.errors()))

    def test_a_row_that_searched_no_alias_is_refused(self) -> None:
        """A work looked for under one name is a false absence waiting."""
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: none-published
              checked_on: "2026-08-01"
              reason: "Looked once."
            """
        )
        self.assertIn("names no aliases_searched", " ".join(self.errors()))

    def test_the_container_route_counts_as_holding_the_language(self) -> None:
        """Basil's English is a passage inside NPNF, not an edition of Basil.

        Read off editions alone, the library reports Basil held in no English
        while the page serves nine English fragments of him — and this file
        would then demand a note saying that English does not exist.
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
            languages = ["eng"]
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
            "passages/basil-1.toml",
            """
            schema = 1
            record_type = "passage"
            id = "passage.npnf.volume-8.new-york-1895.basil-1"
            edition_id = "edition.npnf.volume-8.new-york-1895"
            artifact_id = "artifact.npnf.volume-8.new-york-1895.text"
            locus = "1"
            states = ["cataloged", "acquired", "inspected"]
            context = "The first homily."
            text = "It is right that any one beginning to narrate the formation of the world."
            """,
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
            composed = "378"
            """,
        )
        self.write_aliases(
            extra="""
            - author: Basil the Great
              work: Homiliae in Hexaemeron
              titles:
              - homiliae in hexaemeron
            """
        )
        self.write_edges(
            passage_id="passage.npnf.volume-8.new-york-1895.basil-1",
            work_id="work.basil.hexaemeron",
            work_alias={"author": "Basil the Great", "work": "Homiliae in Hexaemeron"},
            constituent_of="edition.npnf.volume-8.new-york-1895",
            text_date=None,
            text_date_basis=None,
        )
        held = _catena.held_languages(self.root, _catena.load_sources(self.root))
        self.assertIn("en", held["work.basil.hexaemeron"])
        self.assertEqual(self.errors(), [])

    def test_the_page_is_given_the_reason_and_not_the_apparatus(self) -> None:
        self.latin_only()
        self.absences(
            """- work_id: work.augustine.de-civitate-dei
              language: en
              finding: in-copyright
              checked_on: "2026-08-01"
              reason: "Taylor's   is of\\n  1982."
              aliases_searched: [De civitate Dei]
              overturned_by: "A HathiTrust hit."
            """
        )
        served = _catena.absent_by_work(self.root)
        self.assertEqual(
            served,
            {
                "work.augustine.de-civitate-dei": [
                    {
                        "language": "en",
                        "finding": "in-copyright",
                        "reason": "Taylor's is of 1982.",
                    }
                ]
            },
        )


class TitleCoverageTests(unittest.TestCase):
    """Rule 8, measured against the repository's own alias table."""

    def test_the_group_whose_title_still_names_less_than_it_reaches(self) -> None:
        """Rule 8: every tracked alias group now covers its reached books, and
        the detector still rejects a canonical title naming only one book of a
        multi-book group (such as Theodoret's former *Commentarius in Ieremiam*).
        """
        self.assertEqual(_catena.failing_groups(ROOT), [])
        forms = _catena.book_forms(ROOT)
        narrow = {
            "author": "Theodoret of Cyrus",
            "work": "Commentarius in Ieremiam",
            "titles": [
                "commentarius in ieremiam",
                "commentary on baruch",
                "commentary on lamentations",
            ],
        }
        reason = _catena.title_covers_group(narrow, forms)
        self.assertIn("Jer", reason)
        self.assertIn("Bar", reason)
        self.assertIn("Lam", reason)

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


class ParallelTests(CatenaFixture):
    """Rule 15: one text held under two disputed names is hung once.

    Reduced from the case that raised it. PL 52 prints De paralytico curato as
    Chrysologus's Sermo 50 and PL 57 prints the same text as Maximus of Turin's
    Homilia CVIII. Here 11.7 stands for the first and 11.8 for the second. They
    share an edition because nothing in the rule turns on the edition, and a
    second work would bring its own alias, voice and absence rows into a fixture
    about something else. Each refusal is asserted as the ONLY fault in its
    fixture, so no test can pass on a neighbouring error.
    """

    HUNG = "passage.augustine.de-civitate-dei.dods-1871.11.7"
    OTHER = "passage.augustine.de-civitate-dei.dods-1871.11.8"
    THIRD = "passage.augustine.de-civitate-dei.dods-1871.11.9"
    UNKNOWN = "passage.nowhere.sermones.sermo-1"
    EXTENT = {
        "token": "Gen",
        "first_chapter": 1,
        "first_verse": 3,
        "last_chapter": 1,
        "last_verse": 5,
    }

    def setUp(self) -> None:
        super().setUp()
        for locus in ("11.8", "11.9"):
            self.write(
                "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
                f"passages/{locus}.toml",
                f"""
                schema = 1
                record_type = "passage"
                id = "passage.augustine.de-civitate-dei.dods-1871.{locus}"
                edition_id = "edition.augustine.de-civitate-dei.dods-1871"
                artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"
                locus = "{locus}"
                states = ["cataloged", "acquired", "inspected"]
                context = "The same words printed under another name."
                text = "And first of all, indeed, light was made by the word of God."
                """,
            )

    def disputed(self, *others: str) -> str:
        return (
            "Books XI-XIV were issued about 417, if the text is his; "
            + " and ".join(others)
            + " prints it under another name."
        )

    def parallel(self, passage_ids: list[str] | None = None, **fields: object) -> dict:
        entry: dict[str, object] = {
            "passage_ids": passage_ids or [self.HUNG, self.OTHER],
            "hung": self.HUNG,
            "received_basis": "The Breviary reads it under his name.",
            "identity_basis": "Both printings open with the same words.",
        }
        entry.update(fields)
        return entry

    def row(self, passage_id: str) -> dict:
        return {
            "passage_id": passage_id,
            "work_id": "work.augustine.de-civitate-dei",
            "work_alias": {"author": "Augustine of Hippo", "work": "De civitate Dei"},
            "text_date": 417,
            "text_date_basis": "Books XI-XIV were issued about 417.",
            "numbering": "vulgate",
            "extent": dict(self.EXTENT),
            "basis": "The excerpt expounds the making of light.",
        }

    def declare(
        self,
        *parallels: dict,
        also_hung: tuple[dict, ...] = (),
        blocked: tuple[dict, ...] = (),
        **hung_row: object,
    ) -> None:
        import yaml

        hung_row.setdefault("text_date_basis", self.disputed(self.OTHER))
        self.write_edges(**hung_row)
        path = self.root / "src/sources/commentary/fragment-loci.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["fragments"].extend(also_hung)
        if blocked:
            data["blocked"] = list(blocked)
        data["parallels"] = list(parallels)
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def only(self, needle: str) -> None:
        errors = self.errors()
        self.assertEqual(len(errors), 1, errors)
        self.assertIn(needle, errors[0])

    def test_one_text_hung_once_under_its_received_name_validates(self) -> None:
        self.declare(self.parallel())
        self.assertEqual(self.errors(), [])
        with self.subTest("the dispute carried in basis, closing a sentence"):
            self.declare(
                self.parallel(),
                text_date_basis="Books XI-XIV were issued about 417.",
                basis=f"The excerpt expounds the making of light. It also stands as {self.OTHER}.",
            )
            self.assertEqual(self.errors(), [])

    def test_an_unhung_member_hung_as_a_fragment_is_refused(self) -> None:
        self.declare(self.parallel(), also_hung=(self.row(self.OTHER),))
        self.only(f"{self.OTHER} is also hung as a fragment")
        with self.subTest("placed on the page as blocked"):
            self.declare(
                self.parallel(),
                blocked=(
                    {
                        "passage_ids": [self.OTHER],
                        "work_alias": {
                            "author": "Augustine of Hippo",
                            "work": "De civitate Dei",
                        },
                        "numbering": "vulgate",
                        "extent": dict(self.EXTENT),
                        "reason": "A reason.",
                        "fix": "A fix.",
                    },
                ),
            )
            self.only(f"{self.OTHER} also stands in blocked")

    def test_a_parallel_whose_hung_member_is_not_a_fragment_is_refused(self) -> None:
        self.declare(self.parallel([self.OTHER, self.THIRD], hung=self.OTHER))
        self.only(f"hangs {self.OTHER}, which is not a fragment above")

    def test_a_parallel_naming_an_unknown_passage_is_refused(self) -> None:
        self.declare(
            self.parallel([self.HUNG, self.UNKNOWN]),
            text_date_basis=self.disputed(self.UNKNOWN),
        )
        self.only(f"names {self.UNKNOWN}, which is not a passage record")

    def test_a_hung_row_that_does_not_carry_the_dispute_is_refused(self) -> None:
        self.declare(self.parallel(), text_date_basis="Books XI-XIV were issued about 417.")
        self.only("does not carry the dispute")
        with self.subTest("a longer id is not the id"):
            self.declare(self.parallel(), text_date_basis=self.disputed(self.OTHER + "0"))
            self.only("does not carry the dispute")

    def test_an_entry_too_malformed_to_ask_is_refused(self) -> None:
        cases = (
            ("one record", (self.parallel([self.HUNG]),), "two or more distinct passage_ids"),
            (
                "one record twice",
                (self.parallel([self.HUNG, self.HUNG]),),
                "two or more distinct passage_ids",
            ),
            (
                "hung outside its members",
                (self.parallel(hung=self.THIRD),),
                "which is not one of its passage_ids",
            ),
            ("no identity basis", (self.parallel(identity_basis=" "),), "needs its identity_basis"),
            (
                "an unknown field",
                (self.parallel(note="x"),),
                "needs passage_ids, hung, received_basis and identity_basis",
            ),
            (
                "one record in two parallels",
                (self.parallel(), self.parallel([self.HUNG, self.THIRD])),
                "which parallels[1] already names",
            ),
        )
        for name, parallels, needle in cases:
            with self.subTest(name):
                self.declare(*parallels, text_date_basis=self.disputed(self.OTHER, self.THIRD))
                self.only(needle)


class ParallelCorpusTests(unittest.TestCase):
    """Rule 15 against the repository's own edge, on the case that raised it."""

    SERMO = "passage.peter-chrysologus.sermones.1894-garnier-migne-pl-52.sermo-50"
    HOMILIA = "passage.maximus-of-turin.homiliae.1862-migne-pl-57.homilia-108"

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = _catena.load_edges(ROOT)
        cls.sources = _catena.load_sources(ROOT)

    def test_sermo_50_is_hung_once_under_chrysologus(self) -> None:
        entries = [
            entry
            for entry in self.data.get("parallels") or ()
            if self.SERMO in entry["passage_ids"]
        ]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["hung"], self.SERMO)
        self.assertIn(self.HOMILIA, entries[0]["passage_ids"])
        hung = {fragment["passage_id"] for fragment in self.data["fragments"]}
        self.assertIn(self.SERMO, hung)
        self.assertNotIn(self.HOMILIA, hung)
        self.assertEqual(_catena._parallel_errors(self.sources, self.data, "edge"), [])

    def test_the_sermo_50_row_is_refused_once_it_stops_naming_homilia_108(self) -> None:
        data = copy.deepcopy(self.data)
        row = next(one for one in data["fragments"] if one["passage_id"] == self.SERMO)
        row["text_date_basis"] = row["text_date_basis"].replace(self.HOMILIA, "PL 57")
        errors = _catena._parallel_errors(self.sources, data, "edge")
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("does not carry the dispute", errors[0])


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

    def test_linkage_audit_does_not_count_an_unresolved_english_target(self):
        import _catena_snippets
        self.write_edges(english_versions=[{"passage_id": "missing", "coverage": "whole", "basis": "I.7"}])
        report = _catena_snippets.audit(self.root)
        self.assertTrue(report["errors"])
        self.assertEqual(report["counted"]["english_coverage"], {"invalid-link": 1})

    def test_catalogue_refuses_an_edge_whose_text_record_is_missing(self):
        next(self.root.glob("src/sources/works/**/passages/11.7.toml")).unlink()
        with self.assertRaisesRegex(_catena.CatenaError, "held passage text and edition"):
            self.emit()

    def test_the_chapter_spine_carries_no_prose(self) -> None:
        directory = self.emit()
        spine = json.loads(
            (directory / "01-gen" / "1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(spine["fragments"]), 1)
        index = json.loads((directory / "index.json").read_text())
        book = next(row for row in index["held"] if row["token"] == "Gen")
        self.assertEqual(book["commentary_chapters"], [{"chapter": 1, "fragments": 1, "english": 1}])
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


def _u16_slice(text: str, start: int, end: int) -> str:
    return text.encode("utf-16-le")[2 * start : 2 * end].decode("utf-16-le")


class TextStructureTests(unittest.TestCase):
    """Additive UTF-16 `text_structure` projection never alters verbatim `text`."""

    def test_mark_catena_aurea_lemmas_speakers_transitions_notes_and_edge_lines(self) -> None:
        import tomllib

        ed = ROOT / "src/sources/works/thomas-aquinas/catena-aurea-in-marcum/editions/1842-english-oxford-ccel"
        artifact = tomllib.loads((ed / "artifacts/text-790ed587/artifact.toml").read_text(encoding="utf-8"))
        work_id = "work.thomas-aquinas.catena-aurea-in-marcum"

        # 01-02-03 has lemmas, speakers, and [ed. note: ...]
        p01 = tomllib.loads((ed / "passages/01-02-03.toml").read_text(encoding="utf-8"))
        ts01 = _catena.text_structure_for_passage(ROOT, p01, p01["text"], work_id=work_id, artifact=artifact)
        self.assertIsNotNone(ts01)
        self.assertEqual(ts01["version"], 1)
        paras = ts01["paragraphs"]
        self.assertEqual(len(paras), len(p01["transcription_segments"]))
        self.assertTrue(any(p["kind"] == "lemma" for p in paras))
        self.assertTrue(any("speaker" in p for p in paras))
        self.assertTrue(any("notes" in p for p in paras))
        for p in paras:
            chunk = _u16_slice(p01["text"], p["start"], p["end"])
            self.assertEqual(chunk, chunk.strip())
            if "speaker" in p:
                sp = _u16_slice(p01["text"], *p["speaker"])
                self.assertFalse(sp.lower().startswith(("it goes on", "there follows", "wherefore")))
            if "notes" in p:
                for note in p["notes"]:
                    nt = _u16_slice(p01["text"], *note)
                    self.assertTrue(nt.startswith("[ed") and nt.endswith("]"))

        # 01-35-39 has transitional cues (`It goes on:`, `There follows:`, `For there follows:`)
        p35 = tomllib.loads((ed / "passages/01-35-39.toml").read_text(encoding="utf-8"))
        ts35 = _catena.text_structure_for_passage(ROOT, p35, p35["text"], work_id=work_id, artifact=artifact)
        transitions = [
            _u16_slice(p35["text"], *p["transition"])
            for p in ts35["paragraphs"] if "transition" in p
        ]
        self.assertTrue(transitions)
        self.assertIn("It goes on:", transitions)
        self.assertIn("There follows:", transitions)
        for p in ts35["paragraphs"]:
            if "transition" in p:
                self.assertNotIn("speaker", p)

        # Mark L2016 (Chrys.:) and L2867 (Theophylact:) were mis-tagged scripture in CCEL;
        # L3147 (Amen.) is closing plain text, not a lemma.
        for stem, target_line, expected_kind, expect_speaker in (
            ("11-01-10", 2016, "commentary", True),
            ("15-16-20", 2867, "commentary", True),
            ("16-19-20", 3147, "plain", False),
        ):
            pas = tomllib.loads((ed / "passages" / f"{stem}.toml").read_text(encoding="utf-8"))
            ts = _catena.text_structure_for_passage(ROOT, pas, pas["text"], work_id=work_id, artifact=artifact)
            matched = [
                para for seg, para in zip(pas["transcription_segments"], ts["paragraphs"])
                if seg["line"] == target_line
            ]
            self.assertEqual(len(matched), 1)
            self.assertEqual(matched[0]["kind"], expected_kind)
            self.assertEqual("speaker" in matched[0], expect_speaker)

    def test_pinned_gregory_and_severian_recover_paragraphs_without_moving_snippets(self) -> None:
        import tomllib
        import _catena_snippets

        greg_path = ROOT / (
            "src/sources/works/nicene-and-post-nicene-fathers/series-2-volume-5/"
            "editions/new-york-1893/passages/gregory-de-hominis-opificio.toml"
        )
        greg = tomllib.loads(greg_path.read_text(encoding="utf-8"))
        original_text = greg["text"]
        ts = _catena.text_structure_for_passage(
            ROOT, greg, original_text, work_id="work.gregory-of-nyssa.de-hominis-opificio"
        )
        self.assertIsNotNone(ts)
        self.assertEqual(len(ts["paragraphs"]), 280)
        self.assertEqual(greg["text"], original_text)
        self.assertTrue(all(p["kind"] == "plain" for p in ts["paragraphs"]))
        # Verify pinned snippet slices in passage-snippets.yaml remain valid against unchanged text
        doc = _catena._load_yaml(ROOT / _catena_snippets.PATH)
        row = next(r for r in doc["passages"] if r["passage_id"] == greg["id"])
        for sn in _catena_snippets.project(original_text, row["snippets"]):
            self.assertTrue(_u16_slice(original_text, sn["start"], sn["end"]).strip())

        sev_path = ROOT / (
            "src/sources/works/severian-of-gabala/in-cosmogoniam-homiliae/"
            "editions/2010-pearse-bareille-sermon-1/passages/homilia-1.toml"
        )
        sev = tomllib.loads(sev_path.read_text(encoding="utf-8"))
        ts_sev = _catena.text_structure_for_passage(
            ROOT, sev, sev["text"], work_id="work.severian-of-gabala.in-cosmogoniam-homiliae"
        )
        self.assertIsNotNone(ts_sev)
        self.assertEqual(len(ts_sev["paragraphs"]), 18)

    def test_wrapped_lines_and_sentence_splits_are_excluded(self) -> None:
        import tomllib

        cases = (
            (
                "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/passages/11.7.toml",
                "work.augustine.de-civitate-dei",
            ),
            (
                "src/sources/works/peter-chrysologus/sermones/editions/1894-garnier-migne-pl-52/passages/sermo-50.toml",
                "work.peter-chrysologus.sermones",
            ),
            (
                "src/sources/works/origen/homiliae-in-ezechielem/editions/2014-hooker/passages/homily-1-section-6.toml",
                "work.origen.homiliae-in-ezechielem",
            ),
        )
        for rel, work_id in cases:
            with self.subTest(passage=rel):
                pas = tomllib.loads((ROOT / rel).read_text(encoding="utf-8"))
                self.assertIsNone(
                    _catena.text_structure_for_passage(ROOT, pas, pas["text"], work_id=work_id)
                )

    def test_utf16_astral_offsets_speaker_transition_notes_and_minimal_emission(self) -> None:
        # Astral character 😀 occupies 2 UTF-16 code units; offsets must match JS slice.
        text = (
            "Intro 😀 paragraph.\n\n"
            "Bede: It goes on: “Word” [ed. note: gloss 😀 check].\n\n"
            "Augustine [ed. note: ref]: Final comment."
        )
        ts = _catena.text_structure_for_passage(
            ROOT, {}, text, work_id="work.thomas-aquinas.catena-aurea-in-marcum"
        )
        self.assertIsNotNone(ts)
        p0, p1, p2 = ts["paragraphs"]
        self.assertEqual(_u16_slice(text, p0["start"], p0["end"]), "Intro 😀 paragraph.")
        self.assertEqual(_u16_slice(text, *p1["speaker"]), "Bede:")
        self.assertEqual(_u16_slice(text, *p1["transition"]), "It goes on:")
        self.assertEqual(_u16_slice(text, *p1["notes"][0]), "[ed. note: gloss 😀 check]")
        # Speaker before [ed. note: ...] never overlaps its note span.
        self.assertEqual(_u16_slice(text, *p2["speaker"]), "Augustine")
        self.assertEqual(_u16_slice(text, *p2["notes"][0]), "[ed. note: ref]")
        self.assertLess(p2["speaker"][1], p2["notes"][0][0])

        # Minimal emission: single plain paragraph with no notes/speaker/lemma returns None.
        self.assertIsNone(_catena.text_structure_for_passage(ROOT, {}, "Just one plain paragraph."))
        # Single paragraph with literal [ed. note: ...] DOES emit.
        noted = _catena.text_structure_for_passage(
            ROOT, {}, "Single paragraph [ed. note: checked]."
        )
        self.assertIsNotNone(noted)
        self.assertEqual(len(noted["paragraphs"]), 1)
        self.assertEqual(len(noted["paragraphs"][0]["notes"]), 1)

        # Invariant guard fails closed on invalid spans.
        with self.assertRaises(_catena.CatenaError):
            _catena._validate_text_structure(
                {"version": 1, "paragraphs": [{"start": 0, "end": 10, "kind": "plain"}]}, 5
            )


class PipelineConsistencyTests(CatenaFixture):
    """Caching, root propagation, segment edition_id resolution, and paragraph chapters."""

    def test_index_bible_is_cached_and_absent_by_work_reuses_sources(self) -> None:
        from unittest.mock import patch

        self.assertIs(_catena._index_bible(ROOT), _catena._index_bible(ROOT))
        sources = _catena.load_sources(self.root)
        edges = _catena.load_edges(self.root)
        with patch.object(_catena, "load_sources", side_effect=AssertionError("re-walked sources")):
            self.assertEqual(_catena.absent_by_work(self.root, sources=sources, edges=edges), {})

    def test_segment_backed_edition_id_resolved_in_fragments_and_english_versions(self) -> None:
        sources = _catena.Sources(
            works={},
            editions={"ed-la": {"language": "la"}, "ed-en": {"language": "en"}},
            artifacts={},
            segments={"seg-en": {"edition_id": "ed-en"}},
            passages={
                "src": {"edition_id": "ed-la"},
                "tgt": {"segment_id": "seg-en"},
            },
        )
        self.assertEqual(_catena.passage_edition_id(sources, sources.passages["tgt"]), "ed-en")
        extent = dict(token="Gen", first_chapter=1, first_verse=1, last_chapter=1, last_verse=2)
        fragments = [
            {
                "passage_id": "src", "work_id": "w", "extent": extent,
                "english_versions": [{"passage_id": "tgt", "coverage": "whole", "basis": "Matched."}],
            },
            {"passage_id": "tgt", "work_id": "w", "extent": extent},
        ]
        self.assertEqual(_catena._english_version_errors(sources, fragments), [])

    def test_commentary_work_index_accepts_ecclesiastical_writer_role(self) -> None:
        name = "_test_commentary_work_index"
        loader = importlib.machinery.SourceFileLoader(
            name, str(ROOT / "tools/commentary-work-index")
        )
        spec = importlib.util.spec_from_loader(name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            loader.exec_module(module)
        finally:
            sys.modules.pop(name, None)
        self.assertEqual(module.SOURCE_ROLES.get("ecclesiastical-writer"), "ecclesiastical-writer")

    def test_paragraph_index_emits_chapters_map_matching_emitted_files(self) -> None:
        directory, files, _ = _catena._paragraph_files(ROOT, self.root / "out")
        index = json.loads(files[directory / "index.json"])
        self.assertTrue(index["editions"])
        for edition, entry in index["editions"].items():
            self.assertIn("chapters", entry)
            emitted = {
                (json.loads(body)["token"], json.loads(body)["chapter"])
                for path, body in files.items()
                if path != directory / "index.json" and path.relative_to(directory).parts[0] == edition
            }
            listed = {
                (token, chapter)
                for token, chapters in entry["chapters"].items()
                for chapter in chapters
            }
            self.assertEqual(listed, emitted, edition)


if __name__ == "__main__":
    unittest.main()
