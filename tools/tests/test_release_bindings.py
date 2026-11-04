"""Tests for the mechanical release-binding bookkeeping tool."""

import contextlib
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
TOOL_PATH = REPO / "tools" / "release-bindings"


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


def inventory_digest(site_sources: dict) -> str:
    """The record's stated definition, derived here without the tool."""
    text = "".join(
        f"{site_sources[path]}  {path}\n" for path in sorted(site_sources)
    )
    return sha(text.encode("utf-8"))


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
        self.assertIn(
            inventory_digest({"README.md": sha(b"readme v2")}), record_text
        )
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
        self.assertIn(inventory_digest(recorded), self.record.read_text())
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))

    def test_refresh_without_adoption_keeps_the_recorded_input_set(self):
        self.recognize({"web/gpt/articles/example.md"})

        self.tool.refresh(self.tool.load_manifest())

        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]
        self.assertEqual({"README.md"}, set(recorded))

    def test_scoped_adoption_preserves_a_missing_recorded_sibling(self):
        own = self.root / "web/own/page.md"
        own.parent.mkdir(parents=True)
        own.write_bytes(b"own v1")
        sibling_new = self.root / "web/sibling/new.md"
        sibling_new.parent.mkdir(parents=True)
        sibling_new.write_bytes(b"sibling v1")
        self.readme.unlink()
        self.recognize({"web/own/page.md", "web/sibling/new.md"})
        changes = self.tool.refresh(
            self.tool.load_manifest(),
            adopt=True,
            only=["web/own"],
        )

        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]
        self.assertEqual(
            {
                "README.md": sha(b"readme v1"),
                "web/own/page.md": sha(b"own v1"),
            },
            recorded,
        )
        self.assertIn("adopted site web/own/page.md", changes)
        self.assertNotIn("adopted site web/sibling/new.md", changes)
        self.assertNotIn("retired site README.md", changes)

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

    def test_add_alpha_needs_no_installed_pdf_but_a_known_provider(self):
        self.tool.add_publication(
            self.tool.load_manifest(),
            "claude",
            "articles/unprinted",
            "library/faith.md",
            "alpha",
        )
        self.assertFalse((self.root / "pdf/claude/articles/unprinted.pdf").exists())
        record = json.loads(
            (self.root / "release/publications/claude/articles/unprinted.json").read_text()
        )
        self.assertEqual("alpha", record["status"])
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

    def test_migrated_inventory_summary_needs_no_installed_pdfs(self):
        self.tool.migrate_publications(self.tool.load_manifest())

        schema, counts = self.tool.publication_status_counts(
            self.tool.load_manifest()
        )

        self.assertEqual("records", schema)
        self.assertEqual({"alpha": 2, "hold": 0}, counts)
        summary = self.tool.publication_clearance_summary(schema, counts)
        self.assertIn("covers all 2 public-alpha publications", summary)

        self.claude_pdf.unlink()
        self.assertEqual(
            (schema, counts),
            self.tool.publication_status_counts(self.tool.load_manifest()),
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

    # The record binds the manifest's site inventory by one digest. Until
    # 2026-11-04 it carried a second copy of every (path, SHA-256) pair.

    def test_record_binds_the_inventory_by_digest_and_does_not_copy_it(self):
        self.tool.refresh(self.tool.load_manifest())

        record_text = self.record.read_text()
        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]
        self.assertNotIn("`README.md`", record_text)
        self.assertNotIn(sha(b"readme v1"), record_text)
        self.assertIn(
            f"| `release/public-alpha.json:site_sources` | `{inventory_digest(recorded)}` |",
            record_text,
        )
        self.assertEqual(
            inventory_digest(recorded), self.tool.recorded_site_digest(record_text)
        )
        # Every other section survives byte for byte.
        original = RIGHTS_TEMPLATE.format(
            gpt_hash=sha(b"gpt pdf v1"),
            claude_hash=sha(b"claude pdf v1"),
            readme_hash=sha(b"readme v1"),
        )
        header = self.tool.SITE_HEADER
        self.assertEqual(
            original[: original.index(header)], record_text[: record_text.index(header)]
        )
        self.assertTrue(record_text.endswith("## Operational controls\n\nControls text.\n"))

    def test_a_refresh_moves_only_the_digest_row(self):
        self.tool.refresh(self.tool.load_manifest())
        before = self.record.read_text().splitlines()
        self.readme.write_bytes(b"readme v2")

        self.tool.refresh(self.tool.load_manifest())

        after = self.record.read_text().splitlines()
        changed = [(old, new) for old, new in zip(before, after) if old != new]
        self.assertEqual(len(before), len(after))
        self.assertEqual(1, len(changed))
        self.assertIn(inventory_digest({"README.md": sha(b"readme v2")}), changed[0][1])

    def test_status_fails_when_one_inventory_byte_is_tampered(self):
        """A hand edit to the manifest's inventory no longer matches the record."""
        self.tool.refresh(self.tool.load_manifest())
        self.assertEqual(0, self.capture_status()[0])
        manifest = self.read_manifest()
        site_sources = manifest["authorizations"]["auth-1"]["site_sources"]
        honest = inventory_digest(site_sources)
        recorded_hash = site_sources["README.md"]
        site_sources["README.md"] = (
            ("1" if recorded_hash[0] == "0" else "0") + recorded_hash[1:]
        )
        self.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        code, lines = self.capture_status()

        self.assertEqual(1, code)
        digest_lines = [line for line in lines if "site-source digest" in line]
        self.assertEqual(1, len(digest_lines), lines)
        self.assertIn(f"recorded {honest}", digest_lines[0])
        self.assertIn(f"manifest {inventory_digest(site_sources)}", digest_lines[0])
        self.assertIn("stale: 2 stale binding(s)", lines[-1])

    def test_status_fails_when_the_recorded_digest_is_tampered(self):
        self.tool.refresh(self.tool.load_manifest())
        text = self.record.read_text()
        digest = self.tool.recorded_site_digest(text)
        forged = ("1" if digest[0] == "0" else "0") + digest[1:]
        self.record.write_text(text.replace(digest, forged))

        code, lines = self.capture_status()

        self.assertEqual(1, code)
        self.assertEqual(
            [
                f"stale site-source digest: recorded {forged}, manifest {digest}",
                "stale rights_record_sha256",
                "stale: 2 stale binding(s)",
            ],
            lines,
        )

    def test_status_refuses_a_per_path_table_or_edited_prose(self):
        """Only the generated form is read; a legacy copy is a divergence."""
        manifest = self.read_manifest()
        manifest["authorizations"]["auth-1"]["rights_record_sha256"] = sha(
            self.record.read_bytes()
        )
        self.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        code, lines = self.capture_status()

        self.assertEqual(1, code)
        self.assertEqual(
            "stale site-source digest: rights record site-source section is not "
            "in its generated digest form",
            lines[0],
        )

        self.tool.refresh(self.tool.load_manifest())
        self.record.write_text(
            self.record.read_text().replace("authoritative inventory", "inventory")
        )
        with self.assertRaises(self.tool.BindingError):
            self.tool.recorded_site_digest(self.record.read_text())

    def test_approval_states_the_digest_it_verified(self):
        self.tool.refresh(self.tool.load_manifest())
        recorded = self.read_manifest()["authorizations"]["auth-1"]["site_sources"]

        self.tool.approve(
            self.tool.load_manifest(), "Approve the snapshot.", "America/Chicago"
        )

        supplement = self.record.read_text().split("## Exact approved snapshots")[0]
        self.assertIn(f"`{inventory_digest(recorded)}`", supplement)
        self.assertEqual(0, self.tool.report_status(self.tool.load_manifest()))

    def test_digest_row_stays_out_of_the_browser_product_identity(self):
        """A refresh must not invalidate browser products, as the rows never did."""
        sys.path.insert(0, str(REPO / "scripts"))
        try:
            import _browser_products as products
        finally:
            sys.path.remove(str(REPO / "scripts"))
        self.tool.refresh(self.tool.load_manifest())
        before = self.record.read_bytes()
        self.readme.write_bytes(b"readme v2")
        self.tool.refresh(self.tool.load_manifest())
        after = self.record.read_bytes()

        self.assertNotEqual(before, after)
        self.assertEqual(products._rights(before), products._rights(after))


if __name__ == "__main__":
    unittest.main()
