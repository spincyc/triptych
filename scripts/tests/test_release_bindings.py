"""Tests for the mechanical release-binding bookkeeping tool."""

import hashlib
import importlib.machinery
import importlib.util
import json
import pathlib
import tempfile
import unittest

TOOL_PATH = pathlib.Path(__file__).resolve().parent.parent / "release-bindings"


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_release_bindings_tool", str(TOOL_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


RIGHTS_TEMPLATE = """# Rights record

## Basis and authority

Recorded basis.

## Exact approved snapshots

| Publication ID | SHA-256 |
| --- | --- |
| `articles/example` | `{gpt_hash}` |
| `claude:articles/example` | `{claude_hash}` |

## Exact approved reader-facing site sources

| Repository path | SHA-256 |
| --- | --- |
| `README.md` | `{readme_hash}` |

## Operational controls

Controls text.
"""


class ReleaseBindingsTests(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        (self.root / "doc/gpt/articles").mkdir(parents=True)
        (self.root / "doc/claude/articles").mkdir(parents=True)
        (self.root / "release/rights").mkdir(parents=True)
        self.gpt_pdf = self.root / "doc/gpt/articles/example.pdf"
        self.claude_pdf = self.root / "doc/claude/articles/example.pdf"
        self.readme = self.root / "README.md"
        self.gpt_pdf.write_bytes(b"gpt pdf v1")
        self.claude_pdf.write_bytes(b"claude pdf v1")
        self.readme.write_bytes(b"readme v1")
        self.record = self.root / "release/rights/record.md"
        self.record.write_text(
            RIGHTS_TEMPLATE.format(
                gpt_hash=sha(b"gpt pdf v1"),
                claude_hash=sha(b"claude pdf v1"),
                readme_hash=sha(b"readme v1"),
            )
        )
        manifest = {
            "schema_version": 2,
            "release_id": "public-alpha",
            "provider": "gpt",
            "providers": ["gpt", "claude"],
            "expected_counts": {
                "publications": 2,
                "release": 2,
                "review": 0,
                "hold": 0,
                "providers": {"claude": 1, "gpt": 1},
            },
            "authorizations": {
                "auth-1": {
                    "rights_record": "release/rights/record.md",
                    "rights_record_sha256": "0" * 64,
                    "site_sources": {"README.md": sha(b"readme v1")},
                    "approved_on": "2026-07-24",
                    "effective_at": "2026-07-24T00:00:00-05:00",
                }
            },
            "publications": [
                {
                    "id": "articles/example",
                    "catalog": "library/faith.md",
                    "status": "release",
                    "gates": [],
                    "approval": {
                        "authorization": "auth-1",
                        "pdf_sha256": sha(b"gpt pdf v1"),
                    },
                },
                {
                    "id": "claude:articles/example",
                    "catalog": "library/faith.md",
                    "status": "release",
                    "gates": [],
                    "approval": {
                        "authorization": "auth-1",
                        "pdf_sha256": sha(b"claude pdf v1"),
                    },
                },
            ],
        }
        self.manifest_path = self.root / "release/public-alpha.json"
        self.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.tool.ROOT = self.root
        self.tool.MANIFEST = self.manifest_path

    def read_manifest(self):
        return json.loads(self.manifest_path.read_text())

    def test_refresh_settles_and_status_reports_exact(self):
        changes = self.tool.refresh(self.tool.load_manifest())
        self.assertIn("rights_record_sha256", changes)
        self.assertEqual([], self.tool.refresh(self.tool.load_manifest()))
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))

    def test_refresh_updates_site_without_rebinding_changed_pdf(self):
        self.tool.refresh(self.tool.load_manifest())
        original_manifest = self.read_manifest()
        original_record = self.record.read_text()
        self.claude_pdf.write_bytes(b"claude pdf v2")
        self.readme.write_bytes(b"readme v2")
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))
        changes = self.tool.refresh(self.tool.load_manifest())
        self.assertIn("site README.md", changes)
        manifest = self.read_manifest()
        self.assertEqual(
            original_manifest["publications"][1]["approval"]["pdf_sha256"],
            manifest["publications"][1]["approval"]["pdf_sha256"],
        )
        record_text = self.record.read_text()
        self.assertNotIn(sha(b"claude pdf v2"), record_text)
        self.assertIn("## Exact approved snapshots", original_record)
        self.assertIn(sha(b"readme v2"), record_text)
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))

    def test_changed_legacy_review_pdf_needs_no_shared_refresh(self):
        manifest = self.read_manifest()
        review = manifest["publications"][0]
        review["status"] = "review"
        review["gates"] = ["independent-review"]
        review["approval"] = None
        review["review_distribution"] = {
            "authorization": "auth-1",
            "pdf_sha256": sha(b"gpt pdf v1"),
        }
        manifest["expected_counts"].update({"release": 1, "review": 1})
        self.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.tool.refresh(self.tool.load_manifest())

        self.gpt_pdf.write_bytes(b"gpt review pdf v2")
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))
        changes = self.tool.refresh(self.tool.load_manifest())

        self.assertNotIn("pdf articles/example", changes)
        refreshed = self.read_manifest()["publications"][0]
        self.assertEqual(
            sha(b"gpt pdf v1"),
            refreshed["review_distribution"]["pdf_sha256"],
        )
        self.assertIsNone(refreshed["approval"])
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))

    def test_refresh_leaves_legacy_expected_counts_untouched(self):
        manifest = self.read_manifest()
        manifest["expected_counts"]["publications"] = 99
        self.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        changes = self.tool.refresh(self.tool.load_manifest())
        self.assertNotIn("expected_counts", changes)
        expected = self.read_manifest()["expected_counts"]
        self.assertEqual(99, expected["publications"])

    def test_refresh_adopts_and_retires_recognized_site_sources(self):
        page = self.root / "web/gpt/articles/example.md"
        page.parent.mkdir(parents=True)
        page.write_bytes(b"web edition v1")
        self.tool.recognized_site_sources = lambda: {"web/gpt/articles/example.md"}

        changes = self.tool.refresh(self.tool.load_manifest(), adopt=True)

        self.assertIn("adopted site web/gpt/articles/example.md", changes)
        self.assertIn("retired site README.md", changes)
        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]
        self.assertEqual({"web/gpt/articles/example.md": sha(b"web edition v1")}, recorded)
        self.assertIn("web/gpt/articles/example.md", self.record.read_text())
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))

    def test_refresh_without_adoption_keeps_the_recorded_input_set(self):
        self.tool.recognized_site_sources = lambda: {"web/gpt/articles/example.md"}

        self.tool.refresh(self.tool.load_manifest())

        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]
        self.assertEqual({"README.md"}, set(recorded))

    def test_site_refresh_does_not_scan_publication_pdfs(self):
        self.gpt_pdf.unlink()
        self.tool.refresh(self.tool.load_manifest())

    def test_add_publication_qualifies_and_rejects_duplicates(self):
        new_pdf = self.root / "doc/claude/articles/second.pdf"
        new_pdf.write_bytes(b"second")
        publication_id = self.tool.add_publication(
            self.tool.load_manifest(),
            "claude",
            "articles/second",
            "library/faith.md",
            "hold",
        )
        self.assertEqual("claude:articles/second", publication_id)
        record_path = (
            self.root / "release/publications/claude/articles/second.json"
        )
        entry = json.loads(record_path.read_text())
        self.assertEqual("hold", entry["status"])
        self.assertIsNone(entry["authorization"])
        self.assertNotIn("pdf_sha256", entry)
        with self.assertRaises(self.tool.BindingError):
            self.tool.add_publication(
                self.tool.load_manifest(),
                "claude",
                "articles/second",
                "library/faith.md",
                "hold",
            )

    def test_add_alpha_requires_installed_pdf_and_known_provider(self):
        with self.assertRaises(self.tool.BindingError):
            self.tool.add_publication(
                self.tool.load_manifest(),
                "claude",
                "articles/missing",
                "library/faith.md",
                "alpha",
            )
        with self.assertRaises(self.tool.BindingError):
            self.tool.add_publication(
                self.tool.load_manifest(),
                "mistral",
                "articles/example",
                "library/faith.md",
                "hold",
            )

    def test_approve_records_note_and_refreshes(self):
        self.claude_pdf.write_bytes(b"claude pdf v3")
        with self.assertRaises(self.tool.BindingError):
            self.tool.approve(self.tool.load_manifest(), "   ", "America/Chicago")
        self.tool.approve(
            self.tool.load_manifest(),
            "Approve the exact current snapshot.",
            "America/Chicago",
        )
        record_text = self.record.read_text()
        self.assertIn("Approve the exact current snapshot.", record_text)
        self.assertIn("Supplemental exact-current-snapshot clearance", record_text)
        self.assertNotIn(sha(b"claude pdf v3"), record_text)
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))


if __name__ == "__main__":
    unittest.main()
