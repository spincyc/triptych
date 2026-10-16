"""A printable preview cannot silently lose isolated stations or invent joins."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from scripts import _act_history_preview as preview
from tools.tests import test_act_history_reception as reception


ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/map-renderer"
BROWSER = ROOT / "src/web/browser/history/history.js"
NS = {"s": preview.NS}


class ActHistoryPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in ("node", "rsvg-convert", "pdfunite"):
            try:
                preview.executable(name)
            except preview.PreviewError as error:
                raise unittest.SkipTest(str(error)) from error
        SCRATCH.mkdir(parents=True, exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.tool = reception.load_tool()
        data = cls.tool.load(reception.MISSAL)
        cls.plate = Path(cls.tool.plate(data, cls.root / "plate")["written"])
        cls.spine = json.loads(Path(cls.tool.structure(data, cls.root / "data")["written"]).read_text())
        cls.output = cls.root / "preview"
        cls.audit = preview.render_preview(plate_path=cls.plate, spine=cls.spine,
                                          out_dir=cls.output, browser_source=BROWSER,
                                          catalogue={"records": [{"id": "unaccepted-candidate"}]})
        cls.svg = ET.parse(cls.output / "latin-missal-preview.svg").getroot()

    def test_every_station_parent_and_isolated_root_survives(self):
        expected_ids = {s["id"] for s in self.spine["stations"]}
        expected_edges = {(p, s["id"]) for s in self.spine["stations"] for p in s["parents"]}
        marks = self.svg.findall('.//s:g[@data-station]', NS)
        paths = self.svg.findall('.//s:path[@data-from]', NS)
        self.assertEqual({m.get("data-station") for m in marks}, expected_ids)
        self.assertEqual(len(marks), len(expected_ids))
        self.assertEqual({(p.get("data-from"), p.get("data-to")) for p in paths}, expected_edges)
        self.assertEqual(len(paths), len(expected_edges))
        isolated = expected_ids - {s for pair in expected_edges for s in pair}
        self.assertEqual(len(isolated), 4, "the fixture must continue exercising the observed LOOM loss")
        self.assertEqual(self.audit["isolated_count"], len(isolated))
        self.assertNotIn("unaccepted-candidate", ET.tostring(self.svg, encoding="unicode"))
        self.assertEqual(self.audit["status"], "review-preview")
        self.assertEqual(self.audit["renderer"], "existing-browser-geometry")

    def test_printed_stations_and_partial_coverage_remain_explicit(self):
        marks = {m.get("data-station"): m for m in self.svg.findall('.//s:g[@data-station]', NS)}
        for station in self.spine["stations"]:
            circle = marks[station["id"]].find('s:circle', NS)
            self.assertEqual(circle.get("fill") == "white", station["station_kind"] == "printed")
        words = " ".join(self.svg.itertext())
        for phrase in ("recorded lines", "graph steps, not years", "parent-link evidence", "Text coverage is partial"):
            self.assertIn(phrase, words)
        self.assertNotIn("17 traditions", words)
        self.assertEqual(self.audit["reception_count"], 0)

    def test_catalogue_pdf_has_every_station_identifier(self):
        try:
            extractor = preview.executable("pdftotext")
        except preview.PreviewError as error:
            self.skipTest(str(error))
        result = preview.run([extractor, "-layout", str(self.output / "latin-missal-catalogue.pdf"), "-"])
        for station in self.spine["stations"]:
            self.assertIn(station["id"], result.stdout)
        self.assertTrue((self.output / "latin-missal-preview.pdf").read_bytes().startswith(b"%PDF"))

    def test_missing_isolated_station_is_a_refusal_not_a_smaller_map(self):
        changed = copy.deepcopy(self.spine)
        changed["stations"] = [s for s in changed["stations"] if s["id"] != "lugdunense-1503"]
        with self.assertRaisesRegex(preview.PreviewError, "same stations and parent links"):
            preview.render_preview(plate_path=self.plate, spine=changed,
                                   out_dir=self.root / "bad", browser_source=BROWSER)
        self.assertFalse((self.root / "bad").exists())

    def test_browser_extraction_contract_change_refuses(self):
        changed = self.root / "changed-browser.js"
        changed.write_text(BROWSER.read_text().replace("  function connector(from, to) {",
                                                      "  function connectorRenamed(from, to) {"))
        with self.assertRaisesRegex(preview.PreviewError, "extraction contract changed"):
            preview.browser_geometry(self.spine, changed)

    def test_stale_station_metadata_is_refused(self):
        changed = copy.deepcopy(self.spine)
        changed["stations"][0]["date"] = "1490"
        with self.assertRaisesRegex(preview.PreviewError, "station metadata disagree"):
            preview.render_preview(plate_path=self.plate, spine=changed,
                                   out_dir=self.root / "stale", browser_source=BROWSER)

    def test_same_inputs_repeat_the_same_svg(self):
        output = self.root / "repeat"
        preview.render_preview(plate_path=self.plate, spine=self.spine,
                               out_dir=output, browser_source=BROWSER)
        self.assertEqual((output / "latin-missal-preview.svg").read_bytes(),
                         (self.output / "latin-missal-preview.svg").read_bytes())

    def test_declared_reception_gets_band_ring_and_evidence(self):
        source = self.root / "constructed.toml"
        source.write_text(reception.HOLY_WEEK.read_text() + reception.FIXTURE.format(
            receiving=reception.RECEIVING, parents=json.dumps(["vernacular-first-1965", reception.RECEIVED]),
            act_citation="cited-externally", extra="", receptions=reception.RECEPTION.format(
                source=reception.RECEIVED, kind="translates-typical-edition")))
        data = self.tool.load(source)
        plate = Path(self.tool.plate(data, self.root / "fixture-plate")["written"])
        spine = json.loads(Path(self.tool.structure(data, self.root / "fixture-data")["written"]).read_text())
        output = self.root / "reception-preview"
        audit = preview.render_preview(plate_path=plate, spine=spine, out_dir=output, browser_source=BROWSER)
        svg = ET.parse(output / "roman-holy-week-preview.svg").getroot()
        received = svg.findall('.//s:path[@data-reception="true"]', NS)
        self.assertEqual([(p.get("data-from"), p.get("data-to")) for p in received],
                         [(reception.RECEIVED, reception.RECEIVING)])
        self.assertEqual(len(svg.findall('.//s:circle[@data-interchange="true"]', NS)), 1)
        ordinary = svg.find('.//s:path[@data-from="vernacular-first-1965"]', NS)
        self.assertEqual(ordinary.get("data-reception"), "false")
        self.assertNotEqual(ordinary.get("stroke-width"), received[0].get("stroke-width"))
        pages = output / "roman-holy-week-preview-parts"
        evidence = " ".join(" ".join(ET.parse(p).getroot().itertext()) for p in pages.glob("catalogue-*.svg"))
        self.assertIn("A constructed decree of the receiving conference", evidence)
        self.assertIn("which is not a source", evidence)
        self.assertEqual(audit["reception_count"], 1)


if __name__ == "__main__":
    unittest.main()
