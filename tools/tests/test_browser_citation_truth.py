"""Ten places where a browser page stated something the record did not.

These are one fault and not ten. A Triptych page puts the reader's request in
the fragment and keeps it there, so the fragment is the citation: it is what a
reader copies, bookmarks, and sends to somebody else. Every defect below broke
the same promise from a different side -- the address went on naming the thing
that was asked for while other words stood on the page, so the citation did not
merely fail, it lied. A link that plainly refuses costs a reader one click. A
link that quietly opens something else costs them the belief that any of these
addresses mean anything.

  1. SOURCES: a deep link naming a passage the edition does not hold opened
     PASSAGE ONE, with the address still naming the passage asked for. The
     honest refusal already existed in the same file, for the passage-alone
     link Catena Omnia sends; the edition+passage shape -- which is the shape
     this page itself writes, and therefore the shape of every shared link --
     went the other way.
  2. HISTORY: a station id this record does not carry opened the NEWEST
     station and rewrote the hash to name it, so a stale citation resolved to
     a real act and said nothing.
  3. HISTORY: `printed` stations were glossed "a missal survives" on every
     slice, which on the Code of Canon Law labelled Gratian's Decretum a
     surviving missal.
  4. LAW: a `?slice=` the record does not carry left the Body-of-law select
     reading "Loading…" for ever and the citation box disabled, while the
     canon area reported the failure correctly.
  5. HISTORY: `doneBootstrapping` was never called, so a fetch that failed
     long after the page had loaded was reported as a missing data root.
  6. TEXTS: clearing the LAST filter left the fragment naming it behind, so
     the address cited a narrowing that was not in effect and a reload put it
     back.
  7. TEXTS and LAW: a hash value no option carries left the control BLANK at
     selectedIndex -1 while the page behaved as the default.
  8. SCRIPTURE: this file's own header documented `#tier=narrative`, which no
     plan offers, and the page then explained the substitute track in words
     that assumed the reader had chosen it.
  9. HISTORY: the map's `aria-label` called every slice "this missal". The map
     carries `role="img"`, which prunes all its station buttons out of the
     accessibility tree, so on the Code slice that sentence was very nearly the
     whole of the map to a reader who could not see it.
 10. LAW: a list of canons to choose between was captioned "each body of law
     numbers independently, so one number stands in more than one of them" even
     where every canon offered stood in the SAME body -- a true general
     statement printed as the explanation of a case it does not describe.

HOW THESE RUN. What a page paints cannot be replayed against a model, so every
page-level case is driven in real Chromium over CDP against the browser sources
as they stand in the tree, with the data root pointed at `src/web/data`. The
harness below is a near sibling of the one in `test_browser_truthfulness.py`
and is kept here rather than shared for the same reason that one is: it exists
for these tests, nothing else reads it, and a shared harness would have to
answer to both. It adds one act those tests did not need -- refusing a
connection outright, which is the only way to provoke the failure defect 5 is
about, because an HTTP error is not a missing data root and never was.

Wherever the claim can be made against the RECORD rather than against a string
it is: the passage a link names is compared with the passage the page paints,
the tiers the header documents are compared with the tiers the plan declares.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src/web/data"
ACTS = DATA / "structure/act-history"
SOURCES = DATA / "structure/sources"
BROWSER_SOURCE = ROOT / "src/web/browser"

# The edition the deep-link defect was reproduced on. It holds eighteen
# passages, the first of them withheld, so opening "passage one" instead of the
# passage asked for was visible as a refusal standing under the wrong locus.
IRENAEUS = "edition.irenaeus.adversus-haereses.roberts-rambaut-coxe-anf1-1887"
EDITION_FILE = (SOURCES / "editions/irenaeus/adversus-haereses"
                / "1887-roberts-rambaut-coxe-anf1-1887.json")

BROWSERS = ("/usr/bin/chromium", "/usr/bin/chromium-browser",
            "/usr/bin/google-chrome-stable", "/usr/bin/google-chrome")

HARNESS = r"""
/* Minimal real-Chromium harness for tools/tests/test_browser_citation_truth.py.
 * Serves the repository, can be told mid-scenario to refuse a request outright,
 * runs one scenario and writes what it saw as JSON. */

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { join, resolve, sep, extname } from 'node:path';
import process from 'node:process';

const ROOT = resolve(process.argv[2]);
const PLAN = JSON.parse(process.argv[3]);
const CHROME = process.argv[4];
const SCRATCH = resolve(process.argv[5]);
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

/* A refused path drops the connection rather than answering 404. The two are
 * different failures and the pages must not confuse them: a 404 is a file that
 * is not there, a dropped connection is a corpus that cannot be reached, and
 * only the second is what "no data root" means. */
const refusals = [];

