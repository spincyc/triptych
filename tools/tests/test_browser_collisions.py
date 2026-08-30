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

   AN INDEPENDENT COLD REVIEW RETURNED THE FIRST VERSION OF THIS TEST AS
   INSUFFICIENT, and it was right. That version looked for a layout-owned CLASS
   in the selector text, so it saw `.site-header` and missed a bare `a` — which
   reaches every link in the masthead and footer — and `scripture.css` was
   carrying exactly that rule while the test passed. It also read any non-layout
   class ANYWHERE in the selector as page scope, so `.site-header:not(.route-only)`
   counted as scoped by the very class it excludes. And it froze the protected
   exception by the number twelve, so a recorded selector could be replaced by a
   different one at no cost.

   What replaces it does not read selector text for names. It builds the site's
   chrome from the layout the build actually emits — `wrap_in_layout` itself, in
   both its public and preview shells — and asks of every selector arm whether it
   can match one of those elements. Scope is a POSITIVE condition: a class or id
   the layout does not own, asserted rather than excluded, which is why
   `:not()` contents never count and `:is()`/`:where()` contents count only when
   every alternative in the list is itself scoped. What the bounded analyzer
   cannot classify it refuses rather than passes. SITE_CHROME_UNSCOPED records
   the protected remainder as an exact selector inventory with the authority that
   owns it, so neither a new hazard nor a substituted one can arrive unnoticed.

