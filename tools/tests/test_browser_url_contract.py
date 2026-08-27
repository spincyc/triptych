#!/usr/bin/env python3
"""The published address of every browser instrument, written down as a test.

A URL this repository has published is a citation. Renaming a route once left
Catena Omnia answering 404 to links that were already in the wild, and the rule
that came out of it is that a published path is a promise. Nothing enforced it:
nine instruments each keep their own hash vocabulary — seven writing through the
shared router in `shared/browser-core.js`, two pushing history entries of their
own — and no test knew which keys any of them recognised, in which order they
were written, or which spellings were legacy. A cleanup of those routers could
rename `voice` back to `language`, drop `unit` from the Code, or start writing a
legacy alias back out, and every existing test would still pass while every
existing link broke.

This file is the record that makes that fail loudly. Per instrument it pins:
the exact set of recognised hash keys; the legacy aliases accepted as input and
never written back; the canonical hash each instrument emits; the two-sided
cross-instrument links, where the writer's emitted shape is asserted against the
reader's accepted shape so the two cannot drift apart on their own; and the
query parameters, with proof that they survive the instrument's own navigation.

WHERE THE ASSERTIONS COME FROM. Wherever a model can be replayed it is replayed:
`shared/browser-core.js` is loaded and run under node, and the hash-building
function of each page is lifted out of its file and executed on top of the real
router, so the canonical strings below are what the page actually emits rather
than what a regular expression thinks it emits. The node side is embedded in
this file rather than a sibling `.mjs` because the URL contract is one artifact
and splitting it would let half of it be edited without the other half.

Assertions that only read source text are marked WEAK where they occur. They
are the fallback for code that cannot be reached without a browser: top-level
page start-up, event wiring, and query-parameter reads.

The frozen v1 reader-state contract and its permanent legacy-URL inventory are
owned by `guidance/liturgy-reader-state.md`; this file checks the deployed pages
against it rather than restating it.
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
NODE = shutil.which("node")


# ---------------------------------------------------------------------------
# The contract itself, as an inventory. Everything below asserts against this.
# ---------------------------------------------------------------------------

# Every key each instrument reads out of the hash.
RECOGNISED_HASH_KEYS = {
  "catena/catena.js": ["bible", "book", "chapter", "voice"],
  "history/history.js": ["station", "unit"],
  "law/law.js": ["act", "canon", "line", "par", "unit"],
  "liturgy/day.js": [
    "bible", "date", "form", "mass", "missal", "orations", "ordinary", "ordinary-lang",
    "rubrics", "why",
  ],
  "liturgy/liturgy.js": ["bible", "mass", "missal", "orations", "type"],
  "scripture/plan.js": ["period", "reading", "tier"],
  "scripture/track.js": ["bible", "period", "reading", "tier"],
  "sources/sources.js": [
    "author", "category", "edition", "find", "language", "passage", "period",
    "readable", "rights", "sort",
  ],
  "texts/texts.js": ["author", "edition", "find", "reading", "section", "sort"],
}

# Every `T.writeHash([...])` an instrument makes, in the order its keys are
# emitted. A file whose call is built from a variable instead of a literal is
# listed in COMPUTED_HASH_WRITERS and pinned by replaying the function.
WRITTEN_HASH_KEYS = {
  "catena/catena.js": [["book", "chapter", "bible", "voice"]],
  "history/history.js": [["station", "unit"], ["station", "unit"]],
  "law/law.js": [["canon", "par", "line", "act"]],
  "liturgy/liturgy.js": [["missal", "type", "mass", "bible", "orations"]],
  "sources/sources.js": [
    ["edition", "passage"],
    ["author", "category", "language", "period", "rights", "readable", "find", "sort"],
  ],
  "texts/texts.js": [],
  "liturgy/day.js": [],
  "scripture/track.js": [],
}

COMPUTED_HASH_WRITERS = {
  "liturgy/day.js": ["pairs"],
  "scripture/track.js": ["hashPairs()"],
  # texts.js moved its literal into `const pairs` when the mainline
  # fragment-hygiene fix made the write conditional (an unnarrowed corpus
  # clears the fragment instead of writing nothing); the six keys are pinned
  # by test_the_texts_page_still_builds_its_six_pair_writer.
  "texts/texts.js": ["pairs"],
}

# Read as input, never written back out. This is the repository's rule about
# legacy spellings, and the half that matters is the "never written" half.
LEGACY_INPUT_ONLY_ALIASES = {
  # `#unit=<id>` is how another page hands the Code a base unit; the Code
  # answers in citations, so it writes `canon`/`par`/`line` and never `unit`.
  "law/law.js": ["unit"],
  # The Propers reader accepts the candidate spellings of the three semantic
  # selections and strips them from the hash the moment it navigates.
  "liturgy/propers-reader.js": [
    "_candidate-alternative", "_candidate-cycle", "_candidate-translation-witness",
  ],
}

# Query parameters, and the file that reads each one. `data` is read once, in
# the shared core, and therefore belongs to every page that loads it.
QUERY_PARAMETERS = {
  "data": "shared/browser-core.js",
  "plan": "scripture/plan-model.js",
  "slice": "law/law.js",
  "design": "liturgy/reader-visual-reset.js",
}

# The v1 legacy inventory frozen by `guidance/liturgy-reader-state.md`.
FROZEN_DAY_KEYS = [
  "date", "missal", "bible", "orations", "why", "ordinary", "ordinary-lang",
  "rubrics", "mass", "form", "translation-witness", "mode", "location",
]
FROZEN_DAY_VARIANT_KEYS = ["eucharistic-prayer"]
FROZEN_PROPERS_KEYS = [
  "missal", "type", "mass", "bible", "orations", "form", "cycle", "alternative",
  "translation-witness", "mode", "location",
]


# ---------------------------------------------------------------------------
# The node side: the real router, and the page functions run on top of it
# ---------------------------------------------------------------------------

NODE_HARNESS = r"""
'use strict';
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const REQUEST = JSON.parse(process.argv[process.argv.length - 1]);
const BROWSER = path.join(REQUEST.root, 'src/web/browser');