function staticServer() {
  return createServer(async (request, response) => {
    const url = new URL(request.url, 'http://127.0.0.1');
    const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
    if (refusals.some((match) => relative.includes(match))) {
      request.socket.destroy();
      return;
    }
    try {
      const file = resolve(ROOT, relative);
      if (file !== ROOT && !file.startsWith(ROOT + sep)) throw new Error('outside root');
      const body = await readFile(file);
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
  const server = staticServer();
  const port = await listen(server);
  const base = 'http://127.0.0.1:' + port;
  const debugPort = await freePort();
  // Inside the caller's scratch directory, so that a browser profile cannot
  // outlive the test run even if this process is killed outright.
  const profile = await mkdtemp(join(SCRATCH, 'chromium-'));
  // Its own process group, so the whole browser can be killed rather than just
  // the process that was spawned. Killing the parent alone left renderers and
  // the zygote alive, and they recreated the profile directory AFTER it had
  // been removed -- 38 of them survived one run of this file.
  const chrome = spawn(CHROME, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--remote-debugging-port=' + debugPort, '--remote-allow-origins=*',
    '--user-data-dir=' + profile, '--window-size=1280,1600',
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'], detached: true });
  chrome.stderr.on('data', () => {});

  let cdp = null;
  try {
    await waitForJson('http://127.0.0.1:' + debugPort + '/json/version');
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
      } else if (act.do === 'reload') {
        await cdp.send('Page.reload', {});
      } else if (act.do === 'wait') {
        await waitFor(cdp, act.until, act.label || act.until);
      } else if (act.do === 'sleep') {
        await sleep(act.ms);
      } else if (act.do === 'refuse') {
        refusals.push(act.match);
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
    try { process.kill(-chrome.pid, 'SIGKILL'); } catch (_error) { chrome.kill('SIGKILL'); }
    // WAIT for it to be gone before removing anything. Removing first is what
    // leaked: a surviving child rebuilt the directory behind the delete.
    await Promise.race([
      new Promise((accept) => chrome.once('close', accept)),
      sleep(5000)
    ]);
    await new Promise((accept) => server.close(accept));
    // Belt and braces even so. A leftover scratch directory is not a test
    // result: it must never turn a passing scenario into a failure.
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
        profiles = Path(scratch) / "profiles"
        profiles.mkdir()
        result = subprocess.run(
            ["node", str(harness), str(ROOT), json.dumps(plan), chrome, str(profiles)],
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
        # The harness removes its own profile; this is the guarantee that it is
        # gone whatever the harness managed, because `TemporaryDirectory` will
        # raise rather than delete a tree that grew back under it.
        shutil.rmtree(profiles, ignore_errors=True)
    if result.returncode != 0:
        raise AssertionError(result.stderr or "the browser harness failed silently")
    return json.loads(result.stdout)


def page(name: str, query: str = "", fragment: str = "") -> str:
    """One browser page, served out of the tree, reading the tracked data.

    `name` is the directory holding an `index.html`, or a path to the file
    itself where a directory holds more than one page.
    """
    leaf = name if name.endswith(".html") else name + "/index.html"
    address = f"/src/web/browser/{leaf}?data=/src/web/data"
    if query:
        address += "&" + query
    return address + fragment


def slice_file(slice_id: str) -> dict:
    return json.loads((ACTS / f"{slice_id}.json").read_text(encoding="utf-8"))


def source(name: str) -> str:
    return (BROWSER_SOURCE / name).read_text(encoding="utf-8")


# What the Source Library reader is showing, and what the address says it is.
READER = """JSON.stringify({
  hash: location.hash,
  locus: (document.querySelector('#reader .passage-locus') || {}).textContent || '',
  count: (document.querySelector('#reader .passage-count') || {}).textContent || '',
  error: (document.querySelector('#reader .error') || {}).textContent || '',
  selected: (document.getElementById('passage-select') || {}).value || '',
  text: document.getElementById('reader').textContent.replace(/\\s+/g, ' ')
})"""


class DeepLinkedPassageTests(unittest.TestCase):
    """The passage the address names is the passage on the page, or none is.

    `Math.max(0, findIndex(...))` turned "this edition does not hold that
    passage" into index 0, so a link that named a passage the edition never had
    opened its FIRST passage under the original address. The refusal this now
    reaches was already in the same file, three hundred lines below, for the
    link shape that carries a passage and no edition.
    """

    @classmethod
    def setUpClass(cls) -> None:
        passages = json.loads(EDITION_FILE.read_text(encoding="utf-8"))["passages"]
        cls.first = passages[0]
        # A passage well inside the edition and with a locus of its own, so
        # that "the page opened passage one instead" is unmistakable.
        cls.wanted = passages[3]
        assert cls.wanted["locus"] != cls.first["locus"]
        cls.absent = ("passage.irenaeus.adversus-haereses."
                      "roberts-rambaut-coxe-anf1-1887.9.99.9.ocr")
        assert not any(one["id"] == cls.absent for one in passages)
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page(
                    "sources", fragment=f"#edition={IRENAEUS}&passage={cls.wanted['id']}")},
                {"do": "wait", "until": "document.getElementById('passage-select')",
                 "label": "the passage the link names"},
                {"do": "eval", "name": "held", "expression": READER},
                {"do": "navigate", "url": page(
                    "sources", fragment=f"#edition={IRENAEUS}&passage={cls.absent}")},
                {"do": "wait",
                 "until": "document.querySelector('#reader .error') ||"
                          " document.getElementById('passage-select')",
                 "label": "the answer to a passage this edition does not hold"},
                {"do": "sleep", "ms": 400},
                {"do": "eval", "name": "absent", "expression": READER},
            ],
        })

    def held(self) -> dict:
        return json.loads(self.seen["held"])

    def absent_case(self) -> dict:
        return json.loads(self.seen["absent"])

    def test_a_passage_the_edition_holds_is_the_passage_shown(self) -> None:
        # The control. Without it the refusal below could be a page that has
        # simply stopped following deep links at all.
        held = self.held()
        self.assertEqual(held["locus"], self.wanted["locus"])
        self.assertIn(self.wanted["id"], held["hash"])

    def test_a_passage_the_edition_does_not_hold_does_not_open_passage_one(self) -> None:
        absent = self.absent_case()
        self.assertNotEqual(
            absent["locus"], self.first["locus"],
            "the link named a passage this edition does not hold and passage "
            "one was painted under it",
        )
        self.assertEqual(absent["locus"], "")
        self.assertNotIn("Passage 1 of", absent["count"])

    def test_the_refusal_names_the_id_that_was_asked_for(self) -> None:
        absent = self.absent_case()
        self.assertIn(self.absent, absent["error"])
        self.assertIn("can be opened here", absent["error"])

    def test_the_address_and_the_page_agree_about_which_passage_this_is(self) -> None:
        # The property the defect violated, stated once and directly: whatever
        # passage id the address carries, the page either shows THAT passage or
        # shows no passage at all.
        for case in (self.held(), self.absent_case()):
            asked = case["hash"].split("passage=")[1].split("&")[0]
            if not case["locus"]:
                continue
            self.assertEqual(
                asked, self.wanted["id"],
                "the address named one passage and the page painted another",
            )

    def test_the_refusal_leaves_the_link_exactly_as_it_arrived(self) -> None:
        # Nothing is open, so nothing may rewrite the fragment to name a
        # passage that is still being refused.
        absent = self.absent_case()
        self.assertIn(self.absent, absent["hash"])
        self.assertIn("edition=" + IRENAEUS, absent["hash"])

    def test_the_two_routes_share_one_refusal(self) -> None:
        # The point of the fix is that no second wording was written: both the
        # edition+passage link and the passage-alone link reach one function.
        script = source("sources/sources.js")
        passage_refusal = script.split(
            "function reportPassageNotHere(", 1
        )[1].split("function reportEditionNotHere(", 1)[0]
        self.assertEqual(passage_refusal.count("can be opened here"), 1)
        self.assertEqual(script.count("reportPassageNotHere("), 3)
        self.assertNotIn("Math.max(0, (payload.passages", script)


HISTORY_STATE = """JSON.stringify({
  hash: location.hash,
  title: (document.querySelector('#detail .detail-title') || {}).textContent || '',
  error: (document.querySelector('#detail .error') || {}).textContent || '',
  selected: Array.from(document.querySelectorAll('.station-selected'))
    .map((node) => node.getAttribute('data-station')),
  banner: document.getElementById('banner').hidden
    ? '' : document.getElementById('banner').textContent,
  detail: document.getElementById('detail').textContent.replace(/\\s+/g, ' ')
})"""


class UnknownStationTests(unittest.TestCase):
    """A station id this record does not carry opens no station at all.

    `byId.has(...)` guarded the branch that honoured the citation and nothing
    guarded the fall-through, so an unknown id landed on the last station in
    topological order -- and `open` writes the hash, so the address was
    rewritten to name it. A citation for an act that has been renamed, or one
    with a typo in it, therefore resolved silently to whatever the record
    reaches furthest.
    """

    @classmethod
    def setUpClass(cls) -> None:
        stations = slice_file("latin-missal")["stations"]
        cls.newest = stations[-1]["id"]
        cls.real = stations[0]["id"]
        cls.absent = "no-such-station-1234"
        assert not any(one["id"] == cls.absent for one in stations)
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page(
                    "history", fragment="#station=" + cls.absent)},
                {"do": "wait", "until": "document.querySelector('#detail .error') ||"
                                        " document.querySelector('#detail .detail-title')",
                 "label": "the answer to an unknown station"},
                {"do": "eval", "name": "absent", "expression": HISTORY_STATE},
                {"do": "navigate", "url": page(
                    "history", fragment="#station=" + cls.real)},
                {"do": "wait", "until": "document.querySelector('#detail .detail-title')",
                 "label": "a station this record does carry"},
                {"do": "eval", "name": "real", "expression": HISTORY_STATE},
            ],
        })

    def absent_case(self) -> dict:
        return json.loads(self.seen["absent"])

    def real_case(self) -> dict:
        return json.loads(self.seen["real"])

    def test_an_unknown_station_does_not_become_the_newest_one(self) -> None:
        absent = self.absent_case()
        self.assertNotIn(self.newest, absent["detail"])
        self.assertEqual(absent["selected"], [])

    def test_the_address_is_not_rewritten_to_name_a_real_act(self) -> None:
        absent = self.absent_case()
        self.assertIn(self.absent, absent["hash"])
        self.assertNotIn(self.newest, absent["hash"])

    def test_the_refusal_quotes_the_id_and_offers_nothing_instead(self) -> None:
        absent = self.absent_case()
        self.assertIn(self.absent, absent["error"])
        self.assertIn("carries no station", absent["error"])

    def test_a_station_this_record_does_carry_still_opens(self) -> None:
        real = self.real_case()
        self.assertEqual(real["selected"], [self.real])
        self.assertIn(self.real, real["hash"])
        self.assertEqual(real["error"], "")


