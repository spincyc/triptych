"""Four places where the browser told a reader something that was not so.

Each class below is one defect, and each was reproduced in a real browser
before it was fixed. They are grouped here because they are one kind of fault
-- the page states as fact something the record does not say -- and because a
static reading of the source would have caught none of them: two are races or
arithmetic, and the other two are only visible when a page written for the
Missal is pointed at the Code.

  1. SOURCES: selecting a withheld passage while a readable one was still
     being fetched printed the readable passage's words under the withheld
     passage's heading and its "not shown here" notice. That is not a
     rendering glitch; it is the page publishing text the rights decision
     withheld.
  2. LAW: with a body of law chosen, a citation that body does not carry was
     answered with the same number out of a DIFFERENT Code, the select still
     reading the Code the reader chose. Each body of law numbers
     independently, so that is a citation to the wrong law.
  3. HISTORY: the page read `masses` and said "liturgies" whatever slice it
     had been handed, so the Code of Canon Law's state fold reported "92 units
     across undefined liturgies" and listed none of the 83 divisions it held.
  4. HISTORY: the count under each station on the map added the containers an
     act touched to the units it moved and called the sum "changed", so a
     station's caption and its own aria-label gave two different numbers for
     one act.

HOW THESE RUN. There is no headless model to replay for a race or for what a
page paints, so the two page-level defects are driven in real Chromium over
CDP against the browser sources as they stand in the tree, with the data root
pointed at `src/web/data`. The harness is written out below rather than kept
beside this file: it exists for these four tests and nothing else reads it.
Where an assertion can be made against ARITHMETIC rather than against a
string it is -- every caption on both slices is checked against the counts the
spine carries, so a wrong sum fails whatever words surround it.
"""

from __future__ import annotations

import functools
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src/web/data"
ACTS = DATA / "structure/act-history"
SOURCES = DATA / "structure/sources"

# The edition the withheld-passage race was reproduced on: passage 4 is
# readable and 480 words, passage 5 is a facsimile whose bytes are not
# retained, and they sit next to each other in the dropdown.
IRENAEUS = "edition.irenaeus.adversus-haereses.roberts-rambaut-coxe-anf1-1887"
EDITION_FILE = SOURCES / "editions/irenaeus/adversus-haereses/1887-roberts-rambaut-coxe-anf1-1887.json"

BROWSERS = ("/usr/bin/chromium", "/usr/bin/chromium-browser",
            "/usr/bin/google-chrome-stable", "/usr/bin/google-chrome")