function source(file) {
  return fs.readFileSync(path.join(BROWSER, file), 'utf8');
}

/* A string- and comment-aware scanner. It is not a JavaScript parser, but it
 * will not mistake a brace inside a string or a comment for structure, which a
 * regular expression would. */
function scanTo(text, from, opens, closes) {
  let depth = 0;
  let i = from;
  let prev = '';
  while (i < text.length) {
    const ch = text[i];
    const two = text.slice(i, i + 2);
    if (two === '//') { i = text.indexOf('\n', i); if (i < 0) break; continue; }
    if (two === '/*') { i = text.indexOf('*/', i) + 2; continue; }
    if (ch === '"' || ch === "'" || ch === '`') {
      const quote = ch;
      i += 1;
      while (i < text.length) {
        if (text[i] === '\\') { i += 2; continue; }
        if (text[i] === quote) { i += 1; break; }
        i += 1;
      }
      prev = quote;
      continue;
    }
    if (ch === '/' && '(=,:[!&|?{};+'.includes(prev)) {
      i += 1;
      while (i < text.length) {
        if (text[i] === '\\') { i += 2; continue; }
        if (text[i] === '/') { i += 1; break; }
        i += 1;
      }
      continue;
    }
    if (ch === opens) depth += 1;
    else if (ch === closes) { depth -= 1; if (depth === 0) return i; }
    if (!/\s/.test(ch)) prev = ch;
    i += 1;
  }
  throw new Error('unterminated region');
}

function extractFunction(text, name) {
  const start = text.indexOf('function ' + name + '(');
  if (start < 0) throw new Error('no function named ' + name);
  return text.slice(start, scanTo(text, text.indexOf('{', start), '{', '}') + 1);
}

/** Every argument list of `T.writeHash(...)` in a file, as source text. */
function writeHashArguments(text) {
  const out = [];
  let at = 0;
  for (;;) {
    const found = text.indexOf('T.writeHash(', at);
    if (found < 0) return out;
    const open = found + 'T.writeHash('.length - 1;
    const close = scanTo(text, open, '(', ')');
    out.push(text.slice(open + 1, close).trim());
    at = close;
  }
}

/** The right-hand side of the assignment whose left side is `anchor`. */
function assignedExpression(text, anchor) {
  const found = text.indexOf(anchor);
  if (found < 0) throw new Error('no assignment to ' + anchor);
  let i = found + anchor.length;
  while (i < text.length) {
    const ch = text[i];
    const two = text.slice(i, i + 2);
    if (two === '//') { i = text.indexOf('\n', i); continue; }
    if (two === '/*') { i = text.indexOf('*/', i) + 2; continue; }
    if (ch === '"' || ch === "'" || ch === '`') {
      const quote = ch;
      i += 1;
      while (i < text.length) {
        if (text[i] === '\\') { i += 2; continue; }
        if (text[i] === quote) { i += 1; break; }
        i += 1;
      }
      continue;
    }
    if (ch === '(' || ch === '[' || ch === '{') {
      i = scanTo(text, i, ch, { '(': ')', '[': ']', '{': '}' }[ch]) + 1;
      continue;
    }
    if (ch === ';') return text.slice(found + anchor.length, i).trim();
    i += 1;
  }
  throw new Error('unterminated assignment to ' + anchor);
}

/* A scope in which every name the test did not bind is a harmless recording
 * stub, so a fragment of a page can be run without the page around it. */
function stub(name) {
  const target = function () { return stub(name + '()'); };
  return new Proxy(target, {
    get(t, k) {
      if (k === Symbol.toPrimitive) return () => '<' + name + '>';
      if (k === 'then' || typeof k === 'symbol') return undefined;
      return stub(name + '.' + String(k));
    },
    set() { return true; },
    apply() { return stub(name + '()'); },
    has() { return true; }
  });
}

function permissiveObject(real, name) {
  return new Proxy(real, {
    has() { return true; },
    get(t, k) {
      if (k in t) return t[k];
      if (typeof k === 'symbol') return undefined;
      return stub(name + '.' + String(k));
    },
    set(t, k, v) { t[k] = v; return true; }
  });
}

function permissiveScope(bindings) {
  return new Proxy(bindings, {
    has() { return true; },
    get(t, k) {
      if (k === Symbol.unscopables) return undefined;
      if (k in t) return t[k];
      if (typeof k === 'string' && k in globalThis) return globalThis[k];
      return stub(String(k));
    },
    set(t, k, v) { t[k] = v; return true; }
  });
}

/** The shared router, loaded and running against a stub window. */
function loadCore(state) {
  const pathname = state.pathname || '/liturgy/day.html';
  const location = {
    search: state.search || '',
    hash: state.hash || '',
    pathname: pathname,
    href: 'https://example.invalid' + pathname
  };
  const listeners = {};
  const documentListeners = {};
  const window = permissiveObject({
    location: location,
    addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); }
  }, 'window');
  const element = () => permissiveObject({
    style: {}, dataset: {},
    setAttribute() {}, appendChild() {}, addEventListener() {},
    classList: { add() {}, remove() {}, toggle() {} }
  }, 'element');
  const document = permissiveObject({
    addEventListener(type, fn) {
      (documentListeners[type] = documentListeners[type] || []).push(fn);
    },
    createElement: element,
    createTextNode: () => element(),
    getElementById: () => null,
    querySelector: () => null,
    querySelectorAll: () => [],
    body: permissiveObject({ classList: { toggle() {} } }, 'body')
  }, 'document');
  const context = vm.createContext({
    window, document, console, URLSearchParams, URL,
    setTimeout, clearTimeout, queueMicrotask, Promise, JSON, Math, Date,
    fetch: async () => { throw new Error('the harness serves no network'); }
  });
  vm.runInContext(source('shared/browser-core.js'), context, { filename: 'browser-core.js' });
  return { T: context.window.Triptych, window, document, location, listeners, documentListeners };
}

