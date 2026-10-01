#!/usr/bin/env python3
"""Name collisions between the shared browser stylesheet and an instrument's own.

Four defects sat in the browser tree and each one is a class of defect rather
than an incident.

1. TWO COMPONENTS UNDER ONE NAME. `shared/browser-core.css` styled `.field` as a
   control in the bar above a reading page; `history/history.css` styled `.field`
   as a line of one change. Both rules reached every change row and the row
   rendered correctly only because `history.css` is the second `<link>` and
   re-declared `display` and `gap`. `texts/texts.css` had the same arrangement
   with `.detail` and `.detail-title`, and its own comment said so: it restated
   every declaration of the shared rule so the shared one could not show through.
   A correctness that rests on the order of two `<link>` elements, and on nobody
   adding a declaration to the shared rule without restating it downstream, is
   not a correctness. The two components are now `.change-field*` and `.record*`
   and neither meets the shared namespace.

2. ONE FAILURE RENDERING THAT KNEW ONE PAGE. `Triptych.fail` looked up `#reading`
   and returned silently when it was absent. Four different `<main>` ids exist
   across the instruments — `#reading`, `#map`, `#canon`, `#reader-document` —
   so on three of them a caller's message went nowhere at all: no error, no
   spoken line, and the page's "Loading…" placeholder and `aria-busy="true"`
   left standing, which tells a reader the corpus is arriving when it is not.
   `fail` now takes a target and otherwise walks a declared list of landmarks.

3. ONE VOCABULARY GLOSSED TWICE, AND THE SECOND COPY SHORT A TERM. `history.js`
   carries a copy of `law.js`'s `CITATION_WORDS` and the copy had lost
   `'none-claimed'`. Twenty-six of the fifty-nine stations in the default slice
   carry that value, and each rendered `Instrument read: none-claimed — ` with a
   dangling em dash where the corpus has a sentence to say.

4. ONE PAGE'S STYLESHEET RESTYLING EVERY PAGE'S HEADER. The site header,
   footer, banner and breadcrumb belong to `release/public-alpha/layout.html`
   and stand on every page. `liturgy/day-missal.css` restyled them through
   `body > .site-header`, which names no page at all: loaded or bundled
   anywhere else, it re-laid-out that page's header too. A rule may reach the
   layout's chrome only from inside a page scope — a `:has()` naming a class
   the page itself owns — the way `reader-instrument.css` hides it.

These tests are source-level. They read the files rather than a rendered page,
except where a model can be replayed under node, which the landmark test does.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BROWSER = ROOT / "src/web/browser"
CORE_CSS = BROWSER / "shared/browser-core.css"
CORE_JS = BROWSER / "shared/browser-core.js"
LAYOUT = ROOT / "release/public-alpha/layout.html"
GENERATOR = ROOT / "tools/public-alpha"
ACT_HISTORY = ROOT / "src/web/data/structure/act-history"
NODE = shutil.which("node")

# Five instrument rules keep a shared name. Each re-tunes the SAME component for
# its own page — a size, a colour — rather than declaring a second component
# under one word, which is what `.field` and `.detail` did. They are listed
# rather than silently permitted, so the list can only shorten, and only by a
# maintainer who means to shorten it. `.field` and `.detail` were in this shape
# and are not here, because they were renamed instead. The two liturgy entries
# are noted, not endorsed: that tree is an in-progress deliverable and is not
# this change's to touch.
TUNED_SHARED_COMPONENTS = {
  "catena/catena.css": {"tally"},
  "history/history.css": {"held-name"},
  "law/law.css": {"held-name"},
  "liturgy/day-missal.css": {"page-browser"},
  "liturgy/liturgy.css": {"proper-name"},
}


def without_comments(text: str) -> str:
  return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def subject_classes(path: Path) -> set[str]:
  """The classes a stylesheet sets properties on directly.

  Only single-compound selectors count. A descendant selector such as
  `.texts-page .field` or `.passage-nav .field` is an instrument reaching into
  a shared component from inside its own scope, which is how the tree is meant
  to extend the shared sheet; a bare `.field` is a second component wearing the
  first one's name, which is the defect.
  """
  found: set[str] = set()
  for block in re.finditer(r"([^{}]+)\{", without_comments(path.read_text())):
    selector = block.group(1).strip()
    if not selector or selector.startswith("@"):
      continue
    for one in selector.split(","):
      one = one.strip()
      if not one or re.search(r"[\s>+~]", one):
        continue
      found |= set(re.findall(r"\.([A-Za-z0-9_-]+)", one))
  return found


def emitted_classes(path: Path) -> set[str]:
  """Class names a script hands to `T.el(tag, className)` or a page to `class=`."""
  text = path.read_text()
  found: set[str] = set()
  if path.suffix == ".html":
    for value in re.findall(r'class="([^"]*)"', text):
      found |= set(value.split())
    return found
  for call in re.findall(r"T\.el\(\s*'[^']*'\s*,\s*'([^']*)'", text):
    found |= set(call.split())
  for assigned in re.findall(r"\.className\s*=\s*'([^']*)'", text):
    found |= set(assigned.split())
  for added in re.findall(r"classList\.add\(\s*'([^']*)'", text):
    found |= set(added.split())
  return found


def instrument_stylesheets() -> list[Path]:
  # prototypes/ holds unlinked review-only candidates that never load beside
  # browser-core.css, so the shared-namespace rules do not govern them.
  return sorted(
    p for p in BROWSER.rglob("*.css")
    if p != CORE_CSS and "prototypes" not in p.relative_to(BROWSER).parts
  )


def citation_words(path: Path) -> dict[str, str]:
  literal = re.search(r"const CITATION_WORDS = \{(.*?)\n  \};", path.read_text(), re.S)
  if literal is None:
    raise AssertionError(f"{path} no longer declares a CITATION_WORDS object literal")
  return dict(re.findall(r"'([^']+)'\s*:\s*'([^']*)'", literal.group(1)))


def declared_landmarks() -> list[str]:
  literal = re.search(r"const DOCUMENT_LANDMARKS = \[([^\]]*)\];", CORE_JS.read_text())
  if literal is None:
    raise AssertionError("browser-core.js no longer declares DOCUMENT_LANDMARKS")
  return re.findall(r"'([^']+)'", literal.group(1))


def main_ids() -> dict[str, str]:
  """Every `<main id>` in the tree, by the page that carries it."""
  found: dict[str, str] = {}
  for page in sorted(BROWSER.rglob("*.html")):
    # A prototype page never loads the shared failure plumbing, so its <main>
    # is not a landmark browser-core.js has to know.
    if "prototypes" in page.relative_to(BROWSER).parts:
      continue
    for element in re.findall(r"<main[^>]*>", page.read_text()):
      identifier = re.search(r'id="([^"]+)"', element)
      if identifier:
        found[page.relative_to(ROOT).as_posix()] = identifier.group(1)
  return found


class SharedNamespaceTest(unittest.TestCase):
  def test_no_instrument_declares_a_second_component_under_a_shared_name(self):
    """A bare `.field` in history.css shadowed the shared control-bar `.field`.

    The rename is only worth making if nothing takes its place, so this holds
    the whole tree rather than the two files that were fixed.
    """
    shared = subject_classes(CORE_CSS)
    for sheet in instrument_stylesheets():
      name = sheet.relative_to(BROWSER).as_posix()
      with self.subTest(stylesheet=name):
        collisions = (shared & subject_classes(sheet)) - TUNED_SHARED_COMPONENTS.get(name, set())
        self.assertEqual(
          collisions, set(),
          f"{name} sets properties directly on {sorted(collisions)}, which "
          "shared/browser-core.css also owns; rename the instrument's component "
          "or scope the selector under the page class",
        )

  def test_the_history_change_row_is_declared_in_exactly_one_stylesheet(self):
    """The row rendered right only because history.css loaded second.

    One declaring stylesheet per class is the property that removes the
    dependency: with nothing to override, load order cannot decide anything.
    """
    sheets = {p: subject_classes(p) for p in [CORE_CSS] + instrument_stylesheets()}
    emitted = {c for c in emitted_classes(BROWSER / "history/history.js") if c.startswith("change-field")}
    self.assertTrue(emitted, "history.js no longer emits the change-row component")
    for one in sorted(emitted):
      declaring = sorted(p.relative_to(BROWSER).as_posix() for p, s in sheets.items() if one in s)
      with self.subTest(**{"class": one}):
        self.assertLessEqual(len(declaring), 1, f".{one} is declared by {declaring}")

  def test_the_texts_record_card_is_declared_in_exactly_one_stylesheet(self):
    """`.detail` and `.detail-title` were shadowed the same way in texts.css."""
    sheets = {p: subject_classes(p) for p in [CORE_CSS] + instrument_stylesheets()}
    emitted = {c for c in emitted_classes(BROWSER / "texts/texts.js") if c.startswith("record")}
    emitted |= {c for c in emitted_classes(BROWSER / "texts/index.html") if c.startswith("record")}
    self.assertTrue(emitted, "texts no longer emits the record-card component")
    for one in sorted(emitted):
      declaring = sorted(p.relative_to(BROWSER).as_posix() for p, s in sheets.items() if one in s)
      with self.subTest(**{"class": one}):
        self.assertLessEqual(len(declaring), 1, f".{one} is declared by {declaring}")

  def test_the_history_page_emits_no_control_bar_class(self):
    """history/ has no control bar; a `.field` there can only be the old collision."""
    for path in [BROWSER / "history/history.js", BROWSER / "history/index.html"]:
      with self.subTest(path=path.name):
        offending = {c for c in emitted_classes(path) if c == "field" or c.startswith("field-")}
        self.assertEqual(offending, set(), f"{path.name} emits {sorted(offending)}")

  def test_the_texts_page_emits_no_shared_detail_class(self):
    """The record card must not wear the name of the shared record panel."""
    for path in [BROWSER / "texts/texts.js", BROWSER / "texts/index.html"]:
      with self.subTest(path=path.name):
        offending = {c for c in emitted_classes(path) if c == "detail" or c.startswith("detail-")}
        self.assertEqual(offending, set(), f"{path.name} emits {sorted(offending)}")


class DocumentLandmarkTest(unittest.TestCase):
  def test_every_main_in_the_tree_is_a_landmark_the_plumbing_knows(self):
    """`fail` found `#reading` and nothing else, so three instruments got silence."""
    landmarks = declared_landmarks()
    pages = main_ids()
    self.assertGreaterEqual(len(pages), 10, "expected the browser tree to hold its pages")
    for page, identifier in sorted(pages.items()):
      with self.subTest(page=page):
        self.assertIn(
          identifier, landmarks,
          f"{page} names its <main> #{identifier}, which is not in "
          "DOCUMENT_LANDMARKS, so Triptych.fail() on that page renders nowhere",
        )

  def test_reading_is_still_the_first_landmark(self):
    """Every caller that passed no target must keep landing where it did."""
    self.assertEqual(declared_landmarks()[0], "reading")

  @unittest.skipIf(NODE is None, "node is not installed; the model cannot be replayed")
  def test_the_failure_plumbing_reaches_every_landmark(self):
    """Replayed against a stub document, one page landmark at a time.

    A page carrying only `#map` or only `#canon` or only `#reader-document` must
    receive the error, drop `aria-busy`, and get the spoken line. An explicit
    element or id must win over the list, and a page with no landmark at all
    must still be told, through the live region `statusLine` creates.
    """
    result = subprocess.run(
      [NODE, "-e", REPLAY, str(CORE_JS), json.dumps(declared_landmarks())],
      cwd=ROOT, capture_output=True, text=True,
    )
    self.assertEqual(result.returncode, 0, result.stderr.strip())
    report = json.loads(result.stdout)
    for landmark in declared_landmarks():
      with self.subTest(landmark=landmark):
        self.assertEqual(report["alone"][landmark]["region"], landmark)
        self.assertEqual(report["alone"][landmark]["errors"], 1)
        self.assertEqual(report["alone"][landmark]["busy"], "false")
        self.assertEqual(report["alone"][landmark]["spoken"], "boom")
    self.assertEqual(report["default"], declared_landmarks()[0])
    self.assertEqual(report["byId"], declared_landmarks()[-1])
    self.assertEqual(report["byElement"], "somewhere-else")
    self.assertIsNone(report["noLandmark"]["region"])
    self.assertEqual(report["noLandmark"]["spoken"], "boom")


def published_entrances() -> tuple[str, ...]:
  """The entrance directories the build publishes, read off the generator."""
  found = re.search(r"^WEB_BROWSER_ENTRANCES = \(([^)]*)\)", GENERATOR.read_text(), re.M)
  if found is None:
    raise AssertionError("tools/public-alpha no longer declares WEB_BROWSER_ENTRANCES")
  return tuple(re.findall(r'"([^"]+)"', found.group(1)))


def layout_chrome_classes() -> set[str]:
  """Every class the layout stands on every page, and nothing a page owns.

  Read off `layout.html`, plus the two pieces `wrap_in_layout` writes in
  around it — the release banner and the breadcrumb — which are asserted to
  still be the generator's own names. `skip-link` is left out: every browser
  page carries one of its own and the shared core styles that class for both.
  """
  found: set[str] = set()
  for value in re.findall(r'class="([^"{]*)"', LAYOUT.read_text()):
    found |= set(value.split())
  generator = GENERATOR.read_text()
  for written in ("release-banner", "breadcrumb"):
    if f'class="{written}' not in generator:
      raise AssertionError(f"tools/public-alpha no longer writes .{written}")
    found.add(written)
  return found - {"skip-link"}


def selectors(path: Path) -> list[str]:
  """Every complex selector in a stylesheet, split only at TOP-LEVEL commas.

  The commas inside `:has(> .a, > .b)` belong to the argument, not to the
  list; splitting there would read half a scope as a selector of its own.
  """
  found: list[str] = []
  for block in re.finditer(r"([^{}]+)\{", without_comments(path.read_text())):
    prelude = block.group(1).strip()
    if not prelude or prelude.startswith("@"):
      continue
    depth, start = 0, 0
    for index, character in enumerate(prelude):
      if character == "(":
        depth += 1
      elif character == ")":
        depth -= 1
      elif character == "," and depth == 0:
        found.append(prelude[start:index].strip())
        start = index + 1
    found.append(prelude[start:].strip())
  return [one for one in found if one]


# The classes the BUILD writes onto every browser page's wrapper. A `:has()`
# naming one of them scopes nothing, because every page carries it.
BUILD_WRAPPER_CLASSES = {"page-shell", "page-browser", "section-toned"}

def without_where(selector: str) -> str:
  """The selector with every `:where(...)` removed — its specificity-bearing part."""
  return re.sub(r":where\((?:[^()]|\([^()]*\))*\)", "", selector).strip()


def page_scoped(selector: str) -> bool:
  """Does the selector reach the chrome only from inside a named page?

  It must carry a `:has()` whose argument names a class some page owns — not
  a class the build stamps on every wrapper, and not the chrome itself.
  """
  for argument in re.findall(r":has\(([^()]*)\)", selector):
    named = set(re.findall(r"\.([A-Za-z0-9_-]+)", argument))
    named -= BUILD_WRAPPER_CLASSES | layout_chrome_classes()
    named = {one for one in named if not one.startswith("section-")}
    if named:
      return True
  return False


class LayoutChromeScopeTest(unittest.TestCase):
  def test_no_instrument_reaches_the_layout_chrome_unscoped(self):
    """`body > .site-header` in day-missal.css restyled every page's header."""
    chrome = layout_chrome_classes()
    self.assertTrue({"site-header", "site-footer", "brand"} <= chrome, chrome)
    for sheet in instrument_stylesheets():
      name = sheet.relative_to(BROWSER).as_posix()
      unscoped = {
        one for one in selectors(sheet)
        if set(re.findall(r"\.([A-Za-z0-9_-]+)", one)) & chrome and not page_scoped(one)
      }
      with self.subTest(stylesheet=name):
        self.assertEqual(
          unscoped, set(),
          f"{name} reaches the layout's chrome from {sorted(unscoped)}; scope "
          "it under a class the page owns, as `body:has(.reader-instrument) > "
          ".site-header` does",
        )

  def test_the_day_missal_header_rules_keep_their_cascade_weight(self):
    """The scope is a `:where()`, so the four pages' cascade is unchanged.

    Strip the `:where(...)` and each selector is the one it replaced; a scope
    that added specificity could have changed which rule wins on the very
    pages this file is meant for.
    """
    sheet = BROWSER / "liturgy/day-missal.css"
    header = [one for one in selectors(sheet) if ".site-header" in one]
    self.assertEqual(len(header), 12, "the twelve header selectors are all here")
    for one in header:
      with self.subTest(selector=one):
        self.assertTrue(one.startswith("body:where(:has("), one)
        self.assertTrue(without_where(one).startswith("body > .site-header"), one)

  def test_the_sources_chrome_rules_keep_their_cascade_weight(self):
    """The same for Sources: its two chrome rules were bare `.brand a` and
    `.site-footer a`, and with the `:where()` scope removed they still are."""
    sheet = BROWSER / "sources/sources.css"
    chrome = [one for one in selectors(sheet)
              if re.search(r"\.(brand|site-footer)\b", one)]
    self.assertEqual(sorted(without_where(one) for one in chrome),
                     [".brand a", ".site-footer a"])
    for one in chrome:
      with self.subTest(selector=one):
        self.assertTrue(one.startswith(":where(body:has(> .sources-page))"), one)

  def test_the_day_missal_scope_names_exactly_the_pages_that_load_it(self):
    """A page that starts loading day-missal.css is a decision, not a drift.

    The scope lists page classes; this derives the published pages that load
    the sheet and requires each to carry a scoped class and no other page to.
    """
    sheet = BROWSER / "liturgy/day-missal.css"
    scope: set[str] = set()
    for one in selectors(sheet):
      if ".site-header" in one:
        for argument in re.findall(r":has\(([^()]*)\)", one):
          scope |= set(re.findall(r"\.([A-Za-z0-9_-]+)", argument))
    loaders, others = [], []
    for entrance in published_entrances():
      for page in sorted((BROWSER / entrance).glob("*.html")):
        text = page.read_text()
        body = re.search(r'<body[^>]*\bclass="([^"]*)"', text)
        classes = set(body.group(1).split()) if body else set()
        (loaders if 'href="day-missal.css"' in text else others).append((page, classes))
    self.assertGreaterEqual(len(loaders), 4, "expected the Day pages to load the sheet")
    for page, classes in loaders:
      with self.subTest(loads=page.name):
        self.assertTrue(classes & scope, f"{page.name} loads day-missal.css outside its scope")
    for page, classes in others:
      with self.subTest(does_not_load=page.relative_to(BROWSER).as_posix()):
        self.assertFalse(classes & scope, f"{page.name} is in scope but never loads the sheet")


