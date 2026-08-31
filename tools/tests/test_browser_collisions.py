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
   rule in an instrument stylesheet that can match an element the published
   layout owns — the masthead, the brand, the navigation, the release banner, the
   footer, the skip link, and every link, paragraph and span inside them — is a
   rule that reaches every page on the site as soon as a shared bundle carries
   the file. `day-missal.css` does it to `body > .site-header` in twelve
   selectors and cannot be corrected from a corpus lane, because it belongs to a
   protected in-progress Liturgy deliverable; `sources.css` did it to `.brand a`
   and `.site-footer a` and is corrected.

   THE QUESTION "CAN THIS SELECTOR MATCH THE SITE'S CHROME" HAS BEEN ANSWERED
   TWICE, AND THE FIRST ANSWER WAS WITHDRAWN. The first replacement read selector
   text: it split arms into compounds in Python, modelled combinators, `:not()`
   and `:root`, and inferred route scope from names the layout does not own. An
   independent cold review reproduced two classes of unsoundness in it, and both
   were unsoundness for VALID CSS: an unknown pseudo-class was treated as
   satisfiable, which is conservative in a positive position and exactly
   backwards inside `:not()` — so `a:not(:hover)` and
   `.site-header:not(:focus-within)`, which match site chrome in ordinary
   states, were read as unable to — and scope was inferred from raw text, so
   `a[href$=".html"]` was read as scoped by `.html`, a value suffix; and
   `body:has(.plan-page, .site-header) .site-footer a` as scoped when its
   `.site-header` alternative makes it global; and `:is(:not(.plan-page),
   .plan-page) a` — a tautology — as scoped at all. What this suite keeps from
   that pass is only what was always sound: the shell is rendered by the build's
   own `wrap_in_layout`, the page's identity lives on `<main>`, and the
   protected remainder is an exact selector inventory, not a count.

   What decides selector truth now is Chromium. `site_chrome_selector_oracle.mjs`
   serves the build's real shells — the neutral one, with the page's identity
   absent, and every published page exactly as the build emits it — and answers,
   per selector arm and per shell state, whether the arm selects an element the
   layout owns, under a bounded matrix of real user states: the pointer over
   every chrome leaf, a press held there, keyboard focus on every focusable
   chrome element, and the document's fragment target. `:not()`, `:is()`,
   `:where()`, `:has()`, attributes with flags, escapes, nested functional
   pseudos and pseudo-elements are decided by the browser's own engine, because
   the browser is the engine that will run the stylesheet. An arm the browser
   refuses — invalid here, or naming `:visited`, whose truth Chromium withholds
   from script, or forcing a user state in two distinct compounds, which the
   walk holds one at a time and therefore cannot establish — is reported, never
   passed. Python locates rules in tracked files, splits selector lists at
   top-level commas, normalizes identities, orchestrates the protocol and
   compares the verdicts to the recorded inventories; it no longer interprets
   what a selector means.

   The verdict is a differential, not a name scan: an arm is unsafe when it can
   reach site chrome in the NEUTRAL shell — the state in which the route's own
   identity is absent from `<main>` — regardless of what route-looking text it
   contains. An arm that reaches chrome only where a class the layout does not
   own is genuinely projected is positively scoped, which is how this repository
   writes route scope (`body:has(> .sources-page) .site-footer a`). The exact
   semantics, and what is NOT proved, are stated in the oracle harness and in
   SelectorOracleSemanticsTest.