const PROBES = {
  /** The shared router, executed. */
  core(request) {
    const core = loadCore(request);
    const observed = [];
    const stepped = [];
    if (request.observe) core.T.onHashChange((params) => observed.push(params.toString()));
    if (request.arrows) core.T.onArrowStep((delta) => stepped.push(delta));
    for (const write of request.writes || []) core.T.writeHash(write);
    for (const event of request.keys || []) {
      for (const fn of core.documentListeners.keydown || []) {
        fn(Object.assign({ target: null }, event));
      }
    }
    for (const set of request.setHash || []) {
      core.location.hash = set;
      for (const fn of core.listeners.hashchange || []) fn();
    }
    return {
      dataRoot: core.T.dataRoot,
      hash: core.location.hash,
      search: core.location.search,
      read: Object.fromEntries(core.T.readHash().entries()),
      observed, stepped,
      documentEvents: Object.keys(core.documentListeners)
    };
  },

  /** Every literal `T.writeHash([...])` in a file, as the keys it emits. */
  writtenKeys(request) {
    const text = source(request.file);
    const literal = [];
    const computed = [];
    for (const argument of writeHashArguments(text)) {
      if (argument[0] !== '[') { computed.push(argument); continue; }
      const pairs = new Function('scope', 'with (scope) { return ' + argument + '; }')(
        permissiveScope({})
      );
      literal.push(pairs.map((pair) => pair[0]));
    }
    return { literal, computed };
  },

  /** Run named functions out of a page, with the real router beneath them. */
  replay(request) {
    const core = loadCore(request);
    const text = source(request.file);
    const pushed = [];
    const replaced = [];
    const bindings = Object.assign({
      window: core.window,
      document: core.document,
      T: core.T,
      Contract: require(path.join(BROWSER, 'liturgy/reader-state.js')),
      readerShell: { captureSemanticLocation() { return null; } },
      runtime: {},
      URLSearchParams: URLSearchParams,
      history: {
        pushState(state, title, url) { pushed.push(url); },
        replaceState(state, title, url) { replaced.push(url); }
      }
    }, request.bindings || {});
    const names = request.extract || [];
    const api = new Function('scope', 'with (scope) {\n' +
      names.map((name) => extractFunction(text, name)).join('\n') +
      '\nreturn { ' + names.join(', ') + ' };\n}')(permissiveScope(bindings));
    const returned = api[request.call].apply(null, request.args || []);
    return {
      returned: returned === undefined ? null : JSON.parse(JSON.stringify(returned)),
      hash: core.location.hash,
      search: core.location.search,
      pushed, replaced
    };
  },

  /** Evaluate one assignment's right-hand side against the test's own data. */
  assigned(request) {
    const expression = assignedExpression(source(request.file), request.anchor);
    const value = new Function('scope', 'with (scope) { return (' + expression + '); }')(
      permissiveScope(request.bindings || {})
    );
    return { expression, value };
  },

  /** One function's source text, for the assertions that must read it. */
  functionSource(request) {
    return { text: extractFunction(source(request.file), request.name) };
  },

  /** The frozen reader-state contract, required as the module it is. */
  parseLegacy(request) {
    const contract = require(path.join(BROWSER, 'liturgy/reader-state.js'));
    const parsed = contract.parseLegacy(request.entrance, request.hash, request.options || {});
    return {
      recognized: parsed.recognized,
      present: parsed.present,
      unknown: parsed.unknown.map((row) => row.key),
      duplicates: parsed.duplicates.map((row) => row.key)
    };
  },

  /** The exact public inventories exported by the reader-state contract. */
  urlInventory() {
    const contract = require(path.join(BROWSER, 'liturgy/reader-state.js'));
    return contract.URL_INVENTORY;
  }
};

