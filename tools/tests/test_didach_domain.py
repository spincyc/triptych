"""Deployment-location independence: the contracts the didach.ai cutover rests on.

The migration recorded in guidance/didach-domain-migration.md depends on four
properties the generator must keep whichever base path the site is mounted at:
the canonical origin is one derived value, ordinary pages link document-
relatively, the root-served error page links base-anchored, and every served
browser page sits exactly one directory below the site root so `../browse`
and `../shared/` resolve the same way under `/` and under `/triptych/`.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
from pathlib import Path, PurePosixPath
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPOSITORY_ROOT / "tools/public-alpha"


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_didach_domain_tool", str(TOOL_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load tools/public-alpha")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CanonicalOriginTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = load_tool()

    def test_site_origin_is_derived_from_host_and_base_path(self) -> None:
        self.assertEqual(
            self.tool.SITE_ORIGIN,
            self.tool.SITE_SCHEME_HOST + self.tool.SITE_BASE_PATH,
        )

    def test_scheme_host_is_https_and_carries_no_path(self) -> None:
        host = self.tool.SITE_SCHEME_HOST
        self.assertTrue(host.startswith("https://"))
        self.assertFalse(host.endswith("/"))
        self.assertNotIn("/", host.removeprefix("https://"))

    def test_base_path_is_empty_or_slash_led_and_never_slash_trailed(self) -> None:
        base = self.tool.SITE_BASE_PATH
        if base:
            self.assertTrue(base.startswith("/"))
            self.assertFalse(base.endswith("/"))
        else:
            self.assertEqual(base, "")


class PageLinkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = load_tool()

    def test_relative_link_at_root_depth(self) -> None:
        self.assertEqual(self.tool.relative_link("index.html", "assets/site.css"), "assets/site.css")

    def test_relative_link_one_deep(self) -> None:
        self.assertEqual(
            self.tool.relative_link("library/faith.html", "assets/site.css"),
            "../assets/site.css",
        )

    def test_relative_link_two_deep(self) -> None:
        self.assertEqual(
            self.tool.relative_link("web/gpt/example.html", "index.html"),
            "../../index.html",
        )

    def test_ordinary_page_links_stay_document_relative(self) -> None:
        self.assertEqual(
            self.tool.page_link("library/faith.html", "assets/site.css"),
            "../assets/site.css",
        )

    def test_error_page_links_are_anchored_to_the_deployment_base(self) -> None:
        self.assertEqual(
            self.tool.page_link("404.html", "assets/site.css"),
            f"{self.tool.SITE_BASE_PATH}/assets/site.css",
        )


class VerifyLinksPortabilityTest(unittest.TestCase):
    """verify_links is the subpath regression gate; hold both halves of it."""

    def setUp(self) -> None:
        self.tool = load_tool()
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.output = Path(self.temporary_directory.name)
        (self.output / "assets").mkdir()
        (self.output / "liturgy").mkdir()
        (self.output / "assets/site.css").write_text("body{}", encoding="utf-8")
        (self.output / "index.html").write_text(
            "<html><body><a href='liturgy/day.html'>Day</a></body></html>",
            encoding="utf-8",
        )
        (self.output / "liturgy/day.html").write_text(
            "<html><body><a href='../index.html'>Home</a></body></html>",
            encoding="utf-8",
        )

    def base(self) -> str:
        return self.tool.SITE_BASE_PATH

    def write_error_page(self, body: str) -> None:
        (self.output / "404.html").write_text(
            f"<html><body>{body}</body></html>", encoding="utf-8"
        )

    def test_relative_links_verify_clean(self) -> None:
        self.write_error_page(f'<a href="{self.base()}/index.html">Home</a>')
        self.assertEqual(self.tool.verify_links(self.output), [])

    def test_root_relative_link_in_an_ordinary_page_is_refused(self) -> None:
        self.write_error_page(f'<a href="{self.base()}/index.html">Home</a>')
        (self.output / "liturgy/day.html").write_text(
            '<html><body><a href="/index.html">Home</a></body></html>',
            encoding="utf-8",
        )
        errors = self.tool.verify_links(self.output)
        self.assertEqual(len(errors), 1)
        self.assertIn("root-relative link is not portable", errors[0])

    def test_error_page_accepts_base_anchored_links_and_fragments(self) -> None:
        self.write_error_page(
            f'<a href="#main">Skip</a><main id="main">'
            f'<a href="{self.base()}/index.html">Home</a>'
            f'<a href="{self.base()}/assets/site.css">Styles</a></main>'
        )
        self.assertEqual(self.tool.verify_links(self.output), [])

    def test_error_page_refuses_document_relative_links(self) -> None:
        self.write_error_page('<a href="index.html">Home</a>')
        errors = self.tool.verify_links(self.output)
        self.assertEqual(len(errors), 1)
        self.assertIn("anchored to the deployment base", errors[0])

    def test_error_page_refuses_links_outside_the_deployment_base(self) -> None:
        self.write_error_page('<a href="/elsewhere/index.html">Home</a>')
        errors = self.tool.verify_links(self.output)
        if self.base():
            self.assertEqual(len(errors), 1)
            self.assertIn("root-relative link is not portable", errors[0])
        else:
            # With an empty base path every root-relative link is inside the
            # base; this one is then simply broken.
            self.assertEqual(len(errors), 1)
            self.assertIn("broken local link", errors[0])

    def test_error_page_base_anchored_link_must_still_resolve(self) -> None:
        self.write_error_page(f'<a href="{self.base()}/missing.html">Gone</a>')
        errors = self.tool.verify_links(self.output)
        self.assertEqual(len(errors), 1)
        self.assertIn("broken local link", errors[0])


class ServedDepthInvariantTest(unittest.TestCase):
    """Every served browser page sits exactly one directory below the root.

    src/web/browser/shared/browser-core.js resolves its data root as
    `../browse` and every entrance page loads `../shared/browser-core.js`;
    both are correct at depth one and silently wrong at any other depth,
    under every deployment base. The non-recursive glob in web_browser_pages
    makes deeper pages impossible today; this holds the rule if that changes.
    """

    def setUp(self) -> None:
        self.tool = load_tool()

    def test_every_entrance_is_a_single_path_segment(self) -> None:
        for entrance in self.tool.WEB_BROWSER_ENTRANCES:
            self.assertEqual(len(PurePosixPath(entrance).parts), 1, entrance)

    def test_every_served_browser_page_is_exactly_one_directory_deep(self) -> None:
        pages = self.tool.web_browser_pages()
        self.assertTrue(pages)
        for page in pages:
            parts = PurePosixPath(page).parts
            self.assertEqual(len(parts), 2, page)
            self.assertIn(parts[0], self.tool.WEB_BROWSER_ENTRANCES, page)

    def test_the_error_page_is_served_at_the_artifact_root(self) -> None:
        for page in self.tool.ROOT_SERVED_ERROR_PAGES:
            self.assertEqual(len(PurePosixPath(page).parts), 1, page)


if __name__ == "__main__":
    unittest.main()