class CitationVocabularyTest(unittest.TestCase):
  def test_the_two_pages_gloss_the_identical_vocabulary(self):
    """history.js's CITATION_WORDS is a copy of law.js's that lost a key.

    Comparing the two maps, rather than only asserting the missing key is back,
    is the assertion that would have caught the omission when it happened, and
    the one that keeps them together until the shared extraction lands. It is a
    source-level comparison standing in for a runtime one: both literals are
    plain constant tables inside page IIFEs that no node harness loads.
    """
    history = citation_words(BROWSER / "history/history.js")
    law = citation_words(BROWSER / "law/law.js")
    self.assertEqual(history, law, "the history and law glosses have parted")

  def test_none_claimed_is_glossed_and_the_gloss_says_something(self):
    """26 of 59 stations in the default slice rendered `none-claimed — ` bare."""
    words = citation_words(BROWSER / "history/history.js")
    self.assertIn("none-claimed", words)
    self.assertTrue(words["none-claimed"].strip(), "the gloss is empty")

  def test_every_citation_state_the_corpus_carries_is_glossed(self):
    """A station whose state has no gloss renders a dash with nothing after it."""
    words = citation_words(BROWSER / "history/history.js")
    states: dict[str, int] = {}
    for slice_file in sorted(ACT_HISTORY.glob("*.json")):
      if slice_file.name == "index.json":
        continue
      for station in json.loads(slice_file.read_text()).get("stations", []):
        state = station.get("act_citation")
        if state:
          states[state] = states.get(state, 0) + 1
    self.assertTrue(states, "no act-keyed slice carries an act_citation")
    for state, count in sorted(states.items()):
      with self.subTest(state=state, stations=count):
        self.assertIn(state, words)
        self.assertTrue(words[state].strip())