Source-level tests read the files rather than a rendered page; the selector
verdict is the one thing this suite refuses to decide in Python.
"""

from __future__ import annotations

import atexit
import functools
import importlib.machinery
import importlib.util
import json
import os
import queue
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).resolve().parents[2]
BROWSER = ROOT / "src/web/browser"
CORE_CSS = BROWSER / "shared/browser-core.css"
CORE_JS = BROWSER / "shared/browser-core.js"
ACT_HISTORY = ROOT / "src/web/data/structure/act-history"
PUBLIC_ALPHA = ROOT / "tools/public-alpha"
ORACLE = ROOT / "tools/tests/site_chrome_selector_oracle.mjs"
NODE = shutil.which("node")
MAKE = shutil.which("make")

CHROME_CANDIDATES = (
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/google-chrome",
)


def chrome_binary() -> str | None:
  """The Chromium the oracle would drive, or None when this host has none."""
  declared = os.environ.get("TRIPTYCH_CHROME")
  if declared and Path(declared).exists():
    return declared
  for candidate in CHROME_CANDIDATES:
    if Path(candidate).exists():
      return candidate
  return None


CHROMIUM = chrome_binary()
# The semantic verdict is the browser's. Where no browser can be driven, the
# selector tests SKIP with this reason rather than passing on a weaker answer:
# a skip claims nothing, which is the one thing a false green must not do.
BROWSER_REQUIRED = unittest.skipUnless(
  NODE is not None and CHROMIUM is not None,
  "no Chromium to drive (set TRIPTYCH_CHROME); whether a selector can reach the "
  "site's chrome is decided by the browser, and this host cannot observe it, so "
  "these tests claim nothing rather than a proof they did not make",
)


class ProtectedChrome(NamedTuple):
  """One stylesheet reaching the site's chrome that this lane may not correct.

  `selectors` is the exact normalized inventory, in file order, duplicates kept.
  A count would let one recorded selector be replaced by a different one for
  free, which is the defect an independent review found in the first version of
  this record; a list cannot be substituted into.
  """

  authority: str
  reason: str
  selectors: tuple[str, ...]


# Every stylesheet that reaches the published layout's own chrome from outside a
# route scope, with the authority that owns each and why it is not corrected
# here. Nothing is permitted by being listed: the entry is the record that the
# hazard is real, unresolved, and someone else's to resolve.
#
# All four belong to the protected Liturgy reader family. Master-plan decisions
# D2 and D18 and boundary 4 close that family until its owning Liturgy work
# releases or carves out the seam, so scoping any of these is that deliverable's
# change and not a corpus lane's. `shared-shell-blocking-collisions-resolved`
# stays unmet for exactly this reason.
LITURGY_READER_FAMILY = (
  "protected Liturgy reader family; master-plan decisions D2 and D18 and "
  "boundary 4. liturgy-reader-live-ritual-flow-2026-08-07 is in_progress with "
  "all six requirements open"
)

SITE_CHROME_UNSCOPED = {
  "liturgy/day-missal.css": ProtectedChrome(
    authority=LITURGY_READER_FAMILY,
    reason=(
      "The twelve selectors §11.1(d) of guidance/corpus-browser-implementation.md "
      "states exactly. They re-lay-out `body > .site-header` — grid columns, gap, "
      "min-height, padding, the triptych mark's geometry, both brand font sizes, "
      "the nav gap, and `display: none` at print — on every page that loads the "
      "file, which is four published Liturgy routes today and would be the whole "
      "site inside a shared bundle. The smallest mechanical correction and the "
      "one-sentence carve-out it needs are stated there."
    ),
    selectors=(
      "body > .site-header",
      "body > .site-header .triptych-mark",
      "body > .site-header .triptych-mark i",
      "body > .site-header .triptych-mark i:nth-child(2)",
      "body > .site-header .brand a",
      "body > .site-header .brand span",
      "body > .site-header nav",
      # inside @media (max-width: 47.5rem)
      "body > .site-header",
      "body > .site-header .brand span",
      "body > .site-header nav",
      "body > .site-header nav a",
      # inside @media print
      "body > .site-header",
    ),
  ),
  "liturgy/reader-shell.css": ProtectedChrome(
    authority=LITURGY_READER_FAMILY,
    reason=(
      "A bare `html` rule setting `scroll-padding-block` from the reader's own "
      "shell height, and a `:root` block declaring the shell height and the four "
      "safe-area insets. Both reach the document root of every page that loads "
      "the file. `reader-instrument.css` already writes the scoped form of the "
      "same rule as `html:has(.reader-instrument)`, so the correction is known "
      "and is that family's to make."
    ),
    selectors=(
      ":root",
      "html",
      # inside @media (max-width: 47.5rem)
      "html",
    ),
  ),
  "liturgy/reader-instrument.css": ProtectedChrome(
    authority=LITURGY_READER_FAMILY,
    reason=(
      "Two `:root` blocks declaring the instrument's own typeface, ink, paper and "
      "shell-height custom properties at the document root. Every other rule in "
      "the file is scoped through `:has(.reader-instrument)`; these two are not, "
      "so a name collision with a property the site's own stylesheet reads would "
      "reach the chrome of every page carrying the file."
    ),
    selectors=(
      ":root",
      # inside @media (max-width: 47.5rem)
      ":root",
    ),
  ),
  "liturgy/reader-visual-reset.css": ProtectedChrome(
    authority=(
      "liturgy-reader-visual-reset-candidate-2026-08-05 (complete) inside the "
      + LITURGY_READER_FAMILY
    ),
    reason=(
      "Two `:root` blocks of the same shape as reader-instrument.css's, and "
      "`a:focus-visible`, which restyles the focus ring of every masthead, "
      "navigation and footer link on the two published visual-reset routes. The "
      "sibling `button:`/`input:`/`select:`/`summary:focus-visible` rules in the "
      "same block reach no chrome element and are not listed."
    ),
    selectors=(
      ":root",
      "a:focus-visible",
      # inside @media (max-width: 47.5rem)
      ":root",
    ),
  ),
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


# ===========================================================================
# Selector extraction: where the arms come from
#
# This layer locates rules in tracked files and splits selector lists. It does
# NOT decide what any arm means — that is the browser's verdict below. It is
# deliberately small, and what it refuses to split it surfaces: an arm this
# layer cannot extract is an arm nobody has classified, and the semantic tests
# below prove the extraction on exactly the shapes that could confuse it.
# ===========================================================================

def split_top_level(text: str, separator: str = ",") -> list[str]:
  """Split on a separator that is not inside brackets, quotes or parentheses."""
  parts: list[str] = []
  current: list[str] = []
  depth = 0
  quote = ""
  for character in text:
    if quote:
      current.append(character)
      if character == quote:
        quote = ""
      continue
    if character in "\"'":
      quote = character
      current.append(character)
      continue
    if character in "([":
      depth += 1
    elif character in ")]":
      depth -= 1
      if depth < 0:
        raise ValueError(f"unbalanced brackets in {text!r}")
    if character == separator and depth == 0:
      parts.append("".join(current))
      current = []
      continue
    current.append(character)
  if depth or quote:
    raise ValueError(f"unbalanced brackets or quotes in {text!r}")
  parts.append("".join(current))
  return parts


def normalize_selector(selector: str) -> str:
  text = re.sub(r"\s+", " ", selector.strip())
  return re.sub(r"\s*([>+~])\s*", r" \1 ", text).strip()


def selector_arms(path: Path):
  """Every selector arm in one stylesheet, at-rule preludes excluded."""
  for block in re.finditer(r"([^{}]+)\{", without_comments(path.read_text())):
    selector = block.group(1).strip()
    if not selector or selector.startswith("@"):
      continue
    for arm in split_top_level(selector):
      arm = arm.strip()
      if arm:
        yield arm


# ===========================================================================
# The browser as the semantic selector oracle
#
# The shells are not described here and the arms are not interpreted here. The
# build's own `wrap_in_layout` renders every state the oracle judges — the
# neutral one and every published page — and Chromium answers, per arm and per
# state, whether the arm selects an element the layout owns. See
# site_chrome_selector_oracle.mjs for the protocol and the bounded claim.
# ===========================================================================

CHROME_MODEL_CONTENT = '<p id="chrome-model-content">content</p>'
# The page's own classes land on `<main>`, not on `<body>`, so the neutral shell
# is rendered with an empty page class: `<main>`'s class attribute belongs to the
# page, and the neutral state is the one where the page has projected none of it.
CHROME_MODEL_PAGE_CLASS = ""

# The states in which the route's own identity is absent. An arm that reaches
# site chrome in either of these is unscoped, whatever route-looking text it
# carries. Both shells are rendered, because the preview shell adds the release
# banner the public one does not.
NEUTRAL_STATES = frozenset({"chrome-model (public)", "chrome-model (preview)"})

# Where the user-state matrix (hover, active, focus, focus-visible, target) is
# actually walked: the two shells whose reach decides the verdict, plus one
# published page in the preview shell, which is the state carrying the chrome
# element — the release banner — the neutral shells do not have. Every state
# still gets the quiescent pass, which is where static reach is recorded; a
# dynamic reach OUTSIDE the walked states is not observed, and the report names
# the walked states rather than leaving the bound implicit. This is the
# bounded-runtime decision: the walk costs one round trip per sub-state, and
# walking it in all ~36 shells would multiply that by a factor that buys no
# additional verdict, because the chrome is the build's and identical in all of
# them up to the banner.
DYNAMIC_WALK_STATES = sorted(NEUTRAL_STATES) + [
  "browser scripture/index.html (preview)",
]


@functools.lru_cache(maxsize=None)
def public_alpha():
  loader = importlib.machinery.SourceFileLoader(
    "collisions_public_alpha", str(PUBLIC_ALPHA)
  )
  spec = importlib.util.spec_from_loader(loader.name, loader)
  if spec is None:
    raise RuntimeError("could not load tools/public-alpha")
  module = importlib.util.module_from_spec(spec)
  loader.exec_module(module)
  return module


@functools.lru_cache(maxsize=None)
def oracle_states() -> tuple[tuple[str, str], ...]:
  """(name, html) for every shell the oracle judges selectors against.

  Rendered by the build's own machinery, not by a second copy of it: the
  neutral shells through `wrap_in_layout` with the page's identity absent, and
  every published browser page exactly as the build renders it — same wrapper,
  same head extras, same projection of the page's classes onto `<main>`. Four
  site pages outside the browser tree stand in for the routes a shared bundle
  would reach that no instrument stylesheet is linked from. Every state is
  rendered in both the public and the preview shell.
  """
  module = public_alpha()
  states: list[tuple[str, str]] = []

  def render(name, source_relative, output_relative, page_class, title,
             head_extra="", body_extra="", declared_description="",
             declared_robots=""):
    for preview in (False, True):
      html = module.wrap_in_layout(
        source_relative, output_relative, page_class, title, "",
        CHROME_MODEL_CONTENT, preview, {},
        head_extra=head_extra, body_extra=body_extra,
        declared_description=declared_description,
        declared_robots=declared_robots,
      )
      states.append((f"{name} ({'preview' if preview else 'public'})", html))

  render(
    "chrome-model", "src/web/browser/scripture/index.html",
    "scripture/index.html", CHROME_MODEL_PAGE_CLASS, "Chrome model",
  )
  for output_relative, source in sorted(module.web_browser_pages().items()):
    parts = module.browser_page_parts(source, output_relative)
    render(
      f"browser {output_relative}", source.relative_to(ROOT).as_posix(),
      output_relative, parts["page_class"], parts["title"],
      head_extra=parts["head_extra"], body_extra=parts["body_extra"],
      declared_description=parts["declared_description"],
      declared_robots=parts["declared_robots"],
    )
  for source_relative, output_relative in (
    ("README.md", "index.html"),
    ("ABOUT.md", "about.html"),
    ("library/liturgy.md", "library/liturgy.html"),
    ("web/articles/faith/example.md", "web/articles/faith/example.html"),
  ):
    render(
      f"site {output_relative}", source_relative, output_relative,
      module.page_classes(source_relative, output_relative), "Chrome model",
    )
  return tuple(states)


class OracleProtocolError(RuntimeError):
  """The oracle harness failed to answer, or answered with an error."""


class ArmAnswer(NamedTuple):
  """What Chromium said about one selector arm, under the whole state matrix.

  `reach` maps each shell state to None (it selects no chrome element there) or
  to the witness: the user sub-state that reached, and the element reached.
  `refusal` is the stated reason the browser could not be asked at all —
  invalid or unsupported here, naming a pseudo-class whose truth Chromium
  withholds from script, or forcing a user state in two distinct compounds,
  which the walk holds one at a time and so cannot establish. A refusal is an
  unsafe verdict, never a silence.
  """

  arm: str
  accepted: bool
  serialized: str | None
  origin: str | None
  judged: str
  dynamic: bool
  refusal: str | None
  reach: dict


class SelectorOracle:
  """One Chromium session behind the harness's line-JSON protocol.

  The browser is started ONCE for this whole module and every question every
  test asks is answered inside that session, batched per request. That is the
  bounded-runtime contract: not one Chromium per selector, not one per test.
  """

  REQUEST_TIMEOUT_S = 900

  def __init__(self) -> None:
    if NODE is None:
      raise OracleProtocolError("node is not installed; the oracle cannot run")
    # What the harness MEASURED about each shell when it installed itself: the
    # chrome descriptors, the hover targets, the focus stops, the fragment
    # identifiers, and the interactive elements. The last of these is the bound
    # on the form and element states the walk does not force, and it is asserted
    # rather than left as an unread number.
    self.shells: dict = {}
    self.process = subprocess.Popen(
      [NODE, str(ORACLE)],
      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
      text=True, cwd=ROOT,
    )
    self.replies: queue.Queue = queue.Queue()
    self.stderr: list[str] = []
    threading.Thread(target=self._drain, args=(self.process.stdout,), daemon=True).start()
    threading.Thread(
      target=self._drain_stderr, args=(self.process.stderr,), daemon=True
    ).start()

  def _drain(self, stream) -> None:
    for line in stream:
      try:
        self.replies.put(json.loads(line))
      except json.JSONDecodeError:
        self.replies.put({"ok": False, "error": f"unparsable oracle line: {line!r}"})
    self.replies.put(None)

  def _drain_stderr(self, stream) -> None:
    for chunk in stream:
      self.stderr.append(chunk)
      del self.stderr[:-40]

  def request(self, op: str, timeout_s: int | None = None, **fields) -> dict:
    assert self.process.stdin is not None
    self.process.stdin.write(json.dumps({"op": op, **fields}) + "\n")
    self.process.stdin.flush()
    reply = self.replies.get(timeout=timeout_s or self.REQUEST_TIMEOUT_S)
    if reply is None:
      raise OracleProtocolError(
        "the oracle harness exited: " + "".join(self.stderr)[-1500:]
      )
    if not reply.get("ok"):
      raise OracleProtocolError(
        f"oracle op {op!r} failed: {reply.get('error', 'unknown')}"
      )
    return reply

  def close(self) -> None:
    try:
      self.request("quit", timeout_s=30)
    except Exception:
      pass
    try:
      self.process.stdin.close()
    except Exception:
      pass
    self.process.terminate()


_ORACLE: SelectorOracle | None = None


def oracle() -> SelectorOracle:
  global _ORACLE
  if _ORACLE is None:
    client = SelectorOracle()
    atexit.register(client.close)
    client.shells = client.request(
      "init",
      states=[{"name": name, "html": html} for name, html in oracle_states()],
      dynamicStates=DYNAMIC_WALK_STATES,
    )["states"]
    _ORACLE = client
  return _ORACLE


def ask_arms(arms) -> dict[str, ArmAnswer]:
  """Ask Chromium about selector arms, deduplicating the wire requests."""
  unique = list(dict.fromkeys(arms))
  if not unique:
    return {}
  raw = oracle().request("arms", arms=unique)["arms"]
  return {
    arm: ArmAnswer(
      arm=arm, accepted=one["accepted"], serialized=one.get("serialized"),
      origin=one.get("origin"), judged=one["judged"], dynamic=one["dynamic"],
      refusal=one["refusal"], reach=one["reach"],
    )
    for arm, one in raw.items()
  }


def reached_states(answer: ArmAnswer) -> dict:
  """The states in which the arm selects an element the layout owns."""
  return {state: where for state, where in answer.reach.items() if where}


def neutral_reach(answer: ArmAnswer) -> dict:
  """The witnesses for reaching chrome with the route's identity absent."""
  return {
    state: where for state, where in answer.reach.items()
    if where and state in NEUTRAL_STATES
  }