These tests are source-level. They read the files rather than a rendered page,
except where a model can be replayed under node, which the landmark test does,
and where the site's own chrome is read out of the build's layout renderer,
which the site-chrome tests do.
"""

from __future__ import annotations

import functools
import importlib.machinery
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).resolve().parents[2]
BROWSER = ROOT / "src/web/browser"
CORE_CSS = BROWSER / "shared/browser-core.css"
CORE_JS = BROWSER / "shared/browser-core.js"
ACT_HISTORY = ROOT / "src/web/data/structure/act-history"
LAYOUT = ROOT / "release/public-alpha/layout.html"
PUBLIC_ALPHA = ROOT / "tools/public-alpha"
NODE = shutil.which("node")
MAKE = shutil.which("make")


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
# The published chrome, and which selectors can reach it
#
# The site's chrome is not described here. It is rendered by the build's own
# `wrap_in_layout` and read off the result, so a masthead element the layout
# gains — or loses — is governed without anyone remembering to update a second
# handwritten copy of the layout. Both shells are read: the public one, and the
# preview one, which carries the release banner the public one does not.
# ===========================================================================

CHROME_MODEL_CONTENT = '<p id="chrome-model-content">content</p>'
# The page's own classes land on `<main>`, not on `<body>`, so the layout is
# rendered with an empty page class: `<main>`'s class attribute belongs to the
# page and must not be mistaken for something the layout owns.
CHROME_MODEL_PAGE_CLASS = ""
VOID_ELEMENTS = frozenset(
  "area base br col embed hr img input link meta param source track wbr".split()
)


class UnclassifiableSelector(Exception):
  """The bounded analyzer met a selector form it will not guess about.

  Raised rather than swallowed. A selector nobody can classify is not a selector
  anybody has shown to be safe, so it stops the gate instead of passing it.
  """


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
def chrome_documents() -> tuple[str, ...]:
  """The layout as the build emits it, public shell and preview shell."""
  module = public_alpha()
  return tuple(
    module.wrap_in_layout(
      "src/web/browser/scripture/index.html",
      "scripture/index.html",
      CHROME_MODEL_PAGE_CLASS,
      "Chrome model",
      "",
      CHROME_MODEL_CONTENT,
      preview,
      {},
    )
    for preview in (False, True)
  )


class ChromeElement:
  """One element the layout owns, with enough context to match a selector."""

  __slots__ = ("tag", "classes", "identifier", "attributes", "parent", "earlier_siblings")

  def __init__(self, tag: str, attributes: dict[str, str], parent) -> None:
    self.tag = tag
    self.attributes = attributes
    self.classes = frozenset(attributes.get("class", "").split())
    self.identifier = attributes.get("id")
    self.parent = parent
    self.earlier_siblings: tuple[ChromeElement, ...] = ()

  def __repr__(self) -> str:
    return f"<{self.tag} class={sorted(self.classes)} id={self.identifier}>"


class ChromeReader(HTMLParser):
  """Everything outside `<main>`'s content, which is everything the page is not.

  `<main>` itself is kept — it is the layout's landmark and an instrument rule
  that restyles it restyles it on every route the file reaches — while its
  subtree is skipped, because that subtree is the page's own content and styling
  it is what an instrument stylesheet is for.
  """

  def __init__(self) -> None:
    super().__init__(convert_charrefs=True)
    self.elements: list[ChromeElement] = []
    self.open: list[ChromeElement] = []
    self.children: dict[int, list[ChromeElement]] = {}
    self.inside_main = 0

  def handle_starttag(self, tag, attrs):
    if self.inside_main:
      if tag not in VOID_ELEMENTS:
        self.inside_main += 1
      return
    attributes = {name: (value or "") for name, value in attrs}
    parent = self.open[-1] if self.open else None
    element = ChromeElement(tag, attributes, parent)
    siblings = self.children.setdefault(id(parent), [])
    element.earlier_siblings = tuple(siblings)
    siblings.append(element)
    self.elements.append(element)
    if tag == "main":
      self.inside_main = 1
      return
    if tag not in VOID_ELEMENTS:
      self.open.append(element)

  def handle_endtag(self, tag):
    if self.inside_main:
      self.inside_main -= 1
      return
    while self.open:
      if self.open.pop().tag == tag:
        break


@functools.lru_cache(maxsize=None)
def chrome_elements() -> tuple[ChromeElement, ...]:
  found: list[ChromeElement] = []
  for document in chrome_documents():
    reader = ChromeReader()
    reader.feed(document)
    reader.close()
    found.extend(reader.elements)
  return tuple(found)


@functools.lru_cache(maxsize=None)
def layout_owned_classes() -> frozenset[str]:
  """Classes the published layout puts on the chrome around `<main>`."""
  found: set[str] = set()
  for element in chrome_elements():
    found |= element.classes
  return frozenset(found)


@functools.lru_cache(maxsize=None)
def layout_owned_ids() -> frozenset[str]:
  return frozenset(
    element.identifier for element in chrome_elements() if element.identifier
  )


# ---- reading a selector far enough to answer one question about it ----

IDENTIFIER = r"[-_A-Za-z0-9\\]+"
COMBINATORS = frozenset(">+~")


def split_top_level(text: str, separator: str = ",") -> list[str]:
  """Split on a separator that is not inside brackets or quotes."""
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
        raise UnclassifiableSelector(f"unbalanced brackets in {text!r}")
    if character == separator and depth == 0:
      parts.append("".join(current))
      current = []
      continue
    current.append(character)
  if depth or quote:
    raise UnclassifiableSelector(f"unbalanced brackets or quotes in {text!r}")
  parts.append("".join(current))
  return parts


@functools.lru_cache(maxsize=None)
def split_compounds(arm: str) -> tuple[tuple[str, str], ...]:
  """One complex selector as (combinator, compound) pairs, left to right.

  The combinator is the one that precedes its compound: `''` for the first,
  `' '` for a descendant, and `>`/`+`/`~` for the rest.
  """
  found: list[tuple[str, str]] = []
  current: list[str] = []
  pending = ""
  depth = 0
  quote = ""
  after_space = False
  for character in arm:
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
      current.append(character)
      continue
    if character in ")]":
      depth -= 1
      if depth < 0:
        raise UnclassifiableSelector(f"unbalanced brackets in {arm!r}")
      current.append(character)
      continue
    if depth:
      current.append(character)
      continue
    if character.isspace():
      after_space = bool(current)
      continue
    if character in COMBINATORS:
      if current:
        found.append((pending, "".join(current)))
        current = []
      pending = character
      after_space = False
      continue
    if after_space and current:
      found.append((pending, "".join(current)))
      current = []
      pending = " "
      after_space = False
    current.append(character)
  if depth or quote:
    raise UnclassifiableSelector(f"unbalanced brackets or quotes in {arm!r}")
  if current:
    found.append((pending, "".join(current)))
  return tuple(found)


class Pseudo(NamedTuple):
  name: str
  argument: str


class Compound(NamedTuple):
  tag: str
  classes: frozenset[str]
  identifiers: frozenset[str]
  attributes: tuple[str, ...]
  pseudos: tuple[Pseudo, ...]


@functools.lru_cache(maxsize=None)
def parse_compound(text: str) -> Compound:
  if "&" in text:
    raise UnclassifiableSelector(f"CSS nesting is not classified: {text!r}")
  tag = ""
  classes: set[str] = set()
  identifiers: set[str] = set()
  attributes: list[str] = []
  pseudos: list[Pseudo] = []
  index = 0
  while index < len(text):
    character = text[index]
    if character == "*":
      tag = tag or "*"
      index += 1
      continue
    if character in ".#":
      match = re.match(rf"[.#]({IDENTIFIER})", text[index:])
      if match is None:
        raise UnclassifiableSelector(f"unreadable name in {text!r}")
      (classes if character == "." else identifiers).add(match.group(1))
      index += match.end()
      continue
    if character == "[":
      end = text.find("]", index)
      if end == -1:
        raise UnclassifiableSelector(f"unreadable attribute in {text!r}")
      attributes.append(text[index + 1:end])
      index = end + 1
      continue
    if character == ":":
      match = re.match(r"(::?)([A-Za-z-]+)", text[index:])
      if match is None:
        raise UnclassifiableSelector(f"unreadable pseudo in {text!r}")
      name = match.group(2).lower()
      index += match.end()
      argument = ""
      if index < len(text) and text[index] == "(":
        depth = 0
        start = index
        while index < len(text):
          if text[index] == "(":
            depth += 1
          elif text[index] == ")":
            depth -= 1
            if depth == 0:
              index += 1
              break
          index += 1
        if depth:
          raise UnclassifiableSelector(f"unbalanced pseudo argument in {text!r}")
        argument = text[start + 1:index - 1]
      pseudos.append(Pseudo(name, argument))
      continue
    match = re.match(r"[A-Za-z][A-Za-z0-9-]*", text[index:])
    if match is not None and index == 0:
      tag = match.group(0).lower()
      index += match.end()
      continue
    raise UnclassifiableSelector(
      f"unreadable fragment {text[index:]!r} in compound {text!r}"
    )
  return Compound(
    tag, frozenset(classes), frozenset(identifiers), tuple(attributes), tuple(pseudos)
  )


ATTRIBUTE_CONDITION = re.compile(
  rf"""^\s*(?P<name>{IDENTIFIER})\s*
       (?:(?P<operator>[~^$*|]?=)\s*(?P<value>"[^"]*"|'[^']*'|[^\s\]]+))?\s*
       (?:[iIsS]\s*)?$""",
  re.X,
)


def attribute_matches(condition: str, element: ChromeElement) -> bool:
  match = ATTRIBUTE_CONDITION.match(condition)
  if match is None:
    raise UnclassifiableSelector(f"unreadable attribute condition [{condition}]")
  name = match.group("name").lower()
  if name not in element.attributes:
    return False
  if not match.group("operator"):
    return True
  actual = element.attributes[name]
  value = match.group("value").strip("\"'")
  operator = match.group("operator")
  if operator == "=":
    return actual == value
  if operator == "~=":
    return value in actual.split()
  if operator == "^=":
    return actual.startswith(value)
  if operator == "$=":
    return actual.endswith(value)
  if operator == "*=":
    return value in actual
  if operator == "|=":
    return actual == value or actual.startswith(f"{value}-")
  raise UnclassifiableSelector(f"unreadable attribute operator {operator!r}")


def compound_matches(compound: Compound, element: ChromeElement) -> bool:
  """Can this compound select this chrome element?

  Fails closed. `:not()` is evaluated, because a negation is the one pseudo-class
  that can make a selector match FEWER elements and a rule written
  `.site-header:not(.route-only)` must not be read as scoped by the class it
  excludes. `:root` is evaluated because it names one element exactly. Every
  other pseudo-class and every pseudo-element is a state, a position, or a
  relation this analyzer does not evaluate, and is treated as satisfiable: the
  element it qualifies is one the rule can reach.
  """
  if compound.tag and compound.tag != "*" and compound.tag != element.tag:
    return False
  if not compound.classes <= element.classes:
    return False
  if any(name != element.identifier for name in compound.identifiers):
    return False
  if not all(attribute_matches(one, element) for one in compound.attributes):
    return False
  for pseudo in compound.pseudos:
    if pseudo.name == "not":
      for alternative in split_top_level(pseudo.argument):
        alternative = alternative.strip()
        if alternative and selects(alternative, element):
          return False
    elif pseudo.name == "root" and element.tag != "html":
      return False
  return True


def selects(arm: str, element: ChromeElement) -> bool:
  """Does this complex selector match `element` as its subject?"""
  compounds = split_compounds(arm)
  if not compounds:
    return False
  return _selects(compounds, len(compounds) - 1, element)


def _selects(
  compounds: tuple[tuple[str, str], ...], index: int, element: ChromeElement
) -> bool:
  combinator, text = compounds[index]
  if not compound_matches(parse_compound(text), element):
    return False
  if index == 0:
    return True
  if combinator in ("", " "):
    ancestor = element.parent
    while ancestor is not None:
      if _selects(compounds, index - 1, ancestor):
        return True
      ancestor = ancestor.parent
    return False
  if combinator == ">":
    return element.parent is not None and _selects(compounds, index - 1, element.parent)
  if combinator == "+":
    return bool(element.earlier_siblings) and _selects(
      compounds, index - 1, element.earlier_siblings[-1]
    )
  if combinator == "~":
    return any(
      _selects(compounds, index - 1, sibling) for sibling in element.earlier_siblings
    )
  raise UnclassifiableSelector(f"unreadable combinator {combinator!r}")


def reaches_site_chrome(arm: str) -> bool:
  return any(selects(arm, element) for element in chrome_elements())


def _group_after(text: str, opening: int) -> int:
  """The index just past the parenthesis group that starts at `opening`."""
  depth = 0
  index = opening
  while index < len(text):
    if text[index] == "(":
      depth += 1
    elif text[index] == ")":
      depth -= 1
      if depth == 0:
        return index + 1
    index += 1
  raise UnclassifiableSelector(f"unbalanced parenthesis in {text!r}")


def without_negations(arm: str) -> str:
  """Every `:not()` group removed, so nothing inside one can grant scope."""
  text = arm
  while True:
    match = re.search(r":not\(", text, re.I)
    if match is None:
      return text
    end = _group_after(text, match.end() - 1)
    text = f"{text[:match.start()]} {text[end:]}"


def _names(text: str) -> set[str]:
  return set(re.findall(rf"[.#]({IDENTIFIER})", text))


def route_scope(arm: str) -> set[str]:
  """The class and id names in this arm that positively scope it to a route.

  A name counts only when the layout does not own it and the selector ASSERTS it.
  A name inside `:not()` is excluded by the rule rather than required by it, so it
  broadens the match and never counts. A name inside `:is()` or `:where()` counts
  only when every alternative in that list is itself scoped, because one global
  alternative — `:is(.plan-page, .site-header)` — makes the whole list global.
  `:has()` is the opposite case and does count: `body:has(> .sources-page)` is a
  positive statement about which document the rule applies in, and it is how this
  repository already writes route scope where the class sits on `<main>`.
  """
  owned = layout_owned_classes() | layout_owned_ids()
  text = without_negations(arm)
  scope: set[str] = set()
  for functional in ("is", "where"):
    while True:
      match = re.search(rf":{functional}\(", text, re.I)
      if match is None:
        break
      end = _group_after(text, match.end() - 1)
      argument = text[match.end():end - 1]
      alternatives = [one.strip() for one in split_top_level(argument) if one.strip()]
      scoped = [_names(without_negations(one)) - owned for one in alternatives]
      if scoped and all(scoped):
        scope |= set().union(*scoped)
      text = f"{text[:match.start()]} {text[end:]}"
  return scope | (_names(text) - owned)


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


def site_chrome_selectors(path: Path) -> list[str]:
  """Selectors in one stylesheet that reach the layout's chrome unscoped.

  A selector is reported when it can match an element the published layout owns
  and nothing in it positively narrows the match to a route or an instrument. A
  grouped selector is judged arm by arm, so one safe arm cannot carry an unsafe
  one. The result is normalized selector identities in file order, duplicates
  kept, which is what makes the recorded exceptions exact.
  """
  return [
    normalize_selector(arm)
    for arm in selector_arms(path)
    if not route_scope(arm) and reaches_site_chrome(arm)
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
    self.assertIn("main-content", layout_owned_ids())

  def test_the_chrome_model_is_the_layout_the_build_actually_emits(self):
    """Read off `wrap_in_layout`, not off a second copy of the layout.

    The elements that matter are the ones no page owns: the masthead and its
    navigation, the brand, the release banner the preview shell adds, the footer
    and its links. The page's own content is deliberately not in the model — an
    instrument stylesheet styling that is an instrument stylesheet working.
    """
    tags = {element.tag for element in chrome_elements()}
    for expected in ("html", "body", "header", "nav", "footer", "a", "main", "aside"):
      with self.subTest(tag=expected):
        self.assertIn(expected, tags)
    self.assertNotIn(
      "chrome-model-content",
      {element.identifier for element in chrome_elements()},
      "the model reaches inside <main>, so page content would be judged as chrome",
    )
    links = [element for element in chrome_elements() if element.tag == "a"]
    self.assertGreaterEqual(
      len(links), 6,
      "the layout's masthead and footer links are what a bare `a` rule reaches",
    )

  def test_no_unrecorded_instrument_stylesheet_restyles_the_site_chrome(self):
    for sheet in instrument_stylesheets():
      name = sheet.relative_to(BROWSER).as_posix()
      if name in SITE_CHROME_UNSCOPED:
        continue
      with self.subTest(stylesheet=name):
        found = site_chrome_selectors(sheet)
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
    for name, exception in sorted(SITE_CHROME_UNSCOPED.items()):
      with self.subTest(stylesheet=name):
        sheet = BROWSER / name
        self.assertTrue(sheet.is_file(), f"{name} no longer exists; drop its entry")
        self.assertEqual(
          site_chrome_selectors(sheet), list(exception.selectors),
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
      site_chrome_selectors(CORE_CSS),
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


class SiteChromeSelectorSemanticsTest(unittest.TestCase):
  """What the detector means by unsafe, stated as cases rather than as prose.

  Every rejected case below is a selector that can match an element the published
  layout owns with nothing narrowing it to a route. Every accepted case is one
  that either cannot match the chrome or positively says which route it is about.
  None of the class names here are privileged by the implementation: scope is any
  name the layout does not own, read off the layout.
  """

  REJECTED = (
    ".site-header",
    "body > .site-header",
    "a",
    "a:hover",
    ".site-header:not(.route-only)",
    "body .site-footer a",
    ".site-footer:not(.route-only) a",
    "body:not(.route-only) > .site-header nav a",
    ".brand a",
    ".skip-link",
    "html",
    "body",
    ":root",
    "*",
    "nav a",
    "footer p",
    "a:focus-visible",
    ".release-banner strong",
    ":is(.plan-page, .site-header) a",
  )

  ACCEPTED = (
    ".sources-page .page-footer a",
    "body:has(> .sources-page) .site-footer a",
    ".plan-page a",
    ".track-page a:hover",
    ".route-only .site-header",
    ":where(.plan-page, .track-page) a",
    "body:has(.reader-instrument) > .site-header",
    "html:has(.reader-instrument)",
    ".catena-page .skip-link",
    "#main-content a",
    "button:focus-visible",
    "[hidden]",
    ".rail-link:hover",
  )

  def test_every_rejected_selector_is_reported_as_reaching_the_chrome(self):
    for arm in self.REJECTED:
      with self.subTest(selector=arm):
        self.assertFalse(
          route_scope(arm),
          f"{arm} was read as route-scoped, and nothing in it positively names "
          "a route",
        )
        self.assertTrue(
          reaches_site_chrome(arm),
          f"{arm} was read as unable to reach any element the layout owns",
        )

  def test_every_accepted_selector_is_allowed_and_for_the_stated_reason(self):
    for arm in self.ACCEPTED:
      with self.subTest(selector=arm):
        self.assertTrue(
          route_scope(arm) or not reaches_site_chrome(arm),
          f"{arm} is a form this repository uses legitimately and was reported",
        )

  def test_a_negative_condition_is_not_a_positive_scope(self):
    """`.site-header:not(.route-only)` is a rule about every masthead but one.

    Reading `.route-only` there as page scope is the defect an independent review
    found: the class is the one case the rule EXCLUDES.
    """
    self.assertEqual(route_scope(".site-header:not(.route-only)"), set())
    self.assertEqual(route_scope(".site-footer:not(.route-only) a"), set())
    self.assertEqual(route_scope("body:not(.route-only) > .site-header"), set())
    self.assertEqual(route_scope(":not(.route-only) .site-header"), set())
    # The same class asserted rather than excluded does scope the rule.
    self.assertEqual(route_scope(".route-only .site-header"), {"route-only"})

  def test_a_grouped_selector_is_judged_one_arm_at_a_time(self):
    """A safe arm beside an unsafe one must not carry it.

    The whole rule is written once and applies to both, so the unsafe arm reaches
    the chrome whatever the arm beside it says.
    """
    grouped = ".plan-page a,\na:hover"
    arms = [one.strip() for one in split_top_level(grouped)]
    self.assertEqual(arms, [".plan-page a", "a:hover"])
    self.assertTrue(route_scope(arms[0]))
    self.assertFalse(route_scope(arms[1]))
    self.assertTrue(reaches_site_chrome(arms[1]))

  def test_has_is_a_positive_relation_and_is_and_where_are_only_conditionally(self):
    """The three functional pseudo-classes, treated deliberately.

    `:has()` states which document the rule applies in and is how this repository
    already writes route scope where the page class sits on `<main>`. `:is()` and
    `:where()` are lists: they scope only when every alternative does, because one
    global alternative makes the whole list global.
    """
    self.assertEqual(
      route_scope("body:has(> .sources-page) .site-footer a"), {"sources-page"}
    )
    self.assertEqual(
      route_scope(":where(.plan-page, .track-page) a"), {"plan-page", "track-page"}
    )
    self.assertEqual(route_scope(":is(.plan-page, .track-page) a"),
                     {"plan-page", "track-page"})
    self.assertEqual(route_scope(":is(.plan-page, .site-header) a"), set())
    self.assertEqual(route_scope(":where(.site-header, .site-footer) a"), set())
    # A negation nested inside a positive relation still grants nothing.
    self.assertEqual(route_scope("body:has(:not(.plan-page)) .site-footer a"), set())

  def test_the_analyzer_refuses_what_it_cannot_classify(self):
    """Fail closed. A selector nobody can read is not a selector shown to be safe."""
    for unreadable in ("& a", ".site-header:not(.route-only", "a[href", "%bad"):
      with self.subTest(selector=unreadable):
        with self.assertRaises(UnclassifiableSelector):
          route_scope(unreadable)
          reaches_site_chrome(unreadable)

  def test_a_substituted_protected_selector_fails_where_a_count_would_not(self):
    """Why the recorded exception is a list of identities and not the number 12.

    Driven over a temporary stylesheet built from the recorded inventory with one
    selector swapped for a different unscoped one, so the protected file itself is
    not touched: the count is still satisfied, and the inventory is not.
    """
    recorded = list(SITE_CHROME_UNSCOPED["liturgy/day-missal.css"].selectors)
    substituted = recorded[:-1] + [".site-footer a"]
    with tempfile.TemporaryDirectory() as temporary:
      sheet = Path(temporary) / "substituted.css"
      sheet.write_text(
        "\n".join(f"{one} {{ color: red; }}" for one in substituted), encoding="utf-8"
      )
      found = site_chrome_selectors(sheet)
      self.assertEqual(len(found), len(recorded), "the count is unchanged")
      self.assertNotEqual(found, recorded, "the inventory is what notices")

  def test_a_removed_protected_selector_is_noticed_too(self):
    """The exception may shrink, and shrinking must be recorded rather than assumed."""
    recorded = list(SITE_CHROME_UNSCOPED["liturgy/day-missal.css"].selectors)
    with tempfile.TemporaryDirectory() as temporary:
      sheet = Path(temporary) / "shortened.css"
      sheet.write_text(
        "\n".join(f"{one} {{ color: red; }}" for one in recorded[:-1]), encoding="utf-8"
      )
      self.assertNotEqual(site_chrome_selectors(sheet), recorded)

  def test_the_whole_production_tree_is_scanned_and_classified(self):
    """No stylesheet may be silently unreadable, exempt or not.

    Every production browser stylesheet, `browser-core.css` and the recorded
    exceptions included, is put through the analyzer here. A file that raises is
    a file nobody has classified, and the gate above would have skipped it.
    """
    sheets = [CORE_CSS] + instrument_stylesheets()
    self.assertGreaterEqual(len(sheets), 14, "the browser tree lost stylesheets")
    for sheet in sheets:
      with self.subTest(stylesheet=sheet.relative_to(BROWSER).as_posix()):
        site_chrome_selectors(sheet)


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
