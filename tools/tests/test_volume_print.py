"""Chromium checks for bounded reading-plan pages and complete-volume print.

Small, explicitly synthetic periods exercise transport and identity failures.
One generated source track proves the controller assembles every real reading
and verse before opening print. This test never builds a site or a PDF.
"""
from __future__ import annotations

import functools
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.tests.test_web_print_controller import HARNESS, browser

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/browser-print/volume"
CONTROLLER = ROOT / "src/web/browser/shared/print-volume.js"
sys.path.insert(0, str(ROOT / "scripts"))


class TextContent(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.feed(content)

    def handle_data(self, data):
        self.parts.append(data)

    @property
    def normalized(self):
        return " ".join("".join(self.parts).split())


def wrap(body):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Volume test</title></head><body><main>' + body + '</main></body></html>'


def action(expression, name=None):
    return {"do": "eval", "expression": expression, **({"name": name} if name else {})}


def wait(expression):
    return {"do": "wait", "until": expression}


def drive(plan):
    if not shutil.which("node"):
        raise unittest.SkipTest("node is not installed")
    if not CONTROLLER.is_file():
        raise AssertionError("the complete-volume controller is missing")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    plan["responses"] = {"shared/print-volume.js": CONTROLLER.read_text(),
                         **plan.get("responses", {})}
    harness = HARNESS.replace("join(tmpdir(), 'triptych-truthfulness-')",
                              "join(ROOT, '.scratch/browser-print/volume/chrome-')")
    harness = harness.replace("JSON.parse(process.argv[3])",
                              "JSON.parse(await readFile(process.argv[3], 'utf8'))")
    harness = harness.replace("} else if (act.do === 'eval') {", """} else if (act.do === 'media') {
        await cdp.send('Emulation.setEmulatedMedia', {media: act.media});
      } else if (act.do === 'eval') {""")
    harness = harness.replace("} else if (act.do === 'media') {", """} else if (act.do === 'scripts') {
        await cdp.send('Emulation.setScriptExecutionDisabled', {value: !act.enabled});
      } else if (act.do === 'media') {""")
    with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
        script = Path(directory) / "harness.mjs"
        script.write_text(harness)
        instructions = Path(directory) / "plan.json"
        instructions.write_text(json.dumps(plan))
        result = subprocess.run(["node", str(script), str(ROOT), str(instructions), browser()],
                                text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


PRINT_STUB = """window.printCalls = 0; window.print = () => {
  window.dispatchEvent(new Event('beforeprint'));
  window.printCalls++;
  const root = document.querySelector('[data-print-volume]');
  const content = root.querySelector('[data-print-volume-content]');
  window.printSnapshot = {
    ready: root.getAttribute('data-print-volume-ready'),
    periods: [...root.querySelectorAll('[data-volume-period]')].map(n => n.getAttribute('data-volume-period')),
    readings: [...root.querySelectorAll('[id^="reading-"]')].map(n => n.id),
    verses: root.querySelectorAll('.verse').length,
    text: content.textContent,
    url: location.href
  };
  window.dispatchEvent(new Event('afterprint'));
};"""


def fixture():
    """Twelve two-reading periods using the production controller's schema."""
    volume = "synthetic-complete-volume"
    source_digest = hashlib.sha256(b"Explicit synthetic source edition").hexdigest()
    links, responses = [], {}
    for index in range(1, 13):
        key = f"p{index:02d}"
        ids = [str(index * 2 - 1), str(index * 2)]
        body = f'<section data-volume-id="{volume}" data-volume-period="{key}" data-volume-digest="{source_digest}"><h2>Fixture period {index}</h2>'
        for reading in ids:
            body += (f'<section id="reading-{reading}"><h3>Fixture reading {reading}</h3>'
                     f'<p class="bible-paragraph"><span class="verse"><sup class="verse-number">1</sup> '
                     f'Complete source body {reading}, τέλος.</span></p></section>')
        body += '</section>'
        digest = hashlib.sha256(TextContent(body).normalized.encode()).hexdigest()
        path = f"{volume}/period-{key}.html"
        links.append(f'<li><a data-print-volume-part="{key}" data-reading-ids="{" ".join(ids)}" '
                     f'data-verse-count="2" data-content-sha256="{digest}" href="{path}">Period {index}</a></li>')
        responses["reading-plans/" + path] = wrap(body)
    root = (f'<article data-print-volume="{volume}" data-print-volume-digest="{source_digest}"><header><h1>Synthetic complete volume</h1></header>'
            '<nav><ol>' + ''.join(links) + '</ol></nav>'
            '<button data-print-volume-start type="button">Print complete volume</button>'
            '<button data-print-volume-cancel type="button" hidden>Cancel</button>'
            '<p data-print-volume-status role="status"></p><p data-print-volume-notice>Use Print complete volume to load every period.</p>'
            '<div data-print-volume-content><p>Complete synthetic introduction.</p><div data-print-volume-periods></div>'
            '<footer class="source-apparatus">Source rights and qualified edition remain here.</footer></div>'
            '</article><script src="../shared/print-volume.js"></script>')
    responses[f"reading-plans/{volume}.html"] = wrap(root)
    return volume, responses


def plan_for(volume, responses):
    return {"responses": responses, "acts": [
        {"do": "navigate", "url": f"/reading-plans/{volume}.html"},
        wait("document.querySelector('[data-print-volume-start]') && document.readyState === 'complete'"),
        action(PRINT_STUB),
        action("window.originalUrl = location.href; document.querySelector('[data-print-volume-start]').click()"),
        wait("!document.querySelector('[data-print-volume-start]').disabled"),
        action("({calls: printCalls, snapshot: window.printSnapshot, ready: document.querySelector('[data-print-volume]').getAttribute('data-print-volume-ready'), parts: document.querySelectorAll('[data-print-volume-periods] [data-volume-period]').length, status: document.querySelector('[data-print-volume-status]').textContent, url: location.href, originalUrl, fetched: performance.getEntriesByType('resource').map(n => n.name).filter(n => n.includes('/period-'))})", "result")
    ]}


class VolumePrintTests(unittest.TestCase):
    def test_print_query_uses_the_same_complete_guarded_path_without_a_second_click(self):
        for missing in [False, True]:
            with self.subTest(missing=missing):
                volume,responses=fixture()
                route=f"reading-plans/{volume}.html"
                responses[route]=responses[route].replace('<script src="../shared/print-volume.js">','<script>'+PRINT_STUB+'</script><script src="../shared/print-volume.js">')
                if missing:del responses[f"reading-plans/{volume}/period-p07.html"]
                plan={"responses":responses,"acts":[
                    {"do":"navigate","url":f"/reading-plans/{volume}.html?print=1"},
                    wait("window.printCalls===1 || document.querySelector('[data-print-volume-status]')?.textContent.startsWith('Print unavailable:')"),
                    action("({calls:printCalls,snapshot:window.printSnapshot,ready:document.querySelector('[data-print-volume]').dataset.printVolumeReady,parts:document.querySelector('[data-print-volume-periods]').children.length})","result")
                ]}
                result=drive(plan)["result"]
                self.assertEqual(result["calls"],int(not missing),result)
                self.assertEqual(result["ready"],str(not missing).lower())
                if not missing:
                    self.assertEqual(result["parts"],12)
                    self.assertEqual(len(result["snapshot"]["readings"]),24)
                    self.assertTrue(result["snapshot"]["url"].endswith("?print=1"))
                else:self.assertEqual(result["parts"],0)

    def test_all_twelve_periods_and_every_source_row_are_present_before_print(self):
        volume, responses = fixture()
        seen = drive(plan_for(volume, responses))["result"]
        self.assertEqual(seen["calls"], 1)
        self.assertEqual(seen["snapshot"]["ready"], "true")
        self.assertEqual(seen["snapshot"]["periods"], [f"p{n:02d}" for n in range(1, 13)])
        self.assertEqual(seen["snapshot"]["readings"], [f"reading-{n}" for n in range(1, 25)])
        self.assertEqual(seen["snapshot"]["verses"], 24)
        self.assertEqual(len(seen["fetched"]), 12)
        self.assertEqual(seen["url"], seen["originalUrl"])
        self.assertIn("Complete source body 24", seen["snapshot"]["text"])
        self.assertIn("Source rights and qualified edition", seen["snapshot"]["text"])

    def test_missing_part_never_prints_a_partial_volume(self):
        volume, responses = fixture()
        del responses[f"reading-plans/{volume}/period-p07.html"]
        seen = drive(plan_for(volume, responses))["result"]
        self.assertEqual(seen["calls"], 0)
        self.assertNotEqual(seen["ready"], "true")
        self.assertEqual(seen["parts"], 0)
        self.assertTrue(seen["status"])

    def test_duplicate_wrong_order_and_changed_content_parts_are_refused(self):
        for mutation in ("missing-section", "duplicate-sections", "duplicate-period", "duplicate-reading",
                         "wrong-order", "changed-body", "wrong-source-digest"):
            with self.subTest(mutation=mutation):
                volume, responses = fixture()
                path = f"reading-plans/{volume}/period-p07.html"
                if mutation == "missing-section":
                    responses[path] = wrap('<p>The expected section is absent.</p>')
                elif mutation == "duplicate-sections":
                    responses[path] += responses[path]
                elif mutation == "duplicate-period":
                    responses[path] = responses[path].replace('data-volume-period="p07"', 'data-volume-period="p06"')
                elif mutation == "duplicate-reading":
                    responses[path] = responses[path].replace('id="reading-14"', 'id="reading-13"')
                elif mutation == "wrong-order":
                    responses[path] = responses[path].replace('reading-13', 'reading-TEMP').replace('reading-14', 'reading-13').replace('reading-TEMP', 'reading-14')
                elif mutation == "changed-body":
                    responses[path] = responses[path].replace('Complete source body 14', 'Changed source body 14')
                else:
                    responses[path] = re.sub(r'data-volume-digest="[a-f0-9]{64}"',
                                             'data-volume-digest="' + '0' * 64 + '"', responses[path])
                seen = drive(plan_for(volume, responses))["result"]
                self.assertEqual(seen["calls"], 0)
                self.assertNotEqual(seen["ready"], "true")
                self.assertEqual(seen["parts"], 0)
                self.assertTrue(seen["status"])

    def test_cancel_and_url_change_during_loading_refuse_the_old_selection(self):
        for interruption in ("cancel", "url"):
            with self.subTest(interruption=interruption):
                volume, responses = fixture()
                plan = plan_for(volume, responses)
                plan["delays"] = [{"match": "period-p07.html", "ms": 300}]
                expression = ("document.querySelector('[data-print-volume-cancel]').click()"
                              if interruption == "cancel" else "location.hash = '#another-selection'")
                plan["acts"].insert(4, wait("document.querySelectorAll('[data-print-volume-periods] [data-volume-period]').length === 6"))
                plan["acts"].insert(5, action(expression))
                plan["acts"].insert(7, {"do": "sleep", "ms": 400})
                seen = drive(plan)["result"]
                self.assertEqual(seen["calls"], 0)
                self.assertNotEqual(seen["ready"], "true")
                self.assertEqual(seen["parts"], 0)

    def test_unchanged_text_cannot_hide_a_period_or_reading_from_the_print_copy(self):
        # These changes preserve every textContent byte, reading id and verse
        # count. A text hash alone therefore cannot establish a complete copy.
        changes = {
            "hidden-period": ('<section data-volume-id=', '<section hidden data-volume-id='),
            "styled-period": ('<section data-volume-id=', '<section style="display:none" data-volume-id='),
            "hidden-reading": ('<section id="reading-13"', '<section hidden id="reading-13"'),
            "styled-verse": ('<span class="verse"', '<span style="visibility:hidden" class="verse"'),
            "hidden-class": ('<span class="verse"', '<span class="visually-hidden"'),
            "aria-hidden": ('<section data-volume-id=', '<section aria-hidden="true" data-volume-id='),
            "inert": ('<section data-volume-id=', '<section inert data-volume-id='),
            "popover": ('<section data-volume-id=', '<section popover="manual" data-volume-id='),
            "print-control-marker": ('<section data-volume-id=', '<section data-print-volume-controls data-volume-id='),
        }
        for mutation in [*changes, "closed-details", "closed-dialog"]:
            with self.subTest(mutation=mutation):
                volume, responses = fixture()
                path = f"reading-plans/{volume}/period-p07.html"
                original = responses[path]
                if mutation in changes:
                    before, after = changes[mutation]
                    responses[path] = original.replace(before, after, 1)
                else:
                    tag = "details" if mutation == "closed-details" else "dialog"
                    responses[path] = original.replace('<section id="reading-13"',
                                                       '<' + tag + '><section id="reading-13"', 1)
                    responses[path] = responses[path].replace('</section>', '</section></' + tag + '>', 1)
                self.assertEqual(TextContent(original).normalized,
                                 TextContent(responses[path]).normalized)
                seen = drive(plan_for(volume, responses))["result"]
                self.assertEqual(seen["calls"], 0)
                self.assertNotEqual(seen["ready"], "true")
                self.assertEqual(seen["parts"], 0)
                self.assertIn("unexpected markup", seen["status"])

    def test_beforeprint_rechecks_visibility_after_a_complete_volume_was_prepared(self):
        for mutation in ("hidden-period", "styled-verse", "closed-details"):
            with self.subTest(mutation=mutation):
                volume, responses = fixture()
                plan = plan_for(volume, responses)
                change = {
                    "hidden-period": "part.hidden = true",
                    "styled-verse": "part.querySelector('.verse').style.visibility = 'hidden'",
                    "closed-details": "const holder = document.createElement('details'); const reading = part.querySelector('section'); reading.before(holder); holder.appendChild(reading)",
                }[mutation]
                plan["acts"] += [action("""const root = document.querySelector('[data-print-volume]');
                    const part = root.querySelector('[data-volume-period="p07"]');
                    window.wasReady = root.getAttribute('data-print-volume-ready');
                    window.originalPartText = part.textContent; """ + change + ";" + """
                    window.dispatchEvent(new Event('beforeprint'));
                    ({wasReady, ready: root.getAttribute('data-print-volume-ready'),
                      sameText: originalPartText === part.textContent,
                      status: root.querySelector('[data-print-volume-status]').textContent,
                      calls: printCalls})""", "afterMutation")]
                seen = drive(plan)["afterMutation"]
                self.assertEqual(seen["wasReady"], "true")
                self.assertTrue(seen["sameText"])
                self.assertEqual(seen["ready"], "false")
                self.assertEqual(seen["calls"], 1)
                self.assertIn("Print complete volume", seen["status"])


@functools.lru_cache(maxsize=1)
def generated_track():
    """Generate one selected real track; no publication/site build is involved."""
    import _print_catalog as catalog
    typesetter = catalog._bible_typesetter()
    selected = ("full-account", "douay-rheims")
    original = typesetter.volumes
    with patch.object(typesetter, "volumes", side_effect=lambda plan: [pair for pair in original(plan) if pair == selected]):
        pages = catalog._reading_plan_pages(ROOT)
    plans = list(typesetter.plans(ROOT / "src/sources/reading-plans"))
    if len(plans) != 1:
        raise AssertionError("this complete-volume fixture requires the canonical narrative plan")
    volume = typesetter.Volume(plans[0], *selected, ROOT / "src/sources/works")
    return pages, volume


class GeneratedTrackPrintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages, cls.volume = generated_track()
        cls.route = f"reading-plans/{cls.volume.id}.html"
        cls.responses = {route: wrap(page["html"]) for route, page in cls.pages.items()}

    def test_real_full_account_print_contains_all_357_readings_and_13867_verses(self):
        page = self.pages[self.route]
        self.assertEqual(len(page["part_routes"]), 12)
        self.assertTrue(all(len(self.responses[route].encode()) < 1_000_000 for route in self.responses))
        self.assertTrue(all(not path.endswith(".pdf") for path in page["source_paths"]))
        seen = drive(plan_for(self.volume.id, dict(self.responses)))["result"]
        self.assertEqual(seen["calls"], 1)
        snapshot = seen["snapshot"]
        expected_readings = [f'reading-{reading["order"]}'
                             for _, readings in self.volume.periods for reading in readings]
        expected_verses = sum(len(reading["verses"])
                              for _, readings in self.volume.periods for reading in readings)
        self.assertEqual(snapshot["readings"], expected_readings)
        self.assertEqual(len(snapshot["readings"]), 357)
        self.assertEqual(snapshot["verses"], expected_verses)
        self.assertEqual(snapshot["verses"], 13_867)
        self.assertEqual(snapshot["periods"], [period["key"] for period, _ in self.volume.periods])
        self.assertEqual(len(seen["fetched"]), 12)
        self.assertEqual(seen["url"], seen["originalUrl"])
        normalized = " ".join(snapshot["text"].split())
        self.assertIn(" ".join(self.volume.edition.rights["basis"].split()), normalized)
        self.assertIn("Source text retains its own rights", normalized)

    def test_native_premature_print_shows_notice_and_hides_incomplete_content(self):
        plan = plan_for(self.volume.id, dict(self.responses))
        plan["acts"] = plan["acts"][:3] + [
            {"do": "media", "media": "print"},
            action("window.dispatchEvent(new Event('beforeprint')); ({ready: document.querySelector('[data-print-volume]').getAttribute('data-print-volume-ready'), contentDisplay: getComputedStyle(document.querySelector('[data-print-volume-content]')).display, noticeDisplay: getComputedStyle(document.querySelector('[data-print-volume-notice]')).display, calls: printCalls, fetched: performance.getEntriesByType('resource').filter(n => n.name.includes('/period-')).length})", "result")
        ]
        seen = drive(plan)["result"]
        self.assertEqual(seen["ready"], "false")
        self.assertEqual(seen["contentDisplay"], "none")
        self.assertNotEqual(seen["noticeDisplay"], "none")
        self.assertEqual(seen["calls"], 0)
        self.assertEqual(seen["fetched"], 0)

    def test_no_javascript_keeps_twelve_bounded_section_links(self):
        plan = {"responses": dict(self.responses), "acts": [
            {"do": "scripts", "enabled": False},
            {"do": "navigate", "url": "/" + self.route},
            wait("document.readyState === 'complete'"),
            action("({links: [...document.querySelectorAll('[data-print-volume-part]')].map(a => a.getAttribute('href')), printHidden: document.querySelector('[data-print-volume-start]').hidden, readings: document.querySelectorAll('[id^=reading-]').length})", "result")
        ]}
        seen = drive(plan)["result"]
        self.assertEqual(len(seen["links"]), 12)
        self.assertEqual(seen["links"], [route.removeprefix('reading-plans/') for route in self.pages[self.route]["part_routes"]])
        self.assertTrue(seen["printHidden"])
        self.assertEqual(seen["readings"], 0)


if __name__ == "__main__":
    unittest.main()
