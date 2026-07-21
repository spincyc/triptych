from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPOSITORY_ROOT / "scripts/public-alpha"


def load_tool():
    loader = importlib.machinery.SourceFileLoader("test_public_alpha_tool", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load scripts/public-alpha")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PublicAlphaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.tool = load_tool()
        self.tool.ROOT = self.root
        self.tool.MANIFEST_PATH = self.root / "release/public-alpha.json"
        self.tool.TEMPLATE_ROOT = self.root / "release/public-alpha"
        self.tool.OUTPUT_ROOT = self.root / "build/public-alpha"
        self.tool.PAGE_MAP = {
            "README.md": "index.html",
            "library/test.md": "library/test.html",
        }
        self.tool.SITE_SOURCE_PATHS = set(self.tool.PAGE_MAP) | {
            "LICENSES/MIT.txt",
            "release/public-alpha/layout.html",
            "release/public-alpha/assets/site.css",
            "requirements-public-alpha.txt",
            "scripts/public-alpha",
        }
        self.write("README.md", b"# Test\n")
        self.write(
            "library/test.md",
            b"# Test shelf\n\n[Work](../doc/gpt/work.pdf)\n",
        )
        self.write("release/public-alpha/layout.html", b"{{CONTENT}}\n")
        self.write("release/public-alpha/assets/site.css", b"body {}\n")
        self.write("requirements-public-alpha.txt", b"Markdown==3.10.2\n")
        self.write("scripts/public-alpha", b"test generator\n")
        self.write("release/rights/approval.md", b"stale approval record\n")
        self.write("src/gpt/work/main.tex", b"source\n")
        self.write("doc/gpt/work.pdf", b"current pdf bytes\n")
        self.write("LICENSES/MIT.txt", b"test license\n")
        self.manifest = self.make_manifest()
        self.write_manifest()

    def write(self, relative: str, data: bytes) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def make_manifest(self) -> dict:
        stale_hash = "0" * 64
        return {
            "schema_version": 2,
            "release_id": "public-alpha",
            "provider": "gpt",
            "authorizations": {
                "test-authorization": {
                    "basis": "user-attested",
                    "authority_role": "test release authority",
                    "authority_scope": sorted(self.tool.REQUIRED_AUTHORITY_SCOPE),
                    "rights_record": "release/rights/approval.md",
                    "rights_record_sha256": stale_hash,
                    "site_sources": {
                        path: stale_hash for path in sorted(self.tool.SITE_SOURCE_PATHS)
                    },
                    "approved_on": "2020-01-01",
                    "duration": "perpetual",
                    "effective_at": "2020-01-01T00:00:00+00:00",
                    "expires_at": None,
                    "timezone": "UTC",
                    "conditions": ["no-project-initiated-promotion"],
                }
            },
            "gates": {"rights": "Rights review is required."},
            "publications": [
                {
                    "id": "work",
                    "status": "release",
                    "catalog": "library/test.md",
                    "gates": [],
                    "approval": {
                        "authorization": "test-authorization",
                        "pdf_sha256": stale_hash,
                    },
                }
            ],
            "expected_counts": {
                "publications": 1,
                "release": 1,
                "review": 0,
                "hold": 0,
            },
        }

    def write_manifest(self) -> None:
        self.write(
            "release/public-alpha.json",
            (json.dumps(self.manifest, indent=2) + "\n").encode(),
        )

    def add_unapproved_publication(
        self,
        publication_id: str,
        status: str,
        *,
        catalog: str = "library/test.md",
        install_pdf: bool = False,
        link_catalog: str | None = None,
    ) -> None:
        if status not in {"hold", "review"}:
            raise ValueError(f"unsupported unapproved status: {status}")
        self.write(f"src/gpt/{publication_id}/main.tex", b"source\n")
        if install_pdf:
            self.write(f"doc/gpt/{publication_id}.pdf", b"publication pdf bytes\n")
        if link_catalog is not None:
            catalog_path = self.root / link_catalog
            existing = catalog_path.read_bytes() if catalog_path.is_file() else b""
            self.write(
                link_catalog,
                existing
                + f"\n[{publication_id}](../doc/gpt/{publication_id}.pdf)\n".encode(),
            )
        if not install_pdf:
            catalog_path = self.root / catalog
            if catalog_path.is_file():
                existing = catalog_path.read_bytes()
                self.write(
                    catalog,
                    existing
                    + (
                        f"\n{publication_id} private row "
                        f"<!-- triptych-publication-id: {publication_id} -->\n"
                    ).encode(),
                )
        self.manifest["publications"].append(
            {
                "id": publication_id,
                "status": status,
                "catalog": catalog,
                "gates": ["rights"],
                "approval": None,
            }
        )
        statuses = [
            publication["status"] for publication in self.manifest["publications"]
        ]
        self.manifest["expected_counts"] = {
            "publications": len(statuses),
            "release": statuses.count("release"),
            "review": statuses.count("review"),
            "hold": statuses.count("hold"),
        }

    def authorize_current_inputs(self) -> None:
        """Make the synthetic authorization exactly match the fixture files."""
        authorization = self.manifest["authorizations"]["test-authorization"]
        authorization["site_sources"] = {
            source_path: digest((self.root / source_path).read_bytes())
            for source_path in sorted(self.tool.SITE_SOURCE_PATHS)
        }
        publication_rows = []
        for publication in self.manifest["publications"]:
            if publication["status"] != "release":
                continue
            pdf_path = self.root / "doc/gpt" / f"{publication['id']}.pdf"
            pdf_hash = digest(pdf_path.read_bytes())
            publication["approval"]["pdf_sha256"] = pdf_hash
            publication_rows.append((publication["id"], pdf_hash))
        record_lines = ["# Approval", "", "## Exact approved snapshots", ""]
        record_lines.extend(
            f"| `{publication_id}` | `{pdf_hash}` |"
            for publication_id, pdf_hash in sorted(publication_rows)
        )
        record_lines.extend(
            ["", "## Exact approved reader-facing site sources", ""]
        )
        record_lines.extend(
            f"| `{source_path}` | `{source_hash}` |"
            for source_path, source_hash in sorted(authorization["site_sources"].items())
        )
        record = ("\n".join(record_lines) + "\n").encode()
        self.write("release/rights/approval.md", record)
        authorization["rights_record_sha256"] = digest(record)
        self.write_manifest()

    def tracked_bytes(self) -> dict[str, bytes]:
        return {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }

    def run_main(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", [str(TOOL_PATH), *arguments]):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = self.tool.main()
        return result, stdout.getvalue(), stderr.getvalue()

    def test_prepare_emits_deterministic_read_only_inventory_despite_stale_bindings(
        self,
    ) -> None:
        with self.assertRaises(self.tool.ReleaseError):
            self.tool.validate_manifest(self.manifest)

        before = self.tracked_bytes()
        first_result, first_stdout, first_stderr = self.run_main("prepare")
        second_result, second_stdout, second_stderr = self.run_main("prepare")

        self.assertEqual(first_result, 0)
        self.assertEqual(second_result, 0)
        self.assertEqual(first_stderr, "")
        self.assertEqual(second_stderr, "")
        self.assertEqual(first_stdout, second_stdout)
        self.assertEqual(before, self.tracked_bytes())

        inventory = json.loads(first_stdout)
        self.assertFalse(inventory["approval_conferred"])
        self.assertIn("NOT AN APPROVAL OR AUTHORIZATION", inventory["notice"])
        self.assertIn("do not attest rights", inventory["notice"])
        self.assertEqual(
            inventory["pdfs"],
            [
                {
                    "id": "work",
                    "path": "doc/gpt/work.pdf",
                    "sha256": digest(b"current pdf bytes\n"),
                }
            ],
        )
        self.assertEqual(
            [entry["path"] for entry in inventory["site_sources"]],
            sorted(self.tool.SITE_SOURCE_PATHS),
        )
        self.assertNotEqual(
            inventory["pdfs"][0]["sha256"],
            self.manifest["publications"][0]["approval"]["pdf_sha256"],
        )

    def test_prepare_fails_closed_on_nonexhaustive_scope(self) -> None:
        self.write("src/gpt/unregistered/main.tex", b"unregistered\n")

        result, stdout, stderr = self.run_main("prepare")

        self.assertEqual(result, 1)
        self.assertEqual(stdout, "")
        self.assertIn("manifest/source mismatch", stderr)
        self.assertIn("unregistered", stderr)

    def test_source_only_hold_is_valid_and_omitted_from_candidate_pdfs(self) -> None:
        self.add_unapproved_publication("held-work", "hold")
        self.authorize_current_inputs()

        publications = self.tool.validate_manifest(self.manifest)
        inventory = self.tool.prepare_candidate_inventory(self.manifest)

        self.assertEqual(publications["held-work"]["status"], "hold")
        self.assertEqual([entry["id"] for entry in inventory["pdfs"]], ["work"])

    def test_source_only_hold_catalog_entry_is_filtered_from_every_build(self) -> None:
        self.add_unapproved_publication("held-work", "hold")
        catalog = (self.root / "library/test.md").read_text(encoding="utf-8")

        public_catalog = self.tool.filter_catalog(
            "library/test.md", catalog, {"work"}
        )
        empty_catalog = self.tool.filter_catalog("library/test.md", catalog, set())

        self.assertIn("../doc/gpt/work.pdf", public_catalog)
        self.assertNotIn("held-work", public_catalog)
        self.assertNotIn("held-work", empty_catalog)
        self.assertIn("No publications from this section are included", empty_catalog)

        with mock.patch.object(
            self.tool,
            "render_page",
            side_effect=lambda source, markdown, output, preview, authorization: markdown,
        ):
            public_page = self.tool.render_source_page(
                "library/test.md",
                "library/test.html",
                {"work"},
                False,
                {},
            )
            preview_page = self.tool.render_source_page(
                "library/test.md",
                "library/test.html",
                {"work"},
                True,
                {},
            )
        for page in (public_page, preview_page):
            self.assertIn("Work", page)
            self.assertNotIn("held-work", page)
            self.assertNotIn("triptych-publication-id", page)

    def test_source_only_hold_requires_catalog_identity(self) -> None:
        self.add_unapproved_publication("held-work", "hold")
        catalog_path = self.root / "library/test.md"
        catalog_path.write_text(
            catalog_path.read_text(encoding="utf-8").replace(
                "\nheld-work private row "
                "<!-- triptych-publication-id: held-work -->\n",
                "\n",
            ),
            encoding="utf-8",
        )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "held-work: source-only hold entries require exactly one "
            "marked catalog identity, found 0",
            str(failure.exception),
        )

    def test_source_only_hold_rejects_duplicate_catalog_identity(self) -> None:
        self.add_unapproved_publication("held-work", "hold")
        catalog_path = self.root / "library/test.md"
        with catalog_path.open("a", encoding="utf-8") as stream:
            stream.write(
                "held-work duplicate private row "
                "<!-- triptych-publication-id: held-work -->\n"
            )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "held-work: expected at most one marked catalog identity, found 2",
            str(failure.exception),
        )

    def test_source_only_hold_rejects_wrong_catalog_identity(self) -> None:
        self.write("library/other.md", b"# Other shelf\n")
        self.add_unapproved_publication(
            "held-work", "hold", catalog="library/other.md"
        )
        other = self.root / "library/other.md"
        marker = (
            "held-work private row "
            "<!-- triptych-publication-id: held-work -->\n"
        )
        other.write_text(
            other.read_text(encoding="utf-8").replace("\n" + marker, "\n"),
            encoding="utf-8",
        )
        with (self.root / "library/test.md").open("a", encoding="utf-8") as stream:
            stream.write("\n" + marker)
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "held-work: manifest catalog 'library/other.md' does not match "
            "marked identity 'library/test.md'",
            str(failure.exception),
        )

    def test_catalog_rejects_unmanifested_marked_identity(self) -> None:
        with (self.root / "library/test.md").open("a", encoding="utf-8") as stream:
            stream.write(
                "\nghost private row "
                "<!-- triptych-publication-id: ghost-work -->\n"
            )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "marked catalog identities absent from manifest: ['ghost-work']",
            str(failure.exception),
        )

    def test_render_removes_private_supporting_records_column(self) -> None:
        self.write(
            "library/test.md",
            (
                "# Test shelf\n\n"
                "| Publication | Supporting records |\n"
                "| --- | --- |\n"
                "| [Work](../doc/gpt/work.pdf) | "
                "[Source map](../src/gpt/work/research/module-map.md) |\n"
            ).encode(),
        )
        with mock.patch.object(
            self.tool,
            "render_page",
            side_effect=lambda source, markdown, output, preview, authorization: markdown,
        ):
            rendered = self.tool.render_source_page(
                "library/test.md",
                "library/test.html",
                {"work"},
                False,
                {},
            )

        self.assertIn("Publication", rendered)
        self.assertIn("Work", rendered)
        self.assertNotIn("Supporting records", rendered)
        self.assertNotIn("Source map", rendered)

    def test_unmanifested_installed_pdf_is_rejected(self) -> None:
        self.authorize_current_inputs()
        self.write("doc/gpt/unmanifested.pdf", b"unmanifested pdf bytes\n")

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "manifest/PDF mismatch: unmanifested=['unmanifested']",
            str(failure.exception),
        )

    def test_release_entry_requires_installed_pdf(self) -> None:
        self.authorize_current_inputs()
        (self.root / "doc/gpt/work.pdf").unlink()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "work: release entries require an installed PDF",
            str(failure.exception),
        )

    def test_review_entry_requires_installed_pdf(self) -> None:
        self.add_unapproved_publication("review-work", "review")
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "review-work: review entries require an installed PDF",
            str(failure.exception),
        )

    def test_source_only_hold_rejects_catalog_pdf_link(self) -> None:
        self.add_unapproved_publication(
            "held-work",
            "hold",
            link_catalog="library/test.md",
        )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "held-work: source-only hold entries require zero catalog PDF links, found 1",
            str(failure.exception),
        )

    def test_source_only_hold_requires_existing_catalog(self) -> None:
        self.add_unapproved_publication(
            "held-work",
            "hold",
            catalog="library/missing.md",
        )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "held-work: missing catalog library/missing.md",
            str(failure.exception),
        )

    def test_installed_pdf_requires_catalog_link(self) -> None:
        self.add_unapproved_publication("held-work", "hold", install_pdf=True)
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "held-work: expected one catalog link, found 0",
            str(failure.exception),
        )

    def test_installed_pdf_link_must_match_manifest_catalog(self) -> None:
        self.write("library/other.md", b"# Other shelf\n")
        self.add_unapproved_publication(
            "held-work",
            "hold",
            catalog="library/other.md",
            install_pdf=True,
            link_catalog="library/test.md",
        )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "held-work: manifest catalog 'library/other.md' does not match "
            "'library/test.md'",
            str(failure.exception),
        )

    def test_installed_pdf_rejects_multiple_catalog_links(self) -> None:
        catalog = self.root / "library/test.md"
        catalog.write_bytes(
            catalog.read_bytes() + b"\n[Work again](../doc/gpt/work.pdf)\n"
        )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "work: expected one catalog link, found 2",
            str(failure.exception),
        )

    def test_check_binds_every_artifact_input_while_prepare_reports_missing_bindings(
        self,
    ) -> None:
        self.authorize_current_inputs()
        authorization = self.manifest["authorizations"]["test-authorization"]
        authorization["site_sources"].pop("scripts/public-alpha")
        authorization["site_sources"].pop("requirements-public-alpha.txt")
        authorization["site_sources"].pop("LICENSES/MIT.txt")
        self.write_manifest()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)
        self.assertIn("site_sources mismatch", str(failure.exception))
        self.assertIn("scripts/public-alpha", str(failure.exception))
        self.assertIn("requirements-public-alpha.txt", str(failure.exception))
        self.assertIn("LICENSES/MIT.txt", str(failure.exception))

        result, stdout, stderr = self.run_main("prepare")
        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        inventory = json.loads(stdout)
        candidate_paths = {entry["path"] for entry in inventory["site_sources"]}
        self.assertTrue(
            {
                "scripts/public-alpha",
                "requirements-public-alpha.txt",
                "LICENSES/MIT.txt",
            }.issubset(candidate_paths)
        )
        self.assertFalse(inventory["approval_conferred"])

        for command in ("check", "build", "verify"):
            with self.subTest(command=command):
                with mock.patch.object(self.tool, "build_site") as build_site:
                    with mock.patch.object(self.tool, "verify_output") as verify_output:
                        command_result, command_stdout, command_stderr = self.run_main(
                            command
                        )
                self.assertEqual(command_result, 1)
                self.assertEqual(command_stdout, "")
                self.assertIn("site_sources mismatch", command_stderr)
                build_site.assert_not_called()
                verify_output.assert_not_called()

    def test_changed_artifact_inputs_invalidate_exact_authorization(self) -> None:
        for source_path in (
            "scripts/public-alpha",
            "requirements-public-alpha.txt",
            "LICENSES/MIT.txt",
        ):
            with self.subTest(source_path=source_path):
                original = (self.root / source_path).read_bytes()
                self.authorize_current_inputs()
                self.write(source_path, original + b"changed\n")
                with self.assertRaises(self.tool.ReleaseError) as failure:
                    self.tool.validate_manifest(self.manifest)
                self.assertIn(
                    f"site source {source_path} does not match its approved SHA-256",
                    str(failure.exception),
                )
                self.write(source_path, original)

    def test_renderer_must_match_bound_dependency_lock(self) -> None:
        with mock.patch.object(
            self.tool, "distribution_version", return_value="0.0-test-mismatch"
        ):
            with self.assertRaises(self.tool.ReleaseError) as failure:
                self.tool.require_locked_markdown_dependency()
        self.assertIn("does not match the bound dependency lock", str(failure.exception))

    def test_temporary_release_requires_request_time_controls(self) -> None:
        self.authorize_current_inputs()
        authorization = self.manifest["authorizations"]["test-authorization"]
        authorization["duration"] = "temporary"
        authorization["expires_at"] = "2099-01-02T00:00:00+00:00"
        authorization["conditions"] = ["no-project-initiated-promotion"]

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)
        self.assertIn(
            "temporary releases require 'unadvertised-public-hosting'",
            str(failure.exception),
        )

    def test_pages_rejects_artifacts_that_need_request_time_controls(self) -> None:
        self.authorize_current_inputs()
        authorization = self.manifest["authorizations"]["test-authorization"]
        authorization["duration"] = "temporary"
        authorization["expires_at"] = "2099-01-02T00:00:00+00:00"
        authorization["conditions"] = [
            "no-project-initiated-promotion",
            "unadvertised-public-hosting",
        ]
        publications = self.tool.validate_manifest(self.manifest)
        aggregate = self.tool.artifact_authorization(
            self.manifest,
            self.tool.included_publications(publications, False),
        )
        expected = self.tool.expected_artifact_files(
            self.manifest,
            publications,
            False,
            aggregate,
        )
        self.assertIn("_worker.js", expected)
        self.assertIn("_headers", expected)
        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_deployment_target(aggregate, "github-pages")
        self.assertIn("cannot enforce", str(failure.exception))

    def test_pages_accepts_current_perpetual_indexable_profile(self) -> None:
        self.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        aggregate = self.tool.artifact_authorization(
            self.manifest,
            self.tool.included_publications(publications, False),
        )
        self.tool.validate_deployment_target(aggregate, "github-pages")

    def test_pages_workflow_requests_target_compatibility_verification(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "python scripts/public-alpha verify --deployment-target github-pages",
            workflow,
        )
        self.assertLess(
            workflow.index("--deployment-target github-pages"),
            workflow.index("actions/upload-pages-artifact"),
        )

    def test_verify_cli_enforces_named_deployment_target(self) -> None:
        publications = self.tool.publication_map(self.manifest)
        with mock.patch.object(self.tool, "load_manifest", return_value=self.manifest):
            with mock.patch.object(
                self.tool, "validate_manifest", return_value=publications
            ):
                with mock.patch.object(self.tool, "verify_output") as verify_output:
                    with mock.patch.object(
                        self.tool, "validate_deployment_target"
                    ) as validate_target:
                        result, stdout, stderr = self.run_main(
                            "verify", "--deployment-target", "github-pages"
                        )
        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        self.assertIn("verified build/public-alpha/site", stdout)
        verify_output.assert_called_once()
        validate_target.assert_called_once()
        self.assertEqual(validate_target.call_args.args[1], "github-pages")

    def test_preview_records_and_verifies_review_snapshot_without_approval(self) -> None:
        self.write("src/gpt/review-work/main.tex", b"review source\n")
        self.write("doc/gpt/review-work.pdf", b"review pdf bytes\n")
        self.write(
            "library/test.md",
            (
                "# Test shelf\n\n"
                "[Work](../doc/gpt/work.pdf)\n\n"
                "[Review](../doc/gpt/review-work.pdf)\n"
            ).encode(),
        )
        self.manifest["publications"].append(
            {
                "id": "review-work",
                "status": "review",
                "catalog": "library/test.md",
                "gates": ["rights"],
                "approval": None,
            }
        )
        self.manifest["expected_counts"].update(
            {"publications": 2, "release": 1, "review": 1, "hold": 0}
        )
        self.authorize_current_inputs()
        publications = self.tool.validate_manifest(
            self.manifest, require_active_release=False
        )

        rendered_page = (
            '<!doctype html><meta name="robots" content="noindex, nofollow, '
            'noarchive, nosnippet, noimageindex"><title>test</title>\n'
        )
        with mock.patch.object(
            self.tool, "render_source_page", return_value=rendered_page
        ):
            output = self.tool.build_site(self.manifest, publications, preview=True)
            self.tool.verify_output(self.manifest, publications, output, preview=True)

        artifact_manifest = json.loads(
            (output / "PUBLICATION-MANIFEST.json").read_text(encoding="utf-8")
        )
        review_entry = next(
            entry
            for entry in artifact_manifest["publications"]
            if entry["id"] == "review-work"
        )
        self.assertIsNone(review_entry["authorization"])
        self.assertEqual(
            review_entry["pdf_sha256"], digest(b"review pdf bytes\n")
        )

    def test_build_site_does_not_perform_the_independent_verification(self) -> None:
        publications = self.tool.publication_map(self.manifest)
        with mock.patch.object(
            self.tool,
            "render_source_page",
            return_value="<!doctype html><title>test</title>\n",
        ):
            with mock.patch.object(self.tool, "verify_output") as verify_output:
                output = self.tool.build_site(self.manifest, publications, preview=False)

        verify_output.assert_not_called()
        self.assertTrue((output / "SHA256SUMS").is_file())

    def test_build_and_verify_are_explicit_separate_commands(self) -> None:
        publications = self.tool.publication_map(self.manifest)
        output = self.tool.OUTPUT_ROOT / "site"
        with mock.patch.object(self.tool, "load_manifest", return_value=self.manifest):
            with mock.patch.object(
                self.tool, "validate_manifest", return_value=publications
            ):
                with mock.patch.object(
                    self.tool, "build_site", return_value=output
                ) as build_site:
                    with mock.patch.object(self.tool, "verify_output") as verify_output:
                        result, stdout, stderr = self.run_main("build")
        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        self.assertIn("not verified", stdout)
        self.assertIn("scripts/public-alpha verify", stdout)
        build_site.assert_called_once_with(self.manifest, publications, False)
        verify_output.assert_not_called()

        with mock.patch.object(self.tool, "load_manifest", return_value=self.manifest):
            with mock.patch.object(
                self.tool, "validate_manifest", return_value=publications
            ):
                with mock.patch.object(self.tool, "build_site") as build_site:
                    with mock.patch.object(self.tool, "verify_output") as verify_output:
                        result, stdout, stderr = self.run_main("verify")
        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        self.assertIn("verified build/public-alpha/site", stdout)
        build_site.assert_not_called()
        verify_output.assert_called_once_with(
            self.manifest,
            publications,
            self.tool.OUTPUT_ROOT / "site",
            False,
        )


if __name__ == "__main__":
    unittest.main()
