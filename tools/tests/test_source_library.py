from __future__ import annotations

import hashlib
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
TOOL_PATH = ROOT / "tools" / "source-library"
LOADER = importlib.machinery.SourceFileLoader(
    "triptych_source_library", str(TOOL_PATH)
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {TOOL_PATH}")
SOURCE_LIBRARY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SOURCE_LIBRARY
SPEC.loader.exec_module(SOURCE_LIBRARY)


WORK_ID = "work.augustine.de-civitate-dei"
EDITION_ID = "edition.augustine.de-civitate-dei.npnf-dods"
ARTIFACT_ID = "artifact.augustine.de-civitate-dei.npnf-dods.plain-text"
PASSAGE_ID = "passage.augustine.de-civitate-dei.npnf-dods.10.6"
CORPUS_ID = "corpus.augustine.de-civitate-dei.complete-english"
LOCUS = "book-10.chapter-6"

CONTAINER_WORK_ID = "work.ante-nicene-fathers.volume-1"
CONTAINER_EDITION_ID = "edition.ante-nicene-fathers.volume-1.buffalo-1887"
CONTAINER_ARTIFACT_ID = (
    "artifact.ante-nicene-fathers.volume-1.buffalo-1887.plain-text"
)
CONSTITUENT_WORK_ID = "work.irenaeus.adversus-haereses"
CONSTITUENT_EDITION_ID = (
    "edition.irenaeus.adversus-haereses.roberts-rambaut-coxe-anf1-1887"
)
SEGMENT_ID = (
    "segment.irenaeus.adversus-haereses."
    "roberts-rambaut-coxe-anf1-1887.plain-text"
)
SEGMENT_PASSAGE_ID = (
    "passage.irenaeus.adversus-haereses."
    "roberts-rambaut-coxe-anf1-1887.4.14.1"
)
SEGMENT_LOCUS = "book-4.chapter-14.section-1"


class SourceLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "src/sources").mkdir(parents=True)
        (self.root / "src/gpt").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, relative: str, content: str | bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(
                textwrap.dedent(content).lstrip(),
                encoding="utf-8",
            )
        return path

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL_PATH),
                "--root",
                str(self.root),
                *arguments,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def add_valid_vertical_fixture(self) -> bytes:
        artifact_bytes = (
            "No match here.\n"
            "The City offers Sacrifice.\n"
            "A second SACRIFICE witness.\n"
            "Companion: illustration.png\n"
        ).encode("utf-8")
        artifact_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/plain-text/city-of-god.txt"
        )
        self.write(artifact_path, artifact_bytes)
        digest = hashlib.sha256(artifact_bytes).hexdigest()

        self.write(
            "src/sources/works/augustine/de-civitate-dei/work.toml",
            r'''
            schema = 1
            record_type = "work"
            id = "work.augustine.de-civitate-dei"
            title = "De civitate Dei"
            responsible = "Augustine of Hippo"
            work_type = "patristic-treatise"
            languages = ["la"]
            locus_pattern = 'book-[0-9]+\.chapter-[0-9]+'
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/edition.toml",
            '''
            schema = 1
            record_type = "edition"
            id = "edition.augustine.de-civitate-dei.npnf-dods"
            work_id = "work.augustine.de-civitate-dei"
            title = "The City of God"
            language = "en"
            publication = "NPNF, First Series, volume 2"
            date = "1887"
            translators = ["Marcus Dods"]
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/plain-text/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "{ARTIFACT_ID}"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Public-domain translation and transcription"
            rights_jurisdiction = "United States"
            source_url = "https://example.org/city-of-god"
            retrieved = "2026-07-22"
            sha256 = "{digest}"
            byte_size = {len(artifact_bytes)}
            path = "{artifact_path}"
            indexable = true
            encoding = "utf-8"
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/passages/10-6.toml",
            f'''
            schema = 1
            record_type = "passage"
            id = "{PASSAGE_ID}"
            edition_id = "{EDITION_ID}"
            artifact_id = "{ARTIFACT_ID}"
            artifact_sha256 = "{digest}"
            locus = "{LOCUS}"
            states = ["inspected", "verified"]
            context = "The complete chapter and adjacent chapter were inspected."
            physical_line_ranges = [[2, 2]]
            text = "The City offers Sacrifice."
            transcription_segments = [{{ line = 2, text = "The City offers Sacrifice." }}]
            verified_on = "2026-07-22"
            ''',
        )
        corpus_snapshot = hashlib.sha256(
            f"{ARTIFACT_ID}\t{digest}\n".encode("utf-8")
        ).hexdigest()
        self.write(
            "src/sources/corpora/augustine-city-of-god-english.toml",
            f'''
            schema = 1
            record_type = "corpus"
            id = "{CORPUS_ID}"
            title = "Complete English City of God corpus"
            members = ["{ARTIFACT_ID}"]
            snapshot = "sha256:{corpus_snapshot}"
            languages = ["en"]
            scope = "All twenty-two books in the identified English witness."
            completeness = "Complete for this witness, not for Augustine's corpus."
            ''',
        )

        self.write("src/gpt/theology/demo/main.tex", "Demo\n")
        source_only = SOURCE_LIBRARY.load_library(self.root)
        if source_only.errors:
            raise AssertionError(source_only.errors)
        passage_fingerprint = SOURCE_LIBRARY.source_fingerprint(
            source_only, PASSAGE_ID
        )
        corpus_fingerprint = SOURCE_LIBRARY.source_fingerprint(
            source_only, CORPUS_ID
        )
        self.write(
            "src/gpt/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            loci = ["{LOCUS}"]
            role = "direct-witness"
            states = ["inspected", "verified"]
            verified_on = "2026-07-22"
            source_fingerprint = "{passage_fingerprint}"
            context = "The chapter was checked for the document's sacrifice claim."
            claim_keys = ["demo-sacrifice"]

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "negative-search"
            states = ["searched"]
            context = "A bounded literal search found no matching physical lines."
            search_scope = "The complete identified English artifact."
            searched_on = "2026-07-22"
            search_mode = "raw-line-literal-casefold-v1"
            query = "martyrdom"
            method = "Built-in casefolded physical-line literal search."
            matching_line_count = 0
            source_fingerprint = "{corpus_fingerprint}"
            ''',
        )
        return artifact_bytes

    def add_valid_cross_work_segment_fixture(self) -> dict[str, str | bytes]:
        """Add a constituent work bounded inside another work's artifact."""

        artifact_bytes = (
            "needle outside before\n"
            "Container preface.\n"
            "Irenaeus opening needle.\n"
            "Irenaeus shared needle.\n"
            "Irenaeus closing.\n"
            "needle outside after\n"
            "Appendix needle.\n"
        ).encode("utf-8")
        digest = hashlib.sha256(artifact_bytes).hexdigest()
        artifact_path = (
            "src/sources/works/ante-nicene-fathers/volume-1/editions/"
            "buffalo-1887/artifacts/plain-text/anf-volume-1.txt"
        )
        segment_path = (
            "src/sources/works/irenaeus/adversus-haereses/editions/"
            "roberts-rambaut-coxe-anf1-1887/segments/plain-text.toml"
        )
        passage_path = (
            "src/sources/works/irenaeus/adversus-haereses/editions/"
            "roberts-rambaut-coxe-anf1-1887/passages/4-14-1.toml"
        )
        binding_path = (
            "src/gpt/articles/segment-consumer/research/source-bindings.toml"
        )

        self.write(artifact_path, artifact_bytes)
        self.write(
            "src/sources/works/ante-nicene-fathers/volume-1/work.toml",
            r'''
            schema = 1
            record_type = "work"
            id = "work.ante-nicene-fathers.volume-1"
            title = "The Ante-Nicene Fathers, Volume I"
            responsible = "Alexander Roberts and James Donaldson"
            work_type = "edited-anthology"
            languages = ["en"]
            locus_pattern = 'volume-[0-9]+'
            ''',
        )
        self.write(
            "src/sources/works/ante-nicene-fathers/volume-1/editions/"
            "buffalo-1887/edition.toml",
            f'''
            schema = 1
            record_type = "edition"
            id = "{CONTAINER_EDITION_ID}"
            work_id = "{CONTAINER_WORK_ID}"
            title = "The Apostolic Fathers with Justin Martyr and Irenaeus"
            language = "en"
            publication = "Buffalo, 1887"
            date = "1887"
            editors = ["Alexander Roberts", "James Donaldson", "A. Cleveland Coxe"]
            ''',
        )
        self.write(
            "src/sources/works/ante-nicene-fathers/volume-1/editions/"
            "buffalo-1887/artifacts/plain-text/artifact.toml",
            f'''
            schema = 2
            record_type = "artifact"
            id = "{CONTAINER_ARTIFACT_ID}"
            edition_id = "{CONTAINER_EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Public-domain anthology and transcription"
            rights_jurisdiction = "United States"
            source_url = "https://example.org/anf-volume-1.txt"
            retrieved = "2026-07-23"
            sha256 = "{digest}"
            byte_size = {len(artifact_bytes)}
            path = "{artifact_path}"
            page_count = 7
            indexable = true
            encoding = "utf-8"
            ''',
        )
        self.write(
            "src/sources/works/irenaeus/adversus-haereses/work.toml",
            r'''
            schema = 1
            record_type = "work"
            id = "work.irenaeus.adversus-haereses"
            title = "Adversus haereses"
            responsible = "Irenaeus of Lyons"
            work_type = "patristic-treatise"
            languages = ["grc", "la"]
            locus_pattern = 'book-[0-9]+\.chapter-[0-9]+\.section-[0-9]+'
            ''',
        )
        self.write(
            "src/sources/works/irenaeus/adversus-haereses/editions/"
            "roberts-rambaut-coxe-anf1-1887/edition.toml",
            f'''
            schema = 1
            record_type = "edition"
            id = "{CONSTITUENT_EDITION_ID}"
            work_id = "{CONSTITUENT_WORK_ID}"
            title = "Against Heresies"
            language = "en"
            publication = "Ante-Nicene Fathers, volume 1, Buffalo, 1887"
            date = "1887"
            translators = ["Alexander Roberts", "W. H. Rambaut"]
            editors = ["A. Cleveland Coxe"]
            ''',
        )
        self.write(
            segment_path,
            f'''
            schema = 2
            record_type = "segment"
            id = "{SEGMENT_ID}"
            edition_id = "{CONSTITUENT_EDITION_ID}"
            artifact_id = "{CONTAINER_ARTIFACT_ID}"
            artifact_sha256 = "{digest}"
            segment_type = "constituent-work"
            states = ["acquired", "inspected", "verified"]
            context = "The exact constituent range was checked in the container."
            physical_line_ranges = [[3, 5]]
            artifact_page_ranges = [[3, 5]]
            verified_on = "2026-07-23"
            ''',
        )

        with_segment = SOURCE_LIBRARY.load_library(self.root)
        if with_segment.errors:
            raise AssertionError(with_segment.errors)
        self.write(
            passage_path,
            f'''
            schema = 2
            record_type = "passage"
            id = "{SEGMENT_PASSAGE_ID}"
            edition_id = "{CONSTITUENT_EDITION_ID}"
            segment_id = "{SEGMENT_ID}"
            artifact_sha256 = "{digest}"
            locus = "{SEGMENT_LOCUS}"
            states = ["inspected", "verified"]
            context = "The exact section and its constituent context were checked."
            physical_line_ranges = [[4, 4]]
            artifact_page_ranges = [[4, 4]]
            text = "Irenaeus shared needle."
            transcription_segments = [
              {{ line = 4, text = "Irenaeus shared needle." }},
            ]
            verified_on = "2026-07-23"
            ''',
        )
        with_passage = SOURCE_LIBRARY.load_library(self.root)
        if with_passage.errors:
            raise AssertionError(with_passage.errors)
        passage_fingerprint = SOURCE_LIBRARY.source_fingerprint(
            with_passage, SEGMENT_PASSAGE_ID
        )
        self.write("src/gpt/articles/segment-consumer/main.tex", "Segment consumer\n")
        self.write(
            binding_path,
            f'''
            schema = 2
            record_type = "bindings"
            document = "articles/segment-consumer"

            [[bindings]]
            source_id = "{SEGMENT_PASSAGE_ID}"
            role = "direct-witness"
            states = ["inspected", "verified"]
            verified_on = "2026-07-23"
            source_fingerprint = "{passage_fingerprint}"
            context = "The publication checked the section in its exact container."
            claim_keys = ["irenaeus-shared"]
            ''',
        )
        return {
            "artifact_bytes": artifact_bytes,
            "artifact_digest": digest,
            "artifact_path": artifact_path,
            "segment_path": segment_path,
            "passage_path": passage_path,
            "binding_path": binding_path,
            "passage_fingerprint": passage_fingerprint,
        }

    def test_valid_vertical_fixture_and_validate_cli_summary(self) -> None:
        self.add_valid_vertical_fixture()
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertEqual(library.errors, [])
        self.assertEqual(set(library.records), {
            WORK_ID,
            EDITION_ID,
            ARTIFACT_ID,
            PASSAGE_ID,
            CORPUS_ID,
        })
        self.assertEqual(len(library.bindings), 2)
        self.assertEqual(
            {
                source_id: SOURCE_LIBRARY.source_fingerprint(library, source_id)
                for source_id in (
                    WORK_ID,
                    EDITION_ID,
                    ARTIFACT_ID,
                    PASSAGE_ID,
                    CORPUS_ID,
                )
            },
            {
                WORK_ID: "sha256:85f4d7488fcc33a6e1bcfc11cb114c515b8c3b498cb9384049f170ab9eec1e16",
                EDITION_ID: "sha256:bfa1413ee018fa8e945bef9c38866ff9f42b969d6ab6ccfcd63b14ef0d55f06f",
                ARTIFACT_ID: "sha256:357e092e1ef63806b171f2a9eb3d3aaed27b86f33c8bcd96c021a57c735a3d0d",
                PASSAGE_ID: "sha256:17914e31961b4c5f496343ea257d83045fd5e7009b7b078c83957595a2490524",
                CORPUS_ID: "sha256:3cb2023fe299df1c0e88bb744bb3e87554f5528315c049bb21dfa20400142801",
            },
        )

        result = self.run_cli("validate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout,
            "source-library valid: artifact=1 corpus=1 edition=1 "
            "passage=1 segment=0 work=1 bindings=2\n",
        )

    def test_schema_two_segment_preserves_constituent_identity_and_bounds_search(
        self,
    ) -> None:
        self.add_valid_cross_work_segment_fixture()
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertEqual(library.errors, [])
        self.assertEqual(
            {
                record_id: record.record_type
                for record_id, record in library.records.items()
            },
            {
                CONTAINER_WORK_ID: "work",
                CONTAINER_EDITION_ID: "edition",
                CONTAINER_ARTIFACT_ID: "artifact",
                CONSTITUENT_WORK_ID: "work",
                CONSTITUENT_EDITION_ID: "edition",
                SEGMENT_ID: "segment",
                SEGMENT_PASSAGE_ID: "passage",
            },
        )
        self.assertEqual(
            SOURCE_LIBRARY._work_for_source(
                library, SEGMENT_PASSAGE_ID
            ).record_id,
            CONSTITUENT_WORK_ID,
        )
        self.assertEqual(
            [
                (row["line"], row["text"])
                for row in SOURCE_LIBRARY.search_rows(
                    library, SEGMENT_ID, "needle"
                )
            ],
            [
                (3, "Irenaeus opening needle."),
                (4, "Irenaeus shared needle."),
            ],
        )
        self.assertEqual(
            [
                (row["line"], row["text"])
                for row in SOURCE_LIBRARY.search_rows(
                    library, SEGMENT_PASSAGE_ID, "needle"
                )
            ],
            [(4, "Irenaeus shared needle.")],
        )
        constituent_bindings = SOURCE_LIBRARY.binding_rows(
            library, CONSTITUENT_WORK_ID, SEGMENT_LOCUS
        )
        self.assertEqual(
            [row["document"] for row in constituent_bindings],
            ["articles/segment-consumer"],
        )
        container_impact = SOURCE_LIBRARY.impact_rows(
            library, CONTAINER_ARTIFACT_ID
        )
        self.assertTrue(
            {SEGMENT_ID, SEGMENT_PASSAGE_ID}
            <= {
                row["id"]
                for row in container_impact
                if row["kind"] == "source"
            }
        )
        self.assertEqual(
            [
                row["id"]
                for row in container_impact
                if row["kind"] == "document"
            ],
            ["articles/segment-consumer"],
        )

        result = self.run_cli("validate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "source-library valid: artifact=1 corpus=0 edition=2 "
            "passage=1 segment=1 work=2 bindings=1\n",
        )

    def test_schema_two_source_requires_schema_two_binding_file(self) -> None:
        fixture = self.add_valid_cross_work_segment_fixture()
        binding_path = str(fixture["binding_path"])
        path = self.root / binding_path
        self.write(
            binding_path,
            path.read_text(encoding="utf-8").replace(
                "schema = 2", "schema = 1", 1
            ),
        )

        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertIn(
            "bindings[1] must use schema 2 when naming a schema 2 source",
            "\n".join(library.errors),
        )

    def test_schema_one_does_not_accept_segment_fields_or_records(self) -> None:
        self.add_valid_vertical_fixture()
        passage = self.root / (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/passages/10-6.toml"
        )
        self.write(
            passage.relative_to(self.root).as_posix(),
            passage.read_text(encoding="utf-8")
            + f'segment_id = "{SEGMENT_ID}"\n',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/segments/invalid-v1.toml",
            f'''
            schema = 1
            record_type = "segment"
            id = "{SEGMENT_ID}"
            edition_id = "{EDITION_ID}"
            artifact_id = "{ARTIFACT_ID}"
            artifact_sha256 = "{"0" * 64}"
            segment_type = "constituent-work"
            states = ["cataloged"]
            context = "Invalid schema-version fixture."
            physical_line_ranges = [[1, 1]]
            ''',
        )

        library = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        joined = "\n".join(library.errors)

        self.assertIn("unknown fields: segment_id", joined)
        self.assertIn("segment schema must be integer 2", joined)

    def test_segment_and_segment_passage_ranges_are_exact_and_contained(
        self,
    ) -> None:
        fixture = self.add_valid_cross_work_segment_fixture()
        segment_path = str(fixture["segment_path"])
        passage_path = str(fixture["passage_path"])
        segment_text = (self.root / segment_path).read_text(encoding="utf-8")
        passage_text = (self.root / passage_path).read_text(encoding="utf-8")

        self.write(
            segment_path,
            segment_text.replace(
                "physical_line_ranges = [[3, 5]]",
                "physical_line_ranges = [[true, 1], [0, 1], [5, 4], "
                "[3, 5], [5, 6], [99, 99]]",
            ).replace(
                "artifact_page_ranges = [[3, 5]]",
                "artifact_page_ranges = [[true, 1], [0, 1], [5, 4], "
                "[3, 5], [5, 6], [99, 99]]",
            ),
        )
        malformed = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        malformed_errors = "\n".join(malformed.errors)
        self.assertIn("physical_line_ranges", malformed_errors)
        self.assertIn("artifact_page_ranges", malformed_errors)
        self.assertIn("positive non-boolean integers", malformed_errors)
        self.assertIn("start must not exceed end", malformed_errors)
        self.assertIn("sorted and non-overlapping", malformed_errors)
        self.assertIn("artifact line 7", malformed_errors)
        self.assertIn("artifact page 7", malformed_errors)

        self.write(
            segment_path,
            "\n".join(
                line
                for line in segment_text.splitlines()
                if not line.startswith(
                    ("physical_line_ranges =", "artifact_page_ranges =")
                )
            )
            + "\n",
        )
        unbounded = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        self.assertTrue(
            any(
                "segment" in error
                and "physical_line_ranges or artifact_page_ranges" in error
                for error in unbounded.errors
            ),
            unbounded.errors,
        )

        self.write(segment_path, segment_text)
        self.write(
            passage_path,
            passage_text.replace(
                f'segment_id = "{SEGMENT_ID}"',
                f'artifact_id = "{CONTAINER_ARTIFACT_ID}"\n'
                f'segment_id = "{SEGMENT_ID}"',
            )
            .replace(
                f'artifact_sha256 = "{fixture["artifact_digest"]}"',
                f'artifact_sha256 = "{"0" * 64}"',
            )
            .replace(
                "physical_line_ranges = [[4, 4]]",
                "physical_line_ranges = [[2, 4]]",
            )
            .replace(
                "artifact_page_ranges = [[4, 4]]",
                "artifact_page_ranges = [[4, 6]]",
            ),
        )
        outside = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        outside_errors = "\n".join(outside.errors)
        self.assertIn(
            "schema 2 passage requires exactly one of artifact_id or segment_id",
            outside_errors,
        )
        self.assertIn(
            "artifact_sha256 does not match the controlling artifact",
            outside_errors,
        )
        self.assertTrue(
            any(
                "physical_line_ranges" in error and "segment" in error
                for error in outside.errors
            ),
            outside.errors,
        )
        self.assertTrue(
            any(
                "artifact_page_ranges" in error and "segment" in error
                for error in outside.errors
            ),
            outside.errors,
        )

    def test_segment_parent_mutations_stale_consumers_but_unrelated_segments_do_not(
        self,
    ) -> None:
        fixture = self.add_valid_cross_work_segment_fixture()
        baseline = SOURCE_LIBRARY.load_library(self.root)
        baseline_fingerprint = SOURCE_LIBRARY.source_fingerprint(
            baseline, SEGMENT_PASSAGE_ID
        )
        self.write(
            "src/sources/works/test/unrelated/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.test.unrelated"
            title = "Unrelated constituent"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        self.write(
            "src/sources/works/test/unrelated/editions/test/edition.toml",
            '''
            schema = 1
            record_type = "edition"
            id = "edition.test.unrelated"
            work_id = "work.test.unrelated"
            title = "Unrelated constituent edition"
            language = "en"
            publication = "Test"
            ''',
        )
        self.write(
            "src/sources/works/test/unrelated/editions/test/segments/"
            "unrelated.toml",
            f'''
            schema = 2
            record_type = "segment"
            id = "segment.test.unrelated"
            edition_id = "edition.test.unrelated"
            artifact_id = "{CONTAINER_ARTIFACT_ID}"
            artifact_sha256 = "{fixture["artifact_digest"]}"
            segment_type = "constituent-work"
            states = ["cataloged"]
            context = "A disjoint segment in the same physical container."
            physical_line_ranges = [[6, 7]]
            artifact_page_ranges = [[6, 7]]
            ''',
        )
        with_unrelated = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(with_unrelated.errors, [])
        self.assertEqual(
            SOURCE_LIBRARY.source_fingerprint(
                with_unrelated, SEGMENT_PASSAGE_ID
            ),
            baseline_fingerprint,
        )

        segment_path = str(fixture["segment_path"])
        segment = (self.root / segment_path).read_text(encoding="utf-8")
        self.write(
            segment_path,
            segment.replace(
                "physical_line_ranges = [[3, 5]]",
                "physical_line_ranges = [[2, 5]]",
            ),
        )
        ranged = SOURCE_LIBRARY.load_library(self.root)
        ranged_fingerprint = SOURCE_LIBRARY.source_fingerprint(
            ranged, SEGMENT_PASSAGE_ID
        )
        self.assertNotEqual(ranged_fingerprint, baseline_fingerprint)
        self.assertEqual(
            ranged.errors,
            [
                f'{fixture["binding_path"]}: '
                "bindings[1].source_fingerprint must be "
                f"{ranged_fingerprint!r}"
            ],
        )

        binding_path = str(fixture["binding_path"])
        binding = (self.root / binding_path).read_text(encoding="utf-8")
        self.write(
            binding_path,
            binding.replace(baseline_fingerprint, ranged_fingerprint),
        )
        range_reviewed = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(range_reviewed.errors, [])

        old_bytes = fixture["artifact_bytes"]
        assert isinstance(old_bytes, bytes)
        new_bytes = old_bytes.replace(
            b"needle outside before", b"changed outside segment"
        )
        old_digest = str(fixture["artifact_digest"])
        new_digest = hashlib.sha256(new_bytes).hexdigest()
        artifact_path = str(fixture["artifact_path"])
        self.write(artifact_path, new_bytes)
        artifact_manifest = range_reviewed.records[CONTAINER_ARTIFACT_ID].path
        self.write(
            artifact_manifest.relative_to(self.root).as_posix(),
            artifact_manifest.read_text(encoding="utf-8")
            .replace(old_digest, new_digest)
            .replace(
                f"byte_size = {len(old_bytes)}",
                f"byte_size = {len(new_bytes)}",
            ),
        )
        for manifest_path in (
            segment_path,
            str(fixture["passage_path"]),
            "src/sources/works/test/unrelated/editions/test/segments/"
            "unrelated.toml",
        ):
            manifest = self.root / manifest_path
            self.write(
                manifest_path,
                manifest.read_text(encoding="utf-8").replace(
                    old_digest, new_digest
                ),
            )

        changed = SOURCE_LIBRARY.load_library(self.root)
        changed_fingerprint = SOURCE_LIBRARY.source_fingerprint(
            changed, SEGMENT_PASSAGE_ID
        )
        self.assertNotEqual(changed_fingerprint, ranged_fingerprint)
        self.assertEqual(
            changed.errors,
            [
                f'{fixture["binding_path"]}: '
                "bindings[1].source_fingerprint must be "
                f"{changed_fingerprint!r}"
            ],
        )

    def test_stale_fingerprint_is_reported_and_cli_prints_replacement(self) -> None:
        self.add_valid_vertical_fixture()
        before = SOURCE_LIBRARY.load_library(self.root)
        old_fingerprint = SOURCE_LIBRARY.source_fingerprint(before, PASSAGE_ID)
        artifact_manifest = before.records[ARTIFACT_ID].path
        self.write(
            artifact_manifest.relative_to(self.root).as_posix(),
            artifact_manifest.read_text(encoding="utf-8")
            + 'notes = "Corrected artifact metadata."\n',
        )

        stale = SOURCE_LIBRARY.load_library(self.root)
        new_fingerprint = SOURCE_LIBRARY.source_fingerprint(stale, PASSAGE_ID)
        joined = "\n".join(stale.errors)

        self.assertNotEqual(old_fingerprint, new_fingerprint)
        self.assertIn(
            f"bindings[1].source_fingerprint must be {new_fingerprint!r}",
            joined,
        )

        result = self.run_cli("fingerprint", PASSAGE_ID)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, f"{new_fingerprint}\n")

    def test_shared_passage_change_stales_every_reviewed_consumer(self) -> None:
        self.add_valid_vertical_fixture()
        before = SOURCE_LIBRARY.load_library(self.root)
        old_fingerprint = SOURCE_LIBRARY.source_fingerprint(before, PASSAGE_ID)
        second_document = "articles/shared-source-consumer"
        second_binding_path = (
            "src/gpt/articles/shared-source-consumer/research/source-bindings.toml"
        )
        self.write(f"src/gpt/{second_document}/main.tex", "Second consumer\n")
        self.write(
            second_binding_path,
            f'''
            schema = 1
            record_type = "bindings"
            document = "{second_document}"

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            loci = ["{LOCUS}"]
            role = "textual-control"
            states = ["inspected"]
            source_fingerprint = "{old_fingerprint}"
            context = "A second publication inspected the same shared passage."
            ''',
        )
        with_two_consumers = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(with_two_consumers.errors, [])
        self.assertEqual(
            [
                row["document"]
                for row in SOURCE_LIBRARY.binding_rows(
                    with_two_consumers, PASSAGE_ID
                )
            ],
            [second_document, "theology/demo"],
        )

        passage_manifest = with_two_consumers.records[PASSAGE_ID].path
        self.write(
            passage_manifest.relative_to(self.root).as_posix(),
            passage_manifest.read_text(encoding="utf-8")
            + 'notes = "Corrected shared passage metadata."\n',
        )

        stale = SOURCE_LIBRARY.load_library(self.root)
        new_fingerprint = SOURCE_LIBRARY.source_fingerprint(stale, PASSAGE_ID)
        stale_suffix = (
            f"bindings[1].source_fingerprint must be {new_fingerprint!r}"
        )
        self.assertNotEqual(old_fingerprint, new_fingerprint)
        self.assertEqual(
            stale.errors,
            [
                f"{second_binding_path}: {stale_suffix}",
                "src/gpt/theology/demo/research/source-bindings.toml: "
                f"{stale_suffix}",
            ],
        )

        impact_library = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        self.assertEqual(impact_library.errors, [])
        self.assertEqual(
            {
                row["id"]
                for row in SOURCE_LIBRARY.impact_rows(
                    impact_library, PASSAGE_ID
                )
                if row["kind"] == "document"
            },
            {second_document, "theology/demo"},
        )

        result = self.run_cli("fingerprint", PASSAGE_ID)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, f"{new_fingerprint}\n")

    def test_claude_publication_root_is_validated_alongside_gpt(self) -> None:
        self.add_valid_vertical_fixture()
        before = SOURCE_LIBRARY.load_library(self.root)
        fingerprint = SOURCE_LIBRARY.source_fingerprint(before, PASSAGE_ID)
        self.write("src/claude/theology/demo/main.tex", "Claude demo\n")
        self.write(
            "src/claude/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            loci = ["{LOCUS}"]
            role = "textual-control"
            states = ["inspected"]
            source_fingerprint = "{fingerprint}"
            context = "A second provider inspected the same shared passage."
            ''',
        )

        library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(library.errors, [])
        rows = SOURCE_LIBRARY.binding_rows(library, PASSAGE_ID)
        self.assertEqual(
            [row["document"] for row in rows],
            ["theology/demo", "theology/demo"],
        )
        self.assertEqual(
            sorted(row["path"] for row in rows),
            [
                "src/claude/theology/demo/research/source-bindings.toml",
                "src/gpt/theology/demo/research/source-bindings.toml",
            ],
        )

    def test_claude_binding_errors_cite_claude_relative_document(self) -> None:
        self.add_valid_vertical_fixture()
        self.write("src/claude/theology/demo/main.tex", "Claude demo\n")
        self.write(
            "src/claude/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "claude/theology/demo"

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            loci = ["{LOCUS}"]
            role = "textual-control"
            states = ["cataloged"]
            context = "The document must be provider-root relative."
            ''',
        )

        library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(
            library.errors,
            [
                "src/claude/theology/demo/research/source-bindings.toml: "
                "document must be 'theology/demo' for this path"
            ],
        )

    def test_missing_claude_root_contributes_nothing(self) -> None:
        self.add_valid_vertical_fixture()
        self.assertFalse((self.root / "src/claude").exists())

        library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(library.errors, [])
        self.assertEqual(
            [row["path"] for row in SOURCE_LIBRARY.binding_rows(library, PASSAGE_ID)],
            ["src/gpt/theology/demo/research/source-bindings.toml"],
        )

    def test_all_publication_roots_missing_is_one_error(self) -> None:
        (self.root / "src/gpt").rmdir()

        library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(
            library.errors,
            ["src/gpt, src/claude: no publication root exists"],
        )

    def test_common_typesetting_tree_is_ignored(self) -> None:
        self.add_valid_vertical_fixture()
        self.write("src/common/preamble.tex", "% shared preamble\n")

        library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(library.errors, [])
        self.assertNotIn(
            "src/common",
            "\n".join(library.errors),
        )

    def test_uses_follows_source_ancestry_and_filters_exact_loci(self) -> None:
        self.add_valid_vertical_fixture()
        library = SOURCE_LIBRARY.load_library(self.root)

        work_rows = SOURCE_LIBRARY.binding_rows(library, WORK_ID)
        self.assertEqual(
            [(row["source_id"], row["role"]) for row in work_rows],
            [
                (CORPUS_ID, "negative-search"),
                (PASSAGE_ID, "direct-witness"),
            ],
        )
        self.assertEqual(
            SOURCE_LIBRARY.binding_rows(library, WORK_ID, LOCUS),
            [next(row for row in work_rows if row["source_id"] == PASSAGE_ID)],
        )
        self.assertEqual(
            [row["source_id"] for row in SOURCE_LIBRARY.binding_rows(library, ARTIFACT_ID)],
            [CORPUS_ID, PASSAGE_ID],
        )
        with self.assertRaises(KeyError):
            SOURCE_LIBRARY.binding_rows(library, "work.unknown")

        result = self.run_cli("uses", WORK_ID, "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), work_rows)

    def test_impact_includes_dependent_records_and_bound_documents(self) -> None:
        self.add_valid_vertical_fixture()
        library = SOURCE_LIBRARY.load_library(self.root)

        rows = SOURCE_LIBRARY.impact_rows(library, WORK_ID)
        self.assertEqual(
            {(row["id"], row["type"]) for row in rows if row["kind"] == "source"},
            {
                (EDITION_ID, "edition"),
                (ARTIFACT_ID, "artifact"),
                (PASSAGE_ID, "passage"),
                (CORPUS_ID, "corpus"),
            },
        )
        self.assertEqual(
            [(row["id"], row["type"]) for row in rows if row["kind"] == "document"],
            [
                ("theology/demo", "direct-witness"),
                ("theology/demo", "negative-search"),
            ],
        )
        self.assertEqual(
            rows,
            sorted(
                rows,
                key=lambda row: (
                    row["kind"],
                    row["id"],
                    row["type"],
                    row.get("source_id", ""),
                    tuple(row.get("loci", [])),
                    tuple(row.get("states", [])),
                    row["path"],
                ),
            ),
        )
        document_rows = [row for row in rows if row["kind"] == "document"]
        self.assertTrue(all("source_id" in row for row in document_rows))
        self.assertTrue(all("loci" in row for row in document_rows))
        self.assertTrue(all("states" in row for row in document_rows))

        locus_rows = SOURCE_LIBRARY.impact_rows(library, WORK_ID, LOCUS)
        self.assertEqual(
            [(row["id"], row["type"]) for row in locus_rows if row["kind"] == "document"],
            [("theology/demo", "direct-witness")],
        )

    def test_search_is_bounded_by_registered_text_artifacts(self) -> None:
        self.add_valid_vertical_fixture()
        image = b"\x89PNG\r\n"
        image_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/image/illustration.png"
        )
        self.write(image_path, image)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/image/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.image"
            edition_id = "{EDITION_ID}"
            artifact_type = "facsimile-image"
            media_type = "image/png"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Public-domain scan"
            rights_jurisdiction = "United States"
            source_url = "https://example.org/image.png"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(image).hexdigest()}"
            byte_size = {len(image)}
            path = "{image_path}"
            indexable = false
            ''',
        )
        hidden = b"sacrifice in a deliberately non-indexable derivative\n"
        hidden_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/hidden/hidden.txt"
        )
        self.write(hidden_path, hidden)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/hidden/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.hidden"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Public-domain transcription"
            rights_jurisdiction = "United States"
            source_url = "https://example.org/hidden.txt"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(hidden).hexdigest()}"
            byte_size = {len(hidden)}
            path = "{hidden_path}"
            indexable = false
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/remote/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.remote"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Remote host rights require review"
            source_url = "https://example.org/remote.txt"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(library.errors, [])

        insensitive = SOURCE_LIBRARY.search_rows(library, WORK_ID, "sacrifice")
        self.assertEqual(
            [(row["artifact_id"], row["line"], row["text"]) for row in insensitive],
            [
                (ARTIFACT_ID, 2, "The City offers Sacrifice."),
                (ARTIFACT_ID, 3, "A second SACRIFICE witness."),
            ],
        )
        sensitive = SOURCE_LIBRARY.search_rows(
            library, WORK_ID, "Sacrifice", case_sensitive=True
        )
        self.assertEqual([row["line"] for row in sensitive], [2])
        passage_rows = SOURCE_LIBRARY.search_rows(
            library, PASSAGE_ID, "Sacrifice", case_sensitive=True
        )
        self.assertEqual(
            [(row["line"], row["text"]) for row in passage_rows],
            [(2, "The City offers Sacrifice.")],
        )
        self.assertEqual(
            SOURCE_LIBRARY.search_rows(
                library, PASSAGE_ID, "SACRIFICE", case_sensitive=True
            ),
            [],
        )
        self.assertEqual(SOURCE_LIBRARY.search_rows(library, CORPUS_ID, "absent"), [])

        result = self.run_cli("search", WORK_ID, "sacrifice", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), insensitive)
        count = self.run_cli("search", WORK_ID, "sacrifice", "--count")
        self.assertEqual(count.returncode, 0, count.stderr)
        self.assertEqual(count.stdout, "2\n")

    def test_search_supports_tei_without_expanding_a_corpus_snapshot(self) -> None:
        self.add_valid_vertical_fixture()
        tei = b'<TEI><text><p>pax omnium rerum</p></text></TEI>\n'
        tei_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/tei/sample.xml"
        )
        self.write(tei_path, tei)
        tei_id = "artifact.augustine.de-civitate-dei.npnf-dods.tei"
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/tei/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "{tei_id}"
            edition_id = "{EDITION_ID}"
            artifact_type = "tei-xml"
            media_type = "application/tei+xml"
            storage = "tracked"
            rights_status = "licensed"
            rights_basis = "Test license"
            source_url = "https://example.org/sample.xml"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(tei).hexdigest()}"
            byte_size = {len(tei)}
            path = "{tei_path}"
            indexable = true
            encoding = "utf-8"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertEqual(library.errors, [])
        self.assertEqual(
            [row["artifact_id"] for row in SOURCE_LIBRARY.search_rows(library, tei_id, "pax")],
            [tei_id],
        )
        self.assertEqual(SOURCE_LIBRARY.search_rows(library, CORPUS_ID, "pax"), [])

    def test_negative_search_rejects_an_xml_search_representation(self) -> None:
        self.add_valid_vertical_fixture()
        tei = b'<TEI><text><p>pax <hi>omnium</hi> rerum</p></text></TEI>\n'
        tei_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/negative-tei/sample.xml"
        )
        tei_id = "artifact.augustine.de-civitate-dei.npnf-dods.negative-tei"
        self.write(tei_path, tei)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/negative-tei/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "{tei_id}"
            edition_id = "{EDITION_ID}"
            artifact_type = "tei-xml"
            media_type = "application/tei+xml"
            storage = "tracked"
            rights_status = "licensed"
            rights_basis = "Test license"
            source_url = "https://example.org/negative-sample.xml"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(tei).hexdigest()}"
            byte_size = {len(tei)}
            path = "{tei_path}"
            indexable = true
            encoding = "utf-8"
            ''',
        )
        with_tei = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(with_tei.errors, [])
        tei_fingerprint = SOURCE_LIBRARY.source_fingerprint(with_tei, tei_id)
        self.write(
            "src/gpt/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{tei_id}"
            role = "negative-search"
            states = ["searched"]
            context = "Raw XML cannot support a content-level negative search."
            search_scope = "The exact TEI XML serialization."
            searched_on = "2026-07-22"
            search_mode = "raw-line-literal-casefold-v1"
            query = "absent phrase"
            method = "Built-in casefolded physical-line literal search."
            matching_line_count = 0
            source_fingerprint = "{tei_fingerprint}"
            ''',
        )

        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertTrue(
            any(
                "negative-search requires text/plain search representations" in error
                for error in library.errors
            ),
            library.errors,
        )

    def test_search_rejects_empty_boundaries_queries_and_changed_files(self) -> None:
        self.add_valid_vertical_fixture()
        self.write(
            "src/sources/works/test/empty/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.empty"
            title = "Empty boundary"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(library.errors, [])

        with self.assertRaisesRegex(
            SOURCE_LIBRARY.SourceLibraryQueryError, "non-whitespace"
        ):
            SOURCE_LIBRARY.search_rows(library, WORK_ID, "   ")
        with self.assertRaisesRegex(
            SOURCE_LIBRARY.SourceLibraryQueryError, "must not contain a line break"
        ):
            SOURCE_LIBRARY.search_rows(library, WORK_ID, "two\nlines")
        with self.assertRaisesRegex(
            SOURCE_LIBRARY.SourceLibraryQueryError, "no indexable"
        ):
            SOURCE_LIBRARY.search_rows(library, "work.empty", "needle")

        result = self.run_cli("search", WORK_ID, "   ")
        self.assertEqual(result.returncode, 1)
        self.assertIn("search query must contain non-whitespace text", result.stderr)

        artifact = library.records[ARTIFACT_ID]
        artifact_path = self.root / artifact.data["path"]
        artifact_path.write_text("changed but valid UTF-8\n", encoding="utf-8")
        with self.assertRaisesRegex(
            SOURCE_LIBRARY.SourceLibraryQueryError, "changed from its manifest"
        ):
            SOURCE_LIBRARY.search_rows(library, ARTIFACT_ID, "changed")

        artifact_path.unlink()
        with self.assertRaisesRegex(
            SOURCE_LIBRARY.SourceLibraryQueryError, "unavailable"
        ):
            SOURCE_LIBRARY.search_rows(library, ARTIFACT_ID, "needle")

    def test_indexable_artifact_must_be_readable_utf8(self) -> None:
        self.add_valid_vertical_fixture()
        invalid = b"\xff\xfe\x00\x00"
        path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/invalid-utf8/invalid.txt"
        )
        self.write(path, invalid)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/invalid-utf8/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.invalid-utf8"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "licensed"
            rights_basis = "Test license"
            provenance = "Test fixture"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(invalid).hexdigest()}"
            byte_size = {len(invalid)}
            path = "{path}"
            indexable = true
            encoding = "utf-8"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertTrue(
            any("indexable artifact is not readable UTF-8" in error for error in library.errors),
            library.errors,
        )

    def test_malformed_toml_and_record_shape_errors_are_collected(self) -> None:
        self.write(
            "src/sources/works/test/broken/work.toml",
            'schema = 1\ntitle = "unterminated\n',
        )
        self.write(
            "src/sources/works/test/bad-shape/work.toml",
            '''
            schema = 2
            record_type = "work"
            id = "work.bad-shape"
            responsible = "Nobody"
            work_type = "Bad Shape"
            unexpected = "value"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertTrue(any("broken/work.toml: cannot parse TOML" in error for error in library.errors))
        self.assertIn(
            "src/sources/works/test/bad-shape/work.toml: schema must be integer 1",
            library.errors,
        )
        self.assertIn(
            "src/sources/works/test/bad-shape/work.toml: unknown fields: unexpected",
            library.errors,
        )
        self.assertIn(
            "src/sources/works/test/bad-shape/work.toml: missing required fields: title",
            library.errors,
        )
        self.assertIn(
            "src/sources/works/test/bad-shape/work.toml: work_type must be lowercase kebab-case",
            library.errors,
        )

    def test_only_authoritative_manifests_are_loaded_and_paths_are_canonical(self) -> None:
        self.write(
            "src/sources/inventories/legacy-occurrences.toml",
            'this is intentionally not valid TOML = "',
        )
        self.write(
            "src/sources/works/test/misplaced.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.misplaced"
            title = "Misplaced work"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertEqual(library.records, {})
        self.assertEqual(
            library.errors,
            [
                "src/sources/works/test/misplaced.toml: "
                "TOML record is not at a canonical manifest path"
            ],
        )

    def test_source_tree_rejects_every_unowned_file(self) -> None:
        self.add_valid_vertical_fixture()
        rogue_paths = (
            "src/sources/rogue.pdf",
            "src/sources/works/augustine/de-civitate-dei/rogue.pdf",
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/rogue.pdf",
            "src/sources/corpora/nested/ignored.toml",
        )
        for path in rogue_paths:
            self.write(path, b"unowned\n")
        self.write(
            "src/sources/inventories/audit.toml",
            'inventory_format = "reserved and intentionally not a source manifest"\n',
        )
        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        for path in rogue_paths:
            self.assertIn(
                f"{path}: file is outside the source-library schema", joined
            )
        self.assertNotIn("inventories/audit.toml", joined)

    def test_invalid_and_duplicate_ids_are_rejected_deterministically(self) -> None:
        work = '''
            schema = 1
            record_type = "work"
            id = "work.duplicate"
            title = "Duplicate"
            responsible = "Test"
            work_type = "test-work"
        '''
        self.write("src/sources/works/test/first/work.toml", work)
        self.write("src/sources/works/test/second/work.toml", work)
        self.write(
            "src/sources/works/test/invalid/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "Work.Invalid"
            title = "Invalid"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertIn(
            "src/sources/works/test/second/work.toml: duplicate id work.duplicate; "
            "first declared in src/sources/works/test/first/work.toml",
            library.errors,
        )
        self.assertIn(
            "src/sources/works/test/invalid/work.toml: id must contain lowercase letters, digits, dots, or hyphens",
            library.errors,
        )
        self.assertEqual(library.errors, sorted(library.errors))

    def test_nonstring_record_type_is_a_structured_validation_error(self) -> None:
        self.write(
            "src/sources/works/test/wrong-type/work.toml",
            '''
            schema = 1
            record_type = ["work"]
            id = "work.wrong-type"
            title = "Wrong type"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        try:
            library = SOURCE_LIBRARY.load_library(self.root)
        except TypeError as error:
            self.fail(f"validator crashed on a TOML type error: {error}")
        self.assertTrue(
            any("record_type must be one of" in error for error in library.errors),
            library.errors,
        )

    def test_boolean_schema_versions_are_rejected(self) -> None:
        self.write(
            "src/sources/works/test/boolean/work.toml",
            '''
            schema = true
            record_type = "work"
            id = "work.boolean"
            title = "Boolean schema"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        self.write("src/gpt/theology/boolean/main.tex", "Demo\n")
        self.write(
            "src/gpt/theology/boolean/research/source-bindings.toml",
            '''
            schema = true
            record_type = "bindings"
            document = "theology/boolean"

            [[bindings]]
            source_id = "work.boolean"
            role = "lead"
            states = ["cataloged"]
            context = "Test"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertEqual(
            sum("schema must be integer 1" in error for error in library.errors),
            2,
        )

    def test_nested_records_must_match_their_physical_owners(self) -> None:
        self.add_valid_vertical_fixture()
        self.write(
            "src/sources/works/test/other/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.other"
            title = "Other work"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        self.write(
            "src/sources/works/test/other/editions/other/edition.toml",
            '''
            schema = 1
            record_type = "edition"
            id = "edition.other"
            work_id = "work.other"
            title = "Other edition"
            language = "en"
            publication = "Test"
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "cross/edition.toml",
            '''
            schema = 1
            record_type = "edition"
            id = "edition.cross"
            work_id = "work.other"
            title = "Cross-wired edition"
            language = "en"
            publication = "Test"
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/cross/artifact.toml",
            '''
            schema = 1
            record_type = "artifact"
            id = "artifact.cross"
            edition_id = "edition.other"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Test"
            source_url = "https://example.org/cross"
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/passages/cross.toml",
            '''
            schema = 1
            record_type = "passage"
            id = "passage.cross"
            edition_id = "edition.augustine.de-civitate-dei.npnf-dods"
            artifact_id = "artifact.cross"
            locus = "book-10.chapter-6"
            states = ["cataloged"]
            context = "Test"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        self.assertIn("work_id must match enclosing work", joined)
        self.assertIn("edition_id must match enclosing edition", joined)
        self.assertIn("artifact_id must belong to the passage edition", joined)

    def test_relationships_require_existing_records_of_the_right_type(self) -> None:
        self.write(
            "src/sources/works/test/good/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.good"
            title = "Good work"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        self.write(
            "src/sources/corpora/parent.toml",
            '''
            schema = 1
            record_type = "corpus"
            id = "corpus.parent"
            title = "Parent corpus"
            members = ["work.good"]
            snapshot = "test-snapshot"
            scope = "One work."
            ''',
        )
        self.write(
            "src/sources/works/test/good/editions/wrong/edition.toml",
            '''
            schema = 1
            record_type = "edition"
            id = "edition.wrong-parent"
            work_id = "corpus.parent"
            title = "Wrong parent"
            language = "en"
            publication = "Test"
            ''',
        )
        self.write(
            "src/sources/works/test/good/editions/unknown/edition.toml",
            '''
            schema = 1
            record_type = "edition"
            id = "edition.unknown-parent"
            work_id = "work.missing"
            title = "Unknown parent"
            language = "en"
            publication = "Test"
            ''',
        )
        self.write(
            "src/sources/works/test/good/editions/wrong/"
            "artifacts/wrong/artifact.toml",
            '''
            schema = 1
            record_type = "artifact"
            id = "artifact.wrong-parent"
            edition_id = "work.good"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Test"
            source_url = "https://example.org/source"
            derived_from = "work.good"
            ''',
        )
        self.write(
            "src/sources/works/test/good/editions/wrong/passages/wrong.toml",
            '''
            schema = 1
            record_type = "passage"
            id = "passage.wrong-parent"
            edition_id = "work.good"
            artifact_id = "corpus.parent"
            locus = "1"
            states = ["cataloged"]
            context = "Test context"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        joined = "\n".join(library.errors)
        self.assertIn("references unknown source id: work.missing", joined)
        self.assertIn("work_id must reference a work record", joined)
        self.assertIn("edition_id must reference an edition record", joined)
        self.assertIn("derived_from must reference an artifact record", joined)
        self.assertIn("artifact_id must reference an artifact record", joined)

    def test_derived_artifact_requires_an_exactly_hashed_parent(self) -> None:
        self.add_valid_vertical_fixture()
        artifact_root = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts"
        )
        parent_id = "artifact.augustine.de-civitate-dei.npnf-dods.unhashed-parent"
        self.write(
            f"{artifact_root}/unhashed-parent/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "{parent_id}"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Test"
            source_url = "https://example.org/unhashed-parent.txt"
            ''',
        )
        self.write(
            f"{artifact_root}/derived-from-unhashed/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.derived-unhashed"
            edition_id = "{EDITION_ID}"
            artifact_type = "normalized-text"
            media_type = "text/plain"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Test"
            source_url = "https://example.org/derived-unhashed.txt"
            derived_from = "{parent_id}"
            transformation = "Test normalization"
            ''',
        )

        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertTrue(
            any(
                "derived_from artifact must have an exact sha256" in error
                for error in library.errors
            ),
            library.errors,
        )

    def test_tracked_artifact_checks_hash_size_rights_and_safe_paths(self) -> None:
        self.add_valid_vertical_fixture()
        bad_bytes = b"actual artifact bytes\n"
        bad_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/bad/bad.txt"
        )
        self.write(bad_path, bad_bytes)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/bad/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.bad"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "restricted"
            rights_basis = "No redistribution permission"
            provenance = "Test fixture"
            retrieved = "2026-07-22"
            sha256 = "{'0' * 64}"
            byte_size = 999
            path = "{bad_path}"
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/traversal/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.traversal"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Test"
            rights_jurisdiction = "United States"
            provenance = "Test fixture"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(bad_bytes).hexdigest()}"
            byte_size = {len(bad_bytes)}
            path = "../outside.txt"
            ''',
        )
        outside = self.write("outside.txt", bad_bytes)
        link = (
            self.root
            / "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/symlink/link.txt"
        )
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(outside)
        link_path = link.relative_to(self.root).as_posix()
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/symlink/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.symlink"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Test"
            rights_jurisdiction = "United States"
            provenance = "Test fixture"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(bad_bytes).hexdigest()}"
            byte_size = {len(bad_bytes)}
            path = "{link_path}"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        self.assertIn("tracked artifact requires an affirmative distribution rights_status", joined)
        self.assertIn(f"sha256 mismatch for {bad_path}", joined)
        self.assertIn(f"byte_size mismatch for {bad_path}", joined)
        self.assertIn("artifact path must be repository-relative without '..'", joined)
        self.assertIn("artifact path must not be a symbolic link", joined)

    def test_storage_dispositions_control_paths_and_remote_locations(self) -> None:
        self.add_valid_vertical_fixture()
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/remote-invalid/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.remote-invalid"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Rights unresolved"
            path = "src/sources/should-not-be-here.txt"
            sha256 = "0000000000000000000000000000000000000000000000000000000000000000"
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/restricted-valid/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.restricted"
            edition_id = "{EDITION_ID}"
            artifact_type = "book-scan"
            media_type = "application/pdf"
            storage = "restricted"
            rights_status = "restricted"
            rights_basis = "Local consultation only"
            notes = "No source bytes are stored."
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/local-url/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.augustine.de-civitate-dei.npnf-dods.local-url"
            edition_id = "{EDITION_ID}"
            artifact_type = "web-response"
            media_type = "text/html"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Test"
            source_url = "http://user:secret@localhost/private"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        self.assertIn("remote artifact must not declare a tracked path", joined)
        self.assertIn("remote artifact requires source_url", joined)
        self.assertIn("hashed artifact requires retrieved ISO date", joined)
        self.assertIn("source_url must be a public http(s) URL without credentials", joined)
        self.assertFalse(any("restricted-valid.toml" in error for error in library.errors))

    def test_artifact_payloads_have_one_manifest_owner(self) -> None:
        artifact_bytes = self.add_valid_vertical_fixture()
        main_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/plain-text/city-of-god.txt"
        )
        unmanifested = (
            self.root
            / "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/plain-text/unmanifested.pdf"
        )
        unmanifested.write_bytes(b"%PDF-unregistered\n")

        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/cross-pointer/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.cross-pointer"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Test"
            rights_jurisdiction = "United States"
            provenance = "Test fixture"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(artifact_bytes).hexdigest()}"
            byte_size = {len(artifact_bytes)}
            path = "{main_path}"
            ''',
        )

        duplicate_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/duplicate/duplicate.txt"
        )
        self.write(duplicate_path, artifact_bytes)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/duplicate/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.duplicate"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Test"
            rights_jurisdiction = "United States"
            provenance = "Test fixture"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(artifact_bytes).hexdigest()}"
            byte_size = {len(artifact_bytes)}
            path = "{duplicate_path}"
            ''',
        )

        toml_bytes = b'payload = "not a source manifest"\n'
        toml_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/toml-payload/payload.toml"
        )
        self.write(toml_path, toml_bytes)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/toml-payload/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "artifact.toml-payload"
            edition_id = "{EDITION_ID}"
            artifact_type = "plain-text"
            media_type = "text/plain"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Test"
            rights_jurisdiction = "United States"
            provenance = "Test fixture"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(toml_bytes).hexdigest()}"
            byte_size = {len(toml_bytes)}
            path = "{toml_path}"
            indexable = false
            ''',
        )

        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        self.assertIn("artifact path must resolve beneath its artifact manifest directory", joined)
        self.assertIn(f"tracked sha256 is already owned by {ARTIFACT_ID}", joined)
        self.assertIn("unmanifested.pdf: artifact payload is not declared", joined)
        self.assertIn("artifact.toml-payload", library.records)
        self.assertNotIn("payload.toml: cannot parse TOML", joined)

    def test_bindings_validate_owner_target_locus_values_and_duplicates(self) -> None:
        self.add_valid_vertical_fixture()
        bindings_path = "src/gpt/theology/demo/research/source-bindings.toml"
        valid_table = f'''
            source_id = "{PASSAGE_ID}"
            loci = ["{LOCUS}"]
            role = "direct-witness"
            states = ["verified"]
            verified_on = "2026-07-22"
            context = "Checked context."
            claim_keys = ["claim-one"]
        '''
        self.write(
            bindings_path,
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/not-demo"

            [[bindings]]
            {valid_table}

            [[bindings]]
            {valid_table}

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            loci = ["not-a-valid-locus"]
            role = "not-a-role"
            states = ["verified", "verified", "imagined"]
            verified_on = "2026-07-22"
            context = ""
            claim_keys = []
            ''',
        )
        self.write(
            "src/gpt/theology/missing/research/source-bindings.toml",
            '''
            schema = 1
            record_type = "bindings"
            document = "theology/missing"

            [[bindings]]
            source_id = "work.not-registered"
            role = "lead"
            states = ["cataloged"]
            context = "Unresolved lead."
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        self.assertIn("document must be 'theology/demo' for this path", joined)
        self.assertIn("bindings[2] exactly duplicates an earlier binding", joined)
        self.assertIn("bindings[3].role must be one of", joined)
        self.assertIn("bindings[3].states has invalid values: imagined", joined)
        self.assertIn("bindings[3].states contains duplicates", joined)
        self.assertIn("bindings[3].context must be a nonempty string", joined)
        self.assertIn("bindings[3].claim_keys must be a nonempty string array", joined)
        self.assertIn(
            f"bindings[3] locus does not match {WORK_ID}: not-a-valid-locus",
            joined,
        )
        self.assertIn("document has no main.tex: theology/missing", joined)
        self.assertIn("references unknown source id: work.not-registered", joined)

    def test_inspected_and_verified_bindings_require_hashed_artifacts(self) -> None:
        self.add_valid_vertical_fixture()
        remote_id = "artifact.augustine.de-civitate-dei.npnf-dods.unhashed-remote"
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/unhashed-remote/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "{remote_id}"
            edition_id = "{EDITION_ID}"
            artifact_type = "web-text"
            media_type = "text/plain"
            storage = "remote"
            rights_status = "unresolved"
            rights_basis = "Test"
            source_url = "https://example.org/unhashed-remote.txt"
            ''',
        )
        with_remote = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(with_remote.errors, [])
        remote_fingerprint = SOURCE_LIBRARY.source_fingerprint(with_remote, remote_id)
        self.write(
            "src/gpt/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{remote_id}"
            role = "context"
            states = ["inspected"]
            context = "An unhashed remote artifact cannot be pinned as inspected."
            source_fingerprint = "{remote_fingerprint}"

            [[bindings]]
            source_id = "{remote_id}"
            role = "bibliographic"
            states = ["verified"]
            verified_on = "2026-07-22"
            context = "An unhashed remote artifact cannot be pinned as verified."
            source_fingerprint = "{remote_fingerprint}"
            ''',
        )

        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        self.assertIn(
            "bindings[1] inspected state requires exact hashed artifacts", joined
        )
        self.assertIn(
            "bindings[2] verified state requires exact hashed artifacts", joined
        )

    def test_search_bindings_require_a_complete_exact_boundary(self) -> None:
        self.add_valid_vertical_fixture()
        self.write(
            "src/gpt/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "negative-search"
            states = ["cataloged"]
            context = "Missing searched state."

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "lead"
            states = ["searched"]
            context = "Missing search metadata."

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "lead"
            states = ["cataloged"]
            context = "Search metadata without state."
            query = "test"

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            loci = [["{LOCUS}"]]
            role = ["direct-witness"]
            states = [["verified"]]
            context = "Nested arrays must report errors, not crash."

            [[bindings]]
            source_id = "{WORK_ID}"
            role = "negative-search"
            states = ["searched"]
            context = "A work identity is not an exact search boundary."
            search_scope = "An unversioned work identity."
            searched_on = "not-a-date"
            search_mode = "raw-line-literal-casefold-v1"
            query = "test"
            method = "literal"
            matching_line_count = 0

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            role = "direct-witness"
            states = ["verified"]
            context = "Verified state lacks a check date."

            [[bindings]]
            source_id = "{ARTIFACT_ID}"
            role = "lead"
            states = ["indexed"]
            context = "Schema version 1 has no index receipt."
            ''',
        )
        try:
            library = SOURCE_LIBRARY.load_library(self.root)
        except TypeError as error:
            self.fail(f"validator crashed on nested binding arrays: {error}")
        joined = "\n".join(library.errors)

        self.assertIn("negative-search role requires the searched state", joined)
        self.assertIn(
            "searched state requires: matching_line_count, method, query, search_mode, search_scope, searched_on",
            joined,
        )
        self.assertIn("search fields require the searched state", joined)
        self.assertIn("bindings[4].loci must be a nonempty string array", joined)
        self.assertIn("bindings[4].role must be one of", joined)
        self.assertIn("bindings[4].states must be a nonempty string array", joined)
        self.assertIn("bindings[5].searched_on must be an ISO date", joined)
        self.assertIn(
            "bindings[5] searched source must be an exact artifact, ranged passage, or corpus",
            joined,
        )
        self.assertIn("bindings[6] verified state requires verified_on ISO date", joined)
        self.assertIn("bindings[7].states has invalid values: indexed", joined)

    def test_distinct_corpus_queries_are_not_duplicate_bindings(self) -> None:
        self.add_valid_vertical_fixture()
        before = SOURCE_LIBRARY.load_library(self.root)
        corpus_fingerprint = SOURCE_LIBRARY.source_fingerprint(before, CORPUS_ID)
        self.write(
            "src/gpt/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "negative-search"
            states = ["searched"]
            context = "First bounded query."
            search_scope = "The exact one-artifact fixture corpus."
            searched_on = "2026-07-22"
            search_mode = "raw-line-literal-casefold-v1"
            query = "first phrase"
            method = "Built-in casefolded physical-line literal search."
            matching_line_count = 0
            source_fingerprint = "{corpus_fingerprint}"

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "negative-search"
            states = ["searched"]
            context = "Second bounded query."
            search_scope = "The exact one-artifact fixture corpus."
            searched_on = "2026-07-22"
            search_mode = "raw-line-literal-casefold-v1"
            query = "second phrase"
            method = "Built-in casefolded physical-line literal search."
            matching_line_count = 0
            source_fingerprint = "{corpus_fingerprint}"
            ''',
        )
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertEqual(library.errors, [])
        self.assertEqual(len(library.bindings), 2)

    def test_search_receipts_replay_counts_and_negative_requires_zero(self) -> None:
        self.add_valid_vertical_fixture()
        before = SOURCE_LIBRARY.load_library(self.root)
        corpus_fingerprint = SOURCE_LIBRARY.source_fingerprint(before, CORPUS_ID)
        self.write(
            "src/gpt/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "lead"
            states = ["searched"]
            context = "The recorded count is intentionally stale."
            search_scope = "The exact one-artifact fixture corpus."
            searched_on = "2026-07-22"
            search_mode = "raw-line-literal-casefold-v1"
            query = "sacrifice"
            method = "Built-in casefolded physical-line literal search."
            matching_line_count = 1
            source_fingerprint = "{corpus_fingerprint}"

            [[bindings]]
            source_id = "{CORPUS_ID}"
            role = "negative-search"
            states = ["searched"]
            context = "A negative role cannot retain positive matching lines."
            search_scope = "The exact one-artifact fixture corpus."
            searched_on = "2026-07-22"
            search_mode = "raw-line-literal-casefold-v1"
            query = "sacrifice"
            method = "Built-in casefolded physical-line literal search."
            matching_line_count = 2
            source_fingerprint = "{corpus_fingerprint}"
            ''',
        )

        library = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(library.errors)

        self.assertIn(
            "bindings[1].matching_line_count must be 2 for the exact search", joined
        )
        self.assertIn(
            "bindings[2].negative-search role requires matching_line_count = 0",
            joined,
        )

    def test_related_works_do_not_create_false_dependency_ancestry(self) -> None:
        self.write(
            "src/sources/works/test/cycle-a/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.cycle-a"
            title = "Cycle A"
            responsible = "Test"
            work_type = "test-work"
            relations = ["work.cycle-b"]
            ''',
        )
        self.write(
            "src/sources/works/test/cycle-b/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.cycle-b"
            title = "Cycle B"
            responsible = "Test"
            work_type = "test-work"
            relations = ["work.cycle-a"]
            ''',
        )
        first = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(first.errors, [])
        self.assertEqual(SOURCE_LIBRARY.impact_rows(first, "work.cycle-a"), [])
        self.assertEqual(SOURCE_LIBRARY.impact_rows(first, "work.cycle-b"), [])

    def test_dependency_cycles_are_reported_without_recursion(self) -> None:
        self.write(
            "src/sources/works/test/cycle/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.cycle"
            title = "Cycle"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        self.write(
            "src/sources/works/test/cycle/editions/test/edition.toml",
            '''
            schema = 1
            record_type = "edition"
            id = "edition.cycle.test"
            work_id = "work.cycle"
            title = "Cycle edition"
            language = "en"
            publication = "Test"
            ''',
        )
        for name, other in (("a", "b"), ("b", "a")):
            self.write(
                "src/sources/works/test/cycle/editions/test/artifacts/"
                f"{name}/artifact.toml",
                f'''
                schema = 1
                record_type = "artifact"
                id = "artifact.cycle.test.{name}"
                edition_id = "edition.cycle.test"
                artifact_type = "plain-text"
                media_type = "text/plain"
                storage = "remote"
                rights_status = "unresolved"
                rights_basis = "Test"
                source_url = "https://example.org/{name}"
                derived_from = "artifact.cycle.test.{other}"
                transformation = "Test cycle"
                ''',
            )
        first = SOURCE_LIBRARY.load_library(self.root)
        second = SOURCE_LIBRARY.load_library(self.root)
        cycle_errors = [error for error in first.errors if "source dependency cycle" in error]

        self.assertEqual(first.errors, second.errors)
        self.assertEqual(len(cycle_errors), 1)
        self.assertIn("artifact.cycle.test.a", cycle_errors[0])
        self.assertIn("artifact.cycle.test.b", cycle_errors[0])

    def test_deep_dependency_graph_fingerprint_and_cycle_walk_are_iterative(self) -> None:
        library = SOURCE_LIBRARY.Library(
            root=self.root,
            source_root=self.root / "src/sources",
            publication_roots=[self.root / "src/gpt"],
        )
        library.records["work.deep"] = SOURCE_LIBRARY.Record(
            path=self.root / "work.toml",
            record_type="work",
            record_id="work.deep",
            data={"schema": 1, "record_type": "work", "id": "work.deep"},
        )
        library.records["edition.deep"] = SOURCE_LIBRARY.Record(
            path=self.root / "edition.toml",
            record_type="edition",
            record_id="edition.deep",
            data={
                "schema": 1,
                "record_type": "edition",
                "id": "edition.deep",
                "work_id": "work.deep",
            },
        )
        depth = 1_500
        for ordinal in range(depth):
            artifact_id = f"artifact.deep.{ordinal:04d}"
            data = {
                "schema": 1,
                "record_type": "artifact",
                "id": artifact_id,
                "edition_id": "edition.deep",
            }
            if ordinal + 1 < depth:
                data["derived_from"] = f"artifact.deep.{ordinal + 1:04d}"
            library.records[artifact_id] = SOURCE_LIBRARY.Record(
                path=self.root / f"artifact-{ordinal:04d}.toml",
                record_type="artifact",
                record_id=artifact_id,
                data=data,
            )

        try:
            fingerprint = SOURCE_LIBRARY.source_fingerprint(
                library, "artifact.deep.0000"
            )
            SOURCE_LIBRARY._validate_cycles(library)
        except RecursionError as error:
            self.fail(f"deep acyclic graph recursed: {error}")
        self.assertRegex(fingerprint, r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(library.errors, [])

        last_id = f"artifact.deep.{depth - 1:04d}"
        last = library.records[last_id]
        library.records[last_id] = SOURCE_LIBRARY.Record(
            path=last.path,
            record_type=last.record_type,
            record_id=last.record_id,
            data={**last.data, "derived_from": "artifact.deep.0000"},
        )
        library.errors.clear()
        try:
            with self.assertRaises(SOURCE_LIBRARY.SourceLibraryQueryError):
                SOURCE_LIBRARY.source_fingerprint(library, "artifact.deep.0000")
            SOURCE_LIBRARY._validate_cycles(library)
        except RecursionError as error:
            self.fail(f"deep cyclic graph recursed: {error}")
        self.assertEqual(
            sum("source dependency cycle" in error for error in library.errors), 1
        )

    def test_cli_errors_are_sorted_prefixed_repeatable_and_fail_closed(self) -> None:
        self.write(
            "src/sources/works/test/z/work.toml",
            '''
            schema = 2
            record_type = "work"
            id = "work.z"
            title = "Z"
            responsible = "Test"
            work_type = "test-work"
            ''',
        )
        self.write(
            "src/sources/works/test/a/work.toml",
            '''
            schema = 1
            record_type = "work"
            id = "work.a"
            responsible = "Test"
            work_type = "test-work"
            extra = "not allowed"
            ''',
        )

        first = self.run_cli("validate")
        second = self.run_cli("validate")
        self.assertEqual(first.returncode, 1)
        self.assertEqual(second.returncode, 1)
        self.assertEqual(first.stdout, "")
        self.assertEqual(first.stderr, second.stderr)
        lines = first.stderr.splitlines()
        self.assertTrue(lines)
        self.assertTrue(all(line.startswith("source-library error: ") for line in lines))
        self.assertEqual(lines, sorted(lines))

    def test_unknown_query_ids_produce_stable_cli_errors(self) -> None:
        self.add_valid_vertical_fixture()
        for command, extra in (
            ("uses", ()),
            ("impact", ()),
            ("search", ("needle",)),
        ):
            with self.subTest(command=command):
                result = self.run_cli(command, "work.unknown", *extra)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertEqual(
                    result.stderr,
                    "source-library error: unknown source id: work.unknown\n",
                )

    def test_passage_ranges_segments_and_search_receipts_are_exact(self) -> None:
        self.add_valid_vertical_fixture()
        library = SOURCE_LIBRARY.load_library(self.root)

        self.assertEqual(library.errors, [])
        self.assertEqual(
            [row["line"] for row in SOURCE_LIBRARY.search_rows(
                library, PASSAGE_ID, "sacrifice"
            )],
            [2],
        )
        self.assertEqual(
            SOURCE_LIBRARY.search_rows(library, PASSAGE_ID, "No match here"),
            [],
        )

        passage_fingerprint = SOURCE_LIBRARY.source_fingerprint(library, PASSAGE_ID)
        self.write(
            "src/gpt/theology/demo/research/source-bindings.toml",
            f'''
            schema = 1
            record_type = "bindings"
            document = "theology/demo"

            [[bindings]]
            source_id = "{PASSAGE_ID}"
            role = "lead"
            states = ["searched"]
            context = "The exact ranged passage was searched as a locator."
            search_scope = "Only physical line 2 of the exact artifact."
            searched_on = "2026-07-22"
            search_mode = "raw-line-literal-casefold-v1"
            query = "sacrifice"
            method = "Built-in casefolded physical-line literal search."
            matching_line_count = 1
            source_fingerprint = "{passage_fingerprint}"
            ''',
        )
        with_receipt = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(with_receipt.errors, [])

        artifact = with_receipt.records[ARTIFACT_ID]
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/passages/10-6.toml",
            f'''
            schema = 1
            record_type = "passage"
            id = "{PASSAGE_ID}"
            edition_id = "{EDITION_ID}"
            artifact_id = "{ARTIFACT_ID}"
            artifact_sha256 = "{artifact.data['sha256']}"
            locus = "{LOCUS}"
            states = ["inspected"]
            context = "Intentionally invalid locator fixture."
            physical_line_ranges = [[true, 1], [0, 1], [3, 2], [2, 3], [3, 3], [99, 99]]
            text = "The City offers Sacrifice."
            transcription_segments = [
              {{ line = 1, text = "No match here." }},
              {{ line = 2, text = "not an exact segment" }},
              {{ line = 99, text = "future line" }},
            ]
            ''',
        )
        invalid = SOURCE_LIBRARY.load_library(self.root)
        joined = "\n".join(invalid.errors)
        self.assertIn("values must be positive non-boolean integers", joined)
        self.assertIn("start must not exceed end", joined)
        self.assertIn("must be sorted and non-overlapping", joined)
        self.assertIn("ends after artifact line 4", joined)
        self.assertIn("line is outside physical_line_ranges", joined)
        self.assertIn("text is not an exact ordered substring", joined)
        self.assertIn("line is after artifact line 4", joined)
        self.assertIn("do not reproduce text exactly", joined)

    def test_passage_validation_and_search_share_lf_line_boundaries(self) -> None:
        old_bytes = self.add_valid_vertical_fixture()
        new_bytes = b"First\rSecond target\rThird\nFourth\r\n"
        old_digest = hashlib.sha256(old_bytes).hexdigest()
        new_digest = hashlib.sha256(new_bytes).hexdigest()
        artifact_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/plain-text/city-of-god.txt"
        )
        self.write(artifact_path, new_bytes)

        artifact_manifest = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/plain-text/artifact.toml"
        )
        artifact_text = (self.root / artifact_manifest).read_text(encoding="utf-8")
        self.write(
            artifact_manifest,
            artifact_text.replace(old_digest, new_digest).replace(
                f"byte_size = {len(old_bytes)}", f"byte_size = {len(new_bytes)}"
            ),
        )

        passage_manifest = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/passages/10-6.toml"
        )
        passage_text = (self.root / passage_manifest).read_text(encoding="utf-8")
        self.write(
            passage_manifest,
            passage_text.replace(old_digest, new_digest)
            .replace("physical_line_ranges = [[2, 2]]", "physical_line_ranges = [[1, 1]]")
            .replace("The City offers Sacrifice.", "Second target")
            .replace("line = 2", "line = 1"),
        )

        corpus_manifest = "src/sources/corpora/augustine-city-of-god-english.toml"
        corpus_text = (self.root / corpus_manifest).read_text(encoding="utf-8")
        old_snapshot = hashlib.sha256(
            f"{ARTIFACT_ID}\t{old_digest}\n".encode("utf-8")
        ).hexdigest()
        new_snapshot = hashlib.sha256(
            f"{ARTIFACT_ID}\t{new_digest}\n".encode("utf-8")
        ).hexdigest()
        self.write(corpus_manifest, corpus_text.replace(old_snapshot, new_snapshot))

        library = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        self.assertEqual(library.errors, [])
        self.assertEqual(
            [
                (row["line"], row["text"])
                for row in SOURCE_LIBRARY.search_rows(
                    library, PASSAGE_ID, "Second target", case_sensitive=True
                )
            ],
            [(1, "First\rSecond target\rThird")],
        )

    def test_transcription_segments_require_an_indexable_artifact(self) -> None:
        self.add_valid_vertical_fixture()
        artifact_manifest = (
            self.root
            / "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/plain-text/artifact.toml"
        )
        self.write(
            artifact_manifest.relative_to(self.root).as_posix(),
            artifact_manifest.read_text(encoding="utf-8").replace(
                "indexable = true", "indexable = false"
            ),
        )
        passage_manifest = (
            self.root
            / "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/passages/10-6.toml"
        )
        self.write(
            passage_manifest.relative_to(self.root).as_posix(),
            passage_manifest.read_text(encoding="utf-8").replace(
                "physical_line_ranges = [[2, 2]]\n", ""
            ),
        )

        library = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        self.assertIn(
            "text and transcription_segments require an indexable tracked UTF-8 artifact",
            "\n".join(library.errors),
        )

    def test_support_artifacts_are_first_class_dependencies(self) -> None:
        self.add_valid_vertical_fixture()
        before = SOURCE_LIBRARY.load_library(self.root)
        old_fingerprint = SOURCE_LIBRARY.source_fingerprint(before, ARTIFACT_ID)
        support_id = "artifact.augustine.de-civitate-dei.npnf-dods.illustration"
        image = b"\x89PNG\r\n"
        image_path = (
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/illustration/illustration.png"
        )
        self.write(image_path, image)
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/"
            "npnf-dods/artifacts/illustration/artifact.toml",
            f'''
            schema = 1
            record_type = "artifact"
            id = "{support_id}"
            edition_id = "{EDITION_ID}"
            artifact_type = "illustration"
            media_type = "image/png"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Test support image"
            rights_jurisdiction = "United States"
            source_url = "https://example.org/illustration.png"
            retrieved = "2026-07-22"
            sha256 = "{hashlib.sha256(image).hexdigest()}"
            byte_size = {len(image)}
            path = "{image_path}"
            indexable = false
            ''',
        )
        parent_manifest = before.records[ARTIFACT_ID].path
        parent_text = parent_manifest.read_text(encoding="utf-8")
        self.write(
            parent_manifest.relative_to(self.root).as_posix(),
            parent_text
            + f'''support_artifacts = [
              {{ artifact_id = "{support_id}", embedded_reference = "illustration.png" }},
            ]
            ''',
        )

        library = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        self.assertEqual(library.errors, [])
        self.assertNotEqual(
            old_fingerprint,
            SOURCE_LIBRARY.source_fingerprint(library, ARTIFACT_ID),
        )
        impacted_sources = {
            row["id"]
            for row in SOURCE_LIBRARY.impact_rows(library, support_id)
            if row["kind"] == "source"
        }
        self.assertTrue({ARTIFACT_ID, PASSAGE_ID, CORPUS_ID} <= impacted_sources)
        self.assertTrue(
            any(
                row["kind"] == "document" and row["id"] == "theology/demo"
                for row in SOURCE_LIBRARY.impact_rows(library, support_id)
            )
        )
        self.assertEqual(
            len(SOURCE_LIBRARY.search_rows(library, CORPUS_ID, "sacrifice")),
            2,
        )

        for unsafe_reference in (
            "../missing.png",
            "%2e%2e/missing.png",
            "a/%2E%2E/missing.png",
            "safe%2f..%2fmissing.png",
            "a/./illustration.png",
            "a//illustration.png",
        ):
            with self.subTest(unsafe_reference=unsafe_reference):
                self.write(
                    parent_manifest.relative_to(self.root).as_posix(),
                    parent_text
                    + f'''support_artifacts = [
                      {{ artifact_id = "{support_id}", embedded_reference = "{unsafe_reference}" }},
                    ]
                    ''',
                )
                unsafe = SOURCE_LIBRARY.load_library(
                    self.root, check_binding_fingerprints=False
                )
                self.assertIn(
                    "embedded_reference must be a safe relative path",
                    "\n".join(unsafe.errors),
                )

        self.write(
            parent_manifest.relative_to(self.root).as_posix(),
            parent_text
            + f'''support_artifacts = [
              {{ artifact_id = "{support_id}", embedded_reference = "missing.png" }},
            ]
            ''',
        )
        missing = SOURCE_LIBRARY.load_library(
            self.root, check_binding_fingerprints=False
        )
        self.assertIn(
            "embedded_reference does not occur in the exact parent artifact",
            "\n".join(missing.errors),
        )

    def test_git_attributes_preserve_arbitrary_payload_bytes(self) -> None:
        paths = (
            "src/sources/works/x/y/editions/z/artifacts/a/source.txt",
            "src/sources/works/x/y/editions/z/artifacts/a/source.pdf",
            "src/sources/works/x/y/editions/z/artifacts/a/source.unknown",
            "src/sources/works/x/y/editions/z/artifacts/a/artifact.toml",
        )
        result = subprocess.run(
            ["git", "check-attr", "text", "eol", "whitespace", "--", *paths],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

        for payload in paths[:3]:
            self.assertIn(f"{payload}: text: unset", result.stdout)
            self.assertIn(f"{payload}: whitespace: unset", result.stdout)
        self.assertIn(f"{paths[3]}: text: set", result.stdout)
        self.assertIn(f"{paths[3]}: eol: lf", result.stdout)
        self.assertIn(f"{paths[3]}: whitespace: unspecified", result.stdout)


if __name__ == "__main__":
    unittest.main()