class PrintedStationWordsTests(unittest.TestCase):
    """A printed station is glossed in words true of the slice it is on.

    `printed` means an artifact survives and no act has been located for it.
    The gloss said "a missal survives" whatever slice the page had been handed,
    so on the Code of Canon Law it labelled Gratian's Decretum -- whose
    surviving printing is Friedberg's edition of 1879 -- a surviving missal.
    The slice declares no word for the artifact, so none is invented: the fix
    uses `printing`, which `act-history check` requires every printed station
    to name and which the detail panel already prints on the row above.
    """

    @classmethod
    def setUpClass(cls) -> None:
        code = slice_file("code-of-canon-law")
        cls.printed = next(one for one in code["stations"]
                           if one.get("station_kind") == "printed")
        # The premise: this slice really does hold a printed station, it really
        # does name a printing, and that printing is not a missal.
        assert cls.printed["printing"]
        assert "missal" not in cls.printed["printing"]
        missal = slice_file("latin-missal")
        cls.missal_printed = next(one for one in missal["stations"]
                                  if one.get("station_kind") == "printed")
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page(
                    "history", "slice=code-of-canon-law",
                    "#station=" + cls.printed["id"])},
                {"do": "wait", "until": "document.querySelector('#detail .detail-title')",
                 "label": "a printed station of the Code"},
                {"do": "eval", "name": "code", "expression": HISTORY_STATE},
                {"do": "eval", "name": "code_legend",
                 "expression": "document.getElementById('legend')"
                               ".textContent.replace(/\\s+/g, ' ')"},
                {"do": "navigate", "url": page(
                    "history", "slice=latin-missal",
                    "#station=" + cls.missal_printed["id"])},
                {"do": "wait", "until": "document.querySelector('#detail .detail-title')",
                 "label": "a printed station of the Missal"},
                {"do": "eval", "name": "missal", "expression": HISTORY_STATE},
                {"do": "eval", "name": "missal_legend",
                 "expression": "document.getElementById('legend')"
                               ".textContent.replace(/\\s+/g, ' ')"},
            ],
        })

    def test_the_code_slice_does_not_call_its_artifact_a_missal(self) -> None:
        detail = json.loads(self.seen["code"])["detail"]
        self.assertIn("A printed station.", detail)
        self.assertNotIn("missal", detail.lower())

    def test_the_code_legend_does_not_call_its_artifacts_missals(self) -> None:
        self.assertIn("printed", self.seen["code_legend"])
        self.assertNotIn("missal", self.seen["code_legend"].lower())

    def test_the_gloss_names_what_the_record_says_survives(self) -> None:
        detail = json.loads(self.seen["code"])["detail"]
        self.assertIn("printing it stands on survives", detail)
        self.assertIn("the instrument is missing", detail)
        # The word is not invented for the gloss: the panel already prints it.
        self.assertIn(self.printed["printing"], detail)

    def test_the_missal_slice_is_still_told_the_truth_in_the_same_words(self) -> None:
        # The fix is one wording for every slice, not a second one bolted on
        # for the Code -- two glosses is how the first one came to be wrong.
        detail = json.loads(self.seen["missal"])["detail"]
        self.assertIn("printing it stands on survives", detail)
        self.assertIn("printed", self.seen["missal_legend"])

    def test_no_second_gloss_survives_in_the_page(self) -> None:
        # The old wording is quoted in a comment above the fix, deliberately,
        # so this looks for it where it would be PRINTED -- opened by a quote.
        script = source("history/history.js")
        self.assertNotIn("'A printed station. A missal survives", script)
        self.assertNotIn("' — a missal survives", script)
        self.assertEqual(script.count("printing it stands on survives"), 1)


