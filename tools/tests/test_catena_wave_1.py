#!/usr/bin/env python3
"""The Catena Omnia page after the Wave 1 (E0) composition and its E1 corrections.

The composition is a stylesheet-led change over classes the page already
emitted, plus bounded operations in `catena.js` and one static disclosure in
`index.html`. The independent review of the first E1 candidate (roadmap,
2026-08-10) required corrections, and each route-owned one is pinned here by
its own test class:

  Finding 2   ChronologyTest — grouping by author alone filed Augustine's 417
              work under a heading dated 401, ahead of Severian's 401; only a
              contiguous author+date run may share a heading.
  Finding 3   LeadsCopyTest — the acquisition list overlaps held works in the
              generated data, so the page may not claim "not yet acquired" or
              "no text of any of them is held"; the copy asserts no more than
              the record proves.
  Finding 4   RightsRenderingTest — every rights/printing/attribution fact the
              payload supplies is rendered (edition_published carries the
              Voicu/BBAW attribution today), an acknowledgement renders ABOVE
              the prose, rights_basis only without an acknowledgement, and a
              bare `rights: "licensed"` prints truthfully and no more.
  Finding 5   HashValidationTest, VoiceDeepLinkTest, HistoryDeterminismTest —
              typed validation of all four hash keys on cold load and
              hashchange (whole-key voice soundness, chapter ranged against
              the book the page would resolve), failing closed with the URL
              left as written and recovery offered; the deferred-voice deep
              link; deterministic Back/Forward through a route-owned
              hashchange comparison, with arrival normalisation that never
              pushes a history entry.
  Finding 6   StaticDocumentTruthTest, PrintStylesTest, CompositionTest — the
              static document is true without scripts (no permanent Loading,
              no static aria-busy, a real browse entry), narrow enhancement is
              synchronous, and print hides interaction chrome while naming
              itself non-canonical.
  Finding 7   ForcedColorsTest — the reserved paragraph edge forces to Canvas
              and only `.projected` takes CanvasText.
  Finding 8   VoiceCountTruthTest, AbsenceCountTest, ParagraphCountTest,
              AuthorFilterRecoveryTest, IntegrityErrorTest — counts and states
              derive from the typed record, never from a filtered count; an
              expected spine 404 is an error, not an absence; a filter can
              never strand the reader.

The replay proves behaviour by RUNNING THE PAGE under node — the real
`browser-core.js`, the real `catena-model.js`, the real `catena.js`, against
the repository's own corpus with a stub document and network — rather than by
matching strings in the source. Assertions that only read source text are the
fallback for what a replay cannot reach (static markup, stylesheet blocks).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BROWSER = ROOT / "src/web/browser"
CATENA = BROWSER / "catena"
NODE = shutil.which("node")

# `catena-model.js`, byte for byte. The model is UMD and DOM-free, is replayed
# under node by `scripts/_catena.py check`, and no part of E1 touches it: a
# deliberate model change is a deliberate change to this literal. The digest
# is of the tracked file itself — release bindings are the release owner's.
MODEL_SHA256 = "f1ea94f9ec6b54813859c2b526163e90d9de61992b839fe2eb0e349f31ccf57b"

# gzip -9, whole file, mtime pinned to zero. These are the recorded E1
# ceilings — the first candidate raised them to 8,600/13,400 without a waiver
# and the review declined that; the corrected composition fits the originals.
CSS_BUDGET_GZ = 8_000
JS_BUDGET_GZ = 13_000
# The same files with comments stripped: what the composition itself costs.
# Base at main 9b9ff74a7: css 1,813 / js 6,450. The growth is the accepted
# composition plus the correction work this file pins (typed hash validation
# for all four keys, integrity errors, rights facts, chronology grouping,
# filter recovery, route-owned history with arrival replaceState, print and
# forced-colors blocks).
CSS_RULES_BUDGET_GZ = 2_700
JS_CODE_BUDGET_GZ = 8_800

# The review's protected distinctions. The composition deliberately specifies
# no treatment for the `.absence-*` selectors (they render in the page's
# inherited sans and ink — undeclared is the state to protect), and the rest
# keep the section's own palette so they read APART from held commentary.
PROTECTED_SELECTORS = (
    ".absence-note",
    ".absence-list",
    ".absence-reason",
    ".absence-partial",
    ".paragraph-note",
    ".passage-paragraph.projected",
    ".aside-note",
    ".fragment-basis",
    ".spans",
)

PROTECTED_AND_DECLARED = (
    ".paragraph-note",
    ".passage-paragraph.projected",
    ".aside-note",
    ".fragment-basis",
    ".spans",
)


def held(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def without_comments(text: str, *, script: bool = False) -> str:
    stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    if script:
        stripped = re.sub(r"^\s*//.*$", "", stripped, flags=re.M)
    return stripped


def gz(text: str) -> int:
    return len(gzip.compress(text.encode("utf-8"), 9, mtime=0))


def declarations_for(css: str, selector: str) -> list[str]:
    """Every declaration block whose selector list names this exact selector."""
    found: list[str] = []
    for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", without_comments(css)):
        names = [one.strip() for one in block.group(1).split(",")]
        if any(name == selector or name.endswith(" " + selector) for name in names):
            found.append(block.group(2))
    return found


def media_block(css: str, prelude: str) -> str:
    """The body of one `@media` block, brace-balanced."""
    start = css.index(prelude)
    open_at = css.index("{", start)
    depth = 0
    for at in range(open_at, len(css)):
        if css[at] == "{":
            depth += 1
        elif css[at] == "}":
            depth -= 1
            if depth == 0:
                return css[open_at + 1:at]
    raise AssertionError(f"unbalanced media block at {prelude!r}")


# --------------------------------------------------------------------- replay

# A chapter file carrying a `blocked` entry. EXPLICITLY SYNTHETIC: every
# tracked chapter file carries an empty `blocked` array, so the renderer has
# never fired on real data. It is tested anyway — defensively — because the
# distinction between "never acquired" and "held, and not renderable" is one
# the review protected; the real fixture is the generator's to supply, and
# this one is never served.
BLOCKED_FIXTURE = {
    "book": "Gen",
    "chapter": 1,
    "fragments": [],
    "sources": {},
    "leads": [{"author": "Origen", "title": "Homiliae in Genesim", "date": 240}],
    "blocked": [
        {
            "author": "Anonymous",
            "work": "Catena in Genesim",
            "reason": "the witness is held only as page images, and no text has been read off them",
        }
    ],
    "refusals": {},
}

# EXPLICITLY SYNTHETIC licence fixture. The corpus today reduces the Severian
# CC BY-SA terms to `rights: "licensed"` — projecting the full metadata is a
# recorded generator prerequisite — so the renderer's acknowledgement /
# attribution / rights_basis handling can only be proved against a labelled
# fixture. Nothing here asserts the corpus already carries these fields.
LICENCE_FIXTURE = {
    "book": "Gen",
    "chapter": 1,
    "text_prefix": "structure/catena/text/",
    "sources": {
        "0": {
            "author": "Synthetic Author",
            "work": "Synthetic Work",
            "work_id": "work.synthetic",
            "date": 401,
            "language": "grc",
            "voice": "original",
            "rights": "CC BY-SA 4.0",
            "edition": "Synthetic Edition",
            "edition_published": "Synthetic Press, 2018",
            "translators": [],
            "container": "",
            "acknowledgement": "Greek text by A. Editor, CC BY-SA 4.0; share alike.",
            "attribution": "Attribution: A. Editor, Synthetic Academy",
            "rights_basis": "suppressed because an acknowledgement states the terms",
        },
        "1": {
            "author": "Second Author",
            "work": "Second Work",
            "work_id": "work.second",
            "date": 500,
            "language": "la",
            "voice": "original",
            "rights": "licensed",
            "edition": "Second Edition",
            "edition_published": "",
            "translators": [],
            "container": "",
            "rights_basis": "printed because no acknowledgement is recorded",
        },
    },
    "fragments": [
        {
            "id": "synthetic-ack",
            "locator": "1",
            "source": "0",
            "review": "inspected",
            "text_words": 4,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 1,
                       "last_chapter": 1, "last_verse": 1},
        },
        {
            "id": "synthetic-late",
            "locator": "2",
            "source": "1",
            "review": "inspected",
            "text_words": 2,
            "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 2,
                       "last_chapter": 1, "last_verse": 2},
        },
    ],
    "leads": [],
    "blocked": [],
    "refusals": {},
}

GEN1 = "#book=Gen&chapter=1&bible=douay-rheims"
GEN2 = "#book=Gen&chapter=2&bible=douay-rheims"
GEN42 = "#book=Gen&chapter=42&bible=douay-rheims"

SCENARIOS = [
    {"name": "default", "hash": GEN1,
     "steps": [{"do": "openFirstFragment", "label": "opened"}]},
    {"name": "voice-held", "hash": GEN1 + "&voice=translation:en"},
    {"name": "voice-not-held", "hash": GEN1 + "&voice=translation:de"},
    # Genesis 10 holds 71 fragments, every one in its author's own Latin: the
    # selected-empty-voice chapter finding 8 demands be told truthfully.
    {"name": "voice-empty-chapter",
     "hash": "#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en"},
    {"name": "numbering-refusal", "hash": "#book=Ps&chapter=13&bible=king-james-version"},
    {"name": "acquisition-only", "hash": "#book=Ex&chapter=3&bible=douay-rheims"},
    # Exodus 1 is absent from the index's `present` list: no spine is asked for.
    {"name": "nothing-held", "hash": "#book=Ex&chapter=1&bible=douay-rheims"},
    {"name": "narrow", "hash": GEN1, "narrow": True},
    # The corpus's only single-commentator chapter.
    {"name": "one-commentator", "hash": GEN42},
    {"name": "held-unrenderable", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": BLOCKED_FIXTURE}},
    # The real licensed source: six Severian/PTA fragments under rights
    # "licensed", their attribution carried today in edition_published.
    {"name": "severian-open", "hash": GEN1,
     "steps": [{"do": "openFragmentOf", "author": "Severian of Gabala", "label": "opened"}]},
    {"name": "synthetic-licence", "hash": GEN1,
     "files": {
         "structure/catena/01-gen/001.json": LICENCE_FIXTURE,
         "structure/catena/text/synthetic-ack.json":
             {"id": "synthetic-ack", "text": "Synthetic words one."},
         "structure/catena/text/synthetic-late.json":
             {"id": "synthetic-late", "text": "Late words.",
              "acknowledgement": "Text-file licence note, CC BY-SA 4.0."},
     },
     "steps": [
         {"do": "openFragmentOf", "author": "Synthetic Author", "label": "first-open"},
         {"do": "openFragmentOf", "author": "Second Author", "label": "second-open"},
     ]},
    # An expected spine that 404s: an integrity error, never "nothing held".
    {"name": "integrity-404", "hash": GEN1,
     "files": {"structure/catena/01-gen/001.json": None}},
    # Fail-closed typed validation, one scenario per key, cold load.
    {"name": "invalid-book", "hash": "#book=Foo&chapter=1&bible=douay-rheims"},
    {"name": "invalid-chapter", "hash": "#book=Gen&chapter=99&bible=douay-rheims"},
    {"name": "invalid-bible", "hash": "#book=Gen&chapter=1&bible=nope"},
    {"name": "invalid-voice", "hash": GEN1 + "&voice=klingon"},
    {"name": "invalid-voice-colon", "hash": GEN1 + "&voice=translation:"},
    # `original:x` parses to an original VOICE without being the literal key;
    # honouring it self-contradicted (an "original — none here" option beside
    # the held original). The whole key must be sound.
    {"name": "invalid-voice-original-lang", "hash": GEN1 + "&voice=original:x"},
    # An out-of-range chapter with no book cited: ranged against the default.
    {"name": "chapter-only-cold", "hash": "#chapter=999"},
    # The same arriving by hashchange: ranged against the CURRENT book.
    {"name": "chapter-only-change", "hash": "#book=Ex&chapter=3&bible=douay-rheims",
     "steps": [{"do": "hash", "value": "#chapter=999", "label": "broken"}]},
    # A broken book beside a sound voice: the seeded control keeps the voice.
    {"name": "invalid-book-with-voice",
     "hash": "#book=Foo&chapter=1&bible=douay-rheims&voice=translation:en"},
    # Value-identical but non-canonical: scrambled order, a leading zero, a
    # percent-encoded colon and an unknown key. Arrival must not rewrite it.
    {"name": "noncanonical-arrival",
     "hash": "#chapter=01&book=Gen&bible=douay-rheims&voice=translation%3Aen&note=kept"},
    # Partial but valid: completed in place, never by pushing an entry.
    {"name": "partial-arrival", "hash": "#book=Gen"},
    {"name": "no-hash-arrival", "hash": ""},
    {"name": "invalid-recovery", "hash": "#book=Foo&chapter=1&bible=douay-rheims",
     "steps": [{"do": "hash", "value": GEN1, "label": "recovered"}]},
    {"name": "hashchange-invalid", "hash": GEN1,
     "steps": [{"do": "hash", "value": "#book=Gen&chapter=99&bible=douay-rheims",
                "label": "broken"}]},
    # Back and Forward, simulated as the browser fires them.
    {"name": "back-forward", "hash": GEN1,
     "steps": [
         {"do": "selectChapter", "value": "2", "label": "stepped"},
         {"do": "hash", "value": GEN1, "label": "back"},
         {"do": "hash", "value": GEN2, "label": "forward"},
     ]},
    # A carried-over exclusion landing on a single-author chapter: the filter
    # must still exist, say so, and offer the way back.
    {"name": "hidden-author-carry", "hash": GEN1,
     "steps": [
         {"do": "toggleAuthor", "author": "Remigius of Auxerre", "label": "hidden"},
         {"do": "hash", "value": GEN42, "label": "gen42"},
         {"do": "toggleAuthor", "author": "Remigius of Auxerre", "label": "restored"},
     ]},
]

REPLAY = r"""
'use strict';

