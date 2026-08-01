"""Tests for the mechanical release-binding bookkeeping tool."""

import contextlib
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

TOOL_PATH = (
    pathlib.Path(__file__).resolve().parents[2] / "tools" / "release-bindings"
)


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
        (self.root / "pdf/gpt/articles").mkdir(parents=True)
        (self.root / "pdf/claude/articles").mkdir(parents=True)
        (self.root / "release/rights").mkdir(parents=True)
        self.gpt_pdf = self.root / "pdf/gpt/articles/example.pdf"
        self.claude_pdf = self.root / "pdf/claude/articles/example.pdf"
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
        # The renderer's recognized set is the second half of the comparison,
        # so every test declares it rather than inheriting the real site's.
        self.recognize({"README.md"})

    def recognize(self, sources):
        self.tool.recognized_site_sources = lambda: set(sources)

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
        # The changed site source is stale until refresh records it. This
        # assertion read 0 until 2026-07-31, which is the defect: it locked in
        # a status that could not see the divergence it was written beside.
        self.assertEqual(1, self.tool.report_status(self.tool.load_manifest()))
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
        review["gates"] = []
        review["approval"] = None
        review["review_distribution"] = {
            "authorization": "auth-1",
            "pdf_sha256": sha(b"gpt pdf v1"),
        }
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

    def capture_status(self):
        """(exit code, printed lines) for a read-only status run."""
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            code = self.tool.report_status(self.tool.load_manifest())
        return code, stream.getvalue().splitlines()

    def test_status_fails_on_a_changed_site_source_and_names_both_hashes(self):
        self.tool.refresh(self.tool.load_manifest())
        self.assertEqual(0, self.capture_status()[0])

        self.readme.write_bytes(b"readme v2")
        code, lines = self.capture_status()

        self.assertEqual(1, code)
        self.assertIn("stale site source README.md", lines[0])
        self.assertIn(sha(b"readme v1"), lines[0])
        self.assertIn(sha(b"readme v2"), lines[0])
        self.assertIn("stale: 1 stale binding(s)", lines[-1])

    def test_status_fails_on_a_site_source_whose_file_is_gone(self):
        self.tool.refresh(self.tool.load_manifest())
        self.assertEqual(0, self.capture_status()[0])

        self.readme.unlink()
        code, lines = self.capture_status()

        self.assertEqual(1, code)
        self.assertIn("missing site source README.md", lines[0])
        self.assertIn(sha(b"readme v1"), lines[0])
        self.assertIn("no such file", lines[0])
        self.assertIn("stale: 1 stale binding(s)", lines[-1])

    def test_status_fails_on_a_recognized_source_the_record_omits(self):
        """The defect: a source never recorded is invisible to a record walk."""
        self.tool.refresh(self.tool.load_manifest())
        self.assertEqual(0, self.capture_status()[0])

        icon = self.root / "assets/icon.png"
        icon.parent.mkdir(parents=True)
        icon.write_bytes(b"icon v1")
        self.recognize({"README.md", "assets/icon.png"})
        code, lines = self.capture_status()

        self.assertEqual(1, code)
        self.assertIn("unrecorded site source assets/icon.png", lines[0])
        self.assertIn(sha(b"icon v1"), lines[0])
        self.assertIn("ADOPT=1", lines[0])
        self.assertIn("stale: 1 stale binding(s)", lines[-1])

        self.tool.refresh(self.tool.load_manifest(), adopt=True)
        self.assertEqual(0, self.capture_status()[0])

    def test_status_fails_on_a_recorded_source_no_longer_recognized(self):
        """A retired file leaves a hash attesting something nothing renders."""
        self.tool.refresh(self.tool.load_manifest())
        self.assertEqual(0, self.capture_status()[0])

        self.recognize(set())
        code, lines = self.capture_status()

        self.assertEqual(1, code)
        self.assertIn("unrecognized site source README.md", lines[0])
        self.assertIn(sha(b"readme v1"), lines[0])
        self.assertIn("no longer reads it", lines[0])
        self.assertIn("stale: 1 stale binding(s)", lines[-1])

    def test_status_passes_and_reports_exact_on_a_settled_tree(self):
        self.tool.refresh(self.tool.load_manifest())

        code, lines = self.capture_status()

        self.assertEqual(0, code)
        self.assertEqual(["exact: 0 stale binding(s)"], lines)

    def test_status_and_refresh_read_one_divergence_comparison(self):
        """`status` must see exactly what `refresh` would rewrite."""
        self.tool.refresh(self.tool.load_manifest())
        self.readme.write_bytes(b"readme v2")

        reported = {
            divergence.source
            for divergence in self.tool.site_source_divergences(
                self.tool.single_authorization(self.tool.load_manifest())
            )
        }
        rewritten = {
            change.removeprefix("site ")
            for change in self.tool.refresh(self.tool.load_manifest())
            if change.startswith("site ")
        }

        self.assertEqual({"README.md"}, reported)
        self.assertEqual(reported, rewritten)

    def test_refresh_leaves_legacy_expected_counts_untouched(self):
        manifest = self.read_manifest()
        manifest["expected_counts"] = {"publications": 99}
        self.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        changes = self.tool.refresh(self.tool.load_manifest())
        self.assertNotIn("expected_counts", changes)
        expected = self.read_manifest()["expected_counts"]
        self.assertEqual(99, expected["publications"])

    def test_refresh_adopts_and_retires_recognized_site_sources(self):
        page = self.root / "web/gpt/articles/example.md"
        page.parent.mkdir(parents=True)
        page.write_bytes(b"web edition v1")
        self.recognize({"web/gpt/articles/example.md"})

        changes = self.tool.refresh(self.tool.load_manifest(), adopt=True)

        self.assertIn("adopted site web/gpt/articles/example.md", changes)
        self.assertIn("retired site README.md", changes)
        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]
        self.assertEqual({"web/gpt/articles/example.md": sha(b"web edition v1")}, recorded)
        self.assertIn("web/gpt/articles/example.md", self.record.read_text())
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))

    def test_refresh_without_adoption_keeps_the_recorded_input_set(self):
        self.recognize({"web/gpt/articles/example.md"})

        self.tool.refresh(self.tool.load_manifest())

        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]
        self.assertEqual({"README.md"}, set(recorded))

    def test_site_refresh_does_not_scan_publication_pdfs(self):
        self.gpt_pdf.unlink()
        self.tool.refresh(self.tool.load_manifest())

    def test_add_publication_qualifies_and_rejects_duplicates(self):
        new_pdf = self.root / "pdf/claude/articles/second.pdf"
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

    def test_migrate_publications_creates_local_records_and_prunes_aggregates(self):
        manifest = self.read_manifest()
        manifest["expected_counts"] = {"publications": 2}
        self.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        migrated = self.tool.migrate_publications(self.tool.load_manifest())

        self.assertEqual(2, migrated)
        manifest = self.read_manifest()
        self.assertNotIn("publications", manifest)
        self.assertNotIn("expected_counts", manifest)
        gpt_record = json.loads(
            (
                self.root
                / "release/publications/gpt/articles/example.json"
            ).read_text()
        )
        self.assertEqual("alpha", gpt_record["status"])
        self.assertEqual("auth-1", gpt_record["authorization"])
        self.assertNotIn("pdf_sha256", gpt_record)

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

    def test_approve_states_the_inventory_size_it_verified(self):
        self.tool.refresh(self.tool.load_manifest())

        self.tool.approve(
            self.tool.load_manifest(), "Approve the snapshot.", "America/Chicago"
        )

        self.assertIn("all 1 exact recognized", self.record.read_text())

    def test_approve_refuses_an_inventory_that_omits_a_recognized_source(self):
        """The claim is computed, not asserted: no completeness, no approval."""
        self.tool.refresh(self.tool.load_manifest())
        icon = self.root / "assets/icon.png"
        icon.parent.mkdir(parents=True)
        icon.write_bytes(b"icon v1")
        self.recognize({"README.md", "assets/icon.png"})
        before = self.record.read_text()

        with self.assertRaises(self.tool.BindingError) as failure:
            self.tool.approve(
                self.tool.load_manifest(), "Approve the snapshot.", "America/Chicago"
            )

        message = str(failure.exception)
        self.assertIn("assets/icon.png", message)
        self.assertIn("refresh-release-bindings ADOPT=1", message)
        self.assertEqual(before, self.record.read_text())


if __name__ == "__main__":
    unittest.main()
