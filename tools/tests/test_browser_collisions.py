#!/usr/bin/env python3
"""Name collisions between the shared browser stylesheet and an instrument's own.

Three defects sat in the browser tree and each one is a class of defect rather
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

4. AN INSTRUMENT RESTYLING THE SITE'S OWN CHROME, UNSCOPED. The fourth hazard of
   the same family, and the one the promised deliverable still holds open. A
   class the published layout owns — `.site-header`, `.site-footer`, `.brand`,
   `.skip-link`, `.triptych-mark` — restyled from an instrument stylesheet with
   no page scope is a rule that reaches every page on the site as soon as a
   shared bundle carries the file. `day-missal.css` does it to `body >
   .site-header` in twelve selectors, and cannot be corrected from a corpus lane
   because it belongs to a protected in-progress Liturgy deliverable;
   `sources.css` did it to `.brand a` and `.site-footer a` and is corrected.
   SITE_CHROME_UNSCOPED records the protected remainder rather than permitting
   the class, so a new one cannot arrive unnoticed while the recorded one waits
   for its owner.

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
ACT_HISTORY = ROOT / "src/web/data/structure/act-history"
LAYOUT = ROOT / "release/public-alpha/layout.html"
NODE = shutil.which("node")

# The one stylesheet still restyling the site's chrome from outside a page scope,
# with the count of selectors that do it and why it is not corrected here.
#
# `day-missal.css` is loaded by four published Liturgy pages and belongs to the
# `liturgy-reader-live-ritual-flow-2026-08-07` deliverable's protected reader
# family, which promised-deliverables.toml records as `in_progress`. Master-plan
# decisions D2 and D18 keep that family closed until its owner releases or
# carves out the seam, so scoping these selectors is that deliverable's change
# and not a corpus lane's. `shared-shell-blocking-collisions-resolved` stays
# unmet for exactly this reason.
#
# The count is here so that the exception cannot quietly grow inside the one
# file that holds it: adding a thirteenth unscoped selector fails this test even
# though the file is exempt.
SITE_CHROME_UNSCOPED = {
  "liturgy/day-missal.css": 12,
}

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


def layout_owned_classes() -> set[str]:
  """Classes the published layout puts on the page around `<main>`.

  Read off `layout.html` rather than listed, so a masthead or footer element the
  layout gains is governed without anyone remembering to add it here. The
  release banner is added by hand because the layout carries it as a `{{…}}`
  marker and `wrap_in_layout` substitutes the element.
  """
  found = {"release-banner"}
  for value in re.findall(r'class="([^"{}]*)"', LAYOUT.read_text()):
    found |= set(value.split())
  return found


def site_chrome_selectors(path: Path) -> list[str]:
  """Selectors in one stylesheet that reach the layout's chrome with no page scope.

  A selector qualifies as scoped when it names any class the layout does not own:
  `body:has(.reader-instrument) > .site-header` is a rule about one kind of page,
  and `body:has(> .sources-page) .site-footer a` is a rule about one route. A
  selector whose only classes are the layout's — `body > .site-header` — is a
  rule about every page on the site, wherever the file is loaded from, and that
  is the hazard.
  """
  owned = layout_owned_classes()
  found: list[str] = []
  for block in re.finditer(r"([^{}]+)\{", without_comments(path.read_text())):
    selector = block.group(1).strip()
    if not selector or selector.startswith("@"):
      continue
    for one in selector.split(","):
      one = one.strip()
      if not one:
        continue
      classes = set(re.findall(r"\.([A-Za-z0-9_-]+)", one))
      if classes & owned and not classes - owned:
        found.append(one)
  return found


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


class SiteChromeScopeTest(unittest.TestCase):
  """The fourth hazard: an instrument stylesheet restyling the site's own chrome.

  `browser_page_parts` appends a browser page's own body classes to `<main>`, not
  to `<body>`, so in the published artifact the page has no class outside the
  landmark. A rule written as `body > .site-header` therefore matches on every
  route the file reaches, and the only thing keeping it off the other twelve is
  which pages happen to link the stylesheet. That is the same
  correctness-by-load-order the `.field` and `.detail` renames removed.
  """

  def test_the_layout_owns_the_chrome_these_tests_are_about(self):
    """If the masthead loses its class the rest of this class proves nothing."""
    owned = layout_owned_classes()
    for expected in ("site-header", "site-footer", "brand", "skip-link", "release-banner"):
      with self.subTest(**{"class": expected}):
        self.assertIn(expected, owned)

  def test_no_unrecorded_instrument_stylesheet_restyles_the_site_chrome(self):
    for sheet in instrument_stylesheets():
      name = sheet.relative_to(BROWSER).as_posix()
      with self.subTest(stylesheet=name):
        found = site_chrome_selectors(sheet)
        if name in SITE_CHROME_UNSCOPED:
          continue
        self.assertEqual(
          found, [],
          f"{name} restyles the published layout's own chrome with no page "
          f"scope: {found}. Pulled into a shared bundle the rule reaches every "
          "page on the site. Scope it by a class the layout does not own, or "
          "record it in SITE_CHROME_UNSCOPED with the authority that owns it",
        )

  def test_the_recorded_exception_neither_grows_nor_outlives_its_file(self):
    """The protected file may keep its selectors; it may not acquire more."""
    for name, expected in sorted(SITE_CHROME_UNSCOPED.items()):
      with self.subTest(stylesheet=name):
        sheet = BROWSER / name
        self.assertTrue(sheet.is_file(), f"{name} no longer exists; drop its entry")
        found = site_chrome_selectors(sheet)
        self.assertEqual(
          len(found), expected,
          f"{name} now has {len(found)} unscoped site-chrome selectors rather "
          f"than the recorded {expected}: {found}. If the protected owner scoped "
          "them, lower the count or delete the entry; if a new one was added, it "
          "widened a hazard the ledger already holds open",
        )

  def test_the_shared_stylesheet_is_the_one_place_the_chrome_is_owned(self):
    """browser-core.css is exempt because owning the shared furniture is its job."""
    self.assertTrue(
      site_chrome_selectors(CORE_CSS),
      "shared/browser-core.css no longer styles the site chrome at all, which "
      "would mean the furniture moved and this test is measuring the wrong file",
    )


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