process.stdout.write(JSON.stringify(PROBES[REQUEST.probe](REQUEST)));
"""


_PROBE_CACHE: dict[str, dict] = {}


def probe(**request) -> dict:
  """Run one node probe and return its JSON answer."""
  request["root"] = str(ROOT)
  payload = json.dumps(request, sort_keys=True)
  if payload not in _PROBE_CACHE:
    result = subprocess.run(
      [NODE, "-e", NODE_HARNESS, payload],
      cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
      raise AssertionError(
        "the URL harness could not run " + request["probe"] + ":\n" + result.stderr.strip()
      )
    _PROBE_CACHE[payload] = json.loads(result.stdout)
  return _PROBE_CACHE[payload]


def text_of(relative: str) -> str:
  return (BROWSER / relative).read_text(encoding="utf-8")


# The receivers a page gives a parsed hash. `T.params` and the several spellings
# of `location.search` are deliberately not among them: those are query reads.
HASH_READ = re.compile(r"\b(?:hash|next|state|arriving)\.get\('([^']+)'\)")


def hash_keys_read_by(relative: str) -> list[str]:
  return sorted(set(HASH_READ.findall(text_of(relative))))


needs_node = unittest.skipIf(NODE is None, "node is not installed; the URL models cannot be run")


# ---------------------------------------------------------------------------


@needs_node
class SharedHashRouterTest(unittest.TestCase):
  """`shared/browser-core.js`, executed. Seven instruments write through this.

  Everything else in this file about a canonical hash is downstream of these
  four rules, so they are pinned first and by running the real thing.
  """

  def test_a_written_hash_keeps_its_order_and_percent_encodes_its_values(self):
    answer = probe(probe="core", writes=[[["book", "Gen"], ["chapter", "1"]]])
    self.assertEqual(answer["hash"], "#book=Gen&chapter=1")
    answer = probe(probe="core", writes=[[["find", "de ciuitate/dei &c"]]])
    # encodeURIComponent, so a space is %20. The two `history.pushState` readers
    # encode with URLSearchParams instead and spell the same space `+`; the two
    # spellings are pinned apart in ReaderShellHashTest.
    self.assertEqual(answer["hash"], "#find=de%20ciuitate%2Fdei%20%26c")
    self.assertEqual(answer["read"], {"find": "de ciuitate/dei &c"})

  def test_an_empty_value_is_left_out_rather_than_written_bare(self):
    answer = probe(probe="core", writes=[[["a", "1"], ["b", ""], ["c", None], ["d", "2"]]])
    self.assertEqual(answer["hash"], "#a=1&d=2")

  def test_a_write_whose_every_value_is_empty_clears_the_old_hash(self):
    """Clearing all state cannot leave an obsolete selection in the URL."""
    answer = probe(
      probe="core", hash="#edition=migne-pl-32&passage=conf%2F1",
      writes=[[["author", ""], ["sort", ""]]],
    )
    self.assertEqual(answer["hash"], "")

  def test_the_router_does_not_replay_its_own_write_to_the_page(self):
    answer = probe(
      probe="core", observe=True,
      writes=[[["book", "Gen"]]],
      setHash=["#book=Gen", "#book=Ex"],
    )
    # The self-written hash is recognised by its text, so only the reader's own
    # navigation reaches the handler.
    self.assertEqual(answer["observed"], ["book=Ex"])

  def test_writing_the_hash_never_disturbs_the_query(self):
    answer = probe(probe="core", search="?data=fixture", writes=[[["book", "Gen"]]])
    self.assertEqual(answer["search"], "?data=fixture")

  def test_the_data_root_is_resolved_from_the_query(self):
    self.assertEqual(probe(probe="core")["dataRoot"], "../browse")
    self.assertEqual(probe(probe="core", search="?data=fixture")["dataRoot"], "../fixture")
    self.assertEqual(probe(probe="core", search="?data=/corpus/")["dataRoot"], "/corpus")


class RecognisedHashKeysTest(unittest.TestCase):
  """The exact set of keys each instrument reads. Removing or renaming one fails.

  WEAK: derived from the source text, because these reads sit inside page
  start-up that cannot run without a browser. The extraction is keyed on the
  receiver a parsed hash is given, not on any single literal, so a rename is
  caught wherever in the file it happens.
  """

  def test_every_instrument_reads_exactly_the_keys_it_published(self):
    for relative, keys in sorted(RECOGNISED_HASH_KEYS.items()):
      with self.subTest(instrument=relative):
        self.assertEqual(hash_keys_read_by(relative), keys)

  def test_catena_does_not_honour_the_language_key_it_replaced(self):
    """`voice` replaced `language`, and the old key is deliberately not read.

    An old `language=en` link opens on everything held rather than on a guess,
    which is a decision recorded in the file. Accepting `language` again would
    be a silent reinterpretation of links already in the wild.
    """
    self.assertNotIn("language", hash_keys_read_by("catena/catena.js"))

  def test_the_day_page_also_reads_the_variant_group_keys_its_manifest_declares(self):
    # WEAK: the key is the group's own id, so there is no literal to pin. What
    # is pinned is that the lookup is still driven by the manifest.
    self.assertIn("const wanted = hash.get(group);", text_of("liturgy/day.js"))


@needs_node
class WrittenHashKeysTest(unittest.TestCase):
  """The keys each instrument writes, evaluated rather than matched.

  The argument of every `T.writeHash([...])` is executed, so a key renamed
  inside any expression is caught, and a call that stops being a literal is
  reported rather than quietly skipped.
  """

  def test_every_instrument_writes_exactly_the_keys_it_published(self):
    for relative, calls in sorted(WRITTEN_HASH_KEYS.items()):
      with self.subTest(instrument=relative):
        answer = probe(probe="writtenKeys", file=relative)
        self.assertEqual(answer["literal"], calls)
        self.assertEqual(answer["computed"], COMPUTED_HASH_WRITERS.get(relative, []))

  def test_the_texts_page_still_builds_its_six_pair_writer(self):
    """The pinned keys survived the literal's move into `const pairs`.

    WEAK: derived from the source text, like RecognisedHashKeysTest, because
    the pair list now feeds a conditional write and no longer appears as a
    `T.writeHash([...])` literal the probe can evaluate.
    """
    import re
    literal = re.search(r"const pairs = \[(.*?)\n    \];", text_of("texts/texts.js"), re.S)
    self.assertIsNotNone(literal, "texts.js no longer builds its `pairs` list")
    self.assertEqual(
      re.findall(r"\['([a-z]+)',", literal.group(1)),
      ["author", "edition", "section", "reading", "sort", "find"],
    )


@needs_node
class CanonicalHashFormTest(unittest.TestCase):
  """The exact hash each instrument emits, produced by replaying its own model.

  Each page's hash-building function is lifted out of its file and run on top of
  the real shared router, so these strings are the ones a reader would copy out
  of the address bar.
  """

  def test_catena_writes_book_chapter_bible_and_voice_in_that_order(self):
    answer = probe(probe="writtenKeys", file="catena/catena.js")
    self.assertEqual(answer["literal"][0], ["book", "chapter", "bible", "voice"])

  def test_the_track_writes_a_reading_or_a_period_but_never_both(self):
    state = {
      "tier": "wide", "view": "reading", "readingKey": "r-014",
      "periodKey": "exodus", "bibleId": "douay-rheims",
    }
    reading = probe(
      probe="replay", file="scripture/track.js", extract=["hashPairs", "href"],
      call="href", args=[None], bindings={"state": state},
    )
    self.assertEqual(reading["returned"], "#tier=wide&reading=r-014&bible=douay-rheims")
    period = probe(
      probe="replay", file="scripture/track.js", extract=["hashPairs", "href"],
      call="href", args=[{"view": "period"}], bindings={"state": state},
    )
    self.assertEqual(period["returned"], "#tier=wide&period=exodus&bible=douay-rheims")
    orient = probe(
      probe="replay", file="scripture/track.js", extract=["hashPairs", "href"],
      call="href", args=[{"view": "orient"}], bindings={"state": state},
    )
    self.assertEqual(orient["returned"], "#tier=wide&bible=douay-rheims")

  def test_the_source_library_writes_an_edition_and_passage_while_reading(self):
    answer = probe(
      probe="replay", file="sources/sources.js", extract=["writeHash"], call="writeHash",
      bindings={
        "open": {
          "edition": {"id": "migne-pl-32"}, "at": 1,
          "payload": {"passages": [{"id": "conf/1"}, {"id": "conf/2"}]},
        },
        "state": {},
      },
    )
    self.assertEqual(answer["hash"], "#edition=migne-pl-32&passage=conf%2F2")

  def test_the_source_library_writes_its_finder_state_and_drops_the_default_sort(self):
    answer = probe(
      probe="replay", file="sources/sources.js", extract=["writeHash"], call="writeHash",
      bindings={
        "open": None,
        "state": {
          "author": "augustinus", "category": "", "language": "la", "period": "",
          "rights": "", "readable": True, "find": "de ciuitate", "sort": "author",
        },
      },
    )
    self.assertEqual(
      answer["hash"],
      "#author=augustinus&language=la&readable=1&find=de%20ciuitate",
    )

  def test_the_code_writes_a_citation_and_the_act_but_never_the_unit(self):
    answer = probe(
      probe="replay", file="law/law.js", extract=["writeState"], call="writeState",
      bindings={
        "opened": {"canon": "1095", "asked": "2", "line": "latin"},
        "openedStation": "act-1983",
      },
    )
    self.assertEqual(answer["hash"], "#canon=1095&par=2&line=latin&act=act-1983")

  def test_the_propers_page_drops_the_orations_key_at_its_default(self):
    base = {
      "missalId": "roman-1962", "kind": "seasonal", "massKey": "adv-1", "bibleId": "dr",
    }
    default = probe(
      probe="replay", file="liturgy/liturgy.js", extract=["writeHash"], call="writeHash",
      bindings={"state": dict(base, orations="la")},
    )
    self.assertEqual(default["hash"], "#missal=roman-1962&type=seasonal&mass=adv-1&bible=dr")
    chosen = probe(
      probe="replay", file="liturgy/liturgy.js", extract=["writeHash"], call="writeHash",
      bindings={"state": dict(base, orations="en")},
    )
    self.assertEqual(
      chosen["hash"],
      "#missal=roman-1962&type=seasonal&mass=adv-1&bible=dr&orations=en",
    )

  def test_the_day_page_writes_its_ten_keys_then_its_variants_in_key_order(self):
    answer = probe(
      probe="replay", file="liturgy/day.js", extract=["writeHash"], call="writeHash",
      bindings={"state": {
        "date": "2026-08-08", "missalId": "roman-1962", "bibleId": "dr", "orations": "en",
        "why": True, "ordinary": True, "ordinaryLang": "la", "showRubrics": False,
        "shownMass": "vigil", "shownForm": "longer",
        "variants": {"eucharistic-prayer": "ep2", "a-group": "x"},
      }},
    )
    self.assertEqual(answer["hash"], (
      "#date=2026-08-08&missal=roman-1962&bible=dr&orations=en&why=1&ordinary=1"
      "&ordinary-lang=la&rubrics=0&mass=vigil&form=longer"
      "&a-group=x&eucharistic-prayer=ep2"
    ))

  def test_the_day_page_omits_every_departure_it_has_not_taken(self):
    answer = probe(
      probe="replay", file="liturgy/day.js", extract=["writeHash"], call="writeHash",
      bindings={"state": {
        "date": "2026-08-08", "missalId": "roman-1962", "bibleId": "dr", "orations": "la",
        "why": False, "ordinary": False, "ordinaryLang": None, "showRubrics": True,
        "shownMass": None, "shownForm": None, "variants": {},
      }},
    )
    self.assertEqual(answer["hash"], "#date=2026-08-08&missal=roman-1962&bible=dr")


@needs_node
class ReaderShellHashTest(unittest.TestCase):
  """The two `history.pushState` instruments, which do not use the shared router.

  Their recognised keys are the frozen v1 inventory, and their canonical form is
  `URLSearchParams.toString()` over the hash already in the address bar.
  """

  def test_the_day_reader_recognises_the_frozen_day_keys_and_its_declared_variants(self):
    hash_ = "#" + "&".join(
      [key + "=v" for key in FROZEN_DAY_KEYS + FROZEN_DAY_VARIANT_KEYS] + ["language=en"]
    )
    answer = probe(
      probe="parseLegacy", entrance="day", hash=hash_,
      options={"variantKeys": FROZEN_DAY_VARIANT_KEYS},
    )
    self.assertEqual(answer["present"], FROZEN_DAY_KEYS + FROZEN_DAY_VARIANT_KEYS)
    self.assertEqual(answer["unknown"], ["language"])

  def test_the_propers_reader_recognises_the_frozen_propers_keys(self):
    hash_ = "#" + "&".join([key + "=v" for key in FROZEN_PROPERS_KEYS] + ["date=2026-08-08"])
    answer = probe(probe="parseLegacy", entrance="propers", hash=hash_)
    self.assertEqual(answer["present"], FROZEN_PROPERS_KEYS)
    # Propers is calendar independent, so a civil date is not one of its keys.
    self.assertEqual(answer["unknown"], ["date"])

  def test_a_repeated_semantic_key_is_reported_rather_than_resolved(self):
    answer = probe(probe="parseLegacy", entrance="propers", hash="#missal=a&missal=b")
    self.assertEqual(answer["duplicates"], ["missal"])

  def test_both_readers_edit_the_hash_in_place_and_keep_the_rest_of_it(self):
    for relative, name in (
      ("liturgy/day-reader.js", "hashWith"),
      ("liturgy/propers-reader.js", "internalHash"),
    ):
      with self.subTest(instrument=relative):
        answer = probe(
          probe="replay", file=relative, extract=[name], call=name,
          hash="#date=2026-08-08&missal=roman-1962&mass=vigil",
          args=[{"bible": "dr", "mass": None}, ["missal"]],
        )
        self.assertEqual(answer["returned"], "#date=2026-08-08&bible=dr")

  def test_a_hash_emptied_by_a_navigation_loses_its_marker_entirely(self):
    answer = probe(
      probe="replay", file="liturgy/day-reader.js", extract=["hashWith"], call="hashWith",
      hash="#mass=vigil", args=[{}, ["mass"]],
    )
    self.assertEqual(answer["returned"], "")

  def test_the_reader_shells_spell_a_space_the_URLSearchParams_way(self):
    answer = probe(
      probe="replay", file="liturgy/day-reader.js", extract=["hashWith"], call="hashWith",
      hash="", args=[{"mass": "in nocte"}, []],
    )
    # `+`, not `%20`: this is a real difference from the shared router above and
    # a cleanup that unified the two would change published addresses.
    self.assertEqual(answer["returned"], "#mass=in+nocte")


@needs_node
class LegacyAliasTest(unittest.TestCase):
  """Legacy spellings are read and never written. Both halves are asserted."""

  def test_the_code_accepts_a_unit_id_as_input(self):
    answer = probe(
      probe="replay", file="law/law.js", extract=["fromHash"], call="fromHash",
      hash="#unit=can-1095-2&line=latin",
    )
    self.assertEqual(answer["returned"]["unit"], "can-1095-2")
    self.assertEqual(answer["returned"]["line"], "latin")

  def test_the_code_never_writes_a_unit_back_out(self):
    for opened in (
      {"canon": "1095", "asked": "2", "line": "latin"},
      None,
    ):
      with self.subTest(opened=opened):
        answer = probe(
          probe="replay", file="law/law.js", extract=["writeState"], call="writeState",
          bindings={"opened": opened, "openedStation": None},
        )
        self.assertNotIn("unit=", answer["hash"])

  def test_every_recorded_input_only_alias_is_read_and_none_is_written(self):
    for relative, aliases in sorted(LEGACY_INPUT_ONLY_ALIASES.items()):
      source = text_of(relative)
      written = probe(probe="writtenKeys", file=relative)
      emitted = {key for call in written["literal"] for key in call}
      for alias in aliases:
        with self.subTest(instrument=relative, alias=alias):
          # WEAK on the reading half for the Propers reader: the alias is looked
          # up through a table, so there is no `get('...')` literal to execute.
          self.assertIn(alias, source, "the alias must still be accepted as input")
          self.assertNotIn(alias, emitted, "a legacy alias is never written back")

  def test_the_candidate_aliases_are_spelled_out_once_and_only_in_their_table(self):
    """One spelling, in `LEGACY_KEYS`, so no other site can emit one by hand.

    WEAK: a count of literals. It is here because the Propers reader has no
    `T.writeHash` call for WrittenHashKeysTest to execute, so the "never
    written" half needs holding some other way.
    """
    source = text_of("liturgy/propers-reader.js")
    for alias in LEGACY_INPUT_ONLY_ALIASES["liturgy/propers-reader.js"]:
      with self.subTest(alias=alias):
        self.assertEqual(source.count("'" + alias + "'"), 1)

  def test_the_propers_reader_strips_its_candidate_aliases_when_it_navigates(self):
    """The alias is removed on the way out, which is what "input only" means."""
    submit = probe(
      probe="functionSource", file="liturgy/propers-reader.js", name="internalHash",
    )
    self.assertIn("params.delete(key)", submit["text"])
    answer = probe(
      probe="replay", file="liturgy/propers-reader.js",
      extract=["internalHash"], call="internalHash",
      hash="#missal=roman-1962&_candidate-cycle=a&cycle=b",
      args=[{"cycle": "a"}, ["_candidate-cycle", "_candidate-alternative"]],
    )
    self.assertEqual(answer["returned"], "#missal=roman-1962&cycle=a")

  def test_the_reading_plan_forwards_the_single_page_readers_old_addresses(self):
    """`#tier`, `#reading` and `#period` at the entrance mean the track page.

    WEAK on the trigger: it is top-level start-up code, so the keys are read out
    of the source. The forwarded target is evaluated, and the assertion below
    ties the trigger keys to the keys the track page actually accepts.
    """
    triggers = hash_keys_read_by("scripture/plan.js")
    self.assertEqual(triggers, ["period", "reading", "tier"])
    self.assertLessEqual(set(triggers), set(hash_keys_read_by("scripture/track.js")))
    self.assertIn("window.location.replace(trackHref(window.location.hash));",
                  text_of("scripture/plan.js"))
    forwarded = probe(
      probe="replay", file="scripture/plan.js", extract=["trackHref"], call="trackHref",
      args=["#tier=wide&reading=r-014&bible=dr"],
      bindings={"SEARCH": "?data=fixture&plan=narrative-spine"},
    )
    self.assertEqual(forwarded["returned"], (
      "track.html?data=fixture&plan=narrative-spine#tier=wide&reading=r-014&bible=dr"
    ))


@needs_node
class CrossInstrumentLinkTest(unittest.TestCase):
  """Documented links between instruments, asserted from both ends at once.

  The writer's emitted URL and the reader's accepted key are checked against
  each other rather than each against a constant, so neither end can be changed
  on its own without this failing.
  """

  def test_catena_links_a_fragment_to_the_passage_the_source_library_opens(self):
    fragment = "basil/hexaemeron/hom 1 §2&3"
    written = probe(
      probe="assigned", file="catena/catena.js", anchor="whole.href =",
      bindings={"fragment": {"id": fragment}},
    )
    url = written["value"]
    self.assertTrue(url.startswith("../sources/#"), url)

    # The writer's half: an id, encoded, under one key.
    self.assertEqual(
      url, "../sources/#passage=basil%2Fhexaemeron%2Fhom%201%20%C2%A72%263"
    )

    # The reader's half, run through the real router the Source Library uses.
    arriving = probe(probe="core", hash=url[len("../sources/"):])["read"]
    self.assertEqual(list(arriving), ["passage"])
    self.assertEqual(arriving["passage"], fragment)

    # And the two ends tied together: the key Catena emits must be one the
    # Source Library reads, and one it writes back when the passage opens.
    emitted = set(arriving)
    self.assertLessEqual(emitted, set(hash_keys_read_by("sources/sources.js")))
    reader_side = probe(probe="writtenKeys", file="sources/sources.js")["literal"][0]
    self.assertLessEqual(emitted, set(reader_side))

  def test_the_source_library_re_emits_the_passage_it_was_sent_to(self):
    """Following the link and then stepping must not lose the deep link's key."""
    answer = probe(
      probe="replay", file="sources/sources.js", extract=["writeHash"], call="writeHash",
      hash="#passage=conf%2F1",
      bindings={
        "open": {
          "edition": {"id": "migne-pl-32"}, "at": 0,
          "payload": {"passages": [{"id": "conf/1"}]},
        },
        "state": {},
      },
    )
    self.assertEqual(answer["hash"], "#edition=migne-pl-32&passage=conf%2F1")

  def test_the_only_cross_entrance_deep_link_in_the_browser_is_that_one(self):
    """A second one would need its own two-sided test; this catches its arrival.

    WEAK: a source scan. It exists so that a new deep link cannot be added
    without either this failing or a contract being written for it.
    """
    found = []
    for script in sorted(BROWSER.rglob("*.js")):
      if "prototypes" in script.parts:
        continue
      for line in script.read_text(encoding="utf-8").splitlines():
        if re.search(r"""\.href\s*=\s*['"]\.\./""", line):
          found.append((script.relative_to(BROWSER).as_posix(), line.strip()))
    self.assertEqual(len(found), 1, found)
    self.assertEqual(found[0][0], "catena/catena.js")


