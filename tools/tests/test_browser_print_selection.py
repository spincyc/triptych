"""Real-browser print preparation over bounded source fixtures.

The Catena fixture retains three unmodified production fragment records and
payloads. Its reduced chapter spine makes fetching all selected bodies explicit
without loading the complete Genesis commentary during a focused regression.
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.tests.test_browser_truthfulness import HARNESS, browser

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/browser-print"
DATA = ROOT / "src/web/data"
SOURCE_EDITION = (
    "structure/sources/editions/irenaeus/adversus-haereses/"
    "1887-roberts-rambaut-coxe-anf1-1887.json"
)
CATENA = "structure/catena/01-gen/001.json"


def drive(plan):
    if shutil.which("node") is None:
        raise unittest.SkipTest("node is not installed")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    harness = HARNESS.replace("mkdtemp, readFile, rm", "mkdtemp, readFile, rm, writeFile")
    harness = harness.replace("join(tmpdir(), 'triptych-truthfulness-')",
                              "join(ROOT, '.scratch/browser-print/chrome-')")
    harness = harness.replace("} else if (act.do === 'eval') {", """} else if (act.do === 'media') {
        await cdp.send('Emulation.setEmulatedMedia', {media: act.media});
      } else if (act.do === 'capture') {
        const shot = await cdp.send('Page.captureScreenshot', {captureBeyondViewport: false});
        await writeFile(join(ROOT, '.scratch/browser-print', act.name + '.png'),
          Buffer.from(shot.data, 'base64'));
      } else if (act.do === 'viewport') {
        await cdp.send('Emulation.setDeviceMetricsOverride', {
          width: act.width, height: act.height, deviceScaleFactor: 1, mobile: false});
      } else if (act.do === 'pdf') {
        const printed = await cdp.send('Page.printToPDF', {
          printBackground: false, displayHeaderFooter: false, preferCSSPageSize: true});
        await writeFile(join(ROOT, '.scratch/browser-print', act.name + '.pdf'),
          Buffer.from(printed.data, 'base64'));
      } else if (act.do === 'eval') {""")
    with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
        script = Path(directory) / "harness.mjs"
        script.write_text(harness, encoding="utf-8")
        result = subprocess.run(["node", str(script), str(ROOT), json.dumps(plan), browser()],
                                text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def route(surface, fragment=""):
    return f"/src/web/browser/{surface}/index.html?data=/src/web/data{fragment}"


def eval_js(expression, name=None):
    return {"do": "eval", "expression": expression, **({"name": name} if name else {})}


def wait(expression):
    return {"do": "wait", "until": expression}


PRINT_STUB = """window.printCalls = 0; window.print = () => {
  window.dispatchEvent(new Event('beforeprint'));
  window.printCalls++;
  window.printSnapshot = {
    hash: location.hash,
    blocked: document.body.classList.contains('browser-print-blocked'),
    closed: [...document.querySelectorAll('.browser-print-content details')]
      .filter(d => !d.closest('[hidden]') && !d.open).length,
    missing: document.querySelectorAll('.fragment-text.missing').length,
    bodies: [...document.querySelectorAll('.fragment-text')]
      .filter(n => !n.closest('[hidden]')).map(n => n.textContent),
    source: document.querySelector('.passage-source')?.textContent,
    passageText: document.querySelector('.passage-text')?.innerText,
    identity: document.querySelector('.browser-print-identity').textContent,
    text: document.querySelector('.browser-print-content').textContent
  };
  window.dispatchEvent(new Event('afterprint'));
};"""


class CompleteSelectionPrintTests(unittest.TestCase):
    def source_plan(self, blocked=False):
        edition = json.loads((DATA / SOURCE_EDITION).read_text())
        passage = next(row for row in edition["passages"] if row.get("readable"))
        address = "#edition=" + edition["edition"]["id"] + "&passage=" + passage["id"]
        plan = {"acts": [
            {"do": "navigate", "url": route("sources", address)},
            wait("document.querySelector('.passage-text') || document.querySelector('.passage-body .notice')"),
            eval_js(PRINT_STUB),
            eval_js("window.originalHash = location.hash; window.originalDetails = [...document.querySelectorAll('#reader details')].map(d => d.open); document.querySelector('.browser-print-actions button').click()"),
            wait("!document.querySelector('.browser-print-actions button').disabled"),
            eval_js("({calls: printCalls, snapshot: window.printSnapshot, hash: location.hash, originalHash, restored: JSON.stringify(originalDetails) === JSON.stringify([...document.querySelectorAll('#reader details')].map(d => d.open)), status: document.querySelector('.browser-print-status').textContent})", "result")
        ]}
        if blocked:
            plan["blocked"] = ["*" + passage["text_path"]]
        return plan, passage

    def test_source_prints_complete_passage_with_qualifications_and_restores_details(self):
        plan, passage = self.source_plan()
        if os.environ.get("TRIPTYCH_PRINT_CAPTURES") == "1":
            plan["acts"].extend([
                {"do": "media", "media": "print"},
                {"do": "capture", "name": "sources-print"},
                {"do": "media", "media": ""},
            ])
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 1)
        self.assertFalse(seen["snapshot"]["blocked"])
        self.assertEqual(seen["snapshot"]["closed"], 0)
        self.assertTrue(seen["restored"])
        self.assertEqual(seen["hash"], seen["originalHash"])
        self.assertIn(passage["artifact_id"], seen["snapshot"]["source"])
        self.assertIn(passage["locus"], seen["snapshot"]["identity"])
        payload = json.loads((DATA / passage["text_path"]).read_text())
        self.assertEqual(" ".join(payload["text"].split()),
                         " ".join(seen["snapshot"]["passageText"].split()))

    def test_source_transport_failure_never_opens_print(self):
        plan, _ = self.source_plan(blocked=True)
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 0)
        self.assertIn("Print unavailable", seen["status"])
        self.assertEqual(seen["hash"], seen["originalHash"])

    def catena_plan(self, blocked=False, capture=False):
        fixture = json.loads((DATA / CATENA).read_text())
        first_author = fixture["sources"][fixture["fragments"][0]["source"]]["author"]
        other = next(row for row in fixture["fragments"]
                     if fixture["sources"][row["source"]]["author"] != first_author)
        fixture["fragments"] = fixture["fragments"][:2] + [other]
        fixture["leads"] = []
        fixture["blocked"] = []
        selected_ids = [row["id"] for row in fixture["fragments"]]
        plan = {"responses": {
            "src/web/data/" + CATENA: json.dumps(fixture),
            "src/web/data/douay-rheims/chapters/Gen/1.json":
                (ROOT / "src/web/browser/fixture/douay-rheims/chapters/Gen/1.json").read_text(),
        }, "acts": [
            {"do": "navigate", "url": route("catena", "#book=Gen&chapter=1&bible=douay-rheims")},
            wait("document.querySelectorAll('.fragment-body').length === 3 && document.querySelector('#reading').getAttribute('aria-busy') === 'false'"),
            eval_js(PRINT_STUB),
            eval_js("window.beforeHash = location.hash; window.beforeDetails = [...document.querySelectorAll('#reading details')].map(d => d.open); document.querySelector('.browser-print-actions button').click()"),
            wait("!document.querySelector('.browser-print-actions button').disabled"),
            eval_js("({calls: printCalls, snapshot: window.printSnapshot, hash: location.hash, beforeHash, restored: JSON.stringify(beforeDetails) === JSON.stringify([...document.querySelectorAll('#reading details')].map(d => d.open)), status: document.querySelector('.browser-print-status').textContent, requested: performance.getEntriesByType('resource').map(r => r.name).filter(n => n.includes('/catena/text/'))})", "result")
        ]}
        if blocked:
            plan["blocked"] = ["*structure/catena/text/" + selected_ids[-1] + ".json"]
        if capture:
            plan["acts"].extend([
                {"do": "capture", "name": "catena-screen"},
                {"do": "media", "media": "print"},
                {"do": "capture", "name": "catena-print"},
                {"do": "media", "media": ""},
                {"do": "pdf", "name": "catena-complete-selection"},
                {"do": "viewport", "width": 393, "height": 852},
                {"do": "capture", "name": "catena-narrow"},
            ])
        return plan, selected_ids

    def test_catena_materializes_closed_selected_fragments_and_restores_every_disclosure(self):
        plan, selected = self.catena_plan(capture=os.environ.get("TRIPTYCH_PRINT_CAPTURES") == "1")
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 1)
        self.assertEqual(len(seen["snapshot"]["bodies"]), 3)
        self.assertEqual(seen["snapshot"]["missing"], 0)
        self.assertEqual(seen["snapshot"]["closed"], 0)
        self.assertTrue(seen["restored"])
        self.assertEqual(seen["hash"], seen["beforeHash"])
        self.assertEqual(len(seen["requested"]), 3)
        for passage in selected:
            self.assertTrue(any(passage in path for path in seen["requested"]))
        self.assertTrue(all(body and body != "Loading…" for body in seen["snapshot"]["bodies"]))
        expected = [json.loads((DATA / ("structure/catena/text/" + passage + ".json")).read_text())["text"]
                    for passage in selected]
        self.assertCountEqual(seen["snapshot"]["bodies"], expected)
        if os.environ.get("TRIPTYCH_PRINT_CAPTURES") == "1" and shutil.which("pdftotext"):
            rendered = subprocess.check_output([
                "pdftotext", "-layout", str(SCRATCH / "catena-complete-selection.pdf"), "-"
            ], text=True)
            words = " ".join(rendered.split())
            for body in expected:
                self.assertIn(" ".join(body.split()[:12]), words)
                self.assertIn(" ".join(body.split()[-12:]), words)

    def test_excluded_authors_are_not_requested_for_print(self):
        plan, _ = self.catena_plan()
        plan["acts"].insert(2, eval_js("const boxes = [...document.querySelectorAll('.author-filter input')]; boxes[boxes.length - 1].click()"))
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 1)
        self.assertEqual(len(seen["snapshot"]["bodies"]), 2)
        self.assertEqual(len(seen["requested"]), 2)
        self.assertIn("Excluding authors:", seen["snapshot"]["identity"])

    def test_author_filter_change_during_preparation_refuses_the_old_selection(self):
        plan, selected = self.catena_plan()
        plan["delays"] = [{"match": selected[0] + ".json", "ms": 500}]
        plan["acts"].insert(4, eval_js("document.querySelector('.author-filter input').click()"))
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 0)
        self.assertEqual(seen["hash"], seen["beforeHash"])
        self.assertIn("selection changed", seen["status"])

    def test_navigation_during_preparation_never_prints_the_previous_selection(self):
        plan, selected = self.catena_plan()
        plan["delays"] = [{"match": selected[0] + ".json", "ms": 500}]
        plan["acts"].insert(4, eval_js("const select = document.querySelector('#chapter-select'); select.value = '2'; select.dispatchEvent(new Event('change'))"))
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 0)
        self.assertIn("selection changed", seen["status"])

    def test_catena_missing_selected_body_prevents_a_partial_print(self):
        plan, _ = self.catena_plan(blocked=True)
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 0)
        self.assertIn("Print unavailable", seen["status"])
        self.assertEqual(seen["hash"], seen["beforeHash"])
        self.assertTrue(seen["restored"])

    def test_native_print_of_lazy_catena_refuses_unprepared_body(self):
        plan, _ = self.catena_plan()
        plan["acts"] = plan["acts"][:2] + [
            eval_js("window.dispatchEvent(new Event('beforeprint')); document.body.classList.contains('browser-print-blocked')", "blocked"),
            eval_js("window.dispatchEvent(new Event('afterprint')); document.body.classList.contains('browser-print-blocked')", "restored")
        ]
        seen = drive(plan)
        self.assertTrue(seen["blocked"])
        self.assertFalse(seen["restored"])

    def test_scripture_missing_tail_blocks_printing_the_reading(self):
        fragment = json.loads((ROOT / "src/web/browser/fixture/douay-rheims/chapters/Gen/2.json").read_text())
        fragment["verses"].pop("2")
        plan = {"responses": {
            "src/web/data/douay-rheims/chapters/Gen/1.json":
                (ROOT / "src/web/browser/fixture/douay-rheims/chapters/Gen/1.json").read_text(),
            "src/web/data/douay-rheims/chapters/Gen/2.json": json.dumps(fragment),
        }, "acts": [
            {"do": "navigate", "url": "/src/web/browser/scripture/track.html?data=/src/web/data#tier=landmarks&reading=1&bible=douay-rheims"},
            wait("document.querySelector('.entry-title') && document.querySelector('#reading').getAttribute('aria-busy') === 'false'"),
            eval_js(PRINT_STUB),
            eval_js("document.querySelector('.browser-print-actions button').click()"),
            wait("!document.querySelector('.browser-print-actions button').disabled"),
            eval_js("({calls: printCalls, status: document.querySelector('.browser-print-status').textContent, notice: document.querySelector('.notice')?.textContent})", "result")
        ]}
        seen = drive(plan)["result"]
        self.assertEqual(seen["calls"], 0)
        self.assertIn("Print unavailable", seen["status"])
        self.assertIn("2", seen["notice"])


class PublicationTargetTests(unittest.TestCase):
    def test_html_targets_are_labelled_as_reader_and_print_without_pdf_or_current_pages(self):
        fixture = json.loads((DATA / "structure/documents/corpus.json").read_text())
        work = copy.deepcopy(fixture["works"][0])
        edition = work["editions"][0]
        work["editions"] = [edition]
        edition.update(available={"reader": True, "print": True},
                       targets={"reader": "web/gpt/real-reader.html", "print": "print/gpt/real-print.html"},
                       print_mode="browser", pages=None, also=[])
        edition.pop("pdf", None)
        fixture["works"] = [work]
        fixture["counted"] = {"documents": 1, "works": 1, "pages": 0}
        seen = drive({"responses": {"src/web/data/structure/documents/corpus.json": json.dumps(fixture)}, "acts": [
            {"do": "navigate", "url": route("texts")},
            wait("document.querySelector('.edition-links a')"),
            eval_js("({links: [...document.querySelectorAll('.edition-links a')].map(a => ({label:a.textContent, path:a.getAttribute('href'), download:a.hasAttribute('download')})), tally: document.querySelector('#tally').textContent})", "result")
        ]})["result"]
        self.assertEqual([link["label"] for link in seen["links"]], ["Read here", "Print view"])
        self.assertEqual([link["path"] for link in seen["links"]],
                         ["../web/gpt/real-reader.html", "../print/gpt/real-print.html"])
        self.assertFalse(any(link["download"] for link in seen["links"]))
        self.assertNotIn("0 pages", seen["tally"])
        self.assertIn("page extents unmeasured", seen["tally"])

    def test_fixed_layout_recipe_is_labelled_as_export_instructions(self):
        fixture = json.loads((DATA / "structure/documents/corpus.json").read_text())
        fixture["works"] = fixture["works"][:1]
        edition = fixture["works"][0]["editions"][0]
        fixture["works"][0]["editions"] = [edition]
        edition.update(available={"reader": False, "print": True},
                       targets={"print": "print/gpt/manual-export.html"},
                       print_mode="manual", pages=None, also=[])
        seen = drive({"responses": {"src/web/data/structure/documents/corpus.json": json.dumps(fixture)}, "acts": [
            {"do": "navigate", "url": route("texts")},
            wait("document.querySelector('.edition-links a')"),
            eval_js("[...document.querySelectorAll('.edition-links a')].map(a => a.textContent)", "labels")
        ]})["labels"]
        self.assertEqual(seen, ["Export instructions"])

    def test_papal_reader_html_retains_extent_and_witness_without_pdf_claims(self):
        fixture = json.loads((DATA / "encyclicals/index.json").read_text())
        row = next(one for one in fixture["encyclicals"] if one["readers"])
        reader = row["readers"][0]
        reader.update(reader="papal-documents/identified-witness.html", extent="fragment")
        for key in ("pdf", "pages", "pdf_sha256"):
            reader.pop(key, None)
        row["readers"] = [reader]
        fixture["encyclicals"] = [row]
        seen = drive({"responses": {"src/web/data/encyclicals/index.json": json.dumps(fixture)}, "acts": [
            {"do": "navigate", "url": route("encyclicals")},
            wait("document.querySelector('.enc-reader-link[href]')"),
            eval_js("({href: document.querySelector('.enc-reader-link').getAttribute('href'), label: document.querySelector('.enc-reader-link').textContent, extent: document.querySelector('.enc-extent').textContent, witness: document.querySelector('.enc-witness').textContent, text: document.body.textContent})", "result")
        ]})["result"]
        self.assertEqual(seen["href"], "../papal-documents/identified-witness.html")
        self.assertIn("Read source · Print", seen["label"])
        self.assertEqual(seen["extent"], "Fragment")
        self.assertEqual(seen["witness"], reader["witness"])
        self.assertNotIn("source PDF", seen["text"])


if __name__ == "__main__":
    unittest.main()