/* The catena page, replayed under node. Every file the page is made of is
 * the real one; only the document, the network and the bible chapter text
 * are stubbed — the chapter text because it is generated into the build. */

const fs = require('fs');
const pathlib = require('path');

const [, , ROOT, PLAN_JSON] = process.argv;
const PLAN = JSON.parse(PLAN_JSON);
const DATA = pathlib.join(ROOT, 'src/web/data');
const BROWSER = pathlib.join(ROOT, 'src/web/browser');

class TextNode {
  constructor(text) { this.nodeType = 3; this.parentNode = null; this.data = String(text); }
  get textContent() { return this.data; }
  set textContent(value) { this.data = String(value); }
}

class ClassList {
  constructor(node) { this.node = node; }
  _names() {
    return this.node.className ? this.node.className.split(/\s+/).filter(Boolean) : [];
  }
  add(...names) {
    const held = this._names();
    for (const name of names) if (!held.includes(name)) held.push(name);
    this.node.className = held.join(' ');
  }
  remove(...names) {
    this.node.className = this._names().filter((one) => !names.includes(one)).join(' ');
  }
  contains(name) { return this._names().includes(name); }
}

class Element {
  constructor(tag) {
    this.nodeType = 1;
    this.localName = String(tag).toLowerCase();
    this.tagName = this.localName.toUpperCase();
    this.childNodes = [];
    this.parentNode = null;
    this.attributes = Object.create(null);
    this.listeners = Object.create(null);
    this.className = '';
    this.style = {};
  }
  get classList() { return new ClassList(this); }
  get firstChild() { return this.childNodes[0] || null; }
  get children() { return this.childNodes.filter((one) => one.nodeType === 1); }
  get id() { return this.attributes.id || ''; }
  set id(value) { this.attributes.id = String(value); }
  appendChild(child) {
    if (child.parentNode) child.parentNode.removeChild(child);
    child.parentNode = this;
    this.childNodes.push(child);
    this._childrenChanged();
    return child;
  }
  insertBefore(child, before) {
    if (!before) return this.appendChild(child);
    if (child.parentNode) child.parentNode.removeChild(child);
    const at = this.childNodes.indexOf(before);
    child.parentNode = this;
    this.childNodes.splice(at < 0 ? this.childNodes.length : at, 0, child);
    this._childrenChanged();
    return child;
  }
  removeChild(child) {
    const at = this.childNodes.indexOf(child);
    if (at >= 0) this.childNodes.splice(at, 1);
    child.parentNode = null;
    this._childrenChanged();
    return child;
  }
  _childrenChanged() {}
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return name in this.attributes ? this.attributes[name] : null; }
  hasAttribute(name) { return name in this.attributes; }
  removeAttribute(name) { delete this.attributes[name]; }
  addEventListener(type, handler) {
    (this.listeners[type] = this.listeners[type] || []).push(handler);
  }
  dispatch(type) {
    for (const handler of this.listeners[type] || []) handler({ target: this, type: type });
  }
  get textContent() { return this.childNodes.map((one) => one.textContent).join(''); }
  set textContent(value) {
    this.childNodes = [];
    if (value !== '' && value !== null && value !== undefined) {
      this.appendChild(new TextNode(value));
    }
  }
  descendants() {
    const out = [];
    const walk = (node) => {
      for (const child of node.childNodes) {
        if (child.nodeType !== 1) continue;
        out.push(child);
        walk(child);
      }
    };
    walk(this);
    return out;
  }
}

/* The one element that needs real semantics: assigning a value no option
 * carries selects nothing and reads back empty. */
class SelectElement extends Element {
  constructor(tag) { super(tag); this.selectedIndex = -1; }
  _options() { return this.descendants().filter((one) => one.localName === 'option'); }
  _childrenChanged() {
    const options = this._options();
    if (!options.length) this.selectedIndex = -1;
    else if (this.selectedIndex < 0 && options.length === 1) this.selectedIndex = 0;
  }
  get value() {
    const options = this._options();
    if (this.selectedIndex < 0 || this.selectedIndex >= options.length) return '';
    const one = options[this.selectedIndex].value;
    return one === undefined ? '' : String(one);
  }
  set value(wanted) {
    this.selectedIndex = this._options().findIndex(
      (one) => String(one.value === undefined ? '' : one.value) === String(wanted));
  }
}

function createElement(tag) {
  const name = String(tag).toLowerCase();
  return name === 'select' ? new SelectElement(name) : new Element(name);
}

