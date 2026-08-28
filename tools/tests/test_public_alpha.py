from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import html
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPOSITORY_ROOT / "tools/public-alpha"


def load_tool():
    loader = importlib.machinery.SourceFileLoader("test_public_alpha_tool", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load tools/public-alpha")
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
        self.tool.POSTCONCILIAR_QUARANTINE_BASELINE_ROWS = 1
        self.quarantine_marker = "PROJECT-CREATED PUBLIC-ALPHA QUARANTINE MUTATION"
        quarantine_hash = digest(self.quarantine_marker.encode())
        self.write(
            self.tool.POSTCONCILIAR_TRANSLATIONS_RELATIVE.as_posix(),
            (
                "[[untranslated]]\n"
                'lang = "en"\n'
                'extent = "body"\n'
                f'quarantined_text_sha256 = ["{quarantine_hash}"]\n'
            ).encode(),
        )
        self.tool.PAGE_MAP = {
            "README.md": "index.html",
            "library/curriculums.md": "library/curriculums.html",
            "library/ecclesiastical-latin.md": "library/ecclesiastical-latin.html",
            "library/test.md": "library/test.html",
        }
        self.tool.SITE_SOURCE_PATHS = set(self.tool.PAGE_MAP) | {
            "LICENSES/MIT.txt",
            "release/public-alpha/layout.html",
            "release/public-alpha/assets/site.css",
            "release/public-alpha/assets/social-card.png",
            "release/public-alpha/assets/icon.png",
            "requirements-public-alpha.txt",
            "tools/public-alpha",
        }
        self.write("README.md", b"# Test\n")
        self.write(
            "library/test.md",
            b"# Test shelf\n\n[Work](../pdf/gpt/work.pdf)\n",
        )
        self.write(
            "library/curriculums.md",
            b"# Curriculums\n\n[Ecclesiastical Latin](ecclesiastical-latin.md)\n",
        )
        self.write(
            "library/ecclesiastical-latin.md",
            b"# Ecclesiastical Latin\n\n[Return to Curriculums](curriculums.md)\n",
        )
        # The stub carries the head markers as well as the content, because the
        # link-preview metadata is verified in the built artifact: a layout that
        # renders no head would let every page pass for want of a place to fail.
        self.write(
            "release/public-alpha/layout.html",
            b'{{ROBOTS}}<link rel="apple-touch-icon" href="{{ICON_PATH}}">'
            b"{{SOCIAL}}{{CONTENT}}\n",
        )
        self.write("release/public-alpha/assets/site.css", b"body {}\n")
        # The real card and icon, because the link-preview metadata reads their
        # own dimensions out of them rather than restating a size beside them.
        for asset in ("assets/social-card.png", "assets/icon.png"):
            self.write(
                f"release/public-alpha/{asset}",
                (REPOSITORY_ROOT / "release/public-alpha" / asset).read_bytes(),
            )
        self.write(
            "requirements-public-alpha.txt",
            (REPOSITORY_ROOT / "requirements-public-alpha.txt").read_bytes(),
        )
        self.write("tools/public-alpha", b"test generator\n")
        self.write("release/rights/approval.md", b"stale approval record\n")
        self.write("src/gpt/work/main.tex", b"source\n")
        self.write("pdf/gpt/work.pdf", b"current pdf bytes\n")
        self.write("LICENSES/MIT.txt", b"test license\n")
        self.manifest = self.make_manifest()
        self.write_manifest()

    def write(self, relative: str, data: bytes) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def test_page_classes_are_semantic_and_stable(self) -> None:
        self.assertEqual(
            self.tool.page_classes("README.md", "index.html"),
            "page-shell page-home page-library-root page-spectrum",
        )
        self.assertEqual(
            self.tool.page_classes("ABOUT.md", "about.html"),
            "page-shell page-utility",
        )
        self.assertEqual(
            self.tool.page_classes("library/test.md", "library/test.html"),
            "page-shell page-catalog",
        )
        self.assertEqual(
            self.tool.page_classes("web/gpt/work.md", "web/gpt/work.html"),
            "page-shell page-reader reading",
        )
        self.assertEqual(
            self.tool.page_classes("CONTRIBUTING.md", "contributing.html"),
            "page-shell page-utility",
        )

    def test_catalog_render_rejects_internal_reader_labels(self) -> None:
        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.reject_internal_reader_labels(
                "library/test.md", "<p>PC-ANN-001</p>"
            )
        self.assertIn(
            "internal postconciliar registry identifier", str(failure.exception)
        )

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.reject_internal_reader_labels(
                "library/test.md", "<!-- triptych-publication-id: work -->"
            )
        self.assertIn("internal publication marker", str(failure.exception))

    def test_public_layout_uses_accessible_restrained_ornament_and_stable_nav(
        self,
    ) -> None:
        layout = (
            REPOSITORY_ROOT / "release/public-alpha/layout.html"
        ).read_text(encoding="utf-8")
        self.assertIn('class="triptych-mark" aria-hidden="true"', layout)
        self.assertIn('class="triptych-divider" aria-hidden="true"', layout)
        self.assertNotIn("℣", layout)
        self.assertNotIn("℟", layout)
        self.assertIn(">About</a>", layout)
        self.assertIn(">Feedback</a>", layout)
        # The library is the landing page now; a separate Library entry would be a
        # second name for Home.
        self.assertNotIn(">Library</a>", layout)
        self.assertIn(
            "AI Driven Studies in Catholic Faith, Worship, and Law",
            layout,
        )
        self.assertNotIn("Faith · Worship · Law", layout)
        self.assertNotIn("Browse the library", layout)
        self.assertNotIn("Give feedback", layout)
        self.assertIn("{{HOME_CURRENT}}", layout)
        self.assertIn("{{BREADCRUMB}}", layout)

    def render_browser_head(self, output_relative: str) -> str:
        source = REPOSITORY_ROOT / "src/web/browser" / output_relative
        tool = load_tool()
        page = tool.render_browser_page(source, output_relative, False, {})
        return page.split("</head>")[0]

    def test_canonical_public_origin_and_relative_artifact_routes_are_distinct(self) -> None:
        tool = load_tool()
        self.assertEqual(tool.SITE_ORIGIN, "https://mystago.gy")
        self.assertEqual(
            tool.public_site_url("liturgy/day.html"),
            "https://mystago.gy/liturgy/day.html",
        )
        self.assertEqual(
            tool.public_site_url(tool.SOCIAL_CARD_RELATIVE),
            "https://mystago.gy/assets/social-card.png",
        )
        for unsafe in ("", "/liturgy/day.html", "../liturgy/day.html"):
            with self.subTest(unsafe=unsafe):
                with self.assertRaises(tool.ReleaseError):
                    tool.public_site_url(unsafe)

        # Canonical metadata is absolute, but artifact navigation stays
        # relative so the same output works at the custom-domain root and in a
        # GitHub Pages project-path preview.
        self.assertEqual(
            tool.relative_link("liturgy/day.html", "index.html"),
            "../index.html",
        )

    def test_every_browser_page_carries_its_own_link_preview(self) -> None:
        """A shared preview is barely better than none, so each page states itself."""
        tool = load_tool()
        seen: dict[str, set[str]] = {"og:title": set(), "og:url": set()}
        indexed = 0
        for output_relative, source in sorted(tool.web_browser_pages().items()):
            head = tool.render_browser_page(source, output_relative, False, {}).split(
                "</head>"
            )[0]
            if f'<meta name="robots" content="{tool.ROBOTS_DIRECTIVES}">' in head:
                self.assertNotIn("og:url", head)
                self.assertNotIn(tool.SITE_ORIGIN, head)
                continue
            indexed += 1
            properties = dict(tool.SOCIAL_PROPERTY_RE.findall(head))
            names = dict(tool.SOCIAL_NAME_RE.findall(head))
            for required in ("og:type", "og:site_name", "og:title", "og:description",
                             "og:url", "og:image", "og:image:width", "og:image:height"):
                self.assertIn(required, properties, f"{output_relative} lacks {required}")
            self.assertEqual(names["twitter:card"], "summary_large_image")
            self.assertEqual(names["description"], properties["og:description"])
            # Apple's TN3156: the site name belongs in og:site_name, not in the
            # title, or the preview reads as the site repeated.
            self.assertEqual(properties["og:site_name"], tool.SITE_NAME)
            self.assertNotIn(f"· {tool.SITE_NAME}", properties["og:title"])
            self.assertEqual(
                properties["og:url"], tool.public_site_url(output_relative)
            )
            self.assertEqual(
                properties["og:image"],
                tool.public_site_url(tool.SOCIAL_CARD_RELATIVE),
            )
            seen["og:title"].add(properties["og:title"])
            seen["og:url"].add(properties["og:url"])
        self.assertEqual(len(seen["og:title"]), indexed)
        self.assertEqual(len(seen["og:url"]), indexed)

    def test_link_preview_description_matches_declared_browser_description(self) -> None:
        head = self.render_browser_head("liturgy/index.html")
        source = (
            REPOSITORY_ROOT / "src/web/browser/liturgy/index.html"
        ).read_text(encoding="utf-8")
        declared = re.search(
            r'<meta name="description" content="([^"]+)"', source
        )
        self.assertIsNotNone(declared)
        expected = html.escape(html.unescape(declared.group(1)), quote=True)
        tool = load_tool()
        properties = dict(tool.SOCIAL_PROPERTY_RE.findall(head))
        names = dict(tool.SOCIAL_NAME_RE.findall(head))
        self.assertEqual(names["description"], expected)
        self.assertEqual(properties["og:description"], expected)
        self.assertEqual(names["twitter:description"], expected)

    def test_link_preview_prefers_a_declared_description_over_a_placeholder(
        self,
    ) -> None:
        tool = load_tool()
        placeholder = '<p class="lede">Loading the plan…</p>'
        self.assertEqual(
            tool.social_description(placeholder, ""), tool.SITE_DESCRIPTION
        )
        self.assertEqual(
            tool.social_description(placeholder, "What this page is."),
            "What this page is.",
        )
        # A lede that says something is used verbatim; a later paragraph on a
        # page that already has a lede never stands in for it.
        stated = (
            '<p class="lede">The full text of any Mass in either missal, in the '
            "translations this site can publish.</p><p>Something else entirely "
            "that is quite long enough to pass the floor on its own.</p>"
        )
        self.assertTrue(tool.social_description(stated, "").startswith("The full text"))

    def test_link_preview_image_meets_apples_stated_minimums(self) -> None:
        tool = load_tool()
        width, height = tool.png_dimensions(
            REPOSITORY_ROOT / "release/public-alpha" / tool.SOCIAL_CARD_RELATIVE
        )
        self.assertGreaterEqual(width, tool.PREVIEW_IMAGE_MINIMUM_WIDTH)
        self.assertGreater(height, 0)
        side, other = tool.png_dimensions(
            REPOSITORY_ROOT / "release/public-alpha" / tool.SITE_ICON_RELATIVE
        )
        self.assertEqual(side, other)
        self.assertGreaterEqual(side, tool.PREVIEW_ICON_MINIMUM_SIDE)

    def test_link_preview_verifier_rejects_the_retired_pages_origin(self) -> None:
        output_relative = "build/link-preview-origin-test"
        output = self.root / output_relative
        for relative in (
            self.tool.SOCIAL_CARD_RELATIVE,
            self.tool.SITE_ICON_RELATIVE,
        ):
            self.write(
                f"{output_relative}/{relative}",
                (self.tool.TEMPLATE_ROOT / relative).read_bytes(),
            )
        page = (
            '<meta name="description" content="Canonical origin test">\n'
            '<link rel="apple-touch-icon" href="assets/icon.png">\n'
            + self.tool.social_meta(
                "index.html", "Canonical origin test", "Canonical origin test"
            )
        )
        self.write(f"{output_relative}/index.html", page.encode())

        self.assertEqual(self.tool.verify_link_previews(output, False, {}), [])

        stale = page.replace(
            "https://mystago.gy/", "https://spincyc.github.io/triptych/"
        )
        self.write(f"{output_relative}/index.html", stale.encode())
        errors = self.tool.verify_link_previews(output, False, {})
        self.assertTrue(
            any("og:url is not https://mystago.gy/" in error for error in errors)
        )
        self.assertTrue(
            any("og:image is not https://mystago.gy/" in error for error in errors)
        )

    def test_no_index_artifact_does_not_advertise_the_public_site(self) -> None:
        tool = load_tool()
        source = REPOSITORY_ROOT / "src/web/browser/liturgy/propers-reader.html"
        page = tool.render_browser_page(
            source, "liturgy/propers-reader.html", True, {}
        )
        self.assertNotIn("og:url", page)
        self.assertNotIn(tool.SITE_ORIGIN, page)
        # It still describes itself, for a reader and for the tab.
        self.assertIn('<meta name="description"', page)

    def test_layout_carries_the_preview_icon_and_social_markers(self) -> None:
        layout = (REPOSITORY_ROOT / "release/public-alpha/layout.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("{{SOCIAL}}", layout)
        self.assertIn('rel="apple-touch-icon"', layout)
        self.assertIn("{{ICON_PATH}}", layout)

    def test_home_browser_title_is_not_duplicated(self) -> None:
        self.assertEqual(self.tool.document_title("Triptych"), "Triptych")
        self.assertEqual(self.tool.document_title("Library"), "Library · Triptych")

    def test_home_identity_moves_to_header_and_opening_section_becomes_h1(self) -> None:
        source = (
            "# Triptych\n\n"
            "*AI Driven Studies in Catholic Faith, Worship, and Law*\n\n"
            "## Don’t Panic!\n\n"
            "Opening.\n\n"
            "## Library\n"
        )
        body = self.tool.page_body_markdown("README.md", source)
        self.assertTrue(body.startswith("# Don’t Panic!\n"))
        self.assertNotIn("# Triptych", body)
        self.assertNotIn("AI Driven Studies", body)
        self.assertIn("## Library", body)
        self.assertEqual(
            self.tool.page_body_markdown("library/test.md", source),
            source,
        )

    def test_primary_navigation_marks_the_contextual_destination(self) -> None:
        self.assertEqual(
            self.tool.navigation_state("README.md"),
            (' aria-current="page"', "", ""),
        )
        self.assertEqual(
            self.tool.navigation_state("ABOUT.md"),
            ("", ' aria-current="page"', ""),
        )
        # A shelf and a reading page are both reached from the landing page,
        # which is where the library lives.
        self.assertEqual(
            self.tool.navigation_state("library/test.md"),
            (' aria-current="page"', "", ""),
        )
        self.assertEqual(
            self.tool.navigation_state("web/gpt/work.md"),
            (' aria-current="page"', "", ""),
        )

    def test_reader_breadcrumb_uses_owning_subject_shelf(self) -> None:
        crumb = self.tool.breadcrumb(
            "web/gpt/history/catholic-exorcism/01-history-and-current-practice.md",
            "web/gpt/history/catholic-exorcism/01-history-and-current-practice.html",
        )
        self.assertIn('aria-label="Breadcrumb"', crumb)
        self.assertIn(">Library</a>", crumb)
        self.assertIn(">Catholic Exorcism</a>", crumb)
        self.assertIn("../../../../library/catholic-exorcism.html", crumb)
        self.assertIn("../../../../index.html", crumb)

    def test_markdown_table_headers_receive_column_scope(self) -> None:
        self.assertEqual(
            self.tool.add_table_header_scopes(
                "<table><thead><tr><th>Name</th><th>Focus</th></tr></thead></table>"
            ),
            '<table><thead><tr><th scope="col">Name</th>'
            '<th scope="col">Focus</th></tr></thead></table>',
        )

    def test_fenced_block_becomes_preformatted_text(self) -> None:
        import markdown

        rendered = markdown.markdown(
            "Create an experimental branch:\n\n```sh\ngit switch -c work\n```\n",
            extensions=self.tool.MARKDOWN_EXTENSIONS,
            output_format="html5",
        )
        self.assertIn('<pre><code class="language-sh">git switch -c work', rendered)
        self.tool.reject_unrendered_code_fences("CONTRIBUTING.md", rendered)

    def test_unrendered_fence_is_refused_with_its_language_named(self) -> None:
        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.reject_unrendered_code_fences(
                "CONTRIBUTING.md", "<p><code>sh\ngit switch -c work</code></p>"
            )
        message = str(failure.exception)
        self.assertIn("tagged 'sh'", message)
        self.assertIn("fenced_code", message)

    def test_untagged_unrendered_fence_is_refused(self) -> None:
        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.reject_unrendered_code_fences(
                "docs/bibles.md", "<li><code>Psalm 100:1-2\nPsalm 102:1</code></li>"
            )
        self.assertIn("fenced code block rendered", str(failure.exception))

    def test_a_wrapped_inline_code_span_is_not_a_fence(self) -> None:
        # Two live pages carry a code span whose source wraps mid-prose. Neither
        # is a fence, and a check that refused them would be unusable.
        self.tool.reject_unrendered_code_fences(
            "docs/bibles.md",
            '<p>records <code>rights_jurisdiction = "United\nStates"</code> beside it</p>',
        )

    def test_no_site_page_renders_a_fence_as_running_prose(self) -> None:
        # Nothing in the ordinary editing workflow renders these pages, which is
        # how a paragraph reading "yaml" followed by four run-together lines
        # reached readers unnoticed. This renders every one of them.
        import markdown

        tool = load_tool()
        for source_relative in sorted({**tool.PAGE_MAP, **tool.document_pages()}):
            with self.subTest(source=source_relative):
                text = (REPOSITORY_ROOT / source_relative).read_text(encoding="utf-8")
                tool.reject_unrendered_code_fences(
                    source_relative,
                    markdown.markdown(
                        tool.page_body_markdown(source_relative, text),
                        extensions=tool.MARKDOWN_EXTENSIONS,
                        output_format="html5",
                    ),
                )

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
            self.write(f"pdf/gpt/{publication_id}.pdf", b"publication pdf bytes\n")
        if link_catalog is not None:
            catalog_path = self.root / link_catalog
            existing = catalog_path.read_bytes() if catalog_path.is_file() else b""
            self.write(
                link_catalog,
                existing
                + f"\n[{publication_id}](../pdf/gpt/{publication_id}.pdf)\n".encode(),
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
                "gates": [],
                "approval": None,
            }
        )

    def publication_provider_and_leaf(self, publication_id: str) -> tuple[str, str]:
        if ":" in publication_id:
            provider, leaf = publication_id.split(":", 1)
            return provider, leaf
        return self.manifest["provider"], publication_id

    def add_claude_publication(
        self,
        leaf: str,
        status: str,
        *,
        install_pdf: bool = True,
        link_catalog: str | None = None,
        link_line: str | None = None,
    ) -> None:
        self.manifest["providers"] = ["gpt", "claude"]
        self.write(f"src/claude/{leaf}/main.tex", b"claude source\n")
        if install_pdf:
            self.write(f"pdf/claude/{leaf}.pdf", b"claude pdf bytes\n")
        if link_catalog is not None:
            catalog_path = self.root / link_catalog
            existing = catalog_path.read_bytes() if catalog_path.is_file() else b""
            addition = link_line or f"[{leaf} claude](../pdf/claude/{leaf}.pdf)"
            self.write(link_catalog, existing + f"\n{addition}\n".encode())
        if status == "release":
            gates: list[str] = []
            approval = {
                "authorization": "test-authorization",
                "pdf_sha256": "0" * 64,
            }
        else:
            gates = []
            approval = None
        self.manifest["publications"].append(
            {
                "id": f"claude:{leaf}",
                "status": status,
                "catalog": "library/test.md",
                "gates": gates,
                "approval": approval,
            }
        )

    def authorize_current_inputs(self) -> None:
        """Make the synthetic authorization exactly match the fixture files."""
        authorization = self.manifest["authorizations"]["test-authorization"]
        authorization["site_sources"] = {
            source_path: digest((self.root / source_path).read_bytes())
            for source_path in sorted(self.tool.site_source_paths())
        }
        publication_rows = []
        for publication in self.manifest["publications"]:
            if publication["status"] not in {"release", "review"}:
                continue
            provider, leaf = self.publication_provider_and_leaf(publication["id"])
            pdf_path = self.root / "pdf" / provider / f"{leaf}.pdf"
            if not pdf_path.is_file():
                continue
            pdf_hash = digest(pdf_path.read_bytes())
            if publication["status"] == "release":
                publication["approval"]["pdf_sha256"] = pdf_hash
            else:
                publication["review_distribution"] = {
                    "authorization": "test-authorization",
                    "pdf_sha256": pdf_hash,
                }
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
                    "path": "pdf/gpt/work.pdf",
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

        self.assertEqual(publications[("gpt", "held-work")]["status"], "hold")
        self.assertEqual([entry["id"] for entry in inventory["pdfs"]], ["work"])

    def test_source_only_hold_catalog_entry_is_filtered_from_every_build(self) -> None:
        self.add_unapproved_publication("held-work", "hold")
        catalog = (self.root / "library/test.md").read_text(encoding="utf-8")

        public_catalog = self.tool.filter_catalog(
            "library/test.md", catalog, {("gpt", "work")}
        )
        empty_catalog = self.tool.filter_catalog("library/test.md", catalog, set())

        self.assertIn("../pdf/gpt/work.pdf", public_catalog)
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
                {("gpt", "work")},
                False,
                {},
            )
            preview_page = self.tool.render_source_page(
                "library/test.md",
                "library/test.html",
                {("gpt", "work")},
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
                "| [Work](../pdf/gpt/work.pdf) | "
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
                {("gpt", "work")},
                False,
                {},
            )

        self.assertIn("Publication", rendered)
        self.assertIn("Work", rendered)
        self.assertNotIn("Supporting records", rendered)
        self.assertNotIn("Source map", rendered)

    def test_curriculum_landing_and_child_catalog_links_are_rewritten(self) -> None:
        with mock.patch.object(
            self.tool,
            "render_page",
            side_effect=lambda source, markdown, output, preview, authorization: markdown,
        ):
            landing = self.tool.render_source_page(
                "library/curriculums.md",
                "library/curriculums.html",
                {("gpt", "work")},
                False,
                {},
            )
            child = self.tool.render_source_page(
                "library/ecclesiastical-latin.md",
                "library/ecclesiastical-latin.html",
                {("gpt", "work")},
                False,
                {},
            )

        self.assertIn("[Ecclesiastical Latin](ecclesiastical-latin.html)", landing)
        self.assertIn("[Return to Curriculums](curriculums.html)", child)

    def test_empty_child_catalog_preserves_its_parent_backlink(self) -> None:
        self.write(
            "library/ecclesiastical-latin.md",
            (
                "# Ecclesiastical Latin\n\n"
                "[Return to Curriculums](curriculums.md)\n\n"
                "[Held](../pdf/gpt/held.pdf)\n"
            ).encode(),
        )
        with mock.patch.object(
            self.tool,
            "render_page",
            side_effect=lambda source, markdown, output, preview, authorization: markdown,
        ):
            child = self.tool.render_source_page(
                "library/ecclesiastical-latin.md",
                "library/ecclesiastical-latin.html",
                set(),
                False,
                {},
            )
        self.assertIn("[Return to Curriculums](curriculums.html)", child)
        self.assertNotIn("Return to the Library", child)

    def test_repository_page_map_includes_curriculum_child_catalog(self) -> None:
        repository_tool = load_tool()

        self.assertEqual(
            repository_tool.PAGE_MAP.get("library/ecclesiastical-latin.md"),
            "library/ecclesiastical-latin.html",
        )

    def test_unmanifested_installed_pdf_is_rejected(self) -> None:
        self.authorize_current_inputs()
        self.write("pdf/gpt/unmanifested.pdf", b"unmanifested pdf bytes\n")

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "manifest/PDF mismatch: unmanifested=['unmanifested']",
            str(failure.exception),
        )

    def test_release_entry_requires_installed_pdf(self) -> None:
        self.authorize_current_inputs()
        (self.root / "pdf/gpt/work.pdf").unlink()

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

    def test_installed_pdf_may_be_owned_by_stable_catalog_marker(self) -> None:
        self.add_unapproved_publication("held-work", "hold", install_pdf=True)
        catalog = self.root / "library/test.md"
        catalog.write_bytes(
            catalog.read_bytes()
            + b"\n<!-- triptych-publication-id: held-work -->\n"
            + b"\n| Other work |\n| --- |\n| Planned |\n"
        )
        self.authorize_current_inputs()

        publications = self.tool.validate_manifest(self.manifest)

        self.assertIn(("gpt", "held-work"), publications)

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
            catalog.read_bytes() + b"\n[Work again](../pdf/gpt/work.pdf)\n"
        )
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "work: expected one catalog link, found 2",
            str(failure.exception),
        )

    def test_candidate_inventory_discovers_inputs_without_tracked_hash_binding(
        self,
    ) -> None:
        self.authorize_current_inputs()
        authorization = self.manifest["authorizations"]["test-authorization"]
        authorization["site_sources"].pop("tools/public-alpha")
        authorization["site_sources"].pop("requirements-public-alpha.txt")
        authorization["site_sources"].pop("LICENSES/MIT.txt")
        self.write_manifest()

        self.tool.validate_manifest(self.manifest)

        result, stdout, stderr = self.run_main("prepare")
        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        inventory = json.loads(stdout)
        candidate_paths = {entry["path"] for entry in inventory["site_sources"]}
        self.assertTrue(
            {
                "tools/public-alpha",
                "requirements-public-alpha.txt",
                "LICENSES/MIT.txt",
            }.issubset(candidate_paths)
        )
        self.assertFalse(inventory["approval_conferred"])

    def test_changed_artifact_inputs_do_not_require_shared_rebinding(self) -> None:
        for source_path in (
            "tools/public-alpha",
            "requirements-public-alpha.txt",
            "LICENSES/MIT.txt",
        ):
            with self.subTest(source_path=source_path):
                original = (self.root / source_path).read_bytes()
                self.authorize_current_inputs()
                self.write(source_path, original + b"changed\n")
                self.tool.validate_manifest(self.manifest)
                self.write(source_path, original)

    def test_renderer_must_match_bound_dependency_lock(self) -> None:
        with mock.patch.object(
            self.tool, "distribution_version", return_value="0.0-test-mismatch"
        ):
            with self.assertRaises(self.tool.ReleaseError) as failure:
                self.tool.require_locked_markdown_dependency()
        self.assertIn("does not match the bound dependency lock", str(failure.exception))

    def test_long_form_contents_marker_renders_linked_unique_anchors(self) -> None:
        headings = "\n\n".join(
            f"## Part {number}\n\nText {number}."
            for number in range(1, 121)
        )
        page = self.tool.render_page(
            "web/gpt/work.md",
            f"# Work\n\n[TOC]\n\n{headings}\n",
            "web/gpt/work.html",
            False,
            self.manifest["authorizations"]["test-authorization"],
        )
        self.assertIn('<div class="toc">', page)
        self.assertEqual(page.count("<h2 id="), 120)
        self.assertEqual(page.count('<a href="#part-'), 120)
        self.assertEqual(
            len(
                {
                    fragment.split('"', 1)[0]
                    for fragment in page.split('<h2 id="')[1:]
                }
            ),
            120,
        )

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
        self.assertIn("run: make check-deployment-sources", workflow)
        self.assertIn(
            "python tools/tpt public-alpha verify --deployment-target github-pages",
            workflow,
        )
        self.assertLess(
            workflow.index("run: make check-deployment-sources"),
            workflow.index("run: make public-site"),
        )
        self.assertLess(
            workflow.index("--deployment-target github-pages"),
            workflow.index("actions/upload-pages-artifact"),
        )

    def test_root_landings_use_the_exact_section_hierarchy(self) -> None:
        expected = [
            ("Faith", "library/faith.md"),
            ("Scripture", "library/scripture.md"),
            ("Liturgy", "library/liturgy.md"),
            ("History", "library/history.md"),
            ("Formation", "library/formation.md"),
            ("Mary", "library/mariology.md"),
            ("Law", "library/law-and-church-discipline.md"),
        ]
        for landing in ("README.md",):
            text = (REPOSITORY_ROOT / landing).read_text(encoding="utf-8")
            text = text.split("## Library", 1)[1].split("## Read in the browser", 1)[0]
            section_links = [
                (label, target)
                for label, target in self.tool.MARKDOWN_LINK_RE.findall(text)
                if target.startswith("library/")
            ]
            self.assertEqual(
                section_links,
                expected,
                f"{landing} must expose only the ordered top-level sections",
            )
            self.assertFalse(
                any("#" in target for _, target in section_links),
                f"{landing} must not promote a child section through a fragment link",
            )

    def test_root_landings_do_not_promote_pictorial_dictionary_child_anchor(self) -> None:
        for landing in ("README.md", "ABOUT.md"):
            text = (REPOSITORY_ROOT / landing).read_text(encoding="utf-8")
            self.assertNotIn("sanctuary-pictorial-dictionaries", text)

    def test_root_landings_use_the_approved_section_descriptions(self) -> None:
        descriptions = (
            "Doctrine, theology, sacraments, virtues, and apologetics.",
            "Biblical studies, translations, textual history, and reception.",
            "The 1962 and postconciliar Roman rites, propers, and calendars.",
            "Biographies, parishes, institutes, and exorcism.",
            "Prayer, novenas, devotions, and curricula.",
            "Dogmas, prayer, apparitions, and history.",
            "Canon law, Church discipline, and heresies.",
        )
        for landing in ("README.md",):
            text = (REPOSITORY_ROOT / landing).read_text(encoding="utf-8")
            for description in descriptions:
                self.assertEqual(text.count(description), 1)

    def test_section_ornaments_are_distinct_and_vr_are_liturgy_only(self) -> None:
        css = (
            REPOSITORY_ROOT / "release/public-alpha/assets/site.css"
        ).read_text(encoding="utf-8")
        expected = {
            "white": ("☧", "✠"),
            "gold": ("α", "ω"),
            "red": ("℣", "℟"),
            "green": ("❦", "✣"),
            "violet": ("✦", "❖"),
            "rose": ("✷", "✥"),
            "black": ("§", "¶"),
        }
        for color, symbols in expected.items():
            block = re.search(
                rf"\.section-{color}\s*\{{(?P<body>.*?)\n\}}",
                css,
                flags=re.DOTALL,
            )
            self.assertIsNotNone(block)
            body = block.group("body")
            self.assertIn(f'--section-symbol-primary: "{symbols[0]}"', body)
            self.assertIn(f'--section-symbol-secondary: "{symbols[1]}"', body)
        self.assertEqual(css.count("℣"), 2)
        self.assertEqual(css.count("℟"), 1)

    def test_public_palette_is_light_and_section_color_reaches_reading_pages(self) -> None:
        css = (
            REPOSITORY_ROOT / "release/public-alpha/assets/site.css"
        ).read_text(encoding="utf-8")
        self.assertIn("color-scheme: only light", css)
        self.assertNotIn("prefers-color-scheme: dark", css)
        self.assertIn("--paper: #ece7de", css)
        self.assertIn("--surface: #f8f5ef", css)
        accents = {
            color: re.search(
                rf"\.section-{color}\s*\{{.*?--section-accent:\s*(#[0-9a-f]{{6}})",
                css,
                flags=re.DOTALL,
            ).group(1)
            for color in ("white", "gold", "red", "green", "violet", "rose", "black")
        }
        self.assertEqual(len(set(accents.values())), 7)
        for token in (
            "--section-pale:",
            "--section-row:",
            "--section-line:",
            ".section-toned h2",
            ".section-toned blockquote",
            ".section-toned tbody tr:nth-child(even)",
            ".section-toned > h2::before",
        ):
            self.assertIn(token, css)

    def test_landing_page_headings_do_not_skip_levels(self) -> None:
        for relative in sorted(self.tool.PAGE_MAP):
            if relative.startswith("release/") or relative in {"LICENSE", "THIRD_PARTY.md"}:
                continue
            path = REPOSITORY_ROOT / relative
            if not path.is_file():
                continue
            previous = None
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = re.match(r"^(#{1,6})\s", line)
                if match is None:
                    continue
                level = len(match.group(1))
                if previous is not None:
                    self.assertLessEqual(
                        level,
                        previous + 1,
                        f"{relative}:{number} skips from h{previous} to h{level}",
                    )
                previous = level

    def test_child_catalogs_link_only_through_their_parent_sections(self) -> None:
        relationships = (
            (
                "library/history.md",
                "catholic-exorcism.md",
                "library/catholic-exorcism.md",
                "history.md",
            ),
            (
                "library/curriculums.md",
                "ecclesiastical-latin.md#chatgpt-edition",
                "library/ecclesiastical-latin.md",
                "curriculums.md",
            ),
        )
        for parent_path, child_target, child_path, return_target in relationships:
            parent = (REPOSITORY_ROOT / parent_path).read_text(encoding="utf-8")
            child = (REPOSITORY_ROOT / child_path).read_text(encoding="utf-8")
            parent_targets = [
                target for _, target in self.tool.MARKDOWN_LINK_RE.findall(parent)
            ]
            child_targets = [
                target for _, target in self.tool.MARKDOWN_LINK_RE.findall(child)
            ]
            self.assertEqual(parent_targets.count(child_target), 1)
            self.assertEqual(child_targets.count(return_target), 1)

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

    def test_public_site_records_and_reaches_legacy_review_as_alpha(self) -> None:
        self.write("src/gpt/review-work/main.tex", b"review source\n")
        self.write("pdf/gpt/review-work.pdf", b"review pdf bytes\n")
        self.write(
            "library/test.md",
            (
                "# Test shelf\n\n"
                "[Work](../pdf/gpt/work.pdf)\n\n"
                "[Review copy](../pdf/gpt/review-work.pdf)\n"
            ).encode(),
        )
        self.manifest["publications"].append(
            {
                "id": "review-work",
                "status": "review",
                "catalog": "library/test.md",
                "gates": [],
                "approval": None,
            }
        )
        self.authorize_current_inputs()
        publications = self.tool.validate_manifest(
            self.manifest, require_active_release=False
        )

        output = self.tool.build_site(self.manifest, publications, preview=False)
        self.tool.verify_output(self.manifest, publications, output, preview=False)

        artifact_manifest = json.loads(
            (output / "PUBLICATION-MANIFEST.json").read_text(encoding="utf-8")
        )
        review_entry = next(
            entry
            for entry in artifact_manifest["publications"]
            if entry["id"] == "review-work"
        )
        self.assertEqual(review_entry["authorization"], "test-authorization")
        self.assertEqual(review_entry["status"], "alpha")
        self.assertNotIn("gates", review_entry)
        self.assertEqual(
            review_entry["pdf_sha256"], digest(b"review pdf bytes\n")
        )
        self.assertTrue((output / "pdf/gpt/review-work.pdf").is_file())
        catalog = (output / "library/test.html").read_text(encoding="utf-8")
        self.assertIn('href="../pdf/gpt/review-work.pdf"', catalog)

    def test_alpha_catalog_link_may_use_terse_reader_label(self) -> None:
        self.add_unapproved_publication(
            "review-work",
            "review",
            install_pdf=True,
            link_catalog="library/test.md",
        )
        catalog_path = self.root / "library/test.md"
        catalog_path.write_text(
            catalog_path.read_text(encoding="utf-8").replace(
                "[review-work]", "[Draft]"
            ),
            encoding="utf-8",
        )
        self.authorize_current_inputs()

        publications = self.tool.validate_manifest(self.manifest)
        self.assertIn(("gpt", "review-work"), publications)

    def build_verified_artifact(self) -> tuple[dict, Path]:
        """A settled tree, built and proven to verify, for a test to then break."""
        self.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        output = self.tool.build_site(self.manifest, publications, preview=False)
        self.tool.verify_output(self.manifest, publications, output, preview=False)
        return publications, output

    def test_verifier_passes_when_every_site_source_matches_its_approved_hash(
        self,
    ) -> None:
        publications, output = self.build_verified_artifact()

        self.assertEqual([], self.tool.site_source_binding_errors(self.manifest))
        self.tool.verify_output(self.manifest, publications, output, preview=False)

    def test_verifier_rejects_a_site_source_that_no_longer_matches_its_hash(
        self,
    ) -> None:
        publications, output = self.build_verified_artifact()
        approved = self.manifest["authorizations"]["test-authorization"][
            "site_sources"
        ]["tools/public-alpha"]
        # A bound input that no page renders from: the artifact is untouched, so
        # only the attestation is wrong, which is the case that used to pass.
        self.write("tools/public-alpha", b"test generator v2\n")

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.verify_output(self.manifest, publications, output, preview=False)

        message = str(failure.exception)
        self.assertIn(
            "site source tools/public-alpha does not match its approved SHA-256",
            message,
        )
        self.assertIn(approved, message)
        self.assertIn(digest(b"test generator v2\n"), message)
        self.assertIn("make refresh-release-bindings ADOPT=1", message)

    def test_verifier_rejects_a_site_source_whose_file_is_gone(self) -> None:
        publications, output = self.build_verified_artifact()
        (self.root / "tools/public-alpha").unlink()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertIn(
            "site source does not exist: tools/public-alpha",
            str(failure.exception),
        )

    def test_verifier_rejects_a_recognized_site_source_the_record_omits(
        self,
    ) -> None:
        """Hashing the record alone reports exact over an input it never names."""
        publications, output = self.build_verified_artifact()
        del self.manifest["authorizations"]["test-authorization"]["site_sources"][
            "tools/public-alpha"
        ]

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.verify_output(self.manifest, publications, output, preview=False)

        message = str(failure.exception)
        self.assertIn(
            "site source tools/public-alpha is recognized by the renderer and "
            "is not in the approved record",
            message,
        )
        self.assertIn("make refresh-release-bindings ADOPT=1", message)

    def test_verifier_rejects_a_recorded_site_source_nothing_renders(self) -> None:
        """A hash attesting a file the release does not use is a false record."""
        publications, output = self.build_verified_artifact()
        self.write("notes/retired.md", b"retired\n")
        self.manifest["authorizations"]["test-authorization"]["site_sources"][
            "notes/retired.md"
        ] = digest(b"retired\n")

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertIn(
            "site source notes/retired.md is recorded but the renderer no "
            "longer reads it",
            str(failure.exception),
        )

    def test_site_source_graph_keeps_every_copied_browser_and_data_input(self) -> None:
        bible_manifest = {
            "bibles": [
                {
                    "id": "offered",
                    "label": "Offered",
                    "language": "la",
                    "numbering": "vulgate",
                    "psalter": "gallican",
                    "rights": "public-domain",
                }
            ]
        }
        self.write(
            "src/web/data/bibles.json",
            (json.dumps(bible_manifest) + "\n").encode(),
        )
        self.write("src/sources/bibles/offered/chapters/Ps/1.json", b"{}\n")

        browser_inputs = {"src/web/browser/shared/browser-core.js"}
        self.write("src/web/browser/shared/browser-core.js", b"// shared\n")
        for entrance in self.tool.WEB_BROWSER_ENTRANCES:
            relative = f"src/web/browser/{entrance}/index.html"
            browser_inputs.add(relative)
            self.write(relative, b"<!doctype html><main>fixture</main>\n")
        for relative in (
            "src/web/browser/liturgy/liturgy.css",
            "src/web/browser/sources/sources.js",
        ):
            browser_inputs.add(relative)
            self.write(relative, b"/* fixture */\n")

        source_projection = "src/web/data/structure/sources/index.json"
        catena_projection = "src/web/data/structure/catena/index.json"
        self.write(source_projection, b'{"works": []}\n')
        self.write(catena_projection, b'{"sources": []}\n')

        recognized = self.tool.site_source_paths()
        copied_inputs = {
            source.relative_to(self.root).as_posix()
            for source in self.tool.web_data_files().values()
        }

        self.assertEqual(
            browser_inputs,
            {
                relative
                for relative in recognized
                if relative.startswith("src/web/browser/")
            },
        )
        self.assertLessEqual(copied_inputs, recognized)
        self.assertIn(source_projection, recognized)
        self.assertIn(catena_projection, recognized)
        self.assertIn(
            "src/sources/bibles/offered/chapters/Ps/1.json", recognized
        )
        self.assertTrue(
            self.tool.is_bound_web_data_source(self.root / source_projection)
        )
        self.assertTrue(
            self.tool.is_bound_web_data_source(self.root / catena_projection)
        )

        # Exact authorization closure must notice a copied family that changes
        # after approval, even when it was not named in an old allowlist.
        self.authorize_current_inputs()
        self.write(catena_projection, b'{"sources": ["changed"]}\n')
        errors = self.tool.site_source_binding_errors(self.manifest)
        self.assertTrue(
            any(catena_projection in error and "does not match" in error for error in errors),
            errors,
        )

    def test_verifier_rejects_tampered_copied_browser_asset_with_fresh_checksums(
        self,
    ) -> None:
        bible_manifest = {
            "bibles": [
                {
                    "id": "offered",
                    "label": "Offered",
                    "language": "la",
                    "numbering": "vulgate",
                    "psalter": "gallican",
                    "rights": "public-domain",
                }
            ]
        }
        self.write(
            "src/web/data/bibles.json",
            (json.dumps(bible_manifest) + "\n").encode(),
        )
        self.write("src/sources/bibles/offered/chapters/Ps/1.json", b"{}\n")
        self.write("src/web/data/structure/sources/index.json", b'{"works": []}\n')
        self.write("src/web/browser/shared/browser-core.js", b"// approved\n")
        self.write("src/web/browser/shared/browser-core.css", b"/* approved */\n")
        for entrance in self.tool.WEB_BROWSER_ENTRANCES:
            self.write(
                f"src/web/browser/{entrance}/index.html",
                b"<!doctype html><main>fixture</main>\n",
            )

        output = self.tool.OUTPUT_ROOT / "site"
        for destination, source in self.tool.web_data_files().items():
            self.write(
                (output.relative_to(self.root) / destination).as_posix(),
                source.read_bytes(),
            )
        for relative, tampered in (
            ("shared/browser-core.js", b"// tampered\n"),
            ("shared/browser-core.css", b"/* tampered */\n"),
        ):
            with self.subTest(relative=relative):
                copied = output / relative
                approved = copied.read_bytes()
                copied.write_bytes(tampered)
                self.tool.write_checksums(output)

                errors = self.tool.verify_web_data(output)

                self.assertTrue(
                    any(
                        relative in error
                        and "does not match its repository source" in error
                        for error in errors
                    ),
                    errors,
                )
                copied.write_bytes(approved)

    def test_liturgy_quarantine_rejects_generic_licensed_source_identity(
        self,
    ) -> None:
        self.write(
            "src/sources/works/example/licensed/editions/fixture/"
            "artifacts/text/artifact.toml",
            (
                'id = "artifact.example.licensed.fixture.text"\n'
                'edition_id = "edition.example.licensed.fixture"\n'
                'rights_status = "licensed"\n'
            ).encode(),
        )
        structure = "src/web/data/structure/propers/test.json"
        for rights in (None, "public-domain"):
            with self.subTest(rights=rights):
                row = {
                    "lang": "en",
                    "source_id": "artifact.example.licensed.fixture.text",
                    "text": "not authorized for every liturgy surface",
                }
                if rights is not None:
                    row["rights"] = rights
                self.write(
                    structure,
                    (json.dumps({"translations": [row]}) + "\n").encode(),
                )

                with self.assertRaises(self.tool.ReleaseError) as failure:
                    self.tool.validate_liturgical_public_data(self.root / structure)

                self.assertIn("protected source identity", str(failure.exception))
                self.assertIn(
                    "artifact.example.licensed.fixture.text",
                    str(failure.exception),
                )

    def test_liturgy_quarantine_rejects_metadata_free_exact_text_value(self) -> None:
        for relative in (
            "src/web/data/structure/propers/test.json",
            "src/web/data/structure/new-public-family/test.json",
            "src/web/data/bibles.json",
        ):
            with self.subTest(relative=relative):
                self.write(
                    relative,
                    (
                        json.dumps(
                            {
                                "translations": [
                                    {"lang": "en", "text": self.quarantine_marker}
                                ]
                            }
                        )
                        + "\n"
                    ).encode(),
                )

                with self.assertRaises(self.tool.ReleaseError) as failure:
                    self.tool.validate_liturgical_public_data(self.root / relative)

                message = str(failure.exception)
                self.assertIn(digest(self.quarantine_marker.encode()), message)
                self.assertNotIn(self.quarantine_marker, message)

    def test_ordinary_language_absence_allows_only_safe_typed_aggregate(
        self,
    ) -> None:
        structure = "src/web/data/structure/ordinary/test.json"
        safe_rows = [
            {
                "key": "text-rights-withheld",
                "lang": "en",
                "count": 2,
                "state": "rights-restricted",
                "kind": "rights-withheld",
            },
            {
                "key": "text-rights-unresolved",
                "lang": "la",
                "count": 1,
                "state": "unresolved",
                "kind": "rights-unresolved",
            },
        ]
        self.write(
            structure,
            (json.dumps({"language_absences": safe_rows}) + "\n").encode(),
        )

        self.tool.validate_liturgical_public_data(self.root / structure)

        unsafe = dict(safe_rows[0])
        unsafe["source_id"] = "edition.example.private"
        self.write(
            structure,
            (json.dumps({"language_absences": [unsafe]}) + "\n").encode(),
        )
        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_liturgical_public_data(self.root / structure)

        self.assertIn(
            "must contain exactly key, lang, count, state and kind",
            str(failure.exception),
        )

    def test_verifier_rejects_copied_pdf_without_owning_catalog_link(self) -> None:
        self.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        output = self.tool.build_site(self.manifest, publications, preview=False)
        catalog_path = output / "library/test.html"
        catalog_path.write_text(
            catalog_path.read_text(encoding="utf-8").replace(
                'href="../pdf/gpt/work.pdf"', 'href="../nonexistent.html"'
            ),
            encoding="utf-8",
        )

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.verify_output(self.manifest, publications, output, preview=False)

        self.assertIn(
            "work: copied PDF is not reachable from library/test.html",
            str(failure.exception),
        )

    def test_legacy_review_is_alpha_included_but_hold_is_excluded(self) -> None:
        self.add_unapproved_publication(
            "review-work",
            "review",
            install_pdf=True,
            link_catalog="library/test.md",
        )
        self.add_unapproved_publication("held-work", "hold")
        self.authorize_current_inputs()

        publications = self.tool.validate_manifest(self.manifest)
        public = self.tool.included_publications(publications, False)
        preview = self.tool.included_publications(publications, True)
        expected = {("gpt", "work"), ("gpt", "review-work")}
        self.assertEqual(set(public), expected)
        self.assertEqual(set(preview), expected)

        catalog = (self.root / "library/test.md").read_text(encoding="utf-8")
        filtered = self.tool.filter_catalog(
            "library/test.md", catalog, set(public)
        )
        self.assertIn("../pdf/gpt/review-work.pdf", filtered)
        self.assertNotIn("held-work", filtered)

        artifact = self.tool.artifact_manifest_data(self.manifest, public, False)
        entries = {entry["id"]: entry for entry in artifact["publications"]}
        self.assertEqual(entries["review-work"]["status"], "alpha")
        self.assertNotIn("gates", entries["review-work"])
        self.assertEqual(
            entries["review-work"]["authorization"], "test-authorization"
        )
        self.assertEqual(
            entries["review-work"]["pdf_sha256"],
            digest(b"publication pdf bytes\n"),
        )
        self.assertNotIn("held-work", entries)

    def test_alpha_does_not_require_unresolved_maturity_gate(self) -> None:
        self.add_unapproved_publication(
            "review-work",
            "review",
            install_pdf=True,
            link_catalog="library/test.md",
        )
        self.authorize_current_inputs()
        self.manifest["publications"][-1]["gates"] = []

        publications = self.tool.validate_manifest(self.manifest)
        self.assertIn(("gpt", "review-work"), publications)

    def test_local_alpha_record_overrides_legacy_row_and_hash_is_generated(self) -> None:
        self.authorize_current_inputs()
        self.write(
            "release/publications/gpt/work.json",
            (
                json.dumps(
                    {
                        "schema_version": 1,
                        "id": "work",
                        "catalog": "library/test.md",
                        "status": "alpha",
                        "authorization": "test-authorization",
                    },
                    indent=2,
                )
                + "\n"
            ).encode(),
        )
        self.write("pdf/gpt/work.pdf", b"new independently published bytes\n")

        publications = self.tool.validate_manifest(self.manifest)
        artifact = self.tool.artifact_manifest_data(
            self.manifest, publications, preview=False
        )

        self.assertIn("release/publications/gpt/work.json", publications[("gpt", "work")]["_alpha_record"])
        self.assertEqual("alpha", artifact["publications"][0]["status"])
        self.assertEqual(
            digest(b"new independently published bytes\n"),
            artifact["publications"][0]["pdf_sha256"],
        )

    def test_url_path_segment_passes_but_a_local_home_path_fails(self) -> None:
        self.authorize_current_inputs()
        publications = self.tool.validate_manifest(self.manifest)
        page = (
            '<!doctype html><meta name="robots" content="index, follow">'
            '<title>test</title><a href="https://example.invalid/home/records">x</a>\n'
        )
        with mock.patch.object(self.tool, "render_source_page", return_value=page):
            with mock.patch.object(
                self.tool, "verify_catalog_reachability", return_value=[]
            ), mock.patch.object(
                self.tool, "verify_link_previews", return_value=[]
            ):
                output = self.tool.build_site(self.manifest, publications, preview=False)
                self.tool.verify_output(self.manifest, publications, output, preview=False)

        leaked = page.replace("https://example.invalid", "file:///home/someone")
        with mock.patch.object(self.tool, "render_source_page", return_value=leaked):
            with mock.patch.object(
                self.tool, "verify_catalog_reachability", return_value=[]
            ), mock.patch.object(
                self.tool, "verify_link_previews", return_value=[]
            ):
                output = self.tool.build_site(self.manifest, publications, preview=False)
                with self.assertRaises(self.tool.ReleaseError) as failure:
                    self.tool.verify_output(
                        self.manifest, publications, output, preview=False
                    )

        self.assertIn("contains home-directory path", str(failure.exception))

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
        self.assertIn("tools/public-alpha verify", stdout)
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


    def mixed_provider_catalog(self) -> str:
        return (
            "# Test shelf\n\n"
            "| Publication | Focus |\n"
            "| --- | --- |\n"
            "| **[Work](../pdf/gpt/work.pdf)** · "
            "[Claude edition](../pdf/claude/work.pdf) | Focus text. |\n"
        )

    def test_mixed_provider_row_degrades_unreleased_edition_to_em_dash(self) -> None:
        filtered = self.tool.filter_catalog(
            "library/test.md", self.mixed_provider_catalog(), {("gpt", "work")}
        )

        self.assertIn("[Work](../pdf/gpt/work.pdf)", filtered)
        self.assertNotIn("pdf/claude", filtered)
        self.assertIn("—", filtered)
        self.assertIn("Focus text.", filtered)

    def test_mixed_provider_row_keeps_every_released_edition(self) -> None:
        filtered = self.tool.filter_catalog(
            "library/test.md",
            self.mixed_provider_catalog(),
            {("gpt", "work"), ("claude", "work")},
        )

        self.assertIn("[Work](../pdf/gpt/work.pdf)", filtered)
        self.assertIn("[Claude edition](../pdf/claude/work.pdf)", filtered)
        self.assertNotIn("—", filtered)

    def read_link_catalog(self) -> str:
        return (
            "# Test shelf\n\n"
            "| Publication | ChatGPT | Claude | Focus |\n"
            "| --- | --- | --- | --- |\n"
            "| **Work** | [PDF](../pdf/gpt/work.pdf) · [Read](../web/gpt/work.html) | "
            "[PDF](../pdf/claude/work.pdf) · [Read](../web/claude/work.html) | "
            "Focus text. |\n"
        )

    def test_excluded_edition_degrades_its_pdf_and_read_links_to_one_dash(self) -> None:
        filtered = self.tool.filter_catalog(
            "library/test.md", self.read_link_catalog(), {("gpt", "work")}
        )

        self.assertIn("[Read](../web/gpt/work.html)", filtered)
        self.assertNotIn("web/claude", filtered)
        self.assertNotIn("pdf/claude", filtered)
        self.assertIn("| — |", filtered)
        self.assertNotIn("— · —", filtered)

    def test_read_links_do_not_change_catalog_occurrence_counting(self) -> None:
        (self.root / "library/test.md").write_text(
            self.read_link_catalog(), encoding="utf-8"
        )

        occurrences, multi_pdf_lines, _, _, _ = self.tool.catalog_occurrences(
            "gpt", ["gpt", "claude"]
        )

        self.assertEqual(occurrences[("gpt", "work")], ["library/test.md"])
        self.assertEqual(occurrences[("claude", "work")], ["library/test.md"])
        self.assertEqual(len(multi_pdf_lines), 1)
        self.assertEqual(
            multi_pdf_lines[0][1], [("gpt", "work"), ("claude", "work")]
        )

    def test_row_with_no_released_edition_is_dropped(self) -> None:
        filtered = self.tool.filter_catalog(
            "library/test.md", self.mixed_provider_catalog(), set()
        )

        self.assertNotIn("pdf/gpt", filtered)
        self.assertNotIn("pdf/claude", filtered)
        self.assertIn("No publications from this section are included", filtered)

    def test_catalog_link_to_undeclared_provider_is_rejected(self) -> None:
        with (self.root / "library/test.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[Other edition](../pdf/other/work.pdf)\n")
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "library/test.md: catalog references undeclared provider edition "
            "pdf/other/work.pdf",
            str(failure.exception),
        )

    def test_mixed_status_row_survives_with_em_dash_for_held_claude_edition(self) -> None:
        self.write(
            "library/test.md",
            "# Test shelf\n\n"
            "[Work](../pdf/gpt/work.pdf) · "
            "[Claude edition](../pdf/claude/work.pdf)\n".encode(),
        )
        self.add_claude_publication("work", "hold")
        self.authorize_current_inputs()

        publications = self.tool.validate_manifest(self.manifest)
        included = self.tool.included_publications(publications, False)
        self.assertEqual(set(included), {("gpt", "work")})

        catalog = (self.root / "library/test.md").read_text(encoding="utf-8")
        filtered = self.tool.filter_catalog("library/test.md", catalog, set(included))
        self.assertIn("[Work](../pdf/gpt/work.pdf)", filtered)
        self.assertNotIn("pdf/claude", filtered)
        self.assertIn("—", filtered)

    def test_released_claude_edition_validates_and_enters_the_artifact(self) -> None:
        self.write(
            "library/test.md",
            "# Test shelf\n\n"
            "[Work](../pdf/gpt/work.pdf) · "
            "[Claude edition](../pdf/claude/work.pdf)\n".encode(),
        )
        self.add_claude_publication("work", "release")
        self.authorize_current_inputs()

        publications = self.tool.validate_manifest(self.manifest)
        included = self.tool.included_publications(publications, False)
        self.assertEqual(set(included), {("gpt", "work"), ("claude", "work")})

        artifact = self.tool.artifact_manifest_data(self.manifest, included, False)
        entries = {entry["id"]: entry["pdf"] for entry in artifact["publications"]}
        self.assertEqual(
            entries,
            {"work": "pdf/gpt/work.pdf", "claude:work": "pdf/claude/work.pdf"},
        )
        expected_files = self.tool.expected_artifact_files(
            self.manifest,
            included,
            False,
            self.tool.artifact_authorization(self.manifest, included),
        )
        self.assertIn("pdf/gpt/work.pdf", expected_files)
        self.assertIn("pdf/claude/work.pdf", expected_files)

    def test_ark_editions_share_one_catalog_row_and_keep_their_titles(self) -> None:
        catalog = (REPOSITORY_ROOT / "library/mariology.md").read_text(
            encoding="utf-8"
        )
        rows = [
            line
            for line in catalog.splitlines()
            if "theology/mariology/ark-of-the-covenant.pdf" in line
        ]

        self.assertEqual(len(rows), 1)
        row = rows[0]
        gpt_link = (
            "[*The Ark and the Mother of the Lord: The Journey of the Covenant "
            "Presence*](../pdf/gpt/theology/mariology/ark-of-the-covenant.pdf)"
        )
        claude_link = (
            "[*The Ark of the Covenant: From Sinai to the Woman Clothed with the "
            "Sun*](../pdf/claude/theology/mariology/ark-of-the-covenant.pdf)"
        )
        self.assertEqual(row.count(gpt_link), 1)
        self.assertEqual(row.count(claude_link), 1)

        gpt_pdf = (
            REPOSITORY_ROOT
            / "pdf/gpt/theology/mariology/ark-of-the-covenant.pdf"
        )
        claude_pdf = (
            REPOSITORY_ROOT
            / "pdf/claude/theology/mariology/ark-of-the-covenant.pdf"
        )
        self.assertNotEqual(
            gpt_pdf.read_bytes(),
            claude_pdf.read_bytes(),
        )

    def test_released_claude_edition_requires_catalog_link(self) -> None:
        self.add_claude_publication("work", "release")
        self.authorize_current_inputs()

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.validate_manifest(self.manifest)

        self.assertIn(
            "claude:work: expected one catalog link, found 0",
            str(failure.exception),
        )

    def test_held_claude_edition_with_installed_pdf_may_stay_unlinked(self) -> None:
        self.add_claude_publication("work", "hold")
        self.authorize_current_inputs()

        publications = self.tool.validate_manifest(self.manifest)

        self.assertEqual(publications[("claude", "work")]["status"], "hold")

    def test_legacy_expected_counts_do_not_gate_discovered_publications(self) -> None:
        self.authorize_current_inputs()
        self.manifest["expected_counts"] = {"providers": {"gpt": 5}}

        publications = self.tool.validate_manifest(self.manifest)

        self.assertEqual({("gpt", "work")}, set(publications))

    def test_publication_naming_undeclared_provider_is_rejected(self) -> None:
        self.manifest["publications"].append(
            {
                "id": "other:work",
                "status": "hold",
                "catalog": "library/test.md",
                "gates": [],
                "approval": None,
            }
        )

        with self.assertRaises(self.tool.ReleaseError) as failure:
            self.tool.publication_map(self.manifest)

        self.assertIn(
            "names an undeclared provider: 'other:work'",
            str(failure.exception),
        )


if __name__ == "__main__":
    unittest.main()