MAP_LABEL = """(document.querySelector('#map svg') || {})
  .getAttribute('aria-label') || ''"""


class MapLabelTests(unittest.TestCase):
    """What the map calls itself is true of the slice it is drawing.

    The label said "the acts that changed this missal" on every slice, so the
    Code of Canon Law was drawn under a sentence calling it a missal. It is not
    one line among many: `role="img"` on the same element prunes all 47 station
    buttons from the accessibility tree, so this is what a screen reader is
    given INSTEAD of the map, not alongside it.

    The slice declares no word for the thing the acts changed, and none is
    invented. The neutral word is used rather than the declared one on purpose:
    this page has two places where an undeclared vocabulary falls back to the
    Missal's own words, both defended because the slice that declares nothing
    is in fact a missal, and a third would leave the same falsehood one
    undeclared slice away from coming back.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page("history", "slice=code-of-canon-law")},
                {"do": "wait", "until": "document.querySelector('#map svg')",
                 "label": "the map of the Code"},
                {"do": "eval", "name": "code", "expression": MAP_LABEL},
                {"do": "navigate", "url": page("history", "slice=latin-missal")},
                {"do": "wait", "until": "document.querySelector('#map svg')",
                 "label": "the map of the Missal"},
                {"do": "eval", "name": "missal", "expression": MAP_LABEL},
            ],
        })

    def test_the_code_slice_is_not_drawn_as_a_missal(self) -> None:
        self.assertNotIn("missal", self.seen["code"].lower())

    def test_the_label_still_says_what_the_drawing_is(self) -> None:
        # Removing the falsehood must not empty the one string that stands in
        # for a pruned subtree.
        stations = len(slice_file("code-of-canon-law")["stations"])
        self.assertIn("The acts this record carries", self.seen["code"])
        self.assertIn(f"{stations} stations", self.seen["code"])

    def test_one_label_serves_every_slice(self) -> None:
        missal = len(slice_file("latin-missal")["stations"])
        self.assertIn("The acts this record carries", self.seen["missal"])
        self.assertIn(f"{missal} stations", self.seen["missal"])

    def test_nothing_printed_by_this_page_calls_an_unnamed_slice_a_missal(self) -> None:
        # The two survivors are the guarded fallbacks the file argues for, and
        # both are reached only where the slice declares no word of its own.
        script = source("history/history.js")
        printed = [line for line in script.splitlines()
                   if "missal" in line.lower() and "*" not in line
                   and not line.lstrip().startswith("//")]
        self.assertEqual(
            [line.strip() for line in printed],
            [": 'Read the missal as it stood after this act',"],
        )


LAW_CONTROLS = """JSON.stringify({
  options: Array.from(document.getElementById('line-select').options)
    .map((node) => node.textContent),
  index: document.getElementById('line-select').selectedIndex,
  value: document.getElementById('line-select').value,
  placeholder: document.getElementById('citation-input').placeholder,
  disabled: document.getElementById('citation-input').disabled,
  canon: document.getElementById('canon').textContent.replace(/\\s+/g, ' ')
})"""


class LawControlsOnAMissingSliceTests(unittest.TestCase):
    """When the record does not load, the controls say so too.

    `start` is what fills the Body-of-law select and enables the citation box,
    so a `?slice=` the record does not carry left both exactly as the markup
    ships them: a select reading "Loading…" out of a file that was never coming
    and an input refusing every keystroke. The canon area reported the failure
    accurately the whole time; a reader trying to use the page was looking at
    the controls.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.absent = "no-such-body-of-law"
        assert not (ACTS / f"{cls.absent}.json").exists()
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page("law", "slice=" + cls.absent)},
                {"do": "wait", "until": "document.querySelector('#canon .lookup-none')",
                 "label": "the report that the record could not be read"},
                {"do": "eval", "name": "broken", "expression": LAW_CONTROLS},
                {"do": "navigate", "url": page("law")},
                {"do": "wait", "until": "!document.getElementById('line-select').disabled",
                 "label": "the record that does load"},
                {"do": "eval", "name": "whole", "expression": LAW_CONTROLS},
            ],
        })

    def broken(self) -> dict:
        return json.loads(self.seen["broken"])

    def test_the_select_stops_claiming_to_be_loading(self) -> None:
        broken = self.broken()
        self.assertNotIn("Loading…", broken["options"])
        self.assertEqual(len(broken["options"]), 1)

    def test_the_select_says_what_happened(self) -> None:
        broken = self.broken()
        self.assertIn("could not be read", broken["options"][0])

    def test_the_citation_box_stops_promising_a_lookup_it_cannot_run(self) -> None:
        broken = self.broken()
        self.assertTrue(broken["disabled"])
        self.assertIn("could not be read", broken["placeholder"])
        self.assertNotIn("c. 1095", broken["placeholder"])

    def test_the_canon_area_still_reports_it_as_it_always_did(self) -> None:
        self.assertIn("could not be read", self.broken()["canon"])
        self.assertIn(self.absent, self.broken()["canon"])

    def test_a_record_that_does_load_is_untouched(self) -> None:
        whole = json.loads(self.seen["whole"])
        self.assertEqual(whole["options"][0], "Any")
        self.assertFalse(whole["disabled"])
        self.assertIn("c. 1095", whole["placeholder"])