function matches(node, selector) {
  if (selector.startsWith('#')) return node.id === selector.slice(1);
  if (selector.startsWith('.')) return new ClassList(node).contains(selector.slice(1));
  const [tag, ...classes] = selector.split('.');
  if (tag && node.localName !== tag.toLowerCase()) return false;
  return classes.every((one) => new ClassList(node).contains(one));
}

function makeDocument() {
  const root = new Element('html');
  const body = new Element('body');
  body.className = 'catena-page';
  root.appendChild(body);
  const document = {
    documentElement: root,
    body: body,
    listeners: Object.create(null),
    createElement: createElement,
    createTextNode: (text) => new TextNode(text),
    getElementById: (id) => root.descendants().find((one) => one.id === id) || null,
    querySelector: (s) => root.descendants().find((one) => matches(one, s)) || null,
    querySelectorAll: (s) => root.descendants().filter((one) => matches(one, s)),
    addEventListener: (type, handler) => {
      (document.listeners[type] = document.listeners[type] || []).push(handler);
    }
  };
  return document;
}

/* The shape of the STATIC catena/index.html the script reaches into: empty
 * reference, "Needs JavaScript" placeholder options, the open controls
 * disclosure, and a static-entry section in main — no aria-busy, no
 * "Loading" placeholder. */
function buildPage(document) {
  const body = document.body;
  const add = (parent, tag, id, className) => {
    const node = document.createElement(tag);
    if (id) node.id = id;
    if (className) node.className = className;
    parent.appendChild(node);
    return node;
  };
  const header = add(body, 'header', null, 'page-header');
  const line = add(header, 'p', null, 'reference-line');
  add(line, 'span', 'reference');
  add(line, 'span', 'reference-book', 'reference-book');
  add(header, 'p', 'tally', 'tally');
  add(body, 'div', 'banner', 'banner');

  const disclosure = add(body, 'details', 'controls-filter', 'controls-filter');
  disclosure.open = true;
  add(disclosure, 'summary').textContent = 'Change chapter and commentary voice';
  const controls = add(disclosure, 'form', 'controls', 'controls');
  for (const id of ['book-select', 'chapter-select', 'bible-select', 'language-select']) {
    const select = add(add(controls, 'div', null, 'field'), 'select', id);
    select.disabled = true;
    const option = add(select, 'option');
    option.value = '';
    option.textContent = 'Needs JavaScript';
  }
  const steps = add(controls, 'div', null, 'field field-steps');
  add(steps, 'button', 'prev-button').disabled = true;
  add(steps, 'button', 'next-button').disabled = true;

  const reading = add(body, 'main', 'reading', 'reading');
  reading.setAttribute('tabindex', '-1');
  const entry = add(reading, 'section', null, 'static-entry');
  add(entry, 'p').textContent = 'Catena Omnia sets a chapter of Scripture beside every commentary fragment this project holds on it.';
  return { reading: reading, controlsDisclosure: disclosure };
}

const VERSES = {};
for (let n = 1; n <= 31; n += 1) VERSES[String(n)] = 'Verse ' + n + ' of the stub chapter.';

function corpusFile(path) {
  const chapter = /^([a-z0-9-]+)\/chapters\/([^/]+)\/(\d+)\.json$/.exec(path);
  if (chapter) return { book: chapter[2], chapter: Number(chapter[3]), verses: VERSES };
  const onDisk = pathlib.join(DATA, path);
  if (!fs.existsSync(onDisk)) return null;
  return JSON.parse(fs.readFileSync(onDisk, 'utf8'));
}

function inspect(page, document, location, fetched, hashWrites, replaced) {
  const reading = page.reading;
  const nodes = reading.descendants();
  const withClass = (name) => nodes.filter((one) => new ClassList(one).contains(name));
  const first = (name) => withClass(name)[0] || null;
  const text = (node) => (node ? node.textContent : null);
  const byId = (id) => document.getElementById(id);
  const filter = first('author-filter');
  const link = first('fragment-whole');
  const status = byId('reading-status');
  const groups = withClass('author').map((item) => {
    const inside = item.descendants();
    const of = (name) => {
      const found = inside.find((one) => new ClassList(one).contains(name));
      return found ? found.textContent : null;
    };
    const body = inside.find((one) => new ClassList(one).contains('author-body'));
    return {
      author: of('author-name'),
      date: of('author-date'),
      count: of('author-count'),
      open: Boolean(body && body.open),
      hidden: Boolean(item.hidden)
    };
  });
  const errors = withClass('catena-error').map((section) => {
    const inside = section.descendants();
    const anchor = inside.find((one) => one.localName === 'a');
    return {
      heading: section.children[0] ? section.children[0].textContent : null,
      state: section.getAttribute('data-state'),
      details: inside
        .filter((one) => new ClassList(one).contains('error-detail'))
        .map((one) => one.textContent),
      recoveryHref: anchor ? anchor.href : null
    };
  });
  const ackPlacement = withClass('fragment-body')
    .filter((body) => body.descendants()
      .some((one) => new ClassList(one).contains('fragment-acknowledgement')))
    .map((body) => {
      const kids = body.children.map((one) => one.className || one.localName);
      return kids.indexOf('fragment-acknowledgement') < kids.findIndex(
        (one) => String(one).startsWith('fragment-text'));
    });
  return {
    hash: location.hash,
    referenceText: text(byId('reference')),
    tallyText: text(byId('tally')),
    statusText: text(status),
    voice: byId('language-select').value,
    voiceLabels: byId('language-select').descendants()
      .filter((one) => one.localName === 'option')
      .map((one) => one.textContent),
    selectValues: {
      book: byId('book-select').value,
      chapter: byId('chapter-select').value,
      bible: byId('bible-select').value
    },
    controlsOpen: Boolean(page.controlsDisclosure.open),
    classes: [...new Set(nodes.map((one) => one.className).filter(Boolean))].sort(),
    dataStates: [...new Set(nodes
      .filter((one) => one.hasAttribute('data-state'))
      .map((one) => one.getAttribute('data-state')))].sort(),
    chapterOpen: Boolean((first('chapter-body') || {}).open),
    chapterCounts: withClass('chapter-count').map(text),
    authorGroups: groups,
    authorFilterInDisclosure: Boolean(
      filter && filter.parentNode
        && new ClassList(filter.parentNode).contains('author-filter-disclosure')),
    authorFilterOpen: Boolean(filter && filter.parentNode && filter.parentNode.open),
    filterLabels: filter
      ? filter.descendants().filter((one) => new ClassList(one).contains('author-toggle'))
          .map(text)
      : [],
    filterChecked: filter
      ? filter.descendants().filter((one) => one.localName === 'input')
          .map((one) => Boolean(one.checked))
      : [],
    fragmentCount: withClass('fragment').length,
    linkText: text(link),
    linkHref: link ? link.href : null,
    refusal: text(first('refusal')),
    paragraphNote: text(first('paragraph-note')),
    projected: nodes.filter((one) => new ClassList(one).contains('projected')).length,
    paragraphs: withClass('passage-paragraph').length,
    spans: withClass('spans').map(text),
    absenceSummary: first('absence-note') ? text(first('absence-note').children[0]) : null,
    absenceReasons: withClass('absence-reason').map(text),
    absencePartials: withClass('absence-partial').map(text),
    sectionHeadings: withClass('section-heading').map(text),
    asideNotes: withClass('aside-note').map(text),
    leads: withClass('lead').map(text),
    blocked: withClass('blocked').map(text),
    fragmentTexts: withClass('fragment-text').map(text),
    fragmentBases: withClass('fragment-basis').map(text),
    sourceLines: withClass('fragment-source').map(text),
    acknowledgements: withClass('fragment-acknowledgement').map(text),
    acknowledgementAboveText: ackPlacement,
    languages: withClass('fragment-language').map(text),
    states: withClass('state').map(text),
    errorSections: errors,
    staticEntry: Boolean(first('static-entry')),
    hashWrites: (hashWrites || []).slice(),
    replaced: (replaced || []).slice(),
    fetched: fetched.slice()
  };
}

async function settle() {
  for (let turn = 0; turn < 400; turn += 1) await Promise.resolve();
  await new Promise((accept) => setTimeout(accept, 0));
  for (let turn = 0; turn < 400; turn += 1) await Promise.resolve();
}

