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

  def test_no_published_browser_page_carries_a_second_document_landmark(self):
    """One `<main>` per source page.

    The source side of the boundary. Its companion below asserts the published
    side, because for a long time only this half existed: the artifact nested
    the page's own landmark inside the layout's on all thirteen routes while
    every source file here passed, and no gate read the built page.
    """
    for page in self.pages:
      with self.subTest(page=page.relative_to(ROOT).as_posix()):
        text = page.read_text(encoding="utf-8")
        self.assertEqual(text.count("<main"), 1, "exactly one <main> per source page")
        self.assertEqual(text.count("<h1"), 1, "exactly one <h1> per source page")

  def test_no_built_browser_page_carries_a_second_document_landmark(self):
    """One `<main>` per *built* page — the assertion that was missing.

    A source page with one landmark says nothing about the artifact, which is
    the page re-wrapped in `release/public-alpha/layout.html`. The layout now
    wraps a browser page in a plain `<div id="main-content">` and keeps `<main>`
    for the pages whose only landmark it is, so the reader receives the one
    region the page itself named.
    """
    for page in self.pages:
      output_relative = f"{page.parent.name}/{page.name}"
      with self.subTest(page=page.relative_to(ROOT).as_posix()):
        built = self.module.render_browser_page(page, output_relative, False, {})
        self.assertEqual(built.count("<main"), 1, "exactly one <main> per built page")
        self.assertEqual(built.count("<h1"), 1, "exactly one <h1> per built page")
        self.assertIn('<div id="main-content"', built)
        # The skip link has to land somewhere real, and the layout's is the only
        # one left: the page's own is stripped as the content is taken apart.
        self.assertEqual(built.count('class="skip-link"'), 1)
        self.assertIn('href="#main-content"', built)


if __name__ == "__main__":
  unittest.main()
