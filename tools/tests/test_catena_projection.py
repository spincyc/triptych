"""Canonical chapter display and exact source-controller regressions."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _catena  # noqa: E402
if __package__:
    from .test_catena import CatenaFixture  # noqa: E402
else:
    from test_catena import CatenaFixture  # noqa: E402


class ChapterProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.editions = _catena._scripture_editions(ROOT)
        cls.books = {book["token"]: book for book in _catena.canon(ROOT)}
        cls.projected = {
            token: _catena.scripture_for_book(ROOT, cls.books[token], cls.editions)
            for token in ("Ps", "Gen", "Dan", "Ecclus", "Esth", "Acts", "Mark")
        }

    def chapter(self, token: str, chapter: int) -> dict:
        return self.projected[token]["chapters"][str(chapter)]

    def native(self, token: str, chapter: int, edition: str) -> list[dict]:
        citation = self.chapter(token, chapter)
        reader = next(reader for reader, _ in self.editions if reader.id == edition)
        self.assertNotIn(edition, citation.get("refused", {}))
        self.assertNotIn(reader.addressing, citation.get("refused", {}))
        return citation.get("edition_loci", {}).get(edition, citation["loci"][reader.addressing])

    def test_miserere_uses_native_king_james_psalm_51(self) -> None:
        loci = self.native("Ps", 50, "king-james-version")
        self.assertEqual(loci, [{"chapter": 51, "first": None, "last": None}])
        native = json.loads((ROOT / "src/sources/bibles/king-james-version/chapters/Ps/51.json").read_text())
        self.assertIn("Have mercy upon me", native["verses"]["1"])

    def test_joined_psalm_retains_both_native_chapters(self) -> None:
        self.assertEqual(self.native("Ps", 9, "king-james-version"), [
            {"chapter": 9, "first": None, "last": None},
            {"chapter": 10, "first": None, "last": None},
        ])

    def test_partial_native_psalm_does_not_include_other_canonical_psalm(self) -> None:
        self.assertEqual(self.native("Ps", 147, "king-james-version"), [
            {"chapter": 147, "first": 12, "last": None},
        ])
        self.assertEqual(self.native("Ps", 147, "clementine-vulgate"), [
            {"chapter": 147, "first": None, "last": None},
        ])

    def test_whole_native_psalm_keeps_unaliased_split_and_renumbered_tail_once(self) -> None:
        edition = "catholic-public-domain-version"
        loci = self.native("Ps", 13, edition)
        self.assertEqual(loci, [{"chapter": 13, "first": None, "last": None}])
        _reader, bible = next(pair for pair in self.editions if pair[0].id == edition)
        selected = []
        for locus in loci:
            low, high = bible.chapters[("Ps", locus["chapter"])]
            selected.extend(range(locus.get("first") or low, (locus.get("last") or high) + 1))
        self.assertEqual(selected, list(range(1, 11)))
        self.assertEqual(len(selected), len(set(selected)))

    def test_successful_psalm_projections_never_repeat_native_verses(self) -> None:
        for chapter, citation in self.projected["Ps"]["chapters"].items():
            for reader, bible in self.editions:
                refused = citation.get("refused", {})
                if reader.id in refused or reader.addressing in refused:
                    continue
                loci = citation.get("edition_loci", {}).get(reader.id, citation["loci"][reader.addressing])
                selected = []
                for locus in loci:
                    token = locus.get("book") or "Ps"
                    low, high = bible.chapters[(token, locus["chapter"])]
                    first = low if locus.get("first") is None else locus["first"]
                    last = high if locus.get("last") is None else locus["last"]
                    selected.extend((token, locus["chapter"], verse) for verse in range(first, last + 1))
                with self.subTest(chapter=chapter, edition=reader.id):
                    self.assertEqual(len(selected), len(set(selected)))

    def test_whole_psalm_keeps_existing_edition_refusals(self) -> None:
        for chapter in (42, 92):
            self.assertIn("catholic-public-domain-version", self.chapter("Ps", chapter)["refused"])

    def test_identity_chapter_and_empty_commentary_chapter_are_present(self) -> None:
        chapter = self.chapter("Gen", 40)
        self.assertEqual(chapter["numbering"], "vulgate")
        self.assertEqual(self.native("Gen", 40, "king-james-version"), [
            {"chapter": 40, "first": 1, "last": 23},
        ])
        self.assertEqual(set(self.projected["Gen"]["chapters"]), {str(n) for n in range(1, 51)})

    def test_daniel_chapter_redirect_preserves_two_books(self) -> None:
        self.assertEqual(self.native("Dan", 13, "king-james-version"), [
            {"book": "Sus", "chapter": 1, "first": 1, "last": 64},
            {"book": "Bel", "chapter": 1, "first": 1, "last": 1},
        ])

    def test_reordered_daniel_runs_are_not_coalesced(self) -> None:
        reader, bible = next(pair for pair in self.editions if pair[0].id == "king-james-version")
        loci, problem = _catena._native_scripture_loci(
            reader, bible, "Dan", [{"chapter": 3, "first": 53, "last": 60}],
        )
        self.assertEqual(problem, "")
        song = [locus for locus in loci if locus.get("book") == "SgThree"]
        self.assertGreater(len(song), 3)
        starts = [locus["first"] for locus in song]
        self.assertTrue(any(left > right for left, right in zip(starts, starts[1:])))

    def test_absent_and_unrecorded_verses_refuse_whole_chapter(self) -> None:
        self.assertIn("king-james-version", self.chapter("Dan", 14)["refused"])
        self.assertIn("king-james-version", self.chapter("Dan", 3)["refused"])
        self.assertIn("no verse-level correspondence", self.chapter("Ecclus", 1)["refused"]["king-james-version"])
        self.assertIn("revised-version-1895", self.chapter("Acts", 8)["refused"])

    def test_unestablished_esther_correspondence_is_not_identity(self) -> None:
        self.assertIn("king-james-version", self.chapter("Esth", 15)["refused"])

    def test_unrecorded_longer_native_chapter_is_not_silently_truncated(self) -> None:
        problem = self.chapter("Mark", 9)["refused"]["king-james-version"]
        self.assertIn("1-49", problem)
        self.assertIn("1-50", problem)
        self.assertIn("no chapter correspondence", problem)


class PassageControllerTests(unittest.TestCase):
    passage_id = "passage.augustine.de-civitate-dei.dods-1871.11.7"
    work_id = "work.augustine.de-civitate-dei"
    edition = "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
    artifact_id = "artifact.npnf.container.body"
    segment_id = "segment.augustine.de-civitate-dei.dods-1871.constituent"

    def setUp(self) -> None:
        self.fixture = CatenaFixture()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.root = self.fixture.root

    def segment_passage(self, rights: str = "public-domain") -> None:
        self.fixture.write(
            "src/sources/works/npnf/container/editions/printing/artifacts/body/artifact.toml",
            f'''schema = 2
record_type = "artifact"
id = "{self.artifact_id}"
edition_id = "edition.npnf.container.printing"
rights_status = "{rights}"
rights_basis = "The exact container printing's recorded basis."
''',
        )
        self.fixture.write(self.edition + "segments/constituent.toml", f'''schema = 2
record_type = "segment"
id = "{self.segment_id}"
edition_id = "edition.augustine.de-civitate-dei.dods-1871"
artifact_id = "{self.artifact_id}"
''')
        path = self.root / self.edition / "passages/11.7.toml"
        body = path.read_text().replace("schema = 1", "schema = 2").replace(
            'artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"',
            f'segment_id = "{self.segment_id}"',
        )
        path.write_text(body)

    def errors(self) -> list[str]:
        return _catena._passage_errors(
            _catena.load_sources(self.root), "fragment", self.passage_id, self.work_id,
        )

    def test_direct_artifact_is_unchanged(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_projection_file_includes_a_chapter_with_no_commentary_spine(self) -> None:
        self.fixture.write(str(_catena.MODEL_RELATIVE), (ROOT / _catena.MODEL_RELATIVE).read_text())
        directory, files, _written = _catena._structure_files(self.root, self.root / "out")
        index = json.loads(files[directory / "index.json"])
        self.assertEqual(index["scripture"], "structure/catena/scripture/")
        folder = next(book["path"] for book in index["canon"] if book["token"] == "Gen")
        payload = json.loads(files[directory / "scripture" / f"{folder}.json"])
        self.assertEqual(set(payload["chapters"]), {"1", "2", "3"})
        self.assertNotIn(directory / folder / "003.json", files)

    def test_segment_borrows_exact_container_artifact(self) -> None:
        self.segment_passage()
        sources = _catena.load_sources(self.root)
        artifact = _catena.controlling_artifact(sources, sources.passages[self.passage_id])
        self.assertEqual(artifact["id"], self.artifact_id)
        self.assertEqual(self.errors(), [])
        self.assertEqual(_catena.fragments_for_book(self.root, "Gen")[0]["rights"], "public-domain")

    def test_segment_does_not_bypass_rights(self) -> None:
        self.segment_passage("unknown")
        self.assertTrue(any("may not be published" in error for error in self.errors()))

    def test_missing_segment_has_no_artifact_fallback(self) -> None:
        self.segment_passage()
        (self.root / self.edition / "segments/constituent.toml").unlink()
        errors = self.errors()
        self.assertTrue(any("does not resolve" in error for error in errors))
        self.assertTrue(any("reaches no artifact" in error for error in errors))

    def test_segment_does_not_bypass_explicit_text_gate(self) -> None:
        self.segment_passage()
        path = self.root / self.edition / "passages/11.7.toml"
        path.write_text(path.read_text().replace(
            'text = "And first of all, indeed, light was made by the word of God."', 'text = ""',
        ))
        self.assertTrue(any("has no text" in error for error in self.errors()))


if __name__ == "__main__":
    unittest.main()