async function run(scenario) {
  const document = makeDocument();
  /* The address bar: assignments to location.hash are the PUSHING writes a
   * browser turns into history entries, so they are recorded; the harness's
   * own Back/Forward simulation bypasses the setter, exactly as a browser
   * restoring a hash does not re-assign it. replaceState swaps the entry in
   * place and is recorded separately. */
  let hashValue = scenario.hash || '';
  const hashWrites = [];
  const replaced = [];
  const location = {
    search: '',
    pathname: '/catena/',
    get hash() { return hashValue; },
    set hash(next) { hashValue = String(next); hashWrites.push(hashValue); }
  };
  const window = {
    location: location,
    history: {
      replaceState: (state, title, url) => {
        const target = String(url);
        const cut = target.indexOf('#');
        hashValue = cut >= 0 ? target.slice(cut) : '';
        replaced.push(target);
      }
    },
    listeners: Object.create(null),
    addEventListener: (type, handler) => {
      (window.listeners[type] = window.listeners[type] || []).push(handler);
    },
    matchMedia: (query) => ({
      media: query,
      matches: Boolean(scenario.narrow) && /max-width/.test(query)
    })
  };
  const page = buildPage(document);
  const overrides = scenario.files || {};
  const fetched = [];

  global.window = window;
  global.document = document;
  global.location = location;
  global.fetch = async (url) => {
    const path = String(url).replace(/^\.\.\/browse\//, '');
    fetched.push(path);
    const has = Object.prototype.hasOwnProperty.call(overrides, path);
    const body = has ? overrides[path] : corpusFile(path);
    if (body === null || body === undefined) {
      return { ok: false, status: 404, json: async () => null };
    }
    return { ok: true, status: 200, json: async () => body };
  };

  for (const file of ['shared/browser-core.js', 'catena/catena-model.js', 'catena/catena.js']) {
    const source = fs.readFileSync(pathlib.join(BROWSER, file), 'utf8');
    new Function('window', 'self', 'document', 'fetch', 'location', source)(
      window, window, document, global.fetch, location);
  }
  await settle();

  const snapshots = {};
  snapshots.start = inspect(page, document, location, fetched, hashWrites, replaced);

  for (const step of scenario.steps || []) {
    if (step.do === 'hash') {
      // The browser: Back, Forward, or a typed hash — the URL changes and a
      // hashchange event fires. The raw assignment bypasses the recording
      // setter: history restoration is not a page-initiated write.
      hashValue = step.value;
      for (const handler of window.listeners.hashchange || []) handler({});
      await settle();
    } else if (step.do === 'selectChapter') {
      const select = document.getElementById('chapter-select');
      select.value = step.value;
      select.dispatch('change');
      await settle();
    } else if (step.do === 'toggleAuthor') {
      const filter = document.querySelector('.author-filter');
      const label = filter && filter.descendants().find(
        (one) => new ClassList(one).contains('author-toggle')
          && one.textContent === step.author);
      if (label) {
        const box = label.descendants().find((one) => one.localName === 'input');
        box.checked = !box.checked;
        box.dispatch('change');
      }
      await settle();
    } else if (step.do === 'openFragmentOf') {
      const item = page.reading.descendants().find(
        (one) => new ClassList(one).contains('fragment')
          && one.descendants().some((deep) =>
            new ClassList(deep).contains('fragment-author')
              && deep.textContent === step.author));
      const body = item && item.descendants().find(
        (one) => new ClassList(one).contains('fragment-body'));
      if (body) {
        body.open = true;
        body.dispatch('toggle');
      }
      await settle();
    } else if (step.do === 'openFirstFragment') {
      const body = page.reading.descendants()
        .find((one) => new ClassList(one).contains('fragment-body'));
      if (body) {
        body.open = true;
        body.dispatch('toggle');
      }
      await settle();
    }
    snapshots[step.label || step.do] = inspect(page, document, location, fetched, hashWrites, replaced);
  }

  const report = inspect(page, document, location, fetched, hashWrites, replaced);
  report.snapshots = snapshots;
  return report;
}

(async () => {
  const report = {};
  for (const scenario of PLAN) {
    try {
      report[scenario.name] = await run(scenario);
    } catch (error) {
      report[scenario.name] = { error: String((error && error.stack) || error) };
    }
  }
  process.stdout.write(JSON.stringify(report));
})();
"""


_REPLAYED: dict | None = None


def replayed() -> dict:
    """Run every scenario once; the corpus is large and the states are many."""
    global _REPLAYED
    if _REPLAYED is None:
        handle, path = tempfile.mkstemp(suffix=".js", prefix="catena-replay-")
        os.close(handle)
        try:
            Path(path).write_text(REPLAY, encoding="utf-8")
            result = subprocess.run(
                [NODE, path, str(ROOT), json.dumps(SCENARIOS)],
                cwd=ROOT, capture_output=True, text=True,
            )
            if result.returncode != 0:
                raise AssertionError(result.stderr.strip() or "the replay harness exited non-zero")
            _REPLAYED = json.loads(result.stdout)
        finally:
            os.unlink(path)
    return _REPLAYED


@unittest.skipIf(NODE is None, "node is not installed; the page cannot be replayed")
class ReplayTest(unittest.TestCase):
    """Base for every test that reads the replayed page."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = replayed()

    def page(self, name: str) -> dict:
        one = self.pages[name]
        self.assertNotIn("error", one, one.get("error", ""))
        return one

    def snapshot(self, name: str, label: str) -> dict:
        return self.page(name)["snapshots"][label]


class ChronologyTest(ReplayTest):
    """Finding 2 — the chain's chronology survives grouping.

    The generator orders fragments by text date. The first candidate then
    coalesced every work by author, so Genesis 1 rendered Augustine 401,
    Augustine 417 and Severian 401 under one Augustine heading labelled 401.
    Only a CONTIGUOUS run by one author with one date may share a heading.
    """

    EXPECTED = [
        ("Basil of Caesarea", "378", 18),
        ("Gregory of Nyssa", "379", 1),
        ("Ambrose of Milan", "386", 6),
        ("Jerome", "391", 2),
        ("Augustine of Hippo", "401", 4),
        ("Severian of Gabala", "401", 5),
        ("Augustine of Hippo", "417", 3),
        ("Bede", "717", 35),
        ("Alcuin of York", "796", 4),
        ("Angelomus of Luxeuil", "845", 17),
        ("Remigius of Auxerre", "890", 11),
        ("Martin Luther", "1535", 1),
    ]

    def test_genesis_1_renders_twelve_groups_in_text_date_order(self):
        groups = self.page("default")["authorGroups"]
        self.assertEqual(
            [(one["author"], one["date"]) for one in groups],
            [(author, date) for author, date, _ in self.EXPECTED],
        )

    def test_augustine_severian_augustine_stand_as_three_groups(self):
        groups = self.page("default")["authorGroups"]
        middle = [(one["author"], one["date"]) for one in groups[4:7]]
        self.assertEqual(middle, [
            ("Augustine of Hippo", "401"),
            ("Severian of Gabala", "401"),
            ("Augustine of Hippo", "417"),
        ])

    def test_the_groups_carry_every_fragment_exactly_once(self):
        groups = self.page("default")["authorGroups"]
        counts = [int(re.match(r"(\d+)", one["count"]).group(1)) for one in groups]
        self.assertEqual(counts, [count for _, _, count in self.EXPECTED])
        self.assertEqual(sum(counts), 107)
        self.assertEqual(self.page("default")["fragmentCount"], 107)


class VoiceCountTruthTest(ReplayTest):
    """Finding 8a — the tally states the corpus, never the filter.

    Genesis 10 holds 71 fragments, all in their authors' own Latin. Selecting
    English used to headline "Nothing held here"; the corpus truth now leads
    and the empty selection is a second clause.
    """

    def test_an_empty_voice_selection_never_reads_as_an_empty_chapter(self):
        page = self.page("voice-empty-chapter")
        self.assertEqual(
            page["tallyText"],
            "71 fragments held · none in English translation"
            " · 28 works on the acquisition list")
        self.assertNotIn("Nothing", page["tallyText"])
        self.assertIn("71 fragments held, 0 shown", page["statusText"])
        self.assertTrue(any(
            "71 fragments are held here, in the author’s own language" in one
            for one in page["asideNotes"]))

    def test_a_voice_showing_a_subset_is_a_second_clause(self):
        page = self.page("voice-held")
        self.assertEqual(
            page["tallyText"],
            "107 fragments held · 14 in English translation"
            " · 33 works on the acquisition list")

    def test_the_unfiltered_tally_counts_the_corpus(self):
        self.assertEqual(
            self.page("default")["tallyText"],
            "107 fragments held · 33 works on the acquisition list")

    def test_a_chapter_with_nothing_says_nothing_held(self):
        self.assertEqual(self.page("nothing-held")["tallyText"], "Nothing held here")


class AbsenceCountTest(ReplayTest):
    """Finding 8b — partial-public-domain findings are counted apart.

    Two of Genesis 1's eight recorded English absences are partly public
    domain; filing them under "no English this project may publish" overstated
    the bar the record actually sets.
    """

    def test_the_heading_counts_the_two_findings_apart(self):
        page = self.page("voice-held")
        self.assertEqual(
            page["absenceSummary"],
            "6 works standing here have no English this project may publish; "
            "2 have only a partly public domain English, not yet taken")

    def test_every_absence_still_carries_its_reason_and_partials_their_offer(self):
        page = self.page("voice-held")
        self.assertEqual(len(page["absenceReasons"]), 8)
        self.assertTrue(all(one.strip() for one in page["absenceReasons"]))
        self.assertEqual(len(page["absencePartials"]), 2)
        self.assertTrue(all(one.startswith("Partly public domain — ")
                            for one in page["absencePartials"]))


class ParagraphCountTest(ReplayTest):
    """Finding 8c — the paragraph chip counts paragraphs, not breaks.

    Genesis 1 in the Douay edition carries seven projected BREAKS, which open
    eight PARAGRAPHS; the chip used to print the break count under the word
    "paragraphs".
    """

    def test_the_chip_counts_the_paragraphs_on_the_page(self):
        page = self.page("default")
        self.assertEqual(page["projected"], 7)
        self.assertEqual(page["paragraphs"], 8)
        self.assertIn("8 paragraphs", page["chapterCounts"])
        self.assertNotIn("7 paragraphs", page["chapterCounts"])

    def test_the_note_still_speaks_of_breaks_in_those_words(self):
        self.assertEqual(
            self.page("default")["paragraphNote"],
            "Paragraphs: 7 are projected from the witnesses that concur, and marked.")

    def test_a_chapter_with_no_paragraph_data_says_it_runs_on(self):
        note = self.page("numbering-refusal")["paragraphNote"]
        self.assertIn("No paragraph division is held for this chapter", note)
        self.assertIn("Another edition’s paragraphs are not borrowed for it.", note)


class AuthorFilterRecoveryTest(ReplayTest):
    """Finding 8d — a filter can never strand the reader.

    Exclusions persist across chapters, so a sole author switched off
    elsewhere used to leave a chapter with zero visible fragments and no
    control at all. The filter now exists whenever an exclusion touches the
    chapter, the heading says everything is switched off, and the disclosure
    opens itself.
    """

    def test_a_fresh_single_author_chapter_grows_no_filter(self):
        page = self.page("one-commentator")
        self.assertEqual(page["fragmentCount"], 3)
        self.assertEqual(len(page["authorGroups"]), 1)
        self.assertFalse(page["authorFilterInDisclosure"])

    def test_a_partial_filter_is_reported_against_the_held_total(self):
        hidden = self.snapshot("hidden-author-carry", "hidden")
        self.assertIn("107 fragments held here — 96 shown", hidden["sectionHeadings"])

    def test_a_carried_exclusion_still_offers_the_switch_on_a_sole_author(self):
        gen42 = self.snapshot("hidden-author-carry", "gen42")
        self.assertEqual(gen42["filterLabels"], ["Remigius of Auxerre"])
        self.assertEqual(gen42["filterChecked"], [False])
        self.assertTrue(gen42["authorFilterOpen"],
                        "the disclosure must open when everything is hidden")
        self.assertIn(
            "3 fragments held here — none shown; every author is switched off below",
            gen42["sectionHeadings"])
        self.assertTrue(all(one["hidden"] for one in gen42["authorGroups"]))

    def test_the_switch_restores_the_chain(self):
        restored = self.snapshot("hidden-author-carry", "restored")
        self.assertIn("3 fragments held here", restored["sectionHeadings"])
        self.assertFalse(any(one["hidden"] for one in restored["authorGroups"]))


class IntegrityErrorTest(ReplayTest):
    """Finding 8e — an expected spine that 404s is an error, not an absence.

    The index lists Genesis 1 as present; when its record cannot be fetched
    the page must not say "nothing is held here", which the record proves
    false.
    """

    def test_a_missing_expected_record_renders_as_an_error(self):
        page = self.page("integrity-404")
        self.assertTrue(page["errorSections"])
        error = page["errorSections"][0]
        self.assertEqual(error["heading"], "This chapter’s commentary record did not load")
        self.assertEqual(error["state"], "error")
        self.assertTrue(any("structure/catena/01-gen/001.json" in one
                            for one in error["details"]))

    def test_the_error_never_claims_emptiness(self):
        page = self.page("integrity-404")
        self.assertNotIn("No commentary on this chapter is held yet.", page["asideNotes"])
        self.assertNotIn("Nothing", page["tallyText"])
        self.assertEqual(page["tallyText"], "The commentary record did not load")
        self.assertIn("commentary record unavailable", page["statusText"])

    def test_the_scripture_itself_still_renders(self):
        self.assertTrue(self.page("integrity-404")["chapterOpen"])

    def test_a_chapter_the_index_omits_is_still_a_plain_absence(self):
        page = self.page("nothing-held")
        self.assertFalse(page["errorSections"])
        self.assertIn("No commentary on this chapter is held yet.", page["asideNotes"])
        self.assertFalse(
            [one for one in page["fetched"] if one.startswith("structure/catena/02-ex/")],
            "a chapter the index does not list must not be asked for")


class LeadsCopyTest(ReplayTest):
    """Finding 3, route half — the acquisition list asserts only the record.

    The generated leads overlap held works on real chapters (Genesis 1 lists
    six held works), so the page may claim neither "not yet acquired" nor
    that no text of any lead is held. Identity reconciliation is the
    generator's; the rows are printed as recorded, unhidden and unreordered.
    """

    def test_the_heading_and_note_claim_only_the_record(self):
        page = self.page("acquisition-only")
        self.assertIn("Believed to comment here — the acquisition list",
                      page["sectionHeadings"])
        note = next(one for one in page["asideNotes"]
                    if "acquisition record" in one)
        self.assertIn("printed as recorded", note)
        self.assertIn("not checked against it here", note)

    def test_the_old_overclaims_are_gone(self):
        script = held(CATENA / "catena.js")
        page_source = held(CATENA / "index.html")
        for overclaim in ("not yet acquired", "no text of any"):
            self.assertNotIn(overclaim, script)
            self.assertNotIn(overclaim, page_source)

    def test_the_rows_are_printed_as_recorded(self):
        page = self.page("acquisition-only")
        self.assertEqual(page["fragmentCount"], 0)
        self.assertEqual(len(page["leads"]), 15)
        # Genesis 1's 33 rows include held works; they are not hidden here.
        self.assertEqual(len(self.page("default")["leads"]), 33)

    def test_the_tally_speaks_of_the_list_not_of_acquisition_state(self):
        self.assertIn("works on the acquisition list", self.page("default")["tallyText"])


class RightsRenderingTest(ReplayTest):
    """Finding 4, route half — every rights fact the payload supplies renders.

    The corpus today reduces the Severian CC BY-SA terms to `rights:
    "licensed"` plus an `edition_published` line that carries the Voicu /
    von Stockhausen / BBAW attribution prose; projecting the full licence
    metadata is a recorded generator prerequisite. The page renders every
    field that exists and invents nothing for the ones that do not.
    """

    def test_the_severian_provenance_prints_everything_the_spine_carries(self):
        lines = [one for one in self.page("severian-open")["sourceLines"]
                 if "Patristic Text Archive" in one]
        self.assertEqual(len(lines), 5, "five Severian fragments stand on Genesis 1")
        for line in lines:
            self.assertIn("In cosmogoniam homiliae 1-6, Patristic Text Archive edition pta-grc1", line)
            self.assertIn("Berlin-Brandenburgische Akademie der Wissenschaften, 2018", line)
            self.assertIn("Sever J. Voicu", line)
            self.assertIn("licensed", line)
            self.assertIn("inspected, not collated", line)

    def test_a_bare_licensed_rights_value_prints_truthfully_and_no_more(self):
        page = self.page("severian-open")
        self.assertFalse(page["acknowledgements"],
                         "no acknowledgement exists in the payload; none may be invented")
        self.assertTrue(all("public-domain" in one or "licensed" in one
                            for one in page["sourceLines"]))

    def test_every_fragment_prints_its_edition_printing(self):
        # Every Genesis 1 source records an edition_published; each line
        # carries it (NPNF shown as the concrete witness).
        self.assertTrue(any("New York: Christian Literature Company, 1895" in one
                            for one in self.page("default")["sourceLines"]))

    def test_provenance_stands_whether_or_not_the_text_loads(self):
        # Source lines exist for all 107 fragments before any text is fetched.
        self.assertEqual(len(self.page("voice-held")["snapshots"]["start"]["fetched"]), 6)
        self.assertEqual(len(self.page("default")["sourceLines"]), 107)

    def test_a_recorded_acknowledgement_renders_above_the_prose(self):
        """SYNTHETIC fixture: the corpus does not yet project these fields."""
        start = self.snapshot("synthetic-licence", "first-open")
        self.assertIn("Licence: Greek text by A. Editor, CC BY-SA 4.0; share alike.",
                      start["acknowledgements"])
        self.assertTrue(all(start["acknowledgementAboveText"]),
                        "the acknowledgement must precede the prose it covers")
        severian_line = self.snapshot("synthetic-licence", "first-open")["sourceLines"][0]
        self.assertIn("Attribution: A. Editor, Synthetic Academy", severian_line)
        self.assertNotIn("suppressed because an acknowledgement states the terms",
                         severian_line)

    def test_rights_basis_prints_only_without_an_acknowledgement(self):
        """SYNTHETIC fixture, second source: rights_basis and no acknowledgement."""
        page = self.snapshot("synthetic-licence", "second-open")
        second_line = page["sourceLines"][1]
        self.assertIn("printed because no acknowledgement is recorded", second_line)
        # A text-file acknowledgement arrives with the prose and sits above it.
        self.assertIn("Licence: Text-file licence note, CC BY-SA 4.0.",
                      page["acknowledgements"])
        self.assertTrue(all(page["acknowledgementAboveText"]))


class HashValidationTest(ReplayTest):
    """Finding 5 — the cited state fails closed, cold and on hashchange.

    Every invalid value is retained in the URL exactly as written, named in a
    visible error state, and answered with recovery; no default is silently
    selected and no stale chapter stands under a broken address.
    """

    def assert_failed_closed(self, name: str, written: str, named: str):
        page = self.page(name)
        self.assertEqual(page["hash"], written, "the URL keeps the reader's own text")
        self.assertTrue(page["errorSections"], "a visible error state is owed")
        error = page["errorSections"][0]
        self.assertEqual(error["heading"], "This address names what the page does not have")
        self.assertEqual(error["state"], "error")
        self.assertTrue(any(named in one for one in error["details"]),
                        f"{named!r} not named in {error['details']}")
        self.assertTrue(error["recoveryHref"], "recovery must be offered")
        self.assertEqual(page["referenceText"], "Address not recognised")
        self.assertEqual(page["fragmentCount"], 0, "no content may render under the error")
        self.assertFalse([one for one in page["fetched"] if "/chapters/" in one],
                         "no chapter may be fetched for an invalid address")

    def test_an_unknown_book_fails_closed(self):
        self.assert_failed_closed(
            "invalid-book", "#book=Foo&chapter=1&bible=douay-rheims",
            "book=Foo is not a book of this canon")
        self.assertEqual(self.page("invalid-book")["errorSections"][0]["recoveryHref"],
                         "#book=Gen&chapter=1&bible=douay-rheims")

    def test_a_chapter_out_of_range_fails_closed(self):
        self.assert_failed_closed(
            "invalid-chapter", "#book=Gen&chapter=99&bible=douay-rheims",
            "chapter=99 is not a chapter of Genesis, which has 50")

    def test_an_unknown_bible_fails_closed(self):
        self.assert_failed_closed(
            "invalid-bible", "#book=Gen&chapter=1&bible=nope",
            "bible=nope is not a published edition")

    def test_a_malformed_voice_fails_closed(self):
        self.assert_failed_closed(
            "invalid-voice", "#book=Gen&chapter=1&bible=douay-rheims&voice=klingon",
            "voice=klingon is not a voice")

    def test_a_voice_with_no_language_fails_closed(self):
        self.assert_failed_closed(
            "invalid-voice-colon", "#book=Gen&chapter=1&bible=douay-rheims&voice=translation:",
            "voice=translation: is not a voice")

    def test_an_original_carrying_a_language_fails_closed(self):
        # `parseVoiceKey('original:x')` yields voice === original; honouring
        # the fragment of a key rendered a self-contradicting page.
        self.assert_failed_closed(
            "invalid-voice-original-lang",
            "#book=Gen&chapter=1&bible=douay-rheims&voice=original:x",
            "voice=original:x is not a voice")

    def test_a_bookless_out_of_range_chapter_fails_closed_cold(self):
        self.assert_failed_closed(
            "chapter-only-cold", "#chapter=999",
            "chapter=999 is not a chapter of Genesis, which has 50")

    def test_an_out_of_range_chapter_is_ranged_against_the_current_book(self):
        broken = self.snapshot("chapter-only-change", "broken")
        self.assertEqual(broken["hash"], "#chapter=999")
        self.assertTrue(broken["errorSections"])
        self.assertTrue(any(
            "chapter=999 is not a chapter of Exodus, which has 40" in one
            for one in broken["errorSections"][0]["details"]))
        self.assertEqual(broken["fragmentCount"], 0,
                         "the stale Exodus 3 chain must not stand under the broken address")

    def test_the_invalid_path_seeds_the_voice_control(self):
        # Never a control left saying "Loading…" on the honesty page itself.
        self.assertEqual(self.page("invalid-book")["voiceLabels"], ["Everything held"])
        with_voice = self.page("invalid-book-with-voice")
        self.assertIn("English translation — none here", with_voice["voiceLabels"])
        self.assertEqual(with_voice["voice"], "translation:en")
        self.assertEqual(
            with_voice["errorSections"][0]["recoveryHref"],
            "#book=Gen&chapter=1&bible=douay-rheims&voice=translation%3Aen")

    def test_recovery_keeps_every_sound_value(self):
        # book is broken; chapter and bible are sound and survive; the broken
        # key falls to the default rather than being guessed.
        self.assertEqual(self.page("invalid-chapter")["errorSections"][0]["recoveryHref"],
                         "#book=Gen&chapter=1&bible=douay-rheims")
        self.assertEqual(self.page("invalid-voice")["errorSections"][0]["recoveryHref"],
                         "#book=Gen&chapter=1&bible=douay-rheims")

    def test_the_recovery_link_recovers(self):
        recovered = self.snapshot("invalid-recovery", "recovered")
        self.assertFalse(recovered["errorSections"])
        self.assertEqual(recovered["referenceText"], "Genesis 1")
        self.assertEqual(recovered["fragmentCount"], 107)

    def test_an_invalid_hashchange_replaces_rather_than_leaves_stale_content(self):
        broken = self.snapshot("hashchange-invalid", "broken")
        self.assertEqual(broken["hash"], "#book=Gen&chapter=99&bible=douay-rheims")
        self.assertTrue(broken["errorSections"])
        self.assertEqual(broken["fragmentCount"], 0,
                         "the stale chapter must not stand under the broken address")

    def test_the_controls_take_defaults_but_the_page_does_not_render_them(self):
        page = self.page("invalid-book")
        self.assertEqual(page["selectValues"]["book"], "Gen")
        self.assertEqual(page["fragmentCount"], 0)


class VoiceDeepLinkTest(ReplayTest):
    """Finding 5 — the deferred `voice` deep link, ported from the candidate.

    `start()` used to assign the hash's voice before any option carrying it
    existed; the selection read back empty and the reader's URL was rewritten
    without the key they were sent.
    """

    def test_a_voice_the_chapter_holds_is_honoured_and_kept_in_the_hash(self):
        page = self.page("voice-held")
        self.assertEqual(page["voice"], "translation:en")
        # The arriving address parses to the rendered state, so it is kept
        # byte for byte — no canonicalising rewrite, no extra history entry.
        self.assertEqual(page["hash"], GEN1 + "&voice=translation:en")
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["fragmentCount"], 14)
        self.assertTrue(any("Showing English translation only" in one
                            for one in page["asideNotes"]))

    def test_a_voice_the_chapter_lacks_is_kept_and_named_rather_than_widened(self):
        page = self.page("voice-not-held")
        self.assertEqual(page["voice"], "translation:de")
        self.assertEqual(page["hash"], GEN1 + "&voice=translation:de")
        self.assertEqual(page["hashWrites"], [])
        self.assertIn("German translation — none here", page["voiceLabels"])
        self.assertEqual(page["fragmentCount"], 0)

    def test_the_page_no_longer_assigns_the_voice_before_the_options_exist(self):
        script = held(CATENA / "catena.js")
        start = script.index("async function start()")
        self.assertNotIn("voiceSelect.value = hash.get('voice')", script[start:])
        self.assertIn("wantedVoice = broken.has('voice') ? '' : hash.get('voice') || '';",
                      script[start:])
        self.assertIn("const wanted = voiceSelect.value || wantedVoice;", script)