def reaches_site_chrome(answer: ArmAnswer) -> bool:
  """Can this arm match an element the published layout owns, in any state?"""
  return bool(answer.refusal) or bool(reached_states(answer))


def is_unsafe(answer: ArmAnswer) -> bool:
  """The verdict: refused, or able to reach chrome with no route identity present."""
  return bool(answer.refusal) or bool(neutral_reach(answer))


def scan_tree() -> dict[str, ArmAnswer]:
  """Ask the browser about every arm of every production stylesheet at once.

  One batched request for the whole tree: the browser session is started once
  for the module, and the production scan is one walk of the state matrix, not
  one per stylesheet.
  """
  arms: list[str] = []
  for sheet in [CORE_CSS] + instrument_stylesheets():
    arms.extend(selector_arms(sheet))
  return ask_arms(arms)


def site_chrome_selectors(path: Path, answers: dict | None = None) -> list[str]:
  """Selectors in one stylesheet that reach the layout's chrome unscoped.

  The browser decides, per arm and per shell state, whether the arm selects a
  chrome element; this function only extracts arms, asks, and reports the
  normalized identities of the unsafe ones in file order, duplicates kept,
  which is what makes the recorded exceptions exact. An arm Chromium refuses is
  reported, never dropped. `answers` may carry a result from `scan_tree` so a
  whole-tree audit is one batch rather than one per file.
  """
  arms = list(selector_arms(path))
  if answers is None:
    answers = ask_arms(arms)
  return [
    normalize_selector(arm) for arm in arms
    if is_unsafe(answers[arm])
  ]


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