class HistoryBootstrapTests(unittest.TestCase):
    """A fetch that fails after the page has loaded is not a missing data root.

    The shared loader treats a rejected fetch as proof that no data root exists
    -- but only while bootstrapping, which is why every other page ends
    bootstrapping the moment its spine is in hand. This page never called
    `doneBootstrapping`, so it stayed in bootstrap for the whole session: a
    station fragment that could not be reached an hour later entered the
    built-in fallback and raised the "No data root could be reached" banner
    over a page that had plainly reached the data root already.
    """

    @classmethod
    def setUpClass(cls) -> None:
        stations = slice_file("latin-missal")["stations"]
        # A station whose change set is a fragment of its own, which is the
        # fetch that is going to be refused.
        cls.station = next(one for one in stations if one.get("station_path"))
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page("history")},
                {"do": "wait", "until": "document.querySelector('.station')",
                 "label": "the map"},
                {"do": "refuse", "match": "structure/act-history/latin-missal/"},
                {"do": "eval", "expression":
                    "(() => { location.hash = 'station=" + cls.station["id"] +
                    "'; return true; })()"},
                {"do": "wait", "until": "document.querySelector('#detail .error')",
                 "label": "the report of the refused fetch"},
                {"do": "eval", "name": "after", "expression": HISTORY_STATE},
            ],
        })

    def after(self) -> dict:
        return json.loads(self.seen["after"])

    def test_no_missing_data_root_is_announced(self) -> None:
        self.assertEqual(
            self.after()["banner"], "",
            "a page that had already loaded its record announced that no data "
            "root could be reached",
        )

    def test_the_real_failure_is_reported_instead(self) -> None:
        error = self.after()["error"]
        self.assertIn("could not be read", error)
        self.assertIn("could not be reached", error)
        self.assertNotIn("built-in fallback", error)

    def test_the_page_ends_bootstrapping_exactly_once_on_each_route(self) -> None:
        # Both routes out of the boot chain end it, as the other pages do: the
        # spine arriving, and the spine failing to arrive.
        script = source("history/history.js")
        self.assertEqual(script.count("T.doneBootstrapping();"), 2)