class HistoryDeterminismTest(ReplayTest):
    """Finding 5 — Back and Forward both render, deterministically.

    The shared `T.onHashChange` recognises the router's own writes by a
    remembered string (`lastWritten`, shared/browser-core.js:937-961); after
    Back restores a hash the router's write finds it already in place,
    returns early, and the remembered string goes stale — Forward is then
    swallowed. The route now compares the arriving hash against what its
    current state would write, so its own echoes are skipped and every
    reader move renders. The shared swallow itself remains the shared
    owner's to fix.
    """

    def test_stepping_writes_the_new_chapter_to_the_url(self):
        stepped = self.snapshot("back-forward", "stepped")
        self.assertEqual(stepped["hash"], "#book=Gen&chapter=2&bible=douay-rheims")
        self.assertEqual(stepped["referenceText"], "Genesis 2")

    def test_back_restores_the_earlier_chapter(self):
        back = self.snapshot("back-forward", "back")
        self.assertEqual(back["referenceText"], "Genesis 1")
        self.assertEqual(back["selectValues"]["chapter"], "1")
        self.assertEqual(back["hash"], "#book=Gen&chapter=1&bible=douay-rheims")

    def test_forward_after_back_renders_rather_than_being_swallowed(self):
        forward = self.snapshot("back-forward", "forward")
        self.assertEqual(forward["referenceText"], "Genesis 2")
        self.assertEqual(forward["selectValues"]["chapter"], "2")

    def test_the_route_listens_for_itself_rather_than_through_the_stale_swallow(self):
        script = held(CATENA / "catena.js")
        self.assertNotIn("T.onHashChange(", script)
        self.assertIn("window.addEventListener('hashchange'", script)
        self.assertIn("window.location.hash === currentHashText()", script)

    def test_an_equivalent_arrival_address_is_never_rewritten(self):
        # Scrambled order, `chapter=01`, `%3A`, and an unknown key all parse
        # to the state the page renders; rewriting any of them would push a
        # history entry Back could only bounce off.
        page = self.page("noncanonical-arrival")
        self.assertEqual(
            page["hash"],
            "#chapter=01&book=Gen&bible=douay-rheims&voice=translation%3Aen&note=kept")
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], [])
        self.assertEqual(page["referenceText"], "Genesis 1")
        self.assertEqual(page["voice"], "translation:en")

    def test_a_partial_arrival_is_completed_in_place_not_by_pushing(self):
        page = self.page("partial-arrival")
        self.assertEqual(page["hashWrites"], [],
                         "arrival normalisation must not push a history entry")
        self.assertEqual(page["replaced"], ["#book=Gen&chapter=1&bible=douay-rheims"])
        self.assertEqual(page["hash"], "#book=Gen&chapter=1&bible=douay-rheims")

    def test_a_hashless_arrival_is_completed_in_place_not_by_pushing(self):
        page = self.page("no-hash-arrival")
        self.assertEqual(page["hashWrites"], [])
        self.assertEqual(page["replaced"], ["#book=Gen&chapter=1&bible=douay-rheims"])

    def test_reader_actions_still_push_exactly_one_entry(self):
        # The chapter step is the one page-initiated write in the scenario;
        # the initial canonical arrival and both history moves write nothing.
        page = self.page("back-forward")
        self.assertEqual(page["hashWrites"], ["#book=Gen&chapter=2&bible=douay-rheims"])