@needs_node
class QueryParameterTest(unittest.TestCase):
  """`?data=`, `?plan=`, `?slice=`, `?missals=`, `?design=`, and their survival."""

  def test_every_query_parameter_is_still_read_where_it_was_published(self):
    # WEAK: query reads happen at page start-up, which cannot run headless. The
    # pattern insists the read comes off the search string, not off the hash.
    readers = {
      "data": r"PARAMS\.get\('data'\)",
      "plan": r"T\.params\.get\('plan'\)",
      "slice": r"new URLSearchParams\(window\.location\.search\)\.get\('slice'\)",
      "design": r"new URL\(window\.location\.href\)\.searchParams\.get\('design'\)",
    }
    for key, relative in sorted(QUERY_PARAMETERS.items()):
      with self.subTest(parameter=key):
        self.assertRegex(text_of(relative), readers[key])

  def test_the_slice_parameter_is_read_by_both_act_history_instruments(self):
    for relative in ("history/history.js", "law/law.js"):
      with self.subTest(instrument=relative):
        self.assertIn("new URLSearchParams(window.location.search).get('slice')",
                      text_of(relative))

  def test_the_missals_parameter_is_read_by_both_propers_instruments(self):
    for relative in ("liturgy/liturgy.js", "liturgy/propers-reader.js"):
      with self.subTest(instrument=relative):
        self.assertIn("T.params.get('missals')", text_of(relative))

  def test_the_query_survives_the_crossing_from_the_plan_to_a_track(self):
    answer = probe(
      probe="replay", file="scripture/plan.js", extract=["trackHref"], call="trackHref",
      args=["#tier=wide"], bindings={"SEARCH": "?data=fixture&plan=narrative-spine"},
    )
    self.assertEqual(answer["returned"],
                     "track.html?data=fixture&plan=narrative-spine#tier=wide")

  def test_the_query_survives_the_crossing_back_from_a_track_to_the_plan(self):
    answer = probe(
      probe="assigned", file="scripture/track.js", anchor="planLink.href =",
      bindings={"window": {"location": {"search": "?data=fixture&plan=narrative-spine"}}},
    )
    self.assertEqual(answer["value"], "./?data=fixture&plan=narrative-spine")

  def test_the_query_survives_every_push_the_two_reader_shells_make(self):
    for relative, functions, page, expected_page in (
      ("liturgy/day-reader.js", ["hashWith", "navigate"],
       "/liturgy/day.html", "/liturgy/day.html"),
      ("liturgy/propers-reader.js", ["internalHash", "eventLocation", "navigate"],
       "/liturgy/propers-reader.html", "/liturgy/index.html"),
    ):
      with self.subTest(instrument=relative):
        answer = probe(
          probe="replay", file=relative, extract=functions,
          call="navigate", args=[{"bible": "dr"}, []],
          hash="#missal=roman-1962", search="?data=fixture", pathname=page,
        )
        self.assertEqual(
          answer["pushed"],
          [expected_page + "?data=fixture#missal=roman-1962&bible=dr"],
        )