TEXTS_STATE = """JSON.stringify({
  hash: location.hash,
  href: location.href,
  author: document.getElementById('author-select').value,
  authorIndex: document.getElementById('author-select').selectedIndex,
  authorShown: document.getElementById('author-select').selectedIndex < 0 ? '' :
    document.getElementById('author-select')
      .options[document.getElementById('author-select').selectedIndex].textContent,
  indexes: ['author-select', 'edition-select', 'section-select', 'reading-select',
    'sort-select'].map((id) => document.getElementById(id).selectedIndex),
  tally: document.getElementById('tally').textContent
})"""

PICK_AUTHOR = """(() => {
  const select = document.getElementById('author-select');
  select.value = select.options[1].value;
  select.dispatchEvent(new Event('change'));
  return select.value;
})()"""

CLEAR_AUTHOR = """(() => {
  const select = document.getElementById('author-select');
  select.value = '';
  select.dispatchEvent(new Event('change'));
  return true;
})()"""


class ClearedFilterTests(unittest.TestCase):
    """Clearing the last filter clears the address with it.

    The shared writer declines an all-empty pair list, which is right for a
    page that has never written a fragment and wrong for one whose reader has
    just cleared their only choice: the fragment naming that choice stayed in
    the address, so the address cited a narrowing that was not in effect and a
    reload restored a filter the reader had deliberately dropped.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page("texts")},
                {"do": "wait", "until": "!document.getElementById('author-select').disabled",
                 "label": "the catalogue"},
                {"do": "eval", "name": "picked", "expression": PICK_AUTHOR},
                {"do": "sleep", "ms": 200},
                {"do": "eval", "name": "narrowed", "expression": TEXTS_STATE},
                {"do": "eval", "expression": CLEAR_AUTHOR},
                {"do": "sleep", "ms": 200},
                {"do": "eval", "name": "cleared", "expression": TEXTS_STATE},
                {"do": "reload"},
                {"do": "wait", "until": "!document.getElementById('author-select').disabled",
                 "label": "the catalogue again"},
                {"do": "sleep", "ms": 200},
                {"do": "eval", "name": "reloaded", "expression": TEXTS_STATE},
            ],
        })

    def test_choosing_a_filter_still_writes_it_into_the_address(self) -> None:
        # The control: the fix must not stop the page writing its state, and it
        # must keep writing it in the published form, which is percent-encoded.
        narrowed = json.loads(self.seen["narrowed"])
        self.assertIn("author=" + quote(self.seen["picked"], safe=""),
                      narrowed["hash"])

    def test_clearing_the_last_filter_leaves_no_fragment_behind(self) -> None:
        cleared = json.loads(self.seen["cleared"])
        self.assertEqual(
            cleared["hash"], "",
            "the address went on citing a filter the reader had cleared",
        )
        self.assertNotIn("#", cleared["href"])

    def test_a_reload_does_not_restore_the_cleared_filter(self) -> None:
        reloaded = json.loads(self.seen["reloaded"])
        self.assertEqual(reloaded["author"], "")
        self.assertEqual(reloaded["hash"], "")
        self.assertNotIn(" of ", reloaded["tally"],
                         "the reloaded catalogue was still narrowed")


class InvalidHashControlTests(unittest.TestCase):
    """A control shows the state actually in effect, never a blank.

    Assigning an unknown value to a select leaves it at selectedIndex -1: the
    control reads BLANK, and every reader of `.value` sees the empty string and
    behaves as the default. So the page ran unnarrowed under a control that
    named neither what was asked for nor what was in force.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page(
                    "texts",
                    fragment="#author=no-such-model&edition=no-such-edition"
                             "&section=no-such-section&reading=no-such-reading"
                             "&sort=no-such-sort")},
                {"do": "wait", "until": "!document.getElementById('author-select').disabled",
                 "label": "the catalogue"},
                {"do": "sleep", "ms": 200},
                {"do": "eval", "name": "texts", "expression": TEXTS_STATE},
                {"do": "navigate", "url": page(
                    "law", fragment="#line=no-such-body&canon=1095")},
                {"do": "wait", "until": "!document.getElementById('line-select').disabled &&"
                                        " !document.querySelector('#canon .placeholder')",
                 "label": "the lookup"},
                {"do": "eval", "name": "law", "expression": LAW_CONTROLS},
            ],
        })

    def test_no_texts_control_is_left_blank(self) -> None:
        texts = json.loads(self.seen["texts"])
        self.assertNotIn(-1, texts["indexes"],
                         "a control was left blank at selectedIndex -1")

    def test_the_texts_control_names_the_state_in_force(self) -> None:
        texts = json.loads(self.seen["texts"])
        self.assertEqual(texts["author"], "")
        self.assertEqual(texts["authorShown"], "Any author")

    def test_the_texts_list_and_its_controls_agree(self) -> None:
        # Unnarrowed behaviour under a control that says "Any author" is one
        # state honestly shown; the defect was the same behaviour under a
        # control that said nothing at all.
        texts = json.loads(self.seen["texts"])
        self.assertNotIn(" of ", texts["tally"])

    def test_the_body_of_law_control_is_not_left_blank(self) -> None:
        law = json.loads(self.seen["law"])
        self.assertNotEqual(law["index"], -1)
        self.assertEqual(law["value"], "")
        self.assertEqual(law["options"][law["index"]], "Any")