class StaticDocumentTruthTest(unittest.TestCase):
    """Findings 6 and 8f — the static document is true without scripts.

    No permanent "Loading…", no static aria-busy, no disabled selects
    pretending to load; the main region owns real prose, an honest statement
    that this edition needs JavaScript, and working same-origin links. The
    footer's account of what opens agrees with what actually opens.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.page = held(CATENA / "index.html")

    def test_nothing_static_claims_to_be_loading(self):
        rendered = re.sub(r"<!--.*?-->", "", self.page, flags=re.S)
        self.assertNotIn("Loading", rendered)
        self.assertNotIn("aria-busy", rendered)
        self.assertNotIn('class="placeholder"', rendered)

    def test_the_selects_say_the_truth_as_served(self):
        self.assertEqual(self.page.count('<option value="">Needs JavaScript</option>'), 4)

    def test_the_main_region_owns_static_truth_and_browse_entries(self):
        main = self.page[self.page.index("<main"):self.page.index("</main>")]
        self.assertIn("static-entry", main)
        self.assertIn("needs JavaScript", main)
        self.assertIn('href="../sources/"', main)
        self.assertIn('href="../"', main)
        self.assertIn("rights", main)

    def test_the_controls_disclosure_is_static_open_and_wraps_the_form(self):
        self.assertIn('<details id="controls-filter" class="controls-filter" open>', self.page)
        self.assertIn("<summary>Change chapter and commentary voice</summary>", self.page)
        opening = self.page.index('<details id="controls-filter"')
        form = self.page.index('<form id="controls"')
        closing = self.page.index("</details>", opening)
        self.assertLess(opening, form)
        self.assertLess(self.page.index("</form>"), closing)

    def test_the_footer_agrees_with_what_actually_opens(self):
        # Conditional on rendering, so it is also true with scripts off.
        self.assertIn("Once the page renders, the chapter and the first commentator "
                      "stand open", self.page)
        self.assertNotIn("Everything here is closed until you open it", self.page)
        self.assertNotIn("stand open on arrival", self.page)

    def test_the_footer_keeps_its_six_entrances(self):
        for entrance in ("../scripture/", "../liturgy/", "../history/",
                         "../law/", "../sources/", "../texts/"):
            self.assertIn(f'href="{entrance}"', self.page)


class PrintStylesTest(unittest.TestCase):
    """Finding 6 — browser print hides its chrome and names itself.

    Modelled on liturgy/reader-instrument.css and the corpus-foundation
    prototype (both read-only): interaction chrome goes, the reading order
    stands, and a print-only note says the paper copy is not canonical.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.css = held(CATENA / "catena.css")
        cls.block = media_block(cls.css, "@media print")

    def test_the_interaction_chrome_is_hidden(self):
        for chrome in (".controls-filter", ".author-filter-disclosure",
                       ".skip-link", ".banner"):
            self.assertIn(chrome, self.block)
        self.assertIn("display: none !important", self.block)

    def test_the_reading_order_returns_to_document_flow(self):
        self.assertIn(".catena-page .reading { display: block; }", self.block)

    def test_the_page_names_browser_print_as_non_canonical(self):
        self.assertIn("Browser print", self.block)
        self.assertIn("not a", self.block)
        self.assertIn("canonical rendering", self.block)

    def test_every_print_rule_is_scoped_to_the_page(self):
        for selector_list in re.findall(r"([^{}]+)\{", without_comments(self.block)):
            for one in selector_list.split(","):
                one = one.strip()
                if not one:
                    continue
                self.assertTrue(one.startswith(".catena-page"),
                                f"print rule {one!r} is not scoped to .catena-page")


