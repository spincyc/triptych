"""A declared reception is an interchange; an ordinary parent is not.

Drive the actual history page with the existing Chromium harness and the
generator's constructed reception fixture. The fixture asserts no historical
event. It tests the supported projection, including evidence loaded lazily.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.tests import test_act_history_reception as reception
from tools.tests import test_browser_truthfulness as browser


ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/map-recovery"


def drive(plan: dict) -> dict:
    """Reuse the page harness, adding raw CDP for viewport, keys, and AX proof."""
    if shutil.which("node") is None:
        raise unittest.SkipTest("node is not installed")
    chrome = browser.browser()
    marker = "      } else {\n        throw new Error('unknown act: ' + act.do);"
    assert browser.HARNESS.count(marker) == 1
    harness = browser.HARNESS.replace(marker, """      } else if (act.do === 'cdp') {
        const result = await cdp.send(act.method, act.params || {});
        if (act.name) seen[act.name] = result;
""" + marker)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
        script = Path(temporary) / "harness.mjs"
        script.write_text(harness, encoding="utf-8")
        result = subprocess.run(
            ["node", str(script), str(ROOT), json.dumps(plan), chrome],
            cwd=ROOT, env={**os.environ, "TMPDIR": temporary},
            capture_output=True, text=True, timeout=300,
        )
    if result.returncode:
        raise AssertionError(result.stderr or "browser harness failed silently")
    return json.loads(result.stdout)


class HistoryReceptionBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        browser.browser()
        SCRATCH.mkdir(parents=True, exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        cls.addClassCleanup(cls.temporary.cleanup)
        directory = Path(cls.temporary.name)
        source = directory / "constructed-reception.toml"
        source.write_text(reception.HOLY_WEEK.read_text(encoding="utf-8") +
                          reception.FIXTURE.format(
                              receiving=reception.RECEIVING,
                              parents=json.dumps(["vernacular-first-1965", reception.RECEIVED]),
                              act_citation="cited-externally", extra="",
                              receptions=reception.RECEPTION.format(
                                  source=reception.RECEIVED,
                                  kind="translates-typical-edition")), encoding="utf-8")
        output = directory / "data"
        generated = reception.run("structure", "--source", str(source), "--out", str(output))
        if generated.returncode:
            raise AssertionError(generated.stdout + generated.stderr)
        cls.spine = json.loads((output / "structure/act-history/roman-holy-week.json").read_text())
        cls.receiving = next(row for row in cls.spine["stations"] if row["id"] == reception.RECEIVING)
        cls.edges = json.loads((output / "structure/act-history" /
                               cls.receiving["station_path"]).read_text())["edges"]
        cls.url = ("/src/web/browser/history/index.html?data=/" +
                   output.relative_to(ROOT).as_posix() +
                   "&slice=roman-holy-week#station=" + reception.RECEIVING)

    def test_reception_evidence_and_ordinary_parent_remain_distinct(self):
        seen = drive({"acts": [
            {"do": "navigate", "url": self.url},
            {"do": "wait", "until": "document.querySelector('#detail .detail-changes .detail-summary')"},
            {"do": "eval", "name": "map", "expression": """({
              tracks: [...document.querySelectorAll('path.track')].map(p => ({
                from: p.dataset.from, to: p.dataset.to,
                reception: p.classList.contains('track-reception'),
                width: getComputedStyle(p).strokeWidth, label: p.getAttribute('aria-label')
              })),
              rings: [...document.querySelectorAll('.station-interchange')].map(p => p.dataset.station),
              legend: document.getElementById('legend').textContent,
              evidence: document.querySelector('.detail-receptions').textContent,
              coverage: document.querySelector('header').textContent
            })"""},
            {"do": "cdp", "method": "Accessibility.getFullAXTree", "name": "ax"},
            {"do": "eval", "expression": "document.querySelector('.station[data-station=\"editio-typica-1962\"]').dispatchEvent(new Event('click')); document.querySelector('.station-interchange').focus()"},
            {"do": "cdp", "method": "Input.dispatchKeyEvent", "params": {
                "type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13}},
            {"do": "eval", "name": "hash", "expression": "location.hash"},
            {"do": "eval", "expression": "document.querySelector('.detail-receptions button').click()"},
            {"do": "wait", "until": "location.hash.includes('station=editio-typica-1962')"},
            {"do": "eval", "name": "parent", "expression": "({title: document.querySelector('.detail-title').textContent, reception: !!document.querySelector('.detail-receptions')})"},
        ]})
        tracks = seen["map"]["tracks"]
        expected_edges = sum(len(row["parents"]) for row in self.spine["stations"])
        self.assertEqual(len(tracks), expected_edges, "no invented or missing parent edges")
        received = [row for row in tracks if row["reception"]]
        self.assertEqual([(row["from"], row["to"]) for row in received],
                         [(reception.RECEIVED, reception.RECEIVING)])
        own_parent = next(row for row in tracks if row["to"] == reception.RECEIVING and not row["reception"])
        self.assertNotEqual(received[0]["width"], own_parent["width"])
        self.assertIn("Documented reception", received[0]["label"])
        self.assertEqual(seen["map"]["rings"], [reception.RECEIVING])
        self.assertIn("double-ring", seen["map"]["legend"])
        self.assertIn("asserts no connection", seen["map"]["legend"])
        for field in ("instrument", "citation", "basis"):
            self.assertIn(self.edges["receptions"][0][field], seen["map"]["evidence"])
        self.assertIn("ancestry, not a copy", seen["map"]["evidence"])
        self.assertIn("Text coverage is partial", seen["map"]["coverage"])
        buttons = [node for node in seen["ax"]["nodes"]
                   if not node.get("ignored") and node.get("role", {}).get("value") == "button"]
        self.assertTrue(any("documented reception from" in node.get("name", {}).get("value", "")
                            for node in buttons), "the station must be exposed as an accessible button")
        self.assertIn(reception.RECEIVING, seen["hash"])
        self.assertFalse(seen["parent"]["reception"])
        self.assertEqual(seen["parent"]["title"], next(row["title"] for row in self.spine["stations"]
                                                          if row["id"] == reception.RECEIVED))

    def test_desktop_narrow_and_forced_colors_preserve_map_and_evidence(self):
        actions = [{"do": "navigate", "url": self.url},
                   {"do": "wait", "until": "document.querySelector('#detail .detail-changes .detail-summary')"}]
        for width in (1440, 320):
            actions.extend([
                {"do": "cdp", "method": "Emulation.setDeviceMetricsOverride", "params": {
                    "width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False}},
                {"do": "eval", "name": str(width), "expression": """({
                  viewport: innerWidth, page: document.documentElement.scrollWidth,
                  labels: [...document.querySelectorAll('.route-title-text')].map(n => n.textContent),
                  direction: document.getElementById('map').textContent.includes('Read dates downward within each line'),
                  panels: document.querySelectorAll('.route-panel').length,
                  evidence: document.querySelector('.detail-receptions').getBoundingClientRect().width
                })"""},
            ])
        actions.extend([
            {"do": "cdp", "method": "Emulation.setEmulatedMedia", "params": {
                "features": [{"name": "forced-colors", "value": "active"}]}},
            {"do": "eval", "name": "colors", "expression": """({
              outer: getComputedStyle(document.querySelector('.track-reception')).stroke,
              inner: getComputedStyle(document.querySelector('.track-reception-core')).stroke
            })"""},
        ])
        seen = drive({"acts": actions})
        for width in (1440, 320):
            self.assertLessEqual(seen[str(width)]["page"], width + 1)
            self.assertEqual(set(seen[str(width)]["labels"]), {row["title"] for row in self.spine["stations"]})
            self.assertTrue(seen[str(width)]["direction"])
            self.assertEqual(seen[str(width)]["panels"], len({row["line"] for row in self.spine["stations"]}))
            self.assertGreater(seen[str(width)]["evidence"], 0)
        self.assertNotEqual(seen["colors"]["outer"], seen["colors"]["inner"])

    def test_tracked_slice_does_not_invent_a_reception(self):
        seen = drive({"acts": [
            {"do": "navigate", "url": browser.page("history", "slice=latin-missal")},
            {"do": "wait", "until": "document.querySelector('.station')"},
            {"do": "eval", "name": "receptions", "expression": "document.querySelectorAll('.track-reception').length"},
        ]})
        data = browser.spine("latin-missal")
        self.assertEqual(seen["receptions"], sum(len(row.get("receptions", [])) for row in data["stations"]))


if __name__ == "__main__":
    unittest.main()
