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
    def generate(self, output: Path) -> None:
        subprocess.run(
            [
                str(SCRIPT),
                "--schema", str(SCHEMA),
                "--selections", str(SELECTIONS),
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
            self.assertIn(
                r"{Latin term not asserted}",
                alpha,
            )
            self.assertIn(
                r"\RSDAlphaOmission{obj-chalice}",
                omissions,
            )
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
            self.assertNotIn("editorial-proposal", text)

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