# Replayed by the landmark test. CommonJS so it needs no module flag, and it
# builds the smallest document browser-core.js will load against.
REPLAY = r"""
const fs = require('node:fs');
const vm = require('node:vm');

const source = fs.readFileSync(process.argv[1], 'utf8');
const landmarks = JSON.parse(process.argv[2]);

function element(id) {
  return {
    nodeType: 1, id: id, children: [], attributes: {}, textContent: '', hidden: true,
    firstChild: null,
    appendChild(child) { this.children.push(child); return child; },
    removeChild() {},
    setAttribute(name, value) { this.attributes[name] = value; }
  };
}

function load(ids) {
  const nodes = new Map(ids.map((id) => [id, element(id)]));
  const body = element('body');
  const document = {
    body: body,
    getElementById: (id) => nodes.get(id) || nodes.get('made:' + id) || null,
    createElement: (tag) => {
      const node = element('');
      node.tagName = tag.toUpperCase();
      return node;
    }
  };
  const appendToBody = body.appendChild.bind(body);
  body.appendChild = (child) => {
    if (child.id) nodes.set(child.id, child);
    return appendToBody(child);
  };
  const window = { location: { search: '', hash: '' }, addEventListener() {} };
  const context = vm.createContext({
    window: window, document: document, console: console, URLSearchParams: URLSearchParams,
    fetch: async () => { throw new Error('no network in the replay'); },
    setTimeout: setTimeout, history: { replaceState() {}, pushState() {} }
  });
  context.globalThis = context;
  vm.runInContext(source, context, { filename: 'browser-core.js' });
  return { T: window.Triptych, document: document };
}

const spoken = (document) => {
  const status = document.getElementById('reading-status');
  return status ? status.textContent : null;
};

const report = { alone: {} };
for (const landmark of landmarks) {
  const { T, document } = load([landmark]);
  const region = T.documentRegion();
  T.fail('boom');
  report.alone[landmark] = {
    region: region ? region.id : null,
    errors: region ? region.children.length : 0,
    busy: region ? region.attributes['aria-busy'] : null,
    spoken: spoken(document)
  };
}

const every = load(landmarks);
report.default = every.T.documentRegion().id;
report.byId = every.T.documentRegion(landmarks[landmarks.length - 1]).id;
report.byElement = every.T.documentRegion(element('somewhere-else')).id;

const bare = load([]);
bare.T.fail('boom');
report.noLandmark = { region: bare.T.documentRegion(), spoken: spoken(bare.document) };

process.stdout.write(JSON.stringify(report));
"""


if __name__ == "__main__":
  unittest.main()