class FrozenInventoryTest(unittest.TestCase):
  """The deployed pages against the inventory `liturgy-reader-state.md` freezes.

  The guide owns the contract; this checks that the pages and the guide still
  agree, so a page cannot drift away from a document that says it is frozen.
  """

  @classmethod
  def setUpClass(cls) -> None:
    cls.guidance = (ROOT / "guidance/liturgy-reader-state.md").read_text(encoding="utf-8")

  def rows(self) -> dict[str, tuple[list[str], list[str]]]:
    found = {}
    for line in self.guidance.splitlines():
      match = re.match(r"\|\s*(Day|Propers)\s*\|(.*)\|(.*)\|\s*$", line)
      if match:
        found[match.group(1)] = (
          re.findall(r"`([^`]+)`", match.group(2)),
          re.findall(r"`([^`]+)`", match.group(3)),
        )
    return found

  def test_the_guide_still_carries_the_legacy_url_inventory(self):
    rows = self.rows()
    self.assertEqual(sorted(rows), ["Day", "Propers"])
    self.assertEqual(rows["Day"][0], FROZEN_DAY_KEYS + FROZEN_DAY_VARIANT_KEYS)
    self.assertEqual(rows["Day"][1], ["data"])
    self.assertEqual(rows["Propers"][0], FROZEN_PROPERS_KEYS)
    self.assertEqual(rows["Propers"][1], ["data", "missals"])

  @needs_node
  def test_the_reader_state_module_exports_exactly_the_frozen_inventory(self):
    inventory = probe(probe="urlInventory")
    self.assertEqual(inventory["day"]["hash"], FROZEN_DAY_KEYS + FROZEN_DAY_VARIANT_KEYS)
    self.assertEqual(inventory["day"]["query"], ["data"])
    self.assertEqual(inventory["propers"]["hash"], FROZEN_PROPERS_KEYS)
    self.assertEqual(inventory["propers"]["query"], ["data", "missals"])

  def test_the_deployed_day_page_reads_the_frozen_day_keys(self):
    # `day.js` owns the retained Day vocabulary. Mode, semantic location, and
    # the formulary-scoped witness are owned by the reader-state controller.
    controller_keys = {"mode", "location", "translation-witness"}
    self.assertEqual(
      hash_keys_read_by("liturgy/day.js"),
      sorted(set(FROZEN_DAY_KEYS) - controller_keys),
    )

  def test_both_canonical_pages_load_the_contract_and_their_reader_controller(self):
    for page, controller in (("day.html", "day-reader.js"), ("index.html", "propers-reader.js")):
      with self.subTest(page=page):
        source = text_of("liturgy/" + page)
        scripts = re.findall(r'<script src="([^"]+)"></script>', source)
        self.assertIn("reader-state.js", scripts)
        self.assertIn("reader-state-adapters.js", scripts)
        self.assertIn(controller, scripts)
        self.assertLess(scripts.index("reader-state.js"), scripts.index(controller))
        self.assertLess(scripts.index("reader-state-adapters.js"), scripts.index(controller))