@BROWSER_REQUIRED
class SiteChromeScopeTest(unittest.TestCase):
  """The fourth hazard: an instrument stylesheet restyling the site's own chrome.

  The shells the oracle judges are rendered by `wrap_in_layout` — the public
  and the preview one — with the page's own identity on `<main>` exactly where
  the build puts it. The page's subtree is not chrome; `<main>` itself is, and
  everything around it is.
  """

  def test_the_oracle_serves_the_shell_the_build_actually_emits(self):
    """If the masthead loses its class, or the model starts inside `<main>`,
    every other assertion in this class proves nothing."""
    answer = ask_arms([
      ".site-header", ".site-footer", ".skip-link", ".brand", "#main-content",
      ".release-banner", "a",
    ])
    for arm in (".site-header", ".site-footer", ".skip-link", ".brand", "#main-content"):
      with self.subTest(selector=arm):
        self.assertTrue(
          reaches_site_chrome(answer[arm]),
          f"{arm} was read as unable to reach any element the layout owns",
        )
    banners = {
      state for state, where in answer[".release-banner"].reach.items() if where
    }
    self.assertTrue(
      all(state.endswith("(preview)") for state in banners) and banners,
      f"the release banner must be chrome only in the preview shells, saw {sorted(banners)}",
    )
    # A bare `a` reaches the masthead, navigation and footer links; six is the
    # floor the layout's own furniture sets (brand, three nav, two footer).
    link_reach = reached_states(answer["a"])
    self.assertGreaterEqual(len(link_reach), len(NEUTRAL_STATES))
    for state in NEUTRAL_STATES:
      with self.subTest(state=state):
        self.assertIn(state, link_reach, "a bare `a` did not reach the chrome links")
    content_reach = ask_arms(["#chrome-model-content"])["#chrome-model-content"]
    self.assertFalse(
      reaches_site_chrome(content_reach),
      "the model reaches inside <main>, so page content would be judged as chrome",
    )

  def test_no_unrecorded_instrument_stylesheet_restyles_the_site_chrome(self):
    answers = scan_tree()
    for sheet in instrument_stylesheets():
      name = sheet.relative_to(BROWSER).as_posix()
      if name in SITE_CHROME_UNSCOPED:
        continue
      with self.subTest(stylesheet=name):
        found = site_chrome_selectors(sheet, answers)
        self.assertEqual(
          found, [],
          f"{name} reaches the published layout's own chrome with no route "
          f"scope: {found}. Pulled into a shared bundle the rule reaches every "
          "page on the site. Scope it by a class the layout does not own, or "
          "record it in SITE_CHROME_UNSCOPED with the authority that owns it",
        )

  def test_every_recorded_exception_is_the_exact_selector_inventory(self):
    """Not a count. A count can be substituted into and this cannot.

    Twelve selectors recorded as the number twelve is satisfied by any twelve
    selectors, so a protected rule could be replaced by a different unscoped rule
    at no cost. The inventory is the identities, in file order, duplicates kept.
    """
    answers = scan_tree()
    for name, exception in sorted(SITE_CHROME_UNSCOPED.items()):
      with self.subTest(stylesheet=name):
        sheet = BROWSER / name
        self.assertTrue(sheet.is_file(), f"{name} no longer exists; drop its entry")
        self.assertEqual(
          site_chrome_selectors(sheet, answers), list(exception.selectors),
          f"{name}'s unscoped site-chrome selectors are no longer the recorded "
          "inventory. If its protected owner scoped one, shorten the entry; if "
          "one was added or replaced, it widened a hazard the ledger holds open "
          "on someone else's behalf",
        )

  def test_every_recorded_exception_names_its_authority_and_its_reason(self):
    """An exception with no owner is a permission, which is not what this is."""
    for name, exception in sorted(SITE_CHROME_UNSCOPED.items()):
      with self.subTest(stylesheet=name):
        self.assertTrue(exception.authority.strip())
        self.assertTrue(exception.reason.strip())
        self.assertTrue(exception.selectors, "an empty inventory is not an exception")

  def test_the_recorded_exceptions_are_all_inside_the_protected_liturgy_family(self):
    """The corpus lane may correct its own files and only record the others.

    Every entry is under `liturgy/`. An entry appearing anywhere else would mean
    a corpus-owned stylesheet had been excused instead of fixed, which is the one
    way this record could be misused.
    """
    for name in sorted(SITE_CHROME_UNSCOPED):
      with self.subTest(stylesheet=name):
        self.assertTrue(
          name.startswith("liturgy/"),
          f"{name} is not in the protected Liturgy family, so it is this lane's "
          "to scope rather than to record",
        )

  def test_the_shared_stylesheet_is_the_one_place_the_chrome_is_owned(self):
    """browser-core.css is exempt because owning the shared furniture is its job."""
    self.assertTrue(
      site_chrome_selectors(CORE_CSS, scan_tree()),
      "shared/browser-core.css no longer styles the site chrome at all, which "
      "would mean the furniture moved and this test is measuring the wrong file",
    )

  def test_the_scripture_stylesheet_no_longer_reaches_the_layout_s_links(self):
    """The case the independent review named, held by name rather than by scan.

    `scripture.css` carried a bare `a` and `a:hover`, so on both published
    Scripture routes the masthead, navigation and footer links were coloured by
    the section's ink. They are scoped now, and the scope is written with
    `:where()` so the rules keep the specificity they had: the cascade is
    unchanged and only the set of matched elements is narrowed.
    """
    sheet = BROWSER / "scripture/scripture.css"
    self.assertEqual(site_chrome_selectors(sheet), [])
    arms = list(selector_arms(sheet))
    self.assertNotIn("a", arms)
    self.assertNotIn("a:hover", arms)
    for page_class in ("plan-page", "track-page"):
      with self.subTest(**{"class": page_class}):
        self.assertTrue(
          any(page_class in arm for arm in arms if arm.endswith(("a", "a:hover"))),
          f"the link rules no longer name .{page_class}, which is the class "
          "`browser_page_parts` puts on <main> for that route",
        )