LOOK_UP = """(() => {
  document.getElementById('line-select').value = '';
  document.getElementById('citation-input').value = %s;
  document.getElementById('lookup').dispatchEvent(
    new Event('submit', { cancelable: true }));
  return true;
})()"""

CHOICES = """JSON.stringify({
  caption: (document.querySelector('#canon .lookup-choices .weak') || {})
    .textContent || '',
  bodies: Array.from(document.querySelectorAll('#canon .choice-line'))
    .map((node) => node.textContent),
  count: document.querySelectorAll('#canon .lookup-choices .choice').length,
  none: Boolean(document.querySelector('#canon .lookup-none'))
})"""


class DisambiguationTests(unittest.TestCase):
    """A list of canons is explained by what actually separates them.

    "Each body of law numbers independently, so one number stands in more than
    one of them" is true of this corpus and was printed over every list of
    choices regardless. Looking up 100 offers c. 1008 and c. 1009, both of the
    1983 Code, and nothing has collided: the caption explained a case that had
    not happened. Where two bodies really do answer to one number the sentence
    is kept word for word, because there it is the explanation.
    """

    @classmethod
    def setUpClass(cls) -> None:
        acts = []
        for name, typed in (("one_body", "100"), ("two_bodies", "87")):
            acts.extend([
                {"do": "eval", "expression": LOOK_UP % json.dumps(typed)},
                {"do": "wait",
                 "until": "!document.getElementById('canon').querySelector('.placeholder')",
                 "label": "the lookup for " + typed},
                {"do": "eval", "name": name, "expression": CHOICES},
            ])
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page("law")},
                {"do": "wait", "until": "!document.getElementById('line-select').disabled",
                 "label": "the law page"},
                *acts,
            ],
        })

    def one_body(self) -> dict:
        return json.loads(self.seen["one_body"])

    def two_bodies(self) -> dict:
        return json.loads(self.seen["two_bodies"])

    def test_the_premise_holds_in_the_record(self) -> None:
        # Both scenarios are only worth anything if the record still answers
        # this way; asserted rather than assumed.
        one = self.one_body()
        two = self.two_bodies()
        self.assertEqual(one["count"], 2)
        self.assertEqual(len(set(one["bodies"])), 1)
        self.assertEqual(two["count"], 2)
        self.assertEqual(len(set(two["bodies"])), 2)

    def test_choices_inside_one_body_are_not_called_a_collision(self) -> None:
        caption = self.one_body()["caption"]
        self.assertNotIn(
            "numbers independently", caption,
            "two canons of one Code were explained as one number standing in "
            "more than one body of law",
        )
        self.assertNotIn("more than one of them", caption)

    def test_choices_inside_one_body_still_say_they_are_different_canons(self) -> None:
        caption = self.one_body()["caption"]
        self.assertIn("More than one canon answers to that", caption)
        self.assertIn("not the same canon", caption)

    def test_a_real_collision_across_bodies_is_still_explained(self) -> None:
        caption = self.two_bodies()["caption"]
        self.assertIn("Each body of law numbers independently", caption)
        self.assertIn("more than one of them", caption)


