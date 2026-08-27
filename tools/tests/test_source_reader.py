#!/usr/bin/env python3
"""The source reader: what it may publish, and what it must refuse.

Every assertion here stands for a way this reader could work perfectly and be
wrong. A restricted text served under a permissive neighbour's basis reads
exactly like a text that was cleared; a withheld passage rendered as a blank is
indistinguishable from a passage with nothing in it; a licensed text served
without its acknowledgement looks identical to one that carries no condition.
None of those breaks anything, which is why each one is checked rather than
trusted.

The rights tests are the load-bearing ones. They are written against synthesised
records rather than against whatever the corpus happens to hold today, because a
rule that is only ever exercised by the data in the tree stops being tested the
moment the tree changes.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TOOL = ROOT / "tools" / "source-reader"
TRACKED = ROOT / "src/web/data/structure/sources"
MODEL = ROOT / "src/web/browser/sources/reader-model.js"
PAGE = ROOT / "src/web/browser/sources/index.html"


def _module():
    loader = importlib.machinery.SourceFileLoader("source_reader_under_test", str(TOOL))
    spec = importlib.util.spec_from_loader("source_reader_under_test", loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["source_reader_under_test"] = module
    loader.exec_module(module)
    return module


reader = _module()


class FakeRecord:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.path = Path("/nowhere")


class FakeLibrary:
    """Just enough library for the rights rule to be exercised in isolation."""

    def __init__(self, records: dict, root: Path | None = None) -> None:
        self.records = {key: FakeRecord(value) for key, value in records.items()}
        self.root = root or ROOT


def artifact(**overrides) -> dict:
    base = {
        "id": "artifact.test",
        "rights_status": "public-domain",
        "rights_basis": "Published in 1887 and out of copyright.",
        "storage": "tracked",
        "media_type": "text/plain; charset=utf-8",
        "artifact_type": "transcribed-text",
    }
    base.update(overrides)
    return base


def library_with(**overrides) -> FakeLibrary:
    return FakeLibrary({"artifact.test": artifact(**overrides)})


def passage(**overrides) -> dict:
    base = {"id": "passage.test", "artifact_id": "artifact.test", "locus": "1.1"}
    base.update(overrides)
    return base


class RightsRuleTests(unittest.TestCase):
    """A passage is readable only where a record says both halves of the rule."""

    def test_public_domain_tracked_transcription_is_readable(self) -> None:
        reading = reader.reading_of(library_with(), passage(text="In principio."))
        self.assertTrue(reading["readable"])
        self.assertEqual(reading["text"], "In principio.")

    def test_restricted_rights_are_refused_even_when_the_bytes_are_tracked(self) -> None:
        """The failure this whole tool is built around.

        Bytes on disk are not a permission. An artifact whose rights record says
        the project may read it and not republish it must never be served, and
        the presence of a payload beside the manifest must not change that.
        """
        reading = reader.reading_of(
            library_with(rights_status="restricted"), passage(text="Withheld words.")
        )
        self.assertFalse(reading["readable"])
        self.assertEqual(reading["withheld"], "rights")
        self.assertNotIn("text", reading)

    def test_unresolved_rights_are_refused(self) -> None:
        """An unsettled question is not a permission."""
        reading = reader.reading_of(
            library_with(rights_status="unresolved"), passage(text="Unsettled.")
        )
        self.assertFalse(reading["readable"])
        self.assertEqual(reading["withheld"], "rights")
        self.assertNotIn("text", reading)

    def test_remote_storage_is_refused_even_when_the_rights_are_clear(self) -> None:
        reading = reader.reading_of(
            library_with(storage="remote"), passage(text="Not retained here.")
        )
        self.assertFalse(reading["readable"])
        self.assertEqual(reading["withheld"], "storage")
        self.assertNotIn("text", reading)

    def test_rights_are_reported_before_storage(self) -> None:
        """The governing reason, not an incidental one.

        An artifact that is both restricted and remote is refused for its
        rights, because that is the fact that would still hold if the bytes were
        fetched tomorrow.
        """
        reading = reader.reading_of(
            library_with(rights_status="restricted", storage="remote"), passage()
        )
        self.assertEqual(reading["withheld"], "rights")

    def test_every_refusal_states_a_reason(self) -> None:
        """A blank is indistinguishable from an empty text. There are no blanks."""
        cases = [
            library_with(rights_status="restricted"),
            library_with(rights_status="unresolved"),
            library_with(storage="remote"),
            library_with(storage="restricted"),
            library_with(storage="unavailable"),
            FakeLibrary({}),
        ]
        for held in cases:
            reading = reader.reading_of(held, passage())
            with self.subTest(withheld=reading["withheld"]):
                self.assertFalse(reading["readable"])
                self.assertTrue(str(reading["reason"]).strip())

    def test_a_passage_with_no_controlling_artifact_is_refused_not_crashed(self) -> None:
        reading = reader.reading_of(FakeLibrary({}), passage(text="Orphaned."))
        self.assertFalse(reading["readable"])
        self.assertEqual(reading["withheld"], "uncontrolled")


class ProseRuleTests(unittest.TestCase):
    """Lawful to distribute is not the same as being a reading."""

    def test_a_structured_row_is_not_set_as_prose(self) -> None:
        """The rule that keeps a TSV key and its pagination out of a prayer."""
        held = library_with(media_type="text/tab-separated-values; charset=utf-8")
        reading = reader.reading_of(held, passage(physical_line_ranges=[[1, 2]]))
        self.assertFalse(reading["readable"])
        self.assertEqual(reading["withheld"], "not-prose")

    def test_a_passage_with_neither_transcription_nor_bounds_is_refused(self) -> None:
        reading = reader.reading_of(library_with(), passage())
        self.assertFalse(reading["readable"])
        self.assertEqual(reading["withheld"], "no-transcription")

    def test_withheld_projection_omits_prose_bearing_metadata(self) -> None:
        one = passage(
            context="Protected context must not become a quotation channel.",
            notes="Protected notes must not become a quotation channel.",
        )
        held = library_with(rights_status="unresolved", storage="remote")
        work = {
            "id": "work.test", "title": "W", "author": None,
            "category": None, "languages": [], "alternate_titles": [],
            "description": None,
        }
        edition = {
            "id": "edition.test", "title": "E", "language": "en",
            "date": "2026", "year": 2026, "publication": None,
            "editors": [], "translators": [], "authority": None,
            "jurisdiction": None, "notes": "Protected edition quotation.",
            "artifacts": [{
                **next(iter(held.records.values())).data,
                "notes": "Protected artifact quotation.",
            }],
            "passages": [{**one, "reading": reader.reading_of(held, one)}],
        }
        payload = reader.edition_payload(work, edition)
        row = payload["passages"][0]
        self.assertFalse(row["readable"])
        for field in ("context", "notes", "rights_basis"):
            self.assertNotIn(field, row)
        self.assertNotIn("notes", payload["edition"])
        self.assertNotIn("notes", payload["artifacts"][0])
        self.assertNotIn("rights_basis", payload["artifacts"][0])

    def test_a_transcription_wins_over_line_bounds(self) -> None:
        """The checked transcription is the reading; the bounds are its evidence."""
        reading = reader.reading_of(
            library_with(), passage(text="Checked.", physical_line_ranges=[[1, 1]])
        )
        self.assertTrue(reading["readable"])
        self.assertEqual(reading["source"], "transcription")


class AcknowledgementTests(unittest.TestCase):
    """A licence is a permission with a condition, and the condition travels."""

    def test_a_licensed_text_carries_its_acknowledgement(self) -> None:
        work = {
            "id": "work.test",
            "title": "T",
            "author": "A",
            "category": "c",
            "languages": [],
            "alternate_titles": [],
            "description": None,
        }
        held = library_with(
            rights_status="licensed",
            rights_basis="Licensed under Creative Commons Attribution 4.0 by its author.",
        )
        one = passage(text="Licensed words.")
        edition = {
            "id": "edition.test",
            "title": "E",
            "language": "en",
            "date": "1867",
            "year": 1867,
            "publication": None,
            "editors": [],
            "translators": [],
            "authority": None,
            "jurisdiction": None,
            "notes": None,
            "directory": "editions/test/",
            "file": "1867-test.json",
            "artifacts": [],
            "passages": [{**one, "reading": reader.reading_of(held, one)}],
        }
        payload = reader.edition_payload(work, edition)
        row = payload["passages"][0]
        self.assertTrue(row["readable"])
        self.assertIn("Creative Commons", row["acknowledgement"])

    def test_licensed_is_in_the_distributable_set_and_restricted_is_not(self) -> None:
        self.assertIn("licensed", reader.DISTRIBUTABLE_RIGHTS)
        self.assertIn("public-domain", reader.DISTRIBUTABLE_RIGHTS)
        self.assertNotIn("restricted", reader.DISTRIBUTABLE_RIGHTS)
        self.assertNotIn("unresolved", reader.DISTRIBUTABLE_RIGHTS)
        self.assertIn("licensed", reader.ATTRIBUTION_REQUIRED)


class PathConventionTests(unittest.TestCase):
    """Anything with an inherent order sorts in that order in a listing."""

    def test_an_edition_takes_its_year_as_a_prefix(self) -> None:
        held = FakeLibrary({"edition.test": {}})
        held.records["edition.test"].path = (
            ROOT / "src/sources/works/ns/w/editions/dods-1871/edition.toml"
        )
        held.source_root = ROOT / "src/sources"
        stem = reader.edition_stem(held, {"id": "edition.test", "date": "1871"})
        self.assertEqual(stem, "1871-dods-1871.json")

    def test_an_undated_edition_sorts_after_every_dated_one(self) -> None:
        held = FakeLibrary({"edition.test": {}})
        held.records["edition.test"].path = (
            ROOT / "src/sources/works/ns/w/editions/corrected/edition.toml"
        )
        stem = reader.edition_stem(held, {"id": "edition.test", "date": None})
        self.assertEqual(stem, "undated-corrected.json")
        self.assertGreater(stem, "9999-z.json")

    def test_a_locus_sorts_by_number_and_not_by_string(self) -> None:
        """XI.6 comes before XI.19, which no string ordering gives."""
        loci = ["11.19", "11.6", "11.7", "2.1"]
        self.assertEqual(
            sorted(loci, key=reader._natural), ["2.1", "11.6", "11.7", "11.19"]
        )


class TrackedProjectionTests(unittest.TestCase):
    """The projection a reader is actually served."""

    @classmethod
    def setUpClass(cls) -> None:
        index = TRACKED / "index.json"
        if not index.is_file():
            raise unittest.SkipTest("run `make source-projection` first")
        cls.spine = json.loads(index.read_text(encoding="utf-8"))

    def test_the_spine_carries_no_prose(self) -> None:
        """A search index that shipped the corpus would be the whole failure."""
        for work in self.spine["works"]:
            with self.subTest(work=work["id"]):
                self.assertNotIn("description", work)
                for edition in work["editions"]:
                    self.assertNotIn("text", edition)
                    self.assertNotIn("passages_detail", edition)

    def test_no_text_payload_exists_for_a_withheld_passage(self) -> None:
        """The end-to-end statement of the rights rule.

        Not that the page hides a withheld text — that the words were never
        written into the served tree at all, so no page bug can publish one.
        """
        readable: set[str] = set()
        withheld: set[str] = set()
        for path in (TRACKED / "editions").rglob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            for row in payload["passages"]:
                (readable if row["readable"] else withheld).add(row["id"])
        written = {
            path.stem for path in (TRACKED / "text").glob("*.json")
        } if (TRACKED / "text").is_dir() else set()
        self.assertEqual(written & withheld, set())
        self.assertEqual(written, readable)

    def test_every_withheld_passage_states_its_reason(self) -> None:
        for path in (TRACKED / "editions").rglob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            for row in payload["passages"]:
                if row["readable"]:
                    continue
                with self.subTest(passage=row["id"]):
                    self.assertTrue(str(row.get("reason") or "").strip())
                    self.assertTrue(str(row.get("withheld") or "").strip())

    def test_every_edition_the_spine_names_has_a_file(self) -> None:
        for work in self.spine["works"]:
            for edition in work["editions"]:
                where = TRACKED.parent.parent / (
                    self.spine["root"] + work["directory"] + edition["file"]
                )
                with self.subTest(edition=edition["id"]):
                    self.assertTrue(where.is_file(), f"{where} is missing")

    def test_every_text_payload_names_the_edition_it_belongs_to(self) -> None:
        """The route Catena Omnia follows, written by the generator."""
        directory = TRACKED / "text"
        if not directory.is_dir():
            self.skipTest("no readable passages")
        known = {
            edition["id"]
            for work in self.spine["works"]
            for edition in work["editions"]
        }
        for path in directory.glob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(passage=payload["id"]):
                self.assertIn(payload["edition_id"], known)
                self.assertTrue(payload["edition_path"])


class PageTests(unittest.TestCase):
    """The page and the model it is checked through."""

    def test_the_page_loads_the_model_the_check_replays(self) -> None:
        markup = PAGE.read_text(encoding="utf-8")
        self.assertIn("reader-model.js", markup)
        self.assertIn("sources.js", markup)

    def test_the_model_loads_under_node_and_narrows_nothing_away(self) -> None:
        harness = (
            "const fs=require('fs');const h={exports:{}};"
            "new Function('module','exports',fs.readFileSync(process.argv[1],'utf8'))"
            "(h,h.exports);"
            "const m=h.exports;"
            "process.stdout.write(JSON.stringify(m.tally(m.narrow([], m.blank()))));"
        )
        found = subprocess.run(
            ["node", "-e", harness, str(MODEL)], capture_output=True, text=True
        )
        if found.returncode != 0 and "node" in found.stderr.lower():
            self.skipTest("node is not installed")
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertEqual(
            json.loads(found.stdout),
            {"works": 0, "editions": 0, "passages": 0, "readable": 0},
        )


class CommandTests(unittest.TestCase):
    def test_check_passes_against_the_tracked_projection(self) -> None:
        found = subprocess.run(
            [sys.executable, str(TOOL), "check", "--json"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(found.returncode, 0, found.stderr)
        payload = json.loads(found.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["readable"] + payload["withheld"], payload["passages"])

    def test_an_unknown_author_is_an_error_and_not_an_empty_list(self) -> None:
        """A filter that silently returns nothing reads as a corpus that has nothing."""
        found = subprocess.run(
            [sys.executable, str(TOOL), "list", "--author", "Nobody At All"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(found.returncode, 2)


if __name__ == "__main__":
    unittest.main()