@BROWSER_REQUIRED
class SelectorOracleSemanticsTest(unittest.TestCase):
  """What the oracle means by unsafe, stated as cases rather than as prose.

  Every arm in REACHED is one a real Chromium reported selecting a chrome
  element in the neutral shell — the state where the route's identity is
  absent from `<main>` — under the walk's bounded user-state matrix. Every arm
  in CLEAN is one the same browser reported selecting no chrome element
  anywhere in the matrix. Every arm in REFUSED_STATE_PAIRS is one the walk
  cannot establish either way and therefore refuses. None of the class names
  here are privileged: the oracle judges matching from DOM state, and the
  neutral shell is what makes a route-looking name inside a selector unable to
  buy scope by mere mention.
  """

  # The second cold review's counterexamples, verbatim, plus the shapes the
  # same review said the replacement must also classify.
  REACHED = (
    # Finding 1: negation and case-insensitive attributes.
    "a:not(:hover)",
    ".site-header:not(:focus-within)",
    "[class~=\"SITE-HEADER\" i]",
    # Finding 2: scope read off raw text.
    "a[href$=\".html\"]",
    "body:has(.plan-page, .site-header) .site-footer a",
    ":is(:not(.plan-page), .plan-page) a",
    # The negated class is the one case the rule EXCLUDES, never a scope.
    ".site-header:not(.route-only)",
    # Escaped identifiers, nested functional pseudos, every combinator class,
    # and the bare element forms. Top-level nesting (`& a`) is not valid
    # stylesheet syntax, but Chromium accepts it and matches the skip link with
    # it; the browser's answer is the truth, and it errs toward reporting.
    ".triptych\\-mark",
    "& a",
    "body:has(:is(.site-header)) .site-footer a",
    "body .site-footer a",
    "body > .site-header",
    "nav > a + a",
    "header ~ footer",
    "a",
    "a:hover",
    "a:focus-visible",
    "html",
    "body",
    ":root",
    "*",
    "*::before",
    "a::after",
    "[aria-label=\"Primary navigation\"]",
  )

  CLEAN = (
    # Legitimately route-dependent: reaching chrome genuinely depends on the
    # page state the class names, and the neutral shell has none of them.
    ".sources-page .page-footer a",
    "body:has(> .sources-page) .site-footer a",
    ".plan-page a",
    ".track-page a:hover",
    ".route-only .site-header",
    ":where(.plan-page, .track-page) a",
    "body:has(> .page-browser) > .site-header",
    "html:has(.reader-instrument)",
    ".catena-page .skip-link",
    "#main-content a",
    "button:focus-visible",
    "[hidden]",
    ".rail-link:hover",
    # Escapes that name a class nothing carries, and an attribute value whose
    # comma must not split the arm.
    ".triptych\\-nope",
    "[aria-label=\"Primary, navigation\"]",
  )

  # Two user states held at once, on two DIFFERENT chrome elements. The walk
  # holds one at a time — a press carries its own focus, which is why
  # `.site-header:hover a:focus` is reached by accident — so this shape is one
  # the walk cannot establish, and an independent rereview drove real Chromium
  # into the state (a real Tab, then a real pointer move) and saw both of these
  # match layout-owned elements while the walk reported no reach at all. They
  # are refused, and therefore unsafe, rather than reported safe.
  REFUSED_STATE_PAIRS = (
    "a:focus ~ .site-footer:hover",
    ".skip-link:focus ~ .site-footer:hover a",
  )

  # Every literal this class judges, asked of the browser in ONE batched
  # request in setUpClass, so the whole class costs one walk of the state
  # matrix rather than one per test.
  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.answers = ask_arms(
      list(cls.REACHED) + list(cls.CLEAN) + list(cls.REFUSED_STATE_PAIRS)
      + [
        "body:has(> .plan-page) .site-footer a",
        "body:has(.plan-page, .site-header) .site-footer a",
        "a:active",
        "#main-content:target",
        ".skip-link:focus",
        ".skip-link::before",
        "..dot", ":not()", 'a[href="unterminated', "%bad", "a:visited",
      ]
    )

  def test_every_cold_review_counterexample_reaches_chrome_in_a_neutral_shell(self):
    for arm in self.REACHED:
      with self.subTest(selector=arm):
        answer = self.answers[arm]
        witness = neutral_reach(answer)
        self.assertFalse(
          answer.refusal and not witness,
          f"{arm} was refused instead of decided: {answer.refusal}",
        )
        self.assertTrue(
          witness,
          f"{arm} was read as unable to reach any element the layout owns in "
          f"the neutral shell; the browser saw {answer.reach}",
        )

  def test_every_accepted_selector_is_clean_and_for_the_stated_reason(self):
    for arm in self.CLEAN:
      with self.subTest(selector=arm):
        answer = self.answers[arm]
        self.assertFalse(
          answer.refusal,
          f"{arm} is a form this repository writes and Chromium refused it: "
          f"{answer.refusal}",
        )
        self.assertEqual(
          neutral_reach(answer), {},
          f"{arm} reached site chrome with the route's identity absent: "
          f"{neutral_reach(answer)}",
        )

  def test_route_dependence_is_a_state_differential_and_not_a_name(self):
    """The same chrome element, reached or not, decided by the page state.

    `body:has(> .plan-page) .site-footer a` reaches the footer's links on the
    Scripture plan route — where the build projects `.plan-page` onto `<main>` —
    and reaches nothing in the neutral shell, where that identity is absent.
    That difference, observed rather than inferred, is what positive scope
    means here; `body:has(.plan-page, .site-header) …` fails it because its
    `.site-header` alternative is true everywhere.
    """
    differential = {
      "body:has(> .plan-page) .site-footer a":
        self.answers["body:has(> .plan-page) .site-footer a"],
      "body:has(.plan-page, .site-header) .site-footer a":
        self.answers["body:has(.plan-page, .site-header) .site-footer a"],
    }
    scoped = differential["body:has(> .plan-page) .site-footer a"]
    plan_states = sorted(
      state for state, where in scoped.reach.items()
      if where and "browser scripture/index.html" in state
    )
    self.assertTrue(plan_states, "the plan route was absent from the state matrix")
    self.assertEqual(
      neutral_reach(scoped), {},
      "a selector whose only true alternative is the route class reached the "
      "neutral shell",
    )
    tautology = differential["body:has(.plan-page, .site-header) .site-footer a"]
    for state in NEUTRAL_STATES:
      with self.subTest(state=state):
        self.assertTrue(
          tautology.reach.get(state),
          "the global alternative made this arm safe to fire in the neutral "
          "shell, and the walk did not see it",
        )

  def test_dynamic_states_are_walked_not_assumed(self):
    """A quiescent document would call every one of these safe. It is not.

    Each witness records the user sub-state that reached: `a:hover` is reached
    only with the pointer over a chrome link, `:focus-visible` only with
    keyboard focus on one, `:target` only with the fragment set, and
    `.skip-link:focus` under a held press as much as under focus. None of these
    matches in ordinary state — which is exactly why the walk exists, and why a
    quiescent-only oracle would have reported every one of them as safe.
    """
    for arm in ("a:hover", "a:focus-visible", ".skip-link:focus",
                "#main-content:target", "a:active"):
      with self.subTest(selector=arm):
        answer = self.answers[arm]
        witness = neutral_reach(answer)
        self.assertTrue(witness, f"{arm} reached nothing in the neutral shell")
        substates = {where["substate"] for where in witness.values()}
        self.assertNotIn(
          "quiescent", substates,
          f"{arm} matched in ordinary state, so no walk was needed; move it to "
          "the statically-reached cases",
        )

  def test_pseudo_element_arms_are_judged_by_the_element_they_belong_to(self):
    """`querySelectorAll('*::before')` matches NOTHING — the worst answer.

    So a pseudo-element arm is judged by the element the pseudo-element belongs
    to, which over-approximates in the safe direction: a rule that can draw on
    an element's `::before` reaches that element's rendering. The origin is
    recorded, and the independent sentinel observation below shows the style
    engine agreeing.
    """
    answers = {**self.answers, "a::after": ask_arms(["a::after"])["a::after"]}
    for arm, expected_origin in (
      ("*::before", "*"), ("a::after", "a"), (".skip-link::before", ".skip-link"),
    ):
      with self.subTest(selector=arm):
        answer = answers[arm]
        self.assertIsNone(answer.refusal)
        self.assertEqual(answer.origin, expected_origin)
        self.assertEqual(answer.judged, expected_origin)
        self.assertTrue(neutral_reach(answer), f"{arm} reached nothing")

  def test_what_the_browser_cannot_be_asked_is_reported_and_never_passed(self):
    """Fail closed. A selector Chromium rejects in the version that ships this
    gate is a selector nobody has shown to be safe, and `:visited` is one whose
    truth Chromium deliberately withholds from script."""
    for arm in ("..dot", ":not()", "a[href=\"unterminated", "%bad", "a:visited"):
      with self.subTest(selector=arm):
        answer = self.answers[arm]
        self.assertTrue(
          answer.refusal,
          f"{arm} was decided rather than refused; an unaskable selector must "
          "stop the gate, not pass it",
        )
        self.assertTrue(
          is_unsafe(answer),
          f"{arm} was refused and then treated as safe, which is fail-open",
        )

  def test_two_simultaneous_user_states_are_refused_rather_than_called_safe(self):
    """The walk holds one user state at a time, so this shape is undecided here.

    A reader who tabs to the skip link and then moves the pointer onto the
    footer is in a state the walk never visits, and an independent rereview
    drove real Chromium into exactly that state and watched
    `a:focus ~ .site-footer:hover` match `footer.site-footer` while this harness
    reported no reach at all. Reporting safe there is fail-open, so an arm whose
    serialization forces a user state in two distinct compounds is refused with
    the reason stated. One state in one compound is what the walk does
    establish, and `.track-page a:hover` still classifies as it did.
    """
    for arm in self.REFUSED_STATE_PAIRS:
      with self.subTest(selector=arm):
        answer = self.answers[arm]
        self.assertTrue(
          answer.refusal,
          f"{arm} was decided rather than refused, and the walk cannot hold two "
          "user states on two chrome elements at once, so deciding it is "
          "fail-open",
        )
        self.assertIn("one user state at a time", answer.refusal)
        self.assertTrue(
          is_unsafe(answer),
          f"{arm} was refused and then treated as safe, which is fail-open",
        )
    for arm, expected_reach in ((".track-page a:hover", False), ("a:hover", True)):
      with self.subTest(selector=arm):
        answer = self.answers[arm]
        self.assertIsNone(
          answer.refusal,
          f"{arm} forces one user state in one compound, which the walk does "
          f"establish, and it was refused: {answer.refusal}",
        )
        self.assertEqual(bool(neutral_reach(answer)), expected_reach)

  def test_the_states_the_walk_does_not_force_cannot_become_true(self):
    """The bound the harness measures is read here, so it can fail.

    `:disabled`, `:checked`, `:open` and the rest of the form and element states
    are outside the walk, and the reason they cannot become true for a chrome
    element is that the layout emits nothing that carries them. The harness
    measures that in every shell as it installs itself; asserting the
    measurement is what makes the layout gaining a `<button>`, a `<details>` or
    a `<dialog>` outside `<main>` fail the gate rather than quietly end the
    reasoning.
    """
    shells = oracle().shells
    self.assertEqual(
      sorted(shells), sorted(name for name, _ in oracle_states()),
      "the harness did not measure every shell whose selectors it judges",
    )
    for name, measured in sorted(shells.items()):
      with self.subTest(state=name):
        self.assertTrue(measured["descriptors"], "the shell reported no chrome")
        self.assertEqual(
          measured["interactive"], [],
          f"{name}'s chrome carries {measured['interactive']}, which can hold a "
          "form or element state the walk does not force, so the bound stated in "
          "the harness and in guidance/corpus-browser-implementation.md §11.4 "
          "has stopped holding",
        )

  def test_a_grouped_selector_is_judged_one_arm_at_a_time(self):
    """A safe arm beside an unsafe one must not carry it.

    The whole rule is written once and applies to both, so the unsafe arm
    reaches the chrome whatever the arm beside it says — and the splitter must
    not cut inside the quoted attribute value that contains the comma.
    """
    grouped = "a[title=\"a,b\"], .site-footer a"
    arms = [one.strip() for one in split_top_level(grouped)]
    self.assertEqual(arms, ['a[title="a,b"]', ".site-footer a"],
                     "the splitter cut inside the attribute value")
    answers = ask_arms(arms)
    self.assertEqual(neutral_reach(answers[arms[0]]), {})
    self.assertTrue(neutral_reach(answers[arms[1]]))
    self.assertEqual(
      [normalize_selector(a) for a in arms if is_unsafe(answers[a])],
      [".site-footer a"],
      "the rule's verdict is not the union of its arms' verdicts",
    )

  def test_the_oracle_agrees_with_an_independent_browser_observation(self):
    """Not helper return values: the style engine, read two other ways.

    For each arm, the walk's verdict is compared against (a) the elements a
    rule written with that selector reaches, read through a non-inherited
    property, and (b) `querySelectorAll` over the same document. For the
    pseudo-element arm, (a) is the only observation that can see the
    pseudo-element at all, which is why it is there.
    """
    arms = [
      "a:not(:hover)", ".site-header:not(:focus-within)",
      "[class~=\"SITE-HEADER\" i]", "a[href$=\".html\"]",
      "body:has(.plan-page, .site-header) .site-footer a",
      ":is(:not(.plan-page), .plan-page) a",
      "body:has(> .plan-page) .site-footer a",
      "*::before",
    ]
    oracle().request("arms", arms=arms)
    rows = oracle().request(
      "verify", arms=arms, states=[next(iter(sorted(NEUTRAL_STATES)))]
    )["verification"]
    resting = [row for row in rows if not row["forced"]]
    self.assertTrue(resting, "the independent check produced no resting rows")
    for row in resting:
      with self.subTest(arm=row["arm"], state=row["state"]):
        observed = bool(row["selectorApi"]) or bool(row["sentinel"]["element"]) or \
          any(row["sentinel"]["pseudo"].values())
        answer = ask_arms([row["arm"]])[row["arm"]]
        walked = bool(answer.reach.get(row["state"]))
        self.assertEqual(
          walked, observed,
          f"the walk said {'reach' if walked else 'clean'} and the independent "
          f"style-engine observation said "
          f"{'reach' if observed else 'clean'} (selectorApi="
          f"{row['selectorApi']}, sentinel={row['sentinel']})",
        )
    pseudo = [row for row in resting if row["arm"] == "*::before"]
    self.assertTrue(pseudo, "the pseudo-element arm was not verified")
    # The selector API answers for the ORIGIN (`*`), which does match chrome —
    # that is the over-approximation. The style engine is the observation that
    # can see the pseudo-element itself, and it must agree that the chrome's
    # `::before` boxes were reached.
    self.assertTrue(pseudo[0]["selectorApi"])
    self.assertTrue(
      pseudo[0]["sentinel"]["pseudo"].get("::before"),
      "the style engine drew nothing on the chrome's ::before, so judging the "
      "arm by its origin over-approximates is unproven",
    )

  def test_one_browser_session_answers_every_question(self):
    """The runtime is bounded by batching, and the numbers are measured facts.

    One Chromium session serves this whole module; the shells are navigated a
    bounded number of times, not once per selector; and a report is kept so a
    future maintainer can see the cost rather than guess it.
    """
    report = oracle().request("report")["report"]
    self.assertEqual(report["browserSessions"], 1)
    states = len(oracle_states())
    # Navigation count is driven by how many BATCHES carried new arms, never by
    # how many selectors were asked: that is the bounded-runtime contract.
    self.assertLessEqual(
      report["navigations"], states * (report["batches"] + 1),
      f"the oracle navigated {report['navigations']} times for "
      f"{report['batches']} batches over {states} states",
    )
    self.assertLess(
      report["batches"], report["arms"],
      "batches grew to one per selector, which is the launch-per-selector "
      "shape this harness exists to prevent",
    )
    self.assertGreater(report["arms"], 0)
    self.assertGreater(report["elapsedMs"], 0)
    self.assertTrue(report["forcedStates"], "the state matrix walked nothing")
    self.assertEqual(
      set(report["dynamicStatesWalked"]), set(DYNAMIC_WALK_STATES),
      "the user-state matrix was walked somewhere other than the states whose "
      "reach decides the verdict",
    )


