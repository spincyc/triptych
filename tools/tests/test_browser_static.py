#!/usr/bin/env python3
"""Static gates over every browser source file, not only the liturgy ones.

Seven of the browser JavaScript files are parsed by nothing: no Python test
loads them, no node harness runs them, and `make check` never reads them. Their
only protection is the sha256 pin in `release/public-alpha.json`, which proves a
file did not change, not that it is a program. A syntax error in one of them
reaches the reader as a blank instrument.

The head and whole-document gates run the build's own `browser_page_parts` at
check time. The build already refuses a browser page whose head holds something
the layout has no place for, but it refuses it during `make public-site`, which
`make check` does not run and CI runs only after `check-deployment-sources`. A
page that cannot be published should fail before the deploy is the thing that
says so.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BROWSER = ROOT / "src/web/browser"
NODE = shutil.which("node")


def load_public_alpha():
  path = ROOT / "tools/public-alpha"
  loader = importlib.machinery.SourceFileLoader("browser_static_public_alpha", str(path))
  spec = importlib.util.spec_from_loader(loader.name, loader)
  if spec is None:
    raise RuntimeError("could not load tools/public-alpha")
  module = importlib.util.module_from_spec(spec)
  loader.exec_module(module)
  return module


def browser_scripts() -> list[Path]:
  return sorted(BROWSER.rglob("*.js"))


def browser_pages() -> list[Path]:
  """Exactly the pages the build publishes: top level of each entrance.

  `web_browser_pages` globs non-recursively, so `prototypes/` is excluded here
  for the same reason it is excluded there.
  """
  module = load_public_alpha()
  pages: list[Path] = []
  for entrance in module.WEB_BROWSER_ENTRANCES:
    pages.extend(sorted((BROWSER / entrance).glob("*.html")))
  return pages


class BrowserScriptSyntaxTest(unittest.TestCase):
  @unittest.skipIf(NODE is None, "node is not installed; nothing can parse the browser scripts")
  def test_every_browser_script_parses(self):
    scripts = browser_scripts()
    self.assertGreaterEqual(len(scripts), 20, "expected the browser tree to hold its scripts")
    for script in scripts:
      with self.subTest(script=script.relative_to(ROOT).as_posix()):
        result = subprocess.run(
          [NODE, "--check", str(script)],
          cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr.strip())

  @unittest.skipIf(NODE is None, "node is not installed; nothing can parse the harnesses")
  def test_every_browser_harness_parses(self):
    harnesses = sorted((ROOT / "tools/tests").glob("*.mjs"))
    self.assertGreaterEqual(len(harnesses), 4, "expected the browser harnesses to be present")
    for harness in harnesses:
      with self.subTest(harness=harness.name):
        result = subprocess.run(
          [NODE, "--check", str(harness)],
          cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr.strip())


class BrowserPagePublishabilityTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls) -> None:
    cls.module = load_public_alpha()
    cls.pages = browser_pages()

  def test_the_build_can_dismantle_every_published_browser_page(self):
    self.assertGreaterEqual(len(self.pages), 13, "expected every entrance to keep its pages")
    for page in self.pages:
      output_relative = f"{page.parent.name}/{page.name}"
      with self.subTest(page=page.relative_to(ROOT).as_posix()):
        parts = self.module.browser_page_parts(page, output_relative)
        self.assertTrue(parts["title"], "a published page needs a title")
        self.assertTrue(parts["content"].strip(), "a published page needs content")

  def test_every_entrance_has_a_section_colour(self):
    """The tool aborts at import when one is missing; assert it here too.

    A new entrance directory is otherwise a change whose second half is only
    discovered by running the build.
    """
    for entrance in self.module.WEB_BROWSER_ENTRANCES:
      with self.subTest(entrance=entrance):
        self.assertIn(entrance, self.module.BROWSER_SECTION_COLOURS)

  def test_sources_defers_its_document_landmark_to_the_public_layout(self):
    """The built Sources route has one main rather than a nested pair."""
    source = BROWSER / "sources/index.html"
    output_relative = "sources/index.html"
    rendered = self.module.render_browser_page(source, output_relative, False, {})
    self.assertEqual(source.read_text(encoding="utf-8").count("<main"), 0)
    self.assertEqual(rendered.count("<main"), 1)
    self.assertIn('<main id="main-content"', rendered)

  def test_every_built_browser_page_carries_exactly_one_document_landmark(self):
    """One `<main>` per BUILT page — the publish side, which nothing read.

    Every source page here declared one landmark or none and passed, while the
    artifact wrapped twelve of them in the layout's own `<main>`: two document
    landmarks on every route but Sources, 108 `single-main-element` failures in
    `corpus_browser_gate.mjs`, and no static test that rendered a page. A page
    naming its own `<main>` is wrapped in a plain `<div id="main-content">`; a
    page naming none keeps the layout's. Either way exactly one survives, and
    the layout's skip link — the only one left after the page's own is
    stripped — lands on an element that exists.
    """
    for page in self.pages:
      output_relative = f"{page.parent.name}/{page.name}"
      declared = page.read_text(encoding="utf-8").count("<main")
      with self.subTest(page=page.relative_to(ROOT).as_posix(), declared=declared):
        built = self.module.render_browser_page(page, output_relative, False, {})
        self.assertEqual(built.count("<main"), 1, "exactly one <main> per built page")
        self.assertEqual(built.count("</main>"), 1)
        wrapper = "div" if declared else "main"
        self.assertIn(f'<{wrapper} id="main-content"', built)
        self.assertEqual(built.count('class="skip-link"'), 1)
        self.assertIn('href="#main-content"', built)
        self.assertEqual(built.count('id="main-content"'), 1)

  def test_a_browser_page_with_two_landmarks_is_refused(self):
    """The wrapper can remove a nested pair it made, not one a page made.

    Zero is repaired by the layout and one is kept; two would publish two
    document landmarks whatever the layout did, so the split refuses the page
    rather than choosing which of them a reader should believe.
    """
    # Under the repository, because the split names a page by its path there;
    # `build/` is the ignored place a test may write.
    (ROOT / "build").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "build") as scratch:
      page = Path(scratch) / "index.html"
      page.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>Two</title><link rel=\"stylesheet\" href=\"two.css\"></head>"
        "<body><main id=\"reading\"></main><main id=\"also\"></main>"
        "<script src=\"two.js\"></script></body></html>",
        encoding="utf-8",
      )
      with self.assertRaises(self.module.ReleaseError) as refused:
        self.module.browser_page_parts(page, "catena/index.html")
      self.assertIn("declares 2 <main> elements", str(refused.exception))
      # A `<main>` mentioned in a comment is not a landmark and is not counted.
      page.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>One</title><link rel=\"stylesheet\" href=\"one.css\"></head>"
        "<body><!-- the <main> below is the reading --><main id=\"reading\"></main>"
        "<script src=\"one.js\"></script></body></html>",
        encoding="utf-8",
      )
      parts = self.module.browser_page_parts(page, "catena/index.html")
      self.assertEqual(parts["content_element"], "div")

  def test_a_prose_page_keeps_the_layouts_landmark(self):
    """The default is proved through the real layout, not only declared."""
    prose = self.module.wrap_in_layout(
      "ABOUT.md", "about.html", "page-shell", "About", "", "<p>Prose.</p>",
      False, {},
    )
    self.assertIn('<main id="main-content"', prose)
    self.assertEqual(prose.count("<main"), 1)
    self.assertNotIn("{{CONTENT_ELEMENT}}", prose)

  def test_every_browser_source_keeps_one_page_heading(self):
    for page in self.pages:
      with self.subTest(page=page.relative_to(ROOT).as_posix()):
        text = page.read_text(encoding="utf-8")
        self.assertEqual(text.count("<h1"), 1, "exactly one <h1> per source page")


if __name__ == "__main__":
  unittest.main()