HARNESS = r"""
/* Minimal real-Chromium harness for tools/tests/test_browser_truthfulness.py.
 * Serves the repository, optionally delaying one request path so a race can be
 * provoked deliberately, runs one scenario and writes what it saw as JSON. */

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, join, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(process.argv[2]);
const PLAN = JSON.parse(process.argv[3]);
const CHROME = process.argv[4];
const sleep = (ms) => new Promise((accept) => setTimeout(accept, ms));

function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml'
  })[extname(path)] || 'application/octet-stream';
}

function staticServer(delays) {
  return createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://127.0.0.1');
      const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
      const file = resolve(ROOT, relative);
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
      const body = await readFile(file);
      for (const rule of delays) {
        if (relative.includes(rule.match)) await sleep(rule.ms);
      }
      response.writeHead(200, { 'content-type': mime(file), 'cache-control': 'no-store' });
      response.end(body);
    } catch (_error) {
      response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      response.end('not found');
    }
  });
}

async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  return server.address().port;
}

async function freePort() {
  const server = createServer();
  const port = await listen(server);
  await new Promise((accept) => server.close(accept));
  return port;
}

async function waitForJson(url, attempts = 200) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) { /* the debugging endpoint is not up yet */ }
    await sleep(50);
  }
  throw new Error('Chromium debugging endpoint never answered: ' + url);
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
  }

  async ready() {
    await new Promise((accept, reject) => {
      this.socket.addEventListener('open', accept, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) return;
      const pending = this.pending.get(message.id);
      if (!pending) return;
      this.pending.delete(message.id);
      clearTimeout(pending.timer);
      if (message.error) pending.reject(new Error(message.error.message));
      else pending.accept(message.result);
    });
  }

  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error('CDP command timed out: ' + method));
      }, 30000);
      this.pending.set(id, { accept, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description ||
      result.exceptionDetails.text);
  }
  return result.result.value;
}

async function waitFor(cdp, expression, label, attempts = 300) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await evaluate(cdp, 'Boolean(' + expression + ')')) return;
    await sleep(50);
  }
  throw new Error('Timed out waiting for ' + label);
}

async function run() {
  const server = staticServer(PLAN.delays || []);
  const port = await listen(server);
  const base = 'http://127.0.0.1:' + port;
  const debugPort = await freePort();
  const profile = await mkdtemp(join(tmpdir(), 'triptych-truthfulness-'));
  const chrome = spawn(CHROME, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--remote-debugging-port=' + debugPort, '--remote-allow-origins=*',
    '--user-data-dir=' + profile, '--window-size=1280,1600',
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  chrome.stderr.on('data', () => {});

  let cdp = null;
  try {
    await waitForJson('http://127.0.0.1:' + debugPort + '/json/version');
    // A target of our own rather than whichever one the browser opened with:
    // attaching to the startup page raced its own initialisation and timed
    // the first command out.
    const opened = await fetch(
      'http://127.0.0.1:' + debugPort + '/json/new?' + encodeURIComponent('about:blank'),
      { method: 'PUT' });
    const page = await opened.json();
    cdp = new CDP(page.webSocketDebuggerUrl);
    await cdp.ready();
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');

    const seen = {};
    for (const act of PLAN.acts) {
      if (act.do === 'navigate') {
        await cdp.send('Page.navigate', { url: base + act.url });
        await waitFor(cdp,
          'location.href.indexOf(' + JSON.stringify(act.url.split('#')[0]) + ') !== -1',
          'navigation to ' + act.url);
      } else if (act.do === 'wait') {
        await waitFor(cdp, act.until, act.label || act.until);
      } else if (act.do === 'sleep') {
        await sleep(act.ms);
      } else if (act.do === 'eval') {
        const value = await evaluate(cdp, act.expression);
        if (act.name) seen[act.name] = value;
      } else {
        throw new Error('unknown act: ' + act.do);
      }
    }
    process.stdout.write(JSON.stringify(seen));
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGKILL');
    await new Promise((accept) => server.close(accept));
    // The killed browser can still be writing its profile out, so removing it
    // races and is retried. A leftover scratch directory is not a test result:
    // it must never turn a passing scenario into a failure.
    for (let attempt = 0; attempt < 10; attempt += 1) {
      try {
        await rm(profile, { recursive: true, force: true });
        break;
      } catch (_error) {
        await sleep(100);
      }
    }
  }
}

run().then(() => process.exit(0)).catch((error) => {
  process.stderr.write(String((error && error.stack) || error) + '\n');
  process.exit(1);
});
"""


def browser() -> str:
    """The browser these tests drive, or a skip naming what is missing."""
    named = os.environ.get("TRIPTYCH_CHROME")
    if named and Path(named).exists():
        return named
    for candidate in BROWSERS:
        if Path(candidate).exists():
            return candidate
    raise unittest.SkipTest("no Chromium was found; set TRIPTYCH_CHROME")