@BROWSER_REQUIRED
class ProtectedInventoryMutationTest(unittest.TestCase):
  """That the recorded exception is a list of identities, driven over real files.

  Both mutations are built in a temporary stylesheet from the recorded
  inventory, so the protected file itself is never touched, and both are judged
  by the same browser verdict the production scan uses.
  """

  def mutations_of(self, selectors: list[str]) -> Path:
    temporary = tempfile.TemporaryDirectory()
    self.addCleanup(temporary.cleanup)
    sheet = Path(temporary.name) / "mutated.css"
    sheet.write_text(
      "\n".join(f"{one} {{ color: red; }}" for one in selectors), encoding="utf-8"
    )
    return sheet

  def test_a_substituted_protected_selector_fails_where_a_count_would_not(self):
    recorded = list(SITE_CHROME_UNSCOPED["liturgy/day-missal.css"].selectors)
    substituted = recorded[:-1] + [".site-footer a"]
    found = site_chrome_selectors(self.mutations_of(substituted))
    self.assertEqual(len(found), len(recorded), "the count is unchanged")
    self.assertNotEqual(found, recorded, "the inventory is what notices")

  def test_a_removed_protected_selector_is_noticed_too(self):
    """The exception may shrink, and shrinking must be recorded rather than assumed."""
    recorded = list(SITE_CHROME_UNSCOPED["liturgy/day-missal.css"].selectors)
    found = site_chrome_selectors(self.mutations_of(recorded[:-1]))
    self.assertNotEqual(found, recorded)

  def test_an_extractor_confusing_replacement_still_cannot_pass(self):
    """The inventory holds even when the substituted arm is harder to read.

    A selector with an escaped identifier and a comma inside an attribute value
    must survive extraction, reach chrome, and still fail the inventory.
    """
    recorded = list(SITE_CHROME_UNSCOPED["liturgy/reader-shell.css"].selectors)
    # The substituted arm carries commas inside a functional pseudo, which is
    # the shape a name-scanning extractor is weakest on; it must survive
    # extraction, reach chrome, and still fail the inventory.
    substituted = recorded[:-1] + [
      "body:has(.plan-page, .site-header) .site-footer a",
    ]
    found = site_chrome_selectors(self.mutations_of(substituted))
    self.assertEqual(len(found), len(recorded), "the count is unchanged")
    self.assertNotEqual(found, recorded, "the inventory is what notices")