TRACK_STATE = """JSON.stringify({
  hash: location.hash,
  track: document.getElementById('track-select').value,
  notice: (document.querySelector('.diverted') || {}).textContent || '',
  title: (document.querySelector('.entry-title') || {}).textContent || ''
})"""


class TrackTierTests(unittest.TestCase):
    """The tiers this page documents are tiers the plan offers.

    The header advertised `#tier=narrative` in all three of its worked
    examples, and no plan has ever declared that tier. Every link built from
    the header therefore fell back to the smallest track -- and the page then
    explained itself in words written for a reader who had just narrowed
    deliberately, telling one who had named no track at all that their reading
    was missing from "the smaller selection".
    """

    PLAN = DATA / "structure/readings/narrative-spine.json"

    @classmethod
    def setUpClass(cls) -> None:
        cls.script = source("scripture/track.js")
        cls.header = cls.script.split("'use strict'")[0]
        plan = json.loads(cls.PLAN.read_text(encoding="utf-8"))
        cls.declared = set(plan["tiers"])
        # The premise of the scenario: reading 47 stands in the plan, above the
        # smallest tier, so a link naming it under a tier the plan does not
        # offer really does land somewhere else.
        tier = next(one["tier"] for period in plan["periods"]
                    for one in period["readings"] if one["order"] == 47)
        assert tier != "landmarks"
        assert "narrative" not in cls.declared
        cls.seen = drive({
            "acts": [
                {"do": "navigate", "url": page(
                    "scripture/track.html",
                    fragment="#tier=narrative&reading=47&bible=douay-rheims")},
                {"do": "wait", "until": "document.querySelector('.entry-title')",
                 "label": "the reading the link names"},
                {"do": "eval", "name": "unknown", "expression": TRACK_STATE},
                {"do": "navigate", "url": page(
                    "scripture/track.html",
                    fragment="#tier=full-account&reading=47&bible=douay-rheims")},
                {"do": "wait", "until": "document.querySelector('.entry-title')",
                 "label": "the full account"},
                {"do": "eval", "expression":
                    "(() => { const s = document.getElementById('track-select');"
                    " s.value = 'landmarks';"
                    " s.dispatchEvent(new Event('change')); return true; })()"},
                {"do": "sleep", "ms": 600},
                {"do": "eval", "name": "narrowed", "expression": TRACK_STATE},
            ],
        })

    def test_every_tier_the_header_documents_is_one_the_plan_offers(self) -> None:
        # Read off the plan rather than restated here, so a plan that renames a
        # tier fails this rather than quietly outdating the header again.
        documented = set(re.findall(r"#tier=([a-z0-9-]+)", self.header))
        self.assertTrue(documented, "the header documents no worked example at all")
        self.assertEqual(
            documented - self.declared, set(),
            "the header documents a tier the plan does not offer",
        )

    def test_the_worked_examples_name_a_period_and_a_reading_that_exist(self) -> None:
        plan = json.loads(self.PLAN.read_text(encoding="utf-8"))
        periods = {period["key"] for period in plan["periods"]}
        orders = {str(one["order"]) for period in plan["periods"]
                  for one in period["readings"]}
        for key in re.findall(r"period=([a-z0-9-]+)", self.header):
            self.assertIn(key, periods)
        for key in re.findall(r"reading=([0-9]+)", self.header):
            self.assertIn(key, orders)

    def test_the_page_still_shows_a_track_for_a_tier_it_cannot_offer(self) -> None:
        # Refusing outright would strand every already-shared link built from
        # the old header. The substitution stays; what changes is that it is
        # said, and said about the track the page chose.
        unknown = json.loads(self.seen["unknown"])
        self.assertEqual(unknown["track"], "landmarks")
        self.assertIn("tier=landmarks", unknown["hash"])

    def test_the_reader_is_told_the_plan_has_no_such_track(self) -> None:
        unknown = json.loads(self.seen["unknown"])
        self.assertIn("no “narrative” track", unknown["notice"])
        self.assertIn("Landmarks track is shown", unknown["notice"])

    def test_a_track_the_reader_never_chose_is_not_called_their_selection(self) -> None:
        unknown = json.loads(self.seen["unknown"])
        self.assertNotIn(
            "smaller selection", unknown["notice"],
            "a reader who named no track was told about the selection they made",
        )

    def test_a_reader_who_does_narrow_is_told_what_they_did(self) -> None:
        # The original sentence is right for the reader it was written for and
        # is kept for them word for word.
        narrowed = json.loads(self.seen["narrowed"])
        self.assertIn("not in the Landmarks track, which is the smaller selection",
                      narrowed["notice"])
        self.assertIn("nearest reading before it", narrowed["notice"])


if __name__ == "__main__":
    unittest.main()