def drive(plan: dict) -> dict:
    """Run one scenario in a real browser and return what it observed."""
    if shutil.which("node") is None:  # pragma: no cover - environment without node
        raise unittest.SkipTest("node is not installed")
    chrome = browser()
    with tempfile.TemporaryDirectory() as scratch:
        harness = Path(scratch) / "harness.mjs"
        harness.write_text(HARNESS, encoding="utf-8")
        result = subprocess.run(
            ["node", str(harness), str(ROOT), json.dumps(plan), chrome],
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
    if result.returncode != 0:
        raise AssertionError(result.stderr or "the browser harness failed silently")
    return json.loads(result.stdout)


def page(name: str, query: str = "", fragment: str = "") -> str:
    """One browser page, served out of the tree, reading the tracked data."""
    address = f"/src/web/browser/{name}/index.html?data=/src/web/data"
    if query:
        address += "&" + query
    return address + fragment


def spine(slice_id: str) -> dict:
    return json.loads((ACTS / f"{slice_id}.json").read_text(encoding="utf-8"))


SELECT_PASSAGE = """(() => {
  const select = document.getElementById('passage-select');
  select.value = '%d';
  select.dispatchEvent(new Event('change'));
  return true;
})()"""

BODY_STATE = """JSON.stringify({
  locus: document.querySelector('#passage-body .passage-locus').textContent,
  notice: Boolean(document.querySelector('#passage-body .notice')),
  text: Boolean(document.querySelector('#passage-body .passage-text')),
  classes: Array.from(document.getElementById('passage-body').children)
    .map((node) => node.className)
})"""


class WithheldPassageTests(unittest.TestCase):
    """A passage that may not be shown is never shown with anything under it.

    The reader switches from a readable passage to a withheld one while the
    readable one's text is still on the wire. Before the fix the render token
    was taken AFTER the withheld branch had already returned, so the older
    fetch still believed it was current: it took a child off the withheld
    passage's own notes and appended the previous passage's words below the
    refusal that said they were not shown here.
    """

    @classmethod
    def setUpClass(cls) -> None:
        passages = json.loads(EDITION_FILE.read_text(encoding="utf-8"))["passages"]
        cls.readable = passages[3]
        cls.withheld = passages[4]
        # The premise of the scenario, asserted rather than assumed: without
        # these two neighbours being what they are the race is not provoked.
        assert cls.readable["readable"] and cls.readable["words"] > 100
        assert not cls.withheld["readable"] and cls.withheld.get("reason")
        cls.seen = drive({
            # 2.5 seconds is not a measurement of anything; it is long enough
            # that the switch certainly happens while the fetch is open.
            "delays": [{"match": "structure/sources/text/", "ms": 2500}],
            "acts": [
                {"do": "navigate",
                 "url": page("sources", fragment="#edition=" + IRENAEUS)},
                {"do": "wait", "until": "document.getElementById('passage-select')",
                 "label": "the reader"},
                {"do": "eval", "expression": SELECT_PASSAGE % 3},
                {"do": "sleep", "ms": 300},
                {"do": "eval", "expression": SELECT_PASSAGE % 4},
                {"do": "eval", "name": "at_once", "expression": BODY_STATE},
                {"do": "sleep", "ms": 3500},
                {"do": "eval", "name": "settled", "expression": BODY_STATE},
            ],
        })

    def test_the_withheld_passage_stands_alone_the_moment_it_is_chosen(self) -> None:
        at_once = json.loads(self.seen["at_once"])
        self.assertEqual(at_once["locus"], self.withheld["locus"])
        self.assertTrue(at_once["notice"])
        self.assertFalse(at_once["text"])

    def test_no_words_arrive_under_the_refusal_once_the_older_fetch_returns(self) -> None:
        settled = json.loads(self.seen["settled"])
        self.assertEqual(settled["locus"], self.withheld["locus"])
        self.assertTrue(settled["notice"], "the reason for the absence must stay")
        self.assertFalse(
            settled["text"],
            "the previous passage's words were painted under a withheld passage",
        )
        self.assertNotIn("passage-text", settled["classes"])

    def test_the_withheld_passage_keeps_its_own_notes(self) -> None:
        # The stale render did not only add: it removed. `removeChild` took the
        # last child of the body, which was this passage's editorial note.
        settled = json.loads(self.seen["settled"])
        if self.withheld.get("notes"):
            self.assertIn("passage-notes", settled["classes"])
        self.assertEqual(settled["classes"].count("passage-source"), 1)


LOOK_UP = """(() => {
  document.getElementById('line-select').value = %s;
  document.getElementById('citation-input').value = %s;
  document.getElementById('lookup').dispatchEvent(
    new Event('submit', { cancelable: true }));
  return true;
})()"""

ANSWER = """JSON.stringify({
  opened: (document.querySelector('#canon .canon-line') || {}).textContent || '',
  citation: (document.querySelector('#canon .canon-citation') || {}).textContent || '',
  none: Boolean(document.querySelector('#canon .lookup-none')),
  choices: document.querySelectorAll('#canon .lookup-choices .choice').length,
  prose: document.getElementById('canon').textContent.replace(/\\s+/g, ' '),
  select: document.getElementById('line-select').value,
  hash: location.hash
})"""


class BodyOfLawTests(unittest.TestCase):
    """A body of law asked for is the body of law answered from.

    `can. 1012` stands in the Pio-Benedictine Code and in no other body of law
    this record carries. Asked for under the Code of 1983 it used to open the
    1917 canon, leave the select reading "The Code of 1983", and rewrite the
    hash to `line=pio-benedictine` -- a citation to the wrong law, offered
    under the name of the right one. `can. 87` stands in both, and is here so
    that honouring the choice is shown to select rather than merely to refuse.
    """

    @classmethod
    def setUpClass(cls) -> None:
        acts = []
        for name, line, citation in (
            ("absent_in_chosen", "johanno-pauline", "1012"),
            ("present_in_chosen", "pio-benedictine", "1012"),
            ("unnarrowed", "", "1012"),
            ("shared_under_1983", "johanno-pauline", "87"),
            ("shared_under_1917", "pio-benedictine", "87"),
            ("shared_unnarrowed", "", "87"),
        ):
            acts.extend([
                {"do": "eval",
                 "expression": LOOK_UP % (json.dumps(line), json.dumps(citation))},
                {"do": "wait", "until": "!document.getElementById('canon')"
                                        ".querySelector('.placeholder')",
                 "label": "the lookup for " + citation},
                {"do": "eval", "name": name, "expression": ANSWER},
            ])
        cls.seen = drive({
            "delays": [],
            "acts": [
                {"do": "navigate", "url": page("law")},
                {"do": "wait", "until": "!document.getElementById('line-select').disabled",
                 "label": "the law page"},
                *acts,
            ],
        })

    def answer(self, name: str) -> dict:
        return json.loads(self.seen[name])

    def test_a_canon_the_chosen_code_does_not_carry_is_refused(self) -> None:
        answer = self.answer("absent_in_chosen")
        self.assertTrue(answer["none"], "a canon was opened where none should be")
        self.assertEqual(answer["choices"], 0)
        self.assertIn("no canon numbered 1012", answer["prose"])
        self.assertIn("The Code of 1983", answer["prose"])
        self.assertNotIn("Pio-Benedictine", answer["prose"])

    def test_the_refusal_leaves_the_chosen_code_standing(self) -> None:
        answer = self.answer("absent_in_chosen")
        self.assertEqual(answer["select"], "johanno-pauline")
        self.assertNotIn("line=pio-benedictine", answer["hash"])

    def test_the_same_citation_opens_where_it_does_stand(self) -> None:
        answer = self.answer("present_in_chosen")
        self.assertFalse(answer["none"])
        self.assertEqual(answer["citation"], "c. 1012")
        self.assertIn("Pio-Benedictine", answer["opened"])

    def test_asking_no_body_of_law_still_searches_them_all(self) -> None:
        # Nothing here narrows what an unnarrowed lookup may answer with: the
        # fix honours a choice, it does not impose one.
        answer = self.answer("unnarrowed")
        self.assertFalse(answer["none"])
        self.assertIn("Pio-Benedictine", answer["opened"])

    def test_a_number_two_codes_share_resolves_to_the_one_chosen(self) -> None:
        under_1983 = self.answer("shared_under_1983")
        under_1917 = self.answer("shared_under_1917")
        self.assertEqual(under_1983["citation"], "c. 87")
        self.assertEqual(under_1917["citation"], "c. 87")
        self.assertIn("Code of 1983", under_1983["opened"])
        self.assertIn("Pio-Benedictine", under_1917["opened"])
        self.assertNotEqual(under_1983["hash"], under_1917["hash"])

    def test_a_number_two_codes_share_is_offered_as_two_when_none_is_chosen(self) -> None:
        answer = self.answer("shared_unnarrowed")
        self.assertEqual(answer["choices"], 2)

    def test_no_second_widening_survives_in_the_page(self) -> None:
        # The fallback was one line and could be reintroduced in another; the
        # file is read here so a second one cannot appear unremarked.
        script = (ROOT / "src/web/browser/law/law.js").read_text(encoding="utf-8")
        self.assertNotIn("narrowed.length ? narrowed", script)
        self.assertEqual(script.count("inLine("), 2)


STATION_CAPTIONS = """JSON.stringify(
  Array.from(document.querySelectorAll('.station')).map((node) => ({
    id: node.getAttribute('data-station'),
    caption: node.querySelector('.station-count').textContent,
    label: node.getAttribute('aria-label')
  })))"""

PANEL = """JSON.stringify({
  sections: Array.from(document.querySelectorAll('#detail .detail-section-title'))
    .map((node) => node.textContent),
  follow: Array.from(new Set(Array.from(
    document.querySelectorAll('#detail button.link-button'))
    .map((node) => node.textContent))),
  fold: Array.from(document.querySelectorAll('#detail .fold-summary'))
    .map((node) => node.textContent),
  text: document.getElementById('detail').textContent.replace(/\\s+/g, ' ')
})"""

STATE_FOLD = """JSON.stringify({
  summary: (document.querySelector('#detail .fold-body .detail-summary') ||
    { textContent: '' }).textContent,
  groups: document.querySelectorAll('#detail .fold-body section.mass').length,
  text: (document.querySelector('#detail .fold-body') ||
    { textContent: '' }).textContent.replace(/\\s+/g, ' ')
})"""


@functools.lru_cache(maxsize=None)
def open_slice(slice_id: str, station: str) -> dict:
    """Open one station of one slice and read the panel and its state fold.

    Cached: a browser launch is expensive and every reading below is of the
    same page in the same state, so each pair is visited once.
    """
    return drive({
        "delays": [],
        "acts": [
            {"do": "navigate",
             "url": page("history", "slice=" + slice_id, "#station=" + station)},
            {"do": "wait",
             "until": "document.querySelector('#detail .detail-changes .detail-summary')",
             "label": "the station panel"},
            {"do": "eval", "name": "captions", "expression": STATION_CAPTIONS},
            {"do": "eval", "name": "panel", "expression": PANEL},
            {"do": "eval",
             "expression": "(() => { document.querySelector('#detail details.fold')"
                           ".open = true; return true; })()"},
            {"do": "wait",
             "until": "document.querySelector('#detail .fold-body .detail-summary')",
             "label": "the state fold"},
            {"do": "eval", "name": "state", "expression": STATE_FOLD},
        ],
    })


class SliceVocabularyTests(unittest.TestCase):
    """The page says what the slice says it is, and counts what it carries.

    The Code of Canon Law slice declares `unit_word: canon`,
    `group_word: division` and `group_key: divisions`. The page read none of
    the three: it looked for `masses`, found nothing, printed the count of a
    key the file does not carry as `undefined`, listed none of the 83
    divisions it did carry, and called every canon a prayer.
    """

    STATION = "sacrae-disciplinae-leges-1983"

    @classmethod
    def setUpClass(cls) -> None:
        cls.spine = spine("code-of-canon-law")
        cls.state = json.loads(
            (ACTS / "code-of-canon-law/state"
                    "/1983-01-25-sacrae-disciplinae-leges.json").read_text("utf-8"))
        cls.seen = open_slice("code-of-canon-law", cls.STATION)
        cls.panel = json.loads(cls.seen["panel"])
        cls.fold = json.loads(cls.seen["state"])
        cls.missal = open_slice("latin-missal", "si-quid-est-1634")
        cls.missal_state = json.loads(
            (ACTS / "latin-missal/state/1634-09-02-si-quid-est.json")
            .read_text("utf-8"))

    def test_the_slice_declares_the_words_this_test_holds_it_to(self) -> None:
        self.assertEqual(self.spine["unit_word"], "canon")
        self.assertEqual(self.spine["group_word"], "division")
        self.assertEqual(self.spine["group_key"], "divisions")

    def test_the_state_counts_what_the_fragment_holds(self) -> None:
        totals = self.state["totals"]
        self.assertEqual(
            self.fold["summary"].split(", as this record")[0],
            f"{totals['units']} canons across {totals['divisions']} divisions",
        )
        self.assertNotIn("undefined", self.fold["summary"])
        self.assertNotIn("liturg", self.fold["summary"])

    def test_every_container_the_fragment_holds_is_listed(self) -> None:
        self.assertEqual(self.fold["groups"], len(self.state["divisions"]))
        self.assertGreater(self.fold["groups"], 1)

    def test_nothing_on_the_page_prints_undefined(self) -> None:
        self.assertNotIn("undefined", self.panel["text"])
        self.assertNotIn("undefined", self.fold["text"])

    def test_a_canon_is_offered_as_a_canon(self) -> None:
        self.assertEqual(self.panel["follow"], ["Follow this canon"])
        self.assertEqual(self.panel["fold"],
                         ["Read the canons as they stood after this act"])
        self.assertNotIn("missal", " ".join(self.panel["fold"]))

    def test_the_sections_are_named_for_what_they_hold(self) -> None:
        self.assertIn("The divisions", self.panel["sections"])
        self.assertIn("The canons", self.panel["sections"])
        self.assertNotIn("The liturgies", self.panel["sections"])

    def test_the_missal_counts_its_containers_by_their_own_name(self) -> None:
        # The same reading, on the slice whose vocabulary is the fallback. Its
        # containers ARE masses and it says so, so "liturgies" gives way to the
        # word the record uses -- the one deliberate change on this slice.
        missal = spine("latin-missal")
        self.assertEqual(missal["group_key"], "masses")
        self.assertEqual(missal["group_word"], "mass")
        panel = json.loads(self.missal["panel"])
        fold = json.loads(self.missal["state"])
        self.assertIn("The masses", panel["sections"])
        self.assertNotIn("The liturgies", panel["sections"])
        self.assertEqual(fold["groups"], len(self.missal_state["masses"]))
        self.assertEqual(
            fold["summary"].split(", as this record")[0],
            f"{self.missal_state['totals']['units']} units across "
            f"{self.missal_state['totals']['masses']} masses",
        )

    def test_a_slice_declaring_the_generic_noun_has_declared_nothing(self) -> None:
        # `unit` is the word this page uses when it has NOT been told what a
        # thing is, so a slice that declares it has said nothing, and reading it
        # back as a declaration would spend the page's better word on a
        # placeholder. guidance/corpus-browser-master-plan.md section 6.7 calls
        # this "follow-one-prayer mode" and says it should feel like tracing a
        # lineage; "follow this unit" traces nothing a reader can name.
        #
        # THIS PINS A CONSEQUENCE OF A GENERATED FILE. The durable fix is for
        # the generator to declare `prayer` for the Missal, which is somebody
        # else's change; until then the page must not lose the word, and a
        # future generator writing `unit` again must not take it away silently.
        missal = spine("latin-missal")
        self.assertEqual(missal["unit_word"], "unit")
        panel = json.loads(self.missal["panel"])
        self.assertEqual(panel["follow"], ["Follow this prayer"])
        self.assertEqual(panel["fold"],
                         ["Read the missal as it stood after this act"])
        self.assertIn("The units", panel["sections"])


class StationMagnitudeTests(unittest.TestCase):
    """The number under a station is a number about that station.

    The caption added the containers an act touched to the units it moved, so
    a station whose own aria-label read "38 entered, 4 liturgies touched" was
    captioned "42 changed" -- a number answering to nothing, and larger than
    either quantity the record holds. Nothing here matches a string: every
    caption on both slices is checked against the counts the spine carries.
    """

    UNIT_KEYS = ("units_entered", "units_gone", "units_changed", "unestablished")

    def captions(self, slice_id: str, station: str) -> dict:
        seen = open_slice(slice_id, station)
        return {row["id"]: row for row in json.loads(seen["captions"])}

    def check(self, slice_id: str, station: str) -> None:
        rows = self.captions(slice_id, station)
        stations = spine(slice_id)["stations"]
        self.assertEqual(len(rows), len(stations))
        for one in stations:
            changed = one.get("changed") or {}
            moved = sum(changed.get(key, 0) for key in self.UNIT_KEYS)
            caption = rows[one["id"]]["caption"]
            with self.subTest(station=one["id"]):
                if moved:
                    self.assertEqual(caption.split(" ")[0], str(moved))
                else:
                    self.assertIn(caption, ("nothing changed", "nothing differs"))
                self.assertNotIn("changeds", caption)
                self.assertNotIn("differss", caption)

    def test_every_caption_on_the_code_counts_only_units(self) -> None:
        self.check("code-of-canon-law", "sacrae-disciplinae-leges-1983")

    def test_every_caption_on_the_missal_counts_only_units(self) -> None:
        self.check("latin-missal", "si-quid-est-1634")

    def test_a_caption_and_the_station_it_labels_do_not_disagree(self) -> None:
        # si-quid-est-1634 is the station the disagreement was found on: 38
        # units entered and 4 masses were touched, and the caption said 42.
        rows = self.captions("latin-missal", "si-quid-est-1634")
        row = rows["si-quid-est-1634"]
        self.assertEqual(row["caption"], "38 changed")
        self.assertIn("38 entered", row["label"])
        self.assertIn("4 masses touched", row["label"])

    def test_one_container_touched_is_said_in_the_singular(self) -> None:
        rows = self.captions("latin-missal", "si-quid-est-1634")
        row = rows["editio-typica-1962"]
        self.assertIn("1 mass touched", row["label"])
        self.assertNotIn("1 masses", row["label"])

    def test_a_station_that_moved_nothing_says_so_in_english(self) -> None:
        rows = self.captions("code-of-canon-law", "sacrae-disciplinae-leges-1983")
        quiet = [row["caption"] for row in rows.values()
                 if row["caption"].startswith("nothing")]
        self.assertTrue(quiet)
        self.assertEqual(set(quiet) - {"nothing changed", "nothing differs"}, set())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