@needs_node
class KnownDefectsTest(unittest.TestCase):
  """Defects found while deriving the contract, recorded rather than fixed.

  These tests pass because the defect is present. Each one names what a fix
  would change, so whoever fixes it deletes the test deliberately.
  """

  def test_the_document_corpus_rewrites_the_hash_on_every_keystroke(self):
    """CONFIRMED. `texts/texts.js` binds `input`, and `render` ends by writing.

    `T.writeHash` assigns `window.location.hash`, and assigning a new fragment
    pushes a history entry, so typing a six-letter search leaves six entries in
    the reader's Back button. A fix would debounce the write, or write through
    `history.replaceState` while the field has focus.

    WEAK on the binding: `findInput.addEventListener('input', render)` is
    top-level wiring. The two halves either side of it are executed.
    """
    source = text_of("texts/texts.js")
    self.assertIn("findInput.addEventListener('input', render);", source)
    render = probe(probe="functionSource", file="texts/texts.js", name="render")
    self.assertIn("T.writeHash(", render["text"])
    # Executed: each distinct write is an assignment to location.hash.
    typed = probe(probe="core", writes=[
      [["find", "d"]], [["find", "de"]], [["find", "de "]], [["find", "de c"]],
    ])
    self.assertEqual(typed["hash"], "#find=de%20c")

  def test_the_track_writes_a_history_entry_for_every_arrow_key_step(self):
    """CONFIRMED. One keydown is one step, and one step is one hash write.

    A reader holding the right arrow through a period fills their history with
    one entry per reading. A fix would replace the step's write with
    `history.replaceState`, which the two reader shells already use for the
    entry they do not want kept.

    Executed: the shared arrow stepper fires once per key. WEAK: the chain from
    `step` to `commit` to `T.writeHash` is read out of the file, because the
    step needs the loaded reading plan around it.
    """
    stepping = probe(probe="core", arrows=True, keys=[
      {"key": "ArrowRight"}, {"key": "ArrowRight"}, {"key": "ArrowLeft"},
    ])
    self.assertEqual(stepping["documentEvents"], ["keydown"])
    self.assertEqual(stepping["stepped"], [1, 1, -1])
    source = text_of("scripture/track.js")
    self.assertIn("T.onArrowStep((delta) => step(delta, { moveFocus: false }));", source)
    commit = probe(probe="functionSource", file="scripture/track.js", name="commit")
    self.assertIn("T.writeHash(hashPairs());", commit["text"])
    for name in ("showReading", "showPeriod"):
      with self.subTest(function=name):
        moved = probe(probe="functionSource", file="scripture/track.js", name=name)
        self.assertIn("commit(options);", moved["text"])

  def test_back_to_the_default_corpus_clears_the_reader_hash(self):
    """A default finder URL cannot continue to cite the closed reader."""
    answer = probe(
      probe="replay", file="sources/sources.js", extract=["writeHash"], call="writeHash",
      hash="#edition=migne-pl-32&passage=conf%2F1",
      bindings={
        "open": None,
        "state": {
          "author": "", "category": "", "language": "", "period": "", "rights": "",
          "readable": False, "find": "", "sort": "author",
        },
      },
    )
    self.assertEqual(answer["hash"], "")

    # With one filter set, the finder does write, and the reader keys go.
    filtered = probe(
      probe="replay", file="sources/sources.js", extract=["writeHash"], call="writeHash",
      hash="#edition=migne-pl-32&passage=conf%2F1",
      bindings={
        "open": None,
        "state": {
          "author": "augustinus", "category": "", "language": "", "period": "",
          "rights": "", "readable": False, "find": "", "sort": "author",
        },
      },
    )
    self.assertEqual(filtered["hash"], "#author=augustinus")

  def test_day_history_navigation_still_does_not_restore_the_why_apparatus(self):
    """CONFIRMED, and already recorded in `guidance/liturgy-reader-state.md`.

    `liturgy/day.js` reads `why` at start-up and writes it, but its `hashchange`
    handler does not read it back, so a Back that returns to a hash carrying
    `why=1` leaves the apparatus as it was.

    WEAK: the handler is top-level wiring. The assertion is that `why` is read
    exactly once in the file, which is the start-up read.
    """
    source = text_of("liturgy/day.js")
    self.assertEqual(source.count("hash.get('why')"), 1)
    self.assertEqual(source.count("['why', state.why ? '1' : null]"), 1)


if __name__ == "__main__":
  unittest.main()