class ForcedColorsTest(unittest.TestCase):
    """Finding 7 — the reserved paragraph edge does not lie in forced colors.

    Every paragraph reserves a transparent 2px border; forced-colors mode
    would materialise it as CanvasText and hand an ordinary passage the same
    mark as a projected boundary. The base forces to Canvas and only
    `.projected` takes CanvasText.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.css = held(CATENA / "catena.css")
        cls.block = media_block(cls.css, "@media (forced-colors: active)")

    def test_the_base_border_forces_to_canvas_and_projected_to_canvastext(self):
        self.assertIn(".catena-page .passage-paragraph { border-left-color: Canvas; }",
                      self.block)
        self.assertIn(
            ".catena-page .passage-paragraph.projected { border-left-color: CanvasText; }",
            self.block)

    def test_the_base_rule_still_reserves_the_transparent_edge(self):
        reserved = " ".join(declarations_for(self.css, ".passage-paragraph"))
        self.assertIn("border-left: 2px solid transparent", reserved)

    def test_the_refusal_keeps_a_visible_rule(self):
        self.assertIn(".catena-page .refusal { border-left-color: CanvasText; }",
                      self.block)

    def test_focus_stays_on_the_system_highlight(self):
        self.assertIn("outline-color: Highlight", self.block)

    def test_presence_and_absence_stay_apart_by_line_style(self):
        # Solid (held) against dashed (lead/blocked/refusal) survives forced
        # colors because it is a style, not a colour; assert the styles.
        dashed = " ".join(declarations_for(self.css, ".lead"))
        self.assertIn("1px dashed", dashed)
        for selector in (".fragment", ".author"):
            for block in declarations_for(self.css, selector):
                self.assertNotIn("dashed", block)


class ComposedButNotSimplifiedTest(unittest.TestCase):
    """The composition reaches held commentary and stops there.

    The corrected composition speaks the shared sheet's own vocabulary — the
    candidate's one-off `--tp-*` palette is gone — and the protected
    epistemic selectors keep the section's palette, so they read apart from
    held commentary rather than with it.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.css = held(CATENA / "catena.css")

    def test_no_second_palette_lives_in_this_stylesheet(self):
        self.assertNotIn("--tp-", self.css)
        # And nothing here declares custom properties or styles the shell.
        self.assertNotIn(":root", without_comments(self.css))
        for selector in re.findall(r"(?m)^([^\s@/][^{]*)\{", without_comments(self.css)):
            for one in selector.split(","):
                self.assertNotIn(one.strip(), {"html", "body"})

    def test_the_protected_selectors_that_were_declared_still_are(self):
        for selector in PROTECTED_AND_DECLARED:
            with self.subTest(selector=selector):
                self.assertTrue(declarations_for(self.css, selector),
                                f"{selector} is no longer declared at all")

    def test_the_absence_selectors_stay_deliberately_undeclared(self):
        for selector in PROTECTED_SELECTORS[:4]:
            with self.subTest(selector=selector):
                self.assertFalse(
                    declarations_for(self.css, selector),
                    f"{selector} gained rules; undeclared is the protected state")

    def test_a_projected_break_is_still_drawn_and_a_printed_one_is_not(self):
        blocks = declarations_for(self.css, ".passage-paragraph.projected")
        base = [one for one in blocks if "CanvasText" not in one]
        self.assertEqual(len(base), 1)
        self.assertIn("border-left-color: var(--section-pale)", base[0])

    def test_an_extent_crossing_a_boundary_is_not_normalised_into_the_chips(self):
        spans = " ".join(declarations_for(self.css, ".spans"))
        self.assertIn("color: var(--section-ink)", spans)
        self.assertIn("font-weight: 600", spans)
        chips = declarations_for(self.css, ".fragment-extent")
        self.assertTrue(any("--ink-soft" in one for one in chips),
                        "the extent itself joins the normalised card catalogue")

    def test_the_card_catalogue_speaks_one_voice(self):
        catalogue = None
        for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", without_comments(self.css)):
            names = {one.strip() for one in block.group(1).split(",")}
            if names >= {".fragment-date", ".fragment-extent", ".fragment-language",
                         ".fragment-length", ".author-date", ".author-count"}:
                catalogue = block.group(2)
        self.assertIsNotNone(catalogue)
        self.assertIn("0.8125rem", catalogue)
        self.assertIn("var(--ink-soft)", catalogue)

    def test_what_cannot_be_read_takes_a_dashed_rule_and_commentary_never_does(self):
        dashed = None
        for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", without_comments(self.css)):
            names = {one.strip() for one in block.group(1).split(",")}
            if names == {".lead", ".blocked", ".refusal"}:
                dashed = block.group(2)
        self.assertIsNotNone(dashed, "the lead/blocked/refusal rule is the distinction")
        self.assertIn("border-bottom: 1px dashed", dashed)

    def test_the_refusal_alone_takes_the_negative_ink_among_content_states(self):
        refusal = " ".join(declarations_for(self.css, ".refusal"))
        self.assertIn("border-left: 0.2rem solid var(--notice)", refusal)
        self.assertIn("color: var(--notice)", refusal)
        for selector in (".fragment", ".author", ".lead", ".blocked",
                         ".aside-note", ".absence-note"):
            for block in declarations_for(self.css, selector):
                self.assertNotIn("--notice", block,
                                 f"{selector} may not take the negative ink")

    def test_the_truthful_column_comment_replaced_the_pinned_claim(self):
        self.assertNotIn("never scrolls away", self.css)
        self.assertNotIn("never has to be scrolled", self.css)
        self.assertIn("not pinned", self.css)


