import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "roman-sanctuary-dictionary"
SCHEMA = ROOT / "src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/shared/schema/inventory-schema.toml"
SELECTIONS = ROOT / "src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/shared/schema/edition-selections.toml"
DICTIONARY_ROOT = ROOT / "src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
ARTWORK_MANIFEST = DICTIONARY_ROOT / "research/artwork-manifest.toml"
RECORDS = DICTIONARY_ROOT / "shared/objects"


class DictionaryGeneratorTests(unittest.TestCase):
    def test_public_alpha_review_gate_excludes_unverified_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
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
            sidecar = (output / "ed-comprehensive.review-admissions.toml").read_text()
            review = (output / "ed-comprehensive.review.tex").read_text()
            omissions = (output / "ed-comprehensive.review-omissions.tex").read_text()
            self.assertIn('status = "priestly-review"', sidecar)
            self.assertIn('distribution_state = "public-alpha"', sidecar)
            self.assertIn("admitted_object_count = 6", sidecar)
            self.assertIn("omitted_object_count = 37", sidecar)
            self.assertIn("obj-chalice", review)
            self.assertNotIn("obj-altar-cruet", review)
            self.assertIn(
                r"\RSDReviewOmission{obj-altar-cruet}{Altar cruet}"
                r"{a printed claim remains an unverified lead}",
                omissions,
            )
            self.assertIn(
                r"\RSDReviewOmission{obj-aspergillum}{Aspergillum}"
                r"{object identity or governing status remains unresolved}",
                omissions,
            )

    def test_shared_format_owns_review_label_without_repeated_shell_apparatus(self):
        shell = (DICTIONARY_ROOT / "shared/publication-shell.tex").read_text()
        format_source = (DICTIONARY_ROOT / "shared/dictionary-format.tex").read_text()
        exact_tex_label = "PRIESTLY REVIEW COPY --- NOT FOR PUBLIC RELIANCE"
        self.assertIn(exact_tex_label, format_source)
        self.assertIn(
            r"\DictionaryTitle{\RSDTitle}{\RSDSubtitle}{\RSDEditionLine}",
            shell,
        )
        self.assertNotIn(exact_tex_label, shell)
        self.assertNotIn(r"\section{Review Snapshot and Open Gates}", shell)
        self.assertNotIn(
            "public-distribution manifests bind this snapshot identity",
            shell,
        )
        self.assertNotIn("PRIESTLY REVIEW DRAFT", shell)
        self.assertNotIn("NOT APPROVED FOR INSTRUCTION OR PUBLICATION", shell)

    def test_fixture_renders_canonical_and_derived_views_deterministically(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            records, output = root / "records", root / "out"
            records.mkdir()
            claims = "\n".join(
                f'''[[claims]]
id = "clm-chalice-{kind}"
kind = "{kind}"
text = "Checked {kind} & use."
evidence_state = "checked-paraphrase"
source_ids = ["src-chalice"]'''
                for kind in ("identity", "appearance", "liturgical-use", "ceremonial-presence")
            )
            (records / "chalice.toml").write_text(textwrap.dedent(f'''
                schema_version = 1
                id = "obj-chalice"
                workflow_state = "publication-ready"
                preferred_english_name = "Chalice"
                latin_headword = "calix"
                categories = ["sacred-vessels"]
                periods = ["roman-1962-horizon"]
                statuses = ["universal-roman"]
                ceremonies = ["low-mass"]
                confusable_with = []
                related_objects = []
                [presence]
                locations = ["altar"]
                contexts = ["Mass"]
                [handling]
                ordinary_handlers = ["priest"]
                server_relation = "must-not-handle"
                [audience_relevance]
                altar_server = "required"
                sacristan = "required"
                mc_trainer = "useful"
                general_reader = "required"
                pontifical = "useful"
                {claims}
                [[sources]]
                id = "src-chalice"
                binding = "source-fixture"
                locus = "fixture"
                role = "manual"
                verification_state = "claim-verified"
                [[artwork]]
                id = "art-chalice"
                view = "isolated"
                asset = "assets/chalice.png"
                review_state = "approved"
                depicts = ["obj-chalice"]
            '''), encoding="utf-8")
            manifest = root / "art.toml"
            manifest.write_text('[[asset]]\nid="art-chalice"\npath="assets/chalice.png"\n', encoding="utf-8")
            admissions = root / "review.toml"
            admissions.write_text(textwrap.dedent('''
                schema_version = 1
                [[admissions]]
                object_id = "obj-chalice"
                artwork_ids = ["art-chalice"]
                editions = ["ed-altar-server"]
                priestly_review_ready = true
            '''))
            command = [str(SCRIPT), "--schema", str(SCHEMA), "--selections", str(SELECTIONS),
                       "--artwork-manifest", str(manifest), "--records", str(records),
                       "--review-admissions", str(admissions), "--output", str(output)]
            subprocess.run(command, check=True)
            first = (output / "ed-altar-server.tex").read_bytes()
            subprocess.run(command, check=True)
            self.assertEqual(first, (output / "ed-altar-server.tex").read_bytes())
            text = first.decode()
            self.assertIn(r"\RSDObjectRecord{obj-chalice}{Chalice}{calix}", text)
            self.assertIn(r"Checked identity \& use.", text)
            self.assertIn("makes no inventory-completeness claim", text)
            self.assertIn("obj-chalice", (output / "ed-comprehensive.tex").read_text())
            review = (output / "ed-altar-server.review.tex").read_text()
            self.assertIn("PRIESTLY REVIEW COPY", review)
            self.assertIn("obj-chalice", review)
            register = (output / "ed-altar-server.review-register.tsv").read_text()
            self.assertIn("ed-altar-server\tobj-chalice\tpublication-ready\tart-chalice", register)
            self.assertNotIn("obj-chalice", (output / "ed-sacristan.review.tex").read_text())

    def test_unknown_record_field_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            records = root / "records"
            records.mkdir()
            fixture = (ROOT / "src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/shared/schema/object.example.toml").read_text()
            fixture = fixture.replace("schema_version = 1", "schema_version = 1\nunknown = true", 1)
            (records / "bad.toml").write_text(fixture)
            manifest = root / "art.toml"
            manifest.write_text("", encoding="utf-8")
            result = subprocess.run(
                [str(SCRIPT), "--schema", str(SCHEMA), "--selections", str(SELECTIONS),
                 "--artwork-manifest", str(manifest), "--records", str(records), "--output", str(root / "out")],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown top-level field", result.stderr)

    def test_canonical_art_gate_cannot_be_bypassed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            records = root / "records"
            records.mkdir()
            fixture = (
                ROOT
                / "src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
                / "shared/schema/object.example.toml"
            ).read_text()
            fixture = fixture.replace('workflow_state = "lead"', 'workflow_state = "publication-ready"')
            fixture = fixture.replace('review_state = "prompted"', 'review_state = "generated"')
            (records / "blocked.toml").write_text(fixture)
            manifest = root / "art.toml"
            manifest.write_text(
                '[[asset]]\nid="art-example-isolated"\npath="assets/placeholder-not-present.png"\n',
                encoding="utf-8",
            )
            result = subprocess.run(
                [str(SCRIPT), "--schema", str(SCHEMA), "--selections", str(SELECTIONS),
                 "--artwork-manifest", str(manifest), "--records", str(records),
                 "--output", str(root / "out")],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("canonical inventory validation failed", result.stderr)
            self.assertIn("not allowed for publication-ready", result.stderr)


if __name__ == "__main__":
    unittest.main()
