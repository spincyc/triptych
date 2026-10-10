"""A catalog identity marker cannot replace a reader's publication link."""
from __future__ import annotations

from collections import Counter
import re
import unittest

from tools.tests import test_public_alpha as fixtures


class PublicationLinksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = fixtures.PublicAlphaTest(methodName="runTest")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.tool = self.fixture.tool

    def test_released_pdf_marker_cannot_replace_visible_link(self) -> None:
        for provider in ("gpt", "claude"):
            with self.subTest(provider=provider):
                if provider == "claude":
                    self.fixture.add_claude_publication("work", "release")
                marker = "work" if provider == "gpt" else "claude:work"
                other = "claude" if provider == "gpt" else "gpt"
                self.fixture.write(
                    "library/test.md",
                    (f"# Test\n<!-- triptych-publication-id: {marker} -->\n"
                     + (f"[Other edition](../pdf/{other}/work.pdf)\n"
                        if provider == "claude" else "")).encode(),
                )
                self.fixture.authorize_current_inputs()
                with self.assertRaises(self.tool.ReleaseError) as failure:
                    self.tool.validate_manifest(self.fixture.manifest)
                self.assertIn("expected one catalog link, found 0", str(failure.exception))

    def test_rendered_catalog_marker_cannot_replace_visible_link(self) -> None:
        self.fixture.write(
            "library/test.md", b"# Test\n<!-- triptych-publication-id: work -->\n"
        )
        self.fixture.write(
            "build/public-alpha/site/library/test.html",
            b"<h1>Test</h1><!-- triptych-publication-id: work -->",
        )
        errors = self.tool.verify_catalog_reachability(
            self.fixture.manifest,
            {("gpt", "work"): {"catalog": "library/test.md"}},
            self.fixture.root / "build/public-alpha/site",
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("copied PDF is not reachable", errors[0])

    def test_commented_out_pdf_link_is_not_visible_catalog_ownership(self) -> None:
        for comment in ("<!-- [PDF](../pdf/gpt/work.pdf) -->",
                        "<!--\n[PDF](../pdf/gpt/work.pdf)\n-->"):
            with self.subTest(comment=comment):
                self.fixture.write("library/test.md", f"# Test\n{comment}\n".encode())
                self.fixture.authorize_current_inputs()
                with self.assertRaises(self.tool.ReleaseError) as failure:
                    self.tool.validate_manifest(self.fixture.manifest)
                self.assertIn("expected one catalog link, found 0", str(failure.exception))


class RepositoryPublicationLinksTest(unittest.TestCase):
    def test_every_released_pdf_has_one_visible_link_in_its_own_catalog(self) -> None:
        tool = fixtures.load_tool()
        included = tool.included_publications(tool.publication_map(tool.load_manifest()), False)
        links = {}
        for catalog in sorted({row["catalog"] for row in included.values()}):
            text = (fixtures.REPOSITORY_ROOT / catalog).read_text(encoding="utf-8")
            # HTML comments establish ownership, never reader-visible links.
            visible = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
            links[catalog] = Counter(tool.PDF_LINK_RE.findall(visible))
        for identity, publication in included.items():
            with self.subTest(identity=identity):
                self.assertEqual(links[publication["catalog"]][identity], 1)
                self.assertEqual(sum(rows[identity] for rows in links.values()), 1)

    def test_named_provider_columns_link_only_their_own_editions(self) -> None:
        for catalog in sorted((fixtures.REPOSITORY_ROOT / "library").glob("*.md")):
            providers = {}
            for number, line in enumerate(catalog.read_text(encoding="utf-8").splitlines(), 1):
                if not line.startswith("|"):
                    providers = {}
                    continue
                cells = line.strip("|").split("|")
                if any(cell.strip() in {"ChatGPT", "Claude"} for cell in cells):
                    providers = {i: {"ChatGPT": "gpt", "Claude": "claude"}[cell.strip()]
                                 for i, cell in enumerate(cells)
                                 if cell.strip() in {"ChatGPT", "Claude"}}
                for index, provider in providers.items():
                    with self.subTest(catalog=catalog.name, line=number, provider=provider):
                        self.assertLess(index, len(cells))
                        for linked in re.findall(r"\.\./(?:pdf|web)/(gpt|claude)/", cells[index]):
                            self.assertEqual(linked, provider)


if __name__ == "__main__":
    unittest.main()