class CompositionTest(ReplayTest):
    """The accepted E0 composition, in the corrected mechanics."""

    def test_the_chapter_opens_and_the_first_group_opens_with_it(self):
        page = self.page("default")
        self.assertTrue(page["chapterOpen"])
        opened = [one["open"] for one in page["authorGroups"]]
        self.assertTrue(opened[0])
        self.assertFalse(any(opened[1:]),
                         "only the first group opens; the rest wait to be asked")

    def test_the_author_filter_is_folded_and_closed_when_nothing_is_hidden(self):
        page = self.page("default")
        self.assertTrue(page["authorFilterInDisclosure"])
        self.assertFalse(page["authorFilterOpen"])

    def test_the_controls_fold_synchronously_on_a_narrow_viewport(self):
        self.assertTrue(self.page("default")["controlsOpen"])
        self.assertFalse(self.page("narrow")["controlsOpen"])
        # Synchronously: before the first awaited fetch, so a slow connection
        # cannot shift the page after the fact.
        script = held(CATENA / "catena.js")
        start = script.index("async function start()")
        fold = script.index("controlsDisclosure.open = false", start)
        first_await = script.index("await Promise.all", start)
        self.assertLess(fold, first_await)

    def test_the_wide_grid_uses_explicit_rows_and_no_magic_span(self):
        css = held(CATENA / "catena.css")
        self.assertIn("@media (min-width: 64.0625rem)", css)
        self.assertIn("grid-template-columns: minmax(20rem, 26rem) minmax(0, 44rem)", css)
        self.assertIn("grid-template-rows: auto auto", css)
        self.assertIn("grid-row: 1 / -1", css)
        self.assertNotIn("span 100", css)

    def test_the_script_builds_one_column_for_everything_beside_the_chapter(self):
        page = self.page("default")
        self.assertIn("chain-column", " ".join(page["classes"]))


class TypedStateTest(ReplayTest):
    """Every state the corpus can put on this page, still told apart.

    Held text, an acquisition-list row, a translation absence, a numbering
    refusal, a blocked work, and an error are six different claims; each
    keeps its own class, its own words, and a `data-state` where the DOM
    would otherwise carry the difference only in CSS.
    """

    def test_a_held_fragment_renders_its_text_and_its_apparatus(self):
        page = self.page("default")
        body = [one for one in page["fragmentTexts"] if one != "Loading…"]
        self.assertTrue(body, "opening a fragment must fetch and show its text")
        self.assertTrue(any(one.startswith("Extent — ") for one in page["fragmentBases"]))
        self.assertTrue(any("not collated" in one for one in page["states"]))

    def test_a_numbering_refusal_refuses_rather_than_guesses(self):
        page = self.page("numbering-refusal")
        self.assertIsNotNone(page["refusal"])
        self.assertTrue(page["refusal"].startswith("Boundary not established. "))
        self.assertIn("anchored in Vulgate numbering", page["refusal"])
        self.assertIn("will not guess where the boundary moves to", page["refusal"])
        self.assertIn("King James", page["refusal"])

    def test_a_fragment_that_crosses_a_chapter_boundary_says_so(self):
        page = self.page("default")
        self.assertTrue(page["spans"])
        self.assertEqual(set(page["spans"]), {"— runs across the chapter boundary"})

    def test_the_voice_chip_says_whose_the_language_is(self):
        page = self.page("default")
        self.assertIn("Latin — the author’s own", page["languages"])
        self.assertIn("English translation", page["languages"])
        self.assertIn("Latin translation", page["languages"])

    def test_held_and_not_renderable_keeps_its_own_heading_and_reason(self):
        """SYNTHETIC fixture: no tracked chapter carries a blocked row yet.

        The renderer ships anyway — the distinction between a work nobody
        acquired and a work held that cannot be shown is protected — and the
        real fixture is the generator's to supply.
        """
        page = self.page("held-unrenderable")
        self.assertIn("Held, and not renderable yet", page["sectionHeadings"])
        self.assertEqual(len(page["blocked"]), 1)
        self.assertIn("Anonymous — Catena in Genesim", page["blocked"][0])
        self.assertIn("held only as page images", page["blocked"][0])
        self.assertIn("Believed to comment here — the acquisition list",
                      page["sectionHeadings"])

    def test_each_state_carries_its_typed_attribute(self):
        self.assertIn("held", self.page("default")["dataStates"])
        self.assertIn("lead", self.page("default")["dataStates"])
        self.assertIn("absence", self.page("voice-held")["dataStates"])
        self.assertIn("refusal", self.page("numbering-refusal")["dataStates"])
        self.assertIn("blocked", self.page("held-unrenderable")["dataStates"])
        self.assertIn("error", self.page("integrity-404")["dataStates"])
        self.assertIn("error", self.page("invalid-book")["dataStates"])

    def test_each_state_keeps_a_class_of_its_own(self):
        seen: set[str] = set()
        for name in self.pages:
            page = self.page(name)
            for one in page["classes"]:
                seen |= set(one.split())
        for name in ("fragment", "lead", "blocked", "refusal", "absence-note",
                     "paragraph-note", "passage-paragraph", "projected", "spans",
                     "aside-note", "fragment-basis", "catena-error",
                     "fragment-acknowledgement", "chain-column"):
            with self.subTest(**{"class": name}):
                self.assertIn(name, seen)


class PayloadTest(ReplayTest):
    """What the composition costs a reader, and what it does not cost them."""

    def test_the_stylesheet_holds_the_recorded_ceiling(self):
        css = held(CATENA / "catena.css")
        self.assertLessEqual(gz(css), CSS_BUDGET_GZ, f"catena.css is {gz(css)} B gzipped")
        rules = gz(without_comments(css))
        self.assertLessEqual(rules, CSS_RULES_BUDGET_GZ,
                             f"the declarations alone are {rules} B gzipped")

    def test_the_script_holds_the_recorded_ceiling(self):
        script = held(CATENA / "catena.js")
        self.assertLessEqual(gz(script), JS_BUDGET_GZ, f"catena.js is {gz(script)} B gzipped")
        code = gz(without_comments(script, script=True))
        self.assertLessEqual(code, JS_CODE_BUDGET_GZ, f"the code alone is {code} B gzipped")

    def test_the_corrections_added_no_request_to_a_first_load(self):
        quiet = self.page("voice-held")["fetched"]
        self.assertEqual(quiet, [
            "structure/catena/index.json",
            "bibles.json",
            "structure/paragraphs/index.json",
            "structure/catena/01-gen/001.json",
            "douay-rheims/chapters/Gen/1.json",
            "structure/paragraphs/douay-rheims/01-gen/001.json",
        ])
        opened = self.page("default")["fetched"]
        self.assertEqual(len(opened), len(quiet) + 1)
        self.assertTrue(opened[-1].startswith("structure/catena/text/"))

    def test_an_invalid_address_costs_only_the_indexes(self):
        self.assertEqual(self.page("invalid-book")["fetched"], [
            "structure/catena/index.json",
            "bibles.json",
            "structure/paragraphs/index.json",
        ])


class FrozenContractTest(ReplayTest):
    """What this lane was not allowed to move, and did not."""

    def test_the_one_cross_entrance_link_still_points_where_it_did(self):
        script = held(CATENA / "catena.js")
        self.assertIn(
            "whole.href = '../sources/#passage=' + encodeURIComponent(fragment.id);", script)
        page = self.page("default")
        self.assertTrue(page["linkHref"].startswith("../sources/#passage=passage."))
        self.assertEqual(page["linkText"], "Open this passage in the Source Library")

    def test_the_catena_tree_still_reaches_exactly_one_other_entrance(self):
        hits = []
        for source in sorted(CATENA.glob("*.js")):
            hits += [(source.name, one)
                     for one in re.findall(r"\.href = '(\.\./[^']*)", held(source))]
        self.assertEqual(len(hits), 1, hits)

    def test_the_model_is_byte_identical(self):
        digest = hashlib.sha256((CATENA / "catena-model.js").read_bytes()).hexdigest()
        self.assertEqual(
            digest, MODEL_SHA256,
            "catena-model.js moved; it is UMD, DOM-free, replayed by `catena check`, "
            "and no part of this correction touches it")

    def test_the_model_names_no_part_of_a_document(self):
        source = without_comments(held(CATENA / "catena-model.js"), script=True)
        for name in ("document", "window", "HTMLElement", "querySelector"):
            with self.subTest(name=name):
                self.assertNotIn(name, source)

    def test_the_legacy_language_key_stays_unhonoured(self):
        # Pinned in full by test_browser_url_contract.py:537; restated here so
        # a correction to this file cannot quietly "fix" the old key.
        script = held(CATENA / "catena.js")
        self.assertNotIn("hash.get('language')", script)
        self.assertNotIn("next.get('language')", script)


if __name__ == "__main__":
    unittest.main()
