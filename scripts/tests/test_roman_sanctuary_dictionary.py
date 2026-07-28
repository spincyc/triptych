import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "roman-sanctuary-dictionary"
DICTIONARY_ROOT = ROOT / "src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
SCHEMA = DICTIONARY_ROOT / "shared/schema/inventory-schema.toml"
SELECTIONS = DICTIONARY_ROOT / "shared/schema/edition-selections.toml"
ARTWORK_MANIFEST = DICTIONARY_ROOT / "research/artwork-manifest.toml"
RECORDS = DICTIONARY_ROOT / "shared/objects"


class DictionaryGeneratorTests(unittest.TestCase):
    def generate(self, output: Path, selections: Path = SELECTIONS) -> None:
        subprocess.run(
            [
                str(SCRIPT),
                "--schema", str(SCHEMA),
                "--selections", str(selections),
                "--artwork-manifest", str(ARTWORK_MANIFEST),
                "--records", str(RECORDS),
                "--output", str(output),
            ],
            check=True,
        )

    def test_one_canonical_alpha_view_excludes_unverified_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            alpha = (output / "ed-comprehensive.tex").read_text()
            sidecar = (output / "ed-comprehensive.alpha-admissions.toml").read_text()
            omissions = (output / "ed-comprehensive.alpha-omissions.tex").read_text()
            self.assertIn('status = "alpha"', sidecar)
            self.assertIn('distribution_state = "public-alpha"', sidecar)
            self.assertIn("obj-altar-missal", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-altar-cloths}", alpha)
            self.assertIn(
                r"\RSDObjectRecord{obj-altar-cruet}",
                alpha,
            )
            self.assertIn(
                r"\RSDObjectRecord{obj-communion-plate}",
                alpha,
            )
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-cross}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-bell}", alpha)
            self.assertNotIn(r"\RSDObjectRecord{obj-sacristy-lavatory}", alpha)
            self.assertIn(
                r"{Latin term not asserted}",
                alpha,
            )
            self.assertIn(r"\RSDObjectRecord{obj-chalice}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-paten}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-epistle-book}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-gospel-book}", alpha)
            self.assertNotIn(r"\RSDAlphaOmission{obj-chalice}", omissions)
            self.assertNotIn(r"\RSDAlphaOmission{obj-paten}", omissions)
            shared = "art-paten-catalog-exemplar-comparison"
            self.assertEqual(alpha.count(shared), 2)
            paten_record = alpha.split(r"\RSDObjectRecord{obj-paten}", 1)[1].split(
                r"\RSDEndObjectRecord", 1
            )[0]
            chalice_record = alpha.split(r"\RSDObjectRecord{obj-chalice}", 1)[1].split(
                r"\RSDEndObjectRecord", 1
            )[0]
            self.assertIn(f"{{{shared}}}", paten_record)
            self.assertIn("{obj-paten}", paten_record)
            self.assertIn(f"{{{shared}}}", chalice_record)
            self.assertIn("{obj-paten}", chalice_record)
            self.assertFalse((output / "ed-comprehensive.review.tex").exists())
            self.assertFalse((output / "ed-comprehensive.review-admissions.toml").exists())

    def test_qualifications_are_not_repeated_on_entry_or_coverage_pages(self):
        shell = (DICTIONARY_ROOT / "shared/publication-shell.tex").read_text()
        renderer = (DICTIONARY_ROOT / "shared/generated-record-renderer.tex").read_text()
        format_source = (DICTIONARY_ROOT / "shared/dictionary-format.tex").read_text()
        self.assertIn(r"\large\bfseries ALPHA", format_source)
        self.assertNotIn("ALPHA RECORD", renderer)
        self.assertNotIn("Evidence caveat", renderer)
        self.assertNotIn(r"\section{Coverage}", shell)

    def test_canonical_output_is_deterministic_and_audience_specific(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            first = (output / "ed-sacristan.tex").read_bytes()
            self.generate(output)
            self.assertEqual(first, (output / "ed-sacristan.tex").read_bytes())
            text = first.decode()
            self.assertIn(r"\RSDObjectRecord{obj-altar-missal}", text)
            self.assertIn(r"\RSDSelectedAudienceNote{Prepare the Missal", text)
            self.assertIn(r"\RSDObjectRecord{obj-altar-cloths}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare three clean blessed cloths",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-altar-cruet}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the wine and water vessels",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-communion-plate}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the Communion plate",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-cross}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Confirm the locally appointed focus",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-bell}", text)
            self.assertNotIn(r"\RSDObjectRecord{obj-sacristy-lavatory}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Identify the local bell",
                text,
            )
            self.assertNotIn("editorial-proposal", text)
            self.assertIn(r"\RSDObjectRecord{obj-epistle-book}", text)
            self.assertIn(r"\RSDObjectRecord{obj-gospel-book}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the lesson book",
                text,
            )
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the Gospel book",
                text,
            )

    def test_five_generic_editions_use_declared_dense_section_order(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            expectations = {
                "ed-comprehensive": (
                    r"\RSDDensePlateStart{Church And Sanctuary}{1}",
                    r"\RSDDensePlateStart{Related Ceremonies}{1}",
                ),
                "ed-sacristan": (
                    r"\RSDDensePlateStart{Sanctuary And Altar Preparation}{1}",
                    r"\RSDDensePlateStart{Vessels Linens And Books}{1}",
                ),
                "ed-mc-trainer": (
                    r"\RSDDensePlateStart{People Roles And Stations}{1}",
                    r"\RSDDensePlateStart{Objects And Handoffs}{1}",
                ),
                "ed-general-reader": (
                    r"\RSDDensePlateStart{Sanctuary}{1}",
                    r"\RSDDensePlateStart{Objects And Linens}{1}",
                ),
                "ed-pontifical": (
                    r"\RSDDensePlateStart{Furnishings And Books}{1}",
                    r"\RSDDensePlateStart{Ministers And Object Transfers}{1}",
                ),
            }
            for edition, markers in expectations.items():
                text = (output / f"{edition}.tex").read_text()
                positions = [text.index(marker) for marker in markers]
                self.assertEqual(positions, sorted(positions), edition)
                self.assertIn(r"\RSDDensePlateRowBreak", text)
                self.assertIn(r"\RSDDensePlateCellBreak", text)
            altar_server = (output / "ed-altar-server.tex").read_text()
            self.assertNotIn(r"\RSDDensePlateStart", altar_server)
            for edition in (
                "ed-comprehensive", "ed-sacristan", "ed-mc-trainer",
                "ed-general-reader", "ed-pontifical", "ed-altar-server",
            ):
                text = (output / f"{edition}.tex").read_text()
                self.assertNotIn(r"\RSDStoryPlateStart", text)

    def test_synthetic_story_spreads_are_deterministic_and_exact_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "out"
            selections = root / "edition-selections.toml"
            selections.write_text(SELECTIONS.read_text().replace(
                'audience = "general-reader"',
                'audience = "general-reader"\nlayout_mode = "story-spread-v1"',
                1,
            ))
            self.generate(output, selections)
            first = (output / "ed-general-reader.tex").read_bytes()
            self.generate(output, selections)
            self.assertEqual(first, (output / "ed-general-reader.tex").read_bytes())
            text = first.decode()
            self.assertIn(r"\RSDStoryPlateStart{Sanctuary}{1}", text)
            self.assertIn(r"\RSDStoryPlateStart{Objects And Linens}{1}", text)
            self.assertIn(r"\RSDStoryHeroNext", text)
            self.assertIn(r"\RSDStoryCompanionsStart", text)
            self.assertNotIn(r"\RSDDensePlateStart", text)
            object_ids = [
                line.split("{", 1)[1].split("}", 1)[0]
                for line in text.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            ]
            self.assertEqual(len(object_ids), len(set(object_ids)))
            for edition in (
                "ed-comprehensive", "ed-sacristan",
                "ed-mc-trainer", "ed-pontifical", "ed-altar-server",
            ):
                other = (output / f"{edition}.tex").read_text()
                self.assertNotIn(r"\RSDStoryPlateStart", other)

    def test_text_only_lavatory_is_held_from_every_generated_edition(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            for edition in (
                "ed-comprehensive", "ed-sacristan", "ed-mc-trainer",
                "ed-general-reader", "ed-pontifical", "ed-altar-server",
            ):
                text = (output / f"{edition}.tex").read_text()
                self.assertNotIn(r"\RSDObjectRecord{obj-sacristy-lavatory}", text)

    def test_exact_lesson_books_use_the_tex_native_artwork_exception(self):
        generator = SCRIPT.read_text()
        renderer = (
            DICTIONARY_ROOT / "shared/generated-record-renderer.tex"
        ).read_text()
        self.assertIn('"obj-epistle-book"', generator)
        self.assertIn('"obj-gospel-book"', generator)
        self.assertIn(r"\RSDTeXNativeBookArtwork", renderer)
        self.assertIn("no binding, material, ornament", renderer)

    def test_shared_artwork_uses_data_driven_render_owner(self):
        renderer = (
            DICTIONARY_ROOT / "shared/generated-record-renderer.tex"
        ).read_text()
        self.assertNotIn("obj-chalice", renderer)
        self.assertNotIn("art-paten-catalog-exemplar-comparison", renderer)
        self.assertIn(r"\ifstrequal{\RSDObjectID}{#8}", renderer)

    def test_unknown_record_field_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            records = root / "records"
            records.mkdir()
            fixture = (
                DICTIONARY_ROOT / "shared/schema/object.example.toml"
            ).read_text().replace(
                "schema_version = 1",
                "schema_version = 1\nunknown = true",
                1,
            )
            (records / "bad.toml").write_text(fixture)
            result = subprocess.run(
                [
                    str(SCRIPT),
                    "--schema", str(SCHEMA),
                    "--selections", str(SELECTIONS),
                    "--artwork-manifest", str(ARTWORK_MANIFEST),
                    "--records", str(records),
                    "--output", str(root / "out"),
                ],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown top-level field", result.stderr)


if __name__ == "__main__":
    unittest.main()