class BrowserModelGateReachabilityTest(unittest.TestCase):
  """That the gate runs its own coverage assertion, held from outside that file.

  `test_browser_model_gate.py` asserts this too, and an assertion inside the file
  whose removal it guards against cannot catch its own removal. This suite is in
  `BROWSER_MODEL_TESTS`, so `make check` runs it; dropping the coverage
  prerequisite therefore fails a test that is not the one being dropped. The
  remaining bootstrap — removing both at once — is a visible two-place edit to
  `check:` and to the gate's own rule rather than a silent omission, and that
  limit is recorded in guidance/corpus-browser-implementation.md §11.3.
  """

  MAKEFILE = ROOT / "Makefile"
  COVERAGE_GATE = "check-browser-model-coverage"
  COVERAGE_MODULE = "test_browser_model_gate"

  def rule(self, target: str) -> str:
    text = self.MAKEFILE.read_text(encoding="utf-8")
    found = re.search(rf"^{re.escape(target)}: (.*?)(?<!\\)\n", text, re.M | re.S)
    self.assertIsNotNone(found, f"the Makefile no longer declares `{target}:`")
    assert found is not None
    return found.group(1)

  def test_check_reaches_the_browser_model_gate(self):
    self.assertIn("check-browser-models", self.rule("check").split())

  def test_the_browser_model_gate_requires_the_coverage_target(self):
    self.assertIn(
      self.COVERAGE_GATE, self.rule("check-browser-models").split(),
      "the browser-model gate no longer runs the assertion that keeps its own "
      "coverage honest, which is the state an independent cold review returned "
      "as CHANGES_REQUIRED",
    )

  def test_the_coverage_target_runs_the_coverage_module(self):
    text = self.MAKEFILE.read_text(encoding="utf-8")
    variable = re.search(
      r"^BROWSER_MODEL_GATE_TESTS := (.*?)(?<!\\)\n(?!\t)", text, re.M | re.S
    )
    self.assertIsNotNone(variable, "BROWSER_MODEL_GATE_TESTS is gone")
    assert variable is not None
    self.assertIn(self.COVERAGE_MODULE, variable.group(1))

  @unittest.skipIf(MAKE is None, "make is not installed; the topology cannot be replayed")
  def test_make_reports_that_check_will_run_the_coverage_module(self):
    result = subprocess.run(
      [MAKE or "make", "--no-print-directory", "-n", "check"],
      cwd=ROOT, capture_output=True, text=True,
    )
    self.assertEqual(result.returncode, 0, result.stderr.strip())
    self.assertRegex(
      result.stdout,
      re.compile(
        rf"for module in [^;]*\b{self.COVERAGE_MODULE}\b[^;]*;.*?unittest discover",
        re.S,
      ),
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
